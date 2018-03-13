from nba_py import player
import plotly.offline as po
import plotly.graph_objs as pgo


def get_player_trend(pid, nb_games, name):

    total_fp = []
    game_n_fp = []

    for idx in range(nb_games, 0, -1):
        splits = player.PlayerGeneralSplits(pid, season="2017-18", measure_type="Base",
                                             last_n_games=idx, per_mode='Totals').overall()

        total_fp.append(splits['NBA_FANTASY_PTS'].values[0])

    for idx in range(0, nb_games - 1):
        game_n_fp.append(total_fp[idx] - total_fp[idx + 1])

    game_n_fp.append(total_fp[-1])

    print total_fp
    print game_n_fp

    trace = pgo.Scatter( x=range(nb_games, 0, -1),
                         y=game_n_fp,
                         mode='lines+markers')

    data = [trace]

    po.plot(data, filename='%s Trend.html' % name)


def get_deck_fp(deck):

    nb_games = 10

    # -----------------------------------------------------------------------------------------------

    pids = []
    names = []
    last_n_games_fp = []
    overall_fp = []
    overall_gp = []

    for first_name, last_name in deck:
        pid  = player.get_player(first_name, last_name, season="2017-18")
        pids.append(pid)

        info = player.PlayerSummary(pid).info()
        name = '%s %s' % (info['FIRST_NAME'].values[0], info['LAST_NAME'].values[0])
        names.append(name)

        last_splits =  player.PlayerGeneralSplits(pid, season="2017-18", measure_type="Base", last_n_games=nb_games).overall()
        last_n_games_fp.append(last_splits['NBA_FANTASY_PTS'].values[0])

        overall_splits =  player.PlayerGeneralSplits(pid, season="2017-18", measure_type="Base").overall()
        overall_fp.append(overall_splits['NBA_FANTASY_PTS'].values[0])
        overall_gp.append(overall_splits['GP'].values[0])

    trace1 = pgo.Bar(x=names, y=last_n_games_fp, name='last %d games fp avg' % nb_games)

    trace2 = pgo.Bar(x=names, y=overall_fp, name='season overall fp avg')

    data = [trace1, trace2]

    layout = pgo.Layout(barmode='group', xaxis=dict(tickangle=-45))

    fig = pgo.Figure(data=data, layout=layout)

    po.plot(fig, filename='grouped-bar.html')

    for pid, name in zip(pids, names):
        get_player_trend(pid, nb_games, name)

if __name__ == "__main__":
    # execute only if run as a script

    deck = [
        ["Chris", "Paul"],
        ["Anthony", "Davis"],
        ["Draymond", "Green"],
        ["Rudy", "Gobert"],
        ["DeMar", "DeRozan"],
        ["Karl-Anthony", "Towns"],
        ["Paul", "George"],
    ]

    get_deck_fp(deck)