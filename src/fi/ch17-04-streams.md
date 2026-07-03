## Streamit: futuurit peräkkäin

<!-- Old headings. Do not remove or links may break. -->

<a id="streams"></a>

Tähän mennessä tässä luvussa olemme pitäytyneet pääosin yksittäisissä futuureissa. Yksi suuri poikkeus oli käyttämämme asynkroninen kanava. Muistatko, kuinka käytimme asynkronisen kanavamme vastaanotinta aikaisemmin tässä luvussa [”Viestinvälitys”][17-02-messages]<!-- ignore --> -osiossa. Asynkroninen `recv`-metodi tuottaa ajan mittaan sarjan kohteita. Tämä on esimerkki paljon yleisemmästä mallista, jota kutsutaan _streamiksi_.

Näimme kohteiden sarjan jo luvussa 13, kun tarkastelimme `Iterator`-traitia [Iterator-traitissa ja `next`-metodissa][iterator-trait]<!-- ignore
--> -osiossa, mutta iteraattoreiden ja asynkronisen kanavan vastaanottimen välillä on kaksi eroa. Ensimmäinen ero on aika: iteraattorit ovat synkronisia, kun taas kanavan vastaanotin on asynkroninen. Toinen ero on API. Kun työskentelemme suoraan `Iterator`-tyypin kanssa, kutsumme sen synkronista `next`-metodia. Erityisesti `trpl::Receiver`-streamin kanssa kutsuimme sen sijaan asynkronista `recv`-metodia. Muuten nämä API:t tuntuvat hyvin samankaltaisilta, eikä tämä samankaltaisuus ole sattumaa. Stream on kuin iteraation asynkroninen muoto. Vaikka `trpl::Receiver` odottaa nimenomaan viestien vastaanottamista, yleiskäyttöinen stream-API on paljon laajempi: se tarjoaa seuraavan kohteen samalla tavalla kuin `Iterator`, mutta asynkronisesti.

Iteraattoreiden ja streamien samankaltaisuus Rustissa tarkoittaa, että voimme itse asiassa luoda streamin mistä tahansa iteraattorista. Kuten iteraattorin kanssa, voimme työskennellä streamin kanssa kutsumalla sen `next`-metodia ja odottamalla sitten tulosta, kuten listauksessa 17-30.

<Listing number="17-30" caption="Streamin luominen iteraattorista ja sen arvojen tulostaminen" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-30/src/main.rs:stream}}
```

</Listing>

Aloitamme numerotaulukosta, jonka muunnamme iteraattoriksi ja jolle kutsumme `map`-metodia kaikkien arvojen kaksinkertaistamiseksi. Sitten muunnamme iteraattorin streamiksi `trpl::stream_from_iter`-funktiolla. Seuraavaksi käymme läpi streamin kohteita niiden saapuessa `while let` -silmukassa.

Valitettavasti kun yritämme ajaa koodin, se ei käänny, vaan raportoi, ettei `next`-metodia ole saatavilla:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-30
cargo build
copy only the error output
-->

```console
error[E0599]: no method named `next` found for struct `Iter` in the current scope
  --> src/main.rs:10:40
   |
10 |         while let Some(value) = stream.next().await {
   |                                        ^^^^
   |
   = note: the full type name has been written to '/Users/chris/dev/rust-lang/book/main/listings/ch17-async-await/listing-17-30/target/debug/deps/async_await-575db3dd3197d257.long-type-14490787947592691573.txt'
   = note: consider using `--verbose` to print the full type name to the console
   = help: items from traits can only be used if the trait is in scope
help: the following traits which provide `next` are implemented but not in scope; perhaps you want to import one of them
   |
1  + use crate::trpl::StreamExt;
   |
1  + use futures_util::stream::stream::StreamExt;
   |
1  + use std::iter::Iterator;
   |
1  + use std::str::pattern::Searcher;
   |
help: there is a method `try_next` with a similar name
   |
10 |         while let Some(value) = stream.try_next().await {
   |                                        ~~~~~~~~
```

Kuten tämä tuloste selittää, kääntäjävirheen syy on se, että tarvitsemme oikean traitin näkyvyysalueelle voidaksemme käyttää `next`-metodia. Tähänastisen keskustelumme perusteella saatat kohtuullisesti odottaa, että kyseinen trait olisi `Stream`, mutta se on itse asiassa `StreamExt`. Lyhenne sanasta _extension_, `Ext` on yleinen malli Rust-yhteisössä yhden traitin laajentamiseen toisella.

Käsittelemme `Stream`- ja `StreamExt`-traitteja hieman tarkemmin luvun lopussa, mutta toistaiseksi sinun tarvitsee tietää vain, että `Stream`-trait määrittelee matalan tason rajapinnan, joka yhdistää käytännössä `Iterator`- ja `Future`-traitit. `StreamExt` tarjoaa korkeamman tason API-joukon `Stream`-traitin päälle, mukaan lukien `next`-metodin sekä muita apumetodeja, jotka ovat samankaltaisia kuin `Iterator`-traitin tarjoamat. `Stream` ja `StreamExt` eivät ole vielä osa Rustin standardikirjastoa, mutta useimmat ekosysteemin kirjastot käyttävät samaa määritelmää.

Korjaus kääntäjävirheeseen on lisätä `use`-lause `trpl::StreamExt`-traitille, kuten listauksessa 17-31.

<Listing number="17-31" caption="Iteraattorin käyttäminen onnistuneesti streamin pohjana" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-31/src/main.rs:all}}
```

</Listing>

Kun kaikki nämä osat on koottu yhteen, koodi toimii haluamallamme tavalla! Lisäksi nyt kun `StreamExt` on näkyvyysalueella, voimme käyttää kaikkia sen apumetodeja aivan kuten iteraattoreiden kanssa. Esimerkiksi listauksessa 17-32 käytämme `filter`-metodia suodattaaksemme pois kaiken paitsi kolmen ja viiden monikerrat.

<Listing number="17-32" caption="Streamin suodattaminen `StreamExt::filter`-metodilla" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-32/src/main.rs:all}}
```

</Listing>

Tämä ei tietenkään ole kovin mielenkiintoista, koska voisimme tehdä saman tavallisilla iteraattoreilla ilman mitään asynkronisuutta. Katsotaan, mitä voimme tehdä, mikä _on_ streamien ainutlaatuista.

### Streamien yhdistäminen

Monet käsitteet voidaan luonnollisesti esittää streameina: jonoon tulevat kohteet, tiedostojärjestelmästä inkrementaalisesti haetut datapalat, kun koko aineisto on liian suuri tietokoneen muistiin, tai ajan mittaan saapuva verkkodata. Koska streamit ovat futuureja, voimme käyttää niitä minkä tahansa muun futuurin kanssa ja yhdistellä niitä mielenkiintoisilla tavoilla. Voimme esimerkiksi kerätä tapahtumia erissä välttääksemme liian monta verkkokutsua, asettaa aikakatkaisuja pitkään kestäville operaatiosarjoille tai rajoittaa käyttöliittymän tapahtumia välttääksemme turhaa työtä.

Aloitetaan rakentamalla pieni viestistream, joka toimii sijaisena WebSocketista tai muusta reaaliaikaisesta viestintäprotokollasta saatavalle datavirralle, kuten listauksessa 17-33 näytetään.

<Listing number="17-33" caption="`rx`-vastaanottimen käyttäminen `ReceiverStream`-tyyppinä" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-33/src/main.rs:all}}
```

</Listing>

Ensin luomme funktion nimeltä `get_messages`, joka palauttaa `impl Stream<Item = String>`. Toteutuksessaan se luo asynkronisen kanavan, käy läpi englannin aakkosten ensimmäiset 10 kirjainta ja lähettää ne kanavan yli.

Käytämme myös uutta tyyppiä: `ReceiverStream`, joka muuntaa `trpl::channel`-kanavan `rx`-vastaanottimen `Stream`-tyypiksi, jolla on `next`-metodi. Takaisin `main`-funktiossa käytämme `while let` -silmukkaa tulostaaksemme kaikki streamin viestit.

Kun ajamme tämän koodin, saamme juuri odottamamme tulokset:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Message: 'a'
Message: 'b'
Message: 'c'
Message: 'd'
Message: 'e'
Message: 'f'
Message: 'g'
Message: 'h'
Message: 'i'
Message: 'j'
```

Voisimme tehdä tämän tavallisella `Receiver`-API:lla tai jopa tavallisella `Iterator`-API:lla, joten lisätään ominaisuus, joka vaatii streameja: aikakatkaisu, joka koskee jokaista streamin kohdetta, ja viive lähettämiimme kohteisiin, kuten listauksessa 17-34.

<Listing number="17-34" caption="`StreamExt::timeout`-metodin käyttö streamin kohteille asetettuna aikarajana" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-34/src/main.rs:timeout}}
```

</Listing>

Aloitamme lisäämällä aikakatkaisun streamille `timeout`-metodilla, joka tulee `StreamExt`-traitista. Sitten päivitämme `while let` -silmukan rungon, koska stream palauttaa nyt `Result`-tyypin. `Ok`-variantti tarkoittaa, että viesti saapui ajoissa; `Err`-variantti tarkoittaa, että aikakatkaisu ehti kulua umpeen ennen kuin viesti saapui. Teemme `match`-lausekkeen tuloksen perusteella ja joko tulostamme viestin onnistuneen vastaanoton jälkeen tai tulostamme ilmoituksen aikakatkaisusta. Lopuksi huomaa, että kiinnitämme viestit sen jälkeen, kun olemme asettaneet niille aikakatkaisun, koska aikakatkaisuapuri tuottaa streamin, joka täytyy kiinnittää pollattavaksi.

Koska viestien välillä ei kuitenkaan ole viiveitä, tämä aikakatkaisu ei muuta ohjelman käyttäytymistä. Lisätään lähettämiimme viesteihin vaihteleva viive, kuten listauksessa 17-35.

<Listing number="17-35" caption="Viestien lähettäminen `tx`-kanavan kautta asynkronisella viiveellä tekemättä `get_messages`-funktiosta asynkronista funktiota" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-35/src/main.rs:messages}}
```

</Listing>

`get_messages`-funktiossa käytämme `enumerate`-iteraattorimetodia `messages`-taulukon kanssa, jotta saamme jokaisen lähettämämme kohteen indeksin itse kohteen ohella. Sitten asetamme parillisen indeksin kohteille 100 millisekunnin viiveen ja parittoman indeksin kohteille 300 millisekunnin viiveen simuloidaksemme erilaisia viiveitä, joita saattaisimme nähdä todellisessa viestivirrassa. Koska aikakatkaisumme on 200 millisekuntia, tämän pitäisi vaikuttaa puoleen viesteistä.

Jotta voimme nukkua viestien välillä `get_messages`-funktiossa estämättä suoritusta, meidän täytyy käyttää asynkronisuutta. Emme kuitenkaan voi tehdä `get_messages`-funktiosta itseään asynkronista funktiota, koska silloin palauttaisimme `Future<Output = Stream<Item = String>>` eikä `Stream<Item = String>>`. Kutsujan täytyisi odottaa `get_messages`-funktiota itseään päästäkseen streamiin käsiksi. Muista kuitenkin: kaikki tietyssä futuurissa tapahtuu lineaarisesti; rinnakkaisuus tapahtuu futuurien _välillä_. `get_messages`-funktion odottaminen vaatisi sen lähettämään kaikki viestit, mukaan lukien univiiveen jokaisen viestin välillä, ennen kuin vastaanottimestream palautetaan. Tämän seurauksena aikakatkaisu olisi hyödytön. Streamissä itsessään ei olisi viiveitä; ne kaikki tapahtuisivat ennen kuin stream olisi edes saatavilla.

Sen sijaan jätämme `get_messages`-funktion tavalliseksi funktioksi, joka palauttaa streamin, ja luomme tehtävän käsittelemään asynkroniset `sleep`-kutsut.

> Huom: `spawn_task`-kutsu toimii tällä tavalla, koska olemme jo asettaneet ajoaikamme; jos emme olisi, se aiheuttaisi paniikin. Muut toteutukset tekevät erilaisia kompromisseja: ne saattavat luoda uuden ajoaikamallin ja välttää paniikin, mutta joutua hieman ylimääräiseen yleiskustannukseen, tai ne eivät ehkä tarjoa erillistä tapaa luoda tehtäviä ilman viittausta ajoaikaan. Varmista, että tiedät, minkä kompromissin ajoaikasi on valinnut, ja kirjoita koodisi sen mukaisesti!

Nyt koodimme tuottaa paljon mielenkiintoisemman tuloksen. Joka toisen viestiparin välissä näkyy `Problem: Elapsed(())` -virhe.

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Message: 'a'
Problem: Elapsed(())
Message: 'b'
Message: 'c'
Problem: Elapsed(())
Message: 'd'
Message: 'e'
Problem: Elapsed(())
Message: 'f'
Message: 'g'
Problem: Elapsed(())
Message: 'h'
Message: 'i'
Problem: Elapsed(())
Message: 'j'
```

Aikakatkaisu ei estä viestejä saapumasta lopulta. Saamme silti kaikki alkuperäiset viestit, koska kanavamme on _rajoittamaton_: se voi pitää sisällään niin monta viestiä kuin muistiin mahtuu. Jos viesti ei saavu ennen aikakatkaisua, streamin käsittelijämme huomioi sen, mutta kun se pollaa streamia uudelleen, viesti on ehkä nyt saapunut.

Voit saada erilaista käyttäytymistä tarvittaessa käyttämällä muita kanavatyyppejä tai yleisemmin muita streamityyppejä. Katsotaan yhtä niistä käytännössä yhdistämällä aikavälistream tämän viestistreamin kanssa.

### Streamien sulauttaminen

Ensin luodaan toinen stream, joka tuottaa kohteen joka millisekunti, jos annamme sen ajaa suoraan. Yksinkertaisuuden vuoksi voimme käyttää `sleep`-funktiota viestin lähettämiseen viiveellä ja yhdistää sen samaan lähestymistapaan, jota käytimme `get_messages`-funktiossa streamin luomiseksi kanavasta. Ero on, että tällä kertaa lähetämme takaisin kuluneiden aikavälien määrän, joten palautustyyppi on `impl Stream<Item = u32>`, ja voimme kutsua funktiota `get_intervals` (katso listausta 17-36).

<Listing number="17-36" caption="Streamin luominen laskurilla, joka lähetetään kerran millisekunnissa" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-36/src/main.rs:intervals}}
```

</Listing>

Aloitamme määrittelemällä `count`-muuttujan tehtävässä. (Voimme määritellä sen tehtävän ulkopuolellakin, mutta on selkeämpää rajoittaa minkä tahansa muuttujan näkyvyysalue.) Sitten luomme äärettömän silmukan. Jokaisella silmukan kierroksella nukumme asynkronisesti yhden millisekunnin, kasvatamme laskuria ja lähetämme sen kanavan yli. Koska tämä kaikki on kääritty `spawn_task`-funktion luomaan tehtävään, kaikki tämä — mukaan lukien ääretön silmukka — siivotaan ajoaikamallin mukana.

Tällainen ääretön silmukka, joka päättyy vain kun koko ajoaikamalli puretaan, on melko yleinen asynkronisessa Rustissa: monien ohjelmien täytyy jatkua loputtomasti. Asynkronisuudella tämä ei estä mitään muuta, kunhan jokaisella silmukan kierroksella on vähintään yksi odotuspiste.

Nyt takaisin `main`-funktion asynkronisessa lohkossa voimme yrittää yhdistää `messages`- ja `intervals`-streamit, kuten listauksessa 17-37.

<Listing number="17-37" caption="Yritys yhdistää `messages`- ja `intervals`-streamit" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-37/src/main.rs:main}}
```

</Listing>

Aloitamme kutsumalla `get_intervals`-funktiota. Sitten yhdistämme `messages`- ja `intervals`-streamit `merge`-metodilla, joka yhdistää useita streameja yhdeksi streamiksi, joka tuottaa kohteita mistä tahansa lähdestreamistä heti kun ne ovat saatavilla, asettamatta mitään erityistä järjestystä. Lopuksi käymme läpi tuon yhdistetyn streamin `messages`-streamin sijaan.

Tässä vaiheessa kumpikaan `messages` eikä `intervals` tarvitse olla kiinnitetty tai muuttuva, koska molemmat yhdistetään yhdeksi `merged`-streamiksi. Tämä `merge`-kutsu ei kuitenkaan käänny! (Eikä `next`-kutsu `while let` -silmukassa, mutta palaamme siihen.) Syy on se, että kahdella streamilla on eri tyypit. `messages`-streamin tyyppi on `Timeout<impl Stream<Item = String>>`, missä `Timeout` on tyyppi, joka toteuttaa `Stream`-traitin `timeout`-kutsulle. `intervals`-streamin tyyppi on `impl Stream<Item = u32>`. Näiden kahden streamin yhdistämiseksi meidän täytyy muuntaa toinen vastaamaan toista. Muokkaamme `intervals`-streamia, koska `messages` on jo haluamassamme perusmuodossa ja sen täytyy käsitellä aikakatkaisuvirheitä (katso listausta 17-38).

<!-- We cannot directly test this one, because it never stops. -->

<Listing number="17-38" caption="`intervals`-streamin tyypin yhteensovittaminen `messages`-streamin tyypin kanssa" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-38/src/main.rs:main}}
```

</Listing>

Ensin voimme käyttää `map`-apumetodia muuntaaksemme `intervals`-streamin merkkijonoksi. Toiseksi meidän täytyy vastata `messages`-streamin `Timeout`-tyyppiä. Koska emme kuitenkaan _halua_ aikakatkaisua `intervals`-streamille, voimme luoda aikakatkaisun, joka on pidempi kuin muut käyttämämme kestot. Tässä luomme 10 sekunnin aikakatkaisun `Duration::from_secs(10)`-funktiolla. Lopuksi meidän täytyy tehdä `stream`-muuttujasta muuttuva, jotta `while let` -silmukan `next`-kutsut voivat iteroida streamin läpi, ja kiinnittää se, jotta se on turvallista. Se vie meidät _melkein_ sinne, minne meidän täytyy päästä. Kaikki tyypit tarkistuvat. Jos ajat tämän, on kuitenkin kaksi ongelmaa. Ensinnäkin se ei koskaan pysähdy! Sinun täytyy pysäyttää se näppäinyhdistelmällä <span class="keystroke">ctrl-c</span>. Toiseksi englannin aakkosten viestit hautautuvat kaikkien aikaväilaskuriviestien joukkoon:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the tasks running differently rather than
changes in the compiler -->

```text
--snip--
Interval: 38
Interval: 39
Interval: 40
Message: 'a'
Interval: 41
Interval: 42
Interval: 43
--snip--
```

Listausta 17-39 näyttää yhden tavan ratkaista nämä kaksi viimeistä ongelmaa.

<Listing number="17-39" caption="`throttle`- ja `take`-metodien käyttö yhdistettyjen streamien hallintaan" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-39/src/main.rs:throttle}}
```

</Listing>

Ensin käytämme `throttle`-metodia `intervals`-streamissä, jotta se ei ylikuormita `messages`-streamia. _Rajoittaminen_ (_throttling_) on tapa rajoittaa funktion kutsumistiheyttä — tai tässä tapauksessa sitä, kuinka usein streamia pollataan. Kerran 100 millisekunnissa pitäisi riittää, koska se on suunnilleen se tahti, jolla viestimme saapuvat.

Rajoittaaksemme streamista hyväksymiemme kohteiden määrää, käytämme `take`-metodia `merged`-streamissä, koska haluamme rajoittaa lopullista tulosta, emme vain yhtä streamia tai toista.

Nyt kun ajamme ohjelman, se pysähtyy 20 kohteen haun jälkeen streamista, eikä aikavälit ylikuormita viestejä. Emme myöskään saa `Interval: 100` tai `Interval: 200` ja niin edelleen, vaan saamme `Interval: 1`, `Interval: 2` ja niin edelleen — vaikka meillä on lähdestream, joka _voi_ tuottaa tapahtuman joka millisekunti. Syy on se, että `throttle`-kutsu tuottaa uuden streamin, joka käärii alkuperäisen streamin niin, että alkuperäistä streamia pollataan vain rajoitusnopeudella, ei sen omalla ”alkuperäisellä” nopeudella. Meillä ei ole joukkoa käsittelemättömiä aikaväliviestejä, joita valitsisimme sivuuttaa. Sen sijaan emme koskaan tuota näitä aikaväliviestejä ensinkään! Tämä on Rustin futuurien luontainen ”laiskuus” taas käytössä, antaen meille mahdollisuuden valita suorituskykyominaisuutemme.

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Interval: 1
Message: 'a'
Interval: 2
Interval: 3
Problem: Elapsed(())
Interval: 4
Message: 'b'
Interval: 5
Message: 'c'
Interval: 6
Interval: 7
Problem: Elapsed(())
Interval: 8
Message: 'd'
Interval: 9
Message: 'e'
Interval: 10
Interval: 11
Problem: Elapsed(())
Interval: 12
```

Meidän täytyy vielä käsitellä yksi asia: virheet! Molemmissa näistä kanavapohjaisista streameista `send`-kutsut voivat epäonnistua, kun kanavan toinen puoli sulkeutuu — ja se riippuu vain siitä, miten ajoaikamalli suorittaa streamin muodostavat futuurit. Tähän asti olemme sivuuttaneet tämän mahdollisuuden kutsumalla `unwrap`, mutta hyvin käyttäytyvässä sovelluksessa meidän pitäisi käsitellä virhe eksplisiittisesti, vähintään lopettamalla silmukka, jotta emme yritä lähettää enempää viestejä. Listausta 17-40 näyttää yksinkertaisen virhestrategian: tulosta ongelma ja `break` silmukoista.

<Listing number="17-40" caption="Virheiden käsittely ja silmukoiden sammuttaminen">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-40/src/main.rs:errors}}
```

</Listing>

Kuten tavallisesti, oikea tapa käsitellä viestin lähetysvirhe vaihtelee; varmista vain, että sinulla on strategia.

Nyt kun olemme nähneet paljon asynkronisuutta käytännössä, otetaan askel taaksepäin ja syvennytään muutamaan yksityiskohtaan siitä, miten `Future`, `Stream` ja muut keskeiset traitit, joita Rust käyttää asynkronisuuden toteuttamiseen, toimivat.

[17-02-messages]: ch17-02-concurrency-with-async.html#message-passing
[iterator-trait]: ch13-02-iterators.html#the-iterator-trait-and-the-next-method
