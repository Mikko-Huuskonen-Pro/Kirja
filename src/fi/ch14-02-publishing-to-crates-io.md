## Kirjaston julkaiseminen Crates.io-palveluun

Olemme käyttäneet [crates.io](https://crates.io/)<!-- ignore --> -palvelun paketteja projektiemme riippuvuuksina, mutta voit myös jakaa koodiasi muiden kanssa julkaisemalla omat pakettisi. [crates.io](https://crates.io/)<!-- ignore --> -palvelun crate-rekisteri jakaa pakettiesi lähdekoodin, joten se isännöi pääasiassa avoimen lähdekoodin koodia.

Rustilla ja Cargolla on ominaisuuksia, jotka tekevät julkaistusta paketistasi helpomman löytää ja käyttää. Käsittelemme seuraavaksi joitakin näistä ominaisuuksista ja selitämme sitten, miten paketti julkaistaan.

### Hyödyllisten dokumentaatiokommenttien kirjoittaminen

Pakettiesi tarkka dokumentointi auttaa muita käyttäjiä tietämään, miten ja milloin niitä käytetään, joten dokumentaation kirjoittamiseen kannattaa panostaa aikaa. Luvussa 3 käsittelimme, miten Rust-koodia kommentoidaan kahdella kauttaviivalla `//`. Rustissa on myös erityinen kommenttityyppi dokumentaatiota varten, jota kutsutaan kätevästi _dokumentaatiokommentiksi_ (_documentation comment_), ja joka tuottaa HTML-dokumentaation. HTML näyttää dokumentaatiokommenttien sisällön julkisille API-kohteille, jotka on tarkoitettu ohjelmoijille, jotka haluavat tietää, miten _käyttää_ crateasi, ei sitä, miten crateasi _toteutetaan_.

Dokumentaatiokommentit käyttävät kolmea kauttaviivaa `///` kahden sijaan ja tukevat Markdown-merkintää tekstin muotoiluun. Sijoita dokumentaatiokommentit juuri ennen dokumentoitavaa kohdetta. Listausta 14-1 näyttää dokumentaatiokommentit `add_one`-funktiolle `my_crate`-nimisessä cratessa.

<Listing number="14-1" file-name="src/lib.rs" caption="Dokumentaatiokommentti funktiolle">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-01/src/lib.rs}}
```

</Listing>

Tässä annamme kuvauksen siitä, mitä `add_one`-funktio tekee, aloitamme osion otsikolla `Examples` ja annamme sitten koodin, joka demonstroi `add_one`-funktion käyttöä. Voimme tuottaa HTML-dokumentaation tästä dokumentaatiokommentista ajamalla `cargo doc` -komennon. Tämä komento ajaa Rustin mukana jaeltavan `rustdoc`-työkalun ja sijoittaa tuotetun HTML-dokumentaation _target/doc_-hakemistoon.

Kätevyyttä varten `cargo doc --open` -komennon ajaminen rakentaa nykyisen craten dokumentaation HTML-version (sekä kaikkien craten riippuvuuksien dokumentaation) ja avaa tuloksen verkkoselaimessa. Siirry `add_one`-funktioon ja näet, miten dokumentaatiokommenttien teksti renderöidään, kuten kuvassa 14-1:

<img alt="Rendered HTML documentation for the `add_one` function of `my_crate`" src="img/trpl14-01.png" class="center" />

<span class="caption">Kuva 14-1: HTML-dokumentaatio `add_one`-funktiolle</span>

#### Yleisesti käytetyt osiot

Käytimme `# Examples` -Markdown-otsikkoa listauksessa 14-1 luodaksemme HTML:ään osion otsikolla ”Examples”. Tässä on joitakin muita osioita, joita crate-kirjoittajat käyttävät yleisesti dokumentaatiossaan:

- **Panics**: Tilanteet, joissa dokumentoitu funktio voi panikoida. Funktion kutsujien, jotka eivät halua ohjelmansa panikoivan, tulisi varmistaa, etteivät he kutsu funktiota näissä tilanteissa.
- **Errors**: Jos funktio palauttaa `Result`-arvon, erilaisten virheiden kuvaaminen ja ehtojen, jotka voivat aiheuttaa näiden virheiden palauttamisen, kuvaus voi olla hyödyllistä kutsujille, jotta he voivat kirjoittaa koodia eri virhetyyppien käsittelyyn eri tavoin.
- **Safety**: Jos funktion kutsuminen on `unsafe` (käsittelemme turvattomuutta luvussa 20), pitäisi olla osio, joka selittää, miksi funktio on turvaton ja kattaa invariantit, joiden kutsujien odotetaan ylläpitävän.

Useimmat dokumentaatiokommentit eivät tarvitse kaikkia näitä osioita, mutta tämä on hyvä tarkistuslista muistuttamaan koodisi näkökulmista, joista käyttäjät ovat kiinnostuneita.

#### Dokumentaatiokommentit testeinä

Esimerkkikoodilohkojen lisääminen dokumentaatiokommentteihisi voi auttaa demonstroimaan kirjastosi käyttöä, ja siitä on lisähyöty: `cargo test` -komennon ajaminen ajaa dokumentaatiosi koodiesimerkit testeinä! Mikään ei ole parempaa kuin dokumentaatio esimerkein. Mutta mikään ei ole pahempaa kuin esimerkit, jotka eivät toimi, koska koodi on muuttunut dokumentaation kirjoittamisen jälkeen. Jos ajamme `cargo test` -komennon listauksen 14-1 `add_one`-funktion dokumentaatiolla, näemme testituloksissa osion, joka näyttää tältä:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-01/
cargo test
copy just the doc-tests section below
-->

```text
   Doc-tests my_crate

running 1 test
test src/lib.rs - add_one (line 5) ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.27s
```

Nyt jos muutamme joko funktiota tai esimerkkiä niin, että esimerkin `assert_eq!` panikoi, ja ajamme `cargo test` -komennon uudelleen, näemme, että dokumentaatiotestit havaitsevat esimerkin ja koodin olevan epäsynkassa!

#### Sisältävien kohteiden kommentointi

`//!`-tyylinen dokumentaatiokommentti lisää dokumentaation kommentteja _sisältävälle_ kohteelle sen sijaan, että kommenttien jälkeen tuleville kohteille. Käytämme näitä dokumentaatiokommentteja tyypillisesti crate-juuren tiedostossa (käytännössä _src/lib.rs_) tai moduulin sisällä dokumentoidaksemme craten tai moduulin kokonaisuudessaan.

Esimerkiksi lisätäksemme dokumentaation, joka kuvaa `my_crate`-craten tarkoitusta ja joka sisältää `add_one`-funktion, lisäämme dokumentaatiokommentit, jotka alkavat `//!`-merkinnällä, _src/lib.rs_-tiedoston alkuun, kuten listauksessa 14-2:

<Listing number="14-2" file-name="src/lib.rs" caption="Dokumentaatio `my_crate`-cratelle kokonaisuudessaan">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-02/src/lib.rs:here}}
```

</Listing>

Huomaa, ettei `//!`-merkinnällä alkavan viimeisen rivin jälkeen ole mitään koodia. Koska aloitimme kommentit `///`-merkinnän sijaan `//!`-merkinnällä, dokumentoimme kommenttia sisältävää kohdetta sen sijaan, että dokumentoisimme tämän kommentin jälkeen tulevaa kohdetta. Tässä tapauksessa kyseinen kohde on _src/lib.rs_-tiedosto, joka on crate-juuri. Nämä kommentit kuvaavat koko craten.

Kun ajamme `cargo doc --open` -komennon, nämä kommentit näytetään `my_crate`-craten dokumentaation etusivulla craten julkisten kohteiden listan yläpuolella, kuten kuvassa 14-2:

<img alt="Rendered HTML documentation with a comment for the crate as a whole" src="img/trpl14-02.png" class="center" />

<span class="caption">Kuva 14-2: Renderöity dokumentaatio `my_crate`-cratelle, mukaan lukien kommentti, joka kuvaa craten kokonaisuudessaan</span>

Dokumentaatiokommentit kohteiden sisällä ovat hyödyllisiä erityisesti cratejen ja moduulien kuvaamiseen. Käytä niitä selittämään säilön yleinen tarkoitus auttaaksesi käyttäjiäsi ymmärtämään craten rakenteen.

### Kätevän julkisen API:n vienti `pub use` -lauseella

Julkisen API:n rakenne on tärkeä huomioitava asia craten julkaisemisessa. Crateasi käyttävät ihmiset eivät tunne rakennetta yhtä hyvin kuin sinä, ja heillä saattaa olla vaikeuksia löytää haluamiaan osia, jos cratellasi on suuri moduulihierarkia.

Luvussa 7 käsittelimme, miten kohteet tehdään julkisiksi `pub`-avainsanalla ja tuodaan näkyvyysalueelle `use`-avainsanalla. Kehityksen aikana sinulle järkevä rakenne ei kuitenkaan välttämättä ole kätevä käyttäjillesi. Saatat haluta järjestää struct-rakenteet hierarkiaan, jossa on useita tasoja, mutta sitten ihmiset, jotka haluavat käyttää syvällä hierarkiassa määrittelemääsi tyyppiä, saattavat vaikeuksien kanssa selvittää, että tyyppi on olemassa. Heitä saattaa myös ärsyttää joutua kirjoittamaan `use my_crate::some_module::another_module::UsefulType;` `use my_crate::UsefulType;` -lauseen sijaan.

Hyvä uutinen on, että jos rakenne _ei_ ole kätevä muille kirjastoista käytettäväksi, sinun ei tarvitse järjestellä sisäistä rakennettasi uudelleen: voit sen sijaan viedä kohteita uudelleen luodaksesi julkisen rakenteen, joka poikkeaa yksityisestä rakenteestasi, käyttämällä `pub use` -lauseita. Uudelleenvienti ottaa julkisen kohteen yhdestä paikasta ja tekee sen julkiseksi toisessa paikassa, ikään kuin se olisi määritelty tuossa toisessa paikassa.

Esimerkiksi oletetaan, että teimme `art`-nimisen kirjaston taiteellisten käsitteiden mallintamiseen. Tässä kirjastossa on kaksi moduulia: `kinds`-moduuli, joka sisältää kaksi enumia nimeltä `PrimaryColor` ja `SecondaryColor`, ja `utils`-moduuli, joka sisältää funktion nimeltä `mix`, kuten listauksessa 14-3:

<Listing number="14-3" file-name="src/lib.rs" caption="`art`-kirjasto, jonka kohteet on järjestetty `kinds`- ja `utils`-moduuleihin">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-03/src/lib.rs:here}}
```

</Listing>

Kuva 14-3 näyttää, miltä tämän craten `cargo doc` -komennolla tuottaman dokumentaation etusivu näyttäisi:

<img alt="Rendered documentation for the `art` crate that lists the `kinds` and `utils` modules" src="img/trpl14-03.png" class="center" />

<span class="caption">Kuva 14-3: `art`-craten dokumentaation etusivu, joka listaa `kinds`- ja `utils`-moduulit</span>

Huomaa, että `PrimaryColor`- ja `SecondaryColor`-tyypit eivät ole etusivulla, eikä `mix`-funktio ole. Meidän täytyy klikata `kinds`- ja `utils`-moduuleja nähdäksemme ne.

Toinen tästä kirjastosta riippuva crate tarvitsisi `use`-lauseita, jotka tuovat `art`-craten kohteet näkyvyysalueelle määrittelemällä nykyisen moduulirakenteen. Listausta 14-4 näyttää esimerkin cratesta, joka käyttää `art`-craten `PrimaryColor`- ja `mix`-kohteita:

<Listing number="14-4" file-name="src/main.rs" caption="Crate, joka käyttää `art`-craten kohteita sen sisäisen rakenteen viennin kautta">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-04/src/main.rs}}
```

</Listing>

Listauksen 14-4 koodin kirjoittajan, joka käyttää `art`-cratea, täytyi selvittää, että `PrimaryColor` on `kinds`-moduulissa ja `mix` on `utils`-moduulissa. `art`-craten moduulirakenne on merkityksellisempi `art`-cratea kehittäville kuin sitä käyttäville. Sisäinen rakenne ei sisällä hyödyllistä tietoa jollekin, joka yrittää ymmärtää `art`-craten käyttöä, vaan aiheuttaa hämmennystä, koska sitä käyttävien kehittäjien täytyy selvittää, mistä etsiä, ja heidän täytyy määrittää moduulinimet `use`-lauseissaan.

Poistaaksemme sisäisen rakenteen julkisesta API:sta voimme muokata listauksen 14-3 `art`-crate-koodia lisäämällä `pub use` -lauseita viedäksemme kohteet uudelleen ylimmälle tasolle, kuten listauksessa 14-5:

<Listing number="14-5" file-name="src/lib.rs" caption="`pub use` -lauseiden lisääminen kohteiden uudelleenvientiin">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-05/src/lib.rs:here}}
```

</Listing>

`cargo doc` -komennolla tuottamamme API-dokumentaation etusivu listaa ja linkittää nyt uudelleenviedyt kohteet, kuten kuvassa 14-4, mikä tekee `PrimaryColor`- ja `SecondaryColor`-tyypeistä ja `mix`-funktiosta helpommin löydettäviä.

<img alt="Rendered documentation for the `art` crate with the re-exports on the front page" src="img/trpl14-04.png" class="center" />

<span class="caption">Kuva 14-4: `art`-craten dokumentaation etusivu, joka listaa uudelleenviedyt kohteet</span>

`art`-craten käyttäjät voivat edelleen nähdä ja käyttää listauksen 14-3 sisäistä rakennetta, kuten listauksessa 14-4 demonstroitu, tai he voivat käyttää listauksen 14-5 kätevämpää rakennetta, kuten listauksessa 14-6:

<Listing number="14-6" file-name="src/main.rs" caption="Ohjelma, joka käyttää `art`-craten uudelleenvietyjä kohteita">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-06/src/main.rs:here}}
```

</Listing>

Tapauksissa, joissa on monia sisäkkäisiä moduuleja, uudelleenviedyt tyyppien vienti ylimmälle tasolle `pub use` -lauseella voi merkittävästi parantaa craten käyttäjien kokemusta. Toinen yleinen `pub use` -käyttö on riippuvuuden määritelmien uudelleenvienti nykyisessä cratessa, jotta kyseisen craten määritelmät tulevat osaksi craten julkista API:ta.

Hyödyllisen julkisen API-rakenteen luominen on enemmän taidetta kuin tiedettä, ja voit iteroida löytääksesi käyttäjillesi parhaiten toimivan API:n. `pub use` -valinta antaa sinulle joustavuutta craten sisäisen rakenteen suhteen ja erottaa sen sisäisen rakenteen siitä, mitä esität käyttäjillesi. Tutustu asentamiesi cratejen koodiin nähdäksesi, poikkeaako niiden sisäinen rakenne julkisesta API:sta.

### Crates.io-tilin luominen

Ennen kuin voit julkaista crateja, sinun täytyy luoda tili [crates.io](https://crates.io/)<!-- ignore --> -palveluun ja hankkia API-tunnus. Tee tämä vierailemalla etusivulla osoitteessa [crates.io](https://crates.io/)<!-- ignore --> ja kirjautumalla GitHub-tilin kautta. (GitHub-tili on tällä hetkellä vaatimus, mutta sivusto saattaa tukea muita tapoja tilin luomiseen tulevaisuudessa.) Kun olet kirjautunut sisään, vieraile tilisi asetuksissa osoitteessa [https://crates.io/me/](https://crates.io/me/)<!-- ignore --> ja hae API-avaimesi. Suorita sitten `cargo login` -komento ja liitä API-avaimesi kehotettaessa, näin:

```console
$ cargo login
abcdefghijklmnopqrstuvwxyz012345
```

Tämä komento ilmoittaa Cargolle API-tunnuksestasi ja tallentaa sen paikallisesti tiedostoon _~/.cargo/credentials_. Huomaa, että tämä tunnus on _salaisuus_: älä jaa sitä kenellekään muulle. Jos jaat sen jostain syystä kenellekään, sinun pitäisi mitätöidä se ja luoda uusi tunnus osoitteessa [crates.io](https://crates.io/)<!-- ignore
-->.

### Metatietojen lisääminen uuteen crateen

Oletetaan, että sinulla on crate, jonka haluat julkaista. Ennen julkaisemista sinun täytyy lisätä metatietoja craten _Cargo.toml_-tiedoston `[package]`-osioon.

Cratellasi täytyy olla yksilöllinen nimi. Kun työskentelet craten parissa paikallisesti, voit nimetä craten miten haluat. [crates.io](https://crates.io/)<!-- ignore --> -palvelun cratenimet jaetaan kuitenkin ensimmäisen tulevan periaatteella. Kun craten nimi on varattu, kukaan muu ei voi julkaista cratea sillä nimellä. Ennen julkaisuyritystä etsi haluamasi nimi. Jos nimi on jo käytössä, sinun täytyy löytää toinen nimi ja muokata `name`-kenttää _Cargo.toml_-tiedoston `[package]`-osiossa käyttämään uutta nimeä julkaisemista varten, näin:

<span class="filename">Filename: Cargo.toml</span>

```toml
[package]
name = "guessing_game"
```

Vaikka olisit valinnut yksilöllisen nimen, kun ajat `cargo publish` -komennon julkaistaksesi craten tässä vaiheessa, saat varoituksen ja sitten virheen:

<!-- manual-regeneration
Create a new package with an unregistered name, making no further modifications
  to the generated package, so it is missing the description and license fields.
cargo publish
copy just the relevant lines below
-->

```console
$ cargo publish
    Updating crates.io index
warning: manifest has no description, license, license-file, documentation, homepage or repository.
See https://doc.rust-lang.org/cargo/reference/manifest.html#package-metadata for more info.
--snip--
error: failed to publish to registry at https://crates.io

Caused by:
  the remote server responded with an error (status 400 Bad Request): missing or empty metadata fields: description, license. Please see https://doc.rust-lang.org/cargo/reference/manifest.html for more information on configuring these fields
```

Tämä virhe johtuu siitä, että sinulta puuttuu tärkeitä tietoja: kuvaus ja lisenssi ovat pakollisia, jotta ihmiset tietävät, mitä craten tekee ja millä ehdoilla he voivat käyttää sitä. Lisää _Cargo.toml_-tiedostoon kuvaus, joka on vain lause tai kaksi, koska se näkyy craten kanssa hakutuloksissa. `license`-kenttään sinun täytyy antaa _lisenssitunnistearvo_. [Linux Foundationin Software Package Data Exchange (SPDX)][spdx] listaa tunnisteet, joita voit käyttää tähän arvoon. Esimerkiksi määrittääksesi, että olet lisensoinut craten MIT-lisenssillä, lisää `MIT`-tunniste:

<span class="filename">Filename: Cargo.toml</span>

```toml
[package]
name = "guessing_game"
license = "MIT"
```

Jos haluat käyttää lisenssiä, joka ei esiinny SPDX-listassa, sinun täytyy sijoittaa kyseisen lisenssin teksti tiedostoon, sisällyttää tiedosto projektiisi ja käyttää sitten `license-file`-kenttää määrittämään kyseisen tiedoston nimi `license`-avaimen sijaan.

Ohjeet siihen, mikä lisenssi sopii projektiisi, ylittävät tämän kirjan laajuuden. Monet Rust-yhteisön jäsenet lisensoivat projektinsa samalla tavalla kuin Rust käyttämällä kaksoislisenssiä `MIT OR Apache-2.0`. Tämä käytäntö osoittaa, että voit myös määrittää useita lisenssitunnisteita erotettuna `OR`-sanalla, jotta projektillasi on useita lisenssejä.

Kun olet lisännyt yksilöllisen nimen, version, kuvauksen ja lisenssin, julkaisuvalmiin projektin _Cargo.toml_-tiedosto saattaa näyttää tältä:

<span class="filename">Filename: Cargo.toml</span>

```toml
[package]
name = "guessing_game"
version = "0.1.0"
edition = "2024"
description = "A fun game where you guess what number the computer has chosen."
license = "MIT OR Apache-2.0"

[dependencies]
```

[Cargon dokumentaatio](https://doc.rust-lang.org/cargo/) kuvaa muuta metatietoa, jonka voit määrittää varmistaaksesi, että muut löytävät ja käyttävät crateasi helpommin.

### Julkaiseminen Crates.io-palveluun

Nyt kun olet luonut tilin, tallentanut API-tunnuksesi, valinnut nimen cratelle ja määrittänyt vaaditut metatiedot, olet valmis julkaisemaan! Craten julkaiseminen lataa tietyn version [crates.io](https://crates.io/)<!-- ignore --> -palveluun muiden käytettäväksi.

Ole varovainen, koska julkaisu on _pysyvä_. Versiota ei voi koskaan korvata, eikä koodia voi poistaa. Yksi [crates.io](https://crates.io/)<!-- ignore --> -palvelun tärkeimmistä tavoitteista on toimia pysyvänä koodiarkistona, jotta kaikkien [crates.io](https://crates.io/)<!-- ignore --> -palvelun crateista riippuvien projektien käännökset toimivat edelleen. Versioiden poistamisen salliminen tekisi tämän tavoitteen toteuttamisen mahdottomaksi. Julkaistavien crateversioiden määrälle ei kuitenkaan ole rajaa.

Aja `cargo publish` -komento uudelleen. Sen pitäisi nyt onnistua:

<!-- manual-regeneration
go to some valid crate, publish a new version
cargo publish
copy just the relevant lines below
-->

```console
$ cargo publish
    Updating crates.io index
   Packaging guessing_game v0.1.0 (file:///projects/guessing_game)
   Verifying guessing_game v0.1.0 (file:///projects/guessing_game)
   Compiling guessing_game v0.1.0
(file:///projects/guessing_game/target/package/guessing_game-0.1.0)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.19s
   Uploading guessing_game v0.1.0 (file:///projects/guessing_game)
```

Onnittelut! Olet nyt jakanut koodisi Rust-yhteisön kanssa, ja kuka tahansa voi helposti lisätä craten riippuvuudekseen projektiinsa.

### Olemassa olevan craten uuden version julkaiseminen

Kun olet tehnyt muutoksia crateesi ja olet valmis julkaisemaan uuden version, muutat _Cargo.toml_-tiedostossa määritettyä `version`-arvoa ja julkaiset uudelleen. Käytä [semanttisen versionoinnin sääntöjä][semver] päättääksesi, mikä sopiva seuraava versionumero on tekemiesi muutosten perusteella. Suorita sitten `cargo publish` -komento ladataksesi uuden version.

<!-- Old link, do not remove -->

<a id="removing-versions-from-cratesio-with-cargo-yank"></a>

### Versioiden poistaminen käytöstä Crates.io-palvelussa `cargo yank` -komennolla

Vaikka et voi poistaa craten aiempia versioita, voit estää tulevia projekteja lisäämästä niitä uutena riippuvuutena. Tämä on hyödyllistä, kun crateversio on jostain syystä rikki. Tällaisissa tilanteissa Cargo tukee crateversion _poistamista käytöstä_ (_yanking_).

Version poistaminen käytöstä estää uusia projekteja riippumasta kyseisestä versiosta, mutta sallii kaikkien olemassa olevien projektien, jotka riippuvat siitä, jatkaa. Pohjimmiltaan poistaminen käytöstä tarkoittaa, että kaikki projektit, joilla on _Cargo.lock_-tiedosto, eivät hajoa, eikä mikään tuleva _Cargo.lock_-tiedosto käytä poistettua versiota.

Poistaaksesi craten version käytöstä, craten hakemistossa, jonka olet aiemmin julkaissut, suorita `cargo yank` -komento ja määritä, minkä version haluat poistaa käytöstä. Esimerkiksi jos olemme julkaisseet `guessing_game`-craten version 1.0.1 ja haluamme poistaa sen käytöstä, `guessing_game`-projektin hakemistossa suorittaisimme:

<!-- manual-regeneration:
cargo yank carol-test --version 2.1.0
cargo yank carol-test --version 2.1.0 --undo
-->

```console
$ cargo yank --vers 1.0.1
    Updating crates.io index
        Yank guessing_game@1.0.1
```

Lisäämällä `--undo`-lipun komentoon voit myös perua poistamisen käytöstä ja sallia projektien alkaa riippua versiosta uudelleen:

```console
$ cargo yank --vers 1.0.1 --undo
    Updating crates.io index
      Unyank guessing_game@1.0.1
```

Poistaminen käytöstä _ei_ poista mitään koodia. Se ei esimerkiksi voi poistaa vahingossa ladattuja salaisuuksia. Jos näin tapahtuu, sinun täytyy nollata nämä salaisuudet välittömästi.

[spdx]: http://spdx.org/licenses/
[semver]: http://semver.org/
