from jarEngine.Content.NLP import SPACY, NLTK
# import jarFAIR
from fairNLP import Language
from jarConfig import config
from FLog.LOGGER import Log

Log = Log("Engine.Content.Tokenizer")

VERSION = config.NLP_VERSION

def to_words(content):
    if VERSION == 1:
        return word_tokenizer_v1(content)
    elif VERSION == 2:
        return word_tokenizer_v2(content)
    else:
        return word_tokenizer_v3(content)

def word_tokenizer_v1(content):
    return NLTK.split_words(content)

def word_tokenizer_v2(content):
    return NLTK.tokenize_content_into_words(content)

def word_tokenizer_v3(content) -> []:
    return SPACY.tokenize_content_into_words(content)

def word_tokenizer_FAIR(content):
    return Language.to_words_v1(content)


def tokenize_content(content, topic=None) -> []:
    Log.v(f"1. pre_process_words: IN=[ {content} ]")
    # Clean and Convert words into list
    if config.LANGUAGE == config.GERMAN:
        content = content.translate(config.table)
    list_of_words = to_words(content)
    # Grab latest stop words list
    if topic:
        stop_words = topic.stop_words
    else:
        stop_words = []
    # Loop each word for removal
    i = 0
    run = True
    while run:
        if i > len(list_of_words) - 1:
            run = False
            continue
        word = list_of_words[i]
        # if word is in config or ntlk stop words, remove it.
        if not word.isalpha():
            list_of_words.remove(word)
            continue
        if word in config.removal_words or word in stop_words:
            list_of_words.remove(word)
            continue
        i = i + 1
    Log.v(f"2. pre_process_words: OUT=[ {list_of_words} ]")
    return list_of_words