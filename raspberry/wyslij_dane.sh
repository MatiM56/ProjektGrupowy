#!/bin/bash
# Synchronizacja zebranych baz .db z Raspberry Pi na serwer obliczeniowy.
#
# Uwierzytelnianie odbywa sie kluczem SSH (ssh-copy-id), a NIE haslem w kodzie.
# Konfiguracja przez zmienne srodowiskowe - patrz .env.example w katalogu glownym.

set -euo pipefail

SOURCE="${SNIFFER_OUT_DIR:-/home/admin/sniffer/}"
TARGET="${SERVER_USER:?ustaw SERVER_USER}@${SERVER_HOST:?ustaw SERVER_HOST}:${SERVER_INBOX:-~/dane_odbior_1}"

echo "Uruchamiam synchronizację: $SOURCE -> $TARGET"

rsync -avz --remove-source-files -e ssh "$SOURCE" "$TARGET"

echo "Zsynchronizowano: $(date)"
