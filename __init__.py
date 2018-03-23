import datetime

import games, deck


if __name__ == "__main__":
    # execute only if run as a script

    TODAY = datetime.date.today()
    NB_PLAYERS = 5
    NB_SHORTLIST = 15
    NB_GAMES = 10
    PLOT_TRENDS = True

    shortlist = games.get_day_games(TODAY, NB_PLAYERS, NB_SHORTLIST)

    deck.get_deck_ratings(shortlist, NB_GAMES, PLOT_TRENDS)
