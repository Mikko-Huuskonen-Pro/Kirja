## Älykkäiden osoittimien käsittely kuten tavallisia viitteitä `Deref`-traitin avulla

Toteuttamalla `Deref`-traitin voit mukauttaa _dereferenssioperaattorin_ `*` käyttäytymistä (ei pidä sekoittaa kertolasku- tai globaalioperaattoriin). Kun toteutat `Deref`-traitin niin, että älykästä osoitinta voidaan käsitellä tavallisen viitteen tapaan, voit kirjoittaa koodia, joka toimii viitteillä, ja käyttää sitä koodia myös älykkäiden osoittimien kanssa.

Katsotaan ensin, miten dereferenssioperaattori toimii tavallisten viitteiden kanssa.
Sitten yritämme määrittää oman tyypin, joka käyttäytyy kuten `Box<T>`, ja näemme, miksi
dereferenssioperaattori ei toimi viitteen tavoin juuri määrittämässämme tyypissä. Tutkimme,
miten `Deref`-traitin toteuttaminen mahdollistaa älykkäiden osoittimien toiminnan
viitteiden tapaan. Lopuksi katsomme Rustin _deref-muunnosta_ (`deref coercion`) ja sitä,
miten se antaa meidän työskennellä joko viitteiden tai älykkäiden osoittimien kanssa.

> Huom: Rakennettavassa `MyBox<T>`-tyypissä on yksi suuri ero oikeaan `Box<T>`:ään verrattuna: versiomme ei tallenna dataa keolle.
> Keskitymme tässä esimerkissä `Deref`-traitiin, joten datan varsinaisen tallennuspaikan
> merkitys on vähemmän tärkeä kuin osoitinmaiselle käyttäytymiselle.

<!-- Old link, do not remove -->

<a id="following-the-pointer-to-the-value-with-the-dereference-operator"></a>

### Osoittimen seuraaminen arvon luo

Tavallinen viite on eräs osoitintyyppi, ja yksi tapa ajatella osoitinta on nuolena
jossain muualla tallennettuun arvoon. Listauksessa 15-6 luomme viitteen `i32`-arvoon ja
käytämme dereferenssioperaattoria seurataksemme viitettä arvoon:

<Listing number="15-6" file-name="src/main.rs" caption="Dereferenssioperaattorin käyttö viitteen seuraamiseen `i32`-arvoon">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-06/src/main.rs}}
```

</Listing>

Muuttuja `x` sisältää `i32`-arvon `5`. Asetamme `y`:n viittaamaan `x`:ään. Voimme
varmistaa, että `x` on yhtä suuri kuin `5`. Jos haluamme kuitenkin tehdä väittämän
`y`:n arvosta, meidän on käytettävä `*y`:tä seurataksemme viitettä arvoon, johon se
osoittaa (siksi _dereferenssi_), jotta kääntäjä voi vertailla varsinaista arvoa. Kun
olemme dereferoineet `y`:n, pääsemme käsiksi kokonaislukuun, johon `y` osoittaa, ja
voimme vertailla sitä lukuun `5`.

Jos yrittäisimme kirjoittaa `assert_eq!(5, y);` sen sijaan, saisimme tämän käännösvirheen:

```console
{{#include ../listings/ch15-smart-pointers/output-only-01-comparing-to-reference/output.txt}}
```

Luvun ja viittauksen lukuun vertaileminen ei ole sallittua, koska ne ovat eri tyyppejä.
Meidän on käytettävä dereferenssioperaattoria seurataksemme viitettä arvoon, johon se
osoittaa.

### `Box<T>`:n käyttäminen kuten viitettä

Voimme kirjoittaa Listauksen 15-6 koodin uudelleen käyttämään `Box<T>`:tä viitteen
sijaan; Listauksessa 15-7 `Box<T>`:ään käytetty dereferenssioperaattori toimii samalla
tavalla kuin Listauksessa 15-6 viitteeseen käytetty dereferenssioperaattori:

<Listing number="15-7" file-name="src/main.rs" caption="Dereferenssioperaattorin käyttö `Box<i32>`:llä">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-07/src/main.rs}}
```

</Listing>

Listauksen 15-7 ja Listauksen 15-6 pääero on, että tässä asetamme `y`:n olevan
`Box<T>`-instanssi, joka osoittaa `x`:n kopioidun arvon, eikä viite, joka osoittaa
`x`:n arvoon. Viimeisessä väittämässä voimme käyttää dereferenssioperaattoria
seurataksemme `Box<T>`:n osoitinta samalla tavalla kuin silloin, kun `y` oli viite.
Seuraavaksi tutkimme, mikä `Box<T>`:ssä on erityistä ja mahdollistaa dereferenssioperaattorin
käytön määrittelemällä oman tyypin.

### Oman älykkään osoittimen määrittely

Rakennetaan älykäs osoitin, joka on samanlainen kuin standardikirjaston tarjoama
`Box<T>`-tyyppi, jotta näemme, miten älykkäät osoittimet käyttäytyvät oletuksena
erilailla kuin viitteet. Sitten katsomme, miten lisätään kyky käyttää dereferenssioperaattoria.

`Box<T>`-tyyppi on lopulta määritelty yhden elementin tuple-structina, joten Listauksessa
15-8 määritellään `MyBox<T>`-tyyppi samalla tavalla. Määrittelemme myös `new`-funktion
vastaamaan `Box<T>`:ään määriteltyä `new`-funktiota.

<Listing number="15-8" file-name="src/main.rs" caption="`MyBox<T>`-tyypin määrittely">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-08/src/main.rs:here}}
```

</Listing>

Määrittelemme structin nimeltä `MyBox` ja ilmoitamme geneerisen parametrin `T`, koska
haluamme tyypin voivan sisältää minkä tahansa tyyppisiä arvoja. `MyBox`-tyyppi on
tuple-struct, jossa on yksi `T`-tyyppinen elementti. `MyBox::new`-funktio ottaa yhden
`T`-tyyppisen parametrin ja palauttaa `MyBox`-instanssin, joka sisältää annetun arvon.

Yritetään lisätä Listauksen 15-7 `main`-funktio Listaukseen 15-8 ja muuttaa se käyttämään
määrittämäämme `MyBox<T>`-tyyppiä `Box<T>`:n sijaan. Listauksen 15-9 koodi ei käänny,
koska Rust ei tiedä, miten `MyBox`:ia dereferoidaan.

<Listing number="15-9" file-name="src/main.rs" caption="Yritys käyttää `MyBox<T>`:tä samalla tavalla kuin viitteitä ja `Box<T>`:tä">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-09/src/main.rs:here}}
```

</Listing>

Tässä on tuloksena oleva käännösvirhe:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-09/output.txt}}
```

`MyBox<T>`-tyyppiä ei voi dereferoida, koska emme ole toteuttaneet sitä kykyä tyypille.
Jotta dereferointi `*`-operaattorilla onnistuisi, toteutamme `Deref`-traitin.

<!-- Old link, do not remove -->

<a id="treating-a-type-like-a-reference-by-implementing-the-deref-trait"></a>

### `Deref`-traitin toteuttaminen

Kuten käsiteltiin [”Traitin toteuttaminen tyypille”][impl-trait]<!-- ignore --> -osiossa
Luvussa 10, traitin toteuttamiseksi meidän on annettava toteutukset traitin vaatimille
metodeille. Standardikirjaston tarjoama `Deref`-trait vaatii meitä toteuttamaan yhden
metodin nimeltä `deref`, joka lainaa `self`:n ja palauttaa viitteen sisäiseen dataan.
Listauksessa 15-10 on `Deref`-toteutus, joka lisätään `MyBox<T>`:n määrittelyyn:

<Listing number="15-10" file-name="src/main.rs" caption="`Deref`-traitin toteuttaminen `MyBox<T>`:lle">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-10/src/main.rs:here}}
```

</Listing>

`type Target = T;` -syntaksi määrittelee assosioitun tyypin, jota `Deref`-trait käyttää.
Assosioituneet tyypit ovat hieman erilainen tapa ilmoittaa geneerinen parametri, mutta
sinun ei tarvitse huolehtia niistä nyt; käsittelemme niitä tarkemmin Luvussa 20.

Täytämme `deref`-metodin rungon arvolla `&self.0`, jotta `deref` palauttaa viitteen
arvoon, johon haluamme päästä `*`-operaattorilla; muista Luvun 5 osiosta [”Tuple-structien
käyttö ilman nimettyjä kenttiä eri tyyppien luomiseen”][tuple-structs]<!-- ignore -->, että
`.0` pääsee tuple-structin ensimmäiseen arvoon. Listauksen 15-9 `main`-funktio, joka
kutsuu `*`:ää `MyBox<T>`-arvolla, kääntyy nyt, ja väittämät menevät läpi!

Ilman `Deref`-traitia kääntäjä voi dereferoida vain `&`-viitteitä. `deref`-metodi antaa
kääntäjälle kyvyn ottaa mikä tahansa `Deref`-traitin toteuttava tyyppi ja kutsua `deref`-metodia
saadakseen `&`-viitteen, jonka dereferointi se osaa.

Kun kirjoitimme `*y` Listauksessa 15-9, Rust suoritti kulissien takana tämän koodin:

```rust,ignore
*(y.deref())
```

Rust korvaa `*`-operaattorin kutsulla `deref`-metodiin ja sitten tavallisella dereferoinnilla,
jotta meidän ei tarvitse miettiä, pitääkö `deref`-metodia kutsua. Tämä Rustin ominaisuus
antaa meidän kirjoittaa koodia, joka toimii identtisesti riippumatta siitä, onko meillä
tavallinen viite vai `Deref`-traitin toteuttava tyyppi.

Syy siihen, miksi `deref`-metodi palauttaa viitteen arvoon ja miksi tavallinen dereferointi
sulkujen ulkopuolella lausekkeessa `*(y.deref())` on silti tarpeen, liittyy omistajuusjärjestelmään.
Jos `deref`-metodi palauttaisi arvon suoraan viittauksen sijaan, arvo siirtyisi pois
`self`:stä. Emme halua ottaa omistajuutta `MyBox<T>`:n sisäisestä arvosta tässä tapauksessa
eikä useimmissa tapauksissa, joissa käytämme dereferenssioperaattoria.

Huomaa, että `*`-operaattori korvataan kutsulla `deref`-metodiin ja sitten kutsulla
`*`-operaattoriin vain kerran joka kerta, kun käytämme `*`:ää koodissamme. Koska `*`-operaattorin
korvaaminen ei toistu loputtomasti, päädymme lopulta `i32`-tyyppiseen dataan, joka vastaa
Listauksen 15-9 `assert_eq!`-lausekkeen `5`:ttä.

### Implisiittinen deref-muunnos funktioiden ja metodien kanssa

_Deref-muunnos_ muuntaa viitteen tyypille, joka toteuttaa `Deref`-traitin, viitteeksi
toiseen tyyppiin. Esimerkiksi deref-muunnos voi muuntaa `&String`:n `&str`:ksi, koska
`String` toteuttaa `Deref`-traitin niin, että se palauttaa `&str`:n. Deref-muunnos on
Rustin tarjoama kätevyys funktioiden ja metodien argumenteille, ja se toimii vain tyypeille,
jotka toteuttavat `Deref`-traitin. Se tapahtuu automaattisesi, kun välitämme viitteen
tietyn tyypin arvoon funktiolle tai metodille, joka ei vastaa funktion tai metodin
määrittelyssä olevaa parametrietyyppiä. Sarja kutsuja `deref`-metodiin muuntaa antamamme
tyypin parametrin vaatimaan tyyppiin.

Deref-muunnos lisättiin Rustiin, jotta funktio- ja metodikutsuja kirjoittavat ohjelmoijat
eivät joutuisi lisäämään yhtä monta eksplisiittistä viitettä ja dereferenssiä `&`- ja
`*`-operaattoreilla. Deref-muunnos antaa myös kirjoittaa enemmän koodia, joka toimii
joko viitteillä tai älykkäillä osoittimilla.

Nähdäksemme deref-muunnoksen toiminnassa, käytetään Listauksessa 15-8 määriteltyä
`MyBox<T>`-tyyppiä sekä Listauksessa 15-10 lisättyä `Deref`-toteutusta. Listauksessa 15-11
on funktion määrittely, jolla on merkkijonoviipaleparametri:

<Listing number="15-11" file-name="src/main.rs" caption="`hello`-funktio, jonka parametrilla `name` on tyyppi `&str`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-11/src/main.rs:here}}
```

</Listing>

Voimme kutsua `hello`-funktiota merkkijonoviipaleargumentilla, esimerkiksi `hello("Rust");`.
Deref-muunnos mahdollistaa `hello`-funktion kutsumisen viitteellä `MyBox<String>`-tyyppiseen
arvoon, kuten Listauksessa 15-12 näytetään:

<Listing number="15-12" file-name="src/main.rs" caption="`hello`-funktion kutsuminen viitteellä `MyBox<String>`-arvoon, mikä toimii deref-muunnoksen ansiosta">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-12/src/main.rs:here}}
```

</Listing>

Tässä kutsumme `hello`-funktiota argumentilla `&m`, joka on viite `MyBox<String>`-arvoon.
Koska toteutimme `Deref`-traitin `MyBox<T>`:lle Listauksessa 15-10, Rust voi muuntaa
`&MyBox<String>`:n `&String`:ksi kutsumalla `deref`:iä. Standardikirjasto tarjoaa `Deref`-toteutuksen
`String`:lle, joka palauttaa merkkijonoviipaleen, ja tämä on `Deref`:in API-dokumentaatiossa.
Rust kutsuu `deref`:iä uudelleen muuntaakseen `&String`:n `&str`:ksi, mikä vastaa `hello`-funktion
määrittelyä.

Jos Rust ei toteuttaisi deref-muunnosta, meidän pitäisi kirjoittaa Listauksen 15-13 koodi
Listauksen 15-12 koodin sijaan kutsuaksemme `hello`:a `&MyBox<String>`-tyyppisellä arvolla.

<Listing number="15-13" file-name="src/main.rs" caption="Koodi, jonka meidän pitäisi kirjoittaa, jos Rustissa ei olisi deref-muunnosta">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-13/src/main.rs:here}}
```

</Listing>

`(*m)` dereferoi `MyBox<String>`:n `String`:ksi. Sitten `&` ja `[..]` ottavat `String`:stä
merkkijonoviipaleen, joka on koko merkkijono, vastatakseen `hello`:n signatuuria. Tämä
koodi ilman deref-muunnoksia on vaikeampi lukea, kirjoittaa ja ymmärtää kaikkine näine
symboleineen. Deref-muunnos antaa Rustin käsitellä nämä muunnokset automaattisesti puolestamme.

Kun `Deref`-trait on määritelty mukana oleville tyypeille, Rust analysoi tyypit ja käyttää
`Deref::deref`:iä niin monta kertaa kuin tarvitaan saadakseen viitteen vastaamaan parametrin
tyyppiä. `Deref::deref`:in lisäysten määrä ratkaistaan käännösaikana, joten deref-muunnoksen
hyödyntämisestä ei ole suorituskykyhaittaa ajonaikana!

### Miten deref-muunnos vaikuttaa mutabiliteettiin

Samalla tavalla kuin käytät `Deref`-traitia korvaamaan `*`-operaattorin muuttumattomilla
viitteillä, voit käyttää `DerefMut`-traitia korvaamaan `*`-operaattorin muuttuvilla viitteillä.

Rust tekee deref-muunnoksen, kun se löytää tyypit ja trait-toteutukset kolmessa tapauksessa:

1. `&T`:stä `&U`:ksi, kun `T: Deref<Target=U>`
2. `&mut T`:stä `&mut U`:ksi, kun `T: DerefMut<Target=U>`
3. `&mut T`:stä `&U`:ksi, kun `T: Deref<Target=U>`

Kaksi ensimmäistä tapausta ovat samanlaiset paitsi että toinen toteuttaa mutabiliteetin.
Ensimmäinen tapaus sanoo, että jos sinulla on `&T` ja `T` toteuttaa `Deref`:in johonkin
tyyppiin `U`, voit saada `&U`:n läpinäkyvästi. Toinen tapaus sanoo, että sama deref-muunnos
tapahtuu muuttuville viitteille.

Kolmas tapaus on hankalampi: Rust muuntaa myös muuttuvan viitteen muuttumattomaksi. Mutta
päinvastainen _ei_ ole mahdollista: muuttumattomia viitteitä ei koskaan muunneta muuttuviksi
viitteiksi. Lainaussääntöjen vuoksi, jos sinulla on muuttuva viite, sen täytyy olla ainoa
viite kyseiseen dataan (muuten ohjelma ei kääntyisi). Yhden muuttuvan viitteen muuntaminen
yhteen muuttumattomaan viitteeseen ei koskaan riko lainaussääntöjä. Muuttumattoman viitteen
muuntaminen muuttuvaksi viitteeksi vaatisi, että alkuperäinen muuttumaton viite on ainoa
muuttumaton viite kyseiseen dataan, mutta lainaussäännöt eivät takaa sitä. Siksi Rust ei
voi olettaa, että muuttumattoman viitteen muuntaminen muuttuvaksi viitteeksi on mahdollista.

[impl-trait]: ch10-02-traits.html#implementing-a-trait-on-a-type
[tuple-structs]: ch05-01-defining-structs.html#using-tuple-structs-without-named-fields-to-create-different-types
