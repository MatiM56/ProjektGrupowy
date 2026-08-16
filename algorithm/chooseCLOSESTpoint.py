


def chooseCLOSESTpoint (PossiblePoints, Errors):

    tmpIndex = Errors.index(min(Errors))

    prevPointName = PossiblePoints[tmpIndex]
    PointName = prevPointName[:-3]

    return PointName
