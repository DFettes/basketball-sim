import player
import team
import game
import random

def main():
    p1 = player.Player('Gopal Unibrownguy', 1, floor=70, ceiling=90)
    p2 = player.Player('Dan Fettes', 2, floor=100, ceiling=100)
    p3 = player.Player('Matt Nero', 3, floor=70, ceiling=90)
    p4 = player.Player('Azhar Dewji', 4, floor=70, ceiling=90)
    p5 = player.Player('Janarth K-something', 5, floor=70, ceiling=90)

    p11 = player.Player('Player 1', 1, floor=70, ceiling=90)
    p12 = player.Player('Player 2', 2, floor=70, ceiling=90)
    p13 = player.Player('Player 3', 3, floor=70, ceiling=90)
    p14 = player.Player('Player 4', 4, floor=70, ceiling=90)
    p15 = player.Player('player 5', 5, floor=70, ceiling=90)

    t1 = team.Team('Simcoe Sabres', [p1, p2, p3, p4, p5])
    t2 = team.Team('McMaster Mauraduers', [p11, p12, p13, p14, p15])

    # Make both teams' PG's passers
    p1.o_tendencies['shoot_pass'] = 100
    p11.o_tendencies['shoot_pass'] = 100

    sim_game(t1, t2, pbp=True)
    #sim_season(t1, t2, games=82)


def sim_season(team1, team2, games=82):
    for i in range(games):
        game.game(team1, team2)

    for team in [team1, team2]:
        print ''
        print team.name
        name_width = max([len(p.name) for p in team.players])
        print '|        Name        | PPG  | ASS/G | FG%  | 3PT%  | FGA/G| TO/G | STL/G | BLK/G | REB/G |OREB/G |'
        print '--------------------------------------------------------------------------------------------------'
        for p in team.players:
            p.fga = p.fg2a + p.fg3a
            p.fgm = p.fg2m + p.fg3m
            ppg = '%.1f' % (float(p.points)/games)
            fg_string = '%.1f' % (100*float(p.fgm)/p.fga)
            fg3_string = '%.1f' % (100*float(p.fg3m)/p.fg3a)
            fgag = '%.1f' % (float(p.fga)/games)
            apg = '%2.1f' % (float(p.assists)/games)
            topg = '%.1f' % (float(p.turnovers)/games)
            spg = '%.1f' % (float(p.steals)/games)
            bpg = '%.1f' % (float(p.blocks)/games)
            rpg = '%.1f' % (float(p.rebounds)/games)
            orpg = '%.1f' % (float(p.off_rebounds)/games)
            print '|{0:<{n}}|{1:<{p}}|{2:<{f}}|{3:<{p}}|{4:<{f}}|{5:<{p}}|{6:<{p}}|{7:<{f}}|{8:<{f}}|{9:<{f}}|{10:<{f}}|'.format(p.name,
            ppg, apg, fg_string, fg3_string, fgag, topg, spg, bpg, rpg, orpg, n=20, p=6, f=7)

    print ''
    t1ppg = '%.1f' % (float(team1.season_points)/games)
    t2ppg = '%.1f' % (float(team2.season_points)/games)
    print '%s: %s-%s  -  %s PPG' % (team1.name, team1.wins, team1.losses, t1ppg)
    print '%s: %s-%s  -  %s PPG' % (team2.name, team2.wins, team2.losses, t2ppg)

def sim_game(team1, team2, pbp=False):
    quarters_played = game.game(team1, team2, pbp)

    for team in [team1, team2]:
        print ''
        print team.name
        name_width = max([len(p.name) for p in team.players])
        print '|        Name        |Pts|  FG  | 3PT | AST | TO  | STL | BLK | REB | OREB |'
        print '----------------------------------------------------------------------------'
        for p in team.players:
            p.fga = p.fg2a + p.fg3a
            p.fgm = p.fg2m + p.fg3m
            fg_string = '%s/%s' % (p.fgm, p.fga)
            fg3_string = '%s/%s' % (p.fg3m, p.fg3a)
            print '|{0:<{n}}|{1:<{p}}|{2:<{f}}|{3:<{t}}|{4:<{t}}|{5:<{t}}|{6:<{t}}|{7:<{t}}|{8:<{t}}|{9:<{f}}|'.format(p.name,
            p.points, fg_string, fg3_string, p.assists, p.turnovers, p.steals, p.blocks, p.rebounds, p.off_rebounds, n=20, p=3, f=6, t=5)

    print ''
    if quarters_played == 4:
        print 'FINAL SCORE'
    else:
        print 'FINAL SCORE (%sOT):' % (quarters_played - 4)
    print '%s: %s' % (team1.name, team1.points)
    print '%s: %s' % (team2.name, team2.points)


if __name__ == '__main__':
    main()