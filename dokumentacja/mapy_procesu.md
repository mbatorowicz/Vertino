# Vertino — mapy programu, procesu i operatora

**Maszyna:** Vertino — Stacja oczyszczania opakowań

| Sekcja | Opisuje |
|--------|---------|
| **§1 Mapa programu (drzewo N0000–N0034)** | Program **docelowy** — **nie** w sterowniku |
| **§2–3 Proces i operator** | Proces na maszynie (zgodny z oboma wersjami tam, gdzie nie zaznaczono inaczej) |

**W sterowniku dziś:** 78 sieci — **[plc/STAN_FAKTYCZNY.md](plc/STAN_FAKTYCZNY.md)**  
**Plan PLC:** [plc/03_program_vertino_sieci.md](plc/03_program_vertino_sieci.md)

---

## §1 — Program docelowy (plan, 35 sieci)

> Nie mylić z programem w `SKO-Program.pdw` (78 sieci).

---

## 1. Mapa programu PLC

### 1.1 Drzewo modułów (sieci)

```mermaid
flowchart TB
    subgraph ROOT["Main_unit1 — Vertino Program"]
        direction TB

        subgraph L0["Warstwa 0 — Bezpieczeństwo i gotowość"]
            N00[N0000–N0001 Pilz X0 → M1]
            N02[N0002 Reset HMI M1000 → M200]
            N03[N0003–N0004 System gotowy M10]
            N05[N0005 Kasowanie błędów M501–M507]
        end

        subgraph L1["Warstwa 1 — Konfiguracja"]
            N06[N0006 Walidacja R1400–R1412]
            N07[N0007 FUN141 parametry osi]
            N08[N0008 B4 → T52 → M507 ★]
        end

        subgraph L2["Warstwa 2 — Sterowanie trybem"]
            N09[N0009 START/STOP AUTO M70]
            N10[N0010–N0011 HOME M80→M82]
        end

        subgraph L3["Warstwa 3 — Napędy"]
            N12[N0012 FUN140 Transport R1100]
            N13[N0013 FUN140 Obrót R1200]
            N14[N0014 Y4 SYSTEM_READY]
        end

        subgraph L4["Warstwa 4 — Sekwencer AUTO ★"]
            N15[N0015 Start partii M21]
            N16[N0016 Wejście M22 RST C1 T5]
            N17[N0017 Zliczanie ↑X1 → C1]
            N18[N0018 Koniec partii M233]
            N19[N0019 Stabilizacja M23]
            N20[N0020 B1/B2 czas R1410]
            N21[N0021 Start obrotu M25]
            N22[N0022 Koniec obrotu R1501]
        end

        subgraph L5["Warstwa 5 — Proces pomocniczy"]
            N23[N0023 Przedmuch AUTO Y5 @180°]
            N24[N0024 Przedmuch ręczny]
            N25[N0025 Pauza serwo przy M507]
            N26[N0026 Timeout transportu T5]
            N27[N0027 Timeout obrotu T7]
            N28[N0028 Czas cyklu R1500]
        end

        subgraph L6["Warstwa 6 — Serwis"]
            N29[N0029–N0031 Tryb ręczny M100]
            N32[N0032 Symulacja B4 M1050]
            N33[N0033 Licznik zatorów D204]
        end

        N34[N0034 END]
    end

    L0 --> L1 --> L2 --> L3 --> L4
    L4 --> L5 --> L6 --> N34
```

★ — kluczowe dla B4 / licznika C1

### 1.2 Tabela mapy sieci

| Blok | Sieci | Funkcja | Kluczowe sygnały |
|------|-------|---------|------------------|
| Bezpieczeństwo | N0000–N0001 | Pilz | X0 → M1 |
| Gotowość | N0002–N0005 | M10, reset | M1000, M200, M503–M506 |
| Parametry | N0006–N0007 | Walidacja, serwo | R1400–R1412, FUN141 |
| **B4** | **N0008** | Zator potwierdzony | X4, T52, **M507**, R1507 |
| AUTO on/off | N0009 | Praca ciągła | M1001→M70, M1002 |
| HOME | N0010–N0011 | Referencja 0° | M80, M82, X3, T10 |
| FUN140 | N0012–N0014 | Transport, obrót | M1992, M1993, Y4 |
| **Sekwencer** | **N0015–N0022** | Partia M21→M25 | **C1**, M22–M25, M233 |
| Przedmuch | N0023–N0024 | Y5 | R1501=180, M240 |
| Timeouty | N0025–N0028 | T5, T7, R1500 | M505, M506 |
| Ręczny | N0029–N0032 | HMI serwis | M100, M1010–M1024 |
| Diagnostyka B4 | N0033 | Statystyka | D204, M520 |

### 1.3 Mapa zależności sygnałów (skrót)

```mermaid
flowchart LR
    subgraph WE["Wejścia"]
        X0[X0 Pilz]
        X1[X1 B1]
        X2[X2 B2]
        X3[X3 B3 HOME]
        X4[X4 B4]
    end

    subgraph HMI["HMI → PLC"]
        M1001[M1001 START]
        M1002[M1002 STOP]
        M1000[M1000 RESET]
        M1003[M1003 HOME]
    end

    subgraph CORE["Rdzeń procesu"]
        M10[M10 Gotowy]
        M70[M70 AUTO]
        M21[M21 Start partii]
        M22[M22 Zliczanie]
        C1[C1 Licznik]
        M507[M507 Zator]
        M25[M25 Obrót]
    end

    subgraph WY["Wyjścia"]
        Y0[Y0–Y1 Transport]
        Y2[Y2–Y3 Obrót]
        Y5[Y5 Przedmuch]
        Y4[Y4 Ready LED]
    end

    X0 --> M10
    M1001 --> M70
    M70 --> M21
    M21 --> M22
    X1 --> C1
    M22 --> C1
    X4 --> M507
    M507 -.->|blokuje| M22
    M507 -.->|nie blokuje| M25
    M22 --> Y0
    M25 --> Y2
    R1501[R1501 pozycja] --> Y5
```

### 1.4 Kolejność skanu (kolejka wykonania)

```
Skan PLC (góra → dół):
  N0008 ustawia M507
       ↓
  N0009 sprawdza M70
       ↓
  N0012–N0013 FUN140 (reaguje na M21, M25, /M507)
       ↓
  N0015–N0022 sekwencer (czyta M507, aktualizuje C1, M22…M25)
       ↓
  N0026 timeout T5 (tylko gdy /M507)
```

---

## 2. Drzewo procesu

### 2.1 Proces technologiczny (maszyna)

```mermaid
flowchart TD
    START([Linia zaopatrzona słoikami]) --> CHK_B4{Linia odbiorcza wolna?<br/>B4 OFF}

    CHK_B4 -->|Nie — zator ≥ R1412| PAUSE[PAUZA przepychania<br/>C1 zachowane]
    PAUSE --> CHK_B4

    CHK_B4 -->|Tak| PUSH[Transport — przepychanie partii]
    PUSH --> COUNT{Zliczanie B1<br/>↑X1 → C1}

    COUNT -->|C1 < R1400| PUSH
    COUNT -->|C1 = R1400| STAB[Stabilizacja<br/>B1 zasłonięty przez R1410]

    STAB --> ZONE{Strefy B1/B2 OK?}
    ZONE -->|Błąd pozycji| ERR_POS[Alarm M501/M502<br/>STOP — reset]
    ZONE -->|OK| ROT[Obrót modułu +90°]

    ROT --> POS{Pozycja modułu}
    POS -->|0°| PUSH
    POS -->|90° / 270°| PUSH
    POS -->|180°| BLOW[Przedmuch Y5<br/>oczyszczanie dnem do góry]
    BLOW --> ROT

    ERR_POS --> RESET_SERWIS([Reset + serwis])
```

### 2.2 Proces równoległy — moduł 4×90°

```mermaid
flowchart LR
    subgraph MOD["Moduł obrotowy — 4 partie równolegle"]
        P0["0° GÓRA<br/>wej./wyj."]
        P90["90° BOK<br/>transport"]
        P180["180° DÓŁ<br/>przedmuch"]
        P270["270° BOK<br/>transport"]
    end

    P0 -->|+90°| P90 -->|+90°| P180 -->|+90°| P270 -->|+90°| P0
```

| Pozycja R1501 | Funkcja | Akcja procesowa |
|---------------|---------|-----------------|
| 0° | Góra | Wejście partii / wypychanie oczyszczonych |
| 90° | Bok | Transport międzypozycyjny |
| 180° | Dół | **Przedmuch** (Y5) |
| 270° | Bok | Transport międzypozycyjny |

### 2.3 Drzewo stanów PLC (sekwencer AUTO)

```mermaid
stateDiagram-v2
    direction LR

    [*] --> Idle: M70=OFF

    Idle --> Ready: M1001, M10
    Ready --> M21: /M507, brak M21–M25

    M21 --> M22: FUN140 push, /M507, RST C1
    M22 --> M22: X1↑ → C1++, /M507
    M22 --> M22_Pause: M507 ON — bez zliczania
    M22_Pause --> M22: M507 OFF — wznowienie

    M22 --> M233: C1≥R1400, /M507
    M233 --> M23: stabilizacja start
    M23 --> M23: X1 ON → T6 nabija R1410
    M23 --> M24: T6 OK, /M501/502

    M24 --> M25: start obrotu
    M25 --> M25: FUN140 obrót (M507 ignorowane)
    M25 --> AfterRot: M1993, T8, R1501+=90°

    AfterRot --> M21: następna partia
    AfterRot --> Idle: M1002 STOP

    M22 --> FaultT5: T5, /M507
    M25 --> FaultT7: T7
    FaultT5 --> Idle: M505
    FaultT7 --> Idle: M506
```

### 2.4 Drzewo decyzji — B4 i licznik C1

```mermaid
flowchart TD
    A[Transport aktywny M22] --> B{X4 ciągle ON<br/>≥ R1412 ms?}

    B -->|Nie| C[Normalnie:<br/>↑X1 zlicza C1]
    C --> D{C1 ≥ R1400?}
    D -->|Nie| A
    D -->|Tak, /M507| E[Koniec partii M233]

    B -->|Tak| F[M507 = PAUZA]
    F --> G[Brak +C1<br/>Brak końca partii<br/>C1 bez zmian]
    G --> H{Linie wolna?<br/>/M507}
    H -->|Nie| F
    H -->|Tak| C
```

---

## 3. Drzewo przepływu operatora

### 3.1 Przepływ główny (od włączenia do pracy)

```mermaid
flowchart TD
    START([Rozpoczęcie zmiany]) --> PRE{Kontrola wstępna<br/>lista operatora}

    PRE -->|Nie OK| FIX[Usuń przeszkodę /<br/>zamknij osłony]
    FIX --> PRE

    PRE -->|OK| PWR[Włącz zasilanie<br/>rozdzielnica]
    PWR --> HMI_ON[HMI startuje<br/>automatyczny HOME]

    HMI_ON --> HOME_OK{Ekran:<br/>System OK + HOME OK?}
    HOME_OK -->|Nie| ALM_HOME[Alarm HOME / bezpieczeństwo<br/>→ sekcja alarmów]
    HOME_OK -->|Tak| PARAM[Menu PARAMETRY<br/>R1400, prędkości]

    PARAM --> SAVE[ZAPISZ → ekran GŁÓWNY]
    SAVE --> START_BTN[Naciśnij START<br/>M1001]

    START_BTN --> AUTO[Praca AUTO ciągła<br/>monitorowanie ekranu]
    AUTO --> STOP_BTN{Koniec zmiany?}

    STOP_BTN -->|STOP| STOP[Naciśnij STOP<br/>dokończenie sekwencji]
    STOP --> END([Koniec — statystyki zmiany])

    STOP_BTN -->|Nie| AUTO
```

### 3.2 Przepływ podczas pracy AUTO (ekran operatora)

```mermaid
flowchart TD
    AUTO([Praca AUTO M70]) --> MON[Ekran procesu]

    MON --> T1[Transport AKTYWNY<br/>Partia: C1/R1400]
    T1 --> T2{Licznik rośnie?}
    T2 -->|Tak| T3[Stabilizacja / Kontrola stref]
    T3 --> T4[Obrót — pozycja 90°/180°/270°]
    T4 --> T1

    MON --> ZATOR{B4 — linia odbiorcza<br/>zator?}
    ZATOR -->|Tak| Z1[Status: PAUZA przepychania<br/>Partia: C1 bez zmian]
    Z1 --> Z2[Operator: opróżnij<br/>linię odbiorczą]
    Z2 --> Z3{Linie wolna?}
    Z3 -->|Nie| Z1
    Z3 -->|Tak| T1

    MON --> ALARM{Alarm na HMI?}
    ALARM -->|Tak| ERR_FLOW[→ Drzewo alarmów]
    ALARM -->|Nie| MON
```

### 3.3 Drzewo alarmów i reakcji operatora

```mermaid
flowchart TD
    ALM([Alarm / błąd]) --> TYPE{Typ komunikatu}

    TYPE -->|E-STOP / Pilz| E1[OBWÓD BEZPIECZEŃSTWA]
    E1 --> E2[Usuń przyczynę<br/>Odkręć E-STOP]
    E2 --> E3[RESET żółty / M1000]
    E3 --> E4[Poczekaj HOME → 0°]
    E4 --> E5{System OK?}
    E5 -->|Tak| RESTART[START od nowa]
    E5 -->|Nie| SERWIS1[Wezwij serwis]

    TYPE -->|Zator B4 / M507| B1[Pauza przepychania]
    B1 --> B2[Usuń zator za maszyną<br/>NIE resetuj partii]
    B2 --> B3[Proces wznawia się sam<br/>gdy linia wolna]

    TYPE -->|Błąd pozycji M501/M502| P1[STOP — ryzyko kolizji]
    P1 --> P2[Sprawdź słoiki w strefie<br/>B1/B2]
    P2 --> P3[RESET → HOME]
    P3 --> RESTART

    TYPE -->|Timeout transport/obrót| T1[M505 / M506]
    T1 --> T2[RESET → HOME]
    T2 --> SERWIS2{Powtarza się?}
    SERWIS2 -->|Tak| SERWIS1
    SERWIS2 -->|Nie| RESTART

    TYPE -->|Błąd parametrów M503| R1[Sprawdź PARAMETRY<br/>zakresy R1400–R1412]
    R1 --> R2[ZAPISZ → RESET]
```

### 3.4 Przepływ — tryb ręczny (skrót, serwis)

```mermaid
flowchart LR
    A[STOP AUTO] --> B[System OK]
    B --> C[Wejście w tryb ręczny<br/>hasło serwis]
    C --> D{Akcja}
    D --> D1[Transport FWD/REV]
    D --> D2[Obrót CW/CCW/±90°]
    D --> D3[Przedmuch ręczny]
    D --> D4[HOME M1003]
    D --> D5[Test B4 — tylko serwis]
    D1 & D2 & D3 & D4 --> E[HOME przed powrotem AUTO]
    E --> F[START AUTO]
```

### 3.5 Tabela: ekran HMI → akcja operatora → PLC

| Ekran / przycisk | Operator robi | PLC (Vertino) |
|------------------|---------------|---------------|
| GŁÓWNY — START | Start produkcji | M1001 → M70 |
| GŁÓWNY — STOP | Koniec / pauza zmiany | M1002 → RST M70 |
| RESET (żółty) | Po alarmie | M1000 → M200 → N0005 |
| PARAMETRY | Ustawia R1400…R1412 | Walidacja N0006 |
| HOME | Referencja | M1003 → M80 → N0011 |
| Partia C1/R1400 | Obserwacja | C1, R1400 |
| Pozycja modułu | Obserwacja | R1501 (0/90/180/270) |
| Status B4 / zator | Czeka, opróżnia linię | M507, R1507 |
| Tryb ręczny | Serwis | M100, M1010–M1024 |

---

## Powiązane dokumenty

| Dokument | Zawartość |
|----------|-----------|
| [plc/03_program_vertino_sieci.md](plc/03_program_vertino_sieci.md) | Pełna specyfikacja 35 sieci |
| [maszyna.md](maszyna.md) | Opis urządzenia, cykl 360° |
| [operator.md](operator.md) | Instrukcja krok po kroku |
| [plc/mapowanie.md](mapowanie.md) | Mapowanie I/O |
| [receptury.md](receptury.md) | Profile średnic |

---

**© CNC Solutions — Vertino**
