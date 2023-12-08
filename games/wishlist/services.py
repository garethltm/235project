from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Wishlist, User


def add_wishlist(repo: AbstractRepository, user: User, wishlist: Wishlist):
    return repo.add_wishlist(user, wishlist)


def remove_game_from_wishlist(repo: AbstractRepository, user: User, game: Game):
    return repo.remove_game_from_wishlist(user, game)

