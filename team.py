from nba_py import team as nba_team, constants as nba_constants

import score

def get_team_info(team_id):

    # get team info from team_id
    info = nba_team.TeamSummary(team_id, season='2017-18').info()

    abbr =  info['TEAM_ABBREVIATION'].values[0]
    conf =  info['TEAM_CONFERENCE'].values[0]
    rank =  info['CONF_RANK'].values[0]

    # return data
    return (abbr, conf, rank)


def get_team_best_rated_players(team_id, nb_players):

    players = nba_team.TeamPlayers(team_id).season_totals()

    players = players.sort_values('NBA_FANTASY_PTS', ascending=False)

    player_id = players['PLAYER_ID'].values[0:nb_players]
    player_name = players['PLAYER_NAME'].values[0:nb_players]
    player_fp_avg = players['NBA_FANTASY_PTS'].values[0:nb_players]

    player_ttfl_avg = []
    for idx in range(0,nb_players):
        player_ttfl_avg.append(score.get_ttfl_score(players.iloc[[idx]]))

    for (name, fp_avg, ttfl_avg) in zip(player_name, player_fp_avg, player_ttfl_avg):
        print "%s, FP: %.1f, TTFL: %.1f" % (name, fp_avg, ttfl_avg)

    return player_id
