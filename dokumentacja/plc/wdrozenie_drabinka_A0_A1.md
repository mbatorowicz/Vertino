# Wdrożenie w WinProLadder — A0 (B4) + A1 (przedmuch 180°) — Vertino

**Dotyczy:** programu **produkcyjnego** (78 sieci) w [SKO-Program.pdw](../../plc/SKO-Program.pdw) — **nie** programu docelowego 03.

**Alternatywa:** wdrożyć całość z [03_program_vertino_sieci.md](03_program_vertino_sieci.md) zamiast patchy poniżej.

**Sterownik:** FATEK HB1-14MBJ25 | **Jednostka:** `Main_unit1`  
Zmiany z [audyt.md](audyt.md) (A0, A1). Po edycji: zapis → F9 do PLC → test.

---

## A0 — Pauza przy zatorze B4 (X4) w trakcie zliczania

**Wymaganie:** przy zajętej linii odbiorczej — stop przepychania, **C1 bez resetu**, brak końca partii; po zwolnieniu B4 — wznowienie od aktualnego C1. Obrót modułu **bez** blokady X4 (już OK w N0029).

Używaj kontaktu **`/M507`** (status zatoru po debiouncing — sieci N0041–N0042), nie surowego X4, żeby zgadzało się z HMI i symulacją M1050.

### N0015 — FUN140 Transport

**Było:** `FUN140` uruchamiane przy samym `M21`.

**Ma być:** ruch transportu tylko gdy linia odbiorcza wolna (`/M507`).

```
|--[M21]--[/M507]--+--[FUN140.HSPSO Ps:0 SR:R1100 WR:R1144]--|
|                  |    FO0 -> M1992
|                  |    FO1 -> M501
|                  |    FO2 -> RST M21
```

Mnemotechnika (fragment):

```
ORG        M21
AND   NOT  M507
LD    OPEN
LD    OPEN
FUN   140.HSPSO
           Ps:  0
           SR:  R1100
           WR:  R1144
...
```

### N0021 — Liczenie opakowań na B1

**Było:** impuls B1 zwiększa C1 przy `M22`.

**Ma być:** zliczanie tylko gdy **nie** ma zatoru.

```
|--[X1]--[M22]--[/M507]--[FUN (+1) C1]--|
```

Mnemotechnika:

```
ORG        X1
AND        M22
AND   NOT  M507
FUN   15 _.(+1)
           :  C1
```

### N0022 — Sprawdzenie ilości (koniec partii)

**Było:** `C1 >= R1400` → `M233` przy `M22`.

**Ma być:** koniec partii tylko przy wolnym odbiorze.

```
|--[C1>=R1400]--[M22]--[/M507]--( M233 )--|
```

Mnemotechnika:

```
ORGF  174_.>=
      Sa:  C1
      Sb:  R1400
AND        M22
AND   NOT  M507
OUTS       M233
```

### N0031 — Timeout transportu (T5)

**Było:** timeout T5 mógł zadziałać podczas długiego oczekiwania na B4.

**Ma być:** timeout liczy się tylko gdy zator **nie** trwa (operator czeka na linię, nie na błąd transportu).

```
|--[T5]--[/M507]--( M505 )--|
|              +--( RST M22 )--|
```

Mnemotechnika (dopisz `AND NOT M507` przed wyjściami M505 / RST M22):

```
ORG        T5
AND   NOT  M507
AND   SHORT
OUTS       M505
OUTR       M22
...
```

### Sieci bez zmian (już OK)

| Sieć | Zachowanie |
|------|------------|
| N0020 | Start cyklu — `/X4`, `/M1050` |
| N0021 (start M22) | `RST C1` tylko przy wejściu w M22 — **nie** przy samym B4 |
| N0029 | Start obrotu — bez X4 |

---

## A1 — Przedmuch AUTO tylko przy 180°

**Problem:** N0068 ma `M70` → `Y5` ciągle w AUTO (błąd procesowy).

**Ma być:** zawór Y5 w AUTO tylko gdy moduł w pozycji **180°** (`R1501 = 180`). Przedmuch ręczny (`M240`) bez zmian.

### N0068 — Przedmuch AUTO

**Usuń** prostą linię:

```
|--[M70]--( Y5 )--|    ← USUŃ
```

**Wstaw:**

```
|--[M70]--[R1501=180]--( Y5 )--|
```

W WinProLadder: blok porównania rejestru (np. **WORD =**), źródło `R1501`, wartość stała `180`, wynik w szeregu przed cewką `Y5`.

Mnemotechnika (przykład — sprawdź numer funkcji w podglądzie mnemotechniki po wstawieniu):

```
ORG        M70
ANDF  175_.=
      Sa:  R1501
      Sb:  180
OUTS       Y5
```

### N0069 / M240 — bez zmian

```
|--[M240]--( Y5 )--|    // przedmuch ręczny z HMI
```

---

## Kolejność wdrożenia w WinProLadder

1. Otwórz `plc/SKO-Program.pdw` (offline).
2. Edytuj sieci **N0015, N0021, N0022, N0031, N0068** według schematów powyżej.
3. **F8** — sprawdzenie składni.
4. Zapisz → połącz z PLC → **F9** — uruchom.
5. Test:
   - AUTO, partia w toku (M22, C1>0), włącz B4 (lub M1050 symulacja) → transport stoi, C1 stałe, brak M233.
   - B4 OFF → zliczanie / dokończenie partii.
   - Obrót przy B4 ON — dozwolony.
   - Y5 AUTO — tylko przy R1501=180 (monitor F11).

6. Wydruk PDF → uruchom `narzedzia/generuj_dokumentacje.py` (aktualizacja docs).

---

## Eksport kopii zapasowej

Przed zmianami: `File → Save As` kopia `SKO-Program_przed_A0A1.pdw`.  
Opcjonalnie eksport zmienionych sieci: `File → Export → Ladder Diagram` → `plc/export/sieci/`.

---

**© CNC Solutions — Michał Batorowicz**
