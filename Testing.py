import os
import database_functions
import ticker_analysis_functions
import datetime
import retrieve_financial_information
import datetime
import numpy as np
from numpy import save


Current_Path = os.getcwd()
# logPath = f"{Current_Path}/Data/Raw data/Balance sheets/Annual/A.txt"
logPath = f"{Current_Path}/Data"

database_functions.create_expected_growth_database(logPath, "AAPL")