# Mapa I/O i rejestrów

**Źródło:** wydruk [plc/SKO-Program.pdf](../../plc/SKO-Program.pdf) — komentarze elementów,
indeks krzyżowy (Contact[Network]) i konfiguracja I/O. Stan z 2026-06.

Tabele zawierają **wyłącznie elementy faktycznie używane** w programie (31 sieci).
Pozostałości po starszych wersjach — na końcu dokumentu.

---

## Wejścia fizyczne

| Adres | Symbol | Funkcja | Użycie w programie |
|-------|--------|---------|--------------------|
| X0 | SAFETY_STATUS | Pilz PNOZ X7 (wyjście 13/14) — obwód bezpieczeństwa | N0000, N0002–N0007, N0012, N0017, N0028 |
| X1 | SENSOR_B1 | Czujnik liczenia słoików (wejście do modułu) | N0023 — zliczanie na zboczu **opadającym** |
| X2 | SENSOR_B2 | Wejście DOG bazowania serwo | Tylko w konfiguracji tabeli parametrów serwo ([serwo.md](serwo.md)) — nie występuje w drabince |
| X3 | SENSOR_B3 | Czujnik na wyjściu — czas zasłonięcia przez słoik | N0010–N0011 — pauza M403 gdy zasłonięty > R8 × 0,01 s |
| X4 | KEY_PRZEBRAJ | Styk **NO** kluczyka (ON = **przezbrajanie**, nie serwis) | M330, BS6, M343/M344 |

## Wyjścia fizyczne

| Adres | Symbol | Funkcja | Użycie |
|-------|--------|---------|--------|
| Y1 | — | Napęd transportu/podajnika (załączenie sterowników napędów) | N0022 (M410) |
| Y2 | PSO1 PLS | Impulsy serwo modułu obrotowego | FUN140 (konfiguracja PSO1) |
| Y3 | PSO1 DIR | Kierunek serwo | FUN140 (konfiguracja PSO1) |
| Y4 | Valve | Zawór przedmuchu pneumatycznego | N0009 (M400·/M403·M421) |
| Y5 | PNEUMATIC_VALVE | — | **Nieużywane** w bieżącym programie |

---

## Przekaźniki krokowe S

| Adres | Symbol | Opis |
|-------|--------|------|
| S1 | READY | Gotowość |
| S2 | RUN | Praca automatyczna |
| S3 | ALARM | Alarm |
| S10 | HOMING | Bazowanie |
| S11 | LICZENIE | Transport + zliczanie |
| S12 | OPÓŹNIENIE | Odczekanie T10 po partii |
| S13 | OBRÓT | Obrót modułu |

S0–S499 są **nieretentywne** — po zaniku zasilania maszyna wstaje bez aktywnego kroku.

## Przekaźniki M — interfejs HMI

| Adres | Symbol | Kierunek | Opis |
|-------|--------|----------|------|
| M300 | START | HMI → PLC | Start pracy (zbocze ↑) |
| M301 | STOP | HMI → PLC | Stop pracy |
| M302 | RESET | HMI → PLC | Kasowanie alarmu S3 |
| M305 | MPARA_APPLY | HMI → PLC | Ponowny zapis parametrów serwo (zbocze ↑) |
| M310 | HOME Bt | HMI → PLC | Start bazowania (tylko w READY) |
| M420 | Zezwolenie liczenia | HMI → PLC | Musi być ON, by C0 zliczał (N0023) |
| M421 | Zezwolenie zaworu | HMI → PLC | Musi być ON, by Y4 działał (N0009) |

Uwaga: komentarze fabryczne M420/M421 brzmią „wył. liczenie" / „Wył. zawór",
ale w drabince są to styki **NO** — działają jako zezwolenia (ON = funkcja aktywna).

## Przekaźniki M — logika wewnętrzna

| Adres | Symbol | Opis |
|-------|--------|------|
| M400 | M_EN | Master enable = S2 · X0 |
| M401 | M_EN_FLOW | Zezwolenie przepływu = M400 · /M403 |
| M403 | B3_BLOCK | Pauza — B3 zasłonięty dłużej niż R8 (T30) |
| M410 | — | Zezwolenie transportu = (S11+S12) · M401 → Y1 |
| M431 | — | Obrót aktywny (ACT FUN140/R1400) |
| M432 | — | Obrót zakończony (DN) |
| M433 | — | Błąd obrotu (ERR) → S3 |
| M460 | — | Bazowanie aktywne (ACT FUN140/R1300) |
| M461 | — | Bazowanie zakończone (DN) |
| M462 | — | Błąd bazowania (ERR) → S3 |
| M468 | MPARA_ERR | Błąd zapisu parametrów serwo → S3 |
| M470 | HOME_OK | Maszyna zbazowana (warunek startu) |
| M1924 | First scan | Systemowy — pierwszy skan (ładowanie parametrów) |

## Timery i liczniki

| Adres | Baza | Nastawa | Opis |
|-------|------|---------|------|
| T10 | 0.01 s | **R7** | Opóźnienie po partii (S12) |
| T30 | 0.01 s | **R8** | Próg czasu zasłonięcia czujnika B3 przez słoik |
| C0 | 16-bit, retentywny | **R6** (porównanie) | Licznik sztuk w partii; zerowany przy wejściu w S11 i przy alarmie |

## Rejestry R

| Adres | Opis | Uwagi |
|-------|------|-------|
| R6 | Ilość sztuk w partii (cel C0) | Nastawa z **BS1** (klik operatora); musi być > 0 |
| R7 | Opóźnienie po partii [× 0.01 s] | Nastawa z HMI (SETUP) |
| R8 | Czas przejazdu słoika przy B3 [× 0.01 s] | Próg T30; dłuższe zasłonięcie X3 → M403 |
| R100 | Kopia C0 dla HMI | Aktualizowana w S11 |
| R1200–R1223 | Tabela parametrów serwo (Table1) | [serwo.md](serwo.md) |
| R1300–R1319 | Program serwo HOME (Table2) | DRVZ + ABS 0 |
| R1400–R1410 | Program serwo ROTATE (Table3) | DRV ADR −25000 |
| R1500–R1509 | Rejestry robocze FUN140 HOME (WR) | R1501 zerowany po bazowaniu |
| R1510–R1519 | Rejestry robocze FUN140 ROTATE (WR) | R1511 zerowany po obrocie |

R0–R2999 są **retentywne** — nastawy R6/R7/R8 i tabele serwo przeżywają zanik zasilania.

---

## Pozostałości po starszych wersjach programu (nieużywane)

Poniższe symbole mają komentarze w projekcie, ale **nie występują** w drabince —
do wyczyszczenia w WinProLadder przy najbliższej edycji:

- **M:** M1, M10, M21–M25, M70, M80, M82, M100, M110–M115, M120, M200, M233, M240,
  M321, M322, M404, M406, M407, M409, M501–M507, M520, M1000–M1003, M1010–M1024,
  M1050, M1992, M1993
- **T:** T5, T6, T7, T8, T50, T200
- **C:** C1
- **R:** R524, R1100, R1120, R1507 (R1410/R1411 mają stare komentarze, ale leżą
  w obszarze tabeli ROTATE — komentarz mylący, obszar zajęty przez Table3)
- **D:** D100, D200–D204
- **X/Y:** Y5 (nieużywane w bieżącym programie)

Stare komentarze typu „R1400 = Opakowania w partii", „C1 = Licznik opakowań",
„T5 = Timeout transportu" opisują **poprzedni program** i nie mają związku
z bieżącą logiką. Aktualną ilość sztuk w partii zadaje **R6**, a licznikiem jest **C0**.

---

**© CNC Solutions — Michał Batorowicz**
