from parsePcap import TsnParsePcap
from statsAnalysis import TsnStatsAnalysis
from createPlot import TsnCreatePlot
from util import *


"""
Example:
  - input: multiple files
  - output: plot
  - visualization:
      - mpl
      - boxplot
"""


INPUT = "-BBB"
FRAMESIZE = 60
TAS_CONFIG = 1
INPUT_PATH = '/mnt/harddrive/data/pcaps/'

input_files = ['FibroLAN-FalconRX{}_No-QoS_{}_0.0percent.pcap'.format(INPUT, FRAMESIZE),
               'FibroLAN-FalconRX{}_No-QoS_{}_120.0percent.pcap'.format(INPUT, FRAMESIZE),
               'FibroLAN-FalconRX{}_IEEE-802.1p_{}_120.0percent.pcap'.format(INPUT, FRAMESIZE),
               'FibroLAN-FalconRX{}_TAS{}_{}_120.0percent.pcap'.format(INPUT, TAS_CONFIG, FRAMESIZE)]
input_files = ["{}{}".format(INPUT_PATH, input_file) for input_file in input_files]
output_path = "/home/arch/baseline_test"

mapping = {1: 'robotic',        # vlan prio: 6
           2: 'audio',          # vlan prio: 5
           3: 'video'}          # vlan prio: 4

qos_type = "No-QoS"
bg_load = 0
bg_framesize = FRAMESIZE

xlabels = ['Baseline',
           'Baseline + BG',
           'SPQ + BG',
           'SPQ + TAS + BG']


def main():

    pps = []
    for p in input_files:
        pp = TsnParsePcap(path=p,
                          mapping=mapping,
                          output_path=output_path)
        pp.pcap_to_dfs()
        pps.append(pp)

    dfs = []
    for pp in pps:
        dfs.append(pp.get_dfs())
    cp = TsnCreatePlot(dfs=dfs,
                       output_path=output_path,
                       mapping=mapping,
                       bg_load=bg_load,
                       bg_framesize=bg_framesize,
                       qos_type=qos_type)
    cp.set_style()
    cp.generate_plots(plot_type="boxplot", title=True, xlabels=xlabels)


if __name__ == '__main__':
    main()
