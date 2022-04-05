from Config import env

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

""" 
-> Global Config
"""
BOT_NAME = "TiffanyBot"
MASTER_PATH = env.get_env("TIFFANY_BOT_PATH")

german_key_terms = ["krisen management", "projektmanagement", "expertenmanagement", "uberbruckungsmanagement", "change management"]

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

# ------------------------------------------> SET CLIENT INFO <------------------------------------------------------ #
# 1. REDDIT CLIENT
reddit_user_agent = env.get_env("REDDIT_USER_AGENT")
reddit_client_id = env.get_env("REDDIT_CLIENT_ID")
reddit_client_secret = env.get_env("REDDIT_CLIENT_SECRET")
reddit_username = env.get_env("REDDIT_USERNAME")
reddit_password = env.get_env("REDDIT_PASSWORD")

# 2. TWITTER CLIENT
twitter_consumer_key = env.get_env("TWITTER_CONSUMER_KEY")
twitter_consumer_secret = env.get_env("TWITTER_CONSUMER_SECRET")
twitter_access_token = env.get_env("TWITTER_ACCESS_TOKEN")
twitter_access_token_secret = env.get_env("TWITTER_ACCESS_TOKEN_SECRET")
# Number of Tweets to Pull per User Threshold
number_of_tweets = 200
number_of_tweets_test = 10

# -> SMS NOTIFICATIONS <- #
# TextBelt: https://textbelt.com/ #
sms_key = "3b11437549708345091de04ca87cba6129cdfb493NIMu5rAxH3fm9Ie8EEvYqrZw"
sms_url = 'https://textbelt.com/text'
sms_number = env.get_env("CELL_NUMBER")

# -------------------------------------------> SET THRESHOLDS <------------------------------------------------------ #
# 1. REDDIT CRYPTO
c_goodAuth = {'AutoModerator'}   # authors whom comments are allowed more than once
c_uniqueCmt = True                # allow one comment per author per symbol
c_ignoreAuthP = {'example'}       # authors to ignore for posts
c_ignoreAuthC = {'example'}       # authors to ignore for comment
c_upvoteRatio = 0.70         # upvote ratio for post to be considered, 0.70 = 70%
c_ups = 20       # define # of upvotes, post is considered if upvotes exceed this #
c_limit = 100      # define the limit, comments 'replace more' limit
c_upvotes = 2     # define # of upvotes, comment is considered if upvotes exceed this #
c_picks = 10     # define # of picks here, prints as "Top ## picks are:"
c_picks_ayz = 5   # define # of picks for sentiment analysis
c_comment_upvote_max = 10000000000  # Set to max essentially
c_comment_upvote_min = 25

# 1. REDDIT STOCKS
s_goodAuth = {'AutoModerator'}   # authors whom comments are allowed more than once
s_uniqueCmt = True                # allow one comment per author per symbol
s_ignoreAuthP = {'example'}       # authors to ignore for posts
s_ignoreAuthC = {'example'}       # authors to ignore for comment
s_upvoteRatio = 0.70         # upvote ratio for post to be considered, 0.70 = 70%
s_ups = 20       # define # of upvotes, post is considered if upvotes exceed this #
s_limit = 100      # define the limit, comments 'replace more' limit
s_upvotes = 2     # define # of upvotes, comment is considered if upvotes exceed this #
s_picks = 10     # define # of picks here, prints as "Top ## picks are:"
s_picks_ayz = 5   # define # of picks for sentiment analysis
s_comment_upvote_max = 10000000000  # Set to max essentially
s_comment_upvote_min = 25

# ---------------------------------------------> TRAIN WORDS <------------------------------------------------------- #
# -> BLACKLIST <-
blacklist = {'I', 'NBA', 'ELON', 'WSB', 'THE', 'A', 'ROPE', 'YOLO', 'TOS', 'CEO', 'DD', 'IT', 'OPEN', 'ATH', 'PM', 'IRS',
             'FOR', 'DEC', 'BE', 'IMO', 'ALL', 'RH', 'EV', 'TOS', 'CFO', 'CTO', 'DD', 'BTFD', 'WSB', 'OK', 'PDT', 'RH',
             'KYS', 'FD', 'TYS', 'US', 'USA', 'IT', 'ATH', 'RIP', 'BMW', 'GDP', 'OTM', 'ATM', 'ITM', 'IMO', 'LOL', 'AM',
             'BE', 'PR', 'PRAY', 'PT', 'FBI', 'SEC', 'GOD', 'NOT', 'POS', 'FOMO', 'TL;DR', 'EDIT', 'STILL', 'WTF',
             'RAW', 'PM', 'LMAO', 'LMFAO', 'ROFL', 'EZ', 'RED', 'BEZOS', 'TICK', 'IS', 'PM', 'LPT', 'GOAT', 'FL', 'CA',
             'IL', 'MACD', 'HQ', 'OP', 'PS', 'AH', 'TL', 'JAN', 'FEB', 'JUL', 'AUG', 'SEP', 'SEPT', 'OCT', 'NOV', 'FDA',
             'IV', 'ER', 'IPO', 'MILF', 'BUT', 'SSN', 'FIFA', 'USD', 'CPU', 'AT', 'GG', 'Mar', 'one', 'One', 'see'}

# adding wsb/RedditClient flavour to vader to improve sentiment analysis, score: 4.0 to -4.0
WEIGHTED_WORDS = {
    'citron': -4.0,
    'hidenburg': -4.0,
    'moon': 4.0,
    'highs': 2.0,
    'mooning': 4.0,
    'long': 2.0,
    'short': -2.0,
    'call': 4.0,
    'calls': 4.0,
    'put': -4.0,
    'puts': -4.0,
    'break': 2.0,
    'tendie': 2.0,
    'tendies': 2.0,
    'town': 2.0,
    'overvalued': -3.0,
    'undervalued': 3.0,
    'buy': 4.0,
    'sell': -4.0,
    'hodl': 3.0,
    'gone': -1.0,
    'gtfo': -1.7,
    'paper': -1.7,
    'bullish': 3.7,
    'bearish': -3.7,
    'bagholder': -1.7,
    'gamestonk': 2.0,
    'stonk': 1.9,
    'green': 1.9,
    'money': 1.2,
    'print': 2.2,
    'rocket': 2.2,
    'bull': 2.9,
    'bear': -2.9,
    'pumping': -1.0,
    'sus': -3.0,
    'offering': -2.3,
    'rip': -4.0,
    'downgrade': -3.0,
    'upgrade': 3.0,
    'maintain': 1.0,
    'pump': 1.9,
    'hot': 1.5,
    'drop': -2.5,
    'rebound': 1.5,
    'crack': 2.5,
    'diamond hands': 4.0 }