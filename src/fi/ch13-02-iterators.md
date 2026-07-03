## Kohteiden sarjojen käsittely iteraattoreilla

Iteraattorimalli mahdollistaa tehtävien suorittamisen sarjalle kohteita vuorotellen.
Iteraattori huolehtii logiikasta, jolla käydään läpi jokainen kohde ja määritetään, milloin
sarja on päättynyt. Käyttäessäsi iteraattoreita sinun ei tarvitse toteuttaa tätä logiikkaa
uudelleen itse.

Rustissa iteraattorit ovat _laiskoja_, eli niillä ei ole vaikutusta ennen kuin kutsut
metodeja, jotka kuluttavat iteraattorin sen käyttämiseksi loppuun. Esimerkiksi listauksen 13-10
koodi luo iteraattorin vektorin `v1` alkioille kutsumalla `Vec<T>`-tyypille määriteltyä
`iter`-metodia. Tämä koodi ei itsessään tee mitään hyödyllistä.

<Listing number="13-10" file-name="src/main.rs" caption="Iteraattorin luominen">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-10/src/main.rs:here}}
```

</Listing>

Iteraattori tallennetaan muuttujaan `v1_iter`. Kun iteraattori on luotu, voimme käyttää sitä
monin eri tavoin. Listauksessa 3-5 iteroimme taulukkoa `for`-silmukalla suorittaaksemme
koodia jokaiselle sen alkioille. Taustalla tämä loi ja kulutti implisiittisesti iteraattorin,
mutta ohitimme siihen asti tarkalleen, miten se toimii.

Listauksen 13-11 esimerkissä erotamme iteraattorin luonnin iteraattorin käytöstä `for`-silmukassa.
Kun `for`-silmukkaa kutsutaan käyttäen iteraattoria `v1_iter`-muuttujassa, jokaista iteraattorin
alkiota käytetään yhdessä silmukan kierroksessa, jolloin jokainen arvo tulostetaan.

<Listing number="13-11" file-name="src/main.rs" caption="Iteraattorin käyttö `for`-silmukassa">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-11/src/main.rs:here}}
```

</Listing>

Kielissä, joiden standardikirjasto ei tarjoa iteraattoreita, kirjoittaisit todennäköisesti saman
toiminnallisuuden aloittamalla muuttujan arvosta 0, käyttämällä tuota muuttujaa indeksinä vektoriin
arvon hakemiseksi ja kasvattamalla muuttujan arvoa silmukassa, kunnes se saavuttaa vektorin alkiojen
kokonaismäärän.

Iteraattorit hoitavat koko tämän logiikan puolestasi, vähentäen toistuvaa koodia, jonka voisit
potentiaalisesti kirjoittaa väärin. Iteraattorit antavat sinulle enemmän joustavuutta käyttää samaa
logiikkaa monenlaisissa sarjoissa, eivätkä ne rajoitu vain tietorakenteisiin, joihin pääsee käsiksi
indeksin avulla, kuten vektoreihin. Tarkastellaan, miten iteraattorit tekevät sen.

### `Iterator`-trait ja `next`-metodi

Kaikki iteraattorit toteuttavat standardikirjastossa määritellyn `Iterator`-nimisen traitin.
Traitin määritelmä näyttää tältä:

```rust
pub trait Iterator {
    type Item;

    fn next(&mut self) -> Option<Self::Item>;

    // methods with default implementations elided
}
```

Huomaa, että tämä määritelmä käyttää uutta syntaksia: `type Item` ja `Self::Item`, jotka määrittelevät
tälle traitille liittyvän tyypin. Käsittelemme liittyviä tyyppejä perusteellisesti luvussa 20. Toistaiseksi
riittää tietää, että tämä koodi sanoo, että `Iterator`-traitin toteuttaminen edellyttää myös `Item`-tyypin
määrittelyä, ja tätä `Item`-tyyppiä käytetään `next`-metodin palautustyypissä. Toisin sanoen `Item`-tyyppi
on tyyppi, jonka iteraattori palauttaa.

`Iterator`-trait edellyttää toteuttajilta vain yhden metodin määrittelyä: `next`-metodin, joka palauttaa
yhdellä kerralla yhden iteraattorin alkion käärittynä `Some`-arvoon ja kun iterointi on päättynyt,
palauttaa `None`-arvon.

Voimme kutsua `next`-metodia iteraattoreilla suoraan; listaus 13-12 havainnollistaa, mitä arvoja
palautetaan toistuvilla `next`-kutsuilla iteraattorille, joka on luotu vektorista.

<Listing number="13-12" file-name="src/lib.rs" caption="`next`-metodin kutsuminen iteraattorilla">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-12/src/lib.rs:here}}
```

</Listing>

Huomaa, että meidän täytyi tehdä `v1_iter` muuttuvaksi: iteraattorin `next`-metodin kutsuminen
muuttaa sisäistä tilaa, jota iteraattori käyttää seuratakseen sijaintiaan sarjassa. Toisin sanoen tämä
koodi _kuluttaa_ eli käyttää iteraattorin loppuun. Jokainen `next`-kutsu kuluttaa yhden alkion
iteraattorista. Meidän ei tarvinnut tehdä `v1_iter`-muuttujasta muuttuvaa käyttäessämme `for`-silmukkaa,
koska silmukka otti omistajuuden `v1_iter`-muuttujasta ja teki sen muuttuvaksi taustalla.

Huomaa myös, että `next`-kutsuista saamamme arvot ovat muuttumattomia viittauksia vektorin arvoihin.
`iter`-metodi tuottaa iteraattorin muuttumattomien viittausten yli. Jos haluamme luoda iteraattorin,
joka ottaa omistajuuden `v1`-muuttujasta ja palauttaa omistettuja arvoja, voimme kutsua `into_iter`-metodia
`iter`-metodin sijaan. Vastaavasti, jos haluamme iteroida muuttuvien viittausten yli, voimme kutsua
`iter_mut`-metodia `iter`-metodin sijaan.

### Iteraattorin kuluttavat metodit

`Iterator`-traitilla on useita eri metodeja, joille standardikirjasto tarjoaa oletustoteutukset; näistä
metodeista voi lukea standardikirjaston API-dokumentaatiosta `Iterator`-traitin kohdalta. Jotkin näistä
metodeista kutsuvat määritelmässään `next`-metodia, minkä vuoksi `Iterator`-traitin toteuttamisessa
on pakollista toteuttaa `next`-metodi.

Metodeja, jotka kutsuvat `next`-metodia, kutsutaan _kuluttaviksi sovittimiksi_, koska niiden kutsuminen
käyttää iteraattorin loppuun. Yksi esimerkki on `sum`-metodi, joka ottaa omistajuuden iteraattorista ja
iteroi alkioiden läpi kutsumalla toistuvasti `next`-metodia ja näin kuluttaen iteraattorin. Iteroidessaan
se lisää jokaisen alkion käynnissä olevaan summaan ja palauttaa summan, kun iterointi on valmis. Listauksessa
13-13 on testi, joka havainnollistaa `sum`-metodin käyttöä.

<Listing number="13-13" file-name="src/lib.rs" caption="`sum`-metodin kutsuminen iteraattorin kaikkien alkioiden summan saamiseksi">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-13/src/lib.rs:here}}
```

</Listing>

Emme saa käyttää `v1_iter`-muuttujaa `sum`-kutsun jälkeen, koska `sum` ottaa omistajuuden iteraattorista,
jolle sitä kutsutaan.

### Muita iteraattoreja tuottavat metodit

_Iteraattorisovittimet_ ovat `Iterator`-traitille määriteltyjä metodeja, jotka eivät kuluta iteraattoria.
Sen sijaan ne tuottavat eri iteraattoreja muuttamalla jotakin alkuperäisen iteraattorin ominaisuutta.

Listaus 13-14 näyttää esimerkin iteraattorisovitinmetodin `map` kutsumisesta, joka ottaa sulkeisen
kutsumista varten jokaiselle alkioille, kun alkioiden läpi iteroidaan. `map`-metodi palauttaa uuden
iteraattorin, joka tuottaa muokatut alkiot. Tässä sulkeinen luo uuden iteraattorin, jossa vektorin jokainen
alkio kasvatetaan yhdellä.

<Listing number="13-14" file-name="src/main.rs" caption="Iteraattorisovittimen `map` kutsuminen uuden iteraattorin luomiseksi">

```rust,not_desired_behavior
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-14/src/main.rs:here}}
```

</Listing>

Tämä koodi tuottaa kuitenkin varoituksen:

```console
{{#include ../listings/ch13-functional-features/listing-13-14/output.txt}}
```

Listauksen 13-14 koodi ei tee mitään; määrittämäämme sulkeista ei koskaan kutsuta. Varoitus muistuttaa
miksi: iteraattorisovittimet ovat laiskoja, ja meidän täytyy kuluttaa iteraattori tässä.

Varoituksen korjaamiseksi ja iteraattorin kuluttamiseksi käytämme `collect`-metodia, jota käytimme
`env::args`-funktion kanssa listauksessa 12-1. Tämä metodi kuluttaa iteraattorin ja kerää tuloksena
syntyvät arvot kokoelmatietotyypiksi.

Listauksessa 13-15 keräämme `map`-kutsusta palautetun iteraattorin iteroinnin tulokset vektoriksi.
Tämä vektori sisältää lopulta jokaisen alkuperäisen vektorin alkion kasvatettuna yhdellä.

<Listing number="13-15" file-name="src/main.rs" caption="`map`-metodin kutsuminen uuden iteraattorin luomiseksi ja sitten `collect`-metodin kutsuminen uuden iteraattorin kuluttamiseksi ja vektorin luomiseksi">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-15/src/main.rs:here}}
```

</Listing>

Koska `map` ottaa sulkeisen, voimme määrittää minkä tahansa operaation, jonka haluamme suorittaa
jokaiselle alkioille. Tämä on erinomainen esimerkki siitä, miten sulkeiset antavat sinun mukauttaa
käyttäytymistä samalla kun hyödynnät uudelleen `Iterator`-traitin tarjoamaa iterointikäyttäytymistä.

Voit ketjuttaa useita iteraattorisovitinmetodien kutsuja suorittaaksesi monimutkaisia toimintoja
luettavalla tavalla. Koska kaikki iteraattorit ovat kuitenkin laiskoja, sinun täytyy kutsua yhtä
kuluttavista sovitinmetodeista saadaksesi tuloksia iteraattorisovitinmetodien kutsuista.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-closures-that-capture-their-environment"></a>

### Ympäristönsä sieppaavat sulkeiset

Monet iteraattorisovittimet ottavat sulkeisia argumentteina, ja usein iteraattorisovittimille määrittämämme
sulkeiset ovat sulkeisia, jotka sieppaavat ympäristönsä.

Tätä esimerkkiä varten käytämme `filter`-metodia, joka ottaa sulkeisen. Sulkeinen saa alkion iteraattorista
ja palauttaa `bool`-arvon. Jos sulkeinen palauttaa `true`, arvo sisällytetään `filter`-metodin tuottamaan
iteraattoriin. Jos sulkeinen palauttaa `false`, arvoa ei sisällytetä.

Listauksessa 13-16 käytämme `filter`-metodia sulkeisella, joka sieppaa `shoe_size`-muuttujan ympäristöstään
iteroidakseen `Shoe`-rakenteen instanssien kokoelman yli. Se palauttaa vain kengät, joiden koko on määritetty.

<Listing number="13-16" file-name="src/lib.rs" caption="`filter`-metodin käyttö `shoe_size`-muuttujaa sieppaavan sulkeisen kanssa">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-16/src/lib.rs}}
```

</Listing>

`shoes_in_size`-funktio ottaa omistajuuden kenkävektorista ja kenkäkoosta parametreina. Se palauttaa vektorin,
joka sisältää vain määritetyn kokoiset kengät.

`shoes_in_size`-funktion rungossa kutsumme `into_iter`-metodia luodaksemme iteraattorin, joka ottaa omistajuuden
vektorista. Sen jälkeen kutsumme `filter`-metodia mukauttaaksemme iteraattorin uudeksi iteraattoriksi, joka
sisältää vain ne alkiot, joille sulkeinen palauttaa `true`-arvon.

Sulkeinen sieppaa `shoe_size`-parametrin ympäristöstä ja vertaa arvoa kunkin kengän kokoon, säilyttäen vain
määritetyn kokoiset kengät. Lopuksi `collect`-kutsu kerää mukautetun iteraattorin palauttamat arvot vektoriin,
jonka funktio palauttaa.

Testi osoittaa, että kun kutsumme `shoes_in_size`-funktiota, saamme takaisin vain kengät, joiden koko on sama
kuin määrittämämme arvo.
