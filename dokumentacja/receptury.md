# Receptury — Vertino (profile opakowań)

**Źródło wymiarów:** [srednice_slokow.txt](srednice_slokow.txt)

Średnica [mm] określa przezbrojenie mechaniczne. **R1400** = liczba słoików w partii (1–10) — ustawiana na HMI zgodnie z pojemnością modułu dla danego formatu.

| Profil | Średnica [mm] | R1400 (szac./do kalibracji) | Uwagi |
|--------|---------------|-----------------------------|--------|
| 1 | 75 | Do ustalenia na maszynie | Najmniejszy format |
| 2 | 100 | 4 | Przykład z instrukcji operatora |
| 3 | 120 | Do ustalenia | |
| 4 | 200 | Do ustalenia | |
| 5 | 250 | Do ustalenia | |
| 6 | 500 | Do ustalenia | |
| 7 | 750 | Do ustalenia | Największy format |

## Procedura przezbrojenia

1. Wymiana uchwytów i prowadnic pod średnicę.
2. Ustaw **R1400** na HMI (liczba słoików mieszczących się w module obrotowym).
3. Wykonaj **HOME** (M1003 / automatyczny).
4. Testowa partia — sprawdź C1, pozycjonowanie B1/B2.
5. Zapisz parametry w dzienniku zmiany.

## Wdrożenie w PLC (P1 z audytu)

Docelowo: tablica receptur na HMI (7 profili) → zapis do R1400 (+ ewentualnie R1401–R1403 per profil). Patrz [plc/audyt.md](audyt.md).

**© CNC Solutions — Michał Batorowicz**
