import datetime

import deck, games, team


if __name__ == "__main__":
    # execute only if run as a script

    DATE = datetime.date(2018, 03, 17)
    NB_PLAYERS = 3
    NB_SHORTLIST = 10

    shortlist = games.get_day_games(DATE, NB_PLAYERS, NB_SHORTLIST)

    names = shortlist['PLAYER_NAME'].values
    ttfl_score = shortlist['TTFL_SCORE'].values

    for i in range(0,NB_SHORTLIST):
        print "%s - TTFL:%.1f" % (names[i], ttfl_score[i])

    my_deck = shortlist['PLAYER_ID'].values

    NB_GAMES = 10

    deck.get_deck_ratings(my_deck, names, NB_GAMES)
