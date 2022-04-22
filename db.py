
""" Welcome to Fongo! The pyFongo connection handler. """

# TODO: MASTER IMPORT FOR DATABASE MODULE
from M.MDB import DEFAULT_HOST_INSTANCE
from Jarticle.jURL import jURL
from Jarticle.jArticles import jArticles

DATABASE_INSTANCE = DEFAULT_HOST_INSTANCE
dbURL = jURL
dbArticles = jArticles
collectionArticles = dbArticles.constructor_jarticles()

def getArticlesToday(strDate):
    return collectionArticles.get_articles_by_date(strDate)

def getArticlesLastDayWithArticles():
    return collectionArticles.get_articles_last_day_not_empty()


