import pandas


def fetch_injuries_report(_path):

    # TODO csv automatic fetch from bbreference

    # read from csv file
    injuries_report = pandas.read_csv(_path)

    # remove bbreference player IDs
    for index, row in injuries_report.iterrows():
        row['Player'] = row['Player'].split('\\')[0]

    # return dataframe
    return injuries_report


def check_player_injury(_player, _injuries_report):

    # check player injury status
    player_injury = _injuries_report.loc[_injuries_report['Player'] == _player]

    # return status and injury info dataframe
    return player_injury.empty, player_injury


def check_team_injuries(_team, _injuries_report):

    # check player injury status
    team_injuries = _injuries_report.loc[_injuries_report['Team'] == _team]

    # return status and injury info dataframe
    return team_injuries.empty, team_injuries
