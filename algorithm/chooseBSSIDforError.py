import sqlite3
import os

def czas_na_sekundy(t):
    a = t.split("T")[1]
    h, m, s = map(float, a.split(':'))
    return h * 3600 + m * 60 + s

def chooseBSSIDforError(RasbFileName, NumOfAPs):
    abs_path = os.path.abspath(RasbFileName)
    
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Nie znaleziono pliku bazy danych: {abs_path}")

    conn = sqlite3.connect(abs_path)
    cur = conn.cursor()

    TIMESTAMPes_by_bssid = {} 
    RSSIs_by_bssid = {}
    BSSIDs = []

    try:
        cur.execute('SELECT DISTINCT bssid FROM packets WHERE ssid = "eduroam"')
    except sqlite3.OperationalError as e:
        # Jeśli tu trafimy, to znaczy że plik został otwarty, ale tabela 'packets' nie istnieje
        conn.close()
        raise sqlite3.OperationalError(f"Błąd w pliku {RasbFileName}: {e}")

    NumOfAccessPoints = 0
    for row in cur:
        if row[0] == "ff:ff:ff:ff:ff:ff":
            continue
        BSSIDs.append(row[0])
        NumOfAccessPoints += 1

    # Zebranie danych dla każdego BSSID
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

    # Wyznaczenie średnich mocy
    avrPOW = []
    for bssid in BSSIDs:
        if len(RSSIs_by_bssid[bssid]) > 0:
            avrPOW.append(sum(RSSIs_by_bssid[bssid]) / len(RSSIs_by_bssid[bssid]))
        else:
            avrPOW.append(-100) # Wartość domyślna dla braku danych

    pairs = list(zip(avrPOW, BSSIDs))
    pairs.sort(reverse=True)
    top = pairs[:NumOfAPs]

    topAvrRSSI, topBSSIDs = list(zip(*top))

    conn.close()
    return topBSSIDs, topAvrRSSI
