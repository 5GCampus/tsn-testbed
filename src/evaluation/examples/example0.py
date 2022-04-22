from parsePcap import TsnParsePcap
from statsAnalysis import TsnStatsAnalysis
from createPlot import TsnCreatePlot
from util import *


"""
Example:
  - input: single file
  - output: statistics, plots
  - visualization:
      - mpl + csv
      - latency/ifg over time
      - latency/ifg cdf/ccdf
"""

input_file = "input.pcap"
output_path = "dir/output"


def main():
    switch, streams, qos_type, bg_framesize, bg_load = parse_filename(input_file)
    mapping = create_mapping(streams)
    
    pp = TsnParsePcap(path=input_file,
                      mapping=mapping,
                      output_path=output_path)
    pp.pcap_to_dfs()
    dfs = pp.get_dfs()
    pp.export_dfs_to_csv()
    
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
    # {}_{}cdf with output="csv" produce same csv file, no need to call it twice!
    cp.generate_plots(plot_type="ifg_cdf", output="csv")
    cp.generate_plots(plot_type="latency_cdf", output="mpl")
    cp.generate_plots(plot_type="latency_ccdf", output="mpl", title=False)
    cp.generate_plots(plot_type="latency_cdf", output="csv")


if __name__ == '__main__':
    main()
