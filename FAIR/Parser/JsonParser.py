from FAIR.Core import DICT, DATE
from FAIR.Logger.CoreLogger import Log
from FAIR.Parser import Keys

Log = Log("FAIR.Parser.JsonParser")

keys = Keys.keys

def parse(data, parseAll=False) -> {}:
    Log.d("Parsing data IN", v=f"=[ {data} ]")
    try:
        json_obj = {}
        json_obj["author"] = DICT.get_all(data, keys("author"), force_type=True)
        json_obj["title"] = DICT.get_all(data, keys("title"), force_type=True)
        json_obj["description"] = DICT.get_all(data, keys("description"), force_type=True)
        json_obj["body"] = DICT.get_all(data, keys("body"), force_type=True)
        json_obj["url"] = DICT.get_all(data, keys("url"), force_type=True)
        json_obj["img_url"] = DICT.get_all(data, keys("imgUrl"), force_type=True)
        json_obj["source"] = DICT.get_all(data, keys("source_url"), force_type=True)
        json_obj["tickers"] = DICT.get_all(data, keys("tickers"))
        json_obj["tags"] = DICT.get_all(data, keys("tags"))
        temp_date = DICT.get_all(data, keys("published_date"))
        json_obj["published_date"] = DATE.parse(temp_date)

        if parseAll:
            json_obj["summary"] = DICT.get("summary", data)
            json_obj["comments"] = DICT.get_all(data, keys("comments"))
            json_obj["source_rank"] = DICT.get("source_rank", data)
            json_obj["category"] = DICT.get("category", data)
            json_obj["sentiment"] = DICT.get("sentiment", data)
            json_obj["category_scores"] = DICT.get("category_scores", data)
            json_obj["score"] = DICT.get("score", data)
            json_obj["title_score"] = DICT.get("title_score", data)
            json_obj["description_score"] = DICT.get("description_score", data)
            json_obj["body_score"] = DICT.get("body_score", data)

        Log.v(f"Parsing data OUT=[ {json_obj} ]")
        return json_obj
    except Exception as e:
        Log.e(f"Failed to parse data=[ {data} ]", e)
        return None


def parse_from_reddit_client(raw_post):
    json_objc = {}
    author = DICT.get("author", raw_post)
    json_objc["author"] = DICT.get("name", author)
    json_objc["title"] = DICT.get("title", raw_post)
    json_objc["body"] = DICT.get("selftext", raw_post)
    json_objc["up_votes"] = DICT.get("ups", raw_post)
    json_objc["upvote_ratio"] = DICT.get("upvote_ratio", raw_post)
    json_objc["score"] = DICT.get("score", raw_post)
    json_objc["url"] = DICT.get("url", raw_post)
    json_objc["comments"] = parse_comments_into_json_list(raw_post.comments)
    json_objc["comment_count"] = DICT.get("num_comments", raw_post)
    dt = DATE.convert_reddit_to_datetime(DICT.get("created_utc", raw_post))
    json_objc["published_date"] = DATE.parse(dt)
    json_objc["source"] = "reddit"
    return json_objc

def parse_comments_into_json_list(comments):
    temp_list = []
    for comment in comments:
        try:
            user_name = comment.author.name
            if user_name == "AutoModerator":
                continue
        except Exception as e:
            Log.d("No User for Comment", e)
            continue
        dt = DATE.convert_reddit_to_datetime(comment.created_utc)
        temp_json = {
            "author": user_name,
            "body": comment.body,
            "up_votes": comment.ups,
            "published_date": dt
        }
        temp_list.append(temp_json)
    return temp_list
