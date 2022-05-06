import SozinProcessor_v1 as sp
from jarEngine.Enhancements import TopicProcessor_v1
from jarEngine.Content.NLP import NLTK
from fairNLP import Language
from FList import LIST
from FSON import DICT
from FDate import DATE

from Jarticle.jArticles import jArticles


from FLog.LOGGER import Log
Log = Log("Engine.Processor.HookupProcessor")

WORDS = "words"
BODY = "body"
TITLE = "title"
DESCRIPTION = "description"

"""
-> Maintains the lifecycle of processing a list of hookups
"""


def categorizer(article):
    return TopicProcessor_v1.TopicProcessor().process_single_article_v1(article)

def sozin(content):
    tickers = sp.extract_tickers(content)
    stock_tickers = LIST.get(0, tickers)
    crypto_tickers = LIST.get(1, tickers)
    print("Tickers: " + str(tickers))
    if stock_tickers and crypto_tickers:
        return tickers
    elif stock_tickers:
        return stock_tickers
    elif crypto_tickers:
        return crypto_tickers
    return False

def get_summary(article):
    summary = NLTK.summarize(article["title"], article["body"], 2)
    return summary

def get_sentiment(content):
    sentiment = NLTK.get_content_sentiment(content)
    return sentiment


class ArticleProcessor:
    jdb = None

    # -> SETUP <- #
    def __init__(self):
        """ -> MASTER PROCESSOR ID CREATED HERE <- """
        self.jdb = jArticles.constructor_jarticles()
        articles = self.jdb.get_articles_last_day_not_empty()
        for article in articles:
            self.process_article(article)

    # -> Master Runner of Single Article
    def process_article(self, article):
        updated_date = DICT.get("updatedDate", article, False)
        if updated_date:
            return
        # -> Setup
        # id = DICT.get("_id", article)
        title = DICT.get("title", article)
        body = DICT.get("body", article)
        description = DICT.get("description", article)
        content = Language.combine_args_str(title, body, description)
        article = categorizer(article)
        article["tickers"] = sozin(content)
        article["sentiment"] = get_sentiment(content)
        article["updatedDate"] = DATE.mongo_date_today_str()
        self.update_article_in_database(article)

    # -> MongoDB
    def update_article_in_database(self, article):
        _id = DICT.get("_id", article)
        self.jdb.replace_article(_id, article)







if __name__ == "__main__":
    test = "ACEY2025: 3D Tower Defense Game That virtual world Takes You to the Metaverse on Mars - Bitcoinist"
    ArticleProcessor()