# DOKUMENTACJA TECHNICZNA PRODUCENTA
## VERTINO — STACJA OCZYSZCZANIA OPAKOWAŃ
### **DOKUMENT WEWNĘTRZNY - POZIOM DOSTĘPU: PRODUCENT/SERWIS LEVEL 3**

---

**Numer seryjny maszyny:** VERTINO-MO-2025-___________  
**Data wydania:** Lipiec 2025  
**Klasyfikacja:** POUFNE - tylko autoryzowany personel  

---

## 📋 **CHARAKTERYSTYKA MASZYNY**

### **Przeznaczenie urządzenia**
Vertino (stacja oczyszczania opakowań) jest urządzeniem do oczyszczania opakowań przed procesem napełniania. Maszyna usuwa zanieczyszczenia stałe mogące znajdować się wewnątrz opakowań po procesach transportu, przechowywania i przygotowania.

Proces oczyszczania realizowany jest poprzez obrócenie opakowań do pozycji odwróconej (180°) i intensywny przedmuch sprężonym powietrzem. Wykorzystanie siły grawitacji zapewnia skuteczne usunięcie zanieczyszczeń z wnętrza opakowań.

**Funkcja kontroli przepływu:** Automatyczna kontrola przepływu poprzez czujnik X4 TRANSPORTER_FULL, który pauzuje wprowadzanie nowych partii gdy transporter odbiorczy jest zapełniony, zapobiegając przepełnieniu i stratom produktu.

Urządzenie stanowi element linii technologicznej, zapewniając odpowiednią jakość opakowań przed dalszymi etapami procesu produkcyjnego oraz optymalny przepływ materiału.

### **Charakterystyka konstrukcyjna**
Vertino (stacja oczyszczania opakowań) jest maszyną ciągłego działania wyposażoną w moduł obrotowy z czterema pozycjami roboczymi rozmieszczonymi co 90°. Urządzenie umożliwia równoczesną obsługę czterech partii opakowań w różnych fazach procesu oczyszczania.

**Konstrukcja modułu obrotowego:**
- **Pozycja 0° (GÓRA):** wejście nowej partii / wyjście oczyszczonej
- **Pozycje 90° i 270° (BOK):** pozycje transportowe
- **Pozycja 180° (DÓŁ):** pozycja oczyszczania (przedmuch)

**Proces technologiczny:** step-by-step - każda partia opakowań przechodzi kompletny cykl 360° przez wszystkie cztery pozycje. Oczyszczanie odbywa się w pozycji odwróconej (180°) poprzez intensywny przedmuch sprężonym powietrzem.

**Kontrola przepływu:** Czujnik X4 TRANSPORTER_FULL monitoruje stan transportera odbiorczego i automatycznie wstrzymuje wprowadzanie nowych partii przy zapełnieniu, pozwalając na dokończenie przetwarzania już wprowadzonych partii.

### **Proces technologiczny step-by-step z kontrolą przepływu**
**Pełny cykl partii (360° przez wszystkie pozycje) z X4:**
1. **Kontrola przepływu** - sprawdzenie X4 (transporter odbiorczy wolny)
2. **Wprowadzanie** - transportery M2+M3 wprowadzają grupę opakowań (1-10 sztuk na partię - parametr konfigurowalny)
3. **Liczenie** - czujnik B1 liczy każde opakowanie podczas ruchu transporterów
4. **Stop automatyczny** - po naliczeniu wymaganej ilości → transportery zatrzymują się automatycznie
5. **Stabilizacja pozycji** - 2 sekundy (eliminacja drgań mechanicznych)
6. **Kontrola bezpieczeństwa** - czujnik B1 sprawdza strefę wejścia, czujnik B2 strefę wyjścia
7. **Obrót** - dopiero gdy obie strefy bezpieczne → moduł obrotowy obraca się dokładnie o 90°
8. **Kontynuacja** - automatyczny powrót do wprowadzania następnej partii (jeśli X4 pozwala)

**Parametry procesu:**
- **Partia:** 1-10 opakowań (konfigurowalny)
- **Pozycjonowanie:** dokładnie 90° (kalibrowane mechanicznie i elektronicznie)
- **Prędkość transporterów:** 50-500 Hz (konfigurowalny)
- **Prędkość modułu obrotowego:** 100-1000 Hz (konfigurowalny)
- **Typowy czas cyklu:** 12-18 sekund
- **Kontrola przepływu:** automatyczna pauza/wznowienie (X4)

**Charakterystyka ciągłości procesu z kontrolą przepływu:**
- **4 partie jednocześnie** w różnych fazach cyklu
- **Ciągły przedmuch:** zawsze jedna partia w pozycji odwróconej (180°)
- **Synchronizacja wprowadzania:** nowa partia wypycha przetworzoną (jeśli X4 pozwala)
- **Inteligentna pauza:** proces wstrzymuje wprowadzanie przy zapełnieniu transportera odbiorczego
- **Kontynuacja przetwarzania:** już wprowadzone partie kończą cykl mimo pauzy X4
- **Automatyczne wznowienie:** proces wraca do normy gdy X4 się wyłączy

**System zabezpieczeń:**
- **Pilz PNOZ X7 774303** (kategoria 3, fizyczne odcięcie zasilania napędów)
- **Potrójne czujniki kontroli pozycji:** B1 (wejście), B2 (wyjście), X4 (przepływ)
- **System timeoutów:** 30s transportery, 8s moduł obrotowy, 10s procedura HOME
- **Zabezpieczenie przed kolizją:** kontrola wszystkich stref przed każdym obrotem
- **Kontrola przepływu:** zapobieganie przepełnieniu transportera odbiorczego

---

## 🔧 **SPECYFIKACJA TECHNICZNA FABRYCZNA**

### **System sterowania**
```
PLC: FATEK HB1-14MBJ25
├── Firmware: v3.2 lub nowszy
├── Wejścia cyfrowe: X0-X7 (24V DC, PNP, Sink/Source)
├── Wyjścia cyfrowe: Y0-Y5 (24V DC, NPN, 0.5A)
├── Komunikacja: RS485 Modbus RTU (adres: 1)
├── Programowanie: WinProLadder v3.30 lub nowszy
└── Parametry komunikacji: 9600,8N1,Even

HMI: P5043NB  
├── Ekran: 4.3" TFT, 480x272px, 65k kolorów
├── Komunikacja: Dedykowane złącze FATEK native
├── Programowanie: FvDesigner v1.65 lub nowszy  
├── Adres PLC: 1 (auto-detect)
└── Zasilanie: z PLC przez złącze komunikacyjne
```

### **Mapowanie I/O**
```
WEJŚCIA CYFROWE (24V DC, PNP):
X0 = SAFETY_STATUS    (Pilz PNOZ X7 13/14)
X1 = BUTTON_RESET     (Przycisk RESET, NO)  
X2 = SENSOR_B1        (Liczenie + pozycja, PNP M18, podwójna funkcja)
X3 = SENSOR_B2        (Zabezpieczenie wyjścia, PNP M18)
X4 = TRANSPORTER_FULL (Kontrola przepływu, PNP M18)
X5 = SENSOR_HOME      (Czujnik HOME 0°, PNP M18)
X6 = SPARE_INPUT_1    (Rezerwa, PNP M18)
X7 = SPARE_INPUT_2    (Rezerwa, PNP M18)

WYJŚCIA CYFROWE (24V DC, NPN, 0.5A):
Y0 = TRANSPORT_PULSE  (Sterowniki M2+M3, do 200kHz)
Y1 = TRANSPORT_DIR    (Sterowniki M2+M3, kierunek)
Y2 = ROTATION_PULSE   (Sterownik M1, do 200kHz)  
Y3 = ROTATION_DIR     (Sterownik M1, kierunek)
Y4 = STATUS_LED       (Lampka sygnalizacyjna)
Y5 = PNEUMATIC_VALVE  (Przedmuch pneumatyczny)
```

---

## 📊 **PARAMETRY FABRYCZNE**

### **GRUPA 1: PARAMETRY PODSTAWOWE (R1400-R1409)**
```
R1400 = 3      [1-10]     Opakowania w partii
R1401 = 200    [50-500]   Prędkość transportu [Hz]
R1402 = 400    [100-1000] Prędkość obrotu [Hz]  
R1403 = 12500  [12400-12600] Impulsy 90° (kalibracja)
R1404 = 1      [1-5]      Typ opakowań (różne profile)
R1405-R1409 = 0           Rezerwa podstawowych funkcji
```

### **GRUPA 2: PARAMETRY ZAAWANSOWANE (R1410-R1419)**
```
R1410 = 200    [100-500]  Czas stabilizacji [ms]
R1411 = 100    [50-200]   Pauza po obrocie [ms] 
R1412 = 50     [10-100]   Debouncing czujników [ms] (w tym X4)
R1413 = 30     [20-60]    Timeout transport [s]
R1414 = 8      [5-15]     Timeout obrót [s]
R1415 = 10     [5-20]     Timeout HOME [s]
R1416-R1419 = 0          Rezerwa zaawansowanych funkcji
```

### **GRUPA 3: DIAGNOSTYKA PODSTAWOWA (R1500-R1507)**
```
R1500 = 0      Czas ostatniego cyklu [ms]
R1501 = 0      Pozycja modułu [°] (0/90/180/270)
R1502 = 0      Czas ostatniej sesji [s]
R1503 = 0      Średni czas z ostatnich 10 cykli [ms]
R1504 = 9999   Najkrótszy cykl w sesji [ms]
R1505 = 0      Najdłuższy cykl w sesji [ms]
R1506 = 0      Liczba restartów HOME w sesji
R1507 = 0      Status transportera (0=WOLNY, 1=ZAPEŁNIONY)
R1508-R1519 = 0  Rezerwa dostępnych rozszerzeń
```

### **GRUPA 4: WORK REGISTERS (R500-R559)**
```
R500-R507   = WR Transport AUTO
R508-R515   = WR Obrót 90°
R516-R523   = WR HOME
R524-R531   = WR Transport FWD ręczny
R532-R539   = WR Transport REV ręczny
R540-R547   = WR Obrót CW ręczny
R548-R555   = WR Obrót CCW ręczny
R556-R559   = Rezerwa WR
```

### **GRUPA 5: LICZNIKI DIAGNOSTYCZNE**
```
LICZNIKI PODSTAWOWE:
C1     = Licznik opakowań bieżący
D100   = Licznik partii eksploatacyjny
H10    = Licznik czasu pracy [godz]

LICZNIKI BŁĘDÓW:
D200   = Błędy pozycji wejścia (przy M501)
D201   = Błędy pozycji wyjścia (przy M502)
D202   = Timeout transportu (przy M505)
D203   = Timeout obrotu (przy M506)
D204   = Aktywacje transportera X4 (przy M224)
```

---

## 💾 **PROGRAM PLC - NETWORKS**

### **Struktura programu**
```
TOTAL NETWORKS: 67
SCAN TIME: ~9ms

Networks 001-005: Bezpieczeństwo i system (Pilz PNOZ X7)
Networks 006-015: Procedura HOME
Networks 016-035: Główny proces obrotowy z kontrolą X4
Networks 036-045: Tryb ręczny z testem X4
Networks 046-055: Sygnalizacja i diagnostyka z X4
Networks 056-067: Liczniki i monitoring rozszerzone
```

### **Kluczowe Networks**

#### **NETWORK 001: Wejście bezpieczeństwa**
```ladder
|--[X0]--( SET M1 )--|         // Pilz PNOZ X7 aktywny
|--[/X0]--( RST M1 )--|        // Bezpieczeństwo OFF
```

#### **NETWORK 016: Start cyklu z kontrolą X4**
```ladder
|--[M70]--[M10]--[/M21]--[/M22]--[/M23]--[/M24]--[/M25]--[/M224]--+
|                                                     ( SET M21 )--|
// Warunek [/M224] - blokada gdy transporter zapełniony
```

#### **NETWORK 017A: Status transportera odbiorczego**
```ladder
|--[M224]--( SET M507 )--|          // Transporter zapełniony
|--[/M224]--( RST M507 )--|         // Transporter wolny
```

#### **NETWORK 031: Debouncing rozszerzony**
```ladder
// Wszystkie debouncing z parametru R1412, w tym X4
|--[X2]--( T 36 R1412 )--|     |--[T36]--( SET M220 )--|
|--[/X2]--( T 37 R1412 )--|    |--[T37]--( RST M220 )--|
|--[X3]--( T 38 R1412 )--|     |--[T38]--( SET M221 )--|
|--[/X3]--( T 39 R1412 )--|    |--[T39]--( RST M221 )--|
|--[X4]--( T 40 R1412 )--|     |--[T40]--( SET M224 )--|
|--[/X4]--( T 41 R1412 )--|    |--[T41]--( RST M224 )--|
|--[X5]--( T 42 R1412 )--|     |--[T42]--( SET M225 )--|
|--[/X5]--( T 43 R1412 )--|    |--[T43]--( RST M225 )--|
```

#### **NETWORK 045A: Test X4 ręczny**
```ladder
|--[M1019]--[M100]--( SET M224 )--|     // Symulacja X4
|--[M1020]--[M100]--( RST M224 )--|     // Reset X4
```

#### **NETWORK 055A: Licznik aktywacji X4**
```ladder
|--[M224]--[/M520]--+--( SET M520 )--|   // Edge detection
|                   |--( INC D204 )--|   // Licznik X4
|--[/M224]--( RST M520 )--|
```

#### **NETWORK 065A: Status transportera**
```ladder
|--[M224]--( MOV K1 R1507 )--|          // Zapełniony
|--[/M224]--( MOV K0 R1507 )--|         // Wolny
```

#### **NETWORK 066: Monitoring X4 extended**
```ladder
|--[M224]--[/M522]--+--( SET M522 )--|   // X4 aktywny
|                   |--( T 54 K0 )--|   // Czas zapełnienia
|--[/M224]--+--( RST M522 )--|
|           |--( MOV T54 R1508 )--|     // Czas ostatniego
|           |--( RST T54 )--|
```

#### **NETWORK 067: Diagnostyka X4 zaawansowana**
```ladder
|--[M8000]--( MOV K0 R1508 )--|         // Reset dzienny
|--[M224]--[T54]--[> T54 R1509]--( MOV T54 R1509 )--|
// R1509 = najdłuższy czas zapełnienia w dniu
```

---

## 💻 **PROGRAMY FUN140**

### **Transport AUTO (R1100-R1108)**
```
R1100 = R1401    // Prędkość z parametru
R1101 = 0        // Ciągły
R1102 = 0        // CW
R1103 = 50       // Start freq
R1104 = 50       // Stop freq
R1105 = 100      // Accel time
R1106 = 100      // Decel time
R1107 = 0        // FUN142 control
R1108 = FFFF     // MEND
```

### **Obrót 90° (R1200-R1208)**
```
R1200 = R1402    // Prędkość z parametru
R1201 = R1403    // Impulsy z kalibracji
R1202 = 0        // CW
R1203 = 100      // Start freq
R1204 = 100      // Stop freq
R1205 = 200      // Accel time
R1206 = 200      // Decel time
R1207 = 0        // Pulse count mode
R1208 = FFFF     // MEND
```

### **HOME (R1300-R1308)**
```
R1300 = 100      // HOME speed
R1301 = 0        // Ciągły
R1302 = 1        // CCW (powrót)
R1303 = 50       // Start freq
R1304 = 50       // Stop freq
R1305 = 200      // Accel time
R1306 = 200      // Decel time
R1307 = 1        // Sensor stop (X5)
R1308 = FFFF     // MEND
```

---

## 🖥️ **PROJEKT HMI**

### **EKRAN 1 - GŁÓWNY**
```
┌─────────────────────────────────────┐
│  STACJA KONTROLI OPAKOWAŃ           │
│                                     │
│  Status: [System OK / Błąd]         │
│  Pozycja modułu: [0°/90°/180°/270°] │
│  Partia: [C1] / [R1400]             │
│  Transporter: [WOLNY/ZAPEŁNIONY]    │
│                                     │
│  [START] [STOP] [RESET] [PARAMETRY] │
│                                     │
│  Czas cyklu: R1500 [ms]             │
│  Średni: R1503 [ms]                 │
│  Min/Max: R1504/R1505 [ms]          │
│  Łącznie partii: D100               │
│                                     │
│  Błędy dziś: D200/D201 (wej/wyj)    │
│  Timeouty: D202/D203 (trans/obrót)  │
│  Aktywacje X4: D204 (dziś)          │
└─────────────────────────────────────┘
```

### **EKRAN 2 - PARAMETRY**
```
┌─────────────────────────────────────┐
│ PARAMETRY PROCESU                   │
│                                     │
│ Opakowania w partii: R1400 [1-10]   │
│ Prędkość transportu: R1401 [50-500] │
│ Prędkość obrotu: R1402 [100-1000]   │
│ Typ opakowań: R1404 [1-5]           │
│                                     │
│ ZAAWANSOWANE (serwis):              │
│ Impulsy 90°: R1403 [12400-12600]    │
│ Stabilizacja: R1410 [100-500] ms    │
│ Debouncing: R1412 [10-100] ms       │
│                                     │
│ KONTROLA PRZEPŁYWU:                 │
│ Status X4: R1507 (0=WOLNY/1=ZAPEŁN) │
│ Aktywacje dziś: D204                │
│                                     │
│ [ZAPISZ] [DOMYŚLNE] [GŁÓWNY]        │
└─────────────────────────────────────┘
```

### **EKRAN 3 - TRYB RĘCZNY**
```
┌─────────────────────────────────────┐
│ TRYB RĘCZNY (tylko gdy STOP)        │
│                                     │
│ Transport: [→] [←]                  │
│ Obrót: [CW] [CCW]                   │
│ Pozycja: [+90°] [-90°]              │
│                                     │
│ Funkcje: [HOME] [Przedmuch]         │
│                                     │
│ TEST X4:                            │
│ [X4 ON] [X4 OFF] Status: M224       │
│                                     │
│ Pozycja modułu: R1501 [°]           │
│ Status: OK / Problem                │
│ Transporter: R1507 WOLNY/ZAPEŁN     │
│                                     │
│ [GŁÓWNY]                            │
└─────────────────────────────────────┘
```

### **EKRAN 4 - DIAGNOSTYKA**
```
┌─────────────────────────────────────┐
│ DIAGNOSTYKA SYSTEMU                 │
│                                     │
│ WYDAJNOŚĆ:                          │
│ Czas pracy: H10 [h]                 │
│ Liczba partii: D100                 │
│ Czas ostatniego cyklu: R1500 [ms]   │
│ Średni cykl: R1503 [ms]             │
│ Zakres: R1504-R1505 [ms]            │
│                                     │
│ BŁĘDY:                              │
│ Pozycja wejścia: D200               │
│ Pozycja wyjścia: D201               │
│ Timeout transport: D202             │
│ Timeout obrót: D203                 │
│ Restarty HOME: R1506                │
│                                     │
│ KONTROLA PRZEPŁYWU:                 │
│ Aktywacje X4: D204                  │
│ Ostatnie zapełnienie: R1508 [ms]    │
│ Najdłuższe dziś: R1509 [ms]         │
│ Status bieżący: R1507               │
│                                     │
│ [RESET LICZNIKÓW] [GŁÓWNY]          │
└─────────────────────────────────────┘
```

---

## 🔧 **PROCEDURY DIAGNOSTYCZNE**

### **Test pozycjonowania**
```
1. HOME → R1501 = 0 (pozycja GÓRA)
2. Obrót +90° → R1501 = 90 (pozycja BOK)
3. Obrót +90° → R1501 = 180 (pozycja DÓŁ)
4. Obrót +90° → R1501 = 270 (pozycja BOK)  
5. Obrót +90° → R1501 = 0 (powrót do HOME)

Kalibracja R1403 jeśli pozycja nie odpowiada rzeczywistej
```

### **Test separacji funkcji B1**
```
FUNKCJA LICZENIA (podczas M22=ON):
- Symuluj opakowania na X2 → C1 rośnie do R1400
- Po M22=OFF → liczenie zatrzymane

FUNKCJA POZYCJI (podczas M233=ON):  
- X2=OFF, X3=OFF → M24=ON (można obrócić)
- X2=ON → M501=ON (błąd wejścia)
- X3=ON → M502=ON (błąd wyjścia)
```

### **Test kontroli przepływu X4**
```
FUNKCJA PODSTAWOWA:
1. X4 = OFF (transporter wolny) → M224 = OFF → proces normalny
2. X4 = ON (transporter zapełniony) → M224 = ON → blokada M21
3. Sprawdź debouncing: T40/T41 z parametrem R1412
4. Monitor flagi M507 (status dla HMI)
5. Sprawdź licznik D204 (aktywacje X4)

TEST BLOKADY PROCESU:
1. Force M224 = ON (symulacja zapełnienia)
2. Sprawdź że M21 nie może być aktywne (start cyklu blokowany)
3. Proces kontynuuje przetwarzanie już wprowadzonych partii
4. Force M224 = OFF → proces wraca do normy

TEST HMI:
1. M1019 = ON → M224 = ON (test z HMI)
2. Sprawdź wyświetlanie statusu na ekranie
3. M1020 = ON → M224 = OFF (reset z HMI)
4. Weryfikuj D204++ przy każdej aktywacji

KALIBRACJA POZYCJI X4:
- Pozycjonowanie nad transporterem odbiorczym
- 2-4mm od powierzchni transportera
- Test aktywacji przy różnych poziomach zapełnienia
- Dostrojenie czułości dla optymalnego triggering
```

### **Test timeoutów**
```
Transport: Brak czujnika B1 → timeout R1413s → M505
Obrót: Brak M1992 → timeout R1414s → M506
HOME: Brak X5 → timeout R1415s → M504
X4: Debouncing T40/T41 z parametrem R1412
```

---

## 📊 **MONITORING WYDAJNOŚCI**

### **Wskaźniki podstawowe**
```
PROCES:
- R1503: średni czas cyklu (stabilny = dobry proces)
- R1504/R1505: rozstrzał czasów (mały = powtarzalny)
- R1506: restarty HOME (<5/dzień = dobra kalibracja)
- D100: całkowita liczba partii

BŁĘDY:
- D200/D201: błędy pozycji (<10/dzień = OK)
- D202/D203: timeouty (<5/dzień = OK)

KONTROLA PRZEPŁYWU:
- D204: aktywacje X4 (<20/dzień = prawidłowy przepływ)
- R1508: czas ostatniego zapełnienia (<10s = sprawny odbiór)
- R1509: najdłuższy czas w dniu (trend = analiza problemów)
- R1507: status bieżący (0/1 = monitoring real-time)
```

### **Analiza trendów X4**
```
OPTYMALNE WARTOŚCI:
- D204 < 20 aktywacji/dzień
- R1508 < 5 sekund średnio
- R1509 < 15 sekund maksymalnie

OSTRZEŻENIA:
- D204 > 50/dzień → problem z odbiorem lub przepływem
- R1508 > 10s → wolne opróżnianie transportera
- R1509 rosnące → pogorszenie efektywności odbioru

DZIAŁANIA KORYGUJĄCE:
- Sprawdź szybkość transportera odbiorczego
- Zweryfikuj pozycjonowanie czujnika X4
- Dostraj debouncing R1412 jeśli false triggery
- Optymalizuj proces odbiorczy
```

---

## ⚙️ **SPECYFIKACJA HARDWARE**

### **Czujniki**
```
SENSOR_B1 (X2):
├── Typ: Indukcyjny PNP, M18x1, NO
├── Zasięg: 8mm
├── Funkcja: PODWÓJNA (liczenie + kontrola pozycji)
├── Pozycja: Wejście do modułu (0°)
└── Debouncing: T36/T37 (R1412)

SENSOR_B2 (X3):
├── Typ: Indukcyjny PNP, M18x1, NO  
├── Zasięg: 8mm
├── Funkcja: Zabezpieczenie wyjścia
├── Pozycja: Wyjście z modułu (0°)
└── Debouncing: T38/T39 (R1412)

TRANSPORTER_FULL (X4):
├── Typ: Indukcyjny PNP, M18x1, NO
├── Zasięg: 8mm
├── Funkcja: Kontrola przepływu (zapełnienie transportera)
├── Pozycja: Nad transporterem odbiorczym
├── Montaż: Uchwyt regulowany w osi Z
├── Debouncing: T40/T41 (R1412)
└── Diagnostyka: D204, R1508, R1509

SENSOR_HOME (X5):
├── Typ: Indukcyjny PNP, M18x1, NO
├── Zasięg: 8mm
├── Funkcja: Pozycja referencyjna 0°
├── Pozycja: Na module obrotowym
└── Debouncing: T42/T43 (R1412)
```

### **System bezpieczeństwa**
```
PILZ PNOZ X7 774303:
├── Kategoria: 3 według EN 954-1
├── Wejścia bezpieczeństwa: E-STOP + osłony
├── Wyjścia bezpieczne: 13/14 → X0 (SAFETY_STATUS)
├── Funkcja: Fizyczne odcięcie zasilania napędów
├── Czas reakcji: <20ms
├── Samodiagnostyka: ciągła
└── Reset: manual po usunięciu przyczyny
```

### **Napędy**
```
TRANSPORTERY M2+M3:
├── Typ: Beak SH-D08R
├── Sterowanie: Y0 (impulsy), Y1 (kierunek)  
├── Prędkość: 50-500 Hz (R1401)
├── Funkcja: Transport partii do modułu
└── FUN140: R1100-R1108 (AUTO), R1120-R1138 (MANUAL)

MODUŁ OBROTOWY M1:
├── Typ: SS86D + przekładnia 1:50
├── Sterowanie: Y2 (impulsy), Y3 (kierunek)
├── Prędkość: 100-1000 Hz (R1402)  
├── Pozycjonowanie: R1403 impulsów/90°
├── Funkcja: Obrót modułu co 90°
└── FUN140: R1200-R1208 (AUTO), R1210-R1238 (MANUAL)
```

---

## 🔍 **TROUBLESHOOTING**

### **Problemy X4 TRANSPORTER_FULL**
```
PROBLEM: X4 nie blokuje procesu
OBJAWY: Przepełnienie transportera, opakowania spadają
PRZYCZYNY: 
- Uszkodzony czujnik X4
- Błędne pozycjonowanie X4  
- Problem debouncing T40/T41
- Błąd w Network 016
ROZWIĄZANIE:
- Test czujnika X4 → M224
- Sprawdź pozycjonowanie (2-4mm)
- Weryfikuj debouncing R1412
- Sprawdź Network 016 ([/M224] warunek)

PROBLEM: Częste false triggery X4
OBJAWY: Niepotrzebne pauzy, D204 > 100/dzień
PRZYCZYNY:
- Za czuły czujnik X4
- Wibracje mechaniczne
- Błędna pozycja X4
ROZWIĄZANIE:
- Dostraj pozycję X4 (dalej od transportera)
- Zwiększ debouncing R1412
- Sprawdź mocowanie X4

PROBLEM: Długie zapełnienia (R1508 > 30s)
OBJAWY: Długie pauzy procesu, niska wydajność
PRZYCZYNY:
- Wolny odbiór z transportera
- Zapchanie transportera odbiorczego
- Problem z procesem odbiorczym
ROZWIĄZANIE:
- Sprawdź szybkość transportera odbiorczego
- Wyczyść transporter odbiorczy
- Optymalizuj proces odbiorczy
```

### **Problemy standardowe**
```
PROBLEM: Błędy pozycjonowania (R1501 ≠ rzeczywistość)
ROZWIĄZANIE: Kalibracja R1403 (impulsy 90°)

PROBLEM: Separacja B1 nie działa
ROZWIĄZANIE: Sprawdź timing M22/M233, Network 019/023

PROBLEM: Timeouty (M505, M506)
ROZWIĄZANIE: Dostraj R1413, R1414 do typu opakowań
```

---

## 📈 **KORZYŚCI ROZSZERZENIA**

```
✅ KONTROLA PRZEPŁYWU:
- Zapobieganie przepełnieniu transportera odbiorczego
- Automatyczna pauza i wznowienie procesu
- Ochrona przed stratami produktu
- Monitoring efektywności przepływu (D204, R1508, R1509)

✅ ZWIĘKSZONE BEZPIECZEŃSTWO:
- Pilz PNOZ X7 (kategoria 3)
- Kompletna kontrola wszystkich stref (B1, B2, X4)
- Debouncing dla wszystkich czujników (R1412)
- Diagnostyka w czasie rzeczywistym

✅ PRAKTYCZNE KORZYŚCI:
- 35 rejestrów oszczędności vs wersja podstawowa
- Diagnostyka X4 → praktyczne informacje
- Parametryzacja wszystkich funkcji czasowych → elastyczność
- Test funkcji X4 z HMI → łatwa diagnostyka
- Rezerwa w każdej grupie → dostępne rozszerzenia

✅ PROSTOTA IMPLEMENTACJI:
- Logiczna organizacja adresów z X4
- Łatwe troubleshooting z diagnostyką X4
- Standard przemysłowy z kontrolą przepływu
- Minimalne ryzyko błędów
- Szybkie wdrożenie z rozszerzoną funkcjonalnością

✅ MAINTAINABILITY:
- Czytelny kod dla serwisu (w tym X4 diagnostyka)
- Intuicyjne HMI dla operatora (status transportera)
- Prostsze szkolenia personelu (kontrola przepływu)
- Niezawodne działanie z X4
- Długoterminowa stabilność z monitoringiem
```

---

**© 2025 - Dokumentacja techniczna Vertino**  
**CNC Solutions - Michał Batorowicz**  
**KOMPLETNA SPECYFIKACJA Z X4 TRANSPORTER_FULL + PILZ PNOZ X7**