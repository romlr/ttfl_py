import datetime

import deck, games, team


if __name__ == "__main__":
    # execute only if run as a script

    TODAY = datetime.date.today()
    NB_PLAYERS = 5
    NB_SHORTLIST = 15

    shortlist = games.get_day_games(TODAY, NB_PLAYERS, NB_SHORTLIST)

    names = shortlist['PLAYER_NAME'].values
    ttfl_score = shortlist['TTFL_SCORE'].values
    nba_fp = shortlist['NBA_FANTASY_PTS'].values

    print "SHORTLIST"
    print
    for i in range(0,NB_SHORTLIST):
        print "%s (TTFL:%.1f, NBA FP:%.1f)" % (names[i], ttfl_score[i], nba_fp[i])

    my_deck = shortlist['PLAYER_ID'].values

    NB_GAMES = 10

    deck.get_deck_ratings(my_deck, names, NB_GAMES)
