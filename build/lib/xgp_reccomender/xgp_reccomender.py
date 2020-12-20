import re
import time
import logging
import requests
from bs4 import BeautifulSoup
from xgp_reccomender.Game import Game
import pandas
import os

logger = logging.getLogger("my_logger")
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

class XgpReccomender:

    def __init__(self):
        """Create database of all avaiable Xbox Game Pass games"""
        self.my_taste = self.taste_meter(rate_weight=1)

        with open('xbox_database', 'w') as f:
            if os.stat('xbox_database').st_size == 0:
                f.write('Name:Developer:Genre:Metascore:MyScore\n')

            rated_games = self.rated_games_list()
            for game in self.get_xgp_games():
                if game.name not in rated_games:
                    f.write(f"{re.sub('-', ' ', game.name)}:{game.developer}:{', '.join(game.genres)}:{game.metascore}:{game.my_score}\n")
        
        self.database = self.create_db()

    def get_xgp_games(self):
        """Getting available Xbox Game Pass games"""
        logger.info("Getting available Xbox Game Pass games...")
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
                    game_name = a['href'].split('/')[2] # eg. game_name = ['', 'game', 'Life-Is-Strange-2', 'achievements]
                    gamenames_set.add(game_name)
            page_number += 1
        
        games_set = set()
        logger.info(f'Number of all available games: {len(gamenames_set)}...')
        for count, game in enumerate(gamenames_set):
            logger.info(f'Looking for info about game number: {count}...')
            games_set.add(Game(name=game, my_taste=self.my_taste))
        return games_set

    @staticmethod
    def rated_games_list():
        """Create rated games list"""
        logger.info("Creating rated games list...")
        rated_games = []
        with open('rated_games', 'r') as f:
            for line in f:
                game_name = line.rstrip().split(':')[0]
                rated_games.append(game_name)
        return rated_games

    @staticmethod
    def taste_meter(rate_weight=1):
        """Computing my game taste"""
        logger.info("Computing my game taste...")
        taste_meter = {}
        with open('rated_games', 'r') as f:
            for line in f:
                game_name, rating = line.rstrip().split(':')
                game = Game(name=game_name, my_taste=None)
                for genre in game.genres:
                    if genre not in taste_meter:
                        taste_meter[genre] = rate_weight * int(rating)
                    else:
                        taste_meter[genre] += rate_weight * int(rating)

                if game.developer not in taste_meter:
                    taste_meter[game.developer] = rate_weight * int(rating)
                else:
                    taste_meter[game.developer] += rate_weight * int(rating)
        return taste_meter

    @staticmethod
    def create_db():
        pandas.set_option('display.width', 1000)
        pandas.set_option('colheader_justify', 'center')
        pandas.set_option('display.max_rows', None)

        database = pandas.read_csv('xbox_database', delimiter=':')
        database = database.sort_values('MyScore', ascending=False)
        database = database[database['Metascore'] != 0]

        return database


    def generate_html(self):
        html_string = '''
        <html>
          <head><title>HTML Pandas Dataframe with CSS</title></head>
          <link rel="stylesheet" type="text/css" href="df_style.css"/>
          <body>
            {table}
          </body>
        </html>.
        '''

        # OUTPUT AN HTML FILE
        with open('game_ranking.html', 'w') as f:
            f.write(html_string.format(table=self.database.to_html(classes='mystyle')))
