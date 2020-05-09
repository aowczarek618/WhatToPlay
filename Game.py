import WhatToPlay


class Game:

    def __init__(self, name):
        self.name = name
        self.score = WhatToPlay.check_metascore(self.name)