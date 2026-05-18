# -*- coding: utf-8 -*-
"""Jednorazowa unifikacja nazw Vertino w dokumentacji markdown."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "dokumentacja"

REPLACEMENTS = [
    ("# Dokumentacja — Stacja Kontroli Opakowań (SKO)", "# Dokumentacja — Vertino"),
    ("# Maszyna — Stacja Kontroli Opakowań (SKO)", "# Maszyna — Vertino"),
    ("# Stacja Kontroli Opakowań (SKO)", "# Vertino — Stacja oczyszczania opakowań"),
    ("# Mapowanie rejestrów PLC — SKO", "# Mapowanie rejestrów PLC — Vertino"),
    ("# Audyt programu PLC — SKO", "# Audyt programu PLC — Vertino"),
    ("# Program PLC — SKO", "# Program PLC — Vertino"),
    ("# 02 — Nowy program SKO (specyfikacja drabinki)", "# 02 — Szkic programu (33 sieci, poprzedni)"),
    ("# 01 — Odszyfrowanie starego programu SKO", "# 01 — Odszyfrowanie programu produkcyjnego (78 sieci)"),
    ("IU-SKO-001", "IU-VTN-001"),
    ("IS-SKO-001", "IS-VTN-001"),
    ("SKO-MO-2025", "VERTINO-MO-2025"),
    ("Instrukcja Użytkownika SKO", "Instrukcja użytkownika Vertino"),
    ("Instrukcja Serwisanta SKO", "Instrukcja serwisanta Vertino"),
    ("Dokumentacja Techniczna Producenta SKO", "Dokumentacja techniczna Vertino"),
    ("## STACJA KONTROLI OPAKOWAŃ", "## VERTINO — STACJA OCZYSZCZANIA OPAKOWAŃ"),
    ("STACJA KONTROLI OPAKOWAŃ v2.1", "VERTINO v2.1"),
    ("Stacja Kontroli Opakowań jest", "Vertino (stacja oczyszczania opakowań) jest"),
    ("Stacja Kontroli Opakowań to", "Vertino to"),
    ("Stacja Kontroli Opakowań", "Vertino"),
    ("(plc/lista_sieci.md)", "(lista_sieci.md)"),
    ("(plc/program.md)", "(program.md)"),
    ("(plc/mapowanie.md)", "(mapowanie.md)"),
    ("(plc/audyt.md)", "(audyt.md)"),
    (
        "| **Nowa (docelowa)** | **33** | **[02_program_nowy_sieci.md](02_program_nowy_sieci.md)** — bezpieczniejsza, krótsza |",
        "| **Docelowa (Vertino)** | **35** (N0000–N0034) | **[03_program_vertino_sieci.md](03_program_vertino_sieci.md)** |",
    ),
]

PLC_MAPOWANIE_BLOCK = """**B4 (X4):** czujnik na **wyjściu** maszyny — linia odbiorcza zajęta (zator). **R1507** = 1 gdy X4 = ON.

| Element | Zachowanie (program docelowy Vertino) |
|---------|----------------------------------------|
| **N0008** | X4 (lub M1050) przez **R1412** ms → **M507** |
| **N0015–N0018** | Sekwencer używa **/M507** (zliczanie, koniec partii) |
| **N0021** | Start obrotu — **bez** M507 |

**Program produkcyjny (78 sieci):** wymaganie A0 — patrz [audyt.md](audyt.md), [03_program_vertino_sieci.md](03_program_vertino_sieci.md)."""


def patch_mapowanie(text: str) -> str:
    old = """**B4 (X4):** czujnik na **wyjściu** maszyny — linia odbiorcza zajęta (zator). R1507 = 1 gdy X4 = ON.

| Sieć | Zachowanie B4 |
|------|----------------|
| **019** Start transportu | Kontakt **NC X4** — przepychanie startuje tylko przy B4 = OFF |
| **025** Start obrotu | **Bez X4** — obrót modułu niezależny od zatoru |
| **037–042** | Status R1507, M507, licznik D204 |

**Wymaganie procesowe:** przy zatorze w trakcie zliczania — stop przepychania, **C1 bez resetu**, wznowienie po B4 = OFF. W obecnym programie do dopisania w sieciach N0020–N0023 (patrz [plc/program.md](plc/program.md))."""
    if old in text:
        text = text.replace(old, PLC_MAPOWANIE_BLOCK)
    text = text.replace(
        "> Pełna lista z indeksem N: [lista_sieci.md](plc/lista_sieci.md).",
        "> Pełna lista: [lista_sieci.md](lista_sieci.md). Program docelowy: [03_program_vertino_sieci.md](03_program_vertino_sieci.md).",
    )
    if "R1412" not in text:
        text = text.replace(
            "| R1411 | Pauza po obrocie [ms] | 50–500 | 100 | Timer T8 |",
            "| R1411 | Pauza po obrocie [ms] | 50–500 | 100 | Timer T8 |\n| R1412 | Potwierdzenie zatoru B4 [ms] | 100–3000 | 500 | Timer T52 → M507 |",
        )
    return text


def main():
    for path in DOC.rglob("*.md"):
        if path.name == "KONWENCJE_NAZEWNICTWA.md":
            continue
        text = path.read_text(encoding="utf-8")
        orig = text
        for a, b in REPLACEMENTS:
            text = text.replace(a, b)
        if path.name == "mapowanie.md" and path.parent.name == "plc":
            text = patch_mapowanie(text)
        if text != orig:
            path.write_text(text, encoding="utf-8")
            print("updated", path.relative_to(ROOT))

    root_readme = ROOT / "README.md"
    t = root_readme.read_text(encoding="utf-8")
    t = t.replace(
        "```\nSKO/\n",
        "```\nVertino/                    # folder projektu (nazwa katalogu może być historyczna)\n",
    )
    t = t.replace(
        "**[dokumentacja/README.md](dokumentacja/README.md)** — maszyna, operator, serwis, PLC (78 sieci), techniczna, receptury.",
        "**[dokumentacja/README.md](dokumentacja/README.md)** — Vertino: maszyna, operator, serwis, PLC, mapy procesu.",
    )
    t = t.replace(
        "**Program PLC od nowa:** [01 — odszyfrowanie starego](dokumentacja/plc/01_odszyfrowanie_starego_programu.md) · [02 — nowy program 33 sieci](dokumentacja/plc/02_program_nowy_sieci.md)",
        "**PLC:** [program produkcyjny 78 sieci](dokumentacja/plc/01_odszyfrowanie_starego_programu.md) · **[program docelowy 35 sieci](dokumentacja/plc/03_program_vertino_sieci.md)** · [mapy](dokumentacja/mapy_procesu.md)",
    )
    if "KONWENCJE" not in t:
        t += "\n\nNazewnictwo: [dokumentacja/KONWENCJE_NAZEWNICTWA.md](dokumentacja/KONWENCJE_NAZEWNICTWA.md).\n"
    root_readme.write_text(t, encoding="utf-8")
    print("updated README.md")


if __name__ == "__main__":
    main()
