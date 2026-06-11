# Dokumentacja dostarczana z maszyną

**Urządzenie:** Stacja kontroli opakowań (oczyszczanie przedmuchem)
**Numer projektu:** SKO
**Wykonawca:** CNC Solutions — Michał Batorowicz
**Klient:** _________________________
**Data odbioru:** _________________________

---

## Spis dokumentów

Poniższy zestaw stanowi **komplet dokumentacji użytkowej i serwisowej** przekazywany klientowi wraz z maszyną.

### Dokumenty główne (drukowane — zalecany segregator)

| Lp. | Dokument | Plik | Dla kogo |
|-----|----------|------|----------|
| 1 | **Instrukcja obsługi** | [instrukcja_obslugi.md](instrukcja_obslugi.md) | Operator |
| 2 | **Instrukcja bezpieczeństwa** | [bezpieczenstwo.md](bezpieczenstwo.md) | Operator, serwis |
| 3 | **Opis maszyny i cyklu pracy** | [maszyna.md](maszyna.md) | Operator, serwis |
| 4 | **Instrukcja serwisowa** | [instrukcja_serwisowa.md](instrukcja_serwisowa.md) | Serwis |
| 5 | **Dane techniczne** | [dane_techniczne.md](dane_techniczne.md) | Serwis, utrzymanie ruchu |
| 6 | **Protokół odbioru i uruchomienia** | [odbior_uruchomienie.md](odbior_uruchomienie.md) | Klient + wykonawca |
| 7 | **Średnice obsługiwanych słoików** | [srednice_slokow.txt](srednice_slokow.txt) | Operator |

### Załączniki techniczne (PDF / nośnik USB)

| Lp. | Załącznik | Lokalizacja w projekcie |
|-----|-----------|------------------------|
| A | Schemat elektryczny | [schemat_elektryczny/SKO.pdf](../schemat_elektryczny/SKO.pdf) |
| B | Program PLC — wydruk | [plc/SKO-Program.pdf](../plc/SKO-Program.pdf) |
| C | Karta napędu transportu SH-D08R | [referencje/napedy/SH-D08R.pdf](../referencje/napedy/SH-D08R.pdf) |
| D | Zdjęcia / film z linii | folder [media/](../media/) |
| E | Projekt panelu HMI | [hmi/SKO - Program 1.fpj](../hmi/SKO%20-%20Program%201.fpj) (kopia na USB) |

### Dokumentacja wewnętrzna (NIE przekazywać klientowi)

| Plik | Przeznaczenie |
|------|---------------|
| [plc/propozycja_rozbudowy.md](plc/propozycja_rozbudowy.md) | Specyfikacja wdrożenia PLC |
| [hmi_wdrozenie.md](hmi_wdrozenie.md) | Instrukcja programowania panelu |
| [plc/program.md](plc/program.md), [mapa_io.md](plc/mapa_io.md) | Szczegóły programu dla integratora |

> Szczegółowy opis programu sterownika można przekazać klientowi **na życzenie**
> jako załącznik serwisowy (pliki w `dokumentacja/plc/`).

---

## Wersje oprogramowania

| Element | Wersja / data | Uwagi |
|---------|---------------|-------|
| Program PLC | _____________ | Zgodny z [plc/SKO-Program.pdf](../plc/SKO-Program.pdf) |
| Panel HMI | _____________ | Projekt [hmi/SKO - Program 1.fpj](../hmi/SKO%20-%20Program%201.fpj) |
| Dokumentacja | 2026-06 | Zestaw zgodny z powyższą tabelą |

Przy każdej aktualizacji oprogramowania uzupełnij wersję w protokole odbioru
i przekaż klientowi zaktualizowany wydruk PLC (załącznik B).

---

## Zalecany układ segregatora

```
Segregator „Stacja kontroli opakowań SKO”
├── 1. Instrukcja bezpieczeństwa          (obowiązkowo przy maszynie — kopia)
├── 2. Instrukcja obsługi
├── 3. Opis maszyny
├── 4. Instrukcja serwisowa
├── 5. Dane techniczne
├── 6. Protokół odbioru (podpisany)
├── 7. Średnice słoików
└── Kieszeń: schemat elektryczny (A4/A3)
```

**Nośnik USB** (przyklejony w szafie sterowniczej): PDF schematu, wydruk PLC,
projekt HMI, zdjęcia, ewentualnie film z media/.

---

## Kontakt serwisowy

| | |
|---|---|
| Wykonawca | CNC Solutions — Michał Batorowicz |
| Telefon | _________________________ |
| E-mail | _________________________ |

---

**© CNC Solutions — Michał Batorowicz**
