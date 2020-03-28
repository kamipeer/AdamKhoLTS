# Multiprocessing tutorial video https://www.youtube.com/watch?v=fKl2JW_qrso

import os
import time
import concurrent.futures
import database_functions
import ticker_analysis_functions


def update_database():
    # Defines starting time
    t1 = time.perf_counter()

    # Extraction of S&P 500 tickers
    tickers = database_functions.Ticker_Extractor()
    print(tickers)

    # Defines the database directory
    current_Path = os.getcwd()
    database_base_path = f"{current_Path}/Data"

    # Defines the logPath variable to be used in the map function (logPath list should be same length as tickers list)
    database_path_list = [database_base_path] * len(tickers)

    # Runs the multiprocessing function for creation of company profiles
    # if __name__ == '__main__':
    #     with concurrent.futures.ThreadPoolExecutor() as executor:
    #         executor.map(database_functions.create_company_profile_database, database_path_list, tickers)

    # Calculates finish time for creation of company profiles
    t2 = time.perf_counter()

    # Runs the multiprocessing function for creation of expected growth
    # if __name__ == '__main__':
    #     with concurrent.futures.ThreadPoolExecutor() as executor:
    #         executor.map(database_functions.create_expected_growth_database, database_path_list, tickers)

    # Calculates finish time for creation of company profiles
    t3 = time.perf_counter()

    # Runs the multiprocessing function for creation of database files
    # if __name__ == '__main__':
    #     with concurrent.futures.ThreadPoolExecutor() as executor:
    #         executor.map(database_functions.create_financials_database, database_path_list, tickers)

    # Calculates finish time for creation of database files
    t4 = time.perf_counter()

    # Runs the multiprocessing function for creation of numpy files
    if __name__ == '__main__':
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(database_functions.create_numpy, database_path_list, tickers)

    # Defines completion time
    t5 = time.perf_counter()

    # Prints elapsed time statement
    print(f"Creation of company profiles has taken {t2-t1} seconds")
    print(f"Creation of expected growth files has taken {t3-t2} seconds")
    print(f"Creation of database text files has taken {t4-t3} seconds")
    print(f"Creation of numpy files has taken {t5-t4} seconds")


def condition_1_analysis():
    # Defines starting time
    t1 = time.perf_counter()

    # Extraction of S&P 500 tickers
    tickers = database_functions.Ticker_Extractor()

    # Defines the database directory
    current_Path = os.getcwd()
    database_base_path = f"{current_Path}/Data"

    # Defines the logPath variable to be used in the map function (logPath list should be same length as tickers list)
    database_path_list = [database_base_path] * len(tickers)

    # Runs the multiprocessing function for condition_1 analysis
    if __name__ == '__main__':
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(ticker_analysis_functions.condition_1, database_path_list, tickers)

    # Creates a list from the tickers that pass condition_1
    tickers = []
    for result in results:
        if result != None:
            tickers.append(result)

    # Calculates finish time for condition_1 anaælysis
    t2 = time.perf_counter()

    # Prints elapsed time statement
    print(f"Analysis of condition 1 has taken {t2-t1} seconds")
    return tickers


def industry_average_margins():
    # Defines starting time
    t1 = time.perf_counter()

    # Extraction of S&P 500 tickers
    tickers = database_functions.Ticker_Extractor()

    # Defines the database directory
    current_Path = os.getcwd()
    database_base_path = f"{current_Path}/Data"

    # Defines the logPath variable to be used in the map function (logPath list should be same length as tickers list)
    database_path_list = [database_base_path] * len(tickers)

    # Runs the multiprocessing function for condition_1 analysis
    if __name__ == '__main__':
        with concurrent.futures.ThreadPoolExecutor() as executor:
            ticker_margins = executor.map(ticker_analysis_functions.retrieve_industry_margins, database_path_list, tickers)

    # Creates a list from the tickers that pass condition_1
    margins_list = []
    for i in ticker_margins:
        if i != None:
            margins_list.append(i)

    # Extract all the different industry types and creates a list with each of them
    industry_types_list = list(set([item[1] for item in margins_list]))

    # Collates gross and net margins of all tickers belonging to a specific industry and calculates the industry average gross and net margins
    industry_average_margins_dictionary = {}

    for industry in industry_types_list:
        industry = industry
        # Retrieves all the gross and net margins for items in margins_list that belong to a certain industry and collates them in a list
        industry_gross_margins_list = [item[2] for item in margins_list if item[1] == industry]
        industry_net_margins_list = [item[3] for item in margins_list if item[1] == industry]
        #Calculates the average gross and net margins of a specific industry
        average_gross_margin = sum(industry_gross_margins_list)/len(industry_gross_margins_list)
        average_net_margin = sum(industry_net_margins_list)/len(industry_net_margins_list)
        #Collates all the calculated average margins in a list
        industry_average_margins_dictionary[industry] = [average_gross_margin, average_net_margin]

    # Defines completion time
    t2 = time.perf_counter()

    # Prints elapsed time statement
    print(f"Extraction of industry averages has taken {t2-t1} seconds")

    return industry_average_margins_dictionary


def condition_2_analysis(tickers_condition_1, industry_average_margins_dictionary):
    # Defines starting time
    t1 = time.perf_counter()

    # Defines the database directory
    current_Path = os.getcwd()
    database_base_path = f"{current_Path}/Data"

    # Defines the logPath variable to be used in the map function (logPath list should be same length as tickers list)
    database_path_list = [database_base_path] * len(tickers_condition_1)
    industry_average_margins_dictionary_list = [industry_average_margins_dictionary] * len(tickers_condition_1)

    # Runs the multiprocessing function for condition_2 analysis
    if __name__ == '__main__':
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(ticker_analysis_functions.condition_2, database_path_list, tickers_condition_1, industry_average_margins_dictionary_list)

    # Creates a list from the tickers that pass condition_2
    tickers = []
    for result in results:
        if result != None:
            tickers.append(result)

    # Calculates finish time for condition_1 anaælysis
    t2 = time.perf_counter()

    # Prints elapsed time statement
    print(f"Analysis of condition 2 has taken {t2-t1} seconds")

    return tickers


def condition_3_analysis(tickers_condition_2):
    # Defines starting time
    t1 = time.perf_counter()

    # Defines the database directory
    current_Path = os.getcwd()
    database_base_path = f"{current_Path}/Data"

    # Defines the logPath variable to be used in the map function (logPath list should be same length as tickers list)
    database_path_list = [database_base_path] * len(tickers_condition_2)

    # Runs the multiprocessing function for condition_5 analysis
    if __name__ == '__main__':
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(ticker_analysis_functions.condition_3, database_path_list, tickers_condition_2)

    # Creates a list from the tickers that pass condition_5
    tickers = []
    for result in results:
        if result != None:
            tickers.append(result)

    # Calculates finish time for condition_1 anaælysis
    t2 = time.perf_counter()

    # Prints elapsed time statement
    print(f"Analysis of condition 3 has taken {t2-t1} seconds")

    return tickers


def condition_4_analysis(tickers_condition_3):
    # Defines starting time
    t1 = time.perf_counter()

    # Defines the database directory
    current_Path = os.getcwd()
    database_base_path = f"{current_Path}/Data"

    # Defines the logPath variable to be used in the map function (logPath list should be same length as tickers list)
    database_path_list = [database_base_path] * len(tickers_condition_3)

    # Runs the multiprocessing function for condition_5 analysis
    if __name__ == '__main__':
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(ticker_analysis_functions.condition_4, database_path_list, tickers_condition_3)

    # Creates a list from the tickers that pass condition_5
    tickers = []
    for result in results:
        if result != None:
            tickers.append(result)

    # Calculates finish time for condition_1 anaælysis
    t2 = time.perf_counter()

    # Prints elapsed time statement
    print(f"Analysis of condition 4 has taken {t2-t1} seconds")

    return tickers


def condition_5_analysis(tickers_condition_4):
    # Defines starting time
    t1 = time.perf_counter()

    # Defines the database directory
    current_Path = os.getcwd()
    database_base_path = f"{current_Path}/Data"

    # Defines the logPath variable to be used in the map function (logPath list should be same length as tickers list)
    database_path_list = [database_base_path] * len(tickers_condition_4)

    # Runs the multiprocessing function for condition_5 analysis
    if __name__ == '__main__':
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(ticker_analysis_functions.condition_5, database_path_list, tickers_condition_4)

    # Creates a list from the tickers that pass condition_5
    tickers = []
    for result in results:
        if result != None:
            tickers.append(result)

    # Calculates finish time for condition_1 anaælysis
    t2 = time.perf_counter()

    # Prints elapsed time statement
    print(f"Analysis of condition 5 has taken {t2-t1} seconds")

    return tickers


def condition_6_analysis(tickers_condition_5):
    # Defines starting time
    t1 = time.perf_counter()

    # Defines the database directory
    current_Path = os.getcwd()
    database_base_path = f"{current_Path}/Data"

    # Defines the logPath variable to be used in the map function (logPath list should be same length as tickers list)
    database_path_list = [database_base_path] * len(tickers_condition_5)

    # Runs the multiprocessing function for calculation of intrinsic_values
    if __name__ == '__main__':
        with concurrent.futures.ThreadPoolExecutor() as executor:
            intrinsic_values = executor.map(ticker_analysis_functions.calculate_intrinsic_value, database_path_list, tickers_condition_5)

    # Creates a list from the tickers that pass condition_5
    intrinsic_values_list = []
    for result in intrinsic_values:
        if result != None:
            intrinsic_values_list.append(result)

    print(intrinsic_values_list)

    # Runs the multiprocessing function for condition_6 analysis
    if __name__ == '__main__':
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(ticker_analysis_functions.condition_6, database_path_list, tickers_condition_5, intrinsic_values_list)

    # Creates a list from the tickers that pass condition_5
    tickers = []
    for result in results:
        if result != None:
            tickers.append(result)

    # Calculates finish time for condition_1 anaælysis
    t2 = time.perf_counter()

    # Prints elapsed time statement
    print(f"Analysis of condition 6 has taken {t2-t1} seconds")

    return tickers



# Defines starting time
t1 = time.perf_counter()

# Triggers the update database function
update_database()

# Triggers the condition_1_analysis function:
tickers_condition_1 = condition_1_analysis()
print(tickers_condition_1)

# Triggers the industry_average_margins() function to calculate the industry average margins based on the tickers
industry_average_margins_dictionary = industry_average_margins()

# Triggers the conditions_2_analysis()
tickers_condition_2 = condition_2_analysis(tickers_condition_1, industry_average_margins_dictionary)
print(tickers_condition_2)

# Triggers the conditions_2_analysis()
tickers_condition_3 = condition_3_analysis(tickers_condition_2)
print(tickers_condition_3)

# Triggers the conditions_4_analysis()
tickers_condition_4 = condition_4_analysis(tickers_condition_3)
print(tickers_condition_4)

# Triggers the conditions_5_analysis()
tickers_condition_5 = condition_5_analysis(tickers_condition_4)
print(tickers_condition_5)

# Triggers the conditions_6_analysis()
tickers_condition_6 = condition_6_analysis(tickers_condition_5)
print(tickers_condition_6)

# Defines completion time
t2 = time.perf_counter()

# Prints elapsed time statement
print(f"The entire code takes {t2-t1} seconds to complete")

