import sys
sys.path.append("..")

from evaluation.parsePcap import TsnParsePcap
from evaluation.statsAnalysis import TsnStatsAnalysis
from evaluation.createPlot import TsnCreatePlot
from evaluation.util import parse_filename, create_mapping, create_filename
from argparse import ArgumentParser
from sys import exit


def main():
    parser = ArgumentParser()
    parser.add_argument("-i", "--input-pcap",
                        help="Pcap file.",
                        nargs='+',
                        required=True)
    parser.add_argument("-o", "--output-dir",
                        help="Path for storing output.",
                        default="successful_measurements/")
    parser.add_argument("-c", "--cycle-time",
                        help="TAS Cycle time.",
                        type=float)
    args = parser.parse_args()

    if 1 < len(args.input_pcap) < 4:
        dfs = []
        streams = []
        for i in args.input_pcap:
            switch, stream, qos_type, bg_framesize, bg_load = parse_filename(i)
            streams.append(stream[0])
            mapping_single = create_mapping(stream)
            pp = TsnParsePcap(path=i,
                              mapping=mapping_single,
                              output_path="")  # output path is not required
            pp.pcap_to_dfs()
            dfs.append(pp.get_dfs()[0])
        mapping = create_mapping(streams)
        switch, _, qos_type, bg_framesize, bg_load = parse_filename(args.input_pcap[0])
        input_filename = create_filename(switch, mapping, qos_type, bg_framesize, bg_load)
        output_path = "{}{}-separate".format(args.output_dir, input_filename)

    elif len(args.input_pcap) == 1:
        input_filename = args.input_pcap[0].split("/")[-1].strip(".pcap")
        output_path = "{}{}".format(args.output_dir, input_filename)

        switch, streams, qos_type, bg_framesize, bg_load = parse_filename(args.input_pcap[0])
        mapping = create_mapping(streams)

        if args.cycle_time:
            pp = TsnParsePcap(path=args.input_pcap[0],
                              mapping=mapping,
                              output_path=output_path,
                              cycle_time=args.cycle_time)
        else:
            pp = TsnParsePcap(path=args.input_pcap[0],
                              mapping=mapping,
                              output_path=output_path)

        pp.pcap_to_dfs()
        dfs = pp.get_dfs()
        pp.export_dfs_to_csv()

    else:
        print("Too many arguments!")
        exit(1)

    sa = TsnStatsAnalysis(dfs=dfs,
                          output_path=output_path,
                          mapping=mapping)
    sa.export_statistics_to_csv()

    cp = TsnCreatePlot(dfs=dfs,
                       output_path=output_path,
                       mapping=mapping,
                       bg_load=bg_load,
                       bg_framesize=bg_framesize,
                       qos_type=qos_type)
    cp.set_style()
    cp.generate_plots(plot_type="latency_over_time", output="mpl")
    cp.generate_plots(plot_type="latency_over_time", output="csv")
    cp.generate_plots(plot_type="ifg_over_time", output="mpl")
    cp.generate_plots(plot_type="ifg_over_time", output="csv")
    cp.generate_plots(plot_type="ifg_cdf", output="mpl")
    cp.generate_plots(plot_type="ifg_ccdf", output="mpl")
    cp.generate_plots(plot_type="ifg_cdf", output="csv")
    cp.generate_plots(plot_type="latency_cdf", output="mpl")
    cp.generate_plots(plot_type="latency_ccdf", output="mpl", title=False)
    cp.generate_plots(plot_type="latency_cdf", output="csv")
    if args.cycle_time:
        cp.generate_plots(plot_type="cycle_time", output="mpl",
                          src="Sender", cycle_time=args.cycle_time)
        cp.generate_plots(plot_type="cycle_time", output="mpl",
                          src="Receiver", cycle_time=args.cycle_time)


if __name__ == '__main__':
    main()
