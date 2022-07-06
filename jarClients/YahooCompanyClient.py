from yahoo_fin import stock_info as si
import yfinance as yf
import json

from FSON import DICT
from FLog.LOGGER import Log
Log = Log("Clients.YahooClient")

class CompanyClient:
    client_ticker = None
    info = {}
    news = []
    financials = None
    history = None
    major_holders = None
    institutional_holders = None
    earnings = None
    quarterly_earnings = None
    calendar = None

    def __init__(self, ticker: str):
        # Log.i(f"Starting Client: Ticker={ticker}")
        self.client_ticker = yf.Ticker(ticker.upper())
        # self.get_info()
        self.get_history()
        # self.get_major_holders()
        # self.get_institutional_holders()
        # self.get_earnings()
        # self.get_quarterly_earnings()
        # self.get_calendar()
        # self.get_news()
        # self.get_financials()

    # Get Current Crypto Price for Ticker
    def get_crypto_price(self, ticker):
        cryptos = si.get_top_crypto().iterrows()
        for c in cryptos:
            c = c[1]
            if ticker.upper() in c['Name']:
                print(ticker + ":", c['Price (Intraday)'])
                return c

    def get_info(self):
        self.info = self.client_ticker.info

    def get_history(self):
        self.history = self.client_ticker.history(period='max')

    def get_major_holders(self):
        self.major_holders = self.client_ticker.major_holders

    def get_institutional_holders(self):
        self.institutional_holders = self.client_ticker.institutional_holders

    def get_earnings(self):
        self.earnings = self.client_ticker.earnings

    def get_quarterly_earnings(self):
        self.quarterly_earnings = self.client_ticker.quarterly_earnings

    def get_calendar(self):
        self.calendar = self.client_ticker.calendar

    def get_news(self):
        self.news = self.client_ticker.news

    def get_financials(self):
        self.financials = self.client_ticker.financials

    def print_dict(self, obj):
        print(json.dumps(obj, indent=3))

    @staticmethod
    def to_dict(input):
        return input.to_dict('list')

    # @staticmethod
    # def graph_dataframe(input):
    #     import matplotlib.pyplot as plt
    #     input.plot()
    #     plt.savefig('myfile.pdf')



if __name__ == '__main__':
    y = CompanyClient("MSFT")
    breakdown = DICT.get("client_ticker", y)
    fins = DICT.get("financials", y)
    his = DICT.get("history", y)
    temp = breakdown.earnings
    # y.graph_dataframe(fins)
    print("nothing")


