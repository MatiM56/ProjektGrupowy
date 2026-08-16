#!/bin/bash

PYTHON_SCRIPT="sniffer.py"
BASH_SCRIPT="wyslij_dane.sh"
OUT_PATH="sniffer/"

while true; do
    echo "--- Start sekwencji: $(date) ---"

    CURRENT_DATE=$(date +"%Y-%m-%d_%H-%M-%S")

    echo "Uruchamiam skrypt Python..."
    python3 "$PYTHON_SCRIPT" --out "${OUT_PATH}rpi2_${CURRENT_DATE}.db" --duration=11

    echo "Czekam 1 sek..."
    

    echo "Uruchamiam skrypt Bash..."
    bash "$BASH_SCRIPT"

    echo "--- Koniec sekwencji. ---"
    echo ""
done
