# Arvauspelin ohjelmointi

Hypätään suoraan Rustin pariin työstämällä yhdessä käytännön projekti! Tämä
luku esittelee sinulle muutamia yleisiä Rust-käsitteitä näyttämällä, miten
voit käyttää niitä oikeassa ohjelmassa. Opit `let`-määrittelyistä, `match`-lausekkeista, metodeista, assosioiduista
funktioista, ulkoisista crateista ja paljon muusta! Seuraavissa luvuissa perehdymme
näihin ideoihin tarkemmin. Tässä luvussa harjoittelet vain
perusasioita.

Toteutamme klassisen aloittelijatason ohjelmointitehtävän: arvauspelin. Näin
se toimii: ohjelma generoi satunnaisen kokonaisluvun väliltä 1–100. Se
pyytää sitten pelaajaa syöttämään arvauksen. Kun arvaus on annettu,
ohjelma kertoo, onko arvaus liian pieni vai liian suuri. Jos arvaus on
oikein, peli tulostaa onnitteluviestin ja sulkeutuu.

## Uuden projektin luominen

Luo uusi projekti siirtymällä _projects_-hakemistoon, jonka loit
luvussa 1, ja luo uusi projekti käyttäen Cargoa näin:

```console
$ cargo new guessing_game
$ cd guessing_game
```

Ensimmäinen komento `cargo new` ottaa projektin nimen (`guessing_game`)
ensimmäisenä argumenttina. Toinen komento siirtyy uuden projektin
hakemistoon.

Tarkastele luotua _Cargo.toml_-tiedostoa:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial
rm -rf no-listing-01-cargo-new
cargo new no-listing-01-cargo-new --name guessing_game
cd no-listing-01-cargo-new
cargo run > output.txt 2>&1
cd ../../..
-->

<span class="filename">Filename: Cargo.toml</span>

```toml
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/Cargo.toml}}
```

Kuten näit luvussa 1, `cargo new` generoi sinulle ”Hello, world!” -ohjelman.
Tarkista _src/main.rs_-tiedosto:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/src/main.rs}}
```

Käännetään ja ajetaan nyt tämä ”Hello, world!” -ohjelma samassa vaiheessa
käyttämällä `cargo run` -komentoa:

```console
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/output.txt}}
```

`run`-komento on kätevä, kun täytyy nopeasti iteroida projektia,
kuten teemme tässä pelissä, testaten nopeasti jokaisen version ennen siirtymistä
seuraavaan.

Avaa _src/main.rs_-tiedosto uudelleen. Kirjoitat kaiken koodin tähän tiedostoon.

## Arvauksen käsittely

Arvauspeli-ohjelman ensimmäinen osa pyytää käyttäjän syötettä, käsittelee
sen ja tarkistaa, että syöte on odotetussa muodossa. Aloitamme
sallimalla pelaajan syöttää arvauksen. Syötä listauksen 2-1 koodi
tiedostoon _src/main.rs_.

<Listing number="2-1" file-name="src/main.rs" caption="Koodi, joka hakee arvauksen käyttäjältä ja tulostaa sen">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:all}}
```

</Listing>

Tämä koodi sisältää paljon tietoa, joten käydään se läpi rivi riviltä. Saadaksemme
käyttäjän syötteen ja tulostaaksemme tuloksen, meidän täytyy tuoda
`io`-kirjasto näkyviin. `io`-kirjasto tulee standardikirjastosta,
joka tunnetaan nimellä `std`:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:io}}
```

Oletuksena Rustilla on joukko kohteita, jotka on määritelty standardikirjastossa ja jotka se
tuo näkyviin jokaisessa ohjelmassa. Tätä joukkoa kutsutaan _preludiksi_, ja
voit nähdä kaiken siinä [standardikirjaston dokumentaatiossa][prelude].

Jos haluamasi tyyppi ei ole preludissa, sinun täytyy tuoda kyseinen tyyppi
näkyviin eksplisiittisesti `use`-lauseella. `std::io`-kirjaston käyttö
tarjoaa useita hyödyllisiä ominaisuuksia, mukaan lukien mahdollisuuden hyväksyä
käyttäjän syöte.

Kuten näit luvussa 1, `main`-funktio on ohjelman sisääntulopiste:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:main}}
```

`fn`-syntaksi julistaa uuden funktion; sulkeet `()` osoittavat, ettei
ole parametreja; ja aaltosulje `{` aloittaa funktion rungon.

Kuten opit myös luvussa 1, `println!` on makro, joka tulostaa merkkijonon
näytölle:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:print}}
```

Tämä koodi tulostaa kehotteen, joka kertoo mistä pelissä on kyse, ja pyytää syötettä
käyttäjältä.

### Arvojen tallentaminen muuttujilla

Seuraavaksi luomme _muuttujan_ tallentaaksemme käyttäjän syötteen, näin:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:string}}
```

Nyt ohjelma alkaa olla mielenkiintoinen! Tässä lyhyessä
rivissä tapahtuu paljon. Käytämme `let`-lauseketta luodaksemme muuttujan. Tässä toinen esimerkki:

```rust,ignore
let apples = 5;
```

Tämä rivi luo uuden muuttujan nimeltä `apples` ja sitoo sen arvoon 5. Rustissa
muuttujat ovat oletuksena muuttumattomia, eli kun annamme muuttujalle
arvon, arvo ei muutu. Käsittelemme tätä käsitettä tarkemmin
[”Muuttujat ja muutettavuus”][variables-and-mutability]<!-- ignore -->
-osiossa luvussa 3. Tehdäksemme muuttujan muutettavaksi lisäämme `mut`-avainsanan ennen
muuttujan nimeä:

```rust,ignore
let apples = 5; // immutable
let mut bananas = 5; // mutable
```

> Huom: `//`-syntaksi aloittaa kommentin, joka jatkuu rivin
> loppuun. Rust jättää huomiotta kaiken kommenteissa. Käsittelemme kommentteja tarkemmin
> [luvussa 3][comments]<!-- ignore -->.

Palatessa arvauspeli-ohjelmaan, tiedät nyt että `let mut guess`
esittelee muutettavan muuttujan nimeltä `guess`. Yhtäsuuruusmerkki (`=`) kertoo Rustille, että
haluamme sitoa jotain muuttujaan nyt. Yhtäsuuruusmerkin oikealla puolella on
arvo, johon `guess` sidotaan, eli `String::new`-funktion kutsumisen tulos,
funktio joka palauttaa uuden `String`-instanssin.
[`String`][string]<!-- ignore --> on standardikirjaston tarjoama merkkijonotyyppi,
joka on kasvava, UTF-8 -koodattu tekstinpätkä.

`::`-syntaksi `::new`-rivillä osoittaa, että `new` on assosioitu
funktio `String`-tyypille. _Assosioitu funktio_ on funktio, joka on
toteutettu tyypille, tässä tapauksessa `String`:lle. Tämä `new`-funktio luo
uuden, tyhjän merkkijonon. Löydät `new`-funktion monilta tyypeiltä, koska se on
yleinen nimi funktiolle, joka luo jonkinlaisen uuden arvon.

Kokonaisuudessaan `let mut guess = String::new();` -rivi on luonut muutettavan
muuttujan, joka on tällä hetkellä sidottu uuteen, tyhjään `String`-instanssiin. Huh!

### Käyttäjän syötteen vastaanottaminen

Muista, että sisällytimme syöte-/tulostustoiminnallisuuden standardikirjastosta
`use std::io;` -lauseella ohjelman ensimmäisellä rivillä. Kutsumme nyt
`stdin`-funktiota `io`-moduulista, mikä antaa meidän käsitellä käyttäjän
syötettä:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:read}}
```

Jos emme olisi tuoneet `io`-kirjastoa näkyviin `use std::io;` -lauseella ohjelman
alussa, voisimme silti käyttää funktiota kirjoittamalla funktiokutsun muodossa
`std::io::stdin`. `stdin`-funktio palauttaa instanssin
[`std::io::Stdin`][iostdin]<!-- ignore --> -tyypistä, joka edustaa
käsittelijää päätteen standardisyötteelle.

Seuraavaksi rivi `.read_line(&mut guess)` kutsuu [`read_line`][read_line]<!--
ignore --> -metodia standardisyötteen käsittelijällä saadakseen syötteen käyttäjältä.
Välitämme myös `&mut guess` argumenttina `read_line`-metodille kertoaksemme sille, mihin
merkkijonoon tallentaa käyttäjän syötteen. `read_line`-metodin tehtävä on ottaa
mitä tahansa käyttäjä kirjoittaa standardisyötteeseen ja liittää se merkkijonoon
(ylikirjoittamatta sen sisältöä), joten välitämme tuon merkkijonon
argumenttina. Merkkijonoargumentin täytyy olla muutettava, jotta metodi voi muuttaa
merkkijonon sisältöä.

`&` osoittaa, että tämä argumentti on _viittaus_, joka antaa tavan
antaa useiden koodin osien käyttää samaa dataa ilman, että dataa täytyy
kopioida muistiin useita kertoja. Viittaukset ovat monimutkainen ominaisuus,
ja yksi Rustin suurista eduista on, kuinka turvallista ja helppoa viittausten
käyttö on. Et tarvitse tietää paljoa näistä yksityiskohdista tämän
ohjelman viimeistelyyn. Toistaiseksi sinun tarvitsee tietää vain, että kuten muuttujat, viittaukset ovat
oletuksena muuttumattomia. Siksi sinun täytyy kirjoittaa `&mut guess` eikä
`&guess` tehdäksesi sen muutettavaksi. (Luku 4 selittää viittaukset tarkemmin.)

<!-- Old heading. Do not remove or links may break. -->

<a id="handling-potential-failure-with-the-result-type"></a>

### Mahdollisen epäonnistumisen käsittely `Result`-tyypillä

Työstämme vielä tätä koodiriviä. Käsittelemme nyt kolmatta
tekstiriviä, mutta huomaa, että se on edelleen osa yhtä loogista koodiriviä. Seuraava
osa on tämä metodi:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:expect}}
```

Olisimme voineet kirjoittaa tämän koodin näin:

```rust,ignore
io::stdin().read_line(&mut guess).expect("Failed to read line");
```

Yksi pitkä rivi on kuitenkin vaikea lukea, joten on parasta jakaa se. On
usein viisasta lisätä rivinvaihto ja muuta välilyöntiä auttamaan jakamaan pitkiä
rivejä, kun kutsut metodia `.method_name()` -syntaksilla. Käsitellään nyt,
mitä tämä rivi tekee.

Kuten aiemmin mainittiin, `read_line` laittaa mitä tahansa käyttäjä syöttää merkkijonoon,
jonka välitämme sille, mutta se palauttaa myös `Result`-arvon. [`Result`][result]<!--
ignore --> on [_enum_][enums]<!-- ignore -->, usein kutsuttu _enumiksi_,
joka on tyyppi, joka voi olla yhdessä useista mahdollisista tiloista. Kutakin
mahdollista tilaa kutsutaan _variantiksi_.

[Luku 6][enums]<!-- ignore --> käsittelee enumeja tarkemmin. Näiden
`Result`-tyyppien tarkoitus on koodata virheenkäsittelytietoa.

`Result`-tyypin variantit ovat `Ok` ja `Err`. `Ok`-variantti osoittaa, että
operaatio onnistui, ja se sisältää onnistuneesti generoidun arvon.
`Err`-variantti tarkoittaa, että operaatio epäonnistui, ja se sisältää tietoa
siitä, miten tai miksi operaatio epäonnistui.

`Result`-tyypin arvoilla, kuten minkä tahansa tyypin arvoilla, on niille määriteltyjä metodeja.
`Result`-instanssilla on [`expect`-metodi][expect]<!-- ignore -->,
jota voit kutsua. Jos tämä `Result`-instanssi on `Err`-arvo, `expect`
saa ohjelman kaatumaan ja näyttämään viestin, jonka välitit
argumenttina `expect`-metodille. Jos `read_line`-metodi palauttaa `Err`-arvon, se olisi
todennäköisesti käyttöjärjestelmän virheen seurausta.
Jos tämä `Result`-instanssi on `Ok`-arvo, `expect` ottaa palautusarvon,
jonka `Ok` pitää sisällään, ja palauttaa sen sinulle, jotta voit käyttää sitä.
Tässä tapauksessa tuo arvo on käyttäjän syötteen tavumäärä.

Jos et kutsu `expect`-metodia, ohjelma kääntyy, mutta saat varoituksen:

```console
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-02-without-expect/output.txt}}
```

Rust varoittaa, ettet ole käyttänyt `read_line`-metodin palauttamaa `Result`-arvoa,
osoittaen, ettei ohjelma ole käsitellyt mahdollista virhettä.

Oikea tapa hiljentää varoitus on todella kirjoittaa virheenkäsittelykoodi,
mutta tapauksessamme haluamme vain kaataa ohjelman, kun ongelma ilmenee, joten voimme
käyttää `expect`-metodia. Opit virheistä toipumisesta [luvussa
9][recover]<!-- ignore -->.

### Arvojen tulostaminen `println!`-paikkamerkeillä

Sulkevan aaltosulkeen lisäksi on vielä yksi rivi käsiteltävänä tähänastisessa
koodissa:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:print_guess}}
```

Tämä rivi tulostaa merkkijonon, joka sisältää nyt käyttäjän syötteen. `{}`-merkkien
joukko on paikkamerkki: ajattele `{}`:tä pieninä rapupihdeinä, jotka pitävät
arvon paikallaan. Kun tulostat muuttujan arvon, muuttujan nimi voi
mennä aaltosulkeiden sisään. Kun tulostat lausekkeen evaluoinnin tuloksen, laita tyhjät aaltosulkeet
muotoilumerkkijonoon ja lisää sen jälkeen pilkulla erotettu lista lausekkeista,
jotka tulostetaan kuhunkin tyhjään
aaltosuljepaikkamerkkiin samassa järjestyksessä. Muuttujan ja lausekkeen tulostaminen
yhdessä `println!`-kutsussa näyttäisi tältä:

```rust
let x = 5;
let y = 10;

println!("x = {x} and y + 2 = {}", y + 2);
```

Tämä koodi tulostaisi `x = 5 and y + 2 = 12`.

### Ensimmäisen osan testaaminen

Testataan arvauspelin ensimmäistä osaa. Aja se käyttämällä `cargo run`-komentoa:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-01/
cargo clean
cargo run
input 6 -->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 6.44s
     Running `target/debug/guessing_game`
Guess the number!
Please input your guess.
6
You guessed: 6
```

Tässä vaiheessa pelin ensimmäinen osa on valmis: saamme syötteen
näppäimistöltä ja tulostamme sen.

## Salaisen luvun generointi

Seuraavaksi meidän täytyy generoida salainen luku, jota käyttäjä yrittää arvata. Salaisen
luvun pitäisi olla eri joka kerta, jotta peli on hauska pelata useammin
kuin kerran. Käytämme satunnaista lukua väliltä 1–100, jotta peli ei ole liian
vaikea. Rust ei vielä sisällytä satunnaislukutoiminnallisuutta standardikirjastoonsa.
Rust-tiimi tarjoaa kuitenkin [`rand`-craten][randcrate], jossa
kyseinen toiminnallisuus on.

### Craten käyttö lisätoiminnallisuuden saamiseksi

Muista, että crate on kokoelma Rust-lähdekooditiedostoja. Projekti,
jota olemme rakentaneet, on _binaaricrate_, joka on suoritettava ohjelma. `rand`-
crate on _kirjastocrate_, joka sisältää koodia, joka on tarkoitettu käytettäväksi
muissa ohjelmissa eikä sitä voi suorittaa itsenäisesti.

Cargon koordinointi ulkoisista crateista on se, missä Cargo todella loistaa. Ennen kuin
voimme kirjoittaa koodia, joka käyttää `rand`-cratea, meidän täytyy muokata _Cargo.toml_-tiedostoa
sisällyttääksemme `rand`-craten riippuvuudeksi. Avaa tiedosto nyt ja lisää
seuraava rivi pohjaan, `[dependencies]`-osion otsikon alle, jonka
Cargo loi sinulle. Varmista, että määrittelet `rand`:in täsmälleen kuten tässä,
tällä versionumerolla, tai tämän opetusohjelman koodiesimerkit eivät välttämättä toimi:

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
* ch14-03-cargo-workspaces.md
-->

<span class="filename">Filename: Cargo.toml</span>

```toml
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-02/Cargo.toml:8:}}
```

_Cargo.toml_-tiedostossa kaikki otsikon jälkeen tuleva kuuluu siihen
osioon, joka jatkuu, kunnes toinen osio alkaa. `[dependencies]`-osiossa
kerrot Cargolle, mistä ulkoisista crateista projektisi riippuu ja mitä versioita
näistä crateista tarvitset. Tässä tapauksessa määrittelemme `rand`-craten
semanttisella versionumerolla `0.8.5`. Cargo ymmärtää [semanttisen
versionhallinnan][semver]<!-- ignore --> (joskus kutsutaan _SemVeriksi_), joka on
standardi versionumeroiden kirjoittamiseen. Määrite `0.8.5` on itse asiassa
lyhennys muodolle `^0.8.5`, mikä tarkoittaa mitä tahansa versiota, joka on vähintään 0.8.5 mutta
alle 0.8.9.0.

Cargo pitää näitä versioita julkisesti yhteensopivina version
0.8.5 API:n kanssa, ja tämä määrite varmistaa, että saat uusimman korjausjulkaisun, joka
vielä kääntyy tämän luvun koodin kanssa. Mikään versio 0.9.0 tai suurempi
ei ole taattu sisältävän samaa API:a kuin seuraavat esimerkit käyttävät.

Nyt, muuttamatta mitään koodia, käännetään projekti, kuten listauksessa 2-2.

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
rm Cargo.lock
cargo clean
cargo build -->

<Listing number="2-2" caption="Tuloste `cargo build` -komennon ajosta `rand`-craten lisäämisen jälkeen riippuvuudeksi">

```console
$ cargo build
  Updating crates.io index
   Locking 15 packages to latest Rust 1.85.0 compatible versions
    Adding rand v0.8.5 (available: v0.9.0)
 Compiling proc-macro2 v1.0.93
 Compiling unicode-ident v1.0.17
 Compiling libc v0.2.170
 Compiling cfg-if v1.0.0
 Compiling byteorder v1.5.0
 Compiling getrandom v0.2.15
 Compiling rand_core v0.6.4
 Compiling quote v1.0.38
 Compiling syn v2.0.98
 Compiling zerocopy-derive v0.7.35
 Compiling zerocopy v0.7.35
 Compiling ppv-lite86 v0.2.20
 Compiling rand_chacha v0.3.1
 Compiling rand v0.8.5
 Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
  Finished `dev` profile [unoptimized + debuginfo] target(s) in 2.48s
```

</Listing>

Saatat nähdä eri versionumerot (mutta ne ovat kaikki yhteensopivia koodin
kanssa SemVerin ansiosta!) ja eri rivejä (käyttöjärjestelmästä riippuen),
ja rivit voivat olla eri järjestyksessä.

Kun sisällytämme ulkoisen riippuvuuden, Cargo hakee uusimmat versiot
kaikesta, mitä kyseinen riippuvuus tarvitsee, _rekisteristä_, joka on kopio dataa
[Crates.io][cratesio]-sivustolta. Crates.io on paikka, jossa Rust-ekosysteemin ihmiset
julkaisevat avoimen lähdekoodin Rust-projektejaan muiden käytettäväksi.

Rekisterin päivityksen jälkeen Cargo tarkistaa `[dependencies]`-osion ja
lataa kaikki listatut cratet, joita ei ole vielä ladattu. Tässä tapauksessa,
vaikka listasimme vain `rand`:in riippuvuudeksi, Cargo haki myös muita crateja,
joista `rand` riippuu toimiakseen. Cratet ladattuaan Rust kääntää
ne ja kääntää sitten projektin riippuvuuksien ollessa käytettävissä.

Jos ajat heti `cargo build`-komennon uudelleen tekemättä muutoksia, et
saa mitään tulostetta `Finished`-rivin lisäksi. Cargo tietää, että se on jo
lataanut ja kääntänyt riippuvuudet, etkä ole muuttanut mitään
niistä _Cargo.toml_-tiedostossasi. Cargo tietää myös, ettet ole muuttanut
mitään koodissasi, joten se ei käännä sitäkään uudelleen. Kun ei ole mitään
tehtävää, se yksinkertaisesti lopettaa.

Jos avaat _src/main.rs_-tiedoston, teet pienen muutoksen, tallennat sen ja
käännät uudelleen, näet vain kaksi riviä tulostetta:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
touch src/main.rs
cargo build -->

```console
$ cargo build
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.13s
```

Nämä rivit osoittavat, että Cargo päivittää käännöksen vain pienellä muutoksellasi
_src/main.rs_-tiedostoon. Riippuvuutesi eivät ole muuttuneet, joten Cargo tietää voivansa
käyttää uudelleen jo ladattua ja kääntämäänsä.

#### Toistettavien käännösten varmistaminen _Cargo.lock_-tiedostolla

Cargolla on mekanismi, joka varmistaa, että voit kääntää saman artefaktin joka kerta,
kun sinä tai kuka tahansa kääntää koodisi: Cargo käyttää vain niitä riippuvuuksien versioita,
joita määritit, kunnes ilmoitat toisin. Sanotaan esimerkiksi, että
ensi viikolla `rand`-craten versio 0.8.6 julkaistaan, ja tuo versio
sisältää tärkeän bugikorjauksen, mutta myös regressiota, joka
rikkoo koodisi. Tätä varten Rust luo _Cargo.lock_-tiedoston ensimmäisellä
`cargo build` -ajolla, joten meillä on nyt tämä _guessing_game_-
hakemistossa.

Kun käännät projektin ensimmäistä kertaa, Cargo selvittää kaikki riippuvuuksien versiot,
jotka sopivat kriteereihin, ja kirjoittaa ne sitten
_Cargo.lock_-tiedostoon. Kun käännät projektisi tulevaisuudessa, Cargo näkee
_Cargo.lock_-tiedoston olevan olemassa ja käyttää siellä määriteltyjä versioita
sen sijaan, että tekisi kaiken työn versioiden selvittämiseksi uudelleen. Tämä antaa sinulle
toistettavan käännöksen automaattisesti. Toisin sanoen projektisi pysyy
versiossa 0.8.5, kunnes päivität eksplisiittisesti, _Cargo.lock_-tiedoston ansiosta.
Koska _Cargo.lock_-tiedosto on tärkeä toistettaville käännöksille, se tarkistetaan usein
versionhallintaan muun projektikoodin kanssa.

#### Craten päivittäminen uuden version saamiseksi

Kun _haluat_ päivittää craten, Cargo tarjoaa `update`-komennon,
joka ohittaa _Cargo.lock_-tiedoston ja selvittää kaikki uusimmat versiot,
jotka sopivat määrittelyihisi _Cargo.toml_-tiedostossa. Cargo kirjoittaa sitten nämä
versiot _Cargo.lock_-tiedostoon. Tässä tapauksessa Cargo etsii vain
versioita, jotka ovat suurempia kuin 0.8.5 ja pienempiä kuin 0.9.0. Jos `rand`-cratella on
julkaistu kaksi uutta versiota 0.8.6 ja 0.9.0, näkisit seuraavan, jos
ajaisit `cargo update`-komennon:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
cargo update
assuming there is a new 0.8.x version of rand; otherwise use another update
as a guide to creating the hypothetical output shown here -->

```console
$ cargo update
    Updating crates.io index
     Locking 1 package to latest Rust 1.85.0 compatible version
    Updating rand v0.8.5 -> v0.8.6 (available: v0.9.0)
```

Cargo jättää huomiotta version 0.9.0 julkaisun. Tässä vaiheessa huomaisit myös muutoksen
_Cargo.lock_-tiedostossasi, joka osoittaa, että käyttämäsi `rand`-craten versio on nyt 0.8.6. Käyttääksesi `rand`-version 0.9.0 tai mitä tahansa versiota 0.9._x_-
sarjassa, sinun täytyisi päivittää _Cargo.toml_-tiedosto näyttämään tältä:

```toml
[dependencies]
rand = "0.9.0"
```

Seuraavalla `cargo build` -ajolla Cargo päivittää saatavilla olevien cratejen rekisterin
ja arvioi `rand`-vaatimuksesi uudelleen määrittämäsi uuden version
mukaan.

[Cargosta][doccargo]<!-- ignore --> ja [sen
ekosysteemistä][doccratesio]<!-- ignore --> on paljon enemmän sanottavaa, joita käsittelemme luvussa 14, mutta
toistaiseksi se on kaikki mitä sinun täytyy tietää. Cargo tekee kirjastojen uudelleenkäytöstä hyvin helppoa,
joten rustilaiset voivat kirjoittaa pienempiä projekteja, jotka koostuvat
useista paketeista.

### Satunnaisluvun generointi

Aloitetaan `rand`-craten käyttö luvun generoimiseksi arvattavaksi. Seuraava vaihe on
päivittää _src/main.rs_, kuten listauksessa 2-3.

<Listing number="2-3" file-name="src/main.rs" caption="Koodin lisääminen satunnaisluvun generoimiseksi">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-03/src/main.rs:all}}
```

</Listing>

Ensin lisäämme rivin `use rand::Rng;`. `Rng`-trait määrittelee metodit, jotka
satunnaislukugeneraattorit toteuttavat, ja tämän traitin täytyy olla näkyvissä, jotta voimme
käyttää näitä metodeja. Luku 10 käsittelee traitit tarkemmin.

Seuraavaksi lisäämme kaksi riviä keskelle. Ensimmäisellä rivillä kutsumme
`rand::thread_rng`-funktiota, joka antaa meille tietyn satunnaislukugeneraattorin,
jota käytämme: sellaisen, joka on paikallinen nykyiselle suoritussäikeelle
ja jonka käyttöjärjestelmä siemenöi. Sitten kutsumme `gen_range`-
metodia satunnaislukugeneraattorilla. Tämän metodin määrittelee `Rng`-
trait, jonka toimme näkyviin `use rand::Rng;` -lauseella. `gen_range`-metodi ottaa
alueen lausekkeena argumenttina ja generoi satunnaisluvun alueella. Käyttämämme
alueen lauseke on muodossa `start..=end` ja on sisältävä molemmissa rajoissa, joten meidän
täytyy määritellä `1..=100` pyytääksemme lukua väliltä 1–100.

> Huom: Et vain tiedä, mitä traitteja käyttää ja mitä metodeja ja funktioita
> kutsua cratesta, joten jokaisella cratella on dokumentaatio ohjeineen
> käyttöön. Cargon toinen hieno ominaisuus on, että `cargo doc
> --open` -komennon ajaminen kääntää kaikkien riippuvuuksiesi tarjoaman dokumentaation
> paikallisesti ja avaa sen selaimessasi. Jos olet kiinnostunut muusta
> toiminnallisuudesta `rand`-cratessa, aja esimerkiksi `cargo doc --open` ja
> napsauta `rand` vasemman sivupalkin kohdasta.

Toinen uusi rivi tulostaa salaisen luvun. Tämä on hyödyllistä ohjelmaa
kehittäessä testataksemme sitä, mutta poistamme sen
lopullisesta versiosta. Se ei ole kovin hauska peli, jos ohjelma tulostaa vastauksen heti
käynnistyessään!

Kokeile ajaa ohjelma muutaman kerran:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-03/
cargo run
4
cargo run
5
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.02s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 7
Please input your guess.
4
You guessed: 4

$ cargo run
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.02s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 83
Please input your guess.
5
You guessed: 5
```

Sinun pitäisi saada eri satunnaislukuja, ja niiden kaikkien pitäisi olla lukuja väliltä
1–100. Hienoa työtä!

## Arvauksen vertaaminen salaiseen lukuun

Nyt kun meillä on käyttäjän syöte ja satunnainen luku, voimme vertailla niitä. Tämä vaihe
näytetään listauksessa 2-4. Huomaa, että tämä koodi ei vielä käänny, kuten
selitämme.

<Listing number="2-4" file-name="src/main.rs" caption="Kahden luvun vertailun mahdollisten palautusarvojen käsittely">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-04/src/main.rs:here}}
```

</Listing>

Ensin lisäämme toisen `use`-lauseen tuoden tyypin nimeltä
`std::cmp::Ordering` näkyviin standardikirjastosta. `Ordering`-tyyppi
on toinen enum ja sillä on variantit `Less`, `Greater` ja `Equal`. Nämä ovat
kolme mahdollista tulosta, kun vertaat kahta arvoa.

Sitten lisäämme viisi uutta riviä pohjaan, jotka käyttävät `Ordering`-tyyppiä. `cmp`-metodi vertaa kahta arvoa ja sitä voi
kutsua millä tahansa, jota voi verrata. Se ottaa viittauksen siihen, mihin haluat verrata: tässä se
vertaa `guess`:ia `secret_number`:iin. Sitten se palauttaa `Ordering`-enumin variantin, jonka toimme näkyviin `use`-lauseella. Käytämme
[`match`][match]<!-- ignore --> -lauseketta päättääksemme, mitä tehdä seuraavaksi sen perusteella,
mikä `Ordering`-variantti palautettiin `cmp`-kutsusta arvoilla
`guess` ja `secret_number`.

`match`-lauseke koostuu _haaroista_. Haara koostuu _kuviosta_,
jota vasten matchataan, ja koodista, joka pitäisi suorittaa, jos `match`-lausekkeelle annettu arvo
sopii haaran kuvioon. Rust ottaa `match`-lausekkeelle annetun arvon ja katsoo
jokaisen haaran kuviota vuorollaan. Kuviot ja `match`-rakenne ovat
voimakkaita Rust-ominaisuuksia: ne antavat sinun ilmaista monenlaisia tilanteita, joita koodisi
saattaa kohdata, ja varmistavat, että käsittelet ne kaikki. Nämä ominaisuudet käsitellään
tarkemmin luvuissa 6 ja 19.

Käydään läpi esimerkki käyttämällä tässä käyttämäämme `match`-lauseketta. Sanotaan, että
käyttäjä on arvannut 50 ja tällä kertaa generoitu salainen luku on
38.

Kun koodi vertaa 50:tä 38:een, `cmp`-metodi palauttaa
`Ordering::Greater`, koska 50 on suurempi kuin 38. `match`-lauseke saa
`Ordering::Greater`-arvon ja alkaa tarkistaa kunkin haaran kuviota. Se katsoo
ensimmäisen haaran kuviota `Ordering::Less` ja näkee, ettei arvo
`Ordering::Greater` matchaa `Ordering::Less`:ia, joten se jättää huomiotta koodin
kyseisessä haarassa ja siirtyy seuraavaan haaraan. Seuraavan haaran kuvio on
`Ordering::Greater`, joka _matchaa_ `Ordering::Greater`:in! Kyseiseen haaraan
liittyvä koodi suoritetaan ja tulostaa `Too big!` näytölle. `match`-
lauseke päättyy ensimmäisen onnistuneen matchin jälkeen, joten se ei katso viimeistä
haaraa tässä skenaariossa.

Listauksen 2-4 koodi ei kuitenkaan vielä käänny. Kokeillaan sitä:

<!--
The error numbers in this output should be that of the code **WITHOUT** the
anchor or snip comments
-->

```console
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-04/output.txt}}
```

Virheen ydin sanoo, että tyypit _eivät täsmää_. Rustilla on
vahva, staattinen tyyppijärjestelmä. Sillä on kuitenkin myös tyyppipäättely. Kun kirjoitimme
`let mut guess = String::new()`, Rust pystyi päättelemään, että `guess`:n pitäisi olla
`String` eikä pakottanut meitä kirjoittamaan tyyppiä. `secret_number` sen sijaan
on lukutyyppi. Muutama Rustin lukutyyppi voi olla arvolla välillä 1
ja 100: `i32`, 32-bittinen luku; `u32`, etumerkittömä 32-bittinen luku; `i64`, 64-
bittinen luku; ja muita. Ellei toisin määritellä, Rust oletuksena käyttää
`i32`:ta, joka on `secret_number`:n tyyppi, ellei lisää tyyppitietoa muualla,
mikä saisi Rustin päättelemään eri numeerisen tyypin. Virheen syy
on, että Rust ei voi verrata merkkijonoa ja lukutyyppiä.

Lopulta haluamme muuntaa `String`-merkkijonon, jonka ohjelma lukee syötteenä, lukutyyppiin,
jotta voimme verrata sitä numeerisesti salaiseen lukuun. Teemme sen
lisäämällä tämän rivin `main`-funktion runkoon:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-03-convert-string-to-number/src/main.rs:here}}
```

Rivi on:

```rust,ignore
let guess: u32 = guess.trim().parse().expect("Please type a number!");
```

Luomme muuttujan nimeltä `guess`. Mutta odota, eikö ohjelmalla jo ole
muuttujaa nimeltä `guess`? On, mutta Rust sallii meille hyödyllisesti varjostaa
`guess`:n aiemman arvon uudella. _Varjostus_ antaa meidän käyttää uudelleen `guess`-
muuttujan nimeä sen sijaan, että pakottaisimme meidät luomaan kaksi erillistä muuttujaa, kuten
`guess_str` ja `guess`. Käsittelemme tätä tarkemmin
[luvussa 3][shadowing]<!-- ignore -->, mutta toistaiseksi tiedä, että tätä ominaisuutta
käytetään usein, kun haluat muuntaa arvon tyypistä toiseen.

Sidoimme tämän uuden muuttujan lausekkeeseen `guess.trim().parse()`. `guess`
lausekkeessa viittaa alkuperäiseen `guess`-muuttujaan, joka sisälsi
syötteen merkkijonona. `trim`-metodi `String`-instanssilla poistaa kaiken
väliylityksen alusta ja lopusta, mikä meidän täytyy tehdä ennen kuin voimme muuntaa
merkkijonon `u32`:ksi, joka voi sisältää vain numeerista dataa. Käyttäjän täytyy painaa
<kbd>enter</kbd> tyydyttääkseen `read_line`-metodin ja syöttääkseen arvauksensa, mikä lisää
rivinvaihtomerkin merkkijonoon. Jos käyttäjä kirjoittaa <kbd>5</kbd> ja
painaa <kbd>enter</kbd>, `guess` näyttää tältä: `5\n`. `\n` edustaa
”rivinvaihtoa.” (Windowsissa <kbd>enter</kbd>-näppäimen painaminen tuottaa rivinvaihdon
ja rivinvaihdon, `\r\n`.) `trim`-metodi poistaa `\n`:n tai `\r\n`:n, jolloin
jäljelle jää vain `5`.

Merkkijonojen [`parse`-metodi][parse]<!-- ignore --> muuntaa merkkijonon
toiseen tyyppiin. Tässä käytämme sitä muuntamaan merkkijonosta luvuksi. Meidän täytyy
kertoa Rustille tarkka lukutyyppi, jota haluamme käyttämällä `let guess: u32`. Kaksoispiste
(`:`) `guess`:n jälkeen kertoo Rustille, että annotoimme muuttujan tyypin. Rustilla on
muutama sisäänrakennettu lukutyyppi; tässä nähty `u32` on etumerkittömä 32-bittinen kokonaisluku.
Se on hyvä oletusvalinta pienelle positiiviselle luvulle. Opit muista
lukutyypeistä [luvussa 3][integers]<!-- ignore -->.

Lisäksi tämän esimerkkiohjelman `u32`-annotaatio ja vertailu
`secret_number`:iin tarkoittavat, että Rust päättelee `secret_number`:n olevan myös
`u32`. Joten nyt vertailu on kahden saman
tyypin arvon välillä!

`parse`-metodi toimii vain merkeillä, jotka voidaan loogisesti muuntaa
luvuiksi, ja voi siksi helposti aiheuttaa virheitä. Jos esimerkiksi merkkijono
sisältäisi `A👍%`, sitä ei voisi muuntaa luvuksi. Koska se
saattaa epäonnistua, `parse`-metodi palauttaa `Result`-tyypin, aivan kuten `read_line`-
metodi (käsiteltiin aiemmin [”Mahdollisen epäonnistumisen käsittely
`Result`-tyypillä”](#handling-potential-failure-with-result)<!-- ignore--> -osiossa). Käsittelemme
tämän `Result`-arvon samalla tavalla käyttämällä jälleen `expect`-metodia. Jos `parse`
palauttaa `Err`-`Result`-variantin, koska se ei voinut luoda lukua
merkkijonosta, `expect`-kutsu kaataa pelin ja tulostaa antamamme viestin.
Jos `parse` voi onnistuneesti muuntaa merkkijonon luvuksi, se palauttaa
`Ok`-variantin `Result`-tyypistä, ja `expect` palauttaa haluamamme luvun
`Ok`-arvosta.

Ajetaan ohjelma nyt:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/no-listing-03-convert-string-to-number/
touch src/main.rs
cargo run
  76
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.26s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 58
Please input your guess.
  76
You guessed: 76
Too big!
```

Hienoa! Vaikka arvauksen eteen lisättiin välilyöntejä, ohjelma silti selvitti,
että käyttäjä arvasi 76. Aja ohjelma muutaman kerran varmistaaksesi
erilaisen käyttäytymisen eri syötteillä: arvaa luku oikein,
arvaa liian suuri luku ja arvaa liian pieni luku.

Meillä on nyt suurin osa pelistä toiminnassa, mutta käyttäjä voi tehdä vain yhden arvauksen.
Muutetaan sitä lisäämällä silmukka!

## Useiden arvausten salliminen silmukalla

`loop`-avainsana luo äärettömän silmukan. Lisäämme silmukan antaaksemme käyttäjille
enemmän mahdollisuuksia arvata luku:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-04-looping/src/main.rs:here}}
```

Kuten näet, olemme siirtäneet kaiken arvauskehotteesta eteenpäin
silmukkaan. Muista sisentää silmukan sisällä olevat rivit neljä välilyöntiä lisää
ja aja ohjelma uudelleen. Ohjelma pyytää nyt uutta arvausta ikuisesti,
mikä itse asiassa tuo uuden ongelman. Käyttäjä ei näytä pystyvän lopettamaan!

Käyttäjä voisi aina keskeyttää ohjelman näppäinyhdistelmällä
<kbd>ctrl</kbd>-<kbd>c</kbd>. Mutta on toinen tapa paeta tämä tyydyttämätön
hirviö, kuten mainittiin `parse`-keskustelussa [”Arvauksen vertaaminen salaiseen lukuun”](#comparing-the-guess-to-the-secret-number)<!-- ignore --> -osiossa: jos
käyttäjä syöttää ei-numeerisen vastauksen, ohjelma kaatuu. Voimme hyödyntää
sitä salliaksemme käyttäjän lopettaa, kuten tässä:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/no-listing-04-looping/
touch src/main.rs
cargo run
(too small guess)
(too big guess)
(correct guess)
quit
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.23s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 59
Please input your guess.
45
You guessed: 45
Too small!
Please input your guess.
60
You guessed: 60
Too big!
Please input your guess.
59
You guessed: 59
You win!
Please input your guess.
quit

thread 'main' panicked at src/main.rs:28:47:
Please type a number!: ParseIntError { kind: InvalidDigit }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

`quit`-kirjoittaminen lopettaa pelin, mutta kuten huomaat, myös mikä tahansa
muu ei-numeerinen syöte lopettaa sen. Tämä on lievästi sanottuna epäoptimaalista; haluamme pelin
pysähtyvän myös, kun oikea luku arvataan.

### Lopettaminen oikean arvauksen jälkeen

Ohjelmoidaan peli lopettamaan, kun käyttäjä voittaa, lisäämällä `break`-lause:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-05-quitting/src/main.rs:here}}
```

`break`-rivin lisääminen `You win!`-tekstin jälkeen saa ohjelman poistumaan silmukasta, kun
käyttäjä arvaa salaisen luvun oikein. Silmukasta poistuminen tarkoittaa myös
ohjelman päättymistä, koska silmukka on `main`-funktion viimeinen osa.

### Virheellisen syötteen käsittely

Hienosäätääksemme pelin käyttäytymistä sen sijaan, että kaataisimme ohjelman, kun
käyttäjä syöttää ei-numeerisen arvon, tehdään pelistä sellainen, että se jättää huomiotta ei-numeerisen syötteen, jotta
käyttäjä voi jatkaa arvaamista. Voimme tehdä sen muuttamalla riviä, jossa `guess`
muunnetaan `String`:stä `u32`:ksi, kuten listauksessa 2-5.

<Listing number="2-5" file-name="src/main.rs" caption="Ei-numeerisen arvauksen huomiotta jättäminen ja uuden arvauksen pyytäminen ohjelman kaatamisen sijaan">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-05/src/main.rs:here}}
```

</Listing>

Vaihdamme `expect`-kutsusta `match`-lausekkeeseen siirtyäksemme kaatumisesta
virheenkäsittelyyn. Muista, että `parse` palauttaa `Result`-tyypin
ja `Result` on enum, jolla on variantit `Ok` ja `Err`. Käytämme
tässä `match`-lauseketta, kuten teimme `cmp`-metodin `Ordering`-tuloksen kanssa.

Jos `parse` pystyy onnistuneesti muuttamaan merkkijonon luvuksi, se
palauttaa `Ok`-arvon, joka sisältää tuloksena olevan luvun. Tuo `Ok`-arvo
matchaa ensimmäisen haaran kuvion, ja `match`-lauseke palauttaa vain
`num`-arvon, jonka `parse` tuotti ja laittoi `Ok`-arvon sisään. Tuo luku
päätyy juuri sinne, minne haluamme uudessa `guess`-muuttujassa, jonka luomme.

Jos `parse` _ei_ pysty muuttamaan merkkijonoa luvuksi, se palauttaa
`Err`-arvon, joka sisältää lisätietoa virheestä. `Err`-arvo
ei matchaa ensimmäisen `match`-haaran kuviota `Ok(num)`, mutta se
matchaa toisen haaran kuvion `Err(_)`. Alaviiva `_` on
catch-all-arvo; tässä esimerkissä sanomme haluavamme matchata kaikki `Err`-
arvot riippumatta siitä, mitä tietoa niissä on. Joten ohjelma
suorittaa toisen haaran koodin `continue`, joka kertoo ohjelman siirtyä
seuraavaan silmukan iteratioon ja pyytää uutta arvausta. Eli käytännössä
ohjelma jättää huomiotta kaikki virheet, joita `parse` saattaa kohdata!

Nyt kaiken pitäisi toimia odotetusti. Kokeillaan:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-05/
cargo run
(too small guess)
(too big guess)
foo
(correct guess)
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.13s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 61
Please input your guess.
10
You guessed: 10
Too small!
Please input your guess.
99
You guessed: 99
Too big!
Please input your guess.
foo
Please input your guess.
61
You guessed: 61
You win!
```

Mahtavaa! Pienellä viimeisellä hienosäädöllä viimeistelemme arvauspelin. Muista,
että ohjelma tulostaa edelleen salaisen luvun. Se toimi hyvin
testauksessa, mutta se pilaa pelin. Poistetaan `println!`, joka tulostaa
salainen luvun. Listausta 2-6 näyttää lopullisen koodin.

<Listing number="2-6" file-name="src/main.rs" caption="Valmis arvauspeli-koodi">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-06/src/main.rs}}
```

</Listing>

Tässä vaiheessa olet onnistuneesti rakentanut arvauspelin. Onnittelut!

## Yhteenveto

Tämä projekti oli käytännönläheinen tapa esitellä sinulle monia uusia Rust-käsitteitä:
`let`, `match`, funktiot, ulkoisten cratejen käyttö ja paljon muuta. Seuraavissa
luvuissa opit näistä käsitteistä tarkemmin. Luku 3
käsittelee käsitteitä, joita useimmissa ohjelmointikielissä on, kuten muuttujat, data-
tyypit ja funktiot, ja näyttää, miten niitä käytetään Rustissa. Luku 4 tutkii
omistajuutta, ominaisuutta, joka tekee Rustista erilaisen kuin muut kielet. Luku 5
käsittelee rakenteita ja metodisyntaksia, ja luku 6 selittää, miten enumit toimivat.

[prelude]: ../std/prelude/index.html
[variables-and-mutability]: ch03-01-variables-and-mutability.html#variables-and-mutability
[comments]: ch03-04-comments.html
[string]: ../std/string/struct.String.html
[iostdin]: ../std/io/struct.Stdin.html
[read_line]: ../std/io/struct.Stdin.html#method.read_line
[result]: ../std/result/enum.Result.html
[enums]: ch06-00-enums.html
[expect]: ../std/result/enum.Result.html#method.expect
[recover]: ch09-02-recoverable-errors-with-result.html
[randcrate]: https://crates.io/crates/rand
[semver]: http://semver.org
[cratesio]: https://crates.io/
[doccargo]: https://doc.rust-lang.org/cargo/
[doccratesio]: https://doc.rust-lang.org/cargo/reference/publishing.html
[match]: ch06-02-match.html
[shadowing]: ch03-01-variables-and-mutability.html#shadowing
[parse]: ../std/primitive.str.html#method.parse
[integers]: ch03-02-data-types.html#integer-types
