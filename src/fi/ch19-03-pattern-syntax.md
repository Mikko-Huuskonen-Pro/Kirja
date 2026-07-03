## Mallin syntaksi

Tässä osiossa kokoamme yhteen kaiken syntaksin, joka on sallittu malleissa, ja
käsittelemme, miksi ja milloin saatat haluta käyttää kutakin.

### Literaalien vastaaminen

Kuten näit luvussa 6, voit vastata malleja suoraan literaaleja vasten.
Seuraava koodi antaa joitakin esimerkkejä:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-01-literals/src/main.rs:here}}
```

Tämä koodi tulostaa `one`, koska `x`:n arvo on `1`. Tämä syntaksi on hyödyllinen,
kun haluat koodisi suorittavan toiminnon, jos se saa tietyn konkreettisen arvon.

### Nimetyt muuttujat

Nimetyt muuttujat ovat kiistämättömiä malleja, jotka vastaavat mitä tahansa
arvoa, ja olemme käyttäneet niitä monesti tässä kirjassa. On kuitenkin yksi
monimutkaisuus, kun käytät nimettyjä muuttujia `match`-, `if let`- tai
`while let` -lausekkeissa. Koska jokainen näistä lauseketyypeistä aloittaa uuden
alueen, lausekkeen sisällä mallissa määritellyt muuttujat varjostavat samannimiset
muuttujat rakenteen ulkopuolella, kuten kaikki muuttujat. Listauksessa 19-11
määrittelemme muuttujan nimeltä `x` arvolla `Some(5)` ja muuttujan `y` arvolla
`10`. Luomme sitten `match`-lausekkeen `x`:n arvolle. Katso match-haarojen
malleja ja lopun `println!`-kutsua ja yritä arvata, mitä koodi tulostaa, ennen
kuin suoritat koodin tai luet eteenpäin.

<Listing number="19-11" file-name="src/main.rs" caption="`match`-lauseke, jonka haara esittelee uuden muuttujan, joka varjostaa olemassa olevan muuttujan `y`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-11/src/main.rs:here}}
```

</Listing>

Käydään läpi, mitä tapahtuu, kun `match`-lauseke suoritetaan. Ensimmäisen
match-haaran malli ei vastaa `x`:n määriteltyä arvoa, joten koodi jatkuu.

Toisen match-haaran malli esittelee uuden muuttujan nimeltä `y`, joka vastaa
mitä tahansa arvoa `Some`-arvon sisällä. Koska olemme uudella alueella
`match`-lausekkeen sisällä, tämä on uusi `y`-muuttuja, ei alussa arvolla `10`
määrittelemämme `y`. Tämä uusi `y`-sidonta vastaa mitä tahansa arvoa
`Some`-arvon sisällä, mikä on se, mitä meillä on `x`:ssä. Siksi tämä uusi `y`
sitoutuu `x`:n `Some`-arvon sisäiseen arvoon. Tuo arvo on `5`, joten kyseisen
haaran lauseke suoritetaan ja tulostaa `Matched, y = 5`.

Jos `x` olisi ollut `None`-arvo `Some(5)`:n sijaan, ensimmäisten kahden haaran
mallit eivät olisi vastanneet, joten arvo olisi vastannut alaviivaan. Emme
esitelleet `x`-muuttujaa alaviiva-haaran mallissa, joten lausekkeen `x` on
edelleen ulompi `x`, jota ei ole varjostettu. Tässä hypoteettisessa tapauksessa
`match` tulostaisi `Default case, x = None`.

Kun `match`-lauseke on valmis, sen alue päättyy, ja samoin sisemmän `y`:n alue.
Viimeinen `println!` tuottaa `at the end: x = Some(5), y = 10`.

Luodaksemme `match`-lausekkeen, joka vertaa ulompien `x`- ja `y`-muuttujien
arvoja sen sijaan, että esittelisimme uuden muuttujan, joka varjostaa
olemassa olevan `y`-muuttujan, meidän täytyisi käyttää match-ehtoa. Puhumme
match-ehdoista myöhemmin kohdassa [”Lisäehtoja match-ehtojen
avulla”](#adding-conditionals-with-match-guards)<!-- ignore -->.

<!-- Old headings. Do not remove or links may break. -->
<a id="multiple-patterns"></a>

### Useiden mallien vastaaminen

`match`-lausekkeissa voit vastata useita malleja käyttämällä `|`-syntaksia,
joka on mallien _tai_-operaattori. Esimerkiksi seuraavassa koodissa vastaamme
`x`:n arvoa match-haaroihin, joista ensimmäisessä on _tai_-vaihtoehto, mikä
tarkoittaa, että jos `x`:n arvo vastaa kumman tahansa arvon kyseisessä haarassa,
kyseisen haaran koodi suoritetaan:


```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-02-multiple-patterns/src/main.rs:here}}
```

Tämä koodi tulostaa `one or two`.

### Arvoalueiden vastaaminen `..=`-syntaksilla

`..=`-syntaksi antaa meidän vastata sisältävään arvoalueeseen. Seuraavassa
koodissa, kun malli vastaa mitä tahansa annetun alueen arvoista, kyseinen haara
suoritetaan:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-03-ranges/src/main.rs:here}}
```

Jos `x` on `1`, `2`, `3`, `4` tai `5`, ensimmäinen haara vastaa. Tämä syntaksi
on kätevämpi useille vastaamisarvoille kuin saman idean ilmaiseminen `|`-operaattorilla;
jos käyttäisimme `|`, meidän pitäisi määritellä `1 | 2 | 3 | 4 | 5`. Alueen
määrittely on paljon lyhyempää, varsinkin jos haluamme vastata esimerkiksi
minkä tahansa luvun väliltä 1–1000!

Kääntäjä tarkistaa käännösaikana, ettei alue ole tyhjä, ja koska ainoat tyypit,
joille Rust voi kertoa, onko alue tyhjä vai ei, ovat `char` ja numeeriset arvot,
alueet ovat sallittuja vain numeerisille tai `char`-arvoille.

Tässä on esimerkki `char`-arvoalueiden käytöstä:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-04-ranges-of-char/src/main.rs:here}}
```

Rust voi kertoa, että `'c'` on ensimmäisen mallin alueella, ja tulostaa
`early ASCII letter`.

### Purkaminen arvojen erotteluun

Voimme myös käyttää malleja purkaaksemme rakenteita, enumeja ja tupleja
käyttääksemme näiden arvojen eri osia. Käydään läpi jokainen arvotyyppi.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-structs"></a>

#### Rakenteet

Listaus 19-12 näyttää `Point`-rakenteen, jossa on kentät `x` ja `y`, jotka
voimme purkaa erilleen mallilla `let`-lausekkeessa.

<Listing number="19-12" file-name="src/main.rs" caption="Rakenteen kenttien purkaminen erillisiksi muuttujiksi">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-12/src/main.rs}}
```

</Listing>

Tämä koodi luo muuttujat `a` ja `b`, jotka vastaavat `p`-rakenteen kenttien
`x` ja `y` arvot. Tämä esimerkki osoittaa, etteivät mallin muuttujien nimet
tarvitse vastata rakenteen kenttien nimiä. On kuitenkin yleistä vastata
muuttujien nimet kenttien nimiin, jotta on helpompi muistaa, mistä kentistä
muuttujat tulivat. Tämän yleisen käytännön vuoksi ja koska
`let Point { x: x, y: y } = p;` sisältää paljon toistoa, Rustissa on oikotie
rakenteen kenttiin vastaaville malleille: sinun tarvitsee vain listata rakenteen
kentän nimi, ja mallista luodut muuttujat saavat samat nimet. Listaus 19-13
käyttäytyy samalla tavalla kuin listauksen 19-12 koodi, mutta `let`-mallissa
luodut muuttujat ovat `x` ja `y` `a`:n ja `b`:n sijaan.

<Listing number="19-13" file-name="src/main.rs" caption="Rakenteen kenttien purkaminen rakenteen kenttien oikotiellä">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-13/src/main.rs}}
```

</Listing>

Tämä koodi luo muuttujat `x` ja `y`, jotka vastaavat `p`-muuttujan kentät
`x` ja `y`. Lopputuloksena muuttujat `x` ja `y` sisältävät arvot `p`-rakenteesta.

Voimme myös purkaa literaaliarvoja osana rakenteen mallia sen sijaan, että
loisimme muuttujia kaikille kentille. Näin voimme testata joitakin kenttiä
tiettyjä arvoja vasten samalla kun luomme muuttujia purkaaksemme muut kentät.

Listauksessa 19-14 meillä on `match`-lauseke, joka jakaa `Point`-arvot kolmeen
tapaukseen: pisteet, jotka ovat suoraan `x`-akselilla (tosi kun `y = 0`),
`y`-akselilla (`x = 0`) tai kummallakaan.

<Listing number="19-14" file-name="src/main.rs" caption="Purkaminen ja literaaliarvojen vastaaminen yhdessä mallissa">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-14/src/main.rs:here}}
```

</Listing>

Ensimmäinen haara vastaa minkä tahansa pisteen, joka on `x`-akselilla
määrittämällä, että `y`-kenttä vastaa, jos sen arvo vastaa literaaliarvoa `0`.
Malli luo silti `x`-muuttujan, jota voimme käyttää tämän haaran koodissa.

Vastaavasti toinen haara vastaa minkä tahansa pisteen `y`-akselilla
määrittämällä, että `x`-kenttä vastaa, jos sen arvo on `0`, ja luo `y`-muuttujan
`y`-kentän arvolle. Kolmas haara ei määrittele literaaleja, joten se vastaa
minkä tahansa muun `Point`-arvon ja luo muuttujat sekä `x`- että `y`-kentille.

Tässä esimerkissä arvo `p` vastaa toista haaraa, koska `x` sisältää arvon `0`,
joten tämä koodi tulostaa `On the y axis at 7`.

Muista, että `match`-lauseke lopettaa haarojen tarkistamisen, kun se on löytänyt
ensimmäisen vastaavan mallin, joten vaikka `Point { x: 0, y: 0 }` olisi sekä
`x`- että `y`-akselilla, tämä koodi tulostaisi vain `On the x axis at 0`.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-enums"></a>

#### Enumit

Olemme purkaneet enumeja tässä kirjassa (esimerkiksi listaus 6-5 luvussa 6),
mutta emme ole vielä eksplisiittisesti käsitelleet, että enumin purkamiseen
käytettävä malli vastaa enumiin tallennetun datan määrittelytapaa. Esimerkkinä
listauksessa 19-15 käytämme `Message`-enumia listauksesta 6-2 ja kirjoitamme
`match`-lausekkeen malleilla, jotka purkavat jokaisen sisäisen arvon.

<Listing number="19-15" file-name="src/main.rs" caption="Eri tyyppisiä arvoja sisältävien enum-varianttien purkaminen">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-15/src/main.rs}}
```

</Listing>

Tämä koodi tulostaa `Change color to red 0, green 160, and blue 255`. Kokeile
muuttaa `msg`:n arvoa nähdäksesi muiden haarojen koodin suorituksen.

Enum-varianteille, joilla ei ole dataa, kuten `Message::Quit`, emme voi purkaa
arvoa enempää. Voimme vain vastata literaaliarvoa `Message::Quit`, eikä
kyseisessä mallissa ole muuttujia.

Rakenteen kaltaisille enum-varianteille, kuten `Message::Move`, voimme käyttää
rakenteisiin vastaamiseen samankaltaista mallia. Variantin nimen jälkeen
laitamme aaltosulkeet ja listamme kentät muuttujilla, jotta voimme purkaa osat
käytettäväksi tämän haaran koodissa. Tässä käytämme oikotietä kuten listauksessa
19-13.

Tuple-tyyppisille enum-varianteille, kuten `Message::Write`, joka sisältää
tuplen yhdellä elementillä, ja `Message::ChangeColor`, joka sisältää tuplen
kolmella elementillä, malli on samankaltainen kuin tupleihin vastaamiseen
käytettävä malli. Mallin muuttujien määrän täytyy vastata variantin elementtien
määrää, jota vastaamme.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-nested-structs-and-enums"></a>

#### Sisäkkäiset rakenteet ja enumit

Tähän asti esimerkkimme ovat vastanneet rakenteita tai enumeja yhdellä tasolla,
mutta vastaaminen toimii myös sisäkkäisille alkioille! Voimme esimerkiksi
refaktoroida listauksen 19-15 koodin tukemaan RGB- ja HSV-värejä
`ChangeColor`-viestissä, kuten listauksessa 19-16.

<Listing number="19-16" caption="Sisäkkäisiin enumeihin vastaaminen">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-16/src/main.rs}}
```

</Listing>

`match`-lausekkeen ensimmäisen haaran malli vastaa `Message::ChangeColor`-
enum-variantin, joka sisältää `Color::Rgb`-variantin; malli sitoutuu sitten
kolmeen sisäiseen `i32`-arvoon. Toisen haaran malli vastaa myös
`Message::ChangeColor`-enum-variantin, mutta sisäinen enum vastaa `Color::Hsv`:tä.
Voimme määritellä nämä monimutkaiset ehdot yhdessä `match`-lausekkeessa, vaikka
mukana on kaksi enumia.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-structs-and-tuples"></a>

#### Rakenteet ja tuplet

Voimme sekoittaa, vastata ja sisäkkäistää purkumalleja vielä monimutkaisemmilla
tavoilla. Seuraava esimerkki näyttää monimutkaisen purkamisen, jossa sisäkkäistämme
rakenteita ja tupleja tuplen sisään ja puramme kaikki primitiiviarvot:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-05-destructuring-structs-and-tuples/src/main.rs:here}}
```

Tämä koodi antaa meidän purkaa monimutkaiset tyypit osiinsa, jotta voimme
käyttää kiinnostavia arvoja erikseen.

Purkaminen malleilla on kätevä tapa käyttää arvojen osia, kuten kunkin rakenteen
kentän arvoa, erillään toisistaan.

### Arvojen huomiotta jättäminen mallissa

Olet nähnyt, että on joskus hyödyllistä jättää arvoja huomiotta mallissa, kuten
`match`-lausekkeen viimeisessä haarassa, saadaksesi catch-all-haaran, joka ei
varsinaisesti tee mitään mutta kattaa kaikki jäljellä olevat mahdolliset arvot.
On muutamia tapoja jättää kokonaisia arvoja tai arvojen osia huomiotta mallissa:
käyttämällä `_`-mallia (jonka olet nähnyt), käyttämällä `_`-mallia toisen mallin
sisällä, käyttämällä alaviivalla alkavaa nimeä tai käyttämällä `..`-syntaksia
jättääksemme huomiotta arvon jäljellä olevat osat. Tutkitaan, miten ja miksi
käyttää kutakin näistä malleista.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-an-entire-value-with-_"></a>

#### Kokonainen arvo `_`:llä

Olemme käyttäneet alaviivaa jokerimallina, joka vastaa minkä tahansa arvon mutta
ei sido arvoon. Tämä on erityisen hyödyllistä `match`-lausekkeen viimeisenä
haarana, mutta voimme käyttää sitä missä tahansa mallissa, mukaan lukien
funktioiden parametreissa, kuten listauksessa 19-17.

<Listing number="19-17" file-name="src/main.rs" caption="`_`:n käyttö funktioallekirjoituksessa">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-17/src/main.rs}}
```

</Listing>

Tämä koodi jättää kokonaan huomiotta ensimmäisenä argumenttina välitetyn arvon
`3` ja tulostaa `This code only uses the y parameter: 4`.

Useimmissa tapauksissa, kun et enää tarvitse tiettyä funktioparametria,
muuttaisit allekirjoituksen niin, ettei se sisällä käyttämätöntä parametria.
Funktioparametrin huomiotta jättäminen voi olla erityisen hyödyllistä tapauksissa,
joissa esimerkiksi toteutat traitia, jolloin tarvitset tietyn tyyppiallekirjoituksen,
mutta toteutuksesi funktion runko ei tarvitse yhtä parametreista. Näin vältät
kääntäjän varoituksen käyttämättömistä funktioparametreista, jonka saisit, jos
käyttäisit nimeä sen sijaan.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-parts-of-a-value-with-a-nested-_"></a>

#### Arvon osat sisäkkäisellä `_`:llä

Voimme myös käyttää `_`:tä toisen mallin sisällä jättääksemme huomiotta vain
osan arvosta, esimerkiksi kun haluamme testata vain osan arvosta mutta emme
tarvitse muita osia vastaavassa koodissa, jonka haluamme suorittaa. Listaus
19-18 näyttää koodin, joka vastaa asetuksen arvon hallinnasta. Liiketoimintavaatimus
on, että käyttäjä ei saa ylikirjoittaa olemassa olevaa asetuksen mukautusta,
mutta voi poistaa asetuksen ja antaa sille arvon, jos se on tällä hetkellä
asettamaton.

<Listing number="19-18" caption="Alaviivan käyttö malleissa, jotka vastaavat `Some`-variantteja, kun emme tarvitse `Some`:n sisällä olevaa arvoa">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-18/src/main.rs:here}}
```

</Listing>

Tämä koodi tulostaa `Can't overwrite an existing customized value` ja sitten
`setting is Some(5)`. Ensimmäisessä match-haarassa emme tarvitse vastata tai
käyttää kummankaan `Some`-variantin sisällä olevia arvoja, mutta meidän täytyy
testata tapaus, jossa sekä `setting_value` että `new_setting_value` ovat
`Some`-variantteja. Siinä tapauksessa tulostamme syyn, miksi `setting_value`:a
ei muuteta, eikä sitä muuteta.

Kaikissa muissa tapauksissa (jos jompikumpi `setting_value`:sta tai
`new_setting_value`:sta on `None`), jotka toisen haaran `_`-malli ilmaisee,
haluamme sallia `new_setting_value`:n tulla `setting_value`:ksi.

Voimme myös käyttää alaviivoja useissa paikoissa yhdessä mallissa jättääksemme
huomiotta tiettyjä arvoja. Listaus 19-19 näyttää esimerkin toisen ja neljännen
arvon huomiotta jättämisestä viiden alkion tuplesta.

<Listing number="19-19" caption="Useiden tuple-osien huomiotta jättäminen">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-19/src/main.rs:here}}
```

</Listing>

Tämä koodi tulostaa `Some numbers: 2, 8, 32`, ja arvot `4` ja `16` jätetään
huomiotta.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-an-unused-variable-by-starting-its-name-with-_"></a>

#### Käyttämätön muuttuja aloittamalla sen nimi alaviivalla

Jos luot muuttujan mutta et käytä sitä missään, Rust antaa yleensä varoituksen,
koska käyttämätön muuttuja voi olla bugi. Joskus on kuitenkin hyödyllistä pystyä
luomaan muuttuja, jota et vielä käytä, esimerkiksi prototyyppiessasi tai
aloittaessasi projektia. Tässä tilanteessa voit kertoa Rustille, ettei sen
tarvitse varoittaa käyttämättömästä muuttujasta aloittamalla muuttujan nimen
alaviivalla. Listauksessa 19-20 luomme kaksi käyttämätöntä muuttujaa, mutta
kun käännämme tämän koodin, meidän pitäisi saada varoitus vain yhdestä niistä.

<Listing number="19-20" file-name="src/main.rs" caption="Muuttujan nimen aloittaminen alaviivalla käyttämättömän muuttujan varoituksen välttämiseksi">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-20/src/main.rs}}
```

</Listing>

Tässä saamme varoituksen siitä, ettei muuttujaa `y` käytetä, mutta emme saa
varoitusta siitä, ettei `_x`:ää käytetä.

Huomaa, että pelkän `_`:n käytön ja alaviivalla alkavan nimen käytön välillä on
hienovarainen ero. Syntaksi `_x` sitoo silti arvon muuttujaan, kun taas `_` ei
sido lainkaan. Osoittaaksemme tapauksen, jossa tämä ero on tärkeä, listaus 19-21
antaa meille virheen.

<Listing number="19-21" caption="Alaviivalla alkava käyttämätön muuttuja sitoo silti arvon, mikä saattaa ottaa arvon omistajuuden">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-21/src/main.rs:here}}
```

</Listing>

Saamme virheen, koska `s`-arvo siirretään silti `_s`:ään, mikä estää meitä
käyttämästä `s`:ää uudelleen. Pelkän alaviivan käyttö ei kuitenkaan koskaan sido
arvoon. Listaus 19-22 kääntyy ilman virheitä, koska `s`:ää ei siirretä `_`:ään.

<Listing number="19-22" caption="Alaviivan käyttö ei sido arvoa">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-22/src/main.rs:here}}
```

</Listing>

Tämä koodi toimii hyvin, koska emme koskaan sido `s`:ää mihinkään; sitä ei siirretä.

<a id="ignoring-remaining-parts-of-a-value-with-"></a>

#### Arvon jäljellä olevat osat `..`-syntaksilla

Arvoilla, joilla on monta osaa, voimme käyttää `..`-syntaksia käyttääksemme
tiettyjä osia ja jättääksemme loput huomiotta, välttäen tarpeen listata
alaviivoja jokaiselle huomiotta jätetylle arvolle. `..`-malli jättää huomiotta
kaikki arvon osat, joita emme ole eksplisiittisesti vastanneet mallin lopussa.
Listauksessa 19-23 meillä on `Point`-rakenne, joka sisältää koordinaatin
kolmiulotteisessa avaruudessa. `match`-lausekkeessa haluamme käsitellä vain
`x`-koordinaattia ja jättää huomiotta `y`- ja `z`-kenttien arvot.

<Listing number="19-23" caption="Kaikkien `Point`-rakenteen kenttien huomiotta jättäminen paitsi `x` käyttämällä `..`-syntaksia">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-23/src/main.rs:here}}
```

</Listing>

Listaamme `x`-arvon ja sisällytämme sitten vain `..`-mallin. Tämä on nopeampaa
kuin joutua listaamaan `y: _` ja `z: _`, varsinkin kun työskentelemme rakenteiden
kanssa, joilla on paljon kenttiä tilanteissa, joissa vain yksi tai kaksi kenttää
on relevantteja.

Syntaksi `..` laajenee niin moneen arvoon kuin tarvitaan. Listaus 19-24 näyttää,
miten käyttää `..`-syntaksia tuplen kanssa.

<Listing number="19-24" file-name="src/main.rs" caption="Vain ensimmäisen ja viimeisen arvon vastaaminen tuplesta ja kaikkien muiden arvojen huomiotta jättäminen">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-24/src/main.rs}}
```

</Listing>

Tässä koodissa ensimmäinen ja viimeinen arvo vastataan `first`:llä ja `last`:lla.
`..` vastaa ja jättää huomiotta kaiken keskeltä.

`..`-syntaksin käytön täytyy kuitenkin olla yksiselitteistä. Jos on epäselvää,
mitkä arvot on tarkoitettu vastattaviksi ja mitkä jätettäväksi huomiotta, Rust
antaa virheen. Listaus 19-25 näyttää esimerkin `..`-syntaksin epäselvästä
käytöstä, joten se ei käänny.

<Listing number="19-25" file-name="src/main.rs" caption="Yritys käyttää `..`-syntaksia epäselvästi">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-25/src/main.rs}}
```

</Listing>

Kun käännämme tämän esimerkin, saamme tämän virheen:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-25/output.txt}}
```

Rustille on mahdotonta määrittää, kuinka monta arvoa tuplesta jätetään huomiotta
ennen kuin arvo vastataan `second`:lla ja kuinka monta arvoa jätetään huomiotta
sen jälkeen. Tämä koodi voisi tarkoittaa, että haluamme jättää huomiotta `2`:n,
sitoa `second`:n arvoon `4` ja sitten jättää huomiotta `8`:n, `16`:n ja `32`:n;
tai että haluamme jättää huomiotta `2`:n ja `4`:n, sitoa `second`:n arvoon `8`:n
ja sitten jättää huomiotta `16`:n ja `32`:n; ja niin edelleen. Muuttujan nimi
`second` ei tarkoita Rustille mitään erityistä, joten saamme kääntäjävirheen,
koska `..`-syntaksin käyttö kahdessa paikassa näin on epäselvää.

<!-- Old headings. Do not remove or links may break. -->

<a id="extra-conditionals-with-match-guards"></a>

### Lisäehtoja match-ehtojen avulla

_Match-ehto_ on lisä-`if`-ehto, joka määritellään mallin jälkeen `match`-haarassa
ja jonka täytyy myös täyttyä, jotta haara valitaan. Match-ehdot ovat hyödyllisiä
ilmaisemaan monimutkaisempia ideoita kuin pelkkä malli sallii. Huomaa kuitenkin,
että ne ovat saatavilla vain `match`-lausekkeissa, eivät `if let`- tai
`while let` -lausekkeissa.

Ehto voi käyttää mallissa luotuja muuttujia. Listaus 19-26 näyttää `match`-lausekkeen,
jossa ensimmäisellä haaralla on malli `Some(x)` ja match-ehto `if x % 2 == 0`
(joka on tosi, jos luku on parillinen).

<Listing number="19-26" caption="Match-ehdon lisääminen malliin">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-26/src/main.rs:here}}
```

</Listing>

Tämä esimerkki tulostaa `The number 4 is even`. Kun `num` verrataan ensimmäisen
haaran malliin, se vastaa, koska `Some(4)` vastaa `Some(x)`:n. Sitten match-ehto
tarkistaa, onko `x`:n jakojäännös kahdella jaolla `0`, ja koska se on, ensimmäinen
haara valitaan.

Jos `num` olisi ollut `Some(5)` sen sijaan, ensimmäisen haaran match-ehto olisi
ollut epätosi, koska 5:n jakojäännös kahdella on `1`, mikä ei ole yhtä suuri
kuin `0`. Rust siirtyisi sitten toiseen haaraan, joka vastaisi, koska toisella
haaralla ei ole match-ehtoa ja se siksi vastaa minkä tahansa `Some`-variantin.

Ehtoa `if x % 2 == 0` ei voi ilmaista mallissa, joten match-ehto antaa meille
mahdollisuuden ilmaista tämän logiikan. Tämän lisäilmaisuvoiman haittapuoli on,
että kääntäjä ei yritä tarkistaa tyhjentävyyttä, kun match-ehtolausekkeita on
mukana.

Käsiteltäessä listaus 19-11 mainitsimme, että voisimme käyttää match-ehtoja
ratkaistaksemme mallien varjostusongelmamme. Muista, että loimme uuden muuttujan
`match`-lausekkeen malliin sen sijaan, että olisimme käyttäneet `match`-lausekkeen
ulkopuolista muuttujaa. Tuo uusi muuttuja tarkoitti, ettei voitu testata ulomman
muuttujan arvoa vastaan. Listaus 19-27 näyttää, miten voimme käyttää match-ehtoa
korjataksemme tämän ongelman.

<Listing number="19-27" file-name="src/main.rs" caption="Match-ehdon käyttö ulomman muuttujan yhtäsuuruuden testaamiseen">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-27/src/main.rs}}
```

</Listing>

Tämä koodi tulostaa nyt `Default case, x = Some(5)`. Toisen match-haaran malli
ei esittele uutta `y`-muuttujaa, joka varjostaisi ulomman `y`:n, mikä tarkoittaa,
että voimme käyttää ulompaa `y`:tä match-ehdossa. Sen sijaan, että määrittelisimme
mallin `Some(y)`:ksi, mikä olisi varjostanut ulomman `y`:n, määrittelemme mallin
`Some(n)`:ksi. Tämä luo uuden `n`-muuttujan, joka ei varjosta mitään, koska
`n`-muuttujaa ei ole `match`-lausekkeen ulkopuolella.

Match-ehto `if n == y` ei ole malli eikä siksi esittele uusia muuttujia. Tämä
`y` _on_ ulompi `y` eikä uusi `y`, joka varjostaisi sen, ja voimme etsiä arvoa,
jolla on sama arvo kuin ulommalla `y`:llä vertaamalla `n`:tä `y`:hyn.

Voit myös käyttää _tai_-operaattoria `|`-merkintää match-ehdossa määrittääksesi
useita malleja; match-ehtoehto koskee kaikkia malleja. Listaus 19-28 näyttää
prioriteetin, kun yhdistetään `|`-operaattoria käyttävä malli match-ehtoon.
Tämän esimerkin tärkeä osa on, että `if y` match-ehto koskee `4`:ää, `5`:tä
_ja_ `6`:ta, vaikka saattaisi näyttää siltä, että `if y` koskee vain `6`:ta.

<Listing number="19-28" caption="Useiden mallien yhdistäminen match-ehtoon">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-28/src/main.rs:here}}
```

</Listing>

Match-ehto sanoo, että haara vastaa vain, jos `x`:n arvo on yhtä suuri kuin `4`,
`5` tai `6` _ja_ jos `y` on `true`. Kun tämä koodi suoritetaan, ensimmäisen
haaran malli vastaa, koska `x` on `4`, mutta match-ehto `if y` on epätosi, joten
ensimmäistä haaraa ei valita. Koodi siirtyy toiseen haaraan, joka vastaa, ja
tämä ohjelma tulostaa `no`. Syy on, että `if`-ehto koskee koko mallia
`4 | 5 | 6`, ei vain viimeistä arvoa `6`. Toisin sanoen match-ehdon prioriteetti
malliin nähden käyttäytyy näin:

```text
(4 | 5 | 6) if y => ...
```

eikä näin:

```text
4 | 5 | (6 if y) => ...
```

Kun koodi on suoritettu, prioriteetin käyttäytyminen on ilmeistä: jos match-ehto
koskisi vain viimeistä arvoa `|`-operaattorilla määritellyssä arvolistassa,
haara olisi vastannut ja ohjelma olisi tulostanut `yes`.

<!-- Old headings. Do not remove or links may break. -->

<a id="-bindings"></a>

### `@`-sidonnat

_At_-operaattori `@` antaa meidän luoda muuttujan, joka pitää arvoa samalla kun
testaamme arvoa mallin vastaamista varten. Listauksessa 19-29 haluamme testata,
että `Message::Hello`-viestin `id`-kenttä on alueella `3..=7`. Haluamme myös
sitoa arvon muuttujaan `id`, jotta voimme käyttää sitä haaraan liittyvässä
koodissa.

<Listing number="19-29" caption="`@`:n käyttö arvon sitomiseen mallissa samalla kun sitä testataan">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-29/src/main.rs:here}}
```

</Listing>

Tämä esimerkki tulostaa `Found an id in range: 5`. Määrittämällä `id @` ennen
aluetta `3..=7` kaappaamme minkä tahansa arvon, joka vastasi aluetta, muuttujaan
nimeltä `id` samalla kun testaamme, että arvo vastasi aluemallia.

Toisella haaralla, jossa mallissa on vain alue määriteltynä, haaraan liittyvässä
koodissa ei ole muuttujaa, joka sisältäisi `id`-kentän todellisen arvon.
`id`-kentän arvo olisi voinut olla `10`, `11` tai `12`, mutta kyseiseen malliin
liittyvä koodi ei tiedä, kumpi se on. Mallikoodi ei voi käyttää `id`-kentän
arvoa, koska emme ole tallentaneet `id`-arvoa muuttujaan.

Viimeisellä haaralla, jossa olemme määritelleet muuttujan ilman aluetta, meillä
on arvo käytettävissä haaran koodissa muuttujassa nimeltä `id`. Syy on, että
olemme käyttäneet rakenteen kentän oikotiesyntaksia. Mutta emme ole soveltaneet
mitään testiä `id`-kentän arvolle tässä haarassa, kuten teimme kahdella
ensimmäisellä haaralla: mikä tahansa arvo vastaisi tätä mallia.

`@`-operaattorin avulla voimme testata arvoa ja tallentaa sen muuttujaan yhdessä
mallissa.

## Yhteenveto

Rustin mallit ovat hyvin hyödyllisiä erilaisten datatyyppien erottelussa. Kun
niitä käytetään `match`-lausekkeissa, Rust varmistaa, että mallisi kattavat
jokaisen mahdollisen arvon, tai ohjelmasi ei käänny. Mallit `let`-lausekkeissa
ja funktioiden parametreissa tekevät näistä rakenteista hyödyllisempiä
mahdollistamalla arvojen purkamisen pienempiin osiin ja näiden osien osoittamisen
muuttujiin. Voimme luoda yksinkertaisia tai monimutkaisia malleja tarpeidemme
mukaan.

Seuraavaksi, kirjan toiseksi viimeisessä luvussa, tarkastelemme Rustin eri
ominaisuuksien edistyneitä puolia.
