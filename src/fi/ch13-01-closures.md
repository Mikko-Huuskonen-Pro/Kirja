<!-- Old heading. Do not remove or links may break. -->

<a id="closures-anonymous-functions-that-can-capture-their-environment"></a>

## Sulkeumat: anonyymit funktiot, jotka sieppaavat ympäristönsä

Rustin sulkeumat ovat anonyymejä funktioita, jotka voidaan tallentaa muuttujaan tai
välittää argumenttina toisille funktioille. Sulkeuman voi määrittää yhdessä paikassa ja
kutsua sitä myöhemmin toisessa yhteydessä sen arvioimiseksi. Toisin kuin funktiot,
sulkeumat voivat siepata arvoja siitä laajuudesta, jossa ne on määritelty. Näytämme,
miten nämä sulkeumien ominaisuudet mahdollistavat koodin uudelleenkäytön ja
käyttäytymisen mukauttamisen.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-an-abstraction-of-behavior-with-closures"></a>
<a id="refactoring-using-functions"></a>
<a id="refactoring-with-closures-to-store-code"></a>

### Ympäristön sieppaaminen sulkeumilla

Tarkastelemme ensin, miten voimme käyttää sulkeumia sieppaamaan arvoja määrittelynsä
ympäristöstä myöhempää käyttöä varten. Tässä on skenaario: aika ajoin T-paitayrityksemme
antaa eksklusiivisen, rajoitetun erän paidan postituslistallamme olevalle henkilölle
kampanjana. Postituslistan jäsenet voivat halutessaan lisätä suosikkivärinsä profiiliinsa.
Jos ilmaispaidan voittajalla on suosikkiväri asetettuna, hän saa sen värisen paidan. Jos
henkilö ei ole määrittänyt suosikkiväriä, hän saa sen värin, jota yrityksellä on tällä
hetkellä eniten varastossa.

Tämän toteuttamiseen on monia tapoja. Tässä esimerkissä käytämme `ShirtColor`-enumia,
jolla on variantit `Red` ja `Blue` (rajoitamme värien määrän yksinkertaisuuden vuoksi).
Yrityksen varastoa edustaa `Inventory`-rakenne, jossa on `shirts`-kenttä, joka sisältää
`Vec<ShirtColor>`-vektorin varastossa olevista paidan väreistä. `Inventory`-rakenteelle
määritelty `giveaway`-metodi saa ilmaispaidan voittajan valinnaisen paidan väripreferenssin
ja palauttaa värin, jonka henkilö saa. Tämä asetelma on esitetty listauksessa 13-1:

<Listing number="13-1" file-name="src/main.rs" caption="T-paitayrityksen kampanjatilanne">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-01/src/main.rs}}
```

</Listing>

`main`-funktiossa määritellyssä `store`-muuttujassa on kaksi sinistä ja yksi punainen paita
jäljellä jaettavaksi tässä rajoitetun erän kampanjassa. Kutsumme `giveaway`-metodia
käyttäjälle, joka haluaa punaisen paidan, ja käyttäjälle, jolla ei ole mitään preferenssiä.

Tämän koodin voisi toteuttaa monin tavoin, ja tässä keskitymme sulkeumiin, joten olemme
pysytelleet käsitteissä, jotka olet jo oppinut, lukuun ottamatta `giveaway`-metodin runkoa,
joka käyttää sulkeumaa. `giveaway`-metodissa saamme käyttäjän preferenssin parametrina
tyypiltä `Option<ShirtColor>` ja kutsumme `unwrap_or_else`-metodia `user_preference`-arvolla.
[`unwrap_or_else`-metodi tyypille `Option<T>`][unwrap-or-else]<!-- ignore --> on määritelty
standardikirjastossa. Se ottaa yhden argumentin: sulkeuman ilman argumentteja, joka palauttaa
arvon `T` (saman tyypin, joka on tallennettuna `Option<T>`-tyypin `Some`-varianttiin; tässä
tapauksessa `ShirtColor`). Jos `Option<T>` on `Some`-variantti, `unwrap_or_else` palauttaa
arvon `Some`-variantin sisältä. Jos `Option<T>` on `None`-variantti, `unwrap_or_else` kutsuu
sulkeumaa ja palauttaa sulkeuman palauttaman arvon.

Määrittelemme sulkeumalausekkeen `|| self.most_stocked()` argumentiksi `unwrap_or_else`-metodille.
Tämä on sulkeuma, joka ei itse ota parametreja (jos sulkeumalla olisi parametreja, ne
näkyisivät kahden pystyviivan välissä). Sulkeuman runko kutsuu `self.most_stocked()`-metodia.
Määrittelemme sulkeuman tässä, ja `unwrap_or_else`-metodin toteutus arvioi sulkeuman myöhemmin,
jos tulos tarvitaan.

Tämän koodin suorittaminen tulostaa:

```console
{{#include ../listings/ch13-functional-features/listing-13-01/output.txt}}
```

Yksi mielenkiintoinen näkökohta on, että olemme välittäneet sulkeuman, joka kutsuu
`self.most_stocked()`-metodia nykyisellä `Inventory`-instanssilla. Standardikirjaston ei
tarvinnut tietää mitään määrittelemistämme `Inventory`- tai `ShirtColor`-tyypeistä tai
logiikasta, jota haluamme käyttää tässä skenaariossa. Sulkeuma sieppaa muuttumattoman
viittauksen `self`-`Inventory`-instanssiin ja välittää sen määrittelemämme koodin kanssa
`unwrap_or_else`-metodille. Funktiot puolestaan eivät pysty sieppaamaan ympäristöään tällä
tavalla.

### Sulkeumien tyyppipäätelmä ja annotointi

Funktioiden ja sulkeumien välillä on muitakin eroja. Sulkeumat eivät yleensä vaadi
parametrien tai palautusarvon tyyppien annotointia kuten `fn`-funktiot. Funktioissa
tyyppiannotaatiot ovat pakollisia, koska tyypit ovat osa käyttäjille paljastettua
eksplisiittistä rajapintaa. Tämän rajapinnan jäykkä määrittely on tärkeää varmistaakseen,
että kaikki ovat samaa mieltä siitä, minkä tyyppisiä arvoja funktio käyttää ja palauttaa.
Sulkeumia ei puolestaan käytetä tällaisessa paljastetussa rajapinnassa: ne tallennetaan
muuttujiin ja käytetään nimeämättä niitä ja paljastamatta niitä kirjastomme käyttäjille.

Sulkeumat ovat tyypillisesti lyhyitä ja merkityksellisiä vain kapeassa kontekstissa eivätkä
missä tahansa satunnaisessa skenaariossa. Näissä rajallisissa konteksteissa kääntäjä pystyy
päättelemään parametrien ja palautustyypin tyypit, samoin kuin se pystyy päättelemään useimpien
muuttujien tyypit (on harvinaisia tapauksia, joissa kääntäjä tarvitsee myös sulkeuman
tyyppiannotaatioita).

Kuten muuttujien kanssa, voimme lisätä tyyppiannotaatioita, jos haluamme lisätä eksplisiittisyyttä
ja selkeyttä kustannuksella siitä, että olemme sanallisempia kuin on ehdottoman välttämätöntä.
Sulkeuman tyyppien annotointi näyttäisi listauksessa 13-2 esitetyltä määrittelyltä. Tässä
esimerkissä määrittelemme sulkeuman ja tallennamme sen muuttujaan sen sijaan, että määrittäisimme
sulkeuman siinä kohdassa, jossa välitämme sen argumenttina, kuten teimme listauksessa 13-1.

<Listing number="13-2" file-name="src/main.rs" caption="Sulkeuman parametrin ja palautusarvon tyyppien valinnaisten tyyppiannotaatioiden lisääminen">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-02/src/main.rs:here}}
```

</Listing>

Tyyppiannotaatioiden lisäämisen jälkeen sulkeumien syntaksi näyttää enemmän funktioiden
syntaksilta. Tässä määrittelemme funktion, joka lisää 1 parametrilleen, ja sulkeuman, jolla
on sama käyttäytyminen, vertailua varten. Olemme lisänneet välilyöntejä kohdistaaksemme
asiaankuuluvat osat. Tämä havainnollistaa, miten sulkeumien syntaksi on samankaltainen
kuin funktioiden syntaksi, paitsi pystyviivojen käyttö ja valinnaisen syntaksin määrä:

```rust,ignore
fn  add_one_v1   (x: u32) -> u32 { x + 1 }
let add_one_v2 = |x: u32| -> u32 { x + 1 };
let add_one_v3 = |x|             { x + 1 };
let add_one_v4 = |x|               x + 1  ;
```

Ensimmäinen rivi näyttää funktion määrittelyn, ja toinen rivi näyttää täysin annotoidun
sulkeuman määrittelyn. Kolmannella rivillä poistamme tyyppiannotaatiot sulkeuman määrittelystä.
Neljännellä rivillä poistamme aaltosulkeet, jotka ovat valinnaisia, koska sulkeuman rungossa
on vain yksi lauseke. Nämä ovat kaikki kelvollisia määrittelyjä, jotka tuottavat saman
käyttäytymisen, kun niitä kutsutaan. `add_one_v3`- ja `add_one_v4`-rivit vaativat sulkeumien
arviointia, jotta ne voivat kääntyä, koska tyypit päätellään niiden käytöstä. Tämä on
samankaltaista kuin `let v = Vec::new();`, joka vaatii joko tyyppiannotaatioita tai jonkin
tyypin arvoja lisättäväksi `Vec`-kokoelmaan, jotta Rust pystyy päättelemään tyypin.

Sulkeumien määrittelyissä kääntäjä päättelee yhden konkreettisen tyypin kullekin niiden
parametrille ja palautusarvolle. Esimerkiksi listaus 13-3 näyttää lyhyen sulkeuman määrittelyn,
joka vain palauttaa parametrina saamansa arvon. Tämä sulkeuma ei ole kovin hyödyllinen muuten
kuin tämän esimerkin tarkoituksia varten. Huomaa, ettemme ole lisänneet määrittelyyn mitään
tyyppiannotaatioita. Koska tyyppiannotaatioita ei ole, voimme kutsua sulkeumaa millä tahansa
tyypillä, minkä olemme tehneet tässä ensimmäisellä kerralla `String`-tyypillä. Jos yritämme
sitten kutsua `example_closure`-sulkeumaa kokonaisluvulla, saamme virheen.

<Listing number="13-3" file-name="src/main.rs" caption="Yritys kutsua sulkeumaa, jonka tyypit on päätelty, kahdella eri tyypillä">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-03/src/main.rs:here}}
```

</Listing>

Kääntäjä antaa meille tämän virheen:

```console
{{#include ../listings/ch13-functional-features/listing-13-03/output.txt}}
```

Ensimmäisellä kerralla, kun kutsumme `example_closure`-sulkeumaa `String`-arvolla, kääntäjä
päättelee `x`:n tyypiksi ja sulkeuman palautustyypiksi `String`. Nämä tyypit lukitaan sitten
`example_closure`-sulkeumaan, ja saamme tyyppivirheen, kun yritämme seuraavaksi käyttää
eri tyyppiä saman sulkeuman kanssa.

### Viittausten sieppaaminen tai omistajuuden siirtäminen

Sulkeumat voivat siepata arvoja ympäristöstään kolmella tavalla, jotka vastaavat suoraan
kolmea tapaa, joilla funktio voi ottaa parametrin: lainata muuttumattomasti, lainata
muuttuvasti ja ottaa omistajuuden. Sulkeuma päättää, kumpaa näistä käyttää, sen perusteella,
mitä funktion runko tekee siepatuille arvoille.

Listauksessa 13-4 määrittelemme sulkeuman, joka sieppaa muuttumattoman viittauksen `list`-nimiseen
vektoriin, koska se tarvitsee vain muuttumattoman viittauksen arvon tulostamiseen:

<Listing number="13-4" file-name="src/main.rs" caption="Muuttumattoman viittauksen sieppaavan sulkeuman määrittely ja kutsuminen">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-04/src/main.rs}}
```

</Listing>

Tämä esimerkki havainnollistaa myös, että muuttuja voi sitoutua sulkeuman määrittelyyn, ja
voimme myöhemmin kutsua sulkeumaa käyttämällä muuttujan nimeä ja sulkeita ikään kuin muuttujan
nimi olisi funktion nimi.

Koska voimme olla samanaikaisesti useita muuttumattomia viittauksia `list`-muuttujaan, `list`
on edelleen käytettävissä koodista ennen sulkeuman määrittelyä, sulkeuman määrittelyn jälkeen
mutta ennen sulkeuman kutsumista ja sulkeuman kutsumisen jälkeen. Tämä koodi kääntyy, suorittuu
ja tulostaa:

```console
{{#include ../listings/ch13-functional-features/listing-13-04/output.txt}}
```

Seuraavaksi listauksessa 13-5 muutamme sulkeuman runkoa niin, että se lisää elementin `list`-vektoriin.
Sulkeuma sieppaa nyt muuttuvan viittauksen:

<Listing number="13-5" file-name="src/main.rs" caption="Muuttuvan viittauksen sieppaavan sulkeuman määrittely ja kutsuminen">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-05/src/main.rs}}
```

</Listing>

Tämä koodi kääntyy, suorittuu ja tulostaa:

```console
{{#include ../listings/ch13-functional-features/listing-13-05/output.txt}}
```

Huomaa, ettei `println!`-kutsua ole enää `borrows_mutably`-sulkeuman määrittelyn ja kutsumisen
välissä: kun `borrows_mutably` määritellään, se sieppaa muuttuvan viittauksen `list`-muuttujaan.
Emme käytä sulkeumaa uudelleen sen kutsumisen jälkeen, joten muuttuva laina päättyy. Sulkeuman
määrittelyn ja kutsumisen välissä muuttumatonta lainaa tulostusta varten ei sallita, koska muita
lainoja ei sallita, kun on muuttuva laina. Kokeile lisätä `println!`-kutsu sinne ja katso,
millaisen virheilmoituksen saat!

Jos haluat pakottaa sulkeuman ottamaan omistajuuden arvoista, joita se käyttää ympäristössään,
vaikka sulkeuman runko ei ehdottomasti tarvitsisikaan omistajuutta, voit käyttää `move`-avainsanaa
parametrilistan edessä.

Tämä tekniikka on enimmäkseen hyödyllinen, kun välitetään sulkeuma uudelle säikeelle siirtämään
data niin, että uusi säie omistaa sen. Käsittelemme säikeitä ja syitä niiden käyttöön
yksityiskohtaisesti luvussa 16 puhuessamme rinnakkaisuudesta, mutta tutkitaan nyt lyhyesti
uuden säikeen luomista sulkeumalla, joka tarvitsee `move`-avainsanan. Listaus 13-6 näyttää
listauksen 13-4 muutetun version, joka tulostaa vektorin uudessa säikeessä pääsäikeen sijaan:

<Listing number="13-6" file-name="src/main.rs" caption="`move`-avainsanan käyttö pakottamaan säikeen sulkeuma ottamaan omistajuuden `list`-muuttujasta">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-06/src/main.rs}}
```

</Listing>

Luomme uuden säikeen antamalla säikeelle sulkeuman argumenttina suoritettavaksi. Sulkeuman
runko tulostaa listan. Listauksessa 13-4 sulkeuma sieppasi `list`-muuttujan vain muuttumattomalla
viittauksella, koska se on vähimmän määrä pääsyä `list`-muuttujaan sen tulostamiseen. Tässä
esimerkissä, vaikka sulkeuman runko tarvitsee edelleen vain muuttumattoman viittauksen, meidän
täytyy määrittää, että `list` siirretään sulkeumaan asettamalla `move`-avainsana sulkeuman
määrittelyn alkuun. Uusi säie saattaa valmistua ennen kuin pääsäie valmistuu, tai pääsäie
saattaa valmistua ensin. Jos pääsäie säilyttäisi omistajuuden `list`-muuttujaan mutta päättyisi
ennen uutta säiettä ja pudottaisi `list`-muuttujan, säikeen muuttumaton viittaus olisi virheellinen.
Siksi kääntäjä vaatii, että `list` siirretään uudelle säikeelle annettuun sulkeumaan, jotta
viittaus olisi kelvollinen. Kokeile poistaa `move`-avainsana tai käyttää `list`-muuttujaa
pääsäikeessä sulkeuman määrittelyn jälkeen ja katso, mitä kääntäjävirheitä saat!

<!-- Old headings. Do not remove or links may break. -->

<a id="storing-closures-using-generic-parameters-and-the-fn-traits"></a>
<a id="limitations-of-the-cacher-implementation"></a>
<a id="moving-captured-values-out-of-the-closure-and-the-fn-traits"></a>

### Kaapattujen arvojen siirtäminen sulkeumasta ja `Fn`-traitit

Kun sulkeuma on siepannut viittauksen tai ottanut omistajuuden arvosta sulkeuman määrittelypaikan
ympäristöstä (vaikuttaen siihen, mitä, jos mitään, siirretään sulkeumaan _sisään_), sulkeuman
rungon koodi määrittää, mitä viittauksille tai arvoille tapahtuu, kun sulkeuma arvioidaan myöhemmin
(vaikuttaen siihen, mitä, jos mitään, siirretään sulkeumasta _ulos_). Sulkeuman runko voi tehdä
mitä tahansa seuraavista: siirtää siepatun arvon sulkeumasta ulos, mutatoida siepattua arvoa,
ei siirtää eikä mutatoida arvoa, tai olla alun perin sieppaamatta mitään ympäristöstä.

Tapa, jolla sulkeuma sieppaa ja käsittelee arvoja ympäristöstä, vaikuttaa siihen, mitä traitteja
sulkeuma toteuttaa, ja traittien avulla funktiot ja rakenteet voivat määrittää, millaisia sulkeumia
ne voivat käyttää. Sulkeumat toteuttavat automaattisesti yhden, kaksi tai kaikki kolme näistä
`Fn`-traiteista additiivisesti sen perusteella, miten sulkeuman runko käsittelee arvoja:

1. `FnOnce` koskee sulkeumia, joita voidaan kutsua kerran. Kaikki sulkeumat toteuttavat
   vähintään tämän traitin, koska kaikkia sulkeumia voidaan kutsua. Sulkeuma, joka siirtää
   siepatut arvot rungostaan ulos, toteuttaa vain `FnOnce`-traitin eikä mitään muista `Fn`-traiteista,
   koska sitä voidaan kutsua vain kerran.
2. `FnMut` koskee sulkeumia, jotka eivät siirrä siepattuja arvoja rungostaan ulos, mutta
   jotka saattavat mutatoida siepattuja arvoja. Näitä sulkeumia voidaan kutsua useammin kuin
   kerran.
3. `Fn` koskee sulkeumia, jotka eivät siirrä siepattuja arvoja rungostaan ulos eivätkä mutatoi
   siepattuja arvoja, sekä sulkeumia, jotka eivät sieppaa mitään ympäristöstään. Näitä sulkeumia
   voidaan kutsua useammin kuin kerran mutatoimatta ympäristöään, mikä on tärkeää tapauksissa,
   kuten sulkeuman kutsumisessa useita kertoja rinnakkain.

Katsotaan `unwrap_or_else`-metodin määrittelyä tyypille `Option<T>`, jota käytimme listauksessa 13-1:

```rust,ignore
impl<T> Option<T> {
    pub fn unwrap_or_else<F>(self, f: F) -> T
    where
        F: FnOnce() -> T
    {
        match self {
            Some(x) => x,
            None => f(),
        }
    }
}
```

Muista, että `T` on geneerinen tyyppi, joka edustaa arvon tyyppiä `Option`-tyypin `Some`-variantissa.
Tyyppi `T` on myös `unwrap_or_else`-funktion palautustyyppi: koodi, joka kutsuu `unwrap_or_else`-metodia
`Option<String>`-arvolla, esimerkiksi, saa `String`-arvon.

Seuraavaksi huomaa, että `unwrap_or_else`-funktiolla on lisägeneerinen tyyppiparametri `F`. `F`-tyyppi
on parametrin `f` tyyppi, joka on sulkeuma, jonka annamme kutsuessamme `unwrap_or_else`-metodia.

Geneeriselle tyypille `F` määritelty trait-raja on `FnOnce() -> T`, mikä tarkoittaa, että `F`:n
täytyy voida kutsua kerran, olla ilman argumentteja ja palauttaa `T`. `FnOnce`-traitin käyttö
trait-rajassa ilmaisee rajoitteen, että `unwrap_or_else` kutsuu `f`:ää korkeintaan kerran.
`unwrap_or_else`-metodin rungossa näemme, että jos `Option` on `Some`, `f`:ää ei kutsuta. Jos
`Option` on `None`, `f`:ää kutsutaan kerran. Koska kaikki sulkeumat toteuttavat `FnOnce`-traitin,
`unwrap_or_else` hyväksyy kaikki kolme sulkeumatyyppiä ja on niin joustava kuin mahdollista.

> Huom: Jos haluamamme ei vaadi arvon sieppaamista ympäristöstä, voimme käyttää funktion nimeä
> sulkeuman sijaan. Voimme esimerkiksi kutsua `unwrap_or_else(Vec::new)`-metodia `Option<Vec<T>>`-arvolla
> saadaksemme uuden tyhjän vektorin, jos arvo on `None`. Kääntäjä toteuttaa automaattisesti sen
> `Fn`-traiteista, joka soveltuu funktion määrittelyyn.

Katsotaan nyt standardikirjaston `sort_by_key`-metodin määrittelyä viipaleille nähdäksemme, miten
se eroaa `unwrap_or_else`-metodista ja miksi `sort_by_key` käyttää `FnMut`-traitia `FnOnce`-traitin
sijaan trait-rajana. Sulkeuma saa yhden argumentin viittauksena tarkasteltavan viipaleen nykyiseen
alkioon ja palauttaa järjestettävän tyypin `K` arvon. Tämä funktio on hyödyllinen, kun haluat
järjestää viipaleen jonkin kunkin alkion ominaisuuden mukaan. Listauksessa 13-7 meillä on lista
`Rectangle`-instansseja, ja käytämme `sort_by_key`-metodia järjestääksemme ne `width`-ominaisuuden
mukaan alhaalta ylös:

<Listing number="13-7" file-name="src/main.rs" caption="`sort_by_key`-metodin käyttö suorakulmioiden järjestämiseen leveyden mukaan">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-07/src/main.rs}}
```

</Listing>

Tämä koodi tulostaa:

```console
{{#include ../listings/ch13-functional-features/listing-13-07/output.txt}}
```

Syy siihen, että `sort_by_key` on määritelty ottamaan `FnMut`-sulkeuma, on se, että se kutsuu
sulkeumaa useita kertoja: kerran kullekin viipaleen alkiolle. Sulkeuma `|r| r.width` ei sieppaa,
mutatoi tai siirrä mitään ulos ympäristöstään, joten se täyttää trait-rajavaatimukset.

Sitä vastoin listaus 13-8 näyttää esimerkin sulkeumasta, joka toteuttaa vain `FnOnce`-traitin,
koska se siirtää arvon ympäristöstään ulos. Kääntäjä ei anna meidän käyttää tätä sulkeumaa
`sort_by_key`-metodin kanssa:

<Listing number="13-8" file-name="src/main.rs" caption="Yritys käyttää `FnOnce`-sulkeumaa `sort_by_key`-metodin kanssa">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-08/src/main.rs}}
```

</Listing>

Tämä on keinotekoinen, mutkikas tapa (joka ei toimi) yrittää laskea, kuinka monta kertaa
`sort_by_key` kutsuu sulkeumaa järjestäessään `list`-muuttujaa. Tämä koodi yrittää tehdä
tämän laskennan työntämällä `value`-muuttujan — `String`-arvon sulkeuman ympäristöstä —
`sort_operations`-vektoriin. Sulkeuma sieppaa `value`-muuttujan ja siirtää sen sitten sulkeumasta
ulos siirtämällä `value`-muuttujan omistajuuden `sort_operations`-vektoriin. Tätä sulkeumaa
voidaan kutsua kerran; yritys kutsua sitä toisen kerran ei toimisi, koska `value` ei olisi
enää ympäristössä työnnettäväksi `sort_operations`-vektoriin uudelleen! Siksi tämä sulkeuma
toteuttaa vain `FnOnce`-traitin. Kun yritämme kääntää tämän koodin, saamme tämän virheen,
että `value`-muuttujaa ei voi siirtää sulkeumasta ulos, koska sulkeuman täytyy toteuttaa `FnMut`:

```console
{{#include ../listings/ch13-functional-features/listing-13-08/output.txt}}
```

Virhe osoittaa sulkeuman rungon rivin, joka siirtää `value`-muuttujan ympäristöstä ulos.
Korjataksemme tämän meidän täytyy muuttaa sulkeuman runkoa niin, ettei se siirrä arvoja
ympäristöstä ulos. Laskeaksemme, kuinka monta kertaa sulkeumaa kutsutaan, laskurin pitäminen
ympäristössä ja sen arvon kasvattaminen sulkeuman rungossa on suoraviivaisempi tapa laskea se.
Listauksen 13-9 sulkeuma toimii `sort_by_key`-metodin kanssa, koska se sieppaa vain muuttuvan
viittauksen `num_sort_operations`-laskuriin ja voidaan siksi kutsua useammin kuin kerran:

<Listing number="13-9" file-name="src/main.rs" caption="`FnMut`-sulkeuman käyttö `sort_by_key`-metodin kanssa on sallittua">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-09/src/main.rs}}
```

</Listing>

`Fn`-traitit ovat tärkeitä, kun määritellään tai käytetään funktioita tai tyyppejä, jotka
käyttävät sulkeumia. Seuraavassa osiossa käsittelemme iteraattoreita. Monet iteraattorimetodit
ottavat sulkeuma-argumentteja, joten pidä nämä sulkeumien yksityiskohdat mielessä jatkaessamme!

[unwrap-or-else]: ../std/option/enum.Option.html#method.unwrap_or_else
