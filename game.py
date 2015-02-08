import player
from random import uniform, random

def play(off, deff=None):
    result = None
    points = 0

    random_sp = uniform(0, 100)
    if random_sp < off.o_tendencies['shoot_pass']:
        result = 'PASSED'
    else:
        random_dj = uniform(0, 100)
        if random_dj < off.o_tendencies['drive_jumper']:
            points, result = attempt_jumper(off)
        else:
            points, result = attempt_drive(off)

    return points, result

def attempt_jumper(off, deff=None):
    points = 0
    random_range = uniform(0, 100)
    if random_range < off.shooting_range['close']:
        random_close = random()
        if random_close < 0.007*off.shooting['close']:
            points += 2
            result = 'MADE close'
        else:
            result = 'MISSED close'
    elif random_range < off.shooting_range['mid']:
        random_close = random()
        if random_close < 0.0065*off.shooting['mid']:
            points += 2
            result = 'MADE med'
        else:
            result = 'MISSED mid'
    else:
        random_close = random()
        if random_close < 0.005*off.shooting['long']:
            points += 3
            result = 'MADE 3'
        else:
            result = 'MISSED 3'

    return points, result

def attempt_drive(off, deff=None):
    points = 0
    random_drive = uniform(0, 100)
    if random_drive < off.o_tendencies['layup_dunk']:
        random_layup = random()
        if random_layup < 0.0080*off.driving['layups']:
            points += 2
            result = 'MADE layup'
        else:
            result = 'MISSED layup'
    else:
        random_dunk = random()
        if random_dunk < 0.0085*off.driving['dunking']:
            points += 2
            result = 'MADE dunk'
        else:
            result = 'MISSED dunk'

    return points, result