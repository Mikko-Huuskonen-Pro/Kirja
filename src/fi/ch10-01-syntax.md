## Geneeriset tietotyypit

Käytämme geneerisiä tyyppejä luodaksemme määritelmiä esimerkiksi funktioiden
allekirjoituksille tai structeille, joita voimme sitten käyttää monilla eri
konkreettisilla tietotyypeillä. Aloitetaan katsomalla, miten funktioita,
structeja, enum-arvoja ja metodeja määritellään geneeristen tyyppien avulla.
Sen jälkeen käsittelemme, miten geneeriset tyypit vaikuttavat koodin
suorituskykyyn.

### Funktiomäärittelyissä

Kun määrittelemme funktion, joka käyttää geneerisiä tyyppejä, sijoitamme
geneeriset tyypit funktion allekirjoitukseen sinne, missä yleensä määrittelemme
parametrien ja palautusarvon tietotyypit. Näin koodistamme tulee joustavampaa ja
se tarjoaa kutsujille enemmän toiminnallisuutta samalla kun vältämme koodin
toistamista.

Jatkamme `largest`-funktion parissa. Listaus 10-4 näyttää kaksi funktiota, jotka
molemmat etsivät suurimman arvon viipaleesta. Yhdistämme ne sitten yhdeksi
funktioksi, joka käyttää geneerisiä tyyppejä.

<Listing number="10-4" file-name="src/main.rs" caption="Kaksi funktiota, jotka eroavat vain nimissään ja allekirjoituksissa olevissa tyypeissään">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-04/src/main.rs:here}}
```

</Listing>

Funktio `largest_i32` on se, jonka erotimme listauksessa 10-3 ja joka etsii
suurimman `i32`-arvon viipaleesta. Funktio `largest_char` etsii suurimman
`char`-arvon viipaleesta. Funktioiden rungot ovat samanlaiset, joten poistamme
toiston ottamalla käyttöön geneerisen tyyppiparametrin yhdessä funktiossa.

Parametroidaksemme tyypit uudessa yhdessä funktiossa meidän täytyy nimetä
tyyppiparametri, aivan kuten teemme arvoparametreille funktiossa. Voit käyttää
mitä tahansa tunnistetta tyyppiparametrin nimenä. Käytämme kuitenkin `T`:tä,
koska Rustin käytännön mukaan tyyppiparametrien nimet ovat lyhyitä, usein vain
yksi kirjain, ja Rustin tyyppien nimeämiskäytäntö on UpperCamelCase. Lyhenne
sanasta _type_, `T` on useimpien Rust-ohjelmoijien oletusvalinta.

Kun käytämme parametria funktion rungossa, meidän täytyy ilmoittaa parametrin
nimi allekirjoituksessa, jotta kääntäjä tietää, mitä nimi tarkoittaa.
Vastaavasti, kun käytämme tyyppiparametrin nimeä funktion allekirjoituksessa,
meidän täytyy ilmoittaa tyyppiparametrin nimi ennen kuin käytämme sitä.
Määritelläksemme geneerisen `largest`-funktion sijoitamme tyyppinimien
ilmoitukset kulmasulkeisiin `<>` funktion nimen ja parametrilistan väliin,
näin:

```rust,ignore
fn largest<T>(list: &[T]) -> &T {
```

Luemme tämän määrittelyn näin: ”Funktio `largest` on geneerinen jonkin tyypin
`T` suhteen.” Tällä funktiolla on yksi parametri nimeltä `list`, joka on
tyypin `T` arvojen viipale. Funktio `largest` palauttaa viittauksen arvoon,
jonka tyyppi on sama `T`.

Listaus 10-5 näyttää yhdistetyn `largest`-funktion määrittelyn, joka käyttää
geneeristä tietotyyppiä allekirjoituksessaan. Listaus näyttää myös, miten
funktiota voidaan kutsua joko `i32`-arvojen tai `char`-arvojen viipaleella.
Huomaa, että tämä koodi ei vielä käänny.

<Listing number="10-5" file-name="src/main.rs" caption="`largest`-funktio, joka käyttää geneerisiä tyyppiparametreja; tämä ei vielä käänny">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-05/src/main.rs}}
```

</Listing>

Jos käännämme tämän koodin nyt, saamme seuraavan virheen:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-05/output.txt}}
```

Ohjeteksti mainitsee `std::cmp::PartialOrd`, joka on trait, ja käsittelemme
traitteja seuraavassa osiossa. Toistaiseksi tiedä, että tämä virhe kertoo,
että `largest`-funktion runko ei toimi kaikille mahdollisille tyypeille, joita
`T` voisi olla. Koska haluamme vertailla tyypin `T` arvoja rungossa, voimme
käyttää vain tyyppejä, joiden arvoja voidaan järjestää. Vertailujen
mahdollistamiseksi standardikirjasto tarjoaa `std::cmp::PartialOrd`-traitin,
jonka voit toteuttaa tyypeille (katso lisätietoja liitteestä C). Korjataksemme
listauksen 10-5 voimme seurata ohjetekstin ehdotusta ja rajoittaa tyypit,
jotka kelpaavat `T`:lle, vain niihin, jotka toteuttavat `PartialOrd`-traitin.
Listaus kääntyy silloin, koska standardikirjasto toteuttaa `PartialOrd`-traitin
sekä `i32`- että `char`-tyypeille.

### Struct-määrittelyissä

Voimme myös määritellä structeja käyttämään geneeristä tyyppiparametria
yhdessä tai useammassa kentässä `<>`-syntaksilla. Listaus 10-6 määrittelee
`Point<T>`-structin, joka säilyttää `x`- ja `y`-koordinaattiarvot minkä
tyyppisinä tahansa.

<Listing number="10-6" file-name="src/main.rs" caption="`Point<T>`-struct, joka säilyttää tyypin `T` arvot `x` ja `y`">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-06/src/main.rs}}
```

</Listing>

Syntaksi geneeristen tyyppien käyttöön struct-määrittelyissä on samanlainen
kuin funktiomäärittelyissä. Ensin ilmoitamme tyyppiparametrin nimen
kulmasulkeissa heti structin nimen jälkeen. Sitten käytämme geneeristä tyyppiä
struct-määrittelyssä siinä kohdassa, missä muuten määrittelisimme konkreettiset
tietotyypit.

Huomaa, että koska olemme käyttäneet vain yhtä geneeristä tyyppiä
määritellessämme `Point<T>`:n, tämä määrittely sanoo, että `Point<T>`-struct
on geneerinen jonkin tyypin `T` suhteen ja kentät `x` ja `y` ovat _molemmat_
samaa tyyppiä, mikä se tyyppi sitten onkaan. Jos luomme `Point<T>`-instanssin,
jonka arvot ovat eri tyyppejä, kuten listauksessa 10-7, koodimme ei käänny.

<Listing number="10-7" file-name="src/main.rs" caption="Kenttien `x` ja `y` täytyy olla samaa tyyppiä, koska molemmat käyttävät samaa geneeristä tietotyyppiä `T`.">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-07/src/main.rs}}
```

</Listing>

Tässä esimerkissä, kun annamme kokonaislukuarvon `5` muuttujalle `x`, kerromme
kääntäjälle, että geneerinen tyyppi `T` on kokonaisluku tässä `Point<T>`-
instanssissa. Kun määrittelemme `4.0` muuttujalle `y`, jonka olemme määritelleet
samaan tyyppiin kuin `x`, saamme tyyppivirheen, joka näyttää tältä:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-07/output.txt}}
```

Määritelläksemme `Point`-structin, jossa `x` ja `y` ovat molemmat geneerisiä
mutta voivat olla eri tyyppejä, voimme käyttää useita geneerisiä
tyyppiparametreja. Esimerkiksi listauksessa 10-8 muutamme `Point`-structin
määrittelyn geneeriseksi tyypeille `T` ja `U`, jossa `x` on tyyppiä `T` ja `y`
on tyyppiä `U`.

<Listing number="10-8" file-name="src/main.rs" caption="`Point<T, U>` geneerinen kahden tyypin suhteen, jotta `x` ja `y` voivat olla eri tyyppisiä arvoja">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-08/src/main.rs}}
```

</Listing>

Nyt kaikki näytetyt `Point`-instanssit ovat sallittuja! Voit käyttää
määrittelyssä niin monta geneeristä tyyppiparametria kuin haluat, mutta
useamman kuin muutaman käyttö tekee koodista vaikealukuista. Jos huomaat
tarvitsevasi paljon geneerisiä tyyppejä koodissasi, se voi viitata siihen, että
koodisi kaipaa uudelleenjärjestelyä pienempiin osiin.

### Enum-määrittelyissä

Kuten structeissa, voimme määritellä enum-arvoja säilyttämään geneerisiä
tietotyyppejä variantteihinsa. Katsotaan vielä kerran `Option<T>`-enum-arvoa,
jonka standardikirjasto tarjoaa ja jota käytimme luvussa 6:

```rust
enum Option<T> {
    Some(T),
    None,
}
```

Tämän määrittelyn pitäisi nyt olla selkeämpi. Kuten näet, `Option<T>`-enum on
geneerinen tyypin `T` suhteen ja sillä on kaksi varianttia: `Some`, joka
säilyttää yhden arvon tyypistä `T`, ja variantti `None`, joka ei säilytä
mitään arvoa. Käyttämällä `Option<T>`-enum-arvoa voimme ilmaista abstraktin
käsitteen valinnaisesta arvosta, ja koska `Option<T>` on geneerinen, voimme
käyttää tätä abstraktiota riippumatta valinnaisen arvon tyypistä.

Enum-arvot voivat käyttää myös useita geneerisiä tyyppejä. `Result`-enum-arvon
määrittely, jota käytimme luvussa 9, on yksi esimerkki:

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

`Result`-enum on geneerinen kahden tyypin, `T` ja `E`, suhteen ja sillä on kaksi
varianttia: `Ok`, joka säilyttää arvon tyypistä `T`, ja `Err`, joka säilyttää
arvon tyypistä `E`. Tämä määrittely tekee `Result`-enum-arvon käytöstä
kätevää missä tahansa, missä operaatio voi onnistua (palauttaa arvon jonkin
tyypin `T`) tai epäonnistua (palauttaa virheen jonkin tyypin `E`). Tätä
käytimme avatessamme tiedoston listauksessa 9-3, jossa `T` täytettiin tyypillä
`std::fs::File`, kun tiedosto avattiin onnistuneesti, ja `E` täytettiin tyypillä
`std::io::Error`, kun tiedoston avaamisessa oli ongelmia.

Kun tunnistat koodissasi tilanteita, joissa on useita struct- tai enum-
määrittelyjä, jotka eroavat vain säilyttämiensä arvojen tyypeistä, voit välttää
toiston käyttämällä geneerisiä tyyppejä.

### Metodimäärittelyissä

Voimme toteuttaa metodeja structeille ja enum-arvoille (kuten teimme luvussa 5)
ja käyttää geneerisiä tyyppejä niiden määrittelyissäkin. Listaus 10-9 näyttää
`Point<T>`-structin, jonka määrittelimme listauksessa 10-6, ja siihen
toteutetun `x`-nimisen metodin.

<Listing number="10-9" file-name="src/main.rs" caption="Metodin `x` toteuttaminen `Point<T>`-structille, joka palauttaa viittauksen kentän `x` arvoon tyypistä `T`">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-09/src/main.rs}}
```

</Listing>

Tässä olemme määritelleet `Point<T>`-structille metodin nimeltä `x`, joka
palauttaa viittauksen kentän `x` dataan.

Huomaa, että meidän täytyy ilmoittaa `T` heti `impl`-avainsanan jälkeen, jotta
voimme käyttää `T`:tä määrittääksemme, että toteutamme metodeja tyypille
`Point<T>`. Ilmoittamalla `T`:n geneeriseksi tyypiksi `impl`-avainsanan
jälkeen Rust tunnistaa, että kulmasulkeissa `Point`-tyypin jälkeen oleva tyyppi
on geneerinen tyyppi eikä konkreettinen tyyppi. Olisimme voineet valita
erilaisen nimen tälle geneeriselle parametrille kuin struct-määrittelyssä
ilmoitettu geneerinen parametri, mutta saman nimen käyttö on käytäntö. Jos
kirjoitat metodin `impl`-lohkon sisällä, joka ilmoittaa geneerisen tyypin, se
metodi määritellään minkä tahansa tyypin instanssille, riippumatta siitä, mikä
konkreettinen tyyppi korvaa geneerisen tyypin.

Voimme myös määrittää rajoituksia geneerisille tyypeille määritellessämme
metodeja tyypille. Voisimme esimerkiksi toteuttaa metodeja vain `Point<f32>`-
instansseille eikä `Point<T>`-instansseille millä tahansa geneerisellä
tyypillä. Listauksessa 10-10 käytämme konkreettista tyyppiä `f32`, mikä
tarkoittaa, että emme ilmoita mitään tyyppejä `impl`-avainsanan jälkeen.

<Listing number="10-10" file-name="src/main.rs" caption="`impl`-lohko, joka koskee vain structia, jonka geneerisen tyyppiparametrin `T` konkreettinen tyyppi on tietty">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-10/src/main.rs:here}}
```

</Listing>

Tämä koodi tarkoittaa, että tyypillä `Point<f32>` on `distance_from_origin`-
metodi; muilla `Point<T>`-instansseilla, joissa `T` ei ole tyyppiä `f32`, ei
ole tätä metodia määriteltynä. Metodi mittaa, kuinka kaukana pisteemme on
pisteestä koordinaateissa (0.0, 0.0), ja käyttää matemaattisia operaatioita,
jotka ovat käytettävissä vain liukulukutyypeille.

Struct-määrittelyssä olevat geneeriset tyyppiparametrit eivät aina ole samoja
kuin saman structin metodien allekirjoituksissa käytetyt. Listaus 10-11 käyttää
geneerisiä tyyppejä `X1` ja `Y1` `Point`-structille ja `X2` ja `Y2`
`mixup`-metodin allekirjoituksessa selkeyttääkseen esimerkkiä. Metodi luo uuden
`Point`-instanssin, jossa `x`-arvo tulee `self`-`Point`-instanssista (tyyppiä
`X1`) ja `y`-arvo annetusta `Point`-instanssista (tyyppiä `Y2`).

<Listing number="10-11" file-name="src/main.rs" caption="Metodi, joka käyttää geneerisiä tyyppejä, jotka eroavat structin määrittelystä">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-11/src/main.rs}}
```

</Listing>

Funktiossa `main` olemme määritelleet `Point`-instanssin, jossa `x` on `i32`
(arvolla `5`) ja `y` on `f64` (arvolla `10.4`). Muuttuja `p2` on `Point`-
struct, jossa `x` on merkkijonoviipale (arvolla `"Hello"`) ja `y` on `char`
(arvolla `c`). Kutsumalla `mixup`-metodia `p1`:llä argumenttina `p2` saamme
`p3`:n, jossa `x` on `i32`, koska `x` tuli `p1`:stä. Muuttujassa `p3` `y` on
`char`, koska `y` tuli `p2`:sta. `println!`-makrokutsu tulostaa `p3.x = 5,
p3.y = c`.

Tämän esimerkin tarkoitus on demonstroida tilanne, jossa jotkut geneeriset
parametrit ilmoitetaan `impl`-avainsanalla ja jotkut metodin määrittelyssä.
Tässä geneeriset parametrit `X1` ja `Y1` ilmoitetaan `impl`-avainsanan
jälkeen, koska ne liittyvät struct-määrittelyyn. Geneeriset parametrit `X2` ja
`Y2` ilmoitetaan `fn mixup`-kohdan jälkeen, koska ne ovat merkityksellisiä
vain metodille.

### Geneerisiä tyyppejä käyttävän koodin suorituskyky

Saatat miettiä, aiheutuuko geneeristen tyyppiparametrien käytöstä ajonaikainen
kustannus. Hyvä uutinen on, että geneeristen tyyppien käyttö ei hidasta
ohjelmaasi verrattuna konkreettisiin tyyppeihin.

Rust saavuttaa tämän suorittamalla monomorfisoinnin (*monomorphization*)
geneeristä koodista käännösaikana. _Monomorfisointi_ on prosessi, jossa
geneerinen koodi muutetaan tiettyyn koodiin täyttämällä konkreettiset tyypit,
joita käytetään käännöksen yhteydessä. Tässä prosessissa kääntäjä tekee
vastakkaisen kuin vaiheet, joilla loimme geneerisen funktion listauksessa 10-5:
Kääntäjä tarkastaa kaikki kohdat, joissa geneeristä koodia kutsutaan, ja
generoi koodin konkreettisille tyypeille, joilla geneeristä koodia kutsutaan.

Katsotaan, miten tämä toimii käyttämällä standardikirjaston geneeristä
`Option<T>`-enum-arvoa:

```rust
let integer = Some(5);
let float = Some(5.0);
```

Kun Rust kääntää tämän koodin, se suorittaa monomorfisoinnin. Tämän prosessin
aikana kääntäjä lukee arvot, joita on käytetty `Option<T>`-instansseissa, ja
tunnistaa kaksi `Option<T>`-tyyppiä: toinen on `i32` ja toinen `f64`. Näin se
laajentaa `Option<T>`:n geneerisen määrittelyn kahteen `i32`- ja `f64`-
erikoistuneeseen määrittelyyn korvaten geneerisen määrittelyn tiettyillä
määrittelyillä.

Monomorfisoidun version koodi näyttää suunnilleen seuraavalta (kääntäjä käyttää
eri nimiä kuin mitä käytämme tässä havainnollistukseen):

<Listing file-name="src/main.rs">

```rust
enum Option_i32 {
    Some(i32),
    None,
}

enum Option_f64 {
    Some(f64),
    None,
}

fn main() {
    let integer = Option_i32::Some(5);
    let float = Option_f64::Some(5.0);
}
```

</Listing>

Geneerinen `Option<T>` korvataan kääntäjän luomilla tiettyillä määrittelyillä.
Koska Rust kääntää geneerisen koodin koodiksi, joka määrittää tyypin jokaisessa
instanssissa, emme maksa ajonaikaista kustannusta geneeristen tyyppien
käytöstä. Kun koodi suoritetaan, se toimii aivan kuten jos olisimme
monistaneet jokaisen määrittelyn käsin. Monomorfisointiprosessi tekee Rustin
geneerisistä tyypeistä erittäin tehokkaita ajonaikana.
