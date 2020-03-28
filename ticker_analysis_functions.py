import numpy as np
import os

# Setting Paths:
savingDirectory = "Data/"
logPath = savingDirectory


# CONDITION 1 - GROWING REVENUES, EARNINGS AND CASH FLOWS
def condition_1(database_base_path, ticker):
        try:
            # Loads the numpy files
            annual_income_statements = np.load(f"{database_base_path}/Numpy files/Income statements/Annual/{ticker}.npy")
            annual_cash_flows = np.load(f"{database_base_path}/Numpy files/Cash flows/Annual/{ticker}.npy")
            # Creates a boolean list with the growing revenues, earnings and cash flow conditions for the past 5 years.
            results_condition_1 = [list(annual_income_statements["Revenue"])[i] > list(annual_income_statements["Revenue"])[i+1] and
                                    list(annual_income_statements["Net_Income"])[i] > list(annual_income_statements["Net_Income"])[i+1] and
                                    list(annual_cash_flows["Operating_Cash_Flow"])[i] > list(annual_cash_flows["Operating_Cash_Flow"])[i + 1]
                                    for i in range(0,3)]
            # If all the results from "results_condition_1" are True, it returns the ticker
            if all(results_condition_1) == True:
                print(f"Ticker '{ticker}' has passed condition 1")
                return ticker
            else:
                pass
        except:
            print(f"An error with ticker '{ticker}' occurred")


# CONDITION 2 - SUSTAINABLE COMPETITIVE ADVANTAGE
def retrieve_industry_margins(database_base_path, ticker):
    try:
        # Loads the numpy files
        company_profiles = np.load(f"{database_base_path}/Numpy files/Company profiles/{ticker}.npy")
        annual_income_statements = np.load(f"{database_base_path}/Numpy files/Income statements/Annual/{ticker}.npy")
        # Gather all the relevant ticker information to calculate the gross and net industry margins
        gross_margin_values = [ticker, str(company_profiles["industry"]), annual_income_statements["Gross_Margin"][0], annual_income_statements["Net_Profit_Margin"][0]]
        return gross_margin_values
    except:
        print(f"An error with ticker '{ticker}' occurred")


def condition_2(database_base_path, ticker, industry_average_margins_dictionary):
    try:
        # Loads the numpy files
        company_profiles = np.load(f"{database_base_path}/Numpy files/Company profiles/{ticker}.npy")
        annual_income_statements = np.load(f"{database_base_path}/Numpy files/Income statements/Annual/{ticker}.npy")

        # Defines all the parameters to analyze condition 2
        company_industry = str(company_profiles["industry"])
        company_gross_margin = annual_income_statements["Gross_Margin"][0]
        company_net_margin = annual_income_statements["Net_Profit_Margin"][0]
        industry_average_gross_margin = industry_average_margins_dictionary[company_industry][0]
        industry_average_net_margin = industry_average_margins_dictionary[company_industry][1]

        # Checks whether ticker margin is equal or above industry margins
        if company_gross_margin >= industry_average_gross_margin and company_net_margin >= industry_average_net_margin:
            return ticker
    except:
        print(f"An error with ticker '{ticker}' occurred")


# CONDITION 3 - FUTURE GROWTH DRIVERS
def condition_3(database_base_path, ticker):
    try:
        # Loads the numpy files
        expected_growth = np.load(f"{database_base_path}/Numpy files/Expected growth/{ticker}.npy")

        #Converts the expected_growth array in a 1d array when is a 0d array
        expected_growth = np.atleast_1d(expected_growth)

    # If condition_3 is True, it returns the ticker
        if (list(expected_growth["Expected_growth"])[0] >= 0.10) == True:
            print(f"Ticker '{ticker}' has passed condition 3")
            return ticker
        else:
            pass
    except:
        print(f"An error with ticker '{ticker}' occurred")


# CONDITION 4 - CONSERVATIVE DEBT
def condition_4(database_base_path, ticker):
    try:
        # Loads the numpy files
        annual_income_statements = np.load(f"{database_base_path}/Numpy files/Income statements/Annual/{ticker}.npy")
        quarter_balance_sheet = np.load(f"{database_base_path}/Numpy files/Balance sheets/Quarter/{ticker}.npy")

        # print(quarter_balance_sheet.dtype.names)

        # If condition_4 is True, it returns the ticker
        if (list(quarter_balance_sheet["Longterm_debt"])[0] < (3 * list(annual_income_statements["Net_Income"])[0])) == True:
            print(f"Ticker '{ticker}' has passed condition 4")
            return ticker
        else:
            pass
    except:
        print(f"An error with ticker '{ticker}' occurred")


# CONDITION 5 - RETURN ON EQUITY (The book does not specifically say 5 years, it could be less)
def condition_5(database_base_path, ticker):
    try:
        # Loads the numpy files
        annual_key_metrics = np.load(f"{database_base_path}/Numpy files/Company key metrics/Annual/{ticker}.npy")
        # Creates a boolean list with the growing revenues, earnings and cash flow conditions for the past 5 years.
        results_condition_5 = [list(annual_key_metrics["ROE"])[i] >= 0.12 for i in range(0, 5)]
        # If all the results from "results_condition_1" are True, it returns the ticker
        if all(results_condition_5) == True:
            print(f"Ticker '{ticker}' has passed condition 5")
            return ticker
        else:
            pass
    except:
        print(f"An error with ticker '{ticker}' occurred")


# CONDITION 6 - INTRINSIC VALUE
# TODO Calculate our own beta value

def calculate_intrinsic_value(database_base_path, ticker):
    try:
        # Loads the numpy files
        company_profile = np.load(f"{database_base_path}/Numpy files/Company profiles/{ticker}.npy")
        expected_growth = np.load(f"{database_base_path}/Numpy files/Expected growth/{ticker}.npy")
        cash_flow = np.load(f"{database_base_path}/Numpy files/Cash flows/Quarter/{ticker}.npy")
        quarter_balance_sheet = np.load(f"{database_base_path}/Numpy files/Balance sheets/Quarter/{ticker}.npy")
        company_value = np.load(f"{database_base_path}/Numpy files/Company value/Quarter/{ticker}.npy")

        # Creates the variables that will be used to calculate the intrinsic value
        latest_beta = company_profile["beta"]
        latest_expected_growth = float(expected_growth["Expected_growth"])
        operating_cash_flow_TTM = sum(list(cash_flow["Operating_Cash_Flow"])[0:4])
        long_term_debt = list(quarter_balance_sheet["Longterm_debt"])[0]
        short_term_debt = list(quarter_balance_sheet["Shortterm_debt"])[0]
        cash_and_cash_equivalents = list(quarter_balance_sheet["Cash_and_cash_equivalents"])[0]
        shares_outstanding = list(company_value["Number_of_Shares"])[0]

        # Defines the discount factor
        if latest_beta < 0.8:
            discount_factor = 0.05
        elif 0.8 <= latest_beta < 1:
            discount_factor = 0.06
        elif 1 <= latest_beta < 1.1:
            discount_factor = 0.065
        elif 1.1 <= latest_beta < 1.2:
            discount_factor = 0.07
        elif 1.2 <= latest_beta < 1.3:
            discount_factor = 0.075
        elif 1.3 <= latest_beta < 1.4:
            discount_factor = 0.08
        elif 1.4 <= latest_beta < 1.5:
            discount_factor = 0.085
        else:
            discount_factor = 0.09

        # Calculates intrinsic value
        intrinsic_value = (sum([(operating_cash_flow_TTM + (1+latest_expected_growth)**i)/(1+discount_factor)**i for i in range(1,11)])
                           - long_term_debt - short_term_debt + cash_and_cash_equivalents)/shares_outstanding

        return intrinsic_value

    except:
        print(f"An error with calculating intrinsic value for ticker '{ticker}' occurred")

def condition_6(database_base_path, ticker, intrinsic_value):
    try:
        # Loads the numpy files
        company_profile = np.load(f"{database_base_path}/Numpy files/Company profiles/{ticker}.npy")

        # IChecks if intrinsic value is higher than current price
        if float(company_profile["price"]) < intrinsic_value:
            print(f"Ticker '{ticker}' has passed condition 6")
            return ticker
        else:
            pass
    except:
        print(f"An error in calculating condition 6 with ticker '{ticker}' occurred")

# CONDITION 7 - CONFIRMED UPTREND
# TODO Assess if SMA 50 > SMA 150 and both slope upwards
