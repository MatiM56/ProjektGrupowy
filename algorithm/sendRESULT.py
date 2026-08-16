# Wyznaczenie najlepiej dopasowanego punktu na bazie wyznaczonych błędów

# Wejscia:
# Errors -> lista wcześniej wyznaczonych błędów
# Possible points -> punkty odpowiadające błędom w liscie wyzej
#
# Wyjscie: brak

import sqlite3

closestPoint = "xxx"
RaspberryName = "xxx"

def sendRESULT(closestPoint, RaspberryName):

    ### Utworzenie pliku z tabela zawierajaca zbior   ###
    conn = sqlite3.connect("/home/user/algorytm/wyniki.db")
    cursor = conn.cursor()



    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS lokalizacja (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         timestamp DEFAULT CURRENT_TIMESTAMP,
         id_raspberyy VARCHAR(50) NOT NULL,
         punkt VARCHAR(255)
        )
        """
    )
    conn.commit()

    ### Wpis do tabeli z wynikami ###
    cursor.execute(
        """
        INSERT INTO lokalizacja (id_raspberyy, punkt) VALUES (?, ?)
        """,
        (RaspberryName, closestPoint))
    conn.commit()



    conn.close()
