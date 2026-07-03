## Tietotyypit

Jokainen arvo Rustissa on tiettyä _tietotyyppiä_, joka kertoo Rustille, millaista dataa määritellään, jotta se tietää, miten datan kanssa työskennellään. Tarkastelemme kahta tietotyyppien osajoukkoa: skalaareja ja yhdistelmiä.

Muista, että Rust on _staattisesti tyypitetty_ kieli, mikä tarkoittaa, että sen täytyy tietää kaikkien muuttujien tyypit käännösaikana. Kääntäjä pystyy yleensä päättelemään, mitä tyyppiä haluamme käyttää arvon ja sen käytön perusteella. Tilanteissa, joissa useita tyyppejä on mahdollisia, kuten kun muunnimme `String`-tyypin numerotyypiksi `parse`-funktiolla ["Arvauksen vertaaminen salaisnumeroon"][comparing-the-guess-to-the-secret-number]<!-- ignore --> -osiossa Luvussa 2, meidän täytyy lisätä tyyppiannotaatio, kuten tässä:

```rust
let guess: u32 = "42".parse().expect("Not a number!");
```

Jos emme lisää edellä olevan koodin `: u32` -tyyppiannotaatiota, Rust näyttää seuraavan virheen, mikä tarkoittaa, että kääntäjä tarvitsee meiltä lisätietoa tietääkseen, mitä tyyppiä haluamme käyttää:

```console
{{#include ../listings/ch03-common-programming-concepts/output-only-01-no-type-annotations/output.txt}}
```

Näet erilaisia tyyppiannotaatioita muille tietotyypeille.

### Skalaarityypit

_Skalaari_-tyyppi edustaa yksittäistä arvoa. Rustissa on neljä pääasiallista skalaarityyppiä: kokonaisluvut, liukuluvut, totuusarvot ja merkit. Saatat tunnistaa nämä muista ohjelmointikielistä. Katsotaan, miten ne toimivat Rustissa.

#### Kokonaislukutyypit

_Kokonaisluku_ on luku ilman murto-osaa. Käytimme yhtä kokonaislukutyyppiä Luvussa 2, `u32`-tyyppiä. Tämä tyyppijulistus osoittaa, että siihen liitetyn arvon pitäisi olla etumerkitön kokonaisluku (etumerkityt kokonaislukutyypit alkavat `i`:llä `u`:n sijaan), joka vie 32 bittiä tilaa. Taulukko 3-1 näyttää Rustin sisäänrakennetut kokonaislukutyypit. Voimme käyttää mitä tahansa näistä muunnoksista kokonaislukuarvon tyypin julistamiseen.

<span class="caption">Taulukko 3-1: Kokonaislukutyypit Rustissa</span>

| Pituus  | Etumerkitty | Etumerkitön |
| ------- | ----------- | ----------- |
| 8-bittinen   | `i8`    | `u8`     |
| 16-bittinen  | `i16`   | `u16`    |
| 32-bittinen  | `i32`   | `u32`    |
| 64-bittinen  | `i64`   | `u64`    |
| 128-bittinen | `i128`  | `u128`   |
| Arkkitehtuurista riippuva | `isize` | `usize`  |

Jokainen muunnos voi olla joko etumerkitty tai etumerkitön ja sillä on eksplisiittinen koko.
_Etumerkitty_ ja _etumerkitön_ viittaavat siihen, voiko luku olla negatiivinen—toisin sanoen, tarvitseeko luvulla olla etumerkki (etumerkitty) vai onko se aina positiivinen ja voidaan siten esittää ilman etumerkkiä (etumerkitön). Se on kuin lukujen kirjoittaminen paperille: Kun etumerkillä on merkitystä, luku näytetään plus- tai miinusmerkillä; kun on turvallista olettaa luvun olevan positiivinen, sitä ei näytetä etumerkillä. Etumerkityt luvut tallennetaan [kahden komplementin][twos-complement]<!-- ignore --> esityksellä.

Jokainen etumerkitty muunnos voi tallentaa lukuja väliltä −(2<sup>n − 1</sup>) – 2<sup>n − 1</sup> − 1, missä _n_ on kyseisen muunnoksen käyttämien bittien määrä. Eli `i8` voi tallentaa lukuja −(2<sup>7</sup>) – 2<sup>7</sup> − 1, mikä vastaa −128 – 127. Etumerkittömät muunnokset voivat tallentaa lukuja 0 – 2<sup>n</sup> − 1, joten `u8` voi tallentaa lukuja 0 – 2<sup>8</sup> − 1, mikä vastaa 0 – 255.

Lisäksi `isize`- ja `usize`-tyypit riippuvat tietokoneen arkkitehtuurista, jolla ohjelmasi suoritetaan: 64 bittiä 64-bittisellä arkkitehtuurilla ja 32 bittiä 32-bittisellä arkkitehtuurilla.

Voit kirjoittaa kokonaislukuliteraaleja missä tahansa Taulukossa 3-2 näytetyssä muodossa. Huomaa, että lukuliteraaleilla, jotka voivat olla useita numeerisia tyyppejä, voi olla tyyppiliite, kuten `57u8`, tyypin määrittämiseksi. Lukuliteraalit voivat myös käyttää `_`-merkkiä visuaalisen erottimen roolissa lukujen lukemisen helpottamiseksi, kuten `1_000`, jolla on sama arvo kuin `1000`:lla.

<span class="caption">Taulukko 3-2: Kokonaislukuliteraalit Rustissa</span>

| Lukuliteraalit  | Esimerkki       |
| ---------------- | ------------- |
| Desimaali          | `98_222`      |
| Heksadesimaali              | `0xff`        |
| Oktaaliluku            | `0o77`        |
| Binääri           | `0b1111_0000` |
| Tavu (`u8` vain) | `b'A'`        |

Mistä siis tiedät, mitä kokonaislukutyyppiä käyttää? Jos et ole varma, Rustin oletusarvot ovat yleensä hyvä lähtökohta: Kokonaislukutyypit oletuksena `i32`. Pääasiallinen tilanne, jossa käyttäisit `isize`- tai `usize`-tyyppiä, on kun indeksoit jotakin kokoelmaa.

> ##### Kokonaisluvun ylivuoto
>
> Sanotaan, että sinulla on `u8`-tyyppinen muuttuja, joka voi pitää arvoja 0 – 255. Jos yrität muuttaa muuttujan arvoksi jotain tämän alueen ulkopuolelta, kuten 256, tapahtuu _kokonaisluvun ylivuoto_, mikä voi johtaa kahteen käyttäytymiseen. Kun käännetään debug-tilassa, Rust sisällyttää kokonaisluvun ylivuodon tarkistukset, jotka saavat ohjelmasi _panikoimaan_ ajonaikana, jos tämä tapahtuu. Rust käyttää termiä _panikointi_, kun ohjelma päättyy virheeseen; käsittelemme paniikkeja tarkemmin ["Palautumattomat virheet `panic!`-makrolla"][unrecoverable-errors-with-panic]<!-- ignore --> -osiossa Luvussa 9.
>
> Kun käännetään release-tilassa `--release`-lipulla, Rust _ei_ sisällytä kokonaisluvun ylivuodon tarkistuksia, jotka aiheuttavat paniikin. Sen sijaan, jos ylivuoto tapahtuu, Rust suorittaa _kahden komplementin kiertämisen_. Lyhyesti sanottuna tyypin maksimiarvoa suuremmat arvot "kiertyvät" tyypin vähimmäisarvoon. `u8`-tapauksessa arvo 256 muuttuu 0:ksi, arvo 257 muuttuu 1:ksi ja niin edelleen. Ohjelma ei panikoi, mutta muuttujalla on arvo, joka ei todennäköisesti ole se, mitä odotit. Kokonaisluvun ylivuodon kiertämiskäyttäytymiseen luottaminen katsotaan virheeksi.
>
> Käsitelläksesi ylivuodon mahdollisuuden eksplisiittisesti voit käyttää standardikirjaston tarjoamia metodiperheitä primitiivisille numeerisille tyypeille:
>
> - Kierrä kaikissa käännöstiloissa `wrapping_*`-metodeilla, kuten `wrapping_add`.
> - Palauta `None`-arvo, jos ylivuotoa tapahtuu `checked_*`-metodeilla.
> - Palauta arvo ja totuusarvo, joka osoittaa, tapahtuiko ylivuotoa `overflowing_*`-metodeilla.
> - Rajoita arvon minimi- tai maksimiarvoihin `saturating_*`-metodeilla.

#### Liukulukutyypit

Rustissa on myös kaksi primitiivistä _liukulukutyyppiä_, jotka ovat lukuja desimaalipisteellä. Rustin liukulukutyypit ovat `f32` ja `f64`, joiden koot ovat 32 ja 64 bittiä. Oletustyyppi on `f64`, koska nykyaikaisilla prosessoreilla se on suunnilleen yhtä nopea kuin `f32`, mutta tarjoaa enemmän tarkkuutta. Kaikki liukulukutyypit ovat etumerkittyjä.

Tässä on esimerkki liukuluvuista toiminnassa:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-06-floating-point/src/main.rs}}
```

Liukuluvut esitetään IEEE-754-standardin mukaisesti.

#### Numeeriset operaatiot

Rust tukee perusmatemaattisia operaatioita, joita odotat kaikille lukutyypeille: yhteenlasku, vähennyslasku, kertolasku, jakolasku ja jakojäännös. Kokonaislukujako katkaisee kohti nollaa lähimpään kokonaislukuun. Seuraava koodi näyttää, miten käyttäisit kutakin numeerista operaatiota `let`-lausekkeessa:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-07-numeric-operations/src/main.rs}}
```

Jokainen näiden lausekkeiden lauseke käyttää matemaattista operaattoria ja evaluoituu yhdeksi arvoksi, joka sidotaan sitten muuttujaan. [Liite B][appendix_b]<!-- ignore --> sisältää listan kaikista Rustin tarjoamista operaattoreista.

#### Totuusarvotyyppi

Kuten useimmissa muissa ohjelmointikielissä, totuusarvotyypillä Rustissa on kaksi mahdollista arvoa: `true` ja `false`. Totuusarvot ovat yhden tavun kokoisia. Rustin totuusarvotyyppi määritellään `bool`-avainsanalla. Esimerkiksi:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-08-boolean/src/main.rs}}
```

Pääasiallinen tapa käyttää totuusarvoja on ehtolausekkeiden kautta, kuten `if`-lauseke. Käsittelemme, miten `if`-lausekkeet toimivat Rustissa ["Ohjausrakenteet"][control-flow]<!-- ignore --> -osiossa.

#### Merkkityyppi

Rustin `char`-tyyppi on kielen primitiivisin aakkosellinen tyyppi. Tässä on esimerkkejä `char`-arvojen julistamisesta:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-09-char/src/main.rs}}
```

Huomaa, että määrittelemme `char`-literaalit yksinkertaisilla lainausmerkeillä toisin kuin
merkkijonoliteraalit, jotka käyttävät kaksinkertaisia lainausmerkkejä. Rustin `char`-tyyppi on
4 tavun kokoinen ja edustaa Unicode-skaalaariarvoa, mikä tarkoittaa, että se voi edustaa paljon
enemmän kuin pelkkää ASCII:a. Aksenttimerkit; kiina-, japani- ja koreankieliset merkit; emojit
ja nollaleveyden välilyönnit ovat kaikki kelvollisia `char`-arvoja Rustissa. Unicode-skaalaariarvot
ovat välillä `U+0000` – `U+D7FF` ja `U+E000` – `U+10FFFF`. Unicode:ssa "merkki" ei kuitenkaan
ole oikea käsite, joten intuitiosi siitä, mikä on "merkki", ei välttämättä vastaa sitä, mikä on
`char` Rustissa. Käsittelemme tämän aiheen tarkemmin ["UTF-8-koodatun tekstin tallentaminen merkkijonoilla"][strings]<!-- ignore --> -osiossa Luvussa 8.

### Yhdistelmätyypit

_Yhdistelmätyypit_ voivat ryhmitellä useita arvoja yhdeksi tyypiksi. Rustissa on kaksi primitiivistä yhdistelmätyyppiä: tuplat ja taulukot.

#### Tuplatyyppi

_Tupla_ on yleinen tapa ryhmitellä useita erityyppisiä arvoja yhdeksi yhdistelmätyypiksi. Tuplalla on kiinteä pituus: kun se on julistettu, se ei voi kasvaa tai kutistua.

Luomme tuplan kirjoittamalla pilkuilla erotetun listan arvoista sulkeiden sisään. Jokaisella paikalla tuplassa on tyyppi, eivätkä tuplan eri arvojen tyypit tarvitse olla samoja. Olemme lisänneet valinnaiset tyyppiannotaatiot tähän esimerkkiin:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-10-tuples/src/main.rs}}
```

Muuttuja `tup` sitoo koko tuplan, koska tuplaa pidetään yhtenä yhdistelmäelementtinä. Saadaksemme yksittäiset arvot tuplasta voimme käyttää kuvioiden täsmäyttämistä tuplan purkamiseen, näin:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-11-destructuring-tuples/src/main.rs}}
```

Tämä ohjelma luo ensin tuplan ja sitoo sen muuttujaan `tup`. Sitten se käyttää kuviota `let`-avainsanan kanssa ottaakseen `tup`:n ja muuttaakseen sen kolmeksi erilliseksi muuttujaksi, `x`, `y` ja `z`. Tätä kutsutaan _purkamiseksi_, koska se jakaa yhden tuplan kolmeen osaan. Lopuksi ohjelma tulostaa `y`:n arvon, joka on `6.4`.

Voimme myös käyttää tuplaelementtiä suoraan pisteellä (`.`) ja sen jälkeen sen arvon indeksillä, johon haluamme päästä. Esimerkiksi:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-12-tuple-indexing/src/main.rs}}
```

Tämä ohjelma luo tuplan `x` ja käyttää sitten kunkin tuplaelementin indeksiä. Kuten useimmissa ohjelmointikielissä, tuplan ensimmäinen indeksi on 0.

Tuplaa ilman arvoja kutsutaan erityisellä nimellä _yksikkö_. Tämä arvo ja sen vastaava tyyppi kirjoitetaan molemmat `()` ja edustavat tyhjää arvoa tai tyhjää paluutyyppiä. Lausekkeet palauttavat implisiittisesti yksikköarvon, jos ne eivät palauta mitään muuta arvoa.

#### Taulukkotyyppi

Toinen tapa kerätä useita arvoja on _taulukko_. Toisin kuin tuplassa, jokaisella taulukon elementillä täytyy olla sama tyyppi. Toisin kuin joissakin muissa kielissä, Rustin taulukoilla on kiinteä pituus.

Kirjoitamme taulukon arvot pilkuilla erotettuna listana hakasulkeiden sisään:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-13-arrays/src/main.rs}}
```

Taulukot ovat hyödyllisiä, kun haluat datasi allokoituvan pinolle, kuten muutkin tähän mennessä nähdyistä tyypeistä, eikä keolle (käsittelemme pinoa ja keon tarkemmin [Luvussa 4][stack-and-heap]<!-- ignore -->), tai kun haluat varmistaa, että sinulla on aina kiinteä määrä elementtejä. Taulukko ei kuitenkaan ole yhtä joustava kuin vektorityyppi. Vektori on standardikirjaston tarjoama samankaltainen kokoelmatyyppi, jonka koko _saa_ kasvaa tai kutistua, koska sen sisältö on keossa. Jos et ole varma, käytätkö taulukkoa vai vektoria, käytä todennäköisesti vektoria. [Luku 8][vectors]<!-- ignore --> käsittelee vektoreita tarkemmin.

Taulukot ovat kuitenkin hyödyllisempiä, kun tiedät, ettei elementtien määrän tarvitse muuttua. Esimerkiksi jos käyttäisit kuukausien nimiä ohjelmassa, käyttäisit todennäköisesti taulukkoa vektorin sijaan, koska tiedät sen sisältävän aina 12 elementtiä:

```rust
let months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"];
```

Kirjoitat taulukon tyypin hakasulkeilla, jokaisen elementin tyypillä, puolipisteellä ja sitten taulukon elementtien määrällä, näin:

```rust
let a: [i32; 5] = [1, 2, 3, 4, 5];
```

Tässä `i32` on kunkin elementin tyyppi. Puolipisteen jälkeen luku `5` osoittaa, että taulukko sisältää viisi elementtiä.

Voit myös alustaa taulukon sisältämään saman arvon jokaiselle elementille määrittämällä alkuarvon, sitten puolipisteen ja taulukon pituuden hakasulkeissa, kuten tässä:

```rust
let a = [3; 5];
```

`a`-niminen taulukko sisältää `5` elementtiä, jotka kaikki asetetaan aluksi arvoon `3`. Tämä on sama kuin kirjoittaisi `let a = [3, 3, 3, 3, 3];`, mutta tiiviimmällä tavalla.

<!-- Old headings. Do not remove or links may break. -->
<a id="accessing-array-elements"></a>

#### Taulukkoelementtien käyttö

Taulukko on yksi muistilohko tunnetulla, kiinteällä koolla, joka voidaan allokoida pinolle. Voit käyttää taulukon elementtejä indeksoinnilla, näin:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-14-array-indexing/src/main.rs}}
```

Tässä esimerkissä `first`-niminen muuttuja saa arvon `1`, koska se on taulukon indeksin `[0]` arvo. `second`-niminen muuttuja saa arvon `2` taulukon indeksistä `[1]`.

#### Virheellinen taulukkoelementin käyttö

Katsotaan, mitä tapahtuu, jos yrität käyttää taulukon elementtiä taulukon lopun jälkeen. Sanotaan, että suoritat tämän koodin, samankaltaisena kuin arvauspeli Luvussa 2, saadaksesi taulukon indeksin käyttäjältä:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,panics
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-15-invalid-array-access/src/main.rs}}
```

Tämä koodi kääntyy onnistuneesti. Jos suoritat tämän koodin `cargo run` -komennolla ja kirjoitat `0`, `1`, `2`, `3` tai `4`, ohjelma tulostaa vastaavan arvon taulukon kyseisessä indeksissä. Jos sen sijaan kirjoitat numeron taulukon lopun jälkeen, kuten `10`, näet tulosteen kuten tämä:

<!-- manual-regeneration
cd listings/ch03-common-programming-concepts/no-listing-15-invalid-array-access
cargo run
10
-->

```console
thread 'main' panicked at src/main.rs:19:19:
index out of bounds: the len is 5 but the index is 10
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

Ohjelma johti ajonaikaiseen virheeseen virheellisen arvon käytössä indeksointioperatiossa. Ohjelma päättyi virheilmoitukseen eikä suorittanut viimeistä `println!`-lausetta. Kun yrität käyttää elementtiä indeksoinnilla, Rust tarkistaa, että määrittämäsi indeksi on pienempi kuin taulukon pituus. Jos indeksi on suurempi tai yhtä suuri kuin pituus, Rust panikoi. Tämä tarkistus täytyy tehdä ajonaikana, erityisesti tässä tapauksessa, koska kääntäjä ei voi mahdollisesti tietää, minkä arvon käyttäjä kirjoittaa, kun hän suorittaa koodin myöhemmin.

Tämä on esimerkki Rustin muistiturvallisuusperiaatteista käytännössä. Monissa matalan tason kielissä tällaista tarkistusta ei tehdä, ja kun annat virheellisen indeksin, virheelliseen muistiin voidaan päästä. Rust suojaa sinua tämänkaltaiselta virheeltä poistumalla välittömästi sen sijaan, että sallisi muistin käytön ja jatkuisi. Luku 9 käsittelee lisää Rustin virheenkäsittelystä ja siitä, miten voit kirjoittaa luettavaa, turvallista koodia, joka ei panikoi eikä salli virheellistä muistin käyttöä.

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[twos-complement]: https://en.wikipedia.org/wiki/Two%27s_complement
[control-flow]: ch03-05-control-flow.html#control-flow
[strings]: ch08-02-strings.html#storing-utf-8-encoded-text-with-strings
[stack-and-heap]: ch04-01-what-is-ownership.html#the-stack-and-the-heap
[vectors]: ch08-01-vectors.html
[unrecoverable-errors-with-panic]: ch09-01-unrecoverable-errors-with-panic.html
[appendix_b]: appendix-02-operators.md
