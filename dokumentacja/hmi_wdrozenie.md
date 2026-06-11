# Instrukcja wdrożenia HMI — FvDesigner

**Projekt:** [hmi/SKO - Program 1.fpj](../hmi/SKO%20-%20Program%201.fpj)
**Panel:** P2043NA / P2043EA (480×272, dotyk)
**PLC:** FATEK HB1-14MBJ25 — jednostka `@HB1`
**Program PLC:** wdrożyć najpierw [plc/propozycja_rozbudowy.md](plc/propozycja_rozbudowy.md)

Mapa adresów (skrót): [hmi.md](hmi.md).

---

## 0. Przed rozpoczęciem

1. **Kopia zapasowa:** `File → Save As` → `SKO - Program 1_przed_rozbudowa.fpj`.
2. **PLC online** z rozbudowanym programem (co najmniej adresy M300–M343, R6–R13, M530–M539).
3. W FvDesigner: `Project → Communication Setting` — sprawdź połączenie z `@HB1`
   (port COM / Ethernet jak na maszynie). Test: podgląd X0 na monitorze.
4. Format adresu w tym projekcie (widać na BS2): **`@HB1:R1221`** — stosuj ten sam
   wzorzec dla wszystkich nowych obiektów.

### Konwencja typów obiektów FvDesigner

| Typ obiektu | Skrót | Zastosowanie |
|-------------|-------|--------------|
| Bit Lamp | SL | Lampka statusu (odczyt ON/OFF) |
| Bit Button | BB | Przycisk zapisujący bit do PLC |
| Numeric Display / Input | ND | Odczyt lub edycja rejestru R/D |
| Screen Button | SB | Przejście między ekranami (bez adresu PLC) |
| Text | T | Etykiety statyczne |

### Konwencja akcji przycisków (Bit Button)

| Zachowanie PLC | Ustawienie Write w FvDesigner |
|----------------|-------------------------------|
| Zbocze narastające (`TU M300`) | **On Press = Set**, **On Release = Reset** (impuls) |
| Przełącznik (M420 ON/OFF) | **Toggle** lub Set/Reset z lampką |
| Jog — działa gdy trzymany (M340) | **On Press = Set**, **On Release = Reset** |
| Zerowanie (M311, M312) | **On Press = Set**, **On Release = Reset** |

---

## 1. Ekrany — lista docelowa

| Ekran | Nazwa | Dostęp | Akcja |
|-------|-------|--------|-------|
| BS1 | RUN | operator | **Istnieje** — uzupełnij |
| BS2 | SETUP | hasło serwis | **Istnieje** — rozbuduj |
| BS3 | SERWIS | hasło serwis | **Nowy** |
| BS4 | ALARMY | operator (auto przy S3) | **Nowy** |
| BS5 | Screensaver | — | bez zmian |
| Popup | Klawiatura numeryczna | — | bez zmian (podpięta pod ND) |

Nawigacja:

```
BS1 ──[SET]──► BS2 ──[Wstecz]──► BS1
BS1 ──[SERWIS]──► BS3 ──[Wstecz]──► BS1
BS1 ──[ALARM] lub auto S3 ──► BS4 ──[RESET/Wstecz]──► BS1
```

---

## 2. BS1 (RUN) — uzupełnienia

**Istniejące elementy** (zostaw, tylko zweryfikuj adresy):

| Element UI | Typ | Adres monitora | Uwagi |
|------------|-----|----------------|-------|
| Lampka READY | SL | `@HB1:S1` | ON=zielony |
| Lampka RUN | SL | `@HB1:S2` | ON=zielony |
| Lampka ALARM | SL | `@HB1:S3` | ON=czerwony, opcjonalnie miganie |
| Lampka HOME_OK | SL | `@HB1:M470` | ON=zielony |
| Licznik bieżący | ND Display | `@HB1:R100` | tylko odczyt, 0 miejsc |
| Licznik cel partii | ND Input | `@HB1:R6` | edycja, min=1 max=100, klawiatura popup |
| Separator „/" | Text | — | między R100 a R6 |
| Liczenie — lampka | SL | `@HB1:M420` | |
| Liczenie — przełącznik | BB Toggle | `@HB1:M420` | domyślnie ON przy starcie produkcji |
| Powietrze — lampka | SL | `@HB1:M421` | |
| Powietrze — przełącznik | BB Toggle | `@HB1:M421` | domyślnie ON |
| START | BB | `@HB1:M300` | impuls Set/Reset |
| STOP | BB | `@HB1:M301` | impuls lub Set (PLC trzyma do skasowania) |
| RESET | BB | `@HB1:M302` | impuls Set/Reset |
| HOME | BB | `@HB1:M310` | impuls Set/Reset; **Enable gdy S1=ON** |
| SET | SB | → BS2 | hasło opcjonalne |

**Nowe elementy do dodania:**

| Element UI | Typ | Adres | Położenie / styl |
|------------|-----|-------|------------------|
| „PAUZA B3" | SL + Text | `@HB1:M403` | pasek statusu, ON=żółty |
| „SERWIS" | SL | `@HB1:M320` | mała lampka, ON=pomarańcz |
| Partie łącznie | ND Display | `@HB1:D100` | etykieta „Partie:", tylko odczyt |
| Czas cyklu [s] | ND Display | `@HB1:R201` | etykieta „Cykl:"; **podziel wyświetlanie ÷10** lub opis „×0,1 s" |
| Krok cyklu (opcjonalnie) | Text dynamiczny / 4× SL | S10,S11,S12,S13 | który ON → tekst HOMING/LICZENIE/… |
| Przycisk SERWIS | SB | → BS3 | hasło serwis |
| Przycisk ALARMY | SB | → BS4 | widoczny gdy S3=ON (Visibility: S3=1) |

**Właściwości HOME (Bit Button M310):**

- Tab **Control** → Enable Condition: `@HB1:S1` = ON (tylko w READY).
- Opcjonalnie Disable gdy `@HB1:S2` = ON.

**Właściwości START (M300):**

- Enable: `@HB1:S1` AND `@HB1:M470` AND NOT `@HB1:S3` AND `@HB1:X0`
  (jeśli FvDesigner nie obsługuje wyrażeń — wystarczy obserwacja operatora;
  PLC i tak blokuje start).

---

## 3. BS2 (SETUP) — rozbudowa

Istniejące pola — **popraw etykiety** (zgodnie z PLC):

| Etykieta na ekranie | Adres (już jest) | Min | Max | Domyślnie |
|---------------------|------------------|-----|-----|-----------|
| Opóźnienie po partii [×0,01 s] | `@HB1:R7` | 0 | 30000 | 12 |
| Filtr czujnika B3 [×0,01 s] | `@HB1:R8` | 1 | 30000 | 12 |
| Offset bazy | `@HB1:R1221` | — | — | wg maszyny |

**Nowe pola** (Numeric Input, każde z klawiaturą popup jak istniejące ND):

| Etykieta | Adres | Typ | Min | Max | Domyślnie |
|----------|-------|-----|-----|-----|-----------|
| Ilość w partii [szt.] | `@HB1:R6` | 16-bit | 1 | 100 | 12 |
| Timeout bazowania [×0,1 s] | `@HB1:R9` | 16-bit | 50 | 6000 | 300 |
| Timeout obrotu [×0,1 s] | `@HB1:R10` | 16-bit | 20 | 6000 | 100 |
| Prędkość obrotu | `@HB1:R1403` | **32-bit INT** | 500 | 20000 | 9000 |
| Prędkość bazowania DRVZ | `@HB1:R1303` | **32-bit INT** | 500 | 10000 | 5000 |
| Prędkość dojazdu do 0 | `@HB1:R1312` | **32-bit INT** | 500 | 10000 | 5000 |
| Przyspieszenie / hamowanie | `@HB1:R1211` | 16-bit | 1000 | 60000 | 20000 |
| Creep bazowania | `@HB1:R1209` | 16-bit | 100 | 5000 | 2000 |

**Przycisk ZAPISZ PARAMETRY:**

| Właściwość | Wartość |
|------------|---------|
| Typ | Bit Button |
| Adres | `@HB1:M305` |
| Write | On Press = Set, On Release = Reset |
| Etykieta | „ZAPISZ PARAMETRY" |
| Enable | NOT `@HB1:M431` AND NOT `@HB1:M460` (oś stoi) |
| Tekst pomocy | „Wymagane po zmianie R1211, R1209, R1221" |

**Przycisk Wstecz** → BS1 (SB).

**Zabezpieczenie:** `Screen Properties → Password Level` = 2 (serwis) dla całego BS2.

---

## 4. BS3 (SERWIS) — nowy ekran

Utwórz: `Screen → New` → nazwa **BS3**, tytuł **SERWIS**.
Rozmiar i styl jak BS1 (ciemne tło, czcionka Tahoma/Arial).

### 4.1 Nagłówek i tryby

| Element | Typ | Adres | Uwagi |
|---------|-----|-------|-------|
| Tytuł | Text | — | „SERWIS" |
| TRYB SERWISOWY | BB Toggle + SL | `@HB1:M320` | Enable: `@HB1:S1` |
| Lampka serwis aktywny | SL | `@HB1:M329` | tylko odczyt (PLC ustawia) |
| TRYB PRZEBRAJANIA | BB Toggle + SL | `@HB1:M323` | Enable: M320=ON |
| Lampka przezbrajanie | SL | `@HB1:M330` | tylko odczyt |
| Komunikat | Text | — | „Przezbrajanie: kluczyk Pilz w SERWIS, osłona otwarta OK" |

### 4.2 Nastawy przezbrajania

| Etykieta | Adres | Typ | Min | Max | Domyślnie |
|----------|-------|-----|-----|-----|-----------|
| Prędkość obrotu przezbraj. | `@HB1:R11` | 32-bit | 50 | 2000 | 500 |
| Przyspieszenie przezbraj. | `@HB1:R12` | 16-bit | 10000 | 60000 | 60000 |
| Timeout przezbraj. [×0,1 s] | `@HB1:R13` | 16-bit | 100 | 3600 | 600 |

Enable pól R11–R13: `@HB1:M323` = ON.

### 4.3 Przyciski ruchu

| Etykieta | Adres | Typ Write | Enable |
|----------|-------|-----------|--------|
| TRANSPORT JOG | `@HB1:M340` | Set gdy trzymany / Reset gdy puszczony | M329=ON **AND** M323=OFF |
| PRZEDMUCH ręczny | `@HB1:M341` | Toggle | M329=ON |
| OBRÓT SERWIS +90° | `@HB1:M342` | impuls Set/Reset | M329=ON, M470=ON, M323=OFF, NOT M431 |
| OBRÓT PRZEBRAJANIA +90° | `@HB1:M343` | impuls Set/Reset | M330=ON, NOT M431 |
| HOME | `@HB1:M310` | impuls Set/Reset | S1=ON |
| Lampka ruch osi | `@HB1:M431` | SL (odczyt) | — |
| Lampka przezbr. w toku | `@HB1:M536` | SL (odczyt) | — |

### 4.4 Zerowania

| Etykieta | Adres | Write |
|----------|-------|-------|
| ZERUJ LICZNIK PARTII | `@HB1:M311` | impuls; Enable: NOT S2 |
| ZERUJ STATYSTYKI | `@HB1:M312` | impuls |

### 4.5 Podgląd diagnostyczny (dół ekranu)

Dwie kolumny małych lampek SL (etykieta + lampka):

| Etykieta | Adres |
|----------|-------|
| X0 Bezpieczeństwo | `@HB1:X0` |
| X1 B1 | `@HB1:X1` |
| X3 B3 | `@HB1:X3` |
| Y1 Transport | `@HB1:Y1` |
| Y4 Przedmuch | `@HB1:Y4` |

Numeric Display (tylko odczyt):

| Etykieta | Adres |
|----------|-------|
| Pozycja modułu | `@HB1:R1501` |
| Licznik C0 | `@HB1:R100` |
| Partie total | `@HB1:D100` |
| Sztuki total (32-bit) | `@HB1:D102` | typ ND 32-bit |

**Wstecz** → BS1 (SB). **Password Level** = 2.

---

## 5. BS4 (ALARMY) — nowy ekran

Utwórz **BS4**, tytuł **ALARMY**.

### Lampki przyczyn (SL, ON=czerwony)

| Komunikat | Adres | Priorytet wyświetlania |
|-----------|-------|------------------------|
| Bezpieczeństwo / E-stop / osłona | `@HB1:M535` | 1 |
| Timeout bazowania | `@HB1:M530` | 2 |
| Timeout obrotu | `@HB1:M531` | 3 |
| Błąd serwo — bazowanie | `@HB1:M532` | 4 |
| Błąd serwo — obrót | `@HB1:M533` | 5 |
| Błąd parametrów serwo | `@HB1:M534` | 6 |
| Nieprawidłowa nastawa (R6) | `@HB1:M539` | odwrócona lampka: OFF=gdy błąd* |

\* Dla M539: lampka **OFF** gdy nastawa zła — użyj SL z atrybutem Invert
  lub Text widoczny gdy `@HB1:S3` AND NOT `@HB1:M539`.

### Komunikaty tekstowe (Text, Visibility)

| Tekst | Warunek widoczności |
|-------|---------------------|
| „Wykonaj HOME przed startem" | `@HB1:S3` OFF AND `@HB1:M470` OFF |
| „Naciśnij RESET po usunięciu przyczyny" | `@HB1:S3` ON |

**RESET** — BB `@HB1:M302`, impuls, Enable `@HB1:X0`.

**Wstecz** → BS1 (SB).

### Auto-przejście na BS4 (opcjonalnie)

`Global Script` lub `Screen Control`:

- Gdy `@HB1:S3` przejdzie w ON → `Switch Screen BS4`.
- Po RESET i S3=OFF operator wraca ręcznie lub auto na BS1.

W FvDesigner: obiekt **Bit Lamp** S3 na BS1 z akcją **Screen Switch** ON → BS4
(alternatywa bez skryptów).

---

## 6. Klawiatura numeryczna (popup)

Istniejący ekran popup — podłącz do **wszystkich** nowych pól ND Input:

1. Zaznacz ND → Properties → **Keypad** → wybierz istniejący ekran klawiatury.
2. Dla 32-bit (R1403, R1303, R1312, R1221, R11, D102): ustaw **Data Type =
   32Bit-INT** (jak ND0002 Offset bazy na zrzucie).

---

## 7. Hasła i poziomy użytkownika

| Poziom | Ekrany | Hasło |
|--------|--------|-------|
| 0 (operator) | BS1, BS4, BS5 | brak |
| 2 (serwis) | BS2, BS3 | ustaw w `Project → User Password` |

Operator na BS1 nie widzi SETUP/SERWIS bez hasła.

---

## 8. Wgranie do panelu

1. `Project → Compile` — brak błędów.
2. Podłącz panel P2043 (USB / RS-232 / Ethernet — jak skonfigurowane).
3. `Online → Download Project to HMI`.
4. Restart panelu, sprawdź wersję ekranu startowego = BS1.

---

## 9. Testy HMI (po wgraniu PLC + panelu)

| # | Czynność | Oczekiwany wynik |
|---|----------|------------------|
| H1 | START na BS1 | S2=ON, lampka RUN |
| H2 | Edycja R6 na BS1 lub BS2 | wartość w PLC (F11) = wpisana |
| H3 | Toggle M420 OFF | C0 nie rośnie przy B1 |
| H4 | M305 na BS2 po zmianie R1211 | brak M468, parametr w PLC |
| H5 | BS3: M320 ON przy S1 | M329=ON, START zablokowany |
| H6 | BS3: M342 impuls | obrót modułu, M431 miga |
| H7 | BS3: M323+M343, R11=500 | obrót wyraźnie wolniejszy niż H6 |
| H8 | BS3: M323 ON → M342 disabled | przycisk szary / nie reaguje |
| H9 | Wymuszenie S3 (E-stop) | BS4 lub lampka ALARM, M535=ON |
| H10 | RESET na BS4 | S3=OFF, latch M530–M535 skasowane |
| H11 | M311 zeruj licznik | R100/C0=0 przy STOP |
| H12 | D100 rośnie po partiach | zgodnie z PLC R3 |

---

## 10. Checklist — szybkie odniesienie adresów

### HMI → PLC (zapis)

```
M300 START      M301 STOP       M302 RESET      M305 ZAPISZ PAR.
M310 HOME       M311 ZERUJ C0   M312 ZERUJ STAT.
M320 SERWIS     M323 PRZEZBR.   M329 (tylko PLC)
M340 JOG        M341 PRZEDMUCH  M342 OBRÓT SER.  M343 OBRÓT PRZEZBR.
M420 LICZENIE   M421 POWIETRZE
R6 R7 R8 R9 R10 R11 R12 R13
R1209 R1211 R1221 R1303 R1312 R1403
```

### PLC → HMI (odczyt)

```
S1 S2 S3 S10 S11 S12 S13
M403 M431 M460 M470 M529 M530–M535 M536 M539
X0 X1 X3 Y1 Y4
R100 R1501 R201
D100 D102
C0 (opcjonalnie zamiast R100)
```

---

## 11. Kolejność prac w FvDesigner (zalecana)

1. Zweryfikuj adresy na **BS1** (HOME odblokowany, M310 enable S1).
2. Rozbuduj **BS2** (nowe pola + M305).
3. Utwórz **BS4** (alarmy — działa od razu po PLC P3).
4. Utwórz **BS3** (serwis + przezbrajanie — po PLC R1–R4).
5. Uzupełnij **BS1** (pauza, statystyki, nawigacja).
6. Hasła, compile, download, testy H1–H12.

---

**© CNC Solutions — Michał Batorowicz**
