# Program Vertino — ustrukturyzowane sieci drabinkowe

**Maszyna:** Vertino — Stacja oczyszczania opakowań  
**Sterownik:** FATEK HB1-14MBJ25 | **Jednostka:** `Main_unit1`  
**Sieci:** **35** (N0000–N0034) — bez duplikatów logiki  
**Mapowanie I/O:** bez zmian ([mapowanie.md](mapowanie.md))

**Status:** dokument **planu** — po wdrożeniu zastąpi 78 sieci w `SKO-Program.pdw`. Dopóki nie wgrany: prawda o maszynie = [STAN_FAKTYCZNY.md](STAN_FAKTYCZNY.md).

Jedna definicja B4 → **M507**, jedna maszyna stanów **M21–M25**, jedna walidacja parametrów.

---

## Zasady (z wymagań)

| Temat | Zasada w programie |
|-------|-------------------|
| **Debouncing** | Nie stosować — filtracja wejść w PLC wystarcza |
| **B1 — zliczanie** | Tylko **zbocze narastające** X1 w fazie **M22** → `(+1) C1` (jeden słoik = jeden impuls) |
| **B1 — strefa wejścia** | W **M23** timer **T6** liczy **tylko gdy X1=ON** (B1 zasłonięty). Partia idzie dalej dopiero po **R1410** ms ciągłego B1. Krótkie „obok” nie nabija T6 → **proces się nie zatrzymuje** na błysk |
| **B4 — zator** | X4 (lub symulacja M1050) musi być **ciągle ON** przez **R1412** [ms] → dopiero wtedy **M507** (pauza przepychania) |
| **B4 — obrót** | **M507 nie blokuje** obrotu (M25, FUN140 oś obrotu) |
| **C1 przy zatorze** | **Bez RST** w pauzie; **bez zliczania**; **bez końca partii**; wznowienie po `/M507` |

### Nowy parametr HMI

| Rejestr | Zakres | Domyślnie | Opis |
|---------|--------|-----------|------|
| **R1412** | 100–3000 ms | **500** | Czas ciągłego sygnału B4 (X4) przed uznaniem zatoru → M507 |

*(Dodać do walidacji w N0006: R1412 w zakresie, inaczej M503.)*

---

## Kolejność sieci (kolejność skanu)

```
N0000–N0005   Bezpieczeństwo, gotowość, reset błędów
N0006–N0007   Walidacja, FUN141
N0008         B4 → M507 (jedyne miejsce!)
N0009         START / STOP AUTO
N0010–N0011   HOME
N0012–N0014   FUN140 transport / obrót, Y4
N0015–N0023   Sekwencer AUTO (M21→M25)
N0024–N0028   Przedmuch, timeouty, czas cyklu
N0029–N0032   Tryb ręczny, test B4
N0033         Zbocze B4 → D204
N0034         Koniec programu
```

---

## Flagi pomocnicze (bez duplikatów)

| Flaga | Ustawiana | Znaczenie |
|-------|-----------|-----------|
| **M507** | N0008 | Linia odbiorcza zajęta (zator potwierdzony) |
| **M520** | N0031 | Zbocze B4 (do D204) |
| **M521** | N0016 | Puls wejścia w M22 (PLS) — jednorazowy RST C1 |
| **M1992** | N0012 | Serwo transportu aktywne |
| **M1993** | N0013 | Serwo obrotu — koniec 90° |

---

## Sieci — specyfikacja

### N0000 — Bezpieczeństwo ON

```ladder
|--[ X0 ]--( SET M1 )--|
```

### N0001 — Bezpieczeństwo OFF

```ladder
|--[/X0 ]--( RST M1 )--|
```

### N0002 — Reset błędów z HMI

```ladder
|--[ M1000 ]--( SET M200 )--|
```

### N0003 — System gotowy SET

```ladder
|--[ M1 ]--[ M82 ]--[/M503]--[/M504]--[/M505]--[/M506]--( SET M10 )--|
```

### N0004 — System gotowy RESET

```ladder
|--[/M1 ]--+--( RST M10 )--|
| [/M82]  |
| [ M503 ]|
| [ M504 ]|
| [ M505 ]|
| [ M506 ]|
```

### N0005 — Kasowanie błędów procesu

```ladder
|--[ M200 ]--[ M1 ]--( RST M501 M502 M503 M504 M505 M506 M507 M200 )--|
```

### N0006 — Walidacja parametrów (jedna sieć)

```ladder
|--[ M1924 ]--+--[ R1400 < K1  ]--+--( SET M503 )--|
|            |--[ R1400 > K10 ]--|
|            |--[ R1401 < K50  ]--|
|            |--[ R1401 > K500 ]--|
|            |--[ R1402 < K100 ]--|
|            |--[ R1402 > K1000]--|
|            |--[ R1403 < K12400]--|
|            |--[ R1403 > K12600]--|
|            |--[ R1410 < K50  ]--|
|            |--[ R1410 > K1000]--|
|            |--[ R1411 < K50  ]--|
|            |--[ R1411 > K500 ]--|
|            |--[ R1412 < K100 ]--|
|            |--[ R1412 > K3000]--|
```

### N0007 — FUN141 — parametry osi (First Scan)

```ladder
|--[ M1924 ]--[ FUN141.MPARA  Ps:0  SR:R1120 ]--|  FO0 → M503
|--[ M1924 ]--[ FUN141.MPARA  Ps:1  SR:R1220 ]--|  FO0 → M503
```

---

### N0008 — B4: potwierdzenie zatoru → M507 (JEDYNA SIEC B4)

**X4** lub **M1050** (test) musi być aktywny przez **R1412** ms (timer **T52**, baza 0,01 s).

```ladder
Rung A — sygnał surowy na wyjście diagnostyczne (bez opóźnienia)

|--[ X4 ]--( MOV  K1  R1507 )--|
|--[/X4 ]--( MOV  K0  R1507 )--|

Rung B — timer potwierdzenia zatoru

|--[ X4 ]--+--[ TON  T52  PV=R1412 ]--|        ← 0,01 s × R1412
| [M1050]--+

Rung C — flaga pauzy (tylko tutaj SET/RST M507)

|--[ T52 ]--( SET  M507 )--|                  ← zator POTWIERDZONY
|--[/T52 ]--[/X4 ]--[/M1050]--( RST  M507 )--| ← linia wolna
```

**Uwaga:** Nie używaj `X4` bezpośrednio w sekwencerze — wyłącznie **`/M507`**.

---

### N0009 — START / STOP pracy automatycznej

```ladder
|--[ M1001 ]--[ M10 ]--( SET M70 )--|
|--[ M1002 ]--( RST M70 )--|
|--[/M10 ]--( RST M70 )--|
```

---

### N0010 — Żądanie HOME

```ladder
|--[ M1 ]--[/M82]--( SET M80 )--|
|--[ M1003 ]--[ M100 ]--( SET M80 )--|
```

### N0011 — Procedura HOME

```ladder
|--[ M80 ]--[/M25]--( SET M25 )--[ TON T10 K8000 ]--|

|--[ X3 ]--[ M25 ]--[ M80 ]--|
|         ( RST M25  SET M82  RST M80  RST T10  MOV K0 R1501 )--|

|--[ T10 ]--( SET M504  RST M25  RST M80 )--|

|--[ M80 ]--[ FUN140.HSPSO  Ps:1  SR:R1300  WR:... ]--|
|              FO0→M1993  FO1→M502  FO2→RST M25 (wg konfiguracji HOME) |
```

*(Tabela R1300 — jak w obecnym `Table.tab` / procedura HOME.)*

---

### N0012 — FUN140 — transport (AUTO)

```ladder
|--[ M21 ]--[/M507]--[ FUN140.HSPSO  Ps:0  SR:R1100  WR:R1144 ]--|
|                         FO 0 → SET M1992
|                         FO 1 → SET M501
|                         FO 2 → RST M21
```

### N0013 — FUN140 — obrót 90° (bez M507)

```ladder
|--[ M25 ]--[ FUN140.HSPSO  Ps:1  SR:R1200  WR:R1244 ]--|
|                         FO 0 → SET M1993
|                         FO 1 → SET M502
|                         FO 2 → RST M25
```

### N0014 — Y4 — sygnalizacja gotowości serwo

```ladder
|--[ M1992 ]--( SET Y4 )--|
|--[ M1993 ]--( SET Y4 )--|
|--[/M1992 ]--[/M1993 ]--( RST Y4 )--|
```

---

## Sekwencer AUTO (M21–M25)

### N0015 — Start partii (M21)

```ladder
|--[ M70 ]--[ M10 ]--[/M21]--[/M22]--[/M23]--[/M24]--[/M25]--|
|    [/M507]--( SET M21 )--|
```

### N0016 — Wejście w transport / zliczanie (M22)

```ladder
Rung 1 — start fazy zliczania

|--[ M21 ]--[/M22]--[/M507]--( SET M22 )--|

Rung 2 — reset C1 tylko przy wejściu w M22 (PLS → M521)

|--[ M22 ]--[ PLS ]--( SET M521 )--|
|--[ M521 ]--( RST C1  RST M521 )--|

Rung 3 — timeout transportu (w N0026 nie tyka przy M507)

|--[ M22 ]--[/M507]--[ TON  T5  K30000 ]--|
```

*Alternatywa bez M521: `RST C1` w rungu 1 z kontaktem **różniczkującym** wejścia M22 (one-shot).*

### N0017 — Zliczanie B1 (zbocze narastające)

**Nie** licz przy **M507**. Wejście licznika C1: **X1**, warunek: **M22 · /M507**, typ: **rising edge** (bez dodatkowego timera).

```ladder
|--[ X1 ]--[ M22 ]--[/M507]--[ +( C1 ) ]--|
```

*W WinProLadder: blok **CT** / licznik **C1** — zliczanie na zboczu narastającym X1.*

### N0018 — Koniec partii (ilość OK)

```ladder
|--[ C1 >= R1400 ]--[ M22 ]--[/M507]--( SET M233 )--|
```

### N0019 — Stabilizacja (M23)

```ladder
|--[ M233 ]--( RST M22  SET M23 )--|
```

### N0020 — B1 / B2: potwierdzenie obecności czasem R1410 (nie debounce)

**T6** nabija się **wyłącznie**, gdy czujnik jest zasłonięty — to jest „czas przy B1”, nie filtr drgań.

```ladder
Rung 1 — B1 musi być zasłonięty przez R1410 ms zanim uznamy strefę wejścia

|--[ M23 ]--[/M507]--[ X1 ]--[ TON  T6  PV=R1410 ]--|

Rung 2 — B2: ten sam schemat (jeśli wymagane w procesie)

|--[ M23 ]--[/M507]--[ X2 ]--[ TON  T53  PV=R1410 ]--|

Rung 3 — przejście po potwierdzeniu B1 (i B2 jeśli używane)

|--[ T6 ]--[ M23 ]--[/M501]--|
|    ( RST M23  SET M24  RST M21  RST M233 )--|

Rung 4 — strażnik: zbyt długo w M23 bez potwierdzenia (opcjonalnie, np. 30 s)

|--[ M23 ]--[ TON  T55  K3000 ]--( SET M501  INC D200 )--|
```

*Słoik „obok” B1: krótki X1 **nie** domyka T6 → **M23 czeka**, bez M501, dopóki nie minie T55 (serwis może skrócić przez STOP).*

### N0021 — Start obrotu (M25)

```ladder
|--[ M24 ]--[/M25]--( SET M25 )--[ TON  T7  K8000 ]--|
```

### N0022 — Koniec obrotu, pozycja, następna partia

```ladder
|--[ M1993 ]--[ M25 ]--[/M1992 ]--|
|    ( RST M25  RST M24  RST T7  INC D100 )--|
|--[ TON  T8  PV=R1411 ]--|

|--[ T8 ]--[ M1993 ]--[ ADD  R1501 +90 ]--|
|--[ R1501 >= K360 ]--( MOV K0 R1501 )--|    ← pełny obrót 360°
```

*(Po T8 sekwencer może wrócić do N0015 — kolejna partia.)*

---

### N0023 — Przedmuch AUTO (tylko 180°)

```ladder
|--[ M70 ]--[ R1501 = K180 ]--( SET Y5 )--|
|--[/M70 ]--+--( RST Y5 )--|
| [ R1501 <> K180 ] |
```

### N0024 — Przedmuch ręczny

```ladder
|--[ M1023 ]--[ M100 ]--( SET M240 )--|
|--[ M1024 ]--( RST M240 )--|
|--[ M240 ]--( SET Y5 )--|
|--[/M240 ]--( RST Y5 )--|
```

### N0025 — Pauza: zatrzymaj serwo transportu w M22 + M507

```ladder
|--[ M507 ]--[ M22 ]--[ M1992 ]--( RST M1992 )--|
```

*(Sposób stopu FUN140 — zweryfikować na maszynie; ewentualnie blokada retrigger N0012.)*

### N0026 — Timeout transportu (tylko bez zatoru)

```ladder
|--[ T5 ]--[/M507]--( SET M505  RST M22  INC D202 )--|
```

### N0027 — Timeout obrotu

```ladder
|--[ T7 ]--( SET M506  RST M25  INC D203 )--|
```

### N0028 — Pomiar czasu cyklu → R1500

```ladder
|--[ M21 ]--( SET T50 )--|          ← start pomiaru (wg konwencji Fatek T50)
|--[ T8 ]--( MOV T50 → R1500  RST T50 )--|
```

---

## Tryb ręczny i testy

### N0029 — Warunki trybu ręcznego

```ladder
|--[ M10 ]--[/M70]--( SET M100 )--|
|--[/M10 ]--+--( RST M100 )--|
| [ M70 ]  |
```

### N0030 — Transport ręczny FWD / REV

```ladder
|--[ M1010 ]--[ M100 ]--( SET M110 )--|
|--[ M1011 ]--( RST M110 )--|
|--[ M110 ]--[ FUN140  SR:R524 ]--|

|--[ M1012 ]--[ M100 ]--( SET M111 )--|
|--[ M1013 ]--( RST M111 )--|
|--[ M111 ]--[ FUN140  SR:R532 ]--|
```

### N0031 — Obrót ręczny CW / CCW / ±90°

```ladder
|--[ M1014 ]--[ M100 ]--( SET M112 )--|
|--[ M1015 ]--( RST M112 )--|
|--[ M112 ]--[ FUN140.HSPSO  Ps:1  SR:R540 ]--|

|--[ M1016 ]--[ M100 ]--( SET M113 )--|
|--[ M1017 ]--( RST M113 )--|
|--[ M113 ]--[ FUN140.HSPSO  Ps:1  SR:R548 ]--|

|--[ M1021 ]--[ M100 ]--[/M114]--( SET M114 )--|
|--[ M114 ]--[ FUN140.HSPSO  Ps:1  SR:R556 ]--|  FO2 → RST M114

|--[ M1022 ]--[ M100 ]--[/M115]--( SET M115 )--|
|--[ M115 ]--[ FUN140.HSPSO  Ps:1  SR:R516 ]--|  FO2 → RST M115
```

### N0032 — Symulacja B4 (serwis)

```ladder
|--[ M1019 ]--[ M100 ]--( SET M1050 )--|
|--[ M1020 ]--( RST M1050 )--|
```

### N0033 — Zbocze potwierdzonego zatoru → D204

```ladder
|--[ T52 ]--[/M520]--( SET M520  INC D204 )--|
|--[/T52 ]--( RST M520 )--|
```

### N0034 — Koniec programu

```ladder
|--[ END ]--|
```

---

## Diagram sekwencji AUTO

```
     [/M507]
M70 ───────► M21 ──► FUN140 transport ──► M22 ──► (+C1 na X1↑) ──► M233
              ▲                              │         ▲
              │                              │    M507 pauza: /+C1, /koniec
              │                              ▼
              └──────── M24 ◄── M23 (T6,R1410) ◄──┘
                              │
                              ▼
                            M25 (obrót, BEZ M507)
                              │
                              ▼
                         T8, R1501+=90°, Y5@180°
```

---

## Test akceptacyjny

| # | Scenariusz | Oczekiwane |
|---|------------|------------|
| T1 | X4 krótki błysk (< R1412) | **Brak** M507, proces bez pauzy |
| T2 | X4 długi (≥ R1412) w M22 | M507=1, C1 zamrożone, brak M233 |
| T3 | Po /M507, C1=2, R1400=3 | Zliczenie do 3, normalny koniec |
| T4 | Słoik mija B1 obok w M23 | Przy dobrym R1410 — brak M501 |
| T5 | B4 podczas M25 | Obrót kończy się |
| T6 | R1501=180, AUTO | Y5=ON tylko w 180° |

---

## Wdrożenie w WinProLadder

1. Kopia `SKO-Program.pdw` → `Vertino-Program.pdw`.
2. Usunąć stare sieci; wprowadzić **N0000–N0034** (35 sieci) wg kolejności powyżej.
3. Zachować tabele serwo z `plc/export/Table.tab`.
4. Dodać **R1412** na HMI + wpis w `comments.txt`.
5. Pobrać do sterownika → test T1–T6.

**Powiązane:** [STAN_FAKTYCZNY.md](STAN_FAKTYCZNY.md), [audyt.md](audyt.md), [program.md](program.md).

**© CNC Solutions — Vertino**
