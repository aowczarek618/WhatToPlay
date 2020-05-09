import requests
from bs4 import BeautifulSoup
import re
import operator


class WhatToPlay:

    # Getting available games in Xbox Game Pass
    @staticmethod
    def get_xgp_games():
        page_number = 1
        available_games = set()

        while True:
            true_achievements_url = f"https://www.trueachievements.com/xbox-game-pass/games?page={page_number}"
            page = requests.get(true_achievements_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            site_elems = soup.findAll('tr', id=re.compile('^tr'))

            if not site_elems:
                break

            for site_elem in site_elems:
                for a in site_elem.find_all('a', href=True):
                    game_name = a['href']
                    game_name = game_name.split('/')
                    available_games.add(game_name[2])
                    """
                    # eg. game_name = ['', 'game', 'Life-Is-Strange-2', 'achievements]
                    so to access game name I need '2' element.
                    """
            page_number += 1
        return list(available_games)

    # Checking metascore of a certain game
    @staticmethod
    def check_metascore(game_name):
        game_name = game_name.lower()
        metacritic_url = f"https://www.metacritic.com/game/xbox-one/{game_name}"

        headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"}
        page = requests.get(metacritic_url, headers=headers)
        print(page)
        soup = BeautifulSoup(page.content, 'html.parser')
        site_elems = soup.find(class_='metascore_w xlarge game positive')

        if not site_elems:
            return 0
        else:
            span_elem = site_elems.find('span')
            return int(span_elem.text)

    # Rating a game I played
    def rate_game(self):
        raise NotImplementedError

    # Recommend which game should I play
    @staticmethod
    def recommend_me_sth():
        available_games = WhatToPlay.get_xgp_games()
        available_games_with_scores = {}
        print(len(available_games))

        i = 1
        for game in available_games:
            print(game, i)
            available_games_with_scores[game] = WhatToPlay.check_metascore(game)
            i += 1

        return dict(sorted(available_games_with_scores.items(), key=operator.itemgetter(1), reverse=True))

