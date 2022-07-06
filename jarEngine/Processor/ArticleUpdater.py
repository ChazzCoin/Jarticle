from jarEngine.Enhancements import TopicProcessor_v1, SozinProcessor_v1 as sp
from jarEngine.Content.NLP import NLTK
from fairNLP import Language
from FList import LIST
from FSON import DICT
from FDate import DATE
from Core import Extractor
from jarDiscordAlert import Alert
from jarProvider import ArticleProvider as ap

from Jarticle.jCompany import jCompany
from FLog.LOGGER import Log

Log = Log("Jarticle.Engine.Processor.ArticleProcessor_v2")

WORDS = "words"
BODY = "body"
TITLE = "title"
DESCRIPTION = "description"

"""
-> Maintains the lifecycle of processing a list of hookups
"""

LAST_UPDATE = "May 19 2022"


def update_published_date(article):
    url = article["url"]
    tempDate = Extractor.Extractor.Extract_PublishedDate(url)
    if tempDate:
        return tempDate
    return False

def categorizer(article):
    return TopicProcessor_v1.TopicProcessor().process_single_article_v1(article, isUpdate=True)

def sozin(content):
    tickers = sp.extract_all(content)
    stock_tickers = LIST.get(0, tickers)
    crypto_tickers = LIST.get(1, tickers)
    Log.d("Tickers: " + str(tickers))
    if stock_tickers and crypto_tickers:
        return tickers
    elif stock_tickers:
        return stock_tickers
    elif crypto_tickers:
        return crypto_tickers
    return False


def get_company_reference(article):
    tickers = DICT.get("tickers", article)
    if not tickers:
        return False
    jc = jCompany.constructor_jcompany()
    references = {}
    for key in tickers:
        id = jc.get_company_id_for_ticker(key)
        if id and key not in references.keys():
            references[key] = id
    return references


def get_summary(article):
    body = DICT.get("body", article, default="False")
    summary = NLTK.summarize_v2(body, 4)
    # summary = Language.text_summarizer(body, 4)
    return summary


def get_keywords(article):
    title = DICT.get("title", article, default="False")
    body = DICT.get("body", article, default="False")
    keywords = NLTK.keywords(str(body) + str(title))
    newList = []
    for item in keywords:
        newList.append(item)
    return newList


def get_sentiment(content):
    sentiment = NLTK.get_content_sentiment(content)
    return sentiment


def get_source_page_rank(article):
    from jarEngine.Helper import PageRank
    url = DICT.get("url", article, "unknown")
    rank = PageRank.get_page_rank(url)
    return rank


# -> [MASTER]
def update_enhancements(article, content):
    # article = categorizer(article)
    # article["keywords"] = get_keywords(article)
    # article["summary"] = get_summary(article)
    # article["tickers"] = sozin(content)
    # article["company_ids"] = get_company_reference(article)
    # article["sentiment"] = get_sentiment(content)
    # article["source_rank"] = get_source_page_rank(article)
    # article["updatedDate"] = DATE.mongo_date_today_str()
    return article


def update_enhanced_summary(article):
    article["summary"] = get_summary(article)
    return article


# -> Processing Class Object
class ArticleProcessor:
    overall_count = 0
    success_count = 0
    isTest = False

    @classmethod
    def UPDATE_PUBLISHED_DATE(cls, isTest=False):
        """ -> MASTER PROCESSOR ID CREATED HERE <- """
        newClas = cls()
        newClas.isTest = isTest
        articles = ap.get_no_published_date_not_updated_today(unlimited=True)
        arts = LIST.flatten(articles)
        for article in arts:
            if not article:
                continue
            newClas.update_published_date(article)
        Log.i(f"UPDATED Published Date for {newClas.overall_count} Articles!")
        Log.i(f"Total Articles Touched: {newClas.overall_count}")
        Log.i(f"Total Articles Updated: {newClas.success_count}")

    @classmethod
    def RUN_UPDATE_METAVERSE(cls, isTest=False):
        """ -> MASTER PROCESSOR ID CREATED HERE <- """
        newClas = cls()
        newClas.isTest = isTest
        articles = ap.get_metaverse_articles()
        for article in articles:
            if not article:
                continue
            newClas.update_article(article, isUpdate=True)
        Log.i(f"Enhanced {newClas.overall_count} Articles!")

    def update_published_date(self, article):
        try:
            source = DICT.get("source", article, "False")
            if source == "twitter" or source == "reddit":
                return
            self.overall_count += 1
            self.log_beginning(article)
            published_date = update_published_date(article)
            if published_date:
                self.success_count += 1
                Log.s("Successfully Updated Published Date.")
                article["published_date"] = published_date
                article["updatedDate"] = DATE.mongo_date_today_str()
                # -> Update Article in MongoDB
                self.update_article_in_db(article)
            else:
                Log.w("Failed to Updated Published Date.")
                article["updatedDate"] = DATE.mongo_date_today_str()
                # -> Update Article in MongoDB
                self.update_article_in_db(article)
        except Exception as e:
            Log.e("Failed to updated article Date.", error=e)
            return

    # -> Master Runner of Single Article
    def update_article(self, article, isUpdate):
        # updated_date = DICT.get("updatedDate", article, False)
        source = DICT.get("source", article, "False")
        if source == "twitter" or source == "reddit":
            return
        # if isUpdate and updated_date == LAST_UPDATE:
        #     return
        # -> Setup
        self.overall_count += 1
        self.log_beginning(article)
        # -> Combine All Main Content (Title, Body, Description)
        content = self.prepare_content(article)
        # -> Updaters
        updated_article = update_enhancements(article=article, content=content)
        # -> Update Article in MongoDB
        self.update_article_in_db(updated_article)

    def update_article_in_db(self, updated_article):
        if not self.isTest:
            ap.update_article_in_database(updated_article)

    def log_beginning(self, article):
        id = DICT.get("_id", article)
        date = DICT.get("published_date", article, "unknown")
        Log.i(f"Updating Article ID=[ {id} ], DATE=[ {date} ], COUNT=[ {self.overall_count} ]")

    def prepare_content(self, article):
        title = DICT.get("title", article)
        body = DICT.get("body", article)
        description = DICT.get("description", article)
        # -> Combine All Main Content (Title, Body, Description)
        content = Language.combine_args_str(title, body, description)
        return content

if __name__ == "__main__":
    test = "ACEY2025: 3D Tower Defense Game That virtual world Takes You to the Metaverse on Mars - Bitcoinist"
    ArticleProcessor.UPDATE_PUBLISHED_DATE(isTest=False)