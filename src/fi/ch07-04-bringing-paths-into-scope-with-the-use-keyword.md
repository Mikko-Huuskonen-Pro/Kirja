## Polkujen tuominen laajuuteen `use`-avainsanalla

Funktioiden kutsuminen polkuja kirjoittamalla voi tuntua hankalalta ja toistavalta. Listauksessa 7-7, riippumatta siitä, valitsimmeko absoluuttisen vai suhteellisen polun `add_to_waitlist`-funktioon, jouduimme aina määrittämään myös `front_of_house`- ja `hosting`-moduulit, kun halusimme kutsua `add_to_waitlist`-funktiota. Onneksi on olemassa tapa yksinkertaistaa tätä prosessia: voimme luoda polulle lyhenteen `use`-avainsanalla kerran ja käyttää sitten lyhyempää nimeä kaikkialla muualla laajuudessa.

Listauksessa 7-11 tuomme `crate::front_of_house::hosting`-moduulin `eat_at_restaurant`-funktion laajuuteen, joten meidän tarvitsee vain määrittää `hosting::add_to_waitlist` kutsuaksemme `add_to_waitlist`-funktiota funktiossa `eat_at_restaurant`.

<Listing number="7-11" file-name="src/lib.rs" caption="Moduulin tuominen laajuuteen `use`:lla">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-11/src/lib.rs}}
```

</Listing>

`use`-avainsanan ja polun lisääminen laajuuteen on samankaltaista kuin symbolisen linkin luominen tiedostojärjestelmässä. Lisäämällä `use crate::front_of_house::hosting` crate-juureen, `hosting` on nyt kelvollinen nimi siinä laajuudessa, ikään kuin `hosting`-moduuli olisi määritelty crate-juuressa. `use`:lla laajuuteen tuodut polut tarkistavat myös yksityisyyden, kuten muutkin polut.

Huomaa, että `use` luo lyhenteen vain siihen laajuuteen, jossa `use` esiintyy. Listausta 7-12 siirtää `eat_at_restaurant`-funktion uuteen lapsimoduuliin nimeltä `customer`, joka on sitten eri laajuudessa kuin `use`-lauseke, joten funktion runko ei käänny.

<Listing number="7-12" file-name="src/lib.rs" caption="`use`-lauseke pätee vain laajuudessa, jossa se on.">

```rust,noplayground,test_harness,does_not_compile,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-12/src/lib.rs}}
```

</Listing>

Kääntäjän virhe näyttää, että lyhenne ei enää päde `customer`-moduulissa:

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-12/output.txt}}
```

Huomaa, että on myös varoitus siitä, että `use` ei ole enää käytössä laajuudessaan! Korjataksesi tämän ongelman, siirrä `use` myös `customer`-moduulin sisään, tai viittaa lyhenteeseen emomoduulissa `super::hosting`:lla `customer`-lapsimoduulissa.

### Idiomaattisten `use`-polkujen luominen

Listauksessa 7-11 saatoit ihmetellä, miksi määritimme `use crate::front_of_house::hosting` ja kutsuimme sitten `hosting::add_to_waitlist` funktiossa `eat_at_restaurant`, sen sijaan että määrittäisimme `use`-polun aina `add_to_waitlist`-funktioon saakka saavuttaaksemme saman tuloksen, kuten Listauksessa 7-13.

<Listing number="7-13" file-name="src/lib.rs" caption="`add_to_waitlist`-funktion tuominen laajuuteen `use`:lla, mikä ei ole idiomaattista">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-13/src/lib.rs}}
```

</Listing>

Vaikka sekä Listausta 7-11 että Listausta 7-13 saavuttavat saman tehtävän, Listausta 7-11 on idiomaattinen tapa tuoda funktio laajuuteen `use`:lla. Funktion emomoduulin tuominen laajuuteen `use`:lla tarkoittaa, että meidän täytyy määrittää emomoduuli funktiota kutsuttaessa. Emomoduulin määrittäminen funktiota kutsuttaessa tekee selväksi, ettei funktio ole määritelty paikallisesti, mutta silti minimoidaan koko polun toistuminen. Listauksen 7-13 koodi ei kerro selvästi, mistä `add_to_waitlist` on määritelty.

Toisaalta, kun tuomme rakenteita, enumeja ja muita kohteita `use`:lla, on idiomaattista määrittää koko polku. Listausta 7-14 näyttää idiomaattisen tavan tuoda standardikirjaston `HashMap`-rakenne binääricraten laajuuteen.

<Listing number="7-14" file-name="src/main.rs" caption="`HashMap`:n tuominen laajuuteen idiomaattisella tavalla">

```rust
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-14/src/main.rs}}
```

</Listing>

Tämän idiooman takana ei ole vahvaa syytä: se on vain vakiintunut käytäntö, johon ihmiset ovat tottuneet lukemaan ja kirjoittamaan Rust-koodia tällä tavalla.

Poikkeus tähän idioomaan on, jos tuomme kaksi samaa nimeä käyttävää kohdetta laajuuteen `use`-lausekkeilla, koska Rust ei salli sitä. Listausta 7-15 näyttää, miten tuodaan kaksi `Result`-tyyppiä, joilla on sama nimi mutta eri emomoduulit, ja miten niihin viitataan.

<Listing number="7-15" file-name="src/lib.rs" caption="Kahden saman nimisen tyypin tuominen samaan laajuuteen vaatii niiden emomoduulien käyttöä.">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-15/src/lib.rs:here}}
```

</Listing>

Kuten näet, emomoduulien käyttö erottaa kaksi `Result`-tyyppiä toisistaan. Jos sen sijaan määrittäisimme `use std::fmt::Result` ja `use std::io::Result`, meillä olisi kaksi `Result`-tyyppiä samassa laajuudessa, eikä Rust tietäisi, kumpaa tarkoitamme, kun käytämme `Result`:ia.

### Uusien nimien antaminen `as`-avainsanalla

On olemassa toinen ratkaisu ongelmaan, jossa tuodaan kaksi samaa nimeä käyttävää tyyppiä samaan laajuuteen `use`:lla: polun jälkeen voimme määrittää `as` ja uuden paikallisen nimen, eli _aliasin_, tyypille. Listausta 7-16 näyttää toisen tavan kirjoittaa Listauksen 7-15 koodi uudelleennimeämällä toinen kahdesta `Result`-tyypistä `as`:lla.

<Listing number="7-16" file-name="src/lib.rs" caption="Tyypin uudelleennimeäminen, kun se tuodaan laajuuteen `as`-avainsanalla">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-16/src/lib.rs:here}}
```

</Listing>

Toisessa `use`-lausekkeessa valitsimme uuden nimen `IoResult` tyypille `std::io::Result`, joka ei ole ristiriidassa `std::fmt`:n `Result`-tyypin kanssa, jonka olemme myös tuoneet laajuuteen. Listausta 7-15 ja Listausta 7-16 pidetään idiomaattisina, joten valinta on sinun!

### Nimien uudelleenjulkaisu `pub use`:lla

Kun tuomme nimen laajuuteen `use`-avainsanalla, uudessa laajuudessa käytettävissä oleva nimi on yksityinen. Jotta koodi, joka kutsuu koodiamme, voisi viitata kyseiseen nimeen ikään kuin se olisi määritelty sen koodin laajuudessa, voimme yhdistää `pub` ja `use`. Tätä tekniikkaa kutsutaan _uudelleenjulkaisuksi_, koska tuomme kohteen laajuuteen mutta teemme sen myös muiden saataville tuotavaksi heidän laajuuteensa.

Listausta 7-17 näyttää Listauksen 7-11 koodin, jossa juurimoduulin `use` on muutettu muotoon `pub use`.

<Listing number="7-17" file-name="src/lib.rs" caption="Nimen saataville asettaminen kaikelle koodille uudesta laajuudesta `pub use`:lla">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-17/src/lib.rs}}
```

</Listing>

Ennen tätä muutosta ulkoisen koodin olisi pitänyt kutsua `add_to_waitlist`-funktiota polulla `restaurant::front_of_house::hosting::add_to_waitlist()`, mikä olisi myös vaatinut `front_of_house`-moduulin merkitsemistä `pub`:iksi. Nyt kun tämä `pub use` on uudelleenjulkaissut `hosting`-moduulin juurimoduulista, ulkoinen koodi voi käyttää polkua `restaurant::hosting::add_to_waitlist()` sen sijaan.

Uudelleenjulkaisu on hyödyllistä, kun koodisi sisäinen rakenne poikkeaa siitä, miten koodiasi kutsuvat ohjelmoijat ajattelevat toimialuetta. Esimerkiksi tässä ravintolametaforassa ravintolaa pyörittävät ihmiset ajattelevat ”etutaloa” ja ”takataloa”. Ravintolaa vierailevat asiakkaat eivät kuitenkaan todennäköisesti ajattele ravintolan osia näillä termeillä. `pub use`:lla voimme kirjoittaa koodimme yhdellä rakenteella mutta paljastaa erilaisen rakenteen. Näin kirjastomme on hyvin organisoitu sekä kirjastoa työstäville ohjelmoijille että kirjastoa kutsuville ohjelmoijille. Katsomme toisen esimerkin `pub use`:sta ja sen vaikutuksesta craten dokumentaatioon [”Kätevän julkisen API:n vienti `pub use`:lla”][ch14-pub-use]<!-- ignore --> -osiossa Luvussa 14.

### Ulkoisten pakettien käyttäminen

Luvussa 2 ohjelmoimme arvauspeliprojektin, joka käytti ulkoista pakettia nimeltä `rand` satunnaislukujen saamiseen. Käyttääksemme `rand`:ia projektissamme lisäsimme tämän rivin tiedostoon _Cargo.toml_:

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:
* ch02-00-guessing-game-tutorial.md
* ch14-03-cargo-workspaces.md
-->

<Listing file-name="Cargo.toml">

```toml
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-02/Cargo.toml:9:}}
```

</Listing>

`rand`:in lisääminen riippuvuudeksi tiedostoon _Cargo.toml_ kertoo Cargolle lataamaan `rand`-paketin ja sen riippuvuudet osoitteesta [crates.io](https://crates.io/) ja tekemään `rand`:in saataville projektillemme.

Sitten tuodaksemme `rand`:in määrittelyt pakettimme laajuuteen lisäsimme `use`-rivin, joka alkaa craten nimellä `rand`, ja listasimme kohteet, jotka halusimme tuoda laajuuteen. Muista, että [”Satunnaisluvun generointi”][rand]<!-- ignore --> -osiossa Luvussa 2 toimme `Rng`-traitin laajuuteen ja kutsuimme `rand::thread_rng`-funktiota:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-03/src/main.rs:ch07-04}}
```

Rust-yhteisön jäsenet ovat tehneet monia paketteja saataville osoitteessa [crates.io](https://crates.io/), ja minkä tahansa niistä tuominen pakettiisi sisältää samat vaiheet: niiden listaaminen pakettisi tiedostossa _Cargo.toml_ ja `use`:n käyttö kohteiden tuomiseen laajuuteen niiden crateista.

Huomaa, että standardikirjasto `std` on myös paketti, joka on ulkoinen pakettimme suhteen. Koska standardikirjasto toimitetaan Rust-kielen mukana, meidän ei tarvitse muuttaa tiedostoa _Cargo.toml_ sisällyttääksemme `std`:n. Meidän täytyy kuitenkin viitata siihen `use`:lla tuodaksemme kohteita sieltä pakettimme laajuuteen. Esimerkiksi `HashMap`:n kohdalla käyttäisimme tätä riviä:

```rust
use std::collections::HashMap;
```

Tämä on absoluuttinen polku, joka alkaa `std`:llä, standardikirjaston craten nimellä.

### Sisäkkäisten polkujen käyttö suurten `use`-listojen siistimiseen

Jos käytämme useita samassa cratessa tai moduulissa määriteltyjä kohteita, kunkin kohteen listaaminen omalle rivilleen voi viedä paljon pystysuuntaista tilaa tiedostoissamme. Esimerkiksi nämä kaksi `use`-lauseketta, joita käytimme arvauspelissä Listauksessa 2-4, tuovat kohteita `std`:stä laajuuteen:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-01-use-std-unnested/src/main.rs:here}}
```

</Listing>

Sen sijaan voimme käyttää sisäkkäisiä polkuja tuodaksemme samat kohteet laajuuteen yhdellä rivillä. Teemme tämän määrittämällä polun yhteisen osan, jota seuraa kaksoispiste ja sitten aaltosulkeet eri polkujen osien listan ympärillä, kuten Listauksessa 7-18 on esitetty.

<Listing number="7-18" file-name="src/main.rs" caption="Sisäkkäisen polun määrittäminen useiden saman etuliitteen omaavien kohteiden tuomiseksi laajuuteen">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-18/src/main.rs:here}}
```

</Listing>

Suuremmissa ohjelmissa monien kohteiden tuominen laajuuteen samasta cratesta tai moduulista sisäkkäisiä polkuja käyttäen voi vähentää erillisten `use`-lausekkeiden määrää huomattavasti!

Voimme käyttää sisäkkäistä polkua millaisella tahansa polun tasolla, mikä on hyödyllistä, kun yhdistämme kaksi `use`-lauseketta, joilla on yhteinen alipolku. Esimerkiksi Listausta 7-19 näyttää kaksi `use`-lauseketta: toinen tuo `std::io`:n laajuuteen ja toinen tuo `std::io::Write`:n laajuuteen.

<Listing number="7-19" file-name="src/lib.rs" caption="Kaksi `use`-lauseketta, joista toinen on toisen alipolku">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-19/src/lib.rs}}
```

</Listing>

Näiden kahden polun yhteinen osa on `std::io`, ja se on koko ensimmäinen polku. Yhdistääksemme nämä kaksi polkua yhdeksi `use`-lausekkeeksi voimme käyttää `self`:ää sisäkkäisessä polussa, kuten Listauksessa 7-20 on esitetty.

<Listing number="7-20" file-name="src/lib.rs" caption="Listauksen 7-19 polut yhdistettynä yhdeksi `use`-lausekkeeksi">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-20/src/lib.rs}}
```

</Listing>

Tämä rivi tuo `std::io`:n ja `std::io::Write`:n laajuuteen.

### Glob-operaattori

Jos haluamme tuoda _kaikki_ polussa määritellyt julkiset kohteet laajuuteen, voimme määrittää kyseisen polun, jota seuraa `*`-glob-operaattori:

```rust
use std::collections::*;
```

Tämä `use`-lauseke tuo kaikki `std::collections`:ssa määritellyt julkiset kohteet nykyiseen laajuuteen. Ole varovainen käyttäessäsi glob-operaattoria! Glob voi vaikeuttaa sen tunnistamista, mitkä nimet ovat laajuudessa ja mistä ohjelmassasi käytetty nimi on määritelty.

Glob-operaattoria käytetään usein testauksessa tuomaan kaikki testattava `tests`-moduuliin; puhumme siitä [”Testien kirjoittaminen”][writing-tests]<!-- ignore --> -osiossa Luvussa 11. Glob-operaattoria käytetään joskus myös osana preludimallia: katso [standardikirjaston dokumentaatio](../std/prelude/index.html#other-preludes)<!-- ignore --> lisätietoja tästä mallista.

[ch14-pub-use]: ch14-02-publishing-to-crates-io.html#exporting-a-convenient-public-api-with-pub-use
[rand]: ch02-00-guessing-game-tutorial.html#generating-a-random-number
[writing-tests]: ch11-01-writing-tests.html#how-to-write-tests
