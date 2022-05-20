from jarEngine.Content import Tokenizer

from fairNLP import Language
from FLog.LOGGER import Log
Log = Log("Engine.Processor.WordProcessor")

WORDS = "words"
BODY = "body"
TITLE = "title"
DESCRIPTION = "description"


class ProcessWords:
    processor_id = ""
    db: MongoWords = None
    saveToDb = False
    topic = None
    # FAIR
    data_single_words = {}
    data_filtered_single_words = {}
    data_bi_grams = {}
    data_tri_grams = {}
    data_quad_grams = {}
    data_top_mentioned_words = {}

    """
    -> Shouldn't need to have saved_words. We should pull from the db in this class.
    1. Save words per day, per week, per month, per year.
    """

    # -> Start Here <- #
    def __init__(self, processor_id, topic=None, saveToDb=False):
        Log.i("Starting ProcessWords.")
        self.processor_id = processor_id
        self.topic = topic
        self.saveToDb = saveToDb

    def add_single_hookup(self, hookup: Hookup):
        self.process_single_hookup(hookup)

    def add_hookups(self, hookups: [], topic=None, saveToDb=True):
        self.saveToDb = saveToDb
        if topic:
            self.topic = topic
        self.init_list_of_hookups(hookups)

    # -> Master Runner
    def init_list_of_hookups(self, hookups: [Hookup]):
        if len(hookups) == 0 or hookups is None:
            Log.e("Hookup List is Empty.")
            return "Empty Hookups List"
        Log.d("init_list_of_hookups")
        Log.notify(f"Starting Word Processor.")
        for hookup in hookups:
            self.process_single_hookup(hookup)
        # -> Get POST DATA here.
        self.remove_stop_words()
        self.get_top_ten_terms()
        # -> Save words to database.
        self.save_counted_words_to_db()

    # -> Word Process
    def process_single_hookup(self, hookup: Hookup):
        # Words
        content = Language.combine_args_str(hookup.title, hookup.description, hookup.body)
        tokens = Tokenizer.to_words(content)
        self.set_single_words(tokens)
        self.set_bi_words(tokens)
        self.set_tri_words(tokens)
        self.set_quad_words(tokens)

    # Single Helper
    def set_single_words(self, tokens):
        self.data_single_words = tokens

    # Two Helper
    def set_bi_words(self, tokens):
        self.data_bi_grams = Language.to_bi_grams_v2(tokens)

    # Three Helper
    def set_tri_words(self, tokens):
        self.data_tri_grams = Language.to_tri_grams_v2(tokens)

    # Four Helper
    def set_quad_words(self, tokens):
        self.data_quad_grams = Language.to_quad_grams_v2(tokens)

    def get_top_ten_terms(self):
        unqiue_values = list(set(self.data_filtered_single_words.values()))
        count = len(unqiue_values)
        top_ten = unqiue_values[count-20:count]
        temp = {}
        for key in self.data_filtered_single_words.keys():
            item = self.data_filtered_single_words[key]
            if item in top_ten:
                temp[key] = item
        self.data_top_mentioned_words = temp

    def remove_stop_words(self):
        temp = {}
        for key in self.data_single_words.main_category_keys():
            if key in self.topic.stop_words:
                continue
            else:
                item = self.data_single_words[key]
                temp[key] = item
        self.data_filtered_single_words = temp

    # Database Dump
    def save_counted_words_to_db(self):
        Log.d("save_scored_words_to_db")
        if self.saveToDb:
            temp = {
                "processor_id": self.processor_id,
                "single": self.data_single_words,
                "two": self.data_bi_grams,
                "three": self.data_tri_grams,
                "four": self.data_quad_grams
            }
            self.db.add_word_dump(word_data=temp)

    def get_counted_words_from_db(self) -> []:
        Log.i("Getting ranked words from db...")
        scored_words = self.db.get_latest_scored_words()
        return scored_words

if __name__ == "__main__":
    test = "ACEY2025: 3D Tower Defense Game That virtual world Takes You to the Metaverse on Mars - Bitcoinist"
    # ProcessHookup.match_two_words(test)

# test = "ACEY2025: 3D Tower Defense Game That Takes You to the Metaverse on Mars - Bitcoinist"
# process = ProcessWords(body_of_text=test)
# print(process.all_words)
# print(process.top_five)
