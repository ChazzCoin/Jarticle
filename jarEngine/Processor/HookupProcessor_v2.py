from jarConfig.Topic import Topic
from jarFAIR.Parser.HookupParser import Parser
from jarEngine.Processor.WordProcessor_v2 import ProcessWords
from jarEngine.Processor.SozinProcessor_v1 import ProcessTickers
from jarEngine.Processor.TopicProcessor_v1 import TopicProcessor
from Mongodb.MongoArchive import MongoArchive
import uuid
import gc

from Mongodb.MongoHookup import MongoHookup
from Mongodb.MongoResearch import MongoResearch
from jarFAIR.Core import LIST, DICT, DATE

from jarFAIR.Logger import Log
from Server.Discord.TiffanySays import Say
Log = Log("Engine.Processor.HookupProcessor")
Say = Say()

WORDS = "words"
BODY = "body"
TITLE = "title"
DESCRIPTION = "description"


"""
-> Maintains the lifecycle of processing a list of hookups
"""

class HookupProcessor:
    db_archive = MongoArchive()
    archive_id = None
    archive_date = None
    id = ""
    saveToDb = False
    saveToArchive = False
    tickerProcessor: ProcessTickers = None
    wordProcessor: ProcessWords = None
    topicProcessor: TopicProcessor = None
    total_analyzed_hookups = 0
    original_hookups = []
    processed_hookups = []
    final_json_hookups = []
    topic_name = ""
    topic = Topic()

    # -> SETUP <- #
    def __init__(self, saveToArchive=False, saveToDb=False):
        """ -> MASTER PROCESSOR ID CREATED HERE <- """
        self.id = str(uuid.uuid4())
        self.saveToDb = saveToDb
        self.saveToArchive = saveToArchive
        self.topic_name = self.topic.name

    def process_archive(self, date=None):
        if not date:
            date = str(DATE.get_now_date())
        # 1.
        _records = self.get_records_for_date(date)
        # 2.
        Log.i(f"Processing: {len(_records)} Records")
        for _record in _records:
            # -> process each
            _id = DICT.get("_id", _record)
            Log.i(f"Processing Archive ID=[ {_id} ]")
            # 3.
            record = self.db_archive.get_record_where_id(_id)
            key_date = DICT.get("date", record)
            raw_hookups = DICT.get("raw_hookups", record)
            # 4.
            if raw_hookups:
                self.prepare_hookups(raw_hookups, _id, key_date, record)
                self.start()
            else:
                Log.e(f"raw_hookups is FALSE. Date=[ {key_date} ] Record=[ {_record} ]")

    def get_records_for_date(self, date) -> list:
        temp = self.db_archive.get_list_of_record_ids_where_date(date)
        return MongoResearch.to_list(temp)

    def prepare_hookups(self, raw_hookups, _id, key_date, record):
        parsed_hookups = Parser.parse_list(raw_hookups, parseAll=True)
        self.archive_id = _id
        self.archive_date = key_date
        self.add_hookups(parsed_hookups)
        del record
        del parsed_hookups

    def add_hookups(self, hookups: []):
        self.original_hookups = LIST.merge_hookups(self.original_hookups, hookups)

    # -> INITIATE PROCESS
    def start(self):
        self.init_list_of_hookups(self.original_hookups)

    # -> Master Runner
    def init_list_of_hookups(self, hookups):
        if len(hookups) == 0 or hookups is None:
            Log.e("Hookup List is Empty.")
            return "Empty Hookups List"
        Log.notify(f"Starting Hookup Processor.")
        Log.i(f"Processing Hookups: Topic={self.topic_name}, Count={len(hookups)}, saveToDb={self.saveToDb}")
        # X. - WORD PROCESSOR - Analyze all words by themselves.
        Log.i("--WORD PROCESSOR BEGINNING--")
        self.wordProcessor = ProcessWords(processor_id=self.id, topic=self.topic)
        self.wordProcessor.init_list_of_hookups(hookups)
        # X. - TICKER PROCESSOR - Analyze for Crypto and Stock tickers
        # Log.i("--TICKER PROCESSOR BEGINNING--")
        # self.tickerProcessor = ProcessTickers(hookups)
        # self.tickerProcessor.start(strict=True)
        # self.processing_hookups = self.tickerProcessor.processed_hookups
        # X. - TOPIC PROCESSOR - Loop all raw hookups, score/process each one.
        Log.i("--TOPIC PROCESSOR BEGINNING--")
        self.topicProcessor = TopicProcessor(self.topic, hookups)
        self.processed_hookups = self.topicProcessor.processed_hookups
        # -> SET JSON Hookups
        self.set_final_hookups()
        Log.i("Processing Finished. Finishing up...")
        # -> SAVE Final Hookups to MongoDb
        self.save_hookups_to_db()
        # -> Prepare for next set of hookups
        self.total_analyzed_hookups += len(self.final_json_hookups)

    def clear_memory(self):
        Log.i(f"Clearing Memory after Processing Archive ID=[ {self.archive_id} ]")
        del self.original_hookups
        # del self.processing_hookups
        del self.processed_hookups
        # del self.final_json_hookups
        del self.topicProcessor
        gc.collect()
        self.original_hookups = []
        self.processed_hookups = []
        self.final_json_hookups = []

    def set_final_hookups(self):
        temp = []
        for hookup in self.processed_hookups:
            to_json = Parser.to_json(hookup)
            temp.append(to_json)
        self.final_json_hookups = DICT.remove_duplicates("body", temp)

    def save_hookups_to_db(self):
        if self.saveToDb:
            Log.notify(f"Saving Hookups to Database.")
            Log.i("Saving Hookups to Database")
            db = MongoHookup()
            db.add_hookups(key_date=self.archive_date,
                           archive_id=self.archive_id,
                           list_of_hookups=self.final_json_hookups)


if __name__ == "__main__":
    test = "ACEY2025: 3D Tower Defense Game That virtual world Takes You to the Metaverse on Mars - Bitcoinist"
    hp = HookupProcessor(saveToArchive=False, saveToDb=False)
    hp.process_archive()
