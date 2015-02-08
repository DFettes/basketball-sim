import player
import team
import game
import random

def main():
    p1 = player.Player('Gopal Unibrownguy', 1, floor=70, ceiling=90)
    p2 = player.Player('Dan Fettes', 2, floor=70, ceiling=90)
    p3 = player.Player('Matt Nero', 3, floor=70, ceiling=90)
    p4 = player.Player('Azhar Dewji', 4, floor=40, ceiling=60)
    p5 = player.Player('Janarth K-something', 5, floor=70, ceiling=90)

    p11 = player.Player('Player 1', 1, floor=70, ceiling=90)
    p12 = player.Player('Player 2', 2, floor=70, ceiling=90)
    p13 = player.Player('Player 3', 3, floor=70, ceiling=90)
    p14 = player.Player('Player 4', 4, floor=40, ceiling=60)
    p15 = player.Player('player 5', 5, floor=70, ceiling=90)

    t1 = team.Team('Simcoe Sabres', [p1, p2, p3, p4, p5])
    t2 = team.Team('McMaster Mauraduers', [p11, p12, p13, p14, p15])

    sim_game(t1, t2)


def sim_game(team1, team2):
    quarters_played = game.game(team1, team2)

    for team in [team1, team2]:
        print ''
        print team.name
        name_width = max([len(p.name) for p in team.players])
        print '|        Name        |Pts|  FG  | 3PT |'
        print '---------------------------------------'
        for p in team.players:
            p.fga = p.fg2a + p.fg3a
            p.fgm = p.fg2m + p.fg3m
            fg_string = '%s/%s' % (p.fgm, p.fga)
            fg3_string = '%s/%s' % (p.fg3m, p.fg3a)
            print '|{0:<{n}}|{1:<{p}}|{2:<{f}}|{3:<{t}}|'.format(p.name,
            p.points, fg_string, fg3_string, n=20, p=3, f=6, t=5)

    print ''
    if quarters_played == 4:
        print 'FINAL SCORE'
    else:
        print 'FINAL SCORE (%sOT):' % (quarters_played - 4)
    print '%s: %s' % (team1.name, team1.points)
    print '%s: %s' % (team2.name, team2.points)


def sim_quarter(team1, team2):
    game.quarter(team1, team2)
    print ''
    print 'Team1:', team1.points
    print 'Team2:', team2.points


def sim_possesions(team):
    points = 0
    for i in range(100):
        points += game.possesion(team)[0]
    print ''
    print 'TOTAL POINTS:', points


def sim_plays(player):
    print player.name
    print player.o_tendencies
    print player.shooting_range
    print player.shooting
    print player.driving

    for i in range(10000):
        points, result = game.play(player)

    player.fga = player.fg2a + player.fg3a
    player.fgm = player.fg2m + player.fg3m
    print 'FG: %s/%s' % (player.fgm, player.fga)
    print '2ptFG: %s/%s' % (player.fg2m, player.fg2a)
    print '3ptFG: %s/%s' % (player.fg3m, player.fg3a)
    print 'FGp: %s' % (player.fgm/float(player.fga))
    print '3FGp: %s' % (player.fg3m/float(player.fg3a))


if __name__ == '__main__':
    main()