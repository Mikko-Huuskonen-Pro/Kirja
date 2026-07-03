## Yksisäikeisen palvelimen muuttaminen monisäikeiseksi palvelimeksi

Tällä hetkellä palvelin käsittelee jokaisen pyynnön vuorotellen, eli se ei käsittele toista yhteyttä ennen kuin ensimmäinen on käsitelty loppuun. Jos palvelin saisi yhä enemmän pyyntöjä, tämä peräkkäinen suoritus olisi yhä vähemmän optimaalinen. Jos palvelin saa pyynnön, jonka käsittely kestää kauan, myöhempien pyyntöjen täytyy odottaa, kunnes pitkä pyyntö on valmis — vaikka uudet pyynnöt voisi käsitellä nopeasti. Meidän täytyy korjata tämä, mutta ensin katsomme ongelmaa käytännössä.

### Hitaan pyynnön simulointi nykyisessä palvelintoteutuksessa

Katsomme, miten hitaasti käsiteltävä pyyntö voi vaikuttaa muihin pyyntöihin, joita tehdään nykyiseen palvelintoteutukseemme. Listausta 21-10 toteuttaa pyynnön käsittelyn polulle _/sleep_ simuloidulla hitaalla vastauksella, joka saa palvelimen nukkumaan viisi sekuntia ennen vastaamista.

<Listing number="21-10" file-name="src/main.rs" caption="Hitaan pyynnön simulointi nukkumalla 5 sekuntia">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-10/src/main.rs:here}}
```

</Listing>

Vaihdoimme `if`-lausekkeesta `match`-lausekkeeseen, koska meillä on nyt kolme tapausta. Meidän täytyy eksplisiittisesti matchata `request_line`-viipaletta vasten merkkijonoliteraaliarvoja; `match` ei tee automaattista viittaamista ja käänteisviittaamista kuten yhtäsuuruusmetodi.

Ensimmäinen haara on sama kuin `if`-lohko listauksessa 21-9. Toinen haara matchaa pyynnön polulle _/sleep_. Kun tällainen pyyntö vastaanotetaan, palvelin nukkuu viisi sekuntia ennen onnistuneen HTML-sivun renderöintiä. Kolmas haara on sama kuin `else`-lohko listauksessa 21-9.

Näet, kuinka primitiivinen palvelimemme on: oikeat kirjastot käsittelisivät useiden pyyntöjen tunnistamisen paljon vähemmällä sanamäärällä!

Käynnistä palvelin komennolla `cargo run`. Avaa sitten kaksi selainikkunaa: toinen osoitteeseen _http://127.0.0.1:7878/_ ja toinen osoitteeseen _http://127.0.0.1:7878/sleep_. Jos syötät _/_-URI:n muutaman kerran kuten aiemmin, näet sen vastaavan nopeasti. Mutta jos syötät _/sleep_ ja lataat sitten _/_, näet että _/_ odottaa, kunnes `sleep` on nukkunut koko viisi sekuntiaan ennen latautumista.

On useita tekniikoita, joilla voisimme välttää pyyntöjen jonoutumisen hitaan pyynnön taakse, mukaan lukien asyncin käyttö kuten teimme luvussa 17; toteutamme säikeiden poolin.

### Suorituskyvyn parantaminen säikeiden poolilla

_Säikeiden pooli_ on joukko luotuja säikeitä, jotka odottavat ja ovat valmiita käsittelemään tehtävän. Kun ohjelma vastaanottaa uuden tehtävän, se osoittaa yhden poolin säikeistä tehtävään, ja kyseinen säie käsittelee tehtävän. Poolin jäljellä olevat säikeet ovat käytettävissä käsittelemään muita saapuvia tehtäviä, kun ensimmäinen säie käsittelee. Kun ensimmäinen säie on käsitellyt tehtävänsä, se palautetaan joutilaan säikeiden pooliin, valmiina käsittelemään uuden tehtävän. Säikeiden pooli mahdollistaa yhteyksien käsittelyn rinnakkain ja kasvattaa palvelimen suorituskykyä.

Rajoitamme säikeiden määrän poolissa pieneksi suojautuaksemme DoS-hyökkäyksiltä; jos ohjelma loisi uuden säikeen jokaiselle saapuvalle pyynnölle, joku, joka tekisi 10 miljoonaa pyyntöä palvelimellemme, voisi aiheuttaa kaaosta käyttämällä kaikki palvelimen resurssit ja pysäyttämällä pyyntöjen käsittelyn.

Sen sijaan, että loisimme rajattomasti säikeitä, pidämme kiinteän määrän säikeitä odottamassa poolissa. Saapuvat pyynnöt lähetetään pooliin käsiteltäväksi. Pooli ylläpitää jonoa saapuvista pyynnöistä. Jokainen poolin säikeistä poimii pyynnön tästä jonosta, käsittelee pyynnön ja pyytää sitten jonosta seuraavan pyynnön. Tällä suunnittelulla voimme käsitellä jopa *`N`* pyyntöä rinnakkain, missä *`N`* on säikeiden määrä. Jos jokainen säie vastaa pitkään kestävään pyyntöön, myöhemmät pyynnöt voivat silti jonoutua, mutta olemme kasvattaneet pitkään kestävien pyyntöjen määrää, jonka voimme käsitellä ennen kuin saavutamme tuon pisteen.

Tämä tekniikka on vain yksi monista tavoista parantaa verkkopalvelimen suorituskykyä. Muita vaihtoehtoja, joita voit tutkia, ovat fork/join-malli, yksisäikeinen async I/O -malli ja monisäikeinen async I/O -malli. Jos aihe kiinnostaa, voit lukea lisää muista ratkaisuista ja yrittää toteuttaa niitä; matalan tason kielellä kuten Rust kaikki nämä vaihtoehdot ovat mahdollisia.

Ennen kuin alamme toteuttaa säikeiden poolia, puhutaan siitä, miltä poolin käyttö näyttää. Kun suunnittelet koodia, asiakasrajapinnan kirjoittaminen ensin voi ohjata suunnitteluasi. Kirjoita koodin API niin, että se on rakenteeltaan sellainen, jolla haluat kutsua sitä; toteuta sitten toiminnallisuus tuon rakenteen sisällä sen sijaan, että toteuttaisit toiminnallisuuden ja suunnittelisit julkisen API:n jälkikäteen.

Samoin kuin käytimme testivetoista kehitystä luvun 12 projektissa, käytämme tässä kääntäjävetoista kehitystä. Kirjoitamme koodin, joka kutsuu haluamiamme funktioita, ja katsomme sitten kääntäjän virheitä selvittääksemme, mitä meidän pitää muuttaa seuraavaksi, jotta koodi toimii. Ennen sitä kuitenkin tutkimme tekniikan, jota emme aio käyttää lähtökohtana.

<!-- Old headings. Do not remove or links may break. -->

<a id="code-structure-if-we-could-spawn-a-thread-for-each-request"></a>

#### Säikeen luominen jokaiselle pyynnölle

Tutkitaan ensin, miltä koodimme näyttäisi, jos se loisi uuden säikeen jokaiselle yhteydelle. Kuten aiemmin mainittiin, tämä ei ole lopullinen suunnitelmamme mahdollisesti rajattoman määrän säikeiden luomisen ongelmien vuoksi, mutta se on lähtökohta toimivan monisäikeisen palvelimen saamiseksi ensin. Lisäämme sitten säikeiden poolin parannuksena, ja kahden ratkaisun vertailu on helpompaa. Listausta 21-11 näyttää muutokset `main`-funktioon luodaksemme uuden säikeen käsittelemään jokaista streamia `for`-silmukan sisällä.

<Listing number="21-11" file-name="src/main.rs" caption="Uuden säikeen luominen jokaiselle streamille">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-11/src/main.rs:here}}
```

</Listing>

Kuten opit luvussa 16, `thread::spawn` luo uuden säikeen ja suorittaa sitten sulkeuman koodin uudessa säikeessä. Jos suoritat tämän koodin ja lataat _/sleep_ selaimessasi ja sitten _/_ kahdessa muussa selainvälilehdessä, näet todellakin, etteivät _/_-pyynnöt joudu odottamaan _/sleep_-pyynnön valmistumista. Kuten mainitsimme, tämä kuitenkin lopulta ylikuormittaa järjestelmän, koska loisit uusia säikeitä ilman mitään rajaa.

Saatat myös muistaa luvusta 17, että tämä on juuri sellainen tilanne, jossa async ja await todella loistavat! Pidä tämä mielessä, kun rakennamme säikeiden poolia, ja mieti, miltä asiat näyttäisivät erilaisilta tai samankaltaisilta asyncin kanssa.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-a-similar-interface-for-a-finite-number-of-threads"></a>

#### Rajallisen määrän säikeitä luovan rajapinnan luominen

Haluamme säikeiden poolimme toimivan samankaltaisella, tutulla tavalla, jotta vaihtaminen säikeistä säikeiden pooliin ei vaadi suuria muutoksia API:tamme käyttävään koodiin. Listausta 21-12 näyttää hypoteettisen rajapinnan `ThreadPool`-rakenteelle, jota haluamme käyttää `thread::spawn`-funktion sijaan.

<Listing number="21-12" file-name="src/main.rs" caption="Ihanteellinen `ThreadPool`-rajapintamme">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-12/src/main.rs:here}}
```

</Listing>

Käytämme `ThreadPool::new`-funktiota luodaksemme uuden säikeiden poolin konfiguroitavalla määrällä säikeitä — tässä tapauksessa neljä. Sitten `for`-silmukassa `pool.execute`-funktiolla on samankaltainen rajapinta kuin `thread::spawn`-funktiolla: se ottaa sulkeuman, jonka poolin pitäisi suorittaa jokaiselle streamille. Meidän täytyy toteuttaa `pool.execute` niin, että se ottaa sulkeuman ja antaa sen poolin säikeelle suoritettavaksi. Tämä koodi ei vielä käänny, mutta yritämme, jotta kääntäjä voi ohjata meitä korjaamaan sen.

<!-- Old headings. Do not remove or links may break. -->

<a id="building-the-threadpool-struct-using-compiler-driven-development"></a>

#### `ThreadPool`-rakenteen rakentaminen kääntäjävetoisella kehityksellä

Tee listauksen 21-12 muutokset tiedostoon _src/main.rs_, ja käytetään sitten `cargo check`-komennon kääntäjävirheitä kehityksen ohjaamiseen. Tässä on ensimmäinen virhe, jonka saamme:

```console
{{#include ../listings/ch21-web-server/listing-21-12/output.txt}}
```

Hienoa! Tämä virhe kertoo, että tarvitsemme `ThreadPool`-tyypin tai -moduulin, joten rakennamme sellaisen nyt. `ThreadPool`-toteutuksemme on riippumaton siitä, millaista työtä verkkopalvelimemme tekee. Vaihdetaan siis `hello`-crate binaaricratesta kirjastocrateksi säilyttääksemme `ThreadPool`-toteutuksemme. Kun vaihdamme kirjastocrateksi, voimme myös käyttää erillistä säikeiden poolin kirjastoa mihin tahansa työhön, jossa haluamme käyttää säikeiden poolia — ei vain verkkopyyntöjen palvelemiseen.

Luo tiedosto _src/lib.rs_, joka sisältää seuraavan — yksinkertaisimman `ThreadPool`-rakenteen määrittelyn, jonka voimme toistaiseksi tehdä:

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/src/lib.rs}}
```

</Listing>

Muokkaa sitten tiedostoa _main.rs_ tuomalla `ThreadPool` näkyviin kirjastocratesta lisäämällä seuraava koodi tiedoston _src/main.rs_ alkuun:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/src/main.rs:here}}
```

</Listing>

Tämä koodi ei vieläkään toimi, mutta tarkistetaan se uudelleen saadaksemme seuraavan korjattavan virheen:

```console
{{#include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/output.txt}}
```

Tämä virhe osoittaa, että seuraavaksi meidän täytyy luoda `ThreadPool`-rakenteelle assosioitu funktio nimeltä `new`. Tiedämme myös, että `new`-funktiolla täytyy olla yksi parametri, joka voi ottaa `4` argumentiksi, ja sen pitäisi palauttaa `ThreadPool`-instanssi. Toteutetaan yksinkertaisin `new`-funktio, jolla on nämä ominaisuudet:

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-02-impl-threadpool-new/src/lib.rs}}
```

</Listing>

Valitsimme `usize`-tyypin `size`-parametrille, koska tiedämme, ettei negatiivinen säikeiden määrä ole järkevä. Tiedämme myös käyttäväämme tätä `4`:ää säikeiden kokoelman elementtien määränä, mihin `usize`-tyyppi on tarkoitettu, kuten käsiteltiin [”Kokonaislukutyypit”][integer-types]<!-- ignore --> -osiossa luvussa 3.

Tarkistetaan koodi uudelleen:

```console
{{#include ../listings/ch21-web-server/no-listing-02-impl-threadpool-new/output.txt}}
```

Nyt virhe johtuu siitä, ettei `ThreadPool`-rakenteella ole `execute`-metodia. Muista [”Rajallisen määrän säikeitä luovan rajapinnan luominen”](#creating-a-finite-number-of-threads)<!-- ignore --> -osiosta, että päätimme säikeiden poolimme rajapinnan olevan samankaltainen kuin `thread::spawn`. Lisäksi toteutamme `execute`-funktion niin, että se ottaa annetun sulkeuman ja antaa sen poolin joutilaalle säikeelle suoritettavaksi.

Määrittelemme `execute`-metodin `ThreadPool`-rakenteelle ottamaan sulkeuman parametrina. Muista [”Kaapattujen arvojen siirtäminen sulkeumasta ja `Fn`-traitit”][fn-traits]<!-- ignore --> -osio luvusta 13, jossa voimme ottaa sulkeumia parametreina kolmella eri traitilla: `Fn`, `FnMut` ja `FnOnce`. Meidän täytyy päättää, millaista sulkeumaa käytämme tässä. Tiedämme päätyvämme tekemään jotain samankaltaista kuin standardikirjaston `thread::spawn`-toteutus, joten voimme katsoa, mitä rajoja `thread::spawn`-funktion parametri on. Dokumentaatio näyttää seuraavan:

```rust,ignore
pub fn spawn<F, T>(f: F) -> JoinHandle<T>
    where
        F: FnOnce() -> T,
        F: Send + 'static,
        T: Send + 'static,
```

`F`-tyyppiparametri on se, josta olemme kiinnostuneita tässä; `T`-tyyppiparametri liittyy palautusarvoon, eikä se meitä kiinnosta. Näemme, että `spawn` käyttää `FnOnce`-traitia rajana `F`:lle. Tämä on todennäköisesti se, mitä haluamme, koska lopulta välitämme `execute`-funktioon saamamme argumentin `spawn`-funktiolle. Voimme olla varmempia siitä, että `FnOnce` on haluamamme trait, koska pyynnön käsittelevä säie suorittaa kyseisen pyynnön sulkeuman vain kerran — mikä vastaa `FnOnce`-traitin `Once`-osaa.

`F`-tyyppiparametrilla on myös trait-raja `Send` ja elinikäraja `'static`, jotka ovat hyödyllisiä tilanteessamme: tarvitsemme `Send`-rajan siirtääksemme sulkeuman säikeestä toiseen ja `'static`-rajan, koska emme tiedä, kuinka kauan säikeen suoritus kestää. Luodaan `execute`-metodi `ThreadPool`-rakenteelle, joka ottaa geneerisen parametrin tyypiltä `F` näillä rajoilla:

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-03-define-execute/src/lib.rs:here}}
```

</Listing>

Käytämme edelleen `()`-merkintää `FnOnce`-traitin jälkeen, koska tämä `FnOnce` edustaa sulkeumaa, joka ei ota parametreja ja palauttaa yksikkötyypin `()`. Kuten funktiomäärittelyissä, palautustyypin voi jättää pois allekirjoituksesta, mutta vaikka meillä ei olisi parametreja, tarvitsemme silti sulkeumat.

Taaskin tämä on yksinkertaisin `execute`-metodin toteutus: se ei tee mitään, mutta yritämme vain saada koodin kääntymään. Tarkistetaan se uudelleen:

```console
{{#include ../listings/ch21-web-server/no-listing-03-define-execute/output.txt}}
```

Se kääntyy! Mutta huomaa, että jos yrität `cargo run`-komentoa ja teet pyynnön selaimessa, näet selaimessa samat virheet, joita näimme luvun alussa. Kirjastomme ei vielä kutsu `execute`-funktiolle välitettyä sulkeumaa!

> Huom: Kielistä, joilla on tiukat kääntäjät kuten Haskell ja Rust, saatat kuulla sanonnan: ”jos koodi kääntyy, se toimii.” Mutta tämä sanonta ei ole yleispätevästi totta. Projektimme kääntyy, mutta se ei tee yhtään mitään! Jos rakentaisimme oikean, valmiin projektin, tämä olisi hyvä hetki alkaa kirjoittaa yksikkötestejä varmistaaksemme, että koodi kääntyy _ja_ käyttäytyy haluamallamme tavalla.

Mieti: mitä olisi erilaista tässä, jos ajaisimme _futuren_ sulkeuman sijaan?

#### Säikeiden määrän validointi `new`-funktiossa

Emme tee mitään `new`- ja `execute`-funktioiden parametreilla. Toteutetaan näiden funktioiden rungot haluamallamme käyttäytymisellä. Aloitetaan `new`-funktiosta. Aiemmin valitsimme etumerkittömän tyypin `size`-parametrille, koska pooli negatiivisella säikeiden määrällä ei ole järkevä. Pooli nollalla säikeellä ei kuitenkaan myöskään ole järkevä, vaikka nolla on täysin kelvollinen `usize`-arvo. Lisäämme koodia, joka tarkistaa, että `size` on suurempi kuin nolla, ennen kuin palautamme `ThreadPool`-instanssin, ja saamme ohjelman panikoimaan, jos se saa nollan `assert!`-makron avulla, kuten listauksessa 21-13.

<Listing number="21-13" file-name="src/lib.rs" caption="`ThreadPool::new`-toteutus, joka panikoi jos `size` on nolla">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-13/src/lib.rs:here}}
```

</Listing>

Olemme myös lisänneet dokumentaatiota `ThreadPool`-rakenteellemme doc-kommenteilla. Huomaa, että noudatimme hyviä dokumentointikäytäntöjä lisäämällä osion, joka kuvaa tilanteet, joissa funktiomme voi panikoida, kuten käsiteltiin luvussa 14. Kokeile ajaa `cargo doc --open` ja napsauta `ThreadPool`-rakennetta nähdäksesi, miltä `new`-funktion generoitu dokumentaatio näyttää!

Sen sijaan, että lisäisimme `assert!`-makron kuten teimme tässä, voisimme muuttaa `new`-funktion `build`-funktioksi ja palauttaa `Result`-arvon kuten teimme `Config::build`-funktiolla I/O-projektissa listauksessa 12-9. Päätimme kuitenkin tässä tapauksessa, että säikeiden poolin luominen ilman säikeitä on palautumaton virhe. Jos olet kunnianhimoinen, yritä kirjoittaa funktio nimeltä `build` seuraavalla allekirjoituksella vertailua varten `new`-funktion kanssa:

```rust,ignore
pub fn build(size: usize) -> Result<ThreadPool, PoolCreationError> {
```

#### Tilaa säikeiden tallentamiseen

Nyt kun meillä on tapa varmistaa, että meillä on kelvollinen määrä säikeitä tallennettavaksi pooliin, voimme luoda nämä säikeet ja tallentaa ne `ThreadPool`-rakenteeseen ennen rakenteen palauttamista. Mutta miten ”tallennetaan” säie? Katsotaan `thread::spawn`-funktion allekirjoitusta uudelleen:

```rust,ignore
pub fn spawn<F, T>(f: F) -> JoinHandle<T>
    where
        F: FnOnce() -> T,
        F: Send + 'static,
        T: Send + 'static,
```

`spawn`-funktio palauttaa `JoinHandle<T>`-arvon, missä `T` on sulkeuman palauttama tyyppi. Kokeillaan käyttää myös `JoinHandle`-tyyppiä ja katsotaan, mitä tapahtuu. Tapauksessamme sulkeumat, jotka välitämme säikeiden poolille, käsittelevät yhteyden eivätkä palauta mitään, joten `T` on yksikkötyyppi `()`.

Listauksen 21-14 koodi kääntyy, mutta ei vielä luo säikeitä. Olemme muuttaneet `ThreadPool`-rakenteen määrittelyn sisältämään vektorin `thread::JoinHandle<()>`-instansseja, alustaneet vektorin kapasiteetilla `size`, asettaneet `for`-silmukan, joka suorittaa koodia säikeiden luomiseksi, ja palauttaneet `ThreadPool`-instanssin, joka sisältää ne.

<Listing number="21-14" file-name="src/lib.rs" caption="Vektorin luominen `ThreadPool`-rakenteelle säikeiden säilyttämiseksi">

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-14/src/lib.rs:here}}
```

</Listing>

Olemme tuoneet `std::thread`-moduulin näkyviin kirjastocratessa, koska käytämme `thread::JoinHandle`-tyyppiä `ThreadPool`-rakenteen vektorin alkioille.

Kun kelvollinen koko on vastaanotettu, `ThreadPool`-rakenteemme luo uuden vektorin, joka voi sisältää `size` alkiota. `with_capacity`-funktio tekee saman tehtävän kuin `Vec::new`, mutta tärkeällä erolla: se varaa tilan vektorille etukäteen. Koska tiedämme tarvitsevamme tallentaa `size` elementtiä vektoriin, tämä varaus etukäteen on hieman tehokkaampaa kuin `Vec::new`-funktion käyttö, joka muuttaa kokoaan elementtien lisäämisen yhteydessä.

Kun ajat `cargo check`-komennon uudelleen, sen pitäisi onnistua.

#### `Worker`-rakenne, joka vastaa koodin lähettämisestä `ThreadPool`-rakenteesta säikeelle

Jätimme kommentin `for`-silmukkaan listauksessa 21-14 säikeiden luomiseen liittyen. Tässä katsomme, miten säikeet todella luodaan. Standardikirjasto tarjoaa `thread::spawn`-funktion säikeiden luomiseen, ja `thread::spawn` odottaa saavansa koodin, jonka säikeen pitäisi suorittaa heti säikeen luomisen jälkeen. Tapauksessamme haluamme kuitenkin luoda säikeet ja saada ne _odottamaan_ koodia, jonka lähetämme myöhemmin. Standardikirjaston säikeiden toteutus ei sisällä tapaa tehdä tätä; meidän täytyy toteuttaa se manuaalisesti.

Toteutamme tämän käyttäytymisen esittelemällä uuden tietorakenteen `ThreadPool`-rakenteen ja säikeiden väliin hallitsemaan tätä uutta käyttäytymistä. Kutsumme tätä tietorakennetta _Worker_-rakenteeksi, mikä on yleinen termi poolitoteutuksissa. `Worker` poimii suoritettavaa koodia ja suorittaa koodin `Worker`-rakenteen säikeessä.

Ajattele ravintolan keittiössä työskenteleviä ihmisiä: työntekijät odottavat, kunnes asiakkailta tulee tilauksia, ja he ovat vastuussa näiden tilausten ottamisesta ja täyttämisestä.

Sen sijaan, että tallentaisimme vektorin `JoinHandle<()>`-instansseja säikeiden pooliin, tallennamme `Worker`-rakenteen instansseja. Jokainen `Worker` tallentaa yhden `JoinHandle<()>`-instanssin. Toteutamme sitten metodin `Worker`-rakenteelle, joka ottaa suoritettavan sulkeuman ja lähettää sen jo käynnissä olevalle säikeelle suoritettavaksi. Annamme myös jokaiselle `Worker`-rakenteelle `id`-tunnisteen, jotta voimme erottaa poolin eri `Worker`-instanssit lokituksessa tai virheenkorjauksessa.

Tässä on uusi prosessi, joka tapahtuu, kun luomme `ThreadPool`-rakenteen. Toteutamme koodin, joka lähettää sulkeuman säikeelle, kun olemme asettaneet `Worker`-rakenteen tällä tavalla:

1. Määrittele `Worker`-rakenne, joka sisältää `id`-kentän ja `JoinHandle<()>`-kentän.
2. Muuta `ThreadPool` sisältämään vektori `Worker`-instansseja.
3. Määrittele `Worker::new`-funktio, joka ottaa `id`-numeron ja palauttaa `Worker`-instanssin, joka sisältää `id`-kentän ja säikeen, joka on luotu tyhjällä sulkeumalla.
4. `ThreadPool::new`-funktiossa käytä `for`-silmukan laskuria generoimaan `id`, luo uusi `Worker` kyseisellä `id`:llä ja tallenna worker vektoriin.

Jos haluat haastetta, yritä toteuttaa nämä muutokset itse ennen kuin katsot listauksen 21-15 koodia.

Valmis? Tässä on listausta 21-15 yhdellä tavalla tehdä edellä kuvatut muutokset.

<Listing number="21-15" file-name="src/lib.rs" caption="`ThreadPool`-rakenteen muuttaminen sisältämään `Worker`-instansseja säikeiden suoran tallentamisen sijaan">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-15/src/lib.rs:here}}
```

</Listing>

Olemme muuttaneet `ThreadPool`-rakenteen kentän nimen `threads`-kentästä `workers`-kentäksi, koska se sisältää nyt `Worker`-instansseja `JoinHandle<()>`-instanssien sijaan. Käytämme `for`-silmukan laskuria argumenttina `Worker::new`-funktiolle ja tallennamme jokaisen uuden `Worker`-rakenteen vektoriin nimeltä `workers`.

Ulkoinen koodi (kuten palvelimemme tiedostossa _src/main.rs_) ei tarvitse tietää toteutuksen yksityiskohtia `Worker`-rakenteen käytöstä `ThreadPool`-rakenteen sisällä, joten teemme `Worker`-rakenteen ja sen `new`-funktion yksityisiksi. `Worker::new`-funktio käyttää antamaamme `id`:tä ja tallentaa `JoinHandle<()>`-instanssin, joka on luotu luomalla uusi säie tyhjällä sulkeumalla.

> Huom: Jos käyttöjärjestelmä ei voi luoda säiettä, koska järjestelmäresursseja ei ole tarpeeksi, `thread::spawn` panikoi. Se saa koko palvelimemme panikoimaan, vaikka osa säikeiden luomisesta saattaisi onnistua. Yksinkertaisuuden vuoksi tämä käyttäytyminen on ok, mutta tuotantokäyttöön tarkoitetussa säikeiden poolin toteutuksessa käyttäisit todennäköisesti [`std::thread::Builder`][builder]<!-- ignore --> -rakenteen ja sen [`spawn`][builder-spawn]<!-- ignore --> -metodia, joka palauttaa `Result`-arvon.

Tämä koodi kääntyy ja tallentaa määrän `Worker`-instansseja, jonka annoimme argumenttina `ThreadPool::new`-funktiolle. Mutta emme _vieläkään_ käsittele sulkeumaa, jonka saamme `execute`-funktiossa. Katsotaan seuraavaksi, miten se tehdään.

#### Pyyntöjen lähettäminen säikeille kanavien kautta

Seuraava ongelma, johon tartumme, on se, että `thread::spawn`-funktiolle annetut sulkeumat eivät tee yhtään mitään. Tällä hetkellä saamme sulkeuman, jonka haluamme suorittaa, `execute`-metodissa. Mutta meidän täytyy antaa `thread::spawn`-funktiolle sulkeuma suoritettavaksi, kun luomme jokaisen `Worker`-rakenteen `ThreadPool`-rakenteen luomisen yhteydessä.

Haluamme juuri luomiemme `Worker`-rakenteiden hakevan suoritettavan koodin jonosta, jonka `ThreadPool` pitää hallussaan, ja lähettävän kyseisen koodin säikeelleen suoritettavaksi.

Luvussa 16 opitut kanavat — yksinkertainen tapa kommunikoida kahden säikeen välillä — sopisivat tähän käyttötapaukseen täydellisesti. Käytämme kanavaa työjonona, ja `execute` lähettää työn `ThreadPool`-rakenteesta `Worker`-instansseille, jotka lähettävät työn säikeelleen. Tässä on suunnitelma:

1. `ThreadPool` luo kanavan ja pitää lähettäjän hallussaan.
2. Jokainen `Worker` pitää vastaanottajan hallussaan.
3. Luomme uuden `Job`-rakenteen, joka sisältää sulkeumat, jotka haluamme lähettää kanavaa pitkin.
4. `execute`-metodi lähettää suoritettavan työn lähettäjän kautta.
5. Säikeessään `Worker` silmukoi vastaanottajansa yli ja suorittaa kaikkien vastaanottamiensa töiden sulkeumat.

Aloitetaan luomalla kanava `ThreadPool::new`-funktiossa ja tallentamalla lähettäjä `ThreadPool`-instanssiin, kuten listauksessa 21-16. `Job`-rakenne ei toistaiseksi sisällä mitään, mutta se on tyyppi, jota lähetämme kanavaa pitkin.

<Listing number="21-16" file-name="src/lib.rs" caption="`ThreadPool`-rakenteen muuttaminen tallentamaan kanavan lähettäjä, joka välittää `Job`-instansseja">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-16/src/lib.rs:here}}
```

</Listing>

`ThreadPool::new`-funktiossa luomme uuden kanavan ja annamme poolin pitää lähettäjän hallussaan. Tämä kääntyy onnistuneesti.

Kokeillaan välittää kanavan vastaanottaja jokaiselle `Worker`-rakenteelle, kun säikeiden pooli luo kanavan. Tiedämme haluavamme käyttää vastaanottajaa säikeessä, jonka `Worker`-instanssit luovat, joten viittaamme `receiver`-parametriin sulkeumassa. Listauksen 21-17 koodi ei vielä aivan käänny.

<Listing number="21-17" file-name="src/lib.rs" caption="Vastaanottajan välittäminen jokaiselle `Worker`-rakenteelle">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-17/src/lib.rs:here}}
```

</Listing>

Olemme tehneet pieniä ja suoraviivaisia muutoksia: välitämme vastaanottajan `Worker::new`-funktiolle ja käytämme sitä sitten sulkeuman sisällä.

Kun yritämme tarkistaa tämän koodin, saamme tämän virheen:

```console
{{#include ../listings/ch21-web-server/listing-21-17/output.txt}}
```

Koodi yrittää välittää `receiver`-arvon useille `Worker`-instansseille. Tämä ei toimi, kuten muistat luvusta 16: Rustin tarjoama kanavatoteutus on useita _tuottajia_, yksi _kuluttaja_. Tämä tarkoittaa, ettei voi vain kloonata kanavan kuluttajapäätä korjataksemme tämän koodin. Emme myöskään halua lähettää viestiä useita kertoja useille kuluttajille; haluamme yhden viestilistan useilla `Worker`-instansseilla siten, että jokainen viesti käsitellään kerran.

Lisäksi työn poimiminen kanavan jonosta edellyttää `receiver`-arvon mutatoimista, joten säikeiden täytyy jakaa ja muokata `receiver`-arvoa turvallisesti; muuten saatamme saada kilpailutilanteita (kuten käsiteltiin luvussa 16).

Muista luvussa 16 käsitellyt säieturvalliset älykkäät osoittimet: jakaaksemme omistajuuden useiden säikeiden välillä ja salliaksemme säikeiden mutatoida arvoa, meidän täytyy käyttää `Arc<Mutex<T>>`-rakennetta. `Arc`-tyyppi antaa useiden `Worker`-instanssien omistaa vastaanottajan, ja `Mutex` varmistaa, että vain yksi `Worker` saa työn vastaanottajalta kerrallaan. Listausta 21-18 näyttää tarvittavat muutokset.

<Listing number="21-18" file-name="src/lib.rs" caption="Vastaanottajan jakaminen `Worker`-instanssien kesken `Arc`- ja `Mutex`-rakenteiden avulla">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-18/src/lib.rs:here}}
```

</Listing>

`ThreadPool::new`-funktiossa laitamme vastaanottajan `Arc`- ja `Mutex`-rakenteisiin. Jokaiselle uudelle `Worker`-rakenteelle kloonaamme `Arc`-rakenteen kasvattaaksemme viittauslaskuria, jotta `Worker`-instanssit voivat jakaa vastaanottajan omistajuuden.

Näillä muutoksilla koodi kääntyy! Olemme lähellä maalia!

#### `execute`-metodin toteuttaminen

Toteutetaan vihdoin `execute`-metodi `ThreadPool`-rakenteelle. Muutamme myös `Job`-rakenteen rakenteesta tyyppialiaaksi trait-objektille, joka sisältää `execute`-funktion vastaanottaman sulkeuman tyypin. Kuten käsiteltiin [”Tyyppialiaasien luominen”][creating-type-synonyms-with-type-aliases]<!-- ignore --> -osiossa luvussa 20, tyyppialiaasit antavat meidän lyhentää pitkiä tyyppejä helpompaa käyttöä varten. Katso listaus 21-19.

<Listing number="21-19" file-name="src/lib.rs" caption="`Job`-tyyppialiaasin luominen `Box`-rakenteelle, joka sisältää jokaisen sulkeuman, ja työn lähettäminen kanavaa pitkin">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-19/src/lib.rs:here}}
```

</Listing>

Kun olemme luoneet uuden `Job`-instanssin `execute`-funktiossa saamallamme sulkeumalla, lähetämme työn kanavan lähettäjäpäähän. Kutsumme `unwrap`-metodia `send`-funktiolle tapauksessa, jossa lähetys epäonnistuu. Tämä voi tapahtua esimerkiksi, jos pysäytämme kaikki säikeemme suorittamasta, mikä tarkoittaa, että vastaanottajapää on lopettanut uusien viestien vastaanottamisen. Tällä hetkellä emme voi pysäyttää säikeitämme suorittamasta: säikeemme jatkavat suoritusta niin kauan kuin pooli on olemassa. Käytämme `unwrap`-metodia, koska tiedämme epäonnistumistapauksen olevan mahdoton, mutta kääntäjä ei tiedä sitä.

Mutta emme ole vielä valmiita! `Worker`-rakenteessa sulkeuma, joka välitetään `thread::spawn`-funktiolle, _viittaa_ edelleen vain kanavan vastaanottajapäähän. Sen sijaan tarvitsemme sulkeuman, joka silmukoi ikuisesti pyytäen työtä kanavan vastaanottajapäästä ja suorittaen työn saadessaan sellaisen. Tehdään listauksessa 21-20 näytetty muutos `Worker::new`-funktioon.

<Listing number="21-20" file-name="src/lib.rs" caption="Töiden vastaanottaminen ja suorittaminen `Worker`-instanssin säikeessä">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-20/src/lib.rs:here}}
```

</Listing>

Tässä kutsumme ensin `lock`-metodia `receiver`-arvolla hankkiaksemme mutexin, ja sitten kutsumme `unwrap`-metodia panikoidaksemme mahdollisista virheistä. Lukon hankkiminen voi epäonnistua, jos mutex on _myrkytetty_ tilassa, mikä voi tapahtua, jos jokin toinen säie panikoi pitäessään lukkoa sen sijaan, että vapauttaisi sen. Tässä tilanteessa `unwrap`-kutsu, joka saa tämän säikeen panikoimaan, on oikea toimenpide. Voit vapaasti muuttaa tämän `unwrap`-kutsun `expect`-kutsuksi merkityksellisellä virheilmoituksella.

Jos saamme lukon mutexiin, kutsumme `recv`-metodia vastaanottaaksemme `Job`-työn kanavalta. Lopullinen `unwrap`-kutsu ohittaa myös mahdolliset virheet tässä, mikä voi tapahtua, jos lähettäjää pitävä säie on sulkeutunut — samalla tavalla kuin `send`-metodi palauttaa `Err`-arvon, jos vastaanottaja sulkeutuu.

`recv`-kutsu blokkaa, joten jos työtä ei vielä ole, nykyinen säie odottaa, kunnes työ tulee saataville. `Mutex<T>` varmistaa, että vain yksi `Worker`-säie kerrallaan yrittää pyytää työtä.

Säikeiden poolimme on nyt toimivassa tilassa! Aja `cargo run` ja tee muutama pyyntö:

<!-- manual-regeneration
cd listings/ch21-web-server/listing-21-20
cargo run
make some requests to 127.0.0.1:7878
Can't automate because the output depends on making requests
-->

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
warning: field `workers` is never read
 --> src/lib.rs:7:5
  |
6 | pub struct ThreadPool {
  |            ---------- field in this struct
7 |     workers: Vec<Worker>,
  |     ^^^^^^^
  |
  = note: `#[warn(dead_code)]` on by default

warning: fields `id` and `thread` are never read
  --> src/lib.rs:48:5
   |
47 | struct Worker {
   |        ------ fields in this struct
48 |     id: usize,
   |     ^^
49 |     thread: thread::JoinHandle<()>,
   |     ^^^^^^

warning: `hello` (lib) generated 2 warnings
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 4.91s
     Running `target/debug/hello`
Worker 0 got a job; executing.
Worker 2 got a job; executing.
Worker 1 got a job; executing.
Worker 3 got a job; executing.
Worker 0 got a job; executing.
Worker 2 got a job; executing.
Worker 1 got a job; executing.
Worker 3 got a job; executing.
Worker 0 got a job; executing.
Worker 2 got a job; executing.
```

Onnistui! Meillä on nyt säikeiden pooli, joka käsittelee yhteyksiä asynkronisesti. Enintään neljä säiettä luodaan, joten järjestelmämme ei ylikuormitu, jos palvelin saa paljon pyyntöjä. Jos teemme pyynnön polulle _/sleep_, palvelin voi palvella muita pyyntöjä antamalla toisen säikeen suorittaa ne.

> Huom: Jos avaat _/sleep_-polun useissa selainikkunoissa samanaikaisesti, ne saattavat latautua viiden sekunnin välein yksi kerrallaan. Jotkin verkkoselaimet suorittavat useita saman pyynnön instansseja peräkkäin välimuistisyistä. Tämä rajoitus ei johdu verkkopalvelimestamme.

Tämä on hyvä hetki pysähtyä ja miettiä, miten listauksien 21-18, 21-19 ja 21-20 koodi olisi erilainen, jos käyttäisimme futureja sulkeuman sijaan tehtävänä. Mitkä tyypit muuttuisivat? Miten metodien allekirjoitukset olisivat erilaisia, jos ollenkaan? Mitkä koodin osat pysyisivät samoina?

Kun olet oppinut `while let` -silmukasta luvuissa 17 ja 18, saatat ihmetellä, miksi emme kirjoittaneet worker-säikeen koodia kuten listauksessa 21-21.

<Listing number="21-21" file-name="src/lib.rs" caption="Vaihtoehtoinen `Worker::new`-toteutus `while let` -silmukan avulla">

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-21/src/lib.rs:here}}
```

</Listing>

Tämä koodi kääntyy ja suoritetaan, mutta ei tuota haluttua säikeiden käyttäytymistä: hidas pyyntö saa edelleen muut pyynnöt odottamaan käsittelyä. Syy on hieman hienovarainen: `Mutex`-rakenteella ei ole julkista `unlock`-metodia, koska lukon omistajuus perustuu `lock`-metodin palauttaman `LockResult<MutexGuard<T>>`-rakenteen sisällä olevan `MutexGuard<T>`-rakenteen elinikään. Käännösaikana lainantarkistin voi sitten pakottaa säännön, että `Mutex`-rakenteen suojaamaa resurssia ei voi käyttää, ellemme pidä lukkoa. Tämä toteutus voi kuitenkin myös johtaa siihen, että lukkoa pidetään pidempään kuin tarkoitettu, jos emme ole tietoisia `MutexGuard<T>`-rakenteen elinikästä.

Listauksen 21-20 koodi, joka käyttää `let job = receiver.lock().unwrap().recv().unwrap();`, toimii, koska `let`-lausekkeella kaikki lausekkeen oikean puolen väliaikaiset arvot pudotetaan heti, kun `let`-lause päättyy. `while let` (ja `if let` ja `match`) eivät kuitenkaan pudota väliaikaisia arvoja ennen kuin liittyvä lohko päättyy. Listauksessa 21-21 lukko pysyy hallussa `job()`-kutsun keston ajan, mikä tarkoittaa, etteivät muut `Worker`-instanssit voi vastaanottaa töitä.

[creating-type-synonyms-with-type-aliases]: ch20-03-advanced-types.html#creating-type-synonyms-with-type-aliases
[integer-types]: ch03-02-data-types.html#integer-types
[fn-traits]: ch13-01-closures.html#moving-captured-values-out-of-the-closure-and-the-fn-traits
[builder]: ../std/thread/struct.Builder.html
[builder-spawn]: ../std/thread/struct.Builder.html#method.spawn
