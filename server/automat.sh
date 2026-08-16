#!/bin/bash

# Konfiguracja ścieżek
SOURCE_DIR="/home/user/dane_odbior_1/"
ALGO_SCRIPT="/home/user/algorytm/main.py"
MIGRATE_SCRIPT="/home/user/test1.py"

# Start pętli nieskończonej
while true; do
    echo "--- Rozpoczynam nową iterację: $(date) ---"

    # Wejdź do katalogu z algorytmem
    cd /home/user/algorytm || exit

    # 1. Przetwarzanie plików algorytmem
    # Sprawdzamy, czy w ogóle są jakieś pliki .db, aby nie wyświetlać błędów pętli
    shopt -s nullglob
    files=("$SOURCE_DIR"*.db)
	
    if [ ${#files[@]} -gt 0 ]; then
        for file_path in "${files[@]}"; do
            filename=$(basename "$file_path")
            echo "Praca nad: $filename"
            python3 "$ALGO_SCRIPT" "$file_path"
        done
	
        # 2. Uruchom skrypt migracji (tylko jeśli były pliki do przetworzenia)
        echo "Uruchamiam migrację do MySQL..."
        python3 "$MIGRATE_SCRIPT"
    else
        echo "Brak nowych plików .db do przetworzenia."
    fi	
	

done
