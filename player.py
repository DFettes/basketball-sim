import toks
import random

POSITIONS = {1: 'PG', 2: 'SG', 3: 'SF', 4: 'PF', 5: 'C'}

class Player():
    name = ''
    position = 0

    shooting = {'close': 0, 'mid': 0, 'long': 0, 'ft': 0}
    driving = {'layups': 0, 'dunking': 0}
    skills = {'speed': 0, 'dribbling': 0, 'passing': 0}
    defense = {'rebounding': 0, 'defense': 0, 'blocking': 0, 'stealing': 0}

    o_tendencies = {'shoot_pass': 0, 'drive_jumper': 0, 'layup_dunk': 0}
    d_tendencies = {'go_for_steal': 0, 'go_for_block': 0}
    shooting_range = {'close': 0, 'mid': 0, 'long': 0}
    passing_choice = [0, 0, 0, 0, 0]

    def __init__(self, name, position, shooting=toks.DEF_SHOOTING,
                 driving=toks.DEF_DRIVING, skills=toks.DEF_SKILLS,
                 defense=toks.DEF_DEFENSE, offensive=toks.DEF_OFFENSIVE,
                 defensive=toks.DEF_DEFENSIVE, shot_range=toks.DEF_SHOT_RANGE,
                 passing=toks.DEF_PASSING):

        self.name = name
        self.position = position
        self.position_string = POSITIONS[position]

        self.shooting = shooting
        self.driving = driving
        self.skills = skills
        self.defense = defense

        self.o_tendencies = offensive
        self.d_tendencies = defensive
        self.shooting_range = shot_range
        self.passing_choice = passing


    def print_player(self):
        print self.name
        print self.position_string
        print self.shooting
        print self.driving
        print self.defense
        print self.skills
        print self.o_tendencies
        print self.d_tendencies
        print self.shooting_range
        print self.passing_choice

def random_player(name, position, floor=50, ceiling=100):
    p = Player(name, position)

    for key in p.shooting:
        p.shooting[key] = random.randint(floor, ceiling)
    for key in p.driving:
        p.driving[key] = random.randint(floor, ceiling)
    for key in p.skills:
        p.skills[key] = random.randint(floor, ceiling)
    for key in p.defense:
        p.defense[key] = random.randint(floor, ceiling)

    for key in p.o_tendencies:
        p.o_tendencies[key] = random.randint(0, 100)
    for key in p.d_tendencies:
        p.d_tendencies[key] = random.randint(0, 100)

    total = 0
    shot_range = []
    for i in range(3):
        value = random.randint(0, 100)
        total += value
        shot_range.append(value)
    p.shooting_range['close'] = int(100*float(shot_range[0]) / total)
    p.shooting_range['long'] = int(100*float(shot_range[1]) / total)
    p.shooting_range['long'] = int(100*float(shot_range[2]) / total)
    total = 0

    for i in range(5):
        if i == p.position - 1:
            value = 0
        else:
            value = random.randint(0, 100)
            total += value
        p.passing_choice[i] = value
    for i in range(5):
        if i != p.position - 1:
            p.passing_choice[i] = int(100*float(p.passing_choice[i]) / total)

    return p
