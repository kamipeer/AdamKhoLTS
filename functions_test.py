import os
import retrieve_financial_information
import datetime


def create_database(logPath, ticker):
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

        # Extraction of keys (titles) of each data set and gather it under Keys_dictionary
        Keys_dictionary = {}
        Keys_dictionary["Income_statement_annually_keys"] = list(Data_dictionary["Income_statement_annually"]["financials"][0].keys())
        Keys_dictionary["Income_statement_quarterly_keys"] = list(Data_dictionary["Income_statement_quarterly"]["financials"][0].keys())
        Keys_dictionary["Cash_flow_annually_keys"] = list(Data_dictionary["Cash_flow_annually"]["financials"][0].keys())
        Keys_dictionary["Cash_flow_quarterly_keys"] = list(Data_dictionary["Cash_flow_quarterly"]["financials"][0].keys())
        Keys_dictionary["Balance_sheet_annually_keys"] = list(Data_dictionary["Balance_sheet_annually"]["financials"][0].keys())
        Keys_dictionary["Balance_sheet_quarterly_keys"] = list(Data_dictionary["Balance_sheet_quarterly"]["financials"][0].keys())

        for i in range(0,len(list(Data_dictionary.values()))):
            # If ticker file exists or is not empty, it checks whether the data is complete and if not it completes it:
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
                else:
                    print (f"File for ticker '{ticker} already updated")
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

                    for k in range(0,len(list(Data_dictionary.values())[i]["financials"])):
                        for l in range(0,len(list((list(Data_dictionary.values())[i]["financials"][k]).values()))):
                            if l != len(list((list(Data_dictionary.values())[i]["financials"][k]).values()))-1:
                                f.write(f"{list((list(Data_dictionary.values())[i]['financials'][k]).values())[l]};")
                            else:
                                f.write(f"{list((list(Data_dictionary.values())[i]['financials'][k]).values())[l]}\n")

        print(f"Database files for ticker '{ticker}' have been created successfully")

    except:
        print(f"Something went wrong when creating database for ticker '{ticker}'")
