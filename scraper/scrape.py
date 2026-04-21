#!/usr/bin/env python3
"""
Scraper cien pohonných hmôt – METRO Žilina & Tesco Žilina
Spúšťa sa automaticky cez GitHub Actions každý deň.
"""

import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("pip install requests beautifulsoup4")
    sys.exit(1)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

DATA_FILE = Path(__file__).parent.parent / "data" / "prices.json"


# ── Metro Žilina ──────────────────────────────────────────────────────────────

def scrape_metro() -> dict:
    url = "https://www.metro.sk/predajne/zilina"
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text(separator="\n")
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    targets = {"Natural 95": None, "Nafta diesel": None}

    for i, line in enumerate(lines):
        for name in targets:
            if name.lower() in line.lower() and targets[name] is None:
                # Hľadáme číslo v nasledujúcich riadkoch
                window = " ".join(lines[i: i + 6])
                m = re.search(r"\b(\d+[,\.]\d+)\b", window)
                if m:
                    targets[name] = float(m.group(1).replace(",", "."))

    return {
        "metro_natural95": targets["Natural 95"],
        "metro_diesel":    targets["Nafta diesel"],
    }


# ── Tesco Žilina ──────────────────────────────────────────────────────────────

def scrape_tesco() -> dict:
    url = (
        "https://www.tesco.sk/help/pages/dokumenty/"
        "ostatne-dokumenty/aktualne-ceny-pohonnych-hmot"
    )
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table")

    if not table:
        raise ValueError("Tabuľka na Tesco stránke nebola nájdená.")

    # Zistíme indexy stĺpcov z hlavičky
    headers = [th.get_text(strip=True).upper() for th in table.find_all("th")]
    try:
        nat_idx    = next(i for i, h in enumerate(headers) if "NATURAL 95" in h and "PLUS" not in h)
        diesel_idx = next(i for i, h in enumerate(headers) if h == "DIESEL")
    except StopIteration:
        raise ValueError(f"Stĺpce nenájdené. Hlavičky: {headers}")

    # Nájdeme riadok Žilina
    for row in table.find_all("tr"):
        cells = row.find_all("td")
        if not cells:
            continue
        if "žilina" in cells[0].get_text(strip=True).lower():
            def parse(cell):
                val = cell.get_text(strip=True).replace(",", ".")
                try:
                    return float(val)
                except ValueError:
                    return None

            return {
                "tesco_natural95": parse(cells[nat_idx]),
                "tesco_diesel":    parse(cells[diesel_idx]),
            }

    raise ValueError("Riadok Žilina nebol nájdený v tabuľke.")


# ── Uloženie dát ─────────────────────────────────────────────────────────────

def load_data() -> list:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return []


def save_data(records: list) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def main():
    today = date.today().isoformat()
    print(f"📅 Dátum: {today}")

    records = load_data()

    # Ak už dnes existuje záznam, prepíšeme ho (aktualizácia)
    records = [r for r in records if r.get("date") != today]

    print("⛽ Scraping Metro Žilina...")
    metro = scrape_metro()
    print(f"   Natural 95: {metro['metro_natural95']} EUR/l")
    print(f"   Nafta:      {metro['metro_diesel']} EUR/l")

    print("🛒 Scraping Tesco Žilina...")
    tesco = scrape_tesco()
    print(f"   Natural 95: {tesco['tesco_natural95']} EUR/l")
    print(f"   Diesel:     {tesco['tesco_diesel']} EUR/l")

    record = {"date": today, **metro, **tesco}
    records.append(record)

    # Zoradiť podľa dátumu
    records.sort(key=lambda r: r["date"])

    save_data(records)
    print(f"✅ Uložené do {DATA_FILE}  ({len(records)} záznamov celkom)")


if __name__ == "__main__":
    main()
