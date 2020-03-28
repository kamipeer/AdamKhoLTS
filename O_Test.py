import O_Ticker_Extractor
import retrieve_financial_information
import O_Database
import os
import time

t1 = time.perf_counter()

# Defines the results directory
Current_Path = os.getcwd()
logPath = f"{Current_Path}/Data"

# Extraction of S&P500 tickers
tickerExtractor = O_Ticker_Extractor.TicketExtractor()
tickerExtractor.obtainSymbols()
# tickerExtractor.discardDownloadedTickers(logPath)
tickers = tickerExtractor.getSymbols()

# Create database in text format (raw data)
Database = O_Database.Database(tickers, logPath)
Database.Create_Database()

t2 = time.perf_counter()

print(f"Creation of database text files has taken {t2-t1} seconds")

# Create numpy database from text database
Database.Create_Numpy()

t3 = time.perf_counter()

print(f"Creation of numpy files has taken {t3-t2} seconds")