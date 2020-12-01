import re
import time

import Game
import requests
from bs4 import BeautifulSoup


def get_xgp_games(old_gamenames, rated_gamenames):
    """Getting available Xbox Game Pass game without games which are currently in
    project database file"""
    page_number = 1
    gamenames_set = set()
    games_to_delete = old_gamenames.copy()

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
                if game_name[2] in old_gamenames + rated_gamenames:
                    try:
                        games_to_delete.remove(f"{game_name[2]}")
                    except ValueError:
                        pass
                    continue
                gamenames_set.add(game_name[2])
                """
                # eg. game_name = ['', 'game', 'Life-Is-Strange-2', 'achievements]
                so to access game name I need '2' element.
                """
        page_number += 1
    games_set = set()
    print(f'Number of all new available games: {len(gamenames_set)}')
    i = 1
    for game in gamenames_set:
        print(f'Looking for info about game number: {i}')
        games_set.add(Game.Game(game))
        i += 1
    games_to_delete += rated_gamenames
    return games_set, games_to_delete
