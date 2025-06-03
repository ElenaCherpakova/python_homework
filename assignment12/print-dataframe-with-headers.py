import pandas as pd


class DFPlus(pd.DataFrame):
    @property
    def _constructor(self):
        return DFPlus

    @classmethod
    def from_csv(cls, filepath, **kwargs):
        df = pd.read_csv(filepath, **kwargs)
        return cls(df)

    def print_with_headers(self):
        start = 0
        while start < len(self):
            print(super().iloc[start:start+10])
            start += 10


dfp = DFPlus.from_csv("../csv/products.csv")
dfp.print_with_headers()
