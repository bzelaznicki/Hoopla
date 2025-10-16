import string
from .search_utils import (load_movies, DEFAULT_SEARCH_LIMIT)

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


def process_text(text: str) -> str:
    text = text.lower()
    punc = str.maketrans("", "", string.punctuation)

    text = text.translate(punc)
    return text


def split_text(text: str) -> list[str]:
    tokens = text.split()
    
    text_tokens = []
    for token in tokens:
        if token:
            text_tokens.append(token)
    return text_tokens 


def find_matching_token(q_tokens: list[str], t_tokens: list[str]) -> bool:
    for q_token in q_tokens:
        for t_token in t_tokens:
            if q_token in t_token:
                return True 

    return False 

