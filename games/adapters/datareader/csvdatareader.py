import csv
import os

from pathlib import Path
from games.domainmodel.model import Genre, Game, Publisher, User
from werkzeug.security import generate_password_hash
from games.adapters.repository import AbstractRepository, RepositoryException

class GameFileCSVReader:
    def __init__(self, filename):
        self.__filename = filename
        self.__dataset_of_games = []
        self.__dataset_of_publishers = set()
        self.__dataset_of_genres = set()

    def read_csv_file(self):
        if not os.path.exists(self.__filename):
            print(f"path {self.__filename} does not exist!")
            return
        with open(self.__filename, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    game_id = int(row["AppID"])
                    title = row["Name"]
                    game = Game(game_id, title)
                    game.release_date = row["Release date"]
                    game.price = float(row["Price"])
                    game.description = row["About the game"]
                    game.image_url = row["Header image"]

                    game.isWindows = row["Windows"] == "TRUE"
                    game.isMac = row["Mac"] == "TRUE"
                    game.isLinux = row["Linux"] == "TRUE"

                    publisher = Publisher(row["Publishers"])
                    self.__dataset_of_publishers.add(publisher)
                    game.publisher = publisher

                    genre_names = row["Genres"].split(",")
                    for genre_name in genre_names:
                        genre = Genre(genre_name.strip())
                        self.__dataset_of_genres.add(genre)
                        game.add_genre(genre)

                    self.__dataset_of_games.append(game)

                except ValueError as e:
                    print(f"Skipping row due to invalid data: {e}")
                except KeyError as e:
                    print(f"Skipping row due to missing key: {e}")

    def get_unique_games_count(self):
        return len(self.__dataset_of_games)

    def get_unique_genres_count(self):
        return len(self.__dataset_of_genres)

    def get_unique_publishers_count(self):
        return len(self.__dataset_of_publishers)

    @property
    def dataset_of_games(self) -> list:
        return self.__dataset_of_games

    @property
    def dataset_of_publishers(self) -> set:
        return self.__dataset_of_publishers

    @property
    def dataset_of_genres(self) -> set:
        return self.__dataset_of_genres


class UserFileCSVReader:
    def __init__(self, filename):
        self.__filename = filename
        self.__dataset_of_users = []

    def read_csv_file(self):
        if not os.path.exists(self.__filename):
            print(f"path {self.__filename} does not exist!")
            return
        with open(self.__filename, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    username = row["username"]
                    password = generate_password_hash(row["password"])

                    user = User(username, password)

                    self.__dataset_of_users.append(user)

                except ValueError as e:
                    print(f"Skipping row due to invalid data: {e}")
                except KeyError as e:
                    print(f"Skipping row due to missing key: {e}")

    def get_unique_users_count(self):
        return len(self.__dataset_of_users)

    @property
    def dataset_of_users(self) -> list:
        return self.__dataset_of_users

def load_gamedata(data_path: Path, repo: AbstractRepository):
    data_path = str(Path(data_path) / "games.csv")
    reader = GameFileCSVReader(data_path)
    reader.read_csv_file()
    for game in reader.dataset_of_games:
        repo.add_game(game)
    for genre in reader.dataset_of_genres:
        repo.add_genre(genre)
    for publisher in reader.dataset_of_publishers:
        repo.add_publisher(publisher)


def load_users(data_path: Path, repo: AbstractRepository):
    users_filename = str(Path(data_path) / "users.csv")
    reader = UserFileCSVReader(users_filename)
    reader.read_csv_file()
    for user in reader.dataset_of_users:
        repo.addUser(user)
