## Koodin suorittaminen siivouksen yhteydessä `Drop`-traitin avulla

Toinen älykkäiden osoittimien mallin kannalta tärkeä trait on `Drop`, jonka avulla voit mukauttaa, mitä tapahtuu, kun arvo on poistumassa näkyvyysalueeltaan. Voit toteuttaa `Drop`-traitin mille tahansa tyypille, ja sitä voidaan käyttää resurssien, kuten tiedostojen tai verkkoyhteyksien, vapauttamiseen.

Esittelemme `Drop`-traitin älykkäiden osoittimien yhteydessä, koska `Drop`-traitin toiminnallisuutta käytetään lähes aina älykästä osoitinta toteutettaessa. Esimerkiksi kun `Box<T>` vapautetaan, se vapauttaa keon tilan, johon box osoittaa.

Joissakin kielissä ja joillekin tyypeille ohjelmoijan on kutsuttava koodia muistin tai resurssien vapauttamiseksi aina, kun hän lopettaa kyseisen tyypin instanssin käytön. Esimerkkejä ovat tiedostokahvat, soketit ja lukot. Jos ohjelmoija unohtaa tämän, järjestelmä voi ylikuormittua ja kaatua. Rustissa voit määrittää, että tietty koodi suoritetaan aina, kun arvo poistuu näkyvyysalueeltaan, ja kääntäjä lisää tämän koodin automaattisesti. Näin sinun ei tarvitse huolehtia siivouskoodin sijoittamisesta kaikkialle ohjelmaan, missä tietyn tyypin instanssi on käytetty loppuun — et silti vuoda resursseja!

Määrität koodin, joka suoritetaan arvon poistuessa näkyvyysalueeltaan, toteuttamalla `Drop`-traitin. `Drop`-trait vaatii yhden metodin nimeltä `drop`, joka ottaa muuttuvan viitteen `self`:iin. Nähdäksemme, milloin Rust kutsuu `drop`:ia, toteutetaan `drop` toistaiseksi `println!`-lauseilla.

Listauksessa 15-14 on `CustomSmartPointer`-struct, jonka ainoa mukautettu toiminnallisuus on tulostaa `Dropping CustomSmartPointer!`, kun instanssi poistuu näkyvyysalueeltaan, jotta näemme, milloin Rust suorittaa `drop`-metodin.

<Listing number="15-14" file-name="src/main.rs" caption="`CustomSmartPointer`-struct, joka toteuttaa `Drop`-traitin ja johon voisimme sijoittaa siivouskoodimme">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-14/src/main.rs}}
```

</Listing>

`Drop`-trait sisältyy preludiin, joten meidän ei tarvitse tuoda sitä näkyvyysalueelle. Toteutamme `Drop`-traitin `CustomSmartPointer`:lle ja annamme `drop`-metodille toteutuksen, joka kutsuu `println!`:ää. `drop`-metodin runkoon sijoitettaisiin logiikka, jonka haluaisit suorittaa, kun tyypin instanssi poistuu näkyvyysalueeltaan. Tulostamme tässä tekstiä havainnollistamaan visuaalisesti, milloin Rust kutsuu `drop`:ia.

`main`-funktiossa luomme kaksi `CustomSmartPointer`-instanssia ja tulostamme sitten `CustomSmartPointers created`. `main`-funktion lopussa `CustomSmartPointer`-instanssimme poistuvat näkyvyysalueeltaan, ja Rust kutsuu `drop`-metodiin sijoittamaamme koodia tulostaen viimeisen viestimme. Huomaa, ettemme tarvinneet kutsua `drop`-metodia erikseen.

Kun ajamme tämän ohjelman, näemme seuraavan tulosteen:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-14/output.txt}}
```

Rust kutsui `drop`:ia automaattisesti, kun instanssimme poistuivat näkyvyysalueeltaan, ja suoritti määrittämämme koodin. Muuttujat vapautetaan käänteisessä luontijärjestyksessä, joten `d` vapautettiin ennen `c`:tä. Tämän esimerkin tarkoitus on antaa visuaalinen opas siihen, miten `drop`-metodi toimii; yleensä määrittäisit tyypillesi tarvittavan siivouskoodin tulostusviestin sijaan.

<!-- Old headings. Do not remove or links may break. -->

<a id="dropping-a-value-early-with-std-mem-drop"></a>

Valitettavasti automaattisen `drop`-toiminnallisuuden poistaminen käytöstä ei ole suoraviivaista. `drop`:in poistaminen käytöstä ei yleensä ole tarpeen; `Drop`-traitin koko pointti on, että siitä huolehditaan automaattisesti. Joskus kuitenkin saatat haluta siivota arvon aikaisin. Esimerkki on lukkoja hallitsevien älykkäiden osoittimien käyttö: saatat haluta pakottaa `drop`-metodin, joka vapauttaa lukon, jotta muu koodi samassa näkyvyysalueessa voi hankkia lukon. Rust ei anna sinun kutsua `Drop`-traitin `drop`-metodia käsin; sen sijaan sinun on kutsuttava standardikirjaston tarjoamaa `std::mem::drop`-funktiota, jos haluat pakottaa arvon vapauttamisen ennen näkyvyysalueen loppua.

Yritys kutsua `Drop`-traitin `drop`-metodia käsin muokkaamalla listauksen 15-14 `main`-funktiota ei toimi, kuten listauksessa 15-15 näytetään.

<Listing number="15-15" file-name="src/main.rs" caption="Yritys kutsua `Drop`-traitin `drop`-metodia käsin aikaiseen siivoukseen">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-15/src/main.rs:here}}
```

</Listing>

Kun yritämme kääntää tämän koodin, saamme tämän virheen:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-15/output.txt}}
```

Tämä virheilmoitus kertoo, ettemme saa kutsua `drop`:ia eksplisiittisesti. Virheilmoituksessa käytetään termiä _destructor_ (destruktori), joka on yleinen ohjelmointitermi instanssin siivoavalle funktiolle. _Destruktori_ vastaa _konstruktoria_, joka luo instanssin. Rustin `drop`-funktio on yksi tietty destruktori.

Rust ei anna meidän kutsua `drop`:ia eksplisiittisesti, koska Rust kutsuisi silti `drop`:ia automaattisesti arvolle `main`-funktion lopussa. Tämä aiheuttaisi _double free_ -virheen, koska Rust yrittäisi siivota saman arvon kahdesti.

Emme voi poistaa käytöstä automaattista `drop`-lisäystä arvon poistuessa näkyvyysalueeltaan, emmekä voi kutsua `drop`-metodia eksplisiittisesti. Jos meidän täytyy pakottaa arvon siivous aikaisin, käytämme `std::mem::drop`-funktiota.

`std::mem::drop`-funktio eroaa `Drop`-traitin `drop`-metodista. Kutsumme sitä välittämällä argumenttina arvon, jonka haluamme pakottaa vapautettavaksi. Funktio on preludissa, joten voimme muokata listauksen 15-15 `main`-funktiota kutsumaan `drop`-funktiota, kuten listauksessa 15-16.

<Listing number="15-16" file-name="src/main.rs" caption="`std::mem::drop`-funktion kutsuminen arvon eksplisiittiseen vapauttamiseen ennen näkyvyysalueen loppua">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-16/src/main.rs:here}}
```

</Listing>

Tämän koodin ajaminen tulostaa seuraavaa:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-16/output.txt}}
```

Teksti ``Dropping CustomSmartPointer with data `some data`!`` tulostuu `CustomSmartPointer created`- ja `CustomSmartPointer dropped before the end of main` -tekstien väliin, mikä osoittaa, että `drop`-metodin koodi kutsutaan vapauttamaan `c` tuossa vaiheessa.

Voit käyttää `Drop`-traitin toteutuksessa määriteltyä koodia monin tavoin tehdäksesi siivouksesta kätevää ja turvallista: voisit esimerkiksi luoda oman muistinhallintajärjestelmän! `Drop`-traitin ja Rustin omistajuusjärjestelmän ansiosta sinun ei tarvitse muistaa siivota, koska Rust tekee sen automaattisesti.

Sinun ei myöskään tarvitse huolehtia ongelmista, jotka johtuvat vahingossa käytössä olevien arvojen siivoamisesta: omistajuusjärjestelmä, joka varmistaa viitteiden kelpoisuuden, varmistaa myös, että `drop` kutsutaan vain kerran, kun arvoa ei enää käytetä.

Nyt kun olemme tarkastelleet `Box<T>`:tä ja joitakin älykkäiden osoittimien ominaisuuksia, katsomme muutamia muita standardikirjaston määrittelemiä älykkäitä osoittimia.
