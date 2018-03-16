import plotly.offline as po
import plotly.graph_objs as pgo

from nba_py import player as nba_player, constants as nba_constants

import score


def get_player_log(pid, nb_games):

    games_logs = nba_player.PlayerGameLogs(pid, season='2017-18').info()

    # ---
    game_matchup = []
    game_date = []
    game_fp = []
    game_ttfl = []

    idx = nb_games-1
    while idx >= 0:
        game_matchup.append(games_logs['MATCHUP'].values[idx])
        game_date.append(games_logs['GAME_DATE'].values[idx])
        game_fp.append(score.get_fp_score(games_logs.iloc[[idx]]))
        game_ttfl.append(score.get_ttfl_score(games_logs.iloc[[idx]]))
        idx -= 1

    return (game_matchup, game_date, game_fp, game_ttfl)


def get_player_trend(pid, name, team, av_n_fp, av_n_ttfl, nb_games, av_ov_fp, av_ov_ttfl, ov_gp):

    PLAYER_HEADSHOT_URL = 'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/'
    PLAYER_HEADSHOT_EXT = '.png'

    TEAM_LOGO_URL = 'http://i.cdn.turner.com/nba/nba/.element/img/1.0/teamsites/logos/teamlogos_500x500/'
    TEAM_LOGO_EXT = '.png'

    # ---

    (game_matchup, game_date, game_fp, game_ttfl) = get_player_log(pid, nb_games)

    # ---

    # trace plots for nba fp and ttfl score trends
    xaxis = []
    for (matchup, date) in zip(game_matchup, game_date):
        xaxis.append("%s<br>%s" % (date, matchup))

    trace1 = pgo.Scatter(
        x=xaxis,
        y=game_fp,
        mode='lines+markers',
        name='nba fp trend',
        line=dict(
            shape='spline',
        ),
        hoverinfo='y'
    )

    trace2 = pgo.Scatter(
        x=xaxis,
        y=game_ttfl,
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
        name='overall season (%d) nba fp avg' % ov_gp,
        line = dict(
            dash='dash',
        ),
        hoverinfo='y'
    )

    trace6 = pgo.Scatter(
        x=xaxis,
        y=[av_ov_ttfl]*nb_games,
        mode='lines',
        name='overall season (%d) ttfl avg' % ov_gp,
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
                source=TEAM_LOGO_URL + team.lower() + TEAM_LOGO_EXT,
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                sizex=1, sizey=1,
                xanchor="center", yanchor="middle",
                opacity=0.2,
                layer="below",
            ),
        ],
    )

    fig = pgo.Figure(data=data, layout=layout)

    po.plot(fig, filename='%s Trend.html' % name)
