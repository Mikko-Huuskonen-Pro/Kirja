## Kehittyneet trait-ominaisuudet

Käsittelimme traitit ensin [”Traitit: jaetun käyttäytymisen määrittely”][traits-defining-shared-behavior]<!-- ignore --> -osiossa Luvussa 10, mutta emme käsitelleet kehittyneempiä yksityiskohtia. Nyt kun tiedät enemmän Rustista, voimme syventyä yksityiskohtiin.

### Assosioitujen tyyppien paikanpitäjien määrittäminen trait-määrittelyissä

_Assosioidut tyypit_ yhdistävät tyypin paikanpitäjän traitiin siten, että traitin metodimäärittelyt voivat käyttää näitä paikanpitäjiä signatuureissaan. Traitin toteuttaja määrittää konkreettisen tyypin, jota käytetään paikanpitäjän sijaan kyseisessä toteutuksessa. Näin voimme määritellä traitin, joka käyttää joitakin tyyppejä, ilman että meidän tarvitsee tietää tarkalleen, mitä nämä tyypit ovat, ennen kuin trait toteutetaan.

Olemme kuvanneet useimmat tämän luvun kehittyneistä ominaisuuksista harvoin tarvittaviksi. Assosioidut tyypit ovat jossain välissä: niitä käytetään harvemmin kuin muun kirjan käsittelemiä ominaisuuksia, mutta yleisemmin kuin monia tämän luvun muita ominaisuuksia.

Yksi esimerkki traitista, jolla on assosioitu tyyppi, on standardikirjaston tarjoama `Iterator`-trait. Assosioitu tyyppi on nimeltään `Item`, ja se edustaa niiden arvojen tyyppiä, joita `Iterator`-traitin toteuttava tyyppi iteroi. `Iterator`-traitin määrittely on esitetty Listauksessa 20-13.

<Listing number="20-13" caption="`Iterator`-traitin määrittely, jossa on assosioitu tyyppi `Item`">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-13/src/lib.rs}}
```

</Listing>

Tyyppi `Item` on paikanpitäjä, ja `next`-metodin määrittely osoittaa, että se palauttaa arvoja tyypillä `Option<Self::Item>`. `Iterator`-traitin toteuttajat määrittävät konkreettisen tyypin `Item`-tyypille, ja `next`-metodi palauttaa `Option`-arvon, joka sisältää kyseisen konkreettisen tyypin arvon.

Assosioidut tyypit saattavat vaikuttaa samankaltaiselta käsitteeltä kuin geneeriset tyypit, koska jälkimmäiset antavat meidän määritellä funktion ilman, että määrittelemme, mitä tyyppejä se voi käsitellä. Tarkastellaksemme näiden kahden käsitteen eroa, katsomme `Iterator`-traitin toteutusta tyypille nimeltä `Counter`, joka määrittää `Item`-tyypin olevan `u32`:

<Listing file-name="src/lib.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-22-iterator-on-counter/src/lib.rs:ch19}}
```

</Listing>

Tämä syntaksi vaikuttaa verrattavalta geneeristen tyyppien syntaksiin. Miksi emme siis vain määrittele `Iterator`-traitia geneerisillä tyypeillä, kuten Listauksessa 20-14 on esitetty?

<Listing number="20-14" caption="Hypoteettinen `Iterator`-traitin määrittely geneeristen tyyppien avulla">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-14/src/lib.rs}}
```

</Listing>

Ero on siinä, että kun käytämme geneerisiä tyyppejä, kuten Listauksessa 20-14, meidän täytyy merkitä tyypit jokaisessa toteutuksessa; koska voimme myös toteuttaa `Iterator<String> for Counter` tai minkä tahansa muun tyypin, voisimme olla useita `Iterator`-toteutuksia tyypille `Counter`. Toisin sanoen, kun traitilla on geneerinen parametri, se voidaan toteuttaa tyypille useita kertoja, vaihtamalla geneeristen tyyppiparametrien konkreettisia tyyppejä joka kerta. Kun käytämme `next`-metodia tyypillä `Counter`, meidän täytyisi antaa tyyppimerkinnät osoittaaksemme, mitä `Iterator`-toteutusta haluamme käyttää.

Assosioitujen tyyppien kanssa emme tarvitse merkitä tyyppejä, koska emme voi toteuttaa traitia tyypille useita kertoja. Listauksessa 20-13 assosioituja tyyppejä käyttävällä määrittelyllä voimme valita `Item`-tyypin vain kerran, koska voi olla vain yksi `impl Iterator for Counter`. Emme tarvitse määrittää, että haluamme `u32`-arvojen iteraattorin, joka kerta kun kutsumme `next`-metodia tyypillä `Counter`.

Assosioidut tyypit tulevat myös osaksi traitin sopimusta: traitin toteuttajien täytyy tarjota tyyppi assosioitua tyyppipaikanpitäjää varten. Assosioituilla tyypeillä on usein nimi, joka kuvaa, miten tyyppiä käytetään, ja assosioitujen tyyppien dokumentointi API-dokumentaatiossa on hyvä käytäntö.

### Oletusarvoiset geneeriset tyyppiparametrit ja operaatioiden ylikuormitus

Kun käytämme geneerisiä tyyppiparametreja, voimme määrittää geneeriselle tyypille oletusarvoisen konkreettisen tyypin. Tämä poistaa tarpeen traitin toteuttajien määrittää konkreettinen tyyppi, jos oletustyyppi toimii. Määrität oletustyypin, kun ilmoitat geneerisen tyypin `<PaikanpitäjäTyyppi=KonkreettinenTyyppi>`-syntaksilla.

Erinomainen esimerkki tilanteesta, jossa tämä tekniikka on hyödyllinen, on _operaatioiden ylikuormitus_, jossa mukautat operaattorin (kuten `+`) käyttäytymistä tietyissä tilanteissa.

Rust ei salli omien operaattorien luomista tai mielivaltaisten operaattorien ylikuormittamista. Voit kuitenkin ylikuormittaa operaatiot ja niihin liittyvät traitit, jotka on lueteltu `std::ops`-moduulissa, toteuttamalla operaattoriin liittyvät traitit. Esimerkiksi Listauksessa 20-15 ylikuormitamme `+`-operaattorin kahden `Point`-instanssin yhteenlaskemiseksi. Teemme tämän toteuttamalla `Add`-traitin `Point`-rakenteelle:

<Listing number="20-15" file-name="src/main.rs" caption="`Add`-traitin toteuttaminen `+`-operaattorin ylikuormittamiseksi `Point`-instansseille">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-15/src/main.rs}}
```

</Listing>

`add`-metodi laskee yhteen kahden `Point`-instanssin `x`-arvot ja kahden `Point`-instanssin `y`-arvot luodakseen uuden `Point`-instanssin. `Add`-traitilla on assosioitu tyyppi nimeltä `Output`, joka määrittää `add`-metodin palauttaman tyypin.

Oletusarvoinen geneerinen tyyppi tässä koodissa on `Add`-traitin sisällä. Tässä on sen määrittely:

```rust
trait Add<Rhs=Self> {
    type Output;

    fn add(self, rhs: Rhs) -> Self::Output;
}
```

Tämän koodin pitäisi näyttää yleisesti tutulta: trait, jolla on yksi metodi ja assosioitu tyyppi. Uusi osa on `Rhs=Self`: tätä syntaksia kutsutaan _oletusarvoisiksi tyyppiparametreiksi_. `Rhs`-geneerinen tyyppiparametri (lyhenne sanasta ”right hand side”, oikea puoli) määrittää `rhs`-parametrin tyypin `add`-metodissa. Jos emme määritä konkreettista tyyppiä `Rhs`-parametrille, kun toteutamme `Add`-traitin, `Rhs`-tyypin oletusarvo on `Self`, joka on tyyppi, jolle toteutamme `Add`-traitin.

Kun toteutimme `Add`-traitin tyypille `Point`, käytimme oletusarvoa `Rhs`-parametrille, koska halusimme laskea yhteen kaksi `Point`-instanssia. Katsotaan esimerkkiä `Add`-traitin toteutuksesta, jossa haluamme mukauttaa `Rhs`-tyypin oletusarvon sijaan.

Meillä on kaksi rakennetta, `Millimeters` ja `Meters`, jotka pitävät arvoja eri yksiköissä. Tämä olemassa olevan tyypin ohut käärintä toiseen rakenteeseen tunnetaan _newtype-mallina_, jota käsittelemme tarkemmin [”Newtype-mallin käyttö ulkoisten traitien toteuttamiseen ulkoisille tyypeille”][newtype]<!-- ignore --> -osiossa. Haluamme laskea yhteen millimetreissä olevia arvoja metreissä olevien arvojen kanssa, ja `Add`-toteutuksen pitää tehdä muunnos oikein. Voimme toteuttaa `Add`-traitin tyypille `Millimeters` siten, että `Rhs` on `Meters`, kuten Listauksessa 20-16 on esitetty.

<Listing number="20-16" file-name="src/lib.rs" caption="`Add`-traitin toteuttaminen tyypille `Millimeters` lisätäksemme `Millimeters`-arvoja `Meters`-arvoihin">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-16/src/lib.rs}}
```

</Listing>

Lisätäksemme yhteen `Millimeters`- ja `Meters`-arvoja, määritämme `impl Add<Meters>` asettaaksemme `Rhs`-tyyppiparametrin arvon oletusarvon `Self` sijaan.

Käytät oletusarvoisia tyyppiparametreja kahdella pääasiallisella tavalla:

1. Laajentaaksesi tyyppiä rikkomatta olemassa olevaa koodia
2. Salliaksesi mukautuksen tietyissä tapauksissa, joita useimmat käyttäjät eivät tarvitse

Standardikirjaston `Add`-trait on esimerkki toisesta tarkoituksesta: yleensä lasket yhteen samanlaisia tyyppejä, mutta `Add`-trait tarjoaa mahdollisuuden mukauttaa tämän lisäksi. Oletusarvoisen tyyppiparametrin käyttö `Add`-traitin määrittelyssä tarkoittaa, ettei sinun tarvitse määrittää ylimääräistä parametria useimmiten. Toisin sanoen, hieman toteutusboilerplatea ei tarvita, mikä helpottaa traitin käyttöä.

Ensimmäinen tarkoitus on samanlainen kuin toinen, mutta päinvastoin: jos haluat lisätä tyyppiparametrin olemassa olevaan traitiin, voit antaa sille oletusarvon, jotta voit laajentaa traitin toiminnallisuutta rikkomatta olemassa olevaa toteutuskoodia.

### Tarkasti määritetty syntaksi epäselvyyden poistamiseksi: saman nimisten metodien kutsuminen

Mikään Rustissa ei estä traitia sisältämästä metodia, jolla on sama nimi kuin toisen traitin metodilla, eikä Rust estä sinua toteuttamasta molempia traitteja samalle tyypille. On myös mahdollista toteuttaa metodi suoraan tyypille samalla nimellä kuin traitien metodeilla.

Kun kutsut metodeja, joilla on sama nimi, sinun täytyy kertoa Rustille, mitä haluat käyttää. Harkitse Listauksen 20-17 koodia, jossa olemme määritelleet kaksi traitia, `Pilot` ja `Wizard`, joilla molemmilla on metodi nimeltä `fly`. Toteutamme sitten molemmat traitit tyypille `Human`, jolla on jo suoraan toteutettu metodi nimeltä `fly`. Jokainen `fly`-metodi tekee jotain erilaista.

<Listing number="20-17" file-name="src/main.rs" caption="Kaksi traitia on määritelty sisältämään `fly`-metodin, ja ne on toteutettu tyypille `Human`, jolle on myös toteutettu `fly`-metodi suoraan">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-17/src/main.rs:here}}
```

</Listing>

Kun kutsumme `fly`-metodia `Human`-instanssilla, kääntäjä oletuksena kutsuu suoraan tyypille toteutettua metodia, kuten Listauksessa 20-18 on esitetty.

<Listing number="20-18" file-name="src/main.rs" caption="`fly`-metodin kutsuminen `Human`-instanssilla">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-18/src/main.rs:here}}
```

</Listing>

Tämän koodin suorittaminen tulostaa `*waving arms furiously*`, mikä osoittaa, että Rust kutsui suoraan tyypille `Human` toteutettua `fly`-metodia.

Kutsuaksemme `fly`-metodeja joko `Pilot`- tai `Wizard`-traitista, meidän täytyy käyttää eksplisiittisempää syntaksia määrittääksemme, mitä `fly`-metodia tarkoitamme. Listausta 20-19 demonstroi tätä syntaksia.

<Listing number="20-19" file-name="src/main.rs" caption="Sen määrittäminen, minkä traitin `fly`-metodia haluamme kutsua">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-19/src/main.rs:here}}
```

</Listing>

Traitin nimen määrittäminen ennen metodin nimeä selventää Rustille, mitä `fly`-toteutusta haluamme kutsua. Voisimme myös kirjoittaa `Human::fly(&person)`, mikä on vastaava kuin `person.fly()`, jota käytimme Listauksessa 20-19, mutta tämä on hieman pidempi kirjoittaa, jos emme tarvitse epäselvyyden poistamista.

Tämän koodin suorittaminen tulostaa seuraavan:

```console
{{#include ../listings/ch20-advanced-features/listing-20-19/output.txt}}
```

Koska `fly`-metodilla on `self`-parametri, jos meillä olisi kaksi _tyyppiä_, jotka molemmat toteuttavat yhden _traitin_, Rust voisi selvittää, mitä traitin toteutusta käyttää `self`-parametrin tyypin perusteella.

Assosioituilla funktioilla, jotka eivät ole metodeja, ei kuitenkaan ole `self`-parametria. Kun useat tyypit tai traitit määrittelevät ei-metodifunktioita samalla funktionimellä, Rust ei aina tiedä, mitä tyyppiä tarkoitat, ellet käytä _tarkasti määriteltyä syntaksia_. Esimerkiksi Listauksessa 20-20 luomme traitin eläinsuojalle, joka haluaa nimetä kaikki pentukoirat nimellä _Spot_. Teemme `Animal`-traitin assosioitulla ei-metodifunktiolla `baby_name`. `Animal`-trait on toteutettu rakenteelle `Dog`, jolle tarjoamme myös assosioitua ei-metodifunktiota `baby_name` suoraan.

<Listing number="20-20" file-name="src/main.rs" caption="Trait assosioitulla funktiolla ja tyyppi assosioitulla samannimisellä funktiolla, joka toteuttaa myös traitin">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-20/src/main.rs}}
```

</Listing>

Toteutamme koodin kaikkien pentujen nimeämiseksi Spot-nimellä `baby_name`-assosioitufunktiossa, joka on määritelty tyypille `Dog`. Tyyppi `Dog` toteuttaa myös `Animal`-traitin, joka kuvaa ominaisuuksia, joita kaikilla eläimillä on. Vauvakoirat kutsutaan pentuiksi, ja tämä ilmaistaan `Animal`-traitin toteutuksessa tyypille `Dog` `baby_name`-funktiossa, joka liittyy `Animal`-traitiin.

`main`-funktiossa kutsumme `Dog::baby_name`-funktiota, joka kutsuu suoraan tyypille `Dog` määriteltyä assosioitua funktiota. Tämä koodi tulostaa seuraavan:

```console
{{#include ../listings/ch20-advanced-features/listing-20-20/output.txt}}
```

Tämä tuloste ei ole se, mitä halusimme. Haluamme kutsua `baby_name`-funktiota, joka on osa `Animal`-traitia, jonka toteutimme tyypille `Dog`, jotta koodi tulostaisi `A baby dog is called a puppy`. Listauksessa 20-19 käyttämämme traitin nimen määrittämisen tekniikka ei auta tässä; jos muutamme `main`-funktion Listauksen 20-21 koodiksi, saamme käännösvirheen.

<Listing number="20-21" file-name="src/main.rs" caption="Yritys kutsua `baby_name`-funktiota `Animal`-traitista, mutta Rust ei tiedä, mitä toteutusta käyttää">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-21/src/main.rs:here}}
```

</Listing>

Koska `Animal::baby_name`-funktiolla ei ole `self`-parametria, ja muita tyyppejä voi toteuttaa `Animal`-traitin, Rust ei voi selvittää, mitä `Animal::baby_name`-toteutusta haluamme. Saamme tämän kääntäjävirheen:

```console
{{#include ../listings/ch20-advanced-features/listing-20-21/output.txt}}
```

Poistaaksemme epäselvyyden ja kertoaksemme Rustille, että haluamme käyttää `Animal`-traitin toteutusta tyypille `Dog` toisen tyypin `Animal`-toteutuksen sijaan, meidän täytyy käyttää tarkasti määriteltyä syntaksia. Listausta 20-22 demonstroi tarkasti määritellyn syntaksin käyttöä.

<Listing number="20-22" file-name="src/main.rs" caption="Tarkasti määritellyn syntaksin käyttö määrittääksemme, että haluamme kutsua `baby_name`-funktiota `Animal`-traitista tyypille `Dog` toteutettuna">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-22/src/main.rs:here}}
```

</Listing>

Annamme Rustille tyyppimerkinnän kulmasulkeiden sisällä, mikä osoittaa, että haluamme kutsua `baby_name`-metodia `Animal`-traitista tyypille `Dog` toteutettuna sanomalla, että haluamme käsitellä tyyppiä `Dog` tyypinä `Animal` tässä funktiokutsussa. Tämä koodi tulostaa nyt haluamamme:

```console
{{#include ../listings/ch20-advanced-features/listing-20-22/output.txt}}
```

Yleisesti ottaen tarkasti määritelty syntaksi määritellään seuraavasti:

```rust,ignore
<Tyyppi trait Trait>::funktio(vastaanotin_jos_metodi, seuraava_arg, ...);
```

Assosioituille funktioille, jotka eivät ole metodeja, ei olisi vastaanottajaa: olisi vain muiden argumenttien lista. Voisit käyttää tarkasti määriteltyä syntaksia kaikkialla, missä kutsut funktioita tai metodeja. Sinun on kuitenkin sallittua jättää pois mikä tahansa osa tästä syntaksista, jonka Rust voi selvittää muista tiedoista ohjelmassa. Sinun täytyy käyttää tätä puheliasempaa syntaksia vain tapauksissa, joissa on useita samannimisiä toteutuksia ja Rust tarvitsee apua tunnistaakseen, mitä toteutusta haluat kutsua.

### Ylitraitien käyttö vaatimaan yhden traitin toiminnallisuutta toisessa traitissa

Joskus saatat kirjoittaa trait-määrittelyn, joka riippuu toisesta traitista: jotta tyyppi toteuttaisi ensimmäisen traitin, haluat vaatia, että tyyppi toteuttaa myös toisen traitin. Tekisit näin, jotta trait-määrittelysi voisi käyttää toisen traitin assosioituja kohteita. Trait, johon trait-määrittelysi luottaa, kutsutaan traitisi _ylitraiksi_.

Esimerkiksi sanotaan, että haluamme tehdä `OutlinePrint`-traitin, jolla on `outline_print`-metodi, joka tulostaa annetun arvon muotoiltuna niin, että se on kehystetty tähtimerkeillä. Toisin sanoen, annettuna `Point`-rakenteelle, joka toteuttaa standardikirjaston `Display`-traitin tuottaakseen `(x, y)`, kun kutsumme `outline_print`-metodia `Point`-instanssilla, jolla on `1` arvolle `x` ja `3` arvolle `y`, sen pitäisi tulostaa seuraava:

```text
**********
*        *
* (1, 3) *
*        *
**********
```

`outline_print`-metodin toteutuksessa haluamme käyttää `Display`-traitin toiminnallisuutta. Siksi meidän täytyy määrittää, että `OutlinePrint`-trait toimii vain tyypeille, jotka myös toteuttavat `Display`-traitin ja tarjoavat `OutlinePrint`-traitin tarvitseman toiminnallisuuden. Voimme tehdä tämän trait-määrittelyssä määrittämällä `OutlinePrint: Display`. Tämä tekniikka on samanlainen kuin trait-rajoitteen lisääminen traitiin. Listausta 20-23 demonstroi `OutlinePrint`-traitin toteutusta.

<Listing number="20-23" file-name="src/main.rs" caption="`OutlinePrint`-traitin toteuttaminen, joka vaatii toiminnallisuutta `Display`-traitista">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-23/src/main.rs:here}}
```

</Listing>

Koska olemme määrittäneet, että `OutlinePrint` vaatii `Display`-traitin, voimme käyttää `to_string`-funktiota, joka toteutetaan automaattisesti kaikille tyypeille, jotka toteuttavat `Display`-traitin. Jos yrittäisimme käyttää `to_string`-funktiota lisäämättä kaksoispistettä ja määrittämättä `Display`-traitia traitin nimen jälkeen, saisimme virheen, joka sanoo, ettei tyypille `&Self` löydy metodia nimeltä `to_string` nykyisestä näkyvyysalueesta.

Katsotaan, mitä tapahtuu, kun yritämme toteuttaa `OutlinePrint`-traitin tyypille, joka ei toteuta `Display`-traitia, kuten `Point`-rakenteelle:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-02-impl-outlineprint-for-point/src/main.rs:here}}
```

</Listing>

Saamme virheen, joka sanoo, että `Display` vaaditaan mutta sitä ei ole toteutettu:

```console
{{#include ../listings/ch20-advanced-features/no-listing-02-impl-outlineprint-for-point/output.txt}}
```

Korjataksemme tämän, toteutamme `Display`-traitin tyypille `Point` ja täytämme `OutlinePrint`-traitin vaatiman rajoitteen, näin:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-03-impl-display-for-point/src/main.rs:here}}
```

</Listing>

Tämän jälkeen `OutlinePrint`-traitin toteuttaminen tyypille `Point` kääntyy onnistuneesti, ja voimme kutsua `outline_print`-metodia `Point`-instanssilla näyttääksemme sen tähtimerkkikehyksessä.

### Newtype-mallin käyttö ulkoisten traitien toteuttamiseen ulkoisille tyypeille

[”Traitin toteuttaminen tyypille”][implementing-a-trait-on-a-type]<!-- ignore --> -osiossa Luvussa 10 mainitsimme orpopelisäännön, joka sanoo, että saamme toteuttaa traitin tyypille vain, jos joko trait tai tyyppi on paikallinen crateemme. On mahdollista kiertää tämä rajoitus käyttämällä _newtype-mallia_, joka sisältää uuden tyypin tuple-rakenteessa. (Käsittelimme tuple-rakenteita [”Tuple-rakenteiden käyttö nimeämättömillä kentillä eri tyyppien luomiseksi”][tuple-structs]<!-- ignore --> -osiossa Luvussa 5.) Tuple-rakenteella on yksi kenttä, ja se on ohut kääre tyypin ympärillä, jolle haluamme toteuttaa traitin. Sitten kääretyyppi on paikallinen crateemme, ja voimme toteuttaa traitin kääreelle. _Newtype_ on termi, joka on peräisin Haskell-ohjelmointikielestä. Tämän mallin käytöstä ei ole suorituskykyrangaistusta ajonaikana, ja kääretyyppi poistetaan käännösaikana.

Esimerkkinä sanotaan, että haluamme toteuttaa `Display`-traitin tyypille `Vec<T>`, mitä orpopelisääntö estää meitä tekemästä suoraan, koska `Display`-trait ja `Vec<T>`-tyyppi on määritelty crateemme ulkopuolella. Voimme tehdä `Wrapper`-rakenteen, joka pitää `Vec<T>`-instanssin; sitten voimme toteuttaa `Display`-traitin tyypille `Wrapper` ja käyttää `Vec<T>`-arvoa, kuten Listauksessa 20-24 on esitetty.

<Listing number="20-24" file-name="src/main.rs" caption="`Wrapper`-tyypin luominen `Vec<String>`-tyypin ympärille `Display`-traitin toteuttamiseksi">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-24/src/main.rs}}
```

</Listing>

`Display`-toteutus käyttää `self.0` päästäkseen sisäiseen `Vec<T>`-arvoon, koska `Wrapper` on tuple-rakenne ja `Vec<T>` on tuple-indeksin 0 kohdassa oleva kohde. Sitten voimme käyttää `Display`-traitin toiminnallisuutta tyypillä `Wrapper`.

Tämän tekniikan haittapuoli on, että `Wrapper` on uusi tyyppi, joten sillä ei ole sen pitämän arvon metodeja. Meidän täytyisi toteuttaa kaikki `Vec<T>`-tyypin metodit suoraan tyypille `Wrapper` siten, että metodit delegoivat `self.0`:lle, mikä antaisi meille mahdollisuuden käsitellä tyyppiä `Wrapper` täsmälleen kuten `Vec<T>`:tä. Jos haluaisimme, että uudella tyypillä on jokainen sisäisen tyypin metodi, `Deref`-traitin toteuttaminen (käsitelty [”Älykkäiden osoittimien käsittely tavallisten viittausten tavoin `Deref`-traitin avulla”][smart-pointer-deref]<!-- ignore --> -osiossa Luvussa 15) tyypille `Wrapper` palauttaakseen sisäisen tyypin olisi ratkaisu. Jos emme halua, että `Wrapper`-tyypillä on kaikki sisäisen tyypin metodit — esimerkiksi rajoittaaksemme `Wrapper`-tyypin käyttäytymistä — meidän täytyisi toteuttaa vain haluamamme metodit manuaalisesti.

Tämä newtype-malli on hyödyllinen myös silloin, kun traitit eivät ole mukana. Vaihdetaan fokusta ja katsotaan joitakin kehittyneitä tapoja olla vuorovaikutuksessa Rustin tyyppijärjestelmän kanssa.

[newtype]: ch20-02-advanced-traits.html#using-the-newtype-pattern-to-implement-external-traits-on-external-types
[implementing-a-trait-on-a-type]: ch10-02-traits.html#implementing-a-trait-on-a-type
[traits-defining-shared-behavior]: ch10-02-traits.html#traits-defining-shared-behavior
[smart-pointer-deref]: ch15-02-deref.html#treating-smart-pointers-like-regular-references-with-the-deref-trait
[tuple-structs]: ch05-01-defining-structs.html#using-tuple-structs-without-named-fields-to-create-different-types
