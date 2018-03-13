from nba_py import player
import plotly.offline as po
import plotly.graph_objs as pgo


def get_player_trend(pid, nb_games, name):

    total_fp = []
    total_ttfl = []

    game_n_fp = []
    game_n_ttfl = []

    for idx in range(nb_games, 0, -1):
        splits = player.PlayerGeneralSplits(pid, season="2017-18", measure_type="Base",
                                             last_n_games=idx, per_mode='Totals').overall()

        total_fp.append(splits['NBA_FANTASY_PTS'].values[0])
        total_ttfl.append(get_ttfl_score(splits))

    for idx in range(0, nb_games - 1):
        game_n_fp.append(total_fp[idx] - total_fp[idx + 1])
        game_n_ttfl.append(total_ttfl[idx] - total_ttfl[idx + 1])

    game_n_fp.append(total_fp[-1])
    game_n_ttfl.append(total_ttfl[-1])

    trace1 = pgo.Scatter( x=range(0, nb_games),
                         y=game_n_fp,
                         mode='lines+markers',
                         name='nba fp trend')

    trace2 = pgo.Scatter( x=range(0, nb_games),
                         y=game_n_ttfl,
                         mode='lines+markers',
                         name='ttfl score trend')

    data = [trace1, trace2]

    po.plot(data, filename='%s Trend.html' % name)


def get_ttfl_score(splits):

    bonus = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'FGM', 'FG3M', 'FTM']
    malus = ['TOV', 'FGA', 'FG3A', 'FTA']

    ttfl_score = 0

    for cat in bonus:
        n = 1

        if (cat == 'FGM' or cat == 'FG3M' or cat == 'FTM'):
            n = 2

        ttfl_score = ttfl_score + n*splits[cat].values[0]

    for cat in malus:
        ttfl_score = ttfl_score - splits[cat].values[0]

    return ttfl_score

def get_deck_fp(deck):

    nb_games = 10

    # -----------------------------------------------------------------------------------------------

    pids = []
    names = []

    # ---

    last_n_games_fp = []
    last_n_games_ttfl_score = []

    overall_fp = []
    overall_gp = []
    overall_ttfl_score = []

    # ---

    for first_name, last_name in deck:
        pid  = player.get_player(first_name, last_name, season="2017-18")
        pids.append(pid)

        info = player.PlayerSummary(pid).info()
        name = '%s %s' % (info['FIRST_NAME'].values[0], info['LAST_NAME'].values[0])
        names.append(name)

        last_splits =  player.PlayerGeneralSplits(pid, season="2017-18", measure_type="Base", last_n_games=nb_games).overall()
        last_n_games_fp.append(last_splits['NBA_FANTASY_PTS'].values[0])

        last_n_games_ttfl_score.append(get_ttfl_score(last_splits))

        overall_splits =  player.PlayerGeneralSplits(pid, season="2017-18", measure_type="Base").overall()
        overall_fp.append(overall_splits['NBA_FANTASY_PTS'].values[0])
        overall_gp.append(overall_splits['GP'].values[0])

        overall_ttfl_score.append(get_ttfl_score(overall_splits))

    trace1 = pgo.Bar(x=names, y=last_n_games_fp, name='last %d games fp avg' % nb_games)

    trace2 = pgo.Bar(x=names, y=overall_fp, name='season overall fp avg')

    trace3 = pgo.Bar(x=names, y=last_n_games_ttfl_score, name='last %d games ttfl avg' % nb_games)

    trace4 = pgo.Bar(x=names, y=overall_ttfl_score, name='season overall ttfl avg')

    data = [trace1, trace2, trace3, trace4]

    layout = pgo.Layout(barmode='group', xaxis=dict(tickangle=-45))

    fig = pgo.Figure(data=data, layout=layout)

    po.plot(fig, filename='Deck Ratings.html')

    for pid, name in zip(pids, names):
        get_player_trend(pid, nb_games, name)

if __name__ == "__main__":
    # execute only if run as a script

    deck = [
        ["Anthony", "Davis"],
        # ["Russell", "Westbrook"],
        # ["James", "Harden"],
        # ["Kevin", "Durant"],
        # ["Giannis", "Antetokounmpo"],
    ]

    get_deck_fp(deck)