# Funkcja odpowiada za wyznacznie określonej (N) ilości bssid oraz sredniej arytmetycznej mocy rssi o najmocniejszych średnich mocach odebranego sygnału
#
# Wejscia:
# RasbFileName -> nazwa pliku w którym zawarte są pomiary z raspberry (dane służące do detekcji obecności)
# M - ilość wyznaczanych sygnałów - parametr algorytmu
#
# Wyjscie:
# topBSSIDs -> N elementowa lista bssid o najmocniejszej średniej wartości rssi, posortowana malejaco (pierwszy elem. najwyzsza wartosc rssi)
# topAvrRSSI -> N elementowa lista sredniej arytmetycznej mocy RSSI o najmocniejszej średniej wartości rssi,
#               posortowana malejaco (pierwszy elem. najwyzsza wartosc rssi)

import sqlite3

def czas_na_sekundy(t):
    a = t.split("T")[1]
    h, m, s = map(float, a.split(':'))
    return h * 3600 + m * 60 + s


def chooseBSSIDforError (RasbFileName, M):

    conn = sqlite3.connect(RasbFileName)
    cur = conn.cursor()

    TIMESTAMPes_by_bssid = {}  # typ distionary
    RSSIs_by_bssid = {}
    BSSIDs = []

    ### Dla każdego pliku pomiarowego sprawdzamy od jakich AP wgl odbrano sygnały  - uzyskanie tablicy z kolejnymi BSSID ###
    cur.execute('SELECT DISTINCT bssid  FROM packets WHERE ssid = "eduroam" ')
    NumOfAccessPoints = 0

    for row in cur:
        if row[0] == "ff:ff:ff:ff:ff:ff":  # pozbycie sie ukrytych mac adresow
            continue
        BSSIDs.append(row[0])  # Tablica z wszystkimi adresami w pliku
        NumOfAccessPoints += 1
        # print(row,  "\n")

    # print("\n \n", NumOfAccessPoints, "  ", DBname[DB], "\n") # znaczniki reczne # do usuniecia

    ### Zebranie timestampow i bssid dla kazdego BSSID ###

    for bssid in BSSIDs:

        rRSSI = []
        rTIMESTAMP = []

        cur.execute("SELECT rssi FROM packets WHERE bssid = ?", (bssid,))
        for row in cur:
            rRSSI.append(row[0])
        RSSIs_by_bssid[bssid] = rRSSI

        cur.execute("SELECT timestamp FROM packets WHERE bssid = ?", (bssid,))
        for row in cur:
            rTIMESTAMP.append(row[0])
        TIMESTAMPes_by_bssid[bssid] = rTIMESTAMP

    # for bssid in BSSIDs:
    #
    #     print(bssid, "\n\n")
    #     print(RSSIs_by_bssid[bssid])
    #     print("iufagWJBiUGBF \n\n\n\n\n")
    #
    # print("\n\n\n\n\n Koniec dla jednego pliku")

    ### wyznaczenie okreslonej ilosci najmocniejszych sygnalow dla kazdego AP ###
    avrPOW = []
    for bssid in BSSIDs:
        avrPOW.append(sum(RSSIs_by_bssid[bssid]) / len(RSSIs_by_bssid[bssid]))

    pairs = list(zip(avrPOW, BSSIDs))  # koniecznie ta kolejnosc by sortowalo po rssi
    pairs.sort(reverse=True)  # sortoweanie od największej wartości
    top = pairs[:M]  # wybranie okreslonej ilosci sygnalow o najwiekszych mocach

    topAvrRSSI, topBSSIDs = list(zip(*top))  # ponowne rozbicie par uzyskanie listy tylko z najmocniejszymi sygnalami

    #print(topBSSIDs)

    conn.close()

    return topBSSIDs, topAvrRSSI
