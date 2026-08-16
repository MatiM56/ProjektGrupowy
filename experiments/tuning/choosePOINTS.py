# Funkcja odpowiada za wyznacznie wszystkich punktow, w ktorych potencjalnie moze znajdowac sie urzadzenie
# Punkty sa wyznaczane na bazie okreslenia dla jakich punktow jednoczenie wystepuja wszytskie N (ilosc) BSSID
# odebranych przez urzadzenie w mapie
#
# Wejscia:
# topBSSIDsRASB -> tablica przechowująca N BSSID odebranych przez urzadzenie
# N - ilość branych pod uwage BSSID - parametr algorytmu
#
# Wyjscie:
# PossiblePoints -> tablica zawierajaca nazwy wyznaczonych potencjalnych punktow

import sqlite3

def choosePOINTS(topBSSIDsRASB, N):
    conn = sqlite3.connect("areas.db")
    cur = conn.cursor()

    AllPossiblePoints = []              # Zbior wszystkich pkt w ktorych występuje przynajmniej jedno bssid

    ### Wyznaczenie wszystkich pkt w ktorych występuje przynajmniej jedno bssid
    for topBSSID in topBSSIDsRASB:                                                                                      # iteracja po bssid
        cur.execute("select distinct point from areas WHERE bssid=?", (topBSSID,))
        for row in cur:
            if row[0] not in AllPossiblePoints:
                AllPossiblePoints.append(row[0])

    conn.close()

    PossiblePoints = []                 # Zbior wszystkich pkt w ktorych wystepuja wszystkie BSSID z tablicy topBSSIDsRASB

    ### Sprawdzenie kazdego punku, czy wystepuja w nim wszystkie BSSID
    for point in AllPossiblePoints:

        WhetherDeleteFlag = False

        conn = sqlite3.connect(point)
        cursor = conn.cursor()

        cursor.execute('select distinct bssid from packets WHERE ssid= "eduroam" ')
        RefBSSIDs = []

        for row in cursor:
            RefBSSIDs.append(row[0])

        for topBSSID in topBSSIDsRASB:
            if topBSSID not in RefBSSIDs:
                WhetherDeleteFlag = True

        if WhetherDeleteFlag == False:
            PossiblePoints.append(point)

        WhetherDeleteFlag = False
        conn.close()

    return PossiblePoints