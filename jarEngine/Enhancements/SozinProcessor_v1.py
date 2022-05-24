from FList import LIST
from fairNLP import Ticker
from fopResources import get_stock_tickers, tickers
from jarEngine.Content.NLP import NLTK
from FLog.LOGGER import Log

Log = Log("Jarticle.Engine.Sozin")
STOCK_TICKERS = get_stock_tickers()


# [('Stock', 'AMD'), ('Crypto', 'MANA')]
def extract_tickers(content: str):
    # -> Step 1: Extract Potential Tickers
    potential_tickers = Ticker.find_tickers_strict_v2(content=content)
    # -> Step 2: Verify/Classify Potential Tickers into Stock or Crypto
    list_of_classified = classify_tickers(potential_tickers)
    # -> Step 3: Sort Tickers
    temp_crypto = {}
    temp_stock = {}
    for item in list_of_classified:
        ticker_type = LIST.get(0, item)
        ticker_name = LIST.get(1, item)
        if ticker_type == 'Crypto':
            if temp_crypto.__contains__(ticker_name):
                temp_crypto[ticker_name] += 1
            else:
                temp_crypto[ticker_name] = 1
        elif ticker_type == 'Stock':
            if temp_stock.__contains__(ticker_name):
                temp_stock[ticker_name] += 1
            else:
                temp_stock[ticker_name] = 1
    return temp_stock, temp_crypto

# -> Handles a List of Tickers
def classify_tickers(list_of_potential_tickers):
    """ -> PRIVATE -> Helper Method for classify_ticker() <- """
    Log.d(f"classify_tickers IN: {list_of_potential_tickers}")
    results = []
    stop_words = NLTK.stop_words
    for word in list_of_potential_tickers:
        temp = classify_ticker_v2(word, stopWords=stop_words)
        if temp:
            results.append(temp)
    Log.d(f"classify_tickers OUT: {results}")
    return results
# -> Handles one single Ticker.
def classify_ticker_v2(potential_ticker, stopWords=None):
    """ -> PRIVATE -> Tries to figure out if ticker is a Stock or Crypto <- """
    stock = "Stock"
    crypto = "Crypto"

    # No Ticker should have any lowercase characters!
    for char in potential_ticker:
        if not str(char).isupper():
            return False

    word = potential_ticker.upper()
    if stopWords:
        if word in stopWords or word.lower() in stopWords:
            return False
    # -> BlackList
    if word in tickers.blacklist or word.lower() in tickers.blacklist:
        return False
    # -> Stock -> if in stock tickers and not in crypto tickers
    if word in STOCK_TICKERS:
        if word not in tickers.CRYPTO_TICKERS:
            Log.d(f"classify_tickers: Word={word}, Outcome={(stock, word)}")
            return stock, word
    # -> CRYPTO -> if word is in Special Tickers, crypto.
    if word in tickers.SPECIAL_TICKERS.keys():
        Log.d(f"classify_tickers: Word={word}, Outcome={(crypto, word)}")
        return crypto, word
    # -> CRYPTO -> if word is in crypto tickers
    if word in tickers.CRYPTO_TICKERS:
        Log.d(f"classify_tickers: Word={word}, Outcome={(crypto, word)}")
        return crypto, word