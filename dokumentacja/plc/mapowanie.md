# Mapowanie rejestrów PLC — Vertino

**Sterownik:** FATEK HB1-14MBJ25 | **Program:** 78 sieci (N0000–N0077)

> Numeracja WinProLadder: **N0000–N0077**. Stara numeracja projektu 001–072 = sieci **N0002–N0077** (N0000–N0001: bezpieczeństwo). Pełna lista z indeksem N: [lista_sieci.md](lista_sieci.md).



---

## Wejścia cyfrowe (24 V DC, PNP)

| Ref | Nazwa | Opis |
|-----|-------|------|
| X0 | SAFETY_STATUS | Pilz PNOZ X7 774303 — wyjście 13/14 |
| X1 | SENSOR_B1 | Bariera ultradźwiękowa — zliczanie (1 impuls / słoik) |
| X2 | SENSOR_B2 | Czujnik wyjścia |
| X3 | SENSOR_B3 | Czujnik HOME 0° |
| X4 | SENSOR_B4 | Kontrola przepływu (zewnętrzny transporter) |

**B4 (X4):** czujnik na **wyjściu** — linia odbiorcza zajęta. **R1507** = 1 gdy X4 = ON.

### B4 w programie **produkcyjnym** (stan w sterowniku)

| Sieć | Zachowanie |
|------|------------|
| N0019 | Start cyklu M21 — tylko przy `/X4` i `/M1050` |
| N0021–N0023 | Zliczanie i koniec partii — **bez** warunku X4 w drabince |
| N0030 | Start obrotu — **bez** X4 |
| N0041–N0046 | R1507, M507, D204 |

**Wymaganie procesu** (pauza przy zatorze, C1 bez resetu): nie w pełni zrealizowane — [audyt.md](audyt.md) A0.  
**Plan naprawy:** [03_program_vertino_sieci.md](03_program_vertino_sieci.md) N0008, N0017–N0018 lub [wdrozenie_drabinka_A0_A1.md](wdrozenie_drabinka_A0_A1.md).

## Wyjścia cyfrowe (24 V DC, NPN)

| Ref | Nazwa | Opis |
|-----|-------|------|
| Y0 | TRANSPORT_PULSE | Impulsy transportu (serwo) |
| Y1 | TRANSPORT_DIR | Kierunek transportu |
| Y2 | ROTATION_PULSE | Impulsy obrotu (serwo) |
| Y3 | ROTATION_DIR | Kierunek obrotu |
| Y4 | SYSTEM_READY | Sygnalizacja gotowości |
| Y5 | PNEUMATIC_VALVE | Zawór przedmuchu |

---

## Flagi M

### System i proces

| Ref | Nazwa |
|-----|-------|
| M1 | Bezpieczeństwo aktywne |
| M10 | System gotowy |
| M21 | Start cyklu |
| M22 | Transport aktywny |
| M23 | Stabilizacja |
| M24 | Obrót OK |
| M25 | Obrót aktywny |
| M70 | Praca automatyczna |
| M80 | Żądanie HOME |
| M82 | HOME OK |
| M100 | Tryb ręczny OK |
| M110 | Transport FWD |
| M111 | Transport REV |
| M112 | Obrót CW |
| M113 | Obrót CCW |
| M114 | Obrót +90° |
| M115 | Obrót -90° |
| M200 | Reset błędów |
| M233 | Ilość OK |
| M240 | Przedmuch ręczny |

### Błędy

| Ref | Nazwa |
|-----|-------|
| M501 | Błąd pozycji wejścia |
| M502 | Błąd pozycji wyjścia |
| M503 | Błąd parametrów |
| M504 | Błąd HOME |
| M505 | Timeout transportu |
| M506 | Timeout obrotu |
| M507 | Status transportera (HMI) |
| M520 | Detekcja zbocza B4 |

### HMI

| Ref | Funkcja |
|-----|---------|
| M1000 | RESET |
| M1001 | START AUTO |
| M1002 | STOP AUTO |
| M1003 | HOME REQUEST |
| M1010 | Transport FWD — START |
| M1011 | Transport FWD — STOP |
| M1012 | Transport REV — START |
| M1013 | Transport REV — STOP |
| M1014 | Obrót CW — START |
| M1015 | Obrót CW — STOP |
| M1016 | Obrót CCW — START |
| M1017 | Obrót CCW — STOP |
| M1019 | Test B4 — symulacja ON |
| M1020 | Test B4 — symulacja OFF |
| M1021 | Obrót +90° |
| M1022 | Obrót -90° |
| M1023 | Przedmuch ręczny ON |
| M1024 | Przedmuch ręczny OFF |
| M1050 | Symulacja B4 |

### Serwo

| Ref | Nazwa |
|-----|-------|
| M1992 | Transport serwo aktywne |
| M1993 | Rotation serwo aktywne — koniec obrotu 90° |
| M1924 | First scan |

---

## Timery (FATEK HB1)

| Zakres | Baza czasu |
|--------|------------|
| T0–T49 | 0,01 s |
| T50–T199 | 0,1 s |
| T200–T255 | 1 s |

Czas [s] = baza × PV.

| Ref | Baza | PV | Czas | Rola |
|-----|------|-----|------|------|
| T5 | 0,01 s | K30000 | 300 s | Timeout transportu → M505 |
| T6 | 0,01 s | R1410 | wg R1410 | Stabilizacja (M23) |
| T7 | 0,01 s | K8000 | 80 s | Timeout obrotu → M506 |
| T8 | 0,01 s | R1411 | wg R1411 | Pauza między cyklami |
| T10 | 0,01 s | K8000 | 80 s | Timeout HOME → M504 |
| T50 | 0,1 s | — | pomiar | Czas cyklu → R1500 [ms] |
| T200 | 1 s | — | — | Licznik godzin H10 (3600 s = 1 h) |

---

## Licznik C

| Ref | Opis |
|-----|------|
| C1 | Licznik bieżącej partii transportu; limit **R1400**; wartość **utrzymywana** w rejestrze do jawnego resetu |

**Pauza B4:** nie trzeba „zapisywać” C1 — wystarczy **nie wykonywać RST C1** i **nie zliczać** `( C )` podczas pauzy. Po zwolnieniu linii liczenie kontynuuje od tej samej wartości C1.

---

## Rejestry R — parametry

| Ref | Nazwa | Zakres | Domyślnie | Uwagi |
|-----|-------|--------|-----------|--------|
| R1400 | Opakowania w partii | 1–10 | 3 | C1; walidacja N0033–N0034 |
| R1401 | Prędkość transportu [Hz] | 50–500 | 200 | Walidacja N0035–N0036; FUN140 Transport |
| R1402 | Prędkość obrotu [Hz] | 100–1000 | 400 | Walidacja N0037–N0038; FUN140 Obrót |
| R1403 | Impulsy na 90° | 12400–12600 | 12500 | Walidacja N0039–N0040 |
| R1410 | Czas stabilizacji [ms] | 50–1000 | 200 | Timer T6 |
| R1411 | Pauza po obrocie [ms] | 50–500 | 100 | Timer T8 |
| R1412 | Potwierdzenie zatoru B4 [ms] | 100–3000 | 500 | Tylko program **docelowy** 03 (T52→M507) |

Poza zakresem → M503.

## Rejestry R — diagnostyka

| Ref | Nazwa |
|-----|-------|
| R1500 | Czas ostatniego cyklu [ms] |
| R1501 | Pozycja modułu [0°/90°/180°/270°] |
| R1507 | Status zewn. transportera (0/1) |

## Rejestry R — tabele serwo (Table.tab)

| Nazwa tabeli | Rejestr | Funkcja |
|--------------|---------|---------|
| Transport_AUTO | R1100 | Program pozycjonowania transportu — automatyczny |
| Transport_Parameters | R1120 | Parametry FUN141 — oś transportu |
| Rotation_AUTO | R1200 | Program pozycjonowania obrotu — 90° |
| Rotation_Parameters | R1220 | Parametry FUN141 — oś obrotu |
| Transport FWD | R524 | Work register — transport ręczny do przodu |

- **FUN140** — ruch (sieci: FUN140 Transport, FUN140 Obrót, tryb ręczny, HOME procedure).
- **FUN141** — parametry osi (sieci: Parametry FUN141 — Transport / Obrót).

## Rejestry D

| Ref | Nazwa |
|-----|-------|
| D100 | Licznik partii całkowity |
| D200 | Błędy pozycji wejścia |
| D201 | Błędy pozycji wyjścia |
| D202 | Timeout transportu |
| D203 | Timeout obrotu |
| D204 | Aktywacje czujnika B4 |

## Rejestr H

| Ref | Opis |
|-----|------|
| H10 | Czas pracy [h] (T200) |

---

## Czujniki

| Symbol | Wejście | Funkcja |
|--------|---------|---------|
| B1 | X1 | Zliczanie w **M22** (N0022): **zbocze narastające** X1; kontrola strefy w **M233** |
| B2 | X2 | Kontrola wyjścia (M233) |
| B3 | X3 | HOME modułu obrotowego |
| B4 | X4 | Zator na linii odbiorczej — **pauza przepychania**, nie obrotu; stan ciągły (nie zbocze) |

---

## Lista sieci

Pełna lista N0000–N0077: **[lista_sieci.md](lista_sieci.md)** · szczegóły: **[sieci/](sieci/)**

---

## Procedura po awarii bezpieczeństwa

1. Usuń przyczynę (E-STOP, osłony).
2. Reset Pilz.
3. X0 = ON.
4. HMI → M1000 (reset błędów).
5. HOME (M1003 lub automatyczny).
6. M1001 — START.

---

**© CNC Solutions — Michał Batorowicz**
