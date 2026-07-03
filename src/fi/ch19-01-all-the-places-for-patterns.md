## Kaikki paikat, joissa malleja voidaan käyttää

Mallit esiintyvät monissa paikoissa Rustissa, ja olet käyttänyt niitä paljon huomaamattasi! Tässä osiossa käsitellään kaikkia paikkoja, joissa mallit ovat sallittuja.

### `match`-haarat

Kuten käsittelimme luvussa 6, käytämme malleja `match`-lausekkeiden haaroissa.
Muodollisesti `match`-lausekkeet määritellään avainsanalla `match`, arvolla, jota
vasten verrataan, ja yhdellä tai useammalla match-haaralla, jotka koostuvat
mallista ja lausekkeesta, joka suoritetaan, jos arvo vastaa kyseisen haaran
mallia, näin:

<!--
  Manually formatted rather than using Markdown intentionally: Markdown does not
  support italicizing code in the body of a block like this!
-->

<pre><code>match <em>VALUE</em> {
    <em>PATTERN</em> => <em>EXPRESSION</em>,
    <em>PATTERN</em> => <em>EXPRESSION</em>,
    <em>PATTERN</em> => <em>EXPRESSION</em>,
}</code></pre>

Esimerkiksi tässä on `match`-lauseke listauksesta 6-5, joka vertaa muuttujan
`x` `Option<i32>`-arvoa:

```rust,ignore
match x {
    None => None,
    Some(i) => Some(i + 1),
}
```

Tämän `match`-lausekkeen mallit ovat `None` ja `Some(i)` kunkin nuolen vasemmalla
puolella.

Yksi `match`-lausekkeiden vaatimuksista on, että niiden täytyy olla
tyhjentäviä siinä mielessä, että kaikki `match`-lausekkeen arvon
mahdollisuudet on käsiteltävä. Yksi tapa varmistaa, että olet kattanut
jokaisen mahdollisuuden, on käyttää viimeisessä haarassa catch-all-mallia:
Esimerkiksi mikä tahansa arvo vastaa muuttujan nimeä eikä voi koskaan epäonnistua,
joten se kattaa kaikki jäljellä olevat tapaukset.

Erityinen malli `_` vastaa mitä tahansa, mutta se ei koskaan sido muuttujaan,
joten sitä käytetään usein viimeisessä match-haarassa. `_`-malli voi olla
hyödyllinen, kun haluat jättää huomiotta minkä tahansa määrittelemättömän
arvon, esimerkiksi. Käsittelemme `_`-mallin tarkemmin kohdassa [”Arvojen
huomiotta jättäminen mallissa”][ignoring-values-in-a-pattern]<!-- ignore -->
myöhemmin tässä luvussa.

### `let`-lauseet

Ennen tätä lukua olemme käsitelleet eksplisiittisesti vain mallien käyttöä
`match`- ja `if let` -rakenteissa, mutta itse asiassa olemme käyttäneet malleja
myös muissa paikoissa, mukaan lukien `let`-lauseissa. Harkitse esimerkiksi tätä
suoraviivaista muuttujan sijoittamista `let`-lauseella:

```rust
let x = 5;
```

Joka kerta kun olet käyttänyt tällaista `let`-lausetta, olet käyttänyt malleja,
vaikka et ehkä ole tajunnut sitä! Muodollisesti `let`-lause näyttää tältä:

<!--
  Manually formatted rather than using Markdown intentionally: Markdown does not
  support italicizing code in the body of a block like this!
-->

<pre>
<code>let <em>PATTERN</em> = <em>EXPRESSION</em>;</code>
</pre>

Lausekkeissa kuten `let x = 5;`, joissa PATTERN-paikalla on muuttujan nimi,
muuttujan nimi on vain erityisen yksinkertainen muoto mallista. Rust vertaa
lauseketta malliin ja sijoittaa löytämänsä nimet. Esimerkissä `let x = 5;`
`x` on malli, joka tarkoittaa ”sido tähän vastaava arvo muuttujaan `x`”.
Koska nimi `x` on koko malli, tämä malli käytännössä tarkoittaa ”sido kaikki
muuttujaan `x`, mikä arvo tahansa onkin.”

Nähdäksemme `let`-lauseen mallinmukaisuuspuolen selkeämmin, tarkastele
listaus 19-1, joka käyttää mallia `let`-lauseessa purkaakseen tuplen.


<Listing number="19-1" caption="Mallin käyttö tuplen purkamiseen ja kolmen muuttujan luomiseen kerralla">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-01/src/main.rs:here}}
```

</Listing>

Tässä vertaamme tuplea malliin. Rust vertaa arvoa `(1, 2, 3)` malliin
`(x, y, z)` ja näkee, että arvo vastaa mallia — eli elementtien määrä on
sama molemmissa — joten Rust sitoo `1`:n muuttujaan `x`, `2`:n muuttujaan `y`
ja `3`:n muuttujaan `z`. Voit ajatella tämän tuple-mallin sisältävän kolme
yksittäistä muuttujamallia sisäkkäin.

Jos mallin elementtien määrä ei vastaa tuplen elementtien määrää, kokonaistyyppi
ei vastaa ja saamme kääntäjävirheen. Esimerkiksi listaus 19-2 näyttää yrityksen
purkaa kolmielementtisen tuplen kahteen muuttujaan, mikä ei toimi.

<Listing number="19-2" caption="Virheellinen malli, jonka muuttujien määrä ei vastaa tuplen elementtien määrää">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-02/src/main.rs:here}}
```

</Listing>

Tämän koodin kääntäminen tuottaa seuraavan tyyppivirheen:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-02/output.txt}}
```

Virheen korjaamiseksi voisimme jättää yhden tai useamman tuplen arvoista
huomiotta käyttämällä `_` tai `..`, kuten näet kohdassa [”Arvojen huomiotta
jättäminen mallissa”][ignoring-values-in-a-pattern]<!-- ignore -->. Jos ongelma
on, että mallissa on liikaa muuttujia, ratkaisu on saada tyypit vastaamaan
toisiaan poistamalla muuttujia niin, että muuttujien määrä vastaa tuplen
elementtien määrää.

### Ehdolliset `if let` -lausekkeet

Luvussa 6 käsittelimme, miten `if let` -lausekkeita käytetään pääasiassa
lyhyempänä tapana kirjoittaa vastaava `match`, joka vastaa vain yhtä tapausta.
Valinnaisesti `if let` -lausekkeella voi olla vastaava `else`, joka sisältää
koodin, joka suoritetaan, jos `if let` -lausekkeen malli ei vastaa.

Listaus 19-3 osoittaa, että on myös mahdollista yhdistellä `if let`-,
`else if`- ja `else if let` -lausekkeita. Näin saamme enemmän joustavuutta
kuin `match`-lausekkeella, jossa voimme vertailla vain yhtä arvoa malleihin.
Lisäksi Rust ei vaadi, että `if let`-, `else if`- ja `else if let` -haarojen
sarjan ehdot liittyisivät toisiinsa.

Listauksen 19-3 koodi määrittää taustavärin useiden ehtojen tarkistusten
perusteella. Tässä esimerkissä olemme luoneet muuttujat kovakoodatuilla
arvoilla, jotka oikea ohjelma saattaisi saada käyttäjän syötteestä.

<Listing number="19-3" file-name="src/main.rs" caption="`if let`-, `else if`-, `else if let`- ja `else`-rakenteiden yhdistäminen">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-03/src/main.rs}}
```

</Listing>

Jos käyttäjä määrittää suosikkivärin, sitä käytetään taustavärinä.
Jos suosikkiväriä ei ole määritelty ja tänään on tiistai, taustaväri on
vihreä. Muussa tapauksessa, jos käyttäjä antaa ikänsä merkkijonona ja
voimme jäsentää sen numeroksi onnistuneesti, väri on joko violetti tai
oranssi riippuen luvun arvosta. Jos mikään näistä ehdoista ei täyty,
taustaväri on sininen.

Tämä ehdollinen rakenne mahdollistaa monimutkaisten vaatimusten tukemisen.
Tässä olevilla kovakoodatuilla arvoilla tämä esimerkki tulostaa
`Using purple as the background color`.

Näet, että `if let` voi myös esitellä uusia muuttujia, jotka varjostavat
olemassa olevia muuttujia samalla tavalla kuin `match`-haarat: rivi
`if let Ok(age) = age` esittelee uuden `age`-muuttujan, joka sisältää
`Ok`-variantin sisällä olevan arvon varjostaen olemassa olevan `age`-muuttujan.
Tämä tarkoittaa, että ehdon `if age > 30` täytyy sijoittaa kyseisen lohkon
sisään: emme voi yhdistää näitä kahta ehtoa muotoon `if let Ok(age) = age &&
age > 30`. Uusi `age`, jota haluamme verrata lukuun 30, ei ole voimassa ennen
kuin uusi alue alkaa aaltosulkeilla.

`if let` -lausekkeiden haittapuoli on, että kääntäjä ei tarkista
tyhjentävyyttä, kun taas `match`-lausekkeissa se tekee niin. Jos jättäisimme
pois viimeisen `else`-lohkon ja siten jättäisimme käsittelemättä joitakin
tapauksia, kääntäjä ei varoittaisi meitä mahdollisesta logiikkavirheestä.

### Ehdolliset `while let` -silmukat

Rakenteeltaan samankaltainen kuin `if let`, ehdollinen `while let` -silmukka
sallii `while`-silmukan toimia niin kauan kuin malli vastaa edelleen.
Listauksessa 19-4 näytämme `while let` -silmukan, joka odottaa säikeiden
välillä lähetettyjä viestejä, mutta tässä tapauksessa tarkistaa `Result`-arvon
`Option`-arvon sijaan.

<Listing number="19-4" caption="`while let` -silmukan käyttö arvojen tulostamiseen niin kauan kuin `rx.recv()` palauttaa `Ok`-arvon">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-04/src/main.rs:here}}
```

</Listing>

Tämä esimerkki tulostaa `1`, `2` ja sitten `3`. `recv`-metodi ottaa ensimmäisen
viestin kanavan vastaanottopuolelta ja palauttaa `Ok(value)`-arvon. Kun näimme
`recv`-metodin ensimmäisen kerran luvussa 16, purimme virheen suoraan tai
käytimme sitä iteraattorina `for`-silmukassa. Kuten listaus 19-4 osoittaa,
voimme kuitenkin käyttää myös `while let` -rakennetta, koska `recv`-metodi
palauttaa `Ok`-arvon aina kun viesti saapuu niin kauan kuin lähettäjä on
olemassa, ja tuottaa sitten `Err`-arvon, kun lähettäjäpuoli katkaisee yhteyden.

### `for`-silmukat

`for`-silmukassa avainsanaa `for` seuraava arvo on malli. Esimerkiksi
lausekkeessa `for x in y` arvo `x` on malli. Listaus 19-5 osoittaa, miten
mallia käytetään `for`-silmukassa purkamaan eli erottelemaan tuplen osiin
osana `for`-silmukkaa.


<Listing number="19-5" caption="Mallin käyttö `for`-silmukassa tuplen purkamiseen">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-05/src/main.rs:here}}
```

</Listing>

Listauksen 19-5 koodi tulostaa seuraavan:


```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-05/output.txt}}
```

Mukautamme iteraattoria `enumerate`-metodilla niin, että se tuottaa arvon ja
kyseisen arvon indeksin tuplena. Ensimmäinen tuotettu arvo on tuple
`(0, 'a')`. Kun tämä arvo vastaa mallia `(index, value)`, `index` on `0` ja
`value` on `'a'`, mikä tulostaa tulosteen ensimmäisen rivin.


### Funktioiden parametrit

Funktioiden parametrit voivat myös olla malleja. Listauksen 19-6 koodi, joka
määrittelee funktion nimeltä `foo`, jolla on yksi parametri nimeltä `x` tyypiltään
`i32`, pitäisi nyt näyttää tutulta.

<Listing number="19-6" caption="Funktioallekirjoitus, jossa parametreissa käytetään malleja">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-06/src/main.rs:here}}
```

</Listing>

Osa `x` on malli! Kuten `let`-lauseessa, voimme vastata tuplea funktion
argumenteissa malliin. Listaus 19-7 erottelee tuplen arvot, kun välitämme
sen funktiolle.

<Listing number="19-7" file-name="src/main.rs" caption="Funktio, jonka parametrit purkavat tuplen">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-07/src/main.rs}}
```

</Listing>

Tämä koodi tulostaa `Current location: (3, 5)`. Arvot `&(3, 5)` vastaavat
mallia `&(x, y)`, joten `x` on arvo `3` ja `y` on arvo `5`.

Voimme käyttää malleja myös sulkeumien parametri listoissa samalla tavalla
kuin funktioiden parametri listoissa, koska sulkeumat ovat samankaltaisia
kuin funktiot, kuten käsittelimme luvussa 13.

Tähän mennessä olet nähnyt useita tapoja käyttää malleja, mutta mallit eivät
toimi samalla tavalla kaikissa paikoissa, joissa niitä voi käyttää. Joissakin
paikoissa mallien täytyy olla kiistämättömiä; toisissa olosuhteissa ne voivat
olla kumottavia. Käsittelemme nämä kaksi käsitettä seuraavaksi.

[ignoring-values-in-a-pattern]: ch19-03-pattern-syntax.html#ignoring-values-in-a-pattern
