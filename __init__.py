import datetime

import deck, player, team, games


if __name__ == "__main__":
    # execute only if run as a script

    DECK = [
        ["Ben", "Simmons"],
        ["DeMar", "DeRozan"],
        ["Jonas", "Valanciunas"],
        ["Tobias", "Harris"],
    ]

    NB_GAMES = 15

    # deck.get_deck_ratings(DECK, NB_GAMES)

    today = datetime.date.today()
    games.get_day_games(today)