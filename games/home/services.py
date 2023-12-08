from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Genre, Publisher

import random


def getFeaturedGames(repo: AbstractRepository):
    games = repo.getAllGames()
    return random.sample(games, 3)
