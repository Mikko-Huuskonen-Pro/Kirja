## Testien organisointi

Kuten luvun alussa mainittiin, testaus on monimutkainen ala, ja eri ihmiset käyttävät eri terminologiaa ja organisointia. Rust-yhteisö ajattelee testejä kahden pääkategorian kautta: yksikkötestit ja integraatiotestit. _Yksikkötestit_ ovat pieniä ja keskittyneempiä, testaavat yhden moduulin erillään kerrallaan ja voivat testata yksityisiä rajapintoja. _Integraatiotestit_ ovat täysin kirjastosi ulkopuolella ja käyttävät koodiasi samalla tavalla kuin mikä tahansa muu ulkoinen koodi, käyttäen vain julkista rajapintaa ja mahdollisesti testaten useita moduuleja per testi.

Molempien testityyppien kirjoittaminen on tärkeää varmistaaksesi, että kirjastosi osat toimivat odottamallasi tavalla erikseen ja yhdessä.

### Yksikkötestit

Yksikkötestien tarkoitus on testata jokainen koodin yksikkö erillään muusta koodista, jotta voit nopeasti paikantaa, missä koodi toimii ja missä ei odotetulla tavalla. Sijoitat yksikkötestit _src_-hakemistoon kuhunkin tiedostoon, jossa on testattava koodi. Käytäntö on luoda jokaiseen tiedostoon `tests`-niminen moduuli testifunktioita varten ja merkitä moduuli `cfg(test)`:llä.

#### Testimoduuli ja `#[cfg(test)]`

`#[cfg(test)]`-annotaatio `tests`-moduulissa kertoo Rustille kääntämään ja ajamaan testikoodin vain, kun ajat `cargo test`:in, ei kun ajat `cargo build`:in. Tämä säästää käännösaikaa, kun haluat vain rakentaa kirjaston, ja säästää tilaa lopullisessa käännettyssä artefaktissa, koska testit eivät sisälly siihen. Näet, että koska integraatiotestit sijoitetaan eri hakemistoon, ne eivät tarvitse `#[cfg(test)]`-annotaatiota. Koska yksikkötestit ovat samoissa tiedostoissa kuin koodi, käytät `#[cfg(test)]`:ää määrittämään, ettei niitä sisällytetä käännettyyn tulokseen.

Muista, että kun loimme uuden `adder`-projektin tämän luvun ensimmäisessä osiossa, Cargo generoi tämän koodin puolestamme:

<span class="filename">Filename: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-01/src/lib.rs}}
```

Automaattisesti generoidussa `tests`-moduulissa attribuutti `cfg` tarkoittaa _konfiguraatiota_ ja kertoo Rustille, että seuraava kohde pitäisi sisällyttää vain tietyn konfiguraatioasetuksen perusteella. Tässä tapauksessa konfiguraatioasetus on `test`, jonka Rust tarjoaa testien kääntämiseen ja ajamiseen. `cfg`-attribuutin avulla Cargo kääntää testikoodimme vain, jos aktiivisesti ajamme testit `cargo test`:llä. Tämä sisältää kaikki apufunktiot, jotka saattavat olla tämän moduulin sisällä, `#[test]`:lla merkittyjen funktioiden lisäksi.

#### Yksityisten funktioiden testaaminen

Testausyhteisössä on keskustelua siitä, pitäisikö yksityisiä funktioita testata suoraan, ja muut kielet tekevät yksityisten funktioiden testaamisesta vaikeaa tai mahdotonta. Riippumatta siitä, mihin testausideologiaan sitoudut, Rustin yksityisyyssäännöt sallivat yksityisten funktioiden testaamisen. Harkitse Listauksen 11-12 koodia, jossa on yksityinen funktio `internal_adder`.

<Listing number="11-12" file-name="src/lib.rs" caption="Yksityisen funktion testaaminen">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-12/src/lib.rs}}
```

</Listing>

Huomaa, että `internal_adder`-funktiota ei ole merkitty `pub`:iksi. Testit ovat vain Rust-koodia, ja `tests`-moduuli on vain toinen moduuli. Kuten käsittelimme [”Polut kohteen viittaamiseen moduulipuussa”][paths]<!-- ignore --> -osiossa, lapsimoduulien kohteet voivat käyttää esi-isämoduuliensa kohteita. Tässä testissä tuomme kaikki `tests`-moduulin emon kohteet laajuuteen `use super::*`:lla, ja sitten testi voi kutsua `internal_adder`:ia. Jos et mielestäsi yksityisiä funktioita pitäisi testata, Rustissa ei ole mitään, mikä pakottaisi sinua tekemään niin.

### Integraatiotestit

Rustissa integraatiotestit ovat täysin kirjastosi ulkopuolella. Ne käyttävät kirjastoasi samalla tavalla kuin mikä tahansa muu koodi, mikä tarkoittaa, että ne voivat kutsua vain kirjastosi julkisen API:n osia olevia funktioita. Niiden tarkoitus on testata, toimiiko kirjastosi monet osat yhdessä oikein. Koodin yksiköt, jotka toimivat oikein erikseen, voivat aiheuttaa ongelmia integroituna, joten integroidun koodin testikattavuus on myös tärkeää. Integraatiotestien luomiseksi tarvitset ensin _tests_-hakemiston.

#### _tests_-hakemisto

Luomme _tests_-hakemiston projektihakemiston ylätasolle, _src_:n viereen. Cargo tietää etsiä integraatiotestitiedostoja tästä hakemistosta. Voimme sitten tehdä niin monta testitiedostoa kuin haluamme, ja Cargo kääntää jokaisen tiedoston erillisenä cratenä.

Luodaan integraatiotesti. Kun Listauksen 11-12 koodi on edelleen tiedostossa _src/lib.rs_, tee _tests_-hakemisto ja luo uusi tiedosto nimeltä _tests/integration_test.rs_. Hakemistorakenteesi pitäisi näyttää tältä:

```text
adder
├── Cargo.lock
├── Cargo.toml
├── src
│   └── lib.rs
└── tests
    └── integration_test.rs
```

Kirjoita Listauksen 11-13 koodi tiedostoon _tests/integration_test.rs_.

<Listing number="11-13" file-name="tests/integration_test.rs" caption="Integraatiotesti `adder`-craten funktiolle">

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-13/tests/integration_test.rs}}
```

</Listing>

Jokainen tiedosto _tests_-hakemistossa on erillinen crate, joten meidän täytyy tuoda kirjastomme kunkin testicraten laajuuteen. Tätä varten lisäämme koodin alkuun `use adder::add_two;`, jota emme tarvinne yksikkötesteissä.

Meidän ei tarvitse merkitä mitään koodia tiedostossa _tests/integration_test.rs_ annotaatiolla `#[cfg(test)]`. Cargo käsittelee _tests_-hakemiston erityisesti ja kääntää tämän hakemiston tiedostot vain, kun ajamme `cargo test`:in. Aja `cargo test` nyt:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-13/output.txt}}
```

Tulosteen kolme osiota sisältävät yksikkötestit, integraatiotestin ja dokumentaatiotestit. Huomaa, että jos mikä tahansa testi osiossa epäonnistuu, seuraavia osioita ei ajeta. Esimerkiksi jos yksikkötesti epäonnistuu, integraatio- ja dokumentaatiotesteistä ei tule tulostetta, koska ne ajetaan vain, jos kaikki yksikkötestit läpäisevät.

Yksikkötestien ensimmäinen osio on sama kuin olemme nähneet: yksi rivi kutakin yksikkötestiä kohti (yksi nimeltä `internal`, jonka lisäsimme Listauksessa 11-12) ja sitten yhteenvetorivi yksikkötesteille.

Integraatiotestien osio alkaa rivillä `Running tests/integration_test.rs`. Seuraavaksi on rivi kutakin kyseisen integraatiotestin testifunktiota kohti ja yhteenvetorivi integraatiotestin tuloksille juuri ennen kuin `Doc-tests adder` -osio alkaa.

Jokaisella integraatiotestitiedostolla on oma osionsa, joten jos lisäämme lisää tiedostoja _tests_-hakemistoon, tulee lisää integraatiotestien osioita.

Voimme silti ajaa tietyn integraatiotestifunktion määrittämällä testifunktion nimen argumentiksi `cargo test`:lle. Ajaaaksemme kaikki testit tietyssä integraatiotestitiedostossa, käytä `cargo test`:n `--test`-argumenttia, jota seuraa tiedoston nimi:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-05-single-integration/output.txt}}
```

Tämä komento ajaa vain testit tiedostossa _tests/integration_test.rs_.

#### Alimodulit integraatiotesteissä

Kun lisäät integraatiotestejä, saatat haluta tehdä lisää tiedostoja _tests_-hakemistoon niiden organisoimiseksi; voit esimerkiksi ryhmitellä testifunktiot sen toiminnallisuuden mukaan, jota ne testaavat. Kuten aiemmin mainittiin, jokainen tiedosto _tests_-hakemistossa käännetään omana erillisenä cratenään, mikä on hyödyllistä erillisten laajuuksien luomiseen, jotta käyttäytyminen muistuttaa läheisemmin sitä, miten loppukäyttäjät käyttävät crateasi. Tämä tarkoittaa kuitenkin, että _tests_-hakemiston tiedostot eivät jaa samaa käyttäytymistä kuin _src_:n tiedostot, kuten opit Luvussa 7 koodin jakamisesta moduuleihin ja tiedostoihin.

_tests_-hakemiston tiedostojen erilainen käyttäytyminen näkyy selvimmin, kun sinulla on joukko apufunktioita käytettäväksi useissa integraatiotestitiedostoissa ja yrität seurata Luvun 7 [”Moduulien erottaminen eri tiedostoihin”][separating-modules-into-files]<!-- ignore --> -osion ohjeita erottamaan ne yhteiseen moduuliin. Esimerkiksi, jos luomme tiedoston _tests/common.rs_ ja sijoitamme siihen funktion nimeltä `setup`, voimme lisätä `setup`-funktioon koodia, jota haluamme kutsua useista testifunktioista useissa testitiedostoissa:

<span class="filename">Filename: tests/common.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-12-shared-test-code-problem/tests/common.rs}}
```

Kun ajamme testit uudelleen, näemme testitulosteessa uuden osion _common.rs_-tiedostolle, vaikka tämä tiedosto ei sisällä testifunktioita eikä me kutsuneet `setup`-funktiota mistään:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-12-shared-test-code-problem/output.txt}}
```

Se, että `common` näkyy testituloksissa ja sille näytetään `running 0 tests`, ei ole sitä, mitä halusimme. Halusimme vain jakaa koodia muiden integraatiotestitiedostojen kanssa. Välttääksemme `common`:in näkymisen testitulosteessa, sen sijaan että loisimme _tests/common.rs_:n, luomme _tests/common/mod.rs_:n. Projektihakemisto näyttää nyt tältä:

```text
├── Cargo.lock
├── Cargo.toml
├── src
│   └── lib.rs
└── tests
    ├── common
    │   └── mod.rs
    └── integration_test.rs
```

Tämä on vanhempi nimeämiskäytäntö, jonka Rust myös ymmärtää ja josta mainitsimme [”Vaihtoehtoiset tiedostopolut”][alt-paths]<!-- ignore --> -osiossa Luvussa 7. Tämä tiedoston nimeäminen kertoo Rustille, ettei `common`-moduulia käsitellä integraatiotestitiedostona. Kun siirrämme `setup`-funktion koodin tiedostoon _tests/common/mod.rs_ ja poistamme tiedoston _tests/common.rs_, osio testitulosteessa ei enää näy. _tests_-hakemiston alihakemistojen tiedostoja ei käännetä erillisinä crateina eikä niille tule osioita testitulosteessa.

Kun olemme luoneet _tests/common/mod.rs_:n, voimme käyttää sitä mistä tahansa integraatiotestitiedostosta moduulina. Tässä on esimerkki `setup`-funktion kutsumisesta `it_adds_two`-testistä tiedostossa _tests/integration_test.rs_:

<span class="filename">Filename: tests/integration_test.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-13-fix-shared-test-code-problem/tests/integration_test.rs}}
```

Huomaa, että `mod common;`-määrittely on sama kuin moduulimäärittely, jonka demonstroimme Listauksessa 7-21. Sitten testifunktiossa voimme kutsua funktiota `common::setup()`.

#### Integraatiotestit binääricrateille

Jos projektimme on binääricrate, joka sisältää vain tiedoston _src/main.rs_ eikä tiedostoa _src/lib.rs_, emme voi luoda integraatiotestejä _tests_-hakemistoon ja tuoda _src/main.rs_:ssä määriteltyjä funktioita laajuuteen `use`-lausekkeella. Vain kirjastocratet paljastavat funktioita, joita muut cratet voivat käyttää; binääricratet on tarkoitettu ajettaviksi itsenäisesti.

Tämä on yksi syy siihen, miksi Rust-projektit, jotka tarjoavat binäärin, käyttävät yksinkertaista _src/main.rs_-tiedostoa, joka kutsuu logiikkaa, joka asuu _src/lib.rs_-tiedostossa. Tällä rakenteella integraatiotestit _voivat_ testata kirjastocratea `use`:lla tuoden tärkeän toiminnallisuuden saataville. Jos tärkeä toiminnallisuus toimii, pieni määrä koodia tiedostossa _src/main.rs_ toimii myös, eikä sitä pientä koodimäärää tarvitse testata.

## Yhteenveto

Rustin testausominaisuudet tarjoavat tavan määrittää, miten koodin pitäisi toimia varmistaaksesi, että se jatkaa toimimista odottamallasi tavalla, vaikka teet muutoksia. Yksikkötestit harjoittavat kirjaston eri osia erikseen ja voivat testata yksityisiä toteutustietoja. Integraatiotestit tarkistavat, että kirjaston monet osat toimivat yhdessä oikein, ja ne käyttävät kirjaston julkista API:a testatakseen koodin samalla tavalla kuin ulkoinen koodi käyttää sitä. Vaikka Rustin tyyppijärjestelmä ja omistussäännöt auttavat estämään joitakin virhetyyppejä, testit ovat silti tärkeitä vähentämään logiikkavirheitä, jotka liittyvät siihen, miten koodisi odotetaan käyttäytyvän.

Yhdistetään tässä luvussa ja aiemmissa luvuissa oppimasi tieto ja työskennellään projektin parissa!

[paths]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html
[separating-modules-into-files]: ch07-05-separating-modules-into-different-files.html
[alt-paths]: ch07-05-separating-modules-into-different-files.html#alternate-file-paths
