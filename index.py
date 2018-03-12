from nba_py import player

import plotly.offline as po
import plotly.graph_objs as pgo

def main():

    deck = [
        ["Chris", "Paul"],
        ["Ben", "Simmons"],
        ["Draymond", "Green"],
        ["Rudy", "Gobert"],
        ["DeMar", "DeRozan"],
        ["Karl-Anthony", "Towns"],
        ["Paul", "George"],
    ]

    last_n_games = 1

    # -----------------------------------------------------------------------------------------------

    names = []
    last_n_games_fp = []
    overall_fp = []
    overall_gp = []

    for first_name, last_name in deck:
        pid = player.get_player(first_name, last_name)

        info = player.PlayerSummary(pid).info()
        names.append("%s %s" % (info['FIRST_NAME'].values, info['LAST_NAME'].values))

        last_splits =  player.PlayerGeneralSplits(pid, season="2017-18", measure_type="Base", last_n_games=last_n_games).overall()
        last_n_games_fp.append(last_splits['NBA_FANTASY_PTS'].values)

        overall_splits =  player.PlayerGeneralSplits(pid, season="2017-18", measure_type="Base").overall()
        overall_fp.append(overall_splits['NBA_FANTASY_PTS'].values)
        overall_gp.append(overall_splits['GP'].values)


    print "FANTASY POINTS over %d last games / season overall (games played)" % last_n_games
    print "----------------------------------------------------------------"

    for idx in range(len(deck)):
        print "%s:  %.1f / %.1f (%d)" % (names[idx], last_n_games_fp[idx], overall_fp[idx], overall_gp[idx])

    # data = [pgo.Bar(
    #     x = names,
    #     y = last_n_games_fp
    # )]
    #
    # po.plot(data)


if __name__ == "__main__":
    # execute only if run as a script
    main()