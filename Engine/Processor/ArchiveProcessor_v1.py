from Models.Hookup import Hookup
from Engine.Parser.HookupParser import Parser
from Mongodb.MongoArchive import MongoArchive
from FAIR.Core import LIST


class ArchiveProcessor:
    db = MongoArchive()
    pre_processed_hookups = []
    archive_hookups = []
    processed_hookups = []

    """
    -> 1. Add Hookups freely
    -> 2. Then .start()
    """

    def __init__(self, hookups, start=False):
        self.add_hookups(hookups)
        if start:
            self.start()

    def start(self):
        self.db.addUpdate_archives(self.archive_hookups)
        self.parse_hookups()

    def add_hookups(self, hookups):
        self.pre_processed_hookups = LIST.merge_hookups(self.pre_processed_hookups, hookups)
        self.prepare_hookups()

    def prepare_hookups(self):
        self.archive_hookups.append(Hookup.convert_list_to_archive_json(self.pre_processed_hookups))
        self.archive_hookups = LIST.flatten(self.archive_hookups)
        self.pre_processed_hookups = []

    def parse_hookups(self):
        temp = Parser.parse_list(self.archive_hookups, parseAll=True)
        self.processed_hookups.append(temp)
        self.processed_hookups = LIST.flatten(self.processed_hookups)
        self.archive_hookups = []


