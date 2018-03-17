import datetime

import deck, games, team


if __name__ == "__main__":
    # execute only if run as a script

    NB_PLAYERS = 3
    DATE = datetime.date(2018, 03, 17)

    shortlist = games.get_day_games(DATE, NB_PLAYERS)
    print shortlist

    DECK = [
        ["Karl-Anthony", "Towns"],
        ["Draymond", "Green"],
        ["Damian", "Lillard"],
        ["Khris", "Middleton"],
    ]

    NB_GAMES = 15

    # deck.get_deck_ratings(DECK, NB_GAMES)
