# Panel HMI — interfejs PLC ↔ HMI

**Panel:** FATEK P2043NA/P2043EA (4.3", dotykowy) | **Projekt:** [hmi/SKO - Program 1.fpj](<../hmi/SKO%20-%20Program%201.fpj>) (FvDesigner)

**Instrukcja wdrożenia:** [hmi_wdrozenie.md](hmi_wdrozenie.md)

---

## Trzy prędkości obrotu modułu (ustawienie **BS3 SERWIS**)

| Tryb | Rejestr | Typowo | Użycie |
|------|---------|--------|--------|
| **Produkcja** | R1403 | 9000 Hz | automat |
| **Serwis** | R14 | 4000 Hz | BS3, osłona zamknięta |
| **Przezbrajanie** | R11 | 500 Hz | BS6, klucz X4 |

Dodatkowo na BS3: R1303/R1312 (bazowanie), R12/R13 (przezbrajanie).

---

## Parametry procesowe

| Adres | Funkcja | Zakres | Gdzie |
|-------|---------|--------|-------|
| R6 | Ilość w partii | 1–20 szt. | **BS1** (klik w cel) |
| R7 | **Opóźnienie po zliczeniu** | 0–2 s | BS2 SETUP |
| R8 | Czas przejazdu słoika przy B3 | 0–5 s | BS2 SETUP |

**R7** — po zliczeniu R6 sztuk transport jedzie jeszcze ten czas, żeby ostatni słoik doszedł do gniazda modułu.

---

## Przyciski i statusy

Pełna tabela adresów M300–M344, S1–S13, alarmy M530–M535: [hmi_wdrozenie.md](hmi_wdrozenie.md) §11.

---

## Ekrany

| Ekran | Dostęp | Zawartość |
|-------|--------|-----------|
| **BS1** RUN | operator | produkcja, R6, START/STOP |
| **BS2** SETUP | hasło | R7, R8, R9/R10, offset R1221, M305 |
| **BS3** SERWIS | hasło | **wszystkie prędkości**, jog, M342 (R14) |
| **BS6** PRZEBRAJANIE | auto X4 | regulacja 4 tuneli (blachy), M343 (+90°), jog |
| **BS4** ALARMY | przy S3 | latch M530–M535 |

---

**© CNC Solutions — Michał Batorowicz**
