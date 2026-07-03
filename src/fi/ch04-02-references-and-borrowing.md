## Viittaukset ja lainaaminen

Listauksen 4-5 tuplakoodin ongelma on, että meidän täytyy palauttaa `String` kutsuvalle funktiolle, jotta voimme edelleen käyttää `String`-arvoa
`calculate_length`-kutsun jälkeen, koska `String` siirtyi `calculate_length`-funktion omistukseen. Sen sijaan voimme tarjota viittauksen `String`-arvoon.
Viittaus on kuin osoitin siinä mielessä, että se on osoite, jota seuraamalla pääsemme kyseiseen osoitteeseen tallennettuun dataan; tämän datan omistaa jokin toinen muuttuja.
Toisin kuin osoitin, viittaus on taattu osoittamaan kelvollista tietyn tyyppistä arvoa koko viittauksen eliniän ajan.

Näin määrittelet ja käytät `calculate_length`-funktiota, joka ottaa viittauksen objektiin parametrinaan omistajuuden siirtämisen sijaan:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-07-reference/src/main.rs:all}}
```

</Listing>

Ensinnäkin huomaa, että kaikki tuplakoodi muuttujan määrityksessä ja funktion paluuarvossa on poissa. Toiseksi huomaa, että välitämme `&s1`:n
`calculate_length`-funktiolle ja sen määrityksessä otamme `&String`-tyypin `String`-tyypin sijaan. Nämä et-merkit edustavat viittauksia, ja niiden avulla voit
viitata johonkin arvoon ottamatta sen omistajuutta. Kuva 4-6 havainnollistaa tätä käsitettä.

<img alt="Three tables: the table for s contains only a pointer to the table
for s1. The table for s1 contains the stack data for s1 and points to the
string data on the heap." src="img/trpl04-06.svg" class="center" />

<span class="caption">Kuva 4-6: Kaavio `&String`-tyypin `s`:stä, joka osoittaa `String`-tyypin `s1`:een</span>

> Huom: Viittaamisen vastakohta `&`-merkillä on _dereferointi_, joka tehdään dereferointioperaattorilla `*`. Näemme dereferointioperaattorin käyttöä
> Luvussa 8 ja käsittelemme dereferoinnin yksityiskohdat Luvussa 15.

Katsotaan funktiokutsua tarkemmin:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-07-reference/src/main.rs:here}}
```

`&s1`-syntaksi antaa meidän luoda viittauksen, joka _viittaa_ `s1`:n arvoon mutta ei omista sitä. Koska viittaus ei omista sitä, arvoa, johon se osoittaa,
ei vapauteta, kun viittaus lakkaa olemasta käytössä.

Samoin funktion signatuuri käyttää `&`-merkkiä ilmaisemaan, että parametrin `s` tyyppi on viittaus. Lisätään selittäviä annotaatioita:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-08-reference-with-annotations/src/main.rs:here}}
```

Näkyvyysalue, jolla muuttuja `s` on kelvollinen, on sama kuin minkä tahansa funktion parametrin näkyvyysalue, mutta viittauksen osoittamaa arvoa ei vapauteta,
kun `s` lakkaa olemasta käytössä, koska `s`:llä ei ole omistajuutta. Kun funktioilla on viittauksia parametreina todellisten arvojen sijaan, meidän ei tarvitse
palauttaa arvoja omistajuuden palauttamiseksi, koska emme koskaan omistaneet niitä.

Kutsumme viittauksen luomista _lainaamiseksi_. Kuten oikeassa elämässä, jos henkilö omistaa jotain, voit lainata sen häneltä. Kun olet valmis, sinun täytyy
palauttaa se. Et omista sitä.

Mitä tapahtuu, jos yritämme muuttaa jotain, mitä lainaamme? Kokeile Listauksen 4-6 koodia. Varoitus: se ei toimi!

<Listing number="4-6" file-name="src/main.rs" caption="Yritys muuttaa lainattua arvoa">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-06/src/main.rs}}
```

</Listing>

Tässä on virhe:

```console
{{#include ../listings/ch04-understanding-ownership/listing-04-06/output.txt}}
```

Aivan kuten muuttujat ovat oletusarvoisesti muuttumattomia, viittauksetkin ovat. Emme saa muuttaa jotain, johon meillä on viittaus.

### Muuttuvat viittaukset

Voimme korjata Listauksen 4-6 koodin sallimaan lainatun arvon muuttamisen muutamalla pienellä muutoksella, jotka käyttävät _muuttuvaa viittausta_:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-09-fixes-listing-04-06/src/main.rs}}
```

</Listing>

Ensin muutamme `s`:n muotoon `mut`. Sitten luomme muuttuvan viittauksen `&mut s`:llä, kun kutsumme `change`-funktiota, ja päivitämme funktion signatuurin
hyväksymään muuttuvan viittauksen `some_string: &mut String`. Tämä tekee hyvin selväksi, että `change`-funktio muuttaa lainaamaansa arvoa.

Muuttuvilla viittauksilla on yksi suuri rajoitus: jos sinulla on muuttuva viittaus arvoon, sinulla ei voi olla muita viittauksia kyseiseen arvoon. Tämä koodi,
joka yrittää luoda kaksi muuttuvaa viittausta `s`:ään, epäonnistuu:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-10-multiple-mut-not-allowed/src/main.rs:here}}
```

</Listing>

Tässä on virhe:

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-10-multiple-mut-not-allowed/output.txt}}
```

Tämä virheilmoitus sanoo, että koodi on virheellinen, koska emme voi lainata `s`:ää muuttuvana useammin kuin kerran kerrallaan. Ensimmäinen muuttuva lainaus on
`r1`:ssä ja sen täytyy kestää siihen asti, kunnes sitä käytetään `println!`:ssä, mutta tuon muuttuvan viittauksen luomisen ja sen käytön välissä yritimme luoda
toisen muuttuvan viittauksen `r2`:ssa, joka lainaa samoja tietoja kuin `r1`.

Rajoitus, joka estää useita muuttuvia viittauksia samoihin tietoihin samaan aikaan, sallii mutaation, mutta hyvin kontrolloidulla tavalla. Uusien rustilaisien
on vaikea tottua siihen, koska useimmat kielet sallivat mutaation milloin tahansa. Tämän rajoituksen hyöty on, että Rust voi estää data race -tilanteet
käännösaikana. _Data race_ on samankaltainen kuin kilpailutilanne (race condition), ja se tapahtuu, kun nämä kolme käyttäytymistä esiintyvät:

- Kaksi tai useampi osoitin käyttää samoja tietoja samaan aikaan.
- Vähintään yhtä osoittimista käytetään kirjoittamaan dataan.
- Mitään mekanismia ei käytetä synkronoimaan pääsyä dataan.

Data race -tilanteet aiheuttavat määrittelemätöntä käyttäytymistä, ja niitä voi olla vaikea diagnosoida ja korjata ajonaikana; Rust estää tämän ongelman
kieltäytymällä kääntämästä data race -tilanteita sisältävää koodia!

Kuten aina, voimme käyttää aaltosulkeita luodaksemme uuden näkyvyysalueen, mikä sallii useita muuttuvia viittauksia, mutta ei _samanaikaisia_:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-11-muts-in-separate-scopes/src/main.rs:here}}
```

Rust pakottaa samanlaisen säännön muuttuvien ja muuttumattomien viittausten yhdistämiselle. Tämä koodi johtaa virheeseen:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-12-immutable-and-mutable-not-allowed/src/main.rs:here}}
```

Tässä on virhe:

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-12-immutable-and-mutable-not-allowed/output.txt}}
```

Huh! Emme _myöskään_ voi omistaa muuttuvaa viittausta, kun meillä on muuttumaton viittaus samaan arvoon.

Muuttumattoman viittauksen käyttäjät eivät odota arvon muuttuvan yllättäen altaan! Useita muuttumattomia viittauksia sallitaan kuitenkin, koska kukaan, joka
vain lukee dataa, ei voi vaikuttaa kenenkään muun datan lukemiseen.

Huomaa, että viittauksen näkyvyysalue alkaa siitä, missä se esitellään, ja jatkuu viimeiseen kertaan, jolloin viittausta käytetään. Esimerkiksi tämä koodi
kääntyy, koska muuttumattomien viittausten viimeinen käyttö on `println!`:ssä, ennen kuin muuttuva viittaus esitellään:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-13-reference-scope-ends/src/main.rs:here}}
```

Muuttumattomien viittausten `r1`:n ja `r2`:n näkyvyysalueet päättyvät `println!`:n jälkeen, missä niitä käytetään viimeisen kerran, eli ennen kuin muuttuva
viittaus `r3` luodaan. Nämä näkyvyysalueet eivät limitty, joten tämä koodi on sallittu: kääntäjä voi päätellä, ettei viittausta enää käytetä ennen
näkyvyysalueen päättymistä.

Vaikka lainausvirheet voivat joskus turhauttaa, muista, että Rust-kääntäjä osoittaa mahdollisen bugin varhain (käännösaikana ajonaikaisen sijaan) ja näyttää
tarkalleen, missä ongelma on. Sinun ei sitten tarvitse selvittää, miksi datasi ei ole sitä, mitä luulit sen olevan.

### Riippuvat viittaukset

Kielissä, joissa on osoittimia, on helppo luoda virheellisesti _riippuvan osoittimen_ — osoittimen, joka viittaa muistipaikkaan, joka on saatettu antaa
jollekulle muulle — vapauttamalla muistia mutta säilyttämällä osoitin kyseiseen muistiin. Rustissa kääntäjä puolestaan takaa, ettei viittauksia koskaan ole
riippuvia: jos sinulla on viittaus johonkin dataan, kääntäjä varmistaa, ettei data poistu näkyvyysalueelta ennen kuin viittaus siihen poistuu.

Yritetään luoda riippuva viittaus nähdäksemme, miten Rust estää ne käännösaikaisella virheellä:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-14-dangling-reference/src/main.rs}}
```

</Listing>

Tässä on virhe:

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-14-dangling-reference/output.txt}}
```

Tämä virheilmoitus viittaa ominaisuuteen, jota emme ole vielä käsitelleet: elinikäihin. Käsittelemme elinikäitä yksityiskohtaisesti Luvussa 10. Mutta jos
sivuutat elinikäisiin liittyvät osat, viesti sisältää avaimen siihen, miksi tämä koodi on ongelma:

```text
this function's return type contains a borrowed value, but there is no value
for it to be borrowed from
```

Katsotaan tarkemmin, mitä tapahtuu `dangle`-koodimme jokaisessa vaiheessa:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-15-dangling-reference-annotated/src/main.rs:here}}
```

</Listing>

Koska `s` luodaan `dangle`-funktion sisällä, kun `dangle`-funktion koodi on valmis, `s` vapautetaan. Mutta yritimme palauttaa viittauksen siihen. Tämä
tarkoittaa, että viittaus osoittaisi virheelliseen `String`-arvoon. Se ei käy! Rust ei anna meidän tehdä tätä.

Ratkaisu on palauttaa `String` suoraan:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-16-no-dangle/src/main.rs:here}}
```

Tämä toimii ilman ongelmia. Omistajuus siirtyy ulos, eikä mitään vapauteta.

### Viittausten säännöt

Kerrataan, mitä olemme käsitelleet viittauksista:

- Milloin tahansa voit omistaa _joko_ yhden muuttuvan viittauksen _tai_ minkä tahansa määrän muuttumattomia viittauksia.
- Viittausten on aina oltava kelvollisia.

Seuraavaksi tarkastelemme erilaista viittaustyyppiä: sliceja.
