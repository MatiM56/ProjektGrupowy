import time
import threading
import sqlite3
import os
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
# Klucz sesji Flaska - ustawiany przez zmienna srodowiskowa, patrz .env.example
app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

DB_PATH = os.environ.get('WYNIKI_DB', '/home/user/algorytm/wyniki.db')

def sqlite_polling_thread():
    """Wątek monitorujący najnowsze lokalizacje malinek bezpośrednio z SQLite"""
    last_seen_id = 0 

    while True:
        if os.path.exists(DB_PATH):
            try:
                conn = sqlite3.connect(DB_PATH)
                conn.row_factory = sqlite3.Row 
                cursor = conn.cursor()
                
                cursor.execute("SELECT MAX(id) FROM lokalizacja")
                current_max_id = cursor.fetchone()[0]

                if current_max_id and current_max_id > last_seen_id:
                    query = """
                        SELECT t1.id_raspberyy, t1.punkt, t1.timestamp 
                        FROM lokalizacja t1
                        WHERE t1.id IN (
                            SELECT MAX(id)
                            FROM lokalizacja
                            GROUP BY id_raspberyy
                        )
                    """
                    cursor.execute(query)
                    
                    results = [dict(row) for row in cursor.fetchall()]
                    
                    if results:
                        for row in results:
                            if row['timestamp']:
                                row['timestamp'] = str(row['timestamp'])[:19]
                        
                        socketio.emit('update_map', results)
                        print(f"Przesłano pozycje dla: {[r['id_raspberyy'] for r in results]}")
                        
                        last_seen_id = current_max_id

                cursor.close()
                conn.close()
            except Exception as e:
                print(f"Błąd bazy danych SQLite: {e}")
        else:
            print(f"Oczekiwanie na utworzenie bazy danych: {DB_PATH}")
            
        socketio.sleep(1)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.start_background_task(sqlite_polling_thread)
    
    socketio.run(app, host="0.0.0.0", port=5000, debug=False, allow_unsafe_werkzeug=True)
