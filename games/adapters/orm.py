from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Text, Float, ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from games.domainmodel.model import Game, Publisher, Genre, User, Review, Wishlist

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

genres_table = Table(
    'genres', metadata,
    # For genre again we only have name.
    Column('genre_name', String(64), primary_key=True, nullable=False)
)

publishers_table = Table(
    'publishers', metadata,
    # We only want to maintain those attributes that are in our domain model
    # For publisher, we only have name.
    Column('name', String(255), primary_key=True)  # nullable=False, unique=True)
)

games_table = Table(
    'games', metadata,
    Column('game_id', Integer, primary_key=True),
    Column('game_title', Text, nullable=False),
    Column('game_price', Float, nullable=False),
    Column('release_date', String(50), nullable=False),
    Column('game_description', String(255), nullable=True),
    Column('game_image_url', String(255), nullable=True),
    Column('game_website_url', String(255), nullable=True),
    Column('publisher_name', ForeignKey('publishers.name'))
)

users_table = Table(
    'users', metadata,
    Column('username', String(255), primary_key=True),
    Column('password', String(255), nullable=False)
)

reviews_table = Table(
    'reviews', metadata,
    Column('review_id', Integer, primary_key=True, autoincrement=True),
    Column('game_id', ForeignKey('games.game_id')),
    Column('username', ForeignKey('users.username')),
    Column('rating', Integer, nullable=False),
    Column('comment', Text, nullable=True)
)

game_genres_table = Table(
    'game_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('game_id', ForeignKey('games.game_id')),
    Column('genre_name', ForeignKey('genres.genre_name'))
)

user_reviews_table = Table(
    'user_reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', ForeignKey('users.username')),
    Column('review_id', ForeignKey('reviews.review_id')),
)

game_reviews_table = Table(
    'game_reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('game_id', ForeignKey('games.game_id')),
    Column('review_id', ForeignKey('reviews.review_id')),
)

wishlist_table = Table(
    'wishlists', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', ForeignKey('users.username'))
)

wishlist_game_table = Table(
    'wishlist_games', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('wishlist_id', ForeignKey('wishlists.id')),
    Column('game_id', ForeignKey('games.game_id'))
)




def map_model_to_tables():
    mapper(Publisher, publishers_table, properties={
        '_Publisher__publisher_name': publishers_table.c.name,
    })

    mapper(Genre, genres_table, properties={
        '_Genre__genre_name': genres_table.c.genre_name,
    })

    mapper(Game, games_table, properties={
        '_Game__game_id': games_table.c.game_id,
        '_Game__game_title': games_table.c.game_title,
        '_Game__price': games_table.c.game_price,
        '_Game__release_date': games_table.c.release_date,
        '_Game__description': games_table.c.game_description,
        '_Game__image_url': games_table.c.game_image_url,
        '_Game__website_url': games_table.c.game_website_url,
        '_Game__publisher': relationship(Publisher),
        '_Game__genres': relationship(Genre, secondary=game_genres_table),
        '_Game__reviews': relationship(Review, secondary=game_reviews_table)
    })

    mapper(User, users_table, properties={
        '_User__username': users_table.c.username,
        '_User__password': users_table.c.password,
        '_User__reviews': relationship(Review, secondary=user_reviews_table)
    })

    mapper(Review, reviews_table, properties={
        '_Review__rating': reviews_table.c.rating,
        '_Review__comment': reviews_table.c.comment,
        '_Review__user': relationship(User),
        '_Review__game': relationship(Game)
    })

    mapper(Wishlist, wishlist_table, properties={
        '_Wishlist__user': relationship(User),
        '_Wishlist__list_of_games': relationship(Game, secondary=wishlist_game_table)
    })
