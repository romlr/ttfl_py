def get_fp_score(splits):

    # tables containing stats categories used for nba fp score calculation
    bonus = [['PTS', 1], ['REB', 1.2], ['AST', 1.5], ['STL', 3], ['BLK', 3]]
    malus = [['TOV', 1]]

    # init nba fp score to zero
    fp_score = 0

    # calculate bonus part (1*PTS + 1.2*REB + 1.5*AST + 3*STL + 3*BLK)
    for cat in bonus:
        fp_score = fp_score + cat[1]*splits[cat[0]].values[0]

    # remove malus part from score (- TOV - FGA - FG3A - FTA)
    for cat in malus:
        fp_score = fp_score - cat[1]*splits[cat[0]].values[0]

    # return calculated score
    return fp_score


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
