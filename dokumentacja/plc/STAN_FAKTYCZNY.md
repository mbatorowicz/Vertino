# Stan faktyczny — co jest w sterowniku dziś

**Maszyna:** Vertino | **Plik w PLC:** `plc/SKO-Program.pdw` (nazwa historyczna)  
**Program:** **78 sieci** N0000–N0077 w `Main_unit1` — to jest **jedyny** program wgrany w maszynę.

> Dokumenty opisujące **35 sieci** ([03_program_vertino_sieci.md](03_program_vertino_sieci.md)) to **plan** — nie jest jeszcze w sterowniku.

---

## Jedno miejsce na każdy temat

| Temat | Dokument | Opisuje stan |
|-------|----------|--------------|
| I/O, rejestry R/M/D/C/T | [mapowanie.md](mapowanie.md) | Hardware + program **produkcyjny** |
| Lista sieci | [lista_sieci.md](lista_sieci.md) | Produkcyjny |
| Każda sieć (PDF) | [sieci/](sieci/) | Produkcyjny |
| Mnemoniki | [mnemotechniki.txt](mnemotechniki.txt) | Produkcyjny |
| Luki / co poprawić | [audyt.md](audyt.md) | Produkcyjny vs wymagania |
| Patch przed pełną przebudową | [wdrozenie_drabinka_A0_A1.md](wdrozenie_drabinka_A0_A1.md) | Opcjonalnie w **78 sieciach** |
| Program po refaktoryzacji | [03_program_vertino_sieci.md](03_program_vertino_sieci.md) | **Plan** (nie w PLC) |

---

## Zachowanie B4 w programie produkcyjnym (fakty)

| Element | Stan w sterowniku |
|---------|-------------------|
| Nowy cykl M21 | Blokada przy X4 / M1050 (N0019) |
| Zliczanie C1 w M22 | **Bez** blokady X4 — liczy przy zatorze |
| Koniec partii C1≥R1400 | **Bez** blokady X4 |
| Obrót M25 | Bez X4 |
| M507, R1507, D204 | N0041–N0046 |

Wymaganie procesowe (pauza, C1 bez resetu): **[audyt.md](audyt.md)** A0 — do wdrożenia w PLC lub przez program docelowy 03.

---

## Proces na maszynie (operator)

Opis cyklu i HMI: [../maszyna.md](../maszyna.md), [../operator.md](../operator.md).  
Diagramy **planowanego** programu: [../mapy_procesu.md](../mapy_procesu.md) (sekcja „Program docelowy”).

**© CNC Solutions**
