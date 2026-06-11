# Instrukcja serwisowa

**Urządzenie:** Stacja kontroli opakowań SKO
**Dla:** serwis mechaniczny, automatyka, utrzymanie ruchu

Dokumentacja techniczna programu: [plc/program.md](plc/program.md),
[plc/mapa_io.md](plc/mapa_io.md), [plc/serwo.md](plc/serwo.md).

---

## 1. Zakres serwisu

| Poziom | Zakres |
|--------|--------|
| Operator | Patrz [instrukcja_obslugi.md](instrukcja_obslugi.md) |
| Serwis I | Konserwacja, przezbrajanie, regulacja czujników, wymiana tulei |
| Serwis II | Program PLC/HMI, parametry serwo, diagnostyka napędów |
| Elektryk | Schemat [SKO.pdf](../schemat_elektryczny/SKO.pdf), obwód Pilz |

---

## 2. Konserwacja planowa

| Czynność | Interwał | Uwagi |
|----------|----------|-------|
| Kontrola wytarcia tulei / gniazd modułu | 500 h / 3 mies. | Wymiana wg zużycia |
| Smarowanie prowadnic / łożysk (wg karty) | wg producenta | Patrz dane techniczne |
| Filtr/regulator powietrza | wg klienta | Przed zaworem Y4 |
| Sprawdzenie dokręcenia śrub modułu obrotowego | 6 mies. | Po wibracjach |
| Test E-stop + B4 + kluczyk Pilz | 6 mies. | Protokół w [odbior_uruchomienie.md](odbior_uruchomienie.md) |
| Kopia zapasowa PLC/HMI | po każdej zmianie | `.pdw`, `.fpj` na USB w szafie |

---

## 3. Komponenty główne

| Komponent | Typ | Lokalizacja |
|-----------|-----|-------------|
| PLC | FATEK HB1-14MBJ25-D24A | Szafa sterownicza |
| HMI | FATEK P2043NA/P2043EA | Panel operatorski |
| Bezpieczeństwo | Pilz PNOZ X7 774059 | Szafa, str. 4 schematu |
| Napęd modułu | SS86D + iCAN 57BLF-1830NBB | Moduł obrotowy |
| Napęd transportu | SH-D08R + silnik krokowy | Tor transportu |
| Zawór przedmuchu | Y4 | Strefa modułu |
| Czujnik B1 | X1 — liczenie | Wejście modułu |
| Czujnik B2 | X2 — DOG serwo | Moduł obrotowy |
| Czujnik B3 | X3 — zator wyjścia | Za modułem |
| Czujnik B4 | Osłona — Pilz | Osłona PC |

---

## 4. Parametry — odniesienie

### 4.1 Proces

| Parametr | Adres PLC | Domyślnie | Zakres | Gdzie ustawia |
|----------|-----------|-----------|--------|---------------|
| Ilość w partii | R6 | 12 | 1–100 | **BS1** — operator (klik w cel licznika) |
| Opóźnienie po partii [×0,01 s] | R7 | 12 | 0–30000 | BS2 (SETUP) |
| Czas przejazdu słoika przy B3 [×0,01 s] | R8 | 12 | 1–30000 | BS2 (SETUP) |

**R8:** czas, w którym pojedynczy słoik zasłania czujnik B3 przy normalnym przepływie.
Zasłonięcie dłuższe niż R8 × 0,01 s uruchamia pauzę M403 (linia odbiorcza nie nadąża).

### 4.2 Serwo modułu (SETUP / serwis)

| Parametr | Adres | Uwagi |
|----------|-------|-------|
| Prędkość obrotu | R1403 | Od następnego obrotu |
| Prędkość bazowania | R1303, R1312 | Program HOME |
| Acc/dec | R1211 | Wymaga ZAPISZ PARAMETRY (M305) |
| Creep | R1209 | Wymaga M305 |
| Offset bazy | R1221 | Wymaga M305 + HOME |
| Timeout bazowania [×0,1 s] | R9 | 300 |
| Timeout obrotu [×0,1 s] | R10 | 100 |

### 4.3 Obrot serwisowy (ekran SERWIS)

| Parametr | Adres | Domyślnie | Zakres | Warunek |
|----------|-------|-----------|--------|---------|
| Prędkość serwisowa | R14 | 4000 | 500–15000 | X4=OFF, osłona zamknięta |
| Prędkość przezbrajania | R11 | 500 | 50–2000 | X4=ON (klucz SERWIS) |
| Przyspieszenie przezbraj. | R12 | 60000 | 10000–60000 | X4=ON |
| Timeout przezbraj. [×0,1 s] | R13 | 600 | 100–3600 | X4=ON |

Szczegóły osi: [plc/serwo.md](plc/serwo.md). Obrót produkcyjny: **90°** (−25000 imp,
przekładnia 10:1).

---

## 5. Tryb serwisowy (BS3) i przezbrajanie (BS6)

Procedura operatorska: [instrukcja_obslugi.md](instrukcja_obslugi.md) §8.

### Serwis — wejście na ekran BS3

**M320** włącza się przy wejściu na BS3 (M329 = M320·S1·X0·/X4). **Bez kluczyka**,
osłona zamknięta. Trzy prędkości obrotu: produkcja **R1403**, serwis **R14**, przezbrajanie **R11**.

| Funkcja | Adres |
|---------|-------|
| Jog transportu | M340 |
| Przedmuch | M341 |
| Obrót +90° | M342 (R14) |
| HOME | M310 |

### Przezbrajanie — klucz X4 + ekran BS6

Klucz **PRZEBRAJANIE** → **M330** (= X4), panel **BS6** (instrukcja, przyciski obrotu, jog).

| Funkcja | Adres |
|---------|-------|
| Góra / lewo +90° | M343 (R11) |
| Dół / prawo −90° | M344 (R11) |
| Jog napędów | M340 |

Wdrożenie: [plc/propozycja_rozbudowy.md](plc/propozycja_rozbudowy.md), [hmi_wdrozenie.md](hmi_wdrozenie.md).

---

## 6. Diagnostyka — tabela usterek

| Objaw | Możliwa przyczyna | Działanie |
|-------|-------------------|-----------|
| Brak X0 | E-stop, osłona przy X4=OFF, klucz PRODUKCJA + otwarta osłona | RESET Pilz, zamknij osłonę / klucz PRZEBRAJANIE |
| HOME nie kończy | B2 (DOG) luźny, moduł zablokowany | Regulacja czujnika, mechanika |
| Obrót nie kończy / timeout | Zablokowanie, błąd SS86D | Alarm na panelu, sprawdź ALM+ sterownika |
| C0 nie rośnie | M420 OFF, brak impulsów B1, M403 | Włącz Liczenie, regulacja B1 |
| Ciągła pauza B3 | R8 za małe lub linia odbiorcza nie nadąża | Zwiększ R8 (czas przejazdu słoika przy B3) lub przyspiesz odbiór |
| Partia za krótka/długa | Złe R6 lub R7 | Skoryguj opóźnienie po partii |
| Y4 bez przedmuchu | M421 OFF, M403, brak ciśnienia | Powietrze, zawór, PLC |
| Y1 bez transportu | M403, awaria SH-D08R | Diagnostyka napędu |

**Monitor PLC:** WinProLadder F11 — stany S1/S2/S11–S13, M403, C0, R100.

---

## 7. Wymiana elementów modułu (przezbrajanie)

Średnice słoików: [srednice_slokow.txt](srednice_slokow.txt).

1. Klucz **PRZEBRAJANIE** (X4), ekran **BS6**, obrót M343/M344, jog M340.
2. Demontaż tulei / prowadnic (wg rysunku — uzupełnić numer rysunku: _________).
3. Montaż zestawu na docelowy format, kontrola wymiarowa.
4. Kluczyk PRODUKCJA, HOME, próba z pustym modułem, potem z słoikami.

---

## 8. Odtwarzanie oprogramowania

| Element | Plik | Narzędzie |
|---------|------|-----------|
| PLC | `plc/SKO-Program.pdw` | WinProLadder → F9 |
| HMI | `hmi/SKO - Program 1.fpj` | FvDesigner → Download |
| Potwierdzenie | `plc/SKO-Program.pdf` | Wydruk po zapisie |

Po wgraniu: HOME, test obrotu, test liczenia, protokół punktów z [odbior_uruchomienie.md](odbior_uruchomienie.md).

---

## 9. Części zamienne (do uzupełnienia przez wykonawcę)

| Lp. | Opis | Nr katalogowy | Ilość zalecana |
|-----|------|---------------|----------------|
| 1 | Tuleje gniazd modułu (zestawy per średnica) | | |
| 2 | Czujnik B1/B3 (typ) | | 1 |
| 3 | Elementy quick-connect pneumatyki | | |
| 4 | Bezpiecznik F01 10 A | | 2 |

---

**© CNC Solutions — Michał Batorowicz**
