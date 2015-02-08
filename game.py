import player
from random import uniform, random, randint

def possesion(team):
    shot_clock = 24

    # Wait 3-6 seconds before initiating a play
    wait_time = randint(3, 6)

    # PG carries ball past half most times, else SG or SF
    random_cross_half = uniform(0, 100)

    if random_cross_half < 65:
        points, passed_to, shot_clock = play(team.players[0], team)
    elif random_cross_half < 85:
        points, passed_to, shot_clock = play(team.players[1], team)
    else:
        points, passed_to, shot_clock = play(team.players[2], team)

    while shot_clock > 0 and passed_to != None:
        #print 'PASSED TO:', team.players[passed_to].name
        points, passed_to, shot_clock = play(team.players[passed_to])

    #print 'POINTS:', points
    return points


def play(off, deff=None, shot_clock=24):
    print 'PLAYER:', off.name
    points = 0
    passed_to = None

    # Hold ball while making a decision for a period of time depending on clock
    if shot_clock > 12:
        decision_time = randint(1, 8)
    elif shot_clock > 5:
        decision_time = randint(1, 4)
    else:
        decision_time = randint(0, shot_clock)
    shot_clock -= decision_time
    #print 'SHOT CLOCK:', shot_clock

    # Decide whether to shoot or pass, always shooting if less than 5 secs left
    random_sp = uniform(0, 100)
    if random_sp < off.o_tendencies['shoot_pass'] and shot_clock > 5:
        passed_to = attempt_pass(off)
        off.passes += 1
    else:
        random_dj = uniform(0, 100)
        if random_dj < off.o_tendencies['drive_jumper']:
            #print 'JUMPER BY:', off.name
            points = attempt_jumper(off)
        else:
            #print 'DRIVE BY:', off.name
            points = attempt_drive(off)

    return points, passed_to, shot_clock

def attempt_jumper(off, deff=None):
    points = 0
    random_range = uniform(0, 100)

    if random_range < off.shooting_range['close']:
        off.fg2a += 1
        random_close = random()
        if random_close < 0.007*off.shooting['close']:
            off.fg2m += 1
            points += 2
    elif random_range < off.shooting_range['mid']:
        off.fg2a += 1
        random_close = random()
        if random_close < 0.0065*off.shooting['mid']:
            off.fg2m += 1
            points += 2
    else:
        off.fg3a += 1
        random_close = random()
        if random_close < 0.005*off.shooting['long']:
            off.fg3m += 1
            points += 3

    return points

def attempt_drive(off, deff=None):
    points = 0
    random_drive = uniform(0, 100)

    if random_drive < off.o_tendencies['layup_dunk']:
        off.fg2a += 1
        random_layup = random()
        if random_layup < 0.0080*off.driving['layups']:
            off.fg2m += 1
            points += 2
    else:
        off.fg2a += 1
        random_dunk = random()
        if random_dunk < 0.0085*off.driving['dunking']:
            off.fg2m += 1
            points += 2

    return points

def attempt_pass(off):
    rand_pass = uniform(0, 100)
    total = 0

    for p in range(5):
        total += off.passing_choice[p]
        if rand_pass < total and p != off.position -1:
            passed_to = p
            break

    return passed_to