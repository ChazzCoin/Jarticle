from Topics import Language
from Topics.Futils import DICT

def categorize(content, categories: {}):
    """
    -> Matcher_v3 under the hood, but now categorizes each topic based on topic score.
        - Loops through each topic, scoring the article against each topic.
        - It will return a dict of every score/result per topic.
    """
    # FAIR -> Completely Tokenize Words/Phrases
    word_list = Language.complete_tokenization_v2(content)
    # -> Setup
    return_dict = {}  # { "category_name": ( score, { "weighted_term": "match_count", "weighted_term": "match_count" } ) }
    # 1. -> Loop Each Category
    for category_name in categories.keys():
        # -> Extract Weighted Terms from Category/SubCategory
        weighted_terms = DICT.get("weighted_terms", categories[category_name], default=False)
        if not weighted_terms:
            weighted_terms = categories[category_name]
        return_dict[category_name] = run_matcher(word_list, weighted_terms)
    return return_dict

def run_matcher(word_list, weighted_terms):
    # 2. -> Loop Each Category Weighted Term
    temp_dict = {}  # { "weighted_term": "match_count" }
    score = 0  # "weighted_term" Score * "match_count"
    for w_term in weighted_terms:
        # Stay Safe People
        if not w_term and w_term == "" or w_term == " ":
            continue
        # -> Expand Weighted Term
        expanded_key_list = Language.expand_word(w_term)
        # 3. -> Loop All Tokens AND MATCH!!
        for token in word_list:
            # Stay Safe People
            if not token and token == "" or token == " ":
                continue
            # MATCHER! -> if content word is in expanded weighted term list...
            if token in expanded_key_list:
                # -> We have a match!
                key_score = weighted_terms[w_term]
                score += key_score
                temp_dict = DICT.add_matched_word_to_result(w_term, temp_dict)
    # -> 4. Finish Up
    return score, temp_dict  # ( score, { "weighted_term": "match_count", "weighted_term": "match_count" } )
