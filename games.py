import nba_py as nba
import team

def get_day_games(date):

    NB_PLAYERS = 3

    games = nba.Scoreboard(date.month, date.day, date.year).game_header()

    home_teams = games['HOME_TEAM_ID'].values
    vs_teams = games['VISITOR_TEAM_ID'].values

    print date
    print "----------"

    for ht_id, vt_id in zip(home_teams, vs_teams):

        (ht_abbr, ht_conf, ht_rank) = team.get_team_info(ht_id)
        (vt_abbr, vt_conf, vt_rank) = team.get_team_info(vt_id)

        print "%s (%d) vs. %s (%d)" % (ht_abbr, ht_rank, vt_abbr, vt_rank)

        print "----------"

        team.get_team_best_rated_players(ht_id, NB_PLAYERS)

        print "vs."

        team.get_team_best_rated_players(vt_id, NB_PLAYERS)

        print "----------"
