import pandas as pd

# 入出力ツール
class IOTools:
    def __init__(self) -> None:
        pass

    def load_csv(self, path, cols=[]):
        if not cols: df = pd.read_csv(path)
        else: df = pd.read_csv(path, usecols=cols)
        return df

    def disp_csvinfo(self, df):
        print(df.shape,
              df.columns,
              df.describe(),
              sep="\n")

# 前処理用のツール(PreProcessing)
class PPTools:
    def __init__(self) -> None:
        pass

# 機械学習用ツール(Machine Learning)
class MLTools:
    def __init__(self) -> None:
        pass

class Tools(IOTools, PPTools, MLTools):
    # すべてのツールをオーバーロード
    def __init__(self) -> None:
        super().__init__()

if __name__ == '__main__':
    tools = Tools()
