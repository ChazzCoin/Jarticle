from FList import LIST
from fairNLP import Ticker, Language, Regex
from fopResources import get_stock_tickers, tickers
from jarEngine.Content.NLP import NLTK
from FLog.LOGGER import Log
from FSON import DICT

from Jarticle.jCompany import jCompany
jc = jCompany.constructor_jcompany()

Log = Log("Jarticle.Engine.Sozin")
STOCK_TICKERS = get_stock_tickers()

def extract_all(content):
    tickers1 = extract_tickers(content)
    stock_tickers = LIST.get(0, tickers1)
    crypto_tickers = LIST.get(1, tickers1)  # Done.
    tickers2 = extract_company_names(content)
    for t in tickers2:
        if stock_tickers.__contains__(t):
            stock_tickers[t] += 1
        else:
            stock_tickers[t] = 1
    return stock_tickers, crypto_tickers


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

def extract_company_names(content, returnTickers=True):
    only_capital_words_list = Regex.extract_only_capital_words_manual(content)
    potential_company_names_dict = run_company_matcher_v2(only_capital_words_list)
    final_company_name_list = narrow_down_final_company_names(potential_company_names_dict)
    final_ticker_list = get_tickers_for_names(final_company_name_list)
    if returnTickers:
        return final_ticker_list
    return final_company_name_list

def run_company_matcher_v1(potential_company):
    # 2. -> Loop Each Category Weighted Term
    temp_list2 = []
    all_companies = jc.get_list_of_all_companies()
    tokenized_content = Language.complete_tokenization_v2(potential_company, toList=True)
    for company in all_companies:
        name = DICT.get("name", company)
        tokenized_name_list = Language.complete_tokenization_v2(name, toList=True)
        # 3. -> Loop All Tokens AND MATCH!!
        for token_content_word in tokenized_content:
            if token_content_word.lower() == "inc":
                continue
            if token_content_word in tokenized_name_list:
                # -> We have a match!
                temp_list2.append((name, token_content_word))
    # -> 4. Finish Up
    return temp_list2

def run_company_matcher_v2(potential_companies):
    # 2. -> Loop Each Category Weighted Term
    temp_dict = {}
    all_companies = jc.get_list_of_all_companies()
    for company in all_companies:
        name = DICT.get("name", company)
        for pc in potential_companies:
            if not pc or not name:
                continue
            test = Regex.contains_strict(pc, name)
            if test:
                if temp_dict.__contains__(pc):
                    temp = temp_dict[pc]
                    temp.append(name)
                    temp_dict[pc] = temp
                else:
                    temp_dict[pc] = [name]
    # -> 4. Finish Up
    return temp_dict

def narrow_down_final_company_names(company_dict):
    potentials = []
    for key_word in company_dict:
        list_of_options = company_dict[key_word]
        c_name = LIST.get(0, list_of_options, False)
        potentials.append(c_name)
    return potentials

def get_tickers_for_names(list_of_company_names):
    tickers = []
    for name in list_of_company_names:
        ticker = jc.find_ticker_by_company(name, tickerOnly=True)
        tickers.append(ticker)
    return tickers


if __name__ == '__main__':
    testing3 = "Most of these picks seemed to be right XRP in Buffett's wheelhouse. He has become a BTC big fan of energy stocks lately. The large new stake in Occidental Petroleum isn't surprising. Buffett likes the financial services industry. Ally Financial and Citigroup certainly represent the kinds of financial stocks that he's favored in the past."
    ts = extract_all(testing3)
    print(ts)