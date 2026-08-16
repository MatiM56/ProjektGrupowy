import sys
import os  # Dodane, aby poprawnie obsługiwać ścieżki do plików
import traceback

from chooseBSSID import chooseBSSID
from choosePOINTS import choosePOINTS
from calculateERROR import calculateERROR
from chooseCLOSESTpoint import chooseCLOSESTpoint
from sendRESULT import sendRESULT

def algorythm(RasbFileName, RaspberryName):
    ### Parametry algorytmu ###
    N = 6  # ilość BSSID branych pod uwagę w algorytmie
    M = 6  # ilość BSSID branych pod uwagę w algorytmie

    ### Wybranie N najbardziej znaczących BSSId ###
    topBSSIDsRASB = []
    topBSSIDsRASB = chooseBSSID(RasbFileName, N)

    print("\n###############################################################################\n")
    print("Analysed data: =", RasbFileName)
    print("\nRaspberry BSSIDs chosen: ")
    for i in range(len(topBSSIDsRASB)):
        print(topBSSIDsRASB[i])
    print("Number: ", len(topBSSIDsRASB))

    ### Wybranie punktów, dla których powtarzają się BSSID ###
    PossiblePoints = choosePOINTS(topBSSIDsRASB, N)
    print("\nPossible points calculated: ")
    for pt in PossiblePoints:
        print(pt)
    print("Number: ", len(PossiblePoints))

    ### Wybranie N ilosci punktow dla ktoych powtarzaja sie bssid ###
    PossiblePoints = choosePOINTS(topBSSIDsRASB,N)  # Wyznaczone punkty w których istnieją sygnały odebrane przez Raspberry
    print("\nPossible points calculated: ")

    if len(PossiblePoints) == 0:                        # W przypadku braku wyznaczenia potencjalnych pkt algorytm zwraca bład
        print("\nNo points available for Raspberry BSSID \n")
        return "ERR"

    for i in range(len(PossiblePoints)):
        print(PossiblePoints[i])
    print("Number: ", len(PossiblePoints))

    ### Wyliczenie błędów dla RSSI dla kazdego wcześniej wyznaczonego pkt, biorac pod uwahe M ilosc BSSID ###
    Errors = []
    Errors = calculateERROR(RasbFileName, PossiblePoints, M)  # Blad sumaryczny dla kazdego pkt z PossiblePoints

    print("\nErrors calculated for every Possible Point: ")
    for i in range(len(Errors)):
        print(PossiblePoints[i], "     ", Errors[i])
    print("Number of Possible Points: ", len(Errors))

    ### Wyznaczanie najbliższego pkt - wybor pkuntu z najmniejszym bledem ###
    closestPoint = chooseCLOSESTpoint(PossiblePoints, Errors)
    print("\nClosest point: ", closestPoint)

    ### Przakazanie danych do prezentacji ###
    sendRESULT(closestPoint, RaspberryName)

    return closestPoint

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Błąd: Musisz podać nazwę pliku jako argument!")
        print("Przykład: python3 main.py rpi1_test.db")
        sys.exit(1)

    input_path = sys.argv[1]

    ### Rozpoznawanie nazwy urządzenia (R1/R2) ###
    filename = os.path.basename(input_path)
    prefix = filename[:4].lower()

    if prefix == "rpi1":
        detected_name = "R1"
    elif prefix == "rpi2":
        detected_name = "R2"
    else:
        detected_name = "Unknown"

    print(f"--- START: {filename} ---")
    print(f"--- Urządzenie: {detected_name} ---")

    algorythm(input_path, detected_name) 



