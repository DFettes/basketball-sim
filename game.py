import player
from random import uniform, random, randint
from datetime import datetime, timedelta

TURNOVERS = ['stolen_pass', 'stripped_drive', 'blocked_shot', 'blocked_drive']

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

    if t1.points > t2.points:
        t1.wins += 1
        t2.losses += 1
    else:
        t1.losses += 1
        t2.wins += 1
    t1.season_points += t1.points
    t2.season_points += t2.points

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
            points, possesion_time, reb = possesion(t1, t2, game_clock)
            t1.points += points
            t1.possesions += 1
        else:
            points, possesion_time, reb = possesion(t2, t1, game_clock)
            t2.points += points
            t2.possesions += 1
        diff = timedelta(seconds = possesion_time)
        game_clock -= diff
        if reb != 'off_rebound':
            turn += 1


def possesion(team, deff_team, game_clock=timedelta(minutes = 12)):
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

    if random_cross_half < 55:
        current_player = team.players[0]
        points, passed_to, off, \
        shot_clock , ass, result = play(current_player, deff_team,
                                        shot_clock=shot_clock)
    elif random_cross_half < 80:
        current_player = team.players[1]
        points, passed_to, off, \
        shot_clock, ass, result = play(current_player, deff_team,
                                       shot_clock=shot_clock)
    else:
        current_player = team.players[2]
        points, passed_to, off, \
        shot_clock, ass, result = play(current_player, deff_team,
                                       shot_clock=shot_clock)

    next_player = current_player
    while shot_clock > 0 and passed_to != None and result not in TURNOVERS:
        try:
            current_player = off
            next_player = team.players[passed_to]
        except TypeError:
            pass
        points, passed_to, off, \
        shot_clock, ass, result = play(team.players[passed_to], \
                                  deff_team, shot_clock=shot_clock)

    if points > 0 and current_player != next_player and ass:
        #print 'ASSIST BY ', current_player.name
        current_player.assists += 1
    time_used = 24 - shot_clock

    reb = None
    if result == 'missed_shot':
        reb = rebound(team, deff_team)

    return points, time_used, reb


def play(off, deff=None, shot_clock=24):
    #print 'PLAYER: %s' % off.name
    points = 0
    passed_to = None
    result = None

    # Hold ball while making a decision for a period of time depending on clock
    if shot_clock > 12:
        decision_time = randint(1, 6)
    elif shot_clock > 5:
        decision_time = randint(1, 4)
    else:
        decision_time = 0
    shot_clock -= decision_time

    # Decide whether to shoot or pass, always shooting if less than 5 secs left.
    # Players get more likely to shoot as shot clock gets lower. If decision
    # time greater than 4 secs, any basket will be unassisted
    assisted = True
    if decision_time > 4:
        assisted = False
    random_sp = random()
    urgent = 1 - (24 - shot_clock)/float(25)
    if random_sp < ((off.o_tendencies['shoot_pass'] - 50)/float(300) + urgent) \
    and shot_clock > 5:
        passed_to, result = attempt_pass(off, deff)
        off.passes += 1
    else:
        random_dj = uniform(0, 100)
        if random_dj < off.o_tendencies['drive_jumper']:
            #print 'JUMPER BY:', off.name
            points, result = attempt_jumper(off, deff)
        else:
            #print 'DRIVE BY:', off.name
            points, result = attempt_drive(off, deff)
    off.points += points

    return points, passed_to, off, shot_clock, assisted, result

def attempt_jumper(off, deff=None):
    points = 0
    random_range = uniform(0, 100)
    defender = deff.players[off.position - 1]
    def_block_chance = defender.block_chance
    rand_block = random()

    if random_range < off.shooting_range['close']:
        off.fg2a += 1
        if rand_block < def_block_chance*0.5:
            defender.blocks += 1
            return points, 'blocked_shot'
        random_close = random()
        if random_close < 0.006*off.shooting['close']:
            off.fg2m += 1
            points += 2
            result = 'made_shot'
        else:
            result = 'missed_shot'
    elif random_range < off.shooting_range['mid']:
        off.fg2a += 1
        if rand_block < def_block_chance*0.2:
            defender.blocks += 1
            return points, 'blocked_shot'
        random_close = random()
        if random_close < 0.0055*off.shooting['mid']:
            off.fg2m += 1
            points += 2
            result = 'made_shot'
        else:
            result = 'missed_shot'
    else:
        off.fg3a += 1
        if rand_block < def_block_chance*0.1:
            defender.blocks += 1
            return points, 'blocked_shot'
        random_close = random()
        if random_close < 0.0048*off.shooting['long']:
            off.fg3m += 1
            points += 3
            result = 'made_shot'
        else:
            result = 'missed_shot'

    return points, result

def attempt_drive(off, deff=None):
    points = 0

    # First calculate whether player is stripped of the ball by their defender
    defender = deff.players[off.position - 1]
    protect_ball = 0.92 + (off.protect_drive - defender.steal_pass) / 20
    if protect_ball > 0.97:
        protect_ball = 0.97
    elif protect_ball < 0.87:
        protect_ball = 0.87
    rand_protect = random()
    if rand_protect > protect_ball:
        defender.steals += 1
        off.turnovers += 1
        return points, 'stripped_drive'

    # Decide whether attempting a layup or a dunk. Then combine attributes of
    # player's man defender, plus the two post defenders to calculate whether
    # the dunk or layup is blocked
    def_block_chance = defender.block_chance
    pf_block_chance = deff.players[3].block_chance
    c_block_chance = deff.players[4].block_chance

    rand_block_player = random()
    if off.position == 5:
        total_block_chance = 0.70*def_block_chance + 0.30*pf_block_chance
        if rand_block_player < 0.70:
            block_player = defender
        else:
            block_player = deff.players[3]
    elif off.position == 4:
        total_block_chance = 0.60*def_block_chance + 0.40*c_block_chance
        if rand_block_player < 0.60:
            block_player = defender
        else:
            block_player = deff.players[4]
    else:
        total_block_chance = 0.30*def_block_chance + 0.30*pf_block_chance \
                           + 0.40*c_block_chance
        if rand_block_player < 0.40:
            block_player = defender
        elif rand_block_player < 0.60:
            block_player = deff.players[3]
        else:
            block_player = deff.players[4]

    random_drive = uniform(0, 100)
    if random_drive < off.o_tendencies['layup_dunk']:
        off.fg2a += 1
        random_block = random()
        if random_block < total_block_chance:
            block_player.blocks += 1
            return points, 'blocked_drive'
        random_layup = random()
        if random_layup < 0.0065*off.driving['layups']:
            off.fg2m += 1
            points += 2
            result = 'made_shot'
        else:
            result = 'missed_shot'
    else:
        off.fg2a += 1
        random_block = random()
        if random_block < 0.5*total_block_chance:
            block_player.blocks += 1
            return points, 'blocked_drive'
        random_dunk = random()
        if random_dunk < 0.0080*off.driving['dunking']:
            off.fg2m += 1
            points += 2
            result = 'made_shot'
        else:
            result = 'missed_shot'

    return points, result

def attempt_pass(off, deff):
    # Decide which teammate to attempt a pass to
    rand_pass = uniform(0, 100)
    total = 0

    for p in range(5):
        total += off.passing_choice[p]
        if rand_pass < total and p != off.position -1:
            pass_to = p
            break

    # Give player defending the intended target a 5-25% chance of stealing the
    # pass, depending on attributes
    guarding_pass = deff.players[pass_to ]
    make_pass = 0.96 + (off.complete_pass - guarding_pass.steal_pass) / 50
    if make_pass > 0.98:
        make_pass = 0.98
    elif make_pass < 0.94:
        make_pass = 0.94
    rand_steal = random()
    if rand_steal < make_pass:
        return pass_to, 'made_pass'
    else:
        guarding_pass.steals += 1
        off.turnovers += 1
        return pass_to, 'stolen_pass'

def rebound(off, deff):
    # If attributes are equal, def team will get the rebound ~75% of the time
    deff_rebound_chance = 3*deff.team_rebound_chance()
    off_rebound_chance = off.team_rebound_chance()
    total = deff_rebound_chance + off_rebound_chance
    deff_rebound_chance = deff_rebound_chance / total
    off_rebound_chance = off_rebound_chance / total

    rand_reb_team = random()
    rand_reb_player = random()
    if rand_reb_team < deff_rebound_chance:
        reb_player = deff.player_rebound_chance(rand_reb_player)
        reb_player.def_rebounds += 1
        reb_player.rebounds += 1
        return 'def_rebound'
    else:
        reb_player = off.player_rebound_chance(rand_reb_player)
        reb_player.off_rebounds += 1
        reb_player.rebounds += 1
        return 'off_rebound'
