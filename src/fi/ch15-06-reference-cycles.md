## Viittauskiertoja voi aiheuttaa muistivuotoja

Rustin muistiturvallisuustakuut tekevät vaikeaksi, mutta eivät mahdottomaksi, luoda vahingossa muistia, jota ei koskaan siivota (tunnetaan nimellä _muistivuoto_). Muistivuotojen täydellinen estäminen ei ole yksi Rustin takuista, mikä tarkoittaa, että muistivuodot ovat muistiturvallisia Rustissa. Näemme, että Rust sallii muistivuodot käyttämällä `Rc<T>`:tä ja `RefCell<T>`:tä: on mahdollista luoda viittauksia, joissa kohteet viittaavat toisiinsa kiertona. Tämä luo muistivuotoja, koska kunkin kierron kohteen viittauslaskuri ei koskaan saavuta arvoa 0, eikä arvoja koskaan pudoteta.

### Viittauskierron luominen

Katsotaan, miten viittauskierto voi syntyä ja miten se estetään, aloittaen `List`-enumin määrittelystä ja `tail`-metodista Listauksessa 15-25:

<Listing number="15-25" file-name="src/main.rs" caption="Cons-listan määrittely, joka pitää `RefCell<T>`:tä, jotta voimme muokata sitä, mihin `Cons`-variantti viittaa">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-25/src/main.rs}}
```

</Listing>

Käytämme toista variaatiota `List`-määrittelystä Listauksesta 15-5. `Cons`-variantin toinen elementti on nyt `RefCell<Rc<List>>`, mikä tarkoittaa, että sen sijaan, että voisimme muokata `i32`-arvoa kuten Listauksessa 15-24, haluamme muokata `List`-arvoa, johon `Cons`-variantti osoittaa. Lisäämme myös `tail`-metodin, jotta on kätevää päästä toiseen kohteeseen, jos meillä on `Cons`-variantti.

Listauksessa 15-26 lisäämme `main`-funktion, joka käyttää Listauksen 15-25 määrittelyjä. Tämä koodi luo listan muuttujassa `a` ja listan muuttujassa `b`, joka osoittaa listaan `a`:ssa. Sitten se muokkaa listaa `a`:ssa osoittamaan `b`:hen, luoden viittauskierron. Matkan varrella on `println!`-lauseita, jotka näyttävät, mitkä viittauslaskurit ovat eri vaiheissa tässä prosessissa.

<Listing number="15-26" file-name="src/main.rs" caption="Viittauskierron luominen kahdesta `List`-arvosta, jotka osoittavat toisiinsa">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-26/src/main.rs:here}}
```

</Listing>

Luomme `Rc<List>`-instanssin, joka pitää `List`-arvoa muuttujassa `a` alkuperäisellä listalla `5, Nil`. Luomme sitten `Rc<List>`-instanssin, joka pitää toista `List`-arvoa muuttujassa `b`, joka sisältää arvon 10 ja osoittaa listaan `a`:ssa.

Muokkaamme `a`:ta niin, että se osoittaa `b`:hen `Nil`-arvon sijaan, luoden kierron. Teemme tämän käyttämällä `tail`-metodia saadaksemme viittauksen `RefCell<Rc<List>>`-arvoon `a`:ssa, jonka laitamme muuttujaan `link`. Käytämme sitten `borrow_mut`-metodia `RefCell<Rc<List>>`-arvolla muuttaaksemme sisällä olevan arvon `Rc<List>`-arvosta, joka pitää `Nil`-arvoa, `Rc<List>`-arvoksi `b`:ssä.

Kun suoritamme tämän koodin pitäen viimeinen `println!` kommentoituna toistaiseksi, saamme tämän tulosteen:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-26/output.txt}}
```

`Rc<List>`-instanssien viittauslaskurit sekä `a`:ssa että `b`:ssä ovat 2 sen jälkeen, kun muutamme listan `a`:ssa osoittamaan `b`:hen. `main`-funktion lopussa Rust pudottaa muuttujan `b`, mikä vähentää `b`-`Rc<List>`-instanssin viittauslaskuria 2:sta 1:een. `Rc<List>`-instanssin keossa olemaa muistia ei pudoteta tässä vaiheessa, koska sen viittauslaskuri on 1, ei 0. Sitten Rust pudottaa `a`:n, mikä vähentää `a`-`Rc<List>`-instanssin viittauslaskuria myös 2:sta 1:een. Tämän instanssin muistia ei myöskään voida pudottaa, koska toinen `Rc<List>`-instanssi viittaa siihen edelleen. Listalle varattu muisti pysyy keräämättömänä ikuisesti. Visualisoidaksemme tämän viittauskierron, olemme luoneet kaavion Kuvassa 15-4.

<img alt="Reference cycle of lists" src="img/trpl15-04.svg" class="center" />

<span class="caption">Kuva 15-4: Viittauskierto listoista `a` ja `b`, jotka osoittavat toisiinsa</span>

Jos poistat kommentoinnin viimeisestä `println!`-lauseesta ja suoritat ohjelman, Rust yrittää tulostaa tämän kierron `a`:n osoittaessa `b`:hen, joka osoittaa `a`:han, ja niin edelleen, kunnes se ylivuotaa pinon.

Verrattuna tosielämän ohjelmaan, viittauskierron luomisen seuraukset tässä esimerkissä eivät ole kovin vakavat: heti kierron luomisen jälkeen ohjelma päättyy. Jos kuitenkin monimutkaisempi ohjelma varaisi paljon muistia kiertoon ja pitäisi sitä hallussaan pitkään, ohjelma käyttäisi enemmän muistia kuin tarvitsisi ja saattaisi ylikuormittaa järjestelmän, jolloin käytettävissä oleva muisti loppuisi.

Viittauskiertojen luominen ei ole helppoa, mutta se ei ole mahdotonta. Jos sinulla on `RefCell<T>`-arvoja, jotka sisältävät `Rc<T>`-arvoja tai vastaavia sisäkkäisiä yhdistelmiä tyypeistä, joilla on sisäinen mutabiliteetti ja viittauslaskenta, sinun täytyy varmistaa, ettei luoda kiertoja; et voi luottaa Rustin havaitsevan niitä. Viittauskierron luominen olisi looginen virhe ohjelmassasi, jota sinun pitäisi minimoida automatisoituilla testeillä, koodikatselmoinneilla ja muilla ohjelmistokehityskäytännöillä.

Toinen ratkaisu viittauskiertojen välttämiseksi on järjestää tietorakenteet uudelleen niin, että jotkin viittaukset ilmaisevat omistajuutta ja jotkin eivät. Näin voit olla kiertoja, jotka koostuvat joistakin omistussuhteista ja joistakin ei-omistussuhteista, ja vain omistussuhteet vaikuttavat siihen, voidaanko arvo pudottaa. Listauksessa 15-25 haluamme aina, että `Cons`-variantit omistavat listansa, joten tietorakenteen uudelleenjärjestely ei ole mahdollista. Katsotaan esimerkkiä, jossa käytetään graafeja, jotka koostuvat vanhempisolmuista ja lapsisolmuista, nähdäksemme, milloin ei-omistussuhteet ovat sopiva tapa estää viittauskiertoja.

### Viittauskiertojen estäminen: `Rc<T>`:n muuttaminen `Weak<T>`:ksi

Tähän mennessä olemme osoittaneet, että `Rc::clone`-kutsu kasvattaa `Rc<T>`-instanssin `strong_count`-arvoa, ja `Rc<T>`-instanssi siivotaan vain, jos sen `strong_count` on 0. Voit myös luoda _heikon viittauksen_ `Rc<T>`-instanssin sisällä olevaan arvoon kutsumalla `Rc::downgrade` ja välittämällä viittauksen `Rc<T>`-arvoon. _Vahvat viittaukset_ ovat tapa, jolla voit jakaa `Rc<T>`-instanssin omistajuutta. _Heikot viittaukset_ eivät ilmaise omistussuhdetta, eikä niiden laskuri vaikuta siihen, milloin `Rc<T>`-instanssi siivotaan. Ne eivät aiheuta viittauskiertoa, koska mikä tahansa kierto, johon liittyy heikkoja viittauksia, katkeaa, kun mukana olevien arvojen vahvan viittauksen laskuri on 0.

Kun kutsut `Rc::downgrade`, saat älykkään osoittimen tyypillä `Weak<T>`. Sen sijaan, että `Rc::downgrade`-kutsu kasvattaisi `Rc<T>`-instanssin `strong_count`-arvoa yhdellä, se kasvattaa `weak_count`-arvoa yhdellä. `Rc<T>`-tyyppi käyttää `weak_count`-arvoa seuratakseen, kuinka monta `Weak<T>`-viittausta on olemassa, samalla tavalla kuin `strong_count`. Ero on, että `weak_count`-arvon ei tarvitse olla 0, jotta `Rc<T>`-instanssi siivottaisiin.

Koska arvo, johon `Weak<T>` viittaa, on saatettu pudottaa, tehdäksesi mitään `Weak<T>`:n osoittaman arvon kanssa, sinun täytyy varmistaa, että arvo on edelleen olemassa. Tee tämä kutsumalla `upgrade`-metodia `Weak<T>`-instanssilla, joka palauttaa `Option<Rc<T>>`:n. Saat `Some`-tuloksen, jos `Rc<T>`-arvoa ei ole vielä pudotettu, ja `None`-tuloksen, jos `Rc<T>`-arvo on pudotettu. Koska `upgrade` palauttaa `Option<Rc<T>>`:n, Rust varmistaa, että `Some`- ja `None`-tapaukset käsitellään, eikä virheellistä osoitinta ole.

Esimerkkinä sen sijaan, että käyttäisimme listaa, jonka kohteet tietävät vain seuraavasta kohteesta, luomme puun, jonka kohteet tietävät lapsikohteistaan _ja_ vanhemmistaan.

#### Puutietorakenteen luominen: `Node` lapsisolmuineen

Aloittaaksemme rakennamme puun solmuineen, jotka tietävät lapsisolmuistaan. Luomme rakenteen nimeltä `Node`, joka pitää omaa `i32`-arvoaan sekä viittauksia lapsi-`Node`-arvoihinsa:

<span class="filename">Tiedostonimi: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-27/src/main.rs:here}}
```

Haluamme, että `Node` omistaa lapsensa, ja haluamme jakaa tämän omistajuuden muuttujien kanssa, jotta voimme käyttää jokaista `Node`-arvoa puussa suoraan. Tehdäksemme tämän, määrittelemme `Vec<T>`-kohteet olemaan tyyppiä `Rc<Node>`. Haluamme myös muokata, mitkä solmut ovat toisen solmun lapsia, joten meillä on `RefCell<T>` `children`-kentässä `Vec<Rc<Node>>`-arvon ympärillä.

Seuraavaksi käytämme rakennemäärittelyämme ja luomme yhden `Node`-instanssin nimeltä `leaf` arvolla 3 ilman lapsia, ja toisen instanssin nimeltä `branch` arvolla 5 ja `leaf` yhtenä lapsenaan, kuten Listauksessa 15-27 on esitetty:

<Listing number="15-27" file-name="src/main.rs" caption="`leaf`-solmun luominen ilman lapsia ja `branch`-solmun luominen, jolla `leaf` on yksi lapsistaan">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-27/src/main.rs:there}}
```

</Listing>

Kloonaamme `Rc<Node>`-arvon `leaf`:ssa ja tallennamme sen `branch`:iin, mikä tarkoittaa, että `Node`-arvolla `leaf`:ssa on nyt kaksi omistajaa: `leaf` ja `branch`. Voimme päästä `leaf`:iin `branch`:n kautta `branch.children`-kentän avulla, mutta ei ole tapaa päästä `branch`:iin `leaf`:stä. Syy on, että `leaf`:llä ei ole viittausta `branch`:iin, eikä se tiedä, että ne liittyvät toisiinsa. Haluamme, että `leaf` tietää `branch`:n olevan sen vanhempi. Teemme sen seuraavaksi.

#### Viittauksen lisääminen lapsesta vanhempaan

Jotta lapsisolmu tietäisi vanhemmastaan, meidän täytyy lisätä `parent`-kenttä `Node`-rakennemäärittelyymme. Ongelma on päättää, mikä `parent`-kentän tyypin pitäisi olla. Tiedämme, ettei se voi sisältää `Rc<T>`:tä, koska se loisi viittauskierron `leaf.parent`:n osoittaessa `branch`:iin ja `branch.children`:n osoittaessa `leaf`:iin, mikä aiheuttaisi niiden `strong_count`-arvojen olevan ikuisesti eri kuin 0.

Ajatellen suhteita toisella tavalla, vanhempisolmun pitäisi omistaa lapsensa: jos vanhempisolmu pudotetaan, sen lapsisolmut pitäisi pudottaa myös. Lapsen ei kuitenkaan pitäisi omistaa vanhempaansa: jos pudotamme lapsisolmun, vanhemman pitäisi silti olla olemassa. Tämä on tapaus heikoille viittauksille!

Sen sijaan, että käyttäisimme `Rc<T>`:tä, teemme `parent`-kentän tyypiksi `Weak<T>`, tarkemmin `RefCell<Weak<Node>>`. Nyt `Node`-rakennemäärittelymme näyttää tältä:

<span class="filename">Tiedostonimi: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-28/src/main.rs:here}}
```

Solmu voi viitata vanhempisolmuunsa, mutta se ei omista vanhempaansa. Listauksessa 15-28 päivitämme `main`-funktion käyttämään tätä uutta määrittelyä, jotta `leaf`-solmulla on tapa viitata vanhempaansa, `branch`:iin:

<Listing number="15-28" file-name="src/main.rs" caption="`leaf`-solmu heikolla viittauksella vanhempisolmuunsa `branch`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-28/src/main.rs:there}}
```

</Listing>

`leaf`-solmun luominen näyttää samalta kuin Listauksessa 15-27, paitsi `parent`-kentän osalta: `leaf`:lla ei ole aluksi vanhempaa, joten luomme uuden tyhjän `Weak<Node>`-viittausinstanssin.

Tässä vaiheessa, kun yritämme saada viittauksen `leaf`:n vanhempaan `upgrade`-metodilla, saamme `None`-arvon. Näemme tämän ensimmäisen `println!`-lauseen tulosteesta:

```text
leaf parent = None
```

Kun luomme `branch`-solmun, sillä on myös uusi `Weak<Node>`-viittaus `parent`-kentässä, koska `branch`:lla ei ole vanhempisolmua. Meillä on edelleen `leaf` yhtenä `branch`:n lapsista. Kun meillä on `Node`-instanssi `branch`:ssa, voimme muokata `leaf`:tä antamaan sille `Weak<Node>`-viittauksen vanhempaansa. Käytämme `borrow_mut`-metodia `RefCell<Weak<Node>>`-arvolla `leaf`:n `parent`-kentässä, ja käytämme sitten `Rc::downgrade`-funktiota luodaksemme `Weak<Node>`-viittauksen `branch`:iin `Rc<Node>`-arvosta `branch`:ssa.

Kun tulostamme `leaf`:n vanhemman uudelleen, tällä kertaa saamme `Some`-variantin, joka pitää `branch`:ia: nyt `leaf` voi käyttää vanhempaansa! Kun tulostamme `leaf`:n, vältämme myös kierron, joka lopulta päättyi pinon ylivuotoon kuten Listauksessa 15-26; `Weak<Node>`-viittaukset tulostetaan muodossa `(Weak)`:

```text
leaf parent = Some(Node { value: 5, parent: RefCell { value: (Weak) },
children: RefCell { value: [Node { value: 3, parent: RefCell { value: (Weak) },
children: RefCell { value: [] } }] } })
```

Äärettömän tulosteen puute osoittaa, että tämä koodi ei luonut viittauskiertoa. Voimme myös päätellä tämän katsomalla arvoja, jotka saamme kutsumalla `Rc::strong_count` ja `Rc::weak_count`.

#### `strong_count`- ja `weak_count`-arvojen muutosten visualisointi

Katsotaan, miten `Rc<Node>`-instanssien `strong_count`- ja `weak_count`-arvot muuttuvat luomalla uuden sisäisen näkyvyysalueen ja siirtämällä `branch`:n luominen kyseiseen näkyvyysalueeseen. Näin voimme nähdä, mitä tapahtuu, kun `branch` luodaan ja sitten pudotetaan, kun se poistuu näkyvyysalueelta. Muutokset on esitetty Listauksessa 15-29:

<Listing number="15-29" file-name="src/main.rs" caption="`branch`:n luominen sisäisessä näkyvyysalueessa ja vahvojen ja heikkojen viittauslaskureiden tarkastelu">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-29/src/main.rs:here}}
```

</Listing>

`leaf`:n luomisen jälkeen sen `Rc<Node>`:lla on vahva laskuri 1 ja heikko laskuri 0. Sisäisessä näkyvyysalueessa luomme `branch`:in ja yhdistämme sen `leaf`:iin, jolloin kun tulostamme laskurit, `branch`:n `Rc<Node>`:lla on vahva laskuri 1 ja heikko laskuri 1 (`leaf.parent`:n osoittaessa `branch`:iin `Weak<Node>`-viittauksella). Kun tulostamme laskurit `leaf`:ssä, sillä on vahva laskuri 2, koska `branch`:lla on nyt klooni `leaf`:n `Rc<Node>`-arvosta tallennettuna `branch.children`:iin, mutta heikko laskuri on edelleen 0.

Kun sisäinen näkyvyysalue päättyy, `branch` poistuu näkyvyysalueelta ja `Rc<Node>`:n vahva laskuri laskee 0:aan, joten sen `Node` pudotetaan. Heikko laskuri 1 `leaf.parent`:sta ei vaikuta siihen, pudotetaanko `Node` vai ei, joten emme saa muistivuotoja!

Jos yritämme käyttää `leaf`:n vanhempaa näkyvyysalueen päättymisen jälkeen, saamme `None`:n uudelleen. Ohjelman lopussa `leaf`:n `Rc<Node>`:lla on vahva laskuri 1 ja heikko laskuri 0, koska muuttuja `leaf` on nyt ainoa viittaus `Rc<Node>`-arvoon.

Kaikki laskureiden hallintaan ja arvojen pudottamiseen liittyvä logiikka on sisäänrakennettu `Rc<T>`:ään ja `Weak<T>`:ään ja niiden `Drop`-traitin toteutuksiin. Määrittämällä, että lapsen suhteen vanhempaansa pitäisi olla `Weak<T>`-viittaus `Node`-määrittelyssä, voit saada vanhempisolmut osoittamaan lapsisolmuihin ja päinvastoin luomatta viittauskiertoa ja muistivuotoja.

## Yhteenveto

Tämä luku käsitteli älykkäiden osoittimien käyttöä erilaisten takuujen ja kompromissien tekemiseksi verrattuna niihin, joita Rust tekee oletuksena tavallisilla viittauksilla. `Box<T>`-tyypillä on tunnettu koko, ja se osoittaa keossa varattuun dataan. `Rc<T>`-tyyppi seuraa viittausten määrää keossa olevaan dataan, jotta datalla voi olla useita omistajia. `RefCell<T>`-tyyppi sisäisellä mutabiliteetillaan antaa meille tyypin, jota voimme käyttää, kun tarvitsemme muuttumattoman tyypin mutta meidän täytyy muuttaa sen sisäistä arvoa; se myös pakottaa lainaussäännöt ajonaikana käännösaikan sijaan.

Käsittelimme myös `Deref`- ja `Drop`-traitteja, jotka mahdollistavat suuren osan älykkäiden osoittimien toiminnallisuudesta. Tutkimme viittauskiertoja, jotka voivat aiheuttaa muistivuotoja, ja miten ne estetään käyttämällä `Weak<T>`:tä.

Jos tämä luku on herättänyt kiinnostuksesi ja haluat toteuttaa omat älykkäät osoittimesi, tutustu [”The Rustonomicon”][nomicon] -teokseen saadaksesi lisää hyödyllistä tietoa.

Seuraavaksi puhumme rinnakkaisuudesta Rustissa. Opit jopa muutamasta uudesta älykkäästä osoittimesta.

[nomicon]: ../nomicon/index.html
