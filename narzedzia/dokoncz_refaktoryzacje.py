# -*- coding: utf-8 -*-
"""Kończy refaktoryzację: jedna dokumentacja + linki + brakujące pliki."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "dokumentacja"
DOC_PLC = DOC / "plc"
PLC = ROOT / "plc"
NARZ = ROOT / "narzedzia"


def kopia_stare() -> Path:
    solutions = Path(r"c:\Users\mbato\OneDrive\Desktop\Solutions")
    kopia = next(
        d for d in solutions.iterdir() if "kopia" in d.name.lower() and "stacja" in d.name.lower()
    )
    return kopia / "stare"


def fix_links(text: str) -> str:
    repl = {
        "../05_techniczna/dokumentacja_techniczna.md": "techniczna.md",
        "docs/dokumentacja_techniczna.md": "techniczna.md",
        "dokumentacja_techniczna.md": "techniczna.md",
        "../04_plc/mapowanie_IO_rejestrow.md": "plc/mapowanie.md",
        "mapowanie_IO_rejestrow.md": "plc/mapowanie.md",
        "mapowanie_PLC.md": "plc/mapowanie.md",
        "../04_plc/instrukcja_programowania.md": "plc/program.md",
        "instrukcja_programowania.md": "plc/program.md",
        "../04_plc/informacje_o_programie.md": "plc/program.md",
        "informacje_o_programie.md": "plc/program.md",
        "../04_plc/audyt_i_rekomendacje.md": "plc/audyt.md",
        "audyt_i_rekomendacje.md": "plc/audyt.md",
        "../04_plc/lista_sieci.md": "plc/lista_sieci.md",
        "../04_plc/indeks_krzyzowy.md": "plc/indeks_krzyzowy.md",
        "../04_plc/procedury_plc.md": "plc/program.md",
        "../06_receptury/profile_opakowan.md": "receptury.md",
        "profile_opakowan.md": "receptury.md",
        "01_maszyna/charakterystyka.md": "maszyna.md",
        "01_maszyna/proces_technologiczny.md": "maszyna.md",
        "proces_technologiczny.md": "maszyna.md",
        "charakterystyka.md": "maszyna.md",
        "02_operator/instrukcja_uzytkownika.md": "operator.md",
        "instrukcja_uzytkownika.md": "operator.md",
        "03_serwis/instrukcja_serwisanta.md": "serwis.md",
        "instrukcja_serwisanta.md": "serwis.md",
        "03_serwis/procedury_diagnostyczne.md": "serwis.md#skrot-procedur-diagnostycznych",
        "procedury_diagnostyczne.md": "serwis.md#skrot-procedur-diagnostycznych",
        "dokumentacja/04_plc/": "dokumentacja/plc/",
        "../dokumentacja/04_plc/": "../dokumentacja/plc/",
        "../../plc/program/SKO-Program.pdf": "../../plc/SKO-Program.pdf",
        "../plc/program/SKO-Program.pdf": "../plc/SKO-Program.pdf",
        "../../plc/program/SKO-Program.pdw": "../../plc/SKO-Program.pdw",
        "../plc/program/SKO-Program.pdw": "../plc/SKO-Program.pdw",
        "../zrodla/SKO-Program.pdf": "../plc/SKO-Program.pdf",
        "Średnice słoików.txt": "receptury.md",
        "&lt;": "<",
        "&gt;": ">",
    }
    for a, b in repl.items():
        text = text.replace(a, b)
    return text


PROCEDURY_DIAG = """## Skrót procedur diagnostycznych

### Test HOME (N0010–N0012, N0076)

1. M80 ON → M25, T10 (80 s).
2. X3 ON → M82, R1501 = 0.
3. Brak X3 w 80 s → M504.

### Test obrotu 90°

HOME → 4× obrót → R1501: 0→90→180→270→0. Kalibracja **R1403**.

### Separacja B1

- **M22:** zliczanie X1 → C1.
- **M233:** kontrola pozycji X1/X2 → M501/M502.

### Timeouty

| Timer | Czas | Flaga |
|-------|------|-------|
| T5 | 300 s | M505 |
| T7 | 80 s | M506 |
| T10 | 80 s | M504 |

### Test B4 {#test-b4}

- X4 ON → blokada N0020/N0021; C1 bez resetu (po wdrożeniu A0).
- M1019/M1020 → M1050 symulacja.
- D204 — licznik aktywacji.

### Wartości referencyjne

- D200/D201 < 10/dzień — OK pozycjonowanie.
- D204 < 20/dzień — OK przepływ.
- R1500 stabilny 12–18 s.

---

"""

B4_OPERATOR = """
## Czujnik B4 — zator na linii odbiorczej

Czujnik **B4** (wejście **X4**) monitoruje przepływ na transporterze odbiorczym za stacją.

| Stan B4 | Zachowanie |
|---------|------------|
| **OFF** | Normalne przepychanie i zliczanie partii |
| **ON** | Stop przepychania; **C1 bez resetu**; obrót modułu może trwać |

Usuń zator na linii odbiorczej — maszyna wznowi przepychanie bez utraty zliczonej ilości w partii. Szczegóły: [plc/program.md](plc/program.md) (N0020–N0024), [maszyna.md](maszyna.md#zator-b4).

"""


RECEPTURY = """# Receptury — profile opakowań

**Źródło wymiarów:** [srednice_slokow.txt](srednice_slokow.txt)

Średnica [mm] określa przezbrojenie mechaniczne. **R1400** = liczba słoików w partii (1–10) — ustawiana na HMI zgodnie z pojemnością modułu dla danego formatu.

| Profil | Średnica [mm] | R1400 (szac./do kalibracji) | Uwagi |
|--------|---------------|-----------------------------|--------|
| 1 | 75 | Do ustalenia na maszynie | Najmniejszy format |
| 2 | 100 | 4 | Przykład z instrukcji operatora |
| 3 | 120 | Do ustalenia | |
| 4 | 200 | Do ustalenia | |
| 5 | 250 | Do ustalenia | |
| 6 | 500 | Do ustalenia | |
| 7 | 750 | Do ustalenia | Największy format |

## Procedura przezbrojenia

1. Wymiana uchwytów i prowadnic pod średnicę.
2. Ustaw **R1400** na HMI (liczba słoików mieszczących się w module obrotowym).
3. Wykonaj **HOME** (M1003 / automatyczny).
4. Testowa partia — sprawdź C1, pozycjonowanie B1/B2.
5. Zapisz parametry w dzienniku zmiany.

## Wdrożenie w PLC (P1 z audytu)

Docelowo: tablica receptur na HMI (7 profili) → zapis do R1400 (+ ewentualnie R1401–R1403 per profil). Patrz [plc/audyt.md](plc/audyt.md).

**© CNC Solutions — Michał Batorowicz**
"""


def write_srednice():
    solutions = Path(r"c:\Users\mbato\OneDrive\Desktop\Solutions")
    kopia = next(
        d for d in solutions.iterdir() if "kopia" in d.name.lower() and "stacja" in d.name.lower()
    )
    src = next(kopia.glob("*słoik*"), None) or next(kopia.glob("*slok*"), None)
    text = """75ml  - 46
100ml - 51
120ml - 54
200ml - 63
250ml - 67
500ml - 82
750ml - 93
"""
    if src and src.is_file():
        text = src.read_text(encoding="utf-8")
    (DOC / "srednice_slokow.txt").write_text(text.strip() + "\n", encoding="utf-8")


def create_main_docs():
    stare = kopia_stare()
    op = fix_links((stare / "instrukcja_uzytkownika_poprawiona.md").read_text(encoding="utf-8"))
    if "Czujnik B4" not in op:
        if "**© CNC Solutions" in op:
            op = op.replace("**© CNC Solutions", B4_OPERATOR + "\n**© CNC Solutions", 1)
        else:
            op += B4_OPERATOR
    (DOC / "operator.md").write_text(op, encoding="utf-8")

    se = fix_links((stare / "instr_serv_clean.md").read_text(encoding="utf-8"))
    se = se.replace("# INSTRUKCJA SERWISANTA", "# Instrukcja serwisanta", 1)
    (DOC / "serwis.md").write_text(PROCEDURY_DIAG + se, encoding="utf-8")

    te = fix_links((stare / "dok_tech_clean.md").read_text(encoding="utf-8"))
    (DOC / "techniczna.md").write_text(te, encoding="utf-8")

    write_srednice()
    (DOC / "receptury.md").write_text(RECEPTURY, encoding="utf-8")


def fix_all_markdown_links():
    for path in DOC.rglob("*"):
        if path.suffix not in (".md", ".txt"):
            continue
        text = path.read_text(encoding="utf-8")
        new = fix_links(text)
        if path.is_relative_to(DOC_PLC) and path.name == "mapowanie.md":
            new = re.sub(
                r"\n\*\*Sterownik:\*\* FATEK HB1-14MBJ25\s+\n\*\*Dokument:\*\* REF-MAP-SKO",
                "",
                new,
                count=1,
            )
            new = new.replace(
                "Pełna lista z indeksem N: [lista_sieci.md](../04_plc/lista_sieci.md).",
                "Pełna lista z indeksem N: [lista_sieci.md](lista_sieci.md).",
            )
            new = new.replace("| **019** |", "| **N0020** |")
            new = new.replace("| **025** |", "| **N0029** |")
            new = new.replace("sieciach 019–021", "sieciach N0020–N0023")
        if new != text:
            path.write_text(new, encoding="utf-8")


def write_readmes():
    (DOC / "README.md").write_text(
        """# Dokumentacja — Stacja Kontroli Opakowań (SKO)

**Sterownik:** FATEK HB1-14MBJ25 | **HMI:** P5043NB | **Bezpieczeństwo:** Pilz PNOZ X7

Jedna dokumentacja projektu (operator, serwis, PLC, techniczna, receptury).

---

## Spis treści

| Dokument | Odbiorca | Opis |
|----------|----------|------|
| [maszyna.md](maszyna.md) | Wszyscy | Przeznaczenie, cykl 360°, B4, parametry R |
| [operator.md](operator.md) | Operator | Uruchomienie, HMI, alarmy, dziennik |
| [serwis.md](serwis.md) | Serwis | Diagnostyka, kalibracja, konserwacja |
| [techniczna.md](techniczna.md) | Producent / integrator | Hardware, Modbus, HMI |
| [receptury.md](receptury.md) | Operator / serwis | 7 profili średnic → R1400 |
| [srednice_slokow.txt](srednice_slokow.txt) | — | Wymiary słoików [mm] |

### Program PLC — [plc/](plc/)

| Dokument | Opis |
|----------|------|
| [program.md](plc/program.md) | Architektura, 78 sieci N0000–N0077 |
| [mapowanie.md](plc/mapowanie.md) | X/Y, M, R, D, C, T |
| [lista_sieci.md](plc/lista_sieci.md) | Spis sieci |
| [indeks_krzyzowy.md](plc/indeks_krzyzowy.md) | Adres → sieć |
| [audyt.md](plc/audyt.md) | Stan programu, rekomendacje A0/A1/P1 |
| [mnemotechniki.txt](plc/mnemotechniki.txt) | Listing WinProLadder |
| [sieci/](plc/sieci/) | Opis każdej sieci |

---

## Pliki projektu

| Ścieżka | Opis |
|---------|------|
| [../plc/SKO-Program.pdf](../plc/SKO-Program.pdf) | Eksport WinProLadder (79 str.) |
| [../plc/SKO-Program.pdw](../plc/SKO-Program.pdw) | Projekt sterownika |
| [../plc/export/comments.txt](../plc/export/comments.txt) | Komentarze symboli |
| [../schemat_elektryczny/](../schemat_elektryczny/) | Schemat QET |
| [../hmi/](../hmi/) | Projekt panelu P5043NB |

## Regeneracja opisów sieci z PDF

```bash
python narzedzia/generuj_dokumentacje.py
```

---

**© CNC Solutions — Michał Batorowicz**
""",
        encoding="utf-8",
    )

    (ROOT / "README.md").write_text(
        """# Stacja Kontroli Opakowań (SKO)

Sterownik: **FATEK HB1-14MBJ25** | Panel: **P5043NB** | Bezpieczeństwo: **Pilz PNOZ X7**

## Struktura projektu

```
SKO/
├── dokumentacja/       ← dokumentacja (jeden zestaw plików)
├── plc/                  ← jeden program: SKO-Program.pdw / .pdf
│   └── export/           ← komentarze, drabinka, tabele serwo
├── hmi/                  ← panel P5043NB
├── schemat_elektryczny/  ← QElectroTech
├── referencje/           ← Fatek, napędy
├── mechanika/
├── media/
└── narzedzia/            ← generuj_dokumentacje.py
```

## Dokumentacja

**[dokumentacja/README.md](dokumentacja/README.md)** — maszyna, operator, serwis, PLC (78 sieci), techniczna, receptury.

## Program PLC

| Plik | Opis |
|------|------|
| [plc/SKO-Program.pdw](plc/SKO-Program.pdw) | Projekt WinProLadder |
| [plc/SKO-Program.pdf](plc/SKO-Program.pdf) | Wydruk programu |
| [plc/export/comments.txt](plc/export/comments.txt) | Komentarze symboli |

Mapowanie I/O: [dokumentacja/plc/mapowanie.md](dokumentacja/plc/mapowanie.md)

## Wejścia PLC (skrót)

| Wejście | Czujnik |
|---------|---------|
| X0 | Pilz — bezpieczeństwo |
| X1 | B1 — bariera US |
| X2 | B2 — wyjście |
| X3 | B3 — HOME 0° |
| X4 | B4 — zator linii odbiorczej |

---

**CNC Solutions — Michał Batorowicz**
""",
        encoding="utf-8",
    )

    (PLC / "README.md").write_text(
        """# PLC — FATEK HB1-14MBJ25

**Jeden program produkcyjny** w tym folderze (bez podfolderów `program/` / `testy/`).

| Plik / folder | Zawartość |
|---------------|-----------|
| `SKO-Program.pdw` | Projekt WinProLadder |
| `SKO-Program.pdf` | Wydruk programu (79 str., 78 sieci N0000–N0077) |
| `PlcRegStatus.bin` | Status rejestrów (eksport) |
| [export/](export/) | `comments.txt`, `Ladder Resource.ldr`, `Table.tab` |

Dokumentacja: [../dokumentacja/plc/](../dokumentacja/plc/)
""",
        encoding="utf-8",
    )


def cleanup():
    for d in (PLC / "program", PLC / "testy", ROOT / "archiwum", ROOT / "export"):
        if d.exists():
            shutil.rmtree(d, ignore_errors=True)
    for name in (
        "_build_docs.py",
        "_reorganize.py",
        "_fix_plc_layout.py",
        "_migrate_docs.py",
        "_extract_profile.py",
        "_extract_migrate.py",
        "_pick_sources.py",
        "_profile_extract.txt",
        "_cmp.txt",
    ):
        p = NARZ / name
        if p.exists():
            p.unlink()


def main():
    create_main_docs()
    fix_all_markdown_links()
    write_readmes()
    cleanup()
    print("OK: dokumentacja/, linki, README")


if __name__ == "__main__":
    main()
