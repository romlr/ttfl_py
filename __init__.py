import datetime
from nba_py import constants as nba_constants
import games, deck


if __name__ == "__main__":
    # execute only if run as a script

    DATE = datetime.date.today()
    NB_PLAYERS = 4
    NB_SHORTLIST = 4
    NB_GAMES = 12
    PLOT_TRENDS = True

    # get shortlist from regular season stats
    shortlist = games.get_day_games(DATE, NB_PLAYERS, NB_SHORTLIST, nba_constants.CURRENT_SEASON, nba_constants.SeasonType.Regular)

    # fetch and trace playoffs ratings for shortlist
    deck.get_deck_ratings(shortlist, NB_GAMES, DATE, PLOT_TRENDS, nba_constants.CURRENT_SEASON, nba_constants.SeasonType.Playoffs)
