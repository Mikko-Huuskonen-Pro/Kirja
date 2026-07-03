## Metodisyntaksi

_Metodit_ ovat samankaltaisia kuin funktiot: ne määritellään `fn`-avainsanalla ja
nimellä, niillä voi olla parametreja ja palautusarvo, ja ne sisältävät koodia,
joka suoritetaan, kun metodia kutsutaan jostakin muualta. Toisin kuin funktiot,
metodit määritellään rakenteen (tai luettelotyypin tai trait-objektin, joita
käsitellään [Luvussa 6][enums]<!-- ignore --> ja [Luvussa
18][trait-objects]<!-- ignore -->, vastaavasti) yhteydessä, ja niiden ensimmäinen
parametri on aina `self`, joka edustaa rakenteen instanssia, jolle metodia
kutsutaan.

### Metodin määrittely

Muutetaan `area`-funktio, jolla on `Rectangle`-instanssi parametrina, ja
tehdään sen sijaan `area`-metodi, joka määritellään `Rectangle`-rakenteelle,
kuten Listauksessa 5-13 on esitetty.

<Listing number="5-13" file-name="src/main.rs" caption="`area`-metodin määrittely `Rectangle`-rakenteelle">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-13/src/main.rs}}
```

</Listing>

Määrittääksemme funktion `Rectangle`-kontekstissa, aloitamme `impl`
(toteutus) -lohkon `Rectangle`-rakenteelle. Kaikki tämän `impl`-lohkon sisällä
on liitetty `Rectangle`-tyyppiin. Siirrämme sitten `area`-funktion `impl`-lohkon
aaltosulkeiden sisään ja muutamme ensimmäisen (ja tässä tapauksessa ainoan)
parametrin signatuurissa ja kaikkialla rungossa muotoon `self`. `main`-funktiossa,
jossa kutsuimme `area`-funktiota ja välitimme `rect1`:n argumenttina, voimme
sen sijaan käyttää _metodisyntaksia_ kutsuaksemme `area`-metodia
`Rectangle`-instanssillamme. Metodisyntaksi tulee instanssin jälkeen: lisäämme
pisteen, metodin nimen, sulkeet ja mahdolliset argumentit.

`area`-metodin signatuurissa käytämme `&self`:ää `rectangle: &Rectangle`:n
sijaan. `&self` on itse asiassa lyhenne muodolle `self: &Self`. `impl`-lohkon
sisällä tyyppi `Self` on alias tyypille, jolle `impl`-lohko on tarkoitettu.
Metodeilla täytyy olla ensimmäisenä parametrinaan nimeltään `self` tyyppiä
`Self`, joten Rust antaa sinun lyhentää tämän pelkällä nimellä `self`
ensimmäisessä parametripaikassa. Huomaa, että meidän täytyy silti käyttää `&`:ää
`self`-lyhenteen edessä osoittaaksemme, että tämä metodi lainaa `Self`-instanssia,
aivan kuten teimme `rectangle: &Rectangle`:ssa. Metodit voivat ottaa omistajuuden
`self`:stä, lainata `self`:ää muuttumattomasti, kuten teimme tässä, tai lainata
`self`:ää muuttuvasti, aivan kuten ne voivat tehdä mille tahansa muulle
parametrille.

Valitsimme `&self`:n tässä samasta syystä kuin käytimme `&Rectangle`:a
funktioversiossa: emme halua ottaa omistajuutta, ja haluamme vain lukea
rakenteen dataa, emme kirjoittaa siihen. Jos haluaisimme muuttaa instanssia,
jolle metodia kutsutaan, osana sitä, mitä metodi tekee, käyttäisimme
`&mut self`:ää ensimmäisenä parametrina. Metodi, joka ottaa omistajuuden
instanssista käyttämällä pelkkää `self`:ää ensimmäisenä parametrina, on harvinainen;
tätä tekniikkaa käytetään yleensä silloin, kun metodi muuntaa `self`:n joksikin
muuksi ja haluat estää kutsujaa käyttämästä alkuperäistä instanssia muunnoksen
jälkeen.

Pääsyy metodien käyttämiseen funktioiden sijaan, metodisyntaksin tarjoamisen ja
sen lisäksi, ettei `self`:n tyyppiä tarvitse toistaa jokaisen metodin
signatuurissa, on organisointi. Olemme sijoittaneet kaikki asiat, joita voimme
tehdä tyypin instanssilla, yhteen `impl`-lohkoon sen sijaan, että pakottaisimme
koodimme tulevat käyttäjät etsimään `Rectangle`:n ominaisuuksia eri paikoista
tarjoamassamme kirjastossa.

Huomaa, että voimme halutessamme antaa metodille saman nimen kuin rakenteen
kentällä on. Esimerkiksi voimme määritellä `Rectangle`-rakenteelle metodin, joka
on myös nimeltään `width`:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-06-method-field-interaction/src/main.rs:here}}
```

</Listing>

Tässä valitsemme, että `width`-metodi palauttaa `true`, jos instanssin `width`-
kentän arvo on suurempi kuin `0`, ja `false`, jos arvo on `0`: voimme käyttää
kenttää saman nimisen metodin sisällä mihin tahansa tarkoitukseen. `main`-funktiossa,
kun `rect1.width`:n jälkeen tulee sulkeet, Rust tietää, että tarkoitamme metodia
`width`. Kun emme käytä sulkeita, Rust tietää, että tarkoitamme kenttää `width`.

Usein, mutta ei aina, kun annamme metodille saman nimen kuin kentällä on, haluamme
sen vain palauttavan kentän arvon eikä tekevän mitään muuta. Tällaisia metodeja
kutsutaan _gettereiksi_, eikä Rust toteuta niitä automaattisesti rakenteen
kentille, kuten jotkut muut kielet tekevät. Getterit ovat hyödyllisiä, koska voit
tehdä kentästä yksityisen mutta metodista julkisen ja siten mahdollistaa
vain-luku-pääsyn kyseiseen kenttään osana tyypin julkista API:a. Käsittelemme,
mitä julkinen ja yksityinen ovat ja miten kenttä tai metodi merkitään julkiseksi
tai yksityiseksi, [Luvussa 7][public]<!-- ignore -->.

> ### Missä on `->`-operaattori?
>
> C:ssä ja C++:ssa käytetään kahta eri operaattoria metodien kutsumiseen: käytät
> `.`:a, jos kutsut metodia suoraan objektille, ja `->`:a, jos kutsut metodia
> objektin osoittimella ja sinun täytyy ensin dereferoida osoitin. Toisin sanoen,
> jos `object` on osoitin, `object->something()` on samankaltainen kuin
> `(*object).something()`.
>
> Rustilla ei ole vastaavaa `->`-operaattoria; sen sijaan Rustissa on ominaisuus
> nimeltä _automaattinen viittaaminen ja dereferointi_. Metodien kutsuminen on
> yksi harvoista paikoista Rustissa, joissa tämä käyttäytyminen esiintyy.
>
> Näin se toimii: kun kutsut metodia `object.something()`:lla, Rust lisää
> automaattisesti `&`:n, `&mut`:n tai `*`:n, jotta `object` vastaa metodin
> signatuuria. Toisin sanoen seuraavat ovat samat:
>
> <!-- CAN'T EXTRACT SEE BUG https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust
> # #[derive(Debug,Copy,Clone)]
> # struct Point {
> #     x: f64,
> #     y: f64,
> # }
> #
> # impl Point {
> #    fn distance(&self, other: &Point) -> f64 {
> #        let x_squared = f64::powi(other.x - self.x, 2);
> #        let y_squared = f64::powi(other.y - self.y, 2);
> #
> #        f64::sqrt(x_squared + y_squared)
> #    }
> # }
> # let p1 = Point { x: 0.0, y: 0.0 };
> # let p2 = Point { x: 5.0, y: 6.5 };
> p1.distance(&p2);
> (&p1).distance(&p2);
> ```
>
> Ensimmäinen näyttää paljon siistimmältä. Tämä automaattinen viittaamisen
> käyttäytyminen toimii, koska metodeilla on selkeä vastaanottaja—`self`:n tyyppi.
> Vastaanottajan ja metodin nimen perusteella Rust voi selvästi päätellä, lukeeko
> metodi (`&self`), muuttaako (`&mut self`) vai kuluttaako (`self`) instanssia.
> Se, että Rust tekee lainaamisesta implisiittistä metodien vastaanottajille, on
> merkittävä osa omistajuuden käytännön ergonomiaa.

### Metodit, joilla on useita parametreja

Harjoitellaan metodien käyttöä toteuttamalla toinen metodi `Rectangle`-rakenteelle.
Tällä kertaa haluamme, että `Rectangle`-instanssi ottaa toisen `Rectangle`-
instanssin ja palauttaa `true`, jos toinen `Rectangle` mahtuu kokonaan `self`:n
(eli ensimmäisen `Rectangle`:n) sisään; muuten sen pitäisi palauttaa `false`.
Toisin sanoen, kun olemme määritelleet `can_hold`-metodin, haluamme pystyä
kirjoittamaan Listauksessa 5-14 näytetyn ohjelman.

<Listing number="5-14" file-name="src/main.rs" caption="Vielä kirjoittamattoman `can_hold`-metodin käyttö">

```rust,ignore
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-14/src/main.rs}}
```

</Listing>

Odotettu tuloste näyttäisi seuraavalta, koska `rect2`:n molemmat mitat ovat
pienempiä kuin `rect1`:n mitat, mutta `rect3` on leveämpi kuin `rect1`:

```text
Can rect1 hold rect2? true
Can rect1 hold rect3? false
```

Tiedämme, että haluamme määritellä metodin, joten se on `impl Rectangle` -lohkon
sisällä. Metodin nimi on `can_hold`, ja se ottaa parametrina muuttumattoman
lainauksen toisesta `Rectangle`:sta. Voimme päätellä parametrin tyypin
katsomalla koodia, joka kutsuu metodia: `rect1.can_hold(&rect2)` välittää
`&rect2`:n, joka on muuttumaton lainaus `rect2`:sta, `Rectangle`-instanssista.
Tämä on järkevää, koska meidän täytyy vain lukea `rect2`:a (eikä kirjoittaa,
mikä tarkoittaisi, että tarvitsisimme muuttuvan lainauksen), ja haluamme `main`:in
säilyttävän omistajuuden `rect2`:sta, jotta voimme käyttää sitä uudelleen
`can_hold`-metodin kutsumisen jälkeen. `can_hold`-metodin palautusarvo on
totuusarvo, ja toteutus tarkistaa, ovatko `self`:n leveys ja korkeus suurempia
kuin toisen `Rectangle`:n leveys ja korkeus, vastaavasti. Lisätään uusi
`can_hold`-metodi Listauksen 5-13 `impl`-lohkoon, kuten Listauksessa 5-15 on
esitetty.

<Listing number="5-15" file-name="src/main.rs" caption="`can_hold`-metodin toteutus `Rectangle`-rakenteelle, joka ottaa toisen `Rectangle`-instanssin parametrina">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-15/src/main.rs:here}}
```

</Listing>

Kun ajamme tämän koodin Listauksen 5-14 `main`-funktiolla, saamme haluamamme
tulosteen. Metodeilla voi olla useita parametreja, jotka lisätään signatuuriin
`self`-parametrin jälkeen, ja nämä parametrit toimivat aivan kuten parametrit
funktioissa.

### Liittyvät funktiot

Kaikkia `impl`-lohkon sisällä määriteltyjä funktioita kutsutaan _liittyviksi
funktioiksi_, koska ne liittyvät `impl`:n jälkeen nimettyyn tyyppiin. Voimme
määritellä liittyviä funktioita, joilla ei ole `self`:ää ensimmäisenä
parametrinaan (ja jotka siten eivät ole metodeja), koska niiden ei tarvitse
tyypin instanssia työskennelläkseen. Olemme jo käyttäneet tällaista funktiota:
`String::from`-funktiota, joka on määritelty `String`-tyypille.

Liittyviä funktioita, jotka eivät ole metodeja, käytetään usein konstruktoreina,
jotka palauttavat rakenteen uuden instanssin. Näitä kutsutaan usein `new`:ksi,
mutta `new` ei ole erityinen nimi eikä se ole sisäänrakennettu kieleen. Esimerkiksi
voisimme halutessamme tarjota liittyvän funktion nimeltä `square`, jolla olisi
yksi mittaparametri ja joka käyttäisi sitä sekä leveytenä että korkeutena, mikä
helpottaisi neliön muotoisen `Rectangle`:n luomista sen sijaan, että joutuisimme
määrittämään saman arvon kahdesti:

<span class="filename">Tiedostonimi: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-03-associated-functions/src/main.rs:here}}
```

`Self`-avainsanat palautustyypissä ja funktion rungossa ovat aliaksia tyypille,
joka esiintyy `impl`-avainsanan jälkeen, joka tässä tapauksessa on `Rectangle`.

Kutsuaksemme tätä liittyvää funktiota, käytämme `::`-syntaksia rakenteen nimen
kanssa; `let sq = Rectangle::square(3);` on esimerkki. Tämä funktio on
rakenteen nimiavaruudessa: `::`-syntaksia käytetään sekä liittyville funktioille
että moduulien luomille nimiavaruuksille. Käsittelemme moduuleja [Luvussa
7][modules]<!-- ignore -->.

### Useita `impl`-lohkoja

Jokaisella rakenteella saa olla useita `impl`-lohkoja. Esimerkiksi Listausta 5-15
vastaa Listauksessa 5-16 näytetty koodi, jossa jokainen metodi on omassa
`impl`-lohkossaan.

<Listing number="5-16" caption="Listauksen 5-15 uudelleenkirjoitus useilla `impl`-lohkoilla">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-16/src/main.rs:here}}
```

</Listing>

Ei ole syytä erotella näitä metodeja useisiin `impl`-lohkoihin tässä, mutta
tämä on kelvollista syntaksia. Näemme tapauksen, jossa useat `impl`-lohkot
ovat hyödyllisiä Luvussa 10, jossa käsittelemme geneerisiä tyyppejä ja traitteja.

## Yhteenveto

Rakenteet antavat sinun luoda mukautettuja tyyppejä, jotka ovat merkityksellisiä
sovellusalueellesi. Rakenteiden avulla voit pitää toisiinsa liittyvät datan osat
yhteydessä toisiinsa ja nimetä jokaisen osan, jotta koodisi on selkeää.
`impl`-lohkoissa voit määritellä tyypillesi liittyviä funktioita, ja metodit
ovat eräänlaisia liittyviä funktioita, joiden avulla voit määrittää käyttäytymisen,
joka rakenteidesi instansseilla on.

Mutta rakenteet eivät ole ainoa tapa luoda mukautettuja tyyppejä: siirrytään
Rustin luettelotyyppi-ominaisuuteen lisätäksemme työkalupakkiisi uuden työkalun.

[enums]: ch06-00-enums.html
[trait-objects]: ch18-02-trait-objects.md
[public]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html#exposing-paths-with-the-pub-keyword
[modules]: ch07-02-defining-modules-to-control-scope-and-privacy.html
