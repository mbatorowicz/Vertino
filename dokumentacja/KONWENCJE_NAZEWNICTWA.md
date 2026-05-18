# Konwencje nazewnictwa — Vertino

## Nazwa produktu

| Użycie | Forma |
|--------|--------|
| **Nazwa handlowa / dokumentacja** | **Vertino** |
| **Pełna nazwa** | **Vertino — Stacja oczyszczania opakowań** |
| **Poprzednia nazwa projektu** | SKO (*Stacja Kontroli Opakowań*) — tylko w kontekście historycznym lub plików na dysku |

## Pliki inżynierskie (nazwy na dysku — bez zmiany)

| Plik | Uwagi |
|------|--------|
| `plc/SKO-Program.pdw` | Projekt WinProLadder w sterowniku (nazwa historyczna) |
| `plc/SKO-Program.pdf` | Eksport drabinki |
| `schemat_elektryczny/SKO.qet` | Schemat QET |
| `hmi/SKO - Program HMI.*` | Projekt panelu FvDesigner |

Docelowy program po refaktoryzacji: **`Vertino-Program.pdw`** (kopia po wdrożeniu).

## Kody dokumentów

| Dokument | Kod |
|----------|-----|
| Instrukcja operatora | IU-VTN-001 |
| Instrukcja serwisanta | IS-VTN-001 |
| Mapowanie PLC | REF-MAP-VTN |
| Numer seryjny (nowy) | VERTINO-MO-2025-___________ |

Seria **SKO-MO-2025** — ten sam egzemplarz maszyny przed rebrandem.

## Program PLC w dokumentacji

| Wersja | Sieci | Plik opisu |
|--------|-------|------------|
| Produkcja (sterownik) | 78 (N0000–N0077) | [plc/01_odszyfrowanie_starego_programu.md](plc/01_odszyfrowanie_starego_programu.md) |
| Docelowa **Vertino** | 35 (N0000–N0034) | [plc/03_program_vertino_sieci.md](plc/03_program_vertino_sieci.md) |

## Linki wewnętrzne

- Folder PLC w dokumentacji: `dokumentacja/plc/` (nie `04_plc/`).
- Z poziomu `dokumentacja/plc/*.md` linkuj `lista_sieci.md`, nie `plc/lista_sieci.md`.

**© CNC Solutions**
