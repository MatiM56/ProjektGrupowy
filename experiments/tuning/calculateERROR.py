# Funkcja odpowiada za wyliczenie bledu srednio - kradratowego dla kazdego potencjalnego punktu
#
# Wejscia:
# RasbFileName -> nazwa pliku w którym zawarte są pomiary z raspberry (dane służące do detekcji obecności)
# PossiblePoints -> tablica zawierajaca nazwy wyznaczonych potencjalnych punktow
# M - ilość BSSID w punkcie, dla ktorych jest wyznaczany blad
#
# Wyjscie:
# Errors -> tablica zawierajaca wartosc bledu wyliczona dla kazdego kolejnego punktu


import sqlite3

from chooseBSSIDforError import chooseBSSIDforError

def calculateERROR(RasbFileName, PossiblePoints,  M):


    bssidRASB, rssiRASB = chooseBSSIDforError(RasbFileName, M)    # ponowne wyznacznie okreslonej ilosci sygnalow o sredniej najwiekszej mocy
                                                                  # (moze to byc inna wartosc niz dla wyznaczenia potencjalnych pkt w kltorych nastepuje dopasowanie)
    dataRASB = {}
    dataRASB =dict(zip(bssidRASB, rssiRASB))

    ErForMissingPoint = 1                           # jaki błąd przyjumemy gdy nie ma wystarczającej ilosci odebranych pkt
    Errors = []                                     # wyliczone błędy dla kolejnych wskazanych punktów

    # Wyznacznie dancyh referencyjnych za mapy #
    for point in PossiblePoints:

        bssidMAP = []                         # bssid z radio mapy
        rssiMAP = []                          # rssid z radio mapy
        dataMAP = {}                          # słownik odpowiadający za połaczenie wyzej wspomnianych wartosci

        conn = sqlite3.connect('radioMAP.db')
        cursor = conn.cursor()

        cursor.execute('SELECT bssid FROM radioMAP WHERE point = ?', (point,))      # odczyt bssid
        for row in cursor:
            bssidMAP.append(row[0])

        cursor.execute('SELECT rssi FROM radioMAP WHERE point = ?', (point,))       # odczyt rssi
        for row in cursor:
            rssiMAP.append(row[0])
        conn.close()

        dataMAP = dict(zip(bssidMAP, rssiMAP))                                                          # slownik refData - dane z bazy danych

        pointError = 0                                                                              #
        i = 1                                                                                       # poczatkowa waga bledu

        ifFirst = 1
        for bssid in bssidRASB:

            if bssid in bssidMAP:
                # print(bssid)
                tmpError = abs(dataMAP[bssid] - dataRASB[bssid]) / i    #wyliczenie wazonego bledu

                # if not ifFirst:                                       # wariacja liczenia bledu (inny wzor) - najmocniejszy sygnal ma wage 2, reszta 1
                #     tmpError = tmpError / 2
                # if ifFirst:
                #     ifFirst = 0
                # print("Error =", tmpError)
                pointError =+ tmpError
                i+=1

        if len(Errors) < M:                             # zabezpieczenie przed brakiem okreslonej ilosci bssid w danym pkt
            Errors.append(1000)
        else:
            Errors.append(pointError)
    return Errors