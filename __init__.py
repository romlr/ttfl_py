import datetime

import deck, games, team


if __name__ == "__main__":
    # execute only if run as a script

    TODAY = datetime.date.today()
    NB_PLAYERS = 5
    NB_SHORTLIST = 20

    shortlist = games.get_day_games(TODAY, NB_PLAYERS, NB_SHORTLIST)

    my_deck = shortlist['PLAYER_ID'].values
    names = shortlist['PLAYER_NAME'].values

    NB_GAMES = 10

    deck.get_deck_ratings(my_deck, names, NB_GAMES)
