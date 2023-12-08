import pytest
import os
from games.domainmodel.model import Publisher, Genre, Game, Review, User, Wishlist

from pathlib import Path
from games.adapters.memory_repository import MemoryRepository
from games.adapters.repository_populate import populate
import games.adapters.repository as rp


@pytest.fixture
def user():
    return User("Shyamli", "pw12345")


@pytest.fixture
def game():
    return Game(1, "Domino Game")


@pytest.fixture
def wishlist(user):
    return Wishlist(user)


# Validate data operations of the memory repository components
def test_repository_can_populate():
    # Check if the data can be added to the repository
    rp.repo_instance = MemoryRepository()
    assert len(rp.repo_instance.getAllGames()) == 0
    data_path = Path('games') / 'adapters' / 'data'
    populate(data_path, rp.repo_instance, True)
    assert len(rp.repo_instance.getAllGames()) == 877


def test_repository_can_add_a_game(game):
    # Check if the game can be added to the repository
    rp.repo_instance = MemoryRepository()
    assert len(rp.repo_instance.getAllGames()) == 0
    rp.repo_instance.add_game(game)
    assert len(rp.repo_instance.getAllGames()) == 1
    assert rp.repo_instance.getAllGames()[0].title == "Domino Game"


def test_repository_get_all_games(repo):
    # Check if the repository can retrieve all games
    games = repo.getAllGames()
    assert len(games) == 877


def test_repository_can_get_game_by_id(repo):
    # Check if the repository can retrieve a game by id
    game = repo.getGameById(1436990)
    assert game.game_id == 1436990


def test_repository_can_get_games_by_genres(repo):
    # Check if the repository can retrieve games by genres
    games = repo.getGamesByGenres([Genre("Action")])
    for game in games:
        assert Genre("Action") in game.genres


def test_repository_can_add_a_genre():
    # Check if the genre can be added to the repository
    rp.repo_instance = MemoryRepository()
    assert len(rp.repo_instance.getAllGenres()) == 0
    rp.repo_instance.add_genre(Genre("Action"))
    assert len(rp.repo_instance.getAllGenres()) == 1
    assert rp.repo_instance.getAllGenres()[0].genre_name == "Action"


def test_repository_get_all_genres(repo):
    # Check if the repository can retrieve all genres
    genres = repo.getAllGenres()
    assert len(genres) == 24


def test_repository_can_add_a_publisher():
    # Check if the publisher can be added to the repository
    rp.repo_instance = MemoryRepository()
    assert len(rp.repo_instance.getAllPublishers()) == 0
    rp.repo_instance.add_publisher(Publisher("Activision"))
    assert len(rp.repo_instance.getAllPublishers()) == 1
    assert rp.repo_instance.getAllPublishers()[0].publisher_name == "Activision"


def test_repository_get_all_publishers(repo):
    # Check if the repository can retrieve all publishers
    publishers = repo.getAllPublishers()
    assert len(publishers) == 798


def test_repository_can_add_a_review(user):
    # Check if the review can be added to the repository
    rp.repo_instance = MemoryRepository()
    assert len(rp.repo_instance.getAllReviews()) == 0
    rp.repo_instance.add_review(Review(user, Game(1, "Domino Game"), 5, "This is a review"))
    assert len(rp.repo_instance.getAllReviews()) == 1
    assert rp.repo_instance.getAllReviews()[0].comment == "This is a review"


def test_repository_get_all_reviews(user):
    # Check if the repository can retrieve all reviews
    rp.repo_instance = MemoryRepository()
    assert len(rp.repo_instance.getAllReviews()) == 0
    rp.repo_instance.add_review(Review(user, Game(1, "Domino Game"), 5, "This is a review1"))
    rp.repo_instance.add_review(Review(user, Game(2, "Game2"), 2, "This is a review2"))
    assert len(rp.repo_instance.getAllReviews()) == 2
    rp.repo_instance.add_review(Review(user, Game(3, "Game3"), 1, "This is a review3"))
    assert len(rp.repo_instance.getAllReviews()) == 3
    assert rp.repo_instance.getAllReviews()[0].comment == "This is a review1"


def test_repository_get_wishlist_of_a_user(user, wishlist):
    # Check if the repository can retrieve the wishlist of a user
    rp.repo_instance = MemoryRepository()
    rp.repo_instance.addUser(user)
    assert len(rp.repo_instance.getAllUsers()) == 1
    rp.repo_instance.add_wishlist(user, wishlist)
    assert rp.repo_instance.get_wishlist(user) == wishlist


def test_repository_add_wishlist_to_a_user(user, wishlist):
    # Check if the repository can add a wishlist to a user
    rp.repo_instance = MemoryRepository()
    rp.repo_instance.addUser(user)
    assert len(rp.repo_instance.getAllUsers()) == 1
    assert rp.repo_instance.get_wishlist(user) is None
    rp.repo_instance.add_wishlist(user, wishlist)
    assert rp.repo_instance.get_wishlist(user) == wishlist


def test_repository_update_wishlist_of_a_user(repo, user, wishlist):
    # Check if the repository can update the wishlist of a user
    repo.addUser(user)
    assert len(repo.getAllUsers()) == 3
    wishlist.add_game(Game(1, "Domino Game"))
    repo.add_wishlist(user, wishlist)
    assert repo.get_wishlist(user).select_game(0).title == "Domino Game"
    wishlist2 = Wishlist(user)
    wishlist2.add_game(Game(2, "Game2"))
    repo.update_wishlist(user, wishlist2)
    assert repo.get_wishlist(user).select_game(0).title == "Game2"


def test_repository_remove_game_from_wishlist_of_a_user(repo, user, wishlist):
    # Check if the repository can remove the wishlist of a user
    repo.addUser(user)
    assert len(repo.getAllUsers()) == 3
    wishlist.add_game(Game(1, "Domino Game"))
    wishlist.add_game(Game(2, "Game2"))
    repo.add_wishlist(user, wishlist)
    assert repo.get_wishlist(user).select_game(0).title == "Domino Game"
    repo.remove_game_from_wishlist(user, Game(1, "Domino Game"), )
    assert repo.get_wishlist(user).select_game(0).title == "Game2"


def test_repository_can_add_a_user(user):
    # Check if the user can be added to the repository
    rp.repo_instance = MemoryRepository()
    assert len(rp.repo_instance.getAllUsers()) == 0
    rp.repo_instance.addUser(user)
    assert len(rp.repo_instance.getAllUsers()) == 1
    assert rp.repo_instance.getAllUsers()[0].username == "shyamli"


def test_repository_get_user(user):
    # Check if the repository can retrieve a user by its username
    rp.repo_instance = MemoryRepository()
    assert len(rp.repo_instance.getAllUsers()) == 0
    rp.repo_instance.addUser(user)
    assert len(rp.repo_instance.getAllUsers()) == 1
    assert rp.repo_instance.getUser("shyamli").username == "shyamli"


def test_repository_get_all_users(repo, user):
    # Check if the repository can retrieve all users
    repo.addUser(user)
    assert len(repo.getAllUsers()) == 3
    repo.addUser(User("AaronChiam", "password"))
    assert len(repo.getAllUsers()) == 4
    assert repo.getAllUsers()[2].username == "shyamli"
