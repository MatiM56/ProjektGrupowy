# Glowna funkcja programu - algorytm dopasowujacy
import matplotlib.pyplot as plt
from chooseBSSID import chooseBSSID         # komentarze gotowe
from choosePOINTS import choosePOINTS       # komentarze gotowe
from calculateERROR import calculateERROR   # komentarze gotowe
from chooseCLOSESTpoint import chooseCLOSESTpoint   # komentarze gotowe
from sendRESULT import sendRESULT

def algorythm (RasbFileName, RaspberryName, N, M):
    ### Parametry algorytmu ###
    # N = 6  # ilość BSSID branych pod uwagę w algorytmie - wyznaczenie potencjalnych punktow dopasowania
    # M = 3  # ilość BSSID branych pod uwagę w algorytmie - wyliczenia bledu w potencjalnych pkt
    # RasbFileName = "test1.db"  # miejsce na nazwę pliku z pomiarem lokalizacyjnym
    # RaspberryName = "R1"

    ### Wybranie N najbardziej znaczących BSSId dla pomiary testowego ###
    topBSSIDsRASB = []
    topBSSIDsRASB = chooseBSSID(RasbFileName,N)  # Wyznaczone N najbardziej znaczącacych mac adresow z tych odebranych przez raspberry
    # print("\n###############################################################################\n")
    # print("Analysed data: =", RasbFileName)
    # print("\nRaspberry BSSIDs choosen: ")
    # for i in range(len(topBSSIDsRASB)):
    #     print(topBSSIDsRASB[i])
    # print("Number: ", len(topBSSIDsRASB))

    ### Wybranie N ilosci punktow dla ktoych powtarzaja sie bssid ###
    PossiblePoints = choosePOINTS(topBSSIDsRASB,N)  # Wyznaczone punkty w których istnieją sygnały odebrane przez Raspberry
    # print("\nPossible points calculated: ")

    if len(PossiblePoints) == 0:                        # W przypadku braku wyznaczenia potencjalnych pkt algorytm zwraca bład
    #     print("\nNo points available for Raspberry BSSID \n")
        return "ERR"

    # for i in range(len(PossiblePoints)):
    #     print(PossiblePoints[i])
    # print("Number: ", len(PossiblePoints))

    ### Wyliczenie błędów dla RSSI dla kazdego wcześniej wyznaczonego pkt, biorac pod uwahe M ilosc BSSID ###
    Errors = []
    Errors = calculateERROR(RasbFileName, PossiblePoints, M)  # Blad sumaryczny dla kazdego pkt z PossiblePoints

    # print("\nErrors calculated for every Possible Point: ")
    # for i in range(len(Errors)):
        # print(PossiblePoints[i], "     ", Errors[i])
    # print("Number of Possible Points: ", len(Errors))

    ### Wyznaczanie najbliższego pkt - wybor pkuntu z najmniejszym bledem ###
    closestPoint = chooseCLOSESTpoint(PossiblePoints, Errors)
    # print("\nClosest point: ", closestPoint)

    ### Przakazanie danych do prezentacji ###
    sendRESULT(closestPoint, RaspberryName)

    return closestPoint



def test_algorytmu(N,M):
    roznice = []
    ####### Testy wyliczenia dopasowania
    plikiTestowe = [
        "4p01_30sek.db",
        "4p02_30sek.db",
        "4p03_30sek.db",
        "4p04_30sek.db",
        "4p05_30sek.db",
        "4p06_30sek.db",
        "4p07_30sek.db",
        "4p08_30sek.db",
        "4p09_30sek.db",
        "4p10_30sek.db",
        "4p11_30sek.db",
        "4p12_30sek.db",
        "4p13_30sek.db",
        "4p14_30sek.db",
        "4p15_30sek.db",
        "4p16_30sek.db",
        "4p17_30sek.db",
        # "4p18_30sek.db",
        # "4p19_30sek.db",
        # "4p20_30sek.db",
        "4p21_30sek.db",
        "4p22_30sek.db",
        "4p23_30sek.db",
        # "4p24_30sek.db",
        # "4p25_30sek.db",
        # "4p26_30sek.db",
        # "4p27_30sek.db"
    ]

    wynikiTestowe = []

    for test in plikiTestowe:
        tmp = algorythm(test, test, N, M)
        wynikiTestowe.append(tmp)

    poprawne = 0
    roznica1 = 0
    roznica2 = 0
    roznica3 = 0
    roznica4 = 0
    roznica5 = 0
    roznica6 = 0
    roznica7 = 0
    roznica8 = 0
    roznica9 = 0
    roznica10 = 0

    # print("\nWyniki testowe: ")
    for i in range(len(wynikiTestowe)):
        if plikiTestowe[i][:3] == wynikiTestowe[i][:3]:  # [:3] - porowananie 2 pierwszych liter bo nazwy plikow sa inne
            poprawne += 1

        if abs(int(plikiTestowe[i][2:3]) - int(wynikiTestowe[i][2:3])) == 1:
            roznica1 += 1

        if abs(int(plikiTestowe[i][2:3]) - int(wynikiTestowe[i][2:3])) == 2:
            roznica2 += 1

        if abs(int(plikiTestowe[i][2:3]) - int(wynikiTestowe[i][2:3])) == 3:
            roznica3 += 1

        if abs(int(plikiTestowe[i][2:3]) - int(wynikiTestowe[i][2:3])) == 4:
            roznica4 += 1

        if abs(int(plikiTestowe[i][2:3]) - int(wynikiTestowe[i][2:3])) == 5:
            roznica5 += 1

        if abs(int(plikiTestowe[i][2:3]) - int(wynikiTestowe[i][2:3])) == 6:
            roznica6 += 1

        if abs(int(plikiTestowe[i][2:3]) - int(wynikiTestowe[i][2:3])) == 7:
            roznica7 += 1

        if abs(int(plikiTestowe[i][2:3]) - int(wynikiTestowe[i][2:3])) == 8:
            roznica8 += 1

        if abs(int(plikiTestowe[i][2:3]) - int(wynikiTestowe[i][2:3])) == 9:
            roznica9 += 1

        if abs(int(plikiTestowe[i][2:3]) - int(wynikiTestowe[i][2:3])) == 10:
            roznica10 += 1

    # print(plikiTestowe[i][:3], wynikiTestowe[i][:3])
    # print("\n\n\n poprawnie okreslonych", poprawne)
    # print("blad 1 pkt:", roznica1)
    # print("blad 2 pkt:", roznica2)
    # print("blad 3 pkt:", roznica3)
    # print("blad 4 pkt:", roznica4)
    # print("blad 5 pkt:", roznica5)
    # print("blad 6 pkt:", roznica6)
    # print("blad 7 pkt:", roznica7)
    # print("blad 8 pkt:", roznica8)
    # print("blad 9 pkt:", roznica9)
    # print("blad 10 pkt:", roznica10)

    suma = roznica1 + roznica2 + roznica3 + roznica4 + roznica5 + roznica6 + roznica7 + roznica8 + roznica9 + roznica10 + poprawne
    # print("\nSuma okreslonych: ", suma)
    roznice = [poprawne, roznica1, roznica2, roznica3, roznica4, roznica5, roznica6, roznica7, roznica8, roznica9, roznica10 ]
    # print(roznice)
    poprawne = 0
    roznica1 = 0
    roznica2 = 0
    roznica3 = 0
    roznica4 = 0
    roznica5 = 0
    roznica6 = 0
    roznica7 = 0
    roznica8 = 0
    roznica9 = 0
    roznica10 = 0

    return roznice










#### Testy iteracyjne dla wszystkich param N,M - wyznaczenie rozkladu bledow ###



N = [1, 2, 3, 4, 5, 6]
M = [1, 2, 3, 4, 5, 6]


wyniki = []
for N in N:
    for M in M:
        tmp = []
        # print("\n\n\n\n Parametry" ,"N=", N, "M=", M)
        tmp = test_algorytmu(N, M)
        M = [1, 2, 3, 4, 5, 6]
        wyniki.append(tmp)

N = [1, 2, 3, 4, 5, 6]

### Wypisanie macierzy bledow ###
i=0
for N in N:
    for M in M:
        print("N=", N, "M=", M, "    ", wyniki[i])
        i+=1
    M = [1, 2, 3, 4, 5, 6]

# for i in indeksy:
#     print(wyniki[i])

### Generowanie wykresow  - imo do smieci i tak nic nie widac na nich###
# i =0
# N = [1, 2, 3, 4, 5, 6]
# M = [1, 2, 3, 4, 5, 6]
# indeksy = list(range(0, 11))
# print(indeksy)
#
# for N in N:
#     M = [1, 2, 3, 4, 5, 6]
#     for M in M:
#         plt.plot(indeksy, wyniki[i])
#         plt.xlabel('blad [pkt]')
#         plt.ylabel('ilosc dopasowan')
#         nazwa_pliku = "N = " + str(N) + ", M = " + str(M)
#         plt.title(nazwa_pliku)
#         plt.show()
#         plt.savefig("N = " + str(N) + " M = " + str(M) + " .png")
#         i+=1
#
# print("Analiza skończona")