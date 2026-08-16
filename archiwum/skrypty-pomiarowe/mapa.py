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

# --- Utilities to set channel ---
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
        rt = packet.getlayer(RadioTap)
        if hasattr(rt, "dBm_AntSignal") and rt.dBm_AntSignal is not None:
            return int(rt.dBm_AntSignal)
        if hasattr(rt, "dBm_AntNoise") and rt.dBm_AntNoise is not None:
            return int(rt.dBm_AntNoise)
    return None

attention_lock = threading.Lock()
buffer = []

def packet_handler(packet, current_channel_getter):
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
    row = {
        "timestamp": timestamp,
        "bssid": bssid or "",
        "type": type_,
        "subtype": subtype,
        "ssid": ssid,
        "rssi": rssi if rssi is not None else "",
        "channel": ch
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
    # Upewnij się, że istnieje kolumna na etykietę miejsca.
    cursor.execute("PRAGMA table_info(packets)")
    cols = [row[1] for row in cursor.fetchall()]
    if "label" not in cols:
        cursor.execute("ALTER TABLE packets ADD COLUMN label TEXT")
    connection.commit()
    return connection


def insert_rows(connection, rows, label):
    if not rows:
        return
    cursor = connection.cursor()
    cursor.executemany(
        "INSERT OR REPLACE INTO packets (timestamp, bssid, type, subtype, ssid, rssi, channel, label) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
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
            )
            for r in rows
        ],
    )
    connection.commit()


def writer_thread(db_path, write_interval, running_flag):
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
    parser = argparse.ArgumentParser(description="Scapy channel hopper with SQLite logging")
    parser.add_argument("--iface", required=True, help="monitor-mode interface")
    parser.add_argument("--channels", default="1,6,11", help="comma-separated channels (e.g. 1,6,11 or 1-13)")
    parser.add_argument("--dwell", type=float, default=0.25, help="dwell time per channel in seconds (default 0.25)")
    parser.add_argument("--write-interval", type=float, default=2.0, help="flush database every N seconds (default 2)")
    parser.add_argument("--out", default="scapy_scan.db", help="output SQLite database file")
    parser.add_argument("--duration", type=float, default=10, help="optional: stop after this many seconds (0 = infinite)")
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
    writer = threading.Thread(target=writer_thread, args=(args.out, args.write_interval, running_flag), daemon=True)
    writer.start()

    # Start sniffing
    print(f"Sniffing on {args.iface}. Channels: {chans}. Dwell={args.dwell}s. Writing to {args.out} every {args.write_interval}s")
    packet_count = 0
    try:
        timeout = args.duration if args.duration > 0 else None

        sniff(
            iface=args.iface,
            prn=lambda p: packet_handler(p, lambda: current_channel["ch"]),
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
