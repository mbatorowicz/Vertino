# Dane techniczne

**Urządzenie:** Stacja kontroli opakowań SKO

---

## 1. Identyfikacja

| | |
|---|---|
| Nazwa | Stacja kontroli / oczyszczania opakowań |
| Numer projektu | SKO |
| Wykonawca | CNC Solutions |
| Zastosowanie | Oczyszczanie słoików szklanych przedmuchem przed napełnieniem |
| Środowisko | Hala produkcyjna, linia farmaceutyczna (GMP — wg klienta) |

---

## 2. Parametry zasilania

| Parametr | Wartość |
|----------|---------|
| Napięcie główne | 230 V AC, 50 Hz |
| Moc przyłączeniowa | 2,8 A (wg tabliczki / schematu) |
| Obwód sterowania | 24 V DC / 10 A (zasilacz w szafie) |
| Powietrze | Sprężone, filtrowane — ciśnienie wg regulatora (typ. 6 bar) |
| Wyłącznik główny | -Q, na szafie / przy stanowisku |

---

## 3. Sterowanie

| Element | Typ |
|---------|-----|
| PLC | FATEK HB1-14MBJ25-D24A |
| Panel HMI | FATEK P2043NA / P2043EA, 4,3", dotyk |
| Oprogramowanie | WinProLadder + FvDesigner |
| Bezpieczeństwo | Pilz PNOZ X7 774059, 24 V AC/DC |
| Kluczyk | NC → Pilz; NO → **X4** (przezbrajanie → BS6) |

---

## 4. Napędy

| Funkcja | Napęd | Sterownik | Sygnały PLC |
|---------|-------|-----------|-------------|
| Moduł obrotowy | iCAN 57BLF-1830NBB, 188 W, enkoder | SS86D (AC 18–80 V) | Y2 PLS, Y3 DIR (PSO1) |
| Transport | Silnik krokowy + przekładnia | SH-D08R (×2 wg schematu) | Y1 |
| Przedmuch | Zawór pneumatyczny | — | Y4 |

**Moduł obrotowy:** przekładnia 10:1, krok programowy **90°** (−25000 impulsów
przy 10000 imp/obr silnika).

---

## 5. Czujniki

| Oznaczenie | Wejście | Funkcja | Typ (wg schematu) |
|------------|---------|---------|-------------------|
| B1 | X1 | Liczenie słoików | — |
| B2 | X2 | Baza modułu (DOG serwo) | — |
| B3 | X3 | Wyjście — czas zasłonięcia słoikiem | — |
| B4 | Pilz | Osłona modułu | Schneider XCSZC7902 |
| Bezpieczeństwo | X0 | Status obwodu Pilz | Wyjście 13/14 PNOZ X7 |

---

## 6. Parametry procesowe (zakres)

| Parametr | Zakres |
|----------|--------|
| Ilość słoików w partii | 1–100 (typ. 4–12) |
| Opóźnienie po partii | 0–300 s (R7 × 0,01 s) |
| Czas przejazdu słoika przy B3 | 0,01–300 s (R8 × 0,01 s) |
| Prędkość obrotu | 500–20000 (jednostki serwo) |
| Prędkość przezbrajania | 50–2000 |

---

## 7. Formaty słoików

Obsługiwane średnice (tuleje modułu): patrz [srednice_slokow.txt](srednice_slokow.txt).

| Pojemność | Średnica [mm] | Wysokość / uwagi [mm] |
|-----------|---------------|------------------------|
| 75 ml | 46 | 35 |
| 100 ml | 51 | 35 |
| 120 ml | 54 | 35–41 |
| 150 ml | 57 | 41 |
| 200 ml | 63 | 41 |
| 250 ml | 67 | 41 |
| 500 ml | 82 | 50 |
| 750 ml | 93 | 59 |

---

## 8. Wymiary i masa

| | |
|---|---|
| Wymiary (L × W × H) | __________ mm (uzupełnić po pomiarze) |
| Masa | __________ kg |
| Hałas | __________ dB(A) (pomiar opcjonalny) |

---

## 9. Warunki otoczenia

| Parametr | Wartość |
|----------|---------|
| Temperatura pracy | +5 … +40 °C (zalecane) |
| Wilgotność | 35–85 % RH, bez kondensacji |
| Oświetlenie stanowiska | Zgodnie z wymaganiami klienta / BHP |

---

## 10. Dokumenty powiązane

- Schemat: [schemat_elektryczny/SKO.pdf](../schemat_elektryczny/SKO.pdf)
- Program PLC: [plc/SKO-Program.pdf](../plc/SKO-Program.pdf)
- SH-D08R: [referencje/napedy/SH-D08R.pdf](../referencje/napedy/SH-D08R.pdf)

---

**© CNC Solutions — Michał Batorowicz**
