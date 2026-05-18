# Audyt programu PLC — Vertino (program w sterowniku)

**Data:** 2026-05  
**Sterownik:** FATEK HB1-14MBJ25  
**Program w PLC:** 78 sieci (N0000–N0077) — [STAN_FAKTYCZNY.md](STAN_FAKTYCZNY.md)  
**Źródło stanu:** eksport [SKO-Program.pdf](../../plc/SKO-Program.pdf)

---

## Stan zgodny z maszyną

| Obszar | Ocena |
|--------|-------|
| Sekwencja M21→M22→M23→M233→M24→M25 | OK |
| B4 nie blokuje obrotu (N0030 bez X4) | OK |
| B4 blokuje start transportu (N0021, NC X4) | OK |
| B4 blokuje start cyklu (N0020, X4 / M1050) | OK |
| B1 — bariera US, 1 impuls / słoik | OK (hardware) |
| FUN140/FUN141, M1992/M1993 | OK |
| Walidacja R1400–R1403 (N0033–N0040) | OK |
| Bezpieczeństwo X0 → M1 (N0000–N0001) | OK |

### Mapowanie numeracji sieci

| Dok. projekt (stara) | WinProLadder | Nazwa |
|----------------------|--------------|-------|
| — | N0000–N0001 | Bezpieczeństwo ON/OFF |
| 001 | N0002 | Reset błędów z HMI |
| 019 | N0021 | Start transportu |
| 020 | N0022 | Liczenie opakowań na B1 |
| 021 | N0024 | Koniec transportu |
| 025 | N0030 | Start obrotu |
| 064 | N0068 | Przedmuch AUTO |

Pełna lista: [lista_sieci.md](lista_sieci.md).

---

## Do wdrożenia w PLC (priorytet)

**Instrukcja drabinki (WinProLadder, HB1):** [wdrozenie_drabinka_A0_A1.md](wdrozenie_drabinka_A0_A1.md)  
**Mnemotechnika po zmianach:** [../../plc/patch/mnemotechnika_A0_A1.txt](../../plc/patch/mnemotechnika_A0_A1.txt)

### A0 — Pauza przy zatorze B4 (w trakcie zliczania)

**Wymaganie:** przy X4 = ON — stop przepychania, **C1 bez zmian**, brak końca partii do C1 = R1400.

**Sieci:** N0015 (FUN140), N0021, N0022, N0031 (+ N0020 bez zmian).

**Zmiany:** `/M507` na zliczaniu B1, na `C1>=R1400`, na FUN140 przy `M21`; timeout T5 tylko gdy `/M507`.

### A1 — Przedmuch tylko przy 180° (N0068)

**Było:** `M70` → Y5 (ciągły przedmuch w AUTO).  
**Ma być:** `M70` **i** `R1501 = 180` → Y5; ręczny `M240` → Y5 bez zmian.

### P1 — Receptury średnic → R1400

Zobacz [receptury.md](../receptury.md) — 7 profili, wartość R1400 per średnica.

---

## Optymalizacje (niższy priorytet)

| Id | Temat |
|----|--------|
| A2 | Skrócenie R1411 (T8) po teście |
| B1 | Histereza B4 |
| B3 | Receptury HMI (7 profili) |

---

**© CNC Solutions — Michał Batorowicz**
