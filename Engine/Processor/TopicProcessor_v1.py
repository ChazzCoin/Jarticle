from Engine.Content import Score
from Engine.Content.NLP import NLTK
import FAIR
from FAIR.Core import DICT, LIST

from rsLogger import Log
Log = Log("Engine.Processor.TopicProcessor")

UNKNOWN = "Unknown"
UNSURE = "Unsure"
UNCATEGORIZED = [UNSURE, UNKNOWN]

class TopicProcessor:
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

    def __init__(self, topic, hookups=None):
        self.topic = topic
        if hookups:
            self.init_list_of_hookups(hookups)

    # -> Master Runner
    def init_list_of_hookups(self, hookups):
        # X. - Topic PROCESSOR - Loop all raw hookups, score/process each one.
        for hookup in hookups:
            try:
                # -> SET tickers from TICKER PROCESSOR
                # hookup.tickers = DICT.add(self.tickerProcessor.all_tickers_by_hookup[hookup.id], hookup.tickers)
                # -> BEGIN
                self.process_single_hookup_v2(hookup)
            except Exception as e:
                Log.e(f"Failed to process hookup. hookup= [ {hookup} ] ", error=e)

    def process_single_hookup_v2(self, hookup):
        Log.d(f"analyze_single_hookup: hookup={hookup.id}")
        content = FAIR.Language.combine_args_str(hookup.title, hookup.description, hookup.body)
        # -> Score/Match Content
        Log.d(f"Scoring Hookup: hookup={hookup.id}")
        scores_by_topic = Score.score_content_v3(content, topic=self.topic)  # { "topic": ( 50, { "word": 5 } ) }
        # -> Remove matched topics with low scores
        matched_topics = self.remove_empty_scores(scores_by_topic)
        # -> Temp Variables
        highest_topic_name = LIST.get(0, matched_topics)
        highest_score = LIST.get(1, matched_topics)
        matched_terms = LIST.get(2, matched_topics)
        # -> Check Score...
        if highest_score < 200:
            highest_topic_name = UNKNOWN
        elif highest_score < 500:
            highest_topic_name = UNSURE
        Log.d(f"Setting Variables: hookup={hookup.id}")
        hookup.category = highest_topic_name
        Log.d(f"Categorizing Hookup: hookup={hookup.id}")
        self.categorize_hookup(highest_topic_name, hookup)
        Log.d(f"Set Matched Terms: hookup={hookup.id}")
        hookup.category_scores = matched_terms
        Log.d(f"Set Sentiment: hookup={hookup.id}")
        hookup.sentiment = NLTK.get_content_sentiment(content, self.topic)
        Log.d(f"Set Summary: hookup={hookup.id}")
        hookup.summary = self.get_summary(hookup=hookup)
        # LOCAL -> Set Scoring / Ranking
        hookup.score = highest_score
        Log.d(f"Set Matched Words: hookup={hookup.id}")
        if matched_terms:
            if highest_topic_name not in UNCATEGORIZED:
                self.matched_words_by_hookup[hookup.id] = LIST.get(1, matched_terms[highest_topic_name], default=[])
            # GLOBAL -> Set Overall Top Words
            Log.d(f"Setting overall top words: hookup={hookup.id}")
            for key in matched_terms.main_category_keys():
                temp_tup = DICT.get(key, matched_terms)
                temp_dict = LIST.get(1, temp_tup)
                self.overall_top_words = DICT.add(temp_dict, self.overall_top_words)
        Log.d(f"Add Score to Global List: hookup={hookup.id}")
        self.all_scores.append(float(hookup.score))
        Log.d(f"Add to Pre-Sorted Hookups: hookup={hookup.id}")
        self.processed_hookups.append(hookup)
        Log.d(f"Single Hookup Processed: hookup={hookup.id}")

    def categorize_hookup(self, topic_name, hookup):
        if self.categories.__contains__(topic_name):
            temp_list = self.categories[topic_name]
            temp_list.append(hookup)
            self.categories[topic_name] = temp_list
        else:
            self.categories[topic_name] = [hookup]

    def remove_empty_scores(self, all_scores):
        highest_score = 0
        cat_scores = {}
        highest_topic_name = ""
        for topic_name in self.topic.main_category_names:
            result = all_scores[topic_name]
            score = LIST.get(0, result)
            if score and score > 1:
                if score > highest_score:
                    highest_score = score
                    highest_topic_name = topic_name
                cat_scores[topic_name] = result
        return highest_topic_name, highest_score, cat_scores

    def get_summary(self, hookup):
        summary = NLTK.summarize(self.topic, hookup.title if hookup.title else "", hookup.body, 2)
        return summary