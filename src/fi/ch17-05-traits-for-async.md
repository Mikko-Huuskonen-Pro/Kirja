<!-- Old headings. Do not remove or links may break. -->

<a id="digging-into-the-traits-for-async"></a>

## Async-traitien tarkempi tarkastelu

Olemme tämän luvun ajan käyttäneet `Future`-, `Stream`- ja `StreamExt`-traitiä eri tavoin. Toistaiseksi olemme kuitenkin välttäneet syventymästä liikaa siihen, miten ne toimivat tai miten ne liittyvät toisiinsa, mikä on useimman aikaa ihan hyvä päivittäisessä Rust-työssä. Joskus kohtaat kuitenkin tilanteita, joissa sinun täytyy ymmärtää hieman enemmän näiden traitien yksityiskohtia sekä `Pin`-tyyppiä ja `Unpin`-traitiä. Tässä osiossa syvennymme juuri tarpeeksi auttamaan näissä tilanteissa, jättäen _todella_ syvän sukelluksen muulle dokumentaatiolle.

<!-- Old headings. Do not remove or links may break. -->

<a id="future"></a>

### `Future`-trait

Aloitetaan tarkastelemalla tarkemmin, miten `Future`-trait toimii. Näin Rust määrittelee sen:

```rust
use std::pin::Pin;
use std::task::{Context, Poll};

pub trait Future {
    type Output;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}
```

Tämä trait-määrittely sisältää joukon uusia tyyppejä ja myös syntaksia, jota emme ole vielä nähneet, joten käydään määrittely läpi pala kerrallaan.

Ensinnäkin `Future`:n assosioitu tyyppi `Output` kertoo, mihin future ratkeaa. Tämä on analoginen `Iterator`-traitin `Item`-assosioitulle tyypille. Toiseksi `Future`:lla on `poll`-metodi, joka ottaa `self`-parametrilleen erityisen `Pin`-viittauksen ja muuttuvan viittauksen `Context`-tyyppiin ja palauttaa `Poll<Self::Output>`:in. Puhumme `Pin`:stä ja `Context`:ista hetken kuluttua. Keskitytään toistaiseksi siihen, mitä metodi palauttaa, `Poll`-tyyppiin:

```rust
pub enum Poll<T> {
    Ready(T),
    Pending,
}
```

Tämä `Poll`-tyyppi on samankaltainen kuin `Option`. Siinä on yksi variantti, jossa on arvo, `Ready(T)`, ja yksi ilman arvoa, `Pending`. `Poll` tarkoittaa kuitenkin jotain hyvin erilaista kuin `Option`! `Pending`-variantti ilmaisee, että futurella on vielä työtä tekemättä, joten kutsujan täytyy tarkistaa uudelleen myöhemmin. `Ready`-variantti ilmaisee, että `Future` on saanut työnsä valmiiksi ja `T`-arvo on saatavilla.

> Huom: `poll`:ia on harvoin tarpeen kutsua suoraan, mutta jos joudut tekemään sen, muista, että useimmissa futureissa kutsujan ei pitäisi kutsua `poll`:ia uudelleen sen jälkeen, kun future on palauttanut `Ready`:n. Monet futuret panikoivat, jos niitä pollataan uudelleen valmistuttuaan. Futuret, joita on turvallista pollata uudelleen, sanovat sen eksplisiittisesti dokumentaatiossaan. Tämä on samankaltaista kuin `Iterator::next`:n käyttäytyminen.

Kun näet koodia, joka käyttää `await`:ia, Rust kääntää sen taustalla koodiksi, joka kutsuu `poll`:ia. Jos palaat listaukseen 17-4, jossa tulostimme yhden URL-osoitteen sivun otsikon sen ratkettua, Rust kääntää sen joksikin (vaikkakaan ei täsmälleen) tämän kaltaiseksi:

```rust,ignore
match page_title(url).poll() {
    Ready(page_title) => match page_title {
        Some(title) => println!("The title for {url} was {title}"),
        None => println!("{url} had no title"),
    }
    Pending => {
        // But what goes here?
    }
}
```

Mitä meidän pitäisi tehdä, kun future on vielä `Pending`? Tarvitsemme tavan yrittää uudelleen, ja uudelleen, ja uudelleen, kunnes future vihdoin on valmis. Toisin sanoen tarvitsemme silmukan:

```rust,ignore
let mut page_title_fut = page_title(url);
loop {
    match page_title_fut.poll() {
        Ready(value) => match page_title {
            Some(title) => println!("The title for {url} was {title}"),
            None => println!("{url} had no title"),
        }
        Pending => {
            // continue
        }
    }
}
```

Jos Rust kääntäisi sen täsmälleen tähän koodiin, jokainen `await` estäisi — juuri päinvastoin kuin tavoittelimme! Sen sijaan Rust varmistaa, että silmukka voi luovuttaa ohjauksen jollekin, joka voi keskeyttää työn tämän futuren parissa tehdäkseen työtä muilla futureilla ja tarkistaa tämän myöhemmin uudelleen. Kuten olemme nähneet, tuo jokin on async-ajoympäristö, ja tämä aikataulutus ja koordinointi on yksi sen päätehtävistä.

[”Datan lähettäminen kahden tehtävän välillä viestinvälityksellä”][message-passing]<!-- ignore --> -osiossa kuvasimme `rx.recv`:n odottamista. `recv`-kutsu palauttaa futuren, ja futuren odottaminen pollaa sitä. Huomautimme, että ajoympäristö keskeyttää futuren, kunnes se on valmis joko `Some(message)`:lla tai `None`:lla, kun kanava sulkeutuu. Syvemmällä ymmärryksellä `Future`-traitistä ja erityisesti `Future::poll`:ista näemme, miten se toimii. Ajoympäristö tietää, ettei future ole valmis, kun se palauttaa `Poll::Pending`:in. Vastaavasti ajoympäristö tietää, että future _on_ valmis ja edistää sitä, kun `poll` palauttaa `Poll::Ready(Some(message))`:n tai `Poll::Ready(None)`:n.

Tarkat yksityiskohdat siitä, miten ajoympäristö tekee tämän, ovat tämän kirjan laajuuden ulkopuolella, mutta keskeistä on nähdä futurejen perusmekaniikka: ajoympäristö _pollaa_ jokaista vastuullaan olevaa futurea ja asettaa futuren takaisin lepotilaan, kun se ei ole vielä valmis.

<!-- Old headings. Do not remove or links may break. -->

<a id="pinning-and-the-pin-and-unpin-traits"></a>
<a id="the-pin-and-unpin-traits"></a>

### `Pin`-tyyppi ja `Unpin`-trait

Listauksessa 17-13 käytimme `trpl::join!`-makroa odottamaan kolmea futurea. On kuitenkin yleistä, että kokoelma — kuten vektori — sisältää jonkin määrän futureja, joiden määrää ei tiedetä ennen ajoa. Muutetaan listaus 17-13 listauksen 17-23 koodiksi, joka sijoittaa kolme futurea vektoriin ja kutsuu `trpl::join_all`-funktiota sen sijaan, mikä ei vielä käänny.

<Listing number="17-23" caption="Futurejen odottaminen kokoelmassa"  file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-23/src/main.rs:here}}
```

</Listing>

Sijoitamme jokaisen futuren `Box`:iin tehdäksemme niistä _trait-objekteja_, aivan kuten teimme luvun 12 ”Virheiden palauttaminen `run`:ista” -osiossa. (Käsittelemme trait-objektit yksityiskohtaisesti luvussa 18.) Trait-objektien käyttö antaa meidän käsitellä kunkin näiden tyyppien tuottamaa nimettömää futurea samana tyyppinä, koska kaikki ne toteuttavat `Future`-traitin.

Tämä saattaa yllättää. Loppujen lopuksi mikään async-lohko ei palauta mitään, joten jokainen tuottaa `Future<Output = ()>`:n. Muista kuitenkin, että `Future` on trait ja että kääntäjä luo yksilöllisen enumin jokaiselle async-lohkolle, vaikka niillä olisi identtiset tulostyypit. Aivan kuten et voi laittaa kahta eri käsin kirjoitettua structia `Vec`:iin, et voi sekoittaa kääntäjän luomia enumeja.

Sitten välitämme futurejen kokoelman `trpl::join_all`-funktiolle ja odotamme tulosta. Tämä ei kuitenkaan käänny; tässä on virheilmoitusten olennainen osa.

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-23
cargo build
copy *only* the final `error` block from the errors
-->

```text
error[E0277]: `dyn Future<Output = ()>` cannot be unpinned
  --> src/main.rs:48:33
   |
48 |         trpl::join_all(futures).await;
   |                                 ^^^^^ the trait `Unpin` is not implemented for `dyn Future<Output = ()>`
   |
   = note: consider using the `pin!` macro
           consider using `Box::pin` if you need to access the pinned value outside of the current scope
   = note: required for `Box<dyn Future<Output = ()>>` to implement `Future`
note: required by a bound in `futures_util::future::join_all::JoinAll`
  --> file:///home/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/futures-util-0.3.30/src/future/join_all.rs:29:8
   |
27 | pub struct JoinAll<F>
   |            ------- required by a bound in this struct
28 | where
29 |     F: Future,
   |        ^^^^^^ required by this bound in `JoinAll`
```

Tämän virheilmoituksen huomautus kertoo, että meidän pitäisi käyttää `pin!`-makroa _kiinnittääksemme_ arvot, eli sijoittaa ne `Pin`-tyyppiin, joka takaa, ettei arvoja siirretä muistissa. Virheilmoitus sanoo, että kiinnitys vaaditaan, koska `dyn Future<Output = ()>`:n täytyy toteuttaa `Unpin`-trait, eikä se tällä hetkellä toteuta sitä.

`trpl::join_all`-funktio palauttaa structin nimeltä `JoinAll`. Kyseinen struct on geneerinen tyypin `F` suhteen, joka on rajoitettu toteuttamaan `Future`-traitin. Futuren odottaminen suoraan `await`:illa kiinnittää futuren implisiittisesti. Siksi emme tarvitse `pin!`:ää kaikkialla, missä haluamme odottaa futureja.

Emme kuitenkaan odota futurea suoraan tässä. Sen sijaan rakennamme uuden futuren, `JoinAll`:in, välittämällä futurejen kokoelman `join_all`-funktiolle. `join_all`:n signatuuri vaatii, että kokoelman kohteiden tyypit kaikki toteuttavat `Future`-traitin, ja `Box<T>` toteuttaa `Future`:n vain, jos sen käärimä `T` on future, joka toteuttaa `Unpin`-traitin.

Tämä on paljon sulattavaa! Ymmärtääksemme sen todella, sukellamme hieman syvemmälle siihen, miten `Future`-trait oikeasti toimii, erityisesti kiinnityksen ympärillä. Katso jälleen `Future`-traitin määrittely:

```rust
use std::pin::Pin;
use std::task::{Context, Poll};

pub trait Future {
    type Output;

    // Required method
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}
```

`cx`-parametri ja sen `Context`-tyyppi ovat avain siihen, miten ajoympäristö tietää, milloin tarkistaa minkäkin futuren ja pysyy silti laiskana. Taaskin yksityiskohdat ovat tämän luvun laajuuden ulkopuolella, ja yleensä sinun täytyy miettiä tätä vain kirjoittaessasi oman `Future`-toteutuksen. Keskitymme sen sijaan `self`:n tyyppiin, koska tämä on ensimmäinen kerta, kun näemme metodin, jossa `self`:llä on tyyppiannotaatio. `self`:n tyyppiannotaatio toimii kuten muiden funktioparametrien tyyppiannotaatiot, mutta kahdella keskeisellä erolla:

- Se kertoo Rustille, millaisen tyypin `self`:n täytyy olla, jotta metodia voidaan kutsua.
- Se ei voi olla mikä tahansa tyyppi. Se on rajoitettu siihen tyyppiin, jolle metodi on toteutettu, viittaukseen tai älykkääseen osoittimeen kyseiseen tyyppiin tai `Pin`:iin, joka käärii viittauksen kyseiseen tyyppiin.

Näemme lisää tästä syntaksista [luvussa 18][ch-18]<!-- ignore -->. Toistaiseksi riittää tietää, että jos haluamme pollata futurea tarkistaaksemme, onko se `Pending` vai `Ready(Output)`, tarvitsemme `Pin`:illä käärityn muuttuvan viittauksen tyyppiin.

`Pin` on kääre osoittimia muistuttaville tyypeille kuten `&`, `&mut`, `Box` ja `Rc`. (Teknisesti `Pin` toimii tyyppien kanssa, jotka toteuttavat `Deref`- tai `DerefMut`-traitit, mutta tämä on käytännössä vastaavaa kuin työskennellä vain viittausten ja älykkäiden osoittimien kanssa.) `Pin` ei itse ole osoitin eikä sillä ole omaa käyttäytymistä kuten `Rc`:llä ja `Arc`:illa viittaustenlaskennassa; se on puhtaasti työkalu, jota kääntäjä voi käyttää rajoittaakseen osoittimien käyttöä.

Muistaen, että `await` toteutetaan `poll`-kutsujen kautta, alkaa selittää aiemmin näkemämme virheilmoituksen, mutta se oli `Unpin`:n termeillä, ei `Pin`:n. Miten `Pin` liittyy siis `Unpin`:iin, ja miksi `Future` tarvitsee `self`:n olevan `Pin`-tyypissä `poll`:in kutsumiseksi?

Muista tämän luvun alusta, että futuren odotuspisteet käännetään tilakoneeksi ja kääntäjä varmistaa, että tilakone noudattaa Rustin normaaleja turvallisuussääntöjä, mukaan lukien lainauksen ja omistajuuden. Jotta tämä toimii, Rust katsoo, mitä dataa tarvitaan yhden odotuspisteen ja seuraavan odotuspisteen tai async-lohkon lopun välillä. Se luo sitten vastaavan variantin käännettyyn tilakoneeseen. Jokainen variantti saa tarvitsemansa pääsyn dataan, jota käytetään kyseisessä lähdekoodin osassa, joko ottamalla omistuksen datasta tai saamalla muuttuvan tai muuttumattoman viittauksen siihen.

Tähän asti kaikki hyvin: jos teemme jotain väärin omistajuuden tai viittausten suhteen tietyssä async-lohkossa, lainaustarkistin kertoo sen meille. Kun haluamme siirtää kyseistä lohkoa vastaavaa futurea — kuten siirtää sen `Vec`:iin käytettäväksi `join_all`:in kanssa tai palauttaa sen funktiosta — asiat monimutkaistuvat.

Kun siirrämme futurea — työntämällä sen tietorakenteeseen käytettäväksi `join_all`:in kanssa tai palauttamalla sen funktiosta — se tarkoittaa itse asiassa Rustin meille luoman tilakoneen siirtämistä. Ja toisin kuin useimmat muut tyypit Rustissa, async-lohkoille Rustin luomat futuret voivat päätyä viittaamaan itseensä minkä tahansa variantin kentissä, kuten yksinkertaistetussa kuvassa 17-4.

<figure>

<img alt="A single-column, three-row table representing a future, fut1, which has data values 0 and 1 in the first two rows and an arrow pointing from the third row back to the second row, representing an internal reference within the future." src="img/trpl17-04.svg" class="center" />

<figcaption>Kuva 17-4: Itseensä viittaava tietotyyppi</figcaption>

</figure>

Oletuksena kuitenkin mikä tahansa objekti, jolla on viittaus itseensä, on turvaton siirtää, koska viittaukset osoittavat aina sen todellisen muistiosoitteen, johon ne viittaavat (katso kuva 17-5). Jos siirrät itse tietorakenteen, nämä sisäiset viittaukset jäävät osoittamaan vanhaa sijaintia. Tuo muistisijainti on kuitenkin nyt virheellinen. Ensinnäkin sen arvoa ei päivitetä, kun teet muutoksia tietorakenteeseen. Toiseksi — ja tärkeämpänä — tietokone saa nyt käyttää tuon muistin uudelleen muihin tarkoituksiin! Saatat lopulta lukea täysin asiaan liittymätöntä dataa.

<figure>

<img alt="Two tables, depicting two futures, fut1 and fut2, each of which has one column and three rows, representing the result of having moved a future out of fut1 into fut2. The first, fut1, is grayed out, with a question mark in each index, representing unknown memory. The second, fut2, has 0 and 1 in the first and second rows and an arrow pointing from its third row back to the second row of fut1, representing a pointer that is referencing the old location in memory of the future before it was moved." src="img/trpl17-05.svg" class="center" />

<figcaption>Kuva 17-5: Itseensä viittaavan tietotyypin siirtämisen turvaton tulos</figcaption>

</figure>

Teoriassa Rust-kääntäjä voisi yrittää päivittää jokaisen viittauksen objektiin aina, kun sitä siirretään, mutta se voisi lisätä paljon suorituskykyyn liittyvää yläkulua, erityisesti jos koko viittausten verkko täytyy päivittää. Jos sen sijaan voisimme varmistaa, ettei kyseistä tietorakennetta _siirretä muistissa_, meidän ei tarvitsisi päivittää viittauksia. Tätä varten Rustin lainaustarkistin on olemassa: turvallisessa koodissa se estää sinua siirtämästä mitään kohdetta, johon on aktiivinen viittaus.

`Pin` rakentuu tämän päälle antaakseen meille juuri tarvitsemamme takuun. Kun _kiinnitämme_ arvon käärimällä osoittimen kyseiseen arvoon `Pin`:iin, sitä ei voi enää siirtää. Jos siis sinulla on `Pin<Box<SomeType>>`, kiinnität itse asiassa `SomeType`-arvon, _ei_ `Box`-osoitinta. Kuva 17-6 havainnollistaa tätä prosessia.

<figure>

<img alt="Three boxes laid out side by side. The first is labeled “Pin”, the second “b1”, and the third “pinned”. Within “pinned” is a table labeled “fut”, with a single column; it represents a future with cells for each part of the data structure. Its first cell has the value “0”, its second cell has an arrow coming out of it and pointing to the fourth and final cell, which has the value “1” in it, and the third cell has dashed lines and an ellipsis to indicate there may be other parts to the data structure. All together, the “fut” table represents a future which is self-referential. An arrow leaves the box labeled “Pin”, goes through the box labeled “b1” and terminates inside the “pinned” box at the “fut” table." src="img/trpl17-06.svg" class="center" />

<figcaption>Kuva 17-6: `Box`:in kiinnittäminen, joka osoittaa itseensä viittaavaan future-tyyppiin</figcaption>

</figure>

Itse asiassa `Box`-osoitin voi edelleen liikkua vapaasti. Muista: meidän täytyy varmistaa, että lopulta viitattu data pysyy paikallaan. Jos osoitin liikkuu, _mutta sen osoittama data_ on samassa paikassa, kuten kuvassa 17-7, ongelmaa ei ole. (Itsenäisenä harjoituksena tutustu tyyppien dokumentaatioon sekä `std::pin`-moduuliin ja yritä selvittää, miten tekisit tämän `Pin`:illä, joka käärii `Box`:in.) Keskeistä on, ettei itseensä viittaavaa tyyppiä voi siirtää, koska se on edelleen kiinnitetty.

<figure>

<img alt="Four boxes laid out in three rough columns, identical to the previous diagram with a change to the second column. Now there are two boxes in the second column, labeled “b1” and “b2”, “b1” is grayed out, and the arrow from “Pin” goes through “b2” instead of “b1”, indicating that the pointer has moved from “b1” to “b2”, but the data in “pinned” has not moved." src="img/trpl17-07.svg" class="center" />

<figcaption>Kuva 17-7: `Box`:in siirtäminen, joka osoittaa itseensä viittaavaan future-tyyppiin</figcaption>

</figure>

Useimmat tyypit ovat kuitenkin täysin turvallisia siirtää, vaikka ne sattuisivat olemaan `Pin`-osoittimen takana. Meidän täytyy miettiä kiinnitystä vain, kun kohteilla on sisäisiä viittauksia. Alkeisarvot kuten numerot ja totuusarvot ovat turvallisia, koska niissä ei selvästikään ole sisäisiä viittauksia. Myöskään useimmissa tyypeissä, joita normaalisti käytät Rustissa, ei ole ongelmaa. Voit esimerkiksi siirtää `Vec`:iä huoletta. Tähänastisen perusteella, jos sinulla on `Pin<Vec<String>>`, joudut tekemään kaiken `Pin`:in tarjoamien turvallisten mutta rajoittavien API:en kautta, vaikka `Vec<String>` on aina turvallinen siirtää, jos siihen ei ole muita viittauksia. Tarvitsemme tavan kertoa kääntäjälle, että on turvallista siirtää kohteita tapauksissa kuten tämä — ja siihen tulee `Unpin`.

`Unpin` on merkki-trait, samankaltainen kuin `Send`- ja `Sync`-traitit, joita näimme luvussa 16, eikä sillä siis ole omaa toiminnallisuutta. Merkki-traitit ovat olemassa vain kertoakseen kääntäjälle, että tietyn traitin toteuttavan tyypin käyttö tietyssä kontekstissa on turvallista. `Unpin` kertoo kääntäjälle, että tietyllä tyypillä _ei_ tarvitse ylläpitää takeita siitä, voidaanko kyseinen arvo turvallisesti siirtää.

<!--
  The inline `<code>` in the next block is to allow the inline `<em>` inside it,
  matching what NoStarch does style-wise, and emphasizing within the text here
  that it is something distinct from a normal type.
-->

Aivan kuten `Send`:n ja `Sync`:n kanssa, kääntäjä toteuttaa `Unpin`:in automaattisesti kaikille tyypeille, joille se voi todistaa sen olevan turvallista. Erityistapaus, jälleen samankaltainen kuin `Send`:n ja `Sync`:n kanssa, on tilanne, jossa `Unpin`:iä _ei_ toteuteta tyypille. Tämän merkintä on <code>impl !Unpin for <em>SomeType</em></code>, jossa <code><em>SomeType</em></code> on tyypin nimi, joka _tarvitsee_ ylläpitää näitä takeita ollakseen turvallinen aina, kun osoitin kyseiseen tyyppiin käytetään `Pin`:issä.

Toisin sanoen `Pin`:n ja `Unpin`:in suhteesta on pidettävä mielessä kaksi asiaa. Ensinnäkin `Unpin` on ”normaali” tapaus ja `!Unpin` on erikoistapaus. Toiseksi se, toteuttaako tyyppi `Unpin`:in vai `!Unpin`:in, _merkitsee_ vain, kun käytät kiinnitettyä osoitinta kyseiseen tyyppiin, kuten <code>Pin<&mut <em>SomeType</em>></code>.

Tehdään tästä konkreettista: ajattele `String`:iä. Siinä on pituus ja sen muodostavat Unicode-merkit. Voimme kääriä `String`:in `Pin`:iin, kuten kuvassa 17-8. `String` toteuttaa kuitenkin automaattisesti `Unpin`:in, kuten useimmat muut tyypit Rustissa.

<figure>

<img alt="A box labeled “Pin” on the left with an arrow going from it to a box labeled “String” on the right. The “String” box contains the data 5usize, representing the length of the string, and the letters “h”, “e”, “l”, “l”, and “o” representing the characters of the string “hello” stored in this String instance. A dotted rectangle surrounds the “String” box and its label, but not the “Pin” box." src="img/trpl17-08.svg" class="center" />

<figcaption>Kuva 17-8: `String`:in kiinnittäminen; katkoviiva osoittaa, että `String` toteuttaa `Unpin`-traitin eikä siten ole kiinnitetty</figcaption>

</figure>

Näin voimme tehdä asioita, jotka olisivat laittomia, jos `String` toteuttaisi `!Unpin`:in, kuten korvata yhden merkkijonon toisella täsmälleen samassa muistisijainnissa kuten kuvassa 17-9. Tämä ei riko `Pin`-sopimusta, koska `String`:illä ei ole sisäisiä viittauksia, jotka tekisivät siirtämisestä turvatonta. Siksi se toteuttaa `Unpin`:in eikä `!Unpin`:iä.

<figure>

<img alt="The same “hello” string data from the previous example, now labeled “s1” and grayed out. The “Pin” box from the previous example now points to a different String instance, one that is labeled “s2”, is valid, has a length of 7usize, and contains the characters of the string “goodbye”. s2 is surrounded by a dotted rectangle because it, too, implements the Unpin trait." src="img/trpl17-09.svg" class="center" />

<figcaption>Kuva 17-9: `String`:in korvaaminen täysin eri `String`:illä muistissa</figcaption>

</figure>

Nyt tiedämme tarpeeksi ymmärtääksemme listauksen 17-23 `join_all`-kutsusta raportoidut virheet. Alun perin yritimme siirtää async-lohkojen tuottamat futuret `Vec<Box<dyn Future<Output = ()>>>`:iin, mutta kuten olemme nähneet, näillä futureilla voi olla sisäisiä viittauksia, joten ne eivät automaattisesti toteuta `Unpin`:iä. Kun kiinnitämme ne, voimme välittää tuloksena olevan `Pin`-tyypin `Vec`:iin luottavaisin mielin, ettei futurejen taustalla olevaa dataa _siirretä_. Listaus 17-24 näyttää, miten koodi korjataan kutsumalla `pin!`-makroa siellä, missä kukin kolmesta futuresta määritellään, ja säätämällä trait-objektin tyyppiä.

<Listing number="17-24" caption="Futurejen kiinnittäminen, jotta ne voidaan siirtää vektoriin">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-24/src/main.rs:here}}
```

</Listing>

Tämä esimerkki kääntyy ja suorittuu nyt, ja voisimme lisätä tai poistaa futureja vektorista ajonaikana ja yhdistää ne kaikki.

`Pin` ja `Unpin` ovat tärkeimpiä matalan tason kirjastojen rakentamisessa tai kun rakennat itse ajoympäristön, eivät niinkään päivittäisessä Rust-koodissa. Kun näet nämä traitit virheilmoituksissa, sinulla on nyt kuitenkin parempi käsitys siitä, miten koodisi korjataan!

> Huom: Tämä `Pin`:n ja `Unpin`:in yhdistelmä mahdollistaa koko luokan monimutkaisten tyyppien turvallisen toteuttamisen Rustissa, jotka muuten olisivat haastavia, koska ne ovat itseensä viittaavia. `Pin`:ia vaativat tyypit esiintyvät yleisimmin async-Rustissa tänään, mutta silloin tällöin saatat nähdä niitä myös muissa konteksteissa.
>
> `Pin`:n ja `Unpin`:in toiminnan yksityiskohdat ja säännöt, joita niiden täytyy noudattaa, on käsitelty laajasti `std::pin`:in API-dokumentaatiossa, joten jos haluat oppia lisää, se on hyvä lähtökohta.
>
> Jos haluat ymmärtää, miten asiat toimivat vielä tarkemmin taustalla, katso [_Asynchronous Programming in Rust_][async-book] -kirjan luvut [2][under-the-hood]<!-- ignore --> ja [4][pinning]<!-- ignore -->.

### `Stream`-trait

Nyt kun ymmärrät `Future`-, `Pin`- ja `Unpin`-traitit syvemmin, voimme kääntää huomion `Stream`-traitiin. Kuten opit aiemmin luvussa, streamit muistuttavat asynkronisia iteraattoreita. Toisin kuin `Iterator` ja `Future`, `Stream`:illa ei kuitenkaan ole määrittelyä standardikirjastossa tämän kirjoitushetkellä, mutta `futures`-crate:stä on olemassa hyvin yleinen määrittely, jota käytetään koko ekosysteemissä.

Käydään läpi `Iterator`- ja `Future`-traitien määrittelyt ennen kuin katsomme, miten `Stream`-trait voisi yhdistää ne. `Iterator`:stä saamme käsitteen sarjasta: sen `next`-metodi tarjoaa `Option<Self::Item>`:in. `Future`:sta saamme käsitteen valmiudesta ajan kuluessa: sen `poll`-metodi tarjoaa `Poll<Self::Output>`:in. Esittääksemme kohteiden sarjaa, joka tulee valmiiksi ajan kuluessa, määrittelemme `Stream`-traitin, joka yhdistää nämä ominaisuudet:

```rust
use std::pin::Pin;
use std::task::{Context, Poll};

trait Stream {
    type Item;

    fn poll_next(
        self: Pin<&mut Self>,
        cx: &mut Context<'_>
    ) -> Poll<Option<Self::Item>>;
}
```

`Stream`-trait määrittelee assosioituneen tyypin `Item` streamin tuottamien kohteiden tyypille. Tämä on samankaltainen kuin `Iterator`:issä, jossa kohteita voi olla nollasta moneen, ja erilainen kuin `Future`:issa, jossa on aina yksi `Output`, vaikka se olisi yksikkötyyppi `()`.

`Stream` määrittelee myös metodin näiden kohteiden hakemiseen. Kutsumme sitä `poll_next`:iksi korostaaksemme, että se pollaa samalla tavalla kuin `Future::poll` ja tuottaa kohteiden sarjan samalla tavalla kuin `Iterator::next`. Sen palautustyyppi yhdistää `Poll`:in ja `Option`:in. Ulompi tyyppi on `Poll`, koska valmius täytyy tarkistaa aivan kuten futuressa. Sisempi tyyppi on `Option`, koska sen täytyy ilmaista, onko viestejä enempää, aivan kuten iteraattorissa.

Jokin hyvin samankaltainen määrittely tulee todennäköisesti osaksi Rustin standardikirjastoa. Sillä välin se on osa useimpien ajoympäristöjen työkalupakkia, joten voit luottaa siihen, ja kaiken seuraavan pitäisi yleensä päteä!

[”Streamit: futuret peräkkäin”][streams]<!-- ignore --> -osion esimerkeissä emme kuitenkaan käyttäneet `poll_next`:iä _tai_ `Stream`:iä, vaan `next`:iä ja `StreamExt`:iä. _Voisimme_ työskennellä suoraan `poll_next`-API:n kanssa kirjoittamalla omat `Stream`-tilakoneemme käsin, aivan kuten _voisimme_ työskennellä futurejen kanssa suoraan niiden `poll`-metodin kautta. `await`:in käyttö on kuitenkin paljon miellyttävämpää, ja `StreamExt`-trait tarjoaa `next`-metodin, jotta voimme tehdä juuri sen:

```rust
{{#rustdoc_include ../listings/ch17-async-await/no-listing-stream-ext/src/lib.rs:here}}
```

<!--
TODO: update this if/when tokio/etc. update their MSRV and switch to using async functions
in traits, since the lack thereof is the reason they do not yet have this.
-->

> Huom: Todellinen määrittely, jota käytimme aiemmin luvussa, näyttää hieman erilaiselta, koska se tukee Rust-versioita, jotka eivät vielä tukeneet async-funktioiden käyttöä traiteissa. Sen vuoksi se näyttää tältä:
>
> ```rust,ignore
> fn next(&mut self) -> Next<'_, Self> where Self: Unpin;
> ```
>
> `Next`-tyyppi on `struct`, joka toteuttaa `Future`:n ja antaa meille nimetä `self`-viittauksen eliniän `Next<'_, Self>`:llä, jotta `await` voi toimia tämän metodin kanssa.

`StreamExt`-trait on myös kaikkien streamien kanssa käytettävien mielenkiintoisten metodien koti. `StreamExt` toteutetaan automaattisesti jokaiselle tyypille, joka toteuttaa `Stream`:in, mutta nämä traitit on määritelty erikseen, jotta yhteisö voi iteroida kätevyys-API:ja vaikuttamatta perustavanlaatuiseen traitiin.

`trpl`-crate:ssä käytetyssä `StreamExt`-versiossa trait määrittelee `next`-metodin lisäksi myös oletustoteutuksen `next`:lle, joka käsittelee oikein `Stream::poll_next`:in kutsumisen yksityiskohdat. Tämä tarkoittaa, että vaikka joudut kirjoittamaan oman streamaavan tietotyypin, sinun täytyy toteuttaa _vain_ `Stream`, ja kuka tahansa tietotyyppiäsi käyttävä voi käyttää `StreamExt`:iä ja sen metodeja automaattisesti.

Tämä on kaikki, mitä käsittelemme näiden traitien matalamman tason yksityiskohdista. Lopuksi tarkastellaan, miten futuret (mukaan lukien streamit), tehtävät ja säikeet sopivat yhteen!

[message-passing]: ch17-02-concurrency-with-async.md#sending-data-between-two-tasks-using-message-passing
[ch-18]: ch18-00-oop.html
[async-book]: https://rust-lang.github.io/async-book/
[under-the-hood]: https://rust-lang.github.io/async-book/02_execution/01_chapter.html
[pinning]: https://rust-lang.github.io/async-book/04_pinning/01_chapter.html
[first-async]: ch17-01-futures-and-syntax.html#our-first-async-program
[any-number-futures]: ch17-03-more-futures.html#working-with-any-number-of-futures
[streams]: ch17-04-streams.html
