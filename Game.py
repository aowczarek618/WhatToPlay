import WhatToPlay
import requests
from bs4 import BeautifulSoup
import taste_meter
import time


class Game:
    """Game class containing basic info about certain game: name, metascore, developer, genre"""
    def __init__(self, name):
        self.name = name
        self.metascore, self.developer, self.genre = Game.get_game_info(self)

    def __str__(self):
        return f'Name: {self.name}, metascore: {self.metascore}, developer: {self.developer}, genre: {self.genre}'

    def __repr__(self):
        return f'{self.name}: {self.metascore}'

    # Checking metascore of a certain game
    def get_game_info(self):
        """
        Get info about the game: MetaScore, Developer, Genre.
        Method only is looking for games which metascore is greater or equal than 75
        """
        metacritic_url = f"https://www.metacritic.com/game/xbox-one/{self.name.lower()}"
        headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"}
        page = requests.get(metacritic_url, headers=headers)
        print(f'Page status code: {page.status_code}')
        if page.status_code == 429:
            time.sleep(10)
            page = requests.get(metacritic_url, headers=headers)
        elif page.status_code == 404:
            return 0, '-', '-'
        soup = BeautifulSoup(page.content, 'html.parser')
        site_elems = soup.find(class_='metascore_w xlarge game positive')

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
    def my_score(self, my_taste):
        """Method compute MyScore"""
        my_score = self.metascore
        # Check which of genres a game is and which a developer made the game

        for value, key in my_taste.items():
            if value in self.genre or value in self.developer:
                my_score += key
        return my_score
