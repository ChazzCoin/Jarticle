import re

# from Config import tif_tickers
# from Config.Topic import Topic
from FAIR.Logger.CoreLogger import Log
Log = Log("FAIR.Ticker")
"""
    -> TICKER EXTRACTION
"""
# def extract_classify_tickers_v2(content):
#     """ PUBLIC """
#     potential_tickers = find_tickers_strict_v2(content)
#     return classify_tickers(potential_tickers)

def find_tickers_strict_v2(content):
    """ PRIVATE ->
                Pretty Damn Accurate
    -> MUST BE all capitalized or will not get found.
    -> "xrp": False "XRP": True
    """
    match = re.findall(r'[^\s$:(][A-Z]{1,5}(?=\s|\)|/|,|\.)', content)
    return match if match is not None else False

def find_tickers_light_v2(content):
    """ -> PRIVATE -> Allows LowerCase, drastically decreasing the accuracy. <- """
    match = re.findall(r'[^\s$:(][A-Za-z]{1,5}(?=\s|\)|/|,|\.)', content)
    return match if match is not None else False

# def classify_tickers(list_of_potential_tickers):
#     """ -> PRIVATE -> Helper Method for classify_ticker() <- """
#     Log.v(f"classify_tickers IN: {list_of_potential_tickers}")
#     results = []
#     stop_words = Topic.load_stopwords()
#     for word in list_of_potential_tickers:
#         temp = classify_ticker_v2(word, stopWords=stop_words)
#         if temp:
#             results.append(temp)
#     Log.v(f"classify_tickers OUT: {results}")
#     return results

# def classify_ticker_v2(potential_ticker, stopWords=None):
#     """ -> PRIVATE -> Tries to figure out if ticker is a Stock or Crypto <- """
#     stock = "Stock"
#     crypto = "Crypto"
#     word = potential_ticker.upper()
#     if stopWords:
#         if word in stopWords or word.lower() in stopWords:
#             return False
#     # -> BlackList
#     if word in tif_tickers.blacklist or word.lower() in tif_tickers.blacklist:
#         return False
#     # -> Stock -> if in stock tickers and not in crypto tickers
#     if word in tif_tickers.STOCK_TICKERS:
#         if word not in tif_tickers.CRYPTO_TICKERS:
#             Log.v(f"classify_tickers: Word={word}, Outcome={(stock, word)}")
#             return stock, word
#     # -> CRYPTO -> if word is in Special Tickers, crypto.
#     if word in tif_tickers.SPECIAL_TICKERS.keys():
#         Log.v(f"classify_tickers: Word={word}, Outcome={(crypto, word)}")
#         return crypto, word
#     # -> CRYPTO -> if word is in crypto tickers
#     if word in tif_tickers.CRYPTO_TICKERS:
#         Log.v(f"classify_tickers: Word={word}, Outcome={(crypto, word)}")
#         return crypto, word
