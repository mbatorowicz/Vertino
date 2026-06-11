# Propozycja poprawek i rozbudowy programu

**Status:** PROPOZYCJA — do wdrożenia w WinProLadder (PLC) i FvDesigner (HMI).
**Baza:** bieżący program 31 sieci ([program.md](program.md)), mapa adresów ([mapa_io.md](mapa_io.md)).

Zakres:

- **P1–P6** — poprawki ryzyk wykrytych w audycie programu
- **R1** — tryb serwisowy (ruchy ręczne z HMI)
- **R2** — nastawy prędkości i przyspieszenia serwo z HMI
- **R3** — liczniki statystyczne i czas cyklu
- **R4** — kluczyk przezbrajania (X4), ekran BS6, trzy prędkości obrotu
- **HMI** — nowe ekrany i obiekty

---

## Nowe adresy (zweryfikowane jako wolne)

| Adres | Funkcja | Kierunek |
|-------|---------|----------|
| M311 | Zeruj licznik partii C0 | HMI → PLC |
| M312 | Zeruj statystyki | HMI → PLC |
| M320 | Tryb serwisowy — **włączany przy wejściu na ekran BS3** (HMI) | HMI ↔ PLC |
| M340 | Transport jog (przytrzymany) | HMI → PLC |
| M341 | Przedmuch ręczny | HMI → PLC |
| M342 | Obrót serwis +90° (BS3, R14) | HMI → PLC |
| M343 | Obrót przezbrajania +90° „góra/lewo" (BS6, R11) | HMI → PLC |
| M344 | Obrót przezbrajania −90° „dół/prawo" (BS6, R11) | HMI → PLC |
| M330 | Przezbrajanie aktywne (= **X4**, styk NO kluczyka) | hardware → PLC |
| M536 | Przezbrajanie: ruch w toku (sygnalizacja HMI) | PLC → HMI |
| M530 | Alarm: timeout bazowania | PLC → HMI (latch) |
| M531 | Alarm: timeout obrotu | PLC → HMI (latch) |
| M532 | Alarm: błąd bazowania (serwo) | PLC → HMI (latch) |
| M533 | Alarm: błąd obrotu (serwo) | PLC → HMI (latch) |
| M534 | Alarm: błąd parametrów serwo | PLC → HMI (latch) |
| M535 | Alarm: bezpieczeństwo / E-stop | PLC → HMI (latch) |
| M539 | Nastawy poprawne (warunek startu) | wewnętrzny |
| R9 | Timeout bazowania [× 0.1 s] (zalecane 300 = 30 s) | HMI → PLC |
| R10 | Timeout obrotu [× 0.1 s] (zalecane 100 = 10 s) | HMI → PLC |
| X4 | KEY_PRZEBRAJ — styk **NO** kluczyka (ON = tryb **przezbrajania**) | hardware → PLC |
| R11 | Prędkość obrotu **przezbrajania** (32-bit) — BS6 | HMI → PLC |
| R12 | Przyspieszenie obrotu przezbrajania | HMI → PLC |
| R13 | Timeout obrotu przezbrajania [× 0.1 s] | HMI → PLC |
| R14 | Prędkość obrotu **serwisowa** (32-bit) — BS3 | HMI → PLC |
| R1412 | Bufor: zapis R1403 przed obrotem przezbrajania | wewnętrzny |
| R1413 | Bufor: zapis R1211 przed obrotem przezbrajania | wewnętrzny |
| R201 | Czas ostatniego cyklu [× 0.1 s] | PLC → HMI |
| D100 | Licznik partii (całkowity) | PLC → HMI |
| D102 (32-bit) | Licznik sztuk (całkowity) | PLC → HMI |
| T51 | Timer timeoutu bazowania (0.1 s) | — |
| T52 | Timer timeoutu obrotu (0.1 s) | — |
| T53 | Timer timeoutu obrotu przezbrajania (0.1 s, nastawa R13) | — |
| T55 | Pomiar czasu cyklu (0.1 s) | — |

Rejestry tabel serwo edytowane z HMI (istniejące): R1403 (prędkość obrotu),
R1303/R1312 (prędkości bazowania), R1209 (creep), R1211 (acc/dec), R1221 (offset bazy).

---

# Część 1 — poprawki (P)

## P1 — Timeout bazowania

**Problem:** awaria napędu/czujnika DOG → maszyna wisi w S10 bez alarmu.

Nowa sieć (za N0030):

```
|--[S10]--[/M461]--[T51 .1 R9]--|
|--[T51]--( SET M530 )--( SET S3 )--|
```

```
ORG        S10
AND   NOT  M461
T51   .1   R9
ORG        T51
AND        SHORT
SET( )     M530
SET( )     S3
```

S3 kasuje S10 (istniejąca N0001), co pauzuje FUN140 (wejście PAU w N0017 już
zawiera S3) i zwalnia timer.

## P2 — Timeout obrotu

Analogicznie dla S13:

```
|--[S13]--[/M432]--[T52 .1 R10]--|
|--[T52]--( SET M531 )--( SET S3 )--|
```

```
ORG        S13
AND   NOT  M432
T52   .1   R10
ORG        T52
AND        SHORT
SET( )     M531
SET( )     S3
```

## P3 — Latche przyczyn alarmów + wymuszenie HOME po błędzie ruchu

**Problem:** wyjścia ERR FUN140 są chwilowe — HMI nie wie, co było przyczyną
alarmu; po błędzie serwo można startować bez ponownego bazowania (M470 zostaje).

Nowe sieci:

```
|--[M462]--( SET M532 )--|
|--[M433]--( SET M533 )--|
|--[M468]--( SET M534 )--|
|--[/X0]--( SET M535 )--|
|--[M530 + M531 + M532 + M533]--( RST M470 )--|
```

```
ORG        M462
SET( )     M532
ORG        M433
SET( )     M533
ORG        M468
SET( )     M534
ORG   NOT  X0
SET( )     M535
ORG        M530
OR         M531
OR         M532
OR         M533
RST( )     M470
```

RST M470 wymusza ponowne bazowanie (START wymaga M470 — N0002) po każdym
błędzie/timeoucie ruchu osi.

Kasowanie latchy — rozszerzenie istniejącej N0006 (po RST S3 dopisać):

```
ORG        S3
AND        M302
AND        X0
RST( )     S3
RST( )     M530
RST( )     M531
RST( )     M532
RST( )     M533
RST( )     M534
RST( )     M535
```

## P4 — Walidacja nastaw + blokada startu

**Problem:** R6 = 0 → transport jedzie bez końca partii; brak kontroli zakresu.

Nowa sieć:

```
|--[R6 > 0]--[R6 < 21]--( M539 )--|
```

```
ORGF  171_.>
      Sa:  R6
      Sb:  0
ANDF  172_.<
      Sa:  R6
      Sb:  21
OUT        M539
```

Zmiana **N0002** (START) — dopisać dwa styki:

```
Było:   M300↑ · X0 · /S3 · M470          → SET S2
Będzie: M300↑ · X0 · /S3 · M470 · M539 · /M320 → SET S2
```

(`/M320` — start automatu zablokowany w trybie serwisowym.)
Zakresy pozostałych nastaw (R7–R10, prędkości) ograniczyć w FvDesigner
właściwościami min/max obiektów Numeric Input — patrz sekcja HMI.

## P5 — Partia nieztracona po STOP/alarmie

**Problem:** każde wejście w S11 i każdy alarm zeruje C0 — słoiki, które już
minęły B1, po wznowieniu są liczone drugi raz (partia może mieć nadmiar).

Zmiany w istniejących sieciach:

| Sieć | Zmiana |
|------|--------|
| N0001 (alarm) | **usunąć** `RST C0` |
| N0014 (S11↑) | **usunąć** `RST C0` |
| N0020 (HOME zakończone) | **dodać** `RST C0` (bazowanie = nowa partia) |
| N0029 (obrót zakończony) | **dodać** `RST C0` (partia odwrócona = licznik od zera) |

Nowa sieć — ręczne zerowanie z HMI (tylko poza pracą automatyczną):

```
|--[M311↑]--[/S2]--( RST C0 )--|
```

```
ORG   TU   M311
AND   NOT  S2
RST( )     C0
```

> Konsekwencja: po STOP w połowie partii i ręcznym opróżnieniu toru operator
> musi zewrzeć „Zeruj licznik" (M311) albo wykonać HOME. Opisać w instrukcji.

## P6 — Sygnalizacja pauzy B3 (bez zmian logiki)

M403 już istnieje — wystarczy lampka na HMI (sekcja HMI). Opcjonalnie licznik
aktywacji blokady: `M403↑ → (+1) R202` (diagnostyka spiętrzeń).

---

# Część 2 — rozbudowa (R)

## R1 — Tryb serwisowy (ekran BS3)

**Założenia:**

- tryb serwisowy **M320** włącza się przy **wejściu na ekran SERWIS (BS3)** i
  kasuje przy wyjściu (HMI: *On Screen Open* → Set M320, *On Leave* → Reset M320),
- **nie wymaga** kluczyka — osłona **musi być zamknięta** (B4 w Pilz, X4=OFF),
- ruchy serwisowe wymagają X0=ON; obrót serwisowy wymaga M470,
- M320 blokuje START automatu (P4).

### Sieci

```
|--[M320]--[S1]--[X0]--[/X4]--( M329 )--|     // serwis aktywny — bez klucza przezbrajania
```

```
ORG        M320
AND        S1
AND        X0
AND   NOT  X4
OUT        M329
```

Transport jog — **modyfikacja N0022** (BS3 i BS6 — patrz R4):

```
M410 + (M329 · M340) + (M330 · M340) → Y1
```

Przedmuch ręczny — **modyfikacja N0009**:

```
(M400 · /M403 · M421) + (M329 · M341) + (M330 · M341) → Y4
```

Obrót serwisowy +90° (BS3, **R14**):

```
|--[M329]--[M470]--[M342↑]--[/M431]--|
|          +--[FUN MOV R1403→R1412]--[FUN MOV R14→R1403]--|
|          +--( SET S13 )--|
```

Bazowanie — M310 (istnieje). Jog transportu celowo omija M403 (B3).

## R4 — Kluczyk przezbrajania, ekran BS6, trzy prędkości obrotu

**Cel:** wymiana tulei / prowadnic przy **otwartej osłonie**. Kluczyk sygnalizuje
**tryb przezbrajania** (nie tryb serwisowy). Tryb serwisowy to osobny ekran **BS3**.

### Trzy prędkości obrotu modułu

| Tryb | Ekran / warunek | Rejestr | Typowa wartość | Osłona |
|------|-----------------|---------|----------------|--------|
| **Produkcja** | automat S2 | **R1403** | 9000 Hz | zamknięta |
| **Serwis** | BS3, M329 (M320, X4=OFF) | **R14** | 4000 Hz | **zamknięta** |
| **Przezbrajanie** | BS6, M330 (= X4) | **R11** | 500 Hz | może być **otwarta** |

### Kluczyk — dwa obwody

| Styk | Połączenie | Klucz PRODUKCJA | Klucz PRZEBRAJANIE |
|------|------------|-----------------|---------------------|
| **NC** | Pilz PNOZ X7 | B4 w torze | B4 **pominięty** |
| **NO** | PLC **X4** | OFF | **ON** → M330 |

E-stop w obu pozycjach. **X0** z Pilz — styk NO **nie zastępuje** bezpieczeństwa.

### Ekran PRZEBRAJANIE (BS6)

Po **X4=ON** panel **automatycznie przechodzi na BS6** (*Screen Change* w HMI
przy X4↑ lub stała widoczność z wymuszeniem nawigacji).

**Zawartość BS6:**

1. **Instrukcja** (tekst statyczny):
   - klucz w pozycji przezbrajania, osłona może być otwarta,
   - obracaj moduł krokami, nie wkładaj rąk w gniazda podczas ruchu,
   - po wymianie: klucz → produkcja, zamknij osłonę, HOME.
2. **Przyciski obrotu modułu** (R11, R12, R13):
   - **GÓRA / LEWO** — M343 (+90°),
   - **DÓŁ / PRAWO** — M344 (−90°; ten sam program serwo z **+25000** imp zamiast −25000).
3. **Jog napędów transportu** — M340 (przytrzymany, jak w serwisie).
4. **Przedmuch ręczny** — M341 (opcjonalnie).
5. Nastawy **R11, R12, R13** (edycja na BS6 lub BS2 serwis).
6. Lampki: X0, M330, M431, M536.
7. **Wstecz** — tylko gdy X4=OFF (klucz wyłączony).

### Nastawy

| Rejestr | Domyślnie | Zakres | Ekran |
|---------|-----------|--------|-------|
| R1403 | 9000 | 500–20000 | BS3 — produkcja |
| R14 | 4000 | 500–15000 | BS3 — serwis |
| R11 | 500 | 50–2000 | BS3 — przezbrajanie (używane na BS6) |
| R12 | 60000 | 10000–60000 | BS6 |
| R13 | 600 | 100–3600 | BS6 [× 0.1 s] |

Przy M330 program **klamruje** R11 (min 50, max 2000).

### Sieci PLC

```
|--[X4]--( M330 )--|          // przezbrajanie = kluczyk
ORG   X4
OUT   M330
```

**Obrót przezbrajania +90° (M343):**

```
|--[M330]--[M470]--[M343↑]--[/M431]--|
|          +-- MOV R1403→R1412, R11→R1403, R1211→R1413, R12→R1211, M305 |
|          +-- SET S13, SET M536 |
```

**Obrót −90° (M344):** jak M343, ale przed SET S13: **MOV +25000 → R1406**
(bufor kąta w tabeli ROTATE; po ruchu przywróć −25000).

**Po M432↑ · M536:** przywróć R1403, R1211 z R1412/R1413, RST M536, przywróć R1406.

**Timeout:** T53/R13 gdy M536; T52/R10 w serwisie (M342, R14).

**Blokady:**

- M320 (BS3) i M330 (BS6) **wykluczają się** — M329 wymaga `/X4`,
- M330 → START zablokowany (`/M320` w N0002; M320 OFF w przezbrajaniu),
- X4=OFF + otwarta osłona → X0=OFF,
- X4↓ → HMI wraca z BS6 na BS1, RST M536.

### Procedury

**Serwis (BS3):** klucz PRODUKCJA, osłona zamknięta → wejście na ekran SERWIS →
jog M340, przedmuch M341, obrót M342 (R14), HOME.

**Przezbrajanie (BS6):** STOP → klucz PRZEBRAJANIE (X4) → panel **BS6** →
obrót M343/M344, jog M340 → klucz PRODUKCJA, zamknij osłonę, HOME.

> R11=500 ≈ 8× wolniej niż R14=4000. Cel: 90° w 15–30 s.

## R2 — Nastawy prędkości i przyspieszenia z HMI

Tabele serwo leżą w retentywnych rejestrach R — można je edytować bezpośrednio
z panelu. Podział na dwie grupy:

### Grupa A — działa od następnego ruchu (bez MPARA)

FUN140 czyta tabelę programu przy każdym wywołaniu:

| Rejestr | Nastawa | Obecnie | Zakres zalecany (min/max w HMI) |
|---------|---------|---------|--------------------------------|
| R1403 (32-bit) | Prędkość obrotu | 9000 | 500–20000 |
| R1303 (32-bit) | Prędkość najazdu na bazę (DRVZ) | 5000 | 500–10000 |
| R1312 (32-bit) | Prędkość dojazdu do pozycji 0 | 5000 | 500–10000 |

### Grupa B — wymaga przeładowania parametrów (MPARA, M305)

Parametry osi z Table1 (R1200–R1223):

| Rejestr | Nastawa | Obecnie | Zakres zalecany |
|---------|---------|---------|-----------------|
| R1211 | Czas przyspieszania/hamowania | 20000 | 1000–60000 |
| R1209 | Prędkość pełzania przy bazowaniu (creep) | 2000 | 100–5000 |
| R1221 | Offset bazy (Machine Zero Point) | 1000 | wg maszyny |

Na ekranie nastaw obok pól grupy B umieścić przycisk **„ZAPISZ PARAMETRY"
(M305)** i lampkę M460/M431 („oś w ruchu — zapis niemożliwy" — N0015 blokuje
MPARA podczas ruchu). Po zmianie offsetu bazy wykonać HOME.

> Kąt obrotu (R1406 = 25000) celowo **nie** jest udostępniany — to stała
> konstrukcyjna (90° przy przekładni 10:1). Zmiana tylko z WinProLadder.

### Walidacja w PLC (opcjonalna, zalecana)

Zakresy pilnowane w HMI (min/max), ale dla odporności na błędny zapis
po protokole warto dodać sieć klamrującą przed startem ruchu, np.:

```
|--[R1403 < 500]---[MOV 500 → R1403]--|
|--[R1403 > 20000]-[MOV 20000 → R1403]--|
```

(analogicznie dla pozostałych — 32-bit: porównania D171/D172 i D08.MOV).

## R3 — Liczniki statystyczne i czas cyklu

Nowe sieci:

```
|--[M432↑]--[FUN15 (+1) D100]--|            // partie (total)
|--[S11]--[M410]--[X1↓]--[M420]--[FUN15D (+1) D102]--|   // sztuki (total, 32-bit)
|--[S11 + S12 + S13]--[T55 .1 30000]--|      // pomiar czasu cyklu
|--[M432↑]--[MOV T55 → R201]--|              // zapis czasu cyklu [x 0.1 s]
|--[M312↑]--[MOV 0 → D100]--[DMOV 0 → D102]--[MOV 0 → R201]--|  // zerowanie
```

```
ORG   TU   M432
FUN   15 _.(+1)
           :  D100
ORG        S11
AND        M410
AND   TD   X1
AND        M420
FUN   15D_.(+1)
           :  D102
ORG        S11
OR         S12
OR         S13
T55   .1   30000
ORG   TU   M432
FUN   08 _.MOV
      S :  T55
      D :  R201
ORG   TU   M312
FUN   08 _.MOV
      S :  0
      D :  D100
FUN   08D_.MOV
      S :  0
      D :  D102
FUN   08 _.MOV
      S :  0
      D :  R201
```

D100/D102 są retentywne — statystyki przeżywają wyłączenie zasilania;
zerowanie tylko przyciskiem M312 (ekran serwisowy).

---

# Zmiany HMI (FvDesigner)

**Pełna instrukcja wdrożenia:** [hmi_wdrozenie.md](../hmi_wdrozenie.md) — typy obiektów,
adresy `@HB1:…`, właściwości przycisków, testy H1–H12.

Poniżej skrót zakresu zmian.

## BS1 (RUN) — uzupełnienia

- lampka **„PAUZA — zator B3"** (M403),
- lampka **„SERWIS"** (M320),
- licznik partii D100 i czas cyklu R201 (× 0.1 s) — małe pola statusowe,
- przycisk HOME odblokowany (M310 już obsłużone w PLC).

## BS2 (SETUP) — parametry procesu i osi

| Pole | Adres | Min/Max |
|------|-------|---------|
| Opóźnienie po zliczeniu [×0.01 s] | R7 | 0–200 (0–2 s) |
| Czas przejazdu słoika przy B3 [×0.01 s] | R8 | 0–500 (0–5 s) |
| Timeout bazowania / obrotu | R9, R10 | — |
| Acc/dec, creep, offset | R1211, R1209, R1221 | M305 |

## BS3 (SERWIS) — **wszystkie prędkości obrotu**

| Pole | Adres | Zakres |
|------|-------|--------|
| Prędkość produkcyjna | R1403 | 500–20000 Hz |
| Prędkość serwisowa | R14 | 500–15000 Hz |
| Prędkość przezbrajania | R11 | 50–2000 Hz |
| Przysp. / timeout przezbraj. | R12, R13 | — |
| Prędkości bazowania | R1303, R1312 | 500–10000 Hz |

Wejście → M320; M340/M341/M342 (R14); HOME; zerowania. Niedostępny gdy X4=ON.

## BS6 (PRZEBRAJANIE)

Auto przy X4; instrukcja; M343/M344 (używa R11 z BS3); jog M340; odczyt R11 (bez edycji).

## BS4 (ALARMY) — nowy ekran

| Lampka/komunikat | Bit |
|------------------|-----|
| Bezpieczeństwo / E-stop / osłona | M535 (lub /X0 na żywo) |
| Timeout bazowania | M530 |
| Timeout obrotu | M531 |
| Błąd serwo — bazowanie | M532 |
| Błąd serwo — obrót | M533 |
| Błąd parametrów serwo | M534 |
| Nieprawidłowa nastawa partii (R6) | /M539 |

- przycisk **RESET** (M302),
- informacja „po błędzie ruchu wymagane bazowanie" gdy /M470.

Alternatywnie: obiekt Alarm w FvDesigner z rejestracją historii na bitach M530–M535.

---

# Kolejność wdrożenia

1. **Kopia zapasowa:** `File → Save As` → `SKO-Program_przed_rozbudowa.pdw`;
   w FvDesigner kopia `.fpj`.
2. PLC — poprawki P1–P5 (nowe sieci za N0030 + modyfikacje N0001, N0002,
   N0006, N0014, N0020, N0029). **F8** (składnia) po każdej grupie.
3. PLC — rozbudowa R1–R4 (modyfikacje N0009, N0022, N0029 + nowe sieci).
4. HMI — BS2/BS3/**BS6**/BS4 i uzupełnienia BS1.
5. Nastawy początkowe: R9=300, R10=100, **R11=500, R12=60000, R13=600, R14=4000**
   (R1403/R1303/R1312/R1209/R1211 już mają wartości z tabel — nie nadpisywać zerami!).
6. Wgranie do PLC (**F9**) i panelu, testy wg listy poniżej.
7. Wydruk PDF → `plc/SKO-Program.pdf`, eksporty → `plc/export/`,
   aktualizacja dokumentacji ([README](../README.md) — zasada aktualizacji).

## Testy odbiorcze

| # | Test | Oczekiwany wynik |
|---|------|------------------|
| 1 | START przy R6=0 | Brak startu, komunikat nastaw (/M539) |
| 2 | HOME z zablokowanym mechanicznie modułem | Po R9×0.1 s alarm M530, S3; START wymaga HOME |
| 3 | Obrót z zablokowanym modułem | Po R10×0.1 s alarm M531, S3, M470 skasowane |
| 4 | E-stop w trakcie liczenia → RESET → START | C0 zachowane, partia dokończona bez nadmiaru |
| 5 | STOP w trakcie partii → „Zeruj licznik" → START | Partia od zera |
| 6 | Serwis BS3: wejście na ekran, X4=OFF | M320/M329 ON, jog, M342 (R14) |
| 7 | Przezbrajanie: X4=ON → BS6 | M330 ON, M343/M344 (R11), jog M340 |
| 7b | X4=ON, R11=500 vs BS3 R14=4000 | Obrót wyraźnie wolniejszy na BS6 |
| 7c | X4=ON + otwarta osłona | X0=ON, ruch możliwy |
| 7d | X4=OFF + otwarta osłona | X0=OFF, brak ruchu |
| 7e | X4↓ w trakcie BS6 | Powrót BS1, parametry produkcyjne przywrócone |
| 8 | Zmiana prędkości obrotu na HMI | Następny obrót z nową prędkością bez MPARA |
| 9 | Zmiana acc/dec + ZAPISZ (M305) podczas obrotu | Zapis odrzucony (N0015), po zatrzymaniu — przyjęty |
| 10 | Liczniki D100/D102 po 3 partiach | D100=3, D102=3×R6; M312 zeruje |

---

**© CNC Solutions — Michał Batorowicz**
