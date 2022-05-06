from jarConfig import config
from FLog.LOGGER import Log
from fairNLP import Language
from FSON import DICT

Log = Log("Engine.Content.Matcher")


""" 
Matcher_v1 -> The original.
- Single and Double Term Matching 
"""
def matcher_v1(topic, word, previous_word, terms_match_result):
    Log.v("process_terms")
    # Combine previous word with current word
    word = str(word).lower()
    phrase = str(Language.combine_words(previous_word, word)).lower()
    # -> Loop Weighted Terms
    for key in topic.use_weighted_terms.main_category_keys():
        key_lower = str(key).lower()
        german_encoding = str(key.translate(config.table)).lower()
        # german_translation = STR.to_german(key)
        Log.v(f"match_terms: --> WORD=[ {word} ], PHRASE=[ {phrase} ], --> WEIGHTED_KEY=[ {key}], GERMAN_ENCODING=[ {german_encoding} ]")
        # -> The Matching....
        if phrase == key_lower or phrase == german_encoding:
            Log.d(f"match_terms: Found Phrase: PHRASE=[ {phrase} ] --> WEIGHTED_KEY=[ {key}], GERMAN_ENCODING=[ {german_encoding} ]")
            terms_match_result = DICT.add_matched_word_to_result(phrase, terms_match_result)
            score = topic.use_weighted_terms[key]
            return terms_match_result, score
        elif word == key_lower or word == german_encoding:
            Log.d(f"match_terms: Found Word: WORD=[ {word} ] --> WEIGHTED_KEY=[ {key}], GERMAN_ENCODING=[ {german_encoding} ]")
            terms_match_result = DICT.add_matched_word_to_result(word, terms_match_result)
            score = topic.use_weighted_terms[key]
            return terms_match_result, score
    return False


def matcher_v2(topic, *content):
    """
    -> Matcher_v2, a complete re-write of matcher_v1
        - Single, Double, Triple and Quad Term Matching
        - Weighted Term FAIR Expansion
    """
    Log.v("process_terms")
    # FAIR -> Completely Tokenize Words/Phrases
    word_list = Language.complete_tokenization_v2(content)
    # -> Get Weighted Terms
    weighted_terms = topic.get_topic_weighted_terms(topic.name)
    # -> Loop/Processing Setup
    processing = True
    score = 0
    result_dict = {}
    while processing:
        # -> Loop each Weighted Term
        for weighted_term in weighted_terms.main_category_keys():
            # -> Expand Weighted Term
            expanded_key_list = Language.expand_word(weighted_term)
            # -> Loop All Tokens
            for token in word_list:
                if token in expanded_key_list:
                    key_score = weighted_terms[weighted_term]
                    score += key_score
                    result_dict = DICT.add_matched_word_to_result(weighted_term, result_dict)
        processing = False
    return score, result_dict

def matcher_v3(*content, topic=None):
    """
    -> Matcher_v2 under the hood, but now categorizes each topic based on topic score.
        - Loops through each topic, scoring the article against each topic.
        - It will return a dict of every score/result per topic.
    """
    if not topic:
        topic = Topic()
    # FAIR -> Completely Tokenize Words/Phrases
    word_list = Language.complete_tokenization_v2(content)
    score = 0
    temp_dict = {}
    return_dict = {}
    for topic_name in topic.topic_names:
        weighted_terms = topic.get_topic_weighted_terms(topic_name)
        for w_term in weighted_terms:
            # -> Expand Weighted Term
            expanded_key_list = Language.expand_word(w_term)
            # -> Loop All Tokens
            for token in word_list:
                if token in expanded_key_list:
                    key_score = weighted_terms[w_term]
                    score += key_score
                    temp_dict = DICT.add_matched_word_to_result(w_term, temp_dict)
        return_dict[topic_name] = (score, temp_dict)
        score = 0
        temp_dict = {}
    return return_dict


