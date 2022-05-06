import spacy
from FLog.LOGGER import Log

Log = Log("Engine.Content.NLP_v2")

# nlp = spacy.load('en_core_web_sm')

def tokenize_content_into_words(content) -> []:
    pass
    # tokens = []
    # raw = nlp(content)
    # for token in raw:
    #     tokens.append(token.text)
    # return tokens

# def get_entities(content):
#     raw = nlp(content)
#     return [(token_ent.text, token_ent.label_) for token_ent in raw.ents]

# if __name__ == '__main__':
#     sentence = "Charles, showed Mallory, some of Chace's stuff over at the house last night. From U.S to U.K. I would take on every, single, road available! $350.00"
#     print(get_entities(sentence))