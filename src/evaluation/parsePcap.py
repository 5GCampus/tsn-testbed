from dpkt.pcap import Reader
from decimal import Decimal
from pandas import DataFrame
from math import ceil, floor
from pathlib import Path


class TsnParsePcap():
    """This class parses a captured .pcap file
       to a pandas dataframe"""

    def __init__(self, path, mapping, output_path, cycle_time=None):
        self.path = path
        self.mapping = mapping
        self.dfs = None
        self.dfs_raw = None
        self.output_path = output_path
        self.cycle_time = cycle_time
        self.cycle_resolution = 1e6

        try:
            f = open(self.path, "rb")
            self.pcap = Reader(f)
        except Exception as e:
            print(e)

    def pcap_to_dfs(self):
        pcap_dict = {}
        pcap_dataframes = []

        # initialize dictionary: add lists for each pre-defined source:
        for src in self.mapping.values():
            pcap_dict[src] = {}
            pcap_dict[src]['Timestamp Sender (Unix epoch, s)'] = []
            # add a temporary '0' to sender/receiver timestamp for ifg calculation
            pcap_dict[src]['Timestamp Sender (Unix epoch, s)'].append(0)
            pcap_dict[src]['Timestamp Receiver (Unix epoch, s)'] = []
            pcap_dict[src]['Timestamp Receiver (Unix epoch, s)'].append(0)
            pcap_dict[src]['Latency (ns)'] = []
            pcap_dict[src]['Inter Frame Gap Sender (ns)'] = []
            pcap_dict[src]['Inter Frame Gap Receiver (ns)'] = []
            pcap_dict[src]['Frame No.'] = []
            pcap_dict[src]['Sender Cycle Time (us)'] = []
            pcap_dict[src]['Receiver Cycle Time (us)'] = []

        # loop through all entries in pcap
        for ts, buf in self.pcap:
            hexstream = buf.hex()
            if len(hexstream) <= 128 and hexstream.endswith("00"):
                continue
            # src equals last byte in MAC src addr (see pcap_writer)
            src = self.mapping[int(hexstream[23], 16)]
            frame_id = int(hexstream[44:48], 16)
            # use Decimal as data type for better precision (float is not precise in ns range)
            ts_nsec = Decimal(int(hexstream[108:116], 16))
            ts_sec = Decimal(int(hexstream[100:108], 16))
            # sender time stamp is split in 2 parts, add leading zeros for 2. part
            ts_send = ts_sec + Decimal("0." + str(ts_nsec).zfill(9))
            ts_recv = ts
            latency = ts_recv * Decimal(1e9) - ts_send * Decimal(1e9)

            ts_send_last = pcap_dict[src]['Timestamp Sender (Unix epoch, s)'][-1]
            ts_recv_last = pcap_dict[src]['Timestamp Receiver (Unix epoch, s)'][-1]
            ifg_send = (ts_send - ts_send_last) * Decimal(1e9)
            ifg_recv = (ts_recv - ts_recv_last) * Decimal(1e9)

            if self.cycle_time:
                ts_send_cycletime = round(ts_send % Decimal(self.cycle_time) * Decimal(self.cycle_resolution))
                ts_recv_cycletime = round(ts_recv % Decimal(self.cycle_time) * Decimal(self.cycle_resolution))
            else:
                ts_send_cycletime = None
                ts_recv_cycletime = None

            pcap_dict[src]['Timestamp Sender (Unix epoch, s)'].append(ts_send)
            pcap_dict[src]['Timestamp Receiver (Unix epoch, s)'].append(ts_recv)
            pcap_dict[src]['Latency (ns)'].append(latency)
            pcap_dict[src]['Inter Frame Gap Sender (ns)'].append(ifg_send)
            pcap_dict[src]['Inter Frame Gap Receiver (ns)'].append(ifg_recv)
            pcap_dict[src]['Frame No.'].append(frame_id)
            pcap_dict[src]['Sender Cycle Time (us)'].append(ts_send_cycletime)
            pcap_dict[src]['Receiver Cycle Time (us)'].append(ts_recv_cycletime)

        # delete first entries, since we added a temp value before
        for src in self.mapping.values():
            del pcap_dict[src]['Timestamp Sender (Unix epoch, s)'][0]
            del pcap_dict[src]['Timestamp Receiver (Unix epoch, s)'][0]

        # create dataframe from dictionary of lists, add dataframe to list
        for k, _ in pcap_dict.items():
            df = DataFrame({'Timestamp Sender (Unix epoch, s)': pcap_dict[k]['Timestamp Sender (Unix epoch, s)'],
                            'Timestamp Receiver (Unix epoch, s)': pcap_dict[k]['Timestamp Receiver (Unix epoch, s)'],
                            'Latency (ns)': pcap_dict[k]['Latency (ns)'],
                            'Inter Frame Gap Sender (ns)': pcap_dict[k]['Inter Frame Gap Sender (ns)'],
                            'Inter Frame Gap Receiver (ns)': pcap_dict[k]['Inter Frame Gap Receiver (ns)'],
                            'Frame No.': pcap_dict[k]['Frame No.'],
                            'Sender Cycle Time (us)': pcap_dict[k]['Sender Cycle Time (us)'],
                            'Receiver Cycle Time (us)': pcap_dict[k]['Receiver Cycle Time (us)'],
                            'Source': str(k)},
                           columns=['Timestamp Sender (Unix epoch, s)',
                                    'Timestamp Receiver (Unix epoch, s)',
                                    'Latency (ns)',
                                    'Inter Frame Gap Sender (ns)',
                                    'Inter Frame Gap Receiver (ns)',
                                    'Frame No.',
                                    'Sender Cycle Time (us)',
                                    'Receiver Cycle Time (us)',
                                    'Source'])
            pcap_dataframes.append(df)

        # drop first row: wrong inter frame gap value
        for df in pcap_dataframes:
            df.drop(index=df.index[0], axis=0, inplace=True)

        # sort dataframes for later plotting (ensure same order every time)
        SORT_ORDER = {}
        for k, v in self.mapping.items():
            SORT_ORDER[v] = k - 1

        pcap_dataframes.sort(key=lambda val: SORT_ORDER[val["Source"].iloc[0]])

        self.dfs_raw = pcap_dataframes

        starts = []
        ends = []

        for df in pcap_dataframes:
            starts.append(df['Timestamp Receiver (Unix epoch, s)'].iloc[0])
            ends.append(df['Timestamp Receiver (Unix epoch, s)'].iloc[-1])

        start = Decimal(ceil(max(starts)) + 5)
        end = Decimal(floor(min(ends)) - 5)

        dfs_parallel = []

        for df in pcap_dataframes:
            df = df.loc[df['Timestamp Receiver (Unix epoch, s)'] > start]
            df = df.loc[df['Timestamp Receiver (Unix epoch, s)'] < end]
            dfs_parallel.append(df)

        self.dfs = dfs_parallel

    def export_dfs_to_csv(self):
        # create path if it does not exists:
        csv_path = "{}/csv".format(self.output_path)
        Path(csv_path).mkdir(parents=True, exist_ok=True)

        for df, v in zip(self.dfs, self.mapping.values()):
            csv_file_path = "{}/{}.csv".format(csv_path, v)
            self.export_df_to_csv(df, csv_file_path)

    def export_df_to_csv(self, df, name):
        df.to_csv(name, index=True, header=True)

    def get_dfs(self):
        return self.dfs

    def get_dfs_raw(self):
        return self.dfs_raw
