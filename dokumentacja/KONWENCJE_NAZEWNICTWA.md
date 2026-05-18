# Konwencje nazewnictwa — Vertino

## Nazwa produktu

| Użycie | Forma |
|--------|--------|
| **Nazwa handlowa** | **Vertino** |
| **Pełna nazwa** | **Vertino — Stacja oczyszczania opakowań** |
| **SKO** | Tylko: nazwy plików na dysku, stara seria dokumentów |

## Stan faktyczny vs plan (bez duplikatów)

| Pytanie | Jedyna odpowiedź w dokumentacji |
|---------|----------------------------------|
| Co jest **w sterowniku**? | [plc/STAN_FAKTYCZNY.md](plc/STAN_FAKTYCZNY.md) → 78 sieci, `SKO-Program.pdw` |
| Co **planujemy** wgrać? | [plc/03_program_vertino_sieci.md](plc/03_program_vertino_sieci.md) → 35 sieci |
| Mapowanie I/O (hardware) | [plc/mapowanie.md](plc/mapowanie.md) |
| Opis każdej sieci **produkcyjnej** | [plc/sieci/](plc/sieci/) + [lista_sieci.md](plc/lista_sieci.md) |
| Co poprawić w PLC | [plc/audyt.md](plc/audyt.md) |
| Router PLC | [plc/program.md](plc/program.md) |

**Nie używamy** osobnych „wersji” opisujących to samo (usunięto m.in. `02_program_nowy_sieci.md`).

## Pliki na dysku (nazwy historyczne)

| Plik | Znaczenie |
|------|-----------|
| `plc/SKO-Program.pdw` / `.pdf` | Program **w sterowniku** |
| `Vertino-Program.pdw` | Nazwa po wdrożeniu programu docelowego |
| `schemat_elektryczny/SKO.qet` | Schemat |
| `hmi/SKO - Program HMI.*` | Panel |

## Kody dokumentów

| Dokument | Kod |
|----------|-----|
| Instrukcja operatora | IU-VTN-001 |
| Instrukcja serwisanta | IS-VTN-001 |
| Numer seryjny | VERTINO-MO-2025-___________ |

## Linki w `dokumentacja/plc/`

Z poziomu folderu `plc/`: `lista_sieci.md`, nie `plc/lista_sieci.md`.

**© CNC Solutions**
