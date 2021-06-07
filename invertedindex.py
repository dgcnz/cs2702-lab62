from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk import word_tokenize, sent_tokenize
from typing import List, Dict, Set
from collections import Counter, defaultdict
import bisect
import string

# ********************* PREPROCESSOR ***************************


class Preprocessor:
    stemmer = SnowballStemmer("spanish")
    stop = stopwords.words('spanish')

    def __init__(self):
        pass

    def valid(self, token: str):
        return token not in self.stop and token not in string.punctuation

    def clean(self, word: str):
        return self.stemmer.stem(word.lower())

    def normalize(self, document: str):
        tokens = word_tokenize(document)
        return [self.clean(tkn) for tkn in tokens if self.valid(tkn)]


def preprocess(f):
    def wrapper(instance, *args):
        return f(instance, *[instance.p.clean(str(arg)) for arg in list(args)])

    return wrapper


# ************************** UTILS ********************************


def build_inverted_index(documents: List[str], p: Preprocessor, k: int):
    word_cnt = Counter()
    tokenized_docs = [p.normalize(doc) for doc in documents]
    for doc in tokenized_docs:
        for tkn in doc:
            word_cnt[tkn] += 1

    indexed_words = [word[0] for word in word_cnt.most_common(k)]
    iix = InvertedIndex(indexed_words, p)
    for doc in tokenized_docs:
        iix.add(doc)

    return iix


def contains(a, x):
    i = bisect.bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return True
    return False


# ********************* INVERTED INDEX ***************************


class InvertedIndex:
    n: int = 0
    index: Dict[str, List[int]] = defaultdict(list)
    indexed_words: Set[str] = {}
    p: Preprocessor = None

    def __init__(self, indexed_words: List[str], p: Preprocessor):
        self.indexed_words = set(indexed_words)
        self.p = p

    def add(self, doc_tkns: List[str]):
        for tkn in doc_tkns:
            if tkn in self.indexed_words and not contains(
                    self.index[tkn], self.n):
                bisect.insort(self.index[tkn], self.n)
        self.n += 1

    @preprocess
    def sources(self, word: str):
        if word in self.indexed_words:
            return self.index[word]
        return []


def OR(a: List[int], b: List[int]) -> List[int]:
    ans = []
    i: int = 0
    j: int = 0
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            ans.append(a[i])
            i += 1
        elif b[j] < a[i]:
            ans.append(b[j])
            j += 1
        else:
            ans.append(a[i])
            i += 1
            j += 1

    while i < len(a):
        ans.append(a[i])
        i += 1

    while j < len(b):
        ans.append(b[j])
        j += 1

    return ans


def AND(a: List[int], b: List[int]) -> List[int]:
    ans = []

    i: int = 0
    j: int = 0
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            i += 1
        elif b[j] < a[i]:
            j += 1
        else:
            ans.append(a[i])
            i += 1
            j += 1
    return ans


def ANDNOT(a: List[int], b: List[int]) -> List[int]:
    ans = []

    i: int = 0
    j: int = 0
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            ans.append(a[i])
            i += 1
        elif b[j] < a[i]:
            j += 1
        else:
            i += 1
            j += 1

    while i < len(a):
        ans.append(a[i])
        i += 1

    return ans
