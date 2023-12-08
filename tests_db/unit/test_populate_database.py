from sqlalchemy import select, inspect

from games.adapters.orm import metadata

def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['game_genres', 'game_reviews', 'games', 'genres', 'publishers', 'reviews', 'user_reviews', 'users', 'wishlist_games', 'wishlists']

def test_database_populate_select_all_games(database_engine):

        # Get table information
        inspector = inspect(database_engine)
        name_of_games_table = inspector.get_table_names()[2]

        with database_engine.connect() as connection:
            # query for records in table games
            select_statement = select([metadata.tables[name_of_games_table]])
            result = connection.execute(select_statement)

            all_games = []
            for row in result:
                all_games.append((row['game_id'], row['game_title']))

            nr_games = len(all_games)
            assert nr_games == 877

def test_database_populate_select_all_publishers(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_publishers_table = inspector.get_table_names()[4]

    with database_engine.connect() as connection:
        # query for records in table publishers
        select_statement = select([metadata.tables[name_of_publishers_table]])
        result = connection.execute(select_statement)

        all_publishers = []
        for row in result:
            all_publishers.append(row['name'])

        assert len(all_publishers) == 798

def test_database_populate_select_all_users(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[7]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['username'])

        assert all_users == ['thorke', 'fmercury']

def test_database_populate_select_all_genres(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_genres_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        # query for records in table genres
        select_statement = select([metadata.tables[name_of_genres_table]])
        result = connection.execute(select_statement)

        all_genres = []
        for row in result:
            all_genres.append(row['genre_name'])

        assert len(all_genres) == 24