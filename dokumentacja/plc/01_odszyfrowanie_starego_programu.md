# 01 — Odszyfrowanie programu produkcyjnego (78 sieci)

**Sterownik:** FATEK HB1-14MBJ25 | **Źródło:** `plc/SKO-Program.pdf` (78 sieci N0000–N0077)

Dokument służy do **niczego nie pominąć** przed pisaniem programu od nowa.

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

## 4. Wszystkie 78 starych sieci

### N0000 — Bezpieczeństwo ON

```text
Bezpieczeństwo ON
```

### N0001 — Bezpieczeństwo OFF

```text
X0
M1
Bezpiecz
Bezpieczeństwo OFF
```

### N0002 — Reset błędów z HMI

```text
X0
M1
Bezpiecz
Reset błędów z HMI
```

### N0003 — System gotowy SET

```text
M1000
RESET
M200
Reset
System gotowy - warunek SET
```

### N0004 — System gotowy RESET

```text
M1
Bezpiecz
M82
HOME OK
M503
M504
HOME
M505
Timeout
M506
Timeout
M10
System gotowy - warunek RESET
```

### N0005 — Reset wszystkich błędów

```text
M1
Bezpiecz
M10
M82
HOME OK
M503
M504
HOME
M505
Timeout
M506
Timeout
Reset wszystkich błędów
```

### N0006 — START AUTO

```text
M200
Reset
M1
Bezpiecz
M501
M502
M503
M504
HOME
M505
Timeout
M506
Timeout
M507
M200
Reset
START pracy automatycznej
```

### N0007 — STOP AUTO

```text
M1001
M10
M70
```

### N0008 — Żądanie HOME przy starcie

```text
M10
M70
M1002
Żądanie HOME przy starcie
```

### N0009 — HOME ręczny HMI

```text
M1
Bezpiecz
M82
HOME OK
M80
HOME
HOME ręczny z HMI
```

### N0010 — Start procedury HOME

```text
M1003
HOME
M100
M80
HOME
Start procedury HOME
```

### N0011 — Koniec HOME B3

```text
M80
HOME
M10
M25
Obrót
M25
Obrót
Timeout HOME
Koniec HOME na czujniku B3
```

### N0012 — Timeout HOME

```text
X3
M25
Obrót
M80
HOME
M25
Obrót
M82
HOME OK
M80
HOME
EN RST T10
Timeout HOME
Timeout HOME
```

### N0013 — FUN141 Transport

```text
Timeout
HOME
M504
HOME
M25
Obrót
M80
HOME
Parametry FUN141 - Transport
```

### N0014 — FUN141 Obrót

```text
M1924
First
141.MPARA
M503
Parametry FUN141 - Obrót
```

### N0015 — FUN140 Transport

```text
M1924
First
141.MPARA
M503
FUN140 Transport
```

> **Uwagi:** BRAK: blokada FUN140 transport przy zatorze.

### N0016 — FUN140 Obrót

```text
M21
140.HSPSO
M1992
M501
M21
FUN140 Obrót
```

### N0017 — READY Transport

```text
M25
Obrót
140.HSPSO
M1993
M502
M25
Obrót
Status READY Transport
```

### N0018 — READY Rotation

```text
M1992
```

### N0019 — Start cyklu Y4

```text
M1993
Start cyklu
```

### N0020 — Start transportu M21

```text
M70
M10
M21
M22
M23
M24
Obrót OK
M25
Obrót
X4
M1050
M21
Start transportu
```

> **Uwagi:** OK: start M21 tylko przy wolnym B4 (/X4, /M1050).

### N0021 — Wejście w zliczanie M22

```text
M21
M22
M22
EN RST C1
Licznik opakowań
Timeout transpor
```

### N0022 — Liczenie B1 → C1

```text
X1
M22
Licznik opakowań
```

> **Uwagi:** BRAK: /M507 przy zliczaniu i końcu partii.

### N0023 — Koniec partii C1≥R1400

```text
174. C1
Licznik opakowań
>= R1400
M22
M233
Koniec transportu
```

### N0024 — Stabilizacja M23 T6

```text
M233
M22
M23
Timer stabilizac
```

### N0025 — Kontrola strefy B1

```text
X1
M23
Timer st
M501
Licznik błędów wejścia
```

### N0026 — Kontrola strefy B2

```text
M501
```

### N0027 — Koniec stabilizacji

```text
X2
M23
Timer st
M502
Licznik błędów wyjścia
```

### N0028 — Pozycja OK M24

```text
M502
```

### N0029 — Start obrotu M25

```text
Timer st
M501
M502
M23
M24
Obrót OK
M21
M233
Start obrotu
```

> **Uwagi:** OK: obrót bez blokady B4.

### N0030 — Koniec obrotu

```text
M24
Obrót OK
M25
Obrót
M25
Obrót
Timeout obrotu
```

### N0031 — Timeout transportu T5

```text
M1993
M25
Obrót
M1992
M25
Obrót
M24
Obrót OK
EN RST T7
Timeout obrotu
Licznik partii c
Timeout transportu
```

> **Uwagi:** RYZYKO: timeout T5 podczas oczekiwania na B4.

### N0032 — Timeout obrotu T7

```text
Timeout
M505
Timeout
M22
Timeout transpor
Timeout obrotu
```

### N0033 — Walidacja R1400 min

```text
Timeout
M506
Timeout
M25
Obrót
Timeout obrotu
```

### N0034 — Walidacja R1400 max

```text
M503
```

### N0035 — Walidacja R1401 min

```text
M503
Walidacja prędkości transportu - minimum
```

### N0036 — Walidacja R1401 max

```text
M503
Walidacja prędkości transportu - maksimum
```

### N0037 — Walidacja R1402 min

```text
M503
```

### N0038 — Walidacja R1402 max

```text
M503
```

### N0039 — Walidacja R1403 min

```text
M503
```

### N0040 — Walidacja R1403 max

```text
M503
```

### N0041 — R1507 B4 zajęty

```text
M503
Status zewnętrznego transportera - zajęty
```

### N0042 — Status M507 zajęty

```text
X4
Status zewnętrznego transportera - wolny
```

### N0043 — HMI status SET

```text
X4
Flaga statusu dla HMI - SET
```

### N0044 — HMI status RESET

```text
X4
M507
M1050
Flaga statusu dla HMI - RESET
```

### N0045 — Zbocze B4 D204

```text
X4
M1050
M507
```

### N0046 — Reset zbocza B4

```text
X4
M520
M520
Reset detekcji zbocza
```

### N0047 — Pozycja HOME R1501=0

```text
X4
M520
Aktualizacja pozycji - HOME
```

### N0048 — Pozycja +90° R1501

```text
M82
HOME OK
M25
Obrót
Aktualizacja pozycji - obrót +90°
```

### N0049 — Reset R1501 po 360°

```text
M1993
Reset pozycji na 0° po 360°
```

### N0050 — Start pomiaru T50

```text
M1993
174. R1501
>= 360
Start pomiaru czasu cyklu
```

### N0051 — Zapis czasu R1500

```text
M21
```

### N0052 — Tryb ręczny SET M100

```text
EN RST T50
Warunki trybu ręcznego - SET
```

### N0053 — Tryb ręczny RESET

```text
M10
M70
M100
Warunki trybu ręcznego - RESET
```

### N0054 — Transport FWD start

```text
M10
M70
M100
Transport FWD - START
```

### N0055 — Transport FWD stop

```text
M1010
M100
M110
Transport FWD - STOP
```

### N0056 — Transport REV start

```text
M1011
M110
Transport REV - START
```

### N0057 — Transport REV stop

```text
M1012
M100
M111
Transport REV - STOP
```

### N0058 — Obrót CW start

```text
M1013
M111
Obrót CW - START
```

### N0059 — Obrót CW stop

```text
M1014
M100
M112
Obrót CW
Obrót CW - STOP
```

### N0060 — Obrót CCW start

```text
M1015
M112
Obrót CW
Obrót CCW - START
```

### N0061 — Obrót CCW stop

```text
M1016
M100
M113
Obrót
Obrót CCW - STOP
```

### N0062 — Obrót +90°

```text
M1017
M113
Obrót
Obrót +90°
```

### N0063 — Obrót -90°

```text
M1021
M100
M114
Obrót
M114
Obrót
Obrót -90°
```

### N0064 — Przedmuch ręczny ON

```text
M1022
M100
M115
Obrót
M115
Obrót
Przedmuch ręczny ON
```

### N0065 — Przedmuch ręczny OFF

```text
M1023
M100
M240
Przedmuch ręczny OFF
```

### N0066 — Symulacja B4 ON

```text
M1024
M240
```

### N0067 — Symulacja B4 OFF

```text
M1019
M100
M1050
```

### N0068 — Przedmuch AUTO

```text
M1020
M1050
Przedmuch AUTO
```

> **Uwagi:** BŁĄD: Y5 włączony przez całe M70 (przedmuch non-stop w AUTO).

### N0069 — Przedmuch ręczny Y5

```text
M70
Przedmuch ręczny
```

### N0070 — Transport FWD ręczny

```text
M240
Transport FWD ręczny
```

### N0071 — Transport REV ręczny

```text
M110
140.HSPSO
Transport FWD
Transport REV ręczny
```

### N0072 — Obrót CW ręczny

```text
M111
140.HSPSO
Obrót CW ręczny
```

### N0073 — Obrót CCW ręczny

```text
M112
Obrót CW
140.HSPSO
Obrót CCW ręczny
```

### N0074 — Obrót +90° ręczny

```text
M113
Obrót
140.HSPSO
Obrót +90° ręczny
```

### N0075 — Obrót -90° ręczny

```text
M114
Obrót
140.HSPSO
M114
Obrót
Obrót -90° ręczny
```

### N0076 — HOME procedure

```text
M115
Obrót
140.HSPSO
M115
Obrót
HOME procedure
```

### N0077 — Koniec ORG

```text
M80
HOME
140.HSPSO
00001M  ORG        X0
00002M  OUTS       M1
00003M  ORG   NOT  X0
00004M  OUTR       M1
00005M  ORG        M1000
00006M  OUTS       M200
00007M  ORG        M1
00008M  AND        M82
00009M  AND   NOT  M503
00010M  AND   NOT  M504
00011M  AND   NOT  M505
00012M  AND   NOT  M506
00013M  OUTS       M10
00015M  LD    NOT  M1
00016M  OR    NOT  M82
00017M  OR         M503
00018M  OR         M504
00019M  OR         M505
00020M  OR         M506
00022M  OUTR       M10
00023M  ORG        M200
00024M  AND        M1
00026M  OUTR       M501
00027M  OUTR       M502
00028M  OUTR       M503
00029M  OUTR       M504
00030M  OUTR       M505
```

---

## 5. Luki i błędy (checklist migracji)

- **N0015** FUN140 Transport: BRAK: blokada FUN140 transport przy zatorze.
- **N0020** Start transportu M21: OK: start M21 tylko przy wolnym B4 (/X4, /M1050).
- **N0022** Liczenie B1 → C1: BRAK: /M507 przy zliczaniu i końcu partii.
- **N0029** Start obrotu M25: OK: obrót bez blokady B4.
- **N0031** Timeout transportu T5: RYZYKO: timeout T5 podczas oczekiwania na B4.
- **N0068** Przedmuch AUTO: BŁĄD: Y5 włączony przez całe M70 (przedmuch non-stop w AUTO).

**Dodatkowo:** 8 sieci walidacji (N0033–N0040) można zastąpić **jedną** siecią walidacji. 12 sieci ręcznych start/stop (N0054–N0061) można zastąpić **2 sieciami** z podtrzymaniem M110–M113.

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
