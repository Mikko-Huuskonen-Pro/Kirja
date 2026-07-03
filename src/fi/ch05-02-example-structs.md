## Esimerkkiohjelma, joka käyttää rakenteita

Ymmärtääksemme, milloin rakenteita kannattaa käyttää, kirjoitamme ohjelman, joka laskee suorakulmion pinta-alan. Aloitamme käyttämällä yksittäisiä muuttujia
ja refaktoroimme ohjelman vähitellen niin, että käytämme rakenteita.

Tehdään uusi binääriprojekti Cargo-ohjelmalla nimeltä _rectangles_, joka ottaa suorakulmion leveyden ja korkeuden pikseleinä ja laskee suorakulmion pinta-alan.
Listausta 5-8 näyttää lyhyen ohjelman, joka tekee juuri tämän projektimme _src/main.rs_-tiedostossa.

<Listing number="5-8" file-name="src/main.rs" caption="Suorakulmion pinta-alan laskeminen erillisillä leveys- ja korkeusmuuttujilla">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/src/main.rs:all}}
```

</Listing>

Aja ohjelma komennolla `cargo run`:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/output.txt}}
```

Tämä koodi onnistuu laskemaan suorakulmion pinta-alan kutsumalla `area`-funktiota kummallakin mitalla, mutta voimme tehdä koodista selkeämmän ja luettavamman.

Ongelma tässä koodissa näkyy `area`-funktion signatuurissa:

```rust,ignore
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/src/main.rs:here}}
```

`area`-funktion pitäisi laskea yhden suorakulmion pinta-ala, mutta kirjoittamassamme funktiossa on kaksi parametria, eikä ohjelmassamme ole missään selvää,
että parametrit liittyvät toisiinsa. Olisi luettavampaa ja hallittavampaa ryhmitellä leveys ja korkeus yhteen. Olemme jo käsitelleet yhden tavan tehdä tämä
[Luvun 3 ”Tuplatyyppi”][the-tuple-type]<!-- ignore --> -osiossa: käyttämällä tuplia.

### Refaktorointi tuplilla

Listausta 5-9 näyttää toisen version ohjelmastamme, joka käyttää tuplia.

<Listing number="5-9" file-name="src/main.rs" caption="Suorakulmion leveyden ja korkeuden määrittely tuplalla">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-09/src/main.rs}}
```

</Listing>

Eräästä näkökulmasta tämä ohjelma on parempi. Tuplat antavat lisätä hieman rakennetta, ja välitämme nyt vain yhden argumentin. Mutta toisesta näkökulmasta
tämä versio on epäselvempi: tuplat eivät nimeä elementtejään, joten meidän täytyy indeksoida tuplan osia, mikä tekee laskennastamme vähemmän ilmeistä.

Leveyden ja korkeuden sekoittaminen ei vaikuttaisi pinta-alan laskentaan, mutta jos haluaisimme piirtää suorakulmion ruudulle, se vaikuttaisi! Meidän
piti muistaa, että `width` on tuplan indeksi `0` ja `height` on tuplan indeksi `1`. Tämä olisi vielä vaikeampaa jollekin muulle selvittää ja muistaa, jos
hän käyttäisi koodiamme. Koska emme välittäneet datamme merkitystä koodissamme, virheiden tekeminen on nyt helpompaa.

<!-- Old headings. Do not remove or links may break. -->

<a id="refactoring-with-structs-adding-more-meaning"></a>

### Refaktorointi rakenteilla

Käytämme rakenteita lisätäksemme merkitystä nimeämällä datan. Voimme muuntaa käyttämämme tuplan rakenteeksi, jolla on nimi kokonaisuudelle sekä nimet
osille, kuten Listauksessa 5-10 on esitetty.

<Listing number="5-10" file-name="src/main.rs" caption="`Rectangle`-rakenteen määrittely">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-10/src/main.rs}}
```

</Listing>

Tässä olemme määritelleet rakenteen ja nimenneet sen `Rectangle`. Aaltosulkeiden sisällä määritimme kentät `width` ja `height`, joilla molemmilla on tyyppi
`u32`. Sitten `main`-funktiossa loimme tietyn `Rectangle`-instanssin, jonka leveys on `30` ja korkeus `50`.

`area`-funktiomme on nyt määritelty yhdellä parametrilla, jonka olemme nimenneet `rectangle` ja jonka tyyppi on `Rectangle`-rakenteen instanssin muuttumaton
lainaus. Kuten mainittiin Luvussa 4, haluamme lainata rakenteen omistajuuden siirtämisen sijaan. Näin `main` säilyttää omistajuutensa ja voi jatkaa `rect1`:n
käyttöä, minkä vuoksi käytämme `&`-merkkiä funktion signatuurissa ja funktiokutsussa.

`area`-funktio käyttää `Rectangle`-instanssin `width`- ja `height`-kenttiä (huomaa, että lainatun rakenteen instanssin kenttien käyttö ei siirrä kenttien
arvoja, minkä vuoksi näet usein rakenteiden lainauksia). `area`-funktion signatuuri sanoo nyt täsmälleen, mitä tarkoitamme: laske `Rectangle`-rakenteen
pinta-ala käyttämällä sen `width`- ja `height`-kenttiä. Tämä välittää, että leveys ja korkeus liittyvät toisiinsa, ja antaa kuvaavat nimet arvoille tuplan
indeksiarvojen `0` ja `1` sijaan. Tämä on selkeyden voitto.

<!-- Old headings. Do not remove or links may break. -->

<a id="adding-useful-functionality-with-derived-traits"></a>

### Toiminnallisuuden lisääminen johdettavilla traitteilla

Olisi hyödyllistä pystyä tulostamaan `Rectangle`-instanssi debugatessamme ohjelmaamme ja näkemään kaikkien sen kenttien arvot. Listausta 5-11 yrittää käyttää
[`println!`-makroa][println]<!-- ignore --> kuten aiemmissa luvuissa. Tämä ei kuitenkaan toimi.

<Listing number="5-11" file-name="src/main.rs" caption="Yritys tulostaa `Rectangle`-instanssi">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/src/main.rs}}
```

</Listing>

Kun käännämme tämän koodin, saamme virheen, jonka ydinviesti on:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/output.txt:3}}
```

`println!`-makro voi tehdä monenlaista muotoilua, ja oletusarvoisesti aaltosulkeet kertovat `println!`:lle käyttämään `Display`-nimistä muotoilua: tulostusta,
joka on tarkoitettu suoraan loppukäyttäjälle. Tähän mennessä näkemämme primitiivityypit toteuttavat `Display`-traitin oletusarvoisesti, koska on vain yksi
tapa näyttää `1` tai mikä tahansa muu primitiivityyppi käyttäjälle. Mutta rakenteiden kohdalla se, miten `println!`:n pitäisi muotoilla tuloste, on vähemmän
selvä, koska näyttömahdollisuuksia on enemmän: haluatko pilkkuja vai et? Haluatko tulostaa aaltosulkeet? Pitäisikö kaikki kentät näyttää? Tämän epäselvyyden
vuoksi Rust ei yritä arvata, mitä haluamme, eikä rakenteilla ole valmista `Display`-toteutusta käytettäväksi `println!`:n ja `{}`-paikkamerkin kanssa.

Jos jatkamme virheilmoitusten lukemista, löydämme tämän hyödyllisen huomautuksen:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/output.txt:9:10}}
```

Kokeillaan! `println!`-makrokutsu näyttää nyt tältä: `println!("rect1 is {rect1:?}");`. Määritteen `:?` laittaminen aaltosulkeiden sisään kertoo `println!`:lle,
että haluamme käyttää `Debug`-nimistä tulostusmuotoa. `Debug`-traitin avulla voimme tulostaa rakenteemme tavalla, joka on hyödyllinen kehittäjille, jotta
näemme sen arvon debugatessamme koodiamme.

Käännä koodi tällä muutoksella. Pah! Saamme silti virheen:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-01-debug/output.txt:3}}
```

Mutta kääntäjä antaa taas hyödyllisen huomautuksen:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-01-debug/output.txt:9:10}}
```

Rust _sisältää_ toiminnallisuuden debug-tietojen tulostamiseen, mutta meidän täytyy erikseen valita se käyttöön rakenteellemme. Teemme sen lisäämällä ulkoisen
attribuutin `#[derive(Debug)]` juuri ennen rakenteen määrittelyä, kuten Listauksessa 5-12 on esitetty.

<Listing number="5-12" file-name="src/main.rs" caption="Attribuutin lisääminen `Debug`-traitin johdattamiseen ja `Rectangle`-instanssin tulostaminen debug-muotoilulla">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-12/src/main.rs}}
```

</Listing>

Nyt kun ajamme ohjelman, emme saa virheitä ja näemme seuraavan tulosteen:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-12/output.txt}}
```

Hienoa! Tuloste ei ole kaunein mahdollinen, mutta se näyttää kaikkien tämän instanssin kenttien arvot, mikä auttaisi varmasti debuggauksessa. Kun meillä on
suurempia rakenteita, on hyödyllistä saada hieman helpommin luettava tuloste; näissä tapauksissa voimme käyttää `{:#?}` muodon `{:?}` sijaan `println!`-merkkijonossa.
Tässä esimerkissä `{:#?}`-tyyli tuottaa seuraavan tulosteen:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-02-pretty-debug/output.txt}}
```

Toinen tapa tulostaa arvo `Debug`-muodossa on käyttää [`dbg!`-makroa][dbg]<!-- ignore -->, joka ottaa omistajuuden lausekkeesta (toisin kuin `println!`, joka
ottaa viittauksen), tulostaa tiedoston ja rivinumeron, jossa `dbg!`-makrokutsu tapahtuu koodissasi, sekä kyseisen lausekkeen tulosarvon, ja palauttaa lausekkeen
omistajuuden.

> Huom: `dbg!`-makrokutsu tulostaa vakiovirhevirtaan (`stderr`), toisin kuin `println!`, joka tulostaa vakiotulostusvirtaan (`stdout`). Puhumme `stderr`:stä ja
> `stdout`:sta lisää [Luvun 12 osiossa ”Virheiden ohjaaminen vakiovirheeseen”][err]<!-- ignore -->.

Tässä on esimerkki, jossa olemme kiinnostuneita arvosta, joka sijoitetaan `width`-kenttään, sekä koko rakenteen arvosta `rect1`:ssä:

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-05-dbg-macro/src/main.rs}}
```

Voimme laittaa `dbg!`:n lausekkeen `30 * scale` ympärille, ja koska `dbg!` palauttaa lausekkeen arvon omistajuuden, `width`-kenttä saa saman arvon kuin ilman
`dbg!`-kutsua. Emme halua `dbg!`:n ottavan `rect1`:n omistajuutta, joten käytämme viittausta `rect1`:een seuraavassa kutsussa. Tässä on tämän esimerkin tuloste:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/no-listing-05-dbg-macro/output.txt}}
```

Näemme, että ensimmäinen tuloste tuli _src/main.rs_-tiedoston riviltä 10, jossa debuggaamme lauseketta `30 * scale`, ja sen tulosarvo on `60` (`Debug`-muotoilu
kokonaisluvuille tulostaa vain niiden arvon). `dbg!`-kutsu _src/main.rs_-tiedoston rivillä 14 tulostaa arvon `&rect1`, joka on `Rectangle`-rakenne. Tämä
tuloste käyttää `Rectangle`-tyypin siistiä `Debug`-muotoilua. `dbg!`-makro voi olla todella hyödyllinen selvittäessäsi, mitä koodisi tekee!

`Debug`-traitin lisäksi Rust on tarjonnut joukon traitteja, joita voimme käyttää `derive`-attribuutin kanssa lisätäksemme hyödyllistä käyttäytymistä
mukautetuille tyypeillemme. Nämä traitit ja niiden käyttäytymiset on lueteltu [Liitteessä C][app-c]<!-- ignore -->. Käsittelemme, miten toteutamme nämä traitit
mukautetulla käyttäytymisellä sekä miten luomme omia traitteja Luvussa 10. On myös monia muita attribuutteja kuin `derive`; lisätietoja on [Rust-viitteen
”Attribuutit”-osiossa][attributes].

`area`-funktiomme on hyvin spesifinen: se laskee vain suorakulmioiden pinta-alan. Olisi hyödyllistä sitoa tämä käyttäytyminen tiukemmin `Rectangle`-rakenteeseemme,
koska se ei toimi minkään muun tyypin kanssa. Katsotaan, miten voimme jatkaa tämän koodin refaktorointia muuttamalla `area`-funktion `area`-metodiksi, joka
on määritelty `Rectangle`-tyypillemme.

[the-tuple-type]: ch03-02-data-types.html#the-tuple-type
[app-c]: appendix-03-derivable-traits.md
[println]: ../std/macro.println.html
[dbg]: ../std/macro.dbg.html
[err]: ch12-06-writing-to-stderr-instead-of-stdout.html
[attributes]: ../reference/attributes.html
