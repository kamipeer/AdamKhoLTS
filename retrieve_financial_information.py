import requests
import json
from bs4 import BeautifulSoup

class Financials:

    def __init__(self, symbol):
        self.symbol = symbol


    def Get_company_profile_quarterly(self):

        URL_base = "https://financialmodelingprep.com"
        Account_base = f"/api/v3/company/profile/{self.symbol}"
        URL = f"{URL_base}{Account_base}"

        response = requests.get(URL)
        result = response.json()
        return result

    def Get_income_statement_annually(self):

        URL_base = "https://financialmodelingprep.com"
        Account_base = f"/api/v3/financials/income-statement/{self.symbol}"
        URL = f"{URL_base}{Account_base}"

        response = requests.get(URL)
        result = response.json()
        return result


    def Get_income_statement_quarterly(self):

        URL_base = "https://financialmodelingprep.com"
        Account_base = f"/api/v3/financials/income-statement/{self.symbol}?period=quarter"
        URL = f"{URL_base}{Account_base}"

        response = requests.get(URL)
        result = response.json()
        return result


    def Get_balance_sheet_annually(self):

        URL_base = "https://financialmodelingprep.com"
        Account_base = f"/api/v3/financials/balance-sheet-statement/{self.symbol}"
        URL = f"{URL_base}{Account_base}"

        response = requests.get(URL)
        result = response.json()
        return result


    def Get_balance_sheet_quarterly(self):

        URL_base = "https://financialmodelingprep.com"
        Account_base = f"/api/v3/financials/balance-sheet-statement/{self.symbol}?period=quarter"
        URL = f"{URL_base}{Account_base}"

        response = requests.get(URL)
        result = response.json()
        return result


    def Get_cashflow_statement_annually(self):

        URL_base = "https://financialmodelingprep.com"
        Account_base = f"/api/v3/financials/cash-flow-statement/{self.symbol}"
        URL = f"{URL_base}{Account_base}"

        response = requests.get(URL)
        result = response.json()
        return result


    def Get_cashflow_statement_quarterly(self):

        URL_base = "https://financialmodelingprep.com"
        Account_base = f"/api/v3/financials/cash-flow-statement/{self.symbol}?period=quarter"
        URL = f"{URL_base}{Account_base}"

        response = requests.get(URL)
        result = response.json()
        return result


    def Get_financial_ratios_annually(self):

        URL_base = "https://financialmodelingprep.com"
        Account_base = f"/api/v3/financial-ratios/{self.symbol}"
        URL = f"{URL_base}{Account_base}"

        response = requests.get(URL)
        result = response.json()
        return result


    def Get_company_value_quarterly(self):

        URL_base = "https://financialmodelingprep.com"
        Account_base = f"/api/v3/enterprise-value/{self.symbol}?period=quarter"
        URL = f"{URL_base}{Account_base}"

        response = requests.get(URL)
        result = response.json()
        return result


    def Get_company_key_metrics_annually(self):

        URL_base = "https://financialmodelingprep.com"
        Account_base = f"/api/v3/company-key-metrics/{self.symbol}"
        URL = f"{URL_base}{Account_base}"

        response = requests.get(URL)
        result = response.json()
        return result


    def Get_company_key_metrics_quarterly(self):

        URL_base = "https://financialmodelingprep.com"
        Account_base = f"/api/v3/company-key-metrics/{self.symbol}?period=quarter"
        URL = f"{URL_base}{Account_base}"

        response = requests.get(URL)
        result = response.json()
        return result


    def get_expected_growth(self):
        #https: // www.youtube.com / watch?v = rONhdonaWUo & t = 14s

        # Creates variable containing the URL we want to scrape.
        url = f"https://finance.yahoo.com/quote/{self.symbol}/analysis?p={self.symbol}"

        # Makes a variable with the response to the request to the website to scrape the information.
        response = requests.get(url)

        # Parse the requested information
        soup = BeautifulSoup(response.content, "html.parser")

        # Sorts all the content catalogued as "td" with class "Ta(end) Py(10px)" and puts it in a list format
        # The 5 years projection remains in the index 16 of the list
        expected_growth = soup.find_all("td", {"class": "Ta(end) Py(10px)"})[16].text

        return expected_growth
