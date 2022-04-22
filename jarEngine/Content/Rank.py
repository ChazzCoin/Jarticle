
# -> Return rank with only 1 decimal place
# from Models.Hookup import Hookup
from jarEngine.Helper import PageRank
from jarFAIR.Core import FILE, DICT
from urllib.parse import urlparse
from jarFAIR.Logger.CoreLogger import Log

Log = Log("Engine.Content.Rank")

decimal_place = "%.1f"

def get_page_rank(url):
    """
    Caching Enabled!
    """
    url = urlparse(url).netloc
    cache = FILE.load_dict_from_file("page_rank")
    if cache is not None:
        result = DICT.get(url, cache)
        if result:
            Log.v("Page Rank is Cached!")
            return result
    try:
        providers = PageRank.AlexaTrafficRank()
        Log.v("Grabbing fresh Page Rank for: %s" % (url))
        rank = providers.get_rank(url)
        temp = DICT.merge_dicts(cache, { url: rank })
        FILE.save_dict_to_file("page_rank", temp, FILE.data_path)
    except Exception as e:
        Log.e("Page Rank Failed", error=e)
        rank = None
    Log.d(f"URL: {url}, Rank: {rank}")
    return rank

# highest score divided by 10 = rank_increment
def get_highest_score(list_of_scores) -> float:
    highest_score = 0
    for score in list_of_scores:
        if float(score) > float(highest_score):
            highest_score = score
    Log.d(f"Highest Score: {float(highest_score)}")
    return float(highest_score)

def get_highest_rank(list_of_hookups) -> float:
    highest_rank = 0.0
    for hookup in list_of_hookups:
        rank = hookup.rank
        if float(rank) > float(highest_rank):
            highest_rank = rank
    Log.d(f"Highest Rank: {float(highest_rank)}")
    return float(highest_rank)

def get_highest_ranked_hookup(list_of_hookups):
    highest_rank = list_of_hookups[0]
    for hookup in list_of_hookups:
        rank = hookup.get("rank")
        if float(rank) > float(highest_rank.get("rank")):
            highest_rank = hookup
    return highest_rank

# -> Highest Score Wins.
def get_rank(current_score: float, list_of_scores: []) -> float:
    # Protection.
    if current_score not in list_of_scores:
        Log.v(f"Adding {current_score}")
        list_of_scores.append(float(current_score))
    list_of_scores.sort(reverse=True)
    # TODO: -> Save list of scores.
    Log.v(list_of_scores)
    rank = 0
    for current in list_of_scores:
        if current_score == current:
            return rank + 1
        rank += 1
    return False


if __name__ == "__main__":
    score = 32.3
    scores = [123.4, 232.3, 23, 902.3, 10.5, 1003.43, 123.42, 100]
    scores_sorted = [1003.43, 902.3, 232.3, 123.42, 123.4, 100, 23, 10.5]
    print(get_rank(score, scores))
    # print(get_page_rank("https://www.fs.com/dfsgfgd/gh/fgh"))
