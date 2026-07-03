## `Box<T>`-tyypin käyttö keolla olevan datan osoittamiseen

Yksinkertaisin älykäs osoitin on _box_, jonka tyyppi kirjoitetaan `Box<T>`. _Boxien_ avulla voit tallentaa datan keolle pinon sijaan. Pinossa säilyy osoitin keolla olevaan dataan. Katso luku 4, jos haluat kerrata pinon ja keon eron.

Boxeilla ei ole suorituskykyhaittaa muuta kuin se, että niiden data tallennetaan keolle pinon sijaan. Niillä ei myöskään ole juuri muita erityisominaisuuksia. Käytät niitä useimmiten seuraavissa tilanteissa:

- Kun sinulla on tyyppi, jonka kokoa ei voida tietää käännösaikana, ja haluat käyttää kyseisen tyypin arvoa kontekstissa, joka vaatii tarkan koon
- Kun sinulla on suuri määrä dataa ja haluat siirtää omistajuuden varmistaen, ettei dataa kopioida siirron yhteydessä
- Kun haluat omistaa arvon ja sinulle riittää, että se on tietyn traitin toteuttava tyyppi, etkä välitä sen tarkasta tyypistä

Ensimmäistä tilannetta käsitellään osiossa [”Rekursiivisten tyyppien mahdollistaminen boxeilla”](#enabling-recursive-types-with-boxes)<!-- ignore -->. Toisessa tapauksessa suuren datamäärän omistajuuden siirtäminen voi kestää kauan, koska dataa kopioidaan pinossa. Tämän tilanteen suorituskyvyn parantamiseksi voimme tallentaa suuren datamäärän keolle boxiin. Tällöin pinossa kopioidaan vain pieni määrä osoitindataa, kun taas sen viittaama data pysyy yhdessä paikassa keolla. Kolmatta tapausta kutsutaan _trait-olioksi_, ja [”Trait-objektien käyttö jaettuun käyttäytymiseen abstrahoimiseen”][trait-objects]<!-- ignore --> luvussa 18 on omistettu juuri tälle aiheelle. Siis tässä oppimasi soveltuu uudelleen siinä osiossa!

<!-- Old headings. Do not remove or links may break. -->

<a id="using-boxt-to-store-data-on-the-heap"></a>

### Datan tallentaminen keolle

Ennen kuin käsittelemme `Box<T>`:n käyttötapaa keon tallennukseen, käymme läpi syntaksin ja sen, miten `Box<T>`:n sisällä oleviin arvoihin viitataan.

Listauksessa 15-1 näytetään, miten boxilla tallennetaan `i32`-arvo keolle.

<Listing number="15-1" file-name="src/main.rs" caption="`i32`-arvon tallentaminen keolle boxin avulla">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-01/src/main.rs}}
```

</Listing>

Määrittelemme muuttujan `b` siten, että sen arvo on `Box`, joka osoittaa arvoon `5`, joka on allokoitu keolle. Tämä ohjelma tulostaa `b = 5`; tässä tapauksessa pääsemme boxin dataan käsiksi samalla tavalla kuin jos data olisi pinossa. Kuten minkä tahansa omistetun arvon kohdalla, kun box poistuu näkyvyysalueeltaan — kuten `b` tekee `main`-funktion lopussa — se vapautetaan. Vapautus koskee sekä boxia (joka on pinossa) että sen osoittamaa dataa (joka on keolla).

Yhden arvon sijoittaminen keolle ei ole kovin hyödyllistä, joten et käytä boxeja yksinään tällä tavalla usein. Arvojen, kuten yksittäisen `i32`:n, pitäminen pinossa, missä ne oletusarvoisesti tallennetaan, on sopivampaa useimmissa tilanteissa. Katsotaan seuraavaksi tapausta, jossa boxien avulla voimme määritellä tyyppejä, joita emme voisi määritellä ilman boxeja.

### Rekursiivisten tyyppien mahdollistaminen boxeilla

_Rekursiivisen tyypin_ arvo voi sisältää osanaan toisen saman tyypin arvon. Rekursiiviset tyypit aiheuttavat ongelman, koska Rustin on tiedettävä käännösaikana, kuinka paljon tilaa tyyppi vie. Rekursiivisten tyyppien arvojen sisäkkäisyys voisi kuitenkin teoriassa jatkua äärettömästi, joten Rust ei voi tietää, kuinka paljon tilaa arvo tarvitsee. Koska boxeilla on tunnettu koko, voimme mahdollistaa rekursiiviset tyypit lisäämällä boxin rekursiivisen tyypin määrittelyyn.

Esimerkkinä rekursiivisesta tyypistä tutustutaan cons-listaan. Tämä on funktionaalisten ohjelmointikielten yleinen tietorakenne. Määrittelemämme cons-listatyyppi on yksinkertainen paitsi rekursion osalta; siksi tässä esimerkissä käsiteltävät käsitteet ovat hyödyllisiä aina, kun kohtaat monimutkaisempia tilanteita, joissa on rekursiivisia tyyppejä.

<!-- Old headings. Do not remove or links may break. -->

<a id="more-information-about-the-cons-list"></a>

#### Cons-listan ymmärtäminen

_Cons-lista_ on Lisp-ohjelmointikielestä ja sen murreista peräisin oleva tietorakenne, joka koostuu sisäkkäisistä pareista ja on Lispin versio linkitetystä listasta. Sen nimi tulee Lispin `cons`-funktiosta (lyhenne sanasta _construct function_, rakennusfunktio), joka muodostaa uuden parin kahdesta argumentistaan. Kutsumalla `cons`:ia parille, joka koostuu arvosta ja toisesta parista, voimme rakentaa rekursiivisista pareista koostuvia cons-listoja.

Esimerkiksi tässä on pseudokoodiesitys cons-listasta, joka sisältää listan `1, 2, 3` siten, että jokainen pari on sulkeissa:

```text
(1, (2, (3, Nil)))
```

Jokainen cons-listan alkio sisältää kaksi elementtiä: nykyisen alkion arvon ja seuraavan alkion. Listan viimeinen alkio sisältää vain arvon nimeltä `Nil` ilman seuraavaa alkioita. Cons-lista syntyy kutsumalla `cons`-funktiota rekursiivisesti. Rekursion perustapauksen vakiintunut nimi on `Nil`. Huomaa, että tämä ei ole sama kuin luvussa 6 käsitelty ”null”- tai ”nil”-käsite, joka tarkoittaa virheellistä tai puuttuvaa arvoa.

Cons-lista ei ole Rustissa yleisesti käytetty tietorakenne. Useimmiten, kun Rustissa on lista alkioita, `Vec<T>` on parempi valinta. Muut, monimutkaisemmat rekursiiviset tietotyypit _ovat_ hyödyllisiä eri tilanteissa, mutta aloittamalla cons-listasta tässä luvussa voimme tutkia, miten boxien avulla voidaan määritellä rekursiivinen tietotyyppi ilman liikaa häiriötekijöitä.

Listauksessa 15-2 on enum-määrittely cons-listalle. Huomaa, että tämä koodi ei vielä käänny, koska `List`-tyypillä ei ole tunnettua kokoa, kuten demonstroimme.

<Listing number="15-2" file-name="src/main.rs" caption="Ensimmäinen yritys määritellä enum, joka edustaa `i32`-arvojen cons-listatietorakennetta">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-02/src/main.rs:here}}
```

</Listing>

> Huom: Toteutamme tässä esimerkissä cons-listan, joka sisältää vain `i32`-arvoja. Olisimme voineet toteuttaa sen geneerisesti, kuten käsittelimme luvussa 10, ja määritellä cons-listatyypin, joka voi tallentaa minkä tahansa tyyppisiä arvoja.

`List`-tyypin käyttö listan `1, 2, 3` tallentamiseen näyttäisi listauksen 15-3 koodilta.

<Listing number="15-3" file-name="src/main.rs" caption="`List`-enumin käyttö listan `1, 2, 3` tallentamiseen">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-03/src/main.rs:here}}
```

</Listing>

Ensimmäinen `Cons`-arvo sisältää `1`:n ja toisen `List`-arvon. Tämä `List`-arvo on toinen `Cons`-arvo, joka sisältää `2`:n ja toisen `List`-arvon. Tämä `List`-arvo on vielä yksi `Cons`-arvo, joka sisältää `3`:n ja `List`-arvon, joka on lopulta `Nil`, ei-rekursiivinen variantti, joka merkitsee listan loppua.

Jos yritämme kääntää listauksen 15-3 koodin, saamme listauksessa 15-4 näytetyn virheen.

<Listing number="15-4" caption="Virhe, jonka saamme yrittäessämme määritellä rekursiivisen enumin">

```console
{{#include ../listings/ch15-smart-pointers/listing-15-03/output.txt}}
```

</Listing>

Virhe kertoo, että tällä tyypillä on ”ääretön koko”. Syy on, että olemme määritelleet `List`:in variantilla, joka on rekursiivinen: se sisältää suoraan toisen saman tyypin arvon. Tämän vuoksi Rust ei pysty selvittämään, kuinka paljon tilaa `List`-arvon tallentaminen vaatii. Puretaan seuraavaksi, miksi saamme tämän virheen. Ensin katsomme, miten Rust päättää, kuinka paljon tilaa ei-rekursiivisen tyypin arvo tarvitsee.

#### Ei-rekursiivisen tyypin koon laskeminen

Muista `Message`-enum, jonka määrittelimme listauksessa 6-2, kun käsittelimme enum-määrittelyjä luvussa 6:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-02/src/main.rs:here}}
```

Selvittääkseen, kuinka paljon tilaa `Message`-arvon varaamiseen tarvitaan, Rust käy läpi jokaisen variantin ja katsoo, mikä niistä tarvitsee eniten tilaa. Rust näkee, että `Message::Quit` ei tarvitse lainkaan tilaa, `Message::Move` tarvitsee tilaa kahdelle `i32`-arvolle, ja niin edelleen. Koska vain yhtä varianttia käytetään kerrallaan, enimmäistila, jota `Message`-arvo tarvitsee, on suurimman variantin vaatima tila.

Vertaa tätä siihen, mitä tapahtuu, kun Rust yrittää selvittää, kuinka paljon tilaa rekursiivinen tyyppi, kuten listauksen 15-2 `List`-enum, tarvitsee. Kääntäjä aloittaa `Cons`-variantista, joka sisältää `i32`-tyyppisen arvon ja `List`-tyyppisen arvon. Siksi `Cons` tarvitsee tilaa, joka on yhtä suuri kuin `i32`:n koko plus `List`:in koko. Selvittääkseen, kuinka paljon muistia `List`-tyyppi tarvitsee, kääntäjä katsoo variantteja alkaen `Cons`-variantista. `Cons`-variantti sisältää `i32`-tyyppisen arvon ja `List`-tyyppisen arvon, ja tämä prosessi jatkuu äärettömästi, kuten kuvassa 15-1.

<img alt="Ääretön Cons-lista: suorakulmio, jossa lukee 'Cons' ja joka on jaettu kahteen pienempään suorakulmioon. Ensimmäisessä pienemmässä suorakulmiossa lukee 'i32', ja toisessa pienemmässä suorakulmiossa lukee 'Cons' sekä pienempi versio ulomman 'Cons'-suorakulmion sisällä. 'Cons'-suorakulmiot sisältävät yhä pienempiä versioita itsestään, kunnes pienin mukavasti kokoinen suorakulmio sisältää äärettömyyssymbolin, mikä osoittaa, että toisto jatkuu ikuisesti." src="img/trpl15-01.svg" class="center" style="width: 50%;" />

<span class="caption">Kuva 15-1: Ääretön `List`, joka koostuu äärettömistä `Cons`-varianteista</span>

<!-- Old headings. Do not remove or links may break. -->

<a id="using-boxt-to-get-a-recursive-type-with-a-known-size"></a>

#### Rekursiivisen tyypin saaminen tunnetulla koolla

Koska Rust ei pysty selvittämään, kuinka paljon tilaa rekursiivisesti määritellyille tyypeille varataan, kääntäjä antaa virheen ja tämän hyödyllisen ehdotuksen:

<!-- manual-regeneration
after doing automatic regeneration, look at listings/ch15-smart-pointers/listing-15-03/output.txt and copy the relevant line
-->

```text
help: insert some indirection (e.g., a `Box`, `Rc`, or `&`) to break the cycle
  |
2 |     Cons(i32, Box<List>),
  |               ++++    +
```

Tässä ehdotuksessa _epäsuora viittaus_ tarkoittaa, että arvon sijaan meidän pitäisi muuttaa tietorakennetta siten, että arvo tallennetaan epäsuorasti osoittamalla arvoon sen sijaan, että tallennettaisiin arvo suoraan.

Koska `Box<T>` on osoitin, Rust tietää aina, kuinka paljon tilaa `Box<T>` tarvitsee: osoittimen koko ei muutu sen mukaan, kuinka paljon dataa se osoittaa. Tämä tarkoittaa, että voimme laittaa `Box<T>`:n `Cons`-variantin sisään toisen `List`-arvon sijaan. `Box<T>` osoittaa seuraavaan `List`-arvoon, joka on keolla `Cons`-variantin sisällä olevan arvon sijaan. Käsitteellisesti meillä on edelleen lista, joka on luotu listoista, jotka sisältävät muita listoja, mutta tämä toteutus on nyt enemmän kuin alkioiden asettaminen vierekkäin toistensa sisään sijaan.

Voimme muuttaa listauksen 15-2 `List`-enumin määrittelyn ja listauksen 15-3 `List`:in käytön listauksen 15-5 koodiksi, joka kääntyy.

<Listing number="15-5" file-name="src/main.rs" caption="`List`-määrittely, joka käyttää `Box<T>`:tä tunnetun koon saamiseksi">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-05/src/main.rs}}
```

</Listing>

`Cons`-variantti tarvitsee `i32`:n koon plus tilan boxin osoitindatan tallentamiseen. `Nil`-variantti ei tallenna arvoja, joten se tarvitsee pinosta vähemmän tilaa kuin `Cons`-variantti. Nyt tiedämme, että mikä tahansa `List`-arvo vie `i32`:n koon plus boxin osoitindatan koon. Käyttämällä boxia olemme katkaisseet äärettömän rekursiivisen ketjun, joten kääntäjä pystyy selvittämään tarvitsemansa koon `List`-arvon tallentamiseen. Kuva 15-2 näyttää, miltä `Cons`-variantti näyttää nyt.

<img alt="Suorakulmio, jossa lukee 'Cons' ja joka on jaettu kahteen pienempään suorakulmioon. Ensimmäisessä pienemmässä suorakulmiossa lukee 'i32', ja toisessa pienemmässä suorakulmiossa lukee 'Box' sekä yksi sisäinen suorakulmio, jossa lukee 'usize' ja joka edustaa boxin osoittimen äärellistä kokoa." src="img/trpl15-02.svg" class="center" />

<span class="caption">Kuva 15-2: `List`, joka ei ole äärettömän kokoinen, koska `Cons` sisältää `Box`:in</span>

Boxit tarjoavat vain epäsuoran viittauksen ja keolle allokoinnin; niillä ei ole muita erityisominaisuuksia, kuten muilla älykkäillä osoittimilla, joihin tutustumme. Niillä ei myöskään ole niiden erityisominaisuuksien aiheuttamaa suorituskykyhaittaa, joten ne voivat olla hyödyllisiä cons-listan kaltaisissa tapauksissa, joissa epäsuora viittaus on ainoa tarvittava ominaisuus. Katsomme lisää boxien käyttötapauksia luvussa 18.

`Box<T>`-tyyppi on älykäs osoitin, koska se toteuttaa `Deref`-traitin, jonka ansiosta `Box<T>`-arvoja voidaan käsitellä viitteiden tavoin. Kun `Box<T>`-arvo poistuu näkyvyysalueeltaan, myös boxin osoittama keon data siivotaan `Drop`-traitin toteutuksen ansiosta. Nämä kaksi traitia ovat vielä tärkeämpiä muille älykkäille osoitintyypeille, joita käsittelemme loppuosassa tätä lukua. Tutustutaan seuraavaksi näihin kahteen traitiin tarkemmin.

[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
