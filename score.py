def get_ttfl_score(splits):

    # tables containing stats categories used for ttfl score calculation
    bonus = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'FGM', 'FG3M', 'FTM']
    malus = ['TOV', 'FGA', 'FG3A', 'FTA']

    # init ttfl score to zero
    ttfl_score = 0

    # calculate bonus part (PTS + REB + AST + STL + BLK + 2*FGM + 2*FGM3 + 2*FTM)
    for cat in bonus:
        n = 1

        if (cat == 'FGM' or cat == 'FG3M' or cat == 'FTM'):
            n = 2

        ttfl_score = ttfl_score + n*splits[cat].values[0]

    # remove malus part from score (- TOV - FGA - FG3A - FTA)
    for cat in malus:
        ttfl_score = ttfl_score - splits[cat].values[0]

    # return calculated score
    return ttfl_score
