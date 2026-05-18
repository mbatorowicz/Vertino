# -*- coding: utf-8 -*-
"""Jeden program PLC + jedna dokumentacja — porządkuje cały projekt SKO."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "dokumentacja"
DOC_PLC = DOC / "plc"
PLC = ROOT / "plc"


def rm_tree(path: Path):
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)


def move_file(src: Path, dst: Path):
    if not src.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        dst.unlink()
    shutil.move(str(src), str(dst))


def main():
    # --- PLC: jeden program w korzeniu plc/ ---
    prog = PLC / "program"
    if prog.exists():
        for name in ("SKO-Program.pdw", "SKO-Program.pdf", "PlcRegStatus.bin"):
            move_file(prog / name, PLC / name)
        if prog.exists():
            try:
                prog.rmdir()
            except OSError:
                pass

    # Projekty testowe poza głównym programem
    testy = PLC / "testy"
    szkice = ROOT / "referencje" / "plc_szkice"
    if testy.exists():
        szkice.mkdir(parents=True, exist_ok=True)
        for f in testy.rglob("*.pdw"):
            move_file(f, szkice / f.name)
        rm_tree(testy)

    # --- Przenieś plc z dokumentacji do nowej ścieżki ---
    old_plc = DOC / "04_plc"
    if old_plc.exists():
        for name in (
            "lista_sieci.md",
            "indeks_krzyzowy.md",
            "mnemotechniki_pelny.txt",
            "mapowanie_IO_rejestrow.md",
            "audyt_i_rekomendacje.md",
        ):
            src = old_plc / name
            dst_name = {
                "mapowanie_IO_rejestrow.md": "mapowanie.md",
                "audyt_i_rekomendacje.md": "audyt.md",
                "mnemotechniki_pelny.txt": "mnemotechniki.txt",
            }.get(name, name)
            move_file(src, DOC_PLC / dst_name)
        old_sieci = old_plc / "sieci"
        if old_sieci.exists():
            if (DOC_PLC / "sieci").exists():
                rm_tree(DOC_PLC / "sieci")
            shutil.move(str(old_sieci), str(DOC_PLC / "sieci"))

    # --- Skonsolidowane dokumenty główne (przed usunięciem starych folderów) ---
    create_consolidated_docs()

    # --- Usuń starą strukturę dokumentacji ---
    for d in (
        "01_maszyna",
        "02_operator",
        "03_serwis",
        "04_plc",
        "05_techniczna",
        "06_receptury",
        "zrodla",
    ):
        rm_tree(DOC / d)

    # --- Usuń archiwum i duplikaty ---
    rm_tree(ROOT / "archiwum")
    rm_tree(ROOT / "export")

    print("Struktura plików uporządkowana.")
    print("Regeneracja z PDF: python narzedzia/generuj_dokumentacje.py")


def fix_links(text: str) -> str:
    repl = {
        "../05_techniczna/dokumentacja_techniczna.md": "techniczna.md",
        "dokumentacja_techniczna.md": "techniczna.md",
        "../04_plc/mapowanie_IO_rejestrow.md": "plc/mapowanie.md",
        "mapowanie_PLC.md": "plc/mapowanie.md",
        "../04_plc/instrukcja_programowania.md": "plc/program.md",
        "../04_plc/audyt_i_rekomendacje.md": "plc/audyt.md",
        "../06_receptury/profile_opakowan.md": "receptury.md",
        "proces_technologiczny.md": "maszyna.md",
        "charakterystyka.md": "maszyna.md",
        "instrukcja_serwisanta.md": "serwis.md",
        "procedury_diagnostyczne.md": "serwis.md#procedury-skrot",
        "../../plc/program/SKO-Program.pdf": "../plc/SKO-Program.pdf",
        "../plc/program/SKO-Program.pdf": "../plc/SKO-Program.pdf",
        "../zrodla/SKO-Program.pdf": "../plc/SKO-Program.pdf",
    }
    for a, b in repl.items():
        text = text.replace(a, b)
    return text


def create_consolidated_docs():
    """Uruchom narzedzia/dokoncz_refaktoryzacje.py — pełna konsolidacja z kopii zapasowej."""
    script = ROOT / "narzedzia" / "dokoncz_refaktoryzacje.py"
    if script.exists():
        import runpy

        runpy.run_path(str(script), run_name="__main__")
        return

    op_src = DOC / "02_operator" / "instrukcja_uzytkownika.md"
    if op_src.exists():
        (DOC / "operator.md").write_text(fix_links(op_src.read_text(encoding="utf-8")), encoding="utf-8")


if __name__ == "__main__":
    main()
