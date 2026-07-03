## Futuresit ja asynkroninen syntaksi

Rustin asynkronisen ohjelmoinnin keskeiset elementit ovat _futuresit_ sekä Rustin
`async`- ja `await`-avainsanat.

_Future_ on arvo, joka ei välttämättä ole vielä valmis, mutta valmistuu jossain
vaiheessa tulevaisuudessa. (Tämä sama käsite esiintyy monissa kielissä, joskus
muilla nimillä, kuten _task_ tai _promise_.) Rust tarjoaa `Future`-traitin
rakennuspalikaksi, jotta eri asynkroniset operaatiot voidaan toteuttaa eri
tietorakenteilla mutta yhteisellä rajapinnalla. Rustissa futuresit ovat
tyyppejä, jotka toteuttavat `Future`-traitin. Jokainen future pitää sisällään
oman tietonsa edistymisestä ja siitä, mitä ”valmis” tarkoittaa.

Voit käyttää `async`-avainsanaa lohkoissa ja funktioissa määrittääksesi, että
niitä voidaan keskeyttää ja jatkaa. Async-lohkossa tai async-funktiossa voit
käyttää `await`-avainsanaa _odottaaksesi futurea_ (eli odottaa sen valmistumista).
Jokainen kohta, jossa odotat futurea async-lohkossa tai -funktiossa, on
mahdollinen paikka, jossa kyseinen async-lohko tai -funktio voi pysähtyä ja
jatkaa. Prosessia, jossa tarkistetaan futurelta, onko sen arvo jo saatavilla,
kutsutaan _pollaamiseksi_.

Joissakin muissa kielissä, kuten C#:ssä ja JavaScriptissä, käytetään myös `async`- ja
`await`-avainsanoja asynkroniseen ohjelmointiin. Jos olet tuttu näihin kieliin,
huomaat ehkä merkittäviä eroja siinä, miten Rust tekee asiat, mukaan lukien
syntaksin käsittelyn. Siihen on hyvä syy, kuten näemme!

Kun kirjoitamme async-Rustia, käytämme `async`- ja `await`-avainsanoja useimman
ajan. Rust kääntää ne vastaavaksi koodiksi käyttäen `Future`-traitia, aivan
kuten se kääntää `for`-silmukat vastaavaksi koodiksi käyttäen `Iterator`-traitia.
Koska Rust tarjoaa `Future`-traitin, voit kuitenkin myös toteuttaa sen omille
tietotyypeillesi tarvittaessa. Monet tässä luvussa näkemämme funktiot
palauttavat tyyppejä, joilla on oma `Future`-toteutuksensa. Palaamme traitin
määritelmään luvun lopussa ja syvennymme siihen, miten se toimii, mutta tämä
riittää pitämään meidät liikkeellä.

Tämä kaikki voi tuntua abstraktilta, joten kirjoitetaan ensimmäinen
asynkroninen ohjelmamme: pieni web-skripti. Välitämme komentoriviltä kaksi
URL-osoitetta, haemme molemmat samanaikaisesti ja palautamme sen tuloksen,
joka valmistuu ensin. Tässä esimerkissä on melko paljon uutta syntaksia, mutta
älä huoli — selitämme kaiken tarvittavan matkan varrella.

## Ensimmäinen asynkroninen ohjelmamme

Jotta voimme keskittyä tässä luvussa async-oppimiseen eikä ekosysteemin osien
jongleeraamiseen, olemme luoneet `trpl`-craten (`trpl` on lyhenne sanasta ”The Rust
Programming Language”). Se uudelleen vie kaikki tarvitsemasi tyypit, traitit ja
funktiot, pääasiassa [`futures`][futures-crate]<!-- ignore -->- ja
[`tokio`][tokio]<!-- ignore --> -crateista. `futures`-crate on virallinen koti
Rustin kokeilulle async-koodille, ja se on itse asiassa paikka, jossa `Future`-trait
suunniteltiin alun perin. Tokio on tänään laajimmin käytetty async-ajoympäristö
Rustissa, erityisesti web-sovelluksissa. Muita hyviä ajoympäristöjä on olemassa,
ja ne voivat sopia paremmin tarkoituksiisi. Käytämme `trpl`-cratessa `tokio`-cratea,
koska se on hyvin testattu ja laajalti käytetty.

Joissakin tapauksissa `trpl` myös nimeää uudelleen tai käärii alkuperäisiä API:ja
pitääkseen huomiosi tämän luvun oleellisissa yksityiskohdissa. Jos haluat ymmärtää,
mitä crate tekee, kannustamme tutustumaan [sen lähdekoodiin][crate-source]<!-- ignore -->. Näet,
mistä cratesta kukin uudelleenvienti tulee, ja olemme jättäneet laajat kommentit,
jotka selittävät craten toiminnan.

Luo uusi binääriprojekti nimeltä `hello-async` ja lisää `trpl`-crate riippuvuudeksi:

```console
$ cargo new hello-async
$ cd hello-async
$ cargo add trpl
```

Nyt voimme käyttää `trpl`:n tarjoamia osia kirjoittaaksemme ensimmäisen
asynkronisen ohjelmamme. Rakennamme pienen komentorivityökalun, joka hakee kaksi
verkkosivua, poimii kustakin `<title>`-elementin ja tulostaa sen sivun otsikon,
joka saa koko prosessin valmiiksi ensin.

### `page_title`-funktion määrittely

Aloitetaan kirjoittamalla funktio, joka ottaa yhden sivun URL-osoitteen
parametrina, tekee siihen pyynnön ja palauttaa title-elementin tekstin (katso
Listaus 17-1).

<Listing number="17-1" file-name="src/main.rs" caption="Async-funktion määrittely HTML-sivun title-elementin hakemiseksi">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-01/src/main.rs:all}}
```

</Listing>

Ensin määrittelemme funktion nimeltä `page_title` ja merkitsemme sen `async`-avainsanalla.
Sitten käytämme `trpl::get`-funktiota välitetyn URL-osoitteen hakemiseen ja
lisäämme `await`-avainsanan vastauksen odottamiseen. Saadaksemme vastauksen
tekstin kutsumme sen `text`-metodia ja odotamme sitä jälleen `await`-avainsanalla.
Molemmat vaiheet ovat asynkronisia. `get`-funktiossa meidän täytyy odottaa, että
palvelin lähettää vastauksensa ensimmäisen osan, joka sisältää HTTP-otsikot,
evästeet ja niin edelleen, ja joka voidaan toimittaa erillään vastauksen
rungosta. Erityisesti jos runko on hyvin suuri, sen saapuminen kokonaan voi viedä
aikaa. Koska meidän täytyy odottaa vastauksen _kokonaisuuden_ saapumista,
`text`-metodi on myös async.

Meidän täytyy odottaa näitä futuresia nimenomaisesti, koska Rustin futuresit ovat
_laiskoja_: ne eivät tee mitään, ennen kuin pyydät niitä tekemään niin `await`-avainsanalla.
(Todellisuudessa Rust näyttää kääntäjävaroituksen, jos et käytä futurea.) Tämä saattaa
muistuttaa Luvun 13 keskustelua iteraattoreista osiossa
[Kohteiden sarjan käsittely iteraattoreilla][iterators-lazy]<!-- ignore -->. Iteraattorit
eivät tee mitään, ellet kutsu niiden `next`-metodia — joko suoraan tai käyttämällä
`for`-silmukoita tai metodeja kuten `map`, jotka käyttävät `next`-metodia taustalla.
Samoin futuresit eivät tee mitään, ellet pyydä niitä tekemään niin nimenomaisesti. Tämä
laiskuus antaa Rustin välttää async-koodin suorittamisen, kunnes sitä todella tarvitaan.

> Huom: Tämä eroaa edellisessä luvussa nähdystä käyttäytymisestä, kun käytimme
> `thread::spawn`-funktiota osiossa [Uuden säikeen luominen
> `spawn`-funktiolla][thread-spawn]<!--ignore-->, jossa toiselle säikeelle välittämämme
> sulkeis alkoi suorittaa heti. Se eroaa myös siitä, miten monet muut kielet
> lähestyvät asyncia. Mutta se on tärkeää, jotta Rust voi tarjota
> suorituskykytakuunsa, aivan kuten iteraattoreiden kanssa.

Kun meillä on `response_text`, voimme jäsentää sen `Html`-tyypin instanssiksi
käyttämällä `Html::parse`-funktiota. Raakamerkkijonon sijaan meillä on nyt
tietotyyppi, jota voimme käyttää HTML:n käsittelyyn rikkaampana tietorakenteena.
Erityisesti voimme käyttää `select_first`-metodia löytääksemme annetun CSS-valitsimen
ensimmäisen esiintymän. Välittämällä merkkijonon `"title"` saamme dokumentin
ensimmäisen `<title>`-elementin, jos sellainen on. Koska vastaavaa elementtiä ei
välttämättä ole, `select_first` palauttaa `Option<ElementRef>`-tyypin. Lopuksi
käytämme `Option::map`-metodia, jonka avulla voimme käsitellä `Option`-tyypin
kohteen, jos se on läsnä, ja olla tekemättä mitään, jos sitä ei ole. (Voisimme
käyttää tässä myös `match`-lauseketta, mutta `map` on idiomaattisempi.) Funktiossa,
jonka annamme `map`-metodille, kutsumme `inner_html`-metodia `title_element`-elementille
saadaksemme sen sisällön, joka on `String`. Kun kaikki on sanottu ja tehty, meillä on
`Option<String>`.

Huomaa, että Rustin `await`-avainsana sijoitetaan odotettavan lausekkeen _jälkeen_,
ei ennen sitä. Toisin sanoen se on _jälkiliite_-avainsana. Tämä voi erota siitä,
mihin olet tottunut, jos olet käyttänyt `async`-syntaksia muissa kielissä, mutta
Rustissa se tekee metodiketjuista paljon miellyttävämpiä käyttää. Tämän ansiosta
voimme muuttaa `page_url_for`-funktion runkoa ketjuttamaan `trpl::get`- ja `text`-funktiokutsut
yhteen `await`-avainsanalla niiden välissä, kuten Listauksessa 17-2.

<Listing number="17-2" file-name="src/main.rs" caption="Ketjuttaminen `await`-avainsanalla">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-02/src/main.rs:chaining}}
```

</Listing>

Näin olemme onnistuneesti kirjoittaneet ensimmäisen async-funktiomme! Ennen kuin
lisäämme `main`-funktioon koodia sen kutsumiseksi, puhutaan hieman lisää siitä,
mitä olemme kirjoittaneet ja mitä se tarkoittaa.

Kun Rust näkee `async`-avainsanalla merkityn lohkon, se kääntää sen yksilölliseksi,
anonyymiksi tietotyypiksi, joka toteuttaa `Future`-traitin. Kun Rust näkee
`async`-avainsanalla merkityn funktion, se kääntää sen ei-async-funktioksi,
jonka runko on async-lohko. Async-funktion paluutyyppi on sen anonyymin
tietotyypin tyyppi, jonka kääntäjä luo kyseiselle async-lohkolle.

Näin ollen `async fn` -kirjoittaminen on vastaavaa kuin funktion kirjoittaminen,
joka palauttaa paluutyypin _futuren_. Kääntäjälle funktiomäärittely, kuten
Listauksen 17-1 `async fn page_title`, on vastaava ei-async-funktiolle, joka on
määritelty näin:

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

- Se käyttää `impl Trait` -syntaksia, josta puhuimme takaisin Luvussa 10 osiossa
  [Traitin käyttö parametrina][impl-trait]<!-- ignore -->.
- Palautettu trait on `Future`, jolla on liitetty tyyppi `Output`. Huomaa,
  että `Output`-tyyppi on `Option<String>`, joka on sama kuin `page_title`-funktion
  `async fn` -version alkuperäinen paluutyyppi.
- Kaikki alkuperäisen funktion rungossa kutsuttu koodi on kääritty `async move` -lohkoon.
  Muista, että lohkot ovat lausekkeita. Koko lohko on funktion palauttama lauseke.
- Tämä async-lohko tuottaa arvon, jonka tyyppi on `Option<String>`, kuten juuri
  kuvattiin. Tämä arvo vastaa paluutyypin `Output`-tyyppiä. Tämä on aivan kuten
  muut näkemäsi lohkot.
- Uusi funktion runko on `async move` -lohko, koska se käyttää `url`-parametria.
  (Puhumme paljon enemmän `async`- ja `async move` -eroista myöhemmin tässä luvussa.)

Nyt voimme kutsua `page_title`-funktiota `main`-funktiossa.

## Yhden sivun otsikon määrittäminen

Aloitetaan hakemalla otsikko yhdelle sivulle. Listauksessa 17-3 noudatamme
samaa mallia, jota käytimme Luvussa 12 komentoriviargumenttien hakemiseen osiossa
[Komentoriviargumenttien vastaanottaminen][cli-args]<!-- ignore -->. Sitten
välitämme ensimmäisen URL-osoitteen `page_title`-funktiolle ja odotamme tulosta.
Koska futuren tuottama arvo on `Option<String>`, käytämme `match`-lauseketta
tulostamaan eri viestejä sen mukaan, oliko sivulla `<title>`-elementti.

<Listing number="17-3" file-name="src/main.rs" caption="`page_title`-funktion kutsuminen `main`-funktiosta käyttäjän antamalla argumentilla">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-03/src/main.rs:main}}
```

</Listing>

Valitettavasti tämä koodi ei käänny. Ainoa paikka, jossa voimme käyttää `await`-avainsanaa,
on async-funktioissa tai -lohkoissa, eikä Rust anna meidän merkitä erityistä
`main`-funktiota `async`-funktioksi.

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

Syy siihen, miksi `main` ei voi olla merkitty `async`-funktioksi, on se, että
async-koodi tarvitsee _ajoympäristön_: Rust-craten, joka hallitsee asynkronisen
koodin suorittamisen yksityiskohdat. Ohjelman `main`-funktio voi _alustaa_
ajoympäristön, mutta se ei ole ajoympäristö _itse_. (Näemme pian lisää siitä,
miksi näin on.) Jokaisessa Rust-ohjelmassa, joka suorittaa async-koodia, on
vähintään yksi paikka, jossa ajoympäristö asetetaan ja futuresit suoritetaan.

Useimmat asyncia tukevat kielet sisältävät ajoympäristön, mutta Rust ei sisällä.
Sen sijaan on saatavilla monia eri async-ajoympäristöjä, joista jokainen tekee
eri kompromisseja käyttötapaukselle, johon se on suunnattu. Esimerkiksi
suuren läpimenon web-palvelimella, jossa on monta CPU-ydintä ja paljon RAM-muistia,
on hyvin erilaiset tarpeet kuin mikrokontrollerilla, jossa on yksi ydin, vähän
RAM-muistia eikä heap-allokointimahdollisuutta. Cratet, jotka tarjoavat näitä
ajoympäristöjä, tarjoavat usein myös async-versioita yleisestä toiminnallisuudesta,
kuten tiedosto- tai verkkoliikenteestä.

Tässä ja koko luvun loppuosan ajan käytämme `trpl`-craten `run`-funktiota, joka
ottaa futuren argumenttina ja suorittaa sen loppuun. Taustalla `run`-funktion
kutsuminen asettaa ajoympäristön, jota käytetään välitetyn futuren suorittamiseen.
Kun future valmistuu, `run` palauttaa sen tuottaman arvon.

Voisimme välittää `page_title`-funktion palauttaman futuren suoraan `run`-funktiolle,
ja kun se valmistuisi, voisimme tehdä `match`-lausekkeen tuloksena olevalle
`Option<String>`-tyypille, kuten yritimme Listauksessa 17-3. Useimmissa luvun
esimerkeissä (ja useimmassa tosielämän async-koodissa) teemme kuitenkin enemmän
kuin yhden async-funktiokutsun, joten sen sijaan välitämme `async`-lohkon ja
odotamme nimenomaisesti `page_title`-kutsun tulosta, kuten Listauksessa 17-4.

<Listing number="17-4" caption="Async-lohkon odottaminen `trpl::run`-funktiolla" file-name="src/main.rs">

<!-- should_panic,noplayground because mdbook test does not pass args -->

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch17-async-await/listing-17-04/src/main.rs:run}}
```

</Listing>

Kun ajamme tämän koodin, saamme alun perin odottamamme käyttäytymisen:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-04
cargo build # skip all the build noise
cargo run https://www.rust-lang.org
# copy the output here
-->

```console
$ cargo run -- https://www.rust-lang.org
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.05s
     Running `target/debug/async_await 'https://www.rust-lang.org'`
The title for https://www.rust-lang.org was
            Rust Programming Language
```

Huh — meillä on vihdoin toimivaa async-koodia! Mutta ennen kuin lisäämme koodin
kahden sivun kilpailuttamiseen, käännämme hetkeksi huomiomme takaisin siihen,
miten futuresit toimivat.

Jokainen _odotuspiste_ — eli jokainen paikka, jossa koodi käyttää `await`-avainsanaa —
edustaa paikkaa, jossa ohjaus palautetaan ajoympäristölle. Jotta tämä toimisi,
Rustin täytyy pitää kirjaa async-lohkoon liittyvästä tilasta, jotta ajoympäristö
voi käynnistää muuta työtä ja palata sitten, kun se on valmis yrittämään ensimmäisen
edistämistä uudelleen. Tämä on näkymätön tilakone, ikään kuin olisit kirjoittanut
enumin, joka tallentaa nykyisen tilan jokaisessa odotuspisteessä:

```rust
{{#rustdoc_include ../listings/ch17-async-await/no-listing-state-machine/src/lib.rs:enum}}
```

Siirtymien kirjoittaminen käsin jokaisen tilan välillä olisi kuitenkin työlästä ja
virhealtista, erityisesti kun lisäät myöhemmin toiminnallisuutta ja tiloja koodiin.
Onneksi Rust-kääntäjä luo ja hallitsee tilakoneen tietorakenteet async-koodille
automaattisesti. Tietorakenteisiin liittyvät lainaus- ja omistussäännöt pätevät
edelleen, ja onneksi kääntäjä tarkistaa ne myös puolestamme ja tarjoaa hyödyllisiä
virheilmoituksia. Käymme läpi muutamia niistä myöhemmin tässä luvussa.

Lopulta jokin täytyy suorittaa tämä tilakone, ja se jokin on ajoympäristö. (Tästä
syystä saatat törmätä viittauksiin _suorittimiin_, kun tutkit ajoympäristöjä:
suoritin on osa ajoympäristöä, joka vastaa async-koodin suorittamisesta.)

Nyt näet, miksi kääntäjä esti meitä tekemästä `main`-funktiosta itse async-funktiota
takaisin Listauksessa 17-3. Jos `main` olisi async-funktio, jokin muu joutuisi
hallitsemaan `main`-funktion palauttaman futuren tilakonetta, mutta `main` on
ohjelman lähtökohta! Sen sijaan kutsuimme `trpl::run`-funktiota `main`-funktiossa
asettaaksemme ajoympäristön ja suorittaaksemme `async`-lohkon palauttaman futuren
loppuun.

> Huom: Jotkin ajoympäristöt tarjoavat makroja, jotta _voit_ kirjoittaa async-`main`-funktion.
> Nämä makrot kirjoittavat `async fn main() { ... }` uudelleen tavalliseksi `fn
> main` -funktioksi, joka tekee saman asian kuin teimme käsin Listauksessa 17-5:
> kutsuu funktiota, joka suorittaa futuren loppuun samalla tavalla kuin `trpl::run`.

Nyt yhdistetään nämä osat ja katsotaan, miten voimme kirjoittaa rinnakkaista koodia.

### Kahden URL-osoitteen kilpailuttaminen

Listauksessa 17-5 kutsumme `page_title`-funktiota kahdella eri komentoriviltä
välittämällämme URL-osoitteella ja kilpailutamme ne.

<Listing number="17-5" caption="" file-name="src/main.rs">

<!-- should_panic,noplayground because mdbook does not pass args -->

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch17-async-await/listing-17-05/src/main.rs:all}}
```

</Listing>

Aloitamme kutsumalla `page_title`-funktiota kummallekin käyttäjän antamalle
URL-osoitteelle. Tallennamme tuloksena olevat futuresit `title_fut_1`- ja
`title_fut_2`-muuttujiin. Muista, että nämä eivät tee vielä mitään, koska
futuresit ovat laiskoja emmekä ole vielä odottaneet niitä. Sitten välitämme
futuresit `trpl::race`-funktiolle, joka palauttaa arvon osoittamaan, kumpi
sille välitetyistä futuresista valmistuu ensin.

> Huom: Taustalla `race` on rakennettu yleisemmän `select`-funktion päälle, johon
> törmäät useammin tosielämän Rust-koodissa. `select`-funktio voi tehdä paljon
> asioita, joita `trpl::race`-funktio ei voi, mutta siinä on myös lisämonimutkaisuutta,
> jonka voimme ohittaa toistaiseksi.

Kumpikin future voi oikeutetusti ”voittaa”, joten `Result`-tyypin palauttaminen
ei ole järkevää. Sen sijaan `race` palauttaa tyypin, jota emme ole vielä nähneet,
`trpl::Either`. `Either`-tyyppi on hieman samanlainen kuin `Result` siinä, että
siinä on kaksi tapausta. Toisin kuin `Result`-tyypissä, `Either`-tyypissä ei
kuitenkaan ole sisäänrakennettua käsitystä onnistumisesta tai epäonnistumisesta.
Sen sijaan se käyttää `Left`- ja `Right`-tapauksia ilmaisemaan ”jompikumpi”:

```rust
enum Either<A, B> {
    Left(A),
    Right(B),
}
```

`race`-funktio palauttaa `Left`-arvon kyseisen futuren tulosteella, jos ensimmäinen
argumentti voittaa, ja `Right`-arvon toisen future-argumentin tulosteella, jos
_se_ voittaa. Tämä vastaa argumenttien järjestystä funktiota kutsuttaessa:
ensimmäinen argumentti on toisen argumentin vasemmalla puolella.

Päivitämme myös `page_title`-funktion palauttamaan saman välitetyn URL-osoitteen.
Näin, jos ensimmäisenä palaava sivu ei sisällä ratkaistavaa `<title>`-elementtiä,
voimme silti tulostaa järkevän viestin. Kun tämä tieto on saatavilla, viimeistelemme
päivittämällä `println!`-tulosteen osoittamaan sekä kumpi URL-osoite valmistui
ensin että mikä, jos lainkaan, kyseisen URL-osoitteen verkkosivun `<title>` on.

Olet nyt rakentanut pienen toimivan web-skripti-ohjelman! Valitse pari URL-osoitetta
ja aja komentorivityökalu. Saatat huomata, että jotkin sivustot ovat johdonmukaisesti
nopeampia kuin toiset, kun taas toisissa tapauksissa nopeampi sivusto vaihtelee
ajosta toiseen. Tärkeämpää on, että olet oppinut futuresien kanssa työskentelyn
perusteet, joten nyt voimme syventyä siihen, mitä voimme tehdä asyncilla.

[impl-trait]: ch10-02-traits.html#traits-as-parameters
[iterators-lazy]: ch13-02-iterators.html
[thread-spawn]: ch16-01-threads.html#creating-a-new-thread-with-spawn
[cli-args]: ch12-01-accepting-command-line-arguments.html

<!-- TODO: map source link version to version of Rust? -->

[crate-source]: https://github.com/rust-lang/book/tree/main/packages/trpl
[futures-crate]: https://crates.io/crates/futures
[tokio]: https://tokio.rs
