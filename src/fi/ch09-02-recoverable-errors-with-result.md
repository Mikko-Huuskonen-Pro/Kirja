## Palautuvat virheet `Result`:illa

Useimmat virheet eivät ole tarpeeksi vakavia vaatimaan ohjelman täydellistä pysäyttämistä. Joskus kun funktio epäonnistuu, syy on sellainen, jonka voit helposti tulkita ja vastata siihen. Esimerkiksi jos yrität avata tiedoston ja operaatio epäonnistuu, koska tiedostoa ei ole olemassa, saatat haluta luoda tiedoston sen sijaan, että lopettaisit prosessin.

Muista kohdasta [”Mahdollisen epäonnistumisen käsittely `Result`:illa”][handle_failure]<!-- ignore --> luvussa 2, että `Result`-enum on määritelty kahdella variantilla, `Ok` ja `Err`, seuraavasti:

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

`T` ja `E` ovat geneerisiä tyyppiparametreja: käsittelemme geneerisiä tyyppejä tarkemmin luvussa 10. Mitä sinun tarvitsee tietää nyt on, että `T` edustaa onnistumistapauksessa `Ok`-variantin sisällä palautettavan arvon tyyppiä, ja `E` edustaa epäonnistumistapauksessa `Err`-variantin sisällä palautettavan virheen tyyppiä. Koska `Result`:illa on nämä geneeriset tyyppiparametrit, voimme käyttää `Result`-tyyppiä ja siihen määriteltyjä funktioita monissa eri tilanteissa, joissa haluamme palauttaa erilaisia onnistumis- ja virhearvoja.

Kutsutaan funktiota, joka palauttaa `Result`-arvon, koska funktio voi epäonnistua. Listauksessa 9-3 yritämme avata tiedoston.

<Listing number="9-3" file-name="src/main.rs" caption="Tiedoston avaaminen">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-03/src/main.rs}}
```

</Listing>

`File::open`:n palautustyyppi on `Result<T, E>`. Geneerinen parametri `T` on täytetty `File::open`:n toteutuksessa onnistumisarvon tyypillä, `std::fs::File`, joka on tiedostokahva. Virhearvossa käytetty `E`-tyyppi on `std::io::Error`. Tämä palautustyyppi tarkoittaa, että `File::open`-kutsu voi onnistua ja palauttaa tiedostokahvan, josta voimme lukea tai kirjoittaa. Funktiokutsu voi myös epäonnistua: esimerkiksi tiedostoa ei ehkä ole olemassa, tai meillä ei ehkä ole oikeutta käyttää tiedostoa. `File::open`-funktiolla on oltava tapa kertoa meille, onnistuiko se vai epäonnistuiko, ja antaa meille joko tiedostokahva tai virhetiedot. Tämä tieto on juuri se, mitä `Result`-enum välittää.

Tapauksessa, jossa `File::open` onnistuu, muuttujan `greeting_file_result` arvo on `Ok`-instanssi, joka sisältää tiedostokahvan. Tapauksessa, jossa se epäonnistuu, muuttujan `greeting_file_result` arvo on `Err`-instanssi, joka sisältää lisätietoja tapahtuneesta virhetyypistä.

Meidän on lisättävä listauksen 9-3 koodiin toimia, jotka riippuvat `File::open`:n palauttamasta arvosta. Listaus 9-4 näyttää yhden tavan käsitellä `Result`:ia perustyökalulla, `match`-lausekkeella, jota käsittelimme luvussa 6.

<Listing number="9-4" file-name="src/main.rs" caption="`match`-lausekkeen käyttö palautettavien `Result`-varianttien käsittelyyn">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-04/src/main.rs}}
```

</Listing>

Huomaa, että kuten `Option`-enum, `Result`-enum ja sen variantit on tuotu laajuuteen preludin kautta, joten meidän ei tarvitse määrittää `Result::` ennen `Ok`- ja `Err`-variantteja `match`-haaroissa.

Kun tulos on `Ok`, tämä koodi palauttaa sisäisen `file`-arvon `Ok`-variantista, ja sitten määritämme kyseisen tiedostokahvan arvon muuttujalle `greeting_file`. `match`:in jälkeen voimme käyttää tiedostokahvaa lukemiseen tai kirjoittamiseen.

`match`:in toinen haara käsittelee tapauksen, jossa saamme `Err`-arvon `File::open`:sta. Tässä esimerkissä olemme valinneet kutsua `panic!`-makroa. Jos nykyisessä hakemistossamme ei ole tiedostoa nimeltä _hello.txt_ ja suoritamme tämän koodin, näemme seuraavan tulosteen `panic!`-makrosta:

```console
{{#include ../listings/ch09-error-handling/listing-09-04/output.txt}}
```

Kuten tavallisesti, tämä tuloste kertoo meille tarkalleen, mikä meni pieleen.

### Eri virheiden täsmäyttäminen

Listauksen 9-4 koodi kutsuu `panic!`:ia riippumatta siitä, miksi `File::open` epäonnistui. Haluamme kuitenkin toimia eri tavoin eri epäonnistumissyistä. Jos `File::open` epäonnistui, koska tiedostoa ei ole olemassa, haluamme luoda tiedoston ja palauttaa kahvan uudelle tiedostolle. Jos `File::open` epäonnistui jostain muusta syystä—esimerkiksi koska meillä ei ollut oikeutta avata tiedostoa—haluamme silti, että koodi kutsuu `panic!`:ia samalla tavalla kuin listauksessa 9-4. Tätä varten lisäämme sisäisen `match`-lausekkeen, kuten listauksessa 9-5.

<Listing number="9-5" file-name="src/main.rs" caption="Eri virhetyyppien käsittely eri tavoin">

<!-- ignore this test because otherwise it creates hello.txt which causes other
tests to fail lol -->

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-05/src/main.rs}}
```

</Listing>

`File::open`:n `Err`-variantin sisällä palauttaman arvon tyyppi on `io::Error`, joka on standardikirjaston tarjoama struct. Tällä structilla on metodi `kind`, jota voimme kutsua saadaksemme `io::ErrorKind`-arvon. Enum `io::ErrorKind` on standardikirjaston tarjoama ja sillä on variantteja, jotka edustavat erilaisia virhetyyppejä, jotka voivat johtua `io`-operaatiosta. Variantti, jota haluamme käyttää, on `ErrorKind::NotFound`, joka ilmaisee, että tiedostoa, jota yritämme avata, ei ole vielä olemassa. Joten täsmäytämme `greeting_file_result`:in, mutta meillä on myös sisäinen `match` `error.kind()`:n päällä.

Ehto, jonka haluamme tarkistaa sisäisessä `match`:issa, on se, onko `error.kind()`:n palauttama arvo `ErrorKind`-enumin `NotFound`-variantti. Jos on, yritämme luoda tiedoston `File::create`:lla. Koska `File::create` voi myös epäonnistua, tarvitsemme toisen haaran sisäiseen `match`-lausekkeeseen. Kun tiedostoa ei voida luoda, tulostetaan eri virheilmoitus. Ulomman `match`:in toinen haara pysyy samana, joten ohjelma panikoi kaikissa virheissä paitsi puuttuvan tiedoston virheessä.

> #### Vaihtoehdot `match`:in käytölle `Result<T, E>`:n kanssa
>
> Se on paljon `match`:ia! `match`-lauseke on hyvin hyödyllinen, mutta myös hyvin primitiivinen. Luvussa 13 opit sulkeista, joita käytetään monien `Result<T, E>`:lle määriteltyjen metodien kanssa. Nämä metodit voivat olla tiiviimpiä kuin `match`:in käyttö `Result<T, E>`-arvojen käsittelyssä koodissasi.
>
> Esimerkiksi tässä on toinen tapa kirjoittaa sama logiikka kuin listauksessa 9-5, tällä kertaa käyttäen sulkeita ja `unwrap_or_else`-metodia:
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
> Vaikka tämä koodi käyttäytyy samalla tavalla kuin listaus 9-5, siinä ei ole `match`-lausekkeita ja se on siistimpi lukea. Palaa tähän esimerkkiin luvun 13 jälkeen ja etsi `unwrap_or_else`-metodi standardikirjaston dokumentaatiosta. Monia muita näistä metodeista voi siivota valtavia, sisäkkäisiä `match`-lausekkeita, kun käsittelet virheitä.

<!-- Old headings. Do not remove or links may break. -->

<a id="shortcuts-for-panic-on-error-unwrap-and-expect"></a>

#### Oikotiet paniikkiin virheessä

`match`:in käyttö toimii tarpeeksi hyvin, mutta se voi olla hieman sanallista eikä aina välitä aikomusta hyvin. `Result<T, E>`-tyypillä on monia apumetodeja, jotka on määritelty erilaisiin, tarkempiin tehtäviin. `unwrap`-metodi on oikotiemetodi, joka on toteutettu juuri kuten listauksessa 9-4 kirjoittamamme `match`-lauseke. Jos `Result`-arvo on `Ok`-variantti, `unwrap` palauttaa `Ok`:n sisällä olevan arvon. Jos `Result` on `Err`-variantti, `unwrap` kutsuu `panic!`-makroa puolestamme. Tässä on esimerkki `unwrap`:in toiminnasta:

<Listing file-name="src/main.rs">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-04-unwrap/src/main.rs}}
```

</Listing>

Jos suoritamme tämän koodin ilman _hello.txt_-tiedostoa, näemme virheilmoituksen `unwrap`-metodin tekemästä `panic!`-kutsusta:

<!-- manual-regeneration
cd listings/ch09-error-handling/no-listing-04-unwrap
cargo run
copy and paste relevant text
-->

```text
thread 'main' panicked at src/main.rs:4:49:
called `Result::unwrap()` on an `Err` value: Os { code: 2, kind: NotFound, message: "No such file or directory" }
```

Vastaavasti `expect`-metodi antaa meille myös valita `panic!`-virheilmoituksen. `expect`:in käyttäminen `unwrap`:in sijaan ja hyvien virheilmoitusten antaminen voi välittää aikomuksesi ja helpottaa paniikin lähteen jäljittämistä. `expect`:in syntaksi näyttää tältä:

<Listing file-name="src/main.rs">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-05-expect/src/main.rs}}
```

</Listing>

Käytämme `expect`:ia samalla tavalla kuin `unwrap`:ia: palauttaaksemme tiedostokahvan tai kutsuaksemme `panic!`-makroa. `expect`:in `panic!`-kutsussa käytetty virheilmoitus on parametri, jonka välitämme `expect`:ille, `unwrap`:in käyttämän oletusarvoisen `panic!`-viestin sijaan. Se näyttää tältä:

<!-- manual-regeneration
cd listings/ch09-error-handling/no-listing-05-expect
cargo run
copy and paste relevant text
-->

```text
thread 'main' panicked at src/main.rs:5:10:
hello.txt should be included in this project: Os { code: 2, kind: NotFound, message: "No such file or directory" }
```

Tuotantolaatuisessa koodissa useimmat rustilaiset valitsevat `expect`:in `unwrap`:in sijaan ja antavat enemmän kontekstia siitä, miksi operaation odotetaan aina onnistuvan. Näin, jos oletuksesi koskaan osoittautuvat vääriksi, sinulla on enemmän tietoa virheenkorjaukseen.

### Virheiden propagointi

Kun funktion toteutus kutsuu jotain, mikä voi epäonnistua, sen sijaan että käsittelisit virheen funktion sisällä, voit palauttaa virheen kutsuvalle koodille, jotta se voi päättää, mitä tehdä. Tätä kutsutaan virheen _propagoinniksi_, ja se antaa enemmän hallintaa kutsuvalle koodille, jossa saattaa olla enemmän tietoa tai logiikkaa, joka sanelee, miten virhe pitäisi käsitellä, kuin mitä sinulla on käytettävissäsi koodisi kontekstissa.

Esimerkiksi listaus 9-6 näyttää funktion, joka lukee käyttäjänimen tiedostosta. Jos tiedostoa ei ole olemassa tai sitä ei voida lukea, tämä funktio palauttaa nämä virheet koodille, joka kutsui funktiota.

<Listing number="9-6" file-name="src/main.rs" caption="Funktio, joka palauttaa virheet kutsuvalle koodille `match`:ia käyttäen">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-06/src/main.rs:here}}
```

</Listing>

Tämä funktio voidaan kirjoittaa paljon lyhyemmällä tavalla, mutta aloitamme tekemällä suuren osan manuaalisesti tutkiaksemme virheenkäsittelyä; lopussa näytämme lyhyemmän tavan. Katsotaan ensin funktion palautustyyppiä: `Result<String, io::Error>`. Tämä tarkoittaa, että funktio palauttaa arvon tyyppiä `Result<T, E>`, jossa geneerinen parametri `T` on täytetty konkreettisella tyypillä `String` ja geneerinen tyyppi `E` on täytetty konkreettisella tyypillä `io::Error`.

Jos tämä funktio onnistuu ilman ongelmia, tätä funktiota kutsuva koodi saa `Ok`-arvon, joka sisältää `String`:in—tiedostosta luetun `username`:n. Jos tämä funktio kohtaa ongelmia, kutsuva koodi saa `Err`-arvon, joka sisältää `io::Error`-instanssin, jossa on lisätietoja ongelmista. Valitsimme `io::Error`:in tämän funktion palautustyypiksi, koska se sattuu olemaan virhearvon tyyppi, jonka molemmat tämän funktion rungossa kutsumamme operaatiot voivat palauttaa: `File::open`-funktio ja `read_to_string`-metodi.

Funktion runko alkaa kutsumalla `File::open`-funktiota. Sitten käsittelemme `Result`-arvon `match`:illa, joka on samanlainen kuin listauksen 9-4 `match`. Jos `File::open` onnistuu, tiedostokahva kuviomuuttujassa `file` tulee muuttuvan muuttujan `username_file` arvoksi ja funktio jatkuu. `Err`-tapauksessa `panic!`:in kutsumisen sijaan käytämme `return`-avainsanaa palataksemme aikaisin kokonaan funktiosta ja välittääksemme `File::open`:n virhearvon, nyt kuviomuuttujassa `e`, takaisin kutsuvalle koodille tämän funktion virhearvona.

Joten, jos meillä on tiedostokahva `username_file`:ssa, funktio luo sitten uuden `String`:in muuttujaan `username` ja kutsuu `read_to_string`-metodia tiedostokahvassa `username_file` lukeakseen tiedoston sisällön `username`:iin. `read_to_string`-metodi palauttaa myös `Result`:in, koska se voi epäonnistua, vaikka `File::open` onnistui. Joten tarvitsemme toisen `match`:in käsitelläksemme kyseisen `Result`:in: Jos `read_to_string` onnistuu, funktiomme on onnistunut, ja palautamme tiedostosta nyt `username`:ssa olevan käyttäjänimen `Ok`:ssa käärittynä. Jos `read_to_string` epäonnistuu, palautamme virhearvon samalla tavalla kuin palautimme virhearvon `match`:issa, joka käsitteli `File::open`:n palautusarvon. Meidän ei kuitenkaan tarvitse eksplisiittisesti sanoa `return`, koska tämä on funktion viimeinen lauseke.

Tätä koodia kutsuva koodi käsittelee sitten joko `Ok`-arvon, joka sisältää käyttäjänimen, tai `Err`-arvon, joka sisältää `io::Error`:in. Kutsuvalle koodille jää päätettäväksi, mitä näille arvoille tehdään. Jos kutsuva koodi saa `Err`-arvon, se voisi kutsua `panic!`:ia ja kaataa ohjelman, käyttää oletuskäyttäjänimeä tai hakea käyttäjänimen jostain muualta kuin tiedostosta, esimerkiksi. Meillä ei ole tarpeeksi tietoa siitä, mitä kutsuva koodi todella yrittää tehdä, joten propagoidamme kaiken onnistumis- tai virhetiedon ylöspäin sen käsiteltäväksi asianmukaisesti.

Tämä virheiden propagoinnin malli on niin yleinen Rustissa, että Rust tarjoaa kysymysmerkkioperaattorin `?` helpottamaan tätä.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-shortcut-for-propagating-errors-the--operator"></a>

#### `?`-operaattorin oikotie

Listaus 9-7 näyttää `read_username_from_file`:n toteutuksen, jolla on sama toiminnallisuus kuin listauksessa 9-6, mutta tässä toteutuksessa käytetään `?`-operaattoria.

<Listing number="9-7" file-name="src/main.rs" caption="Funktio, joka palauttaa virheet kutsuvalle koodille `?`-operaattorilla">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-07/src/main.rs:here}}
```

</Listing>

`Result`-arvon jälkeen sijoitettu `?` on määritelty toimimaan lähes samalla tavalla kuin `match`-lausekkeet, jotka määrittelimme käsittelemään `Result`-arvoja listauksessa 9-6. Jos `Result`-arvon arvo on `Ok`, `Ok`:n sisällä oleva arvo palautetaan tästä lausekkeesta ja ohjelma jatkuu. Jos arvo on `Err`, `Err` palautetaan koko funktiosta ikään kuin olisimme käyttäneet `return`-avainsanaa, jotta virhearvo propagoidaan kutsuvalle koodille.

On ero listauksen 9-6 `match`-lausekkeen ja `?`-operaattorin välillä: Virhearvot, joille `?`-operaattoria kutsutaan, käyvät läpi `from`-funktion, joka on määritelty standardikirjaston `From`-traitissa ja jota käytetään arvojen muuntamiseen tyypistä toiseen. Kun `?`-operaattori kutsuu `from`-funktiota, vastaanotettu virhetyyppi muunnetaan nykyisen funktion palautustyypissä määriteltyyn virhetyyppiin. Tämä on hyödyllistä, kun funktio palauttaa yhden virhetyypin edustaen kaikkia tapoja, joilla funktio voi epäonnistua, vaikka osat voivat epäonnistua monista eri syistä.

Esimerkiksi voisimme muuttaa listauksen 9-7 `read_username_from_file`-funktion palauttamaan mukautetun virhetyypin nimeltä `OurError`, jonka määrittelemme. Jos määrittelemme myös `impl From<io::Error> for OurError` rakentaaksemme `OurError`-instanssin `io::Error`:sta, `read_username_from_file`-funktion rungon `?`-operaattorikutsut kutsuvat `from`:ia ja muuntavat virhetyypit lisäämättä enempää koodia funktioon.

Listauksen 9-7 kontekstissa `File::open`-kutsun lopussa oleva `?` palauttaa `Ok`:n sisällä olevan arvon muuttujaan `username_file`. Jos virhe tapahtuu, `?`-operaattori palaa aikaisin koko funktiosta ja antaa minkä tahansa `Err`-arvon kutsuvalle kodelle. Sama pätee `read_to_string`-kutsun lopussa olevaan `?`:ään.

`?`-operaattori poistaa paljon toistuvaa koodia ja yksinkertaistaa tämän funktion toteutusta. Voimme jopa lyhentää tätä koodia edelleen ketjuttamalla metodikutsuja heti `?`:n jälkeen, kuten listauksessa 9-8.

<Listing number="9-8" file-name="src/main.rs" caption="Metodikutsujen ketjuttaminen `?`-operaattorin jälkeen">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-08/src/main.rs:here}}
```

</Listing>

Olemme siirtäneet uuden `String`:in luomisen `username`:ssa funktion alkuun; tämä osa ei ole muuttunut. Sen sijaan, että loisimme muuttujan `username_file`, olemme ketjuttaneet `read_to_string`-kutsun suoraan `File::open("hello.txt")?`:n tulokseen. Meillä on edelleen `?` `read_to_string`-kutsun lopussa, ja palautamme edelleen `Ok`-arvon, joka sisältää `username`:n, kun sekä `File::open` että `read_to_string` onnistuvat virheiden palauttamisen sijaan. Toiminnallisuus on taas sama kuin listauksissa 9-6 ja 9-7; tämä on vain eri, ergonomisempi tapa kirjoittaa se.

Listaus 9-9 näyttää tavan tehdä tämä vielä lyhyemmäksi käyttämällä `fs::read_to_string`:ia.

<Listing number="9-9" file-name="src/main.rs" caption="`fs::read_to_string`:in käyttö tiedoston avaamisen ja lukemisen sijaan">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-09/src/main.rs:here}}
```

</Listing>

Tiedoston lukeminen merkkijonoon on melko yleinen operaatio, joten standardikirjasto tarjoaa kätevän `fs::read_to_string`-funktion, joka avaa tiedoston, luo uuden `String`:in, lukee tiedoston sisällön, laittaa sisällön kyseiseen `String`:iin ja palauttaa sen. Tietysti `fs::read_to_string`:in käyttö ei anna meille mahdollisuutta selittää kaikkea virheenkäsittelyä, joten teimme sen ensin pidemmällä tavalla.

<!-- Old headings. Do not remove or links may break. -->

<a id="where-the--operator-can-be-used"></a>

#### Missä `?`-operaattoria voi käyttää

`?`-operaattoria voi käyttää vain funktioissa, joiden palautustyyppi on yhteensopiva arvon kanssa, jolle `?` käytetään. Tämä johtuu siitä, että `?`-operaattori on määritelty suorittamaan aikainen paluu arvosta funktiosta samalla tavalla kuin listauksessa 9-6 määrittelemämme `match`-lauseke. Listauksessa 9-6 `match` käytti `Result`-arvoa, ja aikaisen paluun haara palautti `Err(e)`-arvon. Funktion palautustyypin on oltava `Result`, jotta se on yhteensopiva tämän `return`:in kanssa.

Listauksessa 9-10 katsotaan virhettä, jonka saamme, jos käytämme `?`-operaattoria `main`-funktiossa, jonka palautustyyppi ei ole yhteensopiva arvon tyypin kanssa, jolle käytämme `?`:ää.

<Listing number="9-10" file-name="src/main.rs" caption="`?`:n käyttö `main`-funktiossa, joka palauttaa `()`, ei käänny.">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-10/src/main.rs}}
```

</Listing>

Tämä koodi avaa tiedoston, mikä voi epäonnistua. `?`-operaattori seuraa `File::open`:n palauttamaa `Result`-arvoa, mutta tällä `main`-funktiolla on palautustyyppi `()`, ei `Result`. Kun käännetään tämä koodi, saamme seuraavan virheilmoituksen:

```console
{{#include ../listings/ch09-error-handling/listing-09-10/output.txt}}
```

Tämä virhe osoittaa, että `?`-operaattoria saa käyttää vain funktiossa, joka palauttaa `Result`:in, `Option`:in tai muun tyypin, joka toteuttaa `FromResidual`:in.

Virheen korjaamiseksi sinulla on kaksi vaihtoehtoa. Yksi vaihtoehto on muuttaa funktiosi palautustyyppi yhteensopivaksi arvon kanssa, jolle käytät `?`-operaattoria, kunhan sinulla ei ole rajoituksia, jotka estävät sen. Toinen vaihtoehto on käyttää `match`:ia tai jotakin `Result<T, E>`:n metodeista käsitelläksesi `Result<T, E>`:n sopivalla tavalla.

Virheilmoitus mainitsi myös, että `?`:ää voi käyttää myös `Option<T>`-arvojen kanssa. Kuten `Result`:in kanssa, voit käyttää `?`:ää `Option`:issa vain funktiossa, joka palauttaa `Option`:in. `?`-operaattorin käyttäytyminen, kun sitä kutsutaan `Option<T>`:llä, on samanlainen kuin kun sitä kutsutaan `Result<T, E>`:llä: Jos arvo on `None`, `None` palautetaan aikaisin funktiosta kyseisessä kohdassa. Jos arvo on `Some`, `Some`:n sisällä oleva arvo on lausekkeen tulosarvo, ja funktio jatkuu. Listaus 9-11 on esimerkki funktiosta, joka löytää annetun tekstin ensimmäisen rivin viimeisen merkin.

<Listing number="9-11" caption="`?`-operaattorin käyttö `Option<T>`-arvolla">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-11/src/main.rs:here}}
```

</Listing>

Tämä funktio palauttaa `Option<char>`:in, koska siellä saattaa olla merkki, mutta se on myös mahdollista, ettei siellä ole. Tämä koodi ottaa `text`-merkkijonoviipaleargumentin ja kutsuu sen `lines`-metodia, joka palauttaa iteraattorin merkkijonon riveistä. Koska tämä funktio haluaa tarkastella ensimmäistä riviä, se kutsuu `next`:ia iteraattorilla saadakseen ensimmäisen arvon iteraattorista. Jos `text` on tyhjä merkkijono, tämä `next`-kutsu palauttaa `None`:n, jolloin käytämme `?`:a pysähtyäksemme ja palauttaaksemme `None`:n funktiosta `last_char_of_first_line`. Jos `text` ei ole tyhjä merkkijono, `next` palauttaa `Some`-arvon, joka sisältää merkkijonoviipaleen ensimmäisestä rivistä `text`:issä.

`?` erottaa merkkijonoviipaleen, ja voimme kutsua `chars`:ia kyseisellä merkkijonoviipaleella saadaksemme iteraattorin sen merkeistä. Olemme kiinnostuneita viimeisestä merkistä tällä ensimmäisellä rivillä, joten kutsumme `last`:ia palauttaaksemme viimeisen kohteen iteraattorista. Tämä on `Option`, koska on mahdollista, että ensimmäinen rivi on tyhjä merkkijono; esimerkiksi jos `text` alkaa tyhjällä rivillä mutta sisältää merkkejä muilla riveillä, kuten `"\nhi"`. Jos kuitenkin ensimmäisellä rivillä on viimeinen merkki, se palautetaan `Some`-variantissa. Keskellä oleva `?`-operaattori antaa meille tiiviin tavan ilmaista tämä logiikka, jolloin voimme toteuttaa funktion yhdellä rivillä. Jos emme voisi käyttää `?`-operaattoria `Option`:issa, meidän pitäisi toteuttaa tämä logiikka useammilla metodikutsuilla tai `match`-lausekkeella.

Huomaa, että voit käyttää `?`-operaattoria `Result`:issa funktiossa, joka palauttaa `Result`:in, ja voit käyttää `?`-operaattoria `Option`:issa funktiossa, joka palauttaa `Option`:in, mutta et voi sekoittaa niitä. `?`-operaattori ei automaattisesti muunna `Result`:ia `Option`:iksi tai päinvastoin; näissä tapauksissa voit käyttää metodeja, kuten `ok`-metodia `Result`:issa tai `ok_or`-metodia `Option`:issa, tehdäksesi muunnoksen eksplisiittisesti.

Tähän mennessä kaikki käyttämämme `main`-funktiot ovat palauttaneet `()`. `main`-funktio on erityinen, koska se on suoritettavan ohjelman sisään- ja uloskäyntipiste, ja sen palautustyypillä on rajoituksia, jotta ohjelma käyttäytyy odotetusti.

Onneksi `main` voi myös palauttaa `Result<(), E>`. Listaus 9-12 sisältää listauksen 9-10 koodin, mutta olemme muuttaneet `main`:in palautustyypiksi `Result<(), Box<dyn Error>>` ja lisänneet paluuarvon `Ok(())` loppuun. Tämä koodi kääntyy nyt.

<Listing number="9-12" file-name="src/main.rs" caption="`main`:in muuttaminen palauttamaan `Result<(), E>` sallii `?`-operaattorin käytön `Result`-arvoilla.">

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-12/src/main.rs}}
```

</Listing>

`Box<dyn Error>`-tyyppi on trait-objekti, jota käsittelemme kohdassa [”Trait-objektien käyttö jaetun käyttäytymisen abstrahointiin”][trait-objects]<!-- ignore --> luvussa 18. Toistaiseksi voit lukea `Box<dyn Error>`:in tarkoittavan ”mitä tahansa virhetyyppiä”. `?`:n käyttö `Result`-arvolla `main`-funktiossa virhetyypillä `Box<dyn Error>` on sallittua, koska se sallii minkä tahansa `Err`-arvon palauttamisen aikaisin. Vaikka tämän `main`-funktion runko palauttaisi vain `std::io::Error`-tyyppisiä virheitä, määrittämällä `Box<dyn Error>` tämä allekirjoitus pysyy oikeana, vaikka `main`:in runkoon lisättäisiin enemmän koodia, joka palauttaa muita virheitä.

Kun `main`-funktio palauttaa `Result<(), E>`, suoritettava lopettaa arvolla `0`, jos `main` palauttaa `Ok(())`, ja lopettaa nollasta poikkeavalla arvolla, jos `main` palauttaa `Err`-arvon. C-kielellä kirjoitetut suoritettavat palauttavat kokonaislukuja lopettaessaan: onnistuneesti lopettavat ohjelmat palauttavat kokonaisluvun `0`, ja virheelliset ohjelmat palauttavat jonkin muun kokonaisluvun kuin `0`. Rust palauttaa myös kokonaislukuja suoritettavista ollakseen yhteensopiva tämän käytännön kanssa.

`main`-funktio voi palauttaa mitä tahansa tyyppejä, jotka toteuttavat [traitin `std::process::Termination`][termination]<!-- ignore -->, joka sisältää funktion `report`, joka palauttaa `ExitCode`:n. Katso standardikirjaston dokumentaatiosta lisätietoja `Termination`-traitin toteuttamisesta omille tyypeillesi.

Nyt kun olemme käsitelleet `panic!`:in kutsumisen tai `Result`:in palauttamisen yksityiskohdat, palataan aiheeseen, miten päättää, kumpaa on sopivaa käyttää missäkin tilanteessa.

[handle_failure]: ch02-00-guessing-game-tutorial.html#handling-potential-failure-with-result
[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[termination]: ../std/process/trait.Termination.html
