from flask import Flask
from flask import render_template

import datetime
import games, deck
from nba_py import constants as nba_constants


if __name__ == "__main__":
    # execute only if run as a script

    # DATE = datetime.datetime(2018, 12, 22)
    DATE = datetime.date.today()
    NB_PLAYERS = 3
    NB_SHORTLIST = 5
    NB_GAMES = 5
    PLOT_TRENDS = True

    # get shortlist from regular season stats
    shortlist = games.get_day_games(DATE, NB_PLAYERS, NB_SHORTLIST, nba_constants.CURRENT_SEASON, nba_constants.SeasonType.Regular)

    # fetch and trace playoffs ratings for shortlist
    deck.get_deck_ratings(shortlist, NB_GAMES, DATE, PLOT_TRENDS, nba_constants.CURRENT_SEASON, nba_constants.SeasonType.Regular)
