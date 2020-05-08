class WhatToPlay:

    # Constructor of WhatToPlay class
    def __init__(self, available_games):
        self.available_games = available_games

    # Getting available games in Xbox Game Pass
    def get_xgp_games(self):
        raise NotImplementedError

    # Checking metascore of a certain game
    def check_metascore(self):
        raise NotImplementedError

    # Rating a game I played
    def rate_game(self):
        raise NotImplementedError

    # Recommend which game should I play
    def recommend_me_sth(self):
        raise NotImplementedError
