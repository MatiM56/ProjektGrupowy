import sqlite3
import os
from chooseBSSIDforError import chooseBSSIDforError

def calculateERROR(RasbFileName, PossiblePoints, M):
    abs_path = os.path.abspath(RasbFileName)
    bssidRASB, rssiRASB = chooseBSSIDforError(abs_path, M)
    
    dataRASB = dict(zip(bssidRASB, rssiRASB))
    Errors = []

    for point in PossiblePoints:
        bssidMAP = [] # FIXED: Case sensitivity consistency
        rssiMAP = []
        
        conn = sqlite3.connect('/home/user/algorytm/radioMAP.db')
        cursor = conn.cursor()

        cursor.execute('SELECT bssid FROM radioMAP WHERE point = ?', (point,))
        for row in cursor:
            bssidMAP.append(row[0])

        cursor.execute('SELECT rssi FROM radioMAP WHERE point = ?', (point,))
        for row in cursor:
            rssiMAP.append(row[0])
        conn.close()

        dataMAP = dict(zip(bssidMAP, rssiMAP))
        pointError = 0
        i = 1
        
        for bssid in bssidRASB:
            if bssid in bssidMAP:
                tmpError = abs(dataMAP[bssid] - dataRASB[bssid]) / i
                pointError += tmpError 
                i += 1
        
        if len(Errors) < M:
            Errors.append(pointError) 
        else:
            Errors.append(pointError)

    return Errors
