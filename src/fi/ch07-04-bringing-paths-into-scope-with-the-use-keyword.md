## Polkujen tuominen laajuuteen `use`-avainsanalla

Polkujen kirjoittaminen funktioiden kutsumiseksi voi tuntua hankalalta ja toistavalta. Listauksessa 7-7, valitsimmepa absoluuttisen tai suhteellisen polun `add_to_waitlist`-funktioon, meidän piti aina määrittää myös `front_of_house` ja `hosting` joka kerta kun halusimme kutsua `add_to_waitlist`-funktiota. Onneksi on olemassa tapa yksinkertaistaa tätä prosessia: Voimme luoda oikotien polkuun `use`-avainsanalla kerran ja käyttää sitten lyhyempää nimeä kaikkialla muualla laajuudessa.

Listauksessa 7-11 tuomme `crate::front_of_house::hosting`-moduulin `eat_at_restaurant`-funktion laajuuteen, jotta meidän tarvitsee vain määrittää `hosting::add_to_waitlist` kutsuaksemme `add_to_waitlist`-funktiota funktiossa `eat_at_restaurant`.

<Listing number="7-11" file-name="src/lib.rs" caption="Moduulin tuominen laajuuteen `use`:lla">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-11/src/lib.rs}}
```

</Listing>

`use`-avainsanan ja polun lisääminen laajuuteen on samanlaista kuin symbolisen linkin luominen tiedostojärjestelmässä. Lisäämällä `use crate::front_of_house::hosting` crate-juureen, `hosting` on nyt kelvollinen nimi kyseisessä laajuudessa, aivan kuin `hosting`-moduuli olisi määritelty crate-juuressa. `use`:lla laajuuteen tuodut polut tarkistavat myös yksityisyyden, kuten kaikki muutkin polut.

Huomaa, että `use` luo oikotien vain sille laajuudelle, jossa `use` esiintyy. Listaus 7-12 siirtää `eat_at_restaurant`-funktion uuteen alimoduuuliin nimeltä `customer`, joka on sitten eri laajuus kuin `use`-lause, joten funktion runko ei käänny.

<Listing number="7-12" file-name="src/lib.rs" caption="`use`-lause pätee vain laajuudessa, jossa se on.">

```rust,noplayground,test_harness,does_not_compile,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-12/src/lib.rs}}
```

</Listing>

Kääntäjän virhe näyttää, että oikotie ei enää päde `customer`-moduulissa:

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-12/output.txt}}
```

Huomaa, että on myös varoitus, että `use` ei ole enää käytössä laajuudessaan! Korjataksesi tämän ongelman, siirrä `use` myös `customer`-moduuliin, tai viittaa emomoduulin oikotiehen `super::hosting`:lla `customer`-alimoduuulissa.

### Idiomatisten `use`-polkujen luominen

Listauksessa 7-11 saatoit ihmetellä, miksi määritimme `use crate::front_of_house::hosting` ja kutsuimme sitten `hosting::add_to_waitlist` funktiossa `eat_at_restaurant`, sen sijaan että määrittäisimme `use`-polun aina `add_to_waitlist`-funktioon saakka saavuttaaksemme saman tuloksen, kuten listauksessa 7-13.

<Listing number="7-13" file-name="src/lib.rs" caption="`add_to_waitlist`-funktion tuominen laajuuteen `use`:lla, mikä ei ole idiomatista">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-13/src/lib.rs}}
```

</Listing>

Vaikka sekä listaus 7-11 että listaus 7-13 saavuttavat saman tehtävän, listaus 7-11 on idiomatinen tapa tuoda funktio laajuuteen `use`:lla. Funktion emomoduulin tuominen laajuuteen `use`:lla tarkoittaa, että meidän on määritettävä emomoduuli funktiota kutsuessamme. Emomoduulin määrittäminen funktiota kutsuttaessa tekee selväksi, että funktiota ei ole määritelty paikallisesti, mutta silti minimoidaan täyden polun toisto. Listauksen 7-13 koodi ei ole selvä siitä, missä `add_to_waitlist` on määritelty.

Toisaalta, kun tuomme structeja, enumeja ja muita kohteita `use`:lla, on idiomatista määrittää täydellinen polku. Listaus 7-14 näyttää idiomatisen tavan tuoda standardikirjaston `HashMap`-struct binääricrate:n laajuuteen.

<Listing number="7-14" file-name="src/main.rs" caption="`HashMap`:n tuominen laajuuteen idiomatiseen tapaan">

```rust
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-14/src/main.rs}}
```

</Listing>

Tämän idiomien takana ei ole vahvaa syytä: se on vain käytäntö, joka on kehittynyt, ja ihmiset ovat tottuneet lukemaan ja kirjoittamaan Rust-koodia tällä tavalla.

Poikkeus tähän idiomiaan on, jos tuomme kaksi samannimistä kohdetta laajuuteen `use`-lauseilla, koska Rust ei salli sitä. Listaus 7-15 näyttää, miten tuoda kaksi samannimistä `Result`-tyyppiä laajuuteen, joilla on sama nimi mutta eri emomoduulit, ja miten viitata niihin.

<Listing number="7-15" file-name="src/lib.rs" caption="Kahden samannimisen tyypin tuominen samaan laajuuteen vaatii niiden emomoduulien käyttämistä.">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-15/src/lib.rs:here}}
```

</Listing>

Kuten näet, emomoduulien käyttäminen erottaa kaksi `Result`-tyyppiä. Jos sen sijaan määrittäisimme `use std::fmt::Result` ja `use std::io::Result`, meillä olisi kaksi `Result`-tyyppiä samassa laajuudessa, eikä Rust tietäisi, mitä tarkoitimme käyttäessämme `Result`:ia.

### Uusien nimien antaminen `as`-avainsanalla

On olemassa toinen ratkaisu ongelmaan, jossa tuodaan kaksi samannimistä tyyppiä samaan laajuuteen `use`:lla: Polun jälkeen voimme määrittää `as` ja uuden paikallisen nimen, eli _aliaksen_, tyypille. Listaus 7-16 näyttää toisen tavan kirjoittaa listauksen 7-15 koodi uudelleennimeämällä yksi kahdesta `Result`-tyypistä `as`:lla.

<Listing number="7-16" file-name="src/lib.rs" caption="Tyypin uudelleennimeäminen, kun se tuodaan laajuuteen `as`-avainsanalla">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-16/src/lib.rs:here}}
```

</Listing>

Toisessa `use`-lauseessa valitsimme uuden nimen `IoResult` tyypille `std::io::Result`, joka ei ole ristiriidassa `std::fmt`:n `Result`:n kanssa, jonka olemme myös tuoneet laajuuteen. Listaukset 7-15 ja 7-16 katsotaan idiomatiseksi, joten valinta on sinun!

### Nimien uudelleenvienti `pub use`:lla

Kun tuomme nimen laajuuteen `use`-avainsanalla, nimi on yksityinen laajuudelle, johon sen tuimme. Jotta koodi kyseisen laajuuden ulkopuolelta voisi viitata kyseiseen nimeen ikään kuin se olisi määritelty kyseisessä laajuudessa, voimme yhdistää `pub` ja `use`. Tätä tekniikkaa kutsutaan _uudelleenvienniksi_, koska tuomme kohteen laajuuteen mutta teemme sen myös muiden saataville heidän tuodakseen sen omaan laajuuteensa.

Listaus 7-17 näyttää listauksen 7-11 koodin, jossa juurimoduulin `use` on muutettu muotoon `pub use`.

<Listing number="7-17" file-name="src/lib.rs" caption="Nimen tekeminen minkä tahansa koodin käytettäväksi uudesta laajuudesta `pub use`:lla">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-17/src/lib.rs}}
```

</Listing>

Ennen tätä muutosta ulkoisen koodin olisi pitänyt kutsua `add_to_waitlist`-funktiota polulla `restaurant::front_of_house::hosting::add_to_waitlist()`, mikä olisi myös vaatinut `front_of_house`-moduulin merkitsemistä `pub`:ksi. Nyt kun tämä `pub use` on vienyt uudelleen `hosting`-moduulin juurimoduulista, ulkoinen koodi voi käyttää polkua `restaurant::hosting::add_to_waitlist()` sen sijaan.

Uudelleenvienti on hyödyllistä, kun koodisi sisäinen rakenne eroaa siitä, miten koodiasi kutsuvat ohjelmoijat ajattelevat toimialuetta. Esimerkiksi tässä ravintolametaforassa ravintolaa pyörittävät ihmiset ajattelevat ”etuosaa” ja ”takaosaa”. Mutta ravintolaa vierailevat asiakkaat eivät todennäköisesti ajattele ravintolan osia näillä termeillä. `pub use`:lla voimme kirjoittaa koodimme yhdellä rakenteella mutta paljastaa eri rakenteen. Näin kirjastomme on hyvin organisoitu sekä kirjastoa työstäville ohjelmoijille että kirjastoa kutsuville ohjelmoijille. Tarkastelemme toista esimerkkiä `pub use`:sta ja sen vaikutuksesta crate:si dokumentaatioon kohdassa [”Kätevän julkisen API:n vienti”][ch14-pub-use]<!-- ignore --> luvussa 14.

### Ulkoisten pakettien käyttö

Luvussa 2 ohjelmoimme arvauspeli-projektin, joka käytti ulkoista pakettia nimeltä `rand` satunnaisten lukujen saamiseksi. Käyttääksemme `rand`:ia projektissamme lisäsimme tämän rivin tiedostoon _Cargo.toml_:

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch01-01-installation.md
* ch02-00-guessing-game-tutorial.md
* ch14-03-cargo-workspaces.md
-->

<Listing file-name="Cargo.toml">

```toml
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-02/Cargo.toml:9:}}
```

</Listing>

`rand`:in lisääminen riippuvuudeksi tiedostoon _Cargo.toml_ kertoo Cargolle ladata `rand`-paketti ja kaikki sen riippuvuudet osoitteesta [crates.io](https://crates.io/) ja tehdä `rand` saataville projektillemme.

Sitten tuodaksemme `rand`-määrittelyt pakettimme laajuuteen lisäsimme `use`-rivin, joka alkaa crate:n nimellä `rand`, ja listasimme kohteet, jotka halusimme tuoda laajuuteen. Muista, että kohdassa [”Satunnaisen luvun generointi”][rand]<!-- ignore --> luvussa 2 toimme `rand::prelude`-moduulin kohteet laajuuteen ja kutsuimme `rand::rng`-funktiota:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-03/src/main.rs:ch07-04}}
```

Rust-yhteisön jäsenet ovat tehneet monia paketteja saataville osoitteessa [crates.io](https://crates.io/), ja minkä tahansa niistä tuominen pakettiisi sisältää samat vaiheet: niiden listaaminen pakettisi _Cargo.toml_-tiedostossa ja `use`:n käyttäminen niiden crate:jen kohteiden tuomiseen laajuuteen.

Huomaa, että standardikirjasto `std` on myös crate, joka on ulkopuolinen paketillemme. Koska standardikirjasto toimitetaan Rust-kielen mukana, meidän ei tarvitse muuttaa _Cargo.toml_:ia sisällyttääksemme `std`:n. Meidän on kuitenkin viitattava siihen `use`:lla tuodaksemme kohteita sieltä pakettimme laajuuteen. Esimerkiksi `HashMap`:n kanssa käyttäisimme tätä riviä:

```rust
use std::collections::HashMap;
```

Tämä on absoluuttinen polku, joka alkaa `std`:llä, standardikirjaston crate:n nimellä.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-nested-paths-to-clean-up-large-use-lists"></a>

### Sisäkkäisten polkujen käyttö `use`-listojen siistimiseen

Jos käytämme useita kohteita, jotka on määritelty samassa crate:ssa tai samassa moduulissa, jokaisen kohteen listaaminen omalle rivilleen voi viedä paljon pystysuuntaista tilaa tiedostoissamme. Esimerkiksi nämä kaksi `use`-lausetta, joita käytimme arvauspelissä listauksessa 2-4, tuovat `std`:n kohteet laajuuteen:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-01-use-std-unnested/src/main.rs:here}}
```

</Listing>

Sen sijaan voimme käyttää sisäkkäisiä polkuja tuodaksemme samat kohteet laajuuteen yhdellä rivillä. Teemme tämän määrittämällä polun yhteisen osan, jota seuraa kaksoispiste, ja sitten aaltosulkeet luettelon polkujen osista, jotka eroavat, kuten listauksessa 7-18.

<Listing number="7-18" file-name="src/main.rs" caption="Sisäkkäisen polun määrittely useiden saman etuliitteen omaavien kohteiden tuomiseksi laajuuteen">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-18/src/main.rs:here}}
```

</Listing>

Suuremmissa ohjelmissa useiden kohteiden tuominen laajuuteen samasta crate:sta tai moduulista sisäkkäisiä polkuja käyttäen voi vähentää tarvittavien erillisten `use`-lausetten määrää huomattavasti!

Voimme käyttää sisäkkäistä polkua milla tahansa polun tasolla, mikä on hyödyllistä yhdistettäessä kahta `use`-lausetta, joilla on yhteinen alipolku. Esimerkiksi listaus 7-19 näyttää kaksi `use`-lausetta: toinen, joka tuo `std::io`:n laajuuteen, ja toinen, joka tuo `std::io::Write`:n laajuuteen.

<Listing number="7-19" file-name="src/lib.rs" caption="Kaksi `use`-lausetta, joista toinen on toisen alipolku">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-19/src/lib.rs}}
```

</Listing>

Näiden kahden polun yhteinen osa on `std::io`, ja se on ensimmäisen polun kokonaisuus. Yhdistääksemme nämä kaksi polkua yhdeksi `use`-lauseeksi voimme käyttää `self`:ä sisäkkäisessä polussa, kuten listauksessa 7-20.

<Listing number="7-20" file-name="src/lib.rs" caption="Listauksen 7-19 polkujen yhdistäminen yhdeksi `use`-lauseeksi">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-20/src/lib.rs}}
```

</Listing>

Tämä rivi tuo `std::io`:n ja `std::io::Write`:n laajuuteen.

<!-- Old headings. Do not remove or links may break. -->

<a id="the-glob-operator"></a>

### Kohteiden tuominen glob-operaattorilla

Jos haluamme tuoda _kaikki_ polussa määritellyt julkiset kohteet laajuuteen, voimme määrittää kyseisen polun, jota seuraa `*`-glob-operaattori:

```rust
use std::collections::*;
```

Tämä `use`-lause tuo kaikki `std::collections`:ssa määritellyt julkiset kohteet nykyiseen laajuuteen. Ole varovainen käyttäessäsi glob-operaattoria! Glob voi vaikeuttaa sen tunnistamista, mitkä nimet ovat laajuudessa ja mistä ohjelmassasi käytetty nimi on määritelty. Lisäksi, jos riippuvuus muuttaa määrittelyjään, tuomasi muuttuvat myös, mikä voi johtaa kääntäjän virheisiin riippuvuutta päivitettäessä, jos riippuvuus lisää määrittelyn samalla nimellä kuin sinun määrittelysi samassa laajuudessa, esimerkiksi.

Glob-operaattoria käytetään usein testauksessa tuomaan kaikki testattava `tests`-moduuliin; käsittelemme tätä kohdassa [”Testien kirjoittaminen”][writing-tests]<!-- ignore --> luvussa 11. Glob-operaattoria käytetään joskus myös osana preludi-mallia: Katso [standardikirjaston dokumentaatiosta](../std/prelude/index.html#other-preludes)<!-- ignore --> lisätietoja tästä mallista.

[ch14-pub-use]: ch14-02-publishing-to-crates-io.html#exporting-a-convenient-public-api
[rand]: ch02-00-guessing-game-tutorial.html#generating-a-random-number
[writing-tests]: ch11-01-writing-tests.html#how-to-write-tests
