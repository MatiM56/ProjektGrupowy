# scapy_channel_hopper.py
# Usage: sudo python3 scapy_channel_hopper.py --iface wlx... --channels 1,6,11 --dwell 0.25 --write-interval 2 --out skan.csv

import argparse
from asyncio import timeout
import threading
import time
import subprocess
import sys
import sqlite3
import os
from datetime import datetime
from scapy.all import sniff, Dot11, Dot11Elt, RadioTap, conf

# Ustawienie kanału
def set_channel(iface, ch):
    try:
        subprocess.run(["iw", "dev", iface, "set", "channel", str(ch)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except Exception:
        return False

def get_ssid(packet):
    if packet.haslayer(Dot11Elt):
        elt = packet.getlayer(Dot11Elt)
        while elt:
            if elt.ID == 0:
                ssid = elt.info.decode(errors="ignore")
                return ssid
            elt = elt.payload.getlayer(Dot11Elt)
    return ""

def get_rssi(packet):
    if packet.haslayer(RadioTap):
        ramka = packet.getlayer(RadioTap)
        if hasattr(ramka, "dBm_AntSignal") and ramka.dBm_AntSignal is not None:
            return ramka.dBm_AntSignal
    return None

def get_noise_level(packet):
    if packet.haslayer(RadioTap):
        ramka = packet.getlayer(RadioTap)
        if hasattr(ramka, "dBm_AntNoise") and ramka.dBm_AntNoise is not None:
            return ramka.dBm_AntNoise
    return None

attention_lock = threading.Lock()
buffer = []

def packet_handler(packet, current_channel_getter, measure_noise):
    if not packet.haslayer(Dot11):
        return
    dot11 = packet.getlayer(Dot11)
    bssid = dot11.addr3 if dot11.addr3 else dot11.addr2
    subtype = dot11.subtype
    type_ = dot11.type
    ssid = get_ssid(packet)
    rssi = get_rssi(packet)
    timestamp = datetime.now().isoformat(timespec='milliseconds')
    ch = current_channel_getter()
    
    # Pomiar poziomu szumu
    
    if measure_noise:
        noise_level = get_noise_level(packet)
    
    row = {
        "timestamp": timestamp,
        "bssid": bssid or "",
        "type": type_,
        "subtype": subtype,
        "ssid": ssid,
        "rssi": rssi if rssi is not None else "",
        "channel": ch,
        "noise_level": noise_level if noise_level is not None else "",
    }
    with attention_lock:
        buffer.append(row)

# --- Channel hopper thread ---
def hopper_thread(iface, channels, dwell, running_flag, current_channel):
    idx = 0
    while running_flag["run"]:
        ch = channels[idx % len(channels)]
        ok = set_channel(iface, ch)
        if not ok:
            pass
        current_channel["ch"] = ch
        time.sleep(dwell)
        idx += 1

def init_db(db_path):
    connection = sqlite3.connect(db_path, check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS packets (
            timestamp TEXT PRIMARY KEY,
            bssid TEXT,
            type INTEGER,
            subtype INTEGER,
            ssid TEXT,
            rssi INTEGER,
            channel INTEGER
        )
        """
    )
    cursor.execute("PRAGMA table_info(packets)")
    columns = [row[1] for row in cursor.fetchall()]
    if "label" not in columns:
        cursor.execute("ALTER TABLE packets ADD COLUMN label TEXT")
    if "noise_level" not in columns:
        cursor.execute("ALTER TABLE packets ADD COLUMN noise_level INTEGER")
    connection.commit()
    return connection


def insert_rows(connection, rows, label):
    if not rows:
        return
    cursor = connection.cursor()
    filtered_rows = []
    for r in rows:
        # Sprawdź ostatni timestamp dla tego samego bssid, type, subtype, channel
        cursor.execute(
            "SELECT MAX(timestamp) FROM packets WHERE bssid=? AND type=? AND subtype=? AND channel=?",
            (r["bssid"], r["type"], r["subtype"], r["channel"])
        )
        result = cursor.fetchone()
        if result and result[0]:
            last_ts_string = result[0]
            last_ts = datetime.fromisoformat(last_ts_string)
            current_ts = datetime.fromisoformat(r["timestamp"])
            diff_ms = (current_ts - last_ts).total_seconds() * 1000
            if diff_ms <= 10:
                continue  # Pomiń pakiet, jeśli różnica <= 10 ms
        filtered_rows.append(r)
    
    if not filtered_rows:
        return
    cursor.executemany(
        "INSERT OR REPLACE INTO packets (timestamp, bssid, type, subtype, ssid, rssi, channel, label, noise_level) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        [
            (
                r["timestamp"],
                r["bssid"],
                r["type"],
                r["subtype"],
                r["ssid"],
                r["rssi"] if r["rssi"] != "" else None,
                r["channel"],
                label,
                r["noise_level"] if r["noise_level"] is not None else None,
            )
            for r in filtered_rows
        ],
    )
    connection.commit()


def insert_noise_rows(connection, noise_rows):
    if not noise_rows:
        return
    cursor = connection.cursor()
    cursor.executemany(
        "INSERT OR REPLACE INTO noise_levels (timestamp, channel, noise_level) VALUES (?, ?, ?)",
        [
            (
                r["timestamp"],
                r["channel"],
                r["noise_level"],
            )
            for r in noise_rows
        ],
    )
    connection.commit()


def writer_thread(db_path, write_interval, running_flag, measure_noise):
    connection = init_db(db_path)
    label = os.path.splitext(os.path.basename(db_path))[0]

    while running_flag["run"]:
        time.sleep(write_interval)
        with attention_lock:
            if not buffer:
                continue
            rows = buffer[:]
            buffer.clear()
        insert_rows(connection, rows, label)

    connection.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--iface", default=" wlx045ea4eeffd4", help="monitor-mode interface")
    parser.add_argument("--channels", default="1-13,36-165", help="comma-separated channels (f.e. 1,6,11 or 1-13)")
    parser.add_argument("--dwell", type=float, default=0.25, help="time per channel in seconds (default 0.25)")
    parser.add_argument("--write-interval", type=float, default=2.0, help="writes to database every N seconds (default 2)")
    parser.add_argument("--out", required=True, help="output SQLite database file")
    parser.add_argument("--duration", type=float, default=10, help="optional: stop after this many seconds (0 = infinite)")
    parser.add_argument("--measure-noise", default=True, action="store_true", help="enable noise level measurement")
    args = parser.parse_args()

    chans = []
    for part in args.channels.split(","):
        if "-" in part:
            a,b = part.split("-",1)
            chans.extend(list(range(int(a), int(b)+1)))
        else:
            chans.append(int(part))

    conf.iface = args.iface

    try:
        subprocess.run(["ip", "link", "show", args.iface], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        print(f"Interface {args.iface} not found. Ensure it's present and in monitor mode.", file=sys.stderr)
        sys.exit(1)

    running_flag = {"run": True}
    current_channel = {"ch": chans[0]}

    # Start hopper
    hopper = threading.Thread(target=hopper_thread, args=(args.iface, chans, args.dwell, running_flag, current_channel), daemon=True)
    hopper.start()

    # Start writer (database logger)
    writer = threading.Thread(target=writer_thread, args=(args.out, args.write_interval, running_flag, args.measure_noise), daemon=True)
    writer.start()

    # Start sniffing
    print(f"Sniffing on {args.iface}.\nChannels: {chans}.\nScanning time per channel={args.dwell} s.\nWriting to {args.out} every {args.write_interval} s")
    if args.measure_noise:
        print("Noise level measurement: ENABLED")
    packet_count = 0
    try:
        timeout = args.duration if args.duration > 0 else None

        sniff(
            iface=args.iface,
            prn=lambda p: packet_handler(p, lambda: current_channel["ch"], args.measure_noise),
            store=False,
            timeout=timeout)
    except KeyboardInterrupt:
        pass
    finally:
        running_flag["run"] = False
        time.sleep(0.5)
        with attention_lock:
            rows = buffer[:]
            buffer.clear()
        if rows:
            connection = init_db(args.out)
            label = os.path.splitext(os.path.basename(args.out))[0]
            insert_rows(connection, rows, label)
            connection.close()
        print("Stopped. Output:", args.out)

if __name__ == "__main__":
    main()
