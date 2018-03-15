import deck

if __name__ == "__main__":
    # execute only if run as a script

    DECK = [
        ["Rudy", "Gobert"],
        ["James", "Harden"],
        ["LeBron", "James"],
        ["Damian", "Lillard"],
        ["Bradley", "Beal"],
    ]

    NB_GAMES = 10

    deck.get_deck_ratings(DECK, NB_GAMES)
