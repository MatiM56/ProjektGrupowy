# Skrypt odpowiada za wykreślenie histogramów mocy rssi oraz przedstawienia mocy rssi w funkcji czasu dla okreslonych bssid (o najwiekszej sredniej mocy)

import sqlite3
import matplotlib.pyplot as plt


def czas_na_sekundy(t):
    a = t.split("T")[1]
    h, m, s = map(float, a.split(':'))
    return h * 3600 + m * 60 + s

lacznie = 0
DBname = [
    "2p16.db",
    "2p17.db",
    "2p18.db",
    "2p19.db",
    "2p20.db",
    "2p21.db",
    "2p22.db",
    "3p16.db",
    "3p17.db",
    "3p18.db",
    "3p19.db",
    "3p20.db",
    "3p21.db",
    "3p22.db",
    "4p16.db",
    "4p17.db",
    "4p18.db",
    "4p19.db",
    "4p20.db",
    "4p21.db",
    "4p22.db",
]
NumOfAPs =  12                   # od ilu AP sygnaly sa brane pod uwage


for DB in range(len(DBname)):
    conn = sqlite3.connect(DBname[DB])
    cur = conn.cursor()

    TIMESTAMPes_by_bssid = {}           # typ distionary
    RSSIs_by_bssid = {}
    BSSIDs = []


    ### Dla każdego pliku pomiarowego sprawdzamy od jakich AP wgl odbrano sygnały  - uzyskanie tablicy z kolejnymi BSSID ###
    # cur.execute('SELECT DISTINCT bssid  FROM packets WHERE ssid = "eduroam" ')
    cur.execute(
        'SELECT DISTINCT bssid FROM packets WHERE ssid = "eduroam" AND type = 0  GROUP BY bssid HAVING COUNT(*) >= 1;    ')
    NumOfAccessPoints = 0

    for row in cur:
        if row[0] == "ff:ff:ff:ff:ff:ff":               # pozbycie sie ukrytych mac adresow
            continue
        BSSIDs.append(row[0])       # Tablica z wszystkimi adresami w pliku
        NumOfAccessPoints+=1
        #print(row,  "\n")

    #print("\n \n", NumOfAccessPoints, "  ", DBname[DB], "\n") # znaczniki reczne # do usuniecia





    ### Zebranie timestampow i bssid dla kazdego BSSID ###

    for bssid in BSSIDs:

        rRSSI = []
        rTIMESTAMP = []

        cur.execute("SELECT rssi FROM packets WHERE bssid = ? AND type = 0", (bssid,))
        for row in cur:
            rRSSI.append(row[0])
        RSSIs_by_bssid[bssid] = rRSSI

        cur.execute("SELECT timestamp FROM packets WHERE bssid = ? AND type = 0", (bssid,))
        for row in cur:
            rTIMESTAMP.append(row[0])
        TIMESTAMPes_by_bssid[bssid] = rTIMESTAMP

        cur.execute("SELECT * FROM packets WHERE bssid = ? AND type = 0", (bssid,))
        for row in cur:
            # print(row)
            lacznie+=1
    # for bssid in BSSIDs:
    #
    #     print(bssid, "\n\n")
    #     print(RSSIs_by_bssid[bssid])
    #     print("iufagWJBiUGBF \n\n\n\n\n")
    #
    # print("\n\n\n\n\n Koniec dla jednego pliku")






    ### wyznaczenie okreslonej ilosci najmocniejszych sygnalow dla kazdego AP ###
    avrPOW = []
    for bssid in BSSIDs:
        avrPOW.append(sum(RSSIs_by_bssid[bssid])/len(RSSIs_by_bssid[bssid]))

    pairs = list(zip(avrPOW, BSSIDs))       # koniecznie ta kolejnosc by sortowalo po rssi
    pairs.sort(reverse=True)                # sortoweanie od największej wartości
    top = pairs[:NumOfAPs]                 # wybranie okreslonej ilosci sygnalow o najwiekszych mocach


    topAvrRSSI, topBSSIDs = list(zip(*top))     # ponowne rozbicie par uzyskanie listy tylko z najmocniejszymi sygnalami

    print("\n\n Analysed point: ", DBname[DB])
    for rssi, bssid in zip(topAvrRSSI, topBSSIDs):
        print(rssi, "     ", bssid)

    #print(topBSSIDs)



    ### Wykreslenie histogramow ###

    fig, axes = plt.subplots(3, 4, figsize=(20, 10))
    axes = axes.flatten()

    for i, bssid in enumerate(topBSSIDs):
        ax = axes[i]
        ax.set_xlim(-100, -10)
        ax.set_ylim(0, 1)

        data = RSSIs_by_bssid[bssid]
        bins = abs(max(data) - min(data))

        if bins == 0:
            bins = 1
            ax.set_title("Error " + bssid)
            continue

        ax.hist(data, bins=bins, density=True)
        ax.set_title("BSSID: " + bssid +  "  Ilosc probek: " + str(len(data)))
        ax.set_xlabel("RSSI [dBm]")
        ax.set_ylabel("P")


    fig.suptitle("Histogramy dla punktu: " + DBname[DB], y=0.99)
    fig.tight_layout()
    plt.savefig("histogram " + DBname[DB] + ".png")
    #plt.show()
    plt.close()

    #print("Halfway Done")


    ### Wykreslenie wykresow czasowych

    fig, axes = plt.subplots(6, 2, figsize=(30, 14))
    axes = axes.flatten()

    for i, bssid in enumerate(topBSSIDs):
        ax = axes[i]

        # ax.set_ylim(0, 1)

        data = RSSIs_by_bssid[bssid]
        label_X = TIMESTAMPes_by_bssid[bssid]

        tmp = []
        for i in range(len(label_X)):                   # zamiana timestampow sql na sekundy
            tmp.append(czas_na_sekundy(label_X[i]))


        a = min(tmp)                                    # pierwqszy pomiar t = 0s
        for i in range(len(tmp)):
            tmp [i] = tmp [i] - a

        label_X = tmp
        ax.set_xlim(0, 300)

        # print("Wykres czasowy")
        # for i in range(len(label_X)):
        #     print(label_X[i], "\n")

        ax.scatter(label_X, data, label=bssid)
        ax.set_title("BSSID: " + bssid + "\nIlosc probek: " + str(len(data)), y = 0.97)
        ax.set_ylabel("RSSI [dBm]")
        ax.set_xlabel("Czas [s]")

    fig.suptitle("Wykres czasowy dla punktu: " + DBname[DB], y=0.95)
    plt.subplots_adjust(hspace=1.0)
    plt.savefig("Czasowy " + DBname[DB] + ".png")


    #plt.show()
    plt.close()
    conn.close()

    print(lacznie)



print("Done")

















