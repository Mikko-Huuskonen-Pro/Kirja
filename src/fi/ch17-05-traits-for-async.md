## Tarkempi katsaus asynkronisuuden traitteihin

<!-- Old headings. Do not remove or links may break. -->

<a id="digging-into-the-traits-for-async"></a>

Koko luvun ajan olemme käyttäneet `Future`-, `Pin`-, `Unpin`-, `Stream`- ja `StreamExt`-traitteja eri tavoin. Tähän asti olemme kuitenkin vältelleet sukeltamasta liian syvälle niiden toiminnan tai yhteensopivuuden yksityiskohtiin, mikä on useimmiten ihan hyvä päivittäisessä Rust-työssäsi. Joskus kohtaat kuitenkin tilanteita, joissa sinun täytyy ymmärtää hieman enemmän näitä yksityiskohtia. Tässä osiossa syvennymme juuri sen verran, että ne auttavat näissä tilanteissa, jättäen _todella_ syvän sukelluksen muulle dokumentaatiolle.

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

Tämä trait-määritelmä sisältää joukon uusia tyyppejä ja myös syntaksia, jota emme ole nähneet aiemmin, joten käydään määritelmä läpi pala kerrallaan.

Ensinnäkin `Future`-traitin assosioitu tyyppi `Output` kertoo, mihin future ratkeaa. Tämä on analoginen `Iterator`-traitin assosioituneelle tyypille `Item`. Toiseksi `Future`-traitilla on myös `poll`-metodi, joka ottaa erityisen `Pin`-viitteen `self`-parametrilleen ja muuttuvan viitteen `Context`-tyyppiin, ja palauttaa `Poll<Self::Output>`-tyypin. Puhumme `Pin`- ja `Context`-tyypeistä hetken kuluttua. Toistaiseksi keskitytään siihen, mitä metodi palauttaa, eli `Poll`-tyyppiin:

```rust
enum Poll<T> {
    Ready(T),
    Pending,
}
```

Tämä `Poll`-tyyppi on samankaltainen kuin `Option`. Siinä on yksi variantti, jolla on arvo, `Ready(T)`, ja yksi, jolla ei ole, `Pending`. `Poll` tarkoittaa kuitenkin jotain aivan erilaista kuin `Option`! `Pending`-variantti ilmaisee, että futuurilla on vielä työtä tekemättä, joten kutsujan täytyy tarkistaa uudelleen myöhemmin. `Ready`-variantti ilmaisee, että future on saanut työnsä valmiiksi ja `T`-arvo on saatavilla.

> Huom: Useimmilla futuureilla kutsujan ei pitäisi kutsua `poll`-metodia uudelleen sen jälkeen, kun future on palauttanut `Ready`-arvon. Monet futuurit panikoivat, jos niitä pollataan uudelleen valmiiksi tultuaan. Futuurit, joita on turvallista pollata uudelleen, sanovat sen eksplisiittisesti dokumentaatiossaan. Tämä on samankaltaista kuin `Iterator::next`-metodin käyttäytyminen.

Kun näet koodia, joka käyttää `await`-avainsanaa, Rust kääntää sen kulissien takana koodiksi, joka kutsuu `poll`-metodia. Jos katsot takaisin listaukseen 17-4, jossa tulostimme yhden URL-osoitteen sivun otsikon sen ratkettua, Rust kääntää sen joksikin tämän kaltaiseksi (vaikkakaan ei täsmälleen tällaiseksi):

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

Mitä meidän pitäisi tehdä, kun future on vielä `Pending`-tilassa? Tarvitsemme jonkin tavan yrittää uudelleen, ja uudelleen, ja uudelleen, kunnes future on vihdoin valmis. Toisin sanoen tarvitsemme silmukan:

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

Jos Rust kääntäisi sen täsmälleen tällaiseksi koodiksi, jokainen `await` estäisi suorituksen — juuri päinvastoin kuin mitä tavoittelimme! Sen sijaan Rust varmistaa, että silmukka voi luovuttaa hallinnan jollekin, joka voi keskeyttää työn tämän futuurin parissa tehdäkseen työtä muiden futuurien kanssa ja tarkistaakseen tämän futuurin uudelleen myöhemmin. Kuten olemme nähneet, tämä jokin on asynkroninen ajoaikamalli, ja tämä ajoitus- ja koordinointityö on yksi sen päätehtävistä.

Aikaisemmin luvussa kuvasimme odottamista `rx.recv`-kutsun parissa. `recv`-kutsu palauttaa futuurin, ja futuurin odottaminen pollaa sitä. Huomasimme, että ajoaikamalli keskeyttää futuurin, kunnes se on valmis joko `Some(message)`- tai `None`-arvolla, kun kanava sulkeutuu. Syvemmällä ymmärryksellämme `Future`-traitista, ja erityisesti `Future::poll`-metodista, näemme miten se toimii. Ajoaikamalli tietää, että future ei ole valmis, kun se palauttaa `Poll::Pending`-arvon. Päinvastoin ajoaikamalli tietää, että future _on_ valmis ja edistää sitä, kun `poll` palauttaa `Poll::Ready(Some(message))`- tai `Poll::Ready(None)`-arvon.

Tarkat yksityiskohdat siitä, miten ajoaikamalli tekee tämän, ylittävät tämän kirjan laajuuden, mutta keskeistä on nähdä futuurien perusmekaniikka: ajoaikamalli _pollaa_ jokaista futuuria, josta se on vastuussa, ja laittaa futuurin takaisin nukkumaan, kun se ei ole vielä valmis.

<!-- Old headings. Do not remove or links may break. -->

<a id="pinning-and-the-pin-and-unpin-traits"></a>

### `Pin`- ja `Unpin`-traitit

Kun esittelimme kiinnittämisen (_pinning_) idean listauksessa 17-16, kohtasimme hyvin mutkikkaan virheilmoituksen. Tässä on jälleen sen olennainen osa:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-16
cargo build
copy *only* the final `error` block from the errors
-->

```text
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

Tämä virheilmoitus kertoo meille paitsi sen, että meidän täytyy kiinnittää arvot, myös sen, miksi kiinnittäminen vaaditaan. `trpl::join_all`-funktio palauttaa rakenteen nimeltä `JoinAll`. Tämä rakenne on geneerinen tyypin `F` suhteen, jota rajoitetaan toteuttamaan `Future`-trait. Futuurin suora odottaminen `await`-avainsanalla kiinnittää futuurin implisiittisesti. Siksi emme tarvitse `pin!`-makroa kaikkialla, missä haluamme odottaa futuureja.

Emme kuitenkaan odota futuuria suoraan tässä. Sen sijaan rakennamme uuden futuurin, `JoinAll`-rakenteen, välittämällä futuurikokoelman `join_all`-funktiolle. `join_all`-funktion signatuuri vaatii, että kokoelman kohteiden tyypit kaikki toteuttavat `Future`-traitin, ja `Box<T>` toteuttaa `Future`-traitin vain, jos sen käärimä `T` on future, joka toteuttaa `Unpin`-traitin.

Se on paljon sulattavaa! Ymmärtääksemme sen todella, sukeltakaamme hieman syvemmälle siihen, miten `Future`-trait oikeasti toimii, erityisesti _kiinnittämisen_ (_pinning_) osalta.

Katso jälleen `Future`-traitin määritelmää:

```rust
use std::pin::Pin;
use std::task::{Context, Poll};

pub trait Future {
    type Output;

    // Required method
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}
```

`cx`-parametri ja sen `Context`-tyyppi ovat avain siihen, miten ajoaikamalli oikeasti tietää, milloin tarkistaa minkä tahansa futuurin ja silti pysyy laiskana. Taaskin, yksityiskohdat siitä, miten se toimii, ylittävät tämän luvun laajuuden, ja sinun täytyy yleensä ajatella tätä vain kirjoittaessasi mukautetun `Future`-toteutuksen. Keskitytään sen sijaan `self`-parametrin tyyppiin, koska tämä on ensimmäinen kerta, kun näemme metodin, jossa `self`:llä on tyyppiannotaatio. `self`-parametrin tyyppiannotaatio toimii kuten muidenkin funktioiden parametrien tyyppiannotaatiot, mutta kahdella keskeisellä erolla:

- Se kertoo Rustille, minkä tyyppisen `self`-parametrin täytyy olla, jotta metodia voidaan kutsua.

- Se ei voi olla mikä tahansa tyyppi. Se on rajoitettu tyyppiin, jolle metodi on toteutettu, viitteeseen tai älykkääseen osoittimeen kyseiseen tyyppiin, tai `Pin`-rakenteeseen, joka käärii viitteen kyseiseen tyyppiin.

Näemme lisää tästä syntaksista [luvussa 18][ch-18]<!-- ignore -->. Toistaiseksi riittää tietää, että jos haluamme pollata futuuria tarkistaaksemme, onko se `Pending`- vai `Ready(Output)`-tilassa, tarvitsemme `Pin`-käärittyn muuttuvan viitteen tyyppiin.

`Pin` on kääre osoittimia muistuttaville tyypeille, kuten `&`, `&mut`, `Box` ja `Rc`. (Teknisesti `Pin` toimii tyyppien kanssa, jotka toteuttavat `Deref`- tai `DerefMut`-traitit, mutta tämä on käytännössä vastaavaa kuin työskentely pelkästään osoittimien kanssa.) `Pin` ei ole itse osoitin eikä sillä ole omaa käyttäytymistään kuten `Rc`- ja `Arc`-tyypeillä on viitelaskennan kanssa; se on puhtaasti työkalu, jota kääntäjä voi käyttää osoittimien käytön rajoitteiden pakottamiseen.

Muistaessamme, että `await` toteutetaan `poll`-kutsujen kautta, alkaa selkiytyä aiemmin näkemämme virheilmoitus, mutta se oli `Unpin`-termin suhteen, ei `Pin`-termin. Miten `Pin` liittyy `Unpin`-traitiin, ja miksi `Future` tarvitsee `self`-parametrin olevan `Pin`-tyypissä `poll`-metodin kutsumiseksi?

Muista tämän luvun aiemmasta osiosta, että futuurin odotuspisteet käännetään tilakoneeksi, ja kääntäjä varmistaa, että tilakone noudattaa kaikkia Rustin tavallisia turvallisuussääntöjä, mukaan lukien lainaamisen ja omistajuuden. Tämän toimimiseksi Rust katsoo, mitä dataa tarvitaan yhden odotuspisteen ja seuraavan odotuspisteen tai asynkronisen lohkon lopun välillä. Se luo sitten vastaavan variantin käännettyyn tilakoneeseen. Jokainen variantti saa tarvitsemansa pääsyn dataan, jota käytetään kyseisessä lähdekoodin osassa, joko ottamalla omistajuuden datasta tai saamalla muuttuvan tai muuttumattoman viitteen siihen.

Tähän asti kaikki hyvin: jos teemme virheen omistajuudessa tai viitteissä tietyssä asynkronisessa lohkossa, lainaustarkistin kertoo meille. Kun haluamme siirtää futuuria, joka vastaa kyseistä lohkoa — kuten siirtää sen `Vec`-rakenteeseen välittääksemme sen `join_all`-funktiolle tai palauttaa sen funktiosta — asiat muuttuvat hankalammiksi.

Kun siirrämme futuuria — joko työntämällä sen tietorakenteeseen käytettäväksi iteraattorina `join_all`-funktion kanssa tai palauttamalla sen funktiosta — se tarkoittaa itse asiassa Rustin luoman tilakoneen siirtämistä. Ja toisin kuin useimmat muut Rustin tyypit, Rustin luomat futuurit asynkronisille lohkoille voivat päättyä viitteisiin itseensä minkä tahansa variantin kentissä, kuten yksinkertaistetussa kuvassa kuvassa 17-4.

<figure>

<img alt="A single-column, three-row table representing a future, fut1, which has data values 0 and 1 in the first two rows and an arrow pointing from the third row back to the second row, representing an internal reference within the future." src="img/trpl17-04.svg" class="center" />

<figcaption>Kuva 17-4: Itseensä viittaava datatyyppi.</figcaption>

</figure>

Oletuksena kuitenkin mikä tahansa objekti, jolla on viite itseensä, on turvatonta siirtää, koska viitteet osoittavat aina niihin viitattujen kohteiden todelliseen muistiosoitteeseen (katso kuva 17-5). Jos siirrät itse datarakenteen, nämä sisäiset viitteet jäävät osoittamaan vanhaa sijaintia. Tämä muistisijainti on kuitenkin nyt virheellinen. Ensinnäkin sen arvoa ei päivitetä, kun teet muutoksia datarakenteeseen. Toiseksi — ja tärkeämpänä — tietokone voi nyt käyttää tämän muistin uudelleen muihin tarkoituksiin! Saatat lopulta lukea täysin asiaan liittymätöntä dataa.

Teoriassa Rust-kääntäjä voisi yrittää päivittää jokaisen viitteen objektiin aina kun sitä siirretään, mutta se voisi lisätä paljon suorituskykyyn liittyvää yleiskustannusta, erityisesti jos koko viiteverkko täytyy päivittää. Jos sen sijaan voisimme varmistaa, että kyseinen datarakenne _ei siirry muistissa_, meidän ei tarvitsisi päivittää viitteitä. Tämä on juuri se, mitä Rustin lainaustarkistin vaatii: turvallisessa koodissa se estää sinua siirtämästä mitään kohdetta, johon on aktiivinen viite.

`Pin` rakentuu tämän päälle antaakseen meille juuri tarvitsemamme takuun. Kun _kiinnitämme_ arvon käärimällä osoittimen kyseiseen arvoon `Pin`-rakenteeseen, arvo ei voi enää siirtyä. Näin ollen, jos sinulla on `Pin<Box<SomeType>>`, kiinnität itse asiassa `SomeType`-arvon, _ei_ `Box`-osoitinta. Kuva 17-6 havainnollistaa tätä prosessia.

<figure>

<img alt="Three boxes laid out side by side. The first is labeled “Pin”, the second “b1”, and the third “pinned”. Within “pinned” is a table labeled “fut”, with a single column; it represents a future with cells for each part of the data structure. Its first cell has the value “0”, its second cell has an arrow coming out of it and pointing to the fourth and final cell, which has the value “1” in it, and the third cell has dashed lines and an ellipsis to indicate there may be other parts to the data structure. All together, the “fut” table represents a future which is self-referential. An arrow leaves the box labeled “Pin”, goes through the box labeled “b1” and has terminates inside the “pinned” box at the “fut” table." src="img/trpl17-06.svg" class="center" />

<figcaption>Kuva 17-6: `Box`-osoittimen kiinnittäminen, joka osoittaa itseensä viittaavaan future-tyyppiin.</figcaption>

</figure>

Itse asiassa `Box`-osoitin voi edelleen liikkua vapaasti. Muista: meidän täytyy varmistaa, että lopulta viitattu data pysyy paikallaan. Jos osoitin liikkuu, _mutta data, johon se osoittaa, on samassa paikassa_, kuten kuvassa 17-7, ongelmaa ei ole. Itsenäisenä harjoituksena tutustu tyyppien dokumentaatioon sekä `std::pin`-moduuliin ja yritä selvittää, miten tekisit tämän `Pin`-rakenteen käärimällä `Box`-osoittimen.) Keskeistä on, että itseensä viittaava tyyppi itsessään ei voi siirtyä, koska se on edelleen kiinnitetty.

<figure>

<img alt="Four boxes laid out in three rough columns, identical to the previous diagram with a change to the second column. Now there are two boxes in the second column, labeled “b1” and “b2”, “b1” is grayed out, and the arrow from “Pin” goes through “b2” instead of “b1”, indicating that the pointer has moved from “b1” to “b2”, but the data in “pinned” has not moved." src="img/trpl17-07.svg" class="center" />

<figcaption>Kuva 17-7: `Box`-osoittimen siirtäminen, joka osoittaa itseensä viittaavaan future-tyyppiin.</figcaption>

</figure>

Useimmat tyypit ovat kuitenkin täysin turvallisia siirtää, vaikka ne sattuisivat olemaan `Pin`-kääreen takana. Meidän täytyy ajatella kiinnittämistä vain, kun kohteilla on sisäisiä viitteitä. Alkeisarvot kuten numerot ja totuusarvot eivät tietenkään sisällä sisäisiä viitteitä, joten ne ovat turvallisia. Eivätkä useimmat tyypit, joiden kanssa normaalisti työskentelet Rustissa. Voit esimerkiksi siirtää `Vec`-rakennetta huolehtimatta. Tähänastisen näkemämme perusteella, jos sinulla on `Pin<Vec<String>>`, joudut tekemään kaiken `Pin`-rakenteen tarjoamien turvallisten mutta rajoittavien API:en kautta, vaikka `Vec<String>` on aina turvallista siirtää, jos siihen ei ole muita viitteitä. Tarvitsemme tavan kertoa kääntäjälle, että on ihan ok siirtää kohteita tapauksissa kuten tämä — ja siihen `Unpin` tulee mukaan.

`Unpin` on merkintätrait (_marker trait_), samankaltainen kuin `Send`- ja `Sync`-traitit, joita näimme luvussa 16, eikä sillä siten ole omaa toiminnallisuutta. Merkintätraitit ovat olemassa vain kertoakseen kääntäjälle, että on turvallista käyttää tiettyä traitia toteuttavaa tyyppiä tietyssä kontekstissa. `Unpin` kertoo kääntäjälle, että tietyllä tyypillä _ei_ tarvitse ylläpitää takuita siitä, voidaanko kyseinen arvo turvallisesti siirtää.

<!--
  The inline `<code>` in the next block is to allow the inline `<em>` inside it,
  matching what NoStarch does style-wise, and emphasizing within the text here
  that it is something distinct from a normal type.
-->

Aivan kuten `Send`- ja `Sync`-traitien kanssa, kääntäjä toteuttaa `Unpin`-traitin automaattisesti kaikille tyypeille, joille se voi todistaa sen olevan turvallista. Erityistapaus, jälleen samankaltainen kuin `Send`- ja `Sync`-traitien kanssa, on tilanne, jossa `Unpin`-traitia _ei_ toteuteta tyypille. Tämän merkintä on <code>impl !Unpin for <em>SomeType</em></code>, missä
<code><em>SomeType</em></code> on tyypin nimi, jonka _täytyy_ ylläpitää näitä takuita turvallisuuden vuoksi aina kun osoitin kyseiseen tyyppiin käytetään `Pin`-rakenteessa.

Toisin sanoen, `Pin`- ja `Unpin`-traitien suhteesta on pidettävä mielessä kaksi asiaa. Ensinnäkin `Unpin` on ”normaali” tapaus ja `!Unpin` on erikoistapaus. Toiseksi sillä, toteuttaako tyyppi `Unpin`- vai `!Unpin`-traitin, on merkitystä _vain_ kun käytät kiinnitettyä osoitinta kyseiseen tyyppiin, kuten <code>Pin<&mut
<em>SomeType</em>></code>.

Tehdäksemme tästä konkreettisen, ajattele `String`-tyyppiä: sillä on pituus ja sitä muodostavat Unicode-merkit. Voimme kääriä `String`-tyypin `Pin`-rakenteeseen, kuten kuvassa 17-8. `String` toteuttaa kuitenkin automaattisesti `Unpin`-traitin, kuten useimmat muutkin Rustin tyypit.

<figure>

<img alt="Concurrent work flow" src="img/trpl17-08.svg" class="center" />

<figcaption>Kuva 17-8: `String`-tyypin kiinnittäminen; katkoviiva osoittaa, että `String` toteuttaa `Unpin`-traitin eikä siten ole kiinnitetty.</figcaption>

</figure>

Tämän seurauksena voimme tehdä asioita, jotka olisivat laittomia, jos `String` toteuttaisi `!Unpin`-traitin sen sijaan, kuten korvata yhden merkkijonon toisella täsmälleen samassa muistisijainnissa kuten kuvassa 17-9. Tämä ei riko `Pin`-sopimusta, koska `String`-tyypillä ei ole sisäisiä viitteitä, jotka tekisivät sen siirtämisestä turvatonta! Siksi se toteuttaa `Unpin`-traitin eikä `!Unpin`-traitia.

<figure>

<img alt="Concurrent work flow" src="img/trpl17-09.svg" class="center" />

<figcaption>Kuva 17-9: `String`-tyypin korvaaminen täysin eri `String`-tyypillä muistissa.</figcaption>

</figure>

Nyt tiedämme tarpeeksi ymmärtääksemme listauksen 17-17 `join_all`-kutsusta raportoidut virheet. Alun perin yritimme siirtää asynkronisten lohkojen tuottamat futuurit `Vec<Box<dyn Future<Output = ()>>>`-rakenteeseen, mutta kuten olemme nähneet, näillä futuureilla voi olla sisäisiä viitteitä, joten ne eivät toteuta `Unpin`-traitia. Ne täytyy kiinnittää, ja sitten voimme välittää `Pin`-tyypin `Vec`-rakenteeseen varmana siitä, että futuurien taustalla oleva data _ei_ siirry.

`Pin`- ja `Unpin`-traitit ovat pääosin tärkeitä matalan tason kirjastojen rakentamisessa tai kun rakennat itse ajoaikamallia, eivät niinkään päivittäisessä Rust-koodissa. Kun näet näitä traitteja virheilmoituksissa, sinulla on nyt kuitenkin parempi käsitys siitä, miten korjata koodisi!

> Huom: Tämä `Pin`- ja `Unpin`-traitien yhdistelmä mahdollistaa kokonaisen luokan monimutkaisten tyyppien turvallisen toteuttamisen Rustissa, jotka muuten olisivat haastavia, koska ne ovat itseensä viittaavia. Tyypit, jotka vaativat `Pin`-traitin, esiintyvät yleisimmin asynkronisessa Rustissa nykyään, mutta silloin tällöin saatat nähdä niitä muissakin konteksteissa.
>
> `Pin`- ja `Unpin`-traitien toiminnan ja niiden ylläpidettävien sääntöjen yksityiskohdat on käsitelty laajasti `std::pin`-moduulin API-dokumentaatiossa, joten jos haluat oppia lisää, se on erinomainen paikka aloittaa.
>
> Jos haluat ymmärtää asioita vielä tarkemmin kulissien takana, katso [_Asynchronous Programming in Rust_][async-book] -kirjan [luvut 2][under-the-hood] ja [4][pinning].

### `Stream`-trait

Nyt kun sinulla on syvempi käsitys `Future`-, `Pin`- ja `Unpin`-traitien toiminnasta, voimme kääntää huomiomme `Stream`-traitiin. Kuten opit aiemmin luvussa, streamit ovat samankaltaisia kuin asynkroniset iteraattorit. Toisin kuin `Iterator`- ja `Future`-traitit, `Stream`-traitilla ei kuitenkaan ole määritelmää standardikirjastossa tämän kirjoitushetkellä, mutta ekosysteemissä on _hyvin_ yleinen määritelmä `futures`-kirjastosta.

Katsotaan `Iterator`- ja `Future`-traitien määritelmiä ennen kuin tarkastelemme, miten `Stream`-trait voisi yhdistää ne. `Iterator`-traitista saamme idean sarjasta: sen `next`-metodi tarjoaa `Option<Self::Item>`-tyypin. `Future`-traitista saamme idean valmiudesta ajan myötä: sen `poll`-metodi tarjoaa `Poll<Self::Output>`-tyypin. Edustaaksemme kohteiden sarjaa, jotka valmistuvat ajan myötä, määrittelemme `Stream`-traitin, joka yhdistää nämä ominaisuudet:

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

`Stream`-trait määrittelee assosioituneen tyypin `Item` streamin tuottamien kohteiden tyypille. Tämä on samankaltaista kuin `Iterator`-traitissa, jossa voi olla nollasta moneen kohdetta, ja erilaista kuin `Future`-traitissa, jossa on aina yksi `Output`, vaikka se olisi yksikkötyyppi `()`.

`Stream` määrittelee myös metodin näiden kohteiden hakemiseksi. Kutsumme sitä `poll_next`-metodiksi korostaaksemme, että se pollaa samalla tavalla kuin `Future::poll` ja tuottaa kohteiden sarjan samalla tavalla kuin `Iterator::next`. Sen paluutyyppi yhdistää `Poll`- ja `Option`-tyypit. Ulompi tyyppi on `Poll`, koska valmius täytyy tarkistaa aivan kuten futuurin kanssa. Sisempi tyyppi on `Option`, koska sen täytyy ilmaista, onko viestejä enemmän, aivan kuten iteraattorin kanssa.

Jokin hyvin samankaltainen kuin tämä määritelmä päätyy todennäköisesti osaksi Rustin standardikirjastoa. Sillä välin se on osa useimpien ajoaikamallien työkalupakkia, joten voit luottaa siihen, ja kaiken sen, mitä käsittelemme seuraavaksi, pitäisi yleensä päteä!

Streamausosiota esimerkissämme emme kuitenkaan käyttäneet `poll_next`-metodia _tai_ `Stream`-traitia, vaan käytimme `next`-metodia ja `StreamExt`-traitia. Voisimme _tietysti_ työskennellä suoraan `poll_next`-API:n kanssa kirjoittamalla omat `Stream`-tilakoneemme, aivan kuten voisimme työskennellä futuurien kanssa suoraan niiden `poll`-metodin kautta. `await`-avainsanan käyttö on kuitenkin paljon mukavampaa, ja `StreamExt`-trait tarjoaa `next`-metodin, jotta voimme tehdä juuri niin:

```rust
{{#rustdoc_include ../listings/ch17-async-await/no-listing-stream-ext/src/lib.rs:here}}
```

<!--
TODO: update this if/when tokio/etc. update their MSRV and switch to using async functions
in traits, since the lack thereof is the reason they do not yet have this.
-->

> Huom: Todellinen määritelmä, jota käytimme aiemmin luvussa, näyttää hieman erilaiselta kuin tämä, koska se tukee Rust-versioita, jotka eivät vielä tukeneet asynkronisten funktioiden käyttöä traitteissa. Tämän seurauksena se näyttää tältä:
>
> ```rust,ignore
> fn next(&mut self) -> Next<'_, Self> where Self: Unpin;
> ```
>
> `Next`-tyyppi on `struct`, joka toteuttaa `Future`-traitin ja antaa meille mahdollisuuden nimetä viitteen `self`-parametriin elinaikana `Next<'_, Self>`-syntaksilla, jotta `await` voi toimia tämän metodin kanssa.

`StreamExt`-trait on myös kaikkien streamien kanssa käytettävien mielenkiintoisten metodien koti. `StreamExt` toteutetaan automaattisesti jokaiselle tyypille, joka toteuttaa `Stream`-traitin, mutta nämä traitit on määritelty erikseen, jotta yhteisö voi iteroida kätevyys-API:en parissa vaikuttamatta perustavanlaatuiseen traitiin.

`trpl`-kirjastossa käytetyssä `StreamExt`-traitin versiossa trait ei ainoastaan määrittele `next`-metodia, vaan tarjoaa myös oletustoteutuksen `next`-metodille, joka käsittelee oikein `Stream::poll_next`-metodin kutsumisen yksityiskohdat. Tämä tarkoittaa, että vaikka sinun täytyy kirjoittaa oma streaming-datatyyppisi, sinun _täytyy_ vain toteuttaa `Stream`-trait, ja kuka tahansa, joka käyttää datatyyppiäsi, voi käyttää `StreamExt`-traitia ja sen metodeja sen kanssa automaattisesti.

Tämä on kaikki, mitä käsittelemme näiden traittien matalan tason yksityiskohdista. Lopuksi tarkastellaan, miten futuurit (mukaan lukien streamit), tehtävät ja säikeet sopivat yhteen!

[ch-18]: ch18-00-oop.html
[async-book]: https://rust-lang.github.io/async-book/
[under-the-hood]: https://rust-lang.github.io/async-book/02_execution/01_chapter.html
[pinning]: https://rust-lang.github.io/async-book/04_pinning/01_chapter.html
[first-async]: ch17-01-futures-and-syntax.html#our-first-async-program
[any-number-futures]: ch17-03-more-futures.html#working-with-any-number-of-futures
