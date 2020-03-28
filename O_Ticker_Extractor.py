import sys
# install finsymbols with pip install finsymbols
from finsymbols import symbols
import os

class TicketExtractor:
    def __init__(self):
        self.sp500 = symbols.get_sp500_symbols()
        self.symbols = []

    def printSymbols(self):
        print("printing symbols...")
        print(self.sp500)

    def listDictionaryKeys(self):
        for key in self.sp500:
            print(key)

    def obtainSymbols(self):
        self.symbols = [company["symbol"][:-1] for company in self.sp500]

    def getSymbols(self):
        print(f"A total of {len(self.sp500)} tickers have been extracted")
        return self.symbols

    def discardDownloadedTickers(self, logPath):
        if os.path.exists(logPath):
            with open(logPath) as f:
                for line in f:
                    symbol = line.partition(' ')[0]
                    if symbol in self.symbols:
                        self.symbols.remove(symbol)
