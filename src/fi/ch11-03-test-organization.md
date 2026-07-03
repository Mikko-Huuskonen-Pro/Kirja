## Testien organisointi

Kuten luvun alussa mainittiin, testaus on monimutkainen ala, ja eri ihmiset
käyttävät eri terminologiaa ja organisointia. Rust-yhteisö ajattelee testejä
kahden pääkategorian kautta: yksikkötestit ja integraatiotestit. _Yksikkötestit_
ovat pieniä ja keskittyneempiä, testaten yhtä moduulia erillään muusta koodista
kerrallaan, ja ne voivat testata yksityisiä rajapintoja. _Integraatiotestit_ ovat
täysin kirjastosi ulkopuolella ja käyttävät koodiasi samalla tavalla kuin
mikä tahansa muu ulkoinen koodi, käyttäen vain julkista rajapintaa ja
mahdollisesti testaten useita moduuleja per testi.

Molempien testityyppien kirjoittaminen on tärkeää varmistaaksesi, että
kirjastosi osat tekevät odottamasi asiat erikseen ja yhdessä.

### Yksikkötestit

Yksikkötestien tarkoitus on testata jokainen koodin yksikkö erillään muusta
koodista nopeasti paikantaakseen, missä koodi toimii ja missä ei odotetulla
tavalla. Laitat yksikkötestit _src_-hakemistoon kuhunkin tiedostoon sen koodin
kanssa, jota ne testaavat. Käytäntö on luoda `tests`-niminen moduuli kuhunkin
tiedostoon testifunktioiden säilyttämiseksi ja merkitä moduuli `cfg(test)`-
attribuutilla.

#### `tests`-moduuli ja `#[cfg(test)]`

`#[cfg(test)]`-merkintä `tests`-moduulissa kertoo Rustille kääntää ja ajaa
testikoodin vain, kun ajat `cargo test`, ei kun ajat `cargo build`. Tämä säästää
käännösaikaa, kun haluat vain rakentaa kirjaston, ja säästää tilaa syntyneessä
käännettyssä artefaktissa, koska testejä ei sisällytetä. Näet, että koska
integraatiotestit menevät eri hakemistoon, niillä ei tarvitse olla `#[cfg(test)]`-
merkintää. Koska yksikkötestit menevät samoihin tiedostoihin koodin kanssa,
käytät `#[cfg(test)]`:ää määrittääksesi, ettei niitä sisällytetä käännettyyn
tulokseen.

Muista, että kun loimme uuden `adder`-projektin tämän luvun ensimmäisessä
osiossa, Cargo loi meille tämän koodin:

<span class="filename">Filename: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-01/src/lib.rs}}
```

Automaattisesti luodussa `tests`-moduulissa `cfg`-attribuutti tarkoittaa
_konfiguraatiota_ (*configuration*) ja kertoo Rustille, että seuraava kohde
tulisi sisällyttää vain tietyn konfiguraatiovaihtoehdon ollessa voimassa. Tässä
tapauksessa konfiguraatiovaihtoehto on `test`, jonka Rust tarjoaa testien
kääntämiseen ja ajamiseen. Käyttämällä `cfg`-attribuuttia Cargo kääntää
testikoodimme vain, jos aktiivisesti ajamme testit `cargo test` -komennolla.
Tämä sisältää kaikki apufunktiot, jotka voivat olla tässä moduulissa, sekä
`#[test]`-merkityt funktiot.

<!-- Old headings. Do not remove or links may break. -->

<a id="testing-private-functions"></a>

#### Yksityisten funktioiden testaaminen

Testausyhteisössä on keskustelua siitä, pitäisikö yksityisiä funktioita testata
suoraan, ja muut kielet tekevät yksityisten funktioiden testaamisesta vaikeaa
tai mahdotonta. Riippumatta siitä, mihin testausideologiaan sitoudut, Rustin
näkyvyyssäännöt sallivat yksityisten funktioiden testaamisen. Harkitse listauksen
11-12 koodia yksityisellä `internal_adder`-funktiolla.

<Listing number="11-12" file-name="src/lib.rs" caption="Yksityisen funktion testaaminen">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-12/src/lib.rs}}
```

</Listing>

Huomaa, että `internal_adder`-funktiota ei ole merkitty `pub`-määritteellä.
Testit ovat vain Rust-koodia, ja `tests`-moduuli on vain toinen moduuli. Kuten
käsiteltiin osiossa [”Polut moduulipuun kohteeseen viittaamiseen”][paths]<!-- ignore -->,
lapsimoduulien kohteet voivat käyttää esi-isämoduuliensa kohteita. Tässä
testissä tuomme kaikki `tests`-moduulin vanhemman moduulin kohteet näkyviin
`use super::*` -lauseella, ja sitten testi voi kutsua `internal_adder`-funktiota.
Jos et mielestäsi yksityisiä funktioita pitäisi testata, Rustissa ei ole mitään,
mikä pakottaisi sinua tekemään niin.

### Integraatiotestit

Rustissa integraatiotestit ovat täysin kirjastosi ulkopuolella. Ne käyttävät
kirjastoasi samalla tavalla kuin mikä tahansa muu koodi, mikä tarkoittaa, että
ne voivat kutsua vain kirjastosi julkisen API:n funktioita. Niiden tarkoitus on
testata, toimivatko kirjastosi monet osat yhdessä oikein. Koodin yksiköt, jotka
toimivat oikein yksinään, voivat aiheuttaa ongelmia integroituna, joten
integroidun koodin testikattavuus on myös tärkeää. Luodaksesi integraatiotestejä
tarvitset ensin _tests_-hakemiston.

#### _tests_-hakemisto

Luomme _tests_-hakemiston projektihakemiston ylätasolle, _src_-hakemiston
viereen. Cargo tietää etsiä integraatiotestitiedostoja tästä hakemistosta.
Voimme sitten tehdä niin monta testitiedostoa kuin haluamme, ja Cargo kääntää
jokaisen tiedoston erillisenä cratena.

Luodaan integraatiotesti. Kun listauksen 11-12 koodi on vielä _src/lib.rs_-
tiedostossa, tee _tests_-hakemisto ja luo uusi tiedosto nimeltä
_tests/integration_test.rs_. Hakemistorakenteesi pitäisi näyttää tältä:

```text
adder
├── Cargo.lock
├── Cargo.toml
├── src
│   └── lib.rs
└── tests
    └── integration_test.rs
```

Syötä listauksen 11-13 koodi _tests/integration_test.rs_-tiedostoon.

<Listing number="11-13" file-name="tests/integration_test.rs" caption="Integraatiotesti `adder`-craten funktiolle">

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-13/tests/integration_test.rs}}
```

</Listing>

Jokainen tiedosto _tests_-hakemistossa on erillinen crate, joten meidän täytyy
tuoda kirjastomme kunkin testicraten näkyvyysalueelle. Siksi lisäämme `use
adder::add_two;` koodin alkuun, jota emme tarvinne yksikkötesteissä.

Emme tarvitse merkitä mitään koodia _tests/integration_test.rs_-tiedostossa
`#[cfg(test)]`-attribuutilla. Cargo käsittelee _tests_-hakemistoa erityisesti
ja kääntää tämän hakemiston tiedostot vain, kun ajamme `cargo test`. Aja
`cargo test` nyt:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-13/output.txt}}
```

Tulosteen kolme osiota sisältävät yksikkötestit, integraatiotestin ja
dokumentaatiotestit. Huomaa, että jos mikä tahansa testi osiossa epäonnistuu,
seuraavia osioita ei ajeta. Esimerkiksi jos yksikkötesti epäonnistuu, integraatio-
ja dokumentaatiotesteistä ei ole tulostetta, koska nämä testit ajetaan vain,
jos kaikki yksikkötestit läpäisevät.

Yksikkötestien ensimmäinen osio on sama kuin olemme nähneet: yksi rivi
kullekin yksikkötestille (yksi nimeltä `internal`, jonka lisäsimme listauksessa
11-12) ja sitten yhteenvetorivi yksikkötesteille.

Integraatiotestien osio alkaa rivillä `Running tests/integration_test.rs`.
Seuraavaksi on rivi kullekin integraatiotestin testifunktiolle ja
yhteenvetorivi integraatiotestin tuloksille juuri ennen kuin `Doc-tests adder`-
osio alkaa.

Jokaisella integraatiotestitiedostolla on oma osionsa, joten jos lisäämme
lisää tiedostoja _tests_-hakemistoon, tulee lisää integraatiotestien osioita.

Voimme silti ajaa tietyn integraatiotestifunktion määrittämällä testifunktion
nimen argumentiksi `cargo test` -komennolle. Ajaaaksesi kaikki testit tietyssä
integraatiotestitiedostossa, käytä `cargo test` -komennon `--test`-argumenttia
ja tiedoston nimeä:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-05-single-integration/output.txt}}
```

Tämä komento ajaa vain _tests/integration_test.rs_-tiedoston testit.

#### Alimodulit integraatiotesteissä

Kun lisäät integraatiotestejä, saatat haluta tehdä lisää tiedostoja _tests_-
hakemistoon järjestääksesi niitä; esimerkiksi voit ryhmitellä testifunktiot
sen toiminnallisuuden mukaan, jota ne testaavat. Kuten aiemmin mainittiin,
jokainen tiedosto _tests_-hakemistossa käännetään omana erillisenä cratenaan,
mikä on hyödyllistä erillisten näkyvyysalueiden luomiseen, jotka jäljittelevät
läheisemmin sitä, miten loppukäyttäjät käyttävät crateasi. Tämä tarkoittaa
kuitenkin, että _tests_-hakemiston tiedostot eivät jaa samaa käyttäytymistä
kuin _src_-hakemiston tiedostot, kuten opit luvussa 7 koodin jakamisesta
moduuleihin ja tiedostoihin.

_tests_-hakemiston tiedostojen erilainen käyttäytyminen näkyy selvimmin, kun
sinulla on joukko apufunktioita useissa integraatiotestitiedostoissa, ja yrität
seurata luvun 7 osion [”Moduulien erottaminen eri tiedostoihin”][separating-modules-into-files]<!-- ignore -->
vaiheita erottaaksesi ne yhteiseen moduuliin. Esimerkiksi jos luomme
_tests/common.rs_-tiedoston ja sijoitamme siihen `setup`-nimisen funktion,
voimme lisätä `setup`-funktioon koodia, jota haluamme kutsua useista testifunktioista
useissa testitiedostoissa:

<span class="filename">Filename: tests/common.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-12-shared-test-code-problem/tests/common.rs}}
```

Kun ajamme testit uudelleen, näemme uuden osion testitulosteessa _common.rs_-
tiedostolle, vaikka tässä tiedostossa ei ole testifunktioita eikä me kutsunut
`setup`-funktiota mistään:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-12-shared-test-code-problem/output.txt}}
```

`common`-näkyminen testituloksissa `running 0 tests` -tulosteella ei ole sitä,
mitä halusimme. Halusimme vain jakaa koodia muiden integraatiotestitiedostojen
kanssa. Välttääksemme `common`-näkymisen testitulosteessa, sen sijaan että
loisimme _tests/common.rs_-tiedoston, luomme _tests/common/mod.rs_-tiedoston.
Projektihakemisto näyttää nyt tältä:

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

Tämä on vanhempi nimeämiskäytäntö, jonka Rust myös ymmärtää ja josta mainittiin
luvun 7 osiossa [”Vaihtoehtoiset tiedostopolut”][alt-paths]<!-- ignore -->.
Tämän niminen tiedosto kertoo Rustille, ettei se käsittele `common`-moduulia
integraatiotestitiedostona. Kun siirrämme `setup`-funktion koodin
_tests/common/mod.rs_-tiedostoon ja poistamme _tests/common.rs_-tiedoston,
testitulosteen osio ei enää näy. _tests_-hakemiston alihakemistojen tiedostoja
ei käännetä erillisinä crateina eikä niillä ole osioita testitulosteessa.

Kun olemme luoneet _tests/common/mod.rs_-tiedoston, voimme käyttää sitä
miltä tahansa integraatiotestitiedostolta moduulina. Tässä on esimerkki
`setup`-funktion kutsumisesta `it_adds_two`-testistä _tests/integration_test.rs_-
tiedostossa:

<span class="filename">Filename: tests/integration_test.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-13-fix-shared-test-code-problem/tests/integration_test.rs}}
```

Huomaa, että `mod common;` -ilmoitus on sama kuin moduuli-ilmoitus, jonka
demonstroimme listauksessa 7-21. Sitten testifunktiossa voimme kutsua
`common::setup()`-funktiota.

#### Integraatiotestit binääricrateille

Jos projektimme on binääricrate, joka sisältää vain _src/main.rs_-tiedoston
eikä _src/lib.rs_-tiedostoa, emme voi luoda integraatiotestejä _tests_-
hakemistoon ja tuoda _src/main.rs_-tiedostossa määriteltyjä funktioita näkyviin
`use`-lauseella. Vain kirjastocratet paljastavat funktioita, joita muut cratet
voivat käyttää; binääricratet on tarkoitettu ajettaviksi itsenäisesti.

Tämä on yksi syy siihen, miksi Rust-projektit, jotka tarjoavat binäärin, käyttävät
suoraviivaista _src/main.rs_-tiedostoa, joka kutsuu logiikkaa, joka asuu
_src/lib.rs_-tiedostossa. Tällä rakenteella integraatiotestit _voivat_ testata
kirjastocratea `use`-lauseella tuodakseen tärkeän toiminnallisuuden näkyviin.
Jos tärkeä toiminnallisuus toimii, pieni määrä koodia _src/main.rs_-tiedostossa
toimii myös, eikä sitä pientä koodimäärää tarvitse testata.

## Yhteenveto

Rustin testausominaisuudet tarjoavat tavan määrittää, miten koodin pitäisi
toimia varmistaaksesi, että se jatkaa toimimista odottamallasi tavalla, vaikka
teet muutoksia. Yksikkötestit testaavat kirjaston eri osia erikseen ja voivat
testata yksityisiä toteutustietoja. Integraatiotestit tarkistavat, että
kirjaston monet osat toimivat yhdessä oikein, ja ne käyttävät kirjaston julkista
API:a testatakseen koodia samalla tavalla kuin ulkoinen koodi käyttää sitä.
Vaikka Rustin tyyppijärjestelmä ja omistajuussäännöt auttavat estämään
joitakin virhetyyppejä, testit ovat silti tärkeitä vähentämään logiikkavirheitä,
jotka liittyvät siihen, miten koodisi odotetaan käyttäytyvän.

Yhdistetään tässä luvussa ja aiemmissa luvuissa oppimasi tieto ja työskennellään
projektin parissa!

[paths]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html
[separating-modules-into-files]: ch07-05-separating-modules-into-different-files.html
[alt-paths]: ch07-05-separating-modules-into-different-files.html#alternate-file-paths
