## Viittauskiertot voivat vuotaa muistia

Rustin muistiturvallisuustakuut tekevät vaikeaksi, mutta eivät mahdottomaksi, luoda vahingossa muistia, jota ei koskaan siivota (tunnetaan nimellä _memory leak_, muistivuoto). Muistivuotojen täydellinen estäminen ei ole yksi Rustin takuista, mikä tarkoittaa, että muistivuodot ovat muistiturvallisia Rustissa. Näemme, että Rust sallii muistivuodot käyttämällä `Rc<T>`:tä ja `RefCell<T>`:tä: on mahdollista luoda viittauksia, joissa kohteet viittaavat toisiinsa kiertona. Tämä luo muistivuotoja, koska kunkin kierron kohteen viittauslaskuri ei koskaan saavuta arvoa 0, eikä arvoja koskaan pudoteta.

### Viittauskierron luominen

Katsotaan, miten viittauskierto voi syntyä ja miten se estetään, aloittaen `List`-enumin määrittelystä ja `tail`-metodista listauksessa 15-25.

<Listing number="15-25" file-name="src/main.rs" caption="Cons-listan määrittely, joka pitää `RefCell<T>`:tä, jotta voimme muokata sitä, mihin `Cons`-variantti viittaa">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-25/src/main.rs:here}}
```

</Listing>

Käytämme toista variaatiota `List`-määrittelystä listauksesta 15-5. `Cons`-variantin toinen elementti on nyt `RefCell<Rc<List>>`, mikä tarkoittaa, että listauksessa 15-24 tekemämme `i32`-arvon muuttamisen sijaan haluamme muokata `List`-arvoa, johon `Cons`-variantti osoittaa. Lisäämme myös `tail`-metodin, jotta on kätevää käyttää toista kohdetta, jos meillä on `Cons`-variantti.

Listauksessa 15-26 lisäämme `main`-funktion, joka käyttää listauksen 15-25 määrittelyjä. Tämä koodi luo listan `a`:ssa ja listan `b`:ssä, joka osoittaa listaan `a`. Sitten se muokkaa listaa `a`:ssa osoittamaan `b`:hen, luoden viittauskierron. Matkan varrella on `println!`-lauseita, jotka näyttävät viittauslaskurit eri vaiheissa.

<Listing number="15-26" file-name="src/main.rs" caption="Kahden toisiinsa osoittavan `List`-arvon viittauskierron luominen">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-26/src/main.rs:here}}
```

</Listing>

Luomme `Rc<List>`-instanssin, joka pitää `List`-arvoa muuttujassa `a` alku listalla `5, Nil`. Sitten luomme `Rc<List>`-instanssin, joka pitää toista `List`-arvoa muuttujassa `b`, joka sisältää arvon `10` ja osoittaa listaan `a`.

Muokkaamme `a`:ta niin, että se osoittaa `b`:hen `Nil`:n sijaan, luoden kierron. Teemme tämän käyttämällä `tail`-metodia saadaksemme viittauksen `a`:n `RefCell<Rc<List>>`:iin, jonka sijoitamme muuttujaan `link`. Sitten käytämme `borrow_mut`-metodia `RefCell<Rc<List>>`:ssa muuttaaksemme sisällä olevan arvon `Rc<List>`:stä, joka pitää `Nil`-arvoa, `b`:n `Rc<List>`:ksi.

Kun ajamme tämän koodin pitäen viimeisen `println!`:n toistaiseksi kommentoituna, saamme tämän tulosteen:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-26/output.txt}}
```

`Rc<List>`-instanssien viittauslaskuri sekä `a`:ssa että `b`:ssä on 2 sen jälkeen, kun muutamme listan `a`:ssa osoittamaan `b`:hen. `main`:in lopussa Rust pudottaa muuttujan `b`, mikä pienentää `b`:n `Rc<List>`-instanssin viittauslaskuria 2:sta 1:een. `Rc<List>`:n keolla olevaa muistia ei pudoteta tässä vaiheessa, koska sen viittauslaskuri on 1, ei 0. Sitten Rust pudottaa `a`:n, mikä pienentää `a`:n `Rc<List>`-instanssin viittauslaskuria myös 2:sta 1:een. Tämän instanssin muistia ei myöskään voida pudottaa, koska toinen `Rc<List>`-instanssi viittaa siihen edelleen. Listalle varattu muisti jää keräämättä ikuisesti. Visualisoidaksemme tämän viittauskierron olemme luoneet kaavion kuvassa 15-4.

<img alt="A rectangle labeled 'a' that points to a rectangle containing the integer 5. A rectangle labeled 'b' that points to a rectangle containing the integer 10. The rectangle containing 5 points to the rectangle containing 10, and the rectangle containing 10 points back to the rectangle containing 5, creating a cycle." src="img/trpl15-04.svg" class="center" />

<span class="caption">Kuva 15-4: Listojen `a` ja `b` viittauskierto, jotka osoittavat toisiinsa</span>

Jos poistat viimeisen `println!`:n kommentoinnin ja ajat ohjelman, Rust yrittää tulostaa tämän kierron `a`:n osoittaessa `b`:hen, `b`:n osoittaessa `a`:han ja niin edelleen, kunnes pino ylivuotaa.

Verrattuna tosielämän ohjelmaan tämän esimerkin viittauskierron seuraukset eivät ole kovin vakavat: heti viittauskierron luomisen jälkeen ohjelma päättyy. Jos monimutkaisempi ohjelma kuitenkin varaisi paljon muistia kiertoon ja pitäisi sitä kauan, ohjelma käyttäisi enemmän muistia kuin tarvitsisi ja saattaisi ylikuormittaa järjestelmän, jolloin käytettävissä oleva muisti loppuisi.

Viittauskiertojen luominen ei ole helppoa, mutta se ei myöskään ole mahdotonta. Jos sinulla on `RefCell<T>`-arvoja, jotka sisältävät `Rc<T>`-arvoja tai vastaavia sisäisen muuttuvuuden ja viittauslaskennan sisäkkäisiä yhdistelmiä, sinun täytyy varmistaa, ettei kiertoja synny; et voi luottaa Rustiin niiden havaitsemisessa. Viittauskierron luominen olisi ohjelmasi logiikkavirhe, jota sinun tulisi minimoida automatisoiduilla testeillä, koodikatselmoinneilla ja muilla ohjelmistokehityskäytännöillä.

Toinen ratkaisu viittauskiertojen välttämiseksi on tietorakenteiden uudelleenjärjestely niin, että jotkut viittaukset ilmaisevat omistajuutta ja jotkut eivät. Näin voit saada kiertoja, jotka koostuvat osittain omistajuussuhteista ja osittain ei-omistajuussuhteista, ja vain omistajuussuhteet vaikuttavat siihen, voidaanko arvo pudottaa. Listauksessa 15-25 haluamme aina, että `Cons`-variantit omistavat listansa, joten tietorakenteen uudelleenjärjestely ei ole mahdollista. Katsotaan esimerkkiä, jossa käytetään vanhempi- ja lapsisolmuista koostuvia graafeja, nähdäksemme, milloin ei-omistajuussuhteet ovat sopiva tapa estää viittauskiertoja.

<!-- Old headings. Do not remove or links may break. -->

<a id="preventing-reference-cycles-turning-an-rct-into-a-weakt"></a>

### Viittauskiertojen estäminen `Weak<T>`:n avulla

Tähän mennessä olemme osoittaneet, että `Rc::clone`:n kutsuminen kasvattaa `Rc<T>`-instanssin `strong_count`:ia, ja `Rc<T>`-instanssi siivotaan vain, jos sen `strong_count` on 0. Voit myös luoda heikon viittauksen `Rc<T>`-instanssin sisällä olevaan arvoon kutsumalla `Rc::downgrade`:a ja välittämällä viittauksen `Rc<T>`:iin. *Vahvat viittaukset* ovat tapa, jolla voit jakaa `Rc<T>`-instanssin omistajuuden. *Heikot viittaukset* eivät ilmaise omistajuussuhdetta, eikä niiden laskuri vaikuta siihen, milloin `Rc<T>`-instanssi siivotaan. Ne eivät aiheuta viittauskiertoa, koska mikä tahansa kierto, johon liittyy heikkoja viittauksia, katkeaa, kun mukana olevien arvojen vahvan viittauksen laskuri on 0.

Kun kutsut `Rc::downgrade`:a, saat älykkään osoittimen tyypin `Weak<T>`. Sen sijaan, että `Rc::downgrade` kasvattaisi `Rc<T>`-instanssin `strong_count`:ia yhdellä, se kasvattaa `weak_count`:ia yhdellä. `Rc<T>`-tyyppi käyttää `weak_count`:ia seuratakseen, kuinka monta `Weak<T>`-viittausta on olemassa, samoin kuin `strong_count`:ia. Ero on, että `weak_count`:in ei tarvitse olla 0, jotta `Rc<T>`-instanssi siivottaisiin.

Koska arvo, johon `Weak<T>` viittaa, on saatettu pudottaa, sinun täytyy varmistaa, että arvo on edelleen olemassa, ennen kuin teet mitään arvolla, johon `Weak<T>` osoittaa. Tee tämä kutsumalla `upgrade`-metodia `Weak<T>`-instanssilla, joka palauttaa `Option<Rc<T>>`:n. Saat tuloksen `Some`, jos `Rc<T>`-arvoa ei ole vielä pudotettu, ja tuloksen `None`, jos `Rc<T>`-arvo on pudotettu. Koska `upgrade` palauttaa `Option<Rc<T>>`:n, Rust varmistaa, että `Some`- ja `None`-tapaukset käsitellään, eikä virheellistä osoitinta synny.

Esimerkkinä sen sijaan, että käyttäisimme listaa, jonka kohteet tietävät vain seuraavasta kohteesta, luomme puun, jonka kohteet tietävät sekä lapsikohteistaan _että_ vanhemmistaan.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-a-tree-data-structure-a-node-with-child-nodes"></a>

#### Puutietorakenteen luominen

Aloitamme rakentamalla puun, jonka solmut tietävät lapsisolmuistaan. Luomme structin nimeltä `Node`, joka pitää oman `i32`-arvonsa sekä viittauksia lapsisolmujensa `Node`-arvoihin:

<span class="filename">Tiedostonimi: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-27/src/main.rs:here}}
```

Haluamme, että `Node` omistaa lapsensa, ja haluamme jakaa tämän omistajuuden muuttujien kanssa, jotta voimme käyttää jokaista puun `Node`:a suoraan. Tätä varten määrittelemme `Vec<T>`-kohteet tyyppiä `Rc<Node>`. Haluamme myös muokata sitä, mitkä solmut ovat toisen solmun lapsia, joten `children`:issa on `RefCell<T>` `Vec<Rc<Node>>`:n ympärillä.

Seuraavaksi käytämme struct-määrittelyämme ja luomme yhden `Node`-instanssin nimeltä `leaf` arvolla `3` ilman lapsia, ja toisen instanssin nimeltä `branch` arvolla `5` ja `leaf` yhtenä lapsenaan, kuten listauksessa 15-27.

<Listing number="15-27" file-name="src/main.rs" caption="`leaf`-solmun luominen ilman lapsia ja `branch`-solmun luominen, jolla `leaf` on yksi lapsistaan">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-27/src/main.rs:there}}
```

</Listing>

Kloonaamme `Rc<Node>`:n `leaf`:ssa ja tallennamme sen `branch`:iin, mikä tarkoittaa, että `leaf`:n `Node`:lla on nyt kaksi omistajaa: `leaf` ja `branch`. Voimme päästä `leaf`:iin `branch`:in kautta `branch.children`:in avulla, mutta emme voi päästä `branch`:iin `leaf`:stä. Syy on, että `leaf`:llä ei ole viittausta `branch`:iin eikä se tiedä niiden olevan suhteessa toisiinsa. Haluamme `leaf`:n tietävän, että `branch` on sen vanhempi. Teemme sen seuraavaksi.

#### Viittauksen lisääminen lapsesta vanhempaan

Jotta lapsisolmu tietäisi vanhempansa, meidän täytyy lisätä `parent`-kenttä `Node`-structin määrittelyyn. Ongelma on päättää, mikä `parent`:in tyypin pitäisi olla. Tiedämme, ettei se voi sisältää `Rc<T>`:tä, koska se loisi viittauskierron `leaf.parent`:in osoittaessa `branch`:iin ja `branch.children`:in osoittaessa `leaf`:iin, mikä saisi niiden `strong_count`-arvot pysymään ikuisesti muussa kuin nollassa.

Ajatellaan suhteita toisella tavalla: vanhempisolmun pitäisi omistaa lapsensa — jos vanhempisolmu pudotetaan, sen lapsisolmut pitäisi pudottaa myös. Lapsisolmun ei kuitenkaan pitäisi omistaa vanhempaansa: jos pudotamme lapsisolmun, vanhemman pitäisi silti olla olemassa. Tämä on tapaus heikoille viittauksille!

Sen sijaan, että käyttäisimme `Rc<T>`:tä, teemme `parent`:in tyypiksi `Weak<T>`:n, tarkemmin `RefCell<Weak<Node>>`:n. Nyt `Node`-structin määrittely näyttää tältä:

<span class="filename">Tiedostonimi: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-28/src/main.rs:here}}
```

Solmu voi viitata vanhempisolmuunsa, mutta se ei omista vanhempaansa. Listauksessa 15-28 päivitämme `main`:ia käyttämään tätä uutta määrittelyä, jotta `leaf`-solmulla on tapa viitata vanhempaansa, `branch`:iin.

<Listing number="15-28" file-name="src/main.rs" caption="`leaf`-solmu, jolla on heikko viittaus vanhempisolmuunsa, `branch`:iin">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-28/src/main.rs:there}}
```

</Listing>

`leaf`-solmun luominen näyttää samalta kuin listauksessa 15-27, paitsi `parent`-kentän osalta: `leaf`:lla ei ole aluksi vanhempaa, joten luomme uuden tyhjän `Weak<Node>`-viittausinstanssin.

Tässä vaiheessa, kun yritämme saada viittauksen `leaf`:n vanhempaan `upgrade`-metodilla, saamme arvon `None`. Näemme tämän ensimmäisen `println!`-lauseen tulosteesta:

```text
leaf parent = None
```

Kun luomme `branch`-solmun, sillä on myös uusi `Weak<Node>`-viittaus `parent`-kentässä, koska `branch`:lla ei ole vanhempisolmua. Meillä on edelleen `leaf` yhtenä `branch`:in lapsista. Kun meillä on `Node`-instanssi `branch`:issa, voimme muokata `leaf`:ia antamaan sille `Weak<Node>`-viittauksen vanhempaansa. Käytämme `borrow_mut`-metodia `leaf`:n `parent`-kentän `RefCell<Weak<Node>>`:ssa, ja sitten käytämme `Rc::downgrade`-funktiota luodaksemme `Weak<Node>`-viittauksen `branch`:iin `branch`:in `Rc<Node>`:sta.

Kun tulostamme `leaf`:n vanhemman uudelleen, saamme tällä kertaa `Some`-variantin, joka pitää `branch`:ia: nyt `leaf` voi käyttää vanhempaansa! Kun tulostamme `leaf`:n, vältämme myös kierron, joka lopulta päättyi pinon ylivuotoon kuten listauksessa 15-26; `Weak<Node>`-viittaukset tulostetaan muodossa `(Weak)`:

```text
leaf parent = Some(Node { value: 5, parent: RefCell { value: (Weak) },
children: RefCell { value: [Node { value: 3, parent: RefCell { value: (Weak) },
children: RefCell { value: [] } }] } })
```

Loputtoman tulosteen puuttuminen osoittaa, että tämä koodi ei luonut viittauskiertoa. Voimme myös päätellä tämän katsomalla arvoja, jotka saamme kutsumalla `Rc::strong_count`:ia ja `Rc::weak_count`:ia.

#### `strong_count`:in ja `weak_count`:in muutosten visualisointi

Katsotaan, miten `Rc<Node>`-instanssien `strong_count`- ja `weak_count`-arvot muuttuvat luomalla uuden sisäisen näkyvyysalueen ja siirtämällä `branch`:in luonnin kyseiseen näkyvyysalueeseen. Näin voimme nähdä, mitä tapahtuu, kun `branch` luodaan ja sitten pudotetaan poistuessaan näkyvyysalueelta. Muutokset on esitetty listauksessa 15-29.

<Listing number="15-29" file-name="src/main.rs" caption="`branch`:in luominen sisäisessä näkyvyysalueessa ja vahvojen ja heikkojen viittausten lukumäärien tarkastelu">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-29/src/main.rs:here}}
```

</Listing>

Kun `leaf` on luotu, sen `Rc<Node>`:lla on vahva laskuri 1 ja heikko laskuri 0. Sisäisessä näkyvyysalueessa luomme `branch`:in ja yhdistämme sen `leaf`:iin, jolloin kun tulostamme laskurit, `branch`:in `Rc<Node>`:lla on vahva laskuri 1 ja heikko laskuri 1 (`leaf.parent`:in osoittaessa `branch`:iin `Weak<Node>`:lla). Kun tulostamme laskurit `leaf`:ssä, näemme, että sillä on vahva laskuri 2, koska `branch`:illa on nyt klooni `leaf`:n `Rc<Node>`:sta tallennettuna `branch.children`:iin, mutta heikko laskuri on edelleen 0.

Kun sisäinen näkyvyysalue päättyy, `branch` poistuu näkyvyysalueelta ja `Rc<Node>`:n vahva laskuri pienenee 0:aan, joten sen `Node` pudotetaan. Heikko laskuri 1 `leaf.parent`:ista ei vaikuta siihen, pudotetaanko `Node`, joten emme saa muistivuotoja!

Jos yritämme käyttää `leaf`:n vanhempaa näkyvyysalueen päättymisen jälkeen, saamme jälleen `None`:n. Ohjelman lopussa `leaf`:n `Rc<Node>`:lla on vahva laskuri 1 ja heikko laskuri 0, koska muuttuja `leaf` on nyt ainoa viittaus `Rc<Node>`:iin.

Kaikki laskureita ja arvojen pudottamista hallitseva logiikka on sisäänrakennettu `Rc<T>`:ään ja `Weak<T>`:ään sekä niiden `Drop`-traitin toteutuksiin. Määrittämällä, että lapsen ja vanhemman välisen suhteen pitäisi olla `Weak<T>`-viittaus `Node`:n määrittelyssä, voit saada vanhempisolmut osoittamaan lapsisolmuihin ja päinvastoin luomatta viittauskiertoa ja muistivuotoja.

## Yhteenveto

Tässä luvussa käsiteltiin, miten älykkäitä osoittimia käytetään tekemään erilaisia takuita ja kompromisseja verrattuna Rustin oletuksiin tavallisten viittausten kanssa. `Box<T>`-tyypillä on tunnettu koko ja se osoittaa keolle varattuun dataan. `Rc<T>`-tyyppi seuraa viittausten määrää keon datassa, jotta datalla voi olla useita omistajia. `RefCell<T>`-tyyppi sisäisellä muuttuvuudellaan antaa tyypin, jota voimme käyttää, kun tarvitsemme muuttumatonta tyyppiä mutta meidän täytyy muuttaa sen sisäistä arvoa; se myös pakottaa lainausperiaatteet ajonaikana käännösaikaan sijaan.

Käsiteltiin myös `Deref`- ja `Drop`-traitit, jotka mahdollistavat suuren osan älykkäiden osoittimien toiminnallisuudesta. Tutustuimme viittauskiertoihin, jotka voivat aiheuttaa muistivuotoja, ja siihen, miten ne estetään `Weak<T>`:n avulla.

Jos tämä luku herätti kiinnostuksesi ja haluat toteuttaa omat älykkäät osoittimesi, tutustu [„The Rustonomicon”][nomicon]-teokseen saadaksesi lisää hyödyllistä tietoa.

Seuraavaksi käsittelemme rinnakkaisuutta Rustissa. Opit jopa muutamasta uudesta älykkäästä osoittimesta.

[nomicon]: ../nomicon/index.html
