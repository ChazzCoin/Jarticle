

from FSON import DICT
from FDate import DATE
from Jarticle.jArticles import jArticles
jdb = jArticles.constructor_jarticles()

def get_last_day_not_empty():
    return jdb.get_articles_last_day_not_empty()

def get_no_category_by_date(date, artsOnly=True):
    if artsOnly:
        return jdb.get_only_articles_no_category_by_date(date)
    return jdb.get_articles_no_category_by_date(date)

def get_no_category_by_1000():
    return jdb.get_only_articles_no_category()


# -> MongoDB
def update_article_in_database(article: {}):
    _id = DICT.get("_id", article)
    return jdb.replace_article(_id, article)

def get_date_range_list(daysBack):
    daysbacklist = DATE.get_range_of_dates_by_day(DATE.mongo_date_today_str(), daysBack)
    tempListOfArticles = []
    for day in daysbacklist:
        tempArts = jdb.get_articles_by_date(day)
        tempListOfArticles.append(tempArts)
    return tempListOfArticles

def get_no_category_date_range_list(daysBack):
    daysbacklist = DATE.get_range_of_dates_by_day(DATE.mongo_date_today_str(), daysBack)
    tempListOfArticles = []
    for day in daysbacklist:
        tempArts = get_no_category_by_date(day)
        tempListOfArticles.append(tempArts)
    return tempListOfArticles

if __name__ == '__main__':
    t = get_no_category_date_range_list(10)
    print(t)