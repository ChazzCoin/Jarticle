from Jarticle.jArticles import jArticles
from FSON import DICT
from FList import LIST
from fairNLP import Language
from fopTopic.Topic import Topic

from FLog.LOGGER import Log
Log = Log("Engine.Processor.TopicProcessor")

# UNKNOWN = "Unknown"
# UNSURE = "Unsure"
# UNCATEGORIZED = [UNSURE, UNKNOWN]
TOPIC = Topic.ALL_CATEGORIES()
JARTICLE = jArticles.constructor_jarticles()

class TopicProcessor:
    j = None
    categories = {}
    topic_name = ""
    topic = None
    all_scores = []
    overall_top_words = {}
    matched_words_by_hookup = {}  # { "<hookup.id>": { "word": 10 } }
    processed_hookups = []

    """
    -> 1. Add Hookups freely
    -> 2. Then .start()
    """

    # def __init__(self):
    #     self.j = jArticles.constructor_jarticles()
    #     articles = JARTICLE.get_articles_last_day_not_empty()
    #     if articles:
    #         self.init_list_of_articles(articles)

    # -> Master Runner
    def init_list_of_articles(self, articles):
        # X. - Topic PROCESSOR - Loop all raw hookups, score/process each one.
        for article in articles:
            try:
                # -> SET tickers from TICKER PROCESSOR
                # hookup.tickers = DICT.add(self.tickerProcessor.all_tickers_by_hookup[hookup.id], hookup.tickers)
                # -> BEGIN
                self.process_single_article_v1(article)
            except Exception as e:
                Log.e(f"Failed to process hookup. hookup= [ {article} ] ", error=e)
                # return article

    def process_single_article_v1(self, article, isUpdate=False):
        try:
            id = DICT.get("_id", article)
            cat_attempt = DICT.get("category", article, False)
            if not isUpdate and cat_attempt:
                return article
            Log.d(f"process_single_article_v1: article={id}")
            title = DICT.get("title", article)
            description = DICT.get("description", article)
            body = DICT.get("body", article)
            content = Language.combine_args_str(title, description, body)
            # -> Score/Match Content
            main_cats = TOPIC.main_categorizer(content)
            sub_cats = TOPIC.sub_categorizer(content)
            # -> Remove matched topics with low scores
            # -> Main Variables
            highest_main_cat_name = LIST.get(0, main_cats)
            highest_main_score = LIST.get(1, main_cats)
            matched_main_terms = LIST.get(2, main_cats)
            # -> Sub Variables
            highest_topic_name = LIST.get(0, sub_cats)

            if highest_topic_name == "metaverse":
                # take secondary list and add scores...
                pass



            highest_score = LIST.get(1, sub_cats)
            matched_terms = LIST.get(2, sub_cats)
            Log.d(f"Setting ALL Variables: article={id}")
            # -> MAIN CATEGORY
            article["category"] = highest_main_cat_name
            article["category_scores"] = matched_main_terms
            article["score"] = highest_main_score
            # -> SUB CATEGORY
            article["sub_category"] = highest_topic_name
            article["sub_category_scores"] = matched_terms
            article["sub_score"] = highest_score
            return article
        except Exception as e:
            print(f"Failed: {e}")
            return article


    """ UNTESTED FUNCTIONS """
    def place_article_in_category_list(self, topic_name, article):
        if self.categories.__contains__(topic_name):
            temp_list = self.categories[topic_name]
            temp_list.append(article)
            self.categories[topic_name] = temp_list
        else:
            self.categories[topic_name] = [article]



if __name__ == '__main__':
    TopicProcessor()