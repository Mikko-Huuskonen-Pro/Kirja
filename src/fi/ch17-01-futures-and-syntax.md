## Futuret ja async-syntaksi

Asynkronisen ohjelmoinnin keskeiset elementit Rustissa ovat _futuret_ sekä Rustin `async`- ja `await`-avainsanat.

_future_ on arvo, joka ei ehkä ole valmis nyt, mutta tulee valmiiksi jossain vaiheessa tulevaisuudessa. (Sama käsite esiintyy monissa kielissä, joskus muilla nimillä kuten _task_ tai _promise_.) Rust tarjoaa `Future`-traitin rakennuspalikkana, jotta eri async-operaatiot voidaan toteuttaa eri tietorakenteilla mutta yhteisellä rajapinnalla. Rustissa futuret ovat tyyppejä, jotka toteuttavat `Future`-traitin. Jokainen future sisältää omat tietonsa edistymisestä ja siitä, mitä ”valmis” tarkoittaa.

Voit käyttää `async`-avainsanaa lohkoissa ja funktioissa määrittääksesi, että ne voidaan keskeyttää ja jatkaa. Async-lohkon tai async-funktion sisällä voit käyttää `await`-avainsanaa _odottaaksesi futurea_ (eli odottaaksesi, että se tulee valmiiksi). Jokainen kohta, jossa odotat futurea async-lohkon tai -funktion sisällä, on mahdollinen paikka, jossa kyseinen lohko tai funktio voi pysähtyä ja jatkaa. Prosessia, jossa tarkistetaan futurelta, onko sen arvo jo saatavilla, kutsutaan _pollaukseksi_.

Joissakin muissa kielissä, kuten C#:ssa ja JavaScriptissä, käytetään myös `async`- ja `await`-avainsanoja async-ohjelmointiin. Jos tunnet nämä kielet, saatat huomata merkittäviä eroja siinä, miten Rust käsittelee syntaksia. Siihen on hyvä syy, kuten näemme!

Kun kirjoitamme async-Rustia, käytämme `async`- ja `await`-avainsanoja useimman aikaa. Rust kääntää ne vastaavaksi koodiksi, joka käyttää `Future`-traitiä, aivan kuten se kääntää `for`-silmukat vastaavaksi koodiksi, joka käyttää `Iterator`-traitiä. Koska Rust tarjoaa `Future`-traitin, voit kuitenkin myös toteuttaa sen omille tietotyypeillesi tarvittaessa. Monet tämän luvun funktiot palauttavat tyyppejä, joilla on oma `Future`-toteutuksensa. Palaamme traitin määrittelyyn luvun lopussa ja syvennymme siihen, miten se toimii, mutta tämä riittää pitämään meidät liikkeessä.

Tämä voi tuntua abstraktilta, joten kirjoitetaan ensimmäinen async-ohjelmamme: pieni verkkoskreipperi. Välitämme komentoriviltä kaksi URL-osoitetta, haemme molemmat samanaikaisesti ja palautamme sen tuloksen, joka valmistuu ensin. Esimerkissä on melko paljon uutta syntaksia, mutta älä huoli — selitämme kaiken tarvittavan matkan varrella.

## Ensimmäinen async-ohjelmamme

Jotta voimme keskittyä tässä luvussa asyncin oppimiseen eikä ekosysteemin osien jongleeraukseen, olemme luoneet `trpl`-crate:n (`trpl` on lyhenne sanasta ”The Rust Programming Language”). Se uudelleen-vie kaikki tarvitsemasi tyypit, traitit ja funktiot, pääasiassa [`futures`][futures-crate]<!-- ignore -->- ja [`tokio`][tokio]<!-- ignore --> -crate:istä. `futures`-crate on virallinen kokeilualusta Rustin async-koodille, ja se on itse asiassa paikka, jossa `Future`-trait alun perin suunniteltiin. Tokio on tänään laajimmin käytetty async-ajoympäristö Rustissa, erityisesti web-sovelluksissa. Muita hyviä ajoympäristöjä on olemassa, ja ne voivat sopia paremmin tarkoituksiisi. Käytämme `tokio`-cratea `trpl`:n alla, koska se on hyvin testattu ja laajalti käytetty.

Joissakin tapauksissa `trpl` myös nimeää uudelleen tai käärii alkuperäisiä API:ja, jotta voit keskittyä tämän luvun oleellisiin yksityiskohtiin. Jos haluat ymmärtää, mitä crate tekee, kannustamme tutustumaan [sen lähdekoodiin][crate-source]. Näet, mistä crate:stä kukin uudelleenvienti tulee, ja olemme jättäneet laajat kommentit selittämään crate:n toimintaa.

Luo uusi binääriprojekti nimeltä `hello-async` ja lisää `trpl`-crate riippuvuudeksi:

```console
$ cargo new hello-async
$ cd hello-async
$ cargo add trpl
```

Nyt voimme käyttää `trpl`:n tarjoamia osia ensimmäisen async-ohjelmamme kirjoittamiseen. Rakennamme pienen komentorivityökalun, joka hakee kaksi verkkosivua, poimii kustakin `<title>`-elementin ja tulostaa sen sivun otsikon, joka valmistuu koko prosessin ensimmäisenä.

### page_title-funktion määrittely

Aloitetaan kirjoittamalla funktio, joka ottaa yhden sivun URL-osoitteen parametrina, tekee siihen pyynnön ja palauttaa `<title>`-elementin tekstin (katso listaus 17-1).

<Listing number="17-1" file-name="src/main.rs" caption="Async-funktion määrittely HTML-sivun title-elementin hakemiseksi">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-01/src/main.rs:all}}
```

</Listing>

Ensin määrittelemme funktion nimeltä `page_title` ja merkitsemme sen `async`-avainsanalla. Sitten käytämme `trpl::get`-funktiota välitetyn URL-osoitteen hakemiseen ja lisäämme `await`-avainsanan odottamaan vastausta. Saadaksemme `response`:n tekstin kutsumme sen `text`-metodia ja odotamme sitä jälleen `await`-avainsanalla. Molemmat vaiheet ovat asynkronisia. `get`-funktiossa meidän täytyy odottaa, että palvelin lähettää vastauksensa ensimmäisen osan, joka sisältää HTTP-otsikot, evästeet ja niin edelleen ja joka voidaan toimittaa erillään vastauksen rungosta. Erityisesti jos runko on hyvin suuri, kaiken saapuminen voi kestää jonkin aikaa. Koska meidän täytyy odottaa vastauksen _kokonaisuuden_ saapumista, `text`-metodi on myös async.

Meidän täytyy odottaa molempia futureja eksplisiittisesti, koska futuret Rustissa ovat _laiskoja_: ne eivät tee mitään, ennen kuin pyydät niitä `await`-avainsanalla. (Itse asiassa Rust näyttää kääntäjävaroituksen, jos et käytä futurea.) Tämä saattaa muistuttaa iteraattorien käsittelyä [”Kohteiden sarjan käsittely iteraattoreilla”][iterators-lazy]<!-- ignore --> -osiossa luvussa 13. Iteraattorit eivät tee mitään, ellet kutsu niiden `next`-metodia — suoraan tai `for`-silmukoiden tai `map`-kaltaisten metodien kautta, jotka käyttävät `next`:iä taustalla. Samoin futuret eivät tee mitään, ellet pyydä niitä eksplisiittisesti. Tämä laiskuus antaa Rustin välttää async-koodin suorittamisen, kunnes sitä todella tarvitaan.

> Huom: Tämä eroaa käyttäytymisestä, jonka näimme käytettäessä `thread::spawn`:ia [”Uuden säikeen luominen spawn:illa”][thread-spawn]<!-- ignore --> -osiossa luvussa 16, jossa toiselle säikeelle välittämämme sulkeuma alkoi suorittua heti. Se eroaa myös monien muiden kielten async-lähestymistavasta. Se on kuitenkin tärkeää, jotta Rust voi tarjota suorituskykytakuunsa, aivan kuten iteraattoreiden kanssa.

Kun meillä on `response_text`, voimme jäsentää sen `Html`-tyypin instanssiksi käyttämällä `Html::parse`:a. Raakamerkkijonon sijaan meillä on nyt tietotyyppi, jolla voimme käsitellä HTML:ää rikkaampana tietorakenteena. Erityisesti voimme käyttää `select_first`-metodia löytääksemme annetun CSS-valitsimen ensimmäisen esiintymän. Välittämällä merkkijonon `"title"` saamme dokumentin ensimmäisen `<title>`-elementin, jos sellainen on. Koska vastaavaa elementtiä ei välttämättä ole, `select_first` palauttaa `Option<ElementRef>`:n. Lopuksi käytämme `Option::map`-metodia, jonka avulla voimme käsitellä `Option`:in sisältämää kohdetta, jos se on läsnä, ja olla tekemättä mitään, jos sitä ei ole. (Voisimme käyttää myös `match`-lauseketta, mutta `map` on idiomaattisempi.) `map`:ille antamamme funktion rungossa kutsumme `inner_html`:ia `title`:lle saadaksemme sen sisällön, joka on `String`. Lopulta meillä on `Option<String>`.

Huomaa, että Rustin `await`-avainsana tulee odotettavan lausekkeen _jälkeen_, ei ennen sitä. Se on siis _jälkiliite_-avainsana. Tämä voi erota siitä, mihin olet tottunut, jos olet käyttänyt `async`:ia muissa kielissä, mutta Rustissa se tekee metodiketjuista paljon miellyttävämpiä. Näin voimme muuttaa `page_title`:n rungon ketjuttamaan `trpl::get`- ja `text`-funktiokutsut yhteen `await`:in välissä, kuten listauksessa 17-2.

<Listing number="17-2" file-name="src/main.rs" caption="Ketjuttaminen `await`-avainsanalla">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-02/src/main.rs:chaining}}
```

</Listing>

Näin olemme onnistuneesti kirjoittaneet ensimmäisen async-funktiomme! Ennen kuin lisäämme `main`:iin koodia sen kutsumiseksi, puhutaan hieman lisää siitä, mitä olemme kirjoittaneet ja mitä se tarkoittaa.

Kun Rust näkee `async`-avainsanalla merkityn _lohkon_, se kääntää sen yksilölliseksi, nimettömäksi tietotyypiksi, joka toteuttaa `Future`-traitin. Kun Rust näkee `async`-avainsanalla merkityn _funktion_, se kääntää sen ei-async-funktioksi, jonka runko on async-lohko. Async-funktion palautustyyppi on kääntäjän kyseiselle async-lohkolle luoman nimettömän tietotyypin tyyppi.

Näin ollen `async fn`:n kirjoittaminen on vastaavaa kuin funktion kirjoittaminen, joka palauttaa palautustyypin _futuren_. Kääntäjälle funktiomäärittely, kuten listauksen 17-1 `async fn page_title`, on karkeasti vastaava ei-async-funktiolle, joka on määritelty näin:

```rust
# extern crate trpl; // required for mdbook test
use std::future::Future;
use trpl::Html;

fn page_title(url: &str) -> impl Future<Output = Option<String>> {
    async move {
        let text = trpl::get(url).await.text().await;
        Html::parse(&text)
            .select_first("title")
            .map(|title| title.inner_html())
    }
}
```

Käydään läpi muunnetun version jokainen osa:

- Se käyttää `impl Trait` -syntaksia, josta puhuimme luvussa 10 [”Traitit parametreina”][impl-trait]<!-- ignore --> -osiossa.
- Palautettu arvo toteuttaa `Future`-traitin, jonka assosioitu tyyppi on `Output`. Huomaa, että `Output`-tyyppi on `Option<String>`, sama kuin alkuperäisen `async fn page_title` -version palautustyyppi.
- Kaikki alkuperäisen funktion rungossa kutsuttu koodi on kääritty `async move` -lohkoon. Muista, että lohkot ovat lausekkeita. Koko lohko on funktion palauttama lauseke.
- Tämä async-lohko tuottaa arvon tyypillä `Option<String>`, kuten juuri kuvattiin. Arvo vastaa palautustyypin `Output`-tyyppiä. Tämä on sama kuin muut näkemäsi lohkot.
- Uusi funktion runko on `async move` -lohko, koska se käyttää `url`-parametria. (Puhumme `async`:sta ja `async move`:sta paljon lisää myöhemmin luvussa.)

Nyt voimme kutsua `page_title`:a `main`:issa.

<!-- Old headings. Do not remove or links may break. -->

<a id ="determining-a-single-pages-title"></a>

### Async-funktion suorittaminen ajoympäristössä

Aloitetaan hakemalla yhden sivun otsikko, kuten listauksessa 17-3. Valitettavasti tämä koodi ei vielä käänny.

<Listing number="17-3" file-name="src/main.rs" caption="`page_title`-funktion kutsuminen `main`:ista käyttäjän antamalla argumentilla">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-03/src/main.rs:main}}
```

</Listing>

Noudatamme samaa mallia, jota käytimme komentoriviargumenttien lukemiseen [”Komentoriviargumenttien hyväksyminen”][cli-args]<!-- ignore --> -osiossa luvussa 12. Sitten välitämme URL-argumentin `page_title`:lle ja odotamme tulosta. Koska futuren tuottama arvo on `Option<String>`, käytämme `match`-lauseketta tulostaaksemme eri viestejä sen mukaan, oliko sivulla `<title>`.

`await`-avainsanaa voi käyttää vain async-funktioissa tai -lohkoissa, eikä Rust anna merkitä erityistä `main`-funktiota `async`:iksi.

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-03
cargo build
copy just the compiler error
-->

```text
error[E0752]: `main` function is not allowed to be `async`
 --> src/main.rs:6:1
  |
6 | async fn main() {
  | ^^^^^^^^^^^^^^^ `main` function is not allowed to be `async`
```

Syy siihen, miksi `main`:ia ei voi merkitä `async`:iksi, on se, että async-koodi tarvitsee _ajoympäristön_: Rust-crate:n, joka hallinnoi asynkronisen koodin suorittamisen yksityiskohdat. Ohjelman `main`-funktio voi _alustaa_ ajoympäristön, mutta se ei _itse_ ole ajoympäristö. (Näemme pian lisää siitä, miksi näin on.) Jokaisessa Rust-ohjelmassa, joka suorittaa async-koodia, on vähintään yksi paikka, jossa ajoympäristö asetetaan suorittamaan futuret.

Useimmat asyncia tukevat kielet sisällyttävät ajoympäristön, mutta Rust ei. Sen sijaan saatavilla on monia eri async-ajoympäristöjä, joista jokainen tekee erilaisia kompromisseja käyttötapaansa sopiviksi. Esimerkiksi suuren läpimenon web-palvelimella, jossa on monta CPU-ydintä ja paljon RAM-muistia, on hyvin erilaiset tarpeet kuin mikrokontrollerilla, jossa on yksi ydin, vähän RAM-muistia eikä heap-allokointimahdollisuutta. Nämä ajoympäristöt tarjoavat usein myös async-versioita yleisestä toiminnallisuudesta, kuten tiedosto- tai verkko-I/O:sta.

Tässä ja luvun lopun osissa käytämme `trpl`-crate:n `block_on`-funktiota, joka ottaa futuren argumenttina ja estää nykyisen säikeen, kunnes tämä future on suoritettu loppuun. Taustalla `block_on`:in kutsuminen asettaa `tokio`-crate:lla ajoympäristön, jota käytetään välitetyn futuren suorittamiseen (`trpl`-crate:n `block_on`:in käyttäytyminen on samankaltainen kuin muiden ajoympäristöcrate:jen `block_on`-funktioilla). Kun future on valmis, `block_on` palauttaa futuren tuottaman arvon.

Voisimme välittää `page_title`:n palauttaman futuren suoraan `block_on`:ille ja, kun se valmistuu, tehdä `match`:in tuloksena olevaan `Option<String>`:iin kuten yritimme listauksessa 17-3. Useimmissa luvun esimerkeissä (ja useimmassa oikean maailman async-koodissa) teemme kuitenkin enemmän kuin yhden async-funktiokutsun, joten sen sijaan välitämme `async`-lohkon ja odotamme eksplisiittisesti `page_title`-kutsun tulosta, kuten listauksessa 17-4.

<Listing number="17-4" caption="Async-lohkon odottaminen `trpl::block_on`:illa" file-name="src/main.rs">

<!-- should_panic,noplayground because mdbook test does not pass args -->

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch17-async-await/listing-17-04/src/main.rs:run}}
```

</Listing>

Kun suoritamme tämän koodin, saamme alun perin odottamamme käyttäytymisen:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-04
cargo build # skip all the build noise
cargo run -- "https://www.rust-lang.org"
# copy the output here
-->

```console
$ cargo run -- "https://www.rust-lang.org"
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.05s
     Running `target/debug/async_await 'https://www.rust-lang.org'`
The title for https://www.rust-lang.org was
            Rust Programming Language
```

Huh — meillä on vihdoin toimivaa async-koodia! Ennen kuin lisäämme koodin kahden sivun kilpailuttamiseen, käännymme hetkeksi takaisin siihen, miten futuret toimivat.

Jokainen _odotuspiste_ — eli jokainen paikka, jossa koodi käyttää `await`-avainsanaa — on paikka, jossa ohjaus palautetaan ajoympäristölle. Jotta tämä toimii, Rustin täytyy pitää kirjaa async-lohkoon liittyvästä tilasta, jotta ajoympäristö voisi käynnistää muuta työtä ja palata sitten, kun se on valmis yrittämään ensimmäisen etenemistä uudelleen. Tämä on näkymätön tilakone, ikään kuin olisit kirjoittanut enumin, joka tallentaa nykyisen tilan jokaisessa odotuspisteessä:

```rust
{{#rustdoc_include ../listings/ch17-async-await/no-listing-state-machine/src/lib.rs:enum}}
```

Jokaisen tilan välillä siirtymisen koodin kirjoittaminen käsin olisi kuitenkin työlästä ja virhealtista, erityisesti kun myöhemmin täytyy lisätä toiminnallisuutta ja tiloja. Onneksi Rust-kääntäjä luo ja hallinnoi async-koodin tilakonedatarakenteet automaattisesti. Normaalit lainaus- ja omistussäännöt datarakenteille pätevät edelleen, ja onneksi kääntäjä tarkistaa nekin puolestamme ja antaa hyödyllisiä virheilmoituksia. Käymme läpi muutamia niistä myöhemmin luvussa.

Lopulta jonkun täytyy suorittaa tämä tilakone, ja se jokin on ajoympäristö. (Siksi saatat törmätä _executor_-mainintoihin tutkiessasi ajoympäristöjä: executor on ajoympäristön osa, joka vastaa async-koodin suorittamisesta.)

Nyt näet, miksi kääntäjä esti meitä tekemästä `main`:ista itse async-funktiota listauksessa 17-3. Jos `main` olisi async-funktio, jonkun muun täytyisi hallita `main`:in palauttaman futuren tilakonetta, mutta `main` on ohjelman lähtökohta! Sen sijaan kutsuimme `trpl::block_on`-funktiota `main`:issa asettaaksemme ajoympäristön ja suorittaaksemme `async`-lohkon palauttaman futuren loppuun.

> Huom: Jotkut ajoympäristöt tarjoavat makroja, joiden avulla _voit_ kirjoittaa async-`main`-funktion. Nämä makrot kirjoittavat `async fn main() { ... }` uudelleen tavalliseksi `fn main`:iksi, joka tekee saman kuin teimme käsin listauksessa 17-4: kutsuu funktiota, joka suorittaa futuren loppuun samalla tavalla kuin `trpl::block_on`.

Nyt yhdistetään nämä palaset ja katsotaan, miten voimme kirjoittaa samanaikaista koodia.

<!-- Old headings. Do not remove or links may break. -->

<a id="racing-our-two-urls-against-each-other"></a>

### Kahden URL-osoitteen kilpailuttaminen samanaikaisesti

Listauksessa 17-5 kutsumme `page_title`:a kahdella eri komentoriviltä välitetyllä URL-osoitteella ja kilpailutamme ne valitsemalla sen futuren, joka valmistuu ensin.

<Listing number="17-5" caption="`page_title`:n kutsuminen kahdelle URL-osoitteelle nähdäksemme, kumpi palautuu ensin" file-name="src/main.rs">

<!-- should_panic,noplayground because mdbook does not pass args -->

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch17-async-await/listing-17-05/src/main.rs:all}}
```

</Listing>

Aloitamme kutsumalla `page_title`:a kummallekin käyttäjän antamalle URL-osoitteelle. Tallennamme tuloksena olevat futuret nimillä `title_fut_1` ja `title_fut_2`. Muista, että ne eivät vielä tee mitään, koska futuret ovat laiskoja emmekä ole vielä odottaneet niitä. Sitten välitämme futuret `trpl::select`:ille, joka palauttaa arvon ilmaisemaan, kumpi sille välitetyistä futureista valmistuu ensin.

> Huom: Taustalla `trpl::select` on rakennettu yleisemmän `select`-funktion päälle, joka on määritelty `futures`-crate:ssä. `futures`-crate:n `select`-funktio voi tehdä paljon asioita, joita `trpl::select` ei voi, mutta siinä on myös lisämonimutkaisuutta, jonka voimme ohittaa toistaiseksi.

Kumpikin future voi oikeutetusti ”voittaa”, joten `Result`:in palauttaminen ei ole järkevää. Sen sijaan `trpl::select` palauttaa tyypin, jota emme ole vielä nähneet: `trpl::Either`. `Either`-tyyppi on hieman samankaltainen kuin `Result`, sillä siinä on kaksi tapausta. Toisin kuin `Result`:issa, `Either`:iin ei ole sisäänrakennettua käsitettä onnistumisesta tai epäonnistumisesta. Sen sijaan se käyttää `Left`:ia ja `Right`:ia ilmaisemaan ”jompaa kumpaa”:

```rust
enum Either<A, B> {
    Left(A),
    Right(B),
}
```

`select`-funktio palauttaa `Left`:in kyseisen futuren tuloksella, jos ensimmäinen argumentti voittaa, ja `Right`:in toisen future-argumentin tuloksella, jos _se_ voittaa. Tämä vastaa argumenttien järjestystä funktiokutsussa: ensimmäinen argumentti on toisen vasemmalla puolella.

Päivitämme myös `page_title`:n palauttamaan saman välitetyn URL-osoitteen. Näin, jos ensin palautuva sivu ei sisällä ratkaistavaa `<title>`:ä, voimme silti tulostaa järkevän viestin. Kun tämä tieto on käytettävissä, viimeistelemme päivittämällä `println!`-tulostuksemme ilmaisemaan sekä kumpi URL-osoite valmistui ensin että mikä, jos lainkaan, kyseisen URL-osoitteen verkkosivun `<title>` on.

Olet nyt rakentanut pienen toimivan verkkoskreipperin! Valitse pari URL-osoitetta ja suorita komentorivityökalu. Saatat huomata, että jotkin sivustot ovat johdonmukaisesti nopeampia kuin toiset, kun taas toisissa tapauksissa nopeampi sivu vaihtelee ajosta toiseen. Tärkeämpää on, että olet oppinut futurejen kanssa työskentelyn perusteet, joten voimme nyt syventyä siihen, mitä asyncilla voi tehdä.

[impl-trait]: ch10-02-traits.html#traits-as-parameters
[iterators-lazy]: ch13-02-iterators.html
[thread-spawn]: ch16-01-threads.html#creating-a-new-thread-with-spawn
[cli-args]: ch12-01-accepting-command-line-arguments.html

<!-- TODO: map source link version to version of Rust? -->

[crate-source]: https://github.com/rust-lang/book/tree/main/packages/trpl
[futures-crate]: https://crates.io/crates/futures
[tokio]: https://tokio.rs
