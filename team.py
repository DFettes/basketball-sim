import player

class Team():
    name = ''
    home = None
    away = None
    players = []
    on_floor = []
    on_bench = []
    points = 0
    possesions = 0

    wins = 0
    losses = 0
    season_points = 0

    def __init__(self, name, players):
        self.name = name
        self.players = players
        self.starters = players[:5]
        self.bench = players[5:]
        self.on_floor = list(self.starters)
        self.on_bench = list(self.bench)

    def team_rebound_chance(self):
        # Give team a weighted rebounding score based on its players
        rebound_chance = 0.29*self.on_floor[4].defense['rebounding'] + \
                         0.24*self.on_floor[3].defense['rebounding'] + \
                         0.19*self.on_floor[2].defense['rebounding'] + \
                         0.15*self.on_floor[1].defense['rebounding'] + \
                         0.13*self.on_floor[1].defense['rebounding']

        return rebound_chance

    def player_rebound_chance(self, rand_reb):
        # Calculate who on the team gets the rebound from their weighted stats
        totals = []
        running_total = 0
        weights = [0.13, 0.15, 0.19, 0.24, 0.29]

        for p, w in zip(self.on_floor, weights):
            weighted_reb = p.defense['rebounding'] * w
            running_total += weighted_reb
            totals.append(running_total)

        rand_reb *= running_total
        for i, total in enumerate(totals):
            if rand_reb < total:
                break

        return self.on_floor[i]
