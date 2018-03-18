import pandas
import nba_py as nba
import team


def print_best_rated_players(players, nb_players):

    name = players['PLAYER_NAME'].values
    ttfl_avg = players['TTFL_SCORE'].values
    fp_avg = players['NBA_FANTASY_PTS'].values

    for i in range(0, nb_players):
        print "%s (TTFL:%.1f, NBA FP: %.1f)" % (name[i], ttfl_avg[i], fp_avg[i])


def get_day_games(date, nb_players, nb_shorlist):

    # init shortlist
    shortlist = pandas.DataFrame()

    # get scoreboard for specified date
    games = nba.Scoreboard(date.month, date.day, date.year).game_header()

    # fetch teams IDs for home and visitors
    home_teams = games['HOME_TEAM_ID'].values
    visitor_teams = games['VISITOR_TEAM_ID'].values

    print date
    print "----------"

    # iterate through home and visitor teams IDs lists
    for ht_id, vt_id in zip(home_teams, visitor_teams):

        # get teams infos
        (ht_abbr, ht_conf, ht_rank) = team.get_team_info(ht_id)
        (vt_abbr, vt_conf, vt_rank) = team.get_team_info(vt_id)

        print "%s (%d) vs. %s (%d)" % (ht_abbr, ht_rank, vt_abbr, vt_rank)

        print "----------"

        # fetch and print N best players from home team
        ht_players = team.get_team_best_rated_players(ht_id, nb_players)
        print_best_rated_players(ht_players, nb_players)

        print "vs."

        # fetch and print N best players from visitor team
        vt_players = team.get_team_best_rated_players(vt_id, nb_players)
        print_best_rated_players(vt_players, nb_players)

        print "----------"

        shortlist = shortlist.append(ht_players)
        shortlist = shortlist.append(vt_players)

    shortlist = shortlist.sort_values('TTFL_SCORE', ascending=False)[0:nb_shorlist]

    return shortlist
