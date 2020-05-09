import requests
from bs4 import BeautifulSoup
import re
import operator


# Getting available games in Xbox Game Pass
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
def get_game_info(game_name):
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
        metascore = int(site_elems.find('span').text)

        site_elems = soup.find(class_='summary_detail developer')
        developer = site_elems.find(class_='data').text
        developer = developer.strip()

        site_elems = soup.find(class_='summary_detail product_genre')
        genres_site_elems = site_elems.findAll('span', class_='data')
        genres = set()
        for genre in genres_site_elems:
            genres.add(genre.get_text())
        return metascore, developer, genres


# Compute game score given by my game taste
def my_score(game):
    # Load from file rated games by me

    # Check which of genres a game is and which a developer made the game

    # Finally, look for taste points in the file for given genres and developers and compute my score
    raise NotImplementedError

