# -*- coding: utf-8 -*-
"""Generuje dokumentację PLC z eksportu SKO-Program.pdf."""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PDF_EXTRACT = ROOT / "narzedzia" / "_pdf_extract.txt"
OUT = ROOT / "dokumentacja" / "plc"
COMMENTS = ROOT / "plc" / "export" / "comments.txt"
PLC_PROGRAM = ROOT / "plc"

# Oficjalne nazwy sieci (z eksportu WinProLadder / mapowanie)
NETWORK_NAMES = {
    0: "Bezpieczeństwo ON",
    1: "Bezpieczeństwo OFF",
    2: "Reset błędów z HMI",
    3: "System gotowy — warunek SET",
    4: "System gotowy — warunek RESET",
    5: "Reset wszystkich błędów",
    6: "START pracy automatycznej",
    7: "STOP pracy automatycznej",
    8: "Żądanie HOME przy starcie",
    9: "HOME ręczny z HMI",
    10: "Start procedury HOME",
    11: "Koniec HOME na czujniku B3",
    12: "Timeout HOME",
    13: "Parametry FUN141 — Transport",
    14: "Parametry FUN141 — Obrót",
    15: "FUN140 Transport",
    16: "FUN140 Obrót",
    17: "Status READY Transport",
    18: "Status READY Rotation",
    19: "Start cyklu",
    20: "Start transportu",
    21: "Liczenie opakowań na B1",
    22: "Sprawdzenie ilości",
    23: "Koniec transportu",
    24: "Kontrola pozycji wejścia — błąd",
    25: "Licznik błędów wejścia",
    26: "Kontrola pozycji wyjścia — błąd",
    27: "Licznik błędów wyjścia",
    28: "Pozycja OK — można obrócić",
    29: "Start obrotu",
    30: "Koniec obrotu",
    31: "Timeout transportu",
    32: "Timeout obrotu",
    33: "Walidacja ilości opakowań — minimum",
    34: "Walidacja ilości opakowań — maksimum",
    35: "Walidacja prędkości transportu — minimum",
    36: "Walidacja prędkości transportu — maksimum",
    37: "Walidacja prędkości obrotu — minimum",
    38: "Walidacja prędkości obrotu — maksimum",
    39: "Walidacja impulsów — minimum",
    40: "Walidacja impulsów — maksimum",
    41: "Status zewnętrznego transportera — zajęty",
    42: "Status zewnętrznego transportera — wolny",
    43: "Flaga statusu dla HMI — SET",
    44: "Flaga statusu dla HMI — RESET",
    45: "Detekcja zbocza B4",
    46: "Reset detekcji zbocza",
    47: "Aktualizacja pozycji — HOME",
    48: "Aktualizacja pozycji — obrót +90°",
    49: "Reset pozycji na 0° po 360°",
    50: "Start pomiaru czasu cyklu",
    51: "Zapis czasu cyklu",
    52: "Warunki trybu ręcznego — SET",
    53: "Warunki trybu ręcznego — RESET",
    54: "Transport FWD — START",
    55: "Transport FWD — STOP",
    56: "Transport REV — START",
    57: "Transport REV — STOP",
    58: "Obrót CW — START",
    59: "Obrót CW — STOP",
    60: "Obrót CCW — START",
    61: "Obrót CCW — STOP",
    62: "Obrót +90°",
    63: "Obrót -90°",
    64: "Przedmuch ręczny ON",
    65: "Przedmuch ręczny OFF",
    66: "Test czujnika B4 — symulacja ON",
    67: "Test czujnika B4 — symulacja OFF",
    68: "Przedmuch AUTO",
    69: "Przedmuch ręczny",
    70: "Transport FWD ręczny",
    71: "Transport REV ręczny",
    72: "Obrót CW ręczny",
    73: "Obrót CCW ręczny",
    74: "Obrót +90° ręczny",
    75: "Obrót -90° ręczny",
    76: "HOME procedure",
    77: "Koniec programu (ORG)",
}

NETWORK_GROUPS = [
    ("000–005", "Bezpieczeństwo, gotowość, reset błędów", range(0, 6)),
    ("006–011", "START/STOP AUTO, procedura HOME", range(6, 12)),
    ("012–018", "FUN141, FUN140, status READY serwo", range(12, 19)),
    ("019–032", "Cykl automatyczny: transport, liczenie, obrót, timeouty", range(19, 33)),
    ("033–046", "Walidacja parametrów, B4, liczniki błędów", range(33, 47)),
    ("047–051", "Pozycja modułu, pomiar czasu cyklu", range(47, 52)),
    ("052–077", "Tryb ręczny, przedmuch, ruchy serwo, HOME", range(52, 78)),
]


def parse_xref_sections(text: str, section_name: str) -> list[tuple[str, str, str]]:
    """Parsuje wszystkie tabele Contact[Network] / Function[Network] z PDF."""
    rows = []
    marker = f"Printed Item: {section_name}"
    pos = 0
    while True:
        start = text.find(marker, pos)
        if start < 0:
            break
        end = text.find("Printed Item:", start + len(marker))
        block = text[start:end if end > 0 else start + 15000]
        for line in block.split("\n"):
            line = line.strip()
            if "Main_unit1" not in line:
                continue
            m = re.match(
                r"^(\S*)\s+(:.+?)\s+Main_unit1\s+((?:N\d{5}\s*)+)$",
                line,
            )
            if m:
                ref = m.group(1) or "(anon)"
                rows.append((ref, m.group(2).strip(), m.group(3).strip()))
        pos = start + len(marker)
    return rows


def extract_full_mnemonic(text: str) -> str:
    idx = text.find("Printed Item: Mnemonic")
    if idx < 0:
        return ""
    end = text.find("Printed Item: Ladder Diagram - Main_unit1", idx)
    return text[idx:end].strip() if end > 0 else text[idx:].strip()


def parse_mnemonic(text: str) -> dict[int, list[str]]:
    """Mnemoniki per sieć z sekcji Mnemonic."""
    result: dict[int, list[str]] = {}
    idx = text.find("Printed Item: Mnemonic")
    if idx < 0:
        return result
    end = text.find("Printed Item: Ladder Diagram - Main_unit1", idx)
    mn = text[idx:end] if end > 0 else text[idx:]
    current = None
    lines_acc: list[str] = []
    for line in mn.split("\n"):
        m = re.match(r"^N(\d{4})$", line.strip())
        if m:
            if current is not None:
                result[current] = lines_acc
            current = int(m.group(1))
            lines_acc = []
            continue
        if current is not None and line.strip():
            if line.startswith("Printed Item"):
                break
            lines_acc.append(line.rstrip())
    if current is not None:
        result[current] = lines_acc
    return result


def load_comments() -> list[dict]:
    rows = []
    if not COMMENTS.exists():
        return rows
    for i, line in enumerate(COMMENTS.read_text(encoding="utf-8", errors="replace").splitlines()):
        if i == 0 or not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) >= 3:
            rows.append({"ref": parts[0], "comment": parts[1], "desc": parts[2]})
    return rows


def extract_network_body(text: str, net_id: int) -> str:
    tag = f"N{net_id:04d}\n"
    start = text.find(tag)
    if start < 0:
        return ""
    start += len(tag)
    m = re.search(r"\nN\d{4}\n", text[start:])
    end = start + m.start() if m else start + 2000
    return text[start:end].strip()


def ins_symbol(ins: str) -> str:
    ins = ins.strip()
    if ":-||-" in ins or ins == ":||":
        return "NO (normalnie otwarty)"
    if ":-|/|-" in ins or ":/" in ins:
        return "NC (normalnie zamknięty)"
    if ":F_Pa" in ins or "F_Pa" in ins:
        return "parametr / funkcja"
    if ":(" in ins or "F_P" in ins:
        return "wyjście / cewka"
    return ins


def load_pdf_text() -> str:
    if PDF_EXTRACT.exists():
        return PDF_EXTRACT.read_text(encoding="utf-8", errors="replace")
    from pypdf import PdfReader

    pdf = PLC_PROGRAM / "SKO-Program.pdf"
    if not pdf.exists():
        pdf = ROOT / "SKO-Program.pdf"
    return "\n".join((p.extract_text() or "") for p in PdfReader(pdf).pages)


def build():
    text = load_pdf_text()
    mnemonics = parse_mnemonic(text)
    contacts_net = parse_xref_sections(text, "Contact[Network]")
    func_net = parse_xref_sections(text, "Function[Network]")
    comments = load_comments()

    OUT.mkdir(parents=True, exist_ok=True)
    # program.md, mapowanie.md, audyt.md — utrzymywane ręcznie / przy refaktoryzacji

    # lista sieci
    net_lines = ["# Lista sieci programu\n\n**Main_unit1** — 78 sieci\n\n---\n\n"]
    for gid, gdesc, grange in NETWORK_GROUPS:
        net_lines.append(f"## Grupa N{gid}\n\n*{gdesc}*\n\n")
        net_lines.append("| Sieć WinPro | Nr proj. | Nazwa |\n|-------------|----------|-------|\n")
        for n in grange:
            proj = n - 1 if n >= 2 else "—"
            proj_s = f"{proj:03d}" if isinstance(proj, int) else proj
            net_lines.append(f"| N{n:04d} | {proj_s} | {NETWORK_NAMES.get(n, '?')} |\n")
        net_lines.append("\n")

    net_lines.append("## Szczegóły\n\nPliki w folderze [sieci/](sieci/).\n\n**© CNC Solutions**\n")
    (OUT / "lista_sieci.md").write_text("".join(net_lines), encoding="utf-8")

    # 03 - indeks krzyżowy
    xref = ["# Indeks krzyżowy (z PDF)\n\nKtóre sieci odwołują się do danego adresu.\n\n---\n\n"]
    xref.append("## Wejścia/wyjścia — Contact[Network]\n\n| Ref | Typ | Sieci |\n|-----|-----|-------|\n")
    for ref, ins, nets in sorted(contacts_net, key=lambda x: x[0]):
        xref.append(f"| {ref} | {ins_symbol(ins)} | {nets} |\n")

    xref.append("\n## Funkcje — Function[Network]\n\n| Funkcja | Sieci |\n|---------|-------|\n")
    for ref, ins, nets in func_net:
        xref.append(f"| {ref} | {nets} |\n")

    # Build reverse index from contacts
    by_ref: dict[str, set[str]] = {}
    for ref, ins, nets in contacts_net:
        for n in re.findall(r"N\d{5}", nets.replace(" ", "")):
            by_ref.setdefault(ref, set()).add(n)
    xref.append("\n## Skrócony indeks adres → sieci\n\n")
    for ref in sorted(by_ref.keys()):
        nets_sorted = ", ".join(sorted(by_ref[ref]))
        xref.append(f"- **{ref}**: {nets_sorted}\n")

    xref.append("\n**© CNC Solutions**\n")
    (OUT / "indeks_krzyzowy.md").write_text("".join(xref), encoding="utf-8")

    # 04 - mnemoniki (pełny listing z PDF)
    full_mn = extract_full_mnemonic(text)
    (OUT / "mnemotechniki.txt").write_text(full_mn, encoding="utf-8")

    # sieci/
    net_dir = OUT / "sieci"
    net_dir.mkdir(exist_ok=True)
    ladder_end = text.find("Printed Item: Mnemonic")
    ladder_text = text[:ladder_end] if ladder_end > 0 else text

    for n in range(78):
        name = NETWORK_NAMES.get(n, f"siec_{n}")
        safe = re.sub(r"[^\w\-]+", "_", name.lower())[:60]
        body = extract_network_body(ladder_text, n)
        mn = mnemonics.get(n, [])
        content = f"# N{n:04d} — {name}\n\n"
        if n >= 2:
            content += f"**Nr w dokumentacji projektu:** {n-1:03d}\n\n"
        content += "## Opis\n\n"
        content += f"Sieć programu **Main_unit1**, indeks **N{n:04d}**.\n\n"
        content += "## Elementy (tekst z drabinki PDF)\n\n```\n"
        content += body[:4000] if body else "(brak)"
        content += "\n```\n\n## Mnemotechnika\n\n```\n"
        content += "\n".join(mn) if mn else "(patrz mnemotechniki.txt)"
        content += "\n```\n\n"
        # xref for this network
        net_tag = f"N{n:04d}"
        used = [
            f"{r} ({ins_symbol(i)})"
            for r, i, nets in contacts_net
            if net_tag in nets.split()
        ]
        if used:
            content += "## Użyte kontakty (indeks PDF)\n\n" + "\n".join(f"- {u}" for u in used) + "\n"
        content += "\n**© CNC Solutions**\n"
        (net_dir / f"N{n:04d}_{safe}.md").write_text(content, encoding="utf-8")

    print(f"OK: {OUT}")
    print(f"Networks: {len(list(net_dir.glob('*.md')))}")


if __name__ == "__main__":
    build()
