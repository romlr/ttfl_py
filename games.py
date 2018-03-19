import pandas
import nba_py as nba
import team
import injuries


def get_injuries_report():

    # local csv file
    PATH = './injuries.csv'

    # fetch up to date injuries report
    injuries_report = injuries.fetch_injuries_report(PATH)

    # return injuries report
    return injuries_report


def print_players(_players, _nb_players, _injuries_report):

    name = _players['PLAYER_NAME'].values
    ttfl_avg = _players['TTFL_SCORE'].values
    fp_avg = _players['NBA_FANTASY_PTS'].values

    for i in range(0, _nb_players):
        status, info =  injuries.check_player_injury(name[i], _injuries_report)

        if not status:
            type = info['Type'].values[0]
            date = info['Date'].values[0]
            injury_status = ' - OUT (%s from %s)' % (type, date)
        else:
            injury_status = ''

        print "%s (TTFL:%.1f, NBA FP: %.1f)%s" % (name[i], ttfl_avg[i], fp_avg[i], injury_status)


def get_day_games(date, nb_players, nb_shorlist):

    # init shortlist
    shortlist = pandas.DataFrame()

    # get scoreboard for specified date
    games = nba.Scoreboard(date.month, date.day, date.year).game_header()

    # fetch teams IDs for home and visitors
    home_teams = games['HOME_TEAM_ID'].values
    visitor_teams = games['VISITOR_TEAM_ID'].values

    # fetch injuries report
    injuries_report = get_injuries_report()

    # ---

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
        ht_br_players = team.get_team_best_rated_players(ht_id, nb_players)
        print_players(ht_br_players, nb_players, injuries_report)

        print "vs."

        # fetch and print N best players from visitor team
        vt_br_players = team.get_team_best_rated_players(vt_id, nb_players)
        print_players(vt_br_players, nb_players, injuries_report)

        print "----------"

        shortlist = shortlist.append(ht_br_players)
        shortlist = shortlist.append(vt_br_players)

    print "SHORTLIST"
    print "----------"

    shortlist = shortlist.sort_values('TTFL_SCORE', ascending=False)[0:nb_shorlist]
    print_players(shortlist, nb_shorlist, injuries_report)

    print "----------"

    return shortlist
