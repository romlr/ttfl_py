import nba_py as nba
import team

def get_day_games(date, nb_best_players):

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

        # get N best players from home team
        (ht_player_id, ht_player_name, ht_player_fp_avg, ht_player_ttfl_avg) = \
            team.get_team_best_rated_players(ht_id, nb_best_players)

        for (id, name, fp_avg, ttfl_avg) in zip(ht_player_id, ht_player_name, ht_player_fp_avg, ht_player_ttfl_avg):
            print "%s (TTFL:%.1f, NBA FP: %.1f)" % (name, ttfl_avg, fp_avg)

        print "vs."

        # get N best players from visitor team
        (vt_player_id, vt_player_name, vt_player_fp_avg, vt_player_ttfl_avg) = \
            team.get_team_best_rated_players(vt_id, nb_best_players)

        for (id, name, fp_avg, ttfl_avg) in zip(vt_player_id, vt_player_name, vt_player_fp_avg, vt_player_ttfl_avg):
            print "%s (TTFL:%.1f, NBA FP: %.1f)" % (name, ttfl_avg, fp_avg)

        print "----------"
