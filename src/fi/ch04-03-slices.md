## Slice-tyyppi

_Slicet_ antavat sinun viitata [kokoelman](ch08-00-common-collections.md) peräkkäiseen
elementtijaksoon koko kokoelman sijaan. Slice on eräänlainen viite, joten sillä ei
ole omistajuutta.

Tässä on pieni ohjelmointiongelma: kirjoita funktio, joka ottaa välilyönneillä erotetun
merkkijonon sanoja ja palauttaa ensimmäisen sanan, jonka se löytää kyseisestä merkkijonosta.
Jos funktio ei löydä välilyöntiä merkkijonosta, koko merkkijonon täytyy olla
yksi sana, joten koko merkkijono pitäisi palauttaa.

Käydään läpi, miten kirjoittaisimme tämän funktion signatuurin käyttämättä
sliceja, jotta ymmärrämme ongelman, jonka slicet ratkaisevat:

```rust,ignore
fn first_word(s: &String) -> ?
```

`first_word`-funktiolla on parametrina `&String`. Emme tarvitse
omistajuutta, joten tämä on hyvä. (Idiomatiisessa Rustissa funktiot eivät ota omistajuutta
argumenteistaan, elleivät sitä tarvitse, ja syyt siihen selviävät
selväksi jatkaessamme!) Mutta mitä meidän pitäisi palauttaa? Meillä ei oikeastaan ole tapaa
puhua merkkijonon osasta. Voisimme kuitenkin palauttaa sanan lopun indeksin,
jonka ilmaisee välilyönti. Kokeillaan sitä, kuten Listauksessa 4-7.

<Listing number="4-7" file-name="src/main.rs" caption="`first_word`-funktio, joka palauttaa tavuintiarvon `String`-parametrin sisällä">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:here}}
```

</Listing>

Koska meidän täytyy käydä `String` läpi elementti kerrallaan ja tarkistaa, onko
arvo välilyönti, muunnamme `String`-mme tavutaulukoksi käyttämällä
`as_bytes`-metodia.

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:as_bytes}}
```

Seuraavaksi luomme iteraattorin tavutaulukon yli käyttämällä `iter`-metodia:

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:iter}}
```

Käsittelemme iteraattoreita yksityiskohtaisemmin [Luvussa 13][ch13]<!-- ignore -->.
Toistaiseksi tiedä, että `iter` on metodi, joka palauttaa jokaisen elementin kokoelmassa
ja että `enumerate` käärii `iter`-metodin tuloksen ja palauttaa jokaisen elementin
osana monikkoa sen sijaan. Monikon ensimmäinen elementti, jonka `enumerate` palauttaa,
on indeksi, ja toinen elementti on viite elementtiin.
Tämä on hieman kätevämpää kuin indeksin laskeminen itse.

Koska `enumerate`-metodi palauttaa monikon, voimme käyttää kuvioita
purkamaan tuon monikon. Käsittelemme kuvioita lisää [Luvussa
6][ch6]<!-- ignore -->. `for`-silmukassa määritämme kuvion, jossa on `i`
monikon indeksille ja `&item` monikon yksittäiselle tavulle.
Koska saamme viitteen elementtiin `.iter().enumerate()`-ketjusta, käytämme
kuviossa `&`-merkkiä.

`for`-silmukan sisällä etsimme välilyöntiä edustavaa tavua
käyttämällä tavuliteraalisyntaksia. Jos löydämme välilyönnin, palautamme sijainnin.
Muuten palautamme merkkijonon pituuden käyttämällä `s.len()`.

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:inside_for}}
```

Meillä on nyt tapa selvittää ensimmäisen sanan lopun indeksi
merkkijonossa, mutta on ongelma. Palautamme `usize`-arvon yksinään, mutta se on
merkityksellinen luku vain `&String`-kontekstissa. Toisin sanoen,
koska se on erillinen arvo `String`-arvosta, ei ole mitään takeita siitä, että se
olisi edelleen kelvollinen tulevaisuudessa. Harkitse Listauksen 4-8 ohjelmaa, joka
käyttää Listauksen 4-7 `first_word`-funktiota.

<Listing number="4-8" file-name="src/main.rs" caption="`first_word`-funktion kutsumisen tuloksen tallentaminen ja `String`-sisällön muuttaminen">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-08/src/main.rs:here}}
```

</Listing>

Tämä ohjelma kääntyy ilman virheitä ja tekisi niin myös, jos käyttäisimme `word`-muuttujaa
`s.clear()`-kutsun jälkeen. Koska `word` ei ole lainkaan yhteydessä `s`-muuttujan tilaan,
`word` sisältää edelleen arvon `5`. Voisimme käyttää arvoa `5` muuttujan `s` kanssa
yrittääksemme poimia ensimmäisen sanan, mutta tämä olisi bugi,
koska `s`-muuttujan sisältö on muuttunut siitä, kun tallensimme arvon `5` muuttujaan `word`.

Huolehtiminen siitä, että `word`-muuttujan indeksi menee epäsynkkaan `s`-muuttujan datan kanssa,
on työlästä ja virhealtista! Näiden indeksien hallinta on vieläkin hauraampaa, jos
kirjoitamme `second_word`-funktion. Sen signatuurin pitäisi näyttää tältä:

```rust,ignore
fn second_word(s: &String) -> (usize, usize) {
```

Nyt seuraamme sekä aloitus- että lopetusindeksiä, ja meillä on vielä enemmän
arvoja, jotka laskettiin tietyn tilan datasta mutta eivät ole lainkaan sidottuja
siihen tilaan. Meillä on kolme toisiinsa liittymätöntä muuttujaa, jotka täytyy
pitää synkassa.

Onneksi Rustilla on ratkaisu tähän ongelmaan: merkkijonoslicet.

### Merkkijonoslicet

_Merkkijonoslice_ on viite `String`-arvon osaan, ja se näyttää tältä:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-17-slice/src/main.rs:here}}
```

Sen sijaan, että viittaisimme koko `String`-arvoon, `hello` on viite
`String`-arvon osaan, joka määritellään ylimääräisessä `[0..5]`-osassa. Luomme slicet
käyttämällä hakasulkeissa olevaa väliä määrittämällä `[aloitusindeksi..lopetusindeksi]`,
missä _`aloitusindeksi`_ on slicen ensimmäinen sijainti ja _`lopetusindeksi`_
on yksi enemmän kuin slicen viimeinen sijainti. Sisäisesti slice-tietorakenne
tallentaa aloitussijainnin ja slicen pituuden, joka
vastaa arvoa _`lopetusindeksi`_ miinus _`aloitusindeksi`_. Eli tapauksessa `let
world = &s[6..11];` `world` olisi slice, joka sisältää osoittimen `s`-arvon indeksin 6 tavuun
pituusarvolla 5.

Kuva 4-7 näyttää tämän kaaviona.

<img alt="Three tables: a table representing the stack data of s, which points
to the byte at index 0 in a table of the string data &quot;hello world&quot; on
the heap. The third table rep-resents the stack data of the slice world, which
has a length value of 5 and points to byte 6 of the heap data table."
src="img/trpl04-07.svg" class="center" style="width: 50%;" />

<span class="caption">Kuva 4-7: Merkkijonoslice viittaa osaan
`String`-arvosta</span>

Rustin `..`-välisyntaksilla, jos haluat aloittaa indeksistä 0, voit jättää pois
arvon kahden pisteen edestä. Toisin sanoen, nämä ovat yhtä suuret:

```rust
let s = String::from("hello");

let slice = &s[0..2];
let slice = &s[..2];
```

Samoin, jos sliceesi sisältää `String`-arvon viimeisen tavun, voit
jättää pois loppunumeron. Tämä tarkoittaa, että nämä ovat yhtä suuret:

```rust
let s = String::from("hello");

let len = s.len();

let slice = &s[3..len];
let slice = &s[3..];
```

Voit myös jättää pois molemmat arvot ottaaksesi slicen koko merkkijonosta. Eli nämä
ovat yhtä suuret:

```rust
let s = String::from("hello");

let len = s.len();

let slice = &s[0..len];
let slice = &s[..];
```

> Huom: Merkkijonoslicen väli-indeksien täytyy olla kelvollisilla UTF-8-merkki
> rajoilla. Jos yrität luoda merkkijonoslicen monitavuisen merkin keskeltä,
> ohjelmasi päättyy virheeseen. Merkkijonoslicien esittelyä varten
> oletamme tässä osiossa vain ASCII-merkkejä; UTF-8-käsittelyn
> tarkempi käsittely on [Luvun 8 osiossa "UTF-8-koodatun tekstin tallentaminen
> merkkijonoilla"][strings]<!-- ignore -->.

Kaiken tämän tiedon valossa kirjoitetaan `first_word` uudelleen palauttamaan
slice. Tyyppi, joka merkitsee "merkkijonoslicea", kirjoitetaan muodossa `&str`:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-18-first-word-slice/src/main.rs:here}}
```

</Listing>

Saamme sanan lopun indeksin samalla tavalla kuin Listauksessa 4-7,
etsimällä ensimmäisen välilyönnin esiintymän. Kun löydämme välilyönnin, palautamme
merkkijonoslicen käyttämällä merkkijonon alkua ja välilyönnin indeksiä
aloitus- ja lopetusindekseinä.

Nyt kun kutsumme `first_word`-funktiota, saamme takaisin yhden arvon, joka on sidottu
taustalla olevaan dataan. Arvo koostuu viitteestä slicen aloituspisteeseen
ja slicen elementtien määrästä.

Slicen palauttaminen toimisi myös `second_word`-funktiolle:

```rust,ignore
fn second_word(s: &String) -> &str {
```

Meillä on nyt suoraviivainen API, jota on paljon vaikeampi sotkea, koska
kääntäjä varmistaa, että `String`-arvoon tehdyt viitteet pysyvät kelvollisina. Muista
bugi Listauksen 4-8 ohjelmassa, kun saimme ensimmäisen sanan lopun indeksin mutta sitten
tyhjensimme merkkijonon, jolloin indeksimme oli virheellinen? Tuo koodi oli
loogisesti virheellinen, mutta se ei näyttänyt välittömiä virheitä. Ongelmat
ilmaantuisivat myöhemmin, jos jatkaisimme ensimmäisen sanan indeksin käyttöä tyhjän
merkkijonon kanssa. Slicet tekevät tästä bugista mahdottoman ja kertovat meille ongelmasta
koodissamme paljon aikaisemmin. `first_word`-funktion slice-version käyttö aiheuttaa
käännösajan virheen:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-19-slice-error/src/main.rs:here}}
```

</Listing>

Tässä on kääntäjän virhe:

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-19-slice-error/output.txt}}
```

Muista lainausperiaatteista, että jos meillä on muuttumaton viite johonkin,
emme voi myöskään ottaa muuttuvaa viitettä. Koska `clear` täytyy
katkaista `String`, sen täytyy saada muuttuva viite. `clear`-kutsun jälkeinen `println!`
käyttää viitettä muuttujassa `word`, joten muuttumattoman
viitteen täytyy olla edelleen aktiivinen tuossa vaiheessa. Rust estää muuttuvan
viitteen `clear`-funktiossa ja muuttumattoman viitteen muuttujassa `word` olemasta
samaan aikaan, ja käännös epäonnistuu. Rust ei ole ainoastaan tehnyt API:stamme helpomman käyttää,
vaan se on myös poistanut kokonaisen virheluokan käännösaikana!

<!-- Old heading. Do not remove or links may break. -->

<a id="string-literals-are-slices"></a>

#### Merkkijonoliteraalit sliceina

Muista, että puhuimme merkkijonoliteraalien tallentumisesta binääritiedostoon. Nyt
kun tiedämme sliceista, voimme ymmärtää merkkijonoliteraalit oikein:

```rust
let s = "Hello, world!";
```

Tässä `s`-muuttujan tyyppi on `&str`: se on slice, joka osoittaa kyseiseen kohtaan
binääritiedostossa. Tämän takia merkkijonoliteraalit ovat myös muuttumattomia; `&str` on
muuttumaton viite.

#### Merkkijonoslicet parametreina

Tieto siitä, että voit ottaa sliceja literaaleista ja `String`-arvoista, johtaa meidät
vielä yhteen parannukseen `first_word`-funktioon, ja se on sen signatuuri:

```rust,ignore
fn first_word(s: &String) -> &str {
```

Kokeneempi rustilainen kirjoittaisi Listauksessa 4-9 näytetyn signatuurin
sen sijaan, koska se antaa meille mahdollisuuden käyttää samaa funktiota sekä `&String`- että
`&str`-arvoilla.

<Listing number="4-9" caption="`first_word`-funktion parantaminen käyttämällä merkkijonoslicea `s`-parametrin tyypinä">

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-09/src/main.rs:here}}
```

</Listing>

Jos meillä on merkkijonoslice, voimme välittää sen suoraan. Jos meillä on `String`, voimme
välittää slicen `String`-arvosta tai viitteen `String`-arvoon. Tämä
joustavuus hyödyntää _deref-pakotuksia_, ominaisuutta, jota käsittelemme
[Luvun 15 osiossa "Implisiittiset deref-pakotukset funktioiden ja
metodien kanssa"][deref-coercions]<!--ignore-->.

Funktion määrittely ottamaan merkkijonoslice `String`-viitteen sijaan
tekee API:stamme yleisemmän ja hyödyllisemmän menettämättä mitään toiminnallisuutta:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-09/src/main.rs:usage}}
```

</Listing>

### Muut slicet

Merkkijonoslicet, kuten saatat kuvitella, ovat merkkijonoihin erityisiä. Mutta on olemassa
yleisempikin slice-tyyppi. Harkitse tätä taulukkoa:

```rust
let a = [1, 2, 3, 4, 5];
```

Aivan kuten saatamme haluta viitata osaan merkkijonosta, saatamme haluta viitata
osaan taulukosta. Teemme sen näin:

```rust
let a = [1, 2, 3, 4, 5];

let slice = &a[1..3];

assert_eq!(slice, &[2, 3]);
```

Tällä slicellä on tyyppi `&[i32]`. Se toimii samalla tavalla kuin merkkijonoslicet,
tallentamalla viitteen ensimmäiseen elementtiin ja pituuden. Käytät tämänlaista
slicea kaikenlaisissa muissa kokoelmissa. Käsittelemme näitä kokoelmia
yksityiskohtaisesti, kun puhumme vektoreista Luvussa 8.

## Yhteenveto

Omistajuuden, lainauksen ja slicejen käsitteet varmistavat muistiturvallisuuden Rust-
ohjelmissa käännösaikana. Rust-kieli antaa sinulle hallinnan muistin käytöstä
samalla tavalla kuin muut järjestelmäohjelmointikielet, mutta se, että datan omistaja
siivoaa automaattisesti datan, kun omistaja poistuu näkyvyysalueelta,
tarkoittaa, että sinun ei tarvitse kirjoittaa ja debugata ylimääräistä koodia saadaksesi tämän hallinnan.

Omistajuus vaikuttaa siihen, miten monet muut Rustin osat toimivat, joten puhumme
näistä käsitteistä lisää koko kirjan ajan. Siirrytään Lukuun 5 ja katsotaan,
miten datan osia ryhmitellään yhteen `struct`-rakenteessa.

[ch13]: ch13-02-iterators.html
[ch6]: ch06-02-match.html#patterns-that-bind-to-values
[strings]: ch08-02-strings.html#storing-utf-8-encoded-text-with-strings
[deref-coercions]: ch15-02-deref.html#implicit-deref-coercions-with-functions-and-methods
