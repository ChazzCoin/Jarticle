from Topics import Resources
from Topics.Categories import MainCategories, SubCategories, Categorizer
from Topics.Resources import Sources

MAIN_CATEGORY_NAMES = MainCategories.get_main_category_names()
SUB_CATEGORY_NAMES = SubCategories.get_sub_category_names()
MAIN_CATEGORY_LIST = MainCategories.keys

"""
::TODO::
When a topic is requested, this class should build all the lists and sources for that topic.
- Each client should get passed this object and use it to do all its searching/matching.
"""
class Topic:
    main_category_names = MAIN_CATEGORY_NAMES
    main_category_keys = MAIN_CATEGORY_LIST
    main_categories = {}
    sub_categories = {}
    sources = {}

    @classmethod
    def ALL_CATEGORIES(cls):
        newCls = cls()
        newCls.build_main_categories()
        newCls.build_sub_categories()
        newCls.build_sources()
        newCls.get_resource_urls()
        return newCls

    @classmethod
    def RUN_FULL_CATEGORIZER(cls, content) -> { str: { str: ( int, { str: int } ) } }:
        newCls = cls()
        newCls.build_main_categories()
        newCls.build_sub_categories()
        newCls.main_categorizer(content)
        newCls.sub_categorizer(content)
        return { "main_categories": newCls.main_categorizer(content),
                 "sub_categories": newCls.sub_categorizer(content) }

    @classmethod
    def RUN_MAIN_CATEGORIZER(cls, content):
        newCls = cls()
        newCls.build_main_categories()
        return newCls.main_categorizer(content)

    @classmethod
    def RUN_SUB_CATEGORIZER(cls, content):
        newCls = cls()
        newCls.build_sub_categories()
        return newCls.sub_categorizer(content)

    # -> Main -> Build All Main Categories -> Dict {}
    def build_main_categories(self, categories: [] = None):
        if categories is None:
            categories = MainCategories.get_main_category_names()
        """  DYNAMIC {JSON/DICT} BUILDER  """
        for category in categories:
            if category == "keys" or str(category).startswith("__"):
                continue
            category = category.lower()
            self.main_categories[category] = self.build_single_main_category(category)

    # -> Main -> Build Single Main Category into Dict {}
    def build_single_main_category(self, category) -> {}:
        temp_json = {}
        for term in self.main_category_keys:
            temp_json[term] = self.get_main_category_var(self.combine_var_name(category, term))
            if term == "rss_feeds":
                # -> Add Both Lists (Terms and sources)
                temp_json[term] = temp_json[term] + Sources().master_rss_list
        return temp_json

    # -> SUB -> Build All Sub Categories into Dict {}
    def build_sub_categories(self) -> {}:
        temp_json = {}
        for sub_cat in SUB_CATEGORY_NAMES:
            temp_json[sub_cat] = self.get_sub_category_var(sub_cat)
        self.sub_categories = temp_json

    """ -> SOURCES <- """
    def build_sources(self) -> {}:
        temp_json = {}
        for key in Sources.__dict__.keys():
            value = Topic.get_source_var(key)
            temp_json[key] = value
        self.sources = temp_json

    def get_resource_urls(self):
        google_sources = Resources.get_google_sources()
        popular_sources = Resources.get_popular_sources()
        rss_sources = Resources.get_rss_sources()
        self.set_source("google_sources", google_sources)
        self.set_source("popular_sources", popular_sources)
        self.set_source("rss_sources", rss_sources)

    def set_source(self, key, value):
        self.sources[key] = value

    def sub_categorizer(self, *content):
        return Categorizer.categorize(content=content, categories=self.sub_categories)

    def main_categorizer(self, *content):
        return Categorizer.categorize(content=content, categories=self.main_categories)

    @staticmethod
    def get_main_category_var(var_name):
        """  GETTER HELPER  """
        return MainCategories().__getattribute__(var_name)

    @staticmethod
    def get_sub_category_var(var_name):
        """  GETTER HELPER  """
        return SubCategories().__getattribute__(var_name)

    @staticmethod
    def get_source_var(var_name):
        """  GETTER HELPER  """
        return Sources().__getattribute__(var_name)

    @staticmethod
    def combine_var_name(topic, term):
        return topic + "_" + term



if __name__ == "__main__":
    # print(TERMS_LIST)
    cont = "hey this is the worlds basketball dumbest content about economy business ripple and of course, the metaverse itself!!! soccer, taxes virtual real estate and all kinds of bitcoin!"
    t = Topic.ALL_CATEGORIES()
    result = t.sub_categorizer(cont)
    print(result)