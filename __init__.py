import datetime
from nba_py import constants as nba_constants
import games, deck


if __name__ == "__main__":
    # execute only if run as a script

    TODAY = datetime.date.today()
    NB_PLAYERS = 4
    NB_SHORTLIST = 4
    NB_GAMES = 4
    PLOT_TRENDS = True
    SEASON = nba_constants.CURRENT_SEASON
    SEASON_TYPE = nba_constants.SeasonType.Playoffs

    shortlist = games.get_day_games(TODAY, NB_PLAYERS, NB_SHORTLIST, SEASON, SEASON_TYPE)

    deck.get_deck_ratings(shortlist, NB_GAMES, PLOT_TRENDS, SEASON, SEASON_TYPE)
