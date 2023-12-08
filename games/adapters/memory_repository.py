from pathlib import Path

import random

from werkzeug.security import generate_password_hash

from games.adapters.repository import AbstractRepository, RepositoryException
from games.domainmodel.model import Genre, Game, Publisher, Review, User, Wishlist

class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__reviews = list()
        self.__games = list()
        self.__genres = list()
        self.__publishers = list()
        self.__wishlists = dict()
        self.__users = list()


    # Game Related Methods
    def add_game(self, game: Game):
        if game not in self.__games:
            self.__games.append(game)

    def getAllGames(self) -> list[Game]:
        return self.__games

    def getGameById(self, id: int):
        for game in self.__games:
            if game.game_id == id:
                return game
        return None

    def getGamesByGenres(self, genres: list[Genre]) -> list[Game]:  # Similar to get_articles_by_date in COVID app??
        games = set()
        if genres is None or len(genres) == 0 or genres[0] == '':
            return self.__games
        for game in self.__games:
            # print(game.genres)
            for genre in genres:
                if genre in game.genres:
                    games.add(game)
        return list(games)

    # Genre Related Methods
    def add_genre(self, genre: Genre):
        if genre not in self.__genres:
            self.__genres.append(genre)

    def getAllGenres(self) -> list[Genre]:
        return self.__genres

    # Publisher Related Methods
    def add_publisher(self, publisher: Publisher):
        if publisher not in self.__publishers:
            self.__publishers.append(publisher)

    def getAllPublishers(self) -> list[Publisher]:
        return list(self.__publishers)

    # Review Related Methods
    def add_review(self, review: Review):
        if review not in self.__reviews:
            self.__reviews.append(review)

    def getAllReviews(self) -> list[Review]:
        return self.__reviews

    # Wishlist Related Methods
    def get_wishlist(self, user: User):
        # if user not in self.__wishlists:
        #     self.__wishlists[user] = Wishlist(user)
        if user not in self.__wishlists:
            return None
        return self.__wishlists[user]

    def add_wishlist(self, user: User, wishlist: Wishlist):
        self.__wishlists[user] = wishlist

    def update_wishlist(self, user: User, wishlist: Wishlist):
        self.__wishlists[user] = wishlist

    def remove_game_from_wishlist(self, user: User, game: Game):
        wishlist = self.get_wishlist(user)
        print(user)
        if game in wishlist.list_of_games():
            wishlist.remove_game(game)
            self.update_wishlist(user, wishlist)  # Save changes back to repository

    # User Related Methods
    def addUser(self, user: User):
        self.__users.append(user)

    def getUser(self, user_name: str) -> User:
        for user in self.__users:
            if user.username == user_name:
                return user
        return None

    def getAllUsers(self) -> list[User]:
        return self.__users