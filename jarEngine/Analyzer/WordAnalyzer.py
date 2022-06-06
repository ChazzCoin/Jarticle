
from FSON import DICT
from FList import LIST
from FDate import DATE
from fairNLP import Language
from jarProvider import ArticleProvider as ap
import fairResources
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

STOPWORDS = fairResources.get_stopwords()

class Analyzer:
    original_dates = []
    raw_content = None
    current_date = str(DATE.get_now_month_day_year_str())
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
    def run_archive_dates(self, datesBack=1):
        """ Add Dates, Get Archives, Parse Hookups -> Start """
        records_by_date = ap.get_date_range_list(datesBack)
        for date_of_arts in records_by_date:
            self.analyze_articles(date_of_arts)

    def analyze_articles(self, articles):
        for art in articles:
            title = DICT.get("title", art, "")
            body = DICT.get("body", art, "")
            description = DICT.get("description", art, "")
            content = Language.combine_args_str(title, description, body)
            self.tokenize_raw_content(content)
        self.set_word_counts()
        self.set_ordered_counts()

    """
        -> MASTER DYNAMIC ANALYZERS
    """
    def tokenize_raw_content(self, raw_content, applyFilter=True):
        raw_results = Language.complete_tokenization_v2(raw_content, toList=False)
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
            temp_one = self.remove_stop_words_from_grams(content, STOPWORDS)
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
        self.insertQuery = {
                            "grams": self.single_grams_count,
                            "bigrams": self.bi_grams_count,
                            "trigrams": self.tri_grams_count,
                            "quadgrams": self.quad_grams_count
                            }


if __name__ == '__main__':
    c = Analyzer()
    c.run_archive_dates(1)