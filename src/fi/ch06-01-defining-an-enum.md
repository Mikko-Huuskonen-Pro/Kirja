## Enumin määrittely

Siinä missä rakenteet antavat tavan ryhmitellä toisiinsa liittyviä kenttiä ja dataa, kuten `Rectangle`-rakenteen `width`- ja `height`-kentät, enumit antavat tavan sanoa, että arvo on yksi mahdollisista arvoista. Esimerkiksi saatamme haluta sanoa, että `Rectangle` on yksi mahdollisista muodoista, joihin kuuluvat myös `Circle` ja `Triangle`. Tätä varten Rust antaa meidän koodata nämä mahdollisuudet enumina.

Katsotaan tilannetta, jonka haluamme ilmaista koodissa, ja nähdään, miksi enumit ovat hyödyllisiä ja sopivampia kuin rakenteet tässä tapauksessa. Oletetaan, että meidän täytyy työskennellä IP-osoitteiden kanssa. Tällä hetkellä IP-osoitteille käytetään kahta pääasiallista standardia: versio neljä ja versio kuusi. Koska nämä ovat ainoat mahdolliset IP-osoitteet, joita ohjelmamme kohtaa, voimme _luetella_ kaikki mahdolliset variantit, mistä sana enumeration eli luettelotyyppi saa nimensä.

Mikä tahansa IP-osoite voi olla joko version neljä tai version kuusi osoite, mutta ei molempia samaan aikaan. Tämä IP-osoitteiden ominaisuus tekee enum-tietorakenteesta sopivan, koska enum-arvo voi olla vain yksi sen varianteista. Sekä version neljä että version kuusi osoitteet ovat silti pohjimmiltaan IP-osoitteita, joten niitä pitäisi käsitellä samana tyypinä, kun koodi käsittelee tilanteita, jotka koskevat mitä tahansa IP-osoitetyyppiä.

Voimme ilmaista tämän käsitteen koodissa määrittelemällä `IpAddrKind`-luettelon ja listaamalla mahdolliset IP-osoitteen tyypit, `V4` ja `V6`. Nämä ovat enumin variantit:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:def}}
```

`IpAddrKind` on nyt mukautettu tietotyyppi, jota voimme käyttää muualla koodissamme.

### Enum-arvot

Voimme luoda kummankin `IpAddrKind`-variantin instanssit näin:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:instance}}
```

Huomaa, että enumin variantit ovat nimetty tunnisteen sisällä, ja käytämme kaksoispistettä erottamaan ne toisistaan. Tämä on hyödyllistä, koska nyt molemmat arvot `IpAddrKind::V4` ja `IpAddrKind::V6` ovat samaa tyyppiä: `IpAddrKind`. Voimme sitten esimerkiksi määritellä funktion, joka ottaa minkä tahansa `IpAddrKind`-arvon:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:fn}}
```

Ja voimme kutsua tätä funktiota kummallakin variantilla:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:fn_call}}
```

Enumien käytössä on vielä enemmän etuja. Kun ajattelemme IP-osoitetyyppiämme tarkemmin, tällä hetkellä meillä ei ole tapaa tallentaa varsinaista IP-osoitteen _dataa_; tiedämme vain sen _tyypin_. Koska opit juuri rakenteista Luvussa 5, saatat olla taipuvainen ratkaisemaan tämän ongelman rakenteilla, kuten Listauksessa 6-1 on esitetty.

<Listing number="6-1" caption="IP-osoitteen datan ja `IpAddrKind`-variantin tallentaminen `struct`-rakenteella">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-01/src/main.rs:here}}
```

</Listing>

Tässä olemme määritelleet `IpAddr`-rakenteen, jolla on kaksi kenttää: `kind`-kenttä, jonka tyyppi on `IpAddrKind` (aiemmin määrittelemämme enum), ja `address`-kenttä, jonka tyyppi on `String`. Meillä on kaksi tämän rakenteen instanssia. Ensimmäinen on `home`, ja sen `kind`-kentän arvo on `IpAddrKind::V4` ja siihen liittyvä osoitedata on `127.0.0.1`. Toinen instanssi on `loopback`. Sen `kind`-kentän arvo on `IpAddrKind`-enumin toinen variantti, `V6`, ja siihen liittyvä osoite on `::1`. Olemme käyttäneet rakennetta niputtaaksemme `kind`- ja `address`-arvot yhteen, joten nyt variantti on yhdistetty arvoon.

Sama käsite voidaan kuitenkin ilmaista tiiviimmin pelkällä enumilla: sen sijaan, että enum olisi rakenteen sisällä, voimme laittaa datan suoraan kuhunkin enum-varianttiin. Tämä uusi `IpAddr`-enumin määrittely sanoo, että sekä `V4`- että `V6`-variantit sisältävät liittyvät `String`-arvot:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-02-enum-with-data/src/main.rs:here}}
```

Liitämme datan suoraan kuhunkin enum-varianttiin, joten erillistä rakennetta ei tarvita. Tässä on myös helpompi nähdä toinen yksityiskohta siitä, miten enumit toimivat: jokaisen määrittelemämme enum-variantin nimi muuttuu myös funktioksi, joka rakentaa enum-instanssin. Toisin sanoen `IpAddr::V4()` on funktiokutsu, joka ottaa `String`-argumentin ja palauttaa `IpAddr`-tyypin instanssin. Saamme tämän konstruktorifunktion automaattisesti enumin määrittelyn seurauksena.

Enumin käytössä on toinenkin etu rakenteeseen verrattuna: jokaisella variantilla voi olla eri tyyppejä ja eri määrä liittyvää dataa. Version neljä IP-osoitteissa on aina neljä numeerista komponenttia, joiden arvot ovat välillä 0–255. Jos haluaisimme tallentaa `V4`-osoitteet neljänä `u8`-arvona mutta ilmaista `V6`-osoitteet yhtenä `String`-arvona, emme voisi tehdä sitä rakenteella. Enumit käsittelevät tämän tapauksen vaivatta:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-03-variants-with-different-data/src/main.rs:here}}
```

Olemme näyttäneet useita eri tapoja määritellä tietorakenteita version neljä ja version kuusi IP-osoitteiden tallentamiseen. Kuitenkin, kuten käy ilmi, IP-osoitteiden tallentaminen ja sen koodaaminen, minkä tyyppisiä ne ovat, on niin yleistä, että [standardikirjastossa on määrittely, jota voimme käyttää!][IpAddr]<!-- ignore --> Katsotaan, miten standardikirjasto määrittelee `IpAddr`:n: siinä on täsmälleen sama enum ja variantit, jotka olemme määritelleet ja käyttäneet, mutta se upottaa osoitedatan varianttien sisään kahden eri rakenteen muodossa, jotka on määritelty eri tavoin kullekin variantille:

```rust
struct Ipv4Addr {
    // --snip--
}

struct Ipv6Addr {
    // --snip--
}

enum IpAddr {
    V4(Ipv4Addr),
    V6(Ipv6Addr),
}
```

Tämä koodi havainnollistaa, että enum-variantin sisään voi laittaa minkä tahansa tyyppistä dataa: merkkijonoja, numeerisia tyyppejä tai rakenteita, esimerkiksi. Voit jopa sisällyttää toisen enumin! Lisäksi standardikirjaston tyypit eivät usein ole paljon monimutkaisempia kuin mitä itse keksisit.

Huomaa, että vaikka standardikirjasto sisältää `IpAddr`-määrittelyn, voimme silti luoda ja käyttää omaa määrittelyämme ilman ristiriitaa, koska emme ole tuoneet standardikirjaston määrittelyä laajuuteemme. Puhumme tyyppejen tuomisesta laajuuteen enemmän Luvussa 7.

Katsotaan toista enum-esimerkkiä Listauksessa 6-2: tässä on laaja kirjo eri tyyppejä upotettuna varianteihin.

<Listing number="6-2" caption="`Message`-enum, jonka variantit tallentavat eri määriä ja tyyppejä arvoja">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-02/src/main.rs:here}}
```

</Listing>

Tässä enumissa on neljä varianttia eri tyypeillä:

- `Quit` ei sisällä lainkaan dataa.
- `Move` sisältää nimettyjä kenttiä, kuten rakenne.
- `Write` sisältää yhden `String`-arvon.
- `ChangeColor` sisältää kolme `i32`-arvoa.

Enumin määrittely varianteilla, kuten Listauksessa 6-2, on samankaltaista kuin erilaisten rakennemäärittelyjen määrittely, paitsi että enum ei käytä `struct`-avainsanaa ja kaikki variantit on ryhmitelty yhteen `Message`-tyypin alle. Seuraavat rakenteet voisivat tallentaa saman datan, jonka edellä olevat enum-variantit tallentavat:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-04-structs-similar-to-message-enum/src/main.rs:here}}
```

Mutta jos käyttäisimme eri rakenteita, joilla kullakin on oma tyypinsä, emme voisi yhtä helposti määritellä funktiota, joka ottaa minkä tahansa näistä viestityypeistä, kuin voisimme Listauksessa 6-2 määritellyllä `Message`-enumilla, joka on yksi tyyppi.

Enumeilla ja rakenteilla on vielä yksi yhteinen piirre: aivan kuten voimme määritellä metodeja rakenteille `impl`:llä, voimme määritellä metodeja myös enumeille. Tässä on `call`-niminen metodi, jonka voisimme määritellä `Message`-enumillemme:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-05-methods-on-enums/src/main.rs:here}}
```

Metodin runko käyttäisi `self`:ää saadakseen arvon, jolle metodia kutsuttiin. Tässä esimerkissä olemme luoneet muuttujan `m`, jonka arvo on `Message::Write(String::from("hello"))`, ja se on se, mikä `self` on `call`-metodin rungossa, kun `m.call()` suoritetaan.

Katsotaan vielä toista standardikirjaston enumia, joka on hyvin yleinen ja hyödyllinen: `Option`.

### `Option`-enum ja sen edut verrattuna null-arvoihin

Tämä osio tutkii `Option`-tapauskatsausta, joka on toinen standardikirjaston määrittelemä enum. `Option`-tyyppi koodaa hyvin yleisen tilanteen, jossa arvo voi olla jotain tai ei mitään.

Esimerkiksi, jos pyydät ensimmäistä alkiota ei-tyhjästä listasta, saat arvon. Jos pyydät ensimmäistä alkiota tyhjästä listasta, et saa mitään. Tämän käsitteen ilmaiseminen tyyppijärjestelmän kautta tarkoittaa, että kääntäjä voi tarkistaa, oletko käsitellyt kaikki tapaukset, jotka sinun pitäisi käsitellä; tämä ominaisuus voi estää virheitä, jotka ovat erittäin yleisiä muissa ohjelmointikielissä.

Ohjelmointikielen suunnittelua ajatellaan usein sen pohjalta, mitä ominaisuuksia sisällytetään, mutta pois jätetyt ominaisuudet ovat myös tärkeitä. Rustissa ei ole null-ominaisuutta, joka on monissa muissa kielissä. _Null_ on arvo, joka tarkoittaa, ettei siinä ole arvoa. Kielissä, joissa on null, muuttujat voivat aina olla jommassakummassa tilassa: null tai ei-null.

Vuoden 2009 esityksessään ”Null References: The Billion Dollar Mistake” Tony Hoare, nullin keksijä, sanoo seuraavaa:

> Kutsun sitä miljardidollarin virheekseni. Silloin suunnittelin ensimmäistä kattavaa tyyppijärjestelmää viittauksille olio-ohjelmointikielessä. Tavoitteenani oli varmistaa, että kaikki viittausten käyttö olisi täysin turvallista ja kääntäjä tarkistaisi sen automaattisesti. Mutta en voinut vastustaa kiusausta laittaa mukaan null-viittaus, yksinkertaisesti koska se oli niin helppo toteuttaa. Tämä on johtanut lukemattomiin virheisiin, haavoittuvuuksiin ja järjestelmän kaatumisiin, jotka ovat todennäköisesti aiheuttaneet miljardin dollarin edestä kipua ja vahinkoa viimeisten neljänkymmenen vuoden aikana.

Ongelma null-arvojen kanssa on, että jos yrität käyttää null-arvoa ei-null-arvona, saat jonkinlaisen virheen. Koska tämä null- tai ei-null-ominaisuus on kaikkialla, on erittäin helppo tehdä tämänkaltaisia virheitä.

Kuitenkin käsite, jota null yrittää ilmaista, on silti hyödyllinen: null on arvo, joka on tällä hetkellä virheellinen tai poissa jostain syystä.

Ongelma ei ole oikeastaan käsitteessä vaan tietyssä toteutuksessa. Siksi Rustissa ei ole null-arvoja, mutta siinä on enum, joka voi koodata käsitteen, että arvo on läsnä tai poissa. Tämä enum on `Option<T>`, ja se on [standardikirjaston määrittelemä][option]<!-- ignore --> seuraavasti:

```rust
enum Option<T> {
    None,
    Some(T),
}
```

`Option<T>`-enum on niin hyödyllinen, että se on jopa mukana preludessa; sinun ei tarvitse tuoda sitä laajuuteen erikseen. Sen variantit ovat myös mukana preludessa: voit käyttää `Some`- ja `None`-variantteja suoraan ilman `Option::`-etuliitettä. `Option<T>`-enum on silti tavallinen enum, ja `Some(T)` ja `None` ovat edelleen tyyppiä `Option<T>`.

`<T>`-syntaksi on Rust-ominaisuus, josta emme ole vielä puhuneet. Se on geneerinen tyyppiparametri, ja käsittelemme geneerisiä tyyppejä tarkemmin Luvussa 10. Toistaiseksi sinun tarvitsee tietää vain, että `<T>` tarkoittaa, että `Option`-enumin `Some`-variantti voi sisältää yhden kappaleen dataa mistä tahansa tyypistä, ja jokainen konkreettinen tyyppi, jota käytetään `T`:n paikalla, tekee koko `Option<T>`-tyypistä eri tyypin. Tässä on esimerkkejä `Option`-arvojen käytöstä numerotyyppejä ja merkkityyppejä tallentaen:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-06-option-examples/src/main.rs:here}}
```

Muuttujan `some_number` tyyppi on `Option<i32>`. Muuttujan `some_char` tyyppi on `Option<char>`, joka on eri tyyppi. Rust voi päätellä nämä tyypit, koska olemme määrittäneet arvon `Some`-variantin sisällä. Muuttujan `absent_number` kohdalla Rust vaatii meitä merkitsemään koko `Option`-tyypin: kääntäjä ei voi päätellä tyyppiä, jota vastaava `Some`-variantti sisältäisi, katsomalla pelkkää `None`-arvoa. Tässä kerromme Rustille, että tarkoitamme `absent_number`:n olevan tyyppiä `Option<i32>`.

Kun meillä on `Some`-arvo, tiedämme, että arvo on läsnä ja se on `Some`-variantin sisällä. Kun meillä on `None`-arvo, se tarkoittaa eräässä mielessä samaa kuin null: meillä ei ole kelvollista arvoa. Miksi `Option<T>` on siis parempi kuin null?

Lyhyesti sanottuna, koska `Option<T>` ja `T` (missä `T` voi olla mikä tahansa tyyppi) ovat eri tyyppejä, kääntäjä ei anna meidän käyttää `Option<T>`-arvoa ikään kuin se olisi varmasti kelvollinen arvo. Esimerkiksi tämä koodi ei käänny, koska se yrittää lisätä `i8`:n `Option<i8>`:aan:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-07-cant-use-option-directly/src/main.rs:here}}
```

Jos ajamme tämän koodin, saamme virheilmoituksen, joka näyttää tältä:

```console
{{#include ../listings/ch06-enums-and-pattern-matching/no-listing-07-cant-use-option-directly/output.txt}}
```

Voimakasta! Käytännössä tämä virheilmoitus tarkoittaa, että Rust ei ymmärrä, miten `i8` ja `Option<i8>` lisätään yhteen, koska ne ovat eri tyyppejä. Kun meillä on arvo tyypiltään kuten `i8` Rustissa, kääntäjä varmistaa, että meillä on aina kelvollinen arvo. Voimme edetä luottavaisin mielin ilman, että meidän täytyy tarkistaa null ennen arvon käyttöä. Vasta kun meillä on `Option<i8>` (tai mikä tahansa tyyppi, jonka kanssa työskentelemme), meidän täytyy huolehtia siitä, että arvo saattaa puuttua, ja kääntäjä varmistaa, että käsittelemme tämän tapauksen ennen arvon käyttöä.

Toisin sanoen sinun täytyy muuntaa `Option<T>` arvoksi `T`, ennen kuin voit suorittaa `T`:n operaatioita sillä. Yleisesti tämä auttaa havaitsemaan yhden yleisimmistä null-ongelmista: oletus, että jokin ei ole null, vaikka se itse asiassa on.

Virheellisen oletuksen riskin poistaminen auttaa sinua luottamaan koodiisi enemmän. Jotta voisit olla arvo, joka saattaa olla null, sinun täytyy erikseen valita se tekemällä arvon tyypiksi `Option<T>`. Sitten kun käytät sitä arvoa, sinun täytyy erikseen käsitellä tapaus, jossa arvo on null. Kaikkialla, missä arvolla on tyyppi, joka ei ole `Option<T>`, voit _turvallisesti_ olettaa, ettei arvo ole null. Tämä oli tarkoituksellinen suunnittelupäätös Rustissa rajoittaakseen nullin yleisyyttä ja lisätäkseen Rust-koodin turvallisuutta.

Miten siis saat `T`-arvon `Some`-variantista, kun sinulla on `Option<T>`-tyyppinen arvo, jotta voit käyttää sitä arvoa? `Option<T>`-enumilla on suuri määrä metodeja, jotka ovat hyödyllisiä eri tilanteissa; voit tutustua niihin [sen dokumentaatiossa][docs]<!-- ignore -->. `Option<T>`-metodien tunteminen on erittäin hyödyllistä Rust-matkallasi.

Yleisesti ottaen, jotta voit käyttää `Option<T>`-arvoa, haluat koodia, joka käsittelee kunkin variantin. Haluat koodia, joka suoritetaan vain, kun sinulla on `Some(T)`-arvo, ja tämä koodi saa käyttää sisäistä `T`:tä. Haluat toisenlaista koodia, joka suoritetaan vain, jos sinulla on `None`-arvo, eikä tässä koodissa ole `T`-arvoa käytettävissä. `match`-lauseke on ohjausrakenne, joka tekee juuri tämän enumien kanssa käytettynä: se suorittaa eri koodia riippuen siitä, mikä enumin variantti sillä on, ja tämä koodi voi käyttää vastaavan arvon sisällä olevaa dataa.

[IpAddr]: ../std/net/enum.IpAddr.html
[option]: ../std/option/enum.Option.html
[docs]: ../std/option/enum.Option.html
