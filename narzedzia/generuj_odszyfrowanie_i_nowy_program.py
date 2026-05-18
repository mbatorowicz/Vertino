# -*- coding: utf-8 -*-
"""Generuje odszyfrowanie starego PLC i specyfikację nowego programu (sieci)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
text = (ROOT / "narzedzia/_pdf_extract.txt").read_text(encoding="utf-8", errors="replace")

NETWORK_NAMES = {
    0: "Bezpieczeństwo ON",
    1: "Bezpieczeństwo OFF",
    2: "Reset błędów z HMI",
    3: "System gotowy SET",
    4: "System gotowy RESET",
    5: "Reset wszystkich błędów",
    6: "START AUTO",
    7: "STOP AUTO",
    8: "Żądanie HOME przy starcie",
    9: "HOME ręczny HMI",
    10: "Start procedury HOME",
    11: "Koniec HOME B3",
    12: "Timeout HOME",
    13: "FUN141 Transport",
    14: "FUN141 Obrót",
    15: "FUN140 Transport",
    16: "FUN140 Obrót",
    17: "READY Transport",
    18: "READY Rotation",
    19: "Start cyklu Y4",
    20: "Start transportu M21",
    21: "Wejście w zliczanie M22",
    22: "Liczenie B1 → C1",
    23: "Koniec partii C1≥R1400",
    24: "Stabilizacja M23 T6",
    25: "Kontrola strefy B1",
    26: "Kontrola strefy B2",
    27: "Koniec stabilizacji",
    28: "Pozycja OK M24",
    29: "Start obrotu M25",
    30: "Koniec obrotu",
    31: "Timeout transportu T5",
    32: "Timeout obrotu T7",
    33: "Walidacja R1400 min",
    34: "Walidacja R1400 max",
    35: "Walidacja R1401 min",
    36: "Walidacja R1401 max",
    37: "Walidacja R1402 min",
    38: "Walidacja R1402 max",
    39: "Walidacja R1403 min",
    40: "Walidacja R1403 max",
    41: "R1507 B4 zajęty",
    42: "Status M507 zajęty",
    43: "HMI status SET",
    44: "HMI status RESET",
    45: "Zbocze B4 D204",
    46: "Reset zbocza B4",
    47: "Pozycja HOME R1501=0",
    48: "Pozycja +90° R1501",
    49: "Reset R1501 po 360°",
    50: "Start pomiaru T50",
    51: "Zapis czasu R1500",
    52: "Tryb ręczny SET M100",
    53: "Tryb ręczny RESET",
    54: "Transport FWD start",
    55: "Transport FWD stop",
    56: "Transport REV start",
    57: "Transport REV stop",
    58: "Obrót CW start",
    59: "Obrót CW stop",
    60: "Obrót CCW start",
    61: "Obrót CCW stop",
    62: "Obrót +90°",
    63: "Obrót -90°",
    64: "Przedmuch ręczny ON",
    65: "Przedmuch ręczny OFF",
    66: "Symulacja B4 ON",
    67: "Symulacja B4 OFF",
    68: "Przedmuch AUTO",
    69: "Przedmuch ręczny Y5",
    70: "Transport FWD ręczny",
    71: "Transport REV ręczny",
    72: "Obrót CW ręczny",
    73: "Obrót CCW ręczny",
    74: "Obrót +90° ręczny",
    75: "Obrót -90° ręczny",
    76: "HOME procedure",
    77: "Koniec ORG",
}


def net_body(n: int) -> str:
    tag = f"N{n:04d}\n"
    s = text.find(tag)
    if s < 0:
        return ""
    s += len(tag)
    m = re.search(r"\nN\d{4}\n", text[s:])
    e = s + m.start() if m else s + 3000
    return text[s:e]


def ladder_lines(body: str) -> list[str]:
    out: list[str] = []
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith("Printed"):
            continue
        if re.match(r"^N\d{4}$", line):
            break
        if re.match(r"^\d{3,4}M$", line):
            continue
        if re.search(r"[XM]\d|FUN|RST|OUT|SET|RESET|>=|174\.|141\.|140\.|Timer|Licznik|Start |Transport|Obrót|HOME|Przedmuch|Bezpie", line, re.I):
            out.append(line)
    return out[:30]


def old_issues(n: int, body: str) -> list[str]:
    notes = []
    if n == 68:
        notes.append("BŁĄD: Y5 włączony przez całe M70 (przedmuch non-stop w AUTO).")
    if n == 22 and "M507" not in body and "X4" not in body:
        notes.append("BRAK: /M507 przy zliczaniu i końcu partii.")
    if n == 15 and "M507" not in body:
        notes.append("BRAK: blokada FUN140 transport przy zatorze.")
    if n == 31 and "M507" not in body:
        notes.append("RYZYKO: timeout T5 podczas oczekiwania na B4.")
    if n == 20 and "X4" in body:
        notes.append("OK: start M21 tylko przy wolnym B4 (/X4, /M1050).")
    if n == 29 and "X4" not in body:
        notes.append("OK: obrót bez blokady B4.")
    return notes


def build_old():
    parts = [
        "# 01 — Odszyfrowanie starego programu SKO\n\n",
        "**Sterownik:** FATEK HB1-14MBJ25 | **Źródło:** `plc/SKO-Program.pdf` (78 sieci N0000–N0077)\n\n",
        "Dokument służy do **niczego nie pominąć** przed pisaniem programu od nowa.\n\n",
        "---\n\n",
        "## Spis treści\n\n",
        "1. [Wymagania procesu](#1-wymagania-procesu)\n",
        "2. [Mapa zasobów](#2-mapa-zasobów)\n",
        "3. [Logika AUTO — krok po kroku](#3-logika-auto)\n",
        "4. [Wszystkie 78 starych sieci](#4-wszystkie-78-starych-sieci)\n",
        "5. [Luki i błędy](#5-luki-i-błędy)\n",
        "6. [FUN140 / tabele](#6-fun140--tabele)\n\n",
        "---\n\n",
        "## 1. Wymagania procesu\n\n",
        "| # | Wymaganie | Stary PLC |\n",
        "|---|-----------|----------|\n",
        "| P1 | Pilz X0=1 → napędy dozwolone | M1, N0000–N0001 |\n",
        "| P2 | HOME przed AUTO (M82) | M80/M25/B3, N0008–N0012, N0076 |\n",
        "| P3 | Partia = R1400 impulsów B1 | C1 w M22 |\n",
        "| P4 | Pauza B4: stop push, C1 zachowany, obrót OK | **niepełne** |\n",
        "| P5 | Przedmuch tylko 180° | **błąd N0068** |\n",
        "| P6 | Walidacja parametrów | N0033–N0040 → M503 |\n",
        "| P7 | Timeouty transport/obrót/HOME | T5/T7/T10 → M505/M506/M504 |\n",
        "| P8 | Tryb ręczny tylko bez AUTO | M100, N0052–N0053 |\n",
        "| P9 | HMI: START/STOP/RESET/HOME/przyciski | M1000–M1024 |\n",
        "| P10 | Diagnostyka D200–D204, R1500 | liczniki w sieciach błędów |\n\n",
        "## 2. Mapa zasobów\n\n",
        "### Wejścia / wyjścia\n\n",
        "| Adres | Symbol | Rola |\n",
        "|-------|--------|------|\n",
        "| X0 | SAFETY_STATUS | Pilz — łańcuch bezpieczeństwa |\n",
        "| X1 | SENSOR_B1 | Zliczanie + strefa wejścia |\n",
        "| X2 | SENSOR_B2 | Strefa wyjścia |\n",
        "| X3 | SENSOR_B3 | HOME 0° |\n",
        "| X4 | SENSOR_B4 | Zator linii odbiorczej |\n",
        "| Y0–Y1 | TRANSPORT | Impuls/kierunek SH-D08R |\n",
        "| Y2–Y3 | ROTATION | Impuls/kierunek SS86D |\n",
        "| Y4 | SYSTEM_READY | Lampka gotowości |\n",
        "| Y5 | PNEUMATIC_VALVE | Przedmuch |\n\n",
        "### Flagi sekwencji AUTO\n\n",
        "| M | Znaczenie |\n",
        "|---|----------|\n",
        "| M10 | System gotowy (M1∧M82∧¬błędy) |\n",
        "| M70 | Praca automatyczna |\n",
        "| M21 | Krok: żądanie transportu / cykl |\n",
        "| M22 | Zliczanie partii (B1→C1) |\n",
        "| M23 | Stabilizacja (T6=R1410) |\n",
        "| M233 | Ilość OK — strefy sprawdzone |\n",
        "| M24 | Gotowy do obrotu |\n",
        "| M25 | Obrót 90° w toku |\n",
        "| M507 | Linia odbiorcza zajęta (X4∨M1050) |\n",
        "| M1992/M1993 | Serwo transport/obrót aktywne |\n\n",
        "## 3. Logika AUTO\n\n",
        "```\n",
        "M1001 + M10 → M70\n",
        "Pętla: M21 → [FUN140 push] → M22 (C1++) → M23 (T6) → strefy B1/B2 → M24 → M25 [FUN140 90°] → T8 → M21\n",
        "Warunek wejścia w M21: ¬M507 (B4 wolny), ¬M1050\n",
        "Obrót (M25): bez warunku B4\n",
        "```\n\n",
        "---\n\n",
        "## 4. Wszystkie 78 starych sieci\n\n",
    ]

    all_issues = []
    for n in range(78):
        name = NETWORK_NAMES.get(n, f"Sieć {n}")
        body = net_body(n)
        lines = ladder_lines(body)
        notes = old_issues(n, body)
        if notes:
            all_issues.append((n, name, notes))

        parts.append(f"### N{n:04d} — {name}\n\n")
        if lines:
            parts.append("```text\n" + "\n".join(lines) + "\n```\n\n")
        else:
            parts.append("*(treść w `mnemotechniki.txt` / PDF str. sieci)*\n\n")
        if notes:
            parts.append("> **Uwagi:** " + " | ".join(notes) + "\n\n")

    parts.append("---\n\n## 5. Luki i błędy (checklist migracji)\n\n")
    for n, name, notes in all_issues:
        parts.append(f"- **N{n:04d}** {name}: {' '.join(notes)}\n")
    parts.append(
        "\n**Dodatkowo:** 8 sieci walidacji (N0033–N0040) można zastąpić **jedną** siecią walidacji. "
        "12 sieci ręcznych start/stop (N0054–N0061) można zastąpić **2 sieciami** z podtrzymaniem M110–M113.\n"
    )

    parts.append(
        "\n---\n\n## 6. FUN140 — tabele (bez zmian w nowym programie)\n\n"
        "| Tabela | SR | Użycie |\n"
        "|--------|-----|--------|\n"
        "| Transport AUTO | R1100 | Push partii, M21 |\n"
        "| Obrót 90° | R1200 | M25, R1402/R1403 |\n"
        "| HOME | R1300 | M80, B3 |\n"
        "| Parametry | R1120, R1220 | FUN141 @ M1924 |\n\n"
        "Wartości R1100–R1108, R1200–R1208, R1300–R1308 — patrz [techniczna.md](../techniczna.md).\n\n"
        "**© CNC Solutions**\n"
    )

    out = ROOT / "dokumentacja/plc/01_odszyfrowanie_starego_programu.md"
    out.write_text("".join(parts), encoding="utf-8")
    return out


# --- Nowy program: ~32 sieci ---
NEW_NETWORKS = [
    ("N0000", "Bezpieczeństwo ON", """
|--[X0]--( SET M1 )--|
"""),
    ("N0001", "Bezpieczeństwo OFF", """
|--[/X0]--( RST M1 )--|
"""),
    ("N0002", "Reset błędów HMI", """
|--[M1000]--( SET M200 )--|
"""),
    ("N0003", "System gotowy SET", """
|--[M1]--[M82]--[/M503]--[/M504]--[/M505]--[/M506]--( SET M10 )--|
"""),
    ("N0004", "System gotowy RESET", """
|--[/M1]--+--( RST M10 )--|
| [/M82] |
| [M503..M506] |
"""),
    ("N0005", "Kasowanie błędów", """
|--[M200]--[M1]--( RST M501 M502 M503 M504 M505 M506 M507 M200 )--|
"""),
    ("N0006", "Walidacja parametrów (jedna sieć)", """
|--[M1924]--+--[R1400<1]--+--( SET M503 )--|
|           | [R1400>10] |
|           | [R1401 poza 50-500] |
|           | [R1402 poza 100-1000] |
|           | [R1403 poza 12400-12600] |
"""),
    ("N0007", "FUN141 — ładowanie osi", """
|--[M1924]--[FUN141.MPARA Ps:0 SR:R1120]--|
|--[M1924]--[FUN141.MPARA Ps:1 SR:R1220]--|
"""),
    ("N0008", "Status B4 → M507, R1507", """
|--[X4]--( MOV 1 R1507 )--|
|--[/X4]--( MOV 0 R1507 )--|
|--[X4]--+--( SET M507 )--|
| [M1050]|
|--[/X4]--[/M1050]--( RST M507 )--|
"""),
    ("N0009", "START / STOP AUTO", """
|--[M1001]--[M10]--( SET M70 )--|
|--[/M10]--+--( RST M70 )--|
| [M1002] |
"""),
    ("N0010", "Żądanie HOME", """
|--[M1]--[/M82]--( SET M80 )--|
|--[M1003]--[M100]--( SET M80 )--|
"""),
    ("N0011", "Procedura HOME", """
|--[M80]--[M10]--[/M25]--( SET M25 )--[T10]--|
|--[X3]--[M25]--[M80]--( RST M25 SET M82 RST T10 MOV 0 R1501 )--|
|--[T10]--( SET M504 RST M25 RST M80 )--|
|--[M80]--[FUN140.HSPSO Ps:1 SR:R1300]--|
"""),
    ("N0012", "FUN140 — transport (tylko wolna linia)", """
|--[M21]--[/M507]--[FUN140.HSPSO Ps:0 SR:R1100 WR:R1144]--|
|   FO0→M1992  FO1→M501  FO2→RST M21 |
"""),
    ("N0013", "FUN140 — obrót 90°", """
|--[M25]--[FUN140.HSPSO Ps:1 SR:R1200 WR:R1244]--|
|   FO0→M1993  FO1→M502  FO2→RST M25 |
"""),
    ("N0014", "Y4 — gotowość serwo", """
|--[M1992]--( SET Y4 )--|
|--[M1993]--( SET Y4 )--|
"""),
    ("N0015", "Sekwencer AUTO — krok 0→1 (start partii)", """
|--[M70]--[M10]--[/M21]--[/M22]--[/M23]--[/M24]--[/M25]--[/M507]--[/M1050]--( SET M21 )--|
"""),
    ("N0016", "Sekwencer — push → zliczanie", """
|--[M21]--[/M22]--( SET M22 RST C1 )--[T5]--|
"""),
    ("N0017", "Sekwencer — zliczanie B1 (pauza B4)", """
|--[X1]--[M22]--[/M507]--[+(C1)]--|
|--[C1>=R1400]--[M22]--[/M507]--( SET M233 )--|
"""),
    ("N0018", "Sekwencer — stabilizacja i strefy", """
|--[M233]--( RST M22 SET M23 )--[T6=R1410]--|
|--[X1]--[M23]--[T6]--( SET M501 )--[INC D200]--|
|--[X2]--[M23]--[T6]--( SET M502 )--[INC D201]--|
|--[T6]--[/M501]--[/M502]--( RST M23 SET M24 RST M21 RST M233 )--|
"""),
    ("N0019", "Sekwencer — start obrotu", """
|--[M24]--[/M25]--( SET M25 )--[T7]--|
"""),
    ("N0020", "Sekwencer — koniec obrotu", """
|--[M1993]--[M25]--[/M1992]--( RST M25 RST M24 INC D100 )--[T8=R1411]--|
|--[T8]--[M1993]--[FUN +(90) R1501]--[R1501>=360→MOV 0 R1501]--|
|   // po T8: N0015 może znów ustawić M21 (następna partia)
"""),
    ("N0021", "Pozycja R1501 — HOME", """
|--[M82]--[/M25]--( MOV 0 R1501 )--|
"""),
    ("N0022", "Przedmuch AUTO (180°)", """
|--[M70]--[R1501=180]--( SET Y5 )--|
|--[/M70]--+--( RST Y5 )--|
| [/R1501=180] |
"""),
    ("N0023", "Przedmuch ręczny", """
|--[M240]--( SET Y5 )--|
|--[/M240]--( RST Y5 )--|
"""),
    ("N0024", "Timeout transportu (bez zatoru)", """
|--[T5]--[/M507]--( SET M505 RST M22 INC D202 )--|
"""),
    ("N0025", "Timeout obrotu", """
|--[T7]--( SET M506 RST M25 INC D203 )--|
"""),
    ("N0026", "Pomiar czasu cyklu", """
|--[M21]--[T50]--|
|--[T8]--( MOV T50 R1500 RST T50 )--|
"""),
    ("N0027", "Tryb ręczny — warunki", """
|--[M10]--[/M70]--( SET M100 )--|
|--[/M10]--+--( RST M100 )--|
| [M70] |
"""),
    ("N0028", "Ręczny — transport FWD/REV", """
|--[M1010]--[M100]--( SET M110 )--|
|--[M1011]--( RST M110 )--|
|--[M110]--[FUN140 SR:R524]--|
|--[M1012]--[M100]--( SET M111 )--|
|--[M1013]--( RST M111 )--|
|--[M111]--[FUN140 SR:R532]--|
"""),
    ("N0029", "Ręczny — obrót CW/CCW/±90°", """
|--[M1014]--[M100]--( SET M112 )--|
|--[M1015]--( RST M112 )--|
|--[M112]--[FUN140.HSPSO Ps:1 SR:R540 WR:R1244]--|
|--[M1016]--[M100]--( SET M113 )--|
|--[M1017]--( RST M113 )--|
|--[M113]--[FUN140.HSPSO Ps:1 SR:R548 WR:R1244]--|
|--[M1021]--[M100]--[/M114]--( SET M114 )--|
|--[M114]--[FUN140.HSPSO Ps:1 SR:R556 WR:R1244]--[FO2→RST M114]--|
|--[M1022]--[M100]--[/M115]--( SET M115 )--|
|--[M115]--[FUN140.HSPSO Ps:1 SR:R516 WR:R1244]--[FO2→RST M115]--|
"""),
    ("N0030", "Test symulacji B4", """
|--[M1019]--[M100]--( SET M1050 )--|
|--[M1020]--( RST M1050 )--|
"""),
    ("N0031", "Zbocze B4 — licznik D204", """
|--[X4]--[/M520]--( SET M520 INC D204 )--|
|--[/X4]--( RST M520 )--|
"""),
    ("N0032", "Koniec programu", """
|--[END]--|
"""),
]


def build_new():
    parts = [
        "# 02 — Nowy program SKO (specyfikacja drabinki)\n\n",
        "**Sterownik:** FATEK HB1-14MBJ25 (bez zmian) | **Sieci:** **33** (zamiast 78)\n\n",
        "## Filozofia\n\n",
        "| Cel | Jak |\n",
        "|-----|-----|\n",
        "| **Bezpieczeństwo** | Pilz na X0; brak obejść; M10 tylko po HOME i bez błędów |\n",
        "| **Niezawodność** | Jedna maszyna stanów (M21–M25); B4 w jednym miejscu (M507); jedna walidacja |\n",
        "| **Szybkość** | Mniej sieci = krótszy scan; FUN140 bez zbędnych retriggerów |\n",
        "| **Kompatybilność HMI** | Te same M1000–M1024, R1400–R1411, C1, D100–D204 |\n\n",
        "**Źródło wymagań:** [01_odszyfrowanie_starego_programu.md](01_odszyfrowanie_starego_programu.md)\n\n",
        "---\n\n",
        "## Mapowanie stary → nowy\n\n",
        "| Stary zakres | Nowa sieć |\n",
        "|--------------|----------|\n",
        "| N0000–N0005 | N0000–N0005 |\n",
        "| N0033–N0040 | **N0006** (jedna walidacja) |\n",
        "| N0013–N0014 | **N0007** |\n",
        "| N0041–N0042, N0045–N0046 | **N0008**, **N0031** |\n",
        "| N0006–N0007 | **N0009** |\n",
        "| N0008–N0012, N0076 | **N0010–N0011** |\n",
        "| N0015–N0018 | **N0012–N0014** |\n",
        "| N0019–N0032 | **N0015–N0020**, **N0024–N0025** |\n",
        "| N0047–N0051 | **N0021**, **N0026** |\n",
        "| N0068–N0069 | **N0022–N0023** |\n",
        "| N0052–N0075 | **N0027–N0029** |\n",
        "| N0077 | **N0032** |\n\n",
        "---\n\n",
        "## Wszystkie sieci nowego programu\n\n",
        "Każda sieć — gotowy szkic do wpisania w WinProLadder (`Main_unit1`).\n\n",
    ]

    for net_id, title, ladder in NEW_NETWORKS:
        parts.append(f"### {net_id} — {title}\n\n")
        parts.append("```ladder\n" + ladder.strip() + "\n```\n\n")

    parts.append(
        "---\n\n"
        "## Kolejność sieci w projekcie (ważne)\n\n"
        "WinProLadder wykonuje sieci **od góry do dołu** co skan. Zalecana kolejność:\n\n"
        "```\n"
        "N0000–N0011  → bezpieczeństwo, gotowość, HOME\n"
        "N0012        → FUN140 transport (przed ustawieniem M21)\n"
        "N0013        → FUN140 obrót\n"
        "N0014        → Y4\n"
        "N0015–N0020  → sekwencer AUTO\n"
        "N0021–N0026  → pozycja, przedmuch, timeouty, czas cyklu\n"
        "N0027–N0031  → ręczny, test B4\n"
        "N0032        → koniec\n"
        "```\n\n"
        "Dzięki temu w jednym skanie: FUN140 kończy poprzedni M21 → N0015 ustawia nowy M21 → N0016 wchodzi w M22 (jak w starym programie, gdzie N0015<N0020<N0021).\n\n"
        "## Kolejność wdrożenia w WinProLadder\n\n"
        "1. Nowy projekt lub kopia `SKO-Program.pdw` → zmień nazwę na `SKO-Program-v2.pdw`.\n"
        "2. Usuń zbędne sieci / zbuduj od N0000 według tego dokumentu (33 sieci).\n"
        "3. Skopiuj tabele FUN140 z `export/Table.tab` (R1100, R1200, R1300).\n"
        "4. Import komentarzy: `export/comments.txt`.\n"
        "5. F8 → download → test: HOME → AUTO → B4 w M22 → przedmuch tylko 180°.\n\n"
        "## Test akceptacyjny\n\n"
        "| # | Test | Oczekiwane |\n"
        "|---|------|------------|\n"
        "| T1 | X0 OFF | Wszystkie napędy zatrzymane, M1=0 |\n"
        "| T2 | START bez HOME | Brak M70 |\n"
        "| T3 | AUTO 3 słoiki, B4 w 2. słoiku | C1=1 po zwolnieniu, dokończenie do 3 |\n"
        "| T4 | B4 ON podczas obrotu | Obrót kończy się |\n"
        "| T5 | R1501=180 | Y5 ON tylko w tej pozycji |\n"
        "| T6 | R1400=0 (błąd) | M503, brak START |\n\n"
        "**© CNC Solutions**\n"
    )

    out = ROOT / "dokumentacja/plc/02_program_nowy_sieci.md"
    out.write_text("".join(parts), encoding="utf-8")
    return out


if __name__ == "__main__":
    o1 = build_old()
    o2 = build_new()
    print("OK:", o1.name, o2.name)
