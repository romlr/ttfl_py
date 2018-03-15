import plotly.offline as po
import plotly.graph_objs as pgo

from nba_py import player as nba_player
import score


def get_player_trend(pid, name, team, av_n_fp, av_n_ttfl, av_ov_fp, av_ov_ttfl, nb_games):

    total_fp = []
    total_ttfl = []

    game_n_fp = []
    game_n_ttfl = []

    PLAYER_HEADSHOT_URL = 'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/'
    PLAYER_HEADSHOT_EXT = '.png'

    TEAM_LOGO_URL = 'https://i.cdn.turner.com/nba/nba/.element/media/2.0/teamsites/lakers/images/gameday/NBA_logos/'
    TEAM_LOGO_EXT = '.png'

    # ---

    # fetch players splits (totals) for each game
    for idx in range(nb_games, 0, -1):
        splits = nba_player.PlayerGeneralSplits(pid, season="2017-18", measure_type="Base",
                                             last_n_games=idx, per_mode='Totals').overall()

        # get nba fantasy points and calculate ttfl score
        total_fp.append(splits['NBA_FANTASY_PTS'].values[0])
        total_ttfl.append(score.get_ttfl_score(splits))

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
        ),
        hoverinfo='y'
    )

    trace2 = pgo.Scatter(
        x=xaxis,
        y=game_n_ttfl,
        mode='lines+markers',
        name='ttfl score trend',
        line = dict(
            shape='spline',
        ),
        hoverinfo='y'
    )

    trace3 = pgo.Scatter(
        x=xaxis,
        y=[av_n_fp]*nb_games,
        mode='lines',
        name='last %d games nba fp avg' % nb_games,
        line = dict(
            dash='dash',
        ),
        hoverinfo='y'
    )

    trace4 = pgo.Scatter(
        x=xaxis,
        y=[av_n_ttfl]*nb_games,
        mode='lines',
        name='last %d games ttfl avg' % nb_games,
        line = dict(
            dash='dash',
        ),
        hoverinfo='y'
    )

    trace5 = pgo.Scatter(
        x=xaxis,
        y=[av_ov_fp]*nb_games,
        mode='lines',
        name='overall season nba fp avg',
        line = dict(
            dash='dash',
        ),
        hoverinfo='y'
    )

    trace6 = pgo.Scatter(
        x=xaxis,
        y=[av_ov_ttfl]*nb_games,
        mode='lines',
        name='overall season ttfl avg',
        line = dict(
            dash='dash',
        ),
        hoverinfo='y'
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
        images=[
            dict(
                source=PLAYER_HEADSHOT_URL + str(pid.values[0]) + PLAYER_HEADSHOT_EXT,
                xref="paper", yref="paper",
                x=0.1, y=1.1,
                sizex=0.25, sizey=0.25,
                xanchor="center", yanchor="top",
                layer = "below",
    ),
            dict(
                source=TEAM_LOGO_URL + team + TEAM_LOGO_EXT,
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                sizex=0.5, sizey=0.5,
                xanchor="center", yanchor="middle",
                opacity=0.2,
                layer="below",
            ),
        ],
    )

    fig = pgo.Figure(data=data, layout=layout)

    po.plot(fig, filename='%s Trend.html' % name)
