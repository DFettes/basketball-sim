import player
import team
import game
import random

def main():
    p1 = player.Player('Kyle Lowry', 1, floor=70, ceiling=80)
    p2 = player.Player('DeMar DeRozan', 2, floor=70, ceiling=80)
    p3 = player.Player('James Johnson', 3, floor=70, ceiling=80)
    p4 = player.Player('Amir Johnson', 4, floor=70, ceiling=80)
    p5 = player.Player('Jonas Valanciunas', 5, floor=70, ceiling=80)
    p6 = player.Player('Lou Williams', 1, floor=70, ceiling=80)
    p7 = player.Player('Terrence Ross', 2, floor=70, ceiling=80)
    p8 = player.Player('Bruno Caboclo', 3, floor=70, ceiling=80)
    p9 = player.Player('Patrick Patterson', 4, floor=70, ceiling=80)
    p10 = player.Player('Chuck Hayes', 5, floor=70, ceiling=80)

    p11 = player.Player('Sam Baskerville', 1, floor=70, ceiling=80)
    p12 = player.Player('Brendan Tracey', 2, floor=70, ceiling=80)
    p13 = player.Player('Connor Petterson', 3, floor=70, ceiling=80)
    p14 = player.Player('Dan Fettes', 4, floor=90, ceiling=100)
    p15 = player.Player('Rick Nydam', 5, floor=70, ceiling=80)
    p16 = player.Player('James Tran', 1, floor=70, ceiling=80)
    p17 = player.Player('Brett Mitchell', 2, floor=70, ceiling=80)
    p18 = player.Player('David Teichrobe', 3, floor=70, ceiling=80)
    p19 = player.Player('Mike North', 4, floor=70, ceiling=80)
    p20 = player.Player('Logan Earnst', 5, floor=70, ceiling=80)

    t1 = team.Team('Toronto Raptors', [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10])
    t2 = team.Team('Simcoe Sabres', [p11, p12, p13, p14, p15, p16, p17, p18, p19, p20])

    sim_game(t1, t2, pbp=False)
    #sim_season(t1, t2, games=82)


def sim_season(team1, team2, games=82):
    for i in range(games):
        game.game(team1, team2)

    for team in [team1, team2]:
        print ''
        print team.name
        name_width = max([len(p.name) for p in team.players])
        print '|        Name        | PPG  | ASS/G | FG%  | 3PT%  | FGA/G| TO/G | STL/G | BLK/G | REB/G |OREB/G | MIN/G |'
        print '----------------------------------------------------------------------------------------------------------'
        for p in team.players:
            p.fga = p.fg2a + p.fg3a
            p.fgm = p.fg2m + p.fg3m
            ppg = '%.1f' % (float(p.points)/games)
            fg_string = '%.1f' % (100*float(p.fgm)/p.fga)
            try:
                fg3_string = '%.1f' % (100*float(p.fg3m)/p.fg3a)
            except:
                fg3_string = '0.0'
            fgag = '%.1f' % (float(p.fga)/games)
            apg = '%2.1f' % (float(p.assists)/games)
            topg = '%.1f' % (float(p.turnovers)/games)
            spg = '%.1f' % (float(p.steals)/games)
            bpg = '%.1f' % (float(p.blocks)/games)
            rpg = '%.1f' % (float(p.rebounds)/games)
            orpg = '%.1f' % (float(p.off_rebounds)/games)
            avg_secs = p.time_played.total_seconds()/games
            hours, remainder = divmod(avg_secs, 3600)
            minutes, seconds = divmod(remainder, 60)
            minutes = '%02d' % minutes
            seconds = '%02d' % seconds
            mpg = '%s:%s' % (minutes, seconds)
            print '|{0:<{n}}|{1:<{p}}|{2:<{f}}|{3:<{p}}|{4:<{f}}|{5:<{p}}|{6:<{p}}|{7:<{f}}|{8:<{f}}|{9:<{f}}|{10:<{f}}|{11:<{f}}|'.format(p.name,
            ppg, apg, fg_string, fg3_string, fgag, topg, spg, bpg, rpg, orpg, mpg, n=20, p=6, f=7)

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
        print '|        Name        |Pts|  FG  | 3PT | AST | TO  | STL | BLK | REB | OREB | MINS |'
        print '----------------------------------------------------------------------------------'
        for p in team.players:
            p.fga = p.fg2a + p.fg3a
            p.fgm = p.fg2m + p.fg3m
            fg_string = '%s/%s' % (p.fgm, p.fga)
            fg3_string = '%s/%s' % (p.fg3m, p.fg3a)
            print '|{0:<{n}}|{1:<{p}}|{2:<{f}}|{3:<{t}}|{4:<{t}}|{5:<{t}}|{6:<{t}}|{7:<{t}}|{8:<{t}}|{9:<{f}}|{10:<{f}}|'.format(p.name,
            p.points, fg_string, fg3_string, p.assists, p.turnovers, p.steals, p.blocks, p.rebounds, p.off_rebounds, p.time_played, n=20, p=3, f=6, t=5)

    print ''
    if quarters_played == 4:
        print 'FINAL SCORE'
    else:
        print 'FINAL SCORE (%sOT):' % (quarters_played - 4)
    print '%s: %s' % (team1.name, team1.points)
    print '%s: %s' % (team2.name, team2.points)


if __name__ == '__main__':
    main()