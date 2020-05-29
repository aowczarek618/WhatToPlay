import Game


# Compute my game taste meter
def taste_meter(filename):
    taste_meter = {}
    with open(filename, 'r') as f:
        for line in f:
            rated_game = line.rstrip().split(':')
            game = Game.Game(rated_game[0])
            game_genres = game.genre
            game_developer = game.developer
            for genre in game_genres:
                if genre not in taste_meter:
                    taste_meter[genre] = int(rated_game[1])
                else:
                    taste_meter[genre] += int(rated_game[1])

            if game_developer not in taste_meter:
                taste_meter[game_developer] = int(rated_game[1])
            else:
                taste_meter[game_developer] += int(rated_game[1])
    return taste_meter
