import plotly.offline as po
import plotly.graph_objs as pgo

from nba_py import player as nba_player
import player, score


def plot_deck_ratings(names, last_n_games_fp, last_n_games_ttfl_score, nb_games, overall_fp, overall_ttfl_score):

    # logos url constants
    NBA_LOGO_URL = 'https://secure.nba.com/assets/amp/include/images/nba-logo.png'
    TTFL_LOGO_URL = 'http//fantasy.trashtalk.co/images/logo.png'

    # trace bars representing last n games and overall season nba fp and ttfl ratings
    trace1 = pgo.Bar(
        x=names,
        y=last_n_games_fp,
        name='last %d games nba fp avg' % nb_games,
        hoverinfo='y'
    )

    trace2 = pgo.Bar(
        x=names,
        y=last_n_games_ttfl_score,
        name='last %d games ttfl avg' % nb_games,
        hoverinfo='y'
    )

    trace3 = pgo.Bar(
        x=names,
        y=overall_fp,
        name='overall season nba fp avg',
        hoverinfo='y'
    )

    trace4 = pgo.Bar(
        x=names,
        y=overall_ttfl_score,
        name='overall season ttfl avg',
        hoverinfo='y'
    )

    data = [trace1, trace2, trace3, trace4]

    layout = pgo.Layout(
        title= 'Deck Ratings',
        barmode='group',
        xaxis= dict(
            title= 'Player',
        ),
        yaxis=dict(
            title='Score',
        ),
    )

    fig = pgo.Figure(data=data, layout=layout)

    po.plot(fig, filename='Deck Ratings.html')


def get_deck_ratings(deck, nb_games):

    pids = []
    names = []
    teams = []

    # ---

    last_n_games_fp = []
    last_n_games_ttfl_score = []

    overall_fp = []
    overall_gp = []
    overall_ttfl_score = []

    # ---

    # iterate through deck and fetch first and last name
    for first_name, last_name in deck:

        # fetch player id for each player based on first and last name
        pid  = nba_player.get_player(first_name, last_name, season="2017-18")
        pids.append(pid)

        # fetch player names from info summary - TODO: add player summary, photo, etc.
        info = nba_player.PlayerSummary(pid).info()
        name = '%s %s' % (info['FIRST_NAME'].values[0], info['LAST_NAME'].values[0])
        names.append(name)
        team = info['TEAM_ABBREVIATION'].values[0]
        teams.append(team)

        # fetch player splits for last N games (passed as parameter)
        last_splits =  nba_player.PlayerGeneralSplits(pid, season="2017-18", measure_type="Base", last_n_games=nb_games).overall()

        # fetch nba fp from splits
        last_n_games_fp.append(last_splits['NBA_FANTASY_PTS'].values[0])

        # calculate ttfl score from splits
        last_n_games_ttfl_score.append(score.get_ttfl_score(last_splits))

        # fetch player splits for overall season
        overall_splits =  nba_player.PlayerGeneralSplits(pid, season="2017-18", measure_type="Base").overall()

        # fetch nba fp and games played from splits
        overall_fp.append(overall_splits['NBA_FANTASY_PTS'].values[0])
        overall_gp.append(overall_splits['GP'].values[0])

        # calculate ttfl score from splits
        overall_ttfl_score.append(score.get_ttfl_score(overall_splits))

    # ---

    plot_deck_ratings(names, last_n_games_fp, last_n_games_ttfl_score, nb_games, overall_fp, overall_ttfl_score)

    # ---

    # iterate through player ids
    for (pid, name, team, av_n_fp, av_n_ttfl, av_ov_fp, av_ov_ttfl, ov_gp) in zip(pids,
                                                                    names,
                                                                    teams,
                                                                    last_n_games_fp,
                                                                    last_n_games_ttfl_score,
                                                                    overall_fp,
                                                                    overall_ttfl_score,
                                                                    overall_gp):

        # get player trend for last nb games
        player.get_player_trend(pid, name, team, av_n_fp, av_n_ttfl, nb_games, av_ov_fp, av_ov_ttfl, ov_gp)
