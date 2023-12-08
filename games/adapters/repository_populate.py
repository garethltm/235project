from pathlib import Path

from games.adapters.repository import AbstractRepository, RepositoryException
from games.adapters.datareader.csvdatareader import load_gamedata, load_users

def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):
    # Load game data into the repository
    load_gamedata(data_path, repo)
    # Load users into the repository
    load_users(data_path, repo)