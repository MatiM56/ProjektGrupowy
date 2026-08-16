# Archiwum

Wcześniejsze warianty skryptów i podejść, zachowane dla historii projektu.
**Nie są częścią działającego systemu** — kod produkcyjny znajduje się w `raspberry/`, `server/`, `algorithm/` i `map/`.

| Katalog | Co to jest |
|---|---|
| `sniffer-warianty/` | dwie wersje sniffera dopasowane do konkretnych kart sieciowych (`eeffd4`, `eeffe9`) — różnią się nazwą interfejsu w `iw dev` na RPi; dodatkowo wczesne wersje `mapa.py` i `wykresy.py` oraz skrypty do ręcznego pobierania baz |
| `skrypty-pomiarowe/` | skrypty `scp` do ściągania pomiarów z RPi na komputer, używane podczas kampanii pomiarowych |
| `algorytm-cpp/` | pierwsze podejście do algorytmu dopasowującego w C++ (Visual Studio) — porzucone na rzecz wersji w Pythonie; zachowany sam kod źródłowy i roboczy schemat |

Skrypty `sciaganie_db.sh` / `sciaganie_db.bat` / `scp.sh` / `scp.bat` pierwotnie miały hasło do RPi wpisane
na sztywno. Zostało usunięte — hasło pobierane jest ze zmiennej środowiskowej `RPI_PWD`.
