<!-- Old headings. Do not remove or links may break. -->

<a id="concurrency-with-async"></a>

## Samanaikaisuuden soveltaminen asyncilla

Tässä osiossa sovellamme asyncia joihinkin samoihin samanaikaisuushaasteisiin, joita käsittelimme säikeillä luvussa 16. Koska käsittelimme siellä jo monia keskeisiä ideoita, keskitymme tässä osiossa siihen, mikä eroaa säikeiden ja futurejen välillä.

Monissa tapauksissa asyncilla työskentelyn API:t ovat hyvin samankaltaisia kuin säikeillä työskentelyn API:t. Toisissa tapauksissa ne ovat hyvin erilaisia. Vaikka API:t _näyttäisivät_ samankaltaisilta säikeiden ja asyncin välillä, niillä on usein erilainen käyttäytyminen — ja niillä on lähes aina erilaiset suorituskykyominaisuudet.

<!-- Old headings. Do not remove or links may break. -->

<a id="counting"></a>

### Uuden tehtävän luominen `spawn_task`:illa

Ensimmäinen operaatio, jota käsittelimme [”Uuden säikeen luominen `spawn`:illa”][thread-spawn]<!-- ignore --> -osiossa luvussa 16, oli laskeminen kahdella erillisellä säikeellä. Tehdään sama asyncilla. `trpl`-crate tarjoaa `spawn_task`-funktion, joka näyttää hyvin samankaltaiselta kuin `thread::spawn`-API, ja `sleep`-funktion, joka on async-versio `thread::sleep`-API:sta. Voimme käyttää näitä yhdessä laskuesimerkin toteuttamiseen, kuten listauksessa 17-6.

<Listing number="17-6" caption="Uuden tehtävän luominen tulostamaan yhtä asiaa, kun päätehtävä tulostaa jotain muuta" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-06/src/main.rs:all}}
```

</Listing>

Lähtökohtanamme asetamme `main`-funktion `trpl::block_on`:illa, jotta ylätason funktiomme voi olla async.

> Huom: Tästä eteenpäin luvussa jokainen esimerkki sisältää täsmälleen saman käärintäkoodin `trpl::block_on`:illa `main`:issa, joten ohitamme sen usein samalla tavalla kuin `main`:in. Muista sisällyttää se koodiisi!

Sitten kirjoitamme kaksi silmukkaa kyseisen lohkon sisään, joista kummassakin on `trpl::sleep`-kutsu, joka odottaa puoli sekuntia (500 millisekuntia) ennen seuraavan viestin lähettämistä. Sijoitamme yhden silmukan `trpl::spawn_task`:n runkoon ja toisen ylätason `for`-silmukkaan. Lisäämme myös `await`:in `sleep`-kutsujen jälkeen.

Tämä koodi käyttäytyy samankaltaisesti kuin säikeisiin perustuva toteutus — mukaan lukien se, että saatat nähdä viestien ilmestyvän eri järjestyksessä omassa terminaalissasi, kun suoritat sen:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the second task!
hi number 1 from the first task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
```

Tämä versio pysähtyy heti, kun pää-async-lohkon rungossa oleva `for`-silmukka päättyy, koska `spawn_task`:n luoma tehtävä sammutetaan, kun `main`-funktio päättyy. Jos haluat sen suorittuvan aina tehtävän valmistumiseen asti, tarvitset join-kahvan odottamaan ensimmäisen tehtävän valmistumista. Säikeillä käytimme `join`-metodia ”estääksemme” säikeen valmistumiseen asti. Listauksessa 17-7 voimme käyttää `await`:ia samaan tarkoitukseen, koska tehtäväkahva itsessään on future. Sen `Output`-tyyppi on `Result`, joten puramme sen myös `await`:in jälkeen.

<Listing number="17-7" caption="`await`:in käyttö join-kahvan kanssa tehtävän suorittamiseksi loppuun" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-07/src/main.rs:handle}}
```

</Listing>

Tämä päivitetty versio suorittaa, kunnes _molemmat_ silmukat päättyvät:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the second task!
hi number 1 from the first task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
hi number 6 from the first task!
hi number 7 from the first task!
hi number 8 from the first task!
hi number 9 from the first task!
```

Tähän mennessä näyttää siltä, että async ja säikeet antavat samankaltaiset tulokset, vain eri syntaksilla: `await`:in käyttö `join`-kutsun sijaan join-kahvalla ja `sleep`-kutsujen odottaminen.

Suurempi ero on se, että emme tarvinneet luoda toista käyttöjärjestelmän säiettä tähän. Itse asiassa emme edes tarvitse luoda tehtävää tässä. Koska async-lohkot käännetään nimettömiksi futureiksi, voimme sijoittaa kummankin silmukan async-lohkoon ja antaa ajoympäristön suorittaa molemmat loppuun `trpl::join`-funktiolla.

[”Kaikkien säikeiden valmistumisen odottaminen”][join-handles]<!-- ignore --> -osiossa luvussa 16 näytimme, miten `join`-metodia käytetään `std::thread::spawn`:in palauttaman `JoinHandle`-tyypin kanssa. `trpl::join`-funktio on samankaltainen, mutta futureille. Kun annat sille kaksi futurea, se tuottaa yhden uuden futuren, jonka tulos on monikko kummankin välittämäsi futuren tuloksista, kun ne _molemmat_ ovat valmiita. Näin listauksessa 17-8 käytämme `trpl::join`:ia odottamaan sekä `fut1`:n että `fut2`:n valmistumista. Emme odota `fut1`:tä ja `fut2`:tä, vaan `trpl::join`:n tuottamaa uutta futurea. Jätämme tuloksen huomiotta, koska se on vain monikko, joka sisältää kaksi yksikköarvoa.

<Listing number="17-8" caption="`trpl::join`:in käyttö kahden nimettömän futuren odottamiseen" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-08/src/main.rs:join}}
```

</Listing>

Kun suoritamme tämän, näemme molempien futurejen suorittuvan loppuun:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the first task!
hi number 1 from the second task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
hi number 6 from the first task!
hi number 7 from the first task!
hi number 8 from the first task!
hi number 9 from the first task!
```

Nyt näet täsmälleen saman järjestyksen joka kerta, mikä on hyvin erilaista kuin säikeillä ja `trpl::spawn_task`:illa listauksessa 17-7. Tämä johtuu siitä, että `trpl::join`-funktio on _reilu_: se tarkistaa kummankin futuren yhtä usein, vuorotellen niitä, eikä koskaan anna toisen edetä, jos toinen on valmis. Säikeillä käyttöjärjestelmä päättää, mitä säiettä tarkistaa ja kuinka kauan antaa sen suorittaa. Async-Rustissa ajoympäristö päättää, mitä tehtävää tarkistaa. (Käytännössä yksityiskohdat monimutkaistuvat, koska async-ajoympäristö voi käyttää käyttöjärjestelmän säikeitä taustalla osana samanaikaisuuden hallintaa, joten reiluuden takaaminen voi olla ajoympäristölle enemmän työtä — mutta se on silti mahdollista!) Ajoympäristöjen ei tarvitse taata reiluutta millekään operaatiolle, ja ne tarjoavat usein eri API:ja, joiden avulla voit valita, haluatko reiluutta.

Kokeile joitakin näistä variaatioista futurejen odottamisessa ja katso, mitä ne tekevät:

- Poista async-lohko kummankin tai molempien silmukoiden ympäriltä.
- Odota kumpaakin async-lohkoa heti sen määrittelyn jälkeen.
- Kääri vain ensimmäinen silmukka async-lohkoon ja odota tuloksena olevaa futurea toisen silmukan rungon jälkeen.

Lisähaasteena katso, osaatko päätellä, mikä tuloste on kussakin tapauksessa _ennen_ koodin suorittamista!

<!-- Old headings. Do not remove or links may break. -->

<a id="message-passing"></a>
<a id="counting-up-on-two-tasks-using-message-passing"></a>

### Datan lähettäminen kahden tehtävän välillä viestinvälityksellä

Datan jakaminen futurejen välillä on myös tuttua: käytämme jälleen viestinvälitystä, mutta tällä kertaa async-versioita tyypeistä ja funktioista. Kuljemme hieman eri polkua kuin [”Datan siirtäminen säikeiden välillä viestinvälityksellä”][message-passing-threads]<!-- ignore --> -osiossa luvussa 16 havainnollistaaksemme keskeisiä eroja säikeisiin ja futureihin perustuvan samanaikaisuuden välillä. Listauksessa 17-9 aloitamme vain yhdellä async-lohkolla — _emme_ luo erillistä tehtävää kuten loimme erillisen säikeen.

<Listing number="17-9" caption="Async-kanavan luominen ja kahden puoliskon antaminen `tx`:lle ja `rx`:lle" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-09/src/main.rs:channel}}
```

</Listing>

Tässä käytämme `trpl::channel`:ia, async-version monituottaja-yksittäiskuluttaja-kanava-API:sta, jota käytimme säikeillä luvussa 16. Async-versio API:sta eroaa vain vähän säikeisiin perustuvasta versiosta: se käyttää muuttuvaa eikä muuttumatonta vastaanottajaa `rx`:ää, ja sen `recv`-metodi tuottaa futuren, jota meidän täytyy odottaa, sen sijaan että se tuottaisi arvon suoraan. Nyt voimme lähettää viestejä lähettäjältä vastaanottajalle. Huomaa, että emme tarvitse luoda erillistä säiettä tai edes tehtävää; meidän täytyy vain odottaa `rx.recv`-kutsua.

Synkroninen `Receiver::recv`-metodi `std::mpsc::channel`:issa estää, kunnes se vastaanottaa viestin. `trpl::Receiver::recv`-metodi ei estä, koska se on async. Sen sijaan että estäisi, se palauttaa ohjauksen ajoympäristölle, kunnes viesti vastaanotetaan tai kanavan lähetyspuoli sulkeutuu. Sitä vastoin emme odota `send`-kutsua, koska se ei estä. Sen ei tarvitse, koska kanava, johon lähetämme, on rajoittamaton.

> Huom: Koska kaikki tämä async-koodi suoritetaan async-lohkossa `trpl::block_on`-kutsussa, kaikki sen sisällä voi välttää estämisen. Koodi _sen ulkopuolella_ kuitenkin estyy, kunnes `block_on`-funktio palaa. Siinä on koko `trpl::block_on`-funktion idea: sen avulla voit _valita_, missä estät jonkin async-koodin joukon, ja siten missä siirryt synkronisen ja asynkronisen koodin välillä.

Huomaa tästä esimerkistä kaksi asiaa. Ensinnäkin viesti saapuu heti. Toiseksi, vaikka käytämme tässä futurea, samanaikaisuutta ei vielä ole. Kaikki listauksessa tapahtuu peräkkäin, aivan kuten ilman futureja.

Käsitellään ensimmäinen osa lähettämällä sarja viestejä ja nukkumalla niiden välissä, kuten listauksessa 17-10.

<!-- We cannot test this one because it never stops! -->

<Listing number="17-10" caption="Useiden viestien lähettäminen ja vastaanottaminen async-kanavan yli ja nukkuminen `await`:illa jokaisen viestin välissä" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-10/src/main.rs:many-messages}}
```

</Listing>

Viestien lähettämisen lisäksi meidän täytyy vastaanottaa ne. Tässä tapauksessa, koska tiedämme kuinka monta viestiä on tulossa, voisimme tehdä sen käsin kutsumalla `rx.recv().await` neljä kertaa. Oikeassa maailmassa odotamme kuitenkin yleensä _tuntemattoman_ määrän viestejä, joten meidän täytyy odottaa, kunnes päätämme, ettei viestejä enää tule.

Listauksessa 16-10 käytimme `for`-silmukkaa käsittelemään kaikki synkronisesta kanavasta vastaanotetut kohteet. Rustilla ei kuitenkaan ole vielä tapaa käyttää `for`-silmukkaa _asynkronisesti tuotetun_ kohteiden sarjan kanssa, joten meidän täytyy käyttää silmukkaa, jota emme ole vielä nähneet: `while let` -ehdosilmukkaa. Tämä on silmukkaversio `if let` -rakenteesta, jonka näimme [”Tiivis ohjausvirta `if let`:illä ja `let...else`:llä”][if-let]<!-- ignore --> -osiossa luvussa 6. Silmukka jatkaa suorittamista niin kauan kuin sen määrittelemä kuvio vastaa edelleen arvoa.

`rx.recv`-kutsu tuottaa futuren, jota odotamme. Ajoympäristö keskeyttää futuren, kunnes se on valmis. Kun viesti saapuu, future ratkeaa `Some(message)`-arvoksi niin monta kertaa kuin viestejä saapuu. Kun kanava sulkeutuu — riippumatta siitä, ovatko _mitkään_ viestit saapuneet — future ratkeaa sen sijaan `None`:ksi ilmaisemaan, ettei arvoja ole enempää ja että meidän pitäisi lopettaa pollaus — eli lopettaa odottaminen.

`while let` -silmukka yhdistää kaiken tämän. Jos `rx.recv().await`:in tulos on `Some(message)`, saamme käyttöön viestin ja voimme käyttää sitä silmukan rungossa, aivan kuten `if let`:illä. Jos tulos on `None`, silmukka päättyy. Joka kerta kun silmukka suoritetaan loppuun, se osuu odotuspisteeseen uudelleen, joten ajoympäristö keskeyttää sen uudelleen, kunnes toinen viesti saapuu.

Koodi lähettää ja vastaanottaa nyt onnistuneesti kaikki viestit. Valitettavasti on vielä pari ongelmaa. Ensinnäkin viestit eivät saavu puolen sekunnin välein. Ne saapuvat kaikki kerralla 2 sekunnin (2 000 millisekunnin) kuluttua ohjelman käynnistymisestä. Toiseksi tämä ohjelma ei myöskään koskaan päätty! Sen sijaan se odottaa ikuisesti uusia viestejä. Sinun täytyy sammuttaa se painamalla <kbd>ctrl</kbd>-<kbd>C</kbd>.

#### Yhden async-lohkon sisällä oleva koodi suoritetaan lineaarisesti

Aloitetaan tutkimalla, miksi viestit saapuvat kaikki kerralla koko viiveen jälkeen sen sijaan, että ne saapuisivat viivein välein. Tietyssä async-lohkossa `await`-avainsanojen esiintymisjärjestys koodissa on myös järjestys, jossa ne suoritetaan ohjelman käydessä.

Listauksessa 17-10 on vain yksi async-lohko, joten kaikki sen sisällä suoritetaan lineaarisesti. Samanaikaisuutta ei vieläkään ole. Kaikki `tx.send`-kutsut tapahtuvat vuorotellen kaikkien `trpl::sleep`-kutsujen ja niihin liittyvien odotuspisteiden kanssa. Vasta sitten `while let` -silmukka pääsee käymään läpi mitään `recv`-kutsujen odotuspisteitä.

Saadaksemme haluamamme käyttäytymisen, jossa nukkumisviive tapahtuu jokaisen viestin välissä, meidän täytyy sijoittaa `tx`- ja `rx`-operaatiot omiin async-lohkoihinsa, kuten listauksessa 17-11. Sitten ajoympäristö voi suorittaa kummankin erikseen käyttämällä `trpl::join`:ia, aivan kuten listauksessa 17-8. Taas odotamme `trpl::join`:in kutsumisen tulosta, emme yksittäisiä futureja. Jos odottaisimme yksittäisiä futureja peräkkäin, päätyisimme takaisin peräkkäiseen kulkuun — juuri sitä, mitä yritämme _välttää_.

<!-- We cannot test this one because it never stops! -->

<Listing number="17-11" caption="`send`- ja `recv`-operaatioiden erottaminen omiin `async`-lohkoihinsa ja näiden lohkojen futurejen odottaminen" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-11/src/main.rs:futures}}
```

</Listing>

Listauksen 17-11 päivitetyllä koodilla viestit tulostetaan 500 millisekunnin välein sen sijaan, että ne tulostuisivat kaikki kerralla 2 sekunnin kuluttua.

#### Omistajuuden siirtäminen async-lohkoon

Ohjelma ei kuitenkaan vieläkään päätty, koska `while let` -silmukan ja `trpl::join`:in vuorovaikutus:

- `trpl::join`:in palauttama future valmistuu vasta, kun _molemmat_ sille välitetyt futuret ovat valmiita.
- `tx_fut`-future valmistuu, kun se on nukkunut viimeisen viestin lähettämisen jälkeen `vals`:issa.
- `rx_fut`-future ei valmistu, ennen kuin `while let` -silmukka päättyy.
- `while let` -silmukka ei päätty, ennen kuin `rx.recv`:n odottaminen tuottaa `None`:n.
- `rx.recv`:n odottaminen palauttaa `None`:n vain, kun kanavan toinen pää on suljettu.
- Kanava sulkeutuu vain, jos kutsumme `rx.close`:a tai kun lähettäjäpuoli `tx` pudotetaan.
- Emme kutsu `rx.close`:a missään, eikä `tx` pudotu ennen kuin `trpl::block_on`:ille välitetty ulompi async-lohko päättyy.
- Lohko ei voi päättyä, koska se on estynyt `trpl::join`:in valmistumiseen, mikä vie meidät takaisin tämän listan alkuun.

Tällä hetkellä viestejä lähettävä async-lohko vain _lainaa_ `tx`:ää, koska viestin lähettäminen ei vaadi omistajuutta, mutta jos voisimme _siirtää_ `tx`:n kyseiseen async-lohkoon, se pudotettaisiin, kun lohko päättyy. [”Viittausten kaappaaminen tai omistajuuden siirtäminen”][capture-or-move]<!-- ignore --> -osiossa luvussa 13 opit käyttämään `move`-avainsanaa sulkeumien kanssa, ja kuten käsiteltiin [”`move`-sulkeumien käyttö säikeiden kanssa”][move-threads]<!-- ignore --> -osiossa luvussa 16, meidän täytyy usein siirtää data sulkeumiin säikeillä työskennellessä. Sama perusdynamiikka pätee async-lohkoihin, joten `move`-avainsana toimii async-lohkojen kanssa samalla tavalla kuin sulkeumien kanssa.

Listauksessa 17-12 muutamme viestien lähettämiseen käytetyn lohkon muodosta `async` muotoon `async move`.

<Listing number="17-12" caption="Listauksen 17-11 koodin versio, joka sammuttuu oikein valmistuttuaan" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-12/src/main.rs:with-move}}
```

</Listing>

Kun suoritamme _tämän_ version koodista, se sammuttuu siististi viimeisen viestin lähettämisen ja vastaanottamisen jälkeen. Seuraavaksi katsotaan, mitä pitäisi muuttaa lähettääksemme dataa useammasta kuin yhdestä futuresta.

#### Usean futuren yhdistäminen `join!`-makrolla

Tämä async-kanava on myös monituottaja-kanava, joten voimme kutsua `clone`:a `tx`:lle, jos haluamme lähettää viestejä useista futureista, kuten listauksessa 17-13.

<Listing number="17-13" caption="Usean tuottajan käyttö async-lohkojen kanssa" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-13/src/main.rs:here}}
```

</Listing>

Ensin kloonaamme `tx`:n luoden `tx1`:n ensimmäisen async-lohkon ulkopuolelle. Siirrämme `tx1`:n kyseiseen lohkoon kuten aiemmin `tx`:n kanssa. Sitten myöhemmin siirrämme alkuperäisen `tx`:n _uuteen_ async-lohkoon, jossa lähetämme lisää viestejä hieman hitaammalla viiveellä. Sijoitamme tämän uuden async-lohkon vastaanottavaan async-lohkoon jälkeen, mutta se voisi olla yhtä hyvin ennen sitä. Ratkaisevaa on järjestys, jossa futureja odotetaan, ei järjestys, jossa ne luodaan.

Molempien viestejä lähettävien async-lohkojen täytyy olla `async move` -lohkoja, jotta sekä `tx` että `tx1` pudotetaan, kun lohkot päättyvät. Muuten päädymme takaisin samaan loputtomaan silmukkaan, jossa aloitimme.

Lopuksi vaihdamme `trpl::join`:ista `trpl::join!`:iin käsitelläksemme lisäfuturen: `join!`-makro odottaa mielivaltaisen määrän futureja, joiden määrä tiedetään kääntöaikana. Käsittelemme tuntemattoman määrän futureja myöhemmin tässä luvussa.

Nyt näemme kaikki viestit molemmista lähettävistä futureista, ja koska lähettävät futuret käyttävät hieman erilaisia viiveitä lähettämisen jälkeen, viestit vastaanotetaan myös näillä eri väleillä:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
received 'hi'
received 'more'
received 'from'
received 'the'
received 'messages'
received 'future'
received 'for'
received 'you'
```

Olemme tutkineet, miten viestinvälitystä käytetään datan lähettämiseen futurejen välillä, miten async-lohkon sisällä oleva koodi suoritetaan peräkkäin, miten omistajuus siirretään async-lohkoon ja miten useita futureja yhdistetään. Seuraavaksi keskustellaan siitä, miten ja miksi kerrotaan ajoympäristölle, että se voi vaihtaa toiseen tehtävään.

[thread-spawn]: ch16-01-threads.html#creating-a-new-thread-with-spawn
[join-handles]: ch16-01-threads.html#waiting-for-all-threads-to-finish
[message-passing-threads]: ch16-02-message-passing.html
[if-let]: ch06-03-if-let.html
[capture-or-move]: ch13-01-closures.html#capturing-references-or-moving-ownership
[move-threads]: ch16-01-threads.html#using-move-closures-with-threads
