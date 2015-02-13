import toks
import random

POSITIONS = {1: 'PG', 2: 'SG', 3: 'SF', 4: 'PF', 5: 'C'}

class Player():
    name = ''
    position = 0

    # Player skills
    shooting = {'close': 0, 'mid': 0, 'long': 0, 'ft': 0}
    driving = {'layups': 0, 'dunking': 0}
    skills = {'speed': 0, 'dribbling': 0, 'passing': 0}
    defense = {'rebounding': 0, 'defense': 0, 'blocking': 0, 'stealing': 0}

    # Player tendencies
    o_tendencies = {'shoot_pass': 0, 'drive_jumper': 0, 'layup_dunk': 0}
    d_tendencies = {'go_for_steal': 0, 'go_for_block': 0}
    shooting_range = {'close': 0, 'mid': 0, 'long': 0}
    passing_choice = [0, 0, 0, 0, 0]

    # Player offensive chance rolls
    complete_pass = 0
    protect_drive = 0

    # Player defensive chance rolls
    steal_pass = 0
    steal_drive = 0
    block_chance = 0

    # Player stats
    games = 0
    fga = 0
    fg2a = 0
    fg3a = 0
    fta = 0
    fgm = 0
    fg2m = 0
    fg3m = 0
    ftm = 0
    points = 0
    assists = 0
    rebounds = 0
    def_rebounds = 0
    off_rebounds = 0
    turnovers = 0
    steals = 0
    blocks = 0
    passes = 0

    def __init__(self, name, position, floor=50, ceiling=100):
        self.name = name
        self.position = position
        self.position_string = POSITIONS[position]

        skills_array = randomize_skills(floor, ceiling)
        self.shooting = skills_array[0]
        self.driving = skills_array[1]
        self.skills = skills_array[2]
        self.defense = skills_array[3]

        tendencies_array = randomize_tendencies(position)
        self.o_tendencies = tendencies_array[0]
        self.d_tendencies = tendencies_array[1]
        self.shooting_range = tendencies_array[2]
        self.passing_choice = tendencies_array[3]

        self.complete_pass = self.skills['passing'] / float(100)
        self.protect_drive = (0.60 * self.skills['dribbling'] + \
                              0.40 * self.skills['speed']) / float(100)

        self.steal_drive = (0.40 * self.defense['defense'] + \
                            0.30 * self.skills['speed'] + \
                            0.30 * self.defense['stealing']) / float(100)
        self.steal_pass = (0.25 * self.defense['defense'] + \
                           0.35 * self.skills['speed'] + \
                           0.40 * self.defense['stealing']) / float(100)
        self.block_chance = (0.80 * self.defense['blocking'] + \
                           0.40 * self.defense['defense']) / float(750)


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

def randomize_skills(floor=50, ceiling=100):
    shooting = {}
    driving = {}
    skills = {}
    defense = {}

    for key in toks.DEF_SHOOTING:
        shooting[key] = random.randint(floor, ceiling)
    for key in toks.DEF_DRIVING:
        driving[key] = random.randint(floor, ceiling)
    for key in toks.DEF_SKILLS:
        skills[key] = random.randint(floor, ceiling)
    for key in toks.DEF_DEFENSE:
        defense[key] = random.randint(floor, ceiling)

    return shooting, driving, skills, defense

def randomize_tendencies(position):
    o_tendencies = {}
    d_tendencies = {}
    shooting_range = {}

    for key in toks.DEF_OFFENSIVE:
        o_tendencies[key] = random.randint(40, 60)
    for key in toks.DEF_DEFENSIVE:
        d_tendencies[key] = random.randint(40, 60)

    total = 0
    shot_range = []
    for i in range(3):
        value = random.randint(20, 80)
        total += value
        shot_range.append(value)
    shooting_range['close'] = 100*float(shot_range[0]) / total
    shooting_range['mid'] = 100*float(shot_range[1]) / total
    shooting_range['long'] = 100*float(shot_range[2]) / total

    total = 0
    passing_choice = []
    for i in range(5):
        if i == position - 1:
            value = 0
        else:
            value = random.randint(20, 80)
            total += value
        passing_choice.append(value)
    for i in range(5):
        if i != position - 1:
            passing_choice[i] = 100*float(passing_choice[i]) / total

    return o_tendencies, d_tendencies, shooting_range, passing_choice