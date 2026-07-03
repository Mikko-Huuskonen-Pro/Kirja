## Testien ajamisen hallinta

Aivan kuten `cargo run` kääntää koodisi ja ajaa syntyneen binääritiedoston,
`cargo test` kääntää koodisi testitilassa ja ajaa syntyneen testibinääritiedoston.
`cargo test` -komennon tuottaman binääritiedoston oletuskäyttäytyminen on ajaa
kaikki testit rinnakkain ja kaapata testien aikana syntynyt tuloste, estäen
tulosteen näyttämisen ja helpottaen testituloksiin liittyvän tulosteen lukemista.
Voit kuitenkin määrittää komentorivivalintoja muuttaaksesi tätä oletuskäyttäytymistä.

Jotkut komentorivivalinnat menevät `cargo test` -komennolle ja jotkut syntyneelle
testibinääritiedostolle. Erottaaksesi nämä kaksi argumenttityyppiä, listaa
`cargo test` -komennolle menevät argumentit, sitten erotin `--` ja sitten
testibinääritiedostolle menevät argumentit. `cargo test --help` näyttää valinnat,
joita voit käyttää `cargo test` -komennolla, ja `cargo test -- --help` näyttää
valinnat, joita voit käyttää erottimen jälkeen. Nämä valinnat on myös dokumentoitu
[_The `rustc` Book_ -kirjan osiossa ”Tests”][tests].

[tests]: https://doc.rust-lang.org/rustc/tests/index.html

### Testien ajaminen rinnakkain tai peräkkäin

Kun ajat useita testejä, ne ajetaan oletusarvoisesti rinnakkain säikeitä käyttäen,
mikä tarkoittaa, että ne valmistuvat nopeammin ja saat palautetta aikaisemmin.
Koska testit ajetaan samaan aikaan, sinun täytyy varmistaa, etteivät testisi
riipu toisistaan tai jaetusta tilasta, mukaan lukien jaettu ympäristö, kuten
nykyinen työhakemisto tai ympäristömuuttujat.

Esimerkiksi sanotaan, että jokainen testisi ajaa koodia, joka luo levylle
tiedoston nimeltä _test-output.txt_ ja kirjoittaa siihen dataa. Sitten jokainen
testi lukee tiedoston datan ja varmistaa, että tiedosto sisältää tietyn arvon,
joka on eri jokaisessa testissä. Koska testit ajetaan samaan aikaan, yksi testi
saattaa ylikirjoittaa tiedoston aikana, jolloin toinen testi kirjoittaa ja lukee
tiedostoa. Toinen testi epäonnistuu silloin, ei siksi että koodi olisi virheellinen,
vaan siksi että testit häiritsivät toisiaan ajettaessa rinnakkain. Yksi ratkaisu
on varmistaa, että jokainen testi kirjoittaa eri tiedostoon; toinen ratkaisu on
ajaa testit yksi kerrallaan.

Jos et halua ajaa testejä rinnakkain tai haluat tarkemman hallinnan käytettävien
säikeiden määrästä, voit lähettää `--test-threads`-lipun ja haluamasi säikeiden
määrän testibinääritiedostolle. Katso seuraava esimerkki:

```console
$ cargo test -- --test-threads=1
```

Asetamme testisäikeiden määräksi `1`, kertoen ohjelmalle, ettei se käytä
rinnakkaisuutta. Testien ajaminen yhdellä säikeellä kestää kauemmin kuin
rinnakkain, mutta testit eivät häiritse toisiaan, jos ne jakavat tilaa.

### Funktioiden tulosteen näyttäminen

Oletusarvoisesti, jos testi läpäisee, Rustin testikirjasto kaappaa kaiken
vakiotulosteeseen tulostetun. Esimerkiksi jos kutsumme `println!`:a testissä ja
testi läpäisee, emme näe `println!`-tulostetta terminaalissa; näemme vain rivin,
joka ilmaisee testin läpäisseen. Jos testi epäonnistuu, näemme kaiken
vakiotulosteeseen tulostetun epäonnistumisviestin mukana.

Esimerkkinä listauksessa 11-10 on hassu funktio, joka tulostaa parametriarvonsa
ja palauttaa 10, sekä testi, joka läpäisee, ja testi, joka epäonnistuu.

<Listing number="11-10" file-name="src/lib.rs" caption="Testit funktiolle, joka kutsuu `println!`-makroa">

```rust,panics,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-10/src/lib.rs}}
```

</Listing>

Kun ajamme nämä testit `cargo test` -komennolla, näemme seuraavan tulosteen:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-10/output.txt}}
```

Huomaa, ettei tässä tulosteessa missään näy `I got the value 4`, joka tulostetaan,
kun läpäisevä testi ajetaan. Tuo tuloste on kaapattu. Epäonnistuneen testin
tuloste `I got the value 8` näkyy testiyhteenvedon osiossa, joka näyttää myös
testin epäonnistumisen syyn.

Jos haluamme nähdä läpäisevien testien tulostetut arvot, voimme kertoa Rustille
näyttämään myös onnistuneiden testien tulosteen `--show-output`-lipulla:

```console
$ cargo test -- --show-output
```

Kun ajamme listauksen 11-10 testit uudelleen `--show-output`-lipulla, näemme
seuraavan tulosteen:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-01-show-output/output.txt}}
```

### Testien osajoukon ajaminen nimen perusteella

Koko testisarjan ajaminen voi joskus kestää kauan. Jos työskentelet tietyn alueen
koodin parissa, saatat haluta ajaa vain kyseiseen koodiin liittyvät testit. Voit
valita, mitkä testit ajetaan, antamalla `cargo test` -komennolle ajettavien
testien nimen tai nimet argumenttina.

Demonstroidaksemme, miten testien osajoukko ajetaan, luomme ensin kolme testiä
`add_two`-funktiollemme, kuten listauksessa 11-11, ja valitsemme, mitkä niistä
ajetaan.

<Listing number="11-11" file-name="src/lib.rs" caption="Kolme testiä kolmella eri nimellä">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-11/src/lib.rs}}
```

</Listing>

Jos ajamme testit antamatta argumentteja, kuten näimme aiemmin, kaikki testit
ajetaan rinnakkain:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-11/output.txt}}
```

#### Yksittäisten testien ajaminen

Voimme antaa `cargo test` -komennolle minkä tahansa testifunktion nimen ajaa
vain kyseisen testin:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-02-single-test/output.txt}}
```

Vain `one_hundred`-niminen testi ajettiin; kaksi muuta testiä ei vastannut
tätä nimeä. Testituloste kertoo, että meillä oli enemmän testejä, joita ei
ajettu, näyttämällä lopussa `2 filtered out`.

Emme voi määrittää useita testinimiä tällä tavalla; vain ensimmäistä `cargo
test` -komennolle annettua arvoa käytetään. Mutta on tapa ajaa useita testejä.

#### Suodatus useiden testien ajamiseen

Voimme määrittää osan testinimestä, ja jokainen testi, jonka nimi vastaa tätä
arvoa, ajetaan. Esimerkiksi koska kahden testimme nimi sisältää `add`, voimme
ajaa nämä kaksi ajamalla `cargo test add`:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-03-multiple-tests/output.txt}}
```

Tämä komento ajoi kaikki testit, joiden nimessä on `add`, ja suodatti pois
`one_hundred`-nimisen testin. Huomaa myös, että moduuli, jossa testi esiintyy,
tulee osaksi testin nimeä, joten voimme ajaa kaikki moduulin testit suodattamalla
moduulin nimen perusteella.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-some-tests-unless-specifically-requested"></a>

### Testien ohittaminen, ellei niitä erikseen pyydetä

Joskus muutama tietty testi voi olla hyvin aikaa vievä suorittaa, joten saatat
haluta jättää ne pois useimmista `cargo test` -ajoista. Sen sijaan, että
listaisit argumentteina kaikki testit, jotka haluat ajaa, voit merkitä aikaa
vievät testit `ignore`-attribuutilla poissulkemista varten, kuten tässä:

<span class="filename">Filename: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-11-ignore-a-test/src/lib.rs:here}}
```

`#[test]`-merkinnän jälkeen lisäämme `#[ignore]`-rivin testiin, jonka haluamme
jättää pois. Nyt kun ajamme testejämme, `it_works` ajetaan, mutta `expensive_test`
ei:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-11-ignore-a-test/output.txt}}
```

`expensive_test`-funktio on listattu `ignored`-tilassa. Jos haluamme ajaa vain
ohitetut testit, voimme käyttää `cargo test -- --ignored`:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-04-running-ignored/output.txt}}
```

Hallitsemalla, mitkä testit ajetaan, voit varmistaa, että `cargo test` -tulokset
palautuvat nopeasti. Kun olet siinä vaiheessa, että on järkevää tarkistaa
`ignored`-testien tulokset ja sinulla on aikaa odottaa tuloksia, voit ajaa
`cargo test -- --ignored` sen sijaan. Jos haluat ajaa kaikki testit riippumatta
siitä, ovatko ne ohitettuja vai eivät, voit ajaa `cargo test -- --include-ignored`.
