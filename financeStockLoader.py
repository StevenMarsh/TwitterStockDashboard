import yfinance as yf
from pandas_datareader import data as pdr
import pandas as pd

yf.pdr_override()

tickerList = ["AAPL", "MSFT", "AMZN", "GOOG", "FB", "BABA", "TSM", "TSLA", "JPM", "V", "JNJ", "WMT", "DIS"]

for ticker in tickerList:

    data = pdr.get_data_yahoo(f"{ticker}", start="2017-01-01", end="2021-03-1")
    data.to_csv(f"{ticker}.csv")


