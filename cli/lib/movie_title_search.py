from .search_utils import (load_movies, DEFAULT_SEARCH_LIMIT)

def search_command(query: str, limit: int = DEFAULT_SEARCH_LIMIT):

    found_movies = []

    movies = load_movies()

    for movie in movies:
        if query.lower() in movie['title'].lower():

            found_movies.append(movie['title'])
            if len(found_movies) >= limit:
                break

    return found_movies
