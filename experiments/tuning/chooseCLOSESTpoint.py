# Funkcja odpowiada za okreslenie, ktory punkt ma najmniejsza wartosc bledu - dokonanie detekcji obecnosci
#
# Wejscia:
# PossiblePoints -> punkty dla ktorych wyliczono blad
# Errors -> bledy odpowiadajace kolejnym punktom z tablicy PossiblePoints
#
# Wyjscie:
# PointName -> nazwa punktu w ktorym najprawdopodobniej znajduje sie urzadzenie, ktorego pozycja miala zostac okreslona

def chooseCLOSESTpoint (PossiblePoints, Errors):

    tmpIndex = Errors.index(min(Errors))

    prevPointName = PossiblePoints[tmpIndex]
    PointName = prevPointName[:4]

    return PointName