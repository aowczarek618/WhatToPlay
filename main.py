import Game
import WhatToPlay
import pandas as pd
import os
import taste_meter


def create_db(games_set, my_taste):
    """Create database of all avaiable Xbox Game Pass games"""
    with open('xbox_database', 'a') as f:
        if os.stat('xbox_database').st_size == 0:
            f.write('Name:Developer:Genre:Metascore:MyScore\n')

        rated_games = rated_games_list()
        for game in games_set:
            if game.name not in rated_games:
                f.write(f'{game.name}:{game.developer}:{game.genre}:{game.metascore}:{game.my_score(my_taste)}\n')
    db = pd.read_csv('xbox_database', delimiter=':')
    return db


def del_unavailable_games_from_db(database, games_to_delete):
    """Delete games from database which are currently unavailable in Xbox Game Pass subscription"""
    for game in games_to_delete:
        database.drop(database[database.name == game].index)
    return database


def rated_games_list():
    """Create rated games list"""
    with open('rated_games', 'r') as f:
        rated_games = []
        for line in f:
            game_name = line.rstrip().split(':')[0]
            rated_games.append(game_name)
    return rated_games


def get_old_gamenames():
    """Get all game names which are in project folder database"""
    old_gamenames = []
    with open('xbox_database', 'a') as f:
        pass  # Create file if doesn't exist, don't overwrite if exists
    with open('xbox_database', 'r') as f:
        for line in f:
            gamename = line.split(':')[0]
            if not gamename == 'Name':
                old_gamenames.append(gamename)
    return old_gamenames


def main():
    """Main function"""
    old_gamenames = get_old_gamenames()
    games_set, games_to_delete = WhatToPlay.get_xgp_games(old_gamenames, rated_games_list())
    my_taste = taste_meter.taste_meter('rated_games')
    db = create_db(games_set, my_taste)
    db = del_unavailable_games_from_db(db, games_to_delete)

    pd.set_option('display.max_rows', None)
    sorted_db = db.sort_values('MyScore', ascending=False)
    sorted_db = sorted_db[sorted_db['Metascore'] != 0]
    print(sorted_db[['Name', 'MyScore']])


if __name__ == '__main__':
    main()
