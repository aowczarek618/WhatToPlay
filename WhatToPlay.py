import requests
from bs4 import BeautifulSoup
import re


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
        return available_games

    # Checking metascore of a certain game
    @staticmethod
    def check_metascore(game_name):
        game_name = game_name.lower()
        metacritic_url = f"https://www.metacritic.com/game/xbox-one/{game_name}"
        page = requests.get(metacritic_url) # Error 403
        soup = BeautifulSoup(page.content, 'html.parser')
        site_elems = soup.find()
        print(site_elems.prettify())

    # Rating a game I played
    def rate_game(self):
        raise NotImplementedError

    # Recommend which game should I play
    def recommend_me_sth(self):
        raise NotImplementedError
