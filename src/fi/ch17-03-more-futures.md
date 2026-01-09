## Työskentely minkä tahansa määrän futuresien kanssa

Kun siirryimme käyttämään kolmea futurea kahden sijaan edellisessä osiossa, meidän
piti myös vaihtaa `join`-funktiosta `join3`-funktioon. Olisi ärsyttävää joutua
kutsumaan eri funktiota aina, kun muutimme yhdistettävien futuresien määrää.
Onneksi meillä on `join`-funktion makromuoto, jolle voimme välittää minkä tahansa
määrän argumentteja. Se myös käsittelee futuresien odottamisen itse.
Näin voisimme kirjoittaa Listauksen 17-13 koodin uudelleen käyttämään `join!`-makroa
`join3`-funktion sijaan, kuten Listauksessa 17-14.

<Listing number="17-14" caption="`join!`-makron käyttö useiden futuresien odottamiseen" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-14/src/main.rs:here}}
```

</Listing>

Tämä on ehdottomasti parannus verrattuna vaihteluun `join`- ja
`join3`- ja `join4`-funktioiden välillä ja niin edelleen! Tämä makromuoto toimii
kuitenkin vain, kun tiedämme futuresien määrän etukäteen. Todellisessa Rust-koodissa
futuresien työntäminen kokoelmaan ja sitten odottaminen, että jokin tai
kaikki niistä valmistuvat, on yleinen malli.

Tarkistaaksemme kaikki futuresit jossakin kokoelmassa, meidän täytyy iteroida ja
yhdistää _kaikki_ ne. `trpl::join_all`-funktio hyväksyy minkä tahansa tyypin, joka
toteuttaa `Iterator`-traitin, josta opit takaisin [Iterator-traitissa ja `next`-metodissa][iterator-trait]<!-- ignore --> Luvussa 13, joten
se vaikuttaa juuri sopivalta. Kokeillaan laittaa futuresimme vektoriin ja
korvata `join!`-makro `join_all`-funktiolla, kuten Listauksessa 17-15.

<Listing  number="17-15" caption="Anonyymien futuresien tallentaminen vektoriin ja `join_all`-funktion kutsuminen">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-15/src/main.rs:here}}
```

</Listing>

Valitettavasti tämä koodi ei käänny. Sen sijaan saamme tämän virheen:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-15/
cargo build
copy just the compiler error
-->

```text
error[E0308]: mismatched types
  --> src/main.rs:45:37
   |
10 |         let tx1_fut = async move {
   |                       ---------- the expected `async` block
...
24 |         let rx_fut = async {
   |                      ----- the found `async` block
...
45 |         let futures = vec![tx1_fut, rx_fut, tx_fut];
   |                                     ^^^^^^ expected `async` block, found a different `async` block
   |
   = note: expected `async` block `{async block@src/main.rs:10:23: 10:33}`
              found `async` block `{async block@src/main.rs:24:22: 24:27}`
   = note: no two async blocks, even if identical, have the same type
   = help: consider pinning your async block and casting it to a trait object
```

Tämä saattaa olla yllättävää. Loppujen lopuksi mikään async-lohkoista ei palauta mitään,
joten jokainen tuottaa `Future<Output = ()>`-tyypin. Muista kuitenkin, että `Future` on trait,
ja että kääntäjä luo yksilöllisen enumin jokaiselle async-lohkolle. Et
voi laittaa kahta eri käsin kirjoitettua rakennetta `Vec`-kokoelmaan, ja sama sääntö
pätee kääntäjän luomiin eri enumeihin.

Jotta tämä toimisi, meidän täytyy käyttää _trait-objekteja_, aivan kuten teimme [Luvun 12 "Virheiden palauttaminen run-funktiosta"][dyn]<!-- ignore --> -osiossa. (Käsittelemme
trait-objekteja yksityiskohtaisesti Luvussa 18.) Trait-objektien käyttö antaa meille mahdollisuuden
käsitellä jokaisen näiden tyyppien tuottaman anonyymin futuren samana tyyppinä, koska
kaikki ne toteuttavat `Future`-traitin.

> Huom: Luvun 8 osiossa [Enumin käyttö useiden arvojen tallentamiseen][enum-alt]<!-- ignore -->, käsittelimme toista tapaa sisällyttää useita
> tyyppejä `Vec`-kokoelmaan: enumin käyttöä edustamaan jokaista tyyppiä, joka voi esiintyä
> vektorissa. Emme voi tehdä sitä täällä kuitenkaan. Ensinnäkin, meillä ei ole tapaa nimetä
> eri tyyppejä, koska ne ovat anonyymejä. Toiseksi, syy, miksi päädyimme vektoriin ja
> `join_all`-funktioon alun perin, oli pystyä työskentelemään dynaamisen futuresien kokoelman
> kanssa, jossa meitä kiinnostaa vain, että niillä on sama
> tulostetyyppi.

Aloitamme käärimällä jokaisen futuren `vec!`-makrossa `Box::new`-funktiolla, kuten
Listauksessa 17-16.

<Listing number="17-16" caption="`Box::new`-funktion käyttö futuresien tyyppien kohdistamiseen `Vec`-kokoelmassa" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-16/src/main.rs:here}}
```

</Listing>

Valitettavasti tämä koodi ei vieläkään käänny. Itse asiassa saamme saman perusvirheen
kuin aiemmin sekä toiselle että kolmannelle `Box::new`-kutsulle, sekä
uudet virheet, jotka viittaavat `Unpin`-traitiin. Palaamme `Unpin`-virheisiin
hetken kuluttua. Korjataan ensin tyyppivirheet `Box::new`-kutsuissa
merkitsemällä nimenomaisesti `futures`-muuttujan tyyppi (katso Listaus 17-17).

<Listing number="17-17" caption="Loput tyyppierrosten korjaaminen käyttämällä nimenomaista tyyppimääritystä" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-17/src/main.rs:here}}
```

</Listing>

Tämä tyyppimääritys on hieman monimutkainen, joten käydään se läpi:

1. Sisimmäinen tyyppi on itse future. Merkitsemme nimenomaisesti, että futuren
   tuloste on yksikkötyyppi `()` kirjoittamalla `Future<Output = ()>`.
2. Sitten merkitsemme traitin `dyn`-avainsanalla merkitsemään sen dynaamiseksi.
3. Koko trait-viite on kääritty `Box`-tyyppiin.
4. Lopuksi, ilmoitamme nimenomaisesti, että `futures` on `Vec`, joka sisältää näitä
   kohteita.

Se teki jo suuren eron. Nyt kun ajamme kääntäjän, saamme vain
virheet, jotka mainitsevat `Unpin`-traitin. Vaikka niitä on kolme, niiden sisältö
on hyvin samankaltainen.

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-16
cargo build
# copy *only* the errors
# fix the paths
-->

```text
error[E0308]: mismatched types
   --> src/main.rs:46:46
    |
10  |         let tx1_fut = async move {
    |                       ---------- the expected `async` block
...
24  |         let rx_fut = async {
    |                      ----- the found `async` block
...
46  |             vec![Box::new(tx1_fut), Box::new(rx_fut), Box::new(tx_fut)];
    |                                     -------- ^^^^^^ expected `async` block, found a different `async` block
    |                                     |
    |                                     arguments to this function are incorrect
    |
    = note: expected `async` block `{async block@src/main.rs:10:23: 10:33}`
               found `async` block `{async block@src/main.rs:24:22: 24:27}`
    = note: no two async blocks, even if identical, have the same type
    = help: consider pinning your async block and casting it to a trait object
note: associated function defined here
   --> file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/alloc/src/boxed.rs:252:12
    |
252 |     pub fn new(x: T) -> Self {
    |            ^^^

error[E0308]: mismatched types
   --> src/main.rs:46:64
    |
10  |         let tx1_fut = async move {
    |                       ---------- the expected `async` block
...
30  |         let tx_fut = async move {
    |                      ---------- the found `async` block
...
46  |             vec![Box::new(tx1_fut), Box::new(rx_fut), Box::new(tx_fut)];
    |                                                       -------- ^^^^^^ expected `async` block, found a different `async` block
    |                                                       |
    |                                                       arguments to this function are incorrect
    |
    = note: expected `async` block `{async block@src/main.rs:10:23: 10:33}`
               found `async` block `{async block@src/main.rs:30:22: 30:32}`
    = note: no two async blocks, even if identical, have the same type
    = help: consider pinning your async block and casting it to a trait object
note: associated function defined here
   --> file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/alloc/src/boxed.rs:252:12
    |
252 |     pub fn new(x: T) -> Self {
    |            ^^^

error[E0277]: `{async block@src/main.rs:10:23: 10:33}` cannot be unpinned
   --> src/main.rs:48:24
    |
48  |         trpl::join_all(futures).await;
    |         -------------- ^^^^^^^ the trait `Unpin` is not implemented for `{async block@src/main.rs:10:23: 10:33}`
    |         |
    |         required by a bound introduced by this call
    |
    = note: consider using the `pin!` macro
            consider using `Box::pin` if you need to access the pinned value outside of the current scope
    = note: required for `Box<{async block@src/main.rs:10:23: 10:33}>` to implement `Future`
note: required by a bound in `join_all`
   --> file:///home/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/futures-util-0.3.30/src/future/join_all.rs:105:14
    |
102 | pub fn join_all<I>(iter: I) -> JoinAll<I::Item>
    |        -------- required by a bound in this function
...
105 |     I::Item: Future,
    |              ^^^^^^ required by this bound in `join_all`

error[E0277]: `{async block@src/main.rs:10:23: 10:33}` cannot be unpinned
  --> src/main.rs:48:9
   |
48 |         trpl::join_all(futures).await;
   |         ^^^^^^^^^^^^^^^^^^^^^^^ the trait `Unpin` is not implemented for `{async block@src/main.rs:10:23: 10:33}`
   |
    = note: consider using the `pin!` macro
           consider using `Box::pin` if you need to access the pinned value outside of the current scope
    = note: required for `Box<{async block@src/main.rs:10:23: 10:33}>` to implement `Future`
note: required by a bound in `futures_util::future::join_all::JoinAll`
  --> file:///home/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/futures-util-0.3.30/src/future/join_all.rs:29:8
    |
27 | pub struct JoinAll<F>
    |            ------- required by a bound in this struct
28 | where
29 |     F: Future,
   |        ^^^^^^ required by this bound in `JoinAll`

error[E0277]: `{async block@src/main.rs:10:23: 10:33}` cannot be unpinned
  --> src/main.rs:48:33
   |
48 |         trpl::join_all(futures).await;
   |                                 ^^^^^ the trait `Unpin` is not implemented for `{async block@src/main.rs:10:23: 10:33}`
   |
    = note: consider using the `pin!` macro
           consider using `Box::pin` if you need to access the pinned value outside of the current scope
    = note: required for `Box<{async block@src/main.rs:10:23: 10:33}>` to implement `Future`
note: required by a bound in `futures_util::future::join_all::JoinAll`
  --> file:///home/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/futures-util-0.3.30/src/future/join_all.rs:29:8
    |
27 | pub struct JoinAll<F>
    |            ------- required by a bound in this struct
28 | where
29 |     F: Future,
   |        ^^^^^^ required by this bound in `JoinAll`
```

Se on _paljon_ sulatettavaa, joten puretaan se osiin. Viestin ensimmäinen osa
kertoo meille, että ensimmäinen async-lohko (`src/main.rs:8:23: 20:10`) ei
toteuta `Unpin`-traitia ja ehdottaa `pin!`- tai `Box::pin`-funktion käyttöä sen
ratkaisemiseksi. Myöhemmin tässä luvussa syvennämme hieman lisää `Pin`- ja
`Unpin`-traitien yksityiskohtiin. Tällä hetkellä voimme kuitenkin vain seurata
kääntäjän neuvoja päästäksemme eteenpäin. Listauksessa 17-18 aloitamme päivittämällä
tyyppimerkinnän `futures`-muuttujalle `Pin`-tyypillä, joka käärii jokaisen `Box`-tyypin. Toiseksi, käytämme `Box::pin`-funktiota kiinnittääksemme
futuresit itse.

<Listing number="17-18" caption="`Pin`- ja `Box::pin`-funktioiden käyttö `Vec`-tyypin tarkistamiseksi" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-18/src/main.rs:here}}
```

</Listing>

Jos kääntämme ja ajamme tämän, saamme vihdoin toivomamme tulosteen:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
received 'hi'
received 'more'
received 'from'
received 'messages'
received 'the'
received 'for'
received 'future'
received 'you'
```

Huh!

Täällä on vielä hieman tutkittavaa. Ensinnäkin, `Pin<Box<T>>`-tyypin käyttö lisää
pienen määrän ylimääräistä työtä laittamalla nämä futuresit pinoon `Box`-tyypin avulla—ja
teemme sen vain saadaksemme tyypit kohdistettua. Emme itse asiassa _tarvitse_
pinomuistin varausta, loppujen lopuksi: nämä futuresit ovat paikallisia tälle
erityiselle funktiolle. Kuten aiemmin mainittiin, `Pin` on itse kääretyyppi, joten voimme saada
hyödyn siitä, että `Vec`-kokoelmassa on yksi tyyppi—alkuperäinen syy, miksi
päädyimme `Box`-tyyppiin—ilman pinomuistin varausta. Voimme käyttää `Pin`-tyyppiä
suoraan jokaisen futuren kanssa käyttämällä `std::pin::pin`-makroa.

Meidän täytyy kuitenkin olla vielä nimenomaisia kiinnitetyn viitteen tyypistä;
muuten Rust ei vieläkään tiedä tulkita näitä dynaamisina trait-objekteina,
mikä on se, mitä tarvitsemme niiden olevan `Vec`-kokoelmassa. Kiinnitämme siis jokaisen futuren
kun määrittelemme sen, ja määrittelemme `futures`-muuttujan `Vec`-kokoelmaksi, joka sisältää kiinnitettyjä muuttuvia
viitteitä dynaamiseen future-tyyppiin, kuten Listauksessa 17-19.

<Listing number="17-19" caption="`Pin`-tyypin suora käyttö `pin!`-makron avulla välttääksemme tarpeettomat pinomuistin varaukset" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-19/src/main.rs:here}}
```

</Listing>

Pääsimme tähän asti unohtamalla tosiasian, että meillä saattaa olla eri `Output`
-tyyppejä. Esimerkiksi Listauksessa 17-20 anonyymi future `a`:lle toteuttaa
`Future<Output = u32>`-tyypin, anonyymi future `b`:lle toteuttaa `Future<Output =
&str>`-tyypin, ja anonyymi future `c`:lle toteuttaa `Future<Output = bool>`-tyypin.

<Listing number="17-20" caption="Kolme eri tyyppistä futurea" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-20/src/main.rs:here}}
```

</Listing>

Voimme käyttää `trpl::join!`-makroa odottaaksemme niitä, koska se antaa meille mahdollisuuden
välittää useita future-tyyppejä ja tuottaa näiden tyyppien tuplen. Emme _voi_ käyttää
`trpl::join_all`-funktiota, koska se vaatii, että kaikki välitetyt futuresit ovat
samaa tyyppiä. Muista, että se virhe sai meidät aloittamaan tämän seikkailun
`Pin`-tyypin kanssa!

Tämä on perustavanlaatuinen kompromissi: voimme joko käsitellä dynaamisen määrän
futureseja `join_all`-funktiolla, niin kauan kuin ne kaikki ovat samaa tyyppiä, tai voimme käsitellä
kiinteän määrän futureseja `join`-funktioilla tai `join!`-makrolla,
vaikka niillä olisi eri tyypit. Tämä on sama skenaario, johon törmäisimme
työskennellessämme minkä tahansa muiden tyyppien kanssa Rustissa. Futuresit eivät ole erityisiä, vaikka meillä
on mukava syntaksi työskentelemiseen niiden kanssa, ja se on hyvä asia.

### Futuresien kilpailuttaminen

Kun "yhdistämme" futuresit `join`-funktio- ja makroperheen avulla, vaadimme
_kaikkien_ niiden valmistuvan ennen kuin siirrymme eteenpäin. Joskus tarvitsemme kuitenkin vain
_jonkin_ futuren joukosta valmistuvan ennen kuin siirrymme eteenpäin—jotain samankaltaista kuin
kilpailuttamassa yhtä futurea toista vastaan.

Listauksessa 17-21 käytämme jälleen `trpl::race`-funktiota suorittaaksemme kaksi futurea, `slow` ja
`fast`, toisiaan vastaan.

<Listing number="17-21" caption="`race`-funktion käyttö saadaksemme sen futuren tuloksen, joka valmistuu ensin" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-21/src/main.rs:here}}
```

</Listing>

Jokainen future tulostaa viestin, kun se alkaa suorittaa, pysähtyy jonkin aikaa
kutsumalla ja odottamalla `sleep`-funktiota, ja sitten tulostaa toisen viestin, kun se
valmistuu. Sitten välitämme sekä `slow`- että `fast`-futuren `trpl::race`-funktiolle ja odotamme, että yksi
niistä valmistuu. (Tulos ei ole liian yllättävä: `fast` voittaa.) Toisin kuin
kun käytimme `race`-funktiota takaisin [Ensimmäisessä async-ohjelmassamme][async-program]<!--
ignore -->, jätämme vain `Either`-instanssin, jonka se palauttaa, huomiotta, koska kaikki
mielenkiintoiset toiminnot tapahtuvat async-lohkojen rungoissa.

Huomaa, että jos vaihdat `race`-funktion argumenttien järjestyksen, "aloitettu"
-viestien järjestys muuttuu, vaikka `fast`-future valmistuu aina
ensimmäisenä. Se johtuu siitä, että tämän erityisen `race`-funktion toteutus ei
ole reilu. Se ajaa aina futuresit, jotka välitetään argumentteina, siinä järjestyksessä, jossa
ne välitetään. Muut toteutukset _ovat_ reiluja ja valitsevat satunnaisesti
minkä futuren kysellä ensin. Riippumatta siitä, onko käyttämämme `race`-funktion toteutus
reilu vai ei, _yksi_ futuresista suoritetaan ensimmäiseen
`await`-pisteeseen rungossaan asti ennen kuin toinen tehtävä voi alkaa.

Muistamme [Ensimmäisestä async-ohjelmastamme][async-program]<!-- ignore -->, että jokaisessa
await-pisteessä Rust antaa ajonaikaisjärjestelmälle mahdollisuuden keskeyttää tehtävä ja vaihtaa
toiseen, jos odotettava future ei ole valmis. Käänteinen on myös totta:
Rust _keskeyttää_ async-lohkot ja luovuttaa ohjauksen takaisin ajonaikaisjärjestelmälle vain
await-pisteessä. Kaikki await-pisteiden välillä on synkronista.

Se tarkoittaa, että jos teet paljon työtä async-lohkossa ilman await-pistettä,
tuo future estää kaikki muut futuresit edistymästä. Saatat joskus
kuulla tämän viitattavan siihen, että yksi future _näännyttää_ muita futureseja. Joissakin tapauksissa
se ei ehkä ole iso juttu. Jos teet kuitenkin jonkinlaista kalliita
asetuksia tai pitkäkestoista työtä, tai jos sinulla on future, joka jatkaa jonkin
erityisen tehtävän suorittamista loputtomasti, sinun täytyy miettiä, milloin ja missä luovuttaa
ohjaus takaisin ajonaikaisjärjestelmälle.

Samalla tavalla, jos sinulla on pitkäkestoisia estäviä operaatioita, async voi olla
hyödyllinen työkalu tarjoamaan tapoja eri ohjelman osien suhtautumiseen
toisiinsa.

Mutta _miten_ luovuttaisit ohjauksen takaisin ajonaikaisjärjestelmälle näissä tapauksissa?

<!-- Old headings. Do not remove or links may break. -->

<a id="yielding"></a>

### Ohjauksen luovuttaminen ajonaikaisjärjestelmälle

Simuloimme pitkäkestoisen operaation. Listaus 17-22 esittelee `slow`
-funktion.

<Listing number="17-22" caption="`thread::sleep`-funktion käyttö hitaiden operaatioiden simuloimiseen" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-22/src/main.rs:slow}}
```

</Listing>

Tämä koodi käyttää `std::thread::sleep`-funktiota `trpl::sleep`-funktion sijaan, jotta `slow`
-funktion kutsuminen estää nykyisen säikeen joksikin millisekunneiksi. Voimme käyttää
`slow`-funktiota edustamaan todellisia operaatioita, jotka ovat sekä pitkäkestoisia että
estäviä.

Listauksessa 17-23 käytämme `slow`-funktiota jäljittelemään tämän tyyppistä CPU-sidonnaista työtä
kahdessa futuressa.

<Listing number="17-23" caption="`thread::sleep`-funktion käyttö hitaiden operaatioiden simuloimiseen" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-23/src/main.rs:slow-futures}}
```

</Listing>

Aluksi jokainen future luovuttaa ohjauksen takaisin ajonaikaisjärjestelmälle vasta _jälkeen_
suoritettuaan joukon hitaita operaatioita. Jos ajat tämän koodin, näet tämän tulosteen:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-23/
cargo run
copy just the output
-->

```text
'a' started.
'a' ran for 30ms
'a' ran for 10ms
'a' ran for 20ms
'b' started.
'b' ran for 75ms
'b' ran for 10ms
'b' ran for 15ms
'b' ran for 350ms
'a' finished.
```

Kuten aiemmassa esimerkissämme, `race`-funktio valmistuu silti heti, kun `a` on valmis.
Näiden kahden futuren välillä ei ole kuitenkaan vuorottelua. `a`-future tekee kaiken
työnsä, kunnes `trpl::sleep`-kutsu odotetaan, sitten `b`-future tekee
kaiken työnsä, kunnes sen oma `trpl::sleep`-kutsu odotetaan, ja lopuksi `a`
-future valmistuu. Salliaaksemme molempien futuresien edistyä hitaiden
tehtävien välillä, tarvitsemme await-pisteitä, jotta voimme luovuttaa ohjauksen takaisin ajonaikaisjärjestelmälle. Se
tarkoittaa, että tarvitsemme jotain, mitä voimme odottaa!

Näemme jo tämän tyyppisen luovutuksen tapahtuvan Listauksessa 17-23: jos
poistaisimme `trpl::sleep`-kutsun `a`-futuren lopusta, se valmistuisi
ilman, että `b`-future suoritetaan _ollenkaan_. Kokeillaan käyttää `sleep`-funktiota
lähtökohtana sallia operaatioiden vaihtaa edistymistä, kuten Listauksessa 17-24.

<Listing number="17-24" caption="`sleep`-funktion käyttö sallia operaatioiden vaihtaa edistymistä" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-24/src/main.rs:here}}
```

</Listing>

Listauksessa 17-24 lisäämme `trpl::sleep`-kutsuja await-pisteineen jokaisen `slow`
-funktion kutsun välillä. Nyt näiden kahden futuren työ on vuoroteltu:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-24
cargo run
copy just the output
-->

```text
'a' started.
'a' ran for 30ms
'b' started.
'b' ran for 75ms
'a' ran for 10ms
'b' ran for 10ms
'a' ran for 20ms
'b' ran for 15ms
'a' finished.
```

`a`-future suoritetaan silti hieman ennen kuin se luovuttaa ohjauksen `b`:lle, koska
se kutsuu `slow`-funktiota ennen kuin koskaan kutsuu `trpl::sleep`-funktiota, mutta sen jälkeen futuresit
vaihtavat edestakaisin aina, kun yksi niistä osuu await-pisteeseen. Tässä tapauksessa olemme
tehneet sen jokaisen `slow`-funktion kutsun jälkeen, mutta voisimme jakaa työn
millä tahansa tavalla, joka on meille järkevin.

Emme kuitenkaan halua _nukkua_ täällä: haluamme edistyä niin nopeasti
kuin mahdollista. Meidän täytyy vain luovuttaa ohjaus takaisin ajonaikaisjärjestelmälle. Voimme tehdä sen
suoraan käyttämällä `yield_now`-funktiota. Listauksessa 17-25 korvaamme kaikki nuo
`sleep`-kutsut `yield_now`-funktiolla.

<Listing number="17-25" caption="`yield_now`-funktion käyttö sallia operaatioiden vaihtaa edistymistä" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-25/src/main.rs:yields}}
```

</Listing>

Tämä koodi on sekä selkeämpi todellisesta tarkoituksesta että voi olla merkittävästi
nopeampi kuin `sleep`-funktion käyttö, koska ajastimet, kuten `sleep`-funktiossa käytetty,
usein rajoittavat, kuinka hienojakoisia ne voivat olla. Käyttämämme `sleep`-funktion versio
nukkuu esimerkiksi aina vähintään millisekunnin, vaikka välittäisimme sille
`Duration`-tyypin, joka on yksi nanosekunti. Nykyaikaiset tietokoneet ovat _nopeita_: ne voivat tehdä
paljon yhdessä millisekunnissa!

Voit nähdä tämän itse asettamalla pienen suorituskykytestin, kuten Listauksessa 17-26. (Tämä ei ole erityisen tiukka tapa
tehdä suorituskykytestaus, mutta se riittää osoittamaan eron täällä.)

<Listing number="17-26" caption="`sleep`- ja `yield_now`-funktioiden suorituskyvyn vertailu" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-26/src/main.rs:here}}
```

</Listing>

Täällä ohitamme kaikki tilatulostukset, välitämme yhden nanosekunnin `Duration`-tyypin
`trpl::sleep`-funktiolle, ja annamme jokaisen futuren suorittaa itsenäisesti, ilman vaihtelua futuresien
välillä. Sitten ajamme 1000 iteraatiota ja näemme, kuinka kauan `trpl::sleep`-funktiota käyttävä
future kestää verrattuna `trpl::yield_now`-funktiota käyttävään futureen.

Versio `yield_now`-funktiolla on _paljon_ nopeampi!

Se tarkoittaa, että async voi olla hyödyllinen jopa laskentasidonnaisille tehtäville, riippuen
siitä, mitä muuta ohjelmasi tekee, koska se tarjoaa hyödyllisen työkalun
rakentamaan suhteita ohjelman eri osien välille. Tämä on
muoto _yhteistyöhön perustuvasta moniajosta_ (cooperative multitasking), jossa jokaisella futurella on valta määrittää
milloin se luovuttaa ohjauksen await-pisteiden kautta. Jokaisella futurella on siis myös
vastuu välttää estäminen liian kauan. Joissakin Rust-pohjaisissa sulautetuissa
käyttöjärjestelmissä tämä on _ainoa_ moniajon muoto!

Todellisessa koodissa et yleensä vuorottele funktiokutsuja await-
pisteillä jokaisella rivillä, tietenkin. Vaikka ohjauksen luovuttaminen tällä tavalla on
suhteellisen halpaa, se ei ole ilmaista. Monissa tapauksissa laskentasidonnaisen
tehtävän jakaminen saattaa tehdä siitä merkittävästi hitaamman, joten joskus on parempi
_kokonaisuuden_ suorituskyvyn kannalta antaa operaation estää lyhyesti. Aina
mitata nähdäksesi, mitkä ovat koodisi todelliset suorituskyvyn pullonkaulat. Taustalla oleva
dynamiikka on tärkeää pitää mielessä, jos _näet_
paljon työtä tapahtuvan sarjassa, jota odotit tapahtuvan rinnakkain!

### Oman async-abstraktioiden rakentaminen

Voimme myös yhdistää futureseja yhteen luodaksemme uusia malleja. Esimerkiksi voimme
rakentaa `timeout`-funktion async-rakennuspalikoilla, joita meillä jo on. Kun
olemme valmiit, tulos on toinen rakennuspalikka, jota voisimme käyttää luodaksemme
vielä enemmän async-abstraktioita.

Listaus 17-27 näyttää, miten odotamme tämän `timeout`-funktion toimivan hitaan
futuren kanssa.

<Listing number="17-27" caption="Kuvittelemamme `timeout`-funktion käyttö hitaan operaation suorittamiseen aikarajalla" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-27/src/main.rs:here}}
```

</Listing>

Toteutetaan tämä! Aluksi mietitään `timeout`-funktion API:

- Sen täytyy olla itse async-funktio, jotta voimme odottaa sitä.
- Sen ensimmäisen parametrin pitäisi olla suoritettava future. Voimme tehdä sen geneeriseksi sallia
  sen toimia minkä tahansa futuren kanssa.
- Sen toinen parametri on maksimiaika odottaa. Jos käytämme `Duration`-tyyppiä,
  se tekee siitä helpon välittää `trpl::sleep`-funktiolle.
- Sen pitäisi palauttaa `Result`-tyyppi. Jos future valmistuu onnistuneesti,
  `Result`-tyyppi on `Ok` futuren tuottaman arvon kanssa. Jos aikaraja
  kuluu ensin, `Result`-tyyppi on `Err` aikarajan odottaman keston kanssa.

Listaus 17-28 näyttää tämän määrityksen.

<!-- This is not tested because it intentionally does not compile. -->

<Listing number="17-28" caption="`timeout`-funktion allekirjoituksen määrittäminen" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-28/src/main.rs:declaration}}
```

</Listing>

Se täyttää tyyppien tavoitteemme. Mietitään nyt _käyttäytymistä_, jota
tarvitsemme: haluamme kilpailuttaa välitetyn futuren kestoa vastaan. Voimme käyttää
`trpl::sleep`-funktiota tekemään ajastinfuturen kestosta, ja käyttää `trpl::race`-funktiota
ajamaan tuon ajastimen futuren kanssa, jonka kutsuja välittää.

Tiedämme myös, että `race`-funktio ei ole reilu, kysellen argumentteja siinä järjestyksessä, jossa
ne välitetään. Välitämme siis `future_to_try`-futuren `race`-funktiolle ensin, jotta se saa
mahdollisuuden valmistua, vaikka `max_time` olisi hyvin lyhyt kesto. Jos
`future_to_try` valmistuu ensin, `race`-funktio palauttaa `Left`-arvon `future_to_try`
:n tulosteen kanssa. Jos `timer`-future valmistuu ensin, `race`-funktio palauttaa `Right`-arvon
ajastimen `()`-tulosteen kanssa.

Listauksessa 17-29 vastaamme `trpl::race`-funktion odottamisen tulokseen.

<Listing number="17-29" caption="`timeout`-funktion määrittäminen `race`- ja `sleep`-funktioiden avulla" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-29/src/main.rs:implementation}}
```

</Listing>

Jos `future_to_try`-future onnistuu ja saamme `Left(output)`-arvon, palautamme
`Ok(output)`-arvon. Jos nukkumisajastin kuluu sen sijaan ja saamme `Right(())`-arvon, jätämme
`()`-arvon huomiotta `_`-merkillä ja palautamme `Err(max_time)`-arvon sen sijaan.

Sen avulla meillä on toimiva `timeout`-funktio, joka on rakennettu kahdesta muusta async-apufunktiosta. Jos
ajamme koodimme, se tulostaa epäonnistumistilan aikarajan jälkeen:

```text
Failed after 2 seconds
```

Koska futuresit yhdistyvät muiden futuresien kanssa, voit rakentaa todella tehokkaita työkaluja
käyttämällä pienempiä async-rakennuspalikoita. Esimerkiksi voit käyttää samaa lähestymistapaa
yhdistääksesi aikarajat uudelleenyrityksiin, ja puolestaan käyttää niitä operaatioiden, kuten
verkkokutsujen, kanssa (yksi esimerkeistä luvun alusta).

Käytännössä työskentelet yleensä suoraan `async`- ja `await`-avainsanojen kanssa, ja
toissijaisesti funktioiden ja makrojen, kuten `join`, `join_all`, `race`, ja niin
edelleen, kanssa. Tarvitset `pin`-funktiota vain ajoittain käyttääksesi futureseja näiden
API:en kanssa.

Olemme nyt nähneet useita tapoja työskennellä useiden futuresien kanssa samaan
aikaan. Seuraavaksi tarkastelemme, miten voimme työskennellä useiden futuresien kanssa
sekvenssissä ajan myötä _virtojen_ (streams) avulla. Tässä on muutama muukin asia, jota saatat haluta
harkita ensin:

- Käytimme `Vec`-kokoelmaa `join_all`-funktion kanssa odottaaksemme, että kaikki futuresit jossakin ryhmässä
  valmistuvat. Miten voisit käyttää `Vec`-kokoelmaa käsittelemään futuresien ryhmän
  sekvenssissä sen sijaan? Mitkä ovat sen tekemisen kompromissit?

- Tutustu `futures::stream::FuturesUnordered`-tyyppiin `futures`
  -cratesta. Miten sen käyttö eroaisi `Vec`-kokoelman käytöstä? (Älä huolehdi
  siitä, että se on craten `stream`-osiosta; se toimii hyvin
  minkä tahansa futuresien kokoelman kanssa.)

[dyn]: ch12-03-improving-error-handling-and-modularity.html
[enum-alt]: ch12-03-improving-error-handling-and-modularity.html#returning-errors-from-the-run-function
[async-program]: ch17-01-futures-and-syntax.html#our-first-async-program
[iterator-trait]: ch13-02-iterators.html#the-iterator-trait-and-the-next-method
