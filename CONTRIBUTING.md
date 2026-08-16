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

## Ustalenia techniczne repozytorium

- Podział systemu realizują katalogi (`raspberry/`, `server/`, `algorithm/`, …). Gałęzie służą do pracy nad
  pojedynczą zmianą i po scaleniu są usuwane.
- Dane dostępowe trzymane są w `.env`, który jest w `.gitignore`. Nową zmienną dopisz do `.env.example`
  z wartością zastępczą.
- Pliki generowane (`__pycache__/`, `wyniki.db`, `archive/`, `.vs/`) są wykluczone przez `.gitignore`.
- `.gitattributes` wymusza końcówki LF w plikach `.sh`, `.py` i `.sql` — inaczej bash na RPi zgłasza
  `bad interpreter: /bin/bash^M`.
- Pomiary referencyjne i przykładowe leżą w `data/`. Pełne kampanie pomiarowe (dziesiątki MB)
  dołączamy jako GitHub Release.

## Współautorstwo commita

Gdy nad zmianą pracowało kilka osób, dopisz na końcu treści commita (po pustej linii):

```
Co-authored-by: Imię Nazwisko <sXXXXXX@student.pg.edu.pl>
```

GitHub pokaże wtedy wszystkie osoby jako autorów commita.
