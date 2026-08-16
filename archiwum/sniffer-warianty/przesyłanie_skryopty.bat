@echo off
chcp 65001 >nul

:: --- Konfiguracja połączenia ---
set RPI_USER=admin
set RPI_IP=192.168.0.164
set DEST_DIR=/home/admin/

:: --- Pobranie nazwy pliku od użytkownika ---
set /p FILE_PATH="Podaj nazwe lub sciezke do pliku, ktory chcesz wyslac: "

:: Sprawdzenie, czy w ogóle coś wpisano
if "%FILE_PATH%"=="" (
    echo Blad: Nie podano nazwy pliku.
    exit /b 1
)

:: Usuwanie ewentualnych cudzysłowów (przydatne np. przy kopiowaniu ścieżki z Windowsa)
set FILE_PATH=%FILE_PATH:"=%

:: Sprawdzenie, czy podany plik rzeczywiście istnieje
if not exist "%FILE_PATH%" (
    echo Blad: Plik "%FILE_PATH%" nie istnieje w tym folderze. Sprawdz czy podajesz dobra nazwe.
    exit /b 1
)

echo Rozpoczynam wysylanie pliku "%FILE_PATH%" do %RPI_USER%@%RPI_IP%...

:: Właściwe polecenie przesyłania
scp "%FILE_PATH%" %RPI_USER%@%RPI_IP%:%DEST_DIR%

:: Sprawdzenie, czy polecenie scp zakończyło się sukcesem
if %ERRORLEVEL% EQU 0 (
    echo Sukces! Plik zostal pomyslnie przeslany na Raspberry Pi.
) else (
    echo Blad: Przesylanie pliku nie powiodlo sie. Sprawdz polaczenie i haslo.
)