import json

from FAIR.Core import FILE, DICT
"""
-> Rules
1. Each "topic" has 3 attributes, a. search_terms b. weighted_terms c. rss_feeds
2. Each "topics" attribute starts with the topic name, underscores only.
"""

# TODO: -? meta_names? shit..
meta_names = FILE.load_dict_from_file("meta_names")

# -------------------------------------> CATEGORIES AND THEIR KEY-TERMS <-------------------------------------------- #
class Terms:
    # -> If any lists are added, add here.
    keys = ["search_terms", "weighted_terms", "rss_feeds"]

    def get_var(self, var_name):
        """  GETTER HELPER  """
        return self.__getattribute__(var_name)

    @staticmethod
    def combine_var_name(topic, term):
        return topic + "_" + term

    extended_stop_words = ["with", "more", "s", "has", "have", "they", "this", "their", "was", "not", "said", "also",
                           "most", "but", "from", "whether", "so", "ways", "if", "were", "have", "my", "being", "re",
                           "what", "where", "many", "other", "t", "i", "than", "had", "who", "amoung", "get", "say",
                           "could", "way", "use", "new", "using", "need", "one", "like", "youll", "youre", "you",
                           "well", "add", "make", "want", "first", "set", "value", "text"]

    ####################################################################################################################
    # -> 0. General <-
    ####################################################################################################################
    general = "General"
    general_search_terms = ["business"]
    general_weighted_terms = {"thousand": 5, "million": 5, "billion": 5, "trillion": 5, "space": 2, "mainstream": 3, "property": 2,
                              "network": 2, "future": 2, "crowdfunding": 4, "economy": 3, "market valuation": 5, "Metrics": 5,
                              "market action": 5, "dominance": 5, "assets": 5, "Drops": 5, "Dips": 5, "value proposition": 5,
                              "fluctuates": 5, "portfolio": 5, "crash": 5, "optimistic": 5, "projections": 5, "hedge fund": 5,
                              "hedgefund": 5, "holders": 5, "holder": 3, "owns": 5, "fund": 5, "game": 5, "gaming": 5,
                              "market capitalization": 5, "developer": 5, "development": 5, "develop": 5, "engineer": 5,
                              "engineering": 5, "4g": 10, "5g": 10, "6g": 10, "fiber": 10, "optical": 10, "fiber optic": 10,
                              "business": 5, "businesses": 5, "meeting": 5, "meetings": 5, "committee": 5, "fed": 10,
                              "the fed": 10, "federal": 5, "federal reserve": 20, "bull market": 5, "bear market": 5,
                              "inflation": 10, "deflation": 10, "plunges": 10, "leaked": 50, "announcement": 10}
    general_rss_feeds = ["http://feeds.marketwatch.com/marketwatch/topstories/",
                         "http://www.infoworld.com/index.rss",
                         "http://www.itworldcanada.com/feed",
                         "http://www.macworld.com/index.rss",
                         "http://www.roadtovr.com/feed",]

    ####################################################################################################################
    # -> 3. Weed <-
    ####################################################################################################################
    weed = "Weed"
    weed_search_terms = ['legalization', 'cannabis stock', 'cannabinoid-therapeutics', 'cannabinoid',
                         'medicinal marijuana', 'cannabis investors', 'pot stock', 'cannabis legalization',
                         'federal decriminalization', 'marijuana stocks', 'marijuana legalization bills',
                         'cannabis market', 'cannabis', 'weed', 'marijuana']
    weed_weighted_terms = {"legalization": 50, "decriminalization": 50, "cannabinoid": 100, "cannabis": 200,
                           "marijuana": 200, "pot": 20, "weed": 100, "stock": 2, "therapeutics": 20, "medicinal": 100}
    weed_rss_feeds = []

    ####################################################################################################################
    # -> 3. Stocks <-
    ####################################################################################################################
    stocks = "Stocks"
    stocks_search_terms = ['merge', 'merger', 'acquisition', 'stepping down', 'IPO', 'partnering', 'stocks', 'economy']
    stocks_weighted_terms = {'merge': 10, 'merger': 50, 'acquisition': 100, 'stepping down': 50, 'IPO': 50, 'partnering': 50,
                             'ROI': 20, 'Incentivize': 20, 'Monetize': 50, 'Deliverable': 50, 'Margin': 50, 'Accounts Payable': 50,
                             'Accounts Receivable': 20, 'Capital': 20, 'Fixed Costs': 50, 'Variable Costs': 50, 'Gross': 10, 'Net': 10,
                             'Benchmarking': 20, 'KPI': 20, 'Metrics': 20, 'Performance Review': 50, 'R&D': 50, 'B2B': 50,
                             'B2C': 20, 'B2G': 20, 'Scalable': 20, 'Responsive Design': 50, 'Core Competency': 50, 'Niche Market': 10,
                             'Marketing': 20, 'Market Research': 20, 'Market Penetration': 50, 'Inbound Marketing': 50, 'Assets': 5,
                             'Liabilities': 50, 'Revenue': 20, 'Expenses': 20, 'Balance sheet': 50, 'Net profit': 20, 'Net loss': 10,
                             'Profit margin': 5, 'Cash flow': 2, 'cash flow': 2, 'Depreciation': 5, 'Fixed Asset': 5, 'Gross Profit': 10,
                             'Intangible Asset': 15, 'Liquidity': 20, 'Profit & Loss': 50, 'Shareholders Equity': 100, 'Annual Percentage': 10,
                             'Appraisal': 15, 'Balloon Loan': 50, 'Bankruptcy': 50, 'Bootstrapping': 25, 'Business Credit': 50, 'Collateral': 10,
                             'Credit Limit': 50, 'Debt Consolidation': 50, "sell off": 50, "target market": 10, "stockholder": 100,
                             "stockholders": 100, "surges": 20, "surge": 10,
                             "Change management": 100, "Lay off": 100, }
    stocks_rss_feeds = ["http://feeds.marketwatch.com/marketwatch/topstories/", "https://seekingalpha.com/feed.xml",
                        "https://www.investing.com/rss/news_25.rss", "https://blog.wallstreetsurvivor.com/feed/",
                        "https://stockstotrade.com/blog/feed/",
                        "https://www.cnbc.com/id/20409666/device/rss/rss.html?x=1",
                        "http://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms",
                        "https://mebfaber.com/feed/", "http://welcome.philstockworld.com/feed/",
                        "https://www.reddit.com/r/stocks/.rss"]
    stocks_reddit_communities = ['wallstreetbets', 'WallStreetbetsELITE', 'deepfuckingvalue', 'stocks', 'investing',
                                 'stockmarket']
    stocks_twitter_users = ['mcuban', 'elonmusk', 'PeterLBrandt', 'CNBC', 'SJosephBurns', 'elerianm', 'IBDinvestors',
                            'jimcramer', 'bespokeinvest', 'wsbmod', 'galgitron', 'thevrsoldier', 'glewmecorp']
    ####################################################################################################################
    # -> X. German <-
    ####################################################################################################################

    german = "German"
    german_search_terms = ['merge', 'merger', 'acquisition', 'stepping down', 'IPO', 'partnering']
    german_weighted_terms = {'merge': 10, 'merger': 10, 'acquisition': 10, 'stepping down': 10, 'IPO': 10, 'partnering': 10,
                             "Change management": 10, "Lay off": 10, "Kündigungen": 10, "Freiberufler": 10,
                             "Freelancer": 10, "Interim": 10, "Interim manager": 10, "Accounting": 10,
                             "Buchführung": 10, "Finance": 10, "Finanzen": 10, "Expansion": 10, "Stellenabbau": 10,
                             "Stellenaufbau": 10, "Einkauf": 10, "Michael page": 10, "Robert half": 10, "Hays": 10,
                             "Human Resources": 10, "HR": 10, "International": 10, "Business": 10, "Unternehmen": 10,
                             'BILANZ': 2, 'VERMÖGENSWERTE': 2, 'VERBINDLICHKEITEN': 5, 'EIGENKAPITAL': 5, 'EINNAHMEN': 5, 'AUFWAND': 5,
                             'GEWINN': 2, 'NETTOVERLUST': 2, 'KAPITALFLUSSRECHNUNG': 5, 'GEWINNMARGE': 5, 'VARIABLE KOSTEN': 5,
                             'Geld verdienen': 5, 'BARGELDFLUSS': 2, 'FESTKOSTEN': 2, 'Fixkosten': 5, 'Netto': 5, 'KPI': 5,
                              'Kernkompetenz': 5, 'Lieferbar': 2, 'Kreditorenbuchhaltung': 2, 'Debitorenbuchhaltung': 5,
                             'Skalierbar': 5, 'Leistungsüberprüfung': 5, 'Alleinstellungsmerkmal': 5}

    german_rss_feeds = ["https://www.wiwo.de/contentexport/feed/rss/schlagzeilen",
                        "https://www.wiwo.de/contentexport/feed/rss/themen",
                        "https://www.wiwo.de/contentexport/feed/rss/unternehmen",
                        "https://www.wiwo.de/contentexport/feed/rss/finanzen",
                        "https://rss.dw.com/xml/rss-de-all",
                        "https://rss.dw.com/xml/rss-de-eco",
                        "https://www.wirtschaftskurier.de/titelthema.html?type=9818",
                        "http://www.wirtschaftskurier.de/unternehmen.html?type=9818",
                        "http://www.wirtschaftskurier.de/finanzen.html?type=9818",
                        "http://www.stern.de/feed/standard/wirtschaft/",
                        "https://www.iwkoeln.de/rss/arbeitsmarkt.xml",
                        "https://www.iwkoeln.de/rss/bildung-und-fachkraefte.xml",
                        "https://www.spiegel.de/international/index.rss", "http://newsfeed.zeit.de/index",
                        "https://www.thelocal.de/feeds/rss.php", "https://www.deutschland.de/en/feed-news/rss.xml",
                        "https://itb-berlin-news.com/feed/", "https://munichnow.com/feed/",
                        "http://feeds.t-online.de/rss/politik", "http://munichnow.com/feed",
                        "https://newsfeed.zeit.de/index", "https://itb-berlin-news.com/feed",
                        "https://www.deutschland.de/en/feed-news/rss.xml", "https://www.spiegel.de/international/index.rss",
                        "https://www.thelocal.de/feeds/rss.php"
                        ]

    german_reddit_communities = ['wallstreetbets', 'WallStreetbetsELITE', 'deepfuckingvalue', 'stocks', 'investing',
                                 'stockmarket']
    german_twitter_users = ['mcuban', 'elonmusk', 'PeterLBrandt', 'CNBC', 'SJosephBurns', 'elerianm', 'IBDinvestors',
                            'jimcramer', 'bespokeinvest', 'wsbmod', 'galgitron', 'thevrsoldier', 'glewmecorp']

    ####################################################################################################################
    # -> X. Crypto <-
    ####################################################################################################################
    crypto = "Crypto"
    crypto_search_terms = ["decentralized", "crypto", "cryptocurrency", "bitcoin", "blockchain", "smart contract"]
    crypto_weighted_terms = {"metaverse": 20, "roblox": 20, "nft": 50, "nfts": 50, "nft's": 50,
                             "decentraland": 20, "glewme": 10, "meta": 20, "sandbox": 20, "mana": 20, "parcel": 20,
                             "tokens": 20, "fork": 5, "hardfork": 20, "softfork": 20, "hard fork": 20, "soft fork": 20,
                             "virtual": 20, "vr": 20, "nonfungible": 20, "stacking": 20, "decentralized": 20, "crypto": 20,
                             "cryptocurrency": 100, "blockchain": 100, "dapp": 45, "land": 20, "opensea": 10, "ethereum": 100,
                             "bitcoin": 100, "xrp": 100, "ripple": 100, "xlm": 20, "web3": 100, "pos": 20, "poe": 20, "iot": 4,
                             "btc": 100, "eth": 100, "Nano Collaborative": 5, "nano": 100, "Banano": 20,
                             "time wonderland": 50, "olympus dao": 20, "sushiswap": 200, "pancakeswap": 20,
                             "Stablecoins": 10, "stablecoin": 50, "altcoin market": 100, "alt market": 100, "alt season": 100,
                             "erc7201": 100, "erc1155": 50, "smart contract": 100, "solidity": 10, "truffle": 20, "ganache": 20,
                             "dex": 20, "defi": 20, "decentralized exchange": 100, "centralized exchange": 20, "ico": 10,
                             "wallet": 20, "minable": 20, "coin": 10, "token": 10}

    crypto_rss_feeds = ["https://cointelegraph.com/rss", "https://coindesk.com/feed", "https://news.bitcoin.com/feed",
                        "https://minergate.com/blog/feed/", "https://coinjournal.net/feed",
                        "https://cryptoinsider.com/feed", "http://www.newsbtc.com/feed",
                        "https://twitter.com/jaxx_io/feed", "https://bitcoinmagazine.com/feed",
                        "https://www.crypto-news.net/feed", "https://www.cryptoninjas.net/feed",
                        "https://ethereumworldnews.com/feed", "https://bravenewcoin.com/feed",
                        "http://www.financemagnates.com/feed", "http://www.cryptoquicknews.com/feed",
                        "http://cryptscout.com/feed", "http://www.coinnewsasia.com/feed"]

    ####################################################################################################################
    # -> X. Metaverse <-
    ####################################################################################################################
    metaverse = "Metaverse"
    metaverse_search_terms = ["metaverse", "virtual world", "vr", "decentraland", "decentralized", "nft",
                              "decentralized world", "augmented reality", "blockchain", "ethereum", "virtual reality"]
    metaverse_search_terms_test = ["metaverse", "virtual world", "nft"]
    metaverse_weighted_custom_terms = {
        "0xearth": 50,
        "3d": 30,
        "activision blizzard": 30,
        "alterverse": 30,
        "amd": 50,
        "ar glasses": 10,
        "ar goggles": 10,
        "ar headset": 10,
        "artificial intelligent": 10,
        "arvr": 10,
        "assets": 20,
        "augmented reality": 30,
        "avatar": 20,
        "average price": 5,
        "binance": 10,
        "bitcoin": 5,
        "blockchain": 20,
        "bought": 5,
        "btc": 2,
        "build": 3,
        "building": 3,
        "centralized": 20,
        "collectible": 10,
        "collectibles": 10,
        "creator economy": 50,
        "crypto based": 5,
        "cryptobased": 5,
        "cryptocountries": 20,
        "cryptocurrency": 10,
        "dapp": 20,
        "decentraland": 5,
        "decentralisation": 10,
        "decentralised": 20,
        "decentralised economy": 30,
        "decentralized": 10,
        "decentralized app": 20,
        "decentralized application": 20,
        "decentralized economy": 30,
        "decentralized world": 50,
        "democratisation": 10,
        "denations": 20,
        "disrupt": 5,
        "disruption": 5,
        "edge computing": 10,
        "eth": 30,
        "ether": 30,
        "ethereum": 30,
        "etherland": 50,
        "fintech": 20,
        "fungible": 30,
        "gaming": 20,
        "gained momentum": 30,
        "glewme": 100,
        "glewme city": 100,
        "glewmecity": 100,
        "gpu": 10,
        "haptic": 10,
        "haptic suit": 15,
        "haptics": 10,
        "hatchables": 20,
        "headset": 5,
        "horizon": 10,
        "horizon world": 10,
        "horizon worlds": 10,
        "human interface": 10,
        "infrastructure": 5,
        "innovation": 3,
        "intel": 20,
        "investment": 5,
        "investment opportunity": 10,
        "iot": 10,
        "land": 20,
        "loopring": 40,
        "mana": 50,
        "meta": 30,
        "meta key": 30,
        "meta platform": 50,
        "meta platforms": 50,
        "metaverse": 200,
        "metaverse industry": 200,
        "microsoft": 20,
        "multiple platforms": 10,
        "nft": 20,
        "NFT Marketplace": 20,
        "nft worlds": 20,
        "nft's": 20,
        "nfts": 20,
        "Niantic": 10,
        "nonfungible": 15,
        "nvidia": 30,
        "oculus": 30,
        "opensea": 50,
        "ovr land": 20,
        "ownable": 50,
        "ownables": 50,
        "parcel": 70,
        "play earn": 50,
        "poe": 10,
        "polka city": 30,
        "pos": 10,
        "property value": 20,
        "real estate": 20,
        "roblox": 50,
        "Roblox Corporation": 20,
        "sandbox": 50,
        "sft": 45,
        "semi fungible"
        "sha-256": 10,
        "sha256": 10,
        "smart chain": 10,
        "snap": 10,
        "solana": 20,
        "sold": 10,
        "somnium": 20,
        "somnium space": 20,
        "spatial computing": 30,
        "speculation": 5,
        "stake": 5,
        "staking": 5,
        "stock": 10,
        "store value": 10,
        "state channel": 10,
        "superworld": 100,
        "TakeTwo": 10,
        "the sandbox": 30,
        "token": 20,
        "tokens": 20,
        "treeverse": 20,
        "ue5": 50,
        "unity": 50,
        "unreal engine": 50,
        "Vans World": 10,
        "vegas city": 20,
        "victoria": 20,
        "victoria vr": 50,
        "virtual": 15,
        "virtual land": 100,
        "virtual meeting": 75,
        "virtual meetings": 75,
        "virtual reality": 75,
        "virtual world": 100,
        "virtual worlds": 100,
        "vr": 20,
        "vr glasses": 10,
        "vr goggles": 10,
        "vr headset": 10,
        "vr world": 20,
        "war raiders": 20,
        "wearable": 5,
        "wearables": 5,
        "web3": 20,
        "web3 gaming": 20,
        "web3 game": 20
                                }
    # -> This master weighted list comes dynamically from meta_names.json
    metaverse_weighted_terms = DICT.merge_dicts(meta_names, metaverse_weighted_custom_terms)
    metaverse_rss_feeds = [ "https://cointelegraph.com/rss", "https://coindesk.com/feed", "https://news.bitcoin.com/feed",
                            "https://minergate.com/blog/feed/", "https://coinjournal.net/feed",
                            "https://cryptoinsider.com/feed", "http://www.newsbtc.com/feed",
                            "https://twitter.com/jaxx_io/feed", "https://bitcoinmagazine.com/feed",
                            "https://www.crypto-news.net/feed", "https://www.cryptoninjas.net/feed",
                            "https://ethereumworldnews.com/feed", "https://bravenewcoin.com/feed",
                            "http://www.financemagnates.com/feed", "http://www.cryptoquicknews.com/feed",
                            "http://cryptscout.com/feed", "http://www.coinnewsasia.com/feed",
                            "https://decentraland.org/blog/feed.xml"]

    ####################################################################################################################
    # -> 5. Android <-
    ####################################################################################################################
    android = "Android"
    android_search_terms = ["android", "android os", "android studio", "android developer", "kotlin", "jetbrains"]
    android_weighted_terms = {"android": 2, "java": 2, "kotlin": 2, "gradle": 3, "coroutine": 3, "jetpack": 2,
                              "async": 2, "google": 2, "vr": 2, "ar": 2, "androiddevsummit": 5, "certification": 5,
                              "beta": 2, "alpha": 2, "canary": 2, "jetbrains": 2, "api": 2, "summit": 3, "stable": 3,
                              "android os": 5, "android developer": 5, "android studio": 5, "virtual reality": 10,
                              "augmented reality": 10, "android dev": 3, "wear os": 3, "app bundle": 5,
                              "app bundles": 5, "google play": 3, "jetpack compose": 5, "dev kit": 5,
                              "development kit": 10, "firebase": 2}
    android_rss_feeds = ["https://www.reddit.com/r/Android.rss", "https://www.androidauthority.com/feed/",
                         "http://feeds.feedburner.com/blogspot/hsDu", "https://medium.com/feed/tag/android",
                         "https://www.reddit.com/r/androiddev.rss", "https://proandroiddev.com/feed",
                         "https://medium.com/feed/@ian-alexander",
                         "http://feeds.feedburner.com/FirebaseBlog", "https://blog.jetbrains.com/kotlin/feed/",
                         "http://feeds.feedburner.com/GDBcode"]
    ####################################################################################################################
    # -> 5. apple <-
    ####################################################################################################################
    apple = "apple"
    apple_search_terms = ["ios", "apple", "apple products", "iphone", "macbook", "apple developer"]
    apple_weighted_terms = {"apple": 100, "ios": 100, "apple inc": 100, "iphone": 50, "mac": 50, "macintosh": 50,
                            "product release": 50, "product releases": 50, "new product": 50, "road map": 20, "apple watches": 50,
                            "new products": 50, "m1": 20, "imac": 50, "apple tv": 50, "airtag": 50, "airtags": 50,
                            "ipad": 50, "pro": 10, "new": 5, "product": 5, "products": 5, "mac pro": 50, "macbook": 50,
                            "macbook pro": 50, "app store": 20, "project": 10, "tim cook": 20, "m1 pro chip": 20,
                            "new model": 20, "new models": 20, "air": 10, "m2": 20, "m2 chip": 20, "apple software": 20,
                            "apples software": 20, "conference": 10, "peek": 5, "airpods": 50, "airpod": 50, "max": 10,
                            "silicon chip": 10, "silicon chips": 10, "apple silicon": 10, "homepod": 50, "series": 10,
                            "rumor": 10, "rumors": 10, "announced": 30, "update": 10, "updates": 10, "exclusive": 10}
    apple_rss_feeds = []
    ####################################################################################################################
    # -> 6. programming <-
    ####################################################################################################################
    programming = "programming"
    programming_search_terms = ["programming", "software development", "computer science", "software engineer",
                                "coding", "computer science", "cyber security"]
    programming_weighted_terms = {"kotlin": 100, "computer science": 100, "java": 100, "javascript": 100, "swift": 100,
                                  "python": 100, "jvm": 20, "php": 50, "bash": 50, "scala": 100, "sql": 100, "nosql": 100,
                                  "mongodb": 100, "mongo": 20, "perl": 50, "c": 50, "c++": 50, "c#": 50, "ruby": 100,
                                  "go": 20, "web based applications": 25, "devops": 20, "programming langauge": 100,
                                  "programming languages": 100, "apps": 10, "application": 10, "applications": 10,
                                  "object oriented": 100, "low level": 10, "gui development": 10, "backend": 10,
                                  "lifecycle": 10, "development": 10, "developers": 10, "html": 50, "css": 50, "xml": 50,
                                  "script": 10, "scripting language": 50, "scripting languages": 50, "unix": 50,
                                  "shell": 10, "package": 10, "library": 10, "module": 10, "dependency": 10, "high level": 10,
                                  "objc": 100, "objective c": 100, "jetpack": 20, "async": 50, "androiddevsummit": 50,
                                  "certification": 5, "beta": 20, "alpha": 20, "canary": 20, "jetbrains": 50, "api": 20,
                                  "summit": 10, "stable": 10, "android os": 5, "android developer": 50,
                                  "android studio": 50, "android dev": 30, "wear os": 15, "app bundle": 50,
                                  "app bundles": 5, "google play": 20, "jetpack compose": 50, "dev kit": 50,
                                  "development kit": 50, "firebase": 50, "debugger": 50, "code": 10, "senior": 10,
                                  "coding": 10, "programming": 50, "programmer": 50, "virtual machine": 20, "software": 20,
                                  "app": 10, "gradle": 30, "coroutine": 30, "xcode": 50, "algo": 10
                                  }

    programming_rss_feeds = ["http://www.thecrazyprogrammer.com/feed", "https://www.sitepoint.com/feed/",
                             "https://www.raywenderlich.com/feed", "https://stackabuse.com/rss/",
                             "https://blog.jooq.org/feed/", "http://feeds.hanselman.com/ScottHanselman",
                             "https://tympanus.net/codrops/feed/", "https://medium.com/feed/better-programming",
                             "https://medium.com/feed/a-technologists-pov", "https://blog.codepen.io/feed/",
                             "https://hackr.io/programming/rss.xml", "https://www.techiedelight.com/feed/",
                             "https://davidwalsh.name/feed", "https://codesignal.com/feed/",
                             "https://alistapart.com/site/rss", "https://www.codingdojo.com/blog/feed",
                             "https://fueled.com/feed/", "https://www.codewall.co.uk/feed/"]


if __name__ == '__main__':
    t = Terms()
    d = t.metaverse_weighted_custom_terms
    new_dict = {}
    sortednames = sorted(d.keys(), key=lambda x: x.lower())
    i = 0
    for word in sortednames:
        new_dict[word] = d[word]
    print(json.dumps(new_dict, indent=2))
