## I/O-projektimme parantaminen

Tämän uuden iteraattoritietämyksen avulla voimme parantaa luvun 12 I/O-projektia
käyttämällä iteraattoreita koodin selkeyttämiseen ja tiivistämiseen. Katsotaan, miten
iteraattorit voivat parantaa `Config::build`- ja `search`-funktioiden toteutusta.

### `clone`-kutsun poistaminen iteraattorilla

Listauksessa 12-6 lisäsimme koodia, joka otti `String`-arvojen viipaleen ja loi
`Config`-rakenteen instanssin indeksoimalla viipaleeseen ja kloonaamalla arvot, jotta
`Config`-rakenne voi omistaa ne. Listauksessa 13-17 olemme toistaneet `Config::build`-funktion
toteutuksen sellaisena kuin se oli listauksessa 12-23.

Silloin sanoin, ettei tehokkaiden `clone`-kutsujen tarvitse huolestuttaa, koska poistamme
ne myöhemmin. No, se aika on nyt!

Tarvitsimme `clone`-kutsun, koska parametrissa `args` on `String`-elementtien viipale,
mutta `build`-funktio ei omista `args`-parametria. Palauttaaksemme `Config`-instanssin
omistajuuden meidän täytyi kloonata arvot `query`- ja `file_path`-kentistä, jotta
`Config`-instanssi voi omistaa arvonsa.

Uudella iteraattoritietämyksellämme voimme muuttaa `build`-funktion ottamaan omistajuuden
iteraattorista argumenttina viipaleen lainaamisen sijaan. Käytämme iteraattorin
toiminnallisuutta viipaleen pituuden tarkistamiseen ja tiettyihin paikkoihin
indeksoimiseen. Tämä selkeyttää, mitä `Config::build` tekee, koska iteraattori käyttää
arvoja.

Kun `Config::build` ottaa omistajuuden iteraattorista eikä enää käytä lainaavia
indeksointioperaatioita, voimme siirtää `String`-arvot iteraattorista `Config`-rakenteeseen
`clone`-kutsun ja uuden allokoinnin sijaan.

#### Palautetun iteraattorin käyttö suoraan

Avaa I/O-projektisi tiedosto _src/main.rs_, jonka pitäisi näyttää tältä:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-12-24-reproduced/src/main.rs:ch13}}
```

Muutamme ensin `main`-funktion alun listauksesta 12-24 listauksen 13-18 koodiin, joka
tällä kertaa käyttää iteraattoria. Tämä ei käänny ennen kuin päivitämme myös
`Config::build`-funktion.

<Listing number="13-18" file-name="src/main.rs" caption="`env::args`-funktion palautusarvon välittäminen `Config::build`-funktiolle">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-18/src/main.rs:here}}
```

</Listing>

`env::args`-funktio palauttaa iteraattorin! Sen sijaan, että keräisimme iteraattorin
arvot vektoriin ja välittäisimme viipaleen `Config::build`-funktiolle, välitämme nyt
suoraan omistajuuden `env::args`-funktion palauttamaan iteraattoriin `Config::build`-funktiolle.

Seuraavaksi päivitämme `Config::build`-funktion määrittelyn. Muutetaan `Config::build`-funktion
allekirjoitus näyttämään listauksen 13-19 mukaiselta. Tämäkään ei vielä käänny, koska
meidän täytyy päivittää funktion runko.

<Listing number="13-19" file-name="src/main.rs" caption="`Config::build`-funktion allekirjoituksen päivittäminen odottamaan iteraattoria">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-19/src/main.rs:here}}
```

</Listing>

Standardikirjaston dokumentaatio `env::args`-funktiolle näyttää, että sen palauttaman
iteraattorin tyyppi on `std::env::Args`, ja tämä tyyppi toteuttaa `Iterator`-traitin ja
palauttaa `String`-arvoja.

Olemme päivittäneet `Config::build`-funktion allekirjoituksen niin, että parametrilla `args`
on geneerinen tyyppi trait-rajoilla `impl Iterator<Item = String>` `&[String]`-tyypin
sijaan. Tämä `impl Trait` -syntaksin käyttö, josta puhuimme luvun 10 osiossa
[”Traitien käyttö parametreina”][impl-trait]<!-- ignore -->, tarkoittaa, että `args` voi
olla mikä tahansa tyyppi, joka toteuttaa `Iterator`-traitin ja palauttaa `String`-kohteita.

Koska otamme omistajuuden `args`-parametrista ja muutamme sitä iteroinnin aikana,
voimme lisätä `mut`-avainsanan `args`-parametrin määrittelyyn tehdäksemme siitä
muuttuvan.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-iterator-trait-methods-instead-of-indexing"></a>

#### `Iterator`-traitin metodien käyttö

Seuraavaksi korjaamme `Config::build`-funktion rungon. Koska `args` toteuttaa `Iterator`-traitin,
tiedämme voivamme kutsua sille `next`-metodia! Listaus 13-20 päivittää listauksen 12-23
koodin käyttämään `next`-metodia.

<Listing number="13-20" file-name="src/main.rs" caption="`Config::build`-funktion rungon muuttaminen käyttämään iteraattorimetodeja">

```rust,ignore,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-20/src/main.rs:here}}
```

</Listing>

Muista, että `env::args`-funktion palautusarvon ensimmäinen arvo on ohjelman nimi. Haluamme
jättää sen huomiotta ja siirtyä seuraavaan arvoon, joten kutsumme ensin `next`-metodia
tekemättä mitään palautusarvolla. Sitten kutsumme `next`-metodia saadaksemme arvon, jonka
haluamme `Config`-rakenteen `query`-kenttään. Jos `next` palauttaa `Some`-variantin,
käytämme `match`-lausetta arvon purkamiseen. Jos se palauttaa `None`-variantin, argumentteja
ei annettu tarpeeksi, ja palaamme aikaisin `Err`-arvolla. Teemme saman `file_path`-arvolle.

<!-- Old headings. Do not remove or links may break. -->

<a id="making-code-clearer-with-iterator-adapters"></a>

### Koodin selkeyttäminen iteraattorisovittimilla

Voimme hyödyntää iteraattoreita myös I/O-projektimme `search`-funktiossa, joka on toistettu
tässä listauksessa 13-21 sellaisena kuin se oli listauksessa 12-19.

<Listing number="13-21" file-name="src/lib.rs" caption="`search`-funktion toteutus listauksesta 12-19">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-19/src/lib.rs:ch13}}
```

</Listing>

Voimme kirjoittaa tämän koodin tiiviimmin iteraattorisovittimien avulla. Samalla voimme
välttää väliaikaisen muuttuvan `results`-vektorin. Funktionaalinen ohjelmointityyli pyrkii
minimoimaan muuttuvan tilan määrän koodin selkeyttämiseksi. Muuttuvan tilan poistaminen
voisi mahdollistaa tulevaisuudessa rinnakkaisen haun, koska emme joutuisi hallitsemaan
samanaikaista pääsyä `results`-vektoriin. Listaus 13-22 näyttää tämän muutoksen.

<Listing number="13-22" file-name="src/lib.rs" caption="Iteraattorisovittimien käyttö `search`-funktion toteutuksessa">

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-22/src/lib.rs:here}}
```

</Listing>

Muista, että `search`-funktion tarkoitus on palauttaa kaikki `contents`-merkkijonon rivit,
jotka sisältävät `query`-merkkijonon. Kuten `filter`-esimerkissä listauksessa 13-16, tämä
koodi käyttää `filter`-sovitinta pitämään vain rivit, joille `line.contains(query)` palauttaa
`true`. Keräämme sitten vastaavat rivit toiseen vektoriin `collect`-metodilla. Paljon
yksinkertaisempaa! Voit vapaasti tehdä saman muutoksen `search_case_insensitive`-funktioon
käyttämällä iteraattorimetodeja.

Lisäparannuksena voit palauttaa iteraattorin `search`-funktiosta poistamalla `collect`-kutsun
ja muuttamalla palautustyypiksi `impl Iterator<Item = &'a str>`, jolloin funktiosta tulee
iteraattorisovitin. Huomaa, että sinun täytyy päivittää myös testit! Etsi suuresta tiedostosta
`minigrep`-työkalullasi ennen ja jälkeen muutoksen tehdessäsi ja havainnoi käyttäytymisen
eroa. Ennen muutosta ohjelma ei tulosta tuloksia ennen kuin se on kerännyt kaikki tulokset,
mutta muutoksen jälkeen tulokset tulostetaan sitä mukaa kun vastaava rivi löytyy, koska
`run`-funktion `for`-silmukka hyödyntää iteraattorin laiskuutta.

<!-- Old headings. Do not remove or links may break. -->

<a id="choosing-between-loops-or-iterators"></a>

### Silmukoiden ja iteraattorien valinta

Seuraava looginen kysymys on, kumpaa tyyliä sinun kannattaa käyttää omassa koodissasi ja
miksi: alkuperäinen toteutus listauksessa 13-21 vai iteraattoreita käyttävä versio
listauksessa 13-22 (olettaen, että keräämme kaikki tulokset ennen palauttamista iteraattorin
sijaan). Useimmat Rust-ohjelmoijat suosivat iteraattorityyliä. Se on aluksi hieman vaikeampi
omaksua, mutta kun saat tuntuman eri iteraattorisovittimista ja niiden toiminnasta,
iteraattorit voivat olla helpommin ymmärrettäviä. Sen sijaan, että säätäisit silmukan eri
osia ja rakentaisit uusia vektoreita, koodi keskittyy silmukan korkean tason tavoitteeseen.
Tämä abstrahoi pois tavanomaista koodia, jolloin tämän koodin ainutlaatuiset käsitteet —
kuten suodatusehto, jonka jokaisen iteraattorin elementin täytyy läpäistä — erottuvat
paremmin.

Ovatko kaksi toteutusta todella vastaavia? Intuitiivinen oletus saattaa olla, että matalamman
tason silmukka on nopeampi. Puhutaan suorituskyvystä.

[impl-trait]: ch10-02-traits.html#traits-as-parameters
