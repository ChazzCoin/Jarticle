import heapq
import re
import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

"""
    !! -> EXPERIMENTAL <- !!
"""

def prepare_sentences(article_text):
    text = article_text.split(". ")
    sentences = []
    for sentence in text:
        # print(sentence)
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    return sentences


def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        nltk.download('stopwords')
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
    all_words = list(set(sent1 + sent2))
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
    # build the vector for the first sentence
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
    # build the vector for the second sentence
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1
    return 1 - cosine_distance(vector1, vector2)


def build_similarity_matrix(sentences, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2:  # ignore if both are same sentences
                continue
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)
    return similarity_matrix


def generate_summary(topic, all_text, top_n=5):
    stop_words = topic.stop_words
    summarize_text = []
    # Step 1 - Read text anc split it
    sentences = prepare_sentences(all_text)
    # Step 2 - Generate Similary Martix across sentences
    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)
    # Step 3 - Rank sentences in similarity martix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)
    # Step 4 - Sort the rank and pick top sentences
    ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    # print("Indexes of top ranked_sentence order are ", ranked_sentence)
    for i in range(top_n):
        summarize_text.append(" ".join(ranked_sentence[i][1]))
    # Step 5 - Offcourse, output the summarize texr
    print("-> Summary...")
    for i in summarize_text:
        print(i)
    # print("Summarize Text: \n", ". ".join(summarize_text))


''' -> Next Summarizer <- '''


def remove_square_brackets_extra_spaces(text):
    newText = re.sub(r'\[[0-9]*\]', ' ', text)
    newText = re.sub(r'\s+', ' ', newText)
    return newText


def remove_special_characters_digits(text):
    newText = re.sub('[^a-zA-Z]', ' ', text)
    newText = re.sub(r'\s+', ' ', newText)
    return newText


def get_processed_article_text(article_text):
    return remove_square_brackets_extra_spaces(article_text)


def get_processed_formatted_article_text(article_text):
    return remove_special_characters_digits(article_text)


"""https://stackabuse.com/text-summarization-with-nltk-in-python/"""


def convert_to_sentences(text):
    # ->
    article_text = get_processed_article_text(text)
    sentence_list = nltk.sent_tokenize(article_text)
    nltk.download('stopwords')
    # ->
    word_frequencies = get_word_frequency(article_text)
    # ->
    sentence_scores = get_sentence_scores(sentence_list, word_frequencies)
    # ->
    summary_sentences = heapq.nlargest(20, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    print(summary)
    # for s in summary_sentences:
    #     print(s)

def get_word_frequency(content):
    word_frequencies = {}
    formatted_article_text = remove_special_characters_digits(content)
    stopwords = nltk.corpus.stopwords.words('english')
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    # ->
    maximum_frequncy = max(word_frequencies.values())
    for word in word_frequencies.main_category_keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequncy)
    return word_frequencies

def get_sentence_scores(sentence_list, word_frequencies):
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.main_category_keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    return sentence_scores