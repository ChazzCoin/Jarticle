import os

MASTER_PATH = os.getcwd()

ENGLISH = "ENGLISH"
GERMAN = "GERMAN"
LANGUAGE = ENGLISH

ERROR = 0  # -> Show ERROR only
INFO = 1  # -> Show ERROR and INFO
DEBUG = 2  # -> Show ERROR, INFO and DEBUG
VERBOSE = 3  # -> Show ERROR, INFO, DEBUG AND VERBOSE
LOG_LEVEL = DEBUG

LATEST = 0  # 0 == LATEST
NLP_VERSION = 1

removal_words = ["in", "the", "by", "to", "of", "as", "on",
                 "is", "now", "be", "will", "a", "it", "it's",
                 "its", "at", "into", "for", "that", "you",
                 "and", "or", "new", "are", "a"]

table = {
         ord('ä'): 'ae',
         ord('ö'): 'oe',
         ord('ü'): 'ue',
         ord('ß'): 'ss',
       }