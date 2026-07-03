## Geneeriset tietotyypit

Käytämme geneerisiä tyyppejä luodaksemme määrityksiä esimerkiksi funktioiden
allekirjoituksille tai rakenteille, joita voimme sitten käyttää monien erilaisten
konkreettisten tietotyyppien kanssa. Katsotaan ensin, miten määritellään
funktioita, rakenteita, luetteloita ja metodeja käyttämällä geneerisiä tyyppejä.
Sen jälkeen keskustelemme siitä, miten geneerisyys vaikuttaa koodin suorituskykyyn.

### Funktiomäärityksissä

Kun määrittelemme geneerisiä tyyppejä käyttävän funktion, sijoitamme geneeriset
tyypit funktion allekirjoitukseen sinne, missä yleensä määrittelemme parametrien
ja paluuarvon tietotyypit. Näin koodistamme tulee joustavampaa ja se tarjoaa
enemmän toiminnallisuutta funktioidemme kutsumisille samalla kun estää koodin
toistumisen.

Jatkamme `largest`-funktiollamme. Listaus 10-4 näyttää kaksi funktiota, jotka
molemmat etsivät suurimman arvon viipaleesta. Yhdistämme ne sitten yhdeksi
geneerisiä tyyppejä käyttäväksi funktioksi.

<Listing number="10-4" file-name="src/main.rs" caption="Kaksi funktiota, jotka eroavat vain nimissään ja allekirjoituksensa tyypeissä">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-04/src/main.rs:here}}
```

</Listing>

`largest_i32`-funktio on se, jonka erotimme listauksesta 10-3 ja joka etsii
suurimman `i32`-arvon viipaleesta. `largest_char`-funktio etsii suurimman
`char`-arvon viipaleesta. Funktioiden rungot sisältävät saman koodin, joten
poistetaan toisto ottamalla käyttöön geneerinen tyyppiparametri yhdessä
funktiossa.

Parametroidaksemme tyypit uudessa yksittäisessä funktiossa meidän täytyy nimetä
tyyppiparametri, aivan kuten teemme arvoparametreille funktiossa. Voit käyttää
mitä tahansa tunnistetta tyyppiparametrin nimenä. Käytämme kuitenkin `T`:tä,
koska Rustin tapana on, että tyyppiparametrien nimet ovat lyhyitä, usein vain
yksi kirjain, ja Rustin tyyppien nimeämiskäytäntö on CamelCase. Lyhenne sanasta
_type_, `T` on useimpien Rust-ohjelmoijien oletusvalinta.

Kun käytämme parametria funktion rungossa, meidän täytyy ilmoittaa parametrin
nimi allekirjoituksessa, jotta kääntäjä tietää, mitä tuo nimi tarkoittaa.
Vastaavasti, kun käytämme tyyppiparametrin nimeä funktion allekirjoituksessa,
meidän täytyy ilmoittaa tyyppiparametrin nimi ennen sen käyttöä. Määritelläksemme
geneerisen `largest`-funktion sijoitamme tyyppinimien ilmoitukset kulmasulkeisiin
`<>`, funktion nimen ja parametrilistan väliin, näin:

```rust,ignore
fn largest<T>(list: &[T]) -> &T {
```

Luemme tämän määrityksen näin: funktio `largest` on geneerinen jonkin tyypin
`T` suhteen. Tällä funktiolla on yksi parametri nimeltä `list`, joka on
viipale arvoista tyyppiä `T`. `largest`-funktio palauttaa viittauksen arvoon
samaa tyyppiä `T`.

Listaus 10-5 näyttää yhdistetyn `largest`-funktiomäärityksen, joka käyttää
geneeristä tietotyyppiä allekirjoituksessaan. Listaus näyttää myös, miten
voimme kutsua funktiota joko `i32`-arvojen tai `char`-arvojen viipaleella.
Huomaa, että tämä koodi ei vielä käänny, mutta korjaamme sen myöhemmin tässä
luvussa.

<Listing number="10-5" file-name="src/main.rs" caption="`largest`-funktio geneerisillä tyyppiparametreilla; tämä ei vielä käänny">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-05/src/main.rs}}
```

</Listing>

Jos käännämme tämän koodin nyt, saamme tämän virheen:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-05/output.txt}}
```

Ohjeteksti mainitsee `std::cmp::PartialOrd`, joka on _trait_, ja käsittelemme
traitteja seuraavassa osiossa. Toistaiseksi tiedä, että tämä virhe kertoo,
että `largest`-funktion runko ei toimi kaikille mahdollisille tyypeille, joita
`T` voisi olla. Koska haluamme vertailla tyyppiä `T` olevia arvoja rungossa,
voimme käyttää vain tyyppejä, joiden arvoja voidaan järjestää. Vertailujen
mahdollistamiseksi standardikirjastossa on `std::cmp::PartialOrd`-trait, jonka
voit toteuttaa tyypeille (katso lisätietoja liitteestä C). Seuraamalla
ohjetekstin ehdotusta rajoitamme `T`:lle kelvolliset tyypit vain niihin, jotka
toteuttavat `PartialOrd`-traitin, ja tämä esimerkki kääntyy, koska
standardikirjasto toteuttaa `PartialOrd`-traitin sekä `i32`- että `char`-tyypeille.

### Rakentemäärityksissä

Voimme myös määritellä rakenteita käyttämään geneeristä tyyppiparametria
yhdessä tai useammassa kentässä `<>`-syntaksilla. Listaus 10-6 määrittelee
`Point<T>`-rakenteen `x`- ja `y`-koordinaattiarvojen tallentamiseen millä
tahansa tyypillä.

<Listing number="10-6" file-name="src/main.rs" caption="`Point<T>`-rakenne, joka pitää `x`- ja `y`-arvot tyyppiä `T`">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-06/src/main.rs}}
```

</Listing>

Geneeristen tyyppien käyttösyntaksi rakentemäärityksissä on samanlainen kuin
funktiomäärityksissä käytetty. Ensin ilmoitamme tyyppiparametrin nimen
kulmasulkeissa heti rakenteen nimen jälkeen. Sitten käytämme geneeristä tyyppiä
rakenteen määrityksessä siinä, missä muuten määrittelisimme konkreettiset
tietotyypit.

Huomaa, että koska olemme käyttäneet vain yhtä geneeristä tyyppiä määritellessämme
`Point<T>`-rakennetta, tämä määritys sanoo, että `Point<T>`-rakenne on geneerinen
jonkin tyypin `T` suhteen, ja kentät `x` ja `y` ovat _molemmat_ samaa tyyppiä,
mikä tuo tyyppi sitten onkin. Jos luomme `Point<T>`-instanssin, jolla on eri
tyyppisiä arvoja, kuten listauksessa 10-7, koodimme ei käänny.

<Listing number="10-7" file-name="src/main.rs" caption="Kenttien `x` ja `y` täytyy olla samaa tyyppiä, koska molemmilla on sama geneerinen tietotyyppi `T`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-07/src/main.rs}}
```

</Listing>

Tässä esimerkissä, kun annamme kokonaislukuarvon `5` muuttujalle `x`, kerromme
kääntäjälle, että geneerinen tyyppi `T` on kokonaisluku tälle `Point<T>`-instanssille.
Kun määrittelemme sitten `4.0` muuttujalle `y`, jonka olemme määritelty olevan
samaa tyyppiä kuin `x`, saamme tyyppien yhteensopimattomuusvirheen, joka näyttää
tältä:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-07/output.txt}}
```

Määritelläksemme `Point`-rakenteen, jossa `x` ja `y` ovat molemmat geneerisiä
mutta voivat olla eri tyyppejä, voimme käyttää useita geneerisiä tyyppiparametreja.
Esimerkiksi listauksessa 10-8 muutamme `Point`-rakenteen määrityksen olemaan
geneerinen tyypeille `T` ja `U`, joissa `x` on tyyppiä `T` ja `y` on tyyppiä `U`.

<Listing number="10-8" file-name="src/main.rs" caption="`Point<T, U>` geneerinen kahden tyypin suhteen, jotta `x` ja `y` voivat olla eri tyyppisiä arvoja">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-08/src/main.rs}}
```

</Listing>

Nyt kaikki näytetyt `Point`-instanssit ovat sallittuja! Voit käyttää määrityksessä
niin monta geneeristä tyyppiparametria kuin haluat, mutta useamman kuin muutaman
käyttö tekee koodistasi vaikeasti luettavaa. Jos huomaat tarvitsevasi paljon
geneerisiä tyyppejä koodissasi, se voi viitata siihen, että koodisi täytyy
uudelleenjärjestää pienempiin osiin.

### Luettelomäärityksissä

Kuten rakenteiden kohdalla, voimme määritellä luetteloita pitämään geneerisiä
tietotyyppejä muunnelmissaan. Katsotaan vielä kerran standardikirjaston
tarjoamaa `Option<T>`-luetteloa, jota käytimme luvussa 6:

```rust
enum Option<T> {
    Some(T),
    None,
}
```

Tämän määrityksen pitäisi nyt olla ymmärrettävämpi. Kuten näet, `Option<T>`-luettelo
on geneerinen tyypin `T` suhteen ja sillä on kaksi muunnelmaa: `Some`, joka
pitää yhden arvon tyyppiä `T`, ja `None`-muunnelma, joka ei pidä mitään arvoa.
Käyttämällä `Option<T>`-luetteloa voimme ilmaista valinnaisen arvon abstraktin
käsitteen, ja koska `Option<T>` on geneerinen, voimme käyttää tätä abstraktiota
riippumatta siitä, mikä valinnaisen arvon tyyppi on.

Luettelot voivat käyttää useita geneerisiä tyyppejä myös. Luvussa 9 käyttämämme
`Result`-luettelon määritys on yksi esimerkki:

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

`Result`-luettelo on geneerinen kahden tyypin, `T` ja `E`, suhteen, ja sillä on
kaksi muunnelmaa: `Ok`, joka pitää arvon tyyppiä `T`, ja `Err`, joka pitää arvon
tyyppiä `E`. Tämä määritys tekee käteväksi käyttää `Result`-luetteloa missä
tahansa, missä meillä on operaatio, joka voi onnistua (palauttaa arvon jonkin
tyypin `T`) tai epäonnistua (palauttaa virheen jonkin tyypin `E`). Itse asiassa
tätä käytimme tiedoston avaamiseen listauksessa 9-3, jossa `T` täytettiin
tyypillä `std::fs::File`, kun tiedosto avattiin onnistuneesti, ja `E` täytettiin
tyypillä `std::io::Error`, kun tiedoston avaamisessa oli ongelmia.

Kun tunnistat koodissasi tilanteita, joissa on useita rakenne- tai luettelomäärityksiä,
jotka eroavat vain niiden pitämien arvojen tyypeissä, voit välttää toiston
käyttämällä geneerisiä tyyppejä sen sijaan.

### Metodimäärityksissä

Voimme toteuttaa metodeja rakenteille ja luetteloille (kuten teimme luvussa 5) ja
käyttää geneerisiä tyyppejä niiden määrityksissä myös. Listaus 10-9 näyttää
listauksessa 10-6 määrittelemämme `Point<T>`-rakenteen, jolle on toteutettu
metodi nimeltä `x`.

<Listing number="10-9" file-name="src/main.rs" caption="Metodin `x` toteuttaminen `Point<T>`-rakenteelle, joka palauttaa viittauksen kenttään `x` tyyppiä `T`">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-09/src/main.rs}}
```

</Listing>

Tässä olemme määritelleet metodin nimeltä `x` tyypille `Point<T>`, joka palauttaa
viittauksen kentän `x` dataan.

Huomaa, että meidän täytyy ilmoittaa `T` heti `impl`-avainsanan jälkeen, jotta
voimme käyttää `T`:tä määrittääksemme, että toteutamme metodeja tyypille
`Point<T>`. Ilmoittamalla `T`:n geneeriseksi tyypiksi `impl`:n jälkeen Rust voi
tunnistaa, että `Point`:in kulmasulkeissa oleva tyyppi on geneerinen tyyppi
eikä konkreettinen tyyppi. Olisimme voineet valita eri nimen tälle geneeriselle
parametrille kuin rakenteen määrityksessä ilmoitettu geneerinen parametri, mutta
saman nimen käyttäminen on tapana. Jos kirjoitat metodin `impl`-lohkossa, joka
ilmoittaa geneerisen tyypin, tuo metodi määritellään minkä tahansa tyypin
instanssille riippumatta siitä, mikä konkreettinen tyyppi korvaa geneerisen
tyypin lopulta.

Voimme myös määrittää rajoituksia geneerisille tyypeille määritellessämme
metodeja tyypille. Voisimme esimerkiksi toteuttaa metodeja vain `Point<f32>`-instansseille
eikä `Point<T>`-instansseille millä tahansa geneerisellä tyypillä. Listauksessa
10-10 käytämme konkreettista tyyppiä `f32`, mikä tarkoittaa, että emme ilmoita
mitään tyyppejä `impl`:n jälkeen.

<Listing number="10-10" file-name="src/main.rs" caption="`impl`-lohko, joka koskee vain rakennetta, jolla on tietty konkreettinen tyyppi geneeriselle tyyppiparametrille `T`">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-10/src/main.rs:here}}
```

</Listing>

Tämä koodi tarkoittaa, että tyypillä `Point<f32>` on `distance_from_origin`-metodi;
muilla `Point<T>`-instansseilla, joissa `T` ei ole tyyppiä `f32`, tätä metodia
ei ole määritelty. Metodi mittaa, kuinka kaukana pisteemme on pisteestä
koordinaateissa (0.0, 0.0), ja käyttää matemaattisia operaatioita, jotka ovat
käytettävissä vain liukulukutyypeille.

Rakenteen määrityksessä olevat geneeriset tyyppiparametrit eivät aina ole samoja
kuin saman rakenteen metodien allekirjoituksissa käytetyt. Listaus 10-11 käyttää
geneerisiä tyyppejä `X1` ja `Y1` `Point`-rakenteelle ja `X2` `Y2` `mixup`-metodin
allekirjoitukselle tehdäkseen esimerkistä selkeämmän. Metodi luo uuden `Point`-instanssin,
jossa `x`-arvo tulee `self`-`Point`:ista (tyyppiä `X1`) ja `y`-arvo annetusta
`Point`-oliosta (tyyppiä `Y2`).

<Listing number="10-11" file-name="src/main.rs" caption="Metodi, joka käyttää geneerisiä tyyppejä, jotka eroavat rakenteen määrityksestä">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-11/src/main.rs}}
```

</Listing>

`main`-funktiossa olemme määritelleet `Point`:in, jolla on `i32` `x`:lle (arvolla
`5`) ja `f64` `y`:lle (arvolla `10.4`). Muuttuja `p2` on `Point`-rakenne, jolla
on merkkijonoviipale `x`:lle (arvolla `"Hello"`) ja `char` `y`:lle (arvolla
`c`). Kutsumalla `mixup`-metodia `p1`:llä argumentilla `p2` saamme `p3`:n, jolla
on `i32` `x`:lle, koska `x` tuli `p1`:stä. Muuttujalla `p3` on `char` `y`:lle,
koska `y` tuli `p2`:sta. `println!`-makrokutsu tulostaa `p3.x = 5, p3.y = c`.

Tämän esimerkin tarkoitus on havainnollistaa tilanne, jossa jotkut geneeriset
parametrit ilmoitetaan `impl`:llä ja jotkut metodin määrityksessä. Tässä
geneeriset parametrit `X1` ja `Y1` ilmoitetaan `impl`:n jälkeen, koska ne
liittyvät rakenteen määritykseen. Geneeriset parametrit `X2` ja `Y2` ilmoitetaan
`fn mixup`:n jälkeen, koska ne ovat merkityksellisiä vain metodille.

### Geneerisiä tyyppejä käyttävän koodin suorituskyky

Saatat miettiä, onko geneeristen tyyppiparametrien käytöllä ajonaikainen hinta.
Hyvä uutinen on, että geneeristen tyyppien käyttö ei tee ohjelmastasi hitaampaa
kuin se olisi konkreettisilla tyypeillä.

Rust saavuttaa tämän suorittamalla geneerisiä tyyppejä käyttävän koodin
monomorfisoinnin käännösaikana. _Monomorfisointi_ on prosessi, jossa geneerinen
koodi muunnetaan tiettyyn koodiksi täyttämällä konkreettiset tyypit, joita
käytetään käännöksen aikana. Tässä prosessissa kääntäjä tekee päinvastaisen
kuin ne vaiheet, joita käytimme geneerisen funktion luomiseen listauksessa 10-5:
kääntäjä katsoo kaikki kohdat, joissa geneeristä koodia kutsutaan, ja generoi
koodin niille konkreettisille tyypeille, joilla geneeristä koodia kutsutaan.

Katsotaan, miten tämä toimii käyttämällä standardikirjaston geneeristä
`Option<T>`-luetteloa:

```rust
let integer = Some(5);
let float = Some(5.0);
```

Kun Rust kääntää tämän koodin, se suorittaa monomorfisoinnin. Tämän prosessin
aikana kääntäjä lukee arvot, joita on käytetty `Option<T>`-instansseissa, ja
tunnistaa kaksi `Option<T>`-lajia: yksi on `i32` ja toinen on `f64`. Näin ollen
se laajentaa `Option<T>`-luettelon geneerisen määrityksen kahteen määritykseen,
jotka on erikoistettu tyypeille `i32` ja `f64`, korvaten geneerisen määrityksen
näillä tiettyillä määrityksillä.

Koodin monomorfisoitu versio näyttää suunnilleen seuraavalta (kääntäjä käyttää
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

Geneerinen `Option<T>` korvataan kääntäjän luomilla tiettyillä määrityksillä.
Koska Rust kääntää geneerisen koodin koodiksi, joka määrittää tyypin jokaisessa
instanssissa, emme maksa ajonaikaista hintaa geneeristen tyyppien käytöstä. Kun
koodi suoritetaan, se toimii aivan kuten toimisi, jos olisimme kopioineet
jokaisen määrityksen käsin. Monomorfisointiprosessi tekee Rustin geneerisistä
tyypeistä erittäin tehokkaita ajonaikana.
