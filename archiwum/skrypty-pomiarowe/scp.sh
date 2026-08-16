#!/usr/bin/env bash

# Skrypt do kopiowania plików z Raspberry Pi wzorem nazwa_pliku_i
# Użytkownik: admin (hasło podajesz przy pierwszym scp)

# Ustaw tutaj adresy IP (edytuj te dwie linie):
HOME_IP="192.168.0.164"
HOTSPOT_IP="172.20.10.13"

# Wybór źródła połączenia: 1 = dom, 2 = hotspot
echo "Wybierz źródło połączenia z Raspberry Pi:"
echo "  1 - dom"
echo "  2 - hotspot (telefon)"
read -p "Twój wybór (1/2): " MODE

case "$MODE" in
  1)
    RPI_IP="$HOME_IP"
    ;;
  2)
    RPI_IP="$HOTSPOT_IP"
    ;;
  *)
    echo "Nieprawidłowy wybór (oczekiwano 1 lub 2)." >&2
    exit 1
    ;;
esac

# Stałe katalogi
REMOTE_DIR="/home/admin"
LOCAL_DIR="$HOME/Desktop"

read -p "Podaj nazwę pliku z rozszerzeniem (bez indeksu, np. pomiar.txt => pomiar_1.txt): " BASE_FILENAME

# Rozdzielenie nazwy i rozszerzenia, aby wstawić indeks przed kropką
BASE_NAME="${BASE_FILENAME%.*}"
EXT=".${BASE_FILENAME##*.}"

START_I=1
read -p "Podaj indeks końcowy i: " END_I

mkdir -p "${LOCAL_DIR}"

for ((i=START_I; i<=END_I; i++)); do
	FILE_NAME="${BASE_NAME}_${i}${EXT}"
	echo "Kopiuję plik: ${FILE_NAME} z ${RPI_IP}:${REMOTE_DIR} do ${LOCAL_DIR}"
	sshpass -p "${RPI_PWD:?ustaw RPI_PWD}" scp "admin@${RPI_IP}:${REMOTE_DIR}/${FILE_NAME}" "${LOCAL_DIR}/" || {
		echo "Błąd kopiowania pliku ${FILE_NAME} (pomijam i lecę dalej)" >&2
	}
done

echo "Kopiowanie zakończone."

