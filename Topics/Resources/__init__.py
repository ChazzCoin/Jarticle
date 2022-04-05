from Topics.Resources.Sources import Sources
import os
from pathlib import Path
import feedparser
import random

def get_parent_directory():
    path = Path(os.getcwd())
    return path.parent.absolute().__str__()

TRENDING_URL = 'http://www.google.com/trends/hottrends/atom/feed?pn=p1'

def google_trends():
    """Returns a list of hit terms via google trends
    """
    try:
        listing = feedparser.parse(TRENDING_URL)['entries']
        trends = [item['title'] for item in listing]
        return trends
    except Exception as e:
        print('ERR hot terms failed!', str(e))
        return None

if __name__ == '__main__':
    print(google_trends())

GOOGLESOURCES = os.path.join(os.getcwd(), 'Topics/Resources/google_sources.txt')
POPULARSOURCES = os.path.join(os.getcwd(), 'Topics/Resources/popular_sources.txt')
RSSSOURCES = os.path.join(os.getcwd(), 'Topics/Resources/popular_sources.txt')

class Resource:
    GOOGLE_SOURCES = GOOGLESOURCES
    POPULAR_SOURCES = POPULARSOURCES
    RSS_SOURCES = RSSSOURCES

def get_random(items):
    selection = random.randint(0, len(items) - 1)
    return items[selection]

def get_google_sources():
    return get_resource(Resource.GOOGLE_SOURCES)

def get_popular_sources():
    return get_resource(Resource.POPULAR_SOURCES)

def get_rss_sources():
    return get_resource(Resource.RSS_SOURCES)

def get_resource(resource):
    """Uses generator to return next useragent in saved file
    """
    with open(resource, 'r') as f:
        urls = ['http://' + u.strip() for u in f.readlines()]
        return urls

# def clean_resource_urls(list_of_urls):
#     new_list = []
#     for item in list_of_urls:
#         newitem = str(item).strip()
#         new_list.append(newitem)
#     return new_list
