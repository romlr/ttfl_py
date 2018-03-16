import pandas

from nba_py import team as nba_team, constants as nba_constants

import score

def get_team_info(team_id):

    # get team info from team_id
    info = nba_team.TeamSummary(team_id, season='2017-18').info()

    # fetch data
    abbr =  info['TEAM_ABBREVIATION'].values[0]
    conf =  info['TEAM_CONFERENCE'].values[0]
    rank =  info['CONF_RANK'].values[0]

    # return data
    return (abbr, conf, rank)


def get_team_best_rated_players(team_id, nb_players):

    player_ttfl_avg = []

    # ---

    # get players splits from team_id
    players = nba_team.TeamPlayers(team_id).season_totals()

    # parse results to calculate ttfl score list
    for index, row in players.iterrows():
        player_ttfl_avg.append(score.get_ttfl_score(players.iloc[[index]]))

    # add ttfl score list to players splits
    players['TTFL_SCORE'] = pandas.Series(player_ttfl_avg, index=players.index)

    # sort players splits per descending ttfl score
    players = players.sort_values('TTFL_SCORE', ascending=False)

    # fetch best N players from players splits
    player_ttfl_avg = players['TTFL_SCORE'].values[0:nb_players]
    player_id = players['PLAYER_ID'].values[0:nb_players]
    player_name = players['PLAYER_NAME'].values[0:nb_players]
    player_fp_avg = players['NBA_FANTASY_PTS'].values[0:nb_players]

    # return data
    return (player_id, player_name, player_fp_avg, player_ttfl_avg)
