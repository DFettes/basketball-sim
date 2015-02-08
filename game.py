import player
from random import uniform, random, randint
from datetime import datetime, timedelta

def game(t1, t2):
    quarters_played = 0
    t1.points = 0
    t1.possesions = 0
    t2.points = 0
    t2.possesions = 0

    # Opening tip
    rand_jumpball = random()
    if rand_jumpball < 0.5:
        turn = 0
    else:
        turn = 1
    q1 = quarter(t1, t2, turn)

    # Team who looses tip gets possesion to start 2nd and 3rd
    if turn == 0:
        q2 = quarter(t1, t2, 1)
        q3 = quarter(t1, t2, 1)
        q4 = quarter(t1, t2, 1)
    else:
        q2 = quarter(t1, t2, 0)
        q3 = quarter(t1, t2, 0)
        q4 = quarter(t1, t2, 1)

    quarters_played = 4
    # If score tied after 4 quarters, start each overtime with jump ball
    while t1.points == t2.points:
        rand_jumpball = random()
        if rand_jumpball < 0.5:
            turn = 0
        else:
            turn = 1
        ot = quarter(t1, t2, turn, ot=True)
        quarters_played += 1

    return quarters_played


def quarter(t1, t2, turn, ot=False):
    # Initiate game clock to 12:00 for each quarter (5:00 for OT). After each
    # possesion subtract the time used for that possession until no time left
    if ot:
        game_clock = timedelta(minutes = 5)
    else:
        game_clock = timedelta(minutes = 12)

    # Alternate possesions between teams
    while game_clock > timedelta(0):
        #print 'GAME CLOCK:', game_clock
        if turn % 2 == 0:
            points, possesion_time = possesion(t1, game_clock)
            t1.points += points
            t1.possesions += 1
        else:
            points, possesion_time = possesion(t2, game_clock)
            t2.points += points
            t2.possesions += 1
        diff = timedelta(seconds = possesion_time)
        game_clock -= diff
        turn += 1


def possesion(team, game_clock=timedelta(minutes = 12)):
    # If less than 24 seconds left in quarter, 'turn off the shot clock'
    if game_clock < timedelta(seconds = 24):
        shot_clock = game_clock.seconds
    else:
        shot_clock = 24

    # Wait 3-6 seconds before initiating a play
    wait_time = randint(3, 6)
    shot_clock -= wait_time

    # PG carries ball past half most times, else SG or SF
    random_cross_half = uniform(0, 100)

    if random_cross_half < 65:
        points, passed_to, shot_clock = play(team.players[0], team,
                                             shot_clock=shot_clock)
    elif random_cross_half < 85:
        points, passed_to, shot_clock = play(team.players[1], team,
                                             shot_clock=shot_clock)
    else:
        points, passed_to, shot_clock = play(team.players[2], team,
                                             shot_clock=shot_clock)

    while shot_clock > 0 and passed_to != None:
        points, passed_to, shot_clock = play(team.players[passed_to], shot_clock=shot_clock)

    #print 'POINTS:', points
    time_used = 24 - shot_clock
    return points, time_used


def play(off, deff=None, shot_clock=24):
    points = 0
    passed_to = None

    # Hold ball while making a decision for a period of time depending on clock
    if shot_clock > 12:
        decision_time = randint(1, 8)
    elif shot_clock > 5:
        decision_time = randint(1, 4)
    else:
        decision_time = 0
    shot_clock -= decision_time

    # Decide whether to shoot or pass, always shooting if less than 5 secs left
    random_sp = uniform(0, 100)
    if random_sp < 1.5*off.o_tendencies['shoot_pass'] and shot_clock > 5:
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
    off.points += points

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