# Wa-Tor

Wa-Tor population dynamics simulation.

## Setup

```bash
$ python -m pip install -r requirements.txt
$ python setup.py develop
$ python -m wator
```

## Qt Checklist

- [x] vytvářet novou simulaci zadaných rozměrů (prázdnou, náhodně generovanou
      apod., jak chcete)
- [x] ukládat a načítat simulaci ve formě NumPy matic do/ze souborů dle volby
      uživatele
    - [x] pokud se to nepovede, musí aplikace zobrazit chybové hlášení
          v grafické podobě (tj. ne jen do konzole)
    - [x] formát souborů viz zadání
- [x] prohlížet simulaci v grafické podobě
    - [x] včetně obrázků ryb a žraloků
    - [x] pokud se simulace celá nevejde do okna, musí mít posuvníky
- [x] klást do simulace zvířata (ryby, žraloky) a odebírat je
     (tyto změny se projeví v paměti na úrovni NumPy matice)
    - [x] kvůli zjednodušení zvažujte pouze situaci, že všichni žraloci mají
          stejnou počáteční energii
    - [x] "věk" zvířat se při vložení do matice nastaví náhodně
- [x] klikat na tlačítko *Next chronon*, které provede a vizualizuje jedno
      volání metody `.tick()`
- [ ] měnit parametry simulace mezi klikáním na tlačítko z předchozího bodu
- [x] nabídka *Help ‣ About* vyvolá okno s informacemi o aplikaci:
    - [x] název
    - [x] stručný popis
    - [x] autor/autoři (vy, případně i my, pokud používáte náš kód)
    - [x] odkaz na repozitář
    - [x] informace o licenci (pozor na licenci PyQt!)
    - [x] pokud používáte public domain grafiku z OpenGameArt.org,
          nemáte právní povinnost zdroj zmínit, ale považujeme to za slušnost

## References

- [assigment numpy](
https://github.com/cvut/MI-PYT/blob/master/tutorials/05_numpy.md
)
- [assigment cython](
https://github.com/cvut/MI-PYT/blob/master/tutorials/07_cython.md
)
- [assigment qt](
https://github.com/cvut/MI-PYT/blob/master/tutorials/09_pyqt.md
)
- [Wikipedia](https://en.wikipedia.org/wiki/Wa-Tor)
