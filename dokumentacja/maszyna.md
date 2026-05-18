# Maszyna — Vertino

**Vertino — Stacja oczyszczania opakowań**  
**Numer seryjny:** VERTINO-MO-2025-___________ *(poprzednia seria dokumentacji: SKO-MO)*
**Sterownik:** FATEK HB1-14MBJ25 | **HMI:** P5043NB | **Bezpieczeństwo:** Pilz PNOZ X7

---

## Przeznaczenie

Stacja oczyszcza opakowania (słoiki) przed napełnianiem: obrót do pozycji **180°** i przedmuch sprężonym powietrzem (**Y5**). Usuwa zanieczyszczenia stałe po transporcie i magazynowaniu.

**Kontrola przepływu:** czujnik **B4** na wyjściu — przy zatorze na linii odbiorczej maszyna zatrzymuje przepychanie (nie obrót), licznik partii **C1** pozostaje w pamięci.

---

## Konstrukcja

| Element | Opis |
|---------|------|
| Moduł obrotowy M1 | 4 pozycje co 90°, przekładnia 1:50 (SS86D) |
| Transportery M2+M3 | Przepychanie partii (Beak SH-D08R) |
| Równoległe partie | Do 4 partii w różnych fazach cyklu 360° |

### Pozycje modułu

| Kąt | Funkcja |
|-----|---------|
| **0°** | Wejście / wyjście partii (góra) |
| **90°** | Pozycja transportowa (bok) |
| **180°** | Oczyszczanie — przedmuch, dnem do góry |
| **270°** | Pozycja transportowa (bok) |

```
        [0° wejście/wyjście]
              │
   [270°] ───┼─── [90°]
              │
        [180° przedmuch]
```

---

## Proces technologiczny

### Cykl jednej partii (360°)

1. Sprawdzenie **B4** (linia odbiorcza wolna).
2. **Transport** — przepychanie; **B1** zlicza słoiki do **R1400**.
3. **Stabilizacja** — czas **R1410** (T6).
4. **Kontrola stref** — B1/B2 (M233).
5. **Obrót 90°** — FUN140, rejestr **R1200**.
6. Powtórzenie — kolejna partia wypycha już oczyszczone słoiki (gdy B4 pozwala).

### Sekwencja PLC (flagi)

```
M70 → M21 → M22 → M23 → M233 → M24 → M25 → M21 …
```

PLC w sterowniku: [plc/STAN_FAKTYCZNY.md](plc/STAN_FAKTYCZNY.md) · plan programu: [plc/03_program_vertino_sieci.md](plc/03_program_vertino_sieci.md).

### Parametry procesu (HMI)

| Rejestr | Zakres | Domyślnie | Znaczenie |
|---------|--------|-----------|-----------|
| R1400 | 1–10 | 3 | Słoiki w partii |
| R1401 | 50–500 Hz | 200 | Prędkość transportu |
| R1402 | 100–1000 Hz | 400 | Prędkość obrotu |
| R1403 | 12400–12600 | 12500 | Impulsy na 90° |
| R1410 | 50–1000 ms | 200 | Stabilizacja |
| R1411 | 50–500 ms | 100 | Pauza po obrocie |

Typowy czas cyklu: **12–18 s** (R1500).

### Zator B4 {#zator-b4}

| Stan B4 | Zachowanie |
|---------|------------|
| OFF | Przepychanie i zliczanie normalne |
| ON | Stop przepychania; **C1 bez resetu**; obrót modułu może trwać |

---

## Dokumenty powiązane

| Dokument | Odbiorca |
|----------|----------|
| [operator.md](operator.md) | Operator |
| [serwis.md](serwis.md) | Serwis |
| [techniczna.md](techniczna.md) | Producent / integrator |
| [plc/](plc/) | Program sterownika |
| [receptury.md](receptury.md) | Profile opakowań |

**© CNC Solutions — Michał Batorowicz**
