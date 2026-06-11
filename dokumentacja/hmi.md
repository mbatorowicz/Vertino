# Panel HMI — interfejs PLC ↔ HMI

**Panel:** FATEK P2043NA/P2043EA (4.3", dotykowy) | **Projekt:** [hmi/SKO - Program 1.fpj](<../hmi/SKO%20-%20Program%201.fpj>) (FvDesigner)

**Instrukcja wdrożenia krok po kroku (FvDesigner):** [hmi_wdrozenie.md](hmi_wdrozenie.md)

Poniższe adresy wynikają z analizy programu PLC ([plc/program.md](plc/program.md)) oraz
propozycji rozbudowy ([plc/propozycja_rozbudowy.md](plc/propozycja_rozbudowy.md)).

---

## Przyciski (HMI → PLC)

| Adres | Funkcja | Typ | Warunki działania |
|-------|---------|-----|-------------------|
| M300 | START | bit, zbocze ↑ | READY + bezpieczeństwo + HOME_OK, brak alarmu |
| M301 | STOP | bit | zawsze |
| M302 | RESET (kasowanie alarmu) | bit | tylko przy zazbrojonym bezpieczeństwie |
| M310 | HOME (bazowanie) | bit, zbocze ↑ | tylko w READY |
| M305 | Zapis parametrów serwo | bit, zbocze ↑ | nie podczas ruchu osi; funkcja serwisowa |
| M420 | Zezwolenie liczenia | bit (przełącznik) | produkcyjnie ON |
| M421 | Zezwolenie zaworu przedmuchu | bit (przełącznik) | produkcyjnie ON |
| M320 | Tryb serwisowy | bit (przełącznik) | tylko w READY (S1) |
| M323 | Tryb przezbrajania | bit (przełącznik) | wymaga M320 |
| M340 | Transport jog (serwis) | bit, trzymany | M329, nie przy M323 |
| M341 | Przedmuch ręczny (serwis) | bit (przełącznik) | M329 |
| M342 | Obrót serwis +90° | bit, impuls | M329, /M323, M470 |
| M343 | Obrót przezbrajania +90° | bit, impuls | M330 |
| M311 | Zeruj licznik partii | bit, impuls | poza S2 |
| M312 | Zeruj statystyki | bit, impuls | — |

## Nastawy (HMI → PLC)

| Adres | Funkcja | Jednostka | Uwagi |
|-------|---------|-----------|-------|
| R6 | Ilość sztuk w partii | szt. | edycja na **BS1** (klik w wartość celu); wymagane > 0 |
| R7 | Opóźnienie po partii | × 0.01 s | nastawa timera T10 |
| R8 | Czas przejazdu słoika przy B3 | × 0.01 s | próg zasłonięcia X3 (T30); dłużej → pauza M403 |
| R9 | Timeout bazowania | × 0.1 s | po wdrożeniu P1 |
| R10 | Timeout obrotu | × 0.1 s | po wdrożeniu P2 |
| R11 | Prędkość obrotu przezbrajania | Hz (32-bit) | tryb M323 |
| R12 | Przyspieszenie przezbrajania | — | kopiowane do R1211 |
| R13 | Timeout obrotu przezbrajania | × 0.1 s | dłuższy niż R10 |
| R1403 | Prędkość obrotu produkcyjna | Hz (32-bit) | od następnego obrotu |
| R1303, R1312 | Prędkości bazowania | Hz (32-bit) | program HOME |
| R1211 | Przyspieszenie/hamowanie osi | — | wymaga M305 |
| R1209 | Creep bazowania | — | wymaga M305 |
| R1221 | Offset bazy (Machine Zero) | 32-bit | wymaga M305 + HOME |

Rejestry są retentywne — nastawy przeżywają wyłączenie zasilania.

## Statusy (PLC → HMI)

| Adres | Funkcja |
|-------|---------|
| S1 | READY |
| S2 | RUN |
| S3 | ALARM |
| S10 / S11 / S12 / S13 | Krok cyklu: bazowanie / liczenie / opóźnienie / obrót |
| R100 | Licznik sztuk bieżącej partii (kopia C0) |
| M470 | Maszyna zbazowana (HOME_OK) |
| M462 / M433 / M468 | Przyczyna alarmu: błąd bazowania / obrotu / parametrów |
| M530–M535 | Latche alarmów (szczegóły na BS4) | po wdrożeniu P3 |
| M403 | Pauza — czujnik B3 (zasłonięty zbyt długo) |
| M329 / M330 | Serwis / przezbrajanie aktywne |
| M431 / M536 | Obrót w toku / obrót przezbrajania |
| M539 | Nastawy poprawne |
| D100 | Licznik partii (total) |
| D102 | Licznik sztuk (total, 32-bit) |
| R201 | Czas ostatniego cyklu [× 0.1 s] |
| X0 | Stan obwodu bezpieczeństwa |

> Rozróżnienie przyczyny alarmu na ekranie: S3 + M462 → „Błąd bazowania",
> S3 + M433 → „Błąd obrotu", S3 + M468 → „Błąd parametrów serwo",
> S3 + /X0 → „Bezpieczeństwo / E-stop".

---

## Ekrany panelu

Zrzuty z FvDesigner: [hmi/Zrzut ekranu 2026-06-11 184233.png](<../hmi/Zrzut ekranu 2026-06-11 184233.png>),
[hmi/Zrzut ekranu 2026-06-11 184312.png](<../hmi/Zrzut ekranu 2026-06-11 184312.png>).

### BS1 (RUN) — ekran główny

![Ekran BS1 RUN](<../hmi/Zrzut ekranu 2026-06-11 184233.png>)

| Element | Powiązanie (wg programu PLC) |
|---------|------------------------------|
| Lampki READY / RUN / ALARM / HOME_OK | S1 / S2 / S3 / M470 |
| Licznik `12 / 12` (bieżący / cel) | R100 / **R6** — **cel edytowalny** (klik → klawiatura popup) |
| Lampka + przełącznik „Liczenie" | M420 |
| Lampka + przełącznik „Powietrze" | M421 |
| START / STOP / RESET | M300 / M301 / M302 |
| HOME / obrót (przyciski wygaszone) | M310 / — |
| SET (prawy górny róg) | przejście do BS2 (SETUP) |

### BS2 (SETUP) — nastawy

![Ekran BS2 SETUP](<../hmi/Zrzut ekranu 2026-06-11 184312.png>)

| Pole | Powiązanie |
|------|-----------|
| „Opóźnienie po partii [× 0,01 s]" | R7 |
| „Czas przejazdu słoika przy B3 [× 0,01 s]" | R8 — czas zasłonięcia czujnika przez jeden słoik; dłużej → pauza |
| „Offset bazy" | **R1221** (32-bit INT) — parametr „Machine Zero Point" w tabeli parametrów serwo (Table1) |

Wprowadzanie wartości przez wyskakującą klawiaturę numeryczną (osobny ekran popup).

> **Uwaga — Offset bazy (R1221):** nowa wartość trafia do osi dopiero po ponownym
> zapisie parametrów (FUN141 MPARA) — czyli po wyzwoleniu **M305** albo po restarcie
> zasilania PLC (pierwszy skan), i wymaga ponownego bazowania (HOME).

### BS5 (Screensaver)

Wygaszacz z logo klienta (exim pharma Laboratories).

### BS3 (SERWIS) i BS4 (ALARMY) — nowe ekrany

Pełna specyfikacja obiektów, adresów `@HB1:…`, typów przycisków i testów:
**[hmi_wdrozenie.md](hmi_wdrozenie.md)** (sekcje 4–5).

---

**© CNC Solutions — Michał Batorowicz**
