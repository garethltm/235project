from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Genre, Publisher, User, Wishlist


class UnknownUserException(Exception):
    pass


def getAllGames(repo: AbstractRepository):
    return repo.getAllGames()


def getAllGenresSorted(repo: AbstractRepository):
    return sorted(repo.getAllGenres(), key=lambda genre: genre.genre_name)


def getPublishers(repo: AbstractRepository):
    return repo.getAllPublishers()


def paginateLists(list: list, page: int, per_page: int):
    start_i = (page - 1) * per_page
    end_i = start_i + per_page
    return list[start_i:end_i]


def getUser(username: str, repo: AbstractRepository):
    user = repo.getUser(username)
    if user is None:
        raise UnknownUserException
    return user


def getGameById(repo: AbstractRepository, game_id: int):
    return repo.getGameById(game_id)

def calculate_average_rating(reviews):
    if len(reviews) == 0:
        return "No Reviews Yet"

    total_ratings = sum(review.rating for review in reviews)
    average_rating = total_ratings / len(reviews)
    return round(average_rating, 1)


def get_wishlist(repo: AbstractRepository, user: User):
    if repo.get_wishlist(user) is None:
        repo.add_wishlist(user, Wishlist(user))
    return repo.get_wishlist(user)


def is_game_in_wishlist(repo: AbstractRepository, user: User, game: Game):
    if repo.get_wishlist(user) is None:
        repo.add_wishlist(user, Wishlist(user))
    wishlist = repo.get_wishlist(user)
    return game in wishlist.list_of_games()
