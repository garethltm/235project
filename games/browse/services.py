from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Genre, User, Wishlist

class UnknownUserException(Exception):
    pass


def getGamesByGenres(repo: AbstractRepository, genre_names: list[str]):
    genres = set()
    if genre_names is None or len(genre_names) == 0 or genre_names == ['']:
        return repo.getAllGames()
    for genre_name in genre_names:
        genres.add(Genre(genre_name))
    return repo.getGamesByGenres(list(genres))


def searchGameByTitle(games: list[Game], search_term: str):
    result = []
    for game in games:
        if search_term.lower() in game.title.lower():
            result.append(game)
    return result


def searchGameByGenre(games: list[Game], search_term: str):
    if search_term[-1] == ";":  
        search_term = search_term[:-1]
    result = []
    search_terms = search_term.lower().split(";")
    for game in games:
        game_genres = [genre.genre_name.lower() for genre in game.genres]
        if all(term in game_genres for term in search_terms):
            result.append(game)
    return result


def searchGameByPublisher(games: list[Game], search_term: str):
    result = []
    for game in games:
        if search_term.lower() in game.publisher.publisher_name.lower():
            result.append(game)
    return result
