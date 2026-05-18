# Analiza programu produkcyjnego (78 sieci)

**Sterownik:** FATEK HB1-14MBJ25 | **Źródło:** `plc/SKO-Program.pdf`  
**Stan:** program **wgrany w sterownik** — patrz [STAN_FAKTYCZNY.md](STAN_FAKTYCZNY.md).

Skrót wymagań i logiki AUTO przed refaktoryzacją. **Bez** powielania opisów sieci (są w [sieci/](sieci/)).

---

## Spis treści

1. [Wymagania procesu](#1-wymagania-procesu)
2. [Mapa zasobów](#2-mapa-zasobów)
3. [Logika AUTO — krok po kroku](#3-logika-auto)
4. [Wszystkie 78 starych sieci](#4-wszystkie-78-starych-sieci)
5. [Luki i błędy](#5-luki-i-błędy)
6. [FUN140 / tabele](#6-fun140--tabele)

---

## 1. Wymagania procesu

| # | Wymaganie | Stary PLC |
|---|-----------|----------|
| P1 | Pilz X0=1 → napędy dozwolone | M1, N0000–N0001 |
| P2 | HOME przed AUTO (M82) | M80/M25/B3, N0008–N0012, N0076 |
| P3 | Partia = R1400 impulsów B1 | C1 w M22 |
| P4 | Pauza B4: stop push, C1 zachowany, obrót OK | **niepełne** |
| P5 | Przedmuch tylko 180° | **błąd N0068** |
| P6 | Walidacja parametrów | N0033–N0040 → M503 |
| P7 | Timeouty transport/obrót/HOME | T5/T7/T10 → M505/M506/M504 |
| P8 | Tryb ręczny tylko bez AUTO | M100, N0052–N0053 |
| P9 | HMI: START/STOP/RESET/HOME/przyciski | M1000–M1024 |
| P10 | Diagnostyka D200–D204, R1500 | liczniki w sieciach błędów |

## 2. Mapa zasobów

### Wejścia / wyjścia

| Adres | Symbol | Rola |
|-------|--------|------|
| X0 | SAFETY_STATUS | Pilz — łańcuch bezpieczeństwa |
| X1 | SENSOR_B1 | Zliczanie + strefa wejścia |
| X2 | SENSOR_B2 | Strefa wyjścia |
| X3 | SENSOR_B3 | HOME 0° |
| X4 | SENSOR_B4 | Zator linii odbiorczej |
| Y0–Y1 | TRANSPORT | Impuls/kierunek SH-D08R |
| Y2–Y3 | ROTATION | Impuls/kierunek SS86D |
| Y4 | SYSTEM_READY | Lampka gotowości |
| Y5 | PNEUMATIC_VALVE | Przedmuch |

### Flagi sekwencji AUTO

| M | Znaczenie |
|---|----------|
| M10 | System gotowy (M1∧M82∧¬błędy) |
| M70 | Praca automatyczna |
| M21 | Krok: żądanie transportu / cykl |
| M22 | Zliczanie partii (B1→C1) |
| M23 | Stabilizacja (T6=R1410) |
| M233 | Ilość OK — strefy sprawdzone |
| M24 | Gotowy do obrotu |
| M25 | Obrót 90° w toku |
| M507 | Linia odbiorcza zajęta (X4∨M1050) |
| M1992/M1993 | Serwo transport/obrót aktywne |

## 3. Logika AUTO

```
M1001 + M10 → M70
Pętla: M21 → [FUN140 push] → M22 (C1++) → M23 (T6) → strefy B1/B2 → M24 → M25 [FUN140 90°] → T8 → M21
Warunek wejścia w M21: ¬M507 (B4 wolny), ¬M1050
Obrót (M25): bez warunku B4
```

---

## 4. Opis sieci (jedno miejsce)

Bez powielania treści w tym pliku:

| Zasób | Plik |
|-------|------|
| Lista N0000–N0077 | [lista_sieci.md](lista_sieci.md) |
| Adres → sieć | [indeks_krzyzowy.md](indeks_krzyzowy.md) |
| Mnemoniki | [mnemotechniki.txt](mnemotechniki.txt) |
| Opis każdej sieci | [sieci/](sieci/) |

## 5. Luki i błędy

→ **[audyt.md](audyt.md)** (stan programu w sterowniku vs wymagania procesu).

---

## 6. FUN140 — tabele (bez zmian w nowym programie)

| Tabela | SR | Użycie |
|--------|-----|--------|
| Transport AUTO | R1100 | Push partii, M21 |
| Obrót 90° | R1200 | M25, R1402/R1403 |
| HOME | R1300 | M80, B3 |
| Parametry | R1120, R1220 | FUN141 @ M1924 |

Wartości R1100–R1108, R1200–R1208, R1300–R1308 — patrz [techniczna.md](../techniczna.md).

**© CNC Solutions**
