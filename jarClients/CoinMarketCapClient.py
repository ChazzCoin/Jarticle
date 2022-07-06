from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
# from FAIR.Core import FILE
from jarDataProvider import jarProvider as Provider
# from Config import env
from FLog.LOGGER import Log

Log = Log("Clients.CoinMarketCapClient")

# -> CoinMarketCap
COIN_MARKET_CAP_BASE_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency"
COIN_MARKET_CAP_URL = ""
COIN_MARKET_CAP_ALL_LISTINGS = "/listings/latest"
CMC_PRO_API_KEY = "f369741c-4e59-4089-9481-87d714ec1200"


API_KEY = CMC_PRO_API_KEY
headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': API_KEY}
parameters = {'start': '1', 'limit': '5000', 'convert': 'USD'}

class CoinMarketCapClient:
    session = Session()
    saved_data = None
    crypto_info = {}
    BASE_URL = COIN_MARKET_CAP_BASE_URL
    ALL_LISTINGS_URL = BASE_URL + COIN_MARKET_CAP_ALL_LISTINGS
    CRYPTO_INFO_URL = BASE_URL + "/info"
    CRYPTO_PRICE_URL = BASE_URL + "/quotes/latest"
    CRYPTO_PRICE_HISTORICAL = BASE_URL + "/listings/historical"

    def __init__(self):
        Log.i(f"Starting Client.")
        self.load_saved_data()
        self.session.headers.update(headers)

    def load_saved_data(self):
        self.saved_data = Provider.get_crypto_data_from_file()

    def request(self, url, params):
        try:
            response = self.session.get(url, params=params)
            data = json.loads(response.text)
            return data
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            Log.e("Failed to create Session", e)
        return

    def get_historical_price_data(self, slugs):
        info_params = {'slug': slugs}
        r = self.request(self.CRYPTO_PRICE_HISTORICAL, info_params)
        data = r
        for d in data:
            details = data
            name = details.get("name")
            self.parse_details(details)
            self.crypto_info[name] = details
        Provider.save_dict_to_file(file_name, self.crypto_info)

    def save_crypto_info(self, slugs, file_name="crypto_info"):
        info_params = {'slug': slugs}
        r = self.request(self.CRYPTO_INFO_URL, info_params)
        data = r
        for d in data:
            details = data
            name = details.get("name")
            self.parse_details(details)
            self.crypto_info[name] = details
        Provider.save_dict_to_file(file_name, self.crypto_info)

    @staticmethod
    def get_metaverse_ticker_data(slugs: [], file_name="top_meta_ticker_info"):
        client = CoinMarketCapClient()
        meta_tickers = {}
        slugs = ",".join(slugs)
        info_params = {'symbol': slugs}
        r = client.request(client.CRYPTO_INFO_URL, info_params)
        data = r
        for d in data:
            details = data
            name = details.get("name")
            client.parse_details(details)
            meta_tickers[name] = details
        Provider.save_dict_to_file(file_name, meta_tickers, file_path=Provider.glewmetv_path)

    @staticmethod
    def get_metaverse_price_data(slugs: [], file_name="top_meta_price_info"):
        client = CoinMarketCapClient()
        meta_tickers = {}
        slugs = ",".join(slugs)
        info_params = {'symbol': slugs}
        r = client.request(client.CRYPTO_PRICE_URL, info_params)
        data = r
        for d in data:
            details = data
            name = details.get("name")
            # client.parse_details(details)
            meta_tickers[name] = details
        Provider.save_dict_to_file(file_name, meta_tickers, file_path=Provider.glewmetv_path)

    def parse_details(self, details):
        Log.p("\n--CRYPTO INFO--")
        Log.p("Name:", details.get("name"))
        Log.p("Type:", details.get("category"))
        Log.p("Description:", details.get("description"))
        urls = details.get("urls")
        Log.p("--URLS--")
        for url in urls:
            Log.p(url, urls[url])
        Log.p("\n")

    def refresh_all_tickers_to_file(self):
        # -> Get Data from CoinMarketCap.
        data = self.request(self.ALL_LISTINGS_URL, parameters)
        # -> Pull out the cryptos and their info
        items = data.get("data")
        # -> Validate Old and New are not the same.
        self.print_data_comparison(items)
        if len(items) == len(self.saved_data):
            Log.i("Nothing New Found.")
            exit()
        # -> Save New crypto_tickers.json info from CoinMarketCap.
        Provider.save_crypto_data_to_file(data)

    def get_new_projects(self):
        # -> Loop new items, look for the odd ones out.
        for item in self.saved_data:
            i = item.get("symbol")
            Log.i("Checking for:", i)
            if i in self.saved_data:
                continue
            else:
                self.print_new_project_found(item)

    def print_data_comparison(self, items):
        Log.p("Old Data:", len(self.saved_data))
        Log.p("New Data:", len(items))

    def print_new_project_found(self, item):
        Log.p("Found New Project")
        Log.p("\nsymbol:", item.get("symbol"))
        Log.p("name:", item.get("name"))
        Log.p("price:", item.get("price"))

    @staticmethod
    def single_request(url, params):
        try:
            session = Session()
            session.headers.update(headers)
            response = session.get(url, params=params)
            data = json.loads(response.text)
            return data
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            Log.e("Failed to get single request", error=e)
        return None

if __name__ == '__main__':
    c = CoinMarketCapClient()
    c.get_metaverse_price_data(["MANA", "AVAX", "SAND", "ETH"])
