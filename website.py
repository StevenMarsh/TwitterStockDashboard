from flask import Flask, render_template, request
import requests
from matplotlib.figure import Figure
from matplotlib import ticker
import base64
import numpy as np
from io import BytesIO
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import col



app = Flask(__name__)
app.debug = True

tickers = ["AAPL", "MSFT", "AMZN", "GOOG", "FB",
                  "KO", "TSLA", "JPM", "V", "WMT", "DIS"]

spark = SparkSession.builder.appName("ticker") \
        .master("local[*]").config("spark.driver.memory", "5g") \
        .config("spark.driver.host", "127.0.0.1") \
        .config("spark.driver.bindAddress", "127.0.0.1") \
        .getOrCreate()


@app.route('/', methods=['GET'])
def dropdown():

    return render_template("home.html", tickers=tickers)

@app.route('/graph' ,methods=['GET', 'POST'])
def getChoice():
    if request.method == "POST":
        tickChoice = request.form.get("tickers", None)
        firstDate = request.form.get("firstdate", None)
        endDate = request.form.get("enddate", None)

        if tickChoice is None:
            tickChoice = request.form.get("tck", None)

        if tickChoice is not None or firstDate is not None:

            tickerDict = {"AAPL": "Apple", "MSFT": "Microsoft", "AMZN": "Amazon", "GOOG": "Google",
                          "FB": "Facebook",
                          "KO": "CocaCola", "TSLA": "Tesla", "JPM": "JPMorgan", "V": "Visa", "WMT": "Walmart",
                          "DIS": "Disney"}

            tick = tickerDict[tickChoice]

            firebaseUrl = "https://twitterfinancedash-default-rtdb.firebaseio.com/" + tickChoice + ".json"

            response = requests.get(url=firebaseUrl)

            dataDict = {}
            data = response.json()

            # with open('data.json', 'w') as outfile:
            #     json.dump(data, outfile, indent=4)
            #
            # tJson = spark.read.json('data.json', multiLine=True)
            #

            for row in data:

                dataDict[row] = data[row]

            y = []
            x = []
            for dates in dataDict.keys():

                try:

                    # df = tJson.where(tJson[dates == dates])[["ticker"]]
                    # print(df.show(2))
                    # print(tJson[["ticker"]].show(2))
                    stockStuff = data[dates]["ticker"].strip('[').strip(']').split(',')
                    closePrice = round(float(stockStuff[0]), 2)

                    y.append(closePrice)
                    x.append(dates)
                except KeyError as ke:
                    print("No ticker for today found")


            fig = Figure()
            ax = fig.subplots()
            ax.set_title(tick)
            ax.set_xlabel("Dates", )
            ax.set_ylabel("Adj Closing Price")
            labels = [x[0], x[int(len(x) * .25)], x[int(len(x) * .5)], x[int(len(x) * .75)], x[int(len(x) - 1)]]
            ax.set_xticklabels(labels, fontsize= 7)
            ax.xaxis.set_major_locator(ticker.LinearLocator(5))

            for tick_ in ax.get_xticklabels():
                tick_.set_rotation(0)
            ax.plot(x, y)

            buf = BytesIO()
            fig.savefig(buf, format="png")
            # Embed the result in the html output.
            plot_data = base64.b64encode(buf.getbuffer()).decode("ascii")


            twitterTuples = []
            for dates in dataDict.keys():
                try:

                    tweets = data[dates]["tweets"].strip('[').strip(']').split('",')
                    for tweet in tweets:
                        tweet = tweet.strip('"')
                        tup = (dates, tweet)
                        twitterTuples.append(tup)

                except KeyError as ke:
                    print("No Tweet for today found")



            rangeTuples = []
            if firstDate is not None and endDate is not None:
                start = list(dataDict.keys()).index(firstDate)
                end = list(dataDict.keys()).index(endDate)
                for i in range(start, end+1):
                    try:
                        curr = list(dataDict.keys())[i]

                        stockStuff = data[curr]["ticker"].strip('[').strip(']').split(',')

                        closePrice = round(float(stockStuff[0]), 2)

                        tweets = data[curr]["tweets"].strip('[').strip(']').split('",')

                        twitList = []
                        for tweet in tweets:
                            tweet = tweet.strip('"')
                            twitList.append(tweet)

                        tup = (curr, closePrice, twitList)
                        rangeTuples.append(tup)

                    except KeyError as ke:
                        print("No Tweet and/or Ticker for today found")

            unique = list(np.unique(np.array(list(dataDict.keys()))))

            return render_template("landing.html", tickChoice=tick, tickers=tickers, plot_data=plot_data,
                                   twitter=twitterTuples, daterange=rangeTuples, unique_dates=unique,choice=tickChoice)

        return render_template("home.html", tickers=tickers)



if __name__ == "__main__":

    app.run()



