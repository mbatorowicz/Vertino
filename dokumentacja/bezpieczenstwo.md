# Instrukcja bezpieczeństwa

**Urządzenie:** Stacja kontroli opakowań SKO
**Obowiązuje:** operatorzy, serwis, konserwacja

Przeczytaj przed pierwszym uruchomieniem. **Kopia niniejszej instrukcji musi być
dostępna przy maszynie** (segregator lub koperta przy panelu).

---

## 1. Ogólne zasady

Maszyna zawiera **elementy ruchome** (transport, moduł obrotowy) i **ciśnienie
pneumatyczne** (przedmuch). Nieprzestrzeganie instrukcji może spowodować
obrażenia ciała lub uszkodzenie urządzenia.

- Obsługę produkcyjną wykonują **wyłącznie przeszkoleni** operatorzy.
- Prace serwisowe — personel z uprawnieniami i przeszkoleniem.
- Strefa maszyny musi być **ograniczona** przed dostępem osób postronnych.

---

## 2. Zagrożenia

| Zagrożenie | Źródło | Środki ochrony |
|------------|--------|----------------|
| Przygniecenie, zaciągnięcie | Transport, moduł obrotowy | Osłona, obwód Pilz, E-stop |
| Cięcie / kontakt z krawędziami | Elementy mechaniczne modułu | Osłona, rękawice przy przezbrajaniu |
| Hałas | Napędy, przedmuch | Słuchawki ochronne (zalecane > 80 dB(A)) |
| Ciśnienie | Przedmuch pneumatyczny | Zawory, odłączenie zasilania powietrza przy serwisie |
| Porażenie prądem | Szafa sterownicza 230 V / 24 V | Blokada wyłącznika głównego, praca pod napięciem tylko przez elektryka |

---

## 3. Obwód bezpieczeństwa

```
E-stop (S1) ──┐
Czujnik osłony B4 ──┼──► Pilz PNOZ X7 ──► zezwolenie napędów + sygnał X0 do PLC
Kluczyk serwisowy ──┘
Przycisk RESET (S2)
```

| Element | Funkcja |
|---------|---------|
| **E-stop (czerwony grzybek)** | Natychmiastowe odcięcie zezwolenia ruchu. Obroć, aby odryglować. |
| **Czujnik osłony B4** (Schneider XCSZC7902) | Magnetyczny — osłona otwarta rozbraja obwód (w trybie PRODUKCJA). |
| **Kluczyk serwisowy Pilz** | **PRODUKCJA:** B4 aktywny. **SERWIS:** B4 pominięty — praca przy otwartej osłonie możliwa tylko w trybie przezbrajania z niską prędkością. |
| **RESET obwodu (S2)** | Po E-stop / otwarciu osłony — reset przekaźnika Pilz. |
| **X0 → PLC** | Status bezpieczeństwa — przy X0=OFF maszyna w ALARM. |

### Pozycje kluczyka serwisowego

| Pozycja | Osłona | Dozwolone |
|---------|--------|-----------|
| **PRODUKCJA** | Musi być zamknięta | Praca automatyczna, serwis przy zamkniętej osłonie |
| **SERWIS** | Może być otwarta | Tylko przezbrajanie (powolny obrót), **nie** produkcja |

**E-stop działa w obu pozycjach klucza.**

---

## 4. Procedury awaryjne

### 4.1 Naciśnięcie E-stop

1. Wszystkie ruchy zatrzymane.
2. Usuń przyczynę (jeśli znana).
3. Odrygluj E-stop.
4. Zamknij osłonę (tryb PRODUKCJA) lub ustaw kluczyk (tryb SERWIS).
5. Naciśnij **RESET** Pilz.
6. Na panelu: **RESET** alarmu.
7. Wykonaj **HOME** przed wznowieniem produkcji.

### 4.2 Wejście w strefę osłony podczas pracy

1. **E-stop** natychmiast.
2. Nie restartuj bez sprawdzenia, czy nikt nie pozostał w strefie.
3. Postępowanie jak w 4.1.

### 4.3 Awaria pneumatyki (syczenie, brak przedmuchu)

1. **STOP** lub E-stop.
2. Odłącz zasilanie powietrzem (zawór główny linii).
3. Wezwij serwis.

---

## 5. Przezbrajanie — bezpieczeństwo

1. **STOP** produkcji.
2. **Kluczyk → SERWIS** (tylko upoważniony personel).
3. Otwórz osłonę.
4. Tryb **przezbrajania** na panelu — **tylko powolny obrót** (+90° krokami).
5. **Nie wkładaj rąk** w gniazda modułu podczas ruchu.
6. Po zakończeniu: wyłącz tryby, **kluczyk → PRODUKCJA**, zamknij osłonę, **HOME**.

---

## 6. Praca pod napięciem

Szafa sterownicza zawiera **230 V AC** i **24 V DC**. Otwieranie szafy —
tylko przez personel z uprawnieniami elektrycznymi. Przed pracą wewnątrz szafy:

1. Wyłącznik główny **OFF** + blokada LOTO (jeśli wymagana u klienta).
2. Zabezpieczenie przed ponownym załączeniem.

---

## 7. Oznakowanie

Na maszynie muszą być czytelne:

- E-stop i RESET
- Wyłącznik główny
- „Elementy ruchome" przy osłonie modułu
- Kierunek podawania słoików (opcjonalnie)

---

## 8. Pozostałości zagrożeń

Mimo zabezpieczeń pozostają:

- Ryzyko przy **ręcznym podawaniu** słoików do modułu (nie stosować w produkcji).
- **Przeciążenie** linii odbiorczej — pauza B3, nie zatrzymanie awaryjne całej linii.
- **Rozbite szkło** — rękawice, zgłoszenie zgodnie z procedurą klienta.

---

**© CNC Solutions — Michał Batorowicz**
