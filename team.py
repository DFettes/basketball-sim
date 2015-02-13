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

    def team_rebound_chance(self):
        # Give team a weighted rebounding score based on its players
        rebound_chance = 0.29*self.players[4].defense['rebounding'] + \
                         0.24*self.players[3].defense['rebounding'] + \
                         0.19*self.players[2].defense['rebounding'] + \
                         0.15*self.players[1].defense['rebounding'] + \
                         0.13*self.players[1].defense['rebounding']

        return rebound_chance

    def player_rebound_chance(self, rand_reb):
        # Calculate who on the team gets the rebound from their weighted stats
        totals = []
        running_total = 0
        weights = [0.13, 0.15, 0.19, 0.24, 0.29]

        for p, w in zip(self.players, weights):
            weighted_reb = p.defense['rebounding'] * w
            running_total += weighted_reb
            totals.append(running_total)

        rand_reb *= running_total
        for i, total in enumerate(totals):
            if rand_reb < total:
                break

        return self.players[i]
