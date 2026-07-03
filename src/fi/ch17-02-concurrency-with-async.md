## Rinnakkaisuuden soveltaminen asyncilla

<!-- Old headings. Do not remove or links may break. -->

<a id="concurrency-with-async"></a>

Tässä osiossa sovellamme asyncia samoihin rinnakkaisuushaasteisiin, joita
käsittelimme säikeillä luvussa 16. Koska käsittelimme siellä jo monia keskeisiä
ideoita, tässä osiossa keskitymme siihen, mikä eroaa säikeiden ja futuresien
välillä.

Monissa tapauksissa asyncilla rinnakkaisuuteen työskentelyn API:t ovat hyvin
samanlaisia kuin säikeillä työskentelyn API:t. Toisissa tapauksissa ne ovat
hyvin erilaisia. Vaikka API:t _näyttäisivätkin_ samanlaisilta säikeiden ja
asyncin välillä, niillä on usein erilainen käyttäytyminen — ja niillä on lähes
aina erilaiset suorituskykyominaisuudet.

<!-- Old headings. Do not remove or links may break. -->

<a id="counting"></a>

### Uuden tehtävän luominen `spawn_task`-funktiolla

Ensimmäinen operaatio, jota käsittelimme osiossa [Uuden säikeen luominen
`spawn`-funktiolla][thread-spawn]<!-- ignore -->, oli laskeminen kahdella erillisellä
säikeellä. Tehdään sama asyncilla. `trpl`-crate tarjoaa `spawn_task`-funktion,
joka näyttää hyvin samalta kuin `thread::spawn`-API, ja `sleep`-funktion, joka
on async-versio `thread::sleep`-API:sta. Voimme käyttää näitä yhdessä
laskuesimerkin toteuttamiseen, kuten Listauksessa 17-6.

<Listing number="17-6" caption="Uuden tehtävän luominen tulostamaan yhtä asiaa, kun päätehtävä tulostaa jotain muuta" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-06/src/main.rs:all}}
```

</Listing>

Lähtökohtanamme asetamme `main`-funktion `trpl::run`-funktiolla, jotta
ylätason funktiomme voi olla async.

> Huom: Tästä eteenpäin tässä luvussa jokainen esimerkki sisältää täsmälleen
> saman käärintäkoodin `trpl::run`-funktiolla `main`-funktiossa, joten ohitamme
> sen usein samalla tavalla kuin ohitamme `main`-funktion. Älä unohda sisällyttää
> sitä koodiisi!

Sitten kirjoitamme kaksi silmukkaa kyseisen lohkon sisään, joista kummassakin on
`trpl::sleep`-kutsu, joka odottaa puoli sekuntia (500 millisekuntia) ennen
seuraavan viestin lähettämistä. Laitamme toisen silmukan `trpl::spawn_task`-funktion
runkoon ja toisen ylätason `for`-silmukkaan. Lisäämme myös `await`-kutsun
`sleep`-kutsujen jälkeen.

Tämä koodi käyttäytyy samankaltaisesti kuin säikeisiin perustuva toteutus — mukaan
lukien se, että saatat nähdä viestien ilmestyvän eri järjestyksessä omassa
terminaalissasi, kun ajat sen:

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

Tämä versio pysähtyy heti, kun pää-async-lohkon rungossa oleva `for`-silmukka
päättyy, koska `spawn_task`-funktion luoma tehtävä sammutetaan, kun `main`-funktio
päättyy. Jos haluat sen ajavan aina tehtävän valmistumiseen asti, sinun täytyy
käyttää join-käsittelijää odottamaan ensimmäisen tehtävän valmistumista. Säikeiden
kanssa käytimme `join`-metodia ”estääksemme” kunnes säie oli valmis. Listauksessa 17-7
voimme käyttää `await`-avainsanaa samaan tarkoitukseen, koska tehtäväkäsittelijä
itse on future. Sen `Output`-tyyppi on `Result`, joten puramme sen myös
odotuksen jälkeen.

<Listing number="17-7" caption="`await`-avainsanan käyttö join-käsittelijän kanssa tehtävän suorittamiseen loppuun" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-07/src/main.rs:handle}}
```

</Listing>

Tämä päivitetty versio ajaa, kunnes _molemmat_ silmukat päättyvät.

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

Tähän asti näyttää siltä, että async ja säikeet antavat meille samat perustulokset,
vain eri syntaksilla: `await`-avainsanan käyttö `join`-metodin kutsumisen sijaan
join-käsittelijälle ja `sleep`-kutsujen odottaminen.

Suurempi ero on se, että emme tarvinneet toista käyttöjärjestelmän säiettä
tähän. Itse asiassa emme edes tarvitse luoda tehtävää tässä. Koska async-lohkot
kääntyvät anonyymeiksi futuresiksi, voimme laittaa kummankin silmukan async-lohkoon
ja antaa ajoympäristön suorittaa molemmat loppuun käyttämällä `trpl::join`-funktiota.

Osiossa [Odottaminen kaikkien säikeiden valmistumiseen `join`-käsittelijöiden avulla][join-handles]<!-- ignore -->
näytimme, miten käytetään `join`-metodia `JoinHandle`-tyypillä, jonka `std::thread::spawn`-kutsu
palauttaa. `trpl::join`-funktio on samanlainen, mutta futuresille. Kun annat sille
kaksi futurea, se tuottaa yhden uuden futuren, jonka tuloste on monikko, joka
sisältää kummankin välittämäsi futuren tulosteen, kun ne _molemmat_ valmistuvat.
Näin ollen Listauksessa 17-8 käytämme `trpl::join`-funktiota odottamaan, että
sekä `fut1` että `fut2` valmistuvat. Emme odota `fut1`- ja `fut2`-futuresia,
vaan `trpl::join`-funktion tuottamaa uutta futurea. Jätämme tulosteen huomiotta,
koska se on vain monikko, joka sisältää kaksi yksikköarvoa.

<Listing number="17-8" caption="`trpl::join`-funktion käyttö kahden anonyymin futuren odottamiseen" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-08/src/main.rs:join}}
```

</Listing>

Kun ajamme tämän, näemme molempien futuresien ajavan loppuun:

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

Nyt näet täsmälleen saman järjestyksen joka kerta, mikä on hyvin erilaista kuin
mitä näimme säikeillä. Tämä johtuu siitä, että `trpl::join`-funktio on _reilu_,
eli se tarkistaa jokaisen futuren yhtä usein, vuorotellen niiden välillä, eikä
koskaan anna toisen kilpailla edelle, jos toinen on valmis. Säikeiden kanssa
käyttöjärjestelmä päättää, mitä säiettä tarkistaa ja kuinka kauan antaa sen
ajaa. Async-Rustissa ajoympäristö päättää, mitä tehtävää tarkistaa. (Käytännössä
yksityiskohdat monimutkaistuvat, koska async-ajoympäristö saattaa käyttää
käyttöjärjestelmän säikeitä taustalla osana rinnakkaisuuden hallintaa, joten
reiluuden takaaminen voi olla enemmän työtä ajoympäristölle — mutta se on silti
mahdollista!) Ajoympäristöjen ei tarvitse taata reiluutta millekään tietylle
operaatiolle, ja ne tarjoavat usein eri API:ja, joiden avulla voit valita,
haluatko reiluutta vai et.

Kokeile joitakin näistä variaatioista futuresien odottamisessa ja katso, mitä ne tekevät:

- Poista async-lohko jommastakummasta tai molemmista silmukoista.
- Odota kutakin async-lohkoa heti sen määrittelyn jälkeen.
- Kääri vain ensimmäinen silmukka async-lohkoon ja odota tuloksena olevaa futurea
  toisen silmukan rungon jälkeen.

Lisähaasteena yritä selvittää, mikä tuloste on kussakin tapauksessa _ennen_
koodin ajamista!

<!-- Old headings. Do not remove or links may break. -->

<a id="message-passing"></a>

### Laskeminen kahdella tehtävällä viestinvälityksen avulla

Datan jakaminen futuresien välillä on myös tuttua: käytämme jälleen viestinvälitystä,
mutta tällä kertaa async-versioita tyypeistä ja funktioista. Otamme hieman
erilaisen polun kuin osiossa [Viestinvälitys datan siirtämiseksi säikeiden välillä][message-passing-threads]<!-- ignore -->
kuvataksemme joitakin keskeisiä eroja säikeisiin ja futuresiin perustuvan
rinnakkaisuuden välillä. Listauksessa 17-9 aloitamme vain yhdellä async-lohkolla — _ilman_
erillisen tehtävän luomista, kuten loimme erillisen säikeen.

<Listing number="17-9" caption="Async-kanavan luominen ja kahden puoliskon antaminen `tx`- ja `rx`-muuttujille" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-09/src/main.rs:channel}}
```

</Listing>

Tässä käytämme `trpl::channel`-funktiota, async-versiota usean tuottajan,
yhden kuluttajan kanava-API:sta, jota käytimme säikeillä takaisin Luvussa 16.
Async-versio API:sta eroaa vain vähän säikeisiin perustuvasta versiosta: se
käyttää muuttuvaa eikä muuttumatonta vastaanotinta `rx`, ja sen `recv`-metodi
tuottaa futuren, jota meidän täytyy odottaa sen sijaan, että se tuottaisi arvon
suoraan. Nyt voimme lähettää viestejä lähettäjältä vastaanottajalle. Huomaa,
että emme tarvitse erillistä säiettä tai edes tehtävää; meidän täytyy vain odottaa
`rx.recv`-kutsua.

Synkroninen `Receiver::recv`-metodi `std::mpsc::channel`-kanavassa estää, kunnes
se vastaanottaa viestin. `trpl::Receiver::recv`-metodi ei tee niin, koska se on
async. Sen sijaan, että se estäisi, se palauttaa ohjauksen ajoympäristölle, kunnes
joko viesti vastaanotetaan tai kanavan lähetyspuoli sulkeutuu. Sitä vastoin emme
odota `send`-kutsua, koska se ei estä. Sen ei tarvitse, koska kanava, johon
lähetämme, on rajoittamaton.

> Huom: Koska kaikki tämä async-koodi ajetaan async-lohkossa `trpl::run`-kutsussa,
> kaikki sen sisällä voi välttää estämisen. Koodi _sen ulkopuolella_ kuitenkin
> estyy `run`-funktion paluuarvoa odottaessa. Siinä on koko `trpl::run`-funktion
> idea: se antaa sinun _valita_, missä estät jonkin async-koodin joukon, ja siten
> missä siirryt synkronisen ja asynkronisen koodin välillä. Useimmissa
> async-ajoympäristöissä `run` on itse asiassa nimetty `block_on` juuri tästä syystä.

Huomaa tästä esimerkistä kaksi asiaa. Ensinnäkin viesti saapuu heti. Toiseksi,
vaikka käytämme tässä futurea, rinnakkaisuutta ei ole vielä. Kaikki listauksessa
tapahtuu peräkkäin, aivan kuten jos futuresia ei olisi mukana.

Käsitellään ensimmäinen osa lähettämällä sarja viestejä ja nukkumalla niiden
välissä, kuten Listauksessa 17-10.

<!-- We cannot test this one because it never stops! -->

<Listing number="17-10" caption="Useiden viestien lähettäminen ja vastaanottaminen async-kanavan kautta ja nukkuminen `await`-avainsanalla jokaisen viestin välissä" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-10/src/main.rs:many-messages}}
```

</Listing>

Viestien lähettämisen lisäksi meidän täytyy vastaanottaa ne. Tässä tapauksessa,
koska tiedämme kuinka monta viestiä on tulossa, voisimme tehdä sen käsin kutsumalla
`rx.recv().await` neljä kertaa. Tosielämässä odotamme kuitenkin yleensä _tuntemattoman_
määrän viestejä, joten meidän täytyy jatkaa odottamista, kunnes selviää, ettei
viestejä enää tule.

Listauksessa 16-10 käytimme `for`-silmukkaa käsittelemään kaikki synkroniselta
kanavalta vastaanotetut kohteet. Rustilla ei ole vielä tapaa kirjoittaa `for`-silmukkaa
_asynkronisen_ kohteiden sarjan yli, joten meidän täytyy käyttää silmukkaa, jota
emme ole vielä nähneet: `while let` -ehdosilmukkaa. Tämä on silmukkaversio
`if let` -rakenteesta, jonka näimme takaisin osiossa [Tiiviimpi ohjausrakenne `if let` ja `let else` -rakenteilla][if-let]<!-- ignore -->. Silmukka jatkaa suorittamista niin kauan kuin
sen määrittämä kuvio vastaa arvoa.

`rx.recv`-kutsu tuottaa futuren, jota odotamme. Ajoympäristö keskeyttää futuren,
kunnes se on valmis. Kun viesti saapuu, future ratkeaa arvoksi `Some(message)` niin
monta kertaa kuin viesti saapuu. Kun kanava sulkeutuu, riippumatta siitä, ovatko
_viestit_ saapuneet, future ratkeaa sen sijaan arvoksi `None` osoittaakseen, ettei
arvoja ole enempää ja että meidän pitäisi lopettaa pollaaminen — eli lopettaa odottaminen.

`while let` -silmukka kokoaa kaiken tämän yhteen. Jos `rx.recv().await`-kutsun
tulos on `Some(message)`, saamme käyttöön viestin ja voimme käyttää sitä silmukan
rungossa, aivan kuten `if let` -rakenteella. Jos tulos on `None`, silmukka päättyy.
Joka kerta kun silmukka valmistuu, se osuu odotuspisteeseen uudelleen, joten
ajoympäristö keskeyttää sen uudelleen, kunnes toinen viesti saapuu.

Koodi lähettää ja vastaanottaa nyt onnistuneesti kaikki viestit. Valitettavasti
ongelmia on kuitenkin vielä pari. Ensinnäkin viestit eivät saavu puolen sekunnin
välein. Ne saapuvat kaikki kerralla 2 sekunnin (2 000 millisekunnin) kuluttua
ohjelman käynnistymisestä. Toiseksi tämä ohjelma ei myöskään koskaan päätty!
Sen sijaan se odottaa ikuisesti uusia viestejä. Sinun täytyy sammuttaa se painamalla <span
class="keystroke">ctrl-c</span>.

Aloitetaan tutkimalla, miksi viestit saapuvat kaikki kerralla koko viiveen jälkeen
eikä viiveiden välein. Tietyssä async-lohkossa `await`-avainsanojen esiintymisjärjestys
koodissa on myös järjestys, jossa ne suoritetaan ohjelman ajossa.

Listauksessa 17-10 on vain yksi async-lohko, joten kaikki sen sisällä ajetaan
lineaarisesti. Rinnakkaisuutta ei ole vieläkään. Kaikki `tx.send`-kutsut tapahtuvat,
`trpl::sleep`-kutsujen ja niihin liittyvien odotuspisteiden välissä. Vasta sen
jälkeen `while let` -silmukka pääsee käymään läpi mitään `recv`-kutsujen odotuspisteitä.

Saadaksemme haluamamme käyttäytymisen, jossa nukkumisviive tapahtuu jokaisen viestin
välissä, meidän täytyy laittaa `tx`- ja `rx`-operaatiot omiin async-lohkoihinsa,
kuten Listauksessa 17-11. Sitten ajoympäristö voi suorittaa kummankin erikseen
käyttämällä `trpl::join`-funktiota, aivan kuten laskuesimerkissä. Taaskin odotamme
`trpl::join`-kutsun tulosta, emme yksittäisiä futuresia. Jos odottaisimme yksittäisiä
futuresia peräkkäin, päätyisimme takaisin peräkkäiseen suoritukseen — juuri sitä,
mitä yritämme _välttää_.

<!-- We cannot test this one because it never stops! -->

<Listing number="17-11" caption="`send`- ja `recv`-operaatioiden erottaminen omiin `async`-lohkoihinsa ja niiden futuresien odottaminen" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-11/src/main.rs:futures}}
```

</Listing>

Listauksen 17-11 päivitetyllä koodilla viestit tulostetaan 500 millisekunnin
välein sen sijaan, että ne tulisivat kaikki kerralla 2 sekunnin kuluttua.

Ohjelma ei kuitenkaan koskaan päätty, koska tavalla, jolla `while let` -silmukka
vuorovaikuttaa `trpl::join`-funktion kanssa:

- `trpl::join`-funktion palauttama future valmistuu vasta, kun _molemmat_ sille
  välitetyt futuresit ovat valmiit.
- `tx`-future valmistuu, kun se on nukkunut viimeisen viestin lähettämisen jälkeen
  `vals`-taulukosta.
- `rx`-future ei valmistu, ennen kuin `while let` -silmukka päättyy.
- `while let` -silmukka ei päätty, ennen kuin `rx.recv`-kutsun odottaminen tuottaa `None`-arvon.
- `rx.recv`-kutsun odottaminen palauttaa `None`-arvon vasta, kun kanavan toinen pää on suljettu.
- Kanava sulkeutuu vain, jos kutsumme `rx.close`-funktiota tai kun lähetyspuoli
  `tx` pudotetaan.
- Emme kutsu `rx.close`-funktiota missään, eikä `tx` pudoteta ennen kuin
  `trpl::run`-funktiolle välitetty uloin async-lohko päättyy.
- Lohko ei voi päättyä, koska se on estynyt `trpl::join`-funktion valmistumista
  odottaessa, mikä vie meidät takaisin tämän listan alkuun.

Voisimme sulkea `rx`-kanavan käsin kutsumalla `rx.close`-funktiota jossain, mutta
se ei juuri järkeä. Pysähtyminen tietyn mielivaltaisen viestimäärän käsittelyn
jälkeen saisi ohjelman sammumaan, mutta voisimme menettää viestejä. Tarvitsemme
jonkin muun tavan varmistaa, että `tx` pudotetaan _ennen_ funktion loppua.

Tällä hetkellä viestejä lähettävä async-lohko lainaa vain `tx`-muuttujaa, koska
viestin lähettäminen ei vaadi omistajuutta, mutta jos voisimme siirtää `tx`-muuttujan
kyseiseen async-lohkoon, se pudotettaisiin, kun lohko päättyy. Luvun 13 osiossa
[Viitteiden tallentaminen ja omistajuuden siirtäminen][capture-or-move]<!-- ignore -->
opit käyttämään `move`-avainsanaa sulkeisissa, ja kuten käsiteltiin Luvun 16 osiossa
[`move`-sulkeiset säikeiden kanssa][move-threads]<!-- ignore
-->, meidän täytyy usein siirtää data sulkeisiin säikeiden kanssa työskennellessä.
Samat perusdynamiikat pätevät async-lohkoihin, joten `move`-avainsana toimii
async-lohkoissa aivan kuten sulkeisissa.

Listauksessa 17-12 muutamme viestejä lähettävän lohkon `async`-lohkosta `async move` -lohkoksi.
Kun ajamme _tämän_ version koodista, se sammuu siististi viimeisen viestin
lähettämisen ja vastaanottamisen jälkeen.

<Listing number="17-12" caption="Listauksen 17-11 koodin tarkistettu versio, joka sammuu oikein valmistuessaan" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-12/src/main.rs:with-move}}
```

</Listing>

Tämä async-kanava on myös usean tuottajan kanava, joten voimme kutsua `clone`-metodia
`tx`-muuttujalle, jos haluamme lähettää viestejä useista futuresista, kuten Listauksessa 17-13.

<Listing number="17-13" caption="Usean tuottajan käyttö async-lohkojen kanssa" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-13/src/main.rs:here}}
```

</Listing>

Ensin kloonaamme `tx`-muuttujan luoden `tx1`-muuttujan ensimmäisen async-lohkon
ulkopuolelle. Siirrämme `tx1`-muuttujan kyseiseen lohkoon samalla tavalla kuin
aiemmin `tx`-muuttujan. Sitten myöhemmin siirrämme alkuperäisen `tx`-muuttujan
_uuteen_ async-lohkoon, jossa lähetämme lisää viestejä hieman hitaammalla viiveellä.
Sattumalta laitamme tämän uuden async-lohkon vastaanottavien viestien async-lohkon
jälkeen, mutta se voisi olla yhtä hyvin ennen sitä. Ratkaisevaa on järjestys, jossa
futuresit odotetaan, ei järjestys, jossa ne luodaan.

Molempien viestejä lähettävien async-lohkojen täytyy olla `async move` -lohkoja,
jotta sekä `tx` että `tx1` pudotetaan, kun nämä lohkot päättyvät. Muuten päädymme
takaisin samaan loputtomaan silmukkaan, jossa aloitimme. Lopuksi vaihdamme
`trpl::join`-funktiosta `trpl::join3`-funktioon käsitelläksemme ylimääräisen futuren.

Nyt näemme kaikki viestit molemmista lähettävistä futuresista, ja koska lähettävät
futuresit käyttävät hieman erilaisia viiveitä lähettämisen jälkeen, viestit
vastaanotetaan myös näillä eri aikaväleillä.

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

Tämä on hyvä alku, mutta se rajoittaa meidät vain pieneen määrään futuresia: kahteen
`join`-funktiolla tai kolmeen `join3`-funktiolla. Katsotaan, miten voisimme työskennellä
useampien futuresien kanssa.

[thread-spawn]: ch16-01-threads.html#creating-a-new-thread-with-spawn
[join-handles]: ch16-01-threads.html#waiting-for-all-threads-to-finish-using-join-handles
[message-passing-threads]: ch16-02-message-passing.html
[if-let]: ch06-03-if-let.html
[capture-or-move]: ch13-01-closures.html#capturing-references-or-moving-ownership
[move-threads]: ch16-01-threads.html#using-move-closures-with-threads
