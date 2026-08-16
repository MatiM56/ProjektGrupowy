import sqlite3
import os

def choosePOINTS(topBSSIDsRASB, N):
    """
    Funkcja wyznacza punkty, w których występuje przynajmniej jeden z BSSID
    odebranych przez Raspberry Pi, opierając się wyłącznie na bazie areas.db.
    """
    areas_path = "/home/user/algorytm/areas.db"
    # Folder, w którym znajdują się pliki .db poszczególnych punktów
    base_dir = "/home/user/algorytm/"
    
    if not os.path.exists(areas_path):
        print(f"  [!] BŁĄD: Nie znaleziono bazy obszarów: {areas_path}")
        return []

    conn = sqlite3.connect(areas_path)
    cur = conn.cursor()
    AllPossiblePoints = [] 

    try:
        for topBSSID in topBSSIDsRASB:
            cur.execute("SELECT DISTINCT point FROM areas WHERE bssid = ?", (topBSSID,))
            rows = cur.fetchall() # Pobieramy wszystko od razu, by nie trzymać kursora
            for row in rows:
                if row[0] not in AllPossiblePoints:
                    AllPossiblePoints.append(row[0])
    except sqlite3.OperationalError as e:
        print(f"  [X] Błąd zapytania do bazy areas.db: {e}")
    finally:
        conn.close()

    PossiblePoints = []

    for point in AllPossiblePoints:
        WhetherDeleteFlag = False
        full_path = os.path.join(base_dir, point)

        # Sprawdzamy czy plik fizycznie istnieje przed próbą połączenia
        if not os.path.exists(full_path):
            # print(f"  [!] Brak pliku: {full_path}") # Opcjonalne info
            continue

        conn = sqlite3.connect(full_path)
        cursor = conn.cursor()

        try:
            # Pobieramy BSSID dla eduroam
            cursor.execute('SELECT DISTINCT bssid FROM packets WHERE ssid = "eduroam"')
            rows = cursor.fetchall() # Kluczowe: pobieramy dane zanim zamkniemy połączenie
            refBSSIDs = [row[0] for row in rows]

            for topBSSID in topBSSIDsRASB:
                if topBSSID not in refBSSIDs:
                    WhetherDeleteFlag = True
                    break # Jeśli brakuje jednego, nie musimy sprawdzać reszty

            if not WhetherDeleteFlag:
                PossiblePoints.append(point)

        except sqlite3.OperationalError as e:
            # To się wykona, jeśli w pliku .db nie ma tabeli 'packets'
            print(f"  [X] Błąd w pliku {point}: {e}")
        finally:
            conn.close() # Zamykamy bazę dopiero po pobraniu danych (fetchall)

    return PossiblePoints
