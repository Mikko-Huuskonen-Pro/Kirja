<!-- Old headings. Do not remove or links may break. -->

<a id="traits-defining-shared-behavior"></a>

## Jaetun käyttäytymisen määrittely traittejen avulla

_Trait_ määrittelee toiminnallisuuden, joka tietyllä tyypillä on ja jonka se
voi jakaa muiden tyyppien kanssa. Voimme käyttää traitteja määrittelemään
jaettua käyttäytymistä abstraktisti. Voimme käyttää _trait-rajoja_ (*trait
bounds*) määrittääksemme, että geneerinen tyyppi voi olla mikä tahansa tyyppi,
jolla on tiettyä käyttäytymistä.

> Huom: Traitit muistuttavat ominaisuutta, jota muissa kielissä usein kutsutaan
> _rajapinnoiksi_ (*interfaces*), vaikka niissä on eroja.

### Traitin määrittely

Tyypin käyttäytyminen koostuu metodeista, joita voimme kutsua kyseiselle
tyypille. Eri tyypit jakavat saman käyttäytymisen, jos voimme kutsua samoja
metodeja kaikille näille tyypeille. Trait-määrittelyt ovat tapa ryhmittää
metodien allekirjoituksia yhteen määrittelemään joukko käyttäytymisiä, joita
tarvitaan jonkin tarkoituksen saavuttamiseksi.

Esimerkiksi sanotaan, että meillä on useita structeja, jotka säilyttävät
erilaisia tekstejä ja määriä: `NewsArticle`-struct, joka säilyttää uutisjutun
tietyssä paikassa, ja `SocialPost`, jossa voi olla enintään 280 merkkiä sekä
metatietoa siitä, oliko kyseessä uusi julkaisu, uudelleenjulkaisu vai vastaus
toiseen julkaisuun.

Haluamme tehdä `aggregator`-nimisen mediakoostajakirjaston, joka voi näyttää
yhteenvetoja tiedoista, jotka voivat olla `NewsArticle`- tai `SocialPost`-
instanssissa. Tarvitsemme yhteenvedon kustakin tyypistä ja pyydämme sitä
kutsumalla `summarize`-metodia instanssilla. Listaus 10-12 näyttää julkisen
`Summary`-traitin määrittelyn, joka ilmaisee tämän käyttäytymisen.

<Listing number="10-12" file-name="src/lib.rs" caption="`Summary`-trait, joka koostuu `summarize`-metodin tarjoamasta käyttäytymisestä">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-12/src/lib.rs}}
```

</Listing>

Tässä ilmoitamme traitin `trait`-avainsanalla ja sitten traitin nimen, joka
tässä tapauksessa on `Summary`. Ilmoitamme traitin myös `pub`-määritteellä,
jotta tästä cratesta riippuvat cratet voivat käyttää tätä traitia myös, kuten
näemme muutamassa esimerkissä. Aaltosulkeiden sisällä ilmoitamme metodien
allekirjoitukset, jotka kuvaavat tämän traitin toteuttavien tyyppien
käyttäytymistä, joka tässä tapauksessa on `fn summarize(&self) -> String`.

Metodin allekirjoituksen jälkeen käytämme puolipistettä aaltosulkeiden sijaan.
Jokaisen tämän traitin toteuttavan tyypin täytyy tarjota oma mukautettu
käyttäytymänsä metodin rungolle. Kääntäjä varmistaa, että jokaisella tyypillä,
jolla on `Summary`-trait, on metodi `summarize` määriteltynä täsmälleen tällä
allekirjoituksella.

Traitilla voi olla useita metodeja rungossaan: Metodien allekirjoitukset
luetellaan yksi per rivi, ja jokainen rivi päättyy puolipisteeseen.

### Traitin toteuttaminen tyypille

Nyt kun olemme määritelleet `Summary`-traitin metodien halutut allekirjoitukset,
voimme toteuttaa sen mediakoostajamme tyypeille. Listaus 10-13 näyttää
`Summary`-traitin toteutuksen `NewsArticle`-structille, joka käyttää otsikkoa,
kirjoittajaa ja sijaintia luodakseen `summarize`-metodin palautusarvon.
`SocialPost`-structille määrittelemme `summarize`-metodin käyttäjänimen
jälkeen koko julkaisun tekstin olettaen, että julkaisun sisältö on jo
rajoitettu 280 merkkiin.

<Listing number="10-13" file-name="src/lib.rs" caption="`Summary`-traitin toteuttaminen tyypeille `NewsArticle` ja `SocialPost`">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-13/src/lib.rs:here}}
```

</Listing>

Traitin toteuttaminen tyypille on samanlaista kuin tavallisten metodien
toteuttaminen. Ero on siinä, että `impl`-avainsanan jälkeen laitamme
toteutettavan traitin nimen, sitten `for`-avainsanan ja sitten tyypin nimen,
jolle haluamme toteuttaa traitin. `impl`-lohkon sisällä laitamme metodien
allekirjoitukset, jotka trait-määrittely on määritellyt. Sen sijaan, että
lisäisimme puolipisteen jokaisen allekirjoituksen jälkeen, käytämme
aaltosulkeita ja täytämme metodin rungon traitin metodien haluamalla
käyttäytymisellä kyseiselle tyypille.

Nyt kun kirjasto on toteuttanut `Summary`-traitin `NewsArticle`- ja
`SocialPost`-tyypeille, craten käyttäjät voivat kutsua trait-metodeja
`NewsArticle`- ja `SocialPost`-instansseilla samalla tavalla kuin kutsumme
tavallisia metodeja. Ainoa ero on, että käyttäjän täytyy tuoda trait
näkyviin tyyppejen ohella. Tässä on esimerkki siitä, miten binääricrate voisi
käyttää `aggregator`-kirjastocrateamme:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-01-calling-trait-method/src/main.rs}}
```

Tämä koodi tulostaa `1 new post: horse_ebooks: of course, as you probably already
know, people`.

Muut `aggregator`-cratesta riippuvat cratet voivat myös tuoda `Summary`-
traitin näkyviin toteuttaakseen `Summary`-traitin omille tyypeilleen. Yksi
rajoitus on huomionarvoista: voimme toteuttaa traitin tyypille vain, jos joko
trait tai tyyppi, tai molemmat, ovat paikallisia crateamme. Esimerkiksi voimme
toteuttaa standardikirjaston traitteja kuten `Display` mukautetulle tyypille
kuten `SocialPost` osana `aggregator`-cratemme toiminnallisuutta, koska tyyppi
`SocialPost` on paikallinen `aggregator`-cratemme. Voimme myös toteuttaa
`Summary`-traitin `Vec<T>`:lle `aggregator`-cratemme, koska trait `Summary` on
paikallinen `aggregator`-cratemme.

Emme voi kuitenkaan toteuttaa ulkoisia traitteja ulkoisille tyypeille.
Esimerkiksi emme voi toteuttaa `Display`-traitia `Vec<T>`:lle
`aggregator`-cratemme sisällä, koska `Display` ja `Vec<T>` on molemmat
määritelty standardikirjastossa eivätkä ole paikallisia `aggregator`-cratemme.
Tämä rajoitus on osa ominaisuutta nimeltä _koherenssi_ (*coherence*), ja
tarkemmin _orvokkosääntöä_ (*orphan rule*), joka on nimetty niin, koska
ylätyyppi ei ole läsnä. Tämä sääntö varmistaa, etteivät muiden ihmisten koodit
voi rikkoa sinun koodiasi ja päinvastoin. Ilman sääntöä kaksi cratea voisi
toteuttaa saman traitin samalle tyypille, eikä Rust tietäisi, mitä toteutusta
käyttää.

<!-- Old headings. Do not remove or links may break. -->

<a id="default-implementations"></a>

### Oletustoteutusten käyttö

Joskus on hyödyllistä, että traitin joillakin tai kaikilla metodeilla on
oletuskäyttäytymistä sen sijaan, että vaadittaisiin toteutuksia kaikille
metodeille jokaiselle tyypille. Sitten, kun toteutamme traitin tietylle
tyypille, voimme säilyttää tai ohittaa kunkin metodin oletuskäyttäytymisen.

Listauksessa 10-14 määrittelemme oletusmerkkijonon `Summary`-traitin
`summarize`-metodille sen sijaan, että määrittelisimme vain metodin
allekirjoituksen, kuten teimme listauksessa 10-12.

<Listing number="10-14" file-name="src/lib.rs" caption="`Summary`-traitin määrittely `summarize`-metodin oletustoteutuksella">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-14/src/lib.rs:here}}
```

</Listing>

Käyttääksemme oletustoteutusta `NewsArticle`-instanssien yhteenvetoon
määrittelemme tyhjän `impl`-lohkon `impl Summary for NewsArticle {}`.

Vaikka emme enää määrittele `summarize`-metodia suoraan `NewsArticle`-tyypille,
olemme tarjonneet oletustoteutuksen ja määritelleet, että `NewsArticle`
toteuttaa `Summary`-traitin. Näin voimme silti kutsua `summarize`-metodia
`NewsArticle`-instanssilla, näin:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-02-calling-default-impl/src/main.rs:here}}
```

Tämä koodi tulostaa `New article available! (Read more...)`.

Oletustoteutuksen luominen ei vaadi meitä muuttamaan mitään `Summary`-traitin
toteutuksesta `SocialPost`-tyypille listauksessa 10-13. Syy on, että syntaksi
oletustoteutuksen ohittamiseen on sama kuin trait-metodin toteuttamiseen, jolla
ei ole oletustoteutusta.

Oletustoteutukset voivat kutsua muita metodeja samassa traitissa, vaikka näillä
muilla metodeilla ei olisikaan oletustoteutusta. Näin trait voi tarjota paljon
hyödyllistä toiminnallisuutta ja vaatia toteuttajilta vain pienen osan
määrittelyä. Esimerkiksi voisimme määritellä `Summary`-traitille
`summarize_author`-metodin, jonka toteutus on pakollinen, ja sitten määritellä
`summarize`-metodin, jolla on oletustoteutus, joka kutsuu `summarize_author`-
metodia:

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/lib.rs:here}}
```

Käyttääksemme tätä `Summary`-traitin versiota meidän täytyy määritellä vain
`summarize_author`, kun toteutamme traitin tyypille:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/lib.rs:impl}}
```

Kun olemme määritelleet `summarize_author`-metodin, voimme kutsua `summarize`-
metodia `SocialPost`-structin instansseilla, ja `summarize`-metodin
oletustoteutus kutsuu tarjoamaamme `summarize_author`-määrittelyä. Koska olemme
toteuttaneet `summarize_author`-metodin, `Summary`-trait on antanut meille
`summarize`-metodin käyttäytymisen ilman, että meidän tarvitsee kirjoittaa
enempää koodia. Tältä se näyttää:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/main.rs:here}}
```

Tämä koodi tulostaa `1 new post: (Read more from @horse_ebooks...)`.

Huomaa, ettei ole mahdollista kutsua oletustoteutusta saman metodin ohittavasta
toteutuksesta.

<!-- Old headings. Do not remove or links may break. -->

<a id="traits-as-parameters"></a>

### Traittien käyttö parametreina

Nyt kun tiedät, miten traitteja määritellään ja toteutetaan, voimme tutkia,
miten traitteja käytetään määrittelemään funktioita, jotka hyväksyvät monia
eri tyyppejä. Käytämme `Summary`-traitia, jonka toteutimme `NewsArticle`- ja
`SocialPost`-tyypeille listauksessa 10-13, määritelläksemme `notify`-funktion,
joka kutsuu `summarize`-metodia `item`-parametrillaan, joka on jokin tyyppi,
joka toteuttaa `Summary`-traitin. Teemme tämän käyttämällä `impl Trait`-
syntaksia, näin:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-04-traits-as-parameters/src/lib.rs:here}}
```

Sen sijaan, että `item`-parametrilla olisi konkreettinen tyyppi, määrittelemme
`impl`-avainsanan ja traitin nimen. Tämä parametri hyväksyy minkä tahansa tyypin,
joka toteuttaa määritellyn traitin. `notify`-funktion rungossa voimme kutsua
mitä tahansa `item`-metodeja, jotka tulevat `Summary`-traitista, kuten
`summarize`. Voimme kutsua `notify`-funktiota ja antaa sille minkä tahansa
`NewsArticle`- tai `SocialPost`-instanssin. Koodi, joka kutsuu funktiota
millä tahansa muulla tyypillä, kuten `String` tai `i32`, ei käänny, koska nämä
tyypit eivät toteuta `Summary`-traitia.

<!-- Old headings. Do not remove or links may break. -->

<a id="fixing-the-largest-function-with-trait-bounds"></a>

#### Trait-rajasyntaksi

`impl Trait` -syntaksi toimii suoraviivaisissa tapauksissa, mutta se on itse
asiassa syntaktista sokeria pidemmälle muodolle, joka tunnetaan nimellä
_trait-raja_ (*trait bound*); se näyttää tältä:

```rust,ignore
pub fn notify<T: Summary>(item: &T) {
    println!("Breaking news! {}", item.summarize());
}
```

Tämä pidempi muoto on vastaava kuin edellisen osion esimerkki, mutta
sanallisempi. Sijoitamme trait-rajat geneerisen tyyppiparametrin ilmoituksen
jälkeen kaksoispisteen jälkeen kulmasulkeisiin.

`impl Trait` -syntaksi on kätevä ja tekee koodista tiiviimpää yksinkertaisissa
tapauksissa, kun taas täydellisempi trait-rajasyntaksi voi ilmaista monimutkaisempaa
muissa tapauksissa. Esimerkiksi voimme olla kaksi parametria, jotka toteuttavat
`Summary`-traitin. Tämä `impl Trait` -syntaksilla näyttää tältä:

```rust,ignore
pub fn notify(item1: &impl Summary, item2: &impl Summary) {
```

`impl Trait` -syntaksin käyttö on sopivaa, jos haluamme tämän funktion
sallivan `item1`:n ja `item2`:n olevan eri tyyppejä (kunhan molemmat tyypit
toteuttavat `Summary`-traitin). Jos haluamme kuitenkin pakottaa molemmat
parametrit olemaan samaa tyyppiä, meidän täytyy käyttää trait-rajaa, näin:

```rust,ignore
pub fn notify<T: Summary>(item1: &T, item2: &T) {
```

Geneerinen tyyppi `T`, joka on määritelty `item1`- ja `item2`-parametrien
tyypiksi, rajoittaa funktion siten, että argumenttina annetun arvon
konkreettisen tyypin täytyy olla sama `item1`:lle ja `item2`:lle.

<!-- Old headings. Do not remove or links may break. -->

<a id="specifying-multiple-trait-bounds-with-the--syntax"></a>

#### Useat trait-rajat `+`-syntaksilla

Voimme myös määrittää useamman kuin yhden trait-rajan. Sanotaan, että haluamme
`notify`-funktion käyttävän näyttömuotoilua sekä `summarize`-metodia
`item`-parametrilla: Määrittelemme `notify`-määrittelyssä, että `item` täytyy
toteuttaa sekä `Display` että `Summary`. Voimme tehdä näin käyttämällä `+`-
syntaksia:

```rust,ignore
pub fn notify(item: &(impl Summary + Display)) {
```

`+`-syntaksi on kelvollinen myös geneeristen tyyppien trait-rajoissa:

```rust,ignore
pub fn notify<T: Summary + Display>(item: &T) {
```

Kun kaksi trait-rajaa on määritelty, `notify`-funktion runko voi kutsua
`summarize`-metodia ja käyttää `{}`-muotoilua `item`-parametrille.

#### Selkeämmät trait-rajat `where`-lausekkeilla

Liian monien trait-rajojen käytöllä on haittapuolensa. Jokaisella geneerisellä
tyypillä on omat trait-rajansa, joten funktioilla, joilla on useita geneerisiä
tyyppiparametreja, voi olla paljon trait-rajatietoa funktion nimen ja
parametrilistan välissä, mikä tekee funktion allekirjoituksesta vaikealukuisen.
Tästä syystä Rustissa on vaihtoehtoinen syntaksi trait-rajojen määrittelyyn
`where`-lausekkeessa funktion allekirjoituksen jälkeen. Sen sijaan, että
kirjoittaisimme tämän:

```rust,ignore
fn some_function<T: Display + Clone, U: Clone + Debug>(t: &T, u: &U) -> i32 {
```

voimme käyttää `where`-lauseketta, näin:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-07-where-clause/src/lib.rs:here}}
```

Tämän funktion allekirjoitus on vähemmän sekava: Funktion nimi, parametrilista
ja palautustyyppi ovat lähellä toisiaan, samoin kuin funktiossa, jossa ei ole
paljon trait-rajoja.

### Traitin toteuttavien tyyppien palauttaminen

Voimme myös käyttää `impl Trait` -syntaksia palautuspaikassa palauttaaksemme
jonkin traitin toteuttavan tyypin arvon, kuten tässä:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-05-returning-impl-trait/src/lib.rs:here}}
```

Käyttämällä `impl Summary` palautustyypinä määrittelemme, että
`returns_summarizable`-funktio palauttaa jonkin `Summary`-traitin toteuttavan
tyypin nimeämättä konkreettista tyyppiä. Tässä tapauksessa
`returns_summarizable` palauttaa `SocialPost`-instanssin, mutta tätä funktiota
kutsuvan koodin ei tarvitse tietää sitä.

Mahdollisuus määrittää palautustyyppi vain sen toteuttaman traitin perusteella
on erityisen hyödyllinen sulkujen ja iteraattorien yhteydessä, joita käsittelemme
luvussa 13. Sulut ja iteraattorit luovat tyyppejä, jotka vain kääntäjä tuntee,
tai tyyppejä, joiden määrittely on hyvin pitkä. `impl Trait` -syntaksi antaa
sinun määrittää tiiviisti, että funktio palauttaa jonkin `Iterator`-traitin
toteuttavan tyypin ilman, että sinun tarvitsee kirjoittaa hyvin pitkää tyyppiä.

Voit kuitenkin käyttää `impl Trait` -syntaksia vain, jos palautat yhden tyypin.
Esimerkiksi tämä koodi, joka palauttaa joko `NewsArticle`- tai `SocialPost`-
instanssin palautustyypin ollessa `impl Summary`, ei toimisi:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-06-impl-trait-returns-one-type/src/lib.rs:here}}
```

Joko `NewsArticle`- tai `SocialPost`-instanssin palauttaminen ei ole sallittua
`impl Trait` -syntaksin kääntäjässä toteutettujen rajoitusten vuoksi. Käsittelemme,
miten kirjoitamme funktion tällä käyttäytymisellä luvun 18 osiossa [”Trait-
olioiden käyttö jaetun käyttäytymisen abstrahointiin”][trait-objects]<!-- ignore -->.

### Metodien ehdollinen toteuttaminen trait-rajojen avulla

Käyttämällä trait-rajaa `impl`-lohkossa, joka käyttää geneerisiä
tyyppiparametreja, voimme toteuttaa metodeja ehdollisesti tyypeille, jotka
toteuttavat määritellyt traitit. Esimerkiksi tyyppi `Pair<T>` listauksessa
10-15 toteuttaa aina `new`-funktion palauttaakseen uuden `Pair<T>`-instanssin
(muista luvun 5 [”Metodisyntaksi”][methods]<!-- ignore --> -osiosta, että
`Self` on tyyppialias `impl`-lohkon tyypille, joka tässä tapauksessa on
`Pair<T>`). Mutta seuraavassa `impl`-lohkossa `Pair<T>` toteuttaa `cmp_display`-
metodin vain, jos sen sisäinen tyyppi `T` toteuttaa `PartialOrd`-traitin, joka
mahdollistaa vertailun, _ja_ `Display`-traitin, joka mahdollistaa tulostamisen.

<Listing number="10-15" file-name="src/lib.rs" caption="Metodien ehdollinen toteuttaminen geneeriselle tyypille trait-rajojen mukaan">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-15/src/lib.rs}}
```

</Listing>

Voimme myös toteuttaa traitin ehdollisesti mille tahansa tyypille, joka
toteuttaa toisen traitin. Traitin toteutukset mille tahansa tyypille, joka
täyttää trait-rajat, kutsutaan _peittoimplementaatioiksi_ (*blanket
implementations*), ja niitä käytetään laajasti Rustin standardikirjastossa.
Esimerkiksi standardikirjasto toteuttaa `ToString`-traitin mille tahansa
tyypille, joka toteuttaa `Display`-traitin. Standardikirjaston `impl`-lohko
näyttää suunnilleen tältä:

```rust,ignore
impl<T: Display> ToString for T {
    // --snip--
}
```

Koska standardikirjastossa on tämä peittoimplementaatio, voimme kutsua
`ToString`-traitin määrittelemää `to_string`-metodia millä tahansa tyypillä,
joka toteuttaa `Display`-traitin. Esimerkiksi voimme muuttaa kokonaisluvut
vastaaviksi `String`-arvoiksi näin, koska kokonaisluvut toteuttavat `Display`-traitin:

```rust
let s = 3.to_string();
```

Peittoimplementaatiot näkyvät traitin dokumentaatiossa ”Implementors”-osiossa.

Traitit ja trait-rajat antavat meille mahdollisuuden kirjoittaa koodia, joka
käyttää geneerisiä tyyppiparametreja vähentääkseen toistoa, mutta myös
määrittää kääntäjälle, että haluamme geneerisen tyypin omaavan tiettyä
käyttäytymistä. Kääntäjä voi sitten käyttää trait-rajatietoa tarkistaakseen,
että kaikki koodissamme käytetyt konkreettiset tyypit tarjoavat oikean
käyttäytymisen. Dynaamisesti tyypitetyissä kielissä saisimme virheen
ajonaikana, jos kutsuisimme metodia tyypille, joka ei määrittele metodia. Mutta
Rust siirtää nämä virheet käännösaikaan, joten meidän täytyy korjata ongelmat
ennen kuin koodimme edes pystyy suorittumaan. Lisäksi emme tarvitse kirjoittaa
koodia, joka tarkistaa käyttäytymistä ajonaikana, koska olemme jo tarkistaneet
käännösaikana. Näin parannamme suorituskykyä luopumatta geneeristen tyyppien
joustavuudesta.

[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[methods]: ch05-03-method-syntax.html#method-syntax
