from nba_py import player
import plotly.offline as po
import plotly.graph_objs as pgo


def get_player_trend(pid, nb_games, name, av_n_fp, av_n_ttfl, av_ov_fp, av_ov_ttfl):

    total_fp = []
    total_ttfl = []

    game_n_fp = []
    game_n_ttfl = []

    # ---

    # fetch players splits (totals) for each game
    for idx in range(nb_games, 0, -1):
        splits = player.PlayerGeneralSplits(pid, season="2017-18", measure_type="Base",
                                             last_n_games=idx, per_mode='Totals').overall()

        # get nba fantasy points and calculate ttfl score
        total_fp.append(splits['NBA_FANTASY_PTS'].values[0])
        total_ttfl.append(get_ttfl_score(splits))

    # calculate individual game splits for each game based on totals fetched
    for idx in range(0, nb_games - 1):
        game_n_fp.append(total_fp[idx] - total_fp[idx + 1])
        game_n_ttfl.append(total_ttfl[idx] - total_ttfl[idx + 1])

    # add latests game splits
    game_n_fp.append(total_fp[-1])
    game_n_ttfl.append(total_ttfl[-1])

    # ---

    # trace plots for nba fp and ttfl score trends
    xaxis = []
    for n in range(nb_games, 0, -1):
        xaxis.append("N - %d" % n)

    trace1 = pgo.Scatter(
        x=xaxis,
        y=game_n_fp,
        mode='lines+markers',
        name='nba fp trend',
        line=dict(
            shape='spline',
        )
    )

    trace2 = pgo.Scatter(
        x=xaxis,
        y=game_n_ttfl,
        mode='lines+markers',
        name='ttfl score trend',
        line = dict(
            shape='spline',
        )
    )

    trace3 = pgo.Scatter(
        x=xaxis,
        y=[av_n_fp]*nb_games,
        mode='lines',
        name='last %d games nba fp avg' % nb_games,
        line = dict(
            dash='dash',
        )
    )

    trace4 = pgo.Scatter(
        x=xaxis,
        y=[av_n_ttfl]*nb_games,
        mode='lines',
        name='last %d games ttfl avg' % nb_games,
        line = dict(
            dash='dash',
        )
    )

    trace5 = pgo.Scatter(
        x=xaxis,
        y=[av_ov_fp]*nb_games,
        mode='lines',
        name='overall season nba fp avg',
        line = dict(
            dash='dash',
        )
    )

    trace6 = pgo.Scatter(
        x=xaxis,
        y=[av_ov_ttfl]*nb_games,
        mode='lines',
        name='overall season ttfl avg',
        line = dict(
            dash='dash',
        )
    )

    data = [trace1, trace2, trace3, trace4, trace5, trace6]

    layout = pgo.Layout(
        title= '%s Rating Trend' % name,
        xaxis= dict(
            title= 'Games',
        ),
        yaxis=dict(
            title='Score',
            range= [0, 100],
        ),
    )

    fig = pgo.Figure(data=data, layout=layout)

    po.plot(fig, filename='%s Trend.html' % name)


def get_ttfl_score(splits):

    # tables containing stats categories used for ttfl score calculation
    bonus = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'FGM', 'FG3M', 'FTM']
    malus = ['TOV', 'FGA', 'FG3A', 'FTA']

    # init ttfl score to zero
    ttfl_score = 0

    # calculate bonus part (PTS + REB + AST + STL + BLK + 2*FGM + 2*FGM3 + 2*FTM)
    for cat in bonus:
        n = 1

        if (cat == 'FGM' or cat == 'FG3M' or cat == 'FTM'):
            n = 2

        ttfl_score = ttfl_score + n*splits[cat].values[0]

    # remove malus part from score (- TOV - FGA - FG3A - FTA)
    for cat in malus:
        ttfl_score = ttfl_score - splits[cat].values[0]

    # return calculated score
    return ttfl_score


def get_deck_ratings(deck, nb_games):

    pids = []
    names = []

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
        pid  = player.get_player(first_name, last_name, season="2017-18")
        pids.append(pid)

        # fetch player names from info summary - TODO: add player summary, photo, etc.
        info = player.PlayerSummary(pid).info()
        name = '%s %s' % (info['FIRST_NAME'].values[0], info['LAST_NAME'].values[0])
        names.append(name)

        # fetch player splits for last N games (passed as parameter)
        last_splits =  player.PlayerGeneralSplits(pid, season="2017-18", measure_type="Base", last_n_games=nb_games).overall()

        # fetch nba fp from splits
        last_n_games_fp.append(last_splits['NBA_FANTASY_PTS'].values[0])

        # calculate ttfl score from splits
        last_n_games_ttfl_score.append(get_ttfl_score(last_splits))

        # fetch player splits for overall season
        overall_splits =  player.PlayerGeneralSplits(pid, season="2017-18", measure_type="Base").overall()

        # fetch nba fp and games played from splits
        overall_fp.append(overall_splits['NBA_FANTASY_PTS'].values[0])
        overall_gp.append(overall_splits['GP'].values[0])

        # calculate ttfl score from splits
        overall_ttfl_score.append(get_ttfl_score(overall_splits))

    # ---

    # trace bars representing last n games and overall season nba fp and ttfl ratings
    trace1 = pgo.Bar(x=names, y=last_n_games_fp, name='last %d games nba fp avg' % nb_games)

    trace2 = pgo.Bar(x=names, y=last_n_games_ttfl_score, name='last %d games ttfl avg' % nb_games)

    trace3 = pgo.Bar(x=names, y=overall_fp, name='overall season nba fp avg')

    trace4 = pgo.Bar(x=names, y=overall_ttfl_score, name='overall season ttfl avg')

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

    # iterate through player ids
    for (pid, name, av_n_fp, av_n_ttfl, av_ov_fp, av_ov_ttfl) in zip(pids,
                                                                    names,
                                                                    last_n_games_fp,
                                                                    last_n_games_ttfl_score,
                                                                    overall_fp,
                                                                    overall_ttfl_score):

        # get player trend for last nb games
        get_player_trend(pid, nb_games, name, av_n_fp, av_n_ttfl, av_ov_fp, av_ov_ttfl)


if __name__ == "__main__":
    # execute only if run as a script

    DECK = [
        ["Chris", "Paul"],
        ["Anthony", "Davis"],
        ["Khris", "Middleton"],
        ["Rudy", "Gobert"],
        ["Ben", "Simmons"],
        ["Karl-Anthony", "Towns"],
        ["DeMar", "DeRozan"],
    ]

    NB_GAMES = 10

    get_deck_ratings(DECK, NB_GAMES)
