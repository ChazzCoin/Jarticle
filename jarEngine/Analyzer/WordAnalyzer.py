
import jarFAIR
from Mongodb.MongoArchive import MongoArchive
from jarFAIR.Core import DICT, DATE, LIST, Ext

"""
-> This Analyzer will grab each day from the archive
    - Count all words.
    - Take the top 200
    - Save into new db for words by date.

    FAIR.completeTokenization

"""

TOKENS = "tokens"
BI_GRAMS = "bi_grams"
TRI_GRAMS = "tri_grams"
QUAD_GRAMS = "quad_grams"


class Analyzer(MongoArchive):
    topic = Topic()
    original_dates = []
    raw_content = None
    archive_ids = []
    archive_dates = []
    current_date = str(DATE.get_now_date())
    original_hookups = []
    # Raw Words
    single_grams = []
    bi_grams = []
    tri_grams = []
    quad_grams = []
    # Counts
    single_grams_count = {}
    bi_grams_count = {}
    tri_grams_count = {}
    quad_grams_count = {}
    # Query
    insertQuery = {}

    def __init__(self):
        super().__init__()

    """
        -> RUNNERS
    """
    # Run Dates in Archive
    @Ext.safe_args
    def run_archive_dates(self, dates):
        """ Add Dates, Get Archives, Parse Hookups -> Start """
        self.original_dates = dates
        for date in self.original_dates:
            self.set_hookups_from_archive(date)
        self.start()

    # Run New Hookups
    def run_hookups(self, hookups: []):
        """ Add Hookups -> Start """
        self.add_hookups(hookups)
        self.start()

    # Run Any String Content
    def run_raw_content(self, raw_content: str):
        """ Add String Content -> Start """
        self.raw_content = raw_content
        self.start()

    """
        -> START / FINISH
    """
    def start(self):
        # Gather All Words
        if self.raw_content:
            self.tokenize_raw_content(self.raw_content)
        else:
            self.prepare_hookups()
        self.finish()

    def finish(self):
        self.set_word_counts()
        self.set_ordered_counts()
        self.build_query()

    """
        -> MASTER DYNAMIC ANALYZERS
    """
    def tokenize_raw_content(self, raw_content, applyFilter=True):
        raw_results = jarFAIR.Language.complete_tokenization_v2(raw_content, toList=False)
        self.single_grams = LIST.flatten(self.single_grams, self.filter(content=raw_results[TOKENS], apply=applyFilter))
        self.bi_grams = LIST.flatten(self.bi_grams, self.filter(content=raw_results[BI_GRAMS], apply=applyFilter))
        self.tri_grams = LIST.flatten(self.tri_grams, self.filter(content=raw_results[TRI_GRAMS], apply=applyFilter))
        self.quad_grams = LIST.flatten(self.quad_grams, self.filter(content=raw_results[QUAD_GRAMS], apply=applyFilter))

    def set_word_counts(self):
        self.single_grams_count = DICT.count_list_of_words(self.single_grams)
        self.bi_grams_count = DICT.count_list_of_words(self.bi_grams)
        self.tri_grams_count = DICT.count_list_of_words(self.tri_grams)
        self.quad_grams_count = DICT.count_list_of_words(self.quad_grams)

    def set_ordered_counts(self):
        self.single_grams_count = DICT.order_by_value(self.single_grams_count)
        self.bi_grams_count = DICT.order_by_value(self.bi_grams_count)
        self.tri_grams_count = DICT.order_by_value(self.tri_grams_count)
        self.quad_grams_count = DICT.order_by_value(self.quad_grams_count)

    """
        -> FILTERS
    """
    def filter(self, content, apply=True):
        if apply:
            temp_one = self.remove_stop_words_from_grams(content, self.topic.stop_words)
            temp = self.filter_words_less_than_x_length(temp_one)
            return temp
        return content

    @staticmethod
    def filter_words_less_than_x_length(grams, x=5):
        results = []
        for word in grams:
            if len(word) < x:
                continue
            else:
                results.append(word)
        return results

    """
        -> HELPERS
    """
    def add_hookups(self, hookups: []):
        self.original_hookups = LIST.merge_hookups(self.original_hookups, hookups)

    def prepare_hookups(self):
        for hookup in self.original_hookups:
            content = jarFAIR.Language.combine_args_str(hookup.title, hookup.description, hookup.body)
            self.tokenize_raw_content(content)

    def set_hookups_from_archive(self, date):
        records = self.get_hookups_from_archive(date)
        for record in records:
            # Init
            self.archive_ids.append(record[0])
            self.archive_dates.append(record[1])
            self.add_hookups(record[2])

    @staticmethod
    def remove_stop_words_from_grams(grams, stopwords):
        temp = []
        for word in grams:
            if word in stopwords:
                continue
            else:
                temp.append(word)
        return temp

    def build_query(self):
        self.insertQuery = {"date": self.archive_dates,
                            "dateCreated": self.current_date,
                            "one": self.single_grams_count,
                            "two": self.bi_grams_count,
                            "three": self.tri_grams_count,
                            "four": self.quad_grams_count}


if __name__ == '__main__':
    c = Analyzer()
    c.run_archive_dates(["February 28 2022", "February 27 2022", "February 26 2022"])