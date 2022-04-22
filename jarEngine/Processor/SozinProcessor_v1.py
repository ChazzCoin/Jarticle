import jarFAIR
from jarFAIR.Core import LIST
from jarEngine.Content import Ticker


class ProcessTickers:
    strict = True
    original_hookups = []
    processed_hookups = []

    """
    -> Add hookups 
    -> Run .start()
    """

    def __init__(self, hookups: []=None, strict=True):
        # -> look at title, description and body...
        self.original_hookups = hookups
        self.strict = strict

    def start(self, strict=True):
        self.strict = strict
        for hookup in self.original_hookups:
            # -> Tokenize
            content = jarFAIR.Language.combine_args_str(hookup.title, hookup.description, hookup.body)
            # -> Find Potential Tickers
            if self.strict:
                potential_tickers = jarFAIR.Ticker.find_tickers_strict_v2(content=content)
            else:
                potential_tickers = jarFAIR.Ticker.find_tickers_light_v2(content=content)
            # -> Classify Tickers into Stock or Crypto
            # [('Stock', 'AMD'), ('Crypto', 'MANA')]
            list_of_classified = Ticker.classify_tickers(potential_tickers)

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

            temp = {}
            temp['Stock'] = temp_stock
            temp['Crypto'] = temp_crypto
            hookup.tickers.append(temp)
            self.processed_hookups.append(hookup)
