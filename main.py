import Game
import WhatToPlay


def write_to_file(my_dict):
    with open('recommended_games.txt', 'w') as f:
        for key, value in my_dict.items():
            f.write(f'{key}, {value}\n')


def main():
    # games_list = WhatToPlay.get_xgp_games()
    # available_games = []
    # for game in games_list:
    #     available_games.append(Game.Game(game))
    print(Game.Game("Red-Dead-Redemption-2"))
    # print(available_games)


if __name__ == '__main__':
    main()
