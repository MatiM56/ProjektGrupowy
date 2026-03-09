import sqlite3
import matplotlib.pyplot as plt
import ctime

conn = sqlite3.connect('Soliton_czasowy_1.db')
cur = conn.cursor()
timestampes = []
rssi = []




# wpisanie kolejnych wartosci RSSI do tablicy (os Y)
cur.execute('SELECT rssi  FROM packets WHERE bssid = "24:36:da:13:c7:4f" order by timestamp  ')

suma=0
i=0
for row in cur:
     rssi.append(row)
     #timestamp.append(i)
     i+=1






# wpisanie kolejnych wartosci timestamp do tablicy (os X)


# zamiana "HH:MM:SS" na liczbę sekund
def czas_na_sekundy(t):
    h, m, s = map(float, t.split(':'))
    return h * 3600 + m * 60 + s

cur.execute('SELECT timestamp FROM packets WHERE bssid = "24:36:da:13:c7:4f" order by timestamp')

timestampes = []
for row in cur:
    row = list(row)
    for timestamp in row:
        # bierzemy tylko część po "T"
        timestamp = timestamp.split("T")[1]
        timestampes.append(timestamp)

# początek pomiaru = pierwszy timestamp (w sekundach)
poczatek_pomiaru = czas_na_sekundy(timestampes[0])

czas = []
for t in timestampes:
    czas_od_poczatku = czas_na_sekundy(t) - poczatek_pomiaru
    czas.append(czas_od_poczatku)

print(czas)
plt.plot(czas, rssi)



print(i)
plt.show()
plt.savefig('RSSI.png')


conn.close()


