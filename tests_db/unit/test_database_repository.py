from datetime import date, datetime

import pytest

import games.adapters.repository as repo
from games.adapters.database_repository import SqlAlchemyRepository
from games.domainmodel.model import Publisher, Genre, Game, Review, User, Wishlist
from games.adapters.repository import RepositoryException


def test_repository_can_add_a_game(session_factory):
    # Check if the game can be added to the repository
    repo = SqlAlchemyRepository(session_factory)

    game = Game(1, "Test Game")
    game.price = 10.0
    game.release_date = 'Oct 21, 2008'

    repo.add_game(game)

    assert repo.getGameById(1) == game

def test_repository_can_get_all_games(session_factory):
    # Check if the repository can retrieve all games
    repo = SqlAlchemyRepository(session_factory)

    games = repo.getAllGames()

    assert len(games) > 500


def test_repository_can_get_game_by_id(session_factory):
    # Check if the repository can retrieve a game by id
    repo = SqlAlchemyRepository(session_factory)

    game = Game(1, "Test Game")
    game.price = 10.0
    game.release_date = 'Oct 21, 2008'
    repo.add_game(game)

    assert repo.getGameById(1) == game

def test_repository_can_get_games_by_genre(session_factory):
    # Check if the repository can retrieve games by genres
    repo = SqlAlchemyRepository(session_factory)

    game = Game(1, "Test Game")
    game.price = 10.0
    game.release_date = 'Oct 21, 2008'
    game2 = Game(2, "Test Game2")
    game2.price = 10.0
    game2.release_date = 'Oct 21, 2008'
    game.genres.append(Genre("Test Genre"))
    repo.add_game(game)
    repo.add_game(game2)

    games = repo.getGamesByGenres([Genre("Test Genre")])

    assert len(games) == 1

def test_repository_can_add_a_genre(session_factory):
    # Check if the genre can be added to the repository
    repo = SqlAlchemyRepository(session_factory)

    genre = Genre("Test Genre")

    repo.add_genre(genre)

    assert genre in repo.getAllGenres()

def test_repository_can_get_all_genres(session_factory):
    # Check if the repository can retrieve all genres
    repo = SqlAlchemyRepository(session_factory)

    genres = repo.getAllGenres()

    assert len(genres) > 20


def test_repository_can_add_a_publisher(session_factory):
    # Check if the publisher can be added to the repository
    repo = SqlAlchemyRepository(session_factory)

    publisher = Publisher("Test Publisher")

    repo.add_publisher(publisher)

    assert publisher in repo.getAllPublishers()

def test_repository_can_get_all_publishers(session_factory):
    # Check if the repository can retrieve all publishers
    repo = SqlAlchemyRepository(session_factory)

    publishers = repo.getAllPublishers()

    assert len(publishers) > 500


def test_repository_can_add_a_review(session_factory):
    # Check if the review can be added to the repository
    repo = SqlAlchemyRepository(session_factory)


    user = User("Test User", "Test Password")
    game = Game(1, "Test Game")
    game.price = 10.0
    game.release_date = 'Oct 21, 2008'
    repo.addUser(user)

    review = Review(user, game, 1, "Test Review")

    repo.add_review(review)

    assert review in repo.getAllReviews()

def test_repository_can_get_all_reviews(session_factory):
    # Check if the repository can retrieve all reviews
    repo = SqlAlchemyRepository(session_factory)

    user = User("Test User", "Test Password")
    game = Game(1, "Test Game")
    game.price = 10.0
    game.release_date = 'Oct 21, 2008'
    reviews = repo.getAllReviews()
    repo.addUser(user)

    initiallen = len(reviews)

    review = Review(user, game, 1, "Test Review")
    repo.add_review(review)

    reviews = repo.getAllReviews()

    assert len(reviews) == initiallen + 1

def test_repository_can_get_a_wishlist(session_factory):
    # Check if the repository can retrieve a wishlist
    repo = SqlAlchemyRepository(session_factory)

    wishlist = Wishlist(User("Test User", "Test Password"))

    repo.add_wishlist(User("Test User", "Test Password"), wishlist)

    assert repo.get_wishlist(User("Test User", "Test Password")) == wishlist

def test_repository_can_add_a_wishlist(session_factory):
    # Check if the wishlist can be added to the repository
    repo = SqlAlchemyRepository(session_factory)

    wishlist = Wishlist(User("Test User", "Test Password"))

    repo.add_wishlist(User("Test User", "Test Password"), wishlist)

    assert repo.get_wishlist(User("Test User", "Test Password")) == wishlist

def test_repository_can_update_a_wishlist(session_factory):
    # Check if the wishlist can be updated in the repository
    repo = SqlAlchemyRepository(session_factory)

    user = User("Test User", "Test Password")
    game = Game(1, "Test Game")
    game.price = 10.0
    game.release_date = 'Oct 21, 2008'
    wishlist = Wishlist(user)

    repo.add_wishlist(user, wishlist)

    assert len(repo.get_wishlist(user).list_of_games()) == 0

    wishlist.add_game(game)

    repo.update_wishlist(user, wishlist)

    assert game in repo.get_wishlist(user).list_of_games()

def test_repository_can_remove_game_from_wishlist(session_factory):
    # Check if the game can be removed from the wishlist in the repository
    repo = SqlAlchemyRepository(session_factory)

    user = User("Test User", "Test Password")
    game = Game(1, "Test Game")
    game.price = 10.0
    game.release_date = 'Oct 21, 2008'
    wishlist = Wishlist(user)
    wishlist.add_game(game)

    repo.add_wishlist(user, wishlist)

    assert repo.get_wishlist(user) == wishlist

    repo.remove_game_from_wishlist(user, game)

    assert game not in repo.get_wishlist(user).list_of_games()

def test_repository_can_add_user(session_factory):
    # Check if the user can be added to the repository
    repo = SqlAlchemyRepository(session_factory)

    user = User("Test User", "Test Password")

    repo.addUser(user)

    assert user in repo.getAllUsers()

def test_repository_can_get_user(session_factory):
    # Check if the repository can retrieve a user by its username
    repo = SqlAlchemyRepository(session_factory)

    user = User("TestUser", "Test Password")

    repo.addUser(user)

    assert repo.getUser("testuser") == user

def test_repository_can_get_all_users(session_factory):
    # Check if the repository can retrieve all users
    repo = SqlAlchemyRepository(session_factory)

    users = repo.getAllUsers()

    assert len(users) >= 0
