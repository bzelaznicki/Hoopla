import string
from .search_utils import (load_movies, DEFAULT_SEARCH_LIMIT)

def search_command(query: str, limit: int = DEFAULT_SEARCH_LIMIT):

    query = process_text(query)
    found_movies = []

    movies = load_movies()

    for movie in movies:
        movie_title = process_text(movie['title'])
        if query in movie_title: 

            found_movies.append(movie['title'])
            if len(found_movies) >= limit:
                break

    return found_movies


def process_text(text: str) -> str:
    text = text.lower()
    punc = str.maketrans("", "", string.punctuation)

    text = text.translate(punc)
    return text
