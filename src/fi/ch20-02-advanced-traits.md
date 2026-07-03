## Edistyneet traitit

Käsittelimme traitit ensimmäisen kerran luvun 10 [”Jaetun käyttäytymisen määrittely traitien avulla”][traits]<!-- ignore --> -kohdassa, mutta emme käsitelleet edistyneempiä yksityiskohtia. Nyt kun tiedät Rustista enemmän, voimme syventyä yksityiskohtiin.

<!-- Old headings. Do not remove or links may break. -->

<a id="specifying-placeholder-types-in-trait-definitions-with-associated-types"></a>
<a id="associated-types"></a>

### Traitien määrittely assosioituneilla tyypeillä

_Assosioituneet tyypit_ yhdistävät tyyppipaikkamerkin traitiin siten, että traitin metodimääritelmissä voidaan käyttää näitä paikkamerkkityyppejä signatuureissa. Traitin toteuttaja määrittää konkreettisen tyypin paikkamerkkityypin sijaan tietylle toteutukselle. Näin voimme määritellä traitin, joka käyttää tyyppejä, tietämättä tarkalleen mitä tyyppejä ne ovat ennen traitin toteutusta.

Olemme kuvanneet useimmat tämän luvun edistyneet ominaisuudet harvoin tarvittaviksi. Assosioituneet tyypit ovat välimaastossa: niitä käytetään harvemmin kuin kirjan muissa osissa selitettyjä ominaisuuksia, mutta yleisemmin kuin monia tämän luvun muita ominaisuuksia.

Esimerkki traitista assosioituneella tyypillä on standardikirjaston tarjoama `Iterator`-trait. Assosioitu tyyppi on nimeltään `Item` ja edustaa niiden arvojen tyyppiä, joita `Iterator`-traitin toteuttava tyyppi iteroi. `Iterator`-traitin määritelmä on listauksessa 20-13.

<Listing number="20-13" caption="`Iterator`-traitin määritelmä, jossa on assosioitu tyyppi `Item`">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-13/src/lib.rs}}
```

</Listing>

Tyyppi `Item` on paikkamerkki, ja `next`-metodin määritelmä näyttää, että se palauttaa arvoja tyypillä `Option<Self::Item>`. `Iterator`-traitin toteuttajat määrittävät konkreettisen tyypin `Item`-tyypille, ja `next`-metodi palauttaa `Option`-arvon, joka sisältää kyseisen konkreettisen tyypin arvon.

Assosioituneet tyypit saattavat vaikuttaa samankaltaiselta käsitteeltä kuin geneerisyys, koska geneerisyyden avulla voidaan määritellä funktio ilman tietoa siitä, mitä tyyppejä se käsittelee. Tarkastellaksemme näiden kahden käsitteen eroa, katsomme `Iterator`-traitin toteutusta tyypille nimeltä `Counter`, jossa `Item`-tyypiksi määritetään `u32`:

<Listing file-name="src/lib.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-22-iterator-on-counter/src/lib.rs:ch19}}
```

</Listing>

Tämä syntaksi näyttää verrattavissa geneerisyyden syntaksiin. Miksi emme siis määrittelisi `Iterator`-traitia geneerisesti, kuten listauksessa 20-14?

<Listing number="20-14" caption="Hypoteettinen `Iterator`-traitin määritelmä geneerisyyttä käyttäen">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-14/src/lib.rs}}
```

</Listing>

Ero on siinä, että geneerisyyttä käytettäessä, kuten listauksessa 20-14, meidän täytyy merkitä tyypit jokaisessa toteutuksessa; koska voimme toteuttaa myös `Iterator<String> for Counter` tai minkä tahansa muun tyypin, `Counter`-tyypille voi olla useita `Iterator`-toteutuksia. Toisin sanoen, kun traitilla on geneerinen parametri, sen voi toteuttaa tyypille useita kertoja vaihtamalla geneerisen tyyppiparametrin konkreettista tyyppiä joka kerta. Kun käytämme `next`-metodia `Counter`-tyypillä, meidän täytyisi antaa tyyppimerkinnät kertomaan, mitä `Iterator`-toteutusta haluamme käyttää.

Assosioituneilla tyypeillä emme tarvitse tyyppimerkintöjä, koska emme voi toteuttaa traitia tyypille useita kertoja. Listauksessa 20-13 assosioituneita tyyppejä käyttävällä määritelmällä voimme valita `Item`-tyypin vain kerran, koska voi olla vain yksi `impl Iterator for Counter`. Emme joudu määrittämään, että haluamme `u32`-arvojen iteraattorin, joka kerta kun kutsumme `next`-metodia `Counter`-tyypillä.

Assosioituneet tyypit ovat myös osa traitin sopimusta: traitin toteuttajien täytyy tarjota tyyppi assosioituneen tyypin paikkamerkin tilalle. Assosioituilla tyypeillä on usein nimi, joka kuvaa tyypin käyttöä, ja assosioituneen tyypin dokumentointi API-dokumentaatiossa on hyvä käytäntö.

<!-- Old headings. Do not remove or links may break. -->

<a id="default-generic-type-parameters-and-operator-overloading"></a>

### Oletusarvoiset geneeriset parametrit ja operaattorin ylikuormitus

Kun käytämme geneerisiä tyyppiparametreja, voimme määrittää geneeriselle tyypille oletusarvoisen konkreettisen tyypin. Tämä poistaa tarpeen, että traitin toteuttajien täytyy määrittää konkreettinen tyyppi, jos oletustyyppi toimii. Oletustyypin määrittelet geneeristä tyyppiä julistaessasi syntaksilla `<PlaceholderType=ConcreteType>`.

Hyvä esimerkki tilanteesta, jossa tämä tekniikka on hyödyllinen, on _operaattorin ylikuormitus_, jossa mukautat operaattorin (kuten `+`) käyttäytymistä tietyissä tilanteissa.

Rust ei salli omien operaattorien luomista tai mielivaltaisten operaattorien ylikuormitusta. Voit kuitenkin ylikuormittaa `std::ops`-moduulissa listattuja operaatioita ja niihin liittyviä traitteja toteuttamalla operaattoriin liittyvät traitit. Esimerkiksi listauksessa 20-15 ylikuormitamme `+`-operaattorin kahden `Point`-instanssin yhteenlaskuun toteuttamalla `Add`-traitin `Point`-rakenteelle.

<Listing number="20-15" file-name="src/main.rs" caption="`Add`-traitin toteutus `+`-operaattorin ylikuormittamiseksi `Point`-instansseille">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-15/src/main.rs}}
```

</Listing>

`add`-metodi laskee kahden `Point`-instanssin `x`-arvot ja kahden `Point`-instanssin `y`-arvot yhteen luodakseen uuden `Point`-instanssin. `Add`-traitilla on assosioitu tyyppi nimeltä `Output`, joka määrittää `add`-metodin palauttaman tyypin.

Tässä koodissa oletusarvoinen geneerinen tyyppi on `Add`-traitin sisällä. Tässä on sen määritelmä:

```rust
trait Add<Rhs=Self> {
    type Output;

    fn add(self, rhs: Rhs) -> Self::Output;
}
```

Tämän koodin pitäisi näyttää yleisesti tutulta: trait yhdellä metodilla ja assosioidulla tyypillä. Uutta on `Rhs=Self`: tätä syntaksia kutsutaan _oletusarvoisiksi tyyppiparametreiksi_. Geneerinen tyyppiparametri `Rhs` (lyhenne ”right-hand side”, oikea puoli) määrittää `add`-metodin `rhs`-parametrin tyypin. Jos emme määritä konkreettista tyyppiä `Rhs`-parametrille toteuttaessamme `Add`-traitia, `Rhs`-tyypiksi tulee oletuksena `Self`, eli tyyppi, jolle toteutamme `Add`-traitin.

Kun toteutimme `Add`-traitin `Point`-tyypille, käytimme oletusta `Rhs`-parametrille, koska halusimme laskea yhteen kaksi `Point`-instanssia. Katsotaan esimerkkiä, jossa haluamme mukauttaa `Rhs`-tyypin oletuksen sijaan.

Meillä on kaksi rakennetta, `Millimeters` ja `Meters`, jotka tallentavat arvoja eri yksiköissä. Tämä olemassa olevan tyypin ohut kääriminen toiseen rakenteeseen tunnetaan _newtype-kuviona_, jota käsittelemme tarkemmin [”Ulkoisten traitien toteuttaminen newtype-kuviolla”][newtype]<!-- ignore --> -kohdassa. Haluamme laskea yhteen millimetreissä olevia arvoja metreissä olevien arvojen kanssa ja `Add`-toteutuksen tekemän muunnoksen oikein. Voimme toteuttaa `Add`-traitin `Millimeters`-tyypille asettaen `Rhs`-tyypiksi `Meters`, kuten listauksessa 20-16.

<Listing number="20-16" file-name="src/lib.rs" caption="`Add`-traitin toteutus `Millimeters`-tyypille `Millimeters`- ja `Meters`-arvojen yhteenlaskuun">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-16/src/lib.rs}}
```

</Listing>

Lisätäksemme `Millimeters`- ja `Meters`-arvoja määrittelemme `impl Add<Meters>` asettaaksemme `Rhs`-tyyppiparametrin arvon oletuksen `Self` sijaan.

Käytät oletusarvoisia tyyppiparametreja pääasiassa kahdella tavalla:

1. Laajentaaksesi tyyppiä rikkomatta olemassa olevaa koodia
2. Salliaksesi mukautuksen tapauksissa, joita useimmat käyttäjät eivät tarvitse

Standardikirjaston `Add`-trait on esimerkki toisesta tarkoituksesta: yleensä lasket yhteen samanlaisia tyyppejä, mutta `Add`-trait tarjoaa mahdollisuuden mukauttaa tätä. Oletusarvoisen tyyppiparametrin käyttö `Add`-traitin määritelmässä tarkoittaa, että ylimääräistä parametria ei tarvitse määrittää useimmiten. Toisin sanoen, toteutusboilerplatea ei tarvita, mikä helpottaa traitin käyttöä.

Ensimmäinen tarkoitus on samanlainen kuin toinen, mutta päinvastoin: jos haluat lisätä tyyppiparametrin olemassa olevaan traitiin, voit antaa sille oletusarvon laajentaaksesi traitin toiminnallisuutta rikkomatta olemassa olevaa toteutuskoodia.

<!-- Old headings. Do not remove or links may break. -->

<a id="fully-qualified-syntax-for-disambiguation-calling-methods-with-the-same-name"></a>
<a id="disambiguating-between-methods-with-the-same-name"></a>

### Samannimisten metodien erottelu

Mikään Rustissa ei estä traitia sisältämästä metodia, jolla on sama nimi kuin toisen traitin metodilla, eikä Rust estä molempien traitien toteuttamista samalle tyypille. On myös mahdollista toteuttaa metodi suoraan tyypille samalla nimellä kuin trait-metodeilla.

Kun kutsut samannimisiä metodeja, sinun täytyy kertoa Rustille, kumpaa haluat käyttää. Harkitse listauksen 20-17 koodia, jossa olemme määritelleet kaksi traitia, `Pilot` ja `Wizard`, joilla molemmilla on metodi nimeltä `fly`. Toteutamme molemmat traitit tyypille `Human`, jolla on jo suoraan toteutettu metodi nimeltä `fly`. Jokainen `fly`-metodi tekee jotain eri.

<Listing number="20-17" file-name="src/main.rs" caption="Kaksi traitia, joilla on `fly`-metodi, toteutetaan `Human`-tyypille, ja `fly`-metodi toteutetaan suoraan `Human`-tyypille.">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-17/src/main.rs:here}}
```

</Listing>

Kun kutsumme `fly`-metodia `Human`-instanssilla, kääntäjä oletuksena kutsuu tyypille suoraan toteutettua metodia, kuten listauksessa 20-18.

<Listing number="20-18" file-name="src/main.rs" caption="`fly`-metodin kutsuminen `Human`-instanssilla">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-18/src/main.rs:here}}
```

</Listing>

Tämän koodin ajaminen tulostaa `*waving arms furiously*`, mikä osoittaa, että Rust kutsui `Human`-tyypille suoraan toteutettua `fly`-metodia.

Kutsuaksemme `fly`-metodeja joko `Pilot`- tai `Wizard`-traitista, tarvitsemme eksplisittisemmän syntaksin määrittääksemme, mitä `fly`-metodia tarkoitamme. Listaus 20-19 demonstroi tätä syntaksia.

<Listing number="20-19" file-name="src/main.rs" caption="Sen määrittäminen, kumman traitin `fly`-metodia haluamme kutsua">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-19/src/main.rs:here}}
```

</Listing>

Trait-nimen kirjoittaminen ennen metodin nimeä selventää Rustille, mitä `fly`-toteutusta haluamme kutsua. Voisimme myös kirjoittaa `Human::fly(&person)`, mikä on vastaava kuin listauksessa 20-19 käyttämämme `person.fly()`, mutta tämä on hieman pidempi kirjoittaa, jos erottelua ei tarvita.

Tämän koodin ajaminen tulostaa seuraavan:

```console
{{#include ../listings/ch20-advanced-features/listing-20-19/output.txt}}
```

Koska `fly`-metodilla on `self`-parametri, jos meillä olisi kaksi _tyyppiä_, jotka molemmat toteuttavat yhden _traitin_, Rust voisi päätellä, mitä trait-toteutusta käyttää `self`-parametrin tyypin perusteella.

Assosioiduilla funktioilla, jotka eivät ole metodeja, ei kuitenkaan ole `self`-parametria. Kun useilla tyypeillä tai traitilla on samannimisiä ei-metodifunktioita, Rust ei aina tiedä, mitä tyyppiä tarkoitat, ellet käytä täysin pätevää syntaksia. Esimerkiksi listauksessa 20-20 luomme traitin eläintarhaa varten, joka haluaa nimetä kaikki pentukoirat Spotiksi. Teemme `Animal`-traitin assosioidulla ei-metodifunktiolla `baby_name`. `Animal`-trait toteutetaan rakenteelle `Dog`, jolle tarjoamme myös suoraan assosioituneen ei-metodifunktion `baby_name`.

<Listing number="20-20" file-name="src/main.rs" caption="Trait assosioituneella funktiolla ja tyyppi samannimisellä assosioituneella funktiolla, joka toteuttaa myös traitin">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-20/src/main.rs}}
```

</Listing>

Toteutamme koodin, joka nimeää kaikki pennut Spotiksi, `Dog`-tyypille määritellyssä `baby_name`-assosioituneessa funktiossa. `Dog`-tyyppi toteuttaa myös `Animal`-traitin, joka kuvaa kaikkien eläinten ominaisuuksia. Koiranpennuja kutsutaan puppies-nimellä, ja tämä ilmaistaan `Animal`-traitin `Dog`-toteutuksessa `Animal`-traitiin liittyvässä `baby_name`-funktiossa.

`main`-funktiossa kutsumme `Dog::baby_name`-funktiota, joka kutsuu suoraan `Dog`-tyypille määriteltyä assosioitunutta funktiota. Tämä koodi tulostaa seuraavan:

```console
{{#include ../listings/ch20-advanced-features/listing-20-20/output.txt}}
```

Tämä tuloste ei ole haluamamme. Haluamme kutsua `baby_name`-funktiota, joka on osa `Animal`-traitia, jonka toteutimme `Dog`-tyypille, jotta koodi tulostaisi `A baby dog is called a puppy`. Listauksessa 20-19 käyttämämme trait-nimen määrittämisen tekniikka ei auta tässä; jos muutamme `main`-funktion listauksen 20-21 koodiksi, saamme käännösvirheen.

<Listing number="20-21" file-name="src/main.rs" caption="Yritys kutsua `baby_name`-funktiota `Animal`-traitista, mutta Rust ei tiedä mitä toteutusta käyttää">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-21/src/main.rs:here}}
```

</Listing>

Koska `Animal::baby_name`-funktiolla ei ole `self`-parametria ja muitakin tyyppejä voi toteuttaa `Animal`-traitin, Rust ei voi päätellä, mitä `Animal::baby_name`-toteutusta haluamme. Saamme tämän kääntäjävirheen:

```console
{{#include ../listings/ch20-advanced-features/listing-20-21/output.txt}}
```

Erottellaksemme ja kertoaksemme Rustille, että haluamme käyttää `Animal`-traitin `Dog`-toteutusta toisen tyypin `Animal`-toteutuksen sijaan, meidän täytyy käyttää täysin pätevää syntaksia. Listaus 20-22 näyttää, miten täysin pätevää syntaksia käytetään.

<Listing number="20-22" file-name="src/main.rs" caption="Täysin pätevän syntaksin käyttö määrittämään, että haluamme kutsua `Animal`-traitin `baby_name`-funktiota `Dog`-toteutuksena">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-22/src/main.rs:here}}
```

</Listing>

Annamme Rustille tyyppimerkinnän kulmasulkeissa, joka osoittaa, että haluamme kutsua `Animal`-traitin `baby_name`-metodia `Dog`-toteutuksena käsittelemällä `Dog`-tyyppiä `Animal`-tyyppinä tässä funktiokutsussa. Tämä koodi tulostaa nyt haluamamme:

```console
{{#include ../listings/ch20-advanced-features/listing-20-22/output.txt}}
```

Yleisesti täysin pätevä syntaksi määritellään seuraavasti:

```rust,ignore
<Type as Trait>::function(receiver_if_method, next_arg, ...);
```

Assosioiduille funktioille, jotka eivät ole metodeja, ei olisi vastaanottajaa: olisi vain muiden argumenttien lista. Voit käyttää täysin pätevää syntaksia kaikkialla, missä kutsut funktioita tai metodeja. Voit kuitenkin jättää pois kaiken osan tästä syntaksista, jonka Rust voi päätellä muusta ohjelman tiedosta. Tarvitset tämän monimutkaisemman syntaksin vain tapauksissa, joissa on useita samannimisiä toteutuksia ja Rust tarvitsee apua tunnistamaan, mitä toteutusta haluat kutsua.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-supertraits-to-require-one-traits-functionality-within-another-trait"></a>

### Supertraitien käyttö

Joskus saatat kirjoittaa trait-määritelmän, joka riippuu toisesta traitista: jotta tyyppi toteuttaisi ensimmäisen traitin, haluat vaatia sen toteuttavan myös toisen traitin. Teet näin, jotta trait-määritelmäsi voi käyttää toisen traitin assosioituja kohteita. Trait, johon trait-määritelmäsi nojaa, on traitisi _supertrait_.

Esimerkiksi haluamme tehdä `OutlinePrint`-traitin, jolla on `outline_print`-metodi, joka tulostaa annetun arvon muotoiltuna niin, että se on kehystetty tähtimerkeillä. Eli kun `Point`-rakenteella, joka toteuttaa standardikirjaston `Display`-traitin tulostaakseen `(x, y)`, kutsumme `outline_print`-metodia `Point`-instanssilla, jossa `x` on `1` ja `y` on `3`, sen pitäisi tulostaa seuraava:

```text
**********
*        *
* (1, 3) *
*        *
**********
```

`outline_print`-metodin toteutuksessa haluamme käyttää `Display`-traitin toiminnallisuutta. Siksi meidän täytyy määrittää, että `OutlinePrint`-trait toimii vain tyypeille, jotka myös toteuttavat `Display`-traitin ja tarjoavat `OutlinePrint`-traitin tarvitseman toiminnallisuuden. Voimme tehdä sen trait-määritelmässä määrittämällä `OutlinePrint: Display`. Tämä tekniikka muistuttaa trait-sidontojen lisäämistä traitiin. Listaus 20-23 näyttää `OutlinePrint`-traitin toteutuksen.

<Listing number="20-23" file-name="src/main.rs" caption="`OutlinePrint`-traitin toteutus, joka vaatii toiminnallisuutta `Display`-traitista">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-23/src/main.rs:here}}
```

</Listing>

Koska olemme määrittäneet, että `OutlinePrint` vaatii `Display`-traitin, voimme käyttää `to_string`-funktiota, joka toteutetaan automaattisesti kaikille `Display`-traitin toteuttaville tyypeille. Jos yrittäisimme käyttää `to_string`-funktiota lisäämättä kaksoispistettä ja `Display`-traitia trait-nimen jälkeen, saisimme virheen, jossa sanotaan, ettei tyypille `&Self` löydy metodia nimeltä `to_string` nykyisestä näkyvyysalueesta.

Katsotaan, mitä tapahtuu, kun yritämme toteuttaa `OutlinePrint`-traitin tyypille, joka ei toteuta `Display`-traitia, kuten `Point`-rakenteelle:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-02-impl-outlineprint-for-point/src/main.rs:here}}
```

</Listing>

Saamme virheen, jossa sanotaan, että `Display` vaaditaan mutta sitä ei ole toteutettu:

```console
{{#include ../listings/ch20-advanced-features/no-listing-02-impl-outlineprint-for-point/output.txt}}
```

Korjataksemme tämän toteutamme `Display`-traitin `Point`-tyypille ja täytämme `OutlinePrint`-traitin vaatiman rajoitteen näin:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-03-impl-display-for-point/src/main.rs:here}}
```

</Listing>

Sitten `OutlinePrint`-traitin toteuttaminen `Point`-tyypille kääntyy onnistuneesti, ja voimme kutsua `outline_print`-metodia `Point`-instanssilla näyttääksemme sen tähtimerkkikehyksessä.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-the-newtype-pattern-to-implement-external-traits-on-external-types"></a>
<a id="using-the-newtype-pattern-to-implement-external-traits"></a>

### Ulkoisten traitien toteuttaminen newtype-kuviolla

Luvun 10 [”Traitin toteuttaminen tyypille”][implementing-a-trait-on-a-type]<!-- ignore --> -kohdassa mainitsimme orporoolin, jonka mukaan saamme toteuttaa traitin tyypille vain, jos trait tai tyyppi, tai molemmat, ovat paikallisia kratellemme. Tämän rajoituksen voi kiertää newtype-kuviolla, jossa luodaan uusi tyyppi monikkorakenteessa. (Käsittelimme monikkorakenteita luvun 5 [”Eri tyyppien luominen monikkorakenteilla”][tuple-structs]<!-- ignore --> -kohdassa.) Monikkorakenteella on yksi kenttä, ja se on ohut kääre tyypin ympärillä, jolle haluamme toteuttaa traitin. Kääretyyppi on sitten paikallinen kratellemme, ja voimme toteuttaa traitin kääretyypille. _Newtype_ on termi, joka on peräisin Haskell-ohjelmointikielestä. Tämän kuvion käytöstä ei ole ajonaikaisen suorituskyvyn rangaistusta, ja kääretyyppi häviää käännösaikana.

Esimerkkinä haluamme toteuttaa `Display`-traitin tyypille `Vec<T>`, mitä orporooli estää tekemästä suoraan, koska `Display`-trait ja `Vec<T>`-tyyppi on määritelty kratellemme ulkopuolella. Voimme tehdä `Wrapper`-rakenteen, joka pitää `Vec<T>`-instanssin; sitten voimme toteuttaa `Display`-traitin `Wrapper`-tyypille ja käyttää `Vec<T>`-arvoa, kuten listauksessa 20-24.

<Listing number="20-24" file-name="src/main.rs" caption="`Wrapper`-tyypin luominen `Vec<String>`-tyypin ympärille `Display`-traitin toteuttamiseksi">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-24/src/main.rs}}
```

</Listing>

`Display`-toteutus käyttää `self.0` päästäkseen sisäiseen `Vec<T>`-arvoon, koska `Wrapper` on monikkorakenne ja `Vec<T>` on monikon indeksin 0 kohde. Sitten voimme käyttää `Display`-traitin toiminnallisuutta `Wrapper`-tyypillä.

Tämän tekniikan haittapuoli on, että `Wrapper` on uusi tyyppi, joten sillä ei ole sen pitämän arvon metodeja. Meidän täytyisi toteuttaa kaikki `Vec<T>`-metodit suoraan `Wrapper`-tyypille niin, että metodit delegoivat `self.0`:lle, jotta voisimme käsitellä `Wrapper`-tyyppiä täsmälleen kuten `Vec<T>`-tyyppiä. Jos haluaisimme uudella tyypillä kaikki sisäisen tyypin metodit, ratkaisu olisi toteuttaa `Deref`-trait `Wrapper`-tyypille palauttaakseen sisäisen tyypin (käsittelimme `Deref`-traitin toteutusta luvun 15 [”Älyosoittimien käyttely tavallisten viitteiden tavoin”][smart-pointer-deref]<!-- ignore --> -kohdassa). Jos emme haluaisi `Wrapper`-tyypillä kaikkia sisäisen tyypin metodeja — esimerkiksi rajoittaaksemme `Wrapper`-tyypin käyttäytymistä — meidän täytyisi toteuttaa manuaalisesti vain haluamamme metodit.

Tämä newtype-kuvio on hyödyllinen myös silloin, kun traitteja ei ole mukana. Siirrytään seuraavaksi tarkastelemaan edistyneitä tapoja vuorovaikuttaa Rustin tyyppijärjestelmän kanssa.

[newtype]: ch20-02-advanced-traits.html#implementing-external-traits-with-the-newtype-pattern
[implementing-a-trait-on-a-type]: ch10-02-traits.html#implementing-a-trait-on-a-type
[traits]: ch10-02-traits.html
[smart-pointer-deref]: ch15-02-deref.html#treating-smart-pointers-like-regular-references
[tuple-structs]: ch05-01-defining-structs.html#creating-different-types-with-tuple-structs
