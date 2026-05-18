# Program PLC — Vertino

**Sterownik:** FATEK HB1-14MBJ25  
**Oprogramowanie:** WinProLadder  
**Jednostka:** `Main_unit1`  

| Wersja | Sieci | Dokumentacja |
|--------|-------|----------------|
| Obecna (produkcja) | 78 (N0000–N0077) | [01_odszyfrowanie_starego_programu.md](01_odszyfrowanie_starego_programu.md) |
| **Docelowa (Vertino)** | **35** (N0000–N0034) | **[03_program_vertino_sieci.md](03_program_vertino_sieci.md)** |

**Pliki na dysku** *(nazwa historyczna SKO-Program)*: [SKO-Program.pdw](../../plc/SKO-Program.pdw) · [SKO-Program.pdf](../../plc/SKO-Program.pdf) · [export/](../../plc/export/) · docelowo `Vertino-Program.pdw`

> Numeracja WinProLadder: **N0000–N0077**. Stara dokumentacja projektu (001–072) = sieci **N0002–N0077** plus N0000–N0001 (bezpieczeństwo).

---

## Architektura

Moduł **4×90°**. Przedmuch **Y5** w pozycji 180° (R1501).

### Gotowość (M10)

- **M1** — X0 (Pilz)
- **M82** — HOME wykonany
- Brak **M503–M506**

### Cykl AUTO

```
M1001 + M10 → M70
M70: M21 → M22 (transport, C1) → M23 (T6) → M233 → M24 → M25 (obrót) → M21
```

### Serwo FUN140 / FUN141

| Oś | FUN140 (SR) | FUN141 (SR) | Koniec |
|----|-------------|-------------|--------|
| Transport | R1100 | R1120 | M1992 |
| Obrót 90° | R1200 | R1220 | M1993 |
| HOME | R1300 | — | M82 / M504 |

Parametry 141.MPARA ładowane przy **M1924** (First Scan) — sieci N0013, N0014.

---

## Czujniki

| Symbol | Wejście | Funkcja |
|--------|---------|---------|
| B1 | X1 | Zliczanie w M22 (N0022); kontrola strefy w M233 |
| B2 | X2 | Kontrola wyjścia w M233 |
| B3 | X3 | HOME 0° |
| B4 | X4 | Zator odbioru — ciągły sygnał |

---

## Licznik C1 i B4

**C1** — licznik rejestrowy; wartość do jawnego **RST C1** (N0021 przy starcie transportu).

Przy zatorze (wymaganie procesowe / audyt A0):

- Nie **RST C1** przy X4 = ON w trakcie M22.
- Nie kończyć partii (`C1 >= R1400`) przy X4 = ON.
- Zatrzymać transport (FUN140); **obrót bez X4**.

### B4 w programie (stan z eksportu)

| Sieć | Zachowanie |
|------|------------|
| N0020 | Start cyklu — blokada X4 lub M1050 |
| N0021 | Start transportu — kontakt **NC X4** |
| N0022 | Liczenie B1 w M22 |
| N0030 | Start obrotu — **bez X4** |
| N0041–N0046 | R1507, M507, D204 |

Pełne mapowanie: [mapowanie.md](mapowanie.md). Lista sieci: [lista_sieci.md](lista_sieci.md). Audyt zmian: [audyt.md](audyt.md).

---

## Struktura sieci (grupy)

| Sieci | Zakres funkcji |
|-------|----------------|
| N0000–N0005 | Bezpieczeństwo, gotowość, reset błędów |
| N0006–N0012 | START/STOP, HOME |
| N0013–N0018 | FUN141, FUN140, READY serwo |
| N0019–N0032 | Cykl: transport, liczenie, obrót, timeouty |
| N0033–N0040 | Walidacja R1400–R1403 |
| N0041–N0046 | B4, status HMI |
| N0047–N0051 | Pozycja R1501, czas cyklu R1500 |
| N0052–N0076 | Tryb ręczny, przedmuch |
| N0077 | Koniec programu (ORG) |

Szczegóły każdej sieci: folder [sieci/](sieci/).

---

## Timery

| Timer | PV | Czas | Sieć / rola |
|-------|-----|------|-------------|
| T5 | K30000 | 300 s | Timeout transportu → M505 |
| T6 | R1410 | parametr | Stabilizacja M23 |
| T7 | K8000 | 80 s | Timeout obrotu → M506 |
| T8 | R1411 | parametr | Pauza po obrocie |
| T10 | K8000 | 80 s | Timeout HOME → M504 |
| T50 | — | pomiar | Czas cyklu → R1500 |
| T200 | — | 3600 s | Licznik godzin H10 |

Bazy Fatek: T0–49 = 0,01 s; T50–199 = 0,1 s; T200–255 = 1 s.

---

## Parametry R (skrót)

| Rejestr | Zakres | Domyślnie |
|---------|--------|-----------|
| R1400 | 1–10 | 3 |
| R1401 | 50–500 Hz | 200 |
| R1402 | 100–1000 Hz | 400 |
| R1403 | 12400–12600 | 12500 |
| R1410 | 50–1000 ms | 200 |
| R1411 | 50–500 ms | 100 |

Poza zakresem → **M503**.

---

## Sterowanie HMI (M)

| M | Funkcja |
|---|---------|
| M1000 | RESET błędów |
| M1001 | START AUTO |
| M1002 | STOP AUTO |
| M1003 | HOME |
| M1010–M1013 | Transport FWD/REV |
| M1014–M1017 | Obrót CW/CCW |
| M1021–M1022 | Obrót ±90° |
| M1023–M1024 | Przedmuch ręczny |
| M1019–M1020 | Test B4 → M1050 |

---

## Po awarii bezpieczeństwa

1. Usuń przyczynę, reset Pilz → **X0 = ON**
2. **M1000** (N0002)
3. **HOME** (M1003 lub auto)
4. **M1001** START

---

## Indeks i mnemotechnika

| Zasób | Plik |
|-------|------|
| Adres → sieć | [indeks_krzyzowy.md](indeks_krzyzowy.md) |
| Listing ASCII | [mnemotechniki.txt](mnemotechniki.txt) |

**© CNC Solutions — Michał Batorowicz**
