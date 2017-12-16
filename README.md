# Wa-Tor

Wa-Tor population dynamics simulation.

## Qt Checklist

- [ ] vytvářet novou simulaci zadaných rozměrů (prázdnou, náhodně generovanou
      apod., jak chcete)
- [ ] ukládat a načítat simulaci ve formě NumPy matic do/ze souborů dle volby
      uživatele
    - [ ] pokud se to nepovede, musí aplikace zobrazit chybové hlášení
          v grafické podobě (tj. ne jen do konzole)
    - [ ] formát souborů viz zadání
- [ ] prohlížet simulaci v grafické podobě
    - [ ] včetně obrázků ryb a žraloků
    - [ ] pokud se simulace celá nevejde do okna, musí mít posuvníky
    - [ ] zoom (např. <kbd>Ctrl</kbd> + kolečko myši) není nutný,
          ale je příjemný, pro velké odzoomování nahraďte obrázky barvou
- [ ] klást do simulace zvířata (ryby, žraloky) a odebírat je
     (tyto změny se projeví v paměti na úrovni NumPy matice)
    - [ ] kvůli zjednodušení zvažujte pouze situaci, že všichni žraloci mají
          stejnou počáteční energii
    - [ ] "věk" zvířat se při vložení do matice nastaví náhodně
- [ ] klikat na tlačítko *Next chronon*, které provede a vizualizuje jedno
      volání metody `.tick()`
- [ ] měnit parametry simulace mezi klikáním na tlačítko z předchozího bodu
- [ ] nabídka *Help ‣ About* vyvolá okno s informacemi o aplikaci:
    - [ ] název
    - [ ] stručný popis
    - [ ] autor/autoři (vy, případně i my, pokud používáte náš kód)
    - [ ] odkaz na repozitář
    - [ ] informace o licenci (pozor na licenci PyQt!)
    - [ ] pokud používáte public domain grafiku z OpenGameArt.org,
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
