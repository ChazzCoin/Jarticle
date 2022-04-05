from FAIR.Core import DICT, DATE
from FAIR.Logger.CoreLogger import Log
import uuid

Log = Log("FAIR.Parser.HookupParser")

potential_keys = {
        "author": ["author", "authors", "screen_name", "user"],
        "title": ["title"],
        "body": ["body", "text", "full_text"],
        "description": ["description", "meta_description"],
        "published_date": ["published_date", "publish_date", "created_at", "parsely-pub-date"],
        "url": ["url", "urls"],
        "imgUrl": ["imgUrl", "meta_img", "profile_image_url"],
        "tags": ["tags", "parsely-tags", "keywords", "meta_keywords", "news_keywords", "parsely-section", "parsely-type"],
        "source_url": ["source_url", "source"],
        "tickers": ["tickers"],
        "companies": ["companies"],
    }


def keys(key) -> []:
    return potential_keys[key]

class Parser:

    @staticmethod
    def parse_list(data, parseAll=False):
        temp_final = []
        for item in data:
            hookup = Parser.parse(item, parseAll=parseAll)
            temp_final.append(hookup)
        return temp_final

    @staticmethod
    def parse(data, parseAll=False):
        Log.d("Parsing data IN", v=f"=[ {data} ]")
        try:
            hookup = Hookup()
            hookup.author = DICT.get_all(data, keys("author"), force_type=True)
            hookup.title = DICT.get_all(data, keys("title"), force_type=True)
            hookup.description = DICT.get_all(data, keys("description"), force_type=True)
            hookup.body = DICT.get_all(data, keys("body"), force_type=True)
            hookup.url = DICT.get_all(data, keys("url"), force_type=True)
            hookup.img_url = DICT.get_all(data, keys("imgUrl"), force_type=True)
            hookup.source = DICT.get_all(data, keys("source_url"), force_type=True)
            hookup.tickers = DICT.get_all(data, keys("tickers"))
            hookup.tags = DICT.get_all(data, keys("tags"))
            temp_date = DICT.get_all(data, keys("published_date"))
            hookup.published_date = DATE.parse(temp_date)

            if parseAll:
                hookup.summary = DICT.get("summary", data)
                hookup.comments = DICT.get("comments", data)
                hookup.source_rank = DICT.get("source_rank", data)
                hookup.category = DICT.get("category", data)
                hookup.sentiment = DICT.get("sentiment", data)
                hookup.category_scores = DICT.get("category_scores", data)
                hookup.score = DICT.get("score", data)
                hookup.title_score = DICT.get("title_score", data)
                hookup.description_score = DICT.get("description_score", data)
                hookup.body_score = DICT.get("body_score", data)
                hookup.rank = DICT.get("rank", data)

            Log.v(f"Parsing data OUT=[ {hookup} ]")
            return hookup
        except Exception as e:
            Log.e(f"Failed to parse data=[ {data} ]", e)
            return None

    @staticmethod
    def to_json(hookup):
        Log.d(f"to_json: IN: {hookup}")
        json = {
            "id": hookup.id,
            "author": hookup.author,
            "title": hookup.title,
            "description": hookup.description,
            "body": hookup.body,
            "summary": hookup.summary,
            "tickers": hookup.tickers,
            "comments": hookup.comments,
            "published_date": hookup.published_date,
            "img_url": hookup.img_url,
            "url": hookup.url,
            "source": hookup.source,
            "source_rank": hookup.source_rank,
            "category": hookup.category,
            "sentiment": hookup.sentiment,
            "category_scores": hookup.category_scores,
            "score": hookup.score,
            "title_score": hookup.title_score,
            "description_score": hookup.description_score,
            "body_score": hookup.body_score,
            "rank": hookup.rank
        }
        Log.v(f"to_json: OUT: {json}")
        return json


class Hookup(object):
    id = ""
    processed = False
    author = ""
    # -> Content
    title: str = ""
    description = ""
    body = ""
    comments = ""
    summary = ""
    tags = ""
    # -> Date
    published_date = ""
    # -> Urls
    img_url = ""
    url = ""
    # -> Source
    source = ""
    source_rank = 0
    category = ""
    # -> Process...
    tickers = {}  # { "stocks": { "BB": 22 }, "crypto": { "MANA": 16 } }
    sentiment = {}
    category_scores = {}
    score = 0
    title_score = 0
    description_score = 0
    body_score = 0
    rank = 0

    def __init__(self):
        self.id = str(uuid.uuid4())

    @staticmethod
    def convert_list_to_archive_json(list_of_hookups):
        temp = []
        if not list_of_hookups:
            return temp
        for hookup in list_of_hookups:
            j = Hookup.to_archive_json(hookup)
            temp.append(j)
        return temp

    @staticmethod
    def to_archive_json(data):
        Log.v(f"to_archive_json: IN: {data}")
        json = {
            "author": DICT.get("author", data),
            "title": DICT.get("title", data),
            "description": DICT.get("description", data),
            "body": DICT.get("body", data),
            "tags": DICT.get("tags", data),
            "published_date": DICT.get("published_date", data),
            "img_url": DICT.get("img_url", data),
            "url": DICT.get("url", data),
            "source": DICT.get("source", data),
        }
        Log.v(f"to_archive_json: OUT: {json}")
        return json

    @staticmethod
    def to_file_json(data):
        from Utils import DICT
        Log.v(f"to_file_json: IN: {data}")
        try:
            json = {
                "source": DICT.get("source", data),
                "source_rank": DICT.get("source_rank", data),
                "author": DICT.get("author", data),
                "category": DICT.get("category", data),
                "description": DICT.get("description", data),
                "url": DICT.get("url", data),
                "tickers": DICT.get("tickers", data),
                "sentiment": DICT.get("sentiment", data),
                "title_score": DICT.get("title_score", data),
                "description_score": DICT.get("description_score", data),
                "body_score": DICT.get("body_score", data),
                "score": DICT.get("score", data),
                "rank": DICT.get("rank", data),
                "category_scores": DICT.get("category_scores", data)
            }
            return json
        except Exception as e:
            Log.e("Failed to parse hookup into json.", error=e)
            return data

    @staticmethod
    def sort_by_date(list_of_hookups) -> dict:
        try:
            from Utils import DICT
            by_date = {}
            for hookup in list_of_hookups:
                temp_date = DICT.get("published_date", hookup)
                if by_date.__contains__(temp_date):
                    temp_list = by_date[temp_date]
                    temp_list.append(hookup)
                    by_date[temp_date] = temp_list
                else:
                    by_date[temp_date] = [hookup]
            return by_date
        except Exception as e:
            Log.e("Failed to sort hookups by date.", error=e)
            return list_of_hookups

    @staticmethod
    def get_top_ranked(hookups):
        highest = []
        if len(hookups) < 1 or hookups is None:
            return highest
        highest = hookups[0]
        for hookup in hookups:
            if hookup.rank > highest.rank:
                highest = hookup
        return highest

    @staticmethod
    def sort_hookups_by_rank(hookups, reversed=True):
        Log.v(f"sort_hookups_by_rank: IN: {hookups}")
        sorted_hookups = sorted(hookups, key=lambda k: k.get("rank"), reverse=reversed)
        return sorted_hookups

    @staticmethod
    def sort_hookups_by_score(hookups, reversed=True):
        Log.v(f"sort_hookups_by_score: IN: {hookups}")
        sorted_hookups = sorted(hookups, key=lambda k: k.get("score"), reverse=reversed)
        return sorted_hookups
