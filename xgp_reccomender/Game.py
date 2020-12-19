import re
import time
import logging
import requests
from bs4 import BeautifulSoup


logger = logging.getLogger("my_logger")
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)


class Game:
    """Game class containing basic info about certain game: name, metascore, developer, genre"""

    def __init__(self, name, my_taste):
        self.name = name
        self.metascore, self.developer, self.genres = self.get_game_info()
        self.my_taste = my_taste
    
    def __str__(self):
        return f'Name: {self.name}, metascore: {self.metascore}, developer: {self.developer}, genre: {self.genre}'

    def __repr__(self):
        return f'{self.name}: {self.metascore}'

    # Checking metascore of a certain game
    def get_game_info(self):
        """Get info about the game: MetaScore, Developer, Genre."""
        metacritic_url = f"https://www.metacritic.com/game/xbox-one/{self.name.lower()}"
        headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"}
        page = requests.get(metacritic_url, headers=headers)
        if page.status_code == 404:
            metacritic_url = f"https://www.metacritic.com/game/xbox-360/{self.name.lower()}"
            page = requests.get(metacritic_url, headers=headers)
        elif page.status_code == 404:
            time.sleep(10)
            page = requests.get(metacritic_url, headers=headers)

        soup = BeautifulSoup(page.content, 'html.parser')
        site_elems = soup.find(class_=re.compile('^metascore_w xlarge game'))

        if not site_elems:
            return 0, '-', '-'

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
    @property    
    def my_score(self):
        """Method compute MyScore"""
        my_score = self.metascore
        # Check which of genres a game is and which a developer made the game
        for key, value in self.my_taste.items():
            if key in self.genres or key in self.developer:
                my_score += value
        return my_score
