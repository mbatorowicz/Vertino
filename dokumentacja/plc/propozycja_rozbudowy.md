# Propozycja poprawek i rozbudowy programu

**Status:** PROPOZYCJA — do wdrożenia w WinProLadder (PLC) i FvDesigner (HMI).
**Baza:** bieżący program 31 sieci ([program.md](program.md)), mapa adresów ([mapa_io.md](mapa_io.md)).

Zakres:

- **P1–P6** — poprawki ryzyk wykrytych w audycie programu
- **R1** — tryb serwisowy (ruchy ręczne z HMI)
- **R2** — nastawy prędkości i przyspieszenia serwo z HMI
- **R3** — liczniki statystyczne i czas cyklu
- **R4** — tryb przezbrajania (powolny obrót 90° bez osłony)
- **HMI** — nowe ekrany i obiekty

---

## Nowe adresy (zweryfikowane jako wolne)

| Adres | Funkcja | Kierunek |
|-------|---------|----------|
| M311 | Zeruj licznik partii C0 | HMI → PLC |
| M312 | Zeruj statystyki | HMI → PLC |
| M320 | Tryb serwisowy (przełącznik) | HMI → PLC |
| M340 | Serwis: transport jog | HMI → PLC |
| M341 | Serwis: przedmuch ręczny | HMI → PLC |
| M342 | Serwis: obrót +90° (zbocze, prędkość produkcyjna R1403) | HMI → PLC |
| M323 | Tryb przezbrajania (przełącznik) | HMI → PLC |
| M343 | Przezbrajanie: obrót +90° (zbocze, **utrzymany** — dead-man) | HMI → PLC |
| M330 | Przezbrajanie aktywne (wewnętrzny: M320·M323·S1) | wewnętrzny |
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
| R11 | Prędkość obrotu przezbrajania (32-bit) — **bardzo niska** | HMI → PLC |
| R12 | Przyspieszenie obrotu przezbrajania (acc/dec, kopiowane tymczasowo do R1211) | HMI → PLC |
| R13 | Timeout obrotu przezbrajania [× 0.1 s] (zalecane 600 = 60 s) | HMI → PLC |
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
|--[R6 > 0]--[R6 < 101]--( M539 )--|
```

```
ORGF  171_.>
      Sa:  R6
      Sb:  0
ANDF  172_.<
      Sa:  R6
      Sb:  101
OUT        M539
```

Zmiana **N0002** (START) — dopisać dwa styki:

```
Było:   M300↑ · X0 · /S3 · M470          → SET S2
Będzie: M300↑ · X0 · /S3 · M470 · M539 · /M320 · /M323 → SET S2
```

(`/M320`, `/M323` — start automatu zablokowany w trybie serwisowym i przezbrajania.)
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

## R1 — Tryb serwisowy

**Założenia bezpieczeństwa:**

- wejście w tryb tylko w READY (S1), wyjście — przełącznikiem M320,
- ruchy serwisowe wymagają zazbrojonego bezpieczeństwa (X0),
- tryb serwisowy blokuje START automatu (P4), a START w toku blokuje tryb
  (warunek S1),
- obrót serwisowy wymaga zbazowanej osi (M470).

### Sieci

Tryb aktywny (sygnalizacja + warunek dla ruchów):

```
|--[M320]--[S1]--[X0]--( M329 )--|     // M329 = serwis aktywny (wewnętrzny)
```

```
ORG        M320
AND        S1
AND        X0
OUT        M329
```

Transport jog — **modyfikacja N0022**:

```
Było:   M410 → Y1
Będzie: M410 + (M329 · M340) → Y1
```

```
ORG        M410
LD         M329
AND        M340
ORB
OUT        Y1
```

Przedmuch ręczny — **modyfikacja N0009** (dodatkowa gałąź równoległa):

```
Było:   M400 · /M403 · M421 → Y4
Będzie: (M400 · /M403 · M421) + (M329 · M341) → Y4
```

Obrót +90° (serwis, prędkość produkcyjna) — nowa sieć; **zablokowany gdy M323=ON**:

```
|--[M329]--[/M323]--[M470]--[M342↑]--[/M431]--( SET S13 )--|
```

```
ORG        M329
AND   NOT  M323
AND        M470
AND   TU   M342
AND   NOT  M431
SET( )     S13
```

Bazowanie ręczne — istnieje (M310, N0012). Uwaga: jog transportu w serwisie
celowo pomija blokadę B3 (M403) — odpowiedzialność operatora; przedmuch
i obrót pozostają dostępne niezależnie od B3.

## R4 — Tryb przezbrajania (powolny obrót 90° bez osłony)

**Cel:** wymiana elementów modułu obrotowego (tuleje, prowadnice) na inny
format słoika — operator pracuje **przy otwartej osłonie**, moduł obraca się
**bardzo powoli** (90° na impuls), żeby można było bezpiecznie ustawić
mechanikę między krokami.

**Różnica względem obrotu serwisowego (M342):**

| | Obrót serwisowy M342 | Przezbrajanie M343 |
|---|---------------------|-------------------|
| Prędkość | R1403 (produkcyjna, np. 9000) | **R11** (np. 300–800) |
| Przyspieszenie | R1211 (produkcyjna) | **R12** (np. 60000 — łagodny start) |
| Timeout | R10 (np. 10 s) | **R13** (np. 60 s) |
| Osłona | zamknięta (B4 w torze Pilz) | **otwarta** — kluczyk serwisowy w pozycji serwisowej |

### Obwód bezpieczeństwa — kluczyk serwisowy (istnieje w schemacie)

W obwodzie **Pilz PNOZ X7** jest **przełącznik serwisowy z kluczykiem** (wg schematu
[SKO.pdf](../../schemat_elektryczny/SKO.pdf), str. 4). Dzięki temu tryb przezbrajania
z otwartą osłoną jest możliwy **bez zmian hardware**:

| Pozycja klucza | B4 (osłona) | E-stop | X0 (PLC) | Ruch napędów |
|----------------|-------------|--------|----------|--------------|
| **Produkcja** | w torze — osłona musi być zamknięta | aktywny | ON gdy wszystko OK | automat / serwis przy zamkniętej osłonie |
| **Serwis** | pominięty w torze Pilz | aktywny | ON przy odryglowanym E-stop | tylko tryb przezbrajania (M323), powolny obrót |

Przy otwartej osłonie **bez** klucza w pozycji serwisowej B4 rozbraja Pilz →
**X0=OFF** → program nie uruchomi obrotu (warunek X0 w N0017/N0028 i M330).

PLC **nie musi** osobno odczytywać pozycji klucza — wystarczy **X0=ON** jako
potwierdzenie, że obwód bezpieczeństwa (w tym wybrany tryb Pilz) jest zazbrojony.
E-stop działa w obu pozycjach klucza.

### Nastawy (panel serwisowy BS3)

| Rejestr | Domyślnie | Zakres HMI | Opis |
|---------|-----------|------------|------|
| R11 | 500 | 50–2000 | Prędkość obrotu przezbrajania [Hz] |
| R12 | 60000 | 10000–60000 | Acc/dec tylko na czas przezbrajania |
| R13 | 600 | 100–3600 | Timeout obrotu [× 0.1 s] |

Przy włączeniu M323 program **klamruje** R11 (min 50, max 2000) — nie da się
przypadkowo ustawić prędkości produkcyjnej.

### Sieci PLC

**Aktywacja trybu:**

```
|--[M320]--[M323]--[S1]--[/S2]--[/S3]--( M330 )--|
```

```
ORG        M320
AND        M323
AND        S1
AND   NOT  S2
AND   NOT  S3
OUT        M330
```

**Przy wejściu w tryb (M330↑)** — jednorazowo łagodne parametry osi:

```
|--[M330↑]--[FUN MOV R1211→R1413]--[FUN MOV R12→R1211]--[M305 impuls]--|
```

(zapis bufora R1413 i MPARA — jak w R2 grupa B; wykonać tylko gdy /M431·/M460)

**Przy wyjściu z trybu (M330↓ / M323 OFF)** — przywrócenie R1211 produkcyjnego
z R1413 + M305.

**Start powolnego obrotu** (M343↑, tylko gdy M330, /M431):

```
|--[M330]--[M343↑]--[/M431]--|
|          +--[FUN MOV R1403→R1412]--|
|          +--[FUN MOV R11→R1403]--|
|          +--( SET S13 )--( SET M536 )--|
```

```
ORG        M330
AND   TU   M343
AND   NOT  M431
FUN   08 _.MOV
      S :  R1403
      D :  R1412
FUN   08 _.MOV
      S :  R11
      D :  R1403
SET( )     S13
SET( )     M536
```

M536 = „obrót przezbrajania w toku" — lampka HMI + wybór timeoutu.

**Po zakończeniu obrotu** — rozszerzenie N0029:

```
Było:   M432↑ → MOV 0→R1511, RST S13
Dopisać: M432↑ · M536 → MOV R1412→R1403, RST M536
```

```
ORG   TU   M432
AND        M536
FUN   08 _.MOV
      S :  R1412
      D :  R1403
RST( )     M536
```

**Timeout przezbrajania** — rozszerzenie P2:

```
|--[S13]--[/M432]--[M536]--[T53 .1 R13]--( SET M531 )--( SET S3 )--|
```

(przy M536=OFF pozostaje istniejący T52/R10)

**Blokady wzajemne:**

- M323=ON → M342 zablokowany (sieć wyżej),
- M323=ON → START automatu zablokowany (`/M323` w N0002 obok `/M320`),
- M323=ON → transport jog (M340) **zablokowany** — tylko obrót modułu,
- S2=ON lub S3=ON → M330=OFF (M323 musi być OFF lub warunek S1 nie spełniony).

### Procedura operatora (przezbrajanie)

1. STOP, **kluczyk serwisowy w pozycji SERWIS**, osłonę można otworzyć, E-stop odryglowany
   (X0=ON — lampka bezpieczeństwa na panelu).
2. Panel → SERWIS → włącz **TRYB SERWISOWY** (M320).
3. Włącz **TRYB PRZEBRAJANIA** (M323) — lampka M330.
4. Ustaw **R11** (prędkość, start od 500) i ewentualnie **R12** (acc/dec).
5. Naciśnij **OBRÓT PRZEBRAJANIA +90°** (M343) — moduł obraca się powoli;
   powtórz 2–4 razy, aż moduł będzie w dogodnej pozycji do wymiany tulei.
6. Wyłącz M323, **kluczyk w pozycję PRODUKCJA**, zamknij osłonę, **HOME**, wyłącz serwis.

> Prędkość startowa R11=500 daje ~50× wolniejszy obrót niż produkcyjne 9000.
> Dostosować na maszynie — cel: pełne 90° w ok. 15–30 s.

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

## BS2 (SETUP) — rozbudowa

| Pole | Adres | Min/Max w obiekcie |
|------|-------|--------------------|
| Ilość w partii | R6 | 1–100 |
| Opóźnienie po partii [×0.01 s] | R7 | 0–30000 |
| Czas przejazdu słoika przy B3 [×0.01 s] | R8 | 1–30000 |
| Timeout bazowania [×0.1 s] | R9 | 50–6000 |
| Timeout obrotu [×0.1 s] | R10 | 20–6000 |
| Prędkość obrotu | R1403 (32-bit) | 500–20000 |
| Prędkość bazowania (DRVZ) | R1303 (32-bit) | 500–10000 |
| Prędkość dojazdu do 0 | R1312 (32-bit) | 500–10000 |
| Przyspieszenie/hamowanie | R1211 | 1000–60000 |
| Creep bazowania | R1209 | 100–5000 |
| Offset bazy | R1221 (32-bit) | wg maszyny |
| ZAPISZ PARAMETRY (przycisk) | M305 | — |

Dostęp do BS2 zabezpieczyć hasłem (poziom użytkownika FvDesigner) —
przynajmniej dla pól grupy B.

## BS3 (SERWIS) — nowy ekran

- przełącznik **TRYB SERWISOWY** (M320) + lampka aktywności (M329),
- przełącznik **TRYB PRZEBRAJANIA** (M323) + lampka M330 + komunikat
  *„Kluczyk SERWIS + otwarta osłona — tylko powolny obrót"* (X0 musi być ON),
- **Prędkość obrotu przezbrajania** (R11, 50–2000, domyślnie 500),
- **Przyspieszenie przezbrajania** (R12, 10000–60000),
- **Timeout przezbrajania** (R13, ×0.1 s, domyślnie 600),
- przycisk **OBRÓT PRZEBRAJANIA +90°** (M343) + lampka ruchu (M536 / M431),
- przycisk **OBRÓT SERWIS +90°** (M342, tylko gdy /M323) + lampka M431,
- przycisk z podtrzymaniem **TRANSPORT JOG** (M340, zablokowany gdy M323),
- przełącznik **PRZEDMUCH** (M341),
- przycisk **HOME** (M310) + lampka M470,
- przycisk **ZERUJ LICZNIK PARTII** (M311), **ZERUJ STATYSTYKI** (M312),
- podgląd wejść X0–X4, wyjść Y1/Y4, pozycji R1501, licznika C0/R100.

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
4. HMI — BS2/BS3/BS4 i uzupełnienia BS1.
5. Nastawy początkowe: R9=300, R10=100, **R11=500, R12=60000, R13=600**
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
| 6 | Serwis: jog/przedmuch/obrót przy S2=ON | Niedostępne (M329=OFF) |
| 7 | Serwis: obrót +90° ×4 (M342, M323=OFF) | Moduł wraca do pozycji wyjściowej |
| 7b | Przezbrajanie: M323, R11=500, obrót ×2 (M343) | Obrót widocznie wolniejszy niż M342; R1403 przywrócone po każdym kroku |
| 7c | Przezbrajanie: M323=ON → próba M342 | Zablokowane |
| 7d | Przezbrajanie: otwarta osłona, klucz w PRODUKCJA | Brak ruchu (X0=OFF, B4 w torze Pilz) |
| 7e | Przezbrajanie: otwarta osłona, klucz w SERWIS, M343 | Powolny obrót 90°, X0=ON |
| 8 | Zmiana prędkości obrotu na HMI | Następny obrót z nową prędkością bez MPARA |
| 9 | Zmiana acc/dec + ZAPISZ (M305) podczas obrotu | Zapis odrzucony (N0015), po zatrzymaniu — przyjęty |
| 10 | Liczniki D100/D102 po 3 partiach | D100=3, D102=3×R6; M312 zeruje |

---

**© CNC Solutions — Michał Batorowicz**
