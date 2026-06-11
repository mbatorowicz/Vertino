# Dokumentacja — Stacja kontroli opakowań

---

## Dokumentacja dla klienta (dostawa z maszyną)

**Spis i instrukcja pakowania:** [DOKUMENTACJA_KLIENTA.md](DOKUMENTACJA_KLIENTA.md)

| Dokument | Plik |
|----------|------|
| Instrukcja obsługi | [instrukcja_obslugi.md](instrukcja_obslugi.md) |
| Bezpieczeństwo | [bezpieczenstwo.md](bezpieczenstwo.md) |
| Opis maszyny | [maszyna.md](maszyna.md) |
| Instrukcja serwisowa | [instrukcja_serwisowa.md](instrukcja_serwisowa.md) |
| Dane techniczne | [dane_techniczne.md](dane_techniczne.md) |
| Protokół odbioru | [odbior_uruchomienie.md](odbior_uruchomienie.md) |

Skrót dla operatora: [operator.md](operator.md).

---

## Dokumentacja techniczna (PLC / HMI)

Opis programu w sterowniku (31 sieci, 2026-06):
[plc/SKO-Program.pdf](../plc/SKO-Program.pdf).

| Dokument | Zawartość |
|----------|-----------|
| [plc/program.md](plc/program.md) | Sieci N0000–N0030, diagram stanów |
| [plc/mapa_io.md](plc/mapa_io.md) | I/O, rejestry |
| [plc/serwo.md](plc/serwo.md) | Oś PSO1, HOME, ROTATE |
| [hmi.md](hmi.md) | Interfejs PLC ↔ HMI |

---

## Dokumentacja wewnętrzna (wykonawca)

| Dokument | Zawartość |
|----------|-----------|
| [plc/propozycja_rozbudowy.md](plc/propozycja_rozbudowy.md) | Specyfikacja rozbudowy PLC |
| [hmi_wdrozenie.md](hmi_wdrozenie.md) | Wdrożenie panelu w FvDesigner |

---

## Aktualizacja po zmianie programu

1. Wydruk PLC → `plc/SKO-Program.pdf`
2. Eksport → `plc/export/`
3. Uzupełnij wersję w [DOKUMENTACJA_KLIENTA.md](DOKUMENTACJA_KLIENTA.md) i protokole odbioru
4. Zaktualizuj dokumenty, których dotyczy zmiana

**© CNC Solutions — Michał Batorowicz**
