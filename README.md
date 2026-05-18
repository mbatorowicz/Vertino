# Vertino — Stacja oczyszczania opakowań

Sterownik: **FATEK HB1-14MBJ25** | Panel: **P5043NB** | Bezpieczeństwo: **Pilz PNOZ X7**
## Struktura projektu

```
Vertino/                    # folder projektu (nazwa katalogu może być historyczna)
├── dokumentacja/       ← dokumentacja (jeden zestaw plików)
├── plc/                  ← jeden program: SKO-Program.pdw / .pdf
│   └── export/           ← komentarze, drabinka, tabele serwo
├── hmi/                  ← panel P5043NB
├── schemat_elektryczny/  ← QElectroTech
├── referencje/           ← Fatek, napędy
├── mechanika/
├── media/
└── narzedzia/            ← generuj_dokumentacje.py
```

## Dokumentacja

**[dokumentacja/README.md](dokumentacja/README.md)** — Vertino: maszyna, operator, serwis, PLC, mapy procesu.

## Program PLC

| Plik | Opis |
|------|------|
| [plc/SKO-Program.pdw](plc/SKO-Program.pdw) | Projekt WinProLadder |
| [plc/SKO-Program.pdf](plc/SKO-Program.pdf) | Wydruk programu |
| [plc/export/comments.txt](plc/export/comments.txt) | Komentarze symboli |

Mapowanie I/O: [dokumentacja/plc/mapowanie.md](dokumentacja/plc/mapowanie.md)

**PLC:** [program produkcyjny 78 sieci](dokumentacja/plc/01_odszyfrowanie_starego_programu.md) · **[program docelowy 35 sieci](dokumentacja/plc/03_program_vertino_sieci.md)** · [mapy](dokumentacja/mapy_procesu.md)

## Wejścia PLC (skrót)

| Wejście | Czujnik |
|---------|---------|
| X0 | Pilz — bezpieczeństwo |
| X1 | B1 — bariera US |
| X2 | B2 — wyjście |
| X3 | B3 — HOME 0° |
| X4 | B4 — zator linii odbiorczej |

---

**CNC Solutions — Michał Batorowicz**

Nazewnictwo: [dokumentacja/KONWENCJE_NAZEWNICTWA.md](dokumentacja/KONWENCJE_NAZEWNICTWA.md).
