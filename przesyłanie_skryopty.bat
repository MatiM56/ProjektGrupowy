@echo off
chcp 65001 >nul
:: Zmiana kodowania na UTF-8, aby polskie znaki w konsoli wyświetlały się poprawnie

:: --- Konfiguracja połączenia ---
set RPI_USER=admin
set RPI_IP=192.168.0.164
set DEST_DIR=/home/admin/


set /p FILE_PATH="Podaj nazwe lub sciezke do pliku, ktory chcesz wyslac: "

set FILE_PATH=%~1

:: Sprawdzenie, czy podany plik rzeczywiście istnieje
if not exist "%FILE_PATH%" (
    echo Błąd: Plik "%FILE_PATH%" nie istnieje.
    exit /b 1
)

echo Rozpoczynam wysyłanie pliku "%FILE_PATH%" do %RPI_USER%@%RPI_IP%...

:: Właściwe polecenie przesyłania (Secure Copy)
scp "%FILE_PATH%" %RPI_USER%@%RPI_IP%:%DEST_DIR%

:: Sprawdzenie, czy polecenie scp zakończyło się sukcesem
if %ERRORLEVEL% EQU 0 (
    echo Sukces! Plik został pomyślnie przesłany na Raspberry Pi.
) else (
    echo Błąd: Przesyłanie pliku nie powiodło się. Sprawdź połączenie i hasło.
)