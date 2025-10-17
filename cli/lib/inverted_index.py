from .movie_title_search import process_text, split_text
from .search_utils import load_movies, CACHE_DIRECTORY
from collections import defaultdict
import os
import pickle

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
        
