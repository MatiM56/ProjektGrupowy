# Skrypt odpowiada za przetworzenie baz danych ze sniffera na gotowa mape, bazujaca na srednim rssi
# Mapa składa się z średnich wartości RSSI dla każdego BSSID w każdym pkt:
# UWAGA rekordy w bazie są pogrupowane dla pkt, ale nie sa uszeregowanie wzgledem najmocniejszego rssi
#             (1, '2p16.db', '9c:d5:7d:24:d8:2f', -83)
#             (2, '2p16.db', '9c:d5:7d:7a:59:6f', -74)
#             (3, '2p16.db', '9c:d5:7d:7a:9d:0f', -77)
#             (4, '2p16.db', '9c:d5:7d:7a:b1:cf', -79)
#             (5, '2p16.db', '9c:d5:7d:7a:cd:2f', -84)
# Skrypt ma możliwość filtrowania danych tworzacych mape:
# FILTR 1: wybór tylko ramek, z ssid = "eduroam", wymog typu ramki (0), minimalna ilosc wystapien = 20
# FILTR 2: określenie progowej mocy rssi, od ktorej uznaje sie ja za rzetelna, aktualnie nie uruchomiony

import sqlite3

dbPoints = [                # wszystkie pliki pomiarowe skladajace sie na mape
    "4p1.db",
"4p2.db",
"4p3.db",
"4p4.db",
"4p5.db",
"4p6.db",
"4p7.db",
"4p8.db",
"4p9.db",
"4p10.db",
"4p11.db",
"4p12.db",
"4p13.db",
"4p14.db",
"4p15.db",
"4p16.db",
"4p17.db",
"4p18.db",
"4p19.db",
"4p20.db",
"4p21.db",
"4p22.db",
"4p23.db",
"4p24.db",
"4p25.db",
"4p26.db",
"4p27.db",
    "xxx.db",
    ]




### Utworzenie pliku z tabela radioMAP ###
conn = sqlite3.connect("radioMAP.db")
cursor = conn.cursor()

cursor.execute(
    """
    DROP TABLE IF EXISTS radioMAP;
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS radioMAP (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        point TEXT,
        bssid TEXT,
        rssi DOUBLE
    )
    """
)
conn.close()


for DB in dbPoints:
    if DB == "xxx.db":
        continue

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    BSSIDs = []             # Zbior BSSID wystepujacych w pliku spelniajacych FILTR 1
    AVRrssi = []


    ### Wybor wszystkich bssid -> FILTR 1
    cursor.execute('SELECT DISTINCT bssid FROM packets WHERE ssid = "eduroam" AND type = 0 GROUP BY bssid HAVING COUNT(*) >= 1;    ')
    for row in cursor:
        if row[0] != "ff:ff:ff:ff:ff:ff":
            BSSIDs.append(row[0])


    ### Wyliczenie sredniego RSSI dla kazdego bssid
    for bssid in BSSIDs:

        cursor.execute('SELECT DISTINCT rssi FROM packets WHERE ssid = "eduroam" AND type = 0 AND bssid = ?', (bssid,))
        tmpRSSI = []

        for row in cursor:
            if (1):                             ## FILTR 2
                tmpRSSI.append(row[0])

        AVRrssi.append(tmpRSSI[0])
        tmpRSSI.clear()

    conn.close()

    ### Wpis RSSI i BSSID do glownej tabeli z mapa ###
    conn = sqlite3.connect('radioMAP.db')
    cursor = conn.cursor()

    for bssid, rssid in zip(BSSIDs, AVRrssi):
        cursor.execute('INSERT INTO radioMAP (point, bssid, rssi)VALUES (?,?,?)', (DB, bssid, rssid))

    conn.commit()
    conn.close()

print("Map prepared")