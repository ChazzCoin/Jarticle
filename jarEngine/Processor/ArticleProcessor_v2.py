from jarEngine.Enhancements import TopicProcessor_v1, SozinProcessor_v1 as sp
from jarEngine.Content.NLP import NLTK
from fairNLP import Language
from FList import LIST
from FSON import DICT
from FDate import DATE

from jarProvider import ArticleProvider as ap

from FLog.LOGGER import Log
Log = Log("Engine.Processor.HookupProcessor")

WORDS = "words"
BODY = "body"
TITLE = "title"
DESCRIPTION = "description"

"""
-> Maintains the lifecycle of processing a list of hookups
"""

LAST_UPDATE = "May 19 2022"

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
    body = DICT.get("body", article, default="False")
    summary = NLTK.summarize_v2(body, 4)
    # summary = Language.text_summarizer(body, 4)
    return summary

def get_keywords(article):
    title = DICT.get("title", article, default="False")
    body = DICT.get("body", article, default="False")
    keywords = NLTK.keywords(body + title)
    newList = []
    for item in keywords:
        newList.append(item)
    return newList

def get_sentiment(content):
    sentiment = NLTK.get_content_sentiment(content)
    return sentiment

# -> [MASTER]
def enhance_article(article, content):
    article = categorizer(article)
    article["keywords"] = get_keywords(article)
    article["summary"] = get_summary(article)
    article["tickers"] = sozin(content)
    article["sentiment"] = get_sentiment(content)
    article["updatedDate"] = DATE.mongo_date_today_str()
    return article

def update_enhanced_summary(article):
    article["summary"] = get_summary(article)
    return article

# -> Processing Class Object
class ArticleProcessor:
    isTest = False

    @classmethod
    def RUN_NEW(cls, isTest=False):
        """ -> MASTER PROCESSOR ID CREATED HERE <- """
        newClas = cls()
        newClas.isTest = isTest
        articles = ap.get_no_category_by_1000()
        arts = LIST.flatten(articles)
        for article in arts:
            if not article:
                continue
            newClas.process_article(article, isUpdate=False)

    @classmethod
    def RUN_UPDATE(cls, isTest=False):
        """ -> MASTER PROCESSOR ID CREATED HERE <- """
        newClas = cls()
        newClas.isTest = isTest
        articles = ap.get_date_range_list(20)
        arts = LIST.flatten(articles)
        for article in arts:
            if not article:
                continue
            newClas.process_article(article, isUpdate=True)

    # -> Master Runner of Single Article
    def process_article(self, article, isUpdate):
        updated_date = DICT.get("updatedDate", article, False)
        source = DICT.get("source", article, "False")
        if not isUpdate and updated_date or source == "twitter" or source == "reddit":
            return
        if isUpdate and updated_date == LAST_UPDATE:
            return
        # -> Setup
        id = DICT.get("_id", article)
        Log.i(f"Enhancing Article ID=[ {id} ]")
        title = DICT.get("title", article)
        body = DICT.get("body", article)
        description = DICT.get("description", article)
        # -> Combine All Main Content (Title, Body, Description)
        content = Language.combine_args_str(title, body, description)
        # -> Enhancers
        enhanced_article = enhance_article(article=article, content=content)
        # -> Update Article in MongoDB
        if not self.isTest:
            ap.update_article_in_database(enhanced_article)


if __name__ == "__main__":
    test = "ACEY2025: 3D Tower Defense Game That virtual world Takes You to the Metaverse on Mars - Bitcoinist"
    ArticleProcessor.RUN_NEW(isTest=False)