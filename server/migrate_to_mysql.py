import sqlite3
import mysql.connector
import mysql.connector.errors
import os
import shutil
import time
import fcntl
import sys

# --- KONFIGURACJA ---
# Dane dostepowe pobierane sa ze zmiennych srodowiskowych - patrz .env.example
MYSQL_CONFIG = {
    'host': os.environ.get('MYSQL_HOST', 'localhost'),
    'user': os.environ['MYSQL_USER'],
    'password': os.environ['MYSQL_PASSWORD'],
    'database': os.environ.get('MYSQL_DATABASE', 'test'),
}
SOURCE_DIR = os.environ.get('SOURCE_DIR', '/home/user/dane_odbior_1/')
ARCHIVE_DIR = os.environ.get('ARCHIVE_DIR', '/home/user/dane_odbior_1/archive')
LOCK_FILE = os.environ.get('LOCK_FILE', '/tmp/migrate_wifi.lock')


def migrate_data(sqlite_db_path, max_retries=3):
    sqlite_conn = None
    mysql_conn = None
    try:
        sqlite_conn = sqlite3.connect(sqlite_db_path)
        sqlite_cursor = sqlite_conn.cursor()

        sqlite_cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='packets'"
        )
        if sqlite_cursor.fetchone() is None:
            print(f"  [!] Plik pusty - brak tabeli 'packets'. Do archiwum.")
            return True

        mysql_conn = mysql.connector.connect(**MYSQL_CONFIG)
        mysql_cursor = mysql_conn.cursor()

        sqlite_cursor.execute(
            "SELECT timestamp, bssid, type, subtype, ssid, rssi, channel, label FROM packets"
        )
        rows = sqlite_cursor.fetchall()

        if not rows:
            print(f"  [!] Tabela pusta. Do archiwum.")
            return True

        insert_query = """
            INSERT IGNORE INTO wifi_logs (timestamp, bssid, type, subtype, ssid, rssi, channel, label)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        # RETRY przy deadlocku
        for attempt in range(max_retries):
            try:
                mysql_cursor.executemany(insert_query, rows)
                mysql_conn.commit()
                added_count = mysql_cursor.rowcount
                print(f"  [+] Zaimportowano: {added_count} (z {len(rows)})")
                return True
            except mysql.connector.errors.DatabaseError as e:
                if e.errno == 1213:  # deadlock
                    print(f"  [!] Deadlock, proba {attempt+1}/{max_retries}. Czekam...")
                    mysql_conn.rollback()
                    time.sleep(2 ** attempt)
                else:
                    raise
        print(f"  [X] Deadlock nie ustapil po {max_retries} probach.")
        return False

    except Exception as e:
        print(f"  [X] Blad: {e}")
        return False
    finally:
        if sqlite_conn: sqlite_conn.close()
        if mysql_conn: mysql_conn.close()


def move_to_archive(file_path, filename):
    try:
        dest = os.path.join(ARCHIVE_DIR, filename)
        if os.path.exists(dest):
            base, ext = os.path.splitext(filename)
            dest = os.path.join(ARCHIVE_DIR, f"{base}_{int(time.time())}{ext}")
        shutil.move(file_path, dest)
        print(f"  [OK] Plik przeniesiony do {dest}")
    except Exception as move_err:
        print(f"  [!] Nie udalo sie przeniesc pliku: {move_err}")


if __name__ == "__main__":
    lock_fp = open(LOCK_FILE, 'w')
    try:
        fcntl.flock(lock_fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        print("Inna instancja juz dziala. Wychodze.")
        sys.exit(0)

    print("Rozpoczynam skanowanie folderu w poszukiwaniu plikow .db...")

    if not os.path.exists(SOURCE_DIR):
        print(f"BLAD: Folder {SOURCE_DIR} nie istnieje!")
        sys.exit(1)

    if not os.path.exists(ARCHIVE_DIR):
        os.makedirs(ARCHIVE_DIR)

    files = [f for f in os.listdir(SOURCE_DIR) if f.endswith('.db')]

    if not files:
        print("Brak plikow do przetworzenia.")
    else:
        for filename in files:
            file_path = os.path.join(SOURCE_DIR, filename)
            print(f"\n--- Przetwarzanie: {filename} ---")

            success = migrate_data(file_path)

            if success:
                move_to_archive(file_path, filename)
            else:
                print(f"  [!] Import nieudany, ale i tak archiwizuje.")
                move_to_archive(file_path, filename)

    print("\nGotowe!")
