import retrieve_financial_information
import os
import numpy as np
import datetime
from datetime import date
from numpy import save

def Ticker_Extractor():
    from finsymbols import symbols

    # Extraction of symbols through funsymbols API
    sp500 = symbols.get_sp500_symbols()

    # Creation of list with the symbols extracted
    symbols = []
    symbols = [company["symbol"][:-1] for company in sp500]

    # Print success statement
    print(f"A total of {len(sp500)} tickers have been extracted")

    return symbols


def create_company_profile_database(logPath, ticker):
    try:
        # Definition of paths
        path = f"{logPath}/Raw data/Company profiles"

        # If the results directory does not exist, it creates it.
        if os.path.isdir(path) != True:
            os.makedirs(path)
        else:
            pass

        # Extraction of raw financial information to Data_dictionary
        Financials = retrieve_financial_information.Financials(ticker)
        Data = Financials.Get_company_profile_quarterly()

        # Extraction of keys (titles) of the data set
        Keys = list(Data["profile"].keys())

        # Creates the ticker.txt file and writes the downloaded data with a ";" delimiter format
        with open(f"{path}/{ticker}.txt", "w") as f:
            # Writes the headers with a ";" delimiter format. Last value is not separated by ";" delimiter
            for j in range(0,len(Keys)):
                if j != len(Keys)-1:
                    f.write(f"{Keys[j]};")
                else:
                    f.write(f"{Keys[j]}")
            f.write("\n")
            # Writes the values with a ";" delimiter format. Last value is not separated by ";" delimiter
            for k in range(0,len(Data["profile"].values())):
                if k != len(list(Data["profile"].values()))-1:
                    f.write(f"{list(Data['profile'].values())[k]};")
                else:
                    f.write(f"{list(Data['profile'].values())[k]}\n")

        print(f"Company profile for ticker '{ticker}' has been created successfully")

    except:
        print(f"Something went wrong when creating the company profile for ticker '{ticker}'")


def create_expected_growth_database(logpath, ticker):
    try:
        # Definition of paths
        path = f"{logpath}/Raw data/Expected growth"

        # If the results directory does not exist, it creates it.
        if os.path.isdir(path) != True:
            os.makedirs(path)
        else:
            pass

        # Extraction of raw expected growth and convert to float without percentage (from XX.XX% to 0.XXXX)
        Financials = retrieve_financial_information.Financials(ticker)
        expected_growth = float(Financials.get_expected_growth()[:-1])*0.01

        # Retrieves current date and converts it in datetime.datetime object
        todays_date = date.today().strftime("%Y-%m-%d")
        todays_date = datetime.datetime.strptime(todays_date,"%Y-%m-%d" )

        if os.path.exists(f"{path}/{ticker}.txt") == True and os.stat(f"{path}/{ticker}.txt").st_size != 0:
            # Read .txt file to extract the latest date recorded
            with open(f"{path}/{ticker}.txt", "r") as f:
                # Returns the first 10 digits of the second line of the raw data file (this includes the latest date recorded) and converts it to data type object
                existing_last_date = datetime.datetime.strptime(f.readlines()[1][0:10], '%Y-%m-%d')
            # Checks whether last date in the downloaded data is more recent than the recorded in the database (.txt)
            if todays_date > existing_last_date:
                # Reads the current data in the database file (.txt)
                with open(f"{path}/{ticker}.txt", "r") as f:
                    existing_data = f.readlines()
                    # Creates the update_data string (line to be inserted in the database)
                    updated_data = f"{todays_date};{expected_growth}\n"
                    # Insert the data in row 1 of the file (top row below the headers)
                    existing_data.insert(1, updated_data)
                    # Re-insert the updated existing_data list to the database
                with open(f"{path}/{ticker}.txt", "w") as f:
                    for raw in existing_data:
                        f.write(raw)
                print(f"Expected growth for ticker '{ticker}' has been updated")

            else:
                print(f"Expected growth for ticker '{ticker}' was already updated")
                pass
        else:
            # Creates the ticker.txt file and writes the downloaded data with a ";" delimiter format
            with open(f"{path}/{ticker}.txt", "w") as f:
                # Writes the headers with a ";" delimiter format. Last value is not separated by ";" delimiter

                f.write(f"Date;Expected_growth\n")
                # Writes the values with a ";" delimiter format. Last value is not separated by ";" delimiter
                f.write(f"{todays_date};{expected_growth}")

            print(f"Expected growth for ticker '{ticker}' has been created successfully")

    except:
        print(f"Something went wrong when creating the expected growth for ticker '{ticker}'")


def create_financials_database(logPath, ticker):
    try:
        # Definition of the dictionaries that will be used later in the function
        Paths_dictionary = {}

        # Definition of paths
        Paths_dictionary["Income_statement_annually_path"] = f"{logPath}/Raw data/Income statements/Annual"
        Paths_dictionary["Income_statement_quarterly_path"] = f"{logPath}/Raw data/Income statements/Quarter"
        Paths_dictionary["Cash_flow_annually_path"] = f"{logPath}/Raw data/Cash flows/Annual"
        Paths_dictionary["Cash_flow_quarterly_path"] = f"{logPath}/Raw data/Cash flows/Quarter"
        Paths_dictionary["Balance_sheet_annually_path"] = f"{logPath}/Raw data/Balance sheets/Annual"
        Paths_dictionary["Balance_sheet_quarterly_path"] = f"{logPath}/Raw data/Balance sheets/Quarter"
        Paths_dictionary["Company_value_quarterly_path"] = f"{logPath}/Raw data/Company value/Quarter"
        Paths_dictionary["Company_key_metrics_annually_path"] = f"{logPath}/Raw data/Company key metrics/Annual"
        Paths_dictionary["Company_key_metrics_quarterly_path"] = f"{logPath}/Raw data/Company key metrics/Quarter"

        # If the results directory does not exist, it creates it.
        for Path in Paths_dictionary.values():
            if os.path.isdir(Path) != True:
                os.makedirs(Path)
            else:
                pass

        # Extraction of raw financial information to Data_dictionary
        Financials = retrieve_financial_information.Financials(ticker)
        Data_dictionary = {}
        Data_dictionary["Income_statement_annually"] = Financials.Get_income_statement_annually()
        Data_dictionary["Income_statement_quarterly"] = Financials.Get_income_statement_quarterly()
        Data_dictionary["Cash_flow_annually"] = Financials.Get_cashflow_statement_annually()
        Data_dictionary["Cash_flow_quarterly"] = Financials.Get_cashflow_statement_quarterly()
        Data_dictionary["Balance_sheet_annually"] = Financials.Get_balance_sheet_annually()
        Data_dictionary["Balance_sheet_quarterly"] = Financials.Get_balance_sheet_quarterly()
        Data_dictionary["Company_value_quarterly"] = Financials.Get_company_value_quarterly()
        Data_dictionary["Company_key_metrics_annually"] = Financials.Get_company_key_metrics_annually()
        Data_dictionary["Company_key_metrics_quarterly"] = Financials.Get_company_key_metrics_quarterly()

        # Change key name of "financials" in order to be able to re-use the rest of the code
        Data_dictionary["Company_value_quarterly"]["financials"] = Data_dictionary["Company_value_quarterly"]["enterpriseValues"]
        del Data_dictionary["Company_value_quarterly"]["enterpriseValues"]
        Data_dictionary["Company_key_metrics_annually"]["financials"] = Data_dictionary["Company_key_metrics_annually"]["metrics"]
        del Data_dictionary["Company_key_metrics_annually"]["metrics"]
        Data_dictionary["Company_key_metrics_quarterly"]["financials"] = Data_dictionary["Company_key_metrics_quarterly"]["metrics"]
        del Data_dictionary["Company_key_metrics_quarterly"]["metrics"]

        # Extraction of keys (titles) of each data set and gather it under Keys_dictionary
        Keys_dictionary = {}
        Keys_dictionary["Income_statement_annually_keys"] = list(Data_dictionary["Income_statement_annually"]["financials"][0].keys())
        Keys_dictionary["Income_statement_quarterly_keys"] = list(Data_dictionary["Income_statement_quarterly"]["financials"][0].keys())
        Keys_dictionary["Cash_flow_annually_keys"] = list(Data_dictionary["Cash_flow_annually"]["financials"][0].keys())
        Keys_dictionary["Cash_flow_quarterly_keys"] = list(Data_dictionary["Cash_flow_quarterly"]["financials"][0].keys())
        Keys_dictionary["Balance_sheet_annually_keys"] = list(Data_dictionary["Balance_sheet_annually"]["financials"][0].keys())
        Keys_dictionary["Balance_sheet_quarterly_keys"] = list(Data_dictionary["Balance_sheet_quarterly"]["financials"][0].keys())
        Keys_dictionary["Company_value_quarterly_keys"] = list(Data_dictionary["Company_value_quarterly"]["financials"][0].keys())
        Keys_dictionary["Company_key_metrics_annually_keys"] = list(Data_dictionary["Company_key_metrics_annually"]["financials"][0].keys())
        Keys_dictionary["Company_key_metrics_quarterly_keys"] = list(Data_dictionary["Company_key_metrics_quarterly"]["financials"][0].keys())


        for i in range(0,len(list(Data_dictionary.values()))):
            # If ticker file exists or is not empty, it checks whether the data is complete and if not, it completes it:
            if os.path.exists(f"{list(Paths_dictionary.values())[i]}/{ticker}.txt") == True and os.stat(f"{list(Paths_dictionary.values())[i]}/{ticker}.txt").st_size != 0:
                #Read .txt file to extract the latest date recorded
                with open(f"{list(Paths_dictionary.values())[i]}/{ticker}.txt", "r") as f:
                    # Returns the first 10 digits of the second line of the raw data file (this includes the latest date recorded) and converts it to data type object
                    existing_last_date = datetime.datetime.strptime(f.readlines()[1][0:10], '%Y-%m-%d')
                # Returns the last date retrieved from the online database and converts it to data type object
                downloaded_last_date = datetime.datetime.strptime(list(Data_dictionary.values())[i]["financials"][0]["date"], '%Y-%m-%d')
                # Checks whether last date in the downloaded data is more recent than the recorded in the database (.txt)
                if downloaded_last_date > existing_last_date:
                    # It checks how many dates in the downloaded data are more recent than the recorded in the database (.txt)
                    for k in range(1,len(list(Data_dictionary.values())[i]["financials"])):
                        # Extracts each date from the downloaded data (from the second date) and converts it to datatime object
                        downloaded_date = datetime.datetime.strptime(list(Data_dictionary.values())[i]["financials"][k]["date"], '%Y-%m-%d')
                        # If the downloaded date is more recent than the latest date in the database (.txt), it goes to the next date
                        if downloaded_date > existing_last_date:
                            continue
                        # If the downloaded date is equal or further than the latest date in the database (.txt), it writes all the most recent downloaded dates in lines under the .txt file
                        else:
                            # Reads the current data in the database file (.txt)
                            with open(f"{list(Paths_dictionary.values())[i]}/{ticker}.txt", "r") as f:
                                existing_data = f.readlines()
                            # Creates an empty list of values to be added
                            updated_data = []
                            # It writes down on a list all the lines (string format) that will be added to the database (.txt)
                            for m in range(0, k):
                                updated_data_line = []
                                for l in range(0, len(list((list(Data_dictionary.values())[i]["financials"][m]).values()))):
                                    if l != len(list((list(Data_dictionary.values())[i]["financials"][m]).values()))-1:
                                        updated_data_line.append(f"{list((list(Data_dictionary.values())[i]['financials'][m]).values())[l]};")
                                    else:
                                        updated_data_line.append(f"{list((list(Data_dictionary.values())[i]['financials'][m]).values())[l]}\n")
                                # Join all the values from the updated_data_line in a unique string that composes an entire line that will be copied to the database
                                updated_data_line = "".join(updated_data_line)
                                # Add the updata_data_line to the updated_data file, which will be later on used to update de database (.txt)
                                updated_data.append(updated_data_line)
                            # Merge the string lines saved in the updated_data file to be part of the existing_data file (in the correct position).
                            for y in range(1, k+1):
                                existing_data.insert(y, updated_data[y-1])
                            # Re-insert the updated existing_data list to the database
                            with open(f"{list(Paths_dictionary.values())[i]}/{ticker}.txt", "w") as f:
                                for raw in existing_data:
                                    f.write(raw)
                            break
                    print(f"File for ticker '{ticker}' has been updated")
                else:
                    print (f"File for ticker '{ticker}' was already updated")
                    pass

            # If ticker file does not exist, it creates a new one with the downloaded data.
            else:
                # Creates the ticker.txt file and writes the downloaded data with a ";" delimiter format
                with open(f"{list(Paths_dictionary.values())[i]}/{ticker}.txt", "w") as f:
                    # Writes the headers with a ";" delimiter format. Last value is not separated by ";" delimiter
                    for j in range(0,len(list(Keys_dictionary.values())[i])):
                        if j != len(list(Keys_dictionary.values())[i])-1:
                            f.write(f"{list(Keys_dictionary.values())[i][j]};")
                        else:
                            f.write(f"{list(Keys_dictionary.values())[i][j]}")
                    f.write("\n")
                    # Writes the values with a ";" delimiter format. Last value is not separated by ";" delimiter
                    for k in range(0,len(list(Data_dictionary.values())[i]["financials"])):
                        for l in range(0,len(list((list(Data_dictionary.values())[i]["financials"][k]).values()))):
                            if l != len(list((list(Data_dictionary.values())[i]["financials"][k]).values()))-1:
                                  f.write(f"{list((list(Data_dictionary.values())[i]['financials'][k]).values())[l]};")
                            else:
                                f.write(f"{list((list(Data_dictionary.values())[i]['financials'][k]).values())[l]}\n")
                print(f"Database files for ticker '{ticker}' have been created successfully")

    except:
        print(f"Something went wrong when creating database for ticker '{ticker}'")



def create_numpy(logPath, ticker):
    try:
        # Definition of the dictionaries that will be used later in the function
        Origin_paths_list = []
        Destination_paths_list = []

        # Definition of origin_paths_list
        Origin_paths_list.append(f"{logPath}/Raw data/Company profiles")
        Origin_paths_list.append(f"{logPath}/Raw data/Expected growth")
        Origin_paths_list.append(f"{logPath}/Raw data/Income statements/Annual")
        Origin_paths_list.append(f"{logPath}/Raw data/Income statements/Quarter")
        Origin_paths_list.append(f"{logPath}/Raw data/Cash flows/Annual")
        Origin_paths_list.append(f"{logPath}/Raw data/Cash flows/Quarter")
        Origin_paths_list.append(f"{logPath}/Raw data/Balance sheets/Annual")
        Origin_paths_list.append(f"{logPath}/Raw data/Balance sheets/Quarter")
        Origin_paths_list.append(f"{logPath}/Raw data/Company value/Quarter")
        Origin_paths_list.append(f"{logPath}/Raw data/Company key metrics/Annual")
        Origin_paths_list.append(f"{logPath}/Raw data/Company key metrics/Quarter")

        # Definition of destination_paths_list
        Destination_paths_list.append(f"{logPath}/Numpy files/Company profiles")
        Destination_paths_list.append(f"{logPath}/Numpy files/Expected growth")
        Destination_paths_list.append(f"{logPath}/Numpy files/Income statements/Annual")
        Destination_paths_list.append(f"{logPath}/Numpy files/Income statements/Quarter")
        Destination_paths_list.append(f"{logPath}/Numpy files/Cash flows/Annual")
        Destination_paths_list.append(f"{logPath}/Numpy files/Cash flows/Quarter")
        Destination_paths_list.append(f"{logPath}/Numpy files/Balance sheets/Annual")
        Destination_paths_list.append(f"{logPath}/Numpy files/Balance sheets/Quarter")
        Destination_paths_list.append(f"{logPath}/Numpy files/Company value/Quarter")
        Destination_paths_list.append(f"{logPath}/Numpy files/Company key metrics/Annual")
        Destination_paths_list.append(f"{logPath}/Numpy files/Company key metrics/Quarter")

        # Creation of numpy files
        for i in range(0,len(Origin_paths_list)):

            # If the results directory does not exist, it creates it.
            if os.path.isdir(Destination_paths_list[i]) != True:
                os.makedirs(Destination_paths_list[i])
            else:
                pass

            # Creation of numpy arrays from text files
            Numpy_array = np.genfromtxt(fname = f"{Origin_paths_list[i]}/{ticker}.txt", delimiter = ";",names = True, dtype = None, encoding = None)

            # Creation of numpy files from numpy arrays
            save(f"{Destination_paths_list[i]}/{ticker}.npy", Numpy_array)

        print(f"Numpy files for ticker '{ticker}' have been created successfully")

    except NameError:
        print(f"Ticker '{ticker}' cannot be found in the database")
    except:
        print(f"Something else went wrong when creating ticker '{ticker}.npy'")
