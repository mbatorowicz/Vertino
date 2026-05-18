# Dokumentacja — Vertino

**Vertino — Stacja oczyszczania opakowań**  
**Sterownik:** FATEK HB1-14MBJ25 | **HMI:** P5043NB | **Bezpieczeństwo:** Pilz PNOZ X7

**[KONWENCJE_NAZEWNICTWA.md](KONWENCJE_NAZEWNICTWA.md)** — jak odróżnić stan w sterowniku od planu.  
**[plc/STAN_FAKTYCZNY.md](plc/STAN_FAKTYCZNY.md)** — co jest wgrane w PLC **dziś**.

---

## Dokumenty

| Dokument | Opis |
|----------|------|
| [mapy_procesu.md](mapy_procesu.md) | Diagramy (plan PLC + proces + operator) |
| [maszyna.md](maszyna.md) | Urządzenie, cykl, B4 |
| [operator.md](operator.md) | Instrukcja operatora |
| [serwis.md](serwis.md) | Serwis |
| [techniczna.md](techniczna.md) | Hardware, HMI |
| [receptury.md](receptury.md) | Profile średnic |
| [srednice_slokow.txt](srednice_slokow.txt) | Wymiary [mm] |

### PLC — [plc/](plc/)

| Dokument | Stan |
|----------|------|
| **[STAN_FAKTYCZNY.md](plc/STAN_FAKTYCZNY.md)** | **W sterowniku (78 sieci)** |
| [program.md](plc/program.md) | Skrócony indeks |
| [mapowanie.md](plc/mapowanie.md) | I/O, rejestry |
| [lista_sieci.md](plc/lista_sieci.md) | Spis N0000–N0077 |
| [sieci/](plc/sieci/) | Opis każdej sieci (eksport PDF) |
| [indeks_krzyzowy.md](plc/indeks_krzyzowy.md) | Adres → sieć |
| [mnemotechniki.txt](plc/mnemotechniki.txt) | Listing |
| [audyt.md](plc/audyt.md) | Luki, rekomendacje |
| [wdrozenie_drabinka_A0_A1.md](plc/wdrozenie_drabinka_A0_A1.md) | Patch w 78 sieciach (opcja) |
| [01_analiza_programu_produkcyjnego.md](plc/01_analiza_programu_produkcyjnego.md) | Wymagania vs produkcja |
| **[03_program_vertino_sieci.md](plc/03_program_vertino_sieci.md)** | **Plan — 35 sieci (nie w PLC)** |

---

## Pliki projektu

| Ścieżka | Opis |
|---------|------|
| [../plc/SKO-Program.pdw](../plc/SKO-Program.pdw) | Program w sterowniku |
| [../plc/SKO-Program.pdf](../plc/SKO-Program.pdf) | Eksport PDF |
| [../plc/export/comments.txt](../plc/export/comments.txt) | Komentarze symboli |

Regeneracja opisów sieci z PDF: `python narzedzia/generuj_dokumentacje.py`

---

**© CNC Solutions — Michał Batorowicz**
