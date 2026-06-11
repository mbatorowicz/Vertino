# Instrukcja obsługi — Stacja kontroli opakowań

**Wersja dokumentu:** 1.0 | **Data:** 2026-06
**Urządzenie:** stacja oczyszczania słoików przedmuchem pneumatycznym

---

## 1. Przeznaczenie

Maszyna do **oczyszczania opakowań szklanych** przedmuchem sprężonego powietrza. Słoiki wjeżdżają w rzędzie, są zliczane,
partiami odwracane w module obrotowym i przedmuchiwane. Stacja pracuje w linii
produkcyjnej przed napełnieniem.

Szczegółowy opis budowy: [maszyna.md](maszyna.md).

---

## 2. Wymagania wobec operatora

- Przeszkolenie z niniejszej instrukcji i [bezpieczenstwo.md](bezpieczenstwo.md).
- Znajomość obsługi panelu dotykowego i procedur awaryjnych.
- W linii farmaceutycznej — stosowanie procedur GMP obowiązujących u klienta.

---

## 3. Panel operatorski (HMI)

**Panel:** FATEK 4,3" dotykowy, montowany przy stanowisku.

### 3.1 Ekran główny (RUN)

| Element | Znaczenie |
|---------|-----------|
| **READY** | Maszyna gotowa do startu (zatrzymana, brak alarmu) |
| **RUN** | Praca automatyczna w toku |
| **ALARM** | Błąd — wymagany RESET po usunięciu przyczyny |
| **HOME_OK** | Moduł obrotowy zbazowany |
| Licznik **X / Y** | X = sztuki w bieżącej partii, **Y = ilość w partii (cel)** — operator ustawia Y **klikając w wartość** na ekranie głównym (wyskakuje klawiatura numeryczna) |
| **Liczenie** | Zezwolenie zliczania słoików (w produkcji: WŁ.) |
| **Powietrze** | Zezwolenie przedmuchu (w produkcji: WŁ.) |
| **PAUZA B3** | Żółta lampka — słoik zbyt długo przy czujniku wyjścia, maszyna czeka |
| **START** | Rozpoczęcie pracy |
| **STOP** | Zatrzymanie pracy |
| **RESET** | Kasowanie alarmu |
| **HOME** | Bazowanie modułu obrotowego |
| **SET** | Wejście w ustawienia (hasło serwisowe) |

### 3.2 Ekran ustawień (SETUP)

Dostęp chroniony hasłem. Parametry do ustawienia przez serwis lub
upoważnionego operatora:

| Parametr | Opis |
|----------|------|
| Opóźnienie po partii | Czas dojazdu ostatniego słoika do gniazda [× 0,01 s] |
| Czas przejazdu słoika przy B3 | Czas, w którym pojedynczy słoik zasłania czujnik B3 przy normalnym przepływie — jeśli B3 jest zasłonięty dłużej, maszyna wstrzymuje transport (linia odbiorcza nie nadąża) [× 0,01 s] |
| Prędkości / timeouty | Parametry serwisowe — patrz [instrukcja_serwisowa.md](instrukcja_serwisowa.md) |

> **Ilość w partii (R6)** operator ustawia na **ekranie głównym** — klik w prawą liczbę licznika `X / Y`, nie w SETUP.

### 3.3 Ekran alarmów (ALARMY)

Wyświetla **przyczynę** ostatniego alarmu (bezpieczeństwo, timeout bazowania
lub obrotu, błąd napędu modułu, błędna nastawa). Przycisk **RESET** po usunięciu
przyczyny.

### 3.4 Ekran serwisowy (SERWIS)

Tylko dla personelu serwisowego (hasło). Tryb serwisowy, przezbrajanie,
ruchy ręczne — patrz rozdział 8 i [instrukcja_serwisowa.md](instrukcja_serwisowa.md).

---

## 4. Przygotowanie do pracy

1. Sprawdź stan linii — słoiki podawane równomiernie, brak zatorów za stacją.
2. **Wyłącznik główny** — załączony.
3. **Kluczyk serwisowy Pilz** — pozycja **PRODUKCJA**.
4. **Osłona** modułu — **zamknięta i zablokowana**.
5. **E-stop** — odryglowany (obraca się).
6. **RESET** obwodu bezpieczeństwa (przycisk przy szafie / panelu) — jeśli lampka
   bezpieczeństwa tego wymaga.
7. Na panelu: lampka **READY**, **HOME_OK** świeci.
8. **Liczenie** i **Powietrze** — włączone.
9. Na ekranie głównym **kliknij wartość ilości partii** (licznik `X / Y`, prawa liczba) i ustaw liczbę słoików przed obrotem modułu (typowo 4–12; formaty: [srednice_slokow.txt](srednice_slokow.txt)).

---

## 5. Uruchomienie produkcji

1. Wciśnij **HOME** (jeśli HOME_OK nie świeci — np. po włączeniu zasilania).
2. Poczekaj na zakończenie bazowania (HOME_OK).
3. Wciśnij **START** — lampka **RUN**, transport rusza.
4. Obserwuj licznik partii i lampkę **PAUZA B3**.

### Przebieg cyklu (skrót)

Słoiki wjeżdżają → liczenie na czujniku B1 → po osiągnięciu ilości partii krótkie
opóźnienie → **obrót modułu o 90°** (transport stoi) → powrót do liczenia.
Przedmuch działa ciągle podczas pracy. Pełny obrót modułu = 4 kroki × 90°.

---

## 6. Zatrzymanie

| Sytuacja | Działanie |
|----------|-----------|
| Koniec zmiany / przerwa | **STOP** — maszyna zatrzymana, można zostawić zasilanie |
| Awaria / zagrożenie | **E-stop** — natychmiastowy stop, wymaga RESET po odryglowaniu |
| Alarm na panelu | Usuń przyczynę → **RESET** → ewentualnie **HOME** → **START** |

Po **STOP** licznik partii **nie** jest zerowany automatycznie — przy wznowieniu
liczenie trwa od bieżącej wartości. Po **alarmie** licznik może wymagać
skorygowania — skonsultuj z serwisem.

---

## 7. Pauza przy czujniku B3 (wyjście)

Gdy słoik **zbyt długo** zasłania czujnik B3 na wyjściu (dłużej niż nastawa R8),
maszyna **sama zatrzymuje** transport i przedmuch — zwykle dlatego, że linia
odbiorcza nie odbiera słoików w tempie podawania (albo jest rzeczywisty zator).
Lampka **PAUZA B3** świeci. **To nie jest błąd** — po zwolnieniu toru praca
wznawia się bez naciśnięcia START. Licznik partii jest zachowany.

Nastawa R8 to **czas przejazdu jednego słoika obok czujnika B3** przy normalnym
przepływie [× 0,01 s]. Ustawia ją serwis na ekranie SETUP.

Jeśli pauza występuje często — skontaktuj się z serwisem (regulacja R8
lub prędkości linii odbiorczej).

---

## 8. Przezbrajanie (zmiana formatu słoika)

Wymiana tulei / prowadnic w module obrotowym. **Tylko personel serwisowy.**

1. **STOP** maszyny.
2. **Kluczyk Pilz → pozycja SERWIS** (patrz [bezpieczenstwo.md](bezpieczenstwo.md)).
3. Otwórz osłonę modułu.
4. Panel → **SERWIS** → włącz **Tryb serwisowy** → **Tryb przezbrajania**.
5. Ustaw **niską prędkość obrotu** (np. 500).
6. Naciskaj **Obrót przezbrajania +90°** — ustaw moduł w dogodnej pozycji,
   wymień elementy na format docelowy (średnice: [srednice_slokow.txt](srednice_slokow.txt)).
7. Wyłącz tryb przezbrajania i serwisowy.
8. **Kluczyk → PRODUKCJA**, zamknij osłonę.
9. **HOME** → **START** — próba jałowa bez słoików, potem produkcja.

---

## 9. Alarmy — co robić

| Komunikat / sytuacja | Prawdopodobna przyczyna | Postępowanie |
|----------------------|-------------------------|--------------|
| Bezpieczeństwo / E-stop | E-stop, otwarta osłona (prod.), kluczyk | Odrygluj E-stop, zamknij osłonę, RESET Pilz, RESET panel |
| Brak HOME_OK przy START | Brak bazowania | HOME, potem START |
| Błąd bazowania | Moduł zablokowany, czujnik bazy | RESET, sprawdź mechanikę, HOME |
| Błąd obrotu | Zablokowany moduł, słoik w gnieździe | RESET, opróżnij moduł, HOME |
| Timeout obrotu/bazowania | Awaria napędu | Wezwij serwis |
| START nie reaguje | Alarm aktywny, brak HOME, R6=0 | RESET, HOME, ustaw ilość partii > 0 |

Szczegółowa diagnostyka: [instrukcja_serwisowa.md](instrukcja_serwisowa.md).

---

## 10. Czego nie robić

- Nie uruchamiaj produkcji przy **otwartej osłonie** (kluczyk w PRODUKCJI).
- Nie wyłączaj **Liczenia** ani **Powietrza** w produkcji bez zgody serwisu.
- Nie wchodź do strefy ruchu modułu bez trybu serwisowego i kluczyka SERWIS.
- Nie zmieniaj parametrów w SETUP bez szkolenia / upoważnienia.
- Nie ignoruj powtarzających się alarmów obrotu — możliwe uszkodzenie napędu.

---

## 11. Konserwacja operatora (codzienna)

| Czynność | Częstotliwość |
|----------|---------------|
| Wizualna kontrola czystości gniazd modułu | co zmianę |
| Sprawdzenie szczelności przewodów pneumatycznych (syczenie) | co zmianę |
| Usunięcie rozsypanych słoików / zatorów z toru | w razie potrzeby |
| Sprawdzenie działania E-stop (test bez obciążenia) | wg procedury klienta GMP |

Pełna konserwacja: [instrukcja_serwisowa.md](instrukcja_serwisowa.md).

---

## 12. Załączniki

- [bezpieczenstwo.md](bezpieczenstwo.md)
- [maszyna.md](maszyna.md)
- [srednice_slokow.txt](srednice_slokow.txt)
- [dane_techniczne.md](dane_techniczne.md)

---

**© CNC Solutions — Michał Batorowicz**
