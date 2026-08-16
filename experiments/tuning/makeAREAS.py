# Generuje tabelę zawartą w pliku areas.db  która zawiera zbior wszystkich bssid wystepujacych w danym punkcie pomiearowym
#
# Wejscia:
#
# Wyjscie:
#

### Aktualnie to samo co mapa bez rssi xD

import sqlite3

DBname = [

    "4p01.db",
"4p02.db",
"4p03.db",
"4p04.db",
"4p05.db",
"4p06.db",
"4p07.db",
"4p08.db",
"4p09.db",
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
"4p27.db"
]

### Utworzenie pliku z tabela areas ###
conn = sqlite3.connect("areas.db")
cursor = conn.cursor()

### Zapis do nowego pliku db ###
cursor.execute(
    """
    DROP TABLE IF EXISTS areas;
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS areas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        point TEXT,
        bssid TEXT
    )
    """
)
conn.close()



for DB in DBname:

    bssid = []
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT bssid FROM packets WHERE ssid = "eduroam" AND type = 0 GROUP BY bssid HAVING COUNT(*) >=1;    ')

    for row in cursor:
        if (row[0] != "ff:ff:ff:ff:ff:ff"):
                bssid.append(row[0])

    conn.close()

    # print(bssid)
    conn = sqlite3.connect('areas.db')
    cursor = conn.cursor()

    for bssid in bssid:
        cursor.execute("INSERT INTO areas (point, bssid) VALUES (?,?)", (DB,bssid))
    conn.commit()
    conn.close()
    # bssid.clear()

print("Created areas table")

conn = sqlite3.connect('areas.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM areas")
for row in cursor:
    print(row, "\n")