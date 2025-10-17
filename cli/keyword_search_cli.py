#!/usr/bin/env python3

import argparse

from lib.movie_title_search import search_command, build_command

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    build_parser= subparsers.add_parser("build", help="Build the index")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            found_movies = search_command(args.query )
            
            for idx, item in enumerate(found_movies): 
                print(f"{idx+1}: {item}")
                
        case "build":
            build_command()        
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
