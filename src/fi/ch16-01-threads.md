## Säikeiden käyttö koodin samanaikaiseen suorittamiseen

Useimmissa nykyisissä käyttöjärjestelmissä suoritetun ohjelman koodi ajetaan _prosessissa_, ja käyttöjärjestelmä hallinnoi useita prosesseja samanaikaisesti. Ohjelman sisällä voit myös olla itsenäisiä osia, jotka suorittavat tehtäviään samanaikaisesti. Näitä itsenäisiä osia suorittavia ominaisuuksia kutsutaan _säikeiksi_. Esimerkiksi verkkopalvelimella voi olla useita säikeitä, jotta se voi vastata useampaan kuin yhteen pyyntöön samanaikaisesti.

Ohjelmasi laskennan jakaminen useisiin säikeisiin useiden tehtävien samanaikaiseen suorittamiseen voi parantaa suorituskykyä, mutta se lisää myös monimutkaisuutta. Koska säikeet voivat suorittaa tehtäviään samanaikaisesti, ei ole luontaista takeetta siitä, missä järjestyksessä koodin eri osat eri säikeillä suoritetaan. Tämä voi johtaa ongelmiin, kuten:

- Kilpailutilanteisiin (_race conditions_), joissa säikeet käyttävät dataa tai resursseja epäjohdonmukaisessa järjestyksessä
- Lukoittumisiin (_deadlocks_), joissa kaksi säiettä odottaa toisiaan, estäen molempia jatkamasta
- Vikoihin, jotka ilmenevät vain tietyissä tilanteissa ja joita on vaikea toistaa ja korjata luotettavasti

Rust yrittää lieventää säikeiden käytön haitallisia vaikutuksia, mutta monisäikeisessä kontekstissa ohjelmointi vaatii silti huolellista pohdintaa ja koodirakennetta, joka poikkeaa yksisäikeisissä ohjelmissa käytetystä.

Ohjelmointikielet toteuttavat säikeet eri tavoin, ja monet käyttöjärjestelmät tarjoavat ohjelmointirajapinnan (API), jota kieli voi kutsua uusien säikeiden luomiseksi. Rustin standardikirjasto käyttää _1:1_-säiemallia, jossa ohjelma käyttää yhtä käyttöjärjestelmän säiettä jokaista kielen säiettä kohden. On olemassa kirjastoja, jotka toteuttavat muita säiemalleja ja tekevät erilaisia kompromisseja verrattuna 1:1-malliin. (Rustin asynkroninen järjestelmä, jota käsittelemme seuraavassa luvussa, tarjoaa toisen lähestymistavan rinnakkaisuuteen.)

### Uuden säikeen luominen `spawn`-funktiolla

Uuden säikeen luomiseksi kutsumme `thread::spawn`-funktiota ja annamme sille sulkeisen (sulkeisista puhuttiin luvussa 13), joka sisältää uudessa säikeessä ajettavan koodin. Esimerkissä 16-1 pääsäie tulostaa tekstiä ja samanaikaisesti luotu säie tulostaa omaa tekstiään.

<Listing number="16-1" file-name="src/main.rs" caption="Uuden säikeen luominen tulostamaan yhtä asiaa, kun pääsäie tulostaa jotain muuta">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-01/src/main.rs}}
```

</Listing>

Huomaa, että kun Rust-ohjelman pääsäie päättyy, kaikki luodut säikeet lopetetaan, riippumatta siitä, ovatko ne suorittaneet kaiken työnsä loppuun. Tämän ohjelman tuloste voi olla hieman erilainen joka kerralla, mutta se näyttää suunnilleen tältä:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the main thread!
hi number 1 from the spawned thread!
hi number 2 from the main thread!
hi number 2 from the spawned thread!
hi number 3 from the main thread!
hi number 3 from the spawned thread!
hi number 4 from the main thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
```

Kutsut `thread::sleep`-funktioon pakottavat säikeen pysähtymään hetkeksi, antaen toiselle säikeelle mahdollisuuden suorittaa tehtäviään. Säikeet todennäköisesti vuorottelevat, mutta tätä ei voida taata: se riippuu käyttöjärjestelmän säikeiden ajoituksesta. Tässä ajossa pääsäie tulosti ensin, vaikka luodun säikeen tulostuslauseke on koodissa ensimmäisenä. Ja vaikka käskimme luodun säikeen tulostaa, kunnes `i` saavuttaa arvon `9`, se pääsi vain `5`:een ennen kuin pääsäie lopetti ohjelman suorittamisen.

Jos ajat tämän koodin ja näet tulostetta vain pääsäikeeltä, tai et näe päällekkäisyyttä lainkaan, kokeile kasvattaa alueiden numeroita luodaksesi enemmän mahdollisuuksia käyttöjärjestelmälle vaihtaa säikeiden välillä.

<!-- Old headings. Do not remove or links may break. -->

<a id="waiting-for-all-threads-to-finish-using-join-handles"></a>

### Kaikkien säikeiden odottaminen

Listauksen 16-1 koodi ei ainoastaan lopeta luotua säiettä ennenaikaisesti useimmiten pääsäikeen päättymisen vuoksi, vaan koska säikeiden suoritusjärjestyksestä ei ole takeetta, emme voi myöskään taata, että luotu säie ehtii suorittaa lainkaan!

Voimme korjata ongelman, jossa luotu säie ei ehdi suorittaa tai päättyy ennenaikaisesti, tallentamalla `thread::spawn`-funktion paluuarvon muuttujaan. `thread::spawn`-funktion paluutyyppi on `JoinHandle<T>`. `JoinHandle<T>` on omistettu arvo, joka kun kutsumme sen `join`-metodia, odottaa säikeen päättymistä. Listausta 16-2 näyttää, miten käytämme listauksessa 16-1 luodun säikeen `JoinHandle<T>`-kahvaa ja kutsumme `join`-metodia varmistaaksemme, että luotu säie päättyy ennen kuin `main` lopettaa.

<Listing number="16-2" file-name="src/main.rs" caption="`JoinHandle<T>`-kahvan tallentaminen `thread::spawn`-funktiosta varmistaaksemme, että säie ajetaan loppuun">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-02/src/main.rs}}
```

</Listing>

`join`-metodin kutsuminen kahvassa _estää_ (_blocks_) tällä hetkellä suoritettavan säikeen, kunnes kahvan edustama säie päättyy. Säikeen estäminen tarkoittaa, että säie ei voi suorittaa työtä tai lopettaa. Koska olemme sijoittaneet `join`-kutsun pääsäikeen `for`-silmukan jälkeen, listauksen 16-2 ajaminen pitäisi tuottaa suunnilleen tämänkaltaisen tulosteen:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the main thread!
hi number 2 from the main thread!
hi number 1 from the spawned thread!
hi number 3 from the main thread!
hi number 2 from the spawned thread!
hi number 4 from the main thread!
hi number 3 from the spawned thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
hi number 6 from the spawned thread!
hi number 7 from the spawned thread!
hi number 8 from the spawned thread!
hi number 9 from the spawned thread!
```

Kaksi säiettä jatkavat vuorottelemista, mutta pääsäie odottaa `handle.join()`-kutsun vuoksi eikä lopeta ennen kuin luotu säie on valmis.

Mutta katsotaanpa, mitä tapahtuu, jos siirrämme `handle.join()`-kutsun `main`-funktion `for`-silmukan _ennen_, näin:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/no-listing-01-join-too-early/src/main.rs}}
```

</Listing>

Pääsäie odottaa luodun säikeen päättymistä ja ajaa sitten `for`-silmukkansa, joten tuloste ei enää vuorottele, kuten tässä:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the spawned thread!
hi number 2 from the spawned thread!
hi number 3 from the spawned thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
hi number 6 from the spawned thread!
hi number 7 from the spawned thread!
hi number 8 from the spawned thread!
hi number 9 from the spawned thread!
hi number 1 from the main thread!
hi number 2 from the main thread!
hi number 3 from the main thread!
hi number 4 from the main thread!
```

Pienillä yksityiskohdilla, kuten siitä, missä `join` kutsutaan, voi olla vaikutusta siihen, suoritetaanko säikeitä samanaikaisesti vai ei.

### `move`-sulkeisten käyttö säikeiden kanssa

Käytämme usein `move`-avainsanaa `thread::spawn`-funktiolle välitettyjen sulkeisten kanssa, koska sulkeis ottaa silloin omistajuuden käyttämistään arvoista ympäristöstään, siirtäen näiden arvojen omistajuuden säikeestä toiseen. [”Viitteiden kaappaaminen tai omistajuuden siirtäminen”][capture]<!-- ignore --> -osiossa luvussa 13 käsittelimme `move`-avainsanaa sulkeisten kontekstissa. Nyt keskitymme enemmän `move`-avainsanan ja `thread::spawn`-funktion vuorovaikutukseen.

Huomaa listauksessa 16-1, että `thread::spawn`-funktiolle välittämämme sulkeis ei ota parametreja: emme käytä mitään dataa pääsäikeestä luodun säikeen koodissa. Käyttääksemme dataa pääsäikeestä luodussa säikeessä luodun säikeen sulkeisen täytyy kaapata tarvitsemansa arvot. Listausta 16-3 näyttää yrityksen luoda vektori pääsäikeessä ja käyttää sitä luodussa säikeessä. Tämä ei kuitenkaan vielä toimi, kuten näet hetken kuluttua.

<Listing number="16-3" file-name="src/main.rs" caption="Yritys käyttää pääsäikeen luomaa vektoria toisessa säikeessä">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-03/src/main.rs}}
```

</Listing>

Sulkeis käyttää `v`-muuttujaa, joten se kaappaa `v`:n ja tekee siitä osan sulkeisen ympäristöä. Koska `thread::spawn` suorittaa tämän sulkeisen uudessa säikeessä, meidän pitäisi pystyä käyttämään `v`:tä kyseisessä uudessa säikeessä. Mutta kun käännetään tämä esimerkki, saamme seuraavan virheen:

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-03/output.txt}}
```

Rust _päättelee_, miten `v` kaapataan, ja koska `println!` tarvitsee vain viitteen `v`:hen, sulkeis yrittää lainata `v`:tä. Ongelma on kuitenkin se, että Rust ei tiedä, kuinka kauan luotu säie ajaa, joten se ei tiedä, onko viite `v`:hen aina kelvollinen.

Listausta 16-4 tarjoaa skenaarion, jossa viite `v`:hen ei todennäköisesti ole kelvollinen.

<Listing number="16-4" file-name="src/main.rs" caption="Säie, jonka sulkeis yrittää kaapata viitteen `v`:hen pääsäikeestä, joka pudottaa `v`:n">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-04/src/main.rs}}
```

</Listing>

Jos Rust sallisi tämän koodin ajamisen, olisi mahdollista, että luotu säie laitettaisiin heti taustalle ajamatta lainkaan. Luodulla säikeellä on viite `v`:hen sisällään, mutta pääsäie pudottaa `v`:n heti käyttäen luvussa 15 käsittelemäämme `drop`-funktiota. Sitten kun luotu säie alkaa suorittaa, `v` ei ole enää kelvollinen, joten viite siihen on myös virheellinen. Voi ei!

Korjataksemme listauksen 16-3 kääntäjävirheen voimme käyttää virheilmoituksen neuvoa:

<!-- manual-regeneration
after automatic regeneration, look at listings/ch16-fearless-concurrency/listing-16-03/output.txt and copy the relevant part
-->

```text
help: to force the closure to take ownership of `v` (and any other referenced variables), use the `move` keyword
  |
6 |     let handle = thread::spawn(move || {
  |                                ++++
```

Lisäämällä `move`-avainsanan ennen sulkeista pakotamme sulkeisen ottamaan omistajuuden käyttämistään arvoista sen sijaan, että antaisimme Rustin päättää, että sen pitäisi lainata arvoja. Listausta 16-3 vastaava muutos listauksessa 16-5 kääntyy ja toimii tarkoitetulla tavalla.

<Listing number="16-5" file-name="src/main.rs" caption="`move`-avainsanan käyttö pakottaaksemme sulkeisen ottamaan omistajuuden käyttämistään arvoista">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-05/src/main.rs}}
```

</Listing>

Saatamme olla halukkaita kokeilemaan samaa korjausta listauksen 16-4 koodiin, jossa pääsäie kutsui `drop`-funktiota käyttämällä `move`-sulkeista. Tämä korjaus ei kuitenkaan toimi, koska se, mitä listaus 16-4 yrittää tehdä, on kielletty eri syystä. Jos lisäisimme `move`-avainsanan sulkeiseen, siirtäisimme `v`:n sulkeisen ympäristöön emmekä voisi enää kutsua `drop`-funktiota pääsäikeessä. Saisimme sen sijaan tämän kääntäjävirheen:

```console
{{#include ../listings/ch16-fearless-concurrency/output-only-01-move-drop/output.txt}}
```

Rustin omistajuussäännöt pelastivat meidät jälleen! Saimme virheen listauksen 16-3 koodista, koska Rust oli varovainen ja lainasi `v`:tä vain säikeelle, mikä tarkoitti, että pääsäie saattoi teoriassa mitätöidä luodun säikeen viitteen. Kertomalla Rustille siirtämään `v`:n omistajuuden luodulle säikeelle takaamme Rustille, että pääsäie ei enää käytä `v`:tä. Jos muuttaisimme listauksen 16-4 samalla tavalla, rikkoisimme omistajuussääntöjä yrittäessämme käyttää `v`:tä pääsäikeessä. `move`-avainsana ohittaa Rustin varovaisen oletuslainaamisen; se ei anna meidän rikkoa omistajuussääntöjä.

Nyt kun olemme käsitelleet säikeet ja säikeiden API:n tarjoamat metodit, katsotaan joitakin tilanteita, joissa säikeitä voi käyttää.

[capture]: ch13-01-closures.html#capturing-references-or-moving-ownership
