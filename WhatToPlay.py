import re

import Game
import requests
from bs4 import BeautifulSoup


# Getting available games in Xbox Game Pass
def get_xgp_games():
    page_number = 1
    gamenames_set = set()

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
                gamenames_set.add(game_name[2])
                """
                # eg. game_name = ['', 'game', 'Life-Is-Strange-2', 'achievements]
                so to access game name I need '2' element.
                """
        page_number += 1
    games_set = set()
    print(len(gamenames_set))
    i = 1
    for game in gamenames_set:
        print(i)
        games_set.add(Game.Game(game))
        i += 1
    return games_set

