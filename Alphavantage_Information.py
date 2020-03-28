#https://stackoverflow.com/questions/48071949/how-to-use-the-alpha-vantage-api-directly-from-python

import requests
import pandas as pd
import time
from datetime import date

class Alphavantage:

    def __init__(self, tickers, logPath):
        self.logPath = logPath
        self.tickers = tickers
        self.dataType = "TIME_SERIES_DAILY"
        self.dataDictionary = {}
        self.logDictionary = {}
        self.apiURL = "https://www.alphavantage.co/query"

    def readLog(self):
        with open(self.logPath, "r") as f:
            lines = f.readlines()
            for line in lines:
                self.logDictionary.update({line.split()[0]: line.split()[1]})


    def writeTickerToTxt(self, ticker, directory):
        print(self.dataDictionary[ticker])
        #ticker_name = self.dataDictionary[ticker]["Meta Data"]["2. Symbol"]
        ticker_data = self.dataDictionary[ticker]["Time Series (Daily)"]

        # Extract keys from the ticker_data
        keys = ticker_data.keys()

        with open(directory + ticker + ".txt", "w") as f:
            for key in keys:
                row = [ticker, key, ticker_data[key]['1. open'], ticker_data[key]['2. high'],
                       ticker_data[key]['3. low'], ticker_data[key]['4. close'], ticker_data[key]['5. volume']]
                for r in row[1:]:
                    f.write(r + " ")
                f.write("\n")

        return True

    def extractData(self, directory):
        for ticker in self.tickers:
            tickerAlreadyExisting = False
            if ticker in self.logDictionary:
                tickerAlreadyExisting = True
                if str(self.logDictionary[ticker]) == str(date.today()):
                    continue
            data = {"function": self.dataType,
            "symbol": ticker,
            "outputsize": "full",
            "datatype": "json",
            "apikey": "FNGQJF40AWU3HKT6"}

            response = requests.get(self.apiURL, data)

            responseTime = str(response).split(" ")[1].split("[")[1].split("]")[0]
            print(ticker, responseTime)
            if int(responseTime) != int(200):
                print("Warning: could not get ticker ", ticker)
                time.sleep(60)
                response = requests.get(self.apiURL, data)

            dataJ = response.json()
            self.dataDictionary.update({ticker: dataJ})
            success = False
            success = self.writeTickerToTxt(ticker, directory)

            if success:
                self.updateLog(ticker, tickerAlreadyExisting)

    def getDictionary(self):
        return self.dataDictionary

    def setDictionary(self, dictionary):
        self.dataDictionary = dictionary

    def Create_Dataframe_From_Alphavantage_API(self, directory):

        # Extract keys from the data_dictionary
        dataDictionaryKeys = self.dataDictionary.keys()

        Master_DataFrame_data_dictionary = []

        for ticker in dataDictionaryKeys:

            print(self.dataDictionary[ticker])
            ticker_name = self.dataDictionary[ticker]["Meta Data"]["2. Symbol"]
            ticker_data = self.dataDictionary[ticker]["Time Series (Daily)"]

            #Extract keys from the ticker_data
            keys = ticker_data.keys()

            self.updateLog(ticker)
            with open(directory + ticker + ".txt", "w") as f:
                for key in keys:
                    row = [ticker_name, key, ticker_data[key]['1. open'], ticker_data[key]['2. high'], ticker_data[key]['3. low'], ticker_data[key]['4. close'], ticker_data[key]['5. volume']]
                    Master_DataFrame_data_dictionary.append(row)
                    for r in row[1:]:
                        f.write(r + " ")
                    f.write("\n")

        Master_Dataframe = pd.DataFrame(Master_DataFrame_data_dictionary, columns=["Ticker", "Date", "Open", "High", "Low", "Close", "Volume"])

        Master_Dataframe = Master_Dataframe.astype({"Ticker": str, "Date": str, "Open": float, "High": float, "Low": float, "Close": float, "Volume": int})

        return Master_Dataframe

    def updateLog(self, ticker, tickerAlreadyExisting):
        today = date.today()
        if tickerAlreadyExisting:
            lines = []
            with open(self.logPath, "r") as f:
                lines = f.readlines()
            linesToWrite = []
            with open(self.logPath, "w") as f:
                for line in lines:
                    if line.startswith(ticker):
                        line = ticker + " " + str(today) + "\n"
                    linesToWrite.append(line)
                f.writelines(linesToWrite)
        else:
            with open(self.logPath, "a") as f:
                f.write(ticker + " " + str(today) + "\n")