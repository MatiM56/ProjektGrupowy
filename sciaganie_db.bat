
@echo off
REM Skrypt Windows do kopiowania plików z Raspberry Pi wzorem nazwa_pliku_i
REM Odpowiednik bashowego skryptu "scp".

REM Ustaw tutaj adresy IP (edytuj te dwie linie):
set "HOME_IP=192.168.0.164"
set "HOTSPOT_IP=172.20.10.13"

REM Wybór źródła połączenia: 1 = dom, 2 = hotspot
echo Wybierz zrodlo polaczenia z Raspberry Pi:
echo   1 - dom
echo   2 - hotspot (telefon)
set /p MODE="Twoj wybor 1 lub 2: "

REM Prosty wybor za pomoca GOTO, bez nawiasow
if "%MODE%"=="1" goto :use_home
if "%MODE%"=="2" goto :use_hotspot
echo Nieprawidlowy wybor (oczekiwano 1 lub 2).
goto :eof

:use_home
set "RPI_IP=%HOME_IP%"
goto :after_mode

:use_hotspot
set "RPI_IP=%HOTSPOT_IP%"

:after_mode

REM Stale katalogi
set "REMOTE_DIR=/home/admin"
set "LOCAL_DESKTOP=%USERPROFILE%\Desktop"

REM Haslo do konta admin na Raspberry Pi (UWAGA: zapisane w jawnym tekscie)
set "RPI_PWD=zaq1@WSX"

set /p BASE_NAME="Podaj bazowa nazwe pliku (bez _i i bez rozszerzenia, np. pomiar): "
REM Docelowy katalog na pliki: Desktop\BAZOWA_NAZWA
set "LOCAL_DIR=%LOCAL_DESKTOP%\%BASE_NAME%"
set /p EXT="Podaj rozszerzenie z kropka (np. .txt): "

set "START_I=1"
set /p END_I="Podaj indeks koncowy i: "

REM Usun ewentualne spacje z END_I
set "END_I=%END_I: =%"

if "%END_I%"=="" goto :eof

if not exist "%LOCAL_DIR%" mkdir "%LOCAL_DIR%"

setlocal enabledelayedexpansion
for /l %%I in (%START_I%,1,%END_I%) do (
    set "FILE_NAME=%BASE_NAME%_%%I%EXT%"
    echo Kopiuje plik: !FILE_NAME! z %RPI_IP%:%REMOTE_DIR% do %LOCAL_DIR%
    REM Uzyj pscp.exe z pakietu PuTTY (musi byc w PATH lub w tym samym katalogu co skrypt)
    pscp.exe -pw "%RPI_PWD%" "admin@%RPI_IP%:%REMOTE_DIR%/!FILE_NAME!" "%LOCAL_DIR%/"
    if errorlevel 1 echo Blad kopiowania pliku !FILE_NAME! (pomijam i lece dalej)
)
endlocal

echo Kopiowanie zakonczone.
