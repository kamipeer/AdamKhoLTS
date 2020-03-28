def Create_Database(logPath, ticker):

    # Definition of the dictionaries that will be used later in the function
    Paths_dictionary = {}
    Financials_dictionary = {}

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
    Financials = Financial_Information.Financials(ticker)
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

    # It creates the ticker file for Annual Income Statement data
    for i in range(0,6):
        with open(f"{list(Paths_dictionary.values())[i]}/{ticker}.txt", "w") as f:
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
                        f.write(f"{list((list(Data_dictionary.values())[i]['financials'][k]).values())[l]}")
                f.write("\n")

    print(f"Database files for ticker '{ticker}' have been created successfully")


def create_empty_files (logPath, ticker):
    with open(f"{logPath}/{ticker}.txt", "w") as f:
        f.write("Success, it worked!")
