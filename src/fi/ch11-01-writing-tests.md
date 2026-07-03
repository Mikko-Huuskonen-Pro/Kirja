## Testien kirjoittaminen

_Testit_ ovat Rust-funktioita, jotka varmistavat, että ei-testikoodi toimii
odotetulla tavalla. Testifunktioiden rungot suorittavat tyypillisesti nämä kolme
toimintoa:

- Valmistele tarvittavat tiedot tai tila.
- Suorita testattava koodi.
- Varmista, että tulokset ovat odotetut.

Katsotaan Rustin tarjoamia ominaisuuksia erityisesti testien kirjoittamiseen,
jotka sisältävät nämä toiminnot: `test`-attribuutti, muutamia makroja ja
`should_panic`-attribuutin.

<!-- Old headings. Do not remove or links may break. -->

<a id="the-anatomy-of-a-test-function"></a>

### Testifunktioiden rakenne

Yksinkertaisimmillaan Rustin testi on funktio, joka on merkitty `test`-
attribuutilla. Attribuutit ovat metatietoa Rust-koodin osista; yksi esimerkki
on `derive`-attribuutti, jota käytimme structeissa luvussa 5. Muuttaaksesi
funktion testifunktioksi, lisää `#[test]` riville ennen `fn`:ää. Kun ajat
testisi `cargo test` -komennolla, Rust rakentaa testiajaminen binääritiedoston,
joka ajaa merkityt funktiot ja raportoi, läpäiseekö kukin testifunktio vai
epäonnistuuko se.

Aina kun luomme uuden kirjastoprojektin Cargolla, testimoduuli testifunktiolla
luodaan automaattisesti meille. Tämä moduuli antaa mallin testien kirjoittamiseen,
jotta sinun ei tarvitse etsiä tarkkaa rakennetta ja syntaksia joka kerta, kun
aloitat uuden projektin. Voit lisätä niin monta lisätestifunktiota ja
testimoduulia kuin haluat!

Tutkimme testien toiminnan eri puolia kokeilemalla mallitestiä ennen kuin
testaamme varsinaista koodia. Sitten kirjoitamme joitakin tosielämän testejä,
jotka kutsuvat kirjoittamaamme koodia ja varmistavat, että sen käyttäytyminen
on oikea.

Luodaan uusi kirjastoprojekti nimeltä `adder`, joka laskee yhteen kaksi lukua:

```console
$ cargo new adder --lib
     Created library `adder` project
$ cd adder
```

`adder`-kirjastosi _src/lib.rs_-tiedoston sisällön pitäisi näyttää listaukselta 11-1.

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

Toistaiseksi keskitytään pelkästään `it_works`-funktioon. Huomaa `#[test]`-
merkintä: Tämä attribuutti ilmaisee, että tämä on testifunktio, joten
testiajaminen tietää käsitellä tätä funktiota testinä. Meillä voi myös olla
ei-testifunktioita `tests`-moduulissa yhteisten skenaarioiden valmisteluun tai
yleisten operaatioiden suorittamiseen, joten meidän täytyy aina ilmaista,
mitkä funktiot ovat testejä.

Esimerkkifunktion runko käyttää `assert_eq!`-makroa varmistaakseen, että `result`,
joka sisältää `add`-funktion kutsun tuloksen arvoilla 2 ja 2, on yhtä suuri kuin 4.
Tämä varmistus toimii esimerkkinä tyypillisestä testin muodosta. Ajetaan se
nähdäksemme, että testi läpäisee.

`cargo test` -komento ajaa kaikki projektimme testit, kuten listauksessa 11-2.

<Listing number="11-2" caption="Automaattisesti luodun testin ajamisen tuloste">

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-01/output.txt}}
```

</Listing>

Cargo käänsi ja ajoi testin. Näemme rivin `running 1 test`. Seuraava rivi näyttää
luodun testifunktion nimen, nimeltä `tests::it_works`, ja että testin ajamisen
tulos on `ok`. Yhteenveto `test result: ok.` tarkoittaa, että kaikki testit
läpäisivät, ja osa `1 passed; 0 failed` laskee läpäisseiden tai epäonnistuneiden
testien määrän.

Testin voi merkitä ohitetuksi, jotta se ei aja tietyssä tilanteessa; käsittelemme
tämän luvun myöhemmässä osiossa [”Testien ohittaminen, ellei niitä erikseen
pyydetä”][ignoring]<!-- ignore -->. Koska emme ole tehneet sitä tässä, yhteenveto
näyttää `0 ignored`. Voimme myös antaa `cargo test` -komennolle argumentin ajaa
vain testit, joiden nimi vastaa merkkijonoa; tätä kutsutaan _suodatukseksi_
(*filtering*), ja käsittelemme sen osiossa [”Testien osajoukon ajaminen
nimen perusteella”][subset]<!-- ignore -->. Tässä emme ole suodattaneet ajettavia
testejä, joten yhteenvedon loppu näyttää `0 filtered out`.

`0 measured` -tilasto koskee suorituskykytestejä (*benchmark tests*). Tällä
hetkellä suorituskykytestit ovat saatavilla vain yönightly-Rustissa. Katso
[dokumentaatio suorituskykytesteistä][bench] saadaksesi lisätietoja.

Testitulosteen seuraava osa alkaen `Doc-tests adder` koskee dokumentaatiotestien
tuloksia. Meillä ei ole vielä dokumentaatiotestejä, mutta Rust voi kääntää
API-dokumentaatiossamme esiintyvät koodiesimerkit. Tämä ominaisuus auttaa
pitämään dokumentaation ja koodin synkassa! Käsittelemme dokumentaatiotestien
kirjoittamista luvun 14 osiossa [”Dokumentaatiokommentit
testeinä”][doc-comments]<!-- ignore -->. Toistaiseksi ohitamme `Doc-tests`-
tulosteen.

Aloitetaan testin mukauttaminen omiin tarpeisiimme. Ensin vaihdetaan `it_works`-
funktion nimi eri nimeksi, kuten `exploration`, näin:

<span class="filename">Filename: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-01-changing-test-name/src/lib.rs}}
```

Sitten ajetaan `cargo test` uudelleen. Tuloste näyttää nyt `exploration` `it_works`-
kohdan sijaan:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-01-changing-test-name/output.txt}}
```

Nyt lisätään toinen testi, mutta tällä kertaa tehdään testi, joka epäonnistuu!
Testit epäonnistuvat, kun jokin testifunktiossa paniikkiutuu. Jokainen testi
ajetaan uudessa säikeessä, ja kun pääsäie näkee testisäikeen kuolleen, testi
merkitään epäonnistuneeksi. Luvussa 9 puhuimme, että yksinkertaisin tapa
paniikkiutua on kutsua `panic!`-makroa. Syötä uusi testi funktiona nimeltä
`another`, jolloin _src/lib.rs_-tiedostosi näyttää listaukselta 11-3.

<Listing number="11-3" file-name="src/lib.rs" caption="Toisen testin lisääminen, joka epäonnistuu, koska kutsumme `panic!`-makroa">

```rust,panics,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-03/src/lib.rs}}
```

</Listing>

Aja testit uudelleen `cargo test` -komennolla. Tulosteen pitäisi näyttää
listaukselta 11-4, joka näyttää, että `exploration`-testimme läpäisi ja
`another` epäonnistui.

<Listing number="11-4" caption="Testitulokset, kun yksi testi läpäisee ja yksi epäonnistuu">

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-03/output.txt}}
```

</Listing>

<!-- manual-regeneration
rg panicked listings/ch11-writing-automated-tests/listing-11-03/output.txt
check the line number of the panic matches the line number in the following paragraph
 -->

`ok`-kohdan sijaan rivi `test tests::another` näyttää `FAILED`. Kaksi uutta
osiota ilmestyy yksittäisten tulosten ja yhteenvedon väliin: Ensimmäinen
näyttää yksityiskohtaisen syyn kunkin testin epäonnistumiselle. Tässä tapauksessa
saamme tiedot, että `tests::another` epäonnistui, koska se paniikkiutui
viestillä `Make this test fail` rivillä 17 _src/lib.rs_-tiedostossa. Seuraava
osio listaa vain kaikkien epäonnistuneiden testien nimet, mikä on hyödyllistä,
kun testejä ja paljon yksityiskohtaista epäonnistuneen testin tulostetta on
paljon. Voimme käyttää epäonnistuneen testin nimeä ajamaan vain kyseisen testin
debugataksemme sitä helpommin; puhumme lisää testien ajamisen tavoista osiossa
[”Testien ajamisen hallinta”][controlling-how-tests-are-run]<!-- ignore -->.

Yhteenvetorivi näkyy lopussa: Kaiken kaikkiaan testituloksemme on `FAILED`.
Yksi testi läpäisi ja yksi epäonnistui.

Nyt kun olet nähnyt, miltä testitulokset näyttävät eri skenaarioissa, katsotaan
joitakin muita makroja kuin `panic!`, jotka ovat hyödyllisiä testeissä.

<!-- Old headings. Do not remove or links may break. -->

<a id="checking-results-with-the-assert-macro"></a>

### Tulosten tarkistaminen `assert!`-makrolla

`assert!`-makro, jonka standardikirjasto tarjoaa, on hyödyllinen, kun haluat
varmistaa, että jokin ehto testissä evaluoituu arvoksi `true`. Annetaan
`assert!`-makrolle argumentti, joka evaluoituu totuusarvoksi. Jos arvo on
`true`, mitään ei tapahdu ja testi läpäisee. Jos arvo on `false`, `assert!`-
makro kutsuu `panic!`:a saadakseen testin epäonnistumaan. `assert!`-makron
käyttö auttaa meitä tarkistamaan, että koodimme toimii tarkoittamallamme tavalla.

Luvussa 5, listauksessa 5-15, käytimme `Rectangle`-structia ja `can_hold`-
metodia, jotka toistetaan tässä listauksessa 11-5. Laitetaan tämä koodi
_src/lib.rs_-tiedostoon ja kirjoitetaan sille testejä `assert!`-makron avulla.

<Listing number="11-5" file-name="src/lib.rs" caption="`Rectangle`-struct ja sen `can_hold`-metodi luvusta 5">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-05/src/lib.rs}}
```

</Listing>

`can_hold`-metodi palauttaa totuusarvon, mikä tekee siitä täydellisen
käyttötapauksen `assert!`-makrolle. Listauksessa 11-6 kirjoitamme testin, joka
testaa `can_hold`-metodia luomalla `Rectangle`-instanssin, jonka leveys on 8 ja
korkeus 7, ja varmistamalla, että se voi sisältää toisen `Rectangle`-instanssin,
jonka leveys on 5 ja korkeus 1.

<Listing number="11-6" file-name="src/lib.rs" caption="Testi `can_hold`-metodille, joka tarkistaa, voiko suurempi suorakulmio todella sisältää pienemmän">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-06/src/lib.rs:here}}
```

</Listing>

Huomaa `use super::*;` -rivi `tests`-moduulin sisällä. `tests`-moduuli on
tavallinen moduuli, joka noudattaa tavallisia näkyvyyssääntöjä, joita käsittelimme
luvussa 7 osiossa [”Polut moduulipuun kohteeseen viittaamiseen”][paths-for-referring-to-an-item-in-the-module-tree]<!-- ignore -->.
Koska `tests`-moduuli on sisämoduuli, meidän täytyy tuoda testattava koodi
ulommassa moduulissa sisämoduulin näkyvyysalueelle. Käytämme tässä globia,
joten kaikki ulommassa moduulissa määrittelemämme on käytettävissä tässä
`tests`-moduulissa.

Olemme nimenneet testimme `larger_can_hold_smaller`, ja olemme luoneet kaksi
tarvitsemaamme `Rectangle`-instanssia. Sitten kutsuimme `assert!`-makroa ja
annoimme sille lausekkeen `larger.can_hold(&smaller)`. Tämän lausekkeen pitäisi
palauttaa `true`, joten testimme pitäisi läpäistä. Katsotaan!

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-06/output.txt}}
```

Se läpäisee! Lisätään toinen testi, joka tällä kertaa varmistaa, ettei pienempi
suorakulmio voi sisältää suurempaa suorakulmiota:

<span class="filename">Filename: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-02-adding-another-rectangle-test/src/lib.rs:here}}
```

Koska `can_hold`-funktion oikea tulos tässä tapauksessa on `false`, meidän
täytyy kääntää tämä tulos ennen kuin annamme sen `assert!`-makrolle. Näin testimme
läpäisee, jos `can_hold` palauttaa `false`:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-02-adding-another-rectangle-test/output.txt}}
```

Kaksi testiä läpäisee! Katsotaan nyt, mitä testituloksille tapahtuu, kun
tuomme virheen koodiimme. Muutamme `can_hold`-metodin toteutusta korvaamalla
suurempi-kuin-merkin (`>`) pienempi-kuin-merkillä (`<`) leveyksiä vertailtaessa:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-03-introducing-a-bug/src/lib.rs:here}}
```

Testien ajaminen nyt tuottaa seuraavan:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-03-introducing-a-bug/output.txt}}
```

Testimme löysivät virheen! Koska `larger.width` on `8` ja `smaller.width` on `5`,
leveyksien vertailu `can_hold`-metodissa palauttaa nyt `false`: 8 ei ole pienempi
kuin 5.

<!-- Old headings. Do not remove or links may break. -->

<a id="testing-equality-with-the-assert_eq-and-assert_ne-macros"></a>

### Yhtäsuuruuden testaaminen `assert_eq!`- ja `assert_ne!`-makroilla

Yleinen tapa varmistaa toiminnallisuus on testata yhtäsuuruutta testattavan
koodin tuloksen ja odottamasi arvon välillä. Voit tehdä tämän `assert!`-makrolla
ja antamalla sille lausekkeen, joka käyttää `==`-operaattoria. Tämä on kuitenkin
niin yleinen testi, että standardikirjasto tarjoaa makroparin — `assert_eq!` ja
`assert_ne!` — suorittaakseen tämän testin kätevämmin. Nämä makrot vertaavat
kahta argumenttia yhtäsuuruuden tai erisuuruuden osalta. Ne myös tulostavat
kaksi arvoa, jos varmistus epäonnistuu, mikä helpottaa _miksi_ testi epäonnistui;
päinvastoin `assert!`-makro ilmaisee vain, että se sai `false`-arvon `==`-
lausekkeelle tulostamatta arvoja, jotka johtivat `false`-arvoon.

Listauksessa 11-7 kirjoitamme funktion nimeltä `add_two`, joka lisää `2`
parametriinsa, ja testaamme sitten tämän funktion `assert_eq!`-makrolla.

<Listing number="11-7" file-name="src/lib.rs" caption="Funktion `add_two` testaaminen `assert_eq!`-makrolla">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-07/src/lib.rs}}
```

</Listing>

Tarkistetaan, että se läpäisee!

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-07/output.txt}}
```

Luomme muuttujan nimeltä `result`, joka sisältää `add_two(2)`-kutsun tuloksen.
Sitten annamme `result`- ja `4`-arvot `assert_eq!`-makrolle. Tulostusrivi
tälle testille on `test tests::it_adds_two ... ok`, ja `ok`-teksti ilmaisee,
että testimme läpäisi!

Tuodaan virhe koodiimme nähdäksemme, miltä `assert_eq!` näyttää epäonnistuessaan.
Muutetaan `add_two`-funktion toteutus lisäämään `3` `2`:n sijaan:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-04-bug-in-add-two/src/lib.rs:here}}
```

Aja testit uudelleen:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-04-bug-in-add-two/output.txt}}
```

Testimme löysi virheen! `tests::it_adds_two` -testi epäonnistui, ja viesti
kertoo, että epäonnistunut varmistus oli `left == right` ja mitkä `left`- ja
`right`-arvot ovat. Tämä viesti auttaa aloittamaan debuggauksen: `left`-
argumentti, jossa meillä oli `add_two(2)`-kutsun tulos, oli `5`, mutta `right`-
argumentti oli `4`. Voit kuvitella, että tästä olisi erityisen hyötyä, kun
testejä on paljon.

Huomaa, että joissakin kielissä ja testikehyksissä yhtäsuuruusvarmistusten
funktioiden parametreja kutsutaan `expected`- ja `actual`-arvoiksi, ja
argumenttien järjestys on merkityksellinen. Rustissa niitä kutsutaan kuitenkin
`left`- ja `right`-arvoiksi, eikä sillä ole väliä, missä järjestyksessä
määrittelemme odottamamme arvon ja koodin tuottaman arvon. Voisimme kirjoittaa
testin varmistuksen muodossa `assert_eq!(4, result)`, mikä johtaisi samaan
epäonnistumisviestiin, joka näyttää `` assertion `left == right` failed ``.

`assert_ne!`-makro läpäisee, jos kaksi antamaamme arvoa eivät ole yhtä suuret,
ja epäonnistuu, jos ne ovat. Tämä makro on hyödyllisin tapauksissa, joissa emme
ole varmoja, mikä arvo _tulee_ olemaan, mutta tiedämme, mikä arvo _ei
todellakaan_ saa olla. Esimerkiksi jos testaamme funktiota, joka muuttaa
syötteensä jollakin tavalla, mutta tapa, jolla syöte muuttuu, riippuu viikonpäivästä,
jolloin ajamme testejämme, paras asia varmistaa saattaa olla, ettei funktion
tuloste ole yhtä suuri kuin syöte.

Pinnan alla `assert_eq!`- ja `assert_ne!`-makrot käyttävät operaattoreita `==`
ja `!=`. Kun varmistukset epäonnistuvat, nämä makrot tulostavat argumenttinsa
debug-muotoilulla, mikä tarkoittaa, että verrattavien arvojen täytyy toteuttaa
`PartialEq`- ja `Debug`-traitit. Kaikki primitiivityypit ja useimmat
standardikirjaston tyypit toteuttavat nämä traitit. Itse määrittelemillesi
structeille ja enum-arvoille sinun täytyy toteuttaa `PartialEq` varmistaaksesi
näiden tyyppien yhtäsuuruuden. Sinun täytyy myös toteuttaa `Debug` tulostaaksesi
arvot, kun varmistus epäonnistuu. Koska molemmat traitit ovat johdettavia
traitteja, kuten mainittiin listauksessa 5-12 luvussa 5, tämä on yleensä
yhtä suoraviivaista kuin `#[derive(PartialEq, Debug)]`-merkinnän lisääminen
struct- tai enum-määrittelyysi. Katso liite C, [”Johdettavat traitit”][derivable-traits]<!-- ignore -->
näistä ja muista johdettavista traiteista.

### Mukautettujen virheviestien lisääminen

Voit myös lisätä mukautetun viestin, joka tulostetaan epäonnistumisviestin
kanssa, valinnaisina argumentteina `assert!`-, `assert_eq!`- ja `assert_ne!`-
makroille. Pakollisten argumenttien jälkeen määritellyt argumentit välitetään
`format!`-makrolle (käsiteltiin luvussa 8 osiossa [”Yhdistäminen `+`- tai
`format!`-operaattorilla”][concatenating]<!-- ignore -->), joten voit antaa
muotoilumerkkijonon, joka sisältää `{}`-paikkamerkit ja arvot näihin
paikkamerkkeihin. Mukautetut viestit ovat hyödyllisiä dokumentoimaan, mitä
varmistus tarkoittaa; kun testi epäonnistuu, sinulla on parempi käsitys siitä,
mikä koodissa on vikana verrattuna siihen, mitä odotimme tapahtuvan.

Esimerkiksi sanotaan, että meillä on funktio, joka tervehtii ihmisiä nimellä,
ja haluamme testata, että funktiolle antamamme nimi näkyy tulosteessa:

<span class="filename">Filename: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-05-greeter/src/lib.rs}}
```

Tämän ohjelman vaatimuksista ei ole vielä sovittu, ja olemme melko varmoja,
että tervehdyksen alussa oleva `Hello`-teksti muuttuu. Päätimme, ettei meidän
haluta päivittää testiä, kun vaatimukset muuttuvat, joten tarkistamme tarkan
yhtäsuuruuden `greeting`-funktion palauttamaan arvoon sen sijaan, että
varmistaisimme vain, että tuloste sisältää syöteparametrin tekstin.

Tuodaan nyt virhe tähän koodiin muuttamalla `greeting` jättämään `name` pois
nähdäksemme, miltä oletusarvoinen testin epäonnistuminen näyttää:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-06-greeter-with-bug/src/lib.rs:here}}
```

Tämän testin ajaminen tuottaa seuraavan:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-06-greeter-with-bug/output.txt}}
```

Tämä tulos ilmaisee vain, että varmistus epäonnistui ja millä rivillä varmistus
on. Hyödyllisempi epäonnistumisviesti tulostaisi `greeting`-funktion arvon.
Lisätään mukautettu epäonnistumisviesti, joka koostuu muotoilumerkkijonosta
paikkamerkillä, joka täytetään todellisella arvolla, jonka saimme `greeting`-
funktiosta:

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-07-custom-failure-message/src/lib.rs:here}}
```

Nyt kun ajamme testin, saamme informatiivisemman virheviestin:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-07-custom-failure-message/output.txt}}
```

Näemme testitulosteessa todellisen arvon, jonka saimme, mikä auttaisi
debuggaamaan, mitä tapahtui sen sijaan, mitä odotimme tapahtuvan.

### Paniikin tarkistaminen `should_panic`-attribuutilla

Palautusarvojen tarkistamisen lisäksi on tärkeää tarkistaa, että koodimme
käsittelee virhetilanteet odottamallamme tavalla. Esimerkiksi harkitse
`Guess`-tyyppiä, jonka loimme luvussa 9, listauksessa 9-13. Muu koodi, joka
käyttää `Guess`-tyyppiä, luottaa takuuseen, että `Guess`-instanssit sisältävät
vain arvoja välillä 1–100. Voimme kirjoittaa testin, joka varmistaa, että
`Guess`-instanssin luominen arvolla tämän alueen ulkopuolelta paniikkiutuu.

Teemme tämän lisäämällä `should_panic`-attribuutin testifunktiollemme. Testi
läpäisee, jos funktion sisällä oleva koodi paniikkiutuu; testi epäonnistuu,
jos funktion sisällä oleva koodi ei paniikkiudu.

Listaus 11-8 näyttää testin, joka tarkistaa, että `Guess::new`-funktion
virhetilanteet tapahtuvat, kun odotamme niitä.

<Listing number="11-8" file-name="src/lib.rs" caption="Testaus, että ehto aiheuttaa `panic!`-kutsun">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-08/src/lib.rs}}
```

</Listing>

Sijoitamme `#[should_panic]`-attribuutin `#[test]`-attribuutin jälkeen ja
ennen testifunktiota, johon se kohdistuu. Katsotaan tulos, kun tämä testi
läpäisee:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-08/output.txt}}
```

Näyttää hyvältä! Tuodaan nyt virhe koodiimme poistamalla ehto, jonka perusteella
`new`-funktio paniikkiutuu, jos arvo on suurempi kuin 100:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-08-guess-with-bug/src/lib.rs:here}}
```

Kun ajamme listauksen 11-8 testin, se epäonnistuu:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-08-guess-with-bug/output.txt}}
```

Emme saa tässä tapauksessa kovin hyödyllistä viestiä, mutta kun katsomme
testifunktiota, näemme, että se on merkitty `#[should_panic]`-attribuutilla.
Saamamme epäonnistuminen tarkoittaa, että testifunktion koodi ei aiheuttanut
paniikkia.

`should_panic`-attribuuttia käyttävät testit voivat olla epätarkkoja.
`should_panic`-testi läpäisisi, vaikka testi paniikkiutuisi eri syystä kuin
odotimme. Tehdäksemme `should_panic`-testeistä tarkempia voimme lisätä valinnaisen
`expected`-parametrin `should_panic`-attribuuttiin. Testiajaminen varmistaa,
että epäonnistumisviesti sisältää annetun tekstin. Esimerkiksi harkitse
muokattua `Guess`-koodia listauksessa 11-9, jossa `new`-funktio paniikkiutuu
eri viesteillä riippuen siitä, onko arvo liian pieni vai liian suuri.

<Listing number="11-9" file-name="src/lib.rs" caption="Testaus `panic!`-kutsulle, jonka paniikkiviesti sisältää määritellyn osamerkkijonon">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-09/src/lib.rs:here}}
```

</Listing>

Tämä testi läpäisee, koska arvo, jonka laitamme `should_panic`-attribuutin
`expected`-parametriin, on osamerkkijono viestistä, jolla `Guess::new`-funktio
paniikkiutuu. Olisimme voineet määrittää koko odottamamme paniikkiviestin,
joka tässä tapauksessa olisi `Guess value must be less than or equal to 100,
got 200`. Mitä määrität riippuu siitä, kuinka uniikki tai dynaaminen paniikkiviesti
on ja kuinka tarkka haluat testisi olevan. Tässä tapauksessa paniikkiviestin
osamerkkijono riittää varmistamaan, että testifunktion koodi suorittaa
`else if value > 100` -tapauksen.

Nähdäksemme, mitä tapahtuu, kun `should_panic`-testi `expected`-viestillä
epäonnistuu, tuodaan taas virhe koodiimme vaihtamalla `if value < 1`- ja
`else if value > 100` -lohkojen rungot:

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-09-guess-with-panic-msg-bug/src/lib.rs:here}}
```

Tällä kertaa kun ajamme `should_panic`-testin, se epäonnistuu:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-09-guess-with-panic-msg-bug/output.txt}}
```

Epäonnistumisviesti ilmaisee, että tämä testi todellakin paniikkiutui kuten
odotimme, mutta paniikkiviesti ei sisältänyt odotettua merkkijonoa `less than
or equal to 100`. Paniikkiviesti, jonka saimme tässä tapauksessa, oli `Guess
value must be greater than or equal to 1, got 200`. Nyt voimme alkaa selvittää,
missä virheemme on!

### `Result<T, E>`-tyypin käyttö testeissä

Kaikki testimme tähän asti paniikkiutuvat epäonnistuessaan. Voimme myös kirjoittaa
testejä, jotka käyttävät `Result<T, E>`-tyyppiä! Tässä on testi listauksesta
11-1, kirjoitettu uudelleen käyttämään `Result<T, E>`-tyyppiä ja palauttamaan
`Err` paniikkiutumisen sijaan:

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-10-result-in-tests/src/lib.rs:here}}
```

`it_works`-funktiolla on nyt palautustyyppi `Result<(), String>`. Funktion
rungossa kutsumme `assert_eq!`-makron sijaan `Ok(())`, kun testi läpäisee, ja
`Err`-arvoa, jonka sisällä on `String`, kun testi epäonnistuu.

Testien kirjoittaminen niin, että ne palauttavat `Result<T, E>`-tyypin, mahdollistaa
kysymysmerkkioperaattorin käytön testien rungossa, mikä voi olla kätevä tapa
kirjoittaa testejä, joiden pitäisi epäonnistua, jos mikä tahansa operaatio
niiden sisällä palauttaa `Err`-variantin.

Et voi käyttää `#[should_panic]`-merkintää testeissä, jotka käyttävät
`Result<T, E>`-tyyppiä. Varmistaaksesi, että operaatio palauttaa `Err`-variantin,
_älä_ käytä kysymysmerkkioperaattoria `Result<T, E>`-arvolla. Sen sijaan käytä
`assert!(value.is_err())`.

Nyt kun tiedät useita tapoja kirjoittaa testejä, katsotaan, mitä tapahtuu, kun
ajamme testejämme, ja tutkitaan eri vaihtoehtoja, joita voimme käyttää `cargo
test` -komennolla.

[concatenating]: ch08-02-strings.html#concatenating-with--or-format
[bench]: ../unstable-book/library-features/test.html
[ignoring]: ch11-02-running-tests.html#ignoring-tests-unless-specifically-requested
[subset]: ch11-02-running-tests.html#running-a-subset-of-tests-by-name
[controlling-how-tests-are-run]: ch11-02-running-tests.html#controlling-how-tests-are-run
[derivable-traits]: appendix-03-derivable-traits.html
[doc-comments]: ch14-02-publishing-to-crates-io.html#documentation-comments-as-tests
[paths-for-referring-to-an-item-in-the-module-tree]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html
