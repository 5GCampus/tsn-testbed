from numpy import savetxt
from pathlib import Path
from sys import exit


class TsnStatsAnalysis():
    """Get statistics from parsed DataFrames,
       save output to csv to later use."""

    def __init__(self, dfs, output_path,  mapping, stats=None, measurements=None):
        self.dfs = dfs
        self.output_path = output_path
        self.mapping = mapping
        self.stats = ["stream",
                      "measurement",
                      "var",
                      "minimum",
                      "maximum",
                      "median",
                      "mean",
                      "std",
                      "p0.01",
                      "p0.05",
                      "p0.10",
                      "p0.80",
                      "p0.95",
                      "p0.99"] if not stats else stats
        self.measurements = ['Latency (ns)',
                             'Inter Frame Gap Sender (ns)',
                             'Inter Frame Gap Receiver (ns)'] if not measurements else measurements

    def export_statistics_to_csv(self):
        statistics = []
        for df, v in zip(self.dfs, self.mapping.values()):
            rows = self.calculate_statistics(df, v)
            for r in rows:
                statistics.append(r)
        header = ",".join(self.stats)

        # create path if it does not exists:
        csv_path = "{}/csv".format(self.output_path)
        Path(csv_path).mkdir(parents=True, exist_ok=True)

        csv_file_path = "{}/statistics.csv".format(csv_path)
        savetxt(csv_file_path,
                statistics,
                delimiter=",",
                header=header,
                fmt='%s',
                comments="")

    def calculate_statistics(self, df, stream):
        rows = []
        for m in self.measurements:
            row = []
            for s in self.stats:
                if s == "stream":
                    row.append(stream)
                elif s == "measurement":
                    row.append(m)
                elif s == "var":
                    row.append(df[m].astype(float).var())
                elif s == "minimum":
                    row.append(df[m].min())
                elif s == "maximum":
                    row.append(df[m].max())
                elif s == "median":
                    row.append(df[m].median())
                elif s == "mean":
                    row.append(df[m].mean())
                elif s == "std":
                    row.append(df[m].astype(float).std())
                else:
                    try:
                        s = float(s.lstrip("p"))
                        if type(s) == float and (0 < s < 1):
                            row.append(df[m].quantile(s, interpolation="nearest"))
                    except Exception:
                        print("ERROR - unknown stats type {}".format(s))
                        exit(1)
            rows.append(row)
        return rows