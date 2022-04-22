from newspaper.nlp import ideal
from jarEngine.Content import Matcher, Tokenizer
from jarConfig import config
from jarEngine.Content.NLP import NLTK
import math

from jarEngine.Helper.Counter import Counter
from jarFAIR.Logger import Log

Log = Log("Engine.Content.Score")
# -> Return rank with only 1 decimal place
decimal_place = "%.1f"


def score_content_v3(content: [], topic=None) -> ():
    Log.v(f"score_content_v3.")
    return Matcher.matcher_v3(content, topic=topic)


def score_content_v2(topic, content: []) -> ():
    Log.v(f"score_content_v2: topicName={topic.name}")
    return Matcher.matcher_v2(topic, content)


# -> Score any content/body
def score_content_v1(topic, content: []) -> ():
    Log.v(f"score_content: topicName={topic.name}")
    terms_match_result = {}
    # -> Null Defense
    if content is None or content == '' or content == ' ':
        Log.d(f"process_content: content is empty: {content}")
        return 0, terms_match_result
    # Tokenize Words
    list_of_words_in_content = Tokenizer.tokenize_content(content, topic=topic)
    # Loop through each word
    i = 0
    score = 0
    previous_word = list_of_words_in_content[0] if len(list_of_words_in_content) > 0 else None
    if previous_word is None:
        Log.d("found none", list_of_words_in_content)
        return 0, terms_match_result
    for word in list_of_words_in_content[1:]:
        # -> 1. Two Words Scoring
        two_term_result = Matcher.matcher_v1(topic, word, previous_word, terms_match_result)
        if two_term_result:
            terms_match_result = two_term_result[0]
            score += two_term_result[1]
        # 3. set previous_word to current word for the next iteration
        previous_word = word
        i += 1
    result = (score, terms_match_result)
    Log.v(f"process_content: Result: {result}")
    return result

def add_matched_word_to_result(word, dic):
    if word in dic.main_category_keys():
        dic[word] += 1
    else:
        dic[word] = 1
    return dic

# -> 2. Scoring
def word_score_length(word, score):
    if len(word) < 3:
        score += 1
    elif len(word) < 4:
        score += 2
    elif len(word) >= 5:
        score += 3
    elif len(word) >= 6:
        score += 4
    elif len(word) >= 7:
        score += 5
    elif len(word) >= 10:
        score += 15
    else:
        score += 0
    return score

def get_overall_score(title_rank, description_rank, body_rank, sentiment):
    if title_rank is None:
        title_rank = 0
    if description_rank is None:
        description_rank = 0
    if body_rank is None:
        body_rank = 0
    total = title_rank + description_rank + body_rank
    pos = sentiment.get("pos", 0)
    neg = sentiment.get("neg", 0)
    if pos != 0 or neg != 0:
        total_pos = total * pos
        total_neg = total * neg
        total = total + total_pos
        total = total - total_neg
    total = float(total) * float(get_sentiment_multiplier(sentiment))
    return decimal_place % total

def get_sentiment_multiplier(sentiment):
    pos = sentiment.get("pos")
    neg = sentiment.get("neg")
    if pos > neg:
        digit = str(pos)[2]
        if float(digit) < 2:
            digit = 1
        senti_multiplier = digit
    else:
        senti_multiplier = 1
    Log.v(f"Sentiment Multiplier: {senti_multiplier}, -> Sentiment:{sentiment}")
    return senti_multiplier

def get_average_sentence_score(raw_content: str, topic, titleWords=None):
    scores = score_content_sentences(topic, raw_content, titleWords)
    temp_score = 0.0
    for score in scores.keys():
        temp_score += scores[score]
    return temp_score

def score_list_of_sentences(topic, list_of_raw_str: [], titleWords=None):
    raw_str_content = ""
    for sentence in list_of_raw_str:
        raw_str_content += sentence
    return score_content_sentences(topic, raw_str_content, titleWords=titleWords)

# -> Works Great
def score_content_sentences(topic, raw_str_content: str, titleWords=None):
    full_raw_content = raw_str_content
    # for content in raw_str_content:
    #     full_raw_content += content
    keywords = topic.get_topic_weighted_terms(topic.name)
    """ Score sentences based on different features """
    senSize = len(full_raw_content)
    sentences = NLTK.tokenize_content_into_sentences(full_raw_content)
    ranks = Counter()
    for i, s in enumerate(sentences):
        sentence = NLTK.split_words(s)
        titleFeature = title_score(titleWords if titleWords is not None else [""], sentence, topic=topic)
        sentenceLength = length_score(len(sentence))
        sentencePosition = NLTK.sentence_position(i + 1, senSize)
        sbsFeature = sbs(sentence, keywords)
        dbsFeature = dbs(sentence, keywords)
        frequency = (sbsFeature + dbsFeature) / 2.0 * 10.0
        # Weighted average of scores from four categories
        totalScore = (titleFeature*1.5 + frequency*2.0 +
                      sentenceLength*1.0 + sentencePosition*1.0)/4.0
        ranks[(i, s)] = totalScore
    return ranks


def sbs(words, keywords):
    score = 0.0
    if len(words) == 0:
        return 0
    for word in words:
        if word in keywords:
            score += keywords[word]
    return (1.0 / math.fabs(len(words)) * score) / 10.0


def dbs(words, keywords):
    if len(words) == 0:
        return 0
    summ = 0
    first = []
    second = []
    for i, word in enumerate(words):
        if word in keywords:
            score = keywords[word]
            if not first:
                first = [i, score]
            else:
                second = first
                first = [i, score]
                dif = first[0] - second[0]
                summ += (first[1] * second[1]) / (dif ** 2)
    # Number of intersections
    k = len(set(keywords.main_category_keys()).intersection(set(words))) + 1
    return 1 / (k * (k + 1.0)) * summ


def length_score(sentence_len):
    return 1 - math.fabs(ideal - sentence_len) / ideal


def title_score(title, sentence, topic):
    stopwords = topic.stop_words
    if title:
        title = [x for x in title if x not in stopwords]
        count = 0.0
        for word in sentence:
            if word not in stopwords and word in title:
                count += 1.0
        return count / max(len(title), 1)
    else:
        return 0


if __name__ == '__main__':
    body = "Markets sank on Monday, extending last weeks losses, as investors took in the latest grim forecasts about the sudden surge in the Omicron variant and after a big setback in President Bidens efforts to pass a comprehensive domestic policy bill. The S&P 500 fell about 1.1 percent, recovering some of its earlier losses. The index fell nearly 2 percent last week. For the first time since Omicron appeared we have reason to be nervous about the variant having an impact on the growth trajectory of the economy, said Lindsey Bell, the chief money and markets strategist at Ally Invest, a foreign exchange company. A slowdown could mean inflation sticks around a bit longer given supply chain constraints. Despite its recent wobbles, the S&P 500 is still up 21 percent this year. In the White House, the future of Mr. Bidens $2.2 trillion domestic policy bill was put in doubt after Senator Joe Manchin III, Democrat of West Virginia, said he would vote against it because he feared it would inflame inflation. The impact began to weigh on prospects for the U.S. economy, adding to negative sentiment in markets. Goldman Sachs said in a research note that it would scale back its projected growth for the economy next year and now expected 2 percent growth in the first quarter, down from 3 percent. Researchers at the bank said Congress could pass some version of the bill, with a focus on manufacturing and supply chain issues. Disagreement over the bill also pushed shares of major engineering and construction materials companies lower. SolarEdge Technologies, which provides solar-powered systems, fell 10.6 percent, while the asphalt maker Vulcan Materials fell 2.9 percent. Investors are also still reacting to the Federal Reserves decision last week to speed up the tapering of its bond-buying program, a possible prelude to higher interest rates, as the Fed tries to quell inflation, wrote Saira Malik, the chief investment officer for global equities at Nuveen, a unit of TIAA. The stock market initially rallied after the announcement. But now, investors have fully digested the Feds plans, raising concerns that a rapid increase in rates might cause economic growth to slow, she wrote in a research note. Shares of technology stocks, which are sensitive to changing views on interest rates, have fallen in recent weeks. Meta, Facebooks parent company, fell 2.5 percent on Monday, while Amazon, Apple and Microsoft were also lower. Over the weekend, more European countries announced restrictions to control the spread of the coronavirus. And Germanys central bank, the Bundesbank, said it would scale back its predictions of economic growth because of recent pandemic restrictions. Markets in Europe were down, with the Stoxx Europe 600 closing 1.4 percent lower. Asian indexes closed lower. Airline and travel stocks fell sharply in midday European trading. But the biggest decliner in Britains FTSE 100 was Informa, which organizes large in-person events. It fell 5.3 percent, after shedding as much as 6.9 percent earlier. The spread of the new variant has also prompted companies to go fully remote, to bar nonessential staff from the office and to cancel mass gatherings. CNN and JPMorgan Chase are among the companies that have set renewed work-from-home models. The World Economic Forum announced Monday that it was postponing its annual meeting in Davos, Switzerland. Economists say the prospect for a year-end rise in the stock market is marred because of news on the Omicron variant. At the same time, trading is generally light during the holidays, making the market more volatile. Given the amount of downside risks going into the new year, its hardly surprising to see investors adopting a more cautious approach as they log off for the holidays, Craig Erlam, a senior market analyst at Oanda, wrote in a note. Senator Manchins assertion that he could not support the domestic policy bill — which would provide tax credits of up to $12,500 for consumers buying electric vehicles — appeared to weigh on the stocks of automakers on Monday. Car companies are investing heavily in production of electric vehicles, believing they will make up an increasing share of the auto market in the years ahead. Shares in the electric carmaker Lucid plunged 5.1 percent and have fallen nearly a third from their high. Rivian, which makes electric trucks and vans, was down 7.9 percent and has lost nearly half of its value since its peak last month. And Tesla shares were down 3.5 percent and have shed more than a quarter of their value since their peak last month. Investors bid up stock in Ford Motor and General Motors this year as those companies moved to make electric vehicles a big part of their product lines. Ford stock was down 1.8 percent Monday, but was still up about 120 percent for the year. G.M. fell 2 percent Monday but has gained about 30 percent this year. The bill would have extended and increased existing tax credits; Lucid and Rivian would still benefit from credits available under the current program. Oil prices also fell on Monday. Futures of West Texas Intermediate, the U.S. benchmark, dropped nearly 4 percent to $68.23 a barrel. Energy stocks were among the worst performers in the S&P 500, with Devon Energy Corporation down 2.4 and Enphase Energy 5.5 percent lower. Peter Eavis , Kevin Granville and Eshe Nelson contributed reporting."
    title = "Oracle takes a big move toward health with a deal to buy Cerner for $28.3 billion."
    title_words = ["Oracle", "takes", "big", "move", "toward", "health", "with", "deal", "buy", "Cerner", "$28.3",
                   "billion"]
    from jarConfig import Terms, config

    weighted = Terms.Terms.metaverse_weighted_terms
    # title_score = title_score(title_words, title)
    # scores = score_sentences(raw_str_content=body, titleWords=title_words, keywords=weighted)
    # print(scores.keys())
    # print(type(scores))
    # for score in scores.keys():
    #     print(scores[score], score[1])