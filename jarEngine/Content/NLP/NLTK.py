import nltk
import re
from jarEngine.Content import Score
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import nltk.data
from FLog.LOGGER import Log

from fopTopic.Topic import Topic

Log = Log("Engine.NLTK")
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

stop_words = stopwords.words('english')
WEIGHTED_TERMS = Topic.ALL_CATEGORIES().get_all_weighted_terms()

def get_content_sentiment(content) -> {}:
    """ Sentiment of Content. """
    vader = SentimentIntensityAnalyzer()
    all_weighted_terms = WEIGHTED_TERMS
    vader.lexicon.update(all_weighted_terms)
    score = vader.polarity_scores(content)
    Log.v("get_content_sentiment:", score)
    return score

def tokenize_content_into_words(content) -> []:
    """ Convert content into list of single words. """
    Log.v("tokenize_content:", content)
    # content = remove_special_characters(content)
    tokens = nltk.word_tokenize(content)
    list_of_words = [token.lower() for token in tokens]
    Log.v("tokenize_content:", list_of_words)
    return list_of_words

def tokenize_content_into_sentences(content):
    """ Split a large string into sentences """
    sentences = tokenizer.tokenize(content)
    sentences = [x.replace('\n', '') for x in sentences if len(x) > 10]
    return sentences

def split_words(text):
    """ ALTERNATIVE: Split a string into array of words. """
    try:
        text = re.sub(r'[^\w ]', '', text)  # strip special chars
        return [x.strip('.').lower() for x in text.split()]
    except TypeError:
        return None

def freq_of_words(content):
    Log.v("freq_of_words:", content)
    fdist = FreqDist(content)
    return fdist

def freg_most_common(top=10, content="", fdist=None):
    if not fdist:
        fdist = freq_of_words(content)
    top = fdist.most_common(top)
    return top

def get_count_single_words(content, top=10):
    """ Count how many times ONE WORD is seen in content """
    fdist = freq_of_words(content)
    return freg_most_common(top=top, fdist=fdist)

def get_count_bi_words(content, top=10):
    """ Count how many times TWO WORDS are seen in content. """
    bi = nltk.collocations.BigramCollocationFinder.from_words(content)
    return bi.ngram_fd.most_common(top)

def get_count_tri_words(content, top=10):
    """ Count how many times THREE WORDS are seen in content. """
    tri = nltk.collocations.TrigramCollocationFinder.from_words(content)
    return tri.ngram_fd.most_common(top)

def get_count_quad_words(content, top=10):
    """ Count how many times FOUR WORDS are seen in content. """
    quad = nltk.collocations.QuadgramCollocationFinder.from_words(content)
    return quad.ngram_fd.most_common(top)

def remove_special_characters(content):
    newText = re.sub('[^a-zA-Z]', ' ', content)
    return newText

def summarize(title='', content='', max_sents=2):
    if not content or not title or max_sents <= 0:
        return []
    summaries = []
    sentences = tokenize_content_into_sentences(content)
    titleWords = split_words(title)
    # Score sentences, and use the top 5 or max_sents sentences
    ranks = Score.score_list_of_sentences(sentences, titleWords).most_common(max_sents)
    for rank in ranks:
        summaries.append(rank[0])
    summaries.sort(key=lambda summary: summary[0])
    return [summary[1] for summary in summaries]

def keywords(content):
    """Get the top 10 keywords and their frequency scores ignores blacklisted
    words in stopwords, counts the number of occurrences of each word, and
    sorts them in reverse natural order (so descending) by number of
    occurrences.
    """
    NUM_KEYWORDS = 10
    content = split_words(content)
    stopwords = ["get_stopwords()"]
    # of words before removing blacklist words
    if content:
        num_words = len(content)
        content = [x for x in content if x not in stopwords]
        freq = {}
        for word in content:
            if word in freq:
                freq[word] += 1
            else:
                freq[word] = 1

        min_size = min(NUM_KEYWORDS, len(freq))
        keywords = sorted(freq.items(),
                          key=lambda x: (x[1], x[0]),
                          reverse=True)
        keywords = keywords[:min_size]
        keywords = dict((x, y) for x, y in keywords)
        for k in keywords:
            articleScore = keywords[k] * 1.0 / max(num_words, 1)
            keywords[k] = articleScore * 1.5 + 1
        return dict(keywords)
    else:
        return dict()

def sentence_position(i, size):
    """Different sentence positions indicate different
    probability of being an important sentence.
    """
    normalized = i * 1.0 / size
    if normalized > 1.0:
        return 0
    elif normalized > 0.9:
        return 0.15
    elif normalized > 0.8:
        return 0.04
    elif normalized > 0.7:
        return 0.04
    elif normalized > 0.6:
        return 0.06
    elif normalized > 0.5:
        return 0.04
    elif normalized > 0.4:
        return 0.05
    elif normalized > 0.3:
        return 0.08
    elif normalized > 0.2:
        return 0.14
    elif normalized > 0.1:
        return 0.23
    elif normalized > 0:
        return 0.17
    else:
        return 0


# if __name__ == "__main__":
#     test = ["ACEY2025: 3D Tower Defense Game That virtual world Takes You to the Metaverse on Mars.",
#             "What could the virtual world hold in store for us to buy next?"]
#     title = "Oracle takes a big move toward health with a deal to buy Cerner for $28.3 billion."
#     title_words = ["Oracle", "takes", "big", "move", "toward", "health", "with", "deal", "buy", "Cerner", "$28.3", "billion"]
#     body = "Markets sank on Monday, extending last weeks losses, as investors took in the latest grim forecasts about the sudden surge in the Omicron variant and after a big setback in President Bidens efforts to pass a comprehensive domestic policy bill. The S&P 500 fell about 1.1 percent, recovering some of its earlier losses. The index fell nearly 2 percent last week. For the first time since Omicron appeared we have reason to be nervous about the variant having an impact on the growth trajectory of the economy, said Lindsey Bell, the chief money and markets strategist at Ally Invest, a foreign exchange company. A slowdown could mean inflation sticks around a bit longer given supply chain constraints. Despite its recent wobbles, the S&P 500 is still up 21 percent this year. In the White House, the future of Mr. Bidens $2.2 trillion domestic policy bill was put in doubt after Senator Joe Manchin III, Democrat of West Virginia, said he would vote against it because he feared it would inflame inflation. The impact began to weigh on prospects for the U.S. economy, adding to negative sentiment in markets. Goldman Sachs said in a research note that it would scale back its projected growth for the economy next year and now expected 2 percent growth in the first quarter, down from 3 percent. Researchers at the bank said Congress could pass some version of the bill, with a focus on manufacturing and supply chain issues. Disagreement over the bill also pushed shares of major engineering and construction materials companies lower. SolarEdge Technologies, which provides solar-powered systems, fell 10.6 percent, while the asphalt maker Vulcan Materials fell 2.9 percent. Investors are also still reacting to the Federal Reserves decision last week to speed up the tapering of its bond-buying program, a possible prelude to higher interest rates, as the Fed tries to quell inflation, wrote Saira Malik, the chief investment officer for global equities at Nuveen, a unit of TIAA. The stock market initially rallied after the announcement. But now, investors have fully digested the Feds plans, raising concerns that a rapid increase in rates might cause economic growth to slow, she wrote in a research note. Shares of technology stocks, which are sensitive to changing views on interest rates, have fallen in recent weeks. Meta, Facebooks parent company, fell 2.5 percent on Monday, while Amazon, Apple and Microsoft were also lower. Over the weekend, more European countries announced restrictions to control the spread of the coronavirus. And Germanys central bank, the Bundesbank, said it would scale back its predictions of economic growth because of recent pandemic restrictions. Markets in Europe were down, with the Stoxx Europe 600 closing 1.4 percent lower. Asian indexes closed lower. Airline and travel stocks fell sharply in midday European trading. But the biggest decliner in Britains FTSE 100 was Informa, which organizes large in-person events. It fell 5.3 percent, after shedding as much as 6.9 percent earlier. The spread of the new variant has also prompted companies to go fully remote, to bar nonessential staff from the office and to cancel mass gatherings. CNN and JPMorgan Chase are among the companies that have set renewed work-from-home models. The World Economic Forum announced Monday that it was postponing its annual meeting in Davos, Switzerland. Economists say the prospect for a year-end rise in the stock market is marred because of news on the Omicron variant. At the same time, trading is generally light during the holidays, making the market more volatile. Given the amount of downside risks going into the new year, its hardly surprising to see investors adopting a more cautious approach as they log off for the holidays, Craig Erlam, a senior market analyst at Oanda, wrote in a note. Senator Manchins assertion that he could not support the domestic policy bill — which would provide tax credits of up to $12,500 for consumers buying electric vehicles — appeared to weigh on the stocks of automakers on Monday. Car companies are investing heavily in production of electric vehicles, believing they will make up an increasing share of the auto market in the years ahead. Shares in the electric carmaker Lucid plunged 5.1 percent and have fallen nearly a third from their high. Rivian, which makes electric trucks and vans, was down 7.9 percent and has lost nearly half of its value since its peak last month. And Tesla shares were down 3.5 percent and have shed more than a quarter of their value since their peak last month. Investors bid up stock in Ford Motor and General Motors this year as those companies moved to make electric vehicles a big part of their product lines. Ford stock was down 1.8 percent Monday, but was still up about 120 percent for the year. G.M. fell 2 percent Monday but has gained about 30 percent this year. The bill would have extended and increased existing tax credits; Lucid and Rivian would still benefit from credits available under the current program. Oil prices also fell on Monday. Futures of West Texas Intermediate, the U.S. benchmark, dropped nearly 4 percent to $68.23 a barrel. Energy stocks were among the worst performers in the S&P 500, with Devon Energy Corporation down 2.4 and Enphase Energy 5.5 percent lower. Peter Eavis , Kevin Granville and Eshe Nelson contributed reporting."
#     from Engine.Content import Word
#     body_words = Word.pre_process_words(body)
#     tri = nltk.collocations.TrigramCollocationFinder.from_words(body_words)
#     print(tri.ngram_fd)
#     print(tri.ngram_fd.most_common(3))
    # freq = freq_of_words(body_words)
    # print(freq.)
    # most_common = freg_most_common(freq)
    # print(most_common)
