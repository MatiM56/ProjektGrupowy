// Algorytm dopasowujący - kod.cpp : Ten plik zawiera funkcję „main”. W nim rozpoczyna się i kończy wykonywanie programu.
//

#include <iostream>
#include <string>

using namespace std;


int main() // dostaje dane
{
    const int N = 3;   //ilość BSSID branych pod uwagę
    const int M = 3;   //ilość pkt zwróconych z serwera

     string zbiorBSSID[N];              // dane z Rasberry
     float zbiorRSSI[N];

     string zbiorBSSIDwzorzec[M][N];       // dane z serwera
     float zbiorRSSIwzorzec[M][N];

     /*Wyliczenie błędów*/
     for (int i = 0; i < M; i++)
     {

     }

     return 0;
}


