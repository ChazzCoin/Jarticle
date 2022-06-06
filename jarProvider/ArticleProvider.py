
from FSON import DICT
from FDate import DATE
from Jarticle.jArticles import jArticles
jdb = jArticles.constructor_jarticles()

# -> MongoDB
def update_article_in_database(article: {}):
    _id = DICT.get("_id", article)
    return jdb.replace_article(_id, article)

def get_date_range_list(daysBack):
    daysbacklist = DATE.get_range_of_dates_by_day(DATE.mongo_date_today_str(), daysBack)
    tempListOfArticles = []
    for day in daysbacklist:
        tempArts = jdb.get_articles_by_date(day, unlimited=True)
        if tempArts:
            tempListOfArticles.append(tempArts)
    return tempListOfArticles

def get_no_category_date_range_list(daysBack):
    daysbacklist = DATE.get_range_of_dates_by_day(DATE.mongo_date_today_str(), daysBack)
    tempListOfArticles = []
    for day in daysbacklist:
        tempArts = get_no_category_by_date(day)
        if tempArts:
            tempListOfArticles.append(tempArts)
    return tempListOfArticles

def get_last_day_not_empty():
    temp = jdb.get_articles_last_day_not_empty()
    if temp and len(temp) > 0:
        return temp
    return False

def get_no_category_by_date(date, artsOnly=True):
    if artsOnly:
        return jdb.get_only_articles_no_category_by_date(date)
    return jdb.get_articles_no_category_by_date(date)

def get_no_category_by_1000():
    temp = jdb.get_only_articles_no_category()
    if temp and len(temp) > 0:
        return temp
    return False

def get_no_category_last_7_days():
    temp = get_no_category_date_range_list(7)
    returnList = []
    if temp and len(temp) > 0:
        for item in temp:
            if not item:
                continue
            returnList.append(item)
        if len(temp) > 0:
            return temp
    return False

def get_ready_to_enhance():
    temp = get_no_category_last_7_days()
    if temp:
        return temp
    temp2 = get_no_category_by_1000()
    if temp2:
        return temp2
    return False

if __name__ == '__main__':
    t = get_no_category_date_range_list(10)
    print(t)