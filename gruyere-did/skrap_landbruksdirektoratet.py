"""
Laster ned Landbruksdirektoratets «Markedsrapport» (2012–2025) og trekker ut tall for ost:
norsk ost solgt i Norge, import av ost og importandel.

Bruk (fra mappen gruyere-did/, med nettilgang til landbruksdirektoratet.no):

    python3 skrap_landbruksdirektoratet.py last-ned            # finner og laster ned PDF-ene
    python3 skrap_landbruksdirektoratet.py ekstraher           # leser PDF-ene og lager uttrekksfiler
    python3 skrap_landbruksdirektoratet.py fyll-inn --bekreft  # skriver forslaget til data/manuelt_norsk_ost.csv

Krever: requests, beautifulsoup4, pdfplumber  (pip install requests beautifulsoup4 pdfplumber)

Hvert tall i uttrekket får med seg rapport, side og tekstutdrag, slik at det kan kontrolleres mot PDF-en.
Les gjennom data/landbruksdirektoratet/forslag_norsk_ost.csv før du kjører fyll-inn: rapportene endrer
oppsett mellom årene, og det automatiske uttrekket er en hjelp, ikke en fasit.
"""

import argparse
import csv
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "data" / "landbruksdirektoratet"
PDF_DIR = OUT / "pdf"
BASE = "https://www.landbruksdirektoratet.no"
HEADERS = {"User-Agent": "Mozilla/5.0 (forskning; osteelastisitet; kontakt via Oslo Economics)"}
PAUSE_S = 1.5  # høflig pause mellom forespørsler

# Kjente PDF-adresser (fra søk 3. oktober 2026). Rapport for år X publiseres normalt i mars år X+1.
SEED_URLS = {
    2019: "https://www.regjeringen.no/contentassets/134748123b43458e888dd7ff6bed10b2/markedsrapport--2019.pdf",
    2020: BASE + "/nb/filarkiv/rapporter/Markedsrapport%202020.pdf/_/attachment/inline/"
          "c6a8882c-e7b8-475e-b131-b761674027e1:f3205e4c9c9189eb2699b9812cdc6cddff35d9e0/"
          "Markedsrapport%202020%20-%20oppdatert%2016.03.21.pdf",
    2021: BASE + "/nb/filarkiv/rapporter/Markedsrapport%202021_Markeds-%20og%20prisvurderinger%20av%20sentrale%20"
          "norske%20landbruksvarer%20og%20R%C3%85K-varer.pdf/_/attachment/inline/"
          "36c6d5df-bbc8-4a21-bdc3-1253ba12f1dc:de99a08bea2aad9e866636775deec0965e4b5cd7/"
          "Markedsrapport%202021_Markeds-%20og%20prisvurderinger%20av%20sentrale%20norske%20landbruksvarer%20og%20"
          "R%C3%85K-varer.pdf",
    2023: BASE + "/nb/nyhetsrom/rapporter/markedsrapport-2023/_/attachment/inline/"
          "e76d4b6a-c5e6-4501-883a-7baabc38f82a:c634d86138f6a78d8e4d6fa281e7ab21fc14eef0/"
          "Markedsrapport%202023%20Rapport%202024%203.pdf",
    2024: BASE + "/nb/filarkiv/rapporter/Markedsrapport%202024%20Rapport%203%202025%20II.pdf/_/attachment/inline/"
          "7eab5aa7-6aec-4aa9-85c8-a0439e47d85d:56aeb815a4ab5ee29f89150c0499d7aa2acd0aab/"
          "Markedsrapport%202024%20Rapport%203%202025%20II.pdf",
    2025: BASE + "/nb/filarkiv/rapporter/Markedsrapport%202025%20Rapport%202026%202%2003.03.26.pdf/_/attachment/inline/"
          "a7c6286b-6686-4c3f-931c-7d82b2deb400:4b43402debb0075e72235e4df7f7fe8b4990b678/"
          "Markedsrapport%202025%20Rapport%202026%202%2003.03.26.pdf",
}
# Egne tillegg: én linje per rapport, «år url», i data/landbruksdirektoratet/urls.txt (overstyrer alt annet).
URL_FILE = OUT / "urls.txt"


# --------------------------------------------------------------------------------------
# Nedlasting
# --------------------------------------------------------------------------------------
def _session():
    import requests

    s = requests.Session()
    s.headers.update(HEADERS)
    return s


def _pdf_links(html, page_url, year):
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = urljoin(page_url, a["href"])
        text = (a.get_text(" ") + " " + href).lower()
        if ".pdf" in href.lower() and "markedsrapport" in text.replace("%20", " ") and str(year) in text:
            links.append(href)
    return links


def _report_pages(html, page_url):
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    return [urljoin(page_url, a["href"]) for a in soup.find_all("a", href=True)
            if "markedsrapport" in a["href"].lower() and ".pdf" not in a["href"].lower()]


def discover(year, s):
    """Prøver kjente sidemønstre og nettstedets søk for å finne PDF-en for et gitt rapportår."""
    candidates = [
        f"{BASE}/nb/nyhetsrom/rapporter/markedsrapport-{year}",
        f"{BASE}/nb/nyhetsrom/rapporter/markedsrapport-for-{year}",
        f"{BASE}/nb/statistikk-og-utviklingstrekk/utvikling-i-jordbruket/markedsrapport-{year}",
    ]
    for url in candidates:
        try:
            r = s.get(url, timeout=30)
            time.sleep(PAUSE_S)
        except Exception as e:  # noqa: BLE001
            print(f"  {year}: {url} feilet ({e.__class__.__name__})")
            continue
        if r.ok:
            links = _pdf_links(r.text, url, year)
            if links:
                return links[0]
    try:
        r = s.get(f"{BASE}/nb/sok", params={"q": f"markedsrapport {year}"}, timeout=30)
        time.sleep(PAUSE_S)
        if r.ok:
            links = _pdf_links(r.text, r.url, year)
            if links:
                return links[0]
            for page in _report_pages(r.text, r.url)[:5]:
                if str(year) not in page:
                    continue
                rp = s.get(page, timeout=30)
                time.sleep(PAUSE_S)
                links = _pdf_links(rp.text, page, year) if rp.ok else []
                if links:
                    return links[0]
    except Exception as e:  # noqa: BLE001
        print(f"  {year}: søk feilet ({e.__class__.__name__})")
    return None


def read_url_file():
    urls = {}
    if URL_FILE.exists():
        for line in URL_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                y, u = line.split(maxsplit=1)
                urls[int(y)] = u
    return urls


def cmd_download(args):
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    s = _session()
    urls = {**SEED_URLS, **read_url_file()}
    log = []
    for year in range(args.fra, args.til + 1):
        target = PDF_DIR / f"markedsrapport_{year}.pdf"
        if target.exists() and not args.på_nytt:
            print(f"{year}: finnes allerede")
            log.append((year, "finnes", target.name, ""))
            continue
        url = urls.get(year) or discover(year, s)
        if not url:
            print(f"{year}: fant ingen PDF – legg inn adressen i {URL_FILE.relative_to(ROOT)}")
            log.append((year, "ikke funnet", "", ""))
            continue
        try:
            r = s.get(url, timeout=120)
            time.sleep(PAUSE_S)
        except Exception as e:  # noqa: BLE001
            print(f"{year}: nedlasting feilet ({e.__class__.__name__}: {e})")
            log.append((year, "feilet", "", url))
            continue
        if not r.ok or not r.content.startswith(b"%PDF"):
            print(f"{year}: svaret er ikke en PDF (HTTP {r.status_code})")
            log.append((year, f"HTTP {r.status_code}", "", url))
            continue
        target.write_bytes(r.content)
        print(f"{year}: lastet ned {len(r.content) / 1e6:.1f} MB")
        log.append((year, "lastet ned", target.name, url))
    with open(OUT / "nedlastingslogg.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["rapportaar", "status", "fil", "url"])
        w.writerows(log)


# --------------------------------------------------------------------------------------
# Uttrekk
# --------------------------------------------------------------------------------------
YEAR_RE = re.compile(r"\b(19[89]\d|20[0-4]\d)\b")
# Tall med mellomrom/hardt mellomrom som tusenskille og komma som desimaltegn: «95 518», «15,5», «1 756»
NUM_RE = re.compile(r"(?<![\d,])-?\d{1,3}(?:[   ]\d{3})+(?:,\d+)?(?![\d])|(?<![\d,])-?\d+(?:,\d+)?(?![\d])")


def parse_num(s):
    s = s.replace(" ", "").replace(" ", "").replace(" ", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def numbers(line):
    return [parse_num(m.group()) for m in NUM_RE.finditer(line)]


def label_of(line):
    m = NUM_RE.search(line)
    return (line[: m.start()] if m else line).strip(" .:-–")


CHEESE_RE = re.compile(r"\bost(er|en|ene)?\b|\bfaste og halvfaste\b|\bgulost", re.I)

# Setningsmønstre for nøkkeltall i løpende tekst
SENTENCE_PATTERNS = {
    "norsk_ost_solgt_tonn": re.compile(
        r"(?:solgt|salg(?:et)?\s+av|omsatt|omsetning(?:en)?\s+av)[^.]{0,80}?norsk(?:produsert)?e?\s+ost[^.]{0,80}?"
        r"(\d{1,3}(?:[   ]\d{3})+|\d{4,6})\s*tonn"
        r"|(?:solgt|omsatt)\s+(\d{1,3}(?:[   ]\d{3})+|\d{4,6})\s*tonn\s+norsk(?:produsert)?e?\s+ost", re.I),
    "import_ost_tonn": re.compile(
        r"import(?:en|ert[e]?)?\s+(?:av\s+)?ost[^.]{0,80}?(\d{1,3}(?:[   ]\d{3})+|\d{4,6})\s*tonn", re.I),
    "importandel_ost_prosent": re.compile(
        r"(?:markedsandel|importandel)[^.]{0,80}?(?:ost|importert)[^.]{0,60}?(\d{1,2}(?:,\d)?)\s*(?:prosent|%)"
        r"|(?:importert\s+ost)[^.]{0,80}?(?:markedsandel|andel)[^.]{0,60}?(\d{1,2}(?:,\d)?)\s*(?:prosent|%)", re.I),
}


def extract_pdf(path, report_year):
    import pdfplumber

    rows = []
    with pdfplumber.open(path) as pdf:
        for pno, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            if not CHEESE_RE.search(text):
                continue
            flat = re.sub(r"\s+", " ", text)

            # 1) Setninger i løpende tekst
            for field, pat in SENTENCE_PATTERNS.items():
                for m in pat.finditer(flat):
                    val = next(g for g in m.groups() if g)
                    snippet = flat[max(0, m.start() - 60): m.end() + 40]
                    yrs = [int(y) for y in YEAR_RE.findall(flat[max(0, m.start() - 200): m.end()])]
                    rows.append(dict(rapportaar=report_year, side=pno, metode="setning", felt=field,
                                     etikett="", dataaar=(yrs[-1] if yrs else report_year),
                                     verdi=parse_num(val), utdrag=snippet))

            # 2) Tabeller som pdfplumber gjenkjenner
            for table in page.extract_tables() or []:
                rows += _from_table(table, report_year, pno)

            # 3) Tabeller som bare finnes som tekstlinjer: en linje med årstall etterfulgt av rader
            lines = text.splitlines()
            for i, line in enumerate(lines):
                yrs = [int(y) for y in YEAR_RE.findall(line)]
                if len(yrs) < 3 or len(numbers(line)) != len(yrs):
                    continue
                for nxt in lines[i + 1: i + 25]:
                    lab, vals = label_of(nxt), numbers(nxt)
                    if YEAR_RE.findall(nxt) and len(YEAR_RE.findall(nxt)) >= 3:
                        break
                    if len(vals) >= len(yrs) and CHEESE_RE.search(lab):
                        for y, v in zip(yrs, vals[-len(yrs):]):
                            rows.append(dict(rapportaar=report_year, side=pno, metode="tekstlinje",
                                             felt=_classify(lab), etikett=lab, dataaar=y, verdi=v, utdrag=nxt.strip()))
    return rows


def _from_table(table, report_year, pno):
    out = []
    header_idx, yrs = None, []
    for i, row in enumerate(table):
        cells = [c or "" for c in row]
        found = [(j, int(YEAR_RE.search(c).group())) for j, c in enumerate(cells) if YEAR_RE.fullmatch(c.strip() or "x")]
        if len(found) >= 3:
            header_idx, yrs = i, found
            break
    if header_idx is None:
        return out
    for row in table[header_idx + 1:]:
        cells = [c or "" for c in row]
        lab = " ".join(c for c in cells[: yrs[0][0]] if c).strip()
        if not CHEESE_RE.search(lab):
            continue
        for j, y in yrs:
            if j < len(cells):
                v = parse_num(cells[j].strip())
                if v is not None:
                    out.append(dict(rapportaar=report_year, side=pno, metode="tabell", felt=_classify(lab),
                                    etikett=lab, dataaar=y, verdi=v, utdrag=" | ".join(cells)))
    return out


def _classify(label):
    l = label.lower()
    if "import" in l and ("andel" in l or "%" in l or "prosent" in l):
        return "importandel_ost_prosent"
    if "import" in l:
        return "import_ost_tonn"
    if "norsk" in l or "innenlandsk" in l or "salg" in l or "solgt" in l or "omsetning" in l:
        return "norsk_ost_solgt_tonn"
    return "annet_ost"


def cmd_extract(args):
    pdfs = sorted(PDF_DIR.glob("markedsrapport_*.pdf"))
    if not pdfs:
        sys.exit(f"Ingen PDF-er i {PDF_DIR.relative_to(ROOT)}. Kjør «last-ned» først.")
    all_rows = []
    for p in pdfs:
        year = int(re.search(r"(\d{4})", p.stem).group(1))
        rows = extract_pdf(p, year)
        print(f"{p.name}: {len(rows)} treff")
        all_rows += rows
    fields = ["rapportaar", "side", "metode", "felt", "etikett", "dataaar", "verdi", "utdrag"]
    with open(OUT / "uttrekk_ost.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(all_rows)

    # Forslag: for hvert dataår velges verdien fra den nyeste rapporten (tar med revisjoner).
    # Tabelltreff foretrekkes framfor tekstlinjer, som igjen foretrekkes framfor setninger.
    rank = {"tabell": 0, "tekstlinje": 1, "setning": 2}
    best = {}
    for r in all_rows:
        if r["felt"] != "norsk_ost_solgt_tonn" or r["verdi"] is None or not (1_000 <= r["verdi"] <= 500_000):
            continue
        key = r["dataaar"]
        score = (-r["rapportaar"], rank[r["metode"]])
        if key not in best or score < best[key][0]:
            best[key] = (score, r)
    with open(OUT / "forslag_norsk_ost.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["aar", "norsk_ost_solgt_tonn", "kilde", "metode", "utdrag", "antall_treff_for_aaret"])
        for y in sorted(best):
            r = best[y][1]
            n = sum(1 for x in all_rows if x["felt"] == "norsk_ost_solgt_tonn" and x["dataaar"] == y)
            w.writerow([y, int(round(r["verdi"])), f"Markedsrapport {r['rapportaar']} s. {r['side']}",
                        r["metode"], r["utdrag"][:200], n])
    print(f"\nSkrev {OUT.relative_to(ROOT)}/uttrekk_ost.csv ({len(all_rows)} rader) og forslag_norsk_ost.csv "
          f"({len(best)} år). Kontroller forslaget mot PDF-ene før «fyll-inn».")


def cmd_fill(args):
    src = OUT / "forslag_norsk_ost.csv"
    dst = ROOT / "data" / "manuelt_norsk_ost.csv"
    if not src.exists():
        sys.exit("Fant ikke forslag_norsk_ost.csv. Kjør «ekstraher» først.")
    with open(src) as f:
        forslag = {int(r["aar"]): r for r in csv.DictReader(f)}
    header = [l for l in dst.read_text().splitlines() if l.startswith("#")]
    with open(dst) as f:
        body = [r for r in csv.DictReader(l for l in f if not l.startswith("#"))]
    changed = 0
    for r in body:
        y = int(r["aar"])
        if y in forslag and (args.overskriv or not r["norsk_ost_solgt_tonn"]):
            r["norsk_ost_solgt_tonn"] = forslag[y]["norsk_ost_solgt_tonn"]
            r["kilde"] = forslag[y]["kilde"] + " (automatisk uttrekk, kontrollert)"
            changed += 1
    if not args.bekreft:
        print(f"Tørrkjøring: {changed} år ville blitt fylt inn. Kjør med --bekreft for å skrive.")
        return
    with open(dst, "w", newline="") as f:
        f.write("\n".join(header) + "\n")
        w = csv.DictWriter(f, fieldnames=["aar", "norsk_ost_solgt_tonn", "kilde"])
        w.writeheader()
        w.writerows(body)
    print(f"Fylte inn {changed} år i {dst.relative_to(ROOT)}. Kjør analyse.py på nytt.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("last-ned", help="finn og last ned markedsrapportene")
    d.add_argument("--fra", type=int, default=2012)
    d.add_argument("--til", type=int, default=2025)
    d.add_argument("--på-nytt", dest="på_nytt", action="store_true", help="last ned selv om filen finnes")
    sub.add_parser("ekstraher", help="trekk ut tall for ost fra nedlastede PDF-er")
    fi = sub.add_parser("fyll-inn", help="skriv forslaget til data/manuelt_norsk_ost.csv")
    fi.add_argument("--bekreft", action="store_true", help="skriv til fil (uten dette: tørrkjøring)")
    fi.add_argument("--overskriv", action="store_true", help="overskriv år som allerede har verdi")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    {"last-ned": cmd_download, "ekstraher": cmd_extract, "fyll-inn": cmd_fill}[args.cmd](args)


if __name__ == "__main__":
    main()
