## Tietotyypit

Jokainen Rustin arvo on tiettyä _tietotyyppiä_, mikä kertoo Rustille, millaista dataa määritetään,
jotta se tietää, kuinka näiden tietojen kanssa työskennellä. Tarkastellaan kahta tietotyyppien
alajoukkoa: skalaari ja yhdiste.

Muista, että Rust on _staattisesti tyypitetty_ kieli, mikä tarkoittaa, että sen täytyy tietää
kaikkien muuttujien tyypit käännösaikana. Kääntäjä voi yleensä päätellä, mitä tyyppiä haluamme
käyttää arvon ja sen käytön perusteella. Tilanteissa, joissa mahdollisia on useita tyyppejä,
kuten kun muunnimme `String`-tyypin numeeriseksi tyypiksi `parse`-metodilla
[”Arvauksen vertaaminen salaisuuteen”][comparing-the-guess-to-the-secret-number]<!-- ignore --> -osiossa
luvussa 2, meidän täytyy lisätä tyyppimäärittely, kuten tässä:

```rust
let guess: u32 = "42".parse().expect("Not a number!");
```

Jos emme lisää edellisessä koodissa näytettyä `: u32` -tyyppimäärittelyä, Rust näyttää seuraavan
virheen, mikä tarkoittaa, että kääntäjä tarvitsee meiltä lisätietoa sen selvittämiseksi, mitä
tyyppiä haluamme käyttää:

```console
{{#include ../listings/ch03-common-programming-concepts/output-only-01-no-type-annotations/output.txt}}
```

Näet erilaisia tyyppimäärittelyjä muille tietotyypeille.

### Skaalarityypit

_Skaalari_tyyppi edustaa yksittäistä arvoa. Rustissa on neljä pääasiallista skalaarityyppiä:
kokonaisluvut, liukuluvut, totuusarvot ja merkit. Saatat tunnistaa nämä muista
ohjelmointikielistä. Katsotaan, miten ne toimivat Rustissa.

#### Kokonaislukutyypit

_Kokonaisluku_ on luku ilman murto-osaa. Käytimme yhtä kokonaislukutyyppiä luvussa 2, `u32`-tyyppiä.
Tämä tyyppimäärittely osoittaa, että siihen liitetyn arvon tulisi olla etumerkitön kokonaisluku
(etumerkilliset kokonaislukutyypit alkavat kirjaimella `i` kirjaimen `u` sijaan), joka vie 32 bittiä
tilaa. Taulukko 3-1 näyttää Rustin sisäänrakennetut kokonaislukutyypit. Voimme käyttää mitä tahansa
näistä muunnelmista kokonaislukuarvon tyypin määrittämiseen.

<span class="caption">Taulukko 3-1: Kokonaislukutyypit Rustissa</span>

| Pituus  | Etumerkillinen | Etumerkitön |
| ------- | -------------- | ----------- |
| 8-bittinen   | `i8`    | `u8`     |
| 16-bittinen  | `i16`   | `u16`    |
| 32-bittinen  | `i32`   | `u32`    |
| 64-bittinen  | `i64`   | `u64`    |
| 128-bittinen | `i128`  | `u128`   |
| arch    | `isize` | `usize`  |

Jokainen muunnelma voi olla joko etumerkillinen tai etumerkitön ja sillä on eksplisiittinen koko.
_Etumerkillinen_ ja _etumerkitön_ viittaavat siihen, voiko luku olla negatiivinen — toisin sanoen,
tarvitseeko luvulla olla etumerkki (etumerkillinen) vai onko se aina positiivinen ja voidaan siten
esittää ilman etumerkkiä (etumerkitön). Se on kuin lukujen kirjoittamista paperille: kun etumerkillä
on merkitystä, luku näytetään plus- tai miinusmerkillä; kun on turvallista olettaa luvun olevan
positiivinen, sitä ei näytetä etumerkillä. Etumerkilliset luvut tallennetaan
[kahden komplementin][twos-complement]<!-- ignore --> esityksellä.

Jokainen etumerkillinen muunnelma voi tallentaa lukuja väliltä −(2<sup>n − 1</sup>) – 2<sup>n −
1</sup> − 1 mukaan lukien, missä _n_ on bittien määrä, joita kyseinen muunnelma käyttää. Eli `i8`
voi tallentaa lukuja väliltä −(2<sup>7</sup>) – 2<sup>7</sup> − 1, mikä vastaa −128 – 127.
Etumerkittömät muunnelmat voivat tallentaa lukuja väliltä 0 – 2<sup>n</sup> − 1, joten `u8` voi
tallentaa lukuja väliltä 0 – 2<sup>8</sup> − 1, mikä vastaa 0 – 255.

Lisäksi `isize`- ja `usize`-tyypit riippuvat tietokoneen arkkitehtuurista, jolla ohjelmasi
suoritetaan, mikä on merkitty taulukossa ”arch”: 64 bittiä 64-bittisellä arkkitehtuurilla ja
32 bittiä 32-bittisellä arkkitehtuurilla.

Voit kirjoittaa kokonaislukuliteraaleja missä tahansa taulukossa 3-2 näytetyssä muodossa. Huomaa,
että lukuliteraaleilla, jotka voivat olla useita numeerisia tyyppejä, voi olla tyyppipääte, kuten
`57u8`, tyypin määrittämiseksi. Lukuliteraalit voivat myös käyttää `_`-merkkiä visuaalisena
erottimena lukujen lukemisen helpottamiseksi, kuten `1_000`, jolla on sama arvo kuin `1000`:lla.

<span class="caption">Taulukko 3-2: Kokonaislukuliteraalit Rustissa</span>

| Lukuliteraalit  | Esimerkki       |
| --------------- | ------------- |
| Desimaali          | `98_222`      |
| Heksadesimaali              | `0xff`        |
| Oktaaliluku            | `0o77`        |
| Binääriluku           | `0b1111_0000` |
| Tavu (`u8` vain) | `b'A'`        |

Mistä siis tiedät, mitä kokonaislukutyyppiä käyttää? Jos et ole varma, Rustin oletukset ovat
yleensä hyvä lähtökohta: kokonaislukutyypit oletuksena ovat `i32`. Pääasiallinen tilanne, jossa
käyttäisit `isize`- tai `usize`-tyyppiä, on kun indeksoit jotakin kokoelmaa.

> ##### Kokonaisluvun ylivuoto
>
> Sanotaan, että sinulla on `u8`-tyyppinen muuttuja, joka voi sisältää arvoja väliltä 0 – 255.
> Jos yrität muuttaa muuttujan arvoksi jotakin tuon välin ulkopuolelta, kuten 256, tapahtuu
> _kokonaisluvun ylivuoto_, mikä voi johtaa kahteen eri käyttäytymiseen. Kun käännät debug-tilassa,
> Rust sisällyttää kokonaisluvun ylivuodon tarkistukset, jotka saavat ohjelman _panikoimaan_
> suorituksen aikana, jos tämä käyttäytyminen tapahtuu. Rust käyttää termiä _panikointi_, kun
> ohjelma päättyy virheeseen; käsittelemme paniikkeja tarkemmin
> [”Palautumattomat virheet `panic!`-makrolla”][unrecoverable-errors-with-panic]<!-- ignore --> -osiossa
> luvussa 9.
>
> Kun käännät release-tilassa `--release`-lipulla, Rust _ei_ sisällytä kokonaisluvun ylivuodon
> tarkistuksia, jotka aiheuttaisivat paniikin. Sen sijaan, jos ylivuoto tapahtuu, Rust suorittaa
> _kahden komplementin kiertämisen_. Lyhyesti sanottuna arvot, jotka ovat suurempia kuin tyypin
> suurin arvo, ”kiertyvät” tyypin pienimpään arvoon. `u8`-tyypin tapauksessa arvo 256 muuttuu
> arvoksi 0, arvo 257 muuttuu arvoksi 1 ja niin edelleen. Ohjelma ei panikoi, mutta muuttujalla on
> arvo, joka ei todennäköisesti ole se, mitä odotit. Ylivuodon kiertämiskäyttäytymiseen luottamista
> pidetään virheenä.
>
> Ylivuodon mahdollisuuden käsittelemiseksi eksplisiittisesti voit käyttää näitä primitiivisten
> numeeristen tyyppien vakiokirjaston tarjoamia metodiperheitä:
>
> - Kierrä kaikissa tiloissa `wrapping_*`-metodeilla, kuten `wrapping_add`.
> - Palauta `None`-arvo, jos ylivuoto tapahtuu, `checked_*`-metodeilla.
> - Palauta arvo ja totuusarvo, joka osoittaa, tapahtuiko ylivuoto, `overflowing_*`-metodeilla.
> - Rajoita arvon minimi- tai maksimiarvoihin `saturating_*`-metodeilla.

#### Liukulukutyypit

Rustissa on myös kaksi primitiivistä _liukulukutyyppiä_, jotka ovat lukuja desimaalipisteellä.
Rustin liukulukutyypit ovat `f32` ja `f64`, joiden koot ovat vastaavasti 32 ja 64 bittiä.
Oletustyyppi on `f64`, koska nykyaikaisilla suorittimilla se on suunnilleen yhtä nopea kuin `f32`,
mutta tarjoaa enemmän tarkkuutta. Kaikki liukulukutyypit ovat etumerkillisiä.

Tässä on esimerkki, joka näyttää liukuluvut käytössä:

<span class="filename">Tiedostonimi: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-06-floating-point/src/main.rs}}
```

Liukuluvut esitetään IEEE-754-standardin mukaisesti.

#### Numeeriset operaatiot

Rust tukee kaikkien lukutyyppien perusmatemaattisia operaatioita, joita voisit odottaa: yhteenlasku,
vähennyslasku, kertolasku, jakolasku ja jakojäännös. Kokonaislukujen jako katkaisee nollaa kohti
lähimpään kokonaislukuun. Seuraava koodi näyttää, miten käyttäisit kutakin numeerista operaatiota
`let`-lauseessa:

<span class="filename">Tiedostonimi: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-07-numeric-operations/src/main.rs}}
```

Jokainen näiden lauseiden lauseke käyttää matemaattista operaattoria ja evaluoituu yhdeksi arvoksi,
joka sidotaan sitten muuttujaan. [Liite B][appendix_b]<!-- ignore --> sisältää luettelon kaikista
Rustin tarjoamista operaattoreista.

#### Totuusarvotyyppi

Kuten useimmissa muissa ohjelmointikielissä, Rustin totuusarvotyypillä on kaksi mahdollista arvoa:
`true` ja `false`. Totuusarvot ovat yhden tavun kokoisia. Rustin totuusarvotyyppi määritellään
käyttämällä `bool`-tyyppiä. Esimerkiksi:

<span class="filename">Tiedostonimi: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-08-boolean/src/main.rs}}
```

Pääasiallinen tapa käyttää totuusarvoja on ehtolausekkeiden kautta, kuten `if`-lausekkeen.
Käsittelemme, miten `if`-lausekkeet toimivat Rustissa,
[”Ohjausrakenne”][control-flow]<!-- ignore --> -osiossa.

#### Merkkityyppi

Rustin `char`-tyyppi on kielen primitiivisin aakkosellinen tyyppi. Tässä on esimerkkejä `char`-arvojen
määrittämisestä:

<span class="filename">Tiedostonimi: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-09-char/src/main.rs}}
```

Huomaa, että määritämme `char`-literaalit yksinkertaisilla heittomerkeillä, toisin kuin
merkkijonoliteraalit, jotka käyttävät kaksinkertaisia heittomerkkejä. Rustin `char`-tyyppi on neljän
tavun kokoinen ja edustaa Unicode-skaalaariarvoa, mikä tarkoittaa, että se voi edustaa paljon
enemmän kuin pelkkää ASCIIa. Aksenttimerkit; kiina-, japani- ja koreankieliset merkit; emojit; ja
nollaleveyden välilyönnit ovat kaikki kelvollisia `char`-arvoja Rustissa. Unicode-skaalaariarvot
vaihtelevat välillä `U+0000` – `U+D7FF` ja `U+E000` – `U+10FFFF` mukaan lukien. ”Merkki” ei
kuitenkaan ole oikeastaan käsite Unicodeissa, joten inhimillinen intuitiosi siitä, mikä on ”merkki”,
ei välttämättä vastaa sitä, mikä on `char` Rustissa. Käsittelemme tätä aihetta tarkemmin
[”UTF-8-koodatun tekstin tallentaminen merkkijonoilla”][strings]<!-- ignore --> -osiossa luvussa 8.

### Yhdistetyt tyypit

_Yhdistetyt tyypit_ voivat ryhmitellä useita arvoja yhdeksi tyypiksi. Rustissa on kaksi
primitiivistä yhdistettyä tyyppiä: tuplet ja taulukot.

#### Tuplet-tyyppi

_Tuplet_ on yleinen tapa ryhmitellä useita eri tyyppisiä arvoja yhdeksi yhdistetyksi tyypiksi.
Tupletilla on kiinteä pituus: kun se on määritelty, sen kokoa ei voi kasvattaa tai pienentää.

Luomme tupletin kirjoittamalla pilkuilla erotetun luettelon arvoista sulkeiden sisään. Jokaisella
tupletin paikalla on tyyppi, eivätkä tupletin eri arvojen tyypit tarvitse olla samoja. Olemme
lisänneet valinnaiset tyyppimäärittelyt tähän esimerkkiin:

<span class="filename">Tiedostonimi: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-10-tuples/src/main.rs}}
```

Muuttuja `tup` sitoo koko tupletin, koska tupletia pidetään yhtenä yhdistettynä elementtinä.
Saadaksemme yksittäiset arvot ulos tupletista voimme käyttää kuvioiden täsmäystä tupletin arvon
purkamiseen, kuten tässä:

<span class="filename">Tiedostonimi: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-11-destructuring-tuples/src/main.rs}}
```

Tämä ohjelma luo ensin tupletin ja sitoo sen muuttujaan `tup`. Se käyttää sitten kuviota `let`-lauseen
kanssa ottaakseen `tup`:n ja muuttaakseen sen kolmeksi erilliseksi muuttujaksi, `x`:ksi, `y`:ksi ja
`z`:ksi. Tätä kutsutaan _purkamiseksi_, koska se jakaa yhden tupletin kolmeen osaan. Lopuksi ohjelma
tulostaa `y`:n arvon, joka on `6.4`.

Voimme myös käyttää tupletin elementtiin suoraan pisteen (`.`) ja sen jälkeen haluamamme arvon
indeksin avulla. Esimerkiksi:

<span class="filename">Tiedostonimi: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-12-tuple-indexing/src/main.rs}}
```

Tämä ohjelma luo tupletin `x` ja käyttää sitten kutakin tupletin elementtiä niiden indeksien avulla.
Kuten useimmissa ohjelmointikielissä, tupletin ensimmäinen indeksi on 0.

Tupletilla, jolla ei ole arvoja, on erityinen nimi, _yksikkö_. Tämä arvo ja sen vastaava tyyppi
kirjoitetaan molemmat `()` ja edustavat tyhjää arvoa tai tyhjää paluutyyppiä. Lausekkeet palauttavat
implisiittisesti yksikköarvon, jos ne eivät palauta mitään muuta arvoa.

#### Taulukkotyyppi

Toinen tapa kerätä useita arvoja on _taulukko_. Toisin kuin tupletissa, jokaisen taulukon elementin
täytyy olla samaa tyyppiä. Toisin kuin joissakin muissa kielissä, Rustin taulukoilla on kiinteä pituus.

Kirjoitamme taulukon arvot pilkuilla erotettuna luettelona hakasulkeiden sisään:

<span class="filename">Tiedostonimi: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-13-arrays/src/main.rs}}
```

Taulukot ovat hyödyllisiä, kun haluat datasi allokoitavan pinolle, kuten muutkin tähän asti
näkemämme tyypit, eikä keolle (käsittelemme pinon ja keon tarkemmin
[luvussa 4][stack-and-heap]<!-- ignore -->) tai kun haluat varmistaa, että sinulla on aina kiinteä
määrä elementtejä. Taulukko ei kuitenkaan ole yhtä joustava kuin vektorityyppi. _Vektori_ on
vakiokirjaston tarjoama vastaava kokoelmatyyppi, jonka kokoa _saa_ kasvattaa tai pienentää. Jos et
ole varma, käytätkö taulukkoa vai vektoria, todennäköisesti sinun kannattaa käyttää vektoria.
[Luku 8][vectors]<!-- ignore --> käsittelee vektoreita tarkemmin.

Taulukot ovat kuitenkin hyödyllisempiä, kun tiedät, ettei elementtien määrän tarvitse muuttua.
Esimerkiksi jos käyttäisit kuukausien nimiä ohjelmassa, käyttäisit todennäköisesti taulukkoa
vektorin sijaan, koska tiedät sen sisältävän aina 12 elementtiä:

```rust
let months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"];
```

Kirjoitat taulukon tyypin käyttämällä hakasulkeita, joiden sisällä on kunkin elementin tyyppi,
puolipiste ja sitten elementtien määrä taulukossa, näin:

```rust
let a: [i32; 5] = [1, 2, 3, 4, 5];
```

Tässä `i32` on kunkin elementin tyyppi. Puolipisteen jälkeen luku `5` osoittaa, että taulukko
sisältää viisi elementtiä.

Voit myös alustaa taulukon sisältämään saman arvon jokaiselle elementille määrittämällä alkuarvon,
jonka jälkeen on puolipiste ja sitten taulukon pituus hakasulkeissa, kuten tässä näytetään:

```rust
let a = [3; 5];
```

Taulukko nimeltä `a` sisältää `5` elementtiä, jotka kaikki asetetaan aluksi arvoon `3`. Tämä vastaa
kirjoittamista `let a = [3, 3, 3, 3, 3];`, mutta tiiviimmässä muodossa.

##### Taulukon elementtien käyttö

Taulukko on yksi tunnetun, kiinteän kokoinen muistilohko, joka voidaan allokoida pinolle. Voit
käyttää taulukon elementtejä indeksoinnilla, kuten tässä:

<span class="filename">Tiedostonimi: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-14-array-indexing/src/main.rs}}
```

Tässä esimerkissä muuttuja nimeltä `first` saa arvon `1`, koska se on taulukon indeksin `[0]` arvo.
Muuttuja nimeltä `second` saa arvon `2` taulukon indeksistä `[1]`.

##### Virheellinen taulukon elementin käyttö

Katsotaan, mitä tapahtuu, jos yrität käyttää taulukon elementtiä, joka on taulukon lopun jälkeen.
Sanotaan, että suoritat tämän koodin, joka on samanlainen kuin arvauspeli luvussa 2, saadaksesi
taulukon indeksin käyttäjältä:

<span class="filename">Tiedostonimi: src/main.rs</span>

```rust,ignore,panics
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-15-invalid-array-access/src/main.rs}}
```

Tämä koodi kääntyy onnistuneesti. Jos suoritat tämän koodin komennolla `cargo run` ja syötät `0`,
`1`, `2`, `3` tai `4`, ohjelma tulostaa vastaavan arvon kyseisestä taulukon indeksistä. Jos sen
sijaan syötät luvun taulukon lopun jälkeen, kuten `10`, näet tulosteen, joka näyttää tältä:

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

Ohjelma johti _suoritusaikaisen_ virheen indeksointiin virheellisen arvon käytön kohdalla. Ohjelma
päättyi virheilmoitukseen eikä suorittanut viimeistä `println!`-lausetta. Kun yrität käyttää
elementtiä indeksoinnilla, Rust tarkistaa, että määrittämäsi indeksi on pienempi kuin taulukon
pituus. Jos indeksi on suurempi tai yhtä suuri kuin pituus, Rust panikoi. Tämä tarkistus täytyy
tehdä suorituksen aikana, erityisesti tässä tapauksessa, koska kääntäjä ei voi mahdollisesti tietää,
minkä arvon käyttäjä syöttää, kun hän suorittaa koodin myöhemmin.

Tämä on esimerkki Rustin muistiturvallisuusperiaatteista käytännössä. Monissa matalan tason kielissä
tällaista tarkistusta ei tehdä, ja kun annat virheellisen indeksin, virheellistä muistia voidaan
käyttää. Rust suojaa sinua tältä virheeltä poistumalla välittömästi sen sijaan, että sallisi
muistin käytön ja jatkuisi. Luku 9 käsittelee lisää Rustin virheenkäsittelystä ja siitä, miten
voit kirjoittaa luettavaa, turvallista koodia, joka ei panikoi eikä salli virheellistä muistin käyttöä.

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[twos-complement]: https://en.wikipedia.org/wiki/Two%27s_complement
[control-flow]: ch03-05-control-flow.html#control-flow
[strings]: ch08-02-strings.html#storing-utf-8-encoded-text-with-strings
[stack-and-heap]: ch04-01-what-is-ownership.html#the-stack-and-the-heap
[vectors]: ch08-01-vectors.html
[unrecoverable-errors-with-panic]: ch09-01-unrecoverable-errors-with-panic.html
[appendix_b]: appendix-02-operators.md
