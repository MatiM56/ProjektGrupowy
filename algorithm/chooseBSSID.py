# Funkcja odpowiada za wyznacznie określonej (N) ilości bssid o najmocniejszych średnich mocach odebranego sygnału
#
# Wejscia:
# RasbFileName -> nazwa pliku w którym zawarte są pomiary z raspberry (dane służące do detekcji obecności)
# N - ilość wyznaczanych sygnałów - parametr algorytmu
#
# Wyjscie:
# topBSSIDs -> N elementowa lista bssid o najmocniejszej średniej wartości rssi, posortowana malejaco (pierwszy elem. najwyzsza wartosc rssi)
#  UWAGA funkcja zwraca tylko liste bssid, nie zwraca wartosci srednich rssi

import sqlite3
import os


def czas_na_sekundy(t):
    a = t.split("T")[1]
    h, m, s = map(float, a.split(':'))
    return h * 3600 + m * 60 + s


def chooseBSSID (RasbFileName, NumOfAPs):
    abs_path = os.path.abspath(RasbFileName)
    
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Baza danych nie istnieje pod ścieżką: {abs_path}")
    try:
        conn = sqlite3.connect(f"file:{abs_path}?mode=ro", uri=True)
        cur = conn.cursor()
    except sqlite3.OperationalError as e:
        print(f"Błąd krytyczny SQLite: {e}")
        raise

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


    avrPOW = []
    for bssid in BSSIDs:
        avrPOW.append(sum(RSSIs_by_bssid[bssid]) / len(RSSIs_by_bssid[bssid]))

    pairs = list(zip(avrPOW, BSSIDs))  # koniecznie ta kolejnosc by sortowalo po rssi
    pairs.sort(reverse=True)  # sortoweanie od największej wartości
    top = pairs[:NumOfAPs]  # wybranie okreslonej ilosci sygnalow o najwiekszych mocach

    topAvrRSSI, topBSSIDs = list(zip(*top))  # ponowne rozbicie par uzyskanie listy tylko z najmocniejszymi sygnalami

    conn.close()

    return topBSSIDs
