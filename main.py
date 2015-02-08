
import player
import game
import random

def main():
    p1 = player.Player('Gopal Unibrownguy', 1)

    p1.shooting = {'close': 50, 'mid': 60, 'long': 90, 'ft': 80}
    p1.driving = {'layups': 65, 'dunking': 30}
    p1.skills = {'speed': 75, 'dribbling': 80, 'passing': 70}
    p1.defense = {'rebounding': 30, 'defense': 65, 'blocking': 20, 'stealing': 70}

    p1.o_tendencies = {'shoot_pass': 10, 'drive_jumper': 70, 'layup_dunk': 40}
    p1.d_tendencies = {'go_for_steal': 60, 'go_for_block': 20}
    p1.shooting_range = {'close': 10, 'mid': 40, 'long': 50}
    p1.passing_choice = [0, 20, 30, 20, 30]

    p2 = player.random_player('Dan Fettes', 2, floor=70, ceiling=90)
    sim_test(p2)



def sim_test(player):
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
