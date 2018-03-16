import deck, player

if __name__ == "__main__":
    # execute only if run as a script

    DECK = [
        ["Chris", "Paul"],
        ["Anthony", "Davis"],
        ["Julius", "Randle"],
        ["Rudy", "Gobert"],
    ]

    NB_GAMES = 10

    deck.get_deck_ratings(DECK, NB_GAMES)