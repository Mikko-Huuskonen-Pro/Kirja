## Cargo-työtilat

Luvussa 12 rakensimme paketin, joka sisälsi binääricraten ja kirjastocraten. Projektin kehittyessä kirjastocrate voi kasvaa niin suureksi, että haluatte jakaa pakettinne edelleen useisiin kirjastocrateihin. Cargo tarjoaa ominaisuuden nimeltä _työtilat_, joka voi auttaa hallitsemaan useita toisiinsa liittyviä paketteja, joita kehitetään rinnakkain.

### Työtilan luominen

_Työtila_ on joukko paketteja, jotka jakavat saman _Cargo.lock_-tiedoston ja tulostushakemiston. Tehdään projekti käyttäen työtilaa—käytämme triviaalia koodia, jotta voimme keskittyä työtilan rakenteeseen. Työtilan voi rakentaa monella tavalla, joten näytämme vain yhden yleisen tavan. Työtilassa on binääri ja kaksi kirjastoa. Binääri, joka tarjoaa päätoiminnallisuuden, riippuu kahdesta kirjastosta. Yksi kirjasto tarjoaa `add_one`-funktion ja toinen kirjasto `add_two`-funktion. Nämä kolme cratea ovat osa samaa työtilaa. Aloitamme luomalla uuden hakemiston työtilalle:

```console
$ mkdir add
$ cd add
```

Seuraavaksi _add_-hakemistossa luomme _Cargo.toml_-tiedoston, joka määrittää koko työtilan. Tässä tiedostossa ei ole `[package]`-osiota. Sen sijaan se alkaa `[workspace]`-osiolla, jonka avulla voimme lisätä jäseniä työtilaan. Varmistamme myös, että käytämme Cargon uusinta ja parasta resolver-algoritmia työtilassamme asettamalla `resolver`-asetuksen arvoksi `"3"`:

<span class="filename">Tiedostonimi: Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-01-workspace/add/Cargo.toml}}
```

Seuraavaksi luomme `adder`-binääricraten suorittamalla `cargo new` -komennon _add_-hakemistossa:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-01-adder-crate/add
remove `members = ["adder"]` from Cargo.toml
rm -rf adder
cargo new adder
copy output below
-->

```console
$ cargo new adder
     Created binary (application) `adder` package
      Adding `adder` as member of workspace at `file:///projects/add`
```

`cargo new` -komennon suorittaminen työtilan sisällä lisää myös automaattisesti juuri luodun paketin työtilan `Cargo.toml`-tiedoston `[workspace]`-määrittelyn `members`-avaimeen, näin:

```toml
{{#include ../listings/ch14-more-about-cargo/output-only-01-adder-crate/add/Cargo.toml}}
```

Tässä vaiheessa voimme rakentaa työtilan suorittamalla `cargo build` -komennon. Tiedostot _add_-hakemistossanne pitäisi näyttää tältä:

```text
├── Cargo.lock
├── Cargo.toml
├── adder
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── target
```

Työtilalla on yksi _target_-hakemisto ylätasolla, johon käännetyt artefaktit sijoitetaan; `adder`-paketilla ei ole omaa _target_-hakemistoa. Vaikka suorittaisimme `cargo build` -komennon _adder_-hakemiston sisältä, käännetyt artefaktit päätyisivät silti hakemistoon _add/target_ eikä _add/adder/target_. Cargo rakentaa _target_-hakemiston työtilassa näin, koska työtilan cratet on tarkoitettu riippuvan toisistaan. Jos jokaisella cratella olisi oma _target_-hakemisto, jokaisen craten täytyisi kääntää uudelleen jokainen työtilan muista crateista sijoittaakseen artefaktit omaan _target_-hakemistoonsa. Jakamalla yhden _target_-hakemiston cratet voivat välttää tarpeettoman uudelleenkääntämisen.

### Toisen paketin luominen työtilaan

Seuraavaksi luodaan työtilaan toinen jäsenpaketti ja kutsutaan sitä `add_one`. Luodaan uusi kirjastocrate nimeltä `add_one`:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-02-add-one/add
remove `"add_one"` from `members` list in Cargo.toml
rm -rf add_one
cargo new add_one --lib
copy output below
-->

```console
$ cargo new add_one --lib
     Created library `add_one` package
      Adding `add_one` as member of workspace at `file:///projects/add`
```

Ylätason _Cargo.toml_-tiedosto sisältää nyt _add_one_-polun `members`-listassa:

<span class="filename">Tiedostonimi: Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/Cargo.toml}}
```

_add_-hakemistossanne pitäisi nyt olla nämä hakemistot ja tiedostot:

```text
├── Cargo.lock
├── Cargo.toml
├── add_one
│   ├── Cargo.toml
│   └── src
│       └── lib.rs
├── adder
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── target
```

Lisätään _add_one/src/lib.rs_-tiedostoon `add_one`-funktio:

<span class="filename">Tiedostonimi: add_one/src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/add_one/src/lib.rs}}
```

Nyt voimme tehdä `adder`-paketista, jossa on binäärimme, riippuvaisen `add_one`-paketista, jossa on kirjastomme. Ensin meidän täytyy lisätä polkuriippuvuus `add_one`-pakettiin tiedostoon _adder/Cargo.toml_.

<span class="filename">Tiedostonimi: adder/Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/adder/Cargo.toml:6:7}}
```

Cargo ei oleta, että työtilan cratet riippuvat toisistaan, joten meidän täytyy määritellä riippuvuussuhteet eksplisiittisesti.

Seuraavaksi käytetään `add_one`-funktiota (`add_one`-cratesta) `adder`-cratessa. Avatkaa _adder/src/main.rs_-tiedosto ja muuttakaa `main`-funktiota kutsumaan `add_one`-funktiota, kuten listauksessa 14-7.

<Listing number="14-7" file-name="adder/src/main.rs" caption="`add_one`-kirjastocraten käyttö `adder`-cratessa">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-07/add/adder/src/main.rs}}
```

</Listing>

Rakennetaan työtila suorittamalla `cargo build` -komento ylätason _add_-hakemistossa!

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-07/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.22s
```

Suorittaaksemme binääricraten _add_-hakemistosta voimme määrittää, minkä paketin työtilassa haluamme suorittaa käyttämällä `-p`-argumenttia ja paketin nimeä komennolla `cargo run`:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-07/add
cargo run -p adder
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo run -p adder
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running `target/debug/adder`
Hello, world! 10 plus one is 11!
```

Tämä suorittaa koodin tiedostossa _adder/src/main.rs_, joka riippuu `add_one`-cratesta.

<!-- Old headings. Do not remove or links may break. -->

<a id="depending-on-an-external-package-in-a-workspace"></a>

### Ulkoisen paketin riippuvuus

Huomaa, että työtilassa on vain yksi _Cargo.lock_-tiedosto ylätasolla sen sijaan, että jokaisella craten hakemistolla olisi oma _Cargo.lock_. Tämä varmistaa, että kaikki cratet käyttävät samaa versiota kaikista riippuvuuksista. Jos lisäämme `rand`-paketin tiedostoihin _adder/Cargo.toml_ ja _add_one/Cargo.toml_, Cargo ratkaisee molemmat yhdeksi `rand`-versioksi ja tallentaa sen yhteen _Cargo.lock_-tiedostoon. Kaikkien työtilan cratejen saman riippuvuuksien käyttö tarkoittaa, että cratet ovat aina yhteensopivia toistensa kanssa. Lisätään `rand`-crate `[dependencies]`-osioon tiedostoon _add_one/Cargo.toml_ voidaksemme käyttää `rand`-cratea `add_one`-cratessa:

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch01-01-installation.md
* ch02-00-guessing-game-tutorial.md
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
-->

<span class="filename">Tiedostonimi: add_one/Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-03-workspace-with-external-dependency/add/add_one/Cargo.toml:6:7}}
```

Voimme nyt lisätä `use rand;` tiedostoon _add_one/src/lib.rs_ ja rakentaa koko työtilan suorittamalla `cargo build` -komennon _add_-hakemistossa, mikä tuo mukaan ja kääntää `rand`-craten. Saamme yhden varoituksen, koska emme viittaa näkyviin tuomaamme `rand`-crateen:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-03-workspace-with-external-dependency/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
    Updating crates.io index
  Downloaded rand v0.10.1
   --snip--
   Compiling rand v0.10.1
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
warning: unused import: `rand`
 --> add_one/src/lib.rs:1:5
  |
1 | use rand;
  |     ^^^^
  |
  = note: `#[warn(unused_imports)]` (part of `#[warn(unused)]`) on by default

warning: `add_one` (lib) generated 1 warning (run `cargo fix --lib -p add_one` to apply 1 suggestion)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.95s
```

Ylätason _Cargo.lock_ sisältää nyt tietoa `add_one`-craten riippuvuudesta `rand`-crateen. Vaikka `rand`-cratea käytetään jossain työtilassa, emme voi käyttää sitä muissa työtilan crateissa, ellemme lisää `rand`-cratea myös niiden _Cargo.toml_-tiedostoihin. Esimerkiksi jos lisäämme `use rand;` tiedostoon _adder/src/main.rs_ `adder`-paketille, saamme virheen:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-03-use-rand/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
  --snip--
   Compiling adder v0.1.0 (file:///projects/add/adder)
error[E0432]: unresolved import `rand`
 --> adder/src/main.rs:2:5
  |
2 | use rand;
  |     ^^^^ no external crate `rand`
```

Korjataksemme tämän muokkaa `adder`-paketin _Cargo.toml_-tiedostoa ja ilmoittakaa, että `rand` on riippuvuus myös sille. `adder`-paketin rakentaminen lisää `rand`-craten `adder`-paketin riippuvuuksien listaan tiedostossa _Cargo.lock_, mutta yhtään lisäkopiota `rand`-cratesta ei ladata. Cargo varmistaa, että jokainen crate jokaisessa työtilan paketissa, joka käyttää `rand`-pakettia, käyttää samaa versiota niin kauan kuin ne määrittävät yhteensopivia versioita `rand`-cratesta, säästäen tilaa ja varmistaen, että työtilan cratet ovat yhteensopivia toistensa kanssa.

Jos työtilan cratet määrittävät yhteensopimattomia versioita samasta riippuvuudesta, Cargo ratkaisee jokaisen niistä, mutta yrittää silti ratkaista mahdollisimman vähän versioita.

### Testin lisääminen työtilaan

Lisäparannuksena lisätään testi `add_one::add_one`-funktiolle `add_one`-cratessa:

<span class="filename">Tiedostonimi: add_one/src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add/add_one/src/lib.rs}}
```

Suorittakaa nyt `cargo test` ylätason _add_-hakemistossa. `cargo test` -komennon suorittaminen tällaisessa työtilassa suorittaa testit kaikille työtilan crateille:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add
cargo test
copy output below; the output updating script doesn't handle subdirectories in
paths properly
-->

```console
$ cargo test
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.20s
     Running unittests src/lib.rs (target/debug/deps/add_one-93c49ee75dc46543)

running 1 test
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests src/main.rs (target/debug/deps/adder-3a47283c568d2b6a)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests add_one

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

Tulosteen ensimmäinen osa osoittaa, että `add_one`-craten `it_works`-testi läpäisi. Seuraava osa osoittaa, että `adder`-cratessa ei löytynyt testejä, ja viimeinen osa osoittaa, että `add_one`-cratessa ei löytynyt dokumentaatiotestejä.

Voimme myös suorittaa testit yhdelle tietylle cratelle työtilassa ylätason hakemistosta käyttämällä `-p`-lippua ja määrittämällä craten nimen, jota haluamme testata:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add
cargo test -p add_one
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo test -p add_one
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running unittests src/lib.rs (target/debug/deps/add_one-93c49ee75dc46543)

running 1 test
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests add_one

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

Tämä tuloste osoittaa, että `cargo test` suoritti vain `add_one`-craten testit eikä suorittanut `adder`-craten testejä.

Jos julkaisette työtilan cratet [crates.io](https://crates.io/)<!-- ignore --> -palveluun, jokainen työtilan crate on julkaistava erikseen. Kuten `cargo test`, voimme julkaista tietyn craten työtilastamme käyttämällä `-p`-lippua ja määrittämällä craten nimen, jonka haluamme julkaista.

Lisäharjoitukseksi lisätkää tähän työtilaan `add_two`-crate samalla tavalla kuin `add_one`-crate!

Kun projektinne kasvaa, harkitkaa työtilan käyttämistä: on helpompi ymmärtää pienempiä yksittäisiä komponentteja kuin yhtä suurta koodipalaa. Lisäksi cratet työtilassa helpottavat cratejen välistä koordinointia, jos niitä muutetaan usein samaan aikaan.
