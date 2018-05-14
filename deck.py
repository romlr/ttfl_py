import plotly.offline as po
import plotly.graph_objs as pgo
import pandas
from nba_py import player as nba_player, constants as nba_constants
import player, score


def plot_deck_ratings(_deck, _nb_games):

    # trace bars representing last n games and overall season nba fp and ttfl ratings
    trace1 = pgo.Bar(
        x=_deck['LAST_N_GAMES_NBA_FANTASY_PTS'],
        y=_deck['PLAYER_NAME'],
        name='last %d games nba fp avg' % _nb_games,
        hoverinfo='x',
        orientation='h'
    )

    trace2 = pgo.Bar(
        x=_deck['LAST_N_GAMES_TTFL_SCORE'],
        y=_deck['PLAYER_NAME'],
        name='last %d games ttfl avg' % _nb_games,
        hoverinfo='x',
        orientation='h'
    )

    trace3 = pgo.Bar(
        x=_deck['NBA_FANTASY_PTS'],
        y=_deck['PLAYER_NAME'],
        name='overall season nba fp avg',
        hoverinfo='x',
        orientation='h'
    )

    trace4 = pgo.Bar(
        x=_deck['TTFL_SCORE'],
        y=_deck['PLAYER_NAME'],
        name='overall season ttfl avg',
        hoverinfo='x',
        orientation='h'
    )

    data = [trace1, trace2, trace3, trace4]

    layout = pgo.Layout(
        title= 'Deck Ratings',
        barmode='group',
    )

    fig = pgo.Figure(data=data, layout=layout)

    po.plot(fig, filename='Deck Ratings.html')


def get_deck_ratings(_deck, _nb_games, _plot_trends, _season, _season_type):

    last_n_games_fp_avg = []
    last_n_games_ttfl_avg = []

    # ---

    print "Fetching deck ratings..."

    # iterate through deck and fetch first and last name
    pids = _deck['PLAYER_ID'].values
    names = _deck['PLAYER_NAME'].values

    for pid, name in zip(pids, names):

        # fetch player splits for last N games (passed as parameter)
        last_splits = nba_player.PlayerGeneralSplits(pid, last_n_games=_nb_games, season_type=_season_type).overall()

        # fetch nba fp from splits
        try:
            last_n_games_fp_avg.append(last_splits['NBA_FANTASY_PTS'].values[0])
        except IndexError:
            last_n_games_fp_avg.append(0.0)

        # calculate ttfl score from splits
        last_n_games_ttfl_avg.append(score.get_ttfl_score(last_splits))

    _deck['LAST_N_GAMES_NBA_FANTASY_PTS'] = pandas.Series(last_n_games_fp_avg, index=_deck.index)
    _deck['LAST_N_GAMES_TTFL_SCORE'] = pandas.Series(last_n_games_ttfl_avg, index=_deck.index)

    print "Deck ratings fetched..."

    print "----------"

    # ---

    print "Tracing deck ratings..."

    plot_deck_ratings(_deck, _nb_games)

    print "Deck ratings traced..."

    print "----------"

    # ---

    if _plot_trends:
        # iterate through player deck
        for index, row in _deck.iterrows():
            player.get_player_trend(row, _nb_games, _season, _season_type)

        # for (pid, name, team, last_n_fp_avg, last_n_ttfl_avg, ov_fp_avg, ov_ttfl_avg, ov_gp) in zip(pids,
        #                                                                                             names,
        #                                                                                             teams,
        #                                                                                             last_n_games_fp_avg,
        #                                                                                             last_n_games_ttfl_avg,
        #                                                                                             overall_fp_avg,
        #                                                                                             overall_ttfl_avg,
        #                                                                                             overall_gp):
        #
        #     # get player trend for last nb games
        #     player.get_player_trend(pid, name, team, last_n_fp_avg, last_n_ttfl_avg, _nb_games, ov_fp_avg, ov_ttfl_avg, ov_gp)
