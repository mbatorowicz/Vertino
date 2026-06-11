# Panel HMI — interfejs PLC ↔ HMI

**Panel:** FATEK P2043NA/P2043EA (4.3", dotykowy) | **Projekt:** [hmi/SKO - Program 1.fpj](<../hmi/SKO%20-%20Program%201.fpj>) (FvDesigner)

**Instrukcja wdrożenia krok po kroku (FvDesigner):** [hmi_wdrozenie.md](hmi_wdrozenie.md)

Poniższe adresy wynikają z analizy programu PLC ([plc/program.md](plc/program.md)) oraz
propozycji rozbudowy ([plc/propozycja_rozbudowy.md](plc/propozycja_rozbudowy.md)).

---

## Trzy prędkości obrotu modułu

| Tryb | Ekran | Rejestr | Typowo |
|------|-------|---------|--------|
| **Produkcja** | automat | R1403 | 9000 Hz |
| **Serwis** | BS3 (wejście → M320) | R14 | 4000 Hz |
| **Przezbrajanie** | BS6 (klucz X4 → M330) | R11 | 500 Hz |

---

## Przyciski (HMI → PLC)

| Adres | Funkcja | Typ | Warunki działania |
|-------|---------|-----|-------------------|
| M300 | START | bit, zbocze ↑ | READY + bezpieczeństwo + HOME_OK, brak alarmu |
| M301 | STOP | bit | zawsze |
| M302 | RESET (kasowanie alarmu) | bit | tylko przy zazbrojonym bezpieczeństwie |
| M310 | HOME (bazowanie) | bit, zbocze ↑ | tylko w READY |
| M305 | Zapis parametrów serwo | bit, zbocze ↑ | nie podczas ruchu osi |
| M420 | Zezwolenie liczenia | bit (przełącznik) | produkcyjnie ON |
| M421 | Zezwolenie zaworu przedmuchu | bit (przełącznik) | produkcyjnie ON |
| M320 | Tryb serwisowy | bit | **Set przy wejściu BS3**, Reset przy wyjściu |
| M340 | Transport jog | bit, trzymany | M329 (BS3) lub M330 (BS6) |
| M341 | Przedmuch ręczny | bit | M329 lub M330 |
| M342 | Obrót serwis +90° | bit, impuls | BS3, M329, R14 |
| M343 | Obrót przezbraj. +90° „góra/lewo" | bit, impuls | BS6, M330, R11 |
| M344 | Obrót przezbraj. −90° „dół/prawo" | bit, impuls | BS6, M330, R11 |
| M311 | Zeruj licznik partii | bit, impuls | poza S2 |
| M312 | Zeruj statystyki | bit, impuls | — |

## Nastawy (HMI → PLC)

| Adres | Funkcja | Jednostka | Uwagi |
|-------|---------|-----------|-------|
| R6 | Ilość sztuk w partii | szt. | edycja na **BS1** (klik w cel) |
| R7 | Opóźnienie po partii | × 0.01 s | BS2 |
| R8 | Czas przejazdu słoika przy B3 | × 0.01 s | BS2 |
| R9 | Timeout bazowania | × 0.1 s | BS2 |
| R10 | Timeout obrotu | × 0.1 s | BS2 |
| R11 | Prędkość obrotu **przezbrajania** | Hz (32-bit) | BS6 |
| R12 | Przyspieszenie przezbrajania | — | BS6 |
| R13 | Timeout obrotu przezbrajania | × 0.1 s | BS6 |
| R14 | Prędkość obrotu **serwisowa** | Hz (32-bit) | BS3 |
| R1403 | Prędkość obrotu **produkcyjna** | Hz (32-bit) | BS2 |
| R1303, R1312 | Prędkości bazowania | Hz (32-bit) | BS2 |
| R1211 | Przyspieszenie/hamowanie osi | — | BS2 + M305 |
| R1209 | Creep bazowania | — | BS2 + M305 |
| R1221 | Offset bazy (Machine Zero) | 32-bit | BS2 + M305 + HOME |

## Statusy (PLC → HMI)

| Adres | Funkcja |
|-------|---------|
| S1–S3, S10–S13 | Stany maszyny |
| R100 | Licznik bieżącej partii |
| M470 | HOME_OK |
| M329 | Serwis aktywny (M320·S1·X0·/X4) |
| M330 | **Przezbrajanie** (= X4, styk NO kluczyka) |
| X4 | Kluczyk — pozycja **przezbrajania** |
| M403 | Pauza B3 |
| M431 / M536 | Obrót w toku / obrót przezbrajania |
| M530–M535, M539 | Alarmy / nastawy |
| D100, D102, R201 | Statystyki, czas cyklu |
| X0 | Bezpieczeństwo Pilz |

---

## Ekrany panelu

Zrzuty: [hmi/Zrzut ekranu 2026-06-11 184233.png](<../hmi/Zrzut ekranu 2026-06-11 184233.png>),
[hmi/Zrzut ekranu 2026-06-11 184312.png](<../hmi/Zrzut ekranu 2026-06-11 184312.png>).

### BS1 (RUN) — ekran główny

| Element | Powiązanie |
|---------|------------|
| Licznik `X / Y` | R100 / R6 (cel edytowalny) |
| START / STOP / RESET / HOME | M300–M302, M310 |
| Przycisk SERWIS → BS3 | Disable gdy X4=1 |
| Lampka PRZEBRAJANIE | M330 (= X4) |

### BS2 (SETUP) — nastawy procesu i serwo

Pełna specyfikacja: [hmi_wdrozenie.md](hmi_wdrozenie.md) §3.

### BS3 (SERWIS)

Wejście na ekran → **M320 ON**. Osłona zamknięta, klucz PRODUKCJA (X4=OFF).
R14, M340 jog, M341, M342 (+90°), HOME, zerowania.

### BS6 (PRZEBRAJANIE)

**Auto** gdy X4=ON (kluczyk). Instrukcja, M343/M344 (góra-dół / lewo-prawo),
jog M340, R11–R13.

### BS4 (ALARMY), BS5 (Screensaver)

Specyfikacja: [hmi_wdrozenie.md](hmi_wdrozenie.md) §6–7.

---

**© CNC Solutions — Michał Batorowicz**
