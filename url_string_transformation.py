"""
Getting a real game name from a url game name for true achievement site (trueachievements.com) eg.
Call-Of-Duty-Black-Ops-4 --> Call of Duty Black Ops 4
Special characters are omitted, no need to implement it.
If I would to be exact, function should return "Call of Duty: Black Ops 4".
"""


def game_name_from_url_true_achievements(game_name):
    return game_name.replace('-', ' ')


"""
Getting a url game name from a real game name for metacritic site (metacritic.com) eg.
Call of Duty Black Ops 4 --> call-of-duty-black-ops-4
Special characters are omitted, no need to implement it.
If I would to be exact, function input should be "Call of Duty: Black Ops 4".
"""


def game_name_to_url_metacritic(game_name):
    game_name = game_name.lower()
    return game_name.replace(' ', '-')

