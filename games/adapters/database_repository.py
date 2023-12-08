from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session

from games.domainmodel.model import Game, Genre, Publisher, User, Review, Wishlist
from games.adapters.repository import AbstractRepository, RepositoryException

class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()



    # Game Related Methods
    def add_game(self, game: Game):
        with self._session_cm as scm:
            scm.session.merge(game)
            scm.commit()

    def getAllGames(self) -> list[Game]:
        games = self._session_cm.session.query(Game).order_by(Game._Game__game_id).all()
        return games

    def getGameById(self, game_id: int):
        game = None
        try:
            game = self._session_cm.session.query(
                Game).filter(Game._Game__game_id == game_id).one()
        except NoResultFound:
            print(f'Game {game_id} was not found')

        return game

    def getGamesByGenres(self, genres: list[Genre]) -> list[Game]:  # Similar to get_articles_by_date in COVID app??
        games = set()
        if genres is None or len(genres) == 0 or genres[0] == '':
            return self.getAllGames()
        for game in self.getAllGames():
            for genre in genres:
                if genre in game.genres:
                    games.add(game)
        return list(games)

    # Genre Related Methods
    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.merge(genre)
            scm.commit()

    def getAllGenres(self) -> list[Genre]:
        genres = self._session_cm.session.query(Genre).all()
        return genres

    # Publisher Related Methods
    def add_publisher(self, publisher: Publisher):
        with self._session_cm as scm:
            scm.session.merge(publisher)
            scm.commit()

    def getAllPublishers(self) -> list[Publisher]:
        publishers = self._session_cm.session.query(Publisher).all()
        return publishers

    # Review Related Methods
    def add_review(self, review: Review):
        try:
            with self._session_cm as scm:
                scm.session.merge(review)
                scm.commit()
        except SQLAlchemyError as e:
            print("Error occurred:", e)
            scm.rollback()

    def getAllReviews(self) -> list[Review]:
        reviews = self._session_cm.session.query(Review).all()
        return reviews

    # Wishlist Related Methods
    def get_wishlist(self, user: User):
        try:
            wishlist = self._session_cm.session.query(Wishlist).filter(Wishlist._Wishlist__user == user).one()
        except NoResultFound:
            return None
        return wishlist

    def add_wishlist(self, user: User, wishlist: Wishlist):
        # wishlist.user = user
        self._session_cm.session.add(wishlist)
        self._session_cm.session.commit()

    def update_wishlist(self, user: User, wishlist: Wishlist):
        existing_wishlist = self.get_wishlist(user)
        if existing_wishlist is not None:
            existing_wishlist.games = wishlist.list_of_games()
            self._session_cm.session.commit()

    def remove_game_from_wishlist(self, user: User, game: Game):
        wishlist = self.get_wishlist(user)
        if game in wishlist.list_of_games():
            wishlist.remove_game(game)
            self._session_cm.session.commit()

    # User Related Methods
    def addUser(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def getUser(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__username == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        return user

    def getAllUsers(self) -> list[User]:
        users = self._session_cm.session.query(User).all()
        return users