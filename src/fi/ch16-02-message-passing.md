<!-- Old headings. Do not remove or links may break. -->

<a id="using-message-passing-to-transfer-data-between-threads"></a>

## Datan siirtäminen säikeiden välillä viestinvälityksellä

Yhä suositumpi lähestymistapa turvallisen rinnakkaisuuden varmistamiseen on viestinvälitys, jossa säikeet tai aktorit kommunikoivat lähettämällä toisilleen viestejä, jotka sisältävät dataa. Tässä on ajatus [Go-ohjelmointikielen dokumentaation](https://golang.org/doc/effective_go.html#concurrency) iskulauseessa: ”Älä kommunikoi jakamalla muistia; sen sijaan jaa muisti kommunikoimalla.”

Viestinvälitykseen perustuvan rinnakkaisuuden toteuttamiseksi Rustin standardikirjasto tarjoaa kanavien toteutuksen. _Kanava_ on yleinen ohjelmointikäsite, jolla data lähetetään säikeestä toiseen.

Voit kuvitella ohjelmoinnissa kanavan suuntaiseksi vesiväyläksi, kuten puroksi tai joeksi. Jos laitat esimerkiksi kumiankan vesiväylään, se kulkee alavirtaan vesiväylän päähän.

Kanavalla on kaksi puoliskoa: lähettäjä ja vastaanotin. Lähettäjäpuoli on ylävirran kohta, johon laitat kumiankan jokeen, ja vastaanotinpuoli on kohta, johon kumiankka päätyy alavirtaan. Ohjelmasi yksi osa kutsuu lähettäjän metodeja datalla, jonka haluat lähettää, ja toinen osa tarkistaa vastaanottopään saapuvat viestit. Kanavaa sanotaan _suljetuksi_, jos jompikumpi lähettäjä- tai vastaanotinpuolisko pudotetaan.

Tässä rakennamme ohjelman, jossa yksi säie tuottaa arvoja ja lähettää ne kanavaa pitkin, ja toinen säie vastaanottaa arvot ja tulostaa ne. Lähetämme yksinkertaisia arvoja säikeiden välillä kanavan avulla havainnollistamaan ominaisuutta. Kun olet tutustunut tekniikkaan, voit käyttää kanavia minkä tahansa toisiinsa kommunikoivien säikeiden välillä, kuten chat-järjestelmässä tai järjestelmässä, jossa useat säikeet suorittavat osia laskennasta ja lähettävät osat yhdelle säikeelle, joka kokoaa tulokset.

Ensin listauksessa 16-6 luomme kanavan, mutta emme tee sillä mitään. Huomaa, että tämä ei vielä käänny, koska Rust ei tiedä, millaisia arvoja haluamme lähettää kanavan kautta.

<Listing number="16-6" file-name="src/main.rs" caption="Kanavan luominen ja kahden puoliskon sijoittaminen muuttujiin `tx` ja `rx`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-06/src/main.rs}}
```

</Listing>

Luomme uuden kanavan `mpsc::channel`-funktiolla; `mpsc` tarkoittaa _multiple producer, single consumer_ (useita tuottajia, yksi kuluttaja). Lyhyesti sanottuna Rustin standardikirjaston kanavatoteutus tarkoittaa, että kanavalla voi olla useita _lähettäviä_ päitä, jotka tuottavat arvoja, mutta vain yksi _vastaanottava_ pää, joka kuluttaa nämä arvot. Kuvittele useita puroja, jotka virtaavat yhteen suureen jokeen: kaikki mihin tahansa puroon lähetetty päätyy lopulta yhteen jokeen. Aloitamme yhdellä tuottajalla, mutta lisäämme useita tuottajia, kun saamme tämän esimerkin toimimaan.

`mpsc::channel`-funktio palauttaa monikon, jonka ensimmäinen elementti on lähettävä pää – lähettäjä – ja toinen elementti on vastaanottava pää – vastaanotin. Lyhenteitä `tx` ja `rx` käytetään perinteisesti monilla aloilla tarkoittamaan _transmitter_ (lähettäjä) ja _receiver_ (vastaanotin), joten nimeämme muuttujamme näin osoittaaksemme kumman pään kyseessä on. Käytämme `let`-lauseketta kuviolla, joka purkaa monikon; käsittelemme kuvioiden käyttöä `let`-lausekkeissa ja purkamista luvussa 19. Toistaiseksi riittää tietää, että `let`-lausekkeen käyttö tällä tavalla on kätevä tapa erottaa `mpsc::channel`-funktion palauttaman monikon osat.

Siirretään lähettävä pää luotuun säikeeseen ja lähetetään yksi merkkijono, jotta luotu säie kommunikoi pääsäikeen kanssa, kuten listauksessa 16-7 näytetään. Tämä on kuin laittaisit kumiankan jokeen ylävirtaan tai lähettäisit chat-viestin säikeestä toiseen.

<Listing number="16-7" file-name="src/main.rs" caption='`tx`:n siirtäminen luotuun säikeeseen ja `"hi"`-merkkijonon lähettäminen'>

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-07/src/main.rs}}
```

</Listing>

Käytämme jälleen `thread::spawn`-funktiota luodaksemme uuden säikeen ja käytämme `move`-avainsanaa siirtääksemme `tx`:n sulkeiseen, jotta luotu säie omistaa `tx`:n. Luodun säikeen täytyy omistaa lähettäjä, jotta se voi lähettää viestejä kanavan kautta.

Lähettäjällä on `send`-metodi, joka ottaa lähetettävän arvon. `send`-metodi palauttaa tyypin `Result<T, E>`, joten jos vastaanotin on jo pudotettu eikä arvoa voi lähettää minnekään, lähetysoperaatio palauttaa virheen. Tässä esimerkissä kutsumme `unwrap`-metodia panikoidaksemme virheen sattuessa. Todellisessa sovelluksessa käsittelisimme sen asianmukaisesti: palaa lukuun 9 tarkastelemaan asianmukaista virheenkäsittelyä.

Listauksessa 16-8 haemme arvon vastaanottajalta pääsäikeessä. Tämä on kuin noutaisit kumiankan vedestä joen päästä tai vastaanottaisit chat-viestin.

<Listing number="16-8" file-name="src/main.rs" caption='Arvon `"hi"` vastaanottaminen pääsäikeessä ja sen tulostaminen'>

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-08/src/main.rs}}
```

</Listing>

Vastaanottajalla on kaksi hyödyllistä metodia: `recv` ja `try_recv`. Käytämme `recv`-metodia, lyhenne sanasta _receive_ (vastaanottaa), joka estää pääsäikeen suorituksen ja odottaa, kunnes arvo lähetetään kanavaa pitkin. Kun arvo on lähetetty, `recv` palauttaa sen tyypissä `Result<T, E>`. Kun lähettäjä sulkeutuu, `recv` palauttaa virheen ilmaistakseen, ettei enempää arvoja ole tulossa.

`try_recv`-metodi ei estä suoritusta, vaan palauttaa tyypin `Result<T, E>` heti: `Ok`-arvon, joka sisältää viestin, jos sellainen on saatavilla, ja `Err`-arvon, jos viestejä ei tällä kertaa ole. `try_recv`-metodin käyttö on hyödyllistä, jos tällä säikeellä on muuta työtä tehtävänä viestien odottamisen ohella: voisimme kirjoittaa silmukan, joka kutsuu `try_recv`-metodia aika ajoin, käsittelee viestin, jos sellainen on saatavilla, ja muuten tekee muuta työtä hetken ennen uutta tarkistusta.

Olemme käyttäneet tässä esimerkissä `recv`-metodia yksinkertaisuuden vuoksi; pääsäikeellä ei ole muuta työtä kuin viestien odottaminen, joten pääsäikeen estäminen on asianmukaista.

Kun ajamme listauksen 16-8 koodin, näemme arvon tulostettuna pääsäikeestä:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Got: hi
```

Täydellistä!

<!-- Old headings. Do not remove or links may break. -->

<a id="channels-and-ownership-transference"></a>

### Omistajuuden siirtäminen kanavien kautta

Omistajuussäännöillä on keskeinen rooli viestien lähettämisessä, koska ne auttavat kirjoittamaan turvallista rinnakkaista koodia. Virheiden estäminen rinnakkaisohjelmoinnissa on etu, joka syntyy omistajuuden huomioimisesta koko Rust-ohjelmassasi. Tehdään koe, joka näyttää, miten kanavat ja omistajuus toimivat yhdessä estäen ongelmia: yritämme käyttää `val`-arvoa luodussa säikeessä _sen jälkeen_, kun olemme lähettäneet sen kanavaa pitkin. Kokeile kääntää listauksen 16-9 koodi nähdäksesi, miksi tämä koodi ei ole sallittu.

<Listing number="16-9" file-name="src/main.rs" caption="Yritys käyttää `val`-arvoa sen jälkeen, kun olemme lähettäneet sen kanavaa pitkin">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-09/src/main.rs}}
```

</Listing>

Tässä yritämme tulostaa `val`-arvon sen jälkeen, kun olemme lähettäneet sen kanavaa pitkin `tx.send`-kutsulla. Tämän salliminen olisi huono ajatus: kun arvo on lähetetty toiseen säikeeseen, kyseinen säie voisi muokata tai pudottaa sen ennen kuin yritämme käyttää arvoa uudelleen. Toisen säikeen muutokset voisivat aiheuttaa virheitä tai odottamattomia tuloksia epäjohdonmukaisen tai olemattoman datan vuoksi. Rust antaa kuitenkin virheen, jos yritämme kääntää listauksen 16-9 koodin:

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-09/output.txt}}
```

Rinnakkaisuusvirheemme aiheutti kääntöaikaisen virheen. `send`-funktio ottaa omistajuuden parametristaan, ja kun arvo siirretään, vastaanotin ottaa sen omistukseensa. Tämä estää meitä vahingossa käyttämästä arvoa uudelleen lähettämisen jälkeen; omistajuusjärjestelmä tarkistaa, että kaikki on kunnossa.

<!-- Old headings. Do not remove or links may break. -->

<a id="sending-multiple-values-and-seeing-the-receiver-waiting"></a>

### Useiden arvojen lähettäminen

Listauksen 16-8 koodi kääntyi ja toimi, mutta se ei selvästi näyttänyt, että kaksi erillistä säiettä kommunikoi kanavan kautta.

Listauksessa 16-10 olemme tehneet muutoksia, jotka todistavat listauksen 16-8 koodin toimivan rinnakkain: luotu säie lähettää nyt useita viestejä ja pysähtyy sekunniksi jokaisen viestin välillä.

<Listing number="16-10" file-name="src/main.rs" caption="Useiden viestien lähettäminen ja tauko jokaisen välillä">

```rust,noplayground
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-10/src/main.rs}}
```

</Listing>

Tällä kertaa luodulla säikeellä on merkkijonovektori, jonka haluamme lähettää pääsäikeeseen. Iteroimme niiden yli lähettäen jokaisen erikseen ja pysähtyen jokaisen välillä kutsumalla `thread::sleep`-funktiota yhden sekunnin `Duration`-arvolla.

Pääsäikeessä emme enää kutsu `recv`-funktiota eksplisiittisesti: sen sijaan käsittelemme `rx`:ää iteraattorina. Jokaisesta vastaanotetusta arvosta tulostamme sen. Kun kanava sulkeutuu, iteraatio päättyy.

Kun ajat listauksen 16-10 koodin, sinun pitäisi nähdä seuraava tuloste yhden sekunnin tauolla jokaisen rivin välillä:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Got: hi
Got: from
Got: the
Got: thread
```

Koska `for`-silmukassamme pääsäikeessä ei ole koodia, joka pysäyttäisi tai viivyttäisi suoritusta, voimme päätellä, että pääsäie odottaa arvoja luodulta säikeeltä.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-multiple-producers-by-cloning-the-transmitter"></a>

### Useiden tuottajien luominen

Aiemmin mainitsimme, että `mpsc` on lyhenne sanasta _multiple producer, single consumer_. Otetaan `mpsc` käyttöön ja laajennetaan listauksen 16-10 koodia luomalla useita säikeitä, jotka kaikki lähettävät arvoja samalle vastaanottajalle. Voimme tehdä näin kloonaamalla lähettäjän, kuten listauksessa 16-11 näytetään.

<Listing number="16-11" file-name="src/main.rs" caption="Useiden viestien lähettäminen useilta tuottajilta">

```rust,noplayground
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-11/src/main.rs:here}}
```

</Listing>

Tällä kertaa ennen ensimmäisen säikeen luomista kutsumme `clone`-metodia lähettäjällä. Tämä antaa meille uuden lähettäjän, jonka voimme välittää ensimmäiselle luodulle säikeelle. Välitämme alkuperäisen lähettäjän toiselle luodulle säikeelle. Näin saamme kaksi säiettä, joista kumpikin lähettää eri viestejä yhdelle vastaanottajalle.

Kun ajat koodin, tulosteesi pitäisi näyttää suunnilleen tältä:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Got: hi
Got: more
Got: from
Got: messages
Got: for
Got: the
Got: thread
Got: you
```

Saatat nähdä arvot eri järjestyksessä järjestelmästäsi riippuen. Tämä tekee rinnakkaisuudesta sekä mielenkiintoista että vaikeaa. Jos kokeilet `thread::sleep`-funktiota antamalla sille erilaisia arvoja eri säikeissä, jokainen ajo on epädeterministisempi ja tuottaa erilaisen tulosteen joka kerta.

Nyt kun olemme tarkastelleet, miten kanavat toimivat, katsotaan toista rinnakkaisuusmenetelmää.
