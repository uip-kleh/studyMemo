import os, sys
sys.path.append(os.pardir)
from common.tools import Tools

if __name__ == '__main__':
    tools = Tools()
    df = tools.load_csv("test.csv")
    tools.disp_csvinfo(df)
