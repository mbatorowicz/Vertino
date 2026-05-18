# Instrukcja użytkownika — Vertino

## Vertino — Stacja oczyszczania opakowań

**Dokument:** IU-VTN-001  
**Wersja:** 2.1 (POPRAWIONA)  
**Data:** Lipiec 2025  

---

## 📄 INFORMACJE O AKTUALIZACJI

### Historia zmian v2.1
```
🔧 AKTUALIZACJE DLA UŻYTKOWNIKÓW v2.1:
✅ Nowe komunikaty błędów na ekranie HMI
✅ Rozszerzona diagnostyka procesu (pozycja modułu, czasy cykli)
✅ Lepsze zabezpieczenia pozycji (nowy czujnik B2)
✅ Ulepszone procedury obsługi błędów
✅ Nowe funkcje monitorowania wydajności
✅ Zaktualizowane procedury bezpieczeństwa
✅ Rozszerzone informacje diagnostyczne
```

---

## 🏭 INFORMACJE OGÓLNE

### Przeznaczenie urządzenia
Vertino (stacja oczyszczania opakowań) jest **maszyną ciągłego działania** w linii pakującej, przeznaczoną do **automatycznego przedmuchu opakowań w pozycji odwróconej**. Urządzenie wyposażone jest w **moduł obrotowy** umożliwiający równoczesną obsługę czterech partii opakowań.

### Proces technologiczny
```
MODUŁ OBROTOWY - 4 POZYCJE:

        [GÓRA - 0°]     ← Wejście/Wyjście partii
             │
[BOK - 270°] ┼ [BOK - 90°]  ← Pozycje transportowe  
             │
        [DÓŁ - 180°]    ← Pozycja przedmuchu (do góry dnem)
```

**Cykl kompletny każdej partii (360°):**
1. **Wejście** - partia wprowadzana do pozycji GÓRA (0°)
2. **Obrót 90°** - partia w pozycji BOK (90°) 
3. **Przedmuch** - partia w pozycji DÓŁ (180°, do góry dnem)
4. **Obrót 90°** - partia w pozycji BOK (270°)
5. **Wyjście** - partia w pozycji GÓRA (0°), wypychana przez następną

### Elementy obsługowe
```
┌─────────────────────────────────────────┐
│ 🖥️  PANEL HMI (4.3" ekran dotykowy)    │
│ 🔴  E-STOP (czerwony - STOP AWARYJNY)   │
│ 🟡  RESET (żółty - kasowanie błędów)    │
│ 🟢  Lampka LED (sygnalizacja stanu)     │
│ 💨  Przedmuch (ciągły podczas pracy)    │
└─────────────────────────────────────────┘
```

---

## 🚀 URUCHOMIENIE STACJI

### KROK 1: Kontrola przed uruchomieniem (ROZSZERZONE v2.1)
```
☐ Sprawdź czy obszar pracy jest wolny od ludzi
☐ Sprawdź czy osłony bezpieczeństwa są zamknięte  
☐ Sprawdź czy E-STOP nie jest wciśnięty
☐ Sprawdź czy moduł obrotowy obraca się swobodnie
☐ Sprawdź czy transport nie jest zablokowany
☐ Sprawdź ciśnienie powietrza (pneumatyka)
☐ Sprawdź czy wszystkie 4 pozycje modułu są wolne
☐ NOWE: Sprawdź czy strefy wejścia i wyjścia są czyste
☐ NOWE: Sprawdź czy brak przewróconych opakowań z poprzedniej zmiany
```

### KROK 2: Włączenie zasilania
```
1. Włącz wyłącznik główny w rozdzielnicy
2. Sprawdź czy panel HMI się uruchamia
3. Poczekaj na automatyczne wykonanie HOME
   → Moduł obrotowy ustawi się w pozycji referencyjnej (0°)
4. Sprawdź czy lampka LED świeci na ZIELONO
5. Sprawdź czy na HMI wyświetla się "System OK"
6. NOWE: Sprawdź czy pozycja modułu pokazuje "GÓRA (0°)"
```

### KROK 3: Sprawdzenie statusu (ROZSZERZONE v2.1)
Po uruchomieniu na ekranie HMI powinna pojawić się informacja:
```
┌─────────────────────────────────────┐
│  VERTINO v2.1      │
│                                     │
│  ✅ System OK                       │
│  ✅ HOME OK (pozycja 0°)            │
│  ⏸️  Zatrzymana                     │
│                                     │
│  Partia: 0 / 3 opakowań            │
│  Pozycja modułu: GÓRA (0°)          │
│  Cykl ostatni: -- sekund           │
│  Łącznie partii: 1247               │
│                                     │
│  📊 Błędy pozycji: 5 / 2 (dziś)    │
│  📊 Timeouty: 0 / 0 (dziś)         │
└─────────────────────────────────────┘
```

---

## ▶️ PRACA AUTOMATYCZNA

### KROK 1: Ustawienie parametrów procesu
```
1. Dotknij "PARAMETRY" na ekranie głównym
2. Ustaw parametry partii:
   
   ┌─────────────────────────────────────┐
   │ PARAMETRY PROCESU                   │
   │                                     │
   │ Opakowania w partii: [3] ↑↓        │ 
   │ Prędkość transportu: [200] Hz       │
   │ Prędkość obrotu: [400] Hz           │
   │                                     │
   │ ⚠️ Zakres: 1-10 opakowań/partia    │
   │                                     │
   │ 📊 Średni czas cyklu: 14.2s        │
   │ 📊 Wydajność: 750 opakowań/h       │
   └─────────────────────────────────────┘
   
3. Dotknij "ZAPISZ"
4. Wróć do ekranu głównego: "GŁÓWNY"
```

### KROK 2: Start procesu ciągłego
```
1. Sprawdź czy status pokazuje "System OK"
2. Sprawdź czy pozycja modułu: "GÓRA (0°)"
3. Dotknij przycisk "START" (zielony)
4. Obserwuj sekwencję procesu:

AUTOMATYCZNA SEKWENCJA:
┌─────────────────────────────────────┐
│ 1. Transport START                  │
│    → Wprowadzanie partii            │
│ 2. Liczenie opakowań (czujnik B1)   │
│    → 1/3... 2/3... 3/3             │
│ 3. Transport STOP                   │
│    → Stabilizacja pozycji (2s)      │
│ 4. Kontrola stref bezpieczeństwa    │
│    → ✅ OK / ❌ Ryzyko kolizji      │
│ 5. Obrót 90°                       │
│    → Następna pozycja modułu        │
│ 6. Powrót do kroku 1                │
│    → Proces ciągły                  │
└─────────────────────────────────────┘
```

### KROK 3: Monitorowanie procesu ciągłego (ROZSZERZONE v2.1)
```
Podczas pracy na ekranie widoczne są:
┌─────────────────────────────────────┐
│ 🔄 PROCES CIĄGŁY AKTYWNY            │
│                                     │
│ Transport: ▶️ AKTYWNY / ⏸️ STOP     │
│ Obrót: 🔄 AKTYWNY / ⏸️ STOP        │
│ Przedmuch: 💨 CIĄGŁY               │
│ Stabilizacja: ⏱️ AKTYWNA / ⏸️ OFF   │
│                                     │
│ Partia bieżąca: 2 / 3 opakowań     │
│ Pozycja modułu: BOK (90°)          │
│ Czas cyklu: 15.3 sekund           │
│ Łącznie partii: 1248               │
│                                     │
│ 📊 DZIŚ: Błędy wej/wyj: 5/2        │
│ 📊 DZIŚ: Timeouty: 0/0             │
│ 🟢 Status: PRACA NORMALNA           │
└─────────────────────────────────────┘

STANY MODUŁU OBROTOWEGO:
• GÓRA (0°): Wejście nowej partii / Wyjście gotowej
• BOK (90°): Transport międzypozycyjny  
• DÓŁ (180°): Przedmuch (opakowania do góry dnem)
• BOK (270°): Transport międzypozycyjny

NOWE FUNKCJE MONITORINGU v2.1:
• Pozycja modułu w czasie rzeczywistym
• Czas każdego cyklu (pomaga w optymalizacji)
• Liczniki błędów dziennych (wej./wyj./timeouty)
• Status stabilizacji (pokazuje kiedy sprawdzane są pozycje)
```

### KROK 4: Kontrola jakości procesu (ROZSZERZONE v2.1)
```
KONTROLA AUTOMATYCZNA:
┌─────────────────────────────────────┐
│ ✅ Pozycja opakowań przed obrotem   │
│    → Czujnik B1 sprawdza wejście    │
│    → Czujnik B2 sprawdza wyjście    │
│ ✅ Dokładność obrotu 90°            │
│    → Pozycjonowanie step-by-step    │
│ ✅ Ciągłość przedmuchu              │
│    → Zawsze partia w pozycji 180°   │
│ ✅ Synchronizacja wprowadzania      │
│    → Nowa partia wypycha gotową     │
│ ✅ Monitoring czasów cykli          │
│    → Wczesne wykrywanie problemów   │
└─────────────────────────────────────┘

NOWE ZABEZPIECZENIA v2.1:
• Podwójna kontrola pozycji (wejście i wyjście)
• Automatyczna stabilizacja przed obrotem
• Timeouty zapobiegające zawieszeniu systemu
• Statystyki błędów dla przewidywania problemów
```

---

## ⏹️ ZATRZYMANIE STACJI

### Zatrzymanie normalne (koniec zmiany)
```
1. Dotknij przycisk "STOP" (czerwony)
2. Maszyna dokończy aktualną sekwencję:
   → Partia wprowadzona zostanie przetworzona
   → Moduł zatrzyma się w pozycji HOME (0°)
3. Przedmuch automatycznie wyłączy się
4. Lampka LED będzie świecić stale (gotowość)
5. NOWE: Na ekranie pojawią się statystyki zmiany:
   - Liczba partii przetworzone
   - Średni czas cyklu
   - Błędy które wystąpiły
   - Wykorzystanie czasu pracy
```

### Zatrzymanie awaryjne (E-STOP)
```
1. Wciśnij czerwony przycisk E-STOP
2. NATYCHMIASTOWE ZATRZYMANIE:
   → Wszystkie ruchy zatrzymują się instantly
   → Transport zatrzymany
   → Moduł obrotowy zatrzymany
   → Przedmuch wyłączony
3. Lampka LED będzie migać (alarm)
4. Na ekranie: "OBWÓD BEZPIECZEŃSTWA NARUSZONY"

⚠️ UWAGA: E-STOP używaj tylko w sytuacjach niebezpiecznych!
Zatrzymanie w trakcie obrotu może wymagać ponownego HOME.
```

### Restart po E-STOP
```
1. Usuń przyczynę zatrzymania awaryjnego
2. Odkręć (pociągnij) przycisk E-STOP  
3. Naciśnij żółty przycisk RESET
4. Poczekaj na automatyczne HOME:
   → Moduł obrotowy ustawi się w pozycji 0°
   → Wszystkie partie zostaną wyczyszczone
5. Sprawdź czy status pokazuje "System OK"
6. Sprawdź pozycję modułu: "GÓRA (0°)"
7. Można wznowić pracę (ale proces zaczyna od nowa)
```

---

## 🔧 TRYB RĘCZNY (SERWISOWY)

### Kiedy używać trybu ręcznego
- **Ustawianie modułu** w konkretnej pozycji
- **Czyszczenie pozycji** modułu obrotowego
- **Testowanie ruchów** po konserwacji
- **Usuwanie zablokowanych** opakowań

### Aktywacja trybu ręcznego
```
1. Zatrzymaj maszynę (STOP)
2. Dotknij "SERWIS" na ekranie HMI
3. Pojawi się ekran kontroli ręcznej:

┌─────────────────────────────────────┐
│ TRYB RĘCZNY - KONTROLA v2.1         │
│                                     │
│ TRANSPORT:                          │
│ [Wprzód →] [Wstecz ←]              │
│                                     │
│ MODUŁ OBROTOWY:                     │  
│ [Obrót CW] [Obrót CCW]             │
│ [+90°]     [-90°]                   │
│                                     │
│ POZYCJONOWANIE:                     │
│ [GÓRA]  [BOK]  [DÓŁ]  [BOK]       │
│  0°     90°    180°   270°         │
│                                     │
│ INNE:                              │
│ [Przedmuch] [HOME] [RESET pozycji] │
│                                     │
│ 📊 Pozycja: GÓRA (0°)              │
│ ⚠️ TRYB SERWISOWY AKTYWNY          │
│ ⚠️ Sprawdź strefy przed ruchem     │
└─────────────────────────────────────┘
```

### Obsługa ruchów ręcznych (ROZSZERZONE v2.1)
```
RUCHY CHWILOWE (trzymaj przycisk wciśnięty):
- Transport → : ruch transporterów do przodu
- Transport ← : ruch transporterów do tyłu  
- Obrót CW    : obrót modułu zgodnie ze wskazówkami zegara
- Obrót CCW   : obrót modułu przeciwnie do wskazówek

RUCHY POZYCYJNE (jeden dotyk):
- +90°        : obrót o dokładnie 90° w prawo
- -90°        : obrót o dokładnie 90° w lewo
- GÓRA        : przejdź do pozycji 0°
- BOK 90°     : przejdź do pozycji 90°  
- DÓŁ         : przejdź do pozycji 180°
- BOK 270°    : przejdź do pozycji 270°

FUNKCJE POMOCNICZE:
- Przedmuch   : włącz/wyłącz przedmuch ręczny
- HOME        : automatyczny powrót do pozycji referencyjnej
- RESET pozycji: zerowanie pozycji (jeśli błędna na ekranie)

NOWE FUNKCJE v2.1:
- Wyświetlanie aktualnej pozycji modułu
- Ostrzeżenia o sprawdzeniu stref przed ruchem
- Lepsze komunikaty o stanie systemu
```

### Uwagi bezpieczeństwa w trybie ręcznym (ROZSZERZONE v2.1)
```
⚠️ PRZED UŻYCIEM TRYBU RĘCZNEGO:
- Sprawdź czy obszar jest wolny od ludzi
- Usuń opakowania z wszystkich pozycji modułu
- Sprawdź czy moduł może się obracać swobodnie
- NOWE: Sprawdź strefy wejścia i wyjścia (czujniki B1/B2)
- NOWE: Upewnij się że nie ma przewróconych opakowań
- Używaj krótkich impulsów ruchu

⚠️ PO ZAKOŃCZENIU PRACY RĘCZNEJ:
- Zawsze wykonaj HOME przed powrotem do trybu auto
- Sprawdź czy pozycja modułu jest prawidłowa (0°)
- Sprawdź czy wszystkie pozycje są wolne
- NOWE: Sprawdź czy pozycja na ekranie odpowiada rzeczywistości
```

### Powrót do trybu automatycznego
```
1. Dotknij "HOME" - moduł ustawi się w pozycji referencyjnej
2. Sprawdź pozycję na ekranie: powinno pokazać "GÓRA (0°)"
3. Dotknij "GŁÓWNY" aby wrócić do ekranu głównego  
4. Sprawdź status: "System OK" i "HOME OK"
5. Sprawdź pozycję: "GÓRA (0°)"
6. Można rozpocząć pracę automatyczną
```

---

## 🚨 ALARMY I BŁĘDY

### Najczęstsze komunikaty błędów (ROZSZERZONE v2.1)
```
┌──────────────────────────────────────────────────────────────┐
│ KOMUNIKAT                     │ PRZYCZYNA    │ CO ROBIĆ       │
├───────────────────────────────┼──────────────┼────────────────┤
│ OBWÓD BEZPIECZEŃSTWA          │ E-STOP       │ Sprawdź E-STOP │
│ NARUSZONY                     │ aktywny      │ i osłony       │
├───────────────────────────────┼──────────────┼────────────────┤
│ BŁĄD POZYCJI WEJŚCIA -        │ Opakowania   │ Usuń wystające│
│ B1 AKTYWNY                    │ wystają      │ opakowania     │
├───────────────────────────────┼──────────────┼────────────────┤
│ BŁĄD POZYCJI WYJŚCIA -        │ Przewrócone  │ Sprawdź strefę │
│ B2 AKTYWNY (NOWY v2.1)        │ opakowania   │ wyjściową      │
├───────────────────────────────┼──────────────┼────────────────┤
│ TIMEOUT TRANSPORTU (30s)      │ Zablokowany  │ Sprawdź trasę  │
│ (NOWY v2.1)                   │ transport    │ transportu     │
├───────────────────────────────┼──────────────┼────────────────┤
│ TIMEOUT OBROTU (8s)           │ Moduł        │ Sprawdź moduł  │
│ (NOWY v2.1)                   │ zablokowany  │ obrotowy       │
├───────────────────────────────┼──────────────┼────────────────┤
│ BŁĄD HOME (10s)               │ Czujnik HOME │ Wywołaj serwis│
│                               │ nie działa   │                │
├───────────────────────────────┼──────────────┼────────────────┤
│ BŁĄD PARAMETRÓW               │ Wartość poza │ Sprawdź        │
│                               │ zakresem     │ parametry 1-10 │
└───────────────────────────────┴──────────────┴────────────────┘
```

### Procedura kasowania błędów (ROZSZERZONE v2.1)
```
1. PRZECZYTAJ komunikat błędu na HMI
2. SPRAWDŹ dodatkowe informacje:
   - Pozycję modułu (którą pokazuje ekran)
   - Liczbę błędów które już wystąpiły dziś
   - Czy to nowy problem czy powtarzający się
3. USUŃ przyczynę błędu zgodnie z tabelą powyżej
4. NACIŚNIJ żółty przycisk RESET lub dotknij "RESET" na HMI
5. POCZEKAJ na automatyczne HOME (moduł → pozycja 0°)
6. SPRAWDŹ czy status pokazuje "System OK"
7. SPRAWDŹ czy pozycja modułu: "GÓRA (0°)"
8. NOWE: Sprawdź czy liczniki błędów się zwiększyły (to normalne)
9. WZNÓW pracę jeśli wszystko OK
```

### Specjalne procedury błędów

#### Ryzyko kolizji - NOWE PODWÓJNE zabezpieczenie v2.1
```
OBJAW: "BŁĄD POZYCJI WEJŚCIA - B1 AKTYWNY" lub 
       "BŁĄD POZYCJI WYJŚCIA - B2 AKTYWNY"

PRZYCZYNA: System wykrył ryzyko kolizji modułu z opakowaniami

MECHANIZM OCHRONY (NOWY v2.1):
- Po zatrzymaniu transportu system czeka 2 sekundy (stabilizacja)
- Następnie sprawdza 2 strefy bezpieczeństwa:
  • Strefa WEJŚCIA (czujnik B1): czy nowa partia prawidłowo ustawiona
  • Strefa WYJŚCIA (czujnik B2): czy brak przewróconych opakowań
- Tylko gdy obie strefy bezpieczne → moduł może się obrócić

PROCEDURA NAPRAWY:
1. STOP maszyny natychmiast
2. Przejdź do trybu RĘCZNY
3. Sprawdź wizualnie obie strefy modułu:
   - WEJŚCIE: czy nowa partia prawidłowo ustawiona
   - WYJŚCIE: czy brak przewróconych/wystających opakowań
4. Usuń wszystkie przeszkody ręcznie
5. Sprawdź czy nic nie blokuje strefy obrotu
6. Dotknij "HOME" → moduł do pozycji 0°
7. RESET → powrót do pracy auto

⚠️ UWAGA: To nowe zabezpieczenie v2.1 chroni przed uszkodzeniem!
- Błąd wejścia: opakowania wystają do strefy obrotu
- Błąd wyjścia: przewrócone opakowania blokują obrót
Nigdy nie ignoruj tych alarmów - mogą prowadzić do kolizji.

CZĘSTE PRZYCZYNY:
- Transport nie zatrzymuje się w tej samej pozycji
- Opakowania różnej wielkości niż standardowe
- Resztki po poprzedniej zmianie w strefie wyjścia
- Zbyt szybki transport (nie ma czasu na stabilizację)
```

#### Nowe timeouty systemu v2.1
```
OBJAW: "TIMEOUT TRANSPORTU (30s)" lub "TIMEOUT OBROTU (8s)"

PRZYCZYNA: System zabezpiecza się przed zawieszeniem

TIMEOUT TRANSPORTU (30s):
- Co znaczy: Transport działa ale nie zatrzymuje się po 30 sekundach
- Możliwe przyczyny: 
  • Czujnik B1 nie wykrywa opakowań (brudny/uszkodzony)
  • Opakowania nie dochodzą do czujnika
  • Transport mechanicznie zablokowany

TIMEOUT OBROTU (8s):
- Co znaczy: Moduł obraca się ale nie kończy obrotu po 8 sekundach
- Możliwe przyczyny:
  • Moduł mechanicznie zablokowany
  • Problem z napędem obrotowym
  • Zbyt dużo opakowań w module (przeciążenie)

PROCEDURA NAPRAWY:  
1. E-STOP (bezpieczeństwo)
2. Sprawdź co blokuje system:
   - Dla transportu: sprawdź trasę transporterów
   - Dla obrotu: sprawdź czy moduł może się obracać
3. Usuń przeszkody z wszystkich pozycji
4. Restart → RESET → HOME
5. Test w trybie ręcznym przed powrotem do auto
6. Powrót do pracy auto

UWAGA: Te timeouty chronią system przed uszkodzeniem
i pomagają szybko znaleźć problemy mechaniczne.
```

---

## 📊 MONITOROWANIE PRACY

### Wskaźniki procesu na HMI (ROZSZERZONE v2.1)
```
EKRAN GŁÓWNY - informacje bieżące:
┌─────────────────────────────────────┐
│ • Partia bieżąca: 2/3 opakowań     │
│ • Pozycja modułu: DÓŁ (180°)       │
│ • Status transportu: AKTYWNY        │
│ • Status obrotu: NIEAKTYWNY         │
│ • Stabilizacja: AKTYWNA             │
│ • Przedmuch: CIĄGŁY                 │
│ • Czas cyklu: 15.3 sekund          │
│                                     │
│ DZIŚ (NOWE v2.1):                   │
│ • Błędy pozycji wej.: 12            │
│ • Błędy pozycji wyj.: 3             │
│ • Timeouty trans.: 0                │
│ • Timeouty obrotu: 1                │
└─────────────────────────────────────┘

EKRAN STATYSTYKI (dotknij "STATS"):
┌─────────────────────────────────────┐
│ • Czas pracy dzisiaj: 6h 23min     │
│ • Partie przetworzone: 847         │
│ • Średni czas partii: 14.2 sek     │
│ • Najszybszy cykl: 12.8 sek        │
│ • Najwolniejszy cykl: 18.1 sek     │
│ • Wykorzystanie: 87%               │
│                                     │
│ PROBLEMY DZIŚ (NOWE):               │
│ • Ostatni błąd: 14:23 (Pozycja B1) │
│ • Częstotliwość błędów: 1.4%        │
│ • Najczęstszy błąd: Pozycja wej.    │
│ • Status: 🟢 NORMALNY               │
└─────────────────────────────────────┘
```

### Sygnalizacja świetlna (ROZSZERZONE v2.1)
```
🟢 ŚWIECI STALE     = Praca normalna (wszystko OK)
🟢 MIGA POWOLI      = Gotowość (zatrzymana, można startować)  
🔴 MIGA SZYBKO      = Błąd systemu (sprawdź HMI)
🟡 MIGA ŚREDNIO     = Ostrzeżenie (częste błędy pozycji)
⚫ ZGASZONA         = System wyłączony lub brak zasilania
💨 Dźwięk           = Przedmuch pneumatyczny aktywny

NOWE WZORCE MIGANIA v2.1:
🟡🔴 NAPRZEMIENNE    = Timeout systemu (transport/obrót)
🔵 MIGA WOLNO       = Tryb serwisowy aktywny
```

### Kontrola wydajności (ROZSZERZONE v2.1)
```
OPTYMALNE PARAMETRY:
┌─────────────────────────────────────┐
│ • Czas partii: 12-18 sekund        │
│ • Wykorzystanie: >85%               │
│ • Błędy pozycji: <5% partii        │
│ • Błędy timeoutu: <1%              │
│ • Pozycja modułu: dokładnie 0-270°  │
│ • Stabilność cykli: ±2s (podobne)   │
└─────────────────────────────────────┘

JEŚLI WYDAJNOŚĆ SPADA:
1. Sprawdź średni czas cyklu (czy roście)
2. Sprawdź częstotliwość błędów pozycji (czy rośnie)  
3. Sprawdź czy pojawiły się nowe timeouty
4. Sprawdź pozycjonowanie modułu (czy dokładne)
5. NOWE: Sprawdź trend błędów (czy problem się pogarsza)
6. Wywołaj serwis do optymalizacji jeśli potrzeba

OSTRZEŻENIA WCZESNE v2.1:
- Czas cyklu >20s → sprawdź mechanikę
- Błędy pozycji >10/dzień → sprawdź czujniki
- 3 timeouty w ciągu dnia → sprawdź system
- Pozycja modułu nieprawidłowa → kalibracja
```

---

## ⚠️ BEZPIECZEŃSTWO

### ZASADY PODSTAWOWE
```
🔴 NIGDY nie obchodź zabezpieczeń
🔴 NIGDY nie wkładaj rąk w obszar modułu obrotowego podczas ruchu
🔴 ZAWSZE używaj E-STOP w sytuacjach niebezpiecznych
🔴 ZAWSZE sprawdź czy wszystkie pozycje są wolne przed startem
🔴 NIGDY nie używaj siły do odblokowania mechanizmów
🔴 NOWE: ZAWSZE sprawdź strefy wejścia i wyjścia przed startem
🟡 Używaj trybu ręcznego tylko przy obsłudze i czyszczeniu
🟡 Przy dziwnych dźwiękach - natychmiast zatrzymaj
🟡 Sprawdzaj pozycje modułu przed każdą zmianą
🟡 NOWE: Zwracaj uwagę na nowe komunikaty błędów
```

### Strefy niebezpieczne (ROZSZERZONE v2.1)
```
OBSZARY WYMAGAJĄCE SZCZEGÓLNEJ OSTROŻNOŚCI:

1. MODUŁ OBROTOWY:
   - Pozycje 0°, 90°, 180°, 270°
   - Strefa obrotu całego modułu
   - Mechanizm napędowy

2. TRANSPORTERY:
   - Wejście do pozycji 0°
   - Wyjście z pozycji 0°
   - Synchronizacja z modułem

3. SYSTEM PNEUMATYCZNY:
   - Dysze przedmuchu w pozycji 180°
   - Ciśnienie robocze
   - Hałas podczas pracy

4. STREFY KONTROLI POZYCJI (NOWE v2.1):
   - Strefa wejścia (kontrolowana przez czujnik B1)
   - Strefa wyjścia (kontrolowana przez czujnik B2)  
   - Obszary stabilizacji po zatrzymaniu transportu
   - Strefy gdzie opakowania mogą się przewrócić
```

### Sytuacje wymagające natychmiastowego E-STOP (ROZSZERZONE v2.1)
```
- Osoba w strefie modułu obrotowego podczas ruchu
- Zablokowanie mechaniczne podczas obrotu
- Nietypowe dźwięki lub wibracje modułu
- Opakowania spadające z pozycji
- Dym lub zapach spalenizny
- Uszkodzenie osłon bezpieczeństwa
- Niekontrolowany ruch modułu
- NOWE: Częste błędy pozycji (>5 z rzędu)
- NOWE: Opakowania blokujące obrót mimo alarm
- NOWE: Timeouty powtarzające się kilka razy z rzędu
```

---

## 🧹 KONSERWACJA PODSTAWOWA

### Codziennie (przed rozpoczęciem pracy) - ROZSZERZONE v2.1
```
☐ Sprawdź czy wszystkie pozycje modułu są czyste i wolne
☐ Sprawdź czy moduł obraca się swobodnie (ręcznie)
☐ Sprawdź czy osłony są sprawne i zamknięte
☐ Sprawdź czy E-STOP działa (naciśnij i puść)
☐ Sprawdź ciśnienie powietrza pneumatyki
☐ Sprawdź czy czujniki B1 i B2 nie są zakurzone
☐ Sprawdź czy transportery nie są zablokowane
☐ Test HOME - czy moduł wraca do pozycji 0°
☐ NOWE: Sprawdź pozycję na ekranie vs. rzeczywista
☐ NOWE: Sprawdź czy brak resztek z poprzedniej zmiany
☐ NOWE: Sprawdź statystyki błędów z poprzedniego dnia
```

### Tygodniowo (ROZSZERZONE v2.1)
```
☐ Oczyść wszystkie pozycje modułu obrotowego
☐ Sprawdź czy czujniki nie są zakurzone (B1 i B2)
☐ Sprawdź połączenia pneumatyczne
☐ Sprawdź działanie przedmuchu w każdej pozycji
☐ Sprawdź dokładność pozycjonowania (0°, 90°, 180°, 270°)
☐ Sprawdź synchronizację transporterów z modułem
☐ Oczyść ekran HMI
☐ NOWE: Sprawdź strefy wejścia i wyjścia (czyszczenie)
☐ NOWE: Analiza statystyk błędów tygodniowych
☐ NOWE: Test nowych zabezpieczeń pozycji
☐ NOWE: Sprawdź czy pozycja na ekranie odpowiada rzeczywistej
```

### Miesięcznie (przez serwis) - ROZSZERZONE v2.1
```
☐ Sprawdzenie i czyszczenie wszystkich czujników
☐ Kontrola połączeń elektrycznych  
☐ Sprawdzenie dokładności obrotu (kalibracja 90°)
☐ Smarowanie łożysk modułu (jeśli wymagane)
☐ Test wszystkich funkcji bezpieczeństwa
☐ Sprawdzenie wydajności procesu
☐ Backup parametrów i statystyk
☐ Analiza historii błędów pozycji
☐ NOWE: Test separacji funkcji czujników (B1 liczenie vs. pozycja)
☐ NOWE: Kalibracja nowych zabezpieczeń pozycji
☐ NOWE: Analiza trendów timeoutów
☐ NOWE: Weryfikacja dokładności pozycji modułu
☐ NOWE: Optymalizacja parametrów na podstawie statystyk
```

---

## 📞 W RAZIE PROBLEMÓW

### Krok po kroku (ROZSZERZONE v2.1)
```
1. ZATRZYMAJ maszynę (STOP lub E-STOP)
2. SPRAWDŹ komunikat błędu na HMI
3. SPRAWDŹ pozycję modułu obrotowego (na ekranie i wizualnie)
4. SPRAWDŹ czy to nowy problem czy powtarzający się
5. SPRAWDŹ dodatkowe informacje (liczniki błędów, czas cyklu)
6. SPRÓBUJ rozwiązać problem wg tabeli alarmów
7. Jeśli nie pomaga - RESET i restart z HOME
8. SPRAWDŹ czy pozycja na ekranie odpowiada rzeczywistej
9. Jeśli problem się powtarza - WYWOŁAJ SERWIS
```

### Informacje do przekazania serwisowi (ROZSZERZONE v2.1)
```
📞 Numer serwisu: ________________
📧 Email serwisu: ________________  
🕒 Godziny pracy: ________________

PODAJ ZAWSZE:
- Numer seryjny maszyny
- Komunikat błędu z HMI (dokładny tekst)
- Pozycję modułu w momencie błędu (z ekranu i wizualnie)
- Fazę procesu (transport/stabilizacja/obrót/pozycja)
- Ile partii zostało przetworzonych przed błędem
- Czy błąd występuje regularnie (jak często)
- Parametry procesu (ilość opakowań, prędkości)
- NOWE: Stan czujników pozycji podczas błędu
- NOWE: Statystyki błędów (ile dzisiaj, ile wczoraj)
- NOWE: Czas ostatniego cyklu (czy normalny)
- NOWE: Czy pozycja na ekranie odpowiada rzeczywistej

NOWE PYTANIA v2.1:
- Czy problem dotyczy konkretnej pozycji modułu?
- Czy błędy pozycji występują z konkretnym typem opakowań?
- Czy timeouty występują w konkretnych warunkach?
- Jak często trzeba wykonywać RESET?
```

### Najczęstsze pytania operatorów (ROZSZERZONE v2.1)

#### "Dlaczego przedmuch jest cały czas włączony?"
```
ODPOWIEDŹ: To jest prawidłowe działanie!
W module zawsze jedna z czterech partii
znajduje się w pozycji DÓŁ (180°) i wymaga przedmuchu.
Dlatego pneumatyka jest aktywna ciągle podczas pracy.
```

#### "Co oznaczają nowe błędy pozycji?"
```  
ODPOWIEDŹ: To nowe zabezpieczenia v2.1!
System ma teraz dwa czujniki zabezpieczające:
- B1 (wejście): sprawdza czy nowa partia prawidłowo ustawiona
- B2 (wyjście): sprawdza czy nie ma przewróconych opakowań

Po zatrzymaniu transportu system czeka 2 sekundy (stabilizacja)
a potem sprawdza obie strefy. Jeśli którykolwiek czujnik wykryje
przeszkodę - zatrzymuje obrót aby uniknąć kolizji.
Zawsze usuń przyczynę przed kontynuowaniem pracy.
```

#### "Co to są nowe timeouty?"
```
ODPOWIEDŹ: To ochrona przed zawieszeniem systemu!
- Timeout transportu (30s): transport nie zatrzymuje się
- Timeout obrotu (8s): moduł nie kończy obrotu

Te zabezpieczenia pomagają szybko wykryć problemy mechaniczne
i chronią system przed uszkodzeniem. Jeśli występują często,
trzeba sprawdzić przyczyny (zablokowanie, uszkodzone czujniki).
```

#### "Dlaczego pozycja na ekranie nie odpowiada rzeczywistej?"
```
ODPOWIEDŹ: To może być problem kalibracji!
Pozycja na ekranie to tylko wskaźnik elektroniczny.
Jeśli nie odpowiada rzeczywistości:
1. Wykonaj HOME (przywróci pozycję referencyjną)
2. Jeśli problem się powtarza - wywołaj serwis
3. System może wymagać kalibracji

Ważne: moduł może pracować nawet jeśli wskaźnik błędny,
ale serwis powinien to skorygować.
```

#### "Czy mogę zmienić liczbę opakowań podczas pracy?"
```  
ODPOWIEDŹ: NIE podczas procesu!
1. Zatrzymaj maszynę (STOP)
2. Zmień parametr w menu "PARAMETRY"  
3. Start - nowy parametr obowiązuje od następnej partii

UWAGA v2.1: Po zmianie parametrów sprawdź:
- Czy średni czas cyklu nie zwiększył się za bardzo
- Czy nie pojawiły się błędy pozycji (przez inne opakowania)
- Czy system nadal pracuje stabilnie
```

---

## 📋 DZIENNIK PRACY

### Dzienne wpisy operatora (ROZSZERZONE v2.1)
```
Data: ___________  Zmiana: ___________  Operator: ___________

SPRAWDZENIE PRZED PRACĄ:
☐ E-STOP sprawny
☐ Osłony zamknięte  
☐ Moduł sprawny (test HOME)
☐ Wszystkie pozycje wolne (0°, 90°, 180°, 270°)
☐ Transportery działają
☐ Czujniki B1 i B2 sprawne
☐ Ciśnienie powietrza OK
☐ NOWE: Pozycja na ekranie vs. rzeczywista OK
☐ NOWE: Strefy wejścia/wyjścia czyste

PARAMETRY PRACY:
Opakowania w partii: _____
Prędkość transportu: _____ Hz
Prędkość obrotu: _____ Hz
Partie przetworzone: _____
Czas pracy: _____ godz

STATYSTYKI BŁĘDÓW (NOWE v2.1):
Błędy pozycji wejścia: _____ (B1)
Błędy pozycji wyjścia: _____ (B2)
Timeouty transportu: _____ (30s)
Timeouty obrotu: _____ (8s)
Średni czas cyklu: _____ s

UWAGI O PROCESIE:
Pozycjonowanie modułu: ☐ Dokładne ☐ Problemy
Przedmuch: ☐ Równomierny ☐ Słaby ☐ Za mocny  
Synchronizacja: ☐ OK ☐ Problemy z timing
Stabilizacja: ☐ OK ☐ Za krótka ☐ Problemy pozycji
Jakość pozycji: ☐ OK ☐ Częste błędy B1/B2

NOWE OBSERWACJE v2.1:
Dokładność pozycji ekran vs. rzeczywistość: ☐ OK ☐ Błędna
Frequency błędów pozycji: ☐ Normalna ☐ Zwiększona ☐ Problematyczna
Stabilność czasów cykli: ☐ Stałe ☐ Zmienne ☐ Trend wzrostowy
System timeoutów: ☐ Brak ☐ Pojedyncze ☐ Częste

UWAGI OGÓLNE: __________________________________
____________________________________________
____________________________________________

ZALECENIA DLA NASTĘPNEJ ZMIANY:
____________________________________________
____________________________________________

Podpis operatora: _______________
```

---

**⚠️ PAMIĘTAJ: Bezpieczeństwo jest najważniejsze!**  
**W v2.1 system ma lepsze zabezpieczenia - ufaj im i nie omijaj alarmów.**

**NOWE w v2.1:**
- Lepsze zabezpieczenia pozycji (podwójne czujniki)
- Monitoring czasów cykli i wydajności  
- Zabezpieczenia przed zawieszeniem (timeouty)
- Lepsza diagnostyka problemów
- Statystyki błędów dla predykcji problemów

---

**© 2025 - Instrukcja użytkownika Vertino v2.1**  
**Dokument zaktualizowany - nowe funkcje bezpieczeństwa i diagnostyki**
## Czujnik B4 — zator na linii odbiorczej

Czujnik **B4** (wejście **X4**) monitoruje przepływ na transporterze odbiorczym za stacją.

| Stan B4 | Zachowanie |
|---------|------------|
| **OFF** | Normalne przepychanie i zliczanie partii |
| **ON** | Stop przepychania; **C1 bez resetu**; obrót modułu może trwać |

Usuń zator na linii odbiorczej — maszyna wznowi przepychanie bez utraty zliczonej ilości w partii. Szczegóły: [plc/program.md](program.md) (N0020–N0024), [maszyna.md](maszyna.md#zator-b4).

