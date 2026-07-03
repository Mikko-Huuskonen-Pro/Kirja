## Palautettavat virheet `Result`-tyypillä

Useimmat virheet eivät ole niin vakavia, että ohjelma täytyisi pysäyttää kokonaan.
Joskus funktion epäonnistuminen johtuu syystä, jonka voit helposti tulkita ja käsitellä.
Esimerkiksi jos yrität avata tiedoston ja operaatio epäonnistuu, koska tiedostoa ei ole olemassa,
voit haluta luoda tiedoston sen sijaan, että prosessi päättyisi.

Muistathan Luvun 2 kohdasta [”Mahdollisen epäonnistumisen käsittely `Result`-tyypillä”][handle_failure]<!--
ignore -->, että `Result`-enum on määritelty kahdella variantilla, `Ok` ja `Err`, seuraavasti:

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

`T` ja `E` ovat geneerisiä tyyppiparametreja: käsittelemme geneerisiä tyyppejä tarkemmin Luvussa 10.
Mitä sinun täytyy tietää nyt, on että `T` edustaa onnistuneessa tapauksessa `Ok`-variantin sisällä
palautettavan arvon tyyppiä ja `E` edustaa epäonnistumistapauksessa `Err`-variantin sisällä palautettavan
virheen tyyppiä. Koska `Result`-tyypillä on nämä geneeriset tyyppiparametrit, voimme käyttää `Result`-tyyppiä
ja siihen määriteltyjä funktioita monissa eri tilanteissa, joissa haluamamme onnistuneen arvon ja virhearvon
tyypit voivat vaihdella.

Kutsutaan funktiota, joka palauttaa `Result`-arvon, koska funktio voi epäonnistua.
Listauksessa 9-3 yritämme avata tiedoston.

<Listing number="9-3" file-name="src/main.rs" caption="Tiedoston avaaminen">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-03/src/main.rs}}
```

</Listing>

`File::open`-funktion paluutyyppi on `Result<T, E>`. Geneerinen parametri `T` on täytetty
`File::open`-toteutuksessa onnistuneen arvon tyypillä `std::fs::File`, joka on tiedostokahva.
Virhearvossa käytetty `E`-tyyppi on `std::io::Error`. Tämä paluutyyppi tarkoittaa, että `File::open`-kutsu
voi onnistua ja palauttaa tiedostokahvan, josta voimme lukea tai johon voimme kirjoittaa.
Funktiokutsu voi myös epäonnistua: esimerkiksi tiedostoa ei ehkä ole olemassa tai meillä ei ehkä ole
oikeutta käyttää tiedostoa. `File::open`-funktiolla täytyy olla tapa kertoa meille, onnistuiko se vai epäonnistuiko,
ja antaa samalla joko tiedostokahva tai virhetiedot. Tämän tiedon välittää juuri `Result`-enum.

Tapauksessa, jossa `File::open` onnistuu, muuttujan `greeting_file_result` arvo on `Ok`-instanssi,
joka sisältää tiedostokahvan. Tapauksessa, jossa se epäonnistuu, muuttujan `greeting_file_result` arvo
on `Err`-instanssi, joka sisältää lisätietoja tapahtuneesta virheestä.

Meidän täytyy lisätä Listauksen 9-3 koodiin toimintoja, jotka riippuvat siitä, minkä arvon `File::open` palauttaa.
Listaus 9-4 näyttää yhden tavan käsitellä `Result`-arvoa perustyökalulla, `match`-lausekkeella, josta puhuimme Luvussa 6.

<Listing number="9-4" file-name="src/main.rs" caption="`match`-lausekkeen käyttö mahdollisesti palautettavien `Result`-varianttien käsittelyyn">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-04/src/main.rs}}
```

</Listing>

Huomaa, että kuten `Option`-enum, myös `Result`-enum ja sen variantit on tuotu näkyvyysalueelle preludessa,
joten emme tarvitse määrittää `Result::`-etuliitettä ennen `Ok`- ja `Err`-variantteja `match`-haaroissa.

Kun tulos on `Ok`, tämä koodi palauttaa sisäisen `file`-arvon `Ok`-variantista, ja sitten sijoitamme
tämän tiedostokahvan arvon muuttujaan `greeting_file`. `match`-lausekkeen jälkeen voimme käyttää tiedostokahvaa lukemiseen tai kirjoittamiseen.

`match`-lausekkeen toinen haara käsittelee tapauksen, jossa saamme `Err`-arvon `File::open`-funktiosta.
Tässä esimerkissä olemme valinneet kutsua `panic!`-makroa. Jos nykyisessä hakemistossamme ei ole
tiedostoa nimeltä _hello.txt_ ja ajamme tämän koodin, näemme seuraavan tulosteen `panic!`-makrosta:

```console
{{#include ../listings/ch09-error-handling/listing-09-04/output.txt}}
```

Kuten tavallisesti, tämä tuloste kertoo meille tarkalleen, mikä meni pieleen.

### Erilaisten virheiden täsmäyttäminen

Listauksen 9-4 koodi kutsuu `panic!`-makroa riippumatta siitä, miksi `File::open` epäonnistui.
Haluamme kuitenkin tehdä eri toimintoja eri epäonnistumissyistä. Jos `File::open` epäonnistui,
koska tiedostoa ei ole olemassa, haluamme luoda tiedoston ja palauttaa kahvan uudelle tiedostolle.
Jos `File::open` epäonnistui jostain muusta syystä — esimerkiksi koska meillä ei ollut oikeutta avata tiedostoa —
haluamme silti, että koodi kutsuu `panic!`-makroa samalla tavalla kuin Listauksessa 9-4.
Tätä varten lisäämme sisäkkäisen `match`-lausekkeen, kuten Listauksessa 9-5 näytetään.

<Listing number="9-5" file-name="src/main.rs" caption="Eri virhetyyppien käsittely eri tavoin">

<!-- ignore this test because otherwise it creates hello.txt which causes other
tests to fail lol -->

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-05/src/main.rs}}
```

</Listing>

`File::open`-funktion `Err`-variantin sisällä palauttaman arvon tyyppi on `io::Error`,
joka on standardikirjaston tarjoama struct. Tällä structilla on metodi `kind`, jota voimme kutsua
saadaksemme `io::ErrorKind`-arvon. Enum `io::ErrorKind` on standardikirjaston tarjoama ja sillä on variantteja,
jotka edustavat eri virhetyyppejä, joita `io`-operaatio voi tuottaa. Variantti, jota haluamme käyttää,
on `ErrorKind::NotFound`, joka ilmaisee, että tiedostoa, jota yritämme avata, ei vielä ole olemassa.
Täsmäytämme siis `greeting_file_result`-arvoon, mutta meillä on myös sisäinen `match` `error.kind()`-arvoon.

Ehto, jonka haluamme tarkistaa sisäisessä `match`-lausekkeessa, on se, onko `error.kind()`-funktion
palauttama arvo `ErrorKind`-enumin `NotFound`-variantti. Jos on, yritämme luoda tiedoston `File::create`-funktiolla.
Koska `File::create` voi myös epäonnistua, tarvitsemme toisen haaran sisäiseen `match`-lausekkeeseen.
Kun tiedostoa ei voida luoda, tulostetaan eri virheilmoitus. Ulomman `match`-lausekkeen toinen haara pysyy samana,
joten ohjelma kaatuu kaikissa virheissä paitsi puuttuvan tiedoston virheessä.

> #### Vaihtoehtoja `match`-lausekkeen käytölle `Result<T, E>`-tyypin kanssa
>
> Se on paljon `match`-lausekkeita! `match`-lauseke on hyvin hyödyllinen, mutta myös hyvin primitiivinen.
> Luvussa 13 opit closureja, joita käytetään monien `Result<T, E>`-tyypille määriteltyjen metodien kanssa.
> Nämä metodit voivat olla tiiviimpiä kuin `match`-lausekkeen käyttö `Result<T, E>`-arvojen käsittelyssä koodissasi.
>
> Esimerkiksi tässä on toinen tapa kirjoittaa sama logiikka kuin Listauksessa 9-5, tällä kertaa käyttäen closureja
> ja `unwrap_or_else`-metodia:
>
> <!-- CAN'T EXTRACT SEE https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust,ignore
> use std::fs::File;
> use std::io::ErrorKind;
>
> fn main() {
>     let greeting_file = File::open("hello.txt").unwrap_or_else(|error| {
>         if error.kind() == ErrorKind::NotFound {
>             File::create("hello.txt").unwrap_or_else(|error| {
>                 panic!("Problem creating the file: {error:?}");
>             })
>         } else {
>             panic!("Problem opening the file: {error:?}");
>         }
>     });
> }
> ```
>
> Vaikka tämä koodi käyttäytyy samoin kuin Listaus 9-5, siinä ei ole yhtään `match`-lauseketta ja se on selkeämpää lukea.
> Palaa tähän esimerkkiin Luvun 13 lukemisen jälkeen ja etsi `unwrap_or_else`-metodia standardikirjaston dokumentaatiosta.
> Paljon muita näitä metodeja voi siivota valtavia sisäkkäisiä `match`-lausekkeita, kun käsittelet virheitä.

#### Oikotiet kaatumiseen virheessä: `unwrap` ja `expect`

`match`-lausekkeen käyttö toimii tarpeeksi hyvin, mutta se voi olla hieman sanallista eikä aina välitä aikomusta hyvin.
`Result<T, E>`-tyypillä on monia apumetodeja erilaisiin, tarkempiin tehtäviin. `unwrap`-metodi on oikotie,
joka on toteutettu aivan kuten Listauksessa 9-4 kirjoittamamme `match`-lauseke. Jos `Result`-arvo on `Ok`-variantti,
`unwrap` palauttaa `Ok`:n sisällä olevan arvon. Jos `Result` on `Err`-variantti, `unwrap` kutsuu `panic!`-makroa puolestamme.
Tässä on esimerkki `unwrap`-metodista käytössä:

<Listing file-name="src/main.rs">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-04-unwrap/src/main.rs}}
```

</Listing>

Jos ajamme tämän koodin ilman _hello.txt_-tiedostoa, näemme virheilmoituksen `unwrap`-metodin tekemästä `panic!`-kutsusta:

<!-- manual-regeneration
cd listings/ch09-error-handling/no-listing-04-unwrap
cargo run
copy and paste relevant text
-->

```text
thread 'main' panicked at src/main.rs:4:49:
called `Result::unwrap()` on an `Err` value: Os { code: 2, kind: NotFound, message: "No such file or directory" }
```

Vastaavasti `expect`-metodi antaa meidän valita myös `panic!`-virheilmoituksen.
`expect`-metodin käyttö `unwrap`-metodin sijaan ja hyvien virheilmoitusten antaminen voi välittää aikomuksesi
ja helpottaa kaatumisen lähteen jäljittämistä. `expect`-metodin syntaksi näyttää tältä:

<Listing file-name="src/main.rs">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-05-expect/src/main.rs}}
```

</Listing>

Käytämme `expect`-metodia samalla tavalla kuin `unwrap`-metodia: palauttaaksemme tiedostokahvan tai kutsuaksemme `panic!`-makroa.
`expect`-metodin `panic!`-kutsussa käyttämä virheilmoitus on parametri, jonka välitämme `expect`-metodille,
eikä `unwrap`-metodin käyttämä oletusarvoinen `panic!`-viesti. Tältä se näyttää:

<!-- manual-regeneration
cd listings/ch09-error-handling/no-listing-05-expect
cargo run
copy and paste relevant text
-->

```text
thread 'main' panicked at src/main.rs:5:10:
hello.txt should be included in this project: Os { code: 2, kind: NotFound, message: "No such file or directory" }
```

Tuotantolaatuisessa koodissa useimmat rustilaiset valitsevat `expect`-metodin `unwrap`-metodin sijaan
ja antavat enemmän kontekstia siitä, miksi operaation odotetaan aina onnistuvan.
Näin, jos oletuksesi osoittautuvat joskus vääriksi, sinulla on enemmän tietoa virheenkorjaukseen.

### Virheiden propagointi

Kun funktion toteutus kutsuu jotain, mikä voi epäonnistua, sen sijaan että käsittelisit virheen funktion sisällä,
voit palauttaa virheen kutsuvalle koodille, jotta se voi päättää, mitä tehdä. Tätä kutsutaan virheen _propagoinniksi_,
ja se antaa enemmän hallintaa kutsuvalle koodille, jossa voi olla enemmän tietoa tai logiikkaa virheen käsittelyyn
kuin mitä sinulla on käytettävissä koodisi kontekstissa.

Esimerkiksi Listaus 9-6 näyttää funktion, joka lukee käyttäjänimen tiedostosta. Jos tiedostoa ei ole olemassa
tai sitä ei voida lukea, tämä funktio palauttaa nämä virheet koodille, joka kutsui funktiota.

<Listing number="9-6" file-name="src/main.rs" caption="Funktio, joka palauttaa virheet kutsuvalle koodille `match`-lausekkeen avulla">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-06/src/main.rs:here}}
```

</Listing>

Tämä funktio voidaan kirjoittaa paljon lyhyemmin, mutta aloitamme tekemällä suuren osan manuaalisesti
virheenkäsittelyn tutkimiseksi; lopussa näytämme lyhyemmän tavan. Tarkastellaan ensin funktion paluutyyppiä:
`Result<String, io::Error>`. Tämä tarkoittaa, että funktio palauttaa `Result<T, E>`-tyypin arvon,
jossa geneerinen parametri `T` on täytetty konkreettisella tyypillä `String` ja geneerinen tyyppi `E`
on täytetty konkreettisella tyypillä `io::Error`.

Jos tämä funktio onnistuu ilman ongelmia, koodi, joka kutsuu tätä funktiota, saa `Ok`-arvon, joka sisältää
`String`-tyypin — tämän funktion tiedostosta lukeman `username`-arvon. Jos tämä funktio kohtaa ongelmia,
kutsuva koodi saa `Err`-arvon, joka sisältää `io::Error`-instanssin lisätiedoilla ongelmista.
Valitsimme `io::Error`-tyypin tämän funktion paluutyypiksi, koska se sattuu olemaan virhearvon tyyppi,
jonka molemmat funktion rungossa kutsumamme operaatiot voivat palauttaa epäonnistuessaan: `File::open`-funktio
ja `read_to_string`-metodi.

Funktion runko alkaa kutsumalla `File::open`-funktiota. Sitten käsittelemme `Result`-arvon `match`-lausekkeella,
joka on samanlainen kuin Listauksen 9-4 `match`. Jos `File::open` onnistuu, tiedostokahva kuviomuuttujassa `file`
tulee muuttujan `username_file` arvoksi ja funktio jatkuu. `Err`-tapauksessa `panic!`-kutsun sijaan käytämme
`return`-avainsanaa palataksemme aikaisin kokonaan funktiosta ja välittääksemme `File::open`-funktion virhearvon,
nyt kuviomuuttujassa `e`, takaisin kutsuvalle koodille tämän funktion virhearvona.

Jos meillä on siis tiedostokahva muuttujassa `username_file`, funktio luo sitten uuden `String`-tyypin muuttujaan `username`
ja kutsuu `read_to_string`-metodia tiedostokahvassa `username_file` lukeakseen tiedoston sisällön muuttujaan `username`.
`read_to_string`-metodi palauttaa myös `Result`-tyypin, koska se voi epäonnistua, vaikka `File::open` onnistui.
Tarvitsemme siis toisen `match`-lausekkeen käsittelemään tuota `Result`-arvoa: jos `read_to_string` onnistuu,
funktiomme on onnistunut ja palautamme tiedostosta nyt `username`-muuttujassa olevan käyttäjänimen `Ok`-arvoon käärittynä.
Jos `read_to_string` epäonnistuu, palautamme virhearvon samalla tavalla kuin palautimme virhearvon `match`-lausekkeessa,
joka käsitteli `File::open`-funktion paluuarvon. Emme kuitenkaan tarvitse eksplisiittisesti sanoa `return`,
koska tämä on funktion viimeinen lauseke.

Tämän koodin kutsuva koodi käsittelee sitten joko `Ok`-arvon, joka sisältää käyttäjänimen, tai `Err`-arvon,
joka sisältää `io::Error`-virheen. Kutsuvalle koodille jää päätettäväksi, mitä näille arvoille tehdään.
Jos kutsuva koodi saa `Err`-arvon, se voi kutsua `panic!`-makroa ja kaataa ohjelman, käyttää oletuskäyttäjänimeä
tai etsiä käyttäjänimen jostain muualta kuin tiedostosta, esimerkiksi. Meillä ei ole tarpeeksi tietoa siitä,
mitä kutsuva koodi todella yrittää tehdä, joten propagoidamme kaiken onnistumis- tai virhetiedon ylöspäin,
jotta se voi käsitellä sen asianmukaisesti.

Tämä virheiden propagoinnin malli on niin yleinen Rustissa, että Rust tarjoaa kysymysmerkkioperaattorin `?`
helpottamaan tätä.

#### Oikotie virheiden propagointiin: `?`-operaattori

Listaus 9-7 näyttää `read_username_from_file`-funktion toteutuksen, jolla on sama toiminnallisuus kuin Listauksessa 9-6,
mutta tässä toteutuksessa käytetään `?`-operaattoria.

<Listing number="9-7" file-name="src/main.rs" caption="Funktio, joka palauttaa virheet kutsuvalle koodille `?`-operaattorin avulla">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-07/src/main.rs:here}}
```

</Listing>

`Result`-arvon perässä oleva `?` on määritelty toimimaan lähes samalla tavalla kuin `match`-lausekkeet,
jotka määritimme `Result`-arvojen käsittelyyn Listauksessa 9-6. Jos `Result`-arvon arvo on `Ok`,
`Ok`:n sisällä oleva arvo palautetaan tästä lausekkeesta ja ohjelma jatkuu. Jos arvo on `Err`,
`Err` palautetaan koko funktiosta ikään kuin olisimme käyttäneet `return`-avainsanaa, jolloin virhearvo
propagoituu kutsuvalle kodelle.

On ero Listauksen 9-6 `match`-lausekkeen ja `?`-operaattorin välillä: virhearvot, joille kutsutaan `?`-operaattoria,
käyvät läpi `from`-funktion, joka on määritelty standardikirjaston `From`-traitissa ja jota käytetään arvojen
muuntamiseen tyypistä toiseen. Kun `?`-operaattori kutsuu `from`-funktiota, vastaanotettu virhetyyppi muunnetaan
nykyisen funktion paluutyypissä määriteltyyn virhetyyppiin. Tämä on hyödyllistä, kun funktio palauttaa yhden virhetyypin
edustaakseen kaikkia tapoja, joilla funktio voi epäonnistua, vaikka osat voivat epäonnistua monista eri syistä.

Esimerkiksi voisimme muuttaa Listauksen 9-7 `read_username_from_file`-funktion palauttamaan mukautetun virhetyypin
nimeltä `OurError`, jonka määrittelemme. Jos määrittelemme myös `impl From<io::Error> for OurError` rakentaaksemme
`OurError`-instanssin `io::Error`-virheestä, `read_username_from_file`-funktion rungon `?`-operaattorikutsut
kutsuvat `from`-funktiota ja muuntavat virhetyypit lisäämättä enempää koodia funktioon.

Listauksen 9-7 kontekstissa `File::open`-kutsun lopussa oleva `?` palauttaa `Ok`:n sisällä olevan arvon
muuttujaan `username_file`. Jos virhe tapahtuu, `?`-operaattori palaa aikaisin koko funktiosta ja antaa
minkä tahansa `Err`-arvon kutsuvalle kodelle. Sama pätee `read_to_string`-kutsun lopussa olevaan `?`-operaattoriin.

`?`-operaattori poistaa paljon pohjakoodia ja yksinkertaistaa tämän funktion toteutusta.
Voimme jopa lyhentää tätä koodia ketjuttamalla metodikutsuja heti `?`-operaattorin jälkeen, kuten Listauksessa 9-8 näytetään.

<Listing number="9-8" file-name="src/main.rs" caption="Metodikutsujen ketjuttaminen `?`-operaattorin jälkeen">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-08/src/main.rs:here}}
```

</Listing>

Olemme siirtäneet uuden `String`-tyypin luomisen muuttujaan `username` funktion alkuun; tuo osa ei ole muuttunut.
Sen sijaan, että loisimme muuttujan `username_file`, olemme ketjuttaneet `read_to_string`-kutsun suoraan
`File::open("hello.txt")?`-kutsun tulokseen. Meillä on silti `?` `read_to_string`-kutsun lopussa, ja palautamme edelleen
`Ok`-arvon, joka sisältää `username`-arvon, kun sekä `File::open` että `read_to_string` onnistuvat virheiden palauttamisen sijaan.
Toiminnallisuus on taas sama kuin Listauksissa 9-6 ja 9-7; tämä on vain erilainen, ergonomisempi tapa kirjoittaa se.

Listaus 9-9 näyttää tavan tehdä tämä vielä lyhyemmäksi käyttämällä `fs::read_to_string`-funktiota.

<Listing number="9-9" file-name="src/main.rs" caption="`fs::read_to_string`-funktion käyttö tiedoston avaamisen ja lukemisen sijaan">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-09/src/main.rs:here}}
```

</Listing>

Tiedoston lukeminen merkkijonoon on melko yleinen operaatio, joten standardikirjasto tarjoaa kätevän
`fs::read_to_string`-funktion, joka avaa tiedoston, luo uuden `String`-tyypin, lukee tiedoston sisällön,
laittaa sisällön kyseiseen `String`-tyyppiin ja palauttaa sen. Totta kai `fs::read_to_string`-funktion käyttö
ei anna meille mahdollisuutta selittää kaikkea virheenkäsittelyä, joten teimme sen ensin pidemmällä tavalla.

#### Missä `?`-operaattoria voi käyttää

`?`-operaattoria voi käyttää vain funktioissa, joiden paluutyyppi on yhteensopiva arvon kanssa, jolle `?` käytetään.
Tämä johtuu siitä, että `?`-operaattori on määritelty suorittamaan aikaisen paluun arvosta funktiosta samalla tavalla
kuin Listauksessa 9-6 määrittelemämme `match`-lauseke. Listauksessa 9-6 `match` käytti `Result`-arvoa,
ja aikaisen paluun haara palautti `Err(e)`-arvon. Funktion paluutyypin täytyy olla `Result`, jotta se on yhteensopiva tämän `return`-kutsun kanssa.

Listauksessa 9-10 tarkastellaan virhettä, jonka saamme, jos käytämme `?`-operaattoria `main`-funktiossa,
jonka paluutyyppi ei ole yhteensopiva tyypin kanssa, jolle käytämme `?`-operaattoria.

<Listing number="9-10" file-name="src/main.rs" caption="`?`-operaattorin käyttö `main`-funktiossa, joka palauttaa `()`, ei käänny.">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-10/src/main.rs}}
```

</Listing>

Tämä koodi avaa tiedoston, mikä voi epäonnistua. `?`-operaattori seuraa `File::open`-funktion palauttamaa `Result`-arvoa,
mutta tällä `main`-funktiolla on paluutyyppi `()`, ei `Result`. Kun käännamme tämän koodin, saamme seuraavan virheilmoituksen:

```console
{{#include ../listings/ch09-error-handling/listing-09-10/output.txt}}
```

Tämä virhe osoittaa, että saamme käyttää `?`-operaattoria vain funktiossa, joka palauttaa `Result`-, `Option`-tyypin
tai muun `FromResidual`-traitin toteuttavan tyypin.

Virheen korjaamiseksi on kaksi vaihtoehtoa. Toinen on muuttaa funktion paluutyyppi yhteensopivaksi arvon kanssa,
jolle käytät `?`-operaattoria, kunhan sinulla ei ole rajoituksia, jotka estävät sen. Toinen on käyttää `match`-lauseketta
tai jotakin `Result<T, E>`-tyypin metodeista käsitelläksesi `Result<T, E>`-arvon sopivalla tavalla.

Virheilmoitus mainitsi myös, että `?`-operaattoria voi käyttää `Option<T>`-arvojen kanssa. Kuten `Result`-tyypin kanssa,
voit käyttää `?`-operaattoria `Option`-tyypillä vain funktiossa, joka palauttaa `Option`-tyypin. `?`-operaattorin käyttäytyminen,
kun sitä kutsutaan `Option<T>`-arvolla, on samanlainen kuin kun sitä kutsutaan `Result<T, E>`-arvolla:
jos arvo on `None`, `None` palautetaan aikaisin funktiosta siinä vaiheessa. Jos arvo on `Some`, `Some`:n sisällä oleva arvo
on lausekkeen tulosarvo ja funktio jatkuu. Listaus 9-11 sisältää esimerkin funktiosta, joka etsii annetun tekstin ensimmäisen rivin viimeisen merkin.

<Listing number="9-11" caption="`?`-operaattorin käyttö `Option<T>`-arvolla">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-11/src/main.rs:here}}
```

</Listing>

Tämä funktio palauttaa `Option<char>`, koska siellä voi olla merkki, mutta se voi myös olla, ettei ole.
Tämä koodi ottaa `text`-merkkijonoviipaleargumentin ja kutsuu sen `lines`-metodia, joka palauttaa iteraattorin
merkkijonon riveille. Koska tämä funktio haluaa tarkastella ensimmäistä riviä, se kutsuu `next`-metodia iteraattorilla
saadakseen ensimmäisen arvon iteraattorista. Jos `text` on tyhjä merkkijono, tämä `next`-kutsu palauttaa `None`,
jolloin käytämme `?`-operaattoria pysähtyäksemme ja palauttaaksemme `None`:n `last_char_of_first_line`-funktiosta.
Jos `text` ei ole tyhjä merkkijono, `next` palauttaa `Some`-arvon, joka sisältää merkkijonoviipaleen tekstin ensimmäisestä rivistä.

`?` purkaa merkkijonoviipaleen, ja voimme kutsua `chars`-metodia kyseisellä merkkijonoviipaleella saadaksemme
sen merkkien iteraattorin. Olemme kiinnostuneita tämän ensimmäisen rivin viimeisestä merkistä, joten kutsumme `last`-metodia
palauttaaksemme iteraattorin viimeisen kohteen. Tämä on `Option`, koska ensimmäinen rivi voi olla tyhjä merkkijono;
esimerkiksi jos `text` alkaa tyhjällä rivillä mutta sisältää merkkejä muilla riveillä, kuten `"\nhi"`.
Jos ensimmäisellä rivillä on kuitenkin viimeinen merkki, se palautetaan `Some`-variantissa. Keskellä oleva `?`-operaattori
antaa meille tiiviin tavan ilmaista tämä logiikka, jolloin voimme toteuttaa funktion yhdellä rivillä. Jos emme voisi käyttää
`?`-operaattoria `Option`-tyypillä, meidän täytyisi toteuttaa tämä logiikka useammilla metodikutsuilla tai `match`-lausekkeella.

Huomaa, että voit käyttää `?`-operaattoria `Result`-arvolla funktiossa, joka palauttaa `Result`-tyypin, ja voit käyttää
`?`-operaattoria `Option`-arvolla funktiossa, joka palauttaa `Option`-tyypin, mutta et voi sekoittaa niitä.
`?`-operaattori ei automaattisesti muunna `Result`-tyyppiä `Option`-tyypiksi tai päinvastoin; näissä tapauksissa
voit käyttää metodeja kuten `ok`-metodia `Result`-tyypillä tai `ok_or`-metodia `Option`-tyypillä tehdäksesi muunnoksen eksplisiittisesti.

Tähän mennessä kaikki käyttämämme `main`-funktiot ovat palauttaneet `()`. `main`-funktio on erityinen, koska se on
suoritettavan ohjelman sisään- ja uloskäyntipiste, ja sen paluutyypillä on rajoituksia, jotta ohjelma käyttäytyy odotetusti.

Onneksi `main` voi myös palauttaa `Result<(), E>`. Listaus 9-12 sisältää Listauksen 9-10 koodin, mutta olemme muuttaneet
`main`-funktion paluutyypiksi `Result<(), Box<dyn Error>>` ja lisänneet paluuarvon `Ok(())` loppuun. Tämä koodi kääntyy nyt.

<Listing number="9-12" file-name="src/main.rs" caption="`main`-funktion muuttaminen palauttamaan `Result<(), E>` sallii `?`-operaattorin käytön `Result`-arvoilla.">

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-12/src/main.rs}}
```

</Listing>

`Box<dyn Error>`-tyyppi on _trait-objekti_, josta puhumme Luvun 18 [”Trait-objektien käyttö eri tyyppisten arvojen sallimiseksi”][trait-objects]<!--
ignore --> -osiossa. Toistaiseksi voit lukea `Box<dyn Error>` merkityksenä ”mikä tahansa virhetyyppi”.
`?`-operaattorin käyttö `Result`-arvolla `main`-funktiossa, jonka virhetyyppi on `Box<dyn Error>`, on sallittua,
koska se sallii minkä tahansa `Err`-arvon palauttamisen aikaisin. Vaikka tämän `main`-funktion runko palauttaa
vain `std::io::Error`-tyyppisiä virheitä, määrittämällä `Box<dyn Error>` tämä signatuuri pysyy oikeana,
vaikka `main`-funktion runkoon lisättäisiin enemmän koodia, joka palauttaa muita virheitä.

Kun `main`-funktio palauttaa `Result<(), E>`, suoritettava ohjelma päättyy arvolla `0`, jos `main` palauttaa `Ok(())`,
ja päättyy nollasta poikkeavalla arvolla, jos `main` palauttaa `Err`-arvon. C-kielellä kirjoitetut suoritettavat tiedostot
palauttavat kokonaislukuja päättyessään: onnistuneesti päättyvät ohjelmat palauttavat kokonaisluvun `0`,
ja virheelliset ohjelmat palauttavat jonkin muun kuin nollan. Rust palauttaa myös kokonaislukuja suoritettavista tiedostoista
tämän käytännön mukaisuuden vuoksi.

`main`-funktio voi palauttaa mitä tahansa tyyppejä, jotka toteuttavat [standardikirjaston `Termination`-traitin][termination]<!-- ignore -->,
joka sisältää `report`-funktion, joka palauttaa `ExitCode`-tyypin. Katso standardikirjaston dokumentaatiosta lisätietoja
`Termination`-traitin toteuttamisesta omille tyypeillesi.

Nyt kun olemme käsitelleet `panic!`-kutsun tai `Result`-paluun yksityiskohdat, palataan aiheeseen siitä,
miten päättää, kumpaa on sopivaa käyttää missäkin tilanteessa.

[handle_failure]: ch02-00-guessing-game-tutorial.html#handling-potential-failure-with-result
[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-that-allow-for-values-of-different-types
[termination]: ../std/process/trait.Termination.html
