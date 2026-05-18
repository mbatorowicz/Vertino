# 02 — Szkic programu (33 sieci, poprzedni)

> **Zastąpiony przez:** [03_program_vertino_sieci.md](03_program_vertino_sieci.md) (35 sieci, wersja docelowa Vertino).

**Sterownik:** FATEK HB1-14MBJ25 (bez zmian) | **Sieci:** **33** (zamiast 78)

## Filozofia

| Cel | Jak |
|-----|-----|
| **Bezpieczeństwo** | Pilz na X0; brak obejść; M10 tylko po HOME i bez błędów |
| **Niezawodność** | Jedna maszyna stanów (M21–M25); B4 w jednym miejscu (M507); jedna walidacja |
| **Szybkość** | Mniej sieci = krótszy scan; FUN140 bez zbędnych retriggerów |
| **Kompatybilność HMI** | Te same M1000–M1024, R1400–R1411, C1, D100–D204 |

**Źródło wymagań:** [01_odszyfrowanie_starego_programu.md](01_odszyfrowanie_starego_programu.md)

---

## Mapowanie stary → nowy

| Stary zakres | Nowa sieć |
|--------------|----------|
| N0000–N0005 | N0000–N0005 |
| N0033–N0040 | **N0006** (jedna walidacja) |
| N0013–N0014 | **N0007** |
| N0041–N0042, N0045–N0046 | **N0008**, **N0031** |
| N0006–N0007 | **N0009** |
| N0008–N0012, N0076 | **N0010–N0011** |
| N0015–N0018 | **N0012–N0014** |
| N0019–N0032 | **N0015–N0020**, **N0024–N0025** |
| N0047–N0051 | **N0021**, **N0026** |
| N0068–N0069 | **N0022–N0023** |
| N0052–N0075 | **N0027–N0029** |
| N0077 | **N0032** |

---

## Wszystkie sieci nowego programu

Każda sieć — gotowy szkic do wpisania w WinProLadder (`Main_unit1`).

### N0000 — Bezpieczeństwo ON

```ladder
|--[X0]--( SET M1 )--|
```

### N0001 — Bezpieczeństwo OFF

```ladder
|--[/X0]--( RST M1 )--|
```

### N0002 — Reset błędów HMI

```ladder
|--[M1000]--( SET M200 )--|
```

### N0003 — System gotowy SET

```ladder
|--[M1]--[M82]--[/M503]--[/M504]--[/M505]--[/M506]--( SET M10 )--|
```

### N0004 — System gotowy RESET

```ladder
|--[/M1]--+--( RST M10 )--|
| [/M82] |
| [M503..M506] |
```

### N0005 — Kasowanie błędów

```ladder
|--[M200]--[M1]--( RST M501 M502 M503 M504 M505 M506 M507 M200 )--|
```

### N0006 — Walidacja parametrów (jedna sieć)

```ladder
|--[M1924]--+--[R1400<1]--+--( SET M503 )--|
|           | [R1400>10] |
|           | [R1401 poza 50-500] |
|           | [R1402 poza 100-1000] |
|           | [R1403 poza 12400-12600] |
```

### N0007 — FUN141 — ładowanie osi

```ladder
|--[M1924]--[FUN141.MPARA Ps:0 SR:R1120]--|
|--[M1924]--[FUN141.MPARA Ps:1 SR:R1220]--|
```

### N0008 — Status B4 → M507, R1507

```ladder
|--[X4]--( MOV 1 R1507 )--|
|--[/X4]--( MOV 0 R1507 )--|
|--[X4]--+--( SET M507 )--|
| [M1050]|
|--[/X4]--[/M1050]--( RST M507 )--|
```

### N0009 — START / STOP AUTO

```ladder
|--[M1001]--[M10]--( SET M70 )--|
|--[/M10]--+--( RST M70 )--|
| [M1002] |
```

### N0010 — Żądanie HOME

```ladder
|--[M1]--[/M82]--( SET M80 )--|
|--[M1003]--[M100]--( SET M80 )--|
```

### N0011 — Procedura HOME

```ladder
|--[M80]--[M10]--[/M25]--( SET M25 )--[T10]--|
|--[X3]--[M25]--[M80]--( RST M25 SET M82 RST T10 MOV 0 R1501 )--|
|--[T10]--( SET M504 RST M25 RST M80 )--|
|--[M80]--[FUN140.HSPSO Ps:1 SR:R1300]--|
```

### N0012 — FUN140 — transport (tylko wolna linia)

```ladder
|--[M21]--[/M507]--[FUN140.HSPSO Ps:0 SR:R1100 WR:R1144]--|
|   FO0→M1992  FO1→M501  FO2→RST M21 |
```

### N0013 — FUN140 — obrót 90°

```ladder
|--[M25]--[FUN140.HSPSO Ps:1 SR:R1200 WR:R1244]--|
|   FO0→M1993  FO1→M502  FO2→RST M25 |
```

### N0014 — Y4 — gotowość serwo

```ladder
|--[M1992]--( SET Y4 )--|
|--[M1993]--( SET Y4 )--|
```

### N0015 — Sekwencer AUTO — krok 0→1 (start partii)

```ladder
|--[M70]--[M10]--[/M21]--[/M22]--[/M23]--[/M24]--[/M25]--[/M507]--[/M1050]--( SET M21 )--|
```

### N0016 — Sekwencer — push → zliczanie

```ladder
|--[M21]--[/M22]--( SET M22 RST C1 )--[T5]--|
```

### N0017 — Sekwencer — zliczanie B1 (pauza B4)

```ladder
|--[X1]--[M22]--[/M507]--[+(C1)]--|
|--[C1>=R1400]--[M22]--[/M507]--( SET M233 )--|
```

### N0018 — Sekwencer — stabilizacja i strefy

```ladder
|--[M233]--( RST M22 SET M23 )--[T6=R1410]--|
|--[X1]--[M23]--[T6]--( SET M501 )--[INC D200]--|
|--[X2]--[M23]--[T6]--( SET M502 )--[INC D201]--|
|--[T6]--[/M501]--[/M502]--( RST M23 SET M24 RST M21 RST M233 )--|
```

### N0019 — Sekwencer — start obrotu

```ladder
|--[M24]--[/M25]--( SET M25 )--[T7]--|
```

### N0020 — Sekwencer — koniec obrotu

```ladder
|--[M1993]--[M25]--[/M1992]--( RST M25 RST M24 INC D100 )--[T8=R1411]--|
|--[T8]--[M1993]--[FUN +(90) R1501]--[R1501>=360→MOV 0 R1501]--|
|   // po T8: N0015 może znów ustawić M21 (następna partia)
```

### N0021 — Pozycja R1501 — HOME

```ladder
|--[M82]--[/M25]--( MOV 0 R1501 )--|
```

### N0022 — Przedmuch AUTO (180°)

```ladder
|--[M70]--[R1501=180]--( SET Y5 )--|
|--[/M70]--+--( RST Y5 )--|
| [/R1501=180] |
```

### N0023 — Przedmuch ręczny

```ladder
|--[M240]--( SET Y5 )--|
|--[/M240]--( RST Y5 )--|
```

### N0024 — Timeout transportu (bez zatoru)

```ladder
|--[T5]--[/M507]--( SET M505 RST M22 INC D202 )--|
```

### N0025 — Timeout obrotu

```ladder
|--[T7]--( SET M506 RST M25 INC D203 )--|
```

### N0026 — Pomiar czasu cyklu

```ladder
|--[M21]--[T50]--|
|--[T8]--( MOV T50 R1500 RST T50 )--|
```

### N0027 — Tryb ręczny — warunki

```ladder
|--[M10]--[/M70]--( SET M100 )--|
|--[/M10]--+--( RST M100 )--|
| [M70] |
```

### N0028 — Ręczny — transport FWD/REV

```ladder
|--[M1010]--[M100]--( SET M110 )--|
|--[M1011]--( RST M110 )--|
|--[M110]--[FUN140 SR:R524]--|
|--[M1012]--[M100]--( SET M111 )--|
|--[M1013]--( RST M111 )--|
|--[M111]--[FUN140 SR:R532]--|
```

### N0029 — Ręczny — obrót CW/CCW/±90°

```ladder
|--[M1014]--[M100]--( SET M112 )--|
|--[M1015]--( RST M112 )--|
|--[M112]--[FUN140.HSPSO Ps:1 SR:R540 WR:R1244]--|
|--[M1016]--[M100]--( SET M113 )--|
|--[M1017]--( RST M113 )--|
|--[M113]--[FUN140.HSPSO Ps:1 SR:R548 WR:R1244]--|
|--[M1021]--[M100]--[/M114]--( SET M114 )--|
|--[M114]--[FUN140.HSPSO Ps:1 SR:R556 WR:R1244]--[FO2→RST M114]--|
|--[M1022]--[M100]--[/M115]--( SET M115 )--|
|--[M115]--[FUN140.HSPSO Ps:1 SR:R516 WR:R1244]--[FO2→RST M115]--|
```

### N0030 — Test symulacji B4

```ladder
|--[M1019]--[M100]--( SET M1050 )--|
|--[M1020]--( RST M1050 )--|
```

### N0031 — Zbocze B4 — licznik D204

```ladder
|--[X4]--[/M520]--( SET M520 INC D204 )--|
|--[/X4]--( RST M520 )--|
```

### N0032 — Koniec programu

```ladder
|--[END]--|
```

---

## Kolejność sieci w projekcie (ważne)

WinProLadder wykonuje sieci **od góry do dołu** co skan. Zalecana kolejność:

```
N0000–N0011  → bezpieczeństwo, gotowość, HOME
N0012        → FUN140 transport (przed ustawieniem M21)
N0013        → FUN140 obrót
N0014        → Y4
N0015–N0020  → sekwencer AUTO
N0021–N0026  → pozycja, przedmuch, timeouty, czas cyklu
N0027–N0031  → ręczny, test B4
N0032        → koniec
```

Dzięki temu w jednym skanie: FUN140 kończy poprzedni M21 → N0015 ustawia nowy M21 → N0016 wchodzi w M22 (jak w starym programie, gdzie N0015<N0020<N0021).

## Kolejność wdrożenia w WinProLadder

1. Nowy projekt lub kopia `SKO-Program.pdw` → zmień nazwę na `SKO-Program-v2.pdw`.
2. Usuń zbędne sieci / zbuduj od N0000 według tego dokumentu (33 sieci).
3. Skopiuj tabele FUN140 z `export/Table.tab` (R1100, R1200, R1300).
4. Import komentarzy: `export/comments.txt`.
5. F8 → download → test: HOME → AUTO → B4 w M22 → przedmuch tylko 180°.

## Test akceptacyjny

| # | Test | Oczekiwane |
|---|------|------------|
| T1 | X0 OFF | Wszystkie napędy zatrzymane, M1=0 |
| T2 | START bez HOME | Brak M70 |
| T3 | AUTO 3 słoiki, B4 w 2. słoiku | C1=1 po zwolnieniu, dokończenie do 3 |
| T4 | B4 ON podczas obrotu | Obrót kończy się |
| T5 | R1501=180 | Y5 ON tylko w tej pozycji |
| T6 | R1400=0 (błąd) | M503, brak START |

**© CNC Solutions**
