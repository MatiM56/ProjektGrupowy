# Praca z repozytorium

## Konfiguracja jednorazowa

```bash
git config --global user.name "Imię Nazwisko"
git config --global user.email "sXXXXXX@student.pg.edu.pl"
git clone https://github.com/MatiM56/ProjektGrupowy.git
cd ProjektGrupowy
cp .env.example .env    # uzupełnij własnymi danymi dostępowymi
```

Do logowania przy `git push` GitHub wymaga **Personal Access Token** zamiast hasła:
Settings → Developer settings → Personal access tokens → Fine-grained tokens → uprawnienie *Contents: Read and write*.
Token wklejasz w miejsce hasła przy pierwszym pushu.

## Codzienna praca

```bash
git pull                          # pobierz zmiany innych
git switch -c nazwa-zmiany        # gałąź robocza na czas jednej zmiany
# ... praca ...
git add <pliki>
git commit -m "Krótki opis zmiany"
git push -u origin nazwa-zmiany
```

Następnie na GitHubie otwórz **Pull Request** do `main`, poproś kogoś z zespołu o przejrzenie i scal.

## Zasady

1. **Gałąź to zmiana, nie moduł.** Podział na części systemu realizują katalogi (`raspberry/`, `server/`,
   `algorithm/`, …), a nie osobne gałęzie. Gałąź żyje tyle, ile trwa jedna zmiana, i po scaleniu jest usuwana.
2. **Żadnych haseł, tokenów ani kluczy w kodzie.** Wszystko wrażliwe trafia do `.env` (ignorowanego przez gita).
   Nową zmienną dopisz do `.env.example` z wartością zastępczą.
3. **Bez plików generowanych.** `__pycache__/`, `wyniki.db`, katalogi `archive/`, pliki `.vs/` — pilnuje tego `.gitignore`.
4. **Duże dane.** Pojedyncze pomiary referencyjne trzymamy w `data/`. Całe kampanie pomiarowe (dziesiątki MB)
   dołączamy jako GitHub Release, nie jako commit.
5. **Commit opisuje zmianę.** „Poprawa czytania kanałów w snifferze" zamiast „update", „poprawki", „zmiany".

## Współautorstwo commita

Gdy nad zmianą pracowało kilka osób, dopisz na końcu treści commita (po pustej linii):

```
Co-authored-by: Imię Nazwisko <sXXXXXX@student.pg.edu.pl>
```

GitHub pokaże wtedy wszystkie osoby jako autorów commita.
