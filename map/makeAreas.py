# Generuje tabelę zawartą w pliku areas.db  która zawiera zbior wszystkich bssid wystepujacych w danym punkcie pomiearowym
#
# Wejscia:
#
# Wyjscie:
#

import sqlite3
import os

# Lista plików pomiarowych
DBname = [
    "4p01.db", "4p02.db", "4p03.db", "4p04.db", "4p05.db", "4p06.db", "4p07.db",
    "4p08.db", "4p09.db", "4p10.db", "4p11.db", "4p12.db", "4p13.db", "4p14.db",
    "4p15.db", "4p16.db", "4p17.db", "4p18.db", "4p19.db", "4p20.db", "4p21.db",
    "4p22.db", "4p23.db", "4p24.db", "4p25.db", "4p26.db", "4p27.db", "4p28.db",
    "4p29.db", "4p30.db", "4p31.db", "4p32.db", "4p33.db", "4p34.db", "4p35.db",
    "4p36.db", "4p37.db", "4p38.db", "4p39.db", "4p40.db", "4p41.db", "4p42.db",
    "4p43.db", "4p44.db", "4p45.db", "4p46.db", "4p47.db", "4p48.db", "4p49.db",
    "4p50.db", "4p51.db", "4p52.db", "4p53.db", "4p54.db", "4p55.db", "4p56.db",
    "4p57.db", "4p58.db"
]

base_path = "/home/user/algorytm"
areas_db_path = os.path.join(base_path, "areas.db")

### Utworzenie pliku z tabelą areas ###
conn = sqlite3.connect(areas_db_path)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS areas;")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS areas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        point TEXT,
        bssid TEXT
    )
""")
conn.commit()
conn.close()

for db_file in DBname:
    full_db_path = os.path.join(base_path, db_file)

    if not os.path.exists(full_db_path):
        print(f"  [!] OSTRZEŻENIE: Pomijam {db_file} - plik nie istnieje w {base_path}")
        continue

    found_bssids = []
    
    try:
        conn = sqlite3.connect(full_db_path)
        cursor = conn.cursor()
        
        # Wykonanie zapytania
        cursor.execute('SELECT DISTINCT bssid FROM packets WHERE ssid = "eduroam" AND type = 0 GROUP BY bssid HAVING COUNT(*) >= 1;')
        
        for row in cursor:
            if row[0] != "ff:ff:ff:ff:ff:ff":
                found_bssids.append(row[0])
        
        conn.close()
        
    except sqlite3.OperationalError as e:
        print(f"  [X] Błąd w pliku {db_file}: {e}")
        if conn: conn.close()
        continue

    conn = sqlite3.connect(areas_db_path)
    cursor = conn.cursor()

    for mac in found_bssids:
        cursor.execute("INSERT INTO areas (point, bssid) VALUES (?,?)", (db_file, mac))
    
    conn.commit()
    conn.close()
    print(f"  [+] Przetworzono: {db_file} ({len(found_bssids)} BSSID)")

print("\n--- Tabela areas została utworzona ---")

# Podgląd wyników
conn = sqlite3.connect(areas_db_path)
cursor = conn.cursor()
cursor.execute("SELECT * FROM areas LIMIT 10") # Limit, żeby nie zasypać konsoli
for row in cursor:
    print(row)
conn.close()
