from nba_py import player


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

    print "FANTASY POINTS over %d last games / season overall (games played)" % last_n_games
    print "----------------------------------------------------------------"

    for first_name, last_name in deck:
        pid = player.get_player(first_name, last_name)

        info = player.PlayerSummary(pid).info()
        name = info['FIRST_NAME'].values + " " + info['LAST_NAME'].values

        last_splits =  player.PlayerGeneralSplits(pid, season="2017-18", measure_type="Base", last_n_games=last_n_games).overall()
        last_n_games_fp = last_splits['NBA_FANTASY_PTS'].values

        overall_splits =  player.PlayerGeneralSplits(pid, season="2017-18", measure_type="Base").overall()
        overall_fp = overall_splits['NBA_FANTASY_PTS'].values
        overall_gp = overall_splits['GP'].values

        print "%s:  %.1f / %.1f (%d)" % (name[0], last_n_games_fp, overall_fp, overall_gp)

if __name__ == "__main__":
    # execute only if run as a script
    main()
