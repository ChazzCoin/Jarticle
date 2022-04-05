from Config import config
from FAIR.Core import DICT
from FAIR.FUNDLE.CoreTerms import Terms
from FAIR.FUNDLE import Sources
from FAIR.Logger import Log
Log = Log("Config.Topic")

def get_topic_variables():
    test = Terms.__dict__.keys()
    variables = []
    for item in test:
        if not item.startswith("__") and item.__contains__("_"):
            variables.append(item)
    return variables


def get_topic_names():
    test = Terms.__dict__.keys()
    variables = []
    for item in test:
        if str(item).startswith("__"):
            continue
        elif str(item).startswith("keys"):
            continue
        elif str(item).__contains__("_"):
            continue
        else:
            variables.append(item)
    return variables


TOPIC_NAMES = get_topic_names()
TERMS_LIST = Terms.keys

"""
::TODO::
When a topic is requested, this class should build all the lists and sources for that topic.
- Each client should get passed this object and use it to do all its searching/matching.
"""
class Topic:
    name = ""
    topic_names = TOPIC_NAMES
    keys = TERMS_LIST
    stop_words = []
    topics = {}
    test_topics = {}

    def __init__(self, topicName=None):
        if topicName:
            self.name = topicName.lower()
        else:
            self.name = "General"
        self.stop_words = self.load_stopwords()
        Log.i(f"Init all Sources with Topic={topicName}")
        self.build_topics(topics=self.topic_names)

    # -> Get Topic Dict with terms
    def get_topic(self, topic_name=None):
        if not topic_name:
            topic_name = self.name
        return self.topics[topic_name.lower()]

    # -> Weighted Terms
    def get_topic_weighted_terms(self, topic_name=None):
        if not topic_name:
            topic_name = self.name
        temp_dict = self.topics[topic_name.lower()]
        weighted_terms = temp_dict["weighted_terms"]
        return weighted_terms

    # -> RSS Feeds
    def get_topic_rss_feeds(self, topic_name=None):
        if not topic_name:
            topic_name = self.name
        temp_dict = self.topics[topic_name.lower()]
        rss_feeds = temp_dict["rss_feeds"]
        return rss_feeds

    # -> Search Terms
    def get_topic_search_terms(self, topic_name=None):
        if not topic_name:
            topic_name = self.name
        temp_dict = self.topics[topic_name.lower()]
        search_terms = temp_dict["search_terms"]
        return search_terms

    def get_all_test_search_terms_for_topic(self, topic):
        topic = topic.lower()
        search_terms = []
        for topic_name in self.topics:
            if topic != topic_name:
                continue
            temp_dict = self.topics[topic_name]
            search_terms = temp_dict["search_terms_test"]
        return search_terms

    def get_all_weighted_terms(self):
        for topic in self.topics:
            temp_dict = self.topics[topic]
            for _ in temp_dict:
                self.all_weighted_terms = DICT.merge_dicts(self.all_weighted_terms, temp_dict["weighted_terms"])

    def get_all_rss_feeds(self):
        rss_feeds = []
        for topic_name in self.topics:
            temp_dict = self.topics[topic_name]
            rss_feeds = temp_dict["rss_feeds"]
        all_feeds = rss_feeds + Sources.master_rss_list
        self.all_rss_feeds = all_feeds
        return all_feeds

    def get_var(self, var_name):
        """  GETTER HELPER  """
        return self.__getattribute__(var_name)

    def build_single_topic(self, topic):
        temp_json = {}
        for term in self.keys:
            temp_json[term] = self.get_term_var(self.combine_var_name(topic, term))
            if term == "rss_feeds":
                temp_json[term] = temp_json[term] + Sources.master_rss_list
        return temp_json

    def build_topics(self, topics: [] = None):
        if topics is None:
            topics = get_topic_names()
        """  DYNAMIC {JSON/DICT} BUILDER  """
        for topic in topics:
            if topic == "keys" or str(topic).startswith("__"):
                continue
            if topic == "rss_feeds":
                Log.i("build_topics: found key rss_feeds")
            topic = topic.lower()
            self.topics[topic] = self.build_single_topic(topic)

    @staticmethod
    def load_stopwords():
        from nltk.corpus import stopwords
        if config.LANGUAGE == config.GERMAN:
            stop_words = stopwords.words('german')
        else:
            stop_words = stopwords.words('english')
        stop_words.extend(Terms.extended_stop_words)
        Log.v("get_stopwords:", stop_words)
        return stop_words

    @staticmethod
    def get_term_var(var_name):
        """  GETTER HELPER  """
        return Terms().__getattribute__(var_name)

    @staticmethod
    def combine_var_name(topic, term):
        return topic + "_" + term


if __name__ == "__main__":
    print(TERMS_LIST)
    t = Topic()
    print(t)
