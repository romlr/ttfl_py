import plotly.offline as po
import plotly.graph_objs as pgo

from nba_py import player as nba_player, constants as nba_constants
import score


def get_player_next_game(pid):

    # fetch next game from pid
    next_game = nba_player.PlayerProfile(pid).next_game()

    date = next_game['GAME_DATE'].values[0]
    player_team = next_game['PLAYER_TEAM_ABBREVIATION'].values[0]
    vs_team = next_game['VS_TEAM_ABBREVIATION'].values[0]
    location = next_game['LOCATION'].values[0]

    return (date, player_team, vs_team, location)


def get_player_log(_pid, _nb_games):

    games_logs = nba_player.PlayerGameLogs(_pid, season='2017-18').info()

    # ---
    game_matchup = []
    game_date = []
    game_fp = []
    game_ttfl = []

    idx = _nb_games-1
    while idx >= 0:
        game_matchup.append(games_logs['MATCHUP'].values[idx])
        game_date.append(games_logs['GAME_DATE'].values[idx])
        game_fp.append(score.get_fp_score(games_logs.iloc[[idx]]))
        game_ttfl.append(score.get_ttfl_score(games_logs.iloc[[idx]]))
        idx -= 1

    return (game_matchup, game_date, game_fp, game_ttfl)


def get_player_trend(_player, _nb_games):

    pid = _player['PLAYER_ID']
    name = _player['PLAYER_NAME']
    team = _player['TEAM_ABBR']
    last_n_games_fp_avg = _player['LAST_N_GAMES_NBA_FANTASY_PTS']
    last_n_games_ttfl_avg = _player['LAST_N_GAMES_TTFL_SCORE']
    ov_fp_avg = _player['NBA_FANTASY_PTS']
    ov_ttfl_avg = _player['TTFL_SCORE']
    ov_gp = _player['GP']

    PLAYER_HEADSHOT_URL = 'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/'
    PLAYER_HEADSHOT_EXT = '.png'

    TEAM_LOGO_URL = 'http://i.cdn.turner.com/nba/nba/.element/img/1.0/teamsites/logos/teamlogos_500x500/'
    TEAM_LOGO_EXT = '.png'

    # ---

    print "Fetching %s log..." % name

    (game_matchup, game_date, game_fp, game_ttfl) = get_player_log(pid, _nb_games)

    print "%s log fetched..." % name

    print "----------"

    # ---

    (ng_date, player_team, vs_team, location) = get_player_next_game(pid)
    if location == 'H':
        ng_matchup = 'vs.'
    else:
        ng_matchup = '@'

    ng_text = '%s <br> %s %s %s' % (ng_date, player_team, ng_matchup, vs_team)

    inj_status = _player['INJ_STATUS']
    if inj_status == 'True':
        injury_text = 'OUT (%s from %s)' % (_player['INJ_TYPE'], _player['INJ_DATE'])
    else:
        injury_text = ''

    # ---

    print "Tracing %s rating trend..." % name

    # trace plots for nba fp and ttfl score trends
    xaxis = []
    for (matchup, date) in zip(game_matchup, game_date):
        xaxis.append("%s %s" % (date, matchup))

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
        y=[last_n_games_fp_avg]*_nb_games,
        mode='lines',
        name='last %d games nba fp avg' % _nb_games,
        line = dict(
            dash='dash',
        ),
        hoverinfo='y'
    )

    trace4 = pgo.Scatter(
        x=xaxis,
        y=[last_n_games_ttfl_avg]*_nb_games,
        mode='lines',
        name='last %d games ttfl avg' % _nb_games,
        line = dict(
            dash='dash',
        ),
        hoverinfo='y'
    )

    trace5 = pgo.Scatter(
        x=xaxis,
        y=[ov_fp_avg]*_nb_games,
        mode='lines',
        name='overall season (%d) nba fp avg' % ov_gp,
        line = dict(
            dash='dash',
        ),
        hoverinfo='y'
    )

    trace6 = pgo.Scatter(
        x=xaxis,
        y=[ov_ttfl_avg]*_nb_games,
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
        titlefont=dict(
            size=18,
        ),
        xaxis=dict(
            tickangle=45,
        ),
        yaxis=dict(
            range= [0, 100],
        ),
        images=[
            dict(
                source=PLAYER_HEADSHOT_URL + str(pid) + PLAYER_HEADSHOT_EXT,
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
        legend=dict(
            x=0.8, y=1.05,
            font=dict(
                size=10,
            ),
            bordercolor='#000000',
            borderwidth=1
        ),
        annotations=pgo.Annotations([
            pgo.Annotation(
                xref='paper', yref='paper',
                x=0.2, y=1.0,
                showarrow=False,
                text='Next Game: %s' % ng_text,
            ),
            pgo.Annotation(
                xref='paper', yref='paper',
                x=0.5, y=1.0,
                showarrow=False,
                text=injury_text,
                font=dict(
                    size=12,
                    color='#D62728'
                ),
            ),
        ]),
    )

    fig = pgo.Figure(data=data, layout=layout)

    po.plot(fig, filename='%s Trend.html' % name)

    print "%s rating trend traced..." % name

    print "----------"
