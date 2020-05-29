import Game
import WhatToPlay
import pandas as pd
import taste_meter


def create_db(games_set, my_taste):
    with open('xbox_database', 'w') as f:
        f.write('Name:Developer:Genre:Metascore:MyScore\n')
        rated_games = rated_games_list()
        for game in games_set:
            if game.name not in rated_games:
                f.write(f'{game.name}:{game.developer}:{game.genre}:{game.metascore}:{game.my_score(my_taste)}\n')


def rated_games_list():
    with open('rated_games', 'r') as f:
        rated_games = []
        for line in f:
            game_name = line.rstrip().split(':')[0]
            rated_games.append(game_name)
    return rated_games


def main():
    games_set = WhatToPlay.get_xgp_games()
    my_taste = taste_meter.taste_meter('rated_games')
    create_db(games_set, my_taste)

    df = pd.read_csv('xbox_database', delimiter=':')
    pd.set_option('display.max_rows', None)
    sorted_df = df.sort_values('MyScore', ascending=False)
    print(sorted_df[['Name', 'Metascore', 'MyScore']])


if __name__ == '__main__':
    main()
