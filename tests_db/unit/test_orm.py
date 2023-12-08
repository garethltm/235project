import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from games.domainmodel.model import Game, Genre, Publisher, User, Wishlist, Review

article_date = datetime.date(2020, 2, 28)

def insert_user(empty_session, values=None):
    # Add a user
    new_name = "Andrew"
    new_password = "1234Adsdsdsd"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                          {'username': new_name, 'password': new_password})
    row = empty_session.execute('SELECT username from users where username = :username',
                                {'username': new_name}).fetchone()
    return row[0]
#
def insert_users(empty_session, values):
    # Add users
    for value in values:
        empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                              {'username': value[0], 'password': value[1]})

def test_loading_of_users(empty_session):
    # Check if the user gets added to the database
    users = list()
    users.append(("Andrew", "1234Adsdsdsd"))
    users.append(("Cindy", "1234Adsdsdsd"))
    insert_users(empty_session, users)

    expected = [
        User("Andrew", "1234Adsdsdsd"),
        User("Cindy", "1234Adsdsdsd")
    ]
    assert empty_session.query(User).all()[0].username == 'Andrew' and empty_session.query(User).all()[1].username == 'Cindy'

def make_user():
    # Create a user
    user = User("Andrew", "1234Adsdsdsd")
    return user

def test_saving_of_users(empty_session):
    # Check if the user gets added to the database
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT username, password FROM users'))
    assert rows == [("andrew", "1234Adsdsdsd")]


def test_saving_of_users_with_common_user_name(empty_session):
    # Check if the user with same username can be added to the database
    insert_user(empty_session, ("andrew", "1234Adsdsdsd"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("andrew", "1234Adsdsdsd")
        empty_session.add(user)
        empty_session.commit()

def insert_game(empty_session):
    # Add a game
    empty_session.execute(
        'INSERT INTO games (game_id, game_title, game_price, release_date, game_description, publisher_name) VALUES '
        '(1, "Test Game", 10.0, "Oct 21, 2008", "Test Description", "Test Publisher")',
    )
    row = empty_session.execute('SELECT game_id from games').fetchone()
    return row[0]

def test_loading_of_game(empty_session):
    # Check if the game gets added to the database
    article_key = insert_game(empty_session)
    fetched_game = empty_session.query(Game).one()

    assert article_key == fetched_game.game_id


def insert_publisher(empty_session):
    # Add a publisher
    empty_session.execute(
        'INSERT INTO publishers (name) VALUES ("Test Publisher")'
    )
    row = empty_session.execute('SELECT name from publishers').fetchone()
    return row[0]

def test_loading_of_publisher(empty_session):
    # Check if the publisher gets added to the database
    publisher_key = insert_publisher(empty_session)
    fetched_publisher = empty_session.query(Publisher).one()
    assert publisher_key == fetched_publisher.publisher_name

def insert_genre(empty_session):
    # Add a genre
    empty_session.execute(
        'INSERT INTO genres (genre_name) VALUES ("Test Genre")'
    )
    row = empty_session.execute('SELECT genre_name from genres').fetchone()
    return row[0]

def insert_game_genre_associations(empty_session, game_key, genre_key):
    # Add a genre to a game
    stmt = 'INSERT INTO game_genres (game_id, genre_name) VALUES (:game_id, :genre_name)'
    empty_session.execute(stmt, {'game_id': game_key, 'genre_name': genre_key})

def test_loading_of_game_genre_associations(empty_session):
    # Check if the genre gets added to the game
    game_key = insert_game(empty_session)
    genre_key = insert_genre(empty_session)
    insert_game_genre_associations(empty_session, game_key, genre_key)

    game = empty_session.query(Game).get(game_key)
    genre = empty_session.query(Genre).get(genre_key)

    assert genre in game.genres

def insert_review(empty_session):
    # Add a review
    empty_session.execute(
        'INSERT INTO reviews (username, game_id, rating, comment) VALUES '
        '("Andrew", 1, 5, "Test Review")',
    )
    row = empty_session.execute('SELECT username from reviews').fetchone()
    return row[0]

def test_loading_of_review(empty_session):
    # Check if the review gets added to the database
    review_key = insert_review(empty_session)
    fetched_review = empty_session.query(Review).one()

    assert review_key == fetched_review.username

def insert_wishlist(empty_session):
    # Add a wishlist
    empty_session.execute(
        'INSERT INTO wishlists (username) VALUES '
        '("Andrew")',
    )
    row = empty_session.execute('SELECT id from wishlists').fetchone()
    return row[0]

def insert_wishlist_game_associations(empty_session, wishlist_key, game_key):
    # Add a game to a wishlist
    stmt = 'INSERT INTO wishlist_games (wishlist_id, game_id) VALUES (:wishlist_id, :game_id)'
    empty_session.execute(stmt, {'wishlist_id': wishlist_key, 'game_id': game_key})

def test_loading_of_wishlist_game_associations(empty_session):
    # Check if the game gets added to a wishlist
    wishlist_key = insert_wishlist(empty_session)
    game_key = insert_game(empty_session)
    insert_wishlist_game_associations(empty_session, wishlist_key, game_key)

    wishlist = empty_session.query(Wishlist).get(wishlist_key)
    game = empty_session.query(Game).get(game_key)

    assert game in wishlist.list_of_games()
