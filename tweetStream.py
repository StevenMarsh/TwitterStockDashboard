import tweepy
import pandas as pd

import yfinance as yf
from pandas_datareader import data as pdr


if __name__ == '__main__':

    consumer_key = "JNix5JFWfu2DRZmxs5uKdCZ2S"
    consumer_secret = "e65UxqbVIxdUIemrXjsoXPnrhJkDTXU7HHfq9zMvjac6AwfGPS"
    access_token = "2193630475-gcXO1u0MejxPNiKdTqbf0c6V7ZFas8sB96cxRnp"
    access_token_secret = "E1H9UVzbhLhHuek6pd8qygbTsPEqF01JfcKoWGR86HAkk"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)


    tickerDict = {"AAPL": "AppleMusic", "MSFT": "microsoft", "AMZN": "amazon", "GOOG": "google", "FB": "facebook",
                  "KO": "CocaCola", "TSLA": "tesla", "JPM": "jpmorgan", "V": "visa", "WMT": "walmart", "DIS":"disney"}

    tweets = []
    time = []
    ticker = []

    yf.pdr_override()



    for ticker, text in tickerDict.items():

        cursor = tweepy.Cursor(api.user_timeline, id=f"{text}", tweet_mode="extended").items(250)

        tweets = []
        time = []
        tickers = []

        for twit in cursor:
            tweets.append(twit.full_text)
            time.append(twit.created_at)
            tickers.append(ticker)

        df = pd.DataFrame({"Ticker": tickers, "Tweets": tweets, "Time": time})
        df.to_csv(f"{ticker}_tweets.csv")

        startDate = str(time[len(time)-1]).split()[0]
        endData = str(time[0]).split()[0]
        data = pdr.get_data_yahoo(f"{ticker}", start=f"{startDate}", end=f"{endData}")
        data.to_csv(f"{ticker}.csv")




