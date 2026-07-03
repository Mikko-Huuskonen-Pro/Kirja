<!-- Old headings. Do not remove or links may break. -->

<a id="using-trait-objects-that-allow-for-values-of-different-types"></a>

## Trait-olioiden käyttö yhteisen käyttäytymisen abstrahoimiseen

Luvussa 8 mainitsimme, että vektorien yksi rajoitus on, että ne voivat tallentaa vain yhden tyyppisiä elementtejä. Loimme kiertotien listauksessa 8-9 määrittelemällä `SpreadsheetCell`-luettelotyypin, jolla on variantteja kokonaislukujen, liukulukujen ja tekstin tallentamiseen. Näin voimme tallentaa eri tyyppistä dataa jokaiseen soluun ja silti pitää vektorin, joka edustaa soluriviä. Tämä on täysin hyvä ratkaisu, kun vaihdettavat kohteet ovat kiinteä joukko tyyppejä, jotka tiedämme käännösaikana.

Joskus haluamme kuitenkin, että kirjastomme käyttäjä voi laajentaa tiettyyn tilanteeseen kelpaavien tyyppien joukkoa. Näyttääksemme, miten tämän voisimme saavuttaa, luomme esimerkin graafisen käyttöliittymän (GUI) työkalusta, joka käy läpi kohteiden listan ja kutsuu jokaisella `draw`-metodia piirtääkseen sen näytölle — yleinen tekniikka GUI-työkaluissa. Luomme kirjastokrateen nimeltä `gui`, joka sisältää GUI-kirjaston rakenteen. Tämä krate voi sisältää joitakin tyyppejä ihmisten käyttöön, kuten `Button` tai `TextField`. Lisäksi `gui`-käyttäjät haluavat luoda omia piirrettäviä tyyppejä: esimerkiksi yksi ohjelmoija saattaa lisätä `Image`-tyypin ja toinen `SelectBox`-tyypin.

Kirjastoa kirjoittaessamme emme voi tietää ja määritellä kaikkia tyyppejä, joita muut ohjelmoijat saattavat haluta luoda. Tiedämme kuitenkin, että `gui`:n täytyy seurata monia eri tyyppisiä arvoja ja kutsua `draw`-metodia jokaisella näistä eri tyyppisistä arvoista. Sen ei tarvitse tietää tarkalleen, mitä tapahtuu kun kutsumme `draw`-metodia, vain että arvolla on kyseinen metodi käytettävissä.

Periytymistä käyttävässä kielessä voisimme määritellä luokan nimeltä `Component`, jolla on metodi `draw`. Muut luokat, kuten `Button`, `Image` ja `SelectBox`, perisivät `Component`-luokasta ja siten perisivät `draw`-metodin. Ne voisivat kukin ylikirjoittaa `draw`-metodin määritelläkseen oman käyttäytymisensä, mutta kehys voisi käsitellä kaikkia tyyppejä kuin ne olisivat `Component`-instansseja ja kutsua niillä `draw`-metodia. Koska Rustissa ei ole periytymistä, tarvitsemme toisen tavan rakentaa `gui`-kirjasto niin, että käyttäjät voivat luoda kirjaston kanssa yhteensopivia uusia tyyppejä.

### Yhteisen käyttäytymisen traitin määrittely

Toteuttaaksemme haluamamme `gui`-käyttäytymisen määrittelemme traitin nimeltä `Draw`, jolla on yksi metodi nimeltä `draw`. Sitten voimme määritellä vektorin, joka ottaa trait-olion. _Trait-olio_ osoittaa sekä määrittelemämme traitin toteuttavan tyypin instanssiin että taulukkoon, jota käytetään trait-metodien hakemiseen kyseiseltä tyypiltä ajonaikana. Luomme trait-olion määrittelemällä jonkinlaisen osoittimen, kuten viitteen tai `Box<T>`-älyosoittimen, sitten `dyn`-avainsanan ja sitten asiaankuuluvan traitin. (Puhumme syystä, miksi trait-olioiden täytyy käyttää osoitinta, kohdassa [”Dynaamisesti mitoitetut tyypit ja `Sized`-trait”][dynamically-sized]<!-- ignore --> luvussa 20.) Voimme käyttää trait-olioita geneerisen tai konkreettisen tyypin sijaan. Missä tahansa käytämme trait-oliota, Rustin tyyppijärjestelmä varmistaa käännösaikana, että kyseisessä kontekstissa käytetty arvo toteuttaa trait-olion traitin. Näin ollen emme tarvitse tietää kaikkia mahdollisia tyyppejä käännösaikana.

Olemme maininneet, että Rustissa vältämme kutsumasta rakenteita ja luettelotyyppejä ”olioiksi” erottaaksemme ne muiden kielten olioista. Rakenteessa tai luettelotyypissä rakenteen kentissä oleva data ja `impl`-lohkojen käyttäytyminen ovat erillään, kun taas muissa kielissä data ja käyttäytyminen yhdistettynä yhteen käsitteeseen merkitään usein olioksi. Trait-oliot eroavat muiden kielten olioista siinä, että trait-olioon ei voi lisätä dataa. Trait-oliot eivät ole yhtä yleisesti hyödyllisiä kuin muiden kielten oliot: niiden erityinen tarkoitus on mahdollistaa abstraktio yhteisen käyttäytymisen yli.

Listaus 18-3 näyttää, miten määritellään trait `Draw` yhdellä `draw`-metodilla.

<Listing number="18-3" file-name="src/lib.rs" caption="`Draw`-traitin määritelmä">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-03/src/lib.rs}}
```

</Listing>

Tämän syntaksin pitäisi näyttää tutulta keskusteluistamme traitien määrittelystä luvussa 10. Seuraavaksi tulee uutta syntaksia: listaus 18-4 määrittelee rakenteen `Screen`, joka sisältää vektorin nimeltä `components`. Tämä vektori on tyyppiä `Box<dyn Draw>`, joka on trait-olio; se on sijaisarvo mille tahansa `Box`-sisällä olevalle tyypille, joka toteuttaa `Draw`-traitin.

<Listing number="18-4" file-name="src/lib.rs" caption="`Screen`-rakenteen määritelmä, jossa `components`-kenttä sisältää `Draw`-traitin toteuttavien trait-olioiden vektorin">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-04/src/lib.rs:here}}
```

</Listing>

`Screen`-rakenteelle määrittelemme metodin `run`, joka kutsuu `draw`-metodia jokaisella `components`-kentän komponentilla, kuten listauksessa 18-5 näytetään.

<Listing number="18-5" file-name="src/lib.rs" caption="`run`-metodi `Screen`-rakenteella, joka kutsuu `draw`-metodia jokaisella komponentilla">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-05/src/lib.rs:here}}
```

</Listing>

Tämä toimii eri tavalla kuin rakenteen määrittely geneerisellä tyyppiparametrilla trait-sidonnoin. Geneerinen tyyppiparametri voidaan korvata vain yhdellä konkreettisella tyypillä kerrallaan, kun taas trait-oliot sallivat useiden konkreettisten tyyppien täyttää trait-olion paikan ajonaikana. Voisimme esimerkiksi määritellä `Screen`-rakenteen käyttämällä geneeristä tyyppiä ja trait-sidontaa, kuten listauksessa 18-6.

<Listing number="18-6" file-name="src/lib.rs" caption="Vaihtoehtoinen `Screen`-rakenteen ja sen `run`-metodin toteutus geneerisyyttä ja trait-sidontoja käyttäen">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-06/src/lib.rs:here}}
```

</Listing>

Tämä rajoittaa meidät `Screen`-instanssiin, jonka komponenttilista sisältää kaikki `Button`- tai kaikki `TextField`-tyyppisiä komponentteja. Jos sinulla on vain homogeenisia kokoelmia, geneerisyyden ja trait-sidontojen käyttö on parempi, koska määritelmät monomorfisoidaan käännösaikana käyttämään konkreettisia tyyppejä.

Toisaalta trait-olioita käyttävällä menetelmällä yksi `Screen`-instanssi voi sisältää `Vec<T>`-vektorin, jossa on sekä `Box<Button>` että `Box<TextField>`. Katsotaan, miten tämä toimii, ja puhumme sitten ajonaikaisen suorituskyvyn vaikutuksista.

### Traitin toteuttaminen

Lisäämme nyt tyyppejä, jotka toteuttavat `Draw`-traitin. Tarjoamme `Button`-tyypin. Varsinaisen GUI-kirjaston toteuttaminen on tämän kirjan laajuuden ulkopuolella, joten `draw`-metodilla ei ole hyödyllistä toteutusta rungossaan. Kuvitellaksemme, miltä toteutus voisi näyttää, `Button`-rakenteella voi olla kentät `width`, `height` ja `label`, kuten listauksessa 18-7.

<Listing number="18-7" file-name="src/lib.rs" caption="`Button`-rakenne, joka toteuttaa `Draw`-traitin">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-07/src/lib.rs:here}}
```

</Listing>

`Button`-rakenteen kentät `width`, `height` ja `label` eroavat muiden komponenttien kentistä; esimerkiksi `TextField`-tyypillä voi olla samat kentät plus `placeholder`-kenttä. Jokainen tyyppi, jonka haluamme piirtää näytölle, toteuttaa `Draw`-traitin, mutta käyttää eri koodia `draw`-metodissa määritelläkseen, miten kyseinen tyyppi piirretään, kuten `Button` tässä (ilman varsinaista GUI-koodia, kuten mainittiin). `Button`-tyypillä voi esimerkiksi olla lisä-`impl`-lohko metodeille, jotka liittyvät siihen, mitä tapahtuu kun käyttäjä napsauttaa painiketta. Tällaiset metodit eivät sovellu tyypeille kuten `TextField`.

Jos joku kirjastomme käyttäjä päättää toteuttaa `SelectBox`-rakenteen, jolla on kentät `width`, `height` ja `options`, he toteuttaisivat `Draw`-traitin myös `SelectBox`-tyypille, kuten listauksessa 18-8.

<Listing number="18-8" file-name="src/main.rs" caption="Toinen krate käyttää `gui`-kirjastoa ja toteuttaa `Draw`-traitin `SelectBox`-rakenteelle">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-08/src/main.rs:here}}
```

</Listing>

Kirjastomme käyttäjä voi nyt kirjoittaa `main`-funktionsa luodakseen `Screen`-instanssin. `Screen`-instanssiin he voivat lisätä `SelectBox`- ja `Button`-komponentit laittamalla kummankin `Box<T>`-säiliöön trait-olioksi. Sitten he voivat kutsua `run`-metodia `Screen`-instanssilla, joka kutsuu `draw`-metodia jokaisella komponentilla. Listaus 18-9 näyttää tämän toteutuksen.

<Listing number="18-9" file-name="src/main.rs" caption="Trait-olioiden käyttö eri tyyppisten, saman traitin toteuttavien arvojen tallentamiseen">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-09/src/main.rs:here}}
```

</Listing>

Kirjastoa kirjoittaessamme emme tienneet, että joku saattaa lisätä `SelectBox`-tyypin, mutta `Screen`-toteutuksemme pystyi toimimaan uudella tyypillä ja piirtämään sen, koska `SelectBox` toteuttaa `Draw`-traitin, mikä tarkoittaa, että se toteuttaa `draw`-metodin.

Tämä käsite — huolehtia vain viesteistä, joihin arvo vastaa, eikä arvon konkreettisesta tyypistä — muistuttaa _ankkutyyppauksen_ käsitettä dynaamisesti tyypitetyissä kielissä: jos se kävelee kuin ankka ja nokkuu kuin ankka, sen täytyy olla ankka! `Screen`-rakenteen `run`-toteutuksessa listauksessa 18-5 `run` ei tarvitse tietää kunkin komponentin konkreettista tyyppiä. Se ei tarkista, onko komponentti `Button`- tai `SelectBox`-instanssi, vaan kutsuu vain komponentin `draw`-metodia. Määrittelemällä `components`-vektorin arvojen tyypiksi `Box<dyn Draw>` olemme määritelleet `Screen`-rakenteen tarvitsevan arvoja, joilla voimme kutsua `draw`-metodia.

Trait-olioiden ja Rustin tyyppijärjestelmän käytön etu koodin kirjoittamisessa, joka muistuttaa ankkutyyppauksen käyttöä, on, ettemme koskaan joudu tarkistamaan ajonaikana, toteuttaako arvo tietyn metodin, emmekä huoli virheistä, jos arvo ei toteuta metodia mutta kutsumme sitä silti. Rust ei käännä koodiamme, jos arvot eivät toteuta trait-olioiden tarvitsemia traitteja.

Esimerkiksi listaus 18-10 näyttää, mitä tapahtuu, jos yritämme luoda `Screen`-rakenteen, jonka komponentti on `String`.

<Listing number="18-10" file-name="src/main.rs" caption="Yritys käyttää tyyppiä, joka ei toteuta trait-olion traitia">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-10/src/main.rs}}
```

</Listing>

Saamme tämän virheen, koska `String` ei toteuta `Draw`-traitia:

```console
{{#include ../listings/ch18-oop/listing-18-10/output.txt}}
```

Tämä virhe kertoo meille, että joko välitämme `Screen`-rakenteelle jotain, mitä emme tarkoittaneet, ja siksi pitäisi välittää eri tyyppi, tai meidän pitäisi toteuttaa `Draw` `String`-tyypille, jotta `Screen` voi kutsua sillä `draw`-metodia.

<!-- Old headings. Do not remove or links may break. -->

<a id="trait-objects-perform-dynamic-dispatch"></a>

### Dynaamisen lähetyksen suorittaminen

Muistutaan kohdasta [”Geneeristä koodia käyttävän koodin suorituskyky”][performance-of-code-using-generics]<!-- ignore --> luvussa 10 keskusteluamme kääntäjän geneerisyyksille suorittamasta monomorfisointiprosessista: kääntäjä generoi ei-geneerisiä toteutuksia funktioille ja metodeille jokaiselle konkreettiselle tyypille, jota käytämme geneerisen tyyppiparametrin sijaan. Monomorfisoinnista syntyvä koodi tekee _staattista lähetystä_, jossa kääntäjä tietää käännösaikana, mitä metodia kutsut. Tämä on vastakohta _dynaamiselle lähetykselle_, jossa kääntäjä ei voi käännösaikana kertoa, mitä metodia kutsut. Dynaamisen lähetyksen tapauksissa kääntäjä tuottaa koodia, joka ajonaikana tietää, mitä metodia kutsua.

Kun käytämme trait-olioita, Rustin täytyy käyttää dynaamista lähetystä. Kääntäjä ei tiedä kaikkia tyyppejä, joita voidaan käyttää trait-olioita käyttävän koodin kanssa, joten se ei tiedä, mitä tyypille toteutettua metodia kutsua. Sen sijaan ajonaikana Rust käyttää trait-olion sisällä olevia osoittimia tietääkseen, mitä metodia kutsua. Tämä haku aiheuttaa ajonaikaisen kustannuksen, jota ei esiinny staattisessa lähetyksessä. Dynaaminen lähetys estää myös kääntäjää valitsemasta metodin koodin sisällyttämistä, mikä puolestaan estää joitakin optimointeja, ja Rustilla on sääntöjä siitä, missä dynaamista lähetystä voi ja ei voi käyttää — näitä kutsutaan _dyn-yhteensopivuudeksi_. Nämä säännöt ovat tämän keskustelun laajuuden ulkopuolella, mutta voit lukea niistä lisää [viitteestä][dyn-compatibility]<!-- ignore -->. Saimme kuitenkin lisäjoustavuutta listauksessa 18-5 kirjoittamaamme koodiin ja pystyimme tukemaan listauksessa 18-9 esitettyä, joten se on harkittava kompromissi.

[performance-of-code-using-generics]: ch10-01-syntax.html#performance-of-code-using-generics
[dynamically-sized]: ch20-03-advanced-types.html#dynamically-sized-types-and-the-sized-trait
[dyn-compatibility]: https://doc.rust-lang.org/reference/items/traits.html#dyn-compatibility
