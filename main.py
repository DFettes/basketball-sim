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

    t1 = team.Team('Simcoe Sabres', [p1, p2, p3, p4, p5])
    t2 = team.Team('McMaster Mauraduers', [p1, p2, p3, p4, p5])

    sim_quarter(t1)


def sim_quarter(team):
    points, possesions = game.quarter(team)
    print ''
    print 'TOTAL POINTS:', points
    print 'POINTS/100POSS:', 100*float(points)/possesions


def sim_possesions(team):
    points = 0
    for i in range(100):
        points += game.possesion(team)[0]
    print ''
    print 'TOTAL POINTS:', points
    for player in team.players:
        print ''
        print player.name
        player.fga = player.fg2a + player.fg3a
        player.fgm = player.fg2m + player.fg3m
        print 'FG: %s/%s' % (player.fgm, player.fga)
        print 'PASSES: %s' % player.passes
        print '2ptFG: %s/%s' % (player.fg2m, player.fg2a)
        print '3ptFG: %s/%s' % (player.fg3m, player.fg3a)


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