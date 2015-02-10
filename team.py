import player

class Team():
    name = ''
    players = []
    points = 0
    possesions = 0

    wins = 0
    losses = 0
    season_points = 0

    def __init__(self, name, players):
        self.name = name
        self.players = players
