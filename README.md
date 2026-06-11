# Stacja kontroli opakowań (SKO)

Stacja oczyszczania słoików przedmuchem pneumatycznym — moduł obrotowy odwraca
partie słoików dnem do góry nad strefą przedmuchu.

**Sterownik:** FATEK HB1-14MBJ25 | **Panel:** FATEK P2043NA/P2043EA | **Bezpieczeństwo:** Pilz PNOZ X7

## Struktura projektu

```
├── dokumentacja/         ← pełna dokumentacja (maszyna, operator, PLC, HMI)
├── plc/                  ← SKO-Program.pdw (WinProLadder) + wydruk PDF
│   └── export/           ← komentarze, drabinka, tabele serwo
├── hmi/                  ← projekt panelu (FvDesigner, .fpj)
├── schemat_elektryczny/  ← QElectroTech (SKO.qet / SKO.pdf)
├── referencje/           ← podręczniki Fatek (PL), karta napędu SH-D08R
└── media/                ← rendery CAD, zdjęcia, film z linii
```

## Dokumentacja

**Pakiet dla klienta:** [dokumentacja/DOKUMENTACJA_KLIENTA.md](dokumentacja/DOKUMENTACJA_KLIENTA.md)

- Instrukcja obsługi: [dokumentacja/instrukcja_obslugi.md](dokumentacja/instrukcja_obslugi.md)
- Bezpieczeństwo · serwis · dane techniczne · protokół odbioru — [dokumentacja/README.md](dokumentacja/README.md)

Techniczna (PLC/HMI): [dokumentacja/plc/program.md](dokumentacja/plc/program.md) · [dokumentacja/hmi.md](dokumentacja/hmi.md)

## Program PLC

| Plik | Opis |
|------|------|
| [plc/SKO-Program.pdw](plc/SKO-Program.pdw) | Projekt WinProLadder (źródło) |
| [plc/SKO-Program.pdf](plc/SKO-Program.pdf) | Wydruk programu — podstawa dokumentacji |
| [plc/export/comment.txt](plc/export/comment.txt) | Komentarze symboli |
| [plc/export/tabele.tab](plc/export/tabele.tab) | Tabele serwo |

## I/O (skrót)

| Adres | Funkcja |
|-------|---------|
| X0 | Pilz — obwód bezpieczeństwa |
| X1 | B1 — liczenie słoików (zbocze opadające) |
| X2 | B2 — baza serwo (DOG) |
| X3 | B3 — spiętrzenie na wyjściu (pauza) |
| Y1 | Napęd transportu |
| Y2/Y3 | Serwo modułu — PLS/DIR (PSO1) |
| Y4 | Zawór przedmuchu |

---

**CNC Solutions — Michał Batorowicz**
