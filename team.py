import pandas
from nba_py import team as nba_team, constants as nba_constants
import score
import injuries


def get_team_info(_team_id):

    # get team info from team_id
    info = nba_team.TeamSummary(_team_id, season='2017-18').info()

    # fetch data
    abbr =  info['TEAM_ABBREVIATION'].values[0]
    conf =  info['TEAM_CONFERENCE'].values[0]
    rank =  info['CONF_RANK'].values[0]

    # return data
    return (abbr, conf, rank)


def get_team_best_rated_players(_team_id, _team_abbr, _nb_players, _injuries_report, _season, _season_type):

    player_ttfl_avg = []

    player_injury_status = []
    player_injury_type = []
    player_injury_date = []

    player_team_id = []
    player_team_abbr = []

    # ---

    # get players splits from team_id
    players = nba_team.TeamPlayers(_team_id, season=_season, season_type=_season_type).season_totals()

    # parse players df rows
    for index, row in players.iterrows():
        # add player ttfl score to list
        player_ttfl_avg.append(score.get_ttfl_score(players.iloc[[index]]))

        # add player injury status to list
        empty, info = injuries.check_player_injury(row['PLAYER_NAME'], _injuries_report)
        if not empty:
            player_injury_status.append('True')
            player_injury_type.append(info['Type'].values[0])
            player_injury_date.append(info['Date'].values[0])
        else:
            player_injury_status.append('False')
            player_injury_type.append('')
            player_injury_date.append('')

        # add player team id and abbr to list
        player_team_id.append(_team_id)
        player_team_abbr.append(_team_abbr)

    # add new series to players splits
    players['TTFL_SCORE'] = pandas.Series(player_ttfl_avg, index=players.index)
    players['INJ_STATUS'] = pandas.Series(player_injury_status, index=players.index)
    players['INJ_TYPE'] = pandas.Series(player_injury_type, index=players.index)
    players['INJ_DATE'] = pandas.Series(player_injury_date, index=players.index)
    players['TEAM_ID'] = pandas.Series(player_team_id, index=players.index)
    players['TEAM_ABBR'] = pandas.Series(player_team_abbr, index=players.index)

    # sort players splits per descending ttfl score
    players = players.sort_values('TTFL_SCORE', ascending=False)

    # fetch best N players from players splits
    players = players[0:_nb_players]

    # return data
    return players