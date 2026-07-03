## Kuvioiden syntaksi

Tässä osiossa kokoamme yhteen kaiken kuvioissa sallitun syntaksin ja käsittelemme, miksi ja milloin saatat haluta käyttää kutakin.

### Literaaleihin matchaaminen

Kuten näit luvussa 6, voit matchata kuvioita suoraan literaaleja vasten. Seuraava koodi antaa joitakin esimerkkejä:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-01-literals/src/main.rs:here}}
```

Tämä koodi tulostaa `one`, koska `x`:n arvo on 1. Tämä syntaksi on hyödyllinen, kun haluat koodisi suorittavan toiminnon, jos se saa tietyn konkreettisen arvon.

### Nimetyihin muuttujiin matchaaminen

Nimetyt muuttujat ovat refutoimattomia kuvioita, jotka matchaavat minkä tahansa arvon, ja olemme käyttäneet niitä monesti kirjassa. On kuitenkin yksi monimutkaisuus, kun käytät nimettyjä muuttujia `match`-, `if let`- tai `while let` -lausekkeissa. Koska jokainen näistä lauseketyypeistä aloittaa uuden alueen, lausekkeen sisällä kuviossa määritellyt muuttujat varjostavat samannimiset muuttujat ulkopuolella, kuten kaikki muuttujat. Listauksessa 19-11 määrittelemme muuttujan nimeltä `x` arvolla `Some(5)` ja muuttujan `y` arvolla `10`. Luomme sitten `match`-lausekkeen `x`:n arvolle. Katso match-haarojen kuvioita ja lopun `println!`-kutsua ja yritä arvata, mitä koodi tulostaa, ennen kuin suoritat koodin tai luet eteenpäin.

<Listing number="19-11" file-name="src/main.rs" caption="`match`-lauseke, jonka haara esittelee uuden muuttujan, joka varjostaa olemassa olevan muuttujan `y`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-11/src/main.rs:here}}
```

</Listing>

Käydään läpi, mitä tapahtuu, kun `match`-lauseke suoritetaan. Ensimmäisen match-haaran kuvio ei matchaa `x`:n määriteltyä arvoa, joten koodi jatkuu.

Toisen match-haaran kuvio esittelee uuden muuttujan nimeltä `y`, joka matchaa minkä tahansa arvon `Some`-arvon sisällä. Koska olemme uudella alueella `match`-lausekkeen sisällä, tämä on uusi `y`-muuttuja, ei alussa arvolla 10 määrittelemämme `y`. Tämä uusi `y`-sidonta matchaa minkä tahansa arvon `Some`-arvon sisällä, mikä on se, mitä meillä on `x`:ssä. Siksi tämä uusi `y` sitoutuu `x`:n `Some`-arvon sisäiseen arvoon. Tuo arvo on `5`, joten kyseisen haaran lauseke suoritetaan ja tulostaa `Matched, y = 5`.

Jos `x` olisi ollut `None`-arvo `Some(5)`:n sijaan, ensimmäisten kahden haaran kuviot eivät olisi matchanneet, joten arvo olisi matchannut alaviivaan. Emme esitelleet `x`-muuttujaa alaviiva-haaran kuviossa, joten lausekkeen `x` on edelleen ulompi `x`, jota ei ole varjostettu. Tässä hypoteettisessa tapauksessa `match` tulostaisi `Default case, x = None`.

Kun `match`-lauseke on valmis, sen alue päättyy, ja samoin sisemmän `y`:n alue. Viimeinen `println!` tuottaa `at the end: x = Some(5), y = 10`.

Luodaksemme `match`-lausekkeen, joka vertaa ulompien `x`- ja `y`-muuttujien arvoja sen sijaan, että esittelisimme uuden muuttujan, joka varjostaa olemassa olevan `y`-muuttujan, meidän täytyisi käyttää match-vartijaa. Puhumme match-vartijoista myöhemmin [”Lisäehtoja match-vartijoiden avulla”](#extra-conditionals-with-match-guards)<!-- ignore --> -osiossa.

### Useita kuvioita

Voit matchata useita kuvioita käyttämällä `|`-syntaksia, joka on kuvioiden _tai_-operaattori. Esimerkiksi seuraavassa koodissa matchaamme `x`:n arvoa match-haaroihin, joista ensimmäisessä on _tai_-vaihtoehto, mikä tarkoittaa, että jos `x`:n arvo matchaa kumman tahansa arvon kyseisessä haarassa, kyseisen haaran koodi suoritetaan:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-02-multiple-patterns/src/main.rs:here}}
```

Tämä koodi tulostaa `one or two`.

### Arvoalueisiin matchaaminen `..=`-syntaksilla

`..=`-syntaksi antaa meidän matchata sisältävään arvoalueeseen. Seuraavassa koodissa, kun kuvio matchaa minkä tahansa annetun alueen arvoista, kyseinen haara suoritetaan:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-03-ranges/src/main.rs:here}}
```

Jos `x` on 1, 2, 3, 4 tai 5, ensimmäinen haara matchaa. Tämä syntaksi on kätevämpi useille match-arvoille kuin saman idean ilmaiseminen `|`-operaattorilla; jos käyttäisimme `|`, meidän pitäisi määritellä `1 | 2 | 3 | 4 | 5`. Alueen määrittely on paljon lyhyempää, varsinkin jos haluamme matchata esimerkiksi minkä tahansa luvun väliltä 1–1000!

Kääntäjä tarkistaa käännösaikana, ettei alue ole tyhjä, ja koska ainoat tyypit, joille Rust voi kertoa, onko alue tyhjä vai ei, ovat `char` ja numeeriset arvot, alueet ovat sallittuja vain numeerisille tai `char`-arvoille.

Tässä on esimerkki `char`-arvoalueiden käytöstä:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-04-ranges-of-char/src/main.rs:here}}
```

Rust voi kertoa, että `'c'` on ensimmäisen kuvion alueella, ja tulostaa `early ASCII letter`.

### Purkaminen arvojen erotteluun

Voimme myös käyttää kuvioita purkaaksemme rakenteita, enumeja ja tupleja käyttääksemme näiden arvojen eri osia. Käydään läpi jokainen arvotyyppi.

#### Rakenteiden purkaminen

Listausta 19-12 näyttää `Point`-rakenteen, jossa on kentät `x` ja `y`, jotka voimme purkaa erilleen kuviolla `let`-lausekkeessa.

<Listing number="19-12" file-name="src/main.rs" caption="Rakenteen kenttien purkaminen erillisiksi muuttujiksi">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-12/src/main.rs}}
```

</Listing>

Tämä koodi luo muuttujat `a` ja `b`, jotka matchaavat `p`-rakenteen kenttien `x` ja `y` arvot. Tämä esimerkki osoittaa, etteivät kuvion muuttujien nimet tarvitse vastata rakenteen kenttien nimiä. On kuitenkin yleistä matchata muuttujien nimet kenttien nimiin, jotta on helpompi muistaa, mistä kentistä muuttujat tulivat. Tämän yleisen käytännön vuoksi ja koska `let Point { x: x, y: y } = p;` sisältää paljon toistoa, Rustissa on oikotie rakenteen kenttiin matchaaville kuvioille: sinun tarvitsee vain listata rakenteen kentän nimi, ja kuviosta luodut muuttujat saavat samat nimet. Listausta 19-13 käyttäytyy samalla tavalla kuin listauksen 19-12 koodi, mutta `let`-kuviossa luodut muuttujat ovat `x` ja `y` `a`:n ja `b`:n sijaan.

<Listing number="19-13" file-name="src/main.rs" caption="Rakenteen kenttien purkaminen rakenteen kenttien oikotiellä">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-13/src/main.rs}}
```

</Listing>

Tämä koodi luo muuttujat `x` ja `y`, jotka matchaavat `p`-muuttujan kentät `x` ja `y`. Lopputuloksena muuttujat `x` ja `y` sisältävät arvot `p`-rakenteesta.

Voimme myös purkaa literaaliarvoja osana rakenteen kuviota sen sijaan, että loisimme muuttujia kaikille kentille. Näin voimme testata joitakin kenttiä tiettyjä arvoja vasten samalla kun luomme muuttujia purkaaksemme muut kentät.

Listauksessa 19-14 meillä on `match`-lauseke, joka jakaa `Point`-arvot kolmeen tapaukseen: pisteet, jotka ovat suoraan `x`-akselilla (tosi kun `y = 0`), `y`-akselilla (`x = 0`) tai kummallakaan.

<Listing number="19-14" file-name="src/main.rs" caption="Purkaminen ja literaaliarvojen matchaaminen yhdessä kuviossa">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-14/src/main.rs:here}}
```

</Listing>

Ensimmäinen haara matchaa minkä tahansa pisteen, joka on `x`-akselilla määrittämällä, että `y`-kenttä matchaa, jos sen arvo matchaa literaaliarvoa `0`. Kuvio luo silti `x`-muuttujan, jota voimme käyttää tämän haaran koodissa.

Vastaavasti toinen haara matchaa minkä tahansa pisteen `y`-akselilla määrittämällä, että `x`-kenttä matchaa, jos sen arvo on `0`, ja luo `y`-muuttujan `y`-kentän arvolle. Kolmas haara ei määrittele literaaleja, joten se matchaa minkä tahansa muun `Point`-arvon ja luo muuttujat sekä `x`- että `y`-kentille.

Tässä esimerkissä arvo `p` matchaa toisen haaran, koska `x` sisältää arvon 0, joten tämä koodi tulostaa `On the y axis at 7`.

Muista, että `match`-lauseke lopettaa haarojen tarkistamisen, kun se on löytänyt ensimmäisen matchaavan kuvion, joten vaikka `Point { x: 0, y: 0}` olisi sekä `x`- että `y`-akselilla, tämä koodi tulostaisi vain `On the x axis at 0`.

#### Enumien purkaminen

Olemme purkaneet enumeja tässä kirjassa (esimerkiksi listaus 6-5 luvussa 6), mutta emme ole vielä eksplisiittisesti käsitelleet, että enumin purkamiseen käytettävä kuvio vastaa enumiin tallennetun datan määrittelytapaa. Esimerkkinä listauksessa 19-15 käytämme `Message`-enumia listauksesta 6-2 ja kirjoitamme `match`-lausekkeen kuvioilla, jotka purkavat jokaisen sisäisen arvon.

<Listing number="19-15" file-name="src/main.rs" caption="Eri tyyppisiä arvoja sisältävien enum-varianttien purkaminen">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-15/src/main.rs}}
```

</Listing>

Tämä koodi tulostaa `Change the color to red 0, green 160, and blue 255`. Kokeile muuttaa `msg`:n arvoa nähdäksesi muiden haarojen koodin suorituksen.

Enum-varianteille, joilla ei ole dataa, kuten `Message::Quit`, emme voi purkaa arvoa enempää. Voimme vain matchata literaaliarvoa `Message::Quit`, eikä kyseisessä kuviossa ole muuttujia.

Rakenteen kaltaisille enum-varianteille, kuten `Message::Move`, voimme käyttää rakenteisiin matchaamiseen samankaltaista kuviota. Variantin nimen jälkeen laitamme aaltosulkeet ja listamme kentät muuttujilla, jotta voimme purkaa osat käytettäväksi tämän haaran koodissa. Tässä käytämme oikotietä kuten listauksessa 19-13.

Tuple-tyyppisille enum-varianteille, kuten `Message::Write`, joka sisältää tuplen yhdellä elementillä, ja `Message::ChangeColor`, joka sisältää tuplen kolmella elementillä, kuvio on samankaltainen kuin tupleihin matchaamiseen käytettävä kuvio. Kuvion muuttujien määrän täytyy vastata variantin elementtien määrää, jota matchaamme.

#### Sisäkkäisten rakenteiden ja enumien purkaminen

Tähän asti esimerkkimme ovat matchanneet rakenteita tai enumeja yhdellä tasolla, mutta matchaaminen toimii myös sisäkkäisille alkioille! Voimme esimerkiksi refaktoroida listauksen 19-15 koodin tukemaan RGB- ja HSV-värejä `ChangeColor`-viestissä, kuten listauksessa 19-16.

<Listing number="19-16" caption="Sisäkkäisiin enumeihin matchaaminen">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-16/src/main.rs}}
```

</Listing>

`match`-lausekkeen ensimmäisen haaran kuvio matchaa `Message::ChangeColor`-enum-variantin, joka sisältää `Color::Rgb`-variantin; kuvio sitoutuu sitten kolmeen sisäiseen `i32`-arvoon. Toisen haaran kuvio matchaa myös `Message::ChangeColor`-enum-variantin, mutta sisäinen enum matchaa `Color::Hsv`:n. Voimme määritellä nämä monimutkaiset ehdot yhdessä `match`-lausekkeessa, vaikka mukana on kaksi enumia.

#### Rakenteiden ja tuplejen purkaminen

Voimme sekoittaa, matchata ja sisäkkäistää purkukuvioita vielä monimutkaisemmilla tavoilla. Seuraava esimerkki näyttää monimutkaisen purkamisen, jossa sisäkkäistämme rakenteita ja tupleja tuplen sisään ja puramme kaikki primitiiviarvot:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-05-destructuring-structs-and-tuples/src/main.rs:here}}
```

Tämä koodi antaa meidän purkaa monimutkaiset tyypit osiinsa, jotta voimme käyttää kiinnostavia arvoja erikseen.

Purkaminen kuvioilla on kätevä tapa käyttää arvojen osia, kuten kunkin rakenteen kentän arvoa, erillään toisistaan.

### Arvojen huomiotta jättäminen kuviossa

Olet nähnyt, että on joskus hyödyllistä jättää arvoja huomiotta kuviossa, kuten `match`-lausekkeen viimeisessä haarassa, saadaksesi catch-all-haaran, joka ei varsinaisesti tee mitään mutta kattaa kaikki jäljellä olevat mahdolliset arvot. On muutamia tapoja jättää kokonaisia arvoja tai arvojen osia huomiotta kuviossa: käyttämällä `_`-kuviota (jonka olet nähnyt), käyttämällä `_`-kuviota toisen kuvion sisällä, käyttämällä alaviivalla alkavaa nimeä tai käyttämällä `..`-syntaksia jättääksemme huomiotta arvon jäljellä olevat osat. Tutkitaan, miten ja miksi käyttää kutakin näistä kuvioista.

#### Kokonaisen arvon huomiotta jättäminen `_`:llä

Olemme käyttäneet alaviivaa jokerikuviona, joka matchaa minkä tahansa arvon mutta ei sido arvoon. Tämä on erityisen hyödyllistä `match`-lausekkeen viimeisenä haarana, mutta voimme käyttää sitä missä tahansa kuviossa, mukaan lukien funktioiden parametreissa, kuten listauksessa 19-17.

<Listing number="19-17" file-name="src/main.rs" caption="`_`:n käyttö funktioallekirjoituksessa">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-17/src/main.rs}}
```

</Listing>

Tämä koodi jättää kokonaan huomiotta ensimmäisenä argumenttina välitetyn arvon `3` ja tulostaa `This code only uses the y parameter: 4`.

Useimmissa tapauksissa, kun et enää tarvitse tiettyä funktioparametria, muuttaisit allekirjoituksen niin, ettei se sisällä käyttämätöntä parametria. Funktioparametrin huomiotta jättäminen voi olla erityisen hyödyllistä tapauksissa, joissa esimerkiksi toteutat traitia, jolloin tarvitset tietyn tyyppiallekirjoituksen, mutta toteutuksesi funktion runko ei tarvitse yhtä parametreista. Näin vältät kääntäjän varoituksen käyttämättömistä funktioparametreista, jonka saisit, jos käyttäisit nimeä sen sijaan.

#### Arvon osien huomiotta jättäminen sisäkkäisellä `_`:llä

Voimme myös käyttää `_`:tä toisen kuvion sisällä jättääksemme huomiotta vain osan arvosta, esimerkiksi kun haluamme testata vain osan arvosta mutta emme tarvitse muita osia vastaavassa koodissa, jonka haluamme suorittaa. Listausta 19-18 näyttää koodin, joka vastaa asetuksen arvon hallinnasta. Liiketoimintavaatimus on, että käyttäjä ei saa ylikirjoittaa olemassa olevaa asetuksen mukautusta, mutta voi poistaa asetuksen ja antaa sille arvon, jos se on tällä hetkellä asettamaton.

<Listing number="19-18" caption="Alaviivan käyttö kuvioissa, jotka matchaavat `Some`-variantteja, kun emme tarvitse `Some`:n sisällä olevaa arvoa">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-18/src/main.rs:here}}
```

</Listing>

Tämä koodi tulostaa `Can't overwrite an existing customized value` ja sitten `setting is Some(5)`. Ensimmäisessä match-haarassa emme tarvitse matchata tai käyttää kummankaan `Some`-variantin sisällä olevia arvoja, mutta meidän täytyy testata tapaus, jossa sekä `setting_value` että `new_setting_value` ovat `Some`-variantteja. Siinä tapauksessa tulostamme syyn, miksi `setting_value`:a ei muuteta, eikä sitä muuteta.

Kaikissa muissa tapauksissa (jos jompikumpi `setting_value`:sta tai `new_setting_value`:sta on `None`), jotka toisen haaran `_`-kuvio ilmaisee, haluamme sallia `new_setting_value`:n tulla `setting_value`:ksi.

Voimme myös käyttää alaviivoja useissa paikoissa yhdessä kuviossa jättääksemme huomiotta tiettyjä arvoja. Listausta 19-19 näyttää esimerkin toisen ja neljännen arvon huomiotta jättämisestä viiden alkion tuplesta.

<Listing number="19-19" caption="Useiden tuple-osien huomiotta jättäminen">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-19/src/main.rs:here}}
```

</Listing>

Tämä koodi tulostaa `Some numbers: 2, 8, 32`, ja arvot 4 ja 16 jätetään huomiotta.

#### Käyttämättömän muuttujan huomiotta jättäminen aloittamalla sen nimi alaviivalla

Jos luot muuttujan mutta et käytä sitä missään, Rust antaa yleensä varoituksen, koska käyttämätön muuttuja voi olla bugi. Joskus on kuitenkin hyödyllistä pystyä luomaan muuttuja, jota et vielä käytä, esimerkiksi prototyyppiessasi tai aloittaessasi projektia. Tässä tilanteessa voit kertoa Rustille, ettei sen tarvitse varoittaa käyttämättömästä muuttujasta aloittamalla muuttujan nimen alaviivalla. Listauksessa 19-20 luomme kaksi käyttämätöntä muuttujaa, mutta kun käännämme tämän koodin, meidän pitäisi saada varoitus vain yhdestä niistä.

<Listing number="19-20" file-name="src/main.rs" caption="Muuttujan nimen aloittaminen alaviivalla käyttämättömän muuttujan varoituksen välttämiseksi">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-20/src/main.rs}}
```

</Listing>

Tässä saamme varoituksen siitä, ettei muuttujaa `y` käytetä, mutta emme saa varoitusta siitä, ettei `_x`:ää käytetä.

Huomaa, että pelkän `_`:n käytön ja alaviivalla alkavan nimen käytön välillä on hienovarainen ero. Syntaksi `_x` sitoo silti arvon muuttujaan, kun taas `_` ei sido lainkaan. Osoittaaksemme tapauksen, jossa tämä ero on tärkeä, listaus 19-21 antaa meille virheen.

<Listing number="19-21" caption="Alaviivalla alkava käyttämätön muuttuja sitoo silti arvon, mikä saattaa ottaa arvon omistajuuden">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-21/src/main.rs:here}}
```

</Listing>

Saamme virheen, koska `s`-arvo siirretään silti `_s`:ään, mikä estää meitä käyttämästä `s`:ää uudelleen. Pelkän alaviivan käyttö ei kuitenkaan koskaan sido arvoon. Listausta 19-22 kääntyy ilman virheitä, koska `s`:ää ei siirretä `_`:ään.

<Listing number="19-22" caption="Alaviivan käyttö ei sido arvoa">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-22/src/main.rs:here}}
```

</Listing>

Tämä koodi toimii hyvin, koska emme koskaan sido `s`:ää mihinkään; sitä ei siirretä.

#### Arvon jäljellä olevien osien huomiotta jättäminen `..`-syntaksilla

Arvoilla, joilla on monta osaa, voimme käyttää `..`-syntaksia käyttääksemme tiettyjä osia ja jättääksemme loput huomiotta, välttäen tarpeen listata alaviivoja jokaiselle huomiotta jätetylle arvolle. `..`-kuvio jättää huomiotta kaikki arvon osat, joita emme ole eksplisiittisesti matchanneet kuvion lopussa. Listauksessa 19-23 meillä on `Point`-rakenne, joka sisältää koordinaatin kolmiulotteisessa avaruudessa. `match`-lausekkeessa haluamme käsitellä vain `x`-koordinaattia ja jättää huomiotta `y`- ja `z`-kenttien arvot.

<Listing number="19-23" caption="Kaikkien `Point`-rakenteen kenttien huomiotta jättäminen paitsi `x` käyttämällä `..`-syntaksia">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-23/src/main.rs:here}}
```

</Listing>

Listaamme `x`-arvon ja sisällytämme sitten vain `..`-kuvion. Tämä on nopeampaa kuin joutua listaamaan `y: _` ja `z: _`, varsinkin kun työskentelemme rakenteiden kanssa, joilla on paljon kenttiä tilanteissa, joissa vain yksi tai kaksi kenttää on relevantteja.

Syntaksi `..` laajenee niin moneen arvoon kuin tarvitaan. Listausta 19-24 näyttää, miten käyttää `..`-syntaksia tuplen kanssa.

<Listing number="19-24" file-name="src/main.rs" caption="Vain ensimmäisen ja viimeisen arvon matchaaminen tuplesta ja kaikkien muiden arvojen huomiotta jättäminen">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-24/src/main.rs}}
```

</Listing>

Tässä koodissa ensimmäinen ja viimeinen arvo matchataan `first`:llä ja `last`:lla. `..` matchaa ja jättää huomiotta kaiken keskeltä.

`..`-syntaksin käytön täytyy kuitenkin olla yksiselitteistä. Jos on epäselvää, mitkä arvot on tarkoitettu matchattaviksi ja mitkä jätettäväksi huomiotta, Rust antaa virheen. Listausta 19-25 näyttää esimerkin `..`-syntaksin epäselvästä käytöstä, joten se ei käänny.

<Listing number="19-25" file-name="src/main.rs" caption="Yritys käyttää `..`-syntaksia epäselvästi">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-25/src/main.rs}}
```

</Listing>

Kun käännämme tämän esimerkin, saamme tämän virheen:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-25/output.txt}}
```

Rustille on mahdotonta määrittää, kuinka monta arvoa tuplesta jätetään huomiotta ennen kuin arvo matchataan `second`:lla ja kuinka monta arvoa jätetään huomiotta sen jälkeen. Tämä koodi voisi tarkoittaa, että haluamme jättää huomiotta `2`:n, sitoa `second`:n arvoon `4` ja sitten jättää huomiotta `8`:n, `16`:n ja `32`:n; tai että haluamme jättää huomiotta `2`:n ja `4`:n, sitoa `second`:n arvoon `8`:n ja sitten jättää huomiotta `16`:n ja `32`:n; ja niin edelleen. Muuttujan nimi `second` ei tarkoita Rustille mitään erityistä, joten saamme kääntäjävirheen, koska `..`-syntaksin käyttö kahdessa paikassa näin on epäselvää.

### Lisäehtoja match-vartijoiden avulla

_Match-vartija_ on lisä-`if`-ehto, joka määritellään kuvion jälkeen `match`-haarassa ja jonka täytyy myös täyttyä, jotta haara valitaan. Match-vartijat ovat hyödyllisiä ilmaisemaan monimutkaisempia ideoita kuin pelkkä kuvio sallii. Ne ovat saatavilla vain `match`-lausekkeissa, eivät `if let`- tai `while let` -lausekkeissa.

Ehto voi käyttää kuviossa luotuja muuttujia. Listausta 19-26 näyttää `match`-lausekkeen, jossa ensimmäisellä haaralla on kuvio `Some(x)` ja match-vartija `if x % 2 == 0` (joka on tosi, jos luku on parillinen).

<Listing number="19-26" caption="Match-vartijan lisääminen kuvioon">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-26/src/main.rs:here}}
```

</Listing>

Tämä esimerkki tulostaa `The number 4 is even`. Kun `num` verrataan ensimmäisen haaran kuvioon, se matchaa, koska `Some(4)` matchaa `Some(x)`:n. Sitten match-vartija tarkistaa, onko `x`:n jakojäännös kahdella jaolla 0, ja koska se on, ensimmäinen haara valitaan.

Jos `num` olisi ollut `Some(5)` sen sijaan, ensimmäisen haaran match-vartija olisi ollut epätosi, koska 5:n jakojäännös kahdella on 1, mikä ei ole yhtä suuri kuin 0. Rust siirtyisi sitten toiseen haaraan, joka matchaisi, koska toisella haaralla ei ole match-vartijaa ja se siksi matchaa minkä tahansa `Some`-variantin.

Ehtoa `if x % 2 == 0` ei voi ilmaista kuviossa, joten match-vartija antaa meille mahdollisuuden ilmaista tämän logiikan. Tämän lisäilmaisuvoiman haittapuoli on, että kääntäjä ei yritä tarkistaa tyhjentävyyttä, kun match-vartijalausekkeita on mukana.

Listauksessa 19-11 mainitsimme, että voisimme käyttää match-vartijoita ratkaistaksemme kuvioiden varjostusongelmamme. Muista, että loimme uuden muuttujan `match`-lausekkeen kuvioon sen sijaan, että olisimme käyttäneet `match`-lausekkeen ulkopuolista muuttujaa. Tuo uusi muuttuja tarkoitti, ettei voitu testata ulomman muuttujan arvoa vastaan. Listausta 19-27 näyttää, miten voimme käyttää match-vartijaa korjataksemme tämän ongelman.

<Listing number="19-27" file-name="src/main.rs" caption="Match-vartijan käyttö ulomman muuttujan yhtäsuuruuden testaamiseen">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-27/src/main.rs}}
```

</Listing>

Tämä koodi tulostaa nyt `Default case, x = Some(5)`. Toisen match-haaran kuvio ei esittele uutta `y`-muuttujaa, joka varjostaisi ulomman `y`:n, mikä tarkoittaa, että voimme käyttää ulompaa `y`:tä match-vartijassa. Sen sijaan, että määrittelisimme kuvion `Some(y)`:ksi, mikä olisi varjostanut ulomman `y`:n, määrittelemme kuvion `Some(n)`:ksi. Tämä luo uuden `n`-muuttujan, joka ei varjosta mitään, koska `n`-muuttujaa ei ole `match`-lausekkeen ulkopuolella.

Match-vartija `if n == y` ei ole kuvio eikä siksi esittele uusia muuttujia. Tämä `y` _on_ ulompi `y` eikä uusi `y`, joka varjostaisi sen, ja voimme etsiä arvoa, jolla on sama arvo kuin ulommalla `y`:llä vertaamalla `n`:tä `y`:hyn.

Voit myös käyttää _tai_-operaattoria `|`-merkintää match-vartijassa määrittääksesi useita kuvioita; match-vartijaehto koskee kaikkia kuvioita. Listausta 19-28 näyttää prioriteetin, kun yhdistetään `|`-operaattoria käyttävä kuvio match-vartijaan. Tämän esimerkin tärkeä osa on, että `if y` match-vartija koskee `4`:ää, `5`:tä _ja_ `6`:ta, vaikka saattaisi näyttää siltä, että `if y` koskee vain `6`:ta.

<Listing number="19-28" caption="Useiden kuvioiden yhdistäminen match-vartijaan">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-28/src/main.rs:here}}
```

</Listing>

Match-ehto sanoo, että haara matchaa vain, jos `x`:n arvo on yhtä suuri kuin `4`, `5` tai `6` _ja_ jos `y` on `true`. Kun tämä koodi suoritetaan, ensimmäisen haaran kuvio matchaa, koska `x` on `4`, mutta match-vartija `if y` on epätosi, joten ensimmäistä haaraa ei valita. Koodi siirtyy toiseen haaraan, joka matchaa, ja tämä ohjelma tulostaa `no`. Syy on, että `if`-ehto koskee koko kuviota `4 | 5 | 6`, ei vain viimeistä arvoa `6`. Toisin sanoen match-vartijan prioriteetti kuvioon nähden käyttäytyy näin:

```text
(4 | 5 | 6) if y => ...
```

eikä näin:

```text
4 | 5 | (6 if y) => ...
```

Kun koodi on suoritettu, prioriteetin käyttäytyminen on ilmeistä: jos match-vartija koskisi vain viimeistä arvoa `|`-operaattorilla määritellyssä arvolistassa, haara olisi matchannut ja ohjelma olisi tulostanut `yes`.

### `@`-sidonnat

_At_-operaattori `@` antaa meidän luoda muuttujan, joka pitää arvoa samalla kun testaamme arvoa kuvion matchausta varten. Listauksessa 19-29 haluamme testata, että `Message::Hello`-viestin `id`-kenttä on alueella `3..=7`. Haluamme myös sitoa arvon muuttujaan `id_variable`, jotta voimme käyttää sitä haaraan liittyvässä koodissa. Voisimme nimetä tämän muuttujan `id`:ksi, samaksi kuin kenttä, mutta tässä esimerkissä käytämme eri nimeä.

<Listing number="19-29" caption="`@`:n käyttö arvon sitomiseen kuviossa samalla kun sitä testataan">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-29/src/main.rs:here}}
```

</Listing>

Tämä esimerkki tulostaa `Found an id in range: 5`. Määrittämällä `id_variable @` ennen aluetta `3..=7` kaappaamme minkä tahansa arvon, joka matchasi alueen, samalla kun testaamme, että arvo matchasi aluekuvion.

Toisella haaralla, jossa kuviossa on vain alue määriteltynä, haaraan liittyvässä koodissa ei ole muuttujaa, joka sisältäisi `id`-kentän todellisen arvon. `id`-kentän arvo olisi voinut olla 10, 11 tai 12, mutta kyseiseen kuvioon liittyvä koodi ei tiedä, kumpi se on. Kuviokoodi ei voi käyttää `id`-kentän arvoa, koska emme ole tallentaneet `id`-arvoa muuttujaan.

Viimeisellä haaralla, jossa olemme määritelleet muuttujan ilman aluetta, meillä on arvo käytettävissä haaran koodissa muuttujassa nimeltä `id`. Syy on, että olemme käyttäneet rakenteen kentän oikotiesyntaksia. Mutta emme ole soveltaneet mitään testiä `id`-kentän arvolle tässä haarassa, kuten teimme kahdella ensimmäisellä haaralla: mikä tahansa arvo matchaisi tämän kuvion.

`@`-operaattorin avulla voimme testata arvoa ja tallentaa sen muuttujaan yhdessä kuviossa.

## Yhteenveto

Rustin kuviot ovat hyvin hyödyllisiä erilaisten datatyyppien erottelussa. Kun niitä käytetään `match`-lausekkeissa, Rust varmistaa, että kuviosi kattavat jokaisen mahdollisen arvon, tai ohjelmasi ei käänny. Kuviot `let`-lausekkeissa ja funktioiden parametreissa tekevät näistä rakenteista hyödyllisempiä mahdollistamalla arvojen purkamisen pienempiin osiin ja näiden osien osoittamisen muuttujiin. Voimme luoda yksinkertaisia tai monimutkaisia kuvioita tarpeidemme mukaan.

Seuraavaksi, kirjan toiseksi viimeisessä luvussa, tarkastelemme Rustin eri ominaisuuksien edistyneitä puolia.
