# ⛽ Ceny PHM – Metro & Tesco Žilina

Automatický tracker cien pohonných hmôt s dennou aktualizáciou a GitHub Pages webstránkou.

**Živá stránka:** `https://<tvoje-meno>.github.io/<nazov-repozitara>/`

---

## 📁 Štruktúra projektu

```
fuel-tracker/
├── .github/
│   └── workflows/
│       └── scrape.yml       ← GitHub Actions (denný cron job)
├── scraper/
│   └── scrape.py            ← Python scraper (Metro + Tesco)
├── data/
│   └── prices.json          ← Historické dáta cien
├── index.html               ← Webstránka (tabuľka + graf)
└── README.md
```

---

## 🚀 Postup nastavenia (krok za krokom)

### Krok 1 – Vytvor GitHub repozitár

1. Choď na [github.com](https://github.com) a prihlás sa
2. Klikni **New repository** (zelené tlačidlo vpravo hore)
3. Vyplň:
   - **Repository name:** `fuel-tracker` (alebo ľubovoľný názov)
   - **Visibility:** ✅ Public *(GitHub Pages funguje zadarmo len pre public repozitáre)*
4. Klikni **Create repository**

---

### Krok 2 – Nahraj súbory do repozitára

**Možnosť A – cez webový prehliadač (jednoduchšie):**

1. V repozitári klikni **Add file → Upload files**
2. Nahraj `index.html` a `data/prices.json`
3. Pre vytvorenie súboru `.github/workflows/scrape.yml`:
   - Klikni **Add file → Create new file**
   - Do poľa Name napíš: `.github/workflows/scrape.yml`
   - Skopíruj obsah súboru `scrape.yml`
4. Rovnako vytvor `scraper/scrape.py`

**Možnosť B – cez Git (odporúčané):**

```bash
git clone https://github.com/<tvoje-meno>/fuel-tracker.git
cd fuel-tracker

# Skopíruj všetky súbory z tohto balíka sem, potom:
git add .
git commit -m "🚀 Prvý commit"
git push origin main
```

---

### Krok 3 – Zapni GitHub Pages

1. V repozitári choď na **Settings** (horná lišta)
2. V ľavom menu klikni **Pages**
3. V sekcii **Source** vyber:
   - Branch: `main`
   - Folder: `/ (root)`
4. Klikni **Save**
5. Po chvíľke (1–2 min) sa objaví zelená lišta s odkazom na tvoju stránku:
   `https://<tvoje-meno>.github.io/fuel-tracker/`

---

### Krok 4 – Prvé ručné spustenie scrapera

1. V repozitári klikni na záložku **Actions**
2. V ľavom menu vyber **Scrape fuel prices**
3. Klikni **Run workflow → Run workflow** (zelené tlačidlo)
4. Počkaj ~30 sekúnd, workflow sa dokončí
5. `data/prices.json` bude aktualizovaný s dnešnými cenami

> ℹ️ Od teraz beží scraper **automaticky každý deň o 7:00 UTC** (9:00 CEST).

---

### Krok 5 – Skontroluj výsledok

Otvor svoju GitHub Pages stránku:
```
https://<tvoje-meno>.github.io/fuel-tracker/
```

Uvidíš:
- 4 karty s aktuálnymi cenami (Metro N95, Metro Diesel, Tesco N95, Tesco Diesel)
- 2 grafy s vývojom cien
- Tabuľku so všetkými historickými záznamami

---

## 🔄 Ako to funguje

```
Každý deň o 7:00
       │
       ▼
GitHub Actions spustí scraper/scrape.py
       │
       ├─► Stiahne https://www.metro.sk/predajne/zilina
       │   Extrahuje: Natural 95, Nafta diesel
       │
       ├─► Stiahne https://www.tesco.sk/help/.../aktualne-ceny-pohonnych-hmot
       │   Nájde riadok Žilina v tabuľke
       │   Extrahuje: NATURAL 95, DIESEL
       │
       └─► Pridá nový riadok do data/prices.json
           Commitne a pushne do repozitára

GitHub Pages servuje index.html
       │
       └─► index.html načíta data/prices.json
           Zobrazí karty, grafy, tabuľku
```

---

## 🛠 Lokálne testovanie scrapera

```bash
# Nainštaluj závislosti
pip install requests beautifulsoup4

# Spusti scraper
python scraper/scrape.py
```

Výstup by mal vyzerať takto:
```
📅 Dátum: 2026-04-21
⛽ Scraping Metro Žilina...
   Natural 95: 1.69 EUR/l
   Nafta:      1.77 EUR/l
🛒 Scraping Tesco Žilina...
   Natural 95: 1.699 EUR/l
   Diesel:     1.769 EUR/l
✅ Uložené do data/prices.json  (1 záznamov celkom)
```

---

## ❓ Časté problémy

| Problém | Riešenie |
|---|---|
| Stránka sa nezobrazuje | Skontroluj Settings → Pages, či je Source nastavený na `main / root` |
| Grafy sú prázdne | Spusti workflow ručne (Actions → Run workflow) |
| Scraper zlyháva | Skontroluj Actions → posledný run → logy. Webová stránka mohla zmeniť štruktúru HTML. |
| `prices.json` sa neaktualizuje | Skontroluj, či má workflow `permissions: contents: write` |

---

## 📊 Formát dát (prices.json)

```json
[
  {
    "date": "2026-04-21",
    "metro_natural95": 1.69,
    "metro_diesel": 1.77,
    "tesco_natural95": 1.699,
    "tesco_diesel": 1.769
  }
]
```

Každý deň sa pridá jeden nový záznam. Záznamy sú zoradené podľa dátumu.
