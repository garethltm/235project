import pytest
import os

from games.authentication.services import AuthenticationException
from games.domainmodel.model import Publisher, Genre, Game, Review, User, Wishlist

from games.home import services as home_services
from games.browse import services as browse_services
from games.authentication import services as auth_services
from games.wishlist import services as wishlist_services
from games.utilities import utilities as utilities


# Home page functionality of the service layer
def test_featured_games(repo):
    # Check if the featured games (random 3) are retrieved correctly
    featured_games = home_services.getFeaturedGames(repo)
    featured_games_rep = home_services.getFeaturedGames(repo)
    assert len(featured_games) == 3
    assert featured_games[0] != featured_games[1]
    assert featured_games[1] != featured_games[2]
    assert featured_games[2] != featured_games[0]
    assert featured_games_rep != featured_games


# Browse page functionality of the service layer
def test_get_games_by_genre(repo):
    # Check if the games by genre are retrieved correctly
    # Note that the OR operation is intended to be tested here
    games = browse_services.getGamesByGenres(repo, ["Action", "Adventure"])
    assert len(games) == 554
    for game in games:
        assert Genre("Action") in game.genres or Genre("Adventure") in game.genres


def test_search_game_by_title(repo):
    # Check if the games by title are retrieved correctly
    games = repo.getAllGames()
    games1 = browse_services.searchGameByTitle(games, "Honkai Impact 3rd")
    assert len(games1) == 1
    assert games1[0].title == "Honkai Impact 3rd"
    games2 = browse_services.searchGameByTitle(games, "Z")
    assert len(games2) == 56
    assert games2[0].title == "TRIZEAL Remix"


def test_search_game_by_genre(repo):
    # Check if the games by genre are retrieved correctly
    # Note that the AND operation is intended to be tested here
    games = repo.getAllGames()
    games1 = browse_services.searchGameByGenre(games, "Action;")
    assert len(games1) == 380
    for game1 in games1:
        assert Genre("Action") in game1.genres
    games2 = browse_services.searchGameByGenre(games, "Action;Adventure;")
    assert len(games2) == 170
    for game2 in games2:
        assert Genre("Action") in game2.genres and Genre("Adventure") in game2.genres


def test_search_game_by_publisher(repo):
    # Check if the games by publisher are retrieved correctly
    games = repo.getAllGames()
    games1 = browse_services.searchGameByPublisher(games, "miHoYo Limited")
    assert len(games1) == 1
    for game1 in games1:
        assert game1.publisher.publisher_name.lower() == "mihoyo limited"
    games2 = browse_services.searchGameByPublisher(games, "8floor")
    assert len(games2) == 5
    for game2 in games2:
        assert game2.publisher.publisher_name.lower() == "8floor"


# Authentication page functionality of the service layer
def test_add_user(repo):
    # Check if the user can be added to the repository
    assert len(repo.getAllUsers()) == 2
    auth_services.addUser("testadd", "testtestA1", repo)
    assert len(repo.getAllUsers()) == 3
    assert repo.getUser("testadd").username == "testadd"
    assert "sha256:" in repo.getUser("testadd").password


def test_get_user(repo):
    # Check if the user can be retrieved from the repository
    # Note that the auth_services version returns a dictionary
    assert len(repo.getAllUsers()) == 2
    repo.addUser(User("testuser", "testtestA1"))
    assert len(repo.getAllUsers()) == 3
    assert auth_services.getUser("testuser", repo)["user_name"] == "testuser"
    assert isinstance(auth_services.getUser("testuser", repo), dict)


def test_auth_user(repo):
    # Check if the user can be authenticated
    assert len(repo.getAllUsers()) == 2
    auth_services.addUser("testuser", "testtestA1", repo)
    assert len(repo.getAllUsers()) == 3
    assert auth_services.authUser("testuser", "testtestA1", repo) == True
    with pytest.raises(AuthenticationException):
        auth_services.authUser("testuser", "testtestA2", repo)


def test_user_to_dict():
    # Check if the user can be converted to a dictionary
    converted_user = auth_services.userToDict(User("testuser", "testtestA1"))
    assert converted_user["user_name"] == "testuser"
    assert converted_user["password"] == "testtestA1"


# Wishlist page functionality of the service layer
def test_add_wishlist(repo):
    # Check if the wishlist can be added to the repository
    assert len(repo.getAllUsers()) == 2
    auth_services.addUser("testuser", "testtestA1", repo)
    assert len(repo.getAllUsers()) == 3
    assert repo.get_wishlist(repo.getUser("testuser")) is None
    wishlist = Wishlist(repo.getUser("testuser"))
    wishlist_services.add_wishlist(repo, repo.getUser("testuser"), wishlist)
    assert repo.get_wishlist(repo.getUser("testuser")) == wishlist


def test_remove_game_from_wishlist(repo):
    # Check if the game can be removed from the wishlist
    assert len(repo.getAllUsers()) == 2
    auth_services.addUser("testuser", "testtestA1", repo)
    assert len(repo.getAllUsers()) == 3
    assert repo.get_wishlist(repo.getUser("testuser")) is None
    wishlist = Wishlist(repo.getUser("testuser"))
    wishlist.add_game(Game(1, "Domino Game"))
    wishlist.add_game(Game(2, "Game2"))
    wishlist_services.add_wishlist(repo, repo.getUser("testuser"), wishlist)
    assert repo.get_wishlist(repo.getUser("testuser")).select_game(0).title == "Domino Game"
    wishlist_services.remove_game_from_wishlist(repo, repo.getUser("testuser"), Game(1, "Domino Game"))
    assert repo.get_wishlist(repo.getUser("testuser")).select_game(0).title == "Game2"


# Utilities functionality of the global service layer
def test_getAllGames(repo):
    # Check if all games are retrieved correctly
    games = utilities.getAllGames(repo)
    assert len(games) == 877


def test_genre_sort(repo):
    # Check if the genres are sorted correctly
    genres_sorted = utilities.getAllGenresSorted(repo)
    assert genres_sorted[0].genre_name == "Action"
    assert genres_sorted[1].genre_name == "Adventure"
    assert genres_sorted[2].genre_name == "Animation & Modeling"
    assert genres_sorted[3].genre_name == "Audio Production"
    assert genres_sorted[4].genre_name == "Casual"
    assert genres_sorted[-1].genre_name == "Web Publishing"


def test_get_publishers(repo):
    # Check if all publishers are retrieved correctly
    publishers = utilities.getPublishers(repo)
    assert len(publishers) == 798


def test_paginate_list(repo):
    # Check if the list is paginated correctly
    games = utilities.getAllGames(repo)
    paginated_games = utilities.paginateLists(games, 1, 10)
    assert len(paginated_games) == 10
    assert paginated_games[0].title == "Call of Duty® 4: Modern Warfare®"
    assert paginated_games[9].title == "Arcadia"


def test_utilities_get_user(repo):
    # Check if the user can be retrieved from the repository
    # Note that utilities version returns a User object
    user = utilities.getUser("thorke", repo)
    assert user.username == "thorke"
    assert isinstance(user, User)


def test_get_game_by_id(repo):
    # Check if the game can be retrieved from the repository
    game = utilities.getGameById(repo, 1436990)
    assert game.title == "Feign"
    assert isinstance(game, Game)


def test_calculate_average_rating(repo):

    # Check if the average rating is calculated correctly
    user = utilities.getUser("thorke", repo)
    game = Game(1, "Test Game")

    # Retrieve all reviews from the database using the repository
    all_reviews = repo.getAllReviews()

    # Filter reviews for the specific game
    reviews = [review for review in all_reviews if review.game == game]
    reviews = reviews[::-1]

    assert utilities.calculate_average_rating(reviews) == "No Reviews Yet"
    repo.add_review(Review(user, game, 5, "Test Review"))

    # Retrieve all reviews from the database using the repository
    all_reviews = repo.getAllReviews()

    # Filter reviews for the specific game
    reviews = [review for review in all_reviews if review.game == game]
    # reviews = reviews[::-1]

    assert utilities.calculate_average_rating(reviews) == 5.0
    repo.add_review(Review(user, game, 4, "Test Review2"))

    # Retrieve all reviews from the database using the repository
    all_reviews = repo.getAllReviews()

    # Filter reviews for the specific game
    reviews = [review for review in all_reviews if review.game == game]
    reviews = reviews[::-1]

    assert utilities.calculate_average_rating(reviews) == 4.5


def test_get_wishlist(repo):
    # Check if the wishlist can be retrieved from the repository
    user = utilities.getUser("thorke", repo)
    wishlist_services.add_wishlist(repo, user, Wishlist(user))
    wishlist = utilities.get_wishlist(repo, user)
    assert isinstance(wishlist, Wishlist)


def test_is_game_in_wishlist(repo):
    # Check if the game is in the wishlist
    user = utilities.getUser("thorke", repo)
    game = Game(1, "Test Game")
    wishlist_services.add_wishlist(repo, user, Wishlist(user))
    wishlist = utilities.get_wishlist(repo, user)
    assert utilities.is_game_in_wishlist(repo, user, game) == False
    wishlist.add_game(game)
    assert utilities.is_game_in_wishlist(repo, user, game) == True
