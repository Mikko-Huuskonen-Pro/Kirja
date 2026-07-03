## Testien kirjoittaminen

Testit ovat Rust-funktioita, jotka varmistavat, että ei-testikoodi toimii odotetulla tavalla.
Testifunktioiden rungot suorittavat tyypillisesti nämä kolme toimintoa:

- Tarvittavan datan tai tilan valmistelu.
- Testattavan koodin suorittaminen.
- Varmistus, että tulokset ovat odotetut.

Tarkastellaan ominaisuuksia, joita Rust tarjoaa erityisesti testien kirjoittamiseen ja jotka toteuttavat nämä toiminnot,
mukaan lukien `test`-attribuutti, muutama makro ja `should_panic`-attribuutti.

### Testifunktion rakenne

Yksinkertaisimmillaan testi Rustissa on funktio, joka on merkitty `test`-attribuutilla.
Attribuutit ovat metatietoa Rust-koodin osista; yksi esimerkki on `derive`-attribuutti, jota käytimme structeissa Luvussa 5.
Muuttaaksesi funktion testifunktioksi, lisää `#[test]` riville ennen `fn`:ää. Kun ajat testit `cargo test` -komennolla,
Rust rakentaa testiajaminen binäärin, joka suorittaa merkityt funktiot ja raportoi, läpäiseekö kukin testifunktio vai epäonnistuuko se.

Aina kun luomme uuden kirjastoprojektin Cargolla, testimoduuli testifunktiolla luodaan automaattisesti puolestamme.
Tämä moduuli antaa mallipohjan testien kirjoittamiseen, joten sinun ei tarvitse etsiä tarkkaa rakennetta ja syntaksia
joka kerta, kun aloitat uuden projektin. Voit lisätä niin monta lisätestifunktiota ja testimoduulia kuin haluat!

Tutkimme testien toiminnan joitakin näkökohtia kokeilemalla mallipohjatestiä ennen kuin testaamme varsinaista koodia.
Sitten kirjoitamme joitakin tosielämän testejä, jotka kutsuvat kirjoittamaamme koodia ja varmistavat sen käyttäytymisen.

Luodaan uusi kirjastoprojekti nimeltä `adder`, joka laskee kaksi lukua yhteen:

```console
$ cargo new adder --lib
     Created library `adder` project
$ cd adder
```

`adder`-kirjaston _src/lib.rs_-tiedoston sisällön pitäisi näyttää Listaukselta 11-1.

<Listing number="11-1" file-name="src/lib.rs" caption="`cargo new` -komennon automaattisesti luoma koodi">

<!-- manual-regeneration
cd listings/ch11-writing-automated-tests
rm -rf listing-11-01
cargo new listing-11-01 --lib --name adder
cd listing-11-01
echo "$ cargo test" > output.txt
RUSTFLAGS="-A unused_variables -A dead_code" RUST_TEST_THREADS=1 cargo test >> output.txt 2>&1
git diff output.txt # commit any relevant changes; discard irrelevant ones
cd ../../..
-->

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-01/src/lib.rs}}
```

</Listing>

Tiedosto alkaa esimerkki-`add`-funktiolla, jotta meillä on jotain testattavaa.

Keskitytään toistaiseksi pelkästään `it_works`-funktioon. Huomaa `#[test]`-annotaatio: tämä attribuutti ilmaisee,
että kyseessä on testifunktio, joten testiajaminen tietää käsitellä tätä funktiota testinä. `tests`-moduulissa voi olla
myös ei-testifunktioita yhteisten skenaarioiden valmisteluun tai yleisiin operaatioihin, joten meidän täytyy aina
ilmaista, mitkä funktiot ovat testejä.

Esimerkkifunktion runko käyttää `assert_eq!`-makroa varmistaakseen, että `result`, joka sisältää `add(2, 2)`-kutsun tuloksen, on yhtä suuri kuin 4.
Tämä varmistus toimii esimerkkinä tyypillisestä testin muodosta. Ajetaan se nähdäksemme, että testi läpäisee.

`cargo test` -komento ajaa kaikki projektin testit, kuten Listauksessa 11-2 näytetään.

<Listing number="11-2" caption="Automaattisesti luodun testin ajamisen tuloste">

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-01/output.txt}}
```

</Listing>

Cargo käänsi ja ajoi testin. Näemme rivin `running 1 test`. Seuraavalla rivillä näkyy luodun testifunktion nimi `tests::it_works`
ja sen ajamisen tulos `ok`. Yhteenveto `test result: ok.` tarkoittaa, että kaikki testit läpäisivät, ja osio `1 passed; 0 failed`
laskee läpäisseiden ja epäonnistuneiden testien määrän.

Testin voi merkitä ohitetuksi, jolloin sitä ei ajeta tietyssä tilanteessa; käsittelemme tämän myöhemmin tässä luvussa
[”Joidenkin testien ohittaminen, ellei niitä erikseen pyydetä”][ignoring]<!-- ignore --> -osiossa. Koska emme ole tehneet sitä tässä,
yhteenveto näyttää `0 ignored`. Voimme myös välittää argumentin `cargo test` -komennolle ajaaaksemme vain testit,
joiden nimi vastaa merkkijonoa; tätä kutsutaan _suodatukseksi_, ja käsittelemme sen
[”Testien osajoukon ajaminen nimen perusteella”][subset]<!-- ignore --> -osiossa. Tässä emme ole suodattaneet ajettavia testejä,
joten yhteenvedon lopussa näkyy `0 filtered out`.

Tilasto `0 measured` on suorituskykytesteille, jotka mittaavat suorituskykyä. Suorituskykytestit ovat kirjoitushetkellä
saatavilla vain yönightly-Rustissa. Katso [suorituskykytestien dokumentaatio][bench] oppiaksesi lisää.

Testitulosteen seuraava osa alkaen `Doc-tests adder` on dokumentaatiotestien tuloksille. Meillä ei ole vielä dokumentaatiotestejä,
mutta Rust voi kääntää API-dokumentaatiossamme esiintyvät koodiesimerkit. Tämä ominaisuus auttaa pitämään dokumentaation
ja koodin synkassa! Käsittelemme dokumentaatiotestien kirjoittamista Luvun 14
[”Dokumentaatiokommentit testeinä”][doc-comments]<!-- ignore --> -osiossa. Toistaiseksi ohitamme `Doc-tests`-tulosteen.

Aloitetaan testin mukauttaminen omiin tarpeisiimme. Muutetaan ensin `it_works`-funktion nimi erilaiseksi, kuten `exploration`, näin:

<span class="filename">Tiedostonimi: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-01-changing-test-name/src/lib.rs}}
```

Aja sitten `cargo test` uudelleen. Tulosteessa näkyy nyt `exploration` `it_works`-funktion sijaan:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-01-changing-test-name/output.txt}}
```

Lisätään nyt toinen testi, mutta tällä kertaa teemme testin, joka epäonnistuu! Testit epäonnistuvat, kun jokin testifunktiossa kaataa ohjelman.
Jokainen testi ajetaan uudessa säikeessä, ja kun pääsäie huomaa testisäikeen kuolleen, testi merkitään epäonnistuneeksi.
Luvussa 9 puhuimme siitä, että yksinkertaisin tapa kaataa ohjelma on kutsua `panic!`-makroa. Syötä uusi testi funktiona nimeltä `another`,
jolloin _src/lib.rs_-tiedostosi näyttää Listaukselta 11-3.

<Listing number="11-3" file-name="src/lib.rs" caption="Toisen testin lisääminen, joka epäonnistuu, koska kutsumme `panic!`-makroa">

```rust,panics,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-03/src/lib.rs}}
```

</Listing>

Aja testit uudelleen `cargo test` -komennolla. Tulosteen pitäisi näyttää Listaukselta 11-4, joka näyttää, että `exploration`-testi läpäisi ja `another` epäonnistui.

<Listing number="11-4" caption="Testitulokset, kun yksi testi läpäisee ja yksi epäonnistuu">

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-03/output.txt}}
```

</Listing>

<!-- manual-regeneration
rg panicked listings/ch11-writing-automated-tests/listing-11-03/output.txt
check the line number of the panic matches the line number in the following paragraph
 -->

`ok`-tekstin sijaan rivi `test tests::another` näyttää `FAILED`. Kaksi uutta osiota ilmestyy yksittäisten tulosten ja yhteenvedon väliin:
ensimmäinen näyttää yksityiskohtaisen syyn kunkin testin epäonnistumiselle. Tässä tapauksessa saamme tiedot, että `another` epäonnistui,
koska se `panicked at 'Make this test fail'` rivillä 17 _src/lib.rs_-tiedostossa. Seuraava osio listaa vain kaikkien epäonnistuneiden testien nimet,
mikä on hyödyllistä, kun testejä ja paljon yksityiskohtaista epäonnistumistulostetta on runsaasti. Voimme käyttää epäonnistuneen testin nimeä
ajaaaksemme vain kyseisen testin virheenkorjausta varten helpommin; puhumme lisää testien ajamisen tavoista
[”Testien ajamisen hallinta”][controlling-how-tests-are-run]<!-- ignore --> -osiossa.

Yhteenvetorivi näytetään lopussa: kaiken kaikkiaan testituloksemme on `FAILED`. Yksi testi läpäisi ja yksi epäonnistui.

Nyt kun olet nähnyt, miltä testitulokset näyttävät eri tilanteissa, tarkastellaan joitakin muita makroja kuin `panic!`, jotka ovat hyödyllisiä testeissä.

### Tulosten tarkistaminen `assert!`-makrolla

`assert!`-makro, jonka standardikirjasto tarjoaa, on hyödyllinen, kun haluat varmistaa, että jokin ehto testissä evaluoituu arvoksi `true`.
Annamme `assert!`-makrolle argumentin, joka evaluoituu totuusarvoksi. Jos arvo on `true`, mitään ei tapahdu ja testi läpäisee.
Jos arvo on `false`, `assert!`-makro kutsuu `panic!`-makroa aiheuttaakseen testin epäonnistumisen. `assert!`-makron käyttö auttaa
varmistamaan, että koodimme toimii tarkoittamallamme tavalla.

Luvun 5 Listauksessa 5-15 käytimme `Rectangle`-structia ja `can_hold`-metodia, jotka toistetaan tässä Listauksessa 11-5.
Laitetaan tämä koodi _src/lib.rs_-tiedostoon ja kirjoitetaan sille testejä `assert!`-makron avulla.

<Listing number="11-5" file-name="src/lib.rs" caption="`Rectangle`-struct ja sen `can_hold`-metodi Luvusta 5">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-05/src/lib.rs}}
```

</Listing>

`can_hold`-metodi palauttaa totuusarvon, joten se on täydellinen käyttötapaus `assert!`-makrolle.
Listauksessa 11-6 kirjoitamme testin, joka testaa `can_hold`-metodia luomalla `Rectangle`-instanssin,
jonka leveys on 8 ja korkeus 7, ja varmistamalla, että se voi sisältää toisen `Rectangle`-instanssin,
jonka leveys on 5 ja korkeus 1.

<Listing number="11-6" file-name="src/lib.rs" caption="Testi `can_hold`-metodille, joka tarkistaa, voiko suurempi suorakulmio todella sisältää pienemmän">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-06/src/lib.rs:here}}
```

</Listing>

Huomaa `use super::*;` -rivi `tests`-moduulin sisällä. `tests`-moduuli on tavallinen moduuli, joka noudattaa tavallisia
näkyvyyssääntöjä, joita käsittelimme Luvussa 7 [”Polut viittaamiseen moduulipuun kohteeseen”][paths-for-referring-to-an-item-in-the-module-tree]<!-- ignore -->
-osiossa. Koska `tests`-moduuli on sisämoduuli, meidän täytyy tuoda testattava koodi ulommassa moduulissa sisämoduulin näkyvyysalueelle.
Käytämme tässä globia, joten kaikki mitä määrittelemme ulommassa moduulissa on käytettävissä tälle `tests`-moduulille.

Olemme nimenneet testimme `larger_can_hold_smaller` ja luoneet kaksi tarvitsemaamme `Rectangle`-instanssia.
Sitten kutsuimme `assert!`-makroa ja välitimme sille `larger.can_hold(&smaller)`-kutsun tuloksen. Tämän lausekkeen pitäisi
palauttaa `true`, joten testimme pitäisi läpäistä. Katsotaan!

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-06/output.txt}}
```

Se läpäisee! Lisätään toinen testi, jossa varmistamme, ettei pienempi suorakulmio voi sisältää suurempaa suorakulmiota:

<span class="filename">Tiedostonimi: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-02-adding-another-rectangle-test/src/lib.rs:here}}
```

Koska `can_hold`-funktion oikea tulos tässä tapauksessa on `false`, meidän täytyy kääntää tuo tulos ennen kuin välitämme sen `assert!`-makrolle.
Näin testimme läpäisee, jos `can_hold` palauttaa `false`:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-02-adding-another-rectangle-test/output.txt}}
```

Kaksi testiä läpäisee! Katsotaan nyt, mitä testituloksille tapahtuu, kun tuomme bugin koodiimme. Muutamme `can_hold`-metodin toteutusta
korvaamalla suurempi-ku-merkin pienempi-ku-merkillä leveyksiä verrattaessa:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-03-introducing-a-bug/src/lib.rs:here}}
```

Testien ajaminen nyt tuottaa seuraavan:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-03-introducing-a-bug/output.txt}}
```

Testimme löysivät bugin! Koska `larger.width` on `8` ja `smaller.width` on `5`, leveyksien vertailu `can_hold`-metodissa palauttaa nyt `false`: 8 ei ole pienempi kuin 5.

### Yhtäsuuruuden testaaminen `assert_eq!`- ja `assert_ne!`-makroilla

Yleinen tapa varmistaa toiminnallisuus on testata testattavan koodin tuloksen ja odotetun paluuarvon yhtäsuuruus.
Voit tehdä tämän käyttämällä `assert!`-makroa ja välittämällä sille lausekkeen `==`-operaattorilla. Tämä on kuitenkin niin yleinen testi,
että standardikirjasto tarjoaa makroparin — `assert_eq!` ja `assert_ne!` — suorittamaan tämän testin kätevämmin.
Nämä makrot vertaavat kahta argumenttia yhtäsuuruuden tai erisuuruuden osalta. Ne myös tulostavat kaksi arvoa, jos varmistus epäonnistuu,
mikä helpottaa näkemään _miksi_ testi epäonnistui; päinvastoin `assert!`-makro ilmaisee vain, että se sai `false`-arvon `==`-lausekkeelle
tulostamatta arvoja, jotka johtivat `false`-arvoon.

Listauksessa 11-7 kirjoitamme funktion nimeltä `add_two`, joka lisää `2` parametriinsa, ja testaamme tämän funktion `assert_eq!`-makrolla.

<Listing number="11-7" file-name="src/lib.rs" caption="Funktion `add_two` testaaminen `assert_eq!`-makrolla">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-07/src/lib.rs}}
```

</Listing>

Tarkistetaan, että se läpäisee!

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-07/output.txt}}
```

Luomme muuttujan nimeltä `result`, joka sisältää `add_two(2)`-kutsun tuloksen. Sitten välitämme `result`-arvon ja `4`:n argumenteiksi `assert_eq!`-makrolle.
Tämän testin tulosrivi on `test tests::it_adds_two ... ok`, ja `ok`-teksti ilmaisee, että testimme läpäisi!

Tuodaan bugi koodiimme nähdäksemme, miltä `assert_eq!` näyttää epäonnistuessaan. Muutetaan `add_two`-funktion toteutus lisäämään `3` `2`:n sijaan:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-04-bug-in-add-two/src/lib.rs:here}}
```

Aja testit uudelleen:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-04-bug-in-add-two/output.txt}}
```

Testimme löysi bugin! `it_adds_two`-testi epäonnistui, ja viesti kertoo, että epäonnistunut varmistus oli ``assertion `left == right` failed``
ja mitkä `left`- ja `right`-arvot ovat. Tämä viesti auttaa aloittamaan virheenkorjauksen: `left`-argumentti, jossa oli `add_two(2)`-kutsun tulos, oli `5`,
mutta `right`-argumentti oli `4`. Voit kuvitella, että tästä olisi erityisen hyötyä, kun testejä on paljon.

Huomaa, että joissakin kielissä ja testikehyksissä yhtäsuuruusvarmistusfunktioiden parametreja kutsutaan `expected` ja `actual`,
ja argumenttien järjestyksellä on merkitystä. Rustissa niitä kutsutaan kuitenkin `left` ja `right`, eikä sillä, missä järjestyksessä määrittelemme
odotetun arvon ja koodin tuottaman arvon, ole merkitystä. Voisimme kirjoittaa tämän testin varmistuksen muodossa `assert_eq!(4, result)`,
mikä johtaisi samaan epäonnistumisviestiin, joka näyttää `` assertion failed: `(left == right)` ``.

`assert_ne!`-makro läpäisee, jos kaksi antamaamme arvoa eivät ole yhtä suuret, ja epäonnistuu, jos ne ovat. Tämä makro on hyödyllisin tapauksissa,
joissa emme ole varmoja, mikä arvo _tulee_ olemaan, mutta tiedämme, mikä arvo _ei ehdottomasti_ saa olla. Esimerkiksi jos testaamme funktiota,
joka muuttaa syötteensä taatusti jollain tavalla, mutta tapa, jolla syöte muuttuu, riippuu viikonpäivästä, jolloin ajamme testejä,
paras varmistus voi olla, että funktion tulos ei ole yhtä suuri kuin syöte.

Pinnan alla `assert_eq!`- ja `assert_ne!`-makrot käyttävät operaattoreita `==` ja `!=`. Kun varmistukset epäonnistuvat, nämä makrot tulostavat
argumenttinsa debug-muotoilulla, mikä tarkoittaa, että vertailtavien arvojen täytyy toteuttaa `PartialEq`- ja `Debug`-traitit.
Kaikki primitiivityypit ja useimmat standardikirjaston tyypit toteuttavat nämä traitit. Itse määrittelemillesi structeille ja enumeille
täytyy toteuttaa `PartialEq` varmistaaksesi näiden tyyppien yhtäsuuruuden. Täytyy myös toteuttaa `Debug` tulostaaksesi arvot, kun varmistus epäonnistuu.
Koska molemmat traitit ovat johdettavia traitteja, kuten mainittiin Luvun 5 Listauksessa 5-12, tämä on yleensä yhtä suoraviivaista
kuin `#[derive(PartialEq, Debug)]`-annotaation lisääminen struct- tai enum-määrittelyysi. Katso liite C,
[”Johdettavat traitit”][derivable-traits]<!-- ignore --> lisätietoja näistä ja muista johdettavista traiteista.

### Mukautettujen virheilmoitusten lisääminen

Voit myös lisätä mukautetun viestin, joka tulostetaan epäonnistumisviestin kanssa, valinnaisina argumentteina `assert!`-, `assert_eq!`- ja `assert_ne!`-makroille.
Kaikki pakollisten argumenttien jälkeen määritetyt argumentit välitetään `format!`-makrolle (käsiteltiin Luvun 8
[”Ketjutus `+`-operaattorilla tai `format!`-makrolla”][concatenation-with-the--operator-or-the-format-macro]<!-- ignore --> -osiossa),
joten voit välittää muotoilumerkkijonon, joka sisältää `{}`-paikkamerkit, ja arvot näihin paikkamerkkeihin. Mukautetut viestit ovat hyödyllisiä
dokumentoimaan, mitä varmistus tarkoittaa; kun testi epäonnistuu, sinulla on parempi käsitys siitä, mikä koodissa on vialla.

Esimerkiksi oletetaan, että meillä on funktio, joka tervehtii ihmisiä nimellä, ja haluamme testata, että funktiolle välitetty nimi näkyy tulosteessa:

<span class="filename">Tiedostonimi: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-05-greeter/src/lib.rs}}
```

Tämän ohjelman vaatimuksista ei ole vielä sovittu, ja olemme melko varmoja, että tervehdyksen alussa oleva `Hello`-teksti muuttuu.
Päätimme, ettei meidän tarvitse päivittää testiä vaatimusten muuttuessa, joten sen sijaan, että tarkistaisimme tarkkaa yhtäsuuruutta
`greeting`-funktion palauttamaan arvoon, varmistamme vain, että tuloste sisältää syöteparametrin tekstin.

Tuodaan nyt bugi tähän koodiin muuttamalla `greeting`-funktiota jättämään `name` pois nähdäksemme, miltä oletusarvoinen testin epäonnistuminen näyttää:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-06-greeter-with-bug/src/lib.rs:here}}
```

Tämän testin ajaminen tuottaa seuraavan:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-06-greeter-with-bug/output.txt}}
```

Tämä tulos ilmaisee vain, että varmistus epäonnistui ja millä rivillä varmistus on. Hyödyllisempi epäonnistumisviesti tulostaisi arvon
`greeting`-funktiosta. Lisätään mukautettu epäonnistumisviesti, joka koostuu muotoilumerkkijonosta paikkamerkillä, joka täytetään
`greeting`-funktiosta saadulla todellisella arvolla:

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-07-custom-failure-message/src/lib.rs:here}}
```

Nyt kun ajamme testin, saamme informatiivisemman virheilmoituksen:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-07-custom-failure-message/output.txt}}
```

Näemme testitulosteessa todellisen arvon, jonka saimme, mikä auttaa selvittämään, mitä tapahtui sen sijaan, mitä odotimme tapahtuvan.

### Kaatumisen tarkistaminen `should_panic`-attribuutilla

Paluuarvojen tarkistamisen lisäksi on tärkeää varmistaa, että koodimme käsittelee virhetilanteet odottamallamme tavalla.
Esimerkiksi tarkastele Luvun 9 Listauksessa 9-13 luomaamme `Guess`-tyyppiä. Muu koodi, joka käyttää `Guess`-tyyppiä,
luottaa siihen, että `Guess`-instanssit sisältävät vain arvoja välillä 1–100. Voimme kirjoittaa testin, joka varmistaa,
että `Guess`-instanssin luominen arvolla tuon alueen ulkopuolelta kaataa ohjelman.

Teemme tämän lisäämällä `should_panic`-attribuutin testifunktioomme. Testi läpäisee, jos funktion sisällä oleva koodi kaataa ohjelman;
testi epäonnistuu, jos funktion sisällä oleva koodi ei kaada ohjelmaa.

Listaus 11-8 näyttää testin, joka tarkistaa, että `Guess::new`-funktion virhetilanteet tapahtuvat odottamallamme tavalla.

<Listing number="11-8" file-name="src/lib.rs" caption="Testaus, että ehto aiheuttaa `panic!`-kutsun">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-08/src/lib.rs}}
```

</Listing>

Sijoitamme `#[should_panic]`-attribuutin `#[test]`-attribuutin jälkeen ja ennen sitä koskevaa testifunktiota. Katsotaan tulos, kun tämä testi läpäisee:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-08/output.txt}}
```

Näyttää hyvältä! Tuodaan nyt bugi koodiimme poistamalla ehto, jonka perusteella `new`-funktio kaataa ohjelman, jos arvo on suurempi kuin 100:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-08-guess-with-bug/src/lib.rs:here}}
```

Kun ajamme Listauksen 11-8 testin, se epäonnistuu:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-08-guess-with-bug/output.txt}}
```

Emme saa tässä tapauksessa kovin hyödyllistä viestiä, mutta kun katsomme testifunktiota, näemme että se on merkitty `#[should_panic]`-attribuutilla.
Saamamme epäonnistuminen tarkoittaa, että testifunktion koodi ei aiheuttanut kaatumista.

`should_panic`-attribuuttia käyttävät testit voivat olla epätarkkoja. `should_panic`-testi läpäisisi, vaikka testi kaatuisi eri syystä kuin odotimme.
Tehdäksemme `should_panic`-testeistä tarkempia, voimme lisätä valinnaisen `expected`-parametrin `should_panic`-attribuuttiin.
Testikehys varmistaa, että virheilmoitus sisältää annetun tekstin. Esimerkiksi tarkastele Listauksen 11-9 muokattua `Guess`-koodia,
jossa `new`-funktio kaataa ohjelman eri viesteillä riippuen siitä, onko arvo liian pieni vai liian suuri.

<Listing number="11-9" file-name="src/lib.rs" caption="Testaus `panic!`-kutsulle, jonka viesti sisältää määritellyn osamerkkijonon">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-09/src/lib.rs:here}}
```

</Listing>

Tämä testi läpäisee, koska arvo, jonka laitamme `should_panic`-attribuutin `expected`-parametriin, on osamerkkijono viestistä,
jonka kanssa `Guess::new`-funktio kaataa ohjelman. Olisimme voineet määrittää koko odottamamme kaatumisviestin,
joka tässä tapauksessa olisi `Guess value must be less than or equal to 100, got 200`. Mitä määrität, riippuu siitä,
kuinka ainutlaatuinen tai dynaaminen kaatumisviesti on ja kuinka tarkka haluat testisi olevan. Tässä tapauksessa
kaatumisviestin osamerkkijono riittää varmistamaan, että testifunktion koodi suorittaa `else if value > 100` -haaran.

Nähdäksemme, mitä tapahtuu, kun `should_panic`-testi `expected`-viestillä epäonnistuu, tuodaan taas bugi koodiimme vaihtamalla
`if value < 1` - ja `else if value > 100` -lohkojen rungot:

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-09-guess-with-panic-msg-bug/src/lib.rs:here}}
```

Tällä kertaa kun ajamme `should_panic`-testin, se epäonnistuu:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-09-guess-with-panic-msg-bug/output.txt}}
```

Epäonnistumisviesti ilmaisee, että tämä testi todella kaatoi ohjelman odottamallamme tavalla, mutta kaatumisviesti ei sisältänyt
odotettua merkkijonoa `less than or equal to 100`. Saamamme kaatumisviesti oli `Guess value must be greater than or equal to 1, got 200.`
Nyt voimme alkaa selvittää, missä bugimme on!

### `Result<T, E>`-tyypin käyttö testeissä

Testimme tähän mennessä ovat kaikki kaatuneet epäonnistuessaan. Voimme myös kirjoittaa testejä, jotka käyttävät `Result<T, E>`-tyyppiä!
Tässä on Listauksen 11-1 testi uudelleenkirjoitettuna käyttämään `Result<T, E>`-tyyppiä ja palauttamaan `Err` kaatumisen sijaan:

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-10-result-in-tests/src/lib.rs:here}}
```

`it_works`-funktiolla on nyt paluutyyppi `Result<(), String>`. Funktion rungossa `assert_eq!`-makron kutsumisen sijaan palautamme `Ok(())`,
kun testi läpäisee, ja `Err`-arvon, jonka sisällä on `String`, kun testi epäonnistuu.

Testien kirjoittaminen niin, että ne palauttavat `Result<T, E>`-tyypin, mahdollistaa kysymysmerkkioperaattorin käytön testien rungossa,
mikä voi olla kätevä tapa kirjoittaa testejä, joiden pitäisi epäonnistua, jos mikä tahansa niiden sisällä oleva operaatio palauttaa `Err`-variantin.

Et voi käyttää `#[should_panic]`-annotaatiota testeissä, jotka käyttävät `Result<T, E>`-tyyppiä. Varmistaaksesi, että operaatio palauttaa `Err`-variantin,
_älä_ käytä kysymysmerkkioperaattoria `Result<T, E>`-arvolla. Käytä sen sijaan `assert!(value.is_err())`.

Nyt kun tiedät useita tapoja kirjoittaa testejä, tarkastellaan, mitä tapahtuu testejä ajettaessa ja tutkitaan eri vaihtoehtoja, joita `cargo test` tarjoaa.

[concatenation-with-the--operator-or-the-format-macro]: ch08-02-strings.html#concatenation-with-the--operator-or-the-format-macro
[bench]: ../unstable-book/library-features/test.html
[ignoring]: ch11-02-running-tests.html#ignoring-some-tests-unless-specifically-requested
[subset]: ch11-02-running-tests.html#running-a-subset-of-tests-by-name
[controlling-how-tests-are-run]: ch11-02-running-tests.html#controlling-how-tests-are-run
[derivable-traits]: appendix-03-derivable-traits.html
[doc-comments]: ch14-02-publishing-to-crates-io.html#documentation-comments-as-tests
[paths-for-referring-to-an-item-in-the-module-tree]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html
