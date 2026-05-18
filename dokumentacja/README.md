# Dokumentacja — Vertino

**Vertino — Stacja oczyszczania opakowań**  
**Sterownik:** FATEK HB1-14MBJ25 | **HMI:** P5043NB | **Bezpieczeństwo:** Pilz PNOZ X7

Jedna dokumentacja projektu (operator, serwis, PLC, techniczna, receptury).  
**Nazewnictwo:** [KONWENCJE_NAZEWNICTWA.md](KONWENCJE_NAZEWNICTWA.md) (Vertino vs nazwy plików SKO-*).

---

## Spis treści

| Dokument | Odbiorca | Opis |
|----------|----------|------|
| [mapy_procesu.md](mapy_procesu.md) | Wszyscy | Mapa programu PLC, drzewo procesu, przepływ operatora |
| [maszyna.md](maszyna.md) | Wszyscy | Przeznaczenie, cykl 360°, B4, parametry R |
| [operator.md](operator.md) | Operator | Uruchomienie, HMI, alarmy, dziennik |
| [serwis.md](serwis.md) | Serwis | Diagnostyka, kalibracja, konserwacja |
| [techniczna.md](techniczna.md) | Producent / integrator | Hardware, Modbus, HMI |
| [receptury.md](receptury.md) | Operator / serwis | 7 profili średnic → R1400 |
| [srednice_slokow.txt](srednice_slokow.txt) | — | Wymiary słoików [mm] |

### Program PLC — [plc/](plc/)

| Dokument | Opis |
|----------|------|
| [01_odszyfrowanie_starego_programu.md](plc/01_odszyfrowanie_starego_programu.md) | **Rozszyfrowanie** starego programu — wszystkie 78 sieci |
| [02_program_nowy_sieci.md](plc/02_program_nowy_sieci.md) | Szkic nowego programu — 33 sieci |
| [03_program_vertino_sieci.md](plc/03_program_vertino_sieci.md) | **Program docelowy Vertino** — 35 sieci |
| [program.md](program.md) | Architektura, porównanie wersji |
| [mapowanie.md](mapowanie.md) | X/Y, M, R, D, C, T |
| [lista_sieci.md](lista_sieci.md) | Spis sieci |
| [indeks_krzyzowy.md](plc/indeks_krzyzowy.md) | Adres → sieć |
| [audyt.md](audyt.md) | Stan programu, rekomendacje A0/A1/P1 |
| [mnemotechniki.txt](plc/mnemotechniki.txt) | Listing WinProLadder |
| [sieci/](plc/sieci/) | Opis każdej sieci |

---

## Pliki projektu

| Ścieżka | Opis |
|---------|------|
| [../plc/SKO-Program.pdf](../plc/SKO-Program.pdf) | Eksport WinProLadder (79 str.) |
| [../plc/SKO-Program.pdw](../plc/SKO-Program.pdw) | Projekt sterownika |
| [../plc/export/comments.txt](../plc/export/comments.txt) | Komentarze symboli |
| [../schemat_elektryczny/](../schemat_elektryczny/) | Schemat QET |
| [../hmi/](../hmi/) | Projekt panelu P5043NB |

## Regeneracja opisów sieci z PDF

```bash
python narzedzia/generuj_dokumentacje.py
```

---

**© CNC Solutions — Michał Batorowicz**
