## Traitit: yhteisen käyttäytymisen määrittely

_Trait_ määrittää toiminnallisuuden, joka tietyllä tyypillä on ja jonka se voi
jakaa muiden tyyppien kanssa. Voimme käyttää traitteja määritelläksemme jaettua
käyttäytymistä abstraktilla tavalla. Voimme käyttää _trait-rajoja_ määrittääksemme,
että geneerinen tyyppi voi olla mikä tahansa tyyppi, jolla on tietty käyttäytyminen.

> Huom: Traitit ovat samanlaisia kuin ominaisuus, jota usein kutsutaan
> _rajapinnoiksi_ (*interfaces*) muissa kielissä, vaikka niissä on eroja.

### Traitin määrittely

Tyyppin käyttäytyminen koostuu metodeista, joita sille voidaan kutsua. Eri tyypit
jakavat saman käyttäytymisen, jos samoja metodeja voidaan kutsua kaikille
näille tyypeille. Trait-määritykset ovat tapa ryhmitellä metodien allekirjoituksia
yhteen määrittelemään joukko käyttäytymisiä, joita tarvitaan jonkin tarkoituksen
saavuttamiseksi.

Esimerkiksi sanotaan, että meillä on useita rakenteita, jotka pitävät erilaisia
tekstilajeja ja -määriä: `NewsArticle`-rakenne, joka pitää tiettyyn paikkaan
jätetyn uutisjutun, ja `SocialPost`, jossa voi olla enintään 280 merkkiä sekä
metatietoa, joka kertoo, oliko kyseessä uusi julkaisu, uudelleenjulkaisu vai
vastaus toiseen julkaisuun.

Haluamme tehdä media-aggregaattorikirjaston `aggregator`, joka voi näyttää
yhteenvetoja datasta, joka saattaa olla tallennettuna `NewsArticle`- tai
`SocialPost`-instanssiin. Tätä varten tarvitsemme yhteenvedon jokaiselta tyypiltä,
ja pyydämme sitä kutsumalla `summarize`-metodia instanssilla. Listaus 10-12
näyttää julkisen `Summary`-traitin määrityksen, joka ilmaisee tämän käyttäytymisen.

<Listing number="10-12" file-name="src/lib.rs" caption="`Summary`-trait, joka koostuu `summarize`-metodin tarjoamasta käyttäytymisestä">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-12/src/lib.rs}}
```

</Listing>

Tässä ilmoitamme traitin `trait`-avainsanalla ja sitten traitin nimen, joka
tässä tapauksessa on `Summary`. Ilmoitamme traitin myös `pub`-avainsanalla, jotta
tästä ohjelmakokonaisuudesta riippuvat ohjelmakokonaisuudet voivat käyttää tätä
traitia myös, kuten näemme muutamassa esimerkissä. Aaltosulkeiden sisällä
ilmoitamme metodien allekirjoitukset, jotka kuvaavat tämän traitin toteuttavien
tyyppien käyttäytymistä, joka tässä tapauksessa on `fn summarize(&self) -> String`.

Metodin allekirjoituksen jälkeen sen sijaan, että tarjoaisimme toteutuksen
aaltosulkeissa, käytämme puolipistettä. Jokaisen tämän traitin toteuttavan tyypin
täytyy tarjota oma mukautettu käyttäytymisensä metodin rungolle. Kääntäjä
varmistaa, että jokaisella tyypillä, jolla on `Summary`-trait, on metodi
`summarize` määritelty täsmälleen tällä allekirjoituksella.

Traitilla voi olla useita metodeja rungossaan: metodien allekirjoitukset on
listattu yksi per rivi, ja jokainen rivi päättyy puolipisteeseen.

### Traitin toteuttaminen tyypille

Nyt kun olemme määritelleet `Summary`-traitin metodien halutut allekirjoitukset,
voimme toteuttaa sen media-aggregaattorimme tyypeille. Listaus 10-13 näyttää
`Summary`-traitin toteutuksen `NewsArticle`-rakenteelle, joka käyttää otsikkoa,
kirjoittajaa ja sijaintia luodakseen `summarize`-metodin paluuarvon. `SocialPost`-rakenteelle
määrittelemme `summarize`:n käyttäjänimen ja koko julkaisun tekstin perässä,
oleteten että julkaisun sisältö on jo rajoitettu 280 merkkiin.

<Listing number="10-13" file-name="src/lib.rs" caption="`Summary`-traitin toteuttaminen `NewsArticle`- ja `SocialPost`-tyypeille">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-13/src/lib.rs:here}}
```

</Listing>

Traitin toteuttaminen tyypille on samanlaista kuin tavallisten metodien toteuttaminen.
Ero on siinä, että `impl`:n jälkeen laitamme toteutettavan traitin nimen, sitten
käytämme `for`-avainsanaa ja määrittelemme tyypin, jolle haluamme toteuttaa traitin.
`impl`-lohkon sisällä laitamme metodien allekirjoitukset, jotka trait-määritys on
määritellyt. Sen sijaan, että lisäisimme puolipisteen jokaisen allekirjoituksen
jälkeen, käytämme aaltosulkeita ja täytämme metodin rungon tietyllä käyttäytymisellä,
jonka haluamme traitin metodeilla olevan kyseiselle tyypille.

Nyt kun kirjasto on toteuttanut `Summary`-traitin `NewsArticle`- ja `SocialPost`-tyypeille,
ohjelmakokonaisuuden käyttäjät voivat kutsua trait-metodeja `NewsArticle`- ja
`SocialPost`-instansseilla samalla tavalla kuin kutsumme tavallisia metodeja.
Ainoa ero on, että käyttäjän täytyy tuoda trait laajuuteen sekä tyypit. Tässä on
esimerkki siitä, miten binääriohjelmakokonaisuus voisi käyttää `aggregator`-kirjastoamme:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-01-calling-trait-method/src/main.rs}}
```

Tämä koodi tulostaa `1 new post: horse_ebooks: of course, as you probably already
know, people`.

Muut `aggregator`-ohjelmakokonaisuudesta riippuvat ohjelmakokonaisuudet voivat
myös tuoda `Summary`-traitin laajuuteen toteuttaakseen `Summary`:n omille
tyypeilleen. Yksi huomioitava rajoitus on, että voimme toteuttaa traitin tyypille
vain jos joko trait tai tyyppi, tai molemmat, ovat paikallisia ohjelmakokonaisuudellemme.
Esimerkiksi voimme toteuttaa standardikirjaston traitteja kuten `Display` mukautetulle
tyypille kuten `SocialPost` osana `aggregator`-ohjelmakokonaisuutemme toiminnallisuutta,
koska tyyppi `SocialPost` on paikallinen `aggregator`-ohjelmakokonaisuudellemme.
Voimme myös toteuttaa `Summary`:n tyypille `Vec<T>` `aggregator`-ohjelmakokonaisuudessamme,
koska trait `Summary` on paikallinen `aggregator`-ohjelmakokonaisuudellemme.

Emme kuitenkaan voi toteuttaa ulkoisia traitteja ulkoisille tyypeille. Esimerkiksi
emme voi toteuttaa `Display`-traitia tyypille `Vec<T>` `aggregator`-ohjelmakokonaisuudessamme,
koska `Display` ja `Vec<T>` on molemmat määritelty standardikirjastossa eivätkä
ole paikallisia `aggregator`-ohjelmakokonaisuudellemme. Tämä rajoitus on osa
ominaisuutta nimeltä _yhtenäisyys_ (*coherence*), ja tarkemmin _orpopelisääntöä_
(*orphan rule*), joka on nimetty niin, koska vanhempityyppi ei ole läsnä. Tämä
sääntö varmistaa, etteivät muiden ihmisten koodit voi rikkoa sinun koodiasi ja
päinvastoin. Ilman sääntöä kaksi ohjelmakokonaisuutta voisi toteuttaa saman traitin
samalle tyypille, eikä Rust tietäisi, mitä toteutusta käyttää.

### Oletustoteutukset

Joskus on hyödyllistä, että traitilla on oletuskäyttäytymistä joillekin tai
kaikille metodeille sen sijaan, että vaadittaisiin toteutuksia kaikille metodeille
jokaisella tyypillä. Sitten kun toteutamme traitin tietylle tyypille, voimme
säilyttää tai ylikirjoittaa kunkin metodin oletuskäyttäytymisen.

Listauksessa 10-14 määrittelemme oletusmerkkijonon `Summary`-traitin `summarize`-metodille
sen sijaan, että määrittelisimme vain metodin allekirjoituksen, kuten teimme
listauksessa 10-12.

<Listing number="10-14" file-name="src/lib.rs" caption="`Summary`-traitin määrittely `summarize`-metodin oletustoteutuksella">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-14/src/lib.rs:here}}
```

</Listing>

Käyttääksemme oletustoteutusta `NewsArticle`-instanssien yhteenvedon tekemiseen,
määrittelemme tyhjän `impl`-lohkon `impl Summary for NewsArticle {}`:lla.

Vaikka emme enää määrittele `summarize`-metodia suoraan `NewsArticle`-tyypille,
olemme tarjonneet oletustoteutuksen ja määritelleet, että `NewsArticle` toteuttaa
`Summary`-traitin. Tämän seurauksena voimme silti kutsua `summarize`-metodia
`NewsArticle`-instanssilla, näin:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-02-calling-default-impl/src/main.rs:here}}
```

Tämä koodi tulostaa `New article available! (Read more...)`.

Oletustoteutuksen luominen ei vaadi meitä muuttamaan mitään `Summary`-traitin
toteutuksesta `SocialPost`-tyypille listauksessa 10-13. Syy on se, että oletustoteutuksen
ylikirjoittamisen syntaksi on sama kuin trait-metodin toteuttamisen syntaksi,
jolla ei ole oletustoteutusta.

Oletustoteutukset voivat kutsua muita metodeja samassa traitissa, vaikka näillä
muilla metodeilla ei olisikaan oletustoteutusta. Näin trait voi tarjota paljon
hyödyllistä toiminnallisuutta ja vaatia toteuttajilta vain pienen osan. Esimerkiksi
voisimme määritellä `Summary`-traitin niin, että sillä on `summarize_author`-metodi,
jonka toteutus on pakollinen, ja sitten määritellä `summarize`-metodin, jolla on
oletustoteutus, joka kutsuu `summarize_author`-metodia:

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/lib.rs:here}}
```

Käyttääksemme tätä `Summary`-versiota, meidän täytyy määritellä vain
`summarize_author`, kun toteutamme traitin tyypille:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/lib.rs:impl}}
```

Kun olemme määritelleet `summarize_author`:in, voimme kutsua `summarize`:a
`SocialPost`-rakenteen instansseilla, ja `summarize`:n oletustoteutus kutsuu
tarjoamaamme `summarize_author`:n määritystä. Koska olemme toteuttaneet
`summarize_author`:in, `Summary`-trait on antanut meille `summarize`-metodin
käyttäytymisen vaatimatta meitä kirjoittamaan enempää koodia. Se näyttää tältä:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/main.rs:here}}
```

Tämä koodi tulostaa `1 new post: (Read more from @horse_ebooks...)`.

Huomaa, että oletustoteutusta ei voi kutsua saman metodin ylikirjoittavasta
toteutuksesta.

### Traitit parametreina

Nyt kun tiedät, miten traitteja määritellään ja toteutetaan, voimme tutkia, miten
traitteja käytetään määrittelemään funktioita, jotka hyväksyvät monia eri tyyppejä.
Käytämme listauksessa 10-13 `NewsArticle`- ja `SocialPost`-tyypeille toteuttamaamme
`Summary`-traitia määritelläksemme `notify`-funktion, joka kutsuu `summarize`-metodia
`item`-parametrillaan, joka on jokin tyyppi, joka toteuttaa `Summary`-traitin.
Teemme tämän käyttämällä `impl Trait` -syntaksia, näin:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-04-traits-as-parameters/src/lib.rs:here}}
```

Sen sijaan, että `item`-parametrilla olisi konkreettinen tyyppi, määrittelemme
`impl`-avainsanan ja traitin nimen. Tämä parametri hyväksyy minkä tahansa tyypin,
joka toteuttaa määritellyn traitin. `notify`-funktion rungossa voimme kutsua
`item`:iin liittyviä metodeja, jotka tulevat `Summary`-traitista, kuten
`summarize`. Voimme kutsua `notify`:a ja välittää sille minkä tahansa `NewsArticle`- tai
`SocialPost`-instanssin. Koodi, joka kutsuu funktiota millä tahansa muulla tyypillä,
kuten `String` tai `i32`, ei käänny, koska nämä tyypit eivät toteuta `Summary`:a.

<!-- Old headings. Do not remove or links may break. -->

<a id="fixing-the-largest-function-with-trait-bounds"></a>

#### Trait-rajojen syntaksi

`impl Trait` -syntaksi toimii suoraviivaisissa tapauksissa, mutta se on itse asiassa
syntaktista sokeria pidemmälle muodolle, joka tunnetaan nimellä _trait-raja_; se
näyttää tältä:

```rust,ignore
pub fn notify<T: Summary>(item: &T) {
    println!("Breaking news! {}", item.summarize());
}
```

Tämä pidempi muoto on vastaava kuin edellisen osion esimerkki, mutta on
sanarikkaampi. Sijoitamme trait-rajat geneerisen tyyppiparametrin ilmoitukseen
kaksoispisteen jälkeen kulmasulkeiden sisään.

`impl Trait` -syntaksi on kätevä ja tekee koodista tiiviimpää yksinkertaisissa
tapauksissa, kun taas täydellisempi trait-rajojen syntaksi voi ilmaista enemmän
monimutkaisuutta muissa tapauksissa. Esimerkiksi voimme olla kaksi parametria,
jotka toteuttavat `Summary`:n. Tämän tekeminen `impl Trait` -syntaksilla näyttää
tältä:

```rust,ignore
pub fn notify(item1: &impl Summary, item2: &impl Summary) {
```

`impl Trait` on sopiva, jos haluamme tämän funktion sallivan `item1`:n ja `item2`:n
olla eri tyyppejä (kunhan molemmat tyypit toteuttavat `Summary`:n). Jos kuitenkin
haluamme pakottaa molemmat parametrit olemaan samaa tyyppiä, meidän täytyy käyttää
trait-rajaa, näin:

```rust,ignore
pub fn notify<T: Summary>(item1: &T, item2: &T) {
```

Geneerinen tyyppi `T`, joka on määritelty `item1`- ja `item2`-parametrien tyypiksi,
rajoittaa funktiota niin, että `item1`:lle ja `item2`:lle argumenttina välitetyn
arvon konkreettisen tyypin täytyy olla sama.

#### Useiden trait-rajojen määrittely `+`-syntaksilla

Voimme myös määrittää useamman kuin yhden trait-rajan. Sanotaan, että haluamme
`notify`:n käyttävän näyttömuotoilua sekä `summarize`:a `item`:issä: määrittelemme
`notify`-määrityksessä, että `item`:in täytyy toteuttaa sekä `Display` että
`Summary`. Voimme tehdä sen käyttämällä `+`-syntaksia:

```rust,ignore
pub fn notify(item: &(impl Summary + Display)) {
```

`+`-syntaksi on kelvollinen myös geneeristen tyyppien trait-rajoissa:

```rust,ignore
pub fn notify<T: Summary + Display>(item: &T) {
```

Kun kaksi trait-rajaa on määritelty, `notify`-funktion runko voi kutsua
`summarize`:a ja käyttää `{}`:a muotoillakseen `item`:in.

#### Selkeämmät trait-rajat `where`-lausekkeilla

Liian monien trait-rajojen käytöllä on haittapuolensa. Jokaisella geneerisellä
tyypillä on omat trait-rajansa, joten funktioilla, joilla on useita geneerisiä
tyyppiparametreja, voi olla paljon trait-rajoihin liittyvää tietoa funktion nimen
ja parametrilistan välissä, mikä tekee funktion allekirjoituksesta vaikeasti
luettavan. Tästä syystä Rustissa on vaihtoehtoinen syntaksi trait-rajojen
määrittelyyn `where`-lausekkeessa funktion allekirjoituksen jälkeen. Sen sijaan,
että kirjoittaisimme tämän:

```rust,ignore
fn some_function<T: Display + Clone, U: Clone + Debug>(t: &T, u: &U) -> i32 {
```

voimme käyttää `where`-lauseketta, näin:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-07-where-clause/src/lib.rs:here}}
```

Tämän funktion allekirjoitus on vähemmän sekava: funktion nimi, parametrilista
ja paluutyyppi ovat lähellä toisiaan, samoin kuin funktiossa, jossa ei ole paljon
trait-rajoja.

### Traitin toteuttavan tyypin palauttaminen

Voimme käyttää `impl Trait` -syntaksia myös palautuspaikassa palauttaaksemme
jonkin traitin toteuttavan tyypin arvon, kuten tässä:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-05-returning-impl-trait/src/lib.rs:here}}
```

Käyttämällä `impl Summary` paluutyypiksi määrittelemme, että `returns_summarizable`-funktio
palauttaa jonkin `Summary`-traitin toteuttavan tyypin nimeämättä konkreettista
tyyppiä. Tässä tapauksessa `returns_summarizable` palauttaa `SocialPost`:in, mutta
tätä funktiota kutsuvan koodin ei tarvitse tietää sitä.

Mahdollisuus määrittää paluutyyppi vain sen toteuttaman traitin perusteella on
erityisen hyödyllinen sulkeumien ja iteraattorien yhteydessä, joita käsittelemme
luvussa 13. Sulkeumat ja iteraattorit luovat tyyppejä, jotka vain kääntäjä tietää,
tai tyyppejä, joiden määrittely on hyvin pitkä. `impl Trait` -syntaksi antaa
sinun määrittää tiiviisti, että funktio palauttaa jonkin `Iterator`-traitin
toteuttavan tyypin kirjoittamatta hyvin pitkää tyyppiä.

Voit kuitenkin käyttää `impl Trait` -syntaksia vain, jos palautat yhden tyypin.
Esimerkiksi tämä koodi, joka palauttaa joko `NewsArticle`:n tai `SocialPost`:in
paluutyypin ollessa `impl Summary`, ei toimisi:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-06-impl-trait-returns-one-type/src/lib.rs:here}}
```

Joko `NewsArticle`:n tai `SocialPost`:in palauttaminen ei ole sallittua `impl Trait`
-syntaksin toteutuksen rajoitusten vuoksi kääntäjässä. Käsittelemme, miten
kirjoitetaan funktio tällä käyttäytymisellä, [”Trait-objektien käyttö eri tyyppisten
arvojen sallimiseksi”][using-trait-objects-that-allow-for-values-of-different-types]<!-- ignore
-->-osiossa luvussa 18.

### Trait-rajojen käyttö metodien ehdolliseen toteuttamiseen

Käyttämällä trait-rajaa `impl`-lohkossa, joka käyttää geneerisiä tyyppiparametreja,
voimme toteuttaa metodeja ehdollisesti tyypeille, jotka toteuttavat määritellyt
traitit. Esimerkiksi tyyppi `Pair<T>` listauksessa 10-15 toteuttaa aina `new`-funktion
palauttaakseen uuden `Pair<T>`-instanssin (muista luvun 5 [”Metodien määrittely”][methods]<!-- ignore --> -osiosta, että `Self` on tyyppialias `impl`-lohkon tyypille, joka tässä tapauksessa on `Pair<T>`). Mutta seuraavassa `impl`-lohkossa `Pair<T>` toteuttaa `cmp_display`-metodin vain, jos sen sisäinen tyyppi `T` toteuttaa `PartialOrd`-traitin, joka mahdollistaa vertailun, _ja_ `Display`-traitin, joka mahdollistaa tulostamisen.

<Listing number="10-15" file-name="src/lib.rs" caption="Metodien ehdollinen toteuttaminen geneeriselle tyypille trait-rajojen mukaan">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-15/src/lib.rs}}
```

</Listing>

Voimme myös toteuttaa traitin ehdollisesti mille tahansa tyypille, joka toteuttaa
toisen traitin. Traitin toteutukset mille tahansa tyypille, joka täyttää
trait-rajat, kutsutaan _yleistoteutuksiksi_ (*blanket implementations*), ja niitä
käytetään laajasti Rustin standardikirjastossa. Esimerkiksi standardikirjasto
toteuttaa `ToString`-traitin mille tahansa tyypille, joka toteuttaa `Display`-traitin.
Standardikirjaston `impl`-lohko näyttää suunnilleen tältä:

```rust,ignore
impl<T: Display> ToString for T {
    // --snip--
}
```

Koska standardikirjastossa on tämä yleistoteutus, voimme kutsua `ToString`-traitin
määrittelemää `to_string`-metodia millä tahansa tyypillä, joka toteuttaa
`Display`-traitin. Esimerkiksi voimme muuntaa kokonaisluvut vastaaviksi
`String`-arvoikseen näin, koska kokonaisluvut toteuttavat `Display`:n:

```rust
let s = 3.to_string();
```

Yleistoteutukset näkyvät traitin dokumentaatiossa ”Implementors”-osiossa.

Traitit ja trait-rajat antavat meille mahdollisuuden kirjoittaa koodia, joka
käyttää geneerisiä tyyppiparametreja toiston vähentämiseksi, mutta myös kertoa
kääntäjälle, että haluamme geneerisen tyypin omaavan tiettyä käyttäytymistä.
Kääntäjä voi sitten käyttää trait-rajoihin liittyvää tietoa tarkistaakseen,
että kaikki koodissamme käytetyt konkreettiset tyypit tarjoavat oikean
käyttäytymisen. Dynaamisesti tyypitetyissä kielissä saisimme virheen ajonaikana,
jos kutsuisimme metodia tyypille, joka ei määrittele metodia. Rust siirtää nämä
virheet käännösaikaan, joten meidän täytyy korjata ongelmat ennen kuin koodimme
pystyy edes suorittumaan. Lisäksi emme joudu kirjoittamaan koodia, joka tarkistaa
käyttäytymistä ajonaikana, koska olemme jo tarkistaneet käännösaikana. Näin
parannamme suorituskykyä luopumatta geneeristen tyyppien joustavuudesta.

[using-trait-objects-that-allow-for-values-of-different-types]: ch18-02-trait-objects.html#using-trait-objects-that-allow-for-values-of-different-types
[methods]: ch05-03-method-syntax.html#defining-methods
