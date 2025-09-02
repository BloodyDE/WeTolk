# WeTolk

> Internes Knowledge- & Ticket-System auf **Django**-Basis – mit strukturierten Eingaben, Tags, Suche, Kommentaren und Dateianhang‑Vorschau.

[![Python](https://img.shields.io/badge/Python-3.13.5-3776AB?logo=python\&logoColor=white)](https://www.python.org/downloads/release/python-3135/)
[![Django](https://img.shields.io/badge/Django-5.2.x-0C4B33?logo=django\&logoColor=white)](https://docs.djangoproject.com/en/5.2/)
[![License](https://img.shields.io/badge/License-TBD-lightgrey.svg)](./LICENSE)

> **Kurzfassung:** WeTolk hilft Teams, Wissen/Tickets klar zu erfassen, zu taggen, zu durchsuchen und zu diskutieren. Dateien können angehängt und – wo möglich – direkt in der Oberfläche vorab angesehen werden.

---

## Inhaltsverzeichnis

* [Features](#features)
* [Screenshots](#screenshots)
* [Tech‑Stack](#tech-stack)
* [Schnellstart](#schnellstart)
* [Konfiguration (\_.env\_)](#konfiguration-env)
* [Datenbank & Migrations](#datenbank--migrations)
* [Tests](#tests)
* [Projektstruktur](#projektstruktur)
* [Deployment (Kurz)](#deployment-kurz)
* [Troubleshooting](#troubleshooting)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [Lizenz](#lizenz)

---

## Features

* 🧾 **Strukturierte Knowledge‑Einträge / Tickets**
  Rollen, Kategorien, Subkategorien, Projekttypen, Titel, Beschreibung, Impact u. a.
* 🔖 **Tags mit Autocomplete**
  Bequeme Schlagwort‑Eingabe (z. B. via Tagify).
* 🔎 **Suche & Filter**
  u. a. nach **Titel** und **Tags**.
* 💬 **Kommentare**
  Ticket‑basierte Diskussion/Notizen.
* 📎 **Dateianhänge mit Vorschau**
  Bilder und – wo sinnvoll – PDFs direkt in der UI sichtbar.
* 🔐 **Login & Rechte**
  Django‑Auth + Admin‑Backend inklusive.
* ⚙️ **.env‑Konfiguration**
  Simple Umschaltung DEV/PROD und optionale Download‑/Export‑Funktionen.

---

## Screenshots

> Siehe `docs/screenshots/`. (Platzhalter – bitte Bilder ergänzen.)

* Ticketliste – Filter & Suche
  `docs/screenshots/ticket-list.png`
* Ticketdetail – Kommentare & Anhänge
  `docs/screenshots/ticket-detail.png`
* Admin – Modelle/Benutzer
  `docs/screenshots/admin.png`

---

## Tech‑Stack

* **Backend:** Django (5.2.x)
* **DB (dev):** SQLite (Default)
  **DB (prod, optional):** PostgreSQL via `DATABASE_URL`
* **Auth:** Django Authentication + Admin
* **Frontend:** Django Templates (mit Widget Tweaks/Tagify, sofern eingebunden)

---

## Schnellstart

**Voraussetzungen:** Python **3.13.5**, `pip`

```bash
# 1) Repo klonen
git clone https://github.com/BloodyDE/WeTolk.git
cd WeTolk

# 2) Virtuelle Umgebung
# Windows
py -3.13 -m venv .venv && .\.venv\Scripts\activate
# macOS/Linux
python3.13 -m venv .venv && source .venv/bin/activate

# 3) Abhängigkeiten
pip install --upgrade pip
pip install -r requirements.txt

# 4) .env anlegen (siehe unten) – Beispiel kopieren
# Windows
copy .env.example .env
# macOS/Linux
cp .env.example .env

# 5) DB migrieren & Admin-User anlegen
python manage.py migrate
python manage.py createsuperuser

# 6) Dev-Server starten
python manage.py runserver

# → http://127.0.0.1:8000/
```

---

## Konfiguration (*`.env`*)

**Minimal nötig:** `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`
**Optional:** `DATABASE_URL`, `DOWNLOAD_PASSWORD`, `DOWNLOAD_DB_PATH`, `MEDIA_ROOT`, `STATIC_ROOT`

**Beispiel (`.env.example`):**

```dotenv
# Sicherheit
SECRET_KEY=please-change-me
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Datenbank (Standard: SQLite)
# Für PostgreSQL via django-environ, z. B.:
# DATABASE_URL=postgres://user:pass@localhost:5432/wetolk

# Uploads/Static (optional, Prod)
# MEDIA_ROOT=/var/www/wetolk/media
# STATIC_ROOT=/var/www/wetolk/static

# Optionale Download-/Export-Funktionen
DOWNLOAD_PASSWORD=CHANGE_ME
DOWNLOAD_DB_PATH=db.sqlite3
```

> **Hinweis:** In Produktion `DEBUG=False` setzen, einen langen zufälligen `SECRET_KEY` verwenden und `ALLOWED_HOSTS` passend pflegen.

---

## Datenbank & Migrations

```bash
# Änderungen an Modellen erzeugen
python manage.py makemigrations

# Migrations anwenden
python manage.py migrate

# (optional) Beispiel-/Startdaten
# python manage.py loaddata initial_data.json
```

---

## Tests

```bash
# pytest (falls konfiguriert)
pytest -q

# Django-Tests
python manage.py test
```

---

## Projektstruktur

```text
WeTolk/
├─ manage.py
├─ requirements.txt
├─ .env.example
├─ ticket_system/              # Django Projekt (Settings, URLs, WSGI/ASGI)
│  ├─ settings.py
│  ├─ urls.py
│  └─ ...
├─ tickets/                    # App: Tickets/Knowledge
│  ├─ models.py
│  ├─ forms.py
│  ├─ views.py
│  ├─ urls.py
│  └─ templates/tickets/
├─ WeConvert/                  # (optional) Konvert-/Vorschau-Funktionen
│  └─ ...
└─ docs/
   └─ screenshots/
```

---

## Deployment (Kurz)

1. **Umgebung setzen:** `DEBUG=False`, `SECRET_KEY`, `ALLOWED_HOSTS`, `DATABASE_URL` (z. B. PostgreSQL)
2. **Abhängigkeiten installieren:** `pip install -r requirements.txt`
3. **Migrations:** `python manage.py migrate`
4. **Static Files sammeln:** `python manage.py collectstatic`
5. **Server starten:**

   * WSGI (z. B. gunicorn) oder ASGI (z. B. uvicorn/daphne) hinter Nginx/Apache
6. **Medien/Backups:** `MEDIA_ROOT` schreiben, DB‑Backups planen

> Tipp: Für einfache Setups funktioniert **Whitenoise** für statische Dateien unter WSGI gut.

---

## Troubleshooting

* **`ImproperlyConfigured: SECRET_KEY not set`** → `.env` prüfen, Key setzen.
* **Migrationen fehlen/konfliktieren** → `makemigrations` + `migrate` ausführen; bei Konflikten Branch‑Stand prüfen.
* **Static Files 404 in Prod** → `collectstatic`, Webserver‑Konfig (Nginx/Apache) und ggf. Whitenoise checken.
* **Dateivorschau zeigt nichts** → Dateityp unterstützen / Browser‑Konsole prüfen / `WeConvert` aktiviert?

---

## Roadmap

* [ ] Kommentare: Mentions/Antworten & Edit‑History
* [ ] Volltextsuche (Titel + Beschreibung + Kommentare)
* [ ] Bessere PDF/Office‑Vorschau
* [ ] Rollen-/Rechte‑Matrix verfeinern
* [ ] REST/GraphQL‑API
* [ ] Audit‑Log & Export

---

## Contributing

1. Fork & Branch erstellen (`feature/<kurzbeschreibung>`)
2. Saubere Commits (z. B. Conventional Commits)
3. Tests ausführen (`pytest`/`manage.py test`)
4. Pull Request erstellen

---

## Lizenz

**TBD** – siehe [`LICENSE`](./LICENSE) (Platzhalter).

---

## Cheat‑Sheet (Windows, lokal)

```powershell
cd "C:\\Visual Studio Code Projekte\\Arbeit\\WeTolk"
.\.venv\Scripts\Activate.ps1
python manage.py runserver
# → http://127.0.0.1:8000/
```
