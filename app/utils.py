'''Utility functions'''

def punctuations():
    '''list of punctuations commonly seen in our source files'''
    return [',', '"', '!', '.', ':', ';', '\n', '\\','“','”',
        '“','*','।','?',';',"'","’","(",")","‘","—"]

def numbers():
    '''list of number characters, to be used along with punctuations'''
    return ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

books = {
1: {"book_code": "gen", "book_name": "genesis"},
2: {"book_code": "exo", "book_name": "exodus"},
3: {"book_code": "lev", "book_name": "leviticus"},
4: {"book_code": "num", "book_name": "numbers"},
5: {"book_code": "deu", "book_name": "deuteronomy"},
6: {"book_code": "jos", "book_name": "joshua"},
7: {"book_code": "jdg", "book_name": "judges"},
8: {"book_code": "rut", "book_name": "ruth"},
9: {"book_code": "1sa", "book_name": "1 samuel"},
10: {"book_code": "2sa", "book_name": "2 samuel"},
11: {"book_code": "1ki", "book_name": "1 kings"},
12: {"book_code": "2ki", "book_name": "2 kings"},
13: {"book_code": "1ch", "book_name": "1 chronicles"},
14: {"book_code": "2ch", "book_name": "2 chronicles"},
15: {"book_code": "ezr", "book_name": "ezra"},
16: {"book_code": "neh", "book_name": "nehemiah"},
17: {"book_code": "est", "book_name": "esther"},
18: {"book_code": "job", "book_name": "job"},
19: {"book_code": "psa", "book_name": "psalms"},
20: {"book_code": "pro", "book_name": "proverbs"},
21: {"book_code": "ecc", "book_name": "ecclesiastes"},
22: {"book_code": "sng", "book_name": "song of solomon"},
23: {"book_code": "isa", "book_name": "isaiah"},
24: {"book_code": "jer", "book_name": "jeremiah"},
25: {"book_code": "lam", "book_name": "lamentations"},
26: {"book_code": "ezk", "book_name": "ezekiel"},
27: {"book_code": "dan", "book_name": "daniel"},
28: {"book_code": "hos", "book_name": "hosea"},
29: {"book_code": "jol", "book_name": "joel"},
30: {"book_code": "amo", "book_name": "amos"},
31: {"book_code": "oba", "book_name": "obadiah"},
32: {"book_code": "jon", "book_name": "jonah"},
33: {"book_code": "mic", "book_name": "micah"},
34: {"book_code": "nam", "book_name": "nahum"},
35: {"book_code": "hab", "book_name": "habakkuk"},
36: {"book_code": "zep", "book_name": "zephaniah"},
37: {"book_code": "hag", "book_name": "haggai"},
38: {"book_code": "zec", "book_name": "zechariah"},
39: {"book_code": "mal", "book_name": "malachi"},
41: {"book_code": "mat", "book_name": "matthew"},
42: {"book_code": "mrk", "book_name": "mark"},
43: {"book_code": "luk", "book_name": "luke"},
44: {"book_code": "jhn", "book_name": "john"},
45: {"book_code": "act", "book_name": "acts"},
46: {"book_code": "rom", "book_name": "romans"},
47: {"book_code": "1co", "book_name": "1 corinthians"},
48: {"book_code": "2co", "book_name": "2 corinthians"},
49: {"book_code": "gal", "book_name": "galatians"},
50: {"book_code": "eph", "book_name": "ephesians"},
51: {"book_code": "php", "book_name": "philippians"},
52: {"book_code": "col", "book_name": "colossians"},
53: {"book_code": "1th", "book_name": "1 thessalonians"},
54: {"book_code": "2th", "book_name": "2 thessalonians"},
55: {"book_code": "1ti", "book_name": "1 timothy"},
56: {"book_code": "2ti", "book_name": "2 timothy"},
57: {"book_code": "tit", "book_name": "titus"},
58: {"book_code": "phm", "book_name": "philemon"},
59: {"book_code": "heb", "book_name": "hebrews"},
60: {"book_code": "jas", "book_name": "james"},
61: {"book_code": "1pe", "book_name": "1 peter"},
62: {"book_code": "2pe", "book_name": "2 peter"},
63: {"book_code": "1jn", "book_name": "1 john"},
64: {"book_code": "2jn", "book_name": "2 john"},
65: {"book_code": "3jn", "book_name": "3 john"},
66: {"book_code": "jud", "book_name": "jude"},
67: {"book_code": "rev", "book_name": "revelation"}
}

def book_code(book_num):
    '''get the book for for the input bokk number'''
    if book_num in books:
        return books[book_num]['book_code'].upper()
    return None

stopwords = {
    "eng": { "postpositions" : ["t", "s"],
             "prepositions": ["a", "an", "the", "is", "are", "was", "were", "has",
             "have", "had", "with", "for"]},
    "hin": { "postpositions" : ["का", "कॆ", 'कि', 'की', 'कॊ', 'कि', 'को', 'मॆं', 'मॆ',
                'सॆ', 'हं', 'हॊ'],
             "prepositions": [] }
}

def prepositions(lang):
    '''returns the prepositions if defined for the language. else []'''
    if lang in stopwords and "prepositions" in stopwords[lang]:
        return stopwords[lang]["prepositions"]
    return []

def postpositions(lang):
    '''returns the postpositions if defined for the language. else []'''
    if lang in stopwords and "postpositions" in stopwords[lang]:
        return stopwords[lang]["postpositions"]
    return []
