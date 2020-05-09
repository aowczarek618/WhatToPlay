import WhatToPlay


def write_to_file(my_dict):
    with open('recommended_games.txt', 'w') as f:
        for key, value in my_dict.items():
            f.write(f'{key}, {value}\n')


def main():
    what_to_play = WhatToPlay.WhatToPlay()
    # print(what_to_play.check_metascore("The-Witcher-3-Wild-Hunt"))
    recommended_games = (what_to_play.recommend_me_sth())
    write_to_file(recommended_games)


if __name__ == '__main__':
    main()
