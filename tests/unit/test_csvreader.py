import pytest
import os

from games.adapters.datareader.csvdatareader import GameFileCSVReader
from games.domainmodel.model import Publisher, Genre, Game, Review, User, Wishlist

# Unit tests for CSVReader
def create_csv_reader():
    dir_name = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    games_file_name = os.path.join(dir_name, "games/adapters/data/games.csv")
    reader = GameFileCSVReader(games_file_name)
    reader.read_csv_file()
    return reader


def test_csv_reader():
    reader = create_csv_reader()
    assert len(reader.dataset_of_games) == 877
    assert len(reader.dataset_of_publishers) == 798
    assert len(reader.dataset_of_genres) == 24


def test_read_csv_file():
    reader = create_csv_reader()
    game = next(iter(reader.dataset_of_games))
    assert game.game_id == 7940
    assert game.title == "Call of Duty® 4: Modern Warfare®"
    assert game.price == 9.99
    assert game.release_date == "Nov 12, 2007"
    assert game.publisher == Publisher("Activision")
    assert game.genres == [Genre("Action")]


def test_tracks_dataset():
    reader = create_csv_reader()
    sorted_games = sorted(reader.dataset_of_games)
    sorted_games_str = str(sorted_games[:3])
    assert sorted_games_str == "[<Game 3010, Xpand Rally>, <Game 7940, Call of Duty® 4: Modern Warfare®>, <Game 11370, Nikopol: Secrets of the Immortals>]"


def test_publisher_dataset():
    reader = create_csv_reader()
    publishers_set = reader.dataset_of_publishers
    sorted_publishers = sorted(publishers_set)
    sorted_publishers_str = str(sorted_publishers[:3])
    assert sorted_publishers_str == "[<Publisher 13-lab,azimuth team>, <Publisher 2Awesome Studio>, <Publisher 2Frogs Software>]"


def test_genres_dataset():
    reader = create_csv_reader()
    genres_set = reader.dataset_of_genres
    sorted_genres = sorted(genres_set)
    sorted_genre_sample = str(sorted_genres[:3])
    assert sorted_genre_sample == "[<Genre Action>, <Genre Adventure>, <Genre Animation & Modeling>]"
