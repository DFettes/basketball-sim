import player

class Team():
    name = ''
    players = []
    points = 0
    possesions = 0

    def __init__(self, name, players):
        self.name = name
        self.players = players
