import WhatToPlay


class Game:

    def __init__(self, name):
        self.name = name
        self.score, self.developer, self.genre = WhatToPlay.get_game_info(self.name)

    def __str__(self):
        return f'Name: {self.name}, metascore: {self.score}, developer: {self.developer}, genre: {self.genre}'

    def __repr__(self):
        return f'{self.name}: {self.score}'
