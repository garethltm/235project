import abc
from games.domainmodel.model import Genre, Game, Publisher, Review, User, Wishlist

repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):
    """Interface for a repository providing access to game data."""

    @abc.abstractmethod
    def add_game(self, game: Game):
        """Adds a game to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        """Adds a browse to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def add_publisher(self, publisher: Publisher):
        """Adds a publisher to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """Adds a review to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def getAllReviews(self) -> list[Review]:
        """Retrieve all reviews stored in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def getAllGames(self):
        """Retrieve all games stored in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def getAllGenres(self):
        """Retrieve all genres stored in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def getAllPublishers(self):
        """Retrieve all publishers stored in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def getGamesByGenres(self, genres: list[Genre]):
        """Retrieve all games that are associated with the given genres."""
        raise NotImplementedError

    def getGameById(self, id: int):
        """Retrieve a game by its id."""
        raise NotImplementedError

    @abc.abstractmethod
    def getUser(self, user_name: str) -> User:
        """Retrieve a user by its username. If no User with the given username exists, this method returns None."""
        raise NotImplementedError

    @abc.abstractmethod
    def getAllUsers(self) -> list[User]:
        """Retrieve all users stored in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def addUser(self, user: User):
        """Add a User to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_wishlist(self, user: User):
        """Retrieve a user's wishlist."""
        raise NotImplementedError

    @abc.abstractmethod
    def add_wishlist(self, user: User, wishlist: Wishlist):
        """Add a wishlist to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def remove_game_from_wishlist(self, user: User, game: Game):
        """Remove a game from a user's wishlist."""
        raise NotImplementedError

    @abc.abstractmethod
    def update_wishlist(self, user: User, wishlist: Wishlist):
        """Update a user's wishlist."""
        raise NotImplementedError