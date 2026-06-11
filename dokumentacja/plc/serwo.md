# Serwo modułu obrotowego — konfiguracja PSO1

**Źródło:** wydruk [plc/SKO-Program.pdf](../../plc/SKO-Program.pdf) — tabele Table1–Table3
i konfiguracja I/O. Eksport tabel: [plc/export/tabele.tab](../../plc/export/tabele.tab).

Oś obrotu modułu pracuje na wyjściu impulsowym **PSO1**:

| Sygnał | Wyjście | Tryb |
|--------|---------|------|
| PLS (impulsy) | Y2 | Pulse + Direction |
| DIR (kierunek) | Y3 | |

Obsługa w programie: FUN141 MPARA (zapis parametrów, sieć N0015)
i FUN140 HSPSO (wykonanie programu ruchu, sieci N0017 i N0028) — [program.md](program.md).

---

## Table1 — parametry osi (R1200–R1223)

| Parametr | Wartość | Uwagi |
|----------|---------|-------|
| Unit | 2: Combine | Pozycje w impulsach (Ps), prędkości w Hz |
| Pulse/Rev | 10000 | Impulsów na obrót silnika |
| Distance/Rev | 360 | Jednostek na obrót |
| Min. Unit | 2 | |
| Max. Speed | 200000 | |
| Start/End Speed | 1 | |
| Creep Speed | 2000 | Prędkość dojazdu przy bazowaniu |
| Acc./Dec. Time | 20000 | |
| Direction Control | 0: Up | |
| Zero Return Direction | 1: Down (Left) | Kierunek najazdu na bazę |
| Interpolation Time Constant | 500 | |
| DOG Input | Normal Open, **wejście 2 (X2)** | Czujnik bazowania |
| Stroke / PG0 / CLR | Not Used | |
| Machine Zero Point | 1000 | **R1221** — edytowalny z HMI jako „Offset bazy" |
| PG0 Count | 1 | |

> DOG na X2 oznacza, że czujnik bazowania modułu jest obsługiwany sprzętowo
> przez funkcję DRVZ — dlatego X2 nie występuje w drabince.

## Table2 — program HOME (R1300–R1319)

| Krok | Polecenie | Prędkość | Zakończenie |
|------|-----------|----------|-------------|
| 1 | DRVZ (najazd na bazę), MD1 | 5000 | GOTO NEXT |
| 2 | DRV ABS 0 (pozycja absolutna 0) | 5000 | MEND |

Wywołanie: FUN140, SR:R1300, WR:R1500 (sieć N0017, krok S10 HOMING).
Po DN (M461) program zeruje R1501 i ustawia M470 HOME_OK.

## Table3 — program ROTATE (R1400–R1410)

| Krok | Polecenie | Prędkość | Zakończenie |
|------|-----------|----------|-------------|
| 1 | DRV ADR **−25000 Ps** (ruch względny), WAIT TIME 100 | 9000 | GOTO END |

Wywołanie: FUN140, SR:R1400, WR:R1510 (sieć N0028, krok S13 OBRÓT).

−25000 impulsów = 2.5 obrotu silnika (przy 10000 imp/obr) = **obrót modułu o 90°**
(przełożenie przekładni 10:1). Pełny obrót modułu = 4 cykle.

## Napęd osi (wg schematu elektrycznego)

| Element | Typ |
|---------|-----|
| Sterownik | Step Servo Driver **SS86D** (zasilanie AC 18–80 V) |
| Silnik | iCAN **57BLF-1830NBB**, 3000 RPM, 188 W, z enkoderem (step-servo, praca w zamkniętej pętli) |
| Sygnały | PUL+ ← Y2, DIR+ ← Y3 |

Schemat: [schemat_elektryczny/SKO.pdf](../../schemat_elektryczny/SKO.pdf), strona 5.

---

## Zmiana parametrów

1. Wartości tabel edytować w WinProLadder (Servo Parameter/Program Table) —
   nie bezpośrednio w rejestrach.
2. Po zmianie Table1 parametry wgrywają się do osi przy pierwszym skanie (M1924)
   lub po wyzwoleniu **M305** z HMI (nie podczas ruchu osi).
3. Zmiany Table2/Table3 obowiązują od następnego wywołania FUN140.

## Rejestry robocze

| Obszar | Funkcja |
|--------|---------|
| R1500– | WR bazowania (R1501 — pozycja, zerowana po DN) |
| R1510– | WR obrotu (R1511 — zerowany po DN) |

---

**© CNC Solutions — Michał Batorowicz**
