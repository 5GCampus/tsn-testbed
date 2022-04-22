from numpy import polyfit, poly1d, sum, \
 linspace, arange, hstack, histogram, ones
from math import floor
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from matplotlib.ticker import PercentFormatter
import seaborn as sns
from pathlib import Path
from csv import writer
from pandas import concat, to_numeric, options, DataFrame
from sys import exit
options.mode.chained_assignment = None


class TsnCreatePlot():
    """This class visualizes the parsed DataFrame data."""

    def __init__(self, dfs, output_path, mapping,
                 bg_load, bg_framesize, qos_type):
        self.dfs = dfs
        self.csv_path = "{}/csv".format(output_path)
        self.plot_path = "{}/plot".format(output_path)
        self.check_create_path()
        self.mapping = mapping
        self.bg_load = bg_load
        self.bg_framesize = bg_framesize
        self.qos_type = qos_type
        self.cycle_resolution = 1e-6

        self.grid_params_major = dict(visible=True,
                                      which='major',
                                      color='lightgrey',
                                      linestyle='-')
        self.grid_params_minor = dict(visible=True,
                                      which='minor',
                                      color='lightgrey',
                                      linestyle='--')
        self.savefig_params = dict(dpi=300,
                                   transparent=False,
                                   facecolor='white',
                                   edgecolor='none')
        self.title_params_left = dict(loc='left',
                                      fontsize=18)
        self.title_params_right = dict(loc='right',
                                       fontsize=13,
                                       color='grey')
        self.text_losses_params = dict(x=1,
                                       y=1,
                                       s='LOSSES',
                                       fontsize=40,
                                       color='red',
                                       ha='right',
                                       va='top')
        self.file_format = ["pdf", "png"]

    def set_style(self):
        sns.set_theme()
        plt.rcParams.update({
            'font.family': 'serif',
            'font.size': 11,
            'text.usetex': True,
            'axes.facecolor': 'white',
            'axes.edgecolor': 'lightgrey',
            'agg.path.chunksize': 10000
        })

        SIZE = 14
        plt.rc('font', size=SIZE)         # controls default text sizes
        plt.rc('axes', titlesize=SIZE)    # fontsize of the axes title
        plt.rc('axes', labelsize=SIZE)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=SIZE)   # fontsize of the tick labels
        plt.rc('ytick', labelsize=SIZE)   # fontsize of the tick labels
        plt.rc('legend', fontsize=SIZE)   # legend fontsize

    def check_create_path(self):
        # create path if it does not exists:
        Path(self.csv_path).mkdir(parents=True, exist_ok=True)
        Path(self.plot_path).mkdir(parents=True, exist_ok=True)
        return

    def export_over_time_to_csv(self, stream, plot_type, x, y,
                                x_poly=None, y_poly=None):
        # x, y to csv:
        out_df = concat([x, y], axis=1)
        file = "{}/{}_{}.csv".format(self.csv_path, plot_type, stream)
        out_df.to_csv(file, index=False, header=True)

        if x_poly is not None:
            # x_poly, model(x_poly) to csv:
            file = "{}/{}_{}_poly.csv".format(self.csv_path, plot_type, stream)
            with open(file, 'w', newline='') as f:
                w = writer(f)
                header = ["x_poly", "y_poly"]
                w.writerow(header)
                w.writerows(zip(x_poly, y_poly))

    def export_c_cdf_to_csv(self, stats_dfs, plot_type):
        for m, stats_df in zip(self.mapping.values(), stats_dfs):
            file = "{}/{}_{}.csv".format(self.csv_path, plot_type, m)
            stats_df.to_csv(file, index=False, header=True)

    def generate_plots(self, plot_type, output="mpl", title=True,
                       xlabels=None, src=None, cycle_time=None):
        if type(self.dfs) == list and plot_type == "boxplot":
            self.boxplot(plot_type, title, xlabels, output)

        elif plot_type == "boxplot" and not type(self.dfs) == list:
            print("ERROR - Please provide a list of DataFrames as input!")
            exit(1)

        else:
            lossesInMeasurement = False
            for df, v in zip(self.dfs, self.mapping.values()):
                losses = self.check_loss(df, v)
                if losses:
                    lossesInMeasurement = True

                if plot_type == "latency_over_time":
                    self.latency_over_time(df=df,
                                           stream=v,
                                           losses=losses,
                                           output=output,
                                           plot_type=plot_type,
                                           title=title)
                elif plot_type == "ifg_over_time":
                    self.ifg_over_time(df=df,
                                       stream=v,
                                       losses=losses,
                                       output=output,
                                       plot_type=plot_type,
                                       title=title,
                                       workaround=False)
            if plot_type == "latency_cdf":
                self.cdf(measurement="Latency (ns)",
                         complementary=False,
                         losses=lossesInMeasurement,
                         output=output,
                         plot_type=plot_type,
                         title=title)
            elif plot_type == "latency_ccdf":
                self.cdf(measurement="Latency (ns)",
                         complementary=True,
                         losses=lossesInMeasurement,
                         output=output,
                         plot_type=plot_type,
                         title=title)
            elif plot_type == "ifg_cdf":
                self.cdf(measurement="Inter Frame Gap Receiver (ns)",
                         complementary=False,
                         losses=lossesInMeasurement,
                         output=output,
                         plot_type=plot_type,
                         title=title)
            elif plot_type == "ifg_ccdf":
                self.cdf(measurement="Inter Frame Gap Receiver (ns)",
                         complementary=True,
                         losses=lossesInMeasurement,
                         output=output,
                         plot_type=plot_type,
                         title=title)
            elif plot_type == "cycle_time":
                self.cycle_time(src=src,
                                output=output,
                                title=title,
                                plot_type=plot_type,
                                losses=lossesInMeasurement,
                                cycle_time=cycle_time)

    @classmethod
    def check_loss(self, df, stream):
        offset = 0
        pcap_pkts = None
        for index, row in df.iterrows():
            pcap_index = row['Frame No.'] + offset
            if not index == pcap_index:
                if row['Frame No.'] == 0:
                    if pcap_pkts:
                        offset += pcap_pkts
                    else:
                        offset += index
                        pcap_pkts = index
                else:
                    print("FRAME LOSS DETECTED IN %s STREAM!" % (stream))
                    print("FRAME INDEX FROM PCAP:", pcap_index)
                    print("EXPECTED INDEX IN DATAFRAME:", index)
                    return True
        return False

    def adjR(self, x, y, degree):
        coeffs = polyfit(x, y, degree)
        p = poly1d(coeffs)
        yhat = p(x)
        ybar = sum(y)/len(y)
        ssreg = sum((yhat - ybar)**2)
        sstot = sum((y - ybar)**2)
        return (degree, 1 - (((1 - (ssreg / sstot)) *
                (len(y) - 1)) / (len(y) - degree - 1)))

    def get_best_fit(self, x, y):
        R = []
        for degree in range(1, 6):
            R.append(self.adjR(x, y, degree))
        return max(R, key=lambda item: item[1])[0]

    def latency_over_time(self, df, stream, losses, output, plot_type, title):
        # loss of accuracy below (for x values):
        # numpy`s polyfit cannot work with Decimal()
        x = to_numeric(df['Timestamp Sender (Unix epoch, s)']
                       - floor(df['Timestamp Sender (Unix epoch, s)'].iloc[0]))
        y = to_numeric(df['Latency (ns)'])

        model = poly1d(polyfit(x, y, self.get_best_fit(x, y)))
        x_poly = linspace(x.iloc[0], x.iloc[-1], 100)
        y_poly = model(x_poly)

        if output == "mpl":
            plt.plot(x, y)
            plt.plot(x_poly, y_poly)

            trailer = "-{}B-{}%".format(self.bg_framesize, self.bg_load) \
                      if self.bg_load > 0 else "-No-BG"
            title_right = "{}{}".format(stream.title(), trailer)
            plt.title("Latency over time", **self.title_params_left)
            plt.title(title_right, **self.title_params_right)

            plt.grid(**self.grid_params_major)
            plt.grid(**self.grid_params_minor)
            plt.ylabel("Latency [ns]")
            plt.xlabel("Time [s]")

            if losses:
                ax = plt.gca()
                ax.text(transform=ax.transAxes, **self.text_losses_params)

            plt.tight_layout()
            file = "{}/latency_{}.png".format(self.plot_path, stream)
            plt.savefig(file, **self.savefig_params)
            plt.close('all')

        elif output == "csv":
            self.export_over_time_to_csv(stream, plot_type, x, y,
                                         x_poly, y_poly)

    def ifg_over_time(self, df, stream, losses, output,
                      plot_type, title, workaround=False):
        offset = 0
        if workaround:
            # skip the first 2/6 frames (workaround for loop measurement
            # due to very low/unrealistic values)
            if stream in ['robotic', 'audio']:
                offset = 1
            elif stream == 'video':
                offset = 5

        x = df['Timestamp Receiver (Unix epoch, s)'].loc[
            df['Frame No.'] > offset] - floor(
            df['Timestamp Receiver (Unix epoch, s)'].iloc[0])
        y = df['Inter Frame Gap Receiver (ns)'].loc[df['Frame No.'] > offset]

        if output == "mpl":
            plt.plot(x, y)
            plt.axhline(y=df['Inter Frame Gap Receiver (ns)'].loc[
                        df['Frame No.'] > offset].mean(),
                        linestyle='--',
                        color="black")

            if stream == "audio":
                plt.axhline(y=2e7, linestyle='--', color="green")
            elif stream == "robotic":
                plt.axhline(y=1e6, linestyle='--', color="green")

            trailer = "-{}B-{}%".format(self.bg_framesize, self.bg_load) \
                      if self.bg_load > 0 else "-No-BG"
            title_right = "{}{}".format(stream.title(), trailer)
            plt.title("IFG (Recv) over time", **self.title_params_left)
            plt.title(title_right, **self.title_params_right)
            plt.grid(**self.grid_params_major)
            plt.grid(**self.grid_params_minor)
            plt.ylabel("IFG [ns]")
            plt.xlabel("Time [s]")

            if losses:
                ax = plt.gca()
                ax.text(transform=ax.transAxes, **self.text_losses_params)

            plt.tight_layout()
            file = "{}/ifg_{}.png".format(self.plot_path, stream)
            plt.savefig(file, **self.savefig_params)
            plt.close('all')

        elif output == "csv":
            self.export_over_time_to_csv(stream, plot_type, x, y)

    def cdf(self, measurement, complementary, losses,
            output, plot_type, title):
        pkt_count = []
        stats_dfs = []
        for df in self.dfs:
            s = df.groupby(measurement)[measurement]\
                         .agg('count').pipe(DataFrame)\
                         .rename(columns={measurement: 'frequency'})
            s['pmf'] = s['frequency'] / sum(s['frequency'])
            pkt_count.append(sum(s['frequency']))
            s['cdf'] = s['pmf'].cumsum()
            s['ccdf'] = 1 - s['pmf'].cumsum()
            s.iloc[-1, s.columns.get_loc('ccdf')] = 0
            s = s.reset_index()
            stats_dfs.append(s)

        if output == "mpl":
            linestyles = ['--', '-.', ':']
            colors = [c for c in sns.color_palette()]

            for stats_df, linestyle in zip(stats_dfs, linestyles):
                plt.plot(stats_df[measurement],
                         stats_df['ccdf'],
                         linestyle=linestyle) if complementary \
                    else plt.plot(stats_df[measurement],
                                  stats_df['cdf'],
                                  linestyle=linestyle)

            handles = []
            for m, c, l in zip(self.mapping.values(), colors, linestyles):
                handles.append(mlines.Line2D([], [],
                                             color=c,
                                             linestyle=l,
                                             markersize=15,
                                             label=m.title()))
            plt.legend(handles=handles,
                       loc='upper right')

            if title:
                trailer = "-{}B-{}%".format(self.bg_framesize, self.bg_load) \
                          if self.bg_load > 0 else "-No-BG"
                title_right = "{}{}".format(self.qos_type, trailer)
                plt.title("CCDF: IFG", **self.title_params_left) \
                    if complementary else plt.title("CDF: IFG",
                                                    **self.title_params_left)
                plt.title(title_right, **self.title_params_right)

            plt.grid(**self.grid_params_major)
            plt.grid(**self.grid_params_minor)

            plt.yscale("log")
            plt.xscale("log")
            plt.ylim((3e-5, 1.3))
            if "latency" in plot_type:
                plt.xlim((3e3, 3e6))
            else:
                plt.xlim((7e3, 1e8))

            # set xlabel:
            label = plot_type.split("_")[0]
            if label == "ifg":
                label = label.upper()
            elif label == "latency":
                label = label.title()
            xlabel = "{} [ns]".format(label)
            plt.xlabel(xlabel)
            plt.ylabel("CCDF") if complementary else plt.ylabel("CDF")

            if losses:
                ax = plt.gca()
                ax.text(transform=ax.transAxes, **self.text_losses_params)

            plt.tight_layout()
            for f in self.file_format:
                file = "{}/{}.{}".format(self.plot_path, plot_type, f)
                plt.savefig(file, **self.savefig_params)
            plt.close('all')

        elif output == "csv":
            self.export_c_cdf_to_csv(stats_dfs, plot_type)

    def boxplot(self, plot_type, title, xlabels, output):
        if type(self.dfs) is not list:
            print("ERROR - Please provide a list of DataFrames as input!")
            exit(1)

        if output == "mpl":
            data = []
            for dfs in self.dfs:
                d = []
                for df in dfs:
                    d.append(df['Latency (ns)'].astype(int))
                data.append(d)

            showfliers = True
            notch = True
            sym = 'o'
            markersize = 0.5
            colors = [c for c in sns.color_palette()]
            hatches = ["//", "\\\\", "oo"]

            i = 1
            for measurement in data:
                offset = -0.2
                for stream, c, h in zip(measurement, colors, hatches):
                    plt.boxplot(stream,
                                positions=[i+offset],
                                showfliers=showfliers,
                                sym=sym,
                                patch_artist=True,
                                boxprops=dict(facecolor=c,
                                              hatch=h),
                                notch=notch,
                                flierprops=dict(markersize=markersize))
                    offset += 0.2
                i += 1.5

            xlocs = arange(1, i, 1.5)
            plt.xticks(xlocs, xlabels, rotation=15)

            handles = []
            for m, c, h in zip(self.mapping.values(), colors, hatches):
                handles.append(mpatches.Patch(facecolor=c,
                                              label=m.title(),
                                              hatch=h,
                                              edgecolor='black'))
            plt.legend(handles=handles,
                       loc='upper left')

            plt.title("Boxplot", **self.title_params_left)
            plt.title("BG Framesize: {}B".format(self.bg_framesize),
                      **self.title_params_right)

            plt.ylabel('Latency [ns]')
            plt.yscale('log')
            plt.grid(**self.grid_params_major)
            plt.grid(**self.grid_params_minor)
            plt.tight_layout()

            for f in self.file_format:
                file = "{}/{}.{}".format(self.plot_path, plot_type, f)
                plt.savefig(file, **self.savefig_params)
            plt.close('all')
        else:
            print("ERROR - There is no other output "
                  "method as mpl currently defined.")
            exit(1)

    def cycle_time(self, src, output, title,
                   plot_type, losses, cycle_time):
        if output == "mpl":
            colors = [c for c in sns.color_palette()]
            x_max = cycle_time * 1e6
            measurement = '{} Cycle Time (us)'.format(src)

            # Combined histogram of all streams:
            data = ()
            weights = []
            bins = []
            for df in self.dfs:
                x = df[measurement]
                data += (x,)
                weights.append(ones(len(x)) / len(x))
                bins.append(histogram(hstack(x), bins=100)[1])

            bins_combined = histogram(hstack(data), bins=100)[1]

            for d, w, m, c in zip(data, weights,
                                  self.mapping.values(), colors):
                plt.hist(x=d,
                         bins=bins_combined,
                         weights=w,
                         label=m,
                         color=c)

            if title:
                title_right = "Cycle: {:.0e}s, " \
                              "Res:{:.0e}s".format(cycle_time,
                                                   self.cycle_resolution)
                plt.title("Histogram: Frames/Cycle", **self.title_params_left)
                plt.title(title_right, **self.title_params_right)

            plt.xlim(0, x_max)
            plt.grid(**self.grid_params_major)
            plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
            plt.xlabel("Cycle Time {} [µs]".format(src))
            plt.legend(loc="upper right")
            if losses:
                ax = plt.gca()
                ax.text(transform=ax.transAxes, **self.text_losses_params)
            plt.tight_layout()

            for f in self.file_format:
                file = "{}/{}_{}.{}".format(self.plot_path, plot_type, src, f)
                plt.savefig(file, **self.savefig_params)
            plt.close('all')

            # histogram for each stream individually
            for x, w, b, c, m in zip(data, weights, bins,
                                     colors, self.mapping.values()):
                plt.hist(x=x, bins=b, weights=w, label=m, color=c)

                if title:
                    title_right = "Cycle: {:.0e}s, " \
                                  "Res:{:.0e}s".format(cycle_time,
                                                       self.cycle_resolution)
                    plt.title("Histogram: Frames/Cycle", **self.title_params_left)
                    plt.title(title_right, **self.title_params_right)

                plt.grid(**self.grid_params_major)
                plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
                plt.xlabel("Cycle Time {} [µs]".format(src))
                plt.legend(loc="upper right")
                if losses:
                    ax = plt.gca()
                    ax.text(transform=ax.transAxes, **self.text_losses_params)
                plt.tight_layout()

                for f in self.file_format:
                    file = "{}/{}_{}_{}.{}".format(self.plot_path,
                                                   plot_type, m, src, f)
                    plt.savefig(file, **self.savefig_params)
                plt.close('all')

        else:
            print("ERROR - There is no other output "
                  "method as mpl currently defined.")
            exit(1)