## Skrót procedur diagnostycznych

### Test HOME (N0010–N0012, N0076)

1. M80 ON → M25, T10 (80 s).
2. X3 ON → M82, R1501 = 0.
3. Brak X3 w 80 s → M504.

### Test obrotu 90°

HOME → 4× obrót → R1501: 0→90→180→270→0. Kalibracja **R1403**.

### Separacja B1

- **M22:** zliczanie X1 → C1.
- **M233:** kontrola pozycji X1/X2 → M501/M502.

### Timeouty

| Timer | Czas | Flaga |
|-------|------|-------|
| T5 | 300 s | M505 |
| T7 | 80 s | M506 |
| T10 | 80 s | M504 |

### Test B4 {#test-b4}

- X4 ON → blokada N0020/N0021; C1 bez resetu (po wdrożeniu A0).
- M1019/M1020 → M1050 symulacja.
- D204 — licznik aktywacji.

### Wartości referencyjne

- D200/D201 < 10/dzień — OK pozycjonowanie.
- D204 < 20/dzień — OK przepływ.
- R1500 stabilny 12–18 s.

---

# Instrukcja serwisanta
## VERTINO — STACJA OCZYSZCZANIA OPAKOWAŃ

**Dokument:** IS-VTN-001  
**Data:** Lipiec 2025  
**Dla:** Serwis techniczny i elektrycy  

---

## 🏭 PODSTAWOWE INFORMACJE

### **Przeznaczenie urządzenia**
Vertino to urządzenie do oczyszczania opakowań przed napełnianiem. Wykorzystuje moduł obrotowy z 4 pozycjami (0°/90°/180°/270°) do obsługi 4 partii jednocześnie. Oczyszczanie przez przedmuch w pozycji odwróconej (180°).

**Funkcja kontroli przepływu:** X4 TRANSPORTER_FULL kontroluje przepływ - pauzuje wprowadzanie nowych partii gdy transporter odbiorczy zapełniony.

> **📋 Pełna specyfikacja techniczna:** patrz `techniczna.md`

---

## 🔧 SPECYFIKACJA TECHNICZNA

### **Hardware - główne komponenty**
```
STEROWNIK: FATEK HB1-14MBJ25
├── Wejścia cyfrowe: X0-X7 (8 szt, 24V DC)
├── Wyjścia cyfrowe: Y0-Y5 (6 szt, NPN 0.5A)
├── Komunikacja: RS485 Modbus RTU
└── Zasilanie: 24V DC ±10%

HMI: P5043NB
├── Ekran: 4.3" TFT 480x272px
├── Komunikacja: Dedykowane złącze z PLC
└── Zasilanie: z PLC przez złącze

NAPĘDY:
├── M2+M3: 2x Beak SH-D08R (transportery)
├── M1: 1x SS86D + przekładnia 1:50 (moduł obrotowy)
└── Zasilanie napędów: 24V przez Pilz PNOZ X7

BEZPIECZEŃSTWO: Pilz PNOZ X7 774303
├── Kategoria: 3 (EN 954-1)
├── Wejścia: E-STOP + osłony
└── Wyjścia: zasilanie napędów + zaworu
```

### **Mapowanie I/O**
```
WEJŚCIA: 
X0=SAFETY (Pilz PNOZ X7), X1=RESET, X2=B1(liczenie+pozycja), 
X3=B2(wyjście), X4=TRANSPORTER_FULL(kontrola przepływu), 
X5=HOME, X6=SPARE_INPUT_1, X7=SPARE_INPUT_2

WYJŚCIA: 
Y0/Y1=Transport, Y2/Y3=Obrót, Y4=LED, Y5=Przedmuch
```

---

## 🔬 DIAGNOSTYKA

### **Kontrola statusu PLC**
```
PODSTAWOWE FLAGI PROCESU:
M1     = Status bezpieczeństwa (Pilz PNOZ X7)
M10    = System gotowy (wszystkie warunki OK)
M70    = Praca automatyczna (proces ciągły)
M82    = HOME wykonany (pozycja 0°)
M200   = Żądanie reset błędów

SEKWENCJA PROCESU OBROTOWEGO:
M21    = Start cyklu (wprowadzanie partii, blokowany przez M224)
M22    = Transport aktywny (liczenie opakowań)  
M23    = Stabilizacja pozycji (pauza po transporcie)
M233   = Stabilizacja zakończona (kontrola pozycji)
M24    = Pozycja OK (można obrócić)
M25    = Obrót aktywny (90°)

FLAGI BŁĘDÓW PROCESU:
M501   = Błąd pozycji wejścia (B1 aktywny podczas M233)
M502   = Błąd pozycji wyjścia (B2 aktywny podczas M233)
M503   = Błąd parametrów procesu (poza zakresem)
M504   = Błąd procedury HOME (timeout)
M505   = Timeout transportu (parametryzowany)
M506   = Timeout obrotu (parametryzowany)
M507   = Status transportera odbiorczego

FLAGI KONTROLI PRZEPŁYWU:
M224   = Transporter zapełniony (X4 po debouncing)
M507   = Status transportera dla HMI
M520   = Edge detection X4 (do licznika D204)
M522   = Flaga X4 aktywny (pomiar czasu zapełnienia)
```

### **Kontrola rejestrów**
```
GRUPA 1: PARAMETRY PODSTAWOWE (R1400-R1409):
R1400  = Opakowania w partii (1-10, default: 3)
R1401  = Prędkość transportu (50-500 Hz, default: 200)
R1402  = Prędkość obrotu (100-1000 Hz, default: 400)
R1403  = Impulsy 90° kalibracja (12400-12600, default: 12500)
R1404  = Typ opakowań (1-5, default: 1)
R1405-R1409 = Spare podstawowe

GRUPA 2: PARAMETRY ZAAWANSOWANE (R1410-R1419):
R1410  = Czas stabilizacji ms (100-500, default: 200)
R1411  = Pauza po obrocie ms (50-200, default: 100)
R1412  = Debouncing czujników ms (10-100, default: 50)
R1413  = Timeout transport s (20-60, default: 30)
R1414  = Timeout obrót s (5-15, default: 8)
R1415  = Timeout HOME s (5-20, default: 10)
R1416-R1419 = Spare zaawansowane

GRUPA 3: DIAGNOSTYKA PODSTAWOWA (R1500-R1507):
R1500  = Czas ostatniego cyklu [ms]
R1501  = Pozycja modułu [°] (0/90/180/270)
R1502  = Czas ostatniej sesji pracy [s]
R1503  = Średni czas cyklu (ostatnie 10) [ms]
R1504  = Najkrótszy cykl w sesji [ms]
R1505  = Najdłuższy cykl w sesji [ms]
R1506  = Liczba restartów HOME w sesji
R1507  = Status transportera (0=WOLNY, 1=ZAPEŁNIONY)

DIAGNOSTYKA X4:
R1508  = Czas ostatniego zapełnienia X4 [ms]
R1509  = Najdłuższy czas zapełnienia w dniu [ms]

LICZNIKI PROCESU:
C1     = Licznik opakowań bieżący (C1 vs R1400)
D100   = Licznik partii eksploatacyjny
H10    = Licznik czasu pracy [godz]

LICZNIKI BŁĘDÓW:
D200   = Błędy pozycji wejścia (przy M501)
D201   = Błędy pozycji wyjścia (przy M502)
D202   = Timeout transportu (przy M505)
D203   = Timeout obrotu (przy M506)
D204   = Aktywacje transportera X4 (przy M224)

WORK REGISTERS (KOMPAKTOWE):
R500-R507   = WR Transport AUTO
R508-R515   = WR Obrót 90°
R516-R523   = WR HOME
R524-R531   = WR Transport FWD ręczny
R532-R539   = WR Transport REV ręczny
R540-R547   = WR Obrót CW ręczny
R548-R555   = WR Obrót CCW ręczny
R556-R559   = Rezerwa WR

PROGRAMY FUN140:
R1100-R1108 = Transport AUTO → reference R1401
R1200-R1208 = Obrót 90° → reference R1402, R1403
R1300-R1308 = HOME (bez zmian)
```

---

## 🔍 PROCEDURY DIAGNOSTYCZNE

### **Test funkcji bazowych**

#### **TEST 1: Pozycjonowanie HOME**
```
PROCEDURA:
1. Monitor M82 (HOME status)
2. Force M80 = ON (żądanie HOME)
3. Sprawdź FUN140: EN=M80, SR=R1300, WR=R516
4. Monitor X5/M225 (czujnik HOME po debouncing R1412)
5. Sprawdź M82 = ON po zakończeniu
6. Sprawdź R1501 = 0 (pozycja modułu)

OCZEKIWANY REZULTAT:
- Moduł obraca się CCW (R1302=1) do czujnika X5
- Stop na X5 = ON (pozycja 0°)
- M82 = ON (HOME OK)
- R1501 = 0 (pozycja referencyjna)
- Timeout kontrolowany przez R1415 (10s default)

JEŚLI BŁĄD:
- Sprawdź program R1300-R1308 (MEND = FFFF)
- Sprawdź czujnik HOME X5 w pozycji 0°
- Sprawdź timeout R1415 (może być za krótki)
- Monitor R1506 (licznik restartów HOME)
```

#### **TEST 2: Obrót step-by-step 90°**
```
PROCEDURA RĘCZNA:
1. Wykonaj HOME (pozycja 0°, R1501=0)
2. Force M112 = ON (obrót CW ręczny)
3. Monitor FUN140: EN=M112, SR=R1210, WR=R540
4. Sprawdź pozycjonowanie: R1403 impulsów = 90°
5. Monitor R1501 po każdym obrocie

SPRAWDZENIE POZYCJI (z rejestrem R1501):
- START: 0° (GÓRA) - X5 aktywny, R1501=0
- Po R1403 imp.: 90° (BOK) - R1501=90
- Po 2×R1403 imp.: 180° (DÓŁ) - R1501=180, pozycja przedmuchu
- Po 3×R1403 imp.: 270° (BOK) - R1501=270
- Po 4×R1403 imp.: 0° (GÓRA) - X5 aktywny, R1501=0

KALIBRACJA:
- R1403 (impulsy 90°): dostrajaj w zakresie 12400-12600
- R1501: musi odpowiadać rzeczywistej pozycji
- Precyzja: ±0.5° dla systemu przemysłowego

JEŚLI BŁĄD:
- Kalibracja R1403 (±50-100 impulsów)
- Sprawdź Network 064 (aktualizacja R1501)
- Sprawdź sterownik SS86D (enkoder)
```

#### **TEST 3: Separacja funkcji B1 i B2**
```
PROCEDURA SEPARACJI FUNKCJI B1:

CZĘŚĆ A - FUNKCJA LICZENIA (podczas M22=ON):
1. Force M22 = ON (transport aktywny)
2. Symuluj opakowania na X2 (ON/OFF)
3. Monitor C1 (licznik) - zwiększa się do R1400
4. Sprawdź debouncing M220 (czas R1412)
5. Force M22 = OFF → liczenie zatrzymane

CZĘŚĆ B - FUNKCJA POZYCJI (podczas M233=ON):
1. Force M233 = ON (stabilizacja zakończona)
2. Test X2 = OFF, X3 = OFF → M24 = ON (bezpieczne)
3. Test X2 = ON → M501 = ON (błąd wejścia)
4. Test X3 = ON → M502 = ON (błąd wyjścia)
5. Monitor liczniki błędów D200/D201

KLUCZOWE SPRAWDZENIE:
- M22 i M233 NIE MOGĄ być aktywne jednocześnie
- Podczas M22: tylko liczenie, brak kontroli pozycji
- Podczas M233: tylko kontrola pozycji, brak liczenia
- Timing: T31 (R1410) → M233 po stabilizacji

JEŚLI BŁĄD:
- Sprawdź Network 019 (funkcja liczenia)
- Sprawdź Network 023 (funkcja pozycji)  
- Sprawdź Network 022 (flaga M233)
- Sprawdź timing stabilizacji R1410 (200ms default)
```

#### **TEST 4: Parametryzowane timeouty**
```
PROCEDURA TESTÓW TIMEOUT:

TEST TIMEOUT TRANSPORTU (R1413):
1. Sprawdź wartość R1413 (default 30s)
2. Force M21 = ON, M22 = ON (transport aktywny)
3. Nie symuluj czujnika B1 → C1 nie rośnie
4. Po R1413 sekund → T30 → M505 = ON
5. Sprawdź D202++ (licznik timeout)

TEST TIMEOUT OBROTU (R1414):
1. Sprawdź wartość R1414 (default 8s)
2. Force M24 = ON, M25 = ON (obrót aktywny)
3. Nie force M1992 → obrót nie kończy się
4. Po R1414 sekund → T32 → M506 = ON
5. Sprawdź D203++ (licznik timeout)

TEST TIMEOUT HOME (R1415):
1. Sprawdź wartość R1415 (default 10s)
2. Force M80 = ON (HOME)
3. Nie aktywuj X5 → HOME nie kończy się
4. Po R1415 sekund → T35 → M504 = ON
5. Sprawdź R1506++ (restarty HOME)

DOSTRAJANIE PARAMETRÓW:
- R1413: zwiększ dla ciężkich opakowań
- R1414: zwiększ dla dużych modułów
- R1415: zwiększ dla wolnych mechanizmów HOME
- Monitor D202-D203 dla optymalizacji wartości
```

#### **TEST 5: Parametryzowany debouncing**
```
PROCEDURA TESTÓW DEBOUNCING (R1412):

TEST PARAMETRU:
1. Sprawdź wartość R1412 (default 50ms)
2. Symuluj szybkie impulsy na X2 (B1)
3. Monitor M220 po czasie R1412
4. Test dla wszystkich czujników X2, X3, X4, X5

SPRAWDZENIE WSZYSTKICH CZUJNIKÓW:
- X2 → T36/T37 → M220 (B1 liczenie+pozycja)
- X3 → T38/T39 → M221 (B2 zabezpieczenie wyjścia)
- X4 → T40/T41 → M224 (TRANSPORTER_FULL)
- X5 → T42/T43 → M225 (HOME pozycja 0°)

OPTYMALIZACJA:
- R1412 za mało → false triggers od drgań
- R1412 za dużo → slow response, missed signals
- Optimal range: 30-70ms dla czujników indukcyjnych
- Test różnych wartości: 10ms, 50ms, 100ms

PRAKTYCZNE ZASTOSOWANIE:
- Czyste środowisko → R1412 = 30ms
- Wibracje mechaniczne → R1412 = 70ms
- Szybka produkcja → balans response/stability
```

#### **TEST 6: Czujnik transportera X4**
```
PROCEDURA TESTÓW X4 TRANSPORTER_FULL:

CZĘŚĆ A - FUNKCJA PODSTAWOWA:
1. Sprawdź pozycjonowanie czujnika X4 nad transporterem odbiorczym
2. Symuluj zapełnienie transportera → X4 = ON
3. Monitor debouncing: X4 → T40 (R1412) → M224 = ON
4. Sprawdź blokadę procesu: M224 = ON → M21 nie może być aktywne
5. Opróżnij transporter → X4 = OFF → M224 = OFF → proces możliwy

CZĘŚĆ B - DIAGNOSTYKA:
1. Monitor flagi M507 (status dla HMI)
2. Sprawdź licznik D204 (aktywacje X4)
3. Monitor czas zapełnienia T54 → R1508
4. Sprawdź najdłuższy czas R1509 (tracking)

CZĘŚĆ C - TEST RĘCZNY Z HMI:
1. Force M1019 = ON → M224 = ON (symulacja zapełnienia)
2. Sprawdź blokadę start cyklu (M21 niemożliwy)
3. Force M1020 = ON → M224 = OFF (reset symulacji)
4. Sprawdź odblokowanie procesu

KALIBRACJA X4:
1. Pozycjonowanie: 2-4mm nad transporterem odbiorczym
2. Test aktywacji przy różnych poziomach zapełnienia
3. Dostrojenie czułości czujnika indukcyjnego
4. Weryfikacja debouncing (R1412 = 50ms default)

ANALIZA DIAGNOSTYCZNA:
- D204: liczba aktywacji dziennie (norma <50)
- R1508: czas ostatniego zapełnienia (norma <30s)
- R1509: najdłuższy czas w dniu (analiza trendów)
- Częste aktywacje → problem z odbiorem lub przepływem

JEŚLI BŁĄD:
- Sprawdź Network 031 (debouncing X4)
- Sprawdź Network 016 (blokada start cyklu)
- Sprawdź Network 055A (licznik D204)
- Sprawdź Network 066-067 (monitoring rozszerzony)
- Sprawdź pozycjonowanie czujnika X4
```

---

## 🛠️ PROCEDURY SERWISOWE

### **Kalibracja modułu**
```
PROCEDURA KOMPLETNEJ KALIBRACJI:

1. PRZYGOTOWANIE:
   - Zatrzymaj system (E-STOP)
   - Usuń wszystkie opakowania
   - Sprawdź swobodę obrotu
   - Sprawdź pozycjonowanie X4 nad transporterem odbiorczym

2. KALIBRACJA MECHANICZNA:
   - Ustaw moduł wizualnie w pozycji 0°
   - Sprawdź czy X5 = ON
   - Dostraj pozycję czujnika X5 ±0.5°

3. KALIBRACJA ELEKTRONICZNA:
   - HOME → R1501 = 0
   - Test: 4 × R1403 impulsów
   - Monitor R1501: 0 → 90 → 180 → 270 → 0
   - Po 4×R1403 impulsów: X5 = ON i R1501 = 0

4. DOSTRAJANIE R1403:
   - Start z R1403 = 12500
   - Test 10x pełny obrót
   - Sprawdź czy zawsze powrót do X5 = ON
   - Adjust R1403 ±50-100 jeśli błąd
   - Tolerancja: ±0.2° (±28 impulsów)

5. WERYFIKACJA FUNKCJI:
   - Test separacji B1 (liczenie vs pozycja)
   - Test czujnika B2 (zabezpieczenie wyjścia)
   - Test czujnika X4 (kontrola przepływu)
   - Test parametrów R1410-R1415
   - Test podstawowej diagnostyki R1500-R1507
```

### **Wymiana czujnika B1**
```
POZYCJONOWANIE:
- Odległość: 2-4mm od opakowań
- Pozycja: wejście do modułu (0°)
- Typ: PNP, M18x1, NO, 24V DC

PROCEDURA WYMIANY:
1. Oznacz dokładną pozycję starego czujnika
2. Wymień na identyczny typ
3. Test funkcji liczenia:
   - Force M22 = ON → symuluj opakowania → C1++
4. Test funkcji pozycji:
   - Force M233 = ON → X2 = OFF → M24 = ON
   - Force M233 = ON → X2 = ON → M501 = ON

KALIBRACJA POZYCJI:
- Transportuj opakowania do pozycji stop
- Zatrzymaj (M22 = OFF)
- Stabilizacja (R1410 ms) → M233 = ON
- Czujnik powinien być OFF (pozycja OK)
- Jeśli ON: przesuń czujnik dalej od stop

VERYFIKACJA:
- M22 i M233 nie nakładają się
- Debouncing R1412 działa poprawnie
- Separacja funkcji działa
```

### **Wymiana czujnika X4**
```
POZYCJONOWANIE X4 TRANSPORTER_FULL:
- Odległość: 2-4mm nad transporterem odbiorczym
- Pozycja: koniec transportera wyjściowego z maszyny
- Typ: PNP, M18x1, NO, 24V DC
- Montaż: uchwyt regulowany w osi Z

PROCEDURA WYMIANY:
1. Oznacz dokładną pozycję starego czujnika X4
2. Wymień na identyczny typ (PNP M18)
3. Test funkcji kontroli przepływu:
   - Symuluj zapełnienie → X4 = ON → M224 = ON
   - Sprawdź blokadę M21 (start cyklu niemożliwy)
   - Usuń zapełnienie → X4 = OFF → M224 = OFF

KALIBRACJA X4:
1. Ustaw transporter odbiorczy w pozycji normalnej (pusty)
2. X4 = OFF → M224 = OFF (transporter wolny)
3. Dodaj opakowania do transportera odbiorczego
4. W momencie zapełnienia → X4 = ON → M224 = ON
5. Dostraj pozycję czujnika dla właściwego triggering

WERYFIKACJA:
- Debouncing T40/T41 → M224 działa (R1412)
- Blokada start cyklu przy M224 = ON
- Licznik D204 zlicza aktywacje
- Status M507 dla HMI aktywny
- Test ręczny M1019/M1020 z HMI

OPTYMALIZACJA:
- Pozycja dla wczesnego wykrycia zapełnienia
- Unikanie false triggers od pojedynczych opakowań
- Stabilne triggering przy pełnym zapełnieniu
```

### **Konserwacja modułu**
```
HARMONOGRAM MIESIĘCZNY:
☐ Analiza czasów cykli (R1503 vs baseline)
☐ Check błędów pozycji (D200/D201 trends)
☐ Analiza restartów HOME (R1506 frequency)
☐ Test dokładności pozycji (R1501 vs rzeczywista)
☐ Optymalizacja parametrów R1410-R1415
☐ Kalibracja debouncing R1412
☐ Performance review (R1504/R1505 consistency)
☐ Analiza aktywacji X4 (D204 frequency)
☐ Kontrola przepływu X4 (R1508/R1509 trends)

HARMONOGRAM KWARTALNY:
☐ Pełna kalibracja R1403 (impulsy 90°)
☐ Analiza trendów R1500-R1509
☐ Optymalizacja wszystkich parametrów
☐ Test powtarzalności pozycjonowania
☐ Sprawdzenie Work Registers efficiency
☐ Update baseline values
☐ Analiza efektywności X4 (zapobieganie przepełnieniu)
☐ Optymalizacja pozycji czujnika X4

WSKAŹNIKI WYDAJNOŚCI:
- R1503 stabilny → proces powtarzalny
- R1504/R1505 różnica < 3s → consistent performance
- R1506 < 5/miesiąc → good positioning quality
- D200-D203 < 10/miesiąc → proper tuning
- D204 < 50/miesiąc → proper X4 flow control
- R1508 < 30s → efficient transporter clearing

WSKAŹNIKI ALARMOWE:
- D204 > 100/dzień → problem z odbiorem lub przepływem
- R1508 > 60s → wolne opróżnianie transportera
- R1509 rośnie → pogorszenie przepływu
```

### **Konfiguracja HMI**
```
EKRAN GŁÓWNY:
- Partia: C1 / R1400
- Pozycja modułu: R1501 (0°/90°/180°/270°)
- Czas cyklu: R1500 [ms]
- Średni: R1503 [ms]
- Min/Max: R1504/R1505 [ms]
- Status transportera: R1507 (0=WOLNY, 1=ZAPEŁNIONY)

EKRAN PARAMETRÓW:
- Podstawowe: R1400-R1404
- Zaawansowane: R1410-R1415 (serwis Level 2)

EKRAN DIAGNOSTYKI:
- Wydajność: R1500-R1507
- Błędy: D200-D203
- Aktywacje X4: D204
- Pozycja: R1501 accuracy
- Restarty: R1506 frequency
- X4 timing: R1508/R1509

EKRAN RĘCZNY:
- Test X4: M1019 (ON) / M1020 (OFF)
- Status X4: M224, M507
- Reset liczników: M1021
```

---

## 📊 PARAMETRY FABRYCZNE

### **Wartości domyślne**
```
GRUPA 1 (R1400-R1409):
R1400 = 3      (opakowania)
R1401 = 200    (transport Hz)
R1402 = 400    (obrót Hz)  
R1403 = 12500  (kalibracja 90°)
R1404 = 1      (typ opakowań)
R1405-R1409 = 0 (spare podstawowe)

GRUPA 2 (R1410-R1419):
R1410 = 200    (stabilizacja ms)
R1411 = 100    (pauza ms) 
R1412 = 50     (debouncing ms)
R1413 = 30     (timeout transport s)
R1414 = 8      (timeout obrót s)
R1415 = 10     (timeout HOME s)
R1416-R1419 = 0 (spare zaawansowane)

GRUPA 3 (R1500-R1507):
R1500-R1507 = 0 (auto-update diagnostics)
```

---

## 📞 WSPARCIE TECHNICZNE

### **Informacje do zgłoszenia**
```
PARAMETRY BIEŻĄCE:
- R1400-R1404 (podstawowe)
- R1410-R1415 (zaawansowane)

DIAGNOSTYKA:
- R1500 (czas ostatniego cyklu)
- R1501 (pozycja modułu)
- R1503 (średni czas)
- R1506 (restarty HOME)
- R1507 (status transportera)

DIAGNOSTYKA X4:
- D204 (liczba aktywacji X4 dziennie)
- R1508 (czas ostatniego zapełnienia)
- R1509 (najdłuższy czas zapełnienia)

LICZNIKI BŁĘDÓW:
- D200-D204 (częstotliwość problemów)

ANALIZA WYDAJNOŚCI:
- R1503 vs expected (baseline)
- R1504/R1505 consistency
- R1506 frequency (quality indicator)
- D200-D204 trends (system health)
- X4 flow control efficiency (D204 analysis)

PRIORYTET:
- Wysoki: R1506 > 10/dzień, R1501 inaccurate, D204 > 100/dzień
- Średni: R1503 > 20s, frequent timeouts, R1508 > 60s
- Niski: parameter tuning, optimization
```

### **Typowe problemy X4**
```
PROBLEM: Częste aktywacje X4 (D204 > 100/dzień)
PRZYCZYNY:
- Wolny odbiór z transportera odbiorczego
- Nieprawidłowa pozycja czujnika X4
- Za czuły czujnik (false triggers)
ROZWIĄZANIE:
- Sprawdź przepływ na transporcie odbiorczym
- Zweryfikuj pozycjonowanie X4
- Dostraj debouncing R1412

PROBLEM: Długie zapełnienia (R1508 > 60s)
PRZYCZYNY:
- Zapchanie transportera odbiorczego
- Wolny proces odbiorczy
- Problem z czujnikiem X4
ROZWIĄZANIE:
- Sprawdź mechanikę transportera odbiorczego
- Zweryfikuj proces odbiorczy
- Test czujnika X4 (M1019/M1020)

PROBLEM: X4 nie blokuje procesu
PRZYCZYNY:
- Uszkodzony czujnik X4
- Błąd w debouncing (T40/T41)
- Problem z Network 016
ROZWIĄZANIE:
- Test X4 → M224 → blokada M21
- Sprawdź debouncing R1412
- Weryfikuj program PLC Network 016
```

---

**© 2025 - Instrukcja serwisanta Vertino - CNC Solutions Michał Batorowicz**