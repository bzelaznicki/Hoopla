import string
from .search_utils import (load_movies, DEFAULT_SEARCH_LIMIT, load_stopwords, CACHE_DIRECTORY)
from nltk.stem import PorterStemmer
from collections import defaultdict
import os
import pickle



def build_command():
    print("Creating inverted index...")
    index = InvertedIndex()
    index.build()
    index.save()
    


def search_command(query: str, limit: int = DEFAULT_SEARCH_LIMIT):

    processed_query = process_text(query)
    found_movies = []

    movies = load_movies()

    for movie in movies:
        q_tokens = split_text(processed_query)
        processed_title = process_text(movie['title'])
        t_tokens = split_text(processed_title)
        if find_matching_token(q_tokens, t_tokens):
            found_movies.append(movie['title'])
            if len(found_movies) >= limit:
                break
    return found_movies


class InvertedIndex:
    def __init__(self):
        self.index: dict[str, set] = defaultdict(set) 
        self.docmap: dict[int, dict] = {}

    def __add_document(self, doc_id, text):
        processed = process_text(text)
        split = split_text(processed) 
        for t in split:
            self.index[t].add(doc_id)

    def get_documents(self, term):
        documents = self.index.get(term.lower(),set())        

        return sorted(documents) 

    def build(self):
        movies = load_movies() 
        for m in movies:
            self.docmap[m['id']] = m
            self.__add_document(m['id'], f"{m['title']} {m['description']}")




    def save(self):
        os.makedirs(CACHE_DIRECTORY, exist_ok=True)
        
        index_file = os.path.join(CACHE_DIRECTORY, "index.pkl")
        docmap_file = os.path.join(CACHE_DIRECTORY, "docmap.pkl")
        with open(index_file, "wb") as f:
            pickle.dump(self.index, f)

        with open(docmap_file, "wb") as f:
            pickle.dump(self.docmap, f)
        
def process_text(text: str) -> str:
    text = text.lower()
    punc = str.maketrans("", "", string.punctuation)

    text = text.translate(punc)
    return text


def split_text(text: str) -> list[str]:
    stemmer = PorterStemmer()
    tokens = text.split()
    stopwords = load_stopwords()
    text_tokens = []
    for token in tokens:
        token = stemmer.stem(token)
        if token in stopwords:
            continue
        if token:
            
            text_tokens.append(token)
    return text_tokens 


def find_matching_token(q_tokens: list[str], t_tokens: list[str]) -> bool:
    for q_token in q_tokens:
        for t_token in t_tokens:
            if q_token in t_token:
                return True 

    return False 

