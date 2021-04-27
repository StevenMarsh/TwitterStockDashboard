import requests
import os
import pandas as pd
import json

if __name__ == '__main__':

    entries = os.listdir("Tweets_Tickers")

    firebaseUrl = "https://twitterfinancedash-default-rtdb.firebaseio.com/"
    for entry in entries:

        print(entry)

        if ".csv" not in entry:
            continue

        if "tweets" in entry:

            twitterSet = pd.read_csv("Tweets_Tickers/" + entry)
            ticker = twitterSet["Ticker"][0]


            dates = twitterSet["Time"].to_list()

            for date in dates:

                currDate = date.split()[0].strip()
                url = firebaseUrl + ticker + "/" + currDate + "/tweets.json"

                singleTweet = twitterSet[twitterSet["Time"].str.contains(currDate)]["Tweets"].to_list()

                singleTweetJson = json.dumps(singleTweet)
                print(singleTweet[0])
                r = requests.patch(url=url, json=singleTweetJson)

                if r.status_code == 400:
                    r = requests.put(url=url, json=singleTweetJson)

        else:

            tickerSet = pd.read_csv("Tweets_Tickers/" + entry)
            ticker = entry.strip(".csv")

            dates = tickerSet["Date"].to_list()

            for date in dates:

                closePrice = tickerSet[tickerSet.values == date]["Close"].to_list()
                volume = tickerSet[tickerSet.values == date]["Volume"].to_list()
                url = firebaseUrl + ticker + "/" + date + "/ticker.json"

                singleTick = [closePrice[0], volume[0]]

                print(singleTick)
                singleTickerJson = json.dumps(singleTick)
                r = requests.patch(url=url, json=singleTickerJson)

                if r.status_code == 400:
                    r = requests.put(url=url, json=singleTickerJson)

