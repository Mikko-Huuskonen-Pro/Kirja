## `panic!` vai ei?

Miten siis päätät, milloin sinun pitäisi kutsua `panic!`:ia ja milloin palauttaa `Result`? Kun koodi panikoi, palautumista ei ole mahdollista. Voit kutsua `panic!`:ia mihin tahansa virhetilanteeseen, onko mahdollinen tapa palautua vai ei, mutta silloin teet päätöksen, että tilanne on palautumaton kutsuvalle koodille. Kun valitset palauttaa `Result`-arvon, annat kutsuvalle koodille vaihtoehtoja. Kutsuva koodi voi valita yrittää palautua tavalla, joka sopii sen tilanteeseen, tai se voi päättää, että `Err`-arvo tässä tapauksessa on palautumaton, jolloin se voi kutsua `panic!`:ia ja muuttaa palautuvan virheesi palautumattomaksi. Siksi `Result`:in palauttaminen on hyvä oletusvalinta, kun määrittelet funktion, joka voi epäonnistua.

Tilanteissa kuten esimerkeissä, prototyyppikoodissa ja testeissä on sopivampaa kirjoittaa koodia, joka panikoi `Result`:in palauttamisen sijaan. Tutkitaan miksi, ja sitten käsitellään tilanteita, joissa kääntäjä ei voi kertoa, että epäonnistuminen on mahdotonta, mutta sinä ihmisenä voit. Luku päättyy yleisiin ohjeisiin siitä, milloin panikoida kirjastokoodissa.

### Esimerkit, prototyyppikoodi ja testit

Kun kirjoitat esimerkkiä havainnollistamaan jotain käsitettä, vankan virheenkäsittelykoodin sisällyttäminen voi tehdä esimerkistä epäselvemmän. Esimerkeissä ymmärretään, että metodin, kuten `unwrap`:in, kutsuminen, joka voi panikoida, on tarkoitettu paikanpitäjäksi sille tavalle, jolla haluat sovelluksesi käsittelevän virheet, mikä voi vaihdella sen mukaan, mitä muu koodisi tekee.

Vastaavasti `unwrap`- ja `expect`-metodit ovat erittäin käteviä prototyyppauksessa, kun et ole vielä valmis päättämään, miten käsitellä virheitä. Ne jättävät selkeät merkit koodiisi siihen asti, kun olet valmis tekemään ohjelmastasi vankemman.

Jos metodikutsu epäonnistuu testissä, haluat koko testin epäonnistuvan, vaikka kyseinen metodi ei olisikaan testattava toiminnallisuus. Koska `panic!` on tapa, jolla testi merkitään epäonnistuneeksi, `unwrap`:in tai `expect`:in kutsuminen on juuri sitä, mitä pitäisi tapahtua.

<!-- Old headings. Do not remove or links may break. -->

<a id="cases-in-which-you-have-more-information-than-the-compiler"></a>

### Kun sinulla on enemmän tietoa kuin kääntäjällä

Olisi myös sopivaa kutsua `expect`:ia, kun sinulla on muuta logiikkaa, joka varmistaa, että `Result`:illa on `Ok`-arvo, mutta logiikka ei ole sellaista, mitä kääntäjä ymmärtää. Sinulla on silti `Result`-arvo, joka on käsiteltävä: mikä tahansa kutsumasi operaatio voi silti epäonnistua yleisesti, vaikka se olisi loogisesti mahdotonta juuri sinun tilanteessasi. Jos voit varmistaa tarkastamalla koodin manuaalisesti, ettet koskaan saa `Err`-varianttia, on täysin hyväksyttävää kutsua `expect`:ia ja dokumentoida syy, miksi uskot, ettei koskaan saa `Err`-varianttia, argumenttitekstissä. Tässä on esimerkki:

```rust
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-08-unwrap-that-cant-fail/src/main.rs:here}}
```

Luomme `IpAddr`-instanssin jäsentämällä kovakoodatun merkkijonon. Näemme, että `127.0.0.1` on kelvollinen IP-osoite, joten `expect`:in käyttö on tässä hyväksyttävää. Kovakoodatun kelvollisen merkkijonon olemassaolo ei kuitenkaan muuta `parse`-metodin palautustyyppiä: saamme silti `Result`-arvon, ja kääntäjä pakottaa meidät käsittelemään `Result`:ia ikään kuin `Err`-variantti olisi mahdollisuus, koska kääntäjä ei ole tarpeeksi älykäs nähdäkseen, että tämä merkkijono on aina kelvollinen IP-osoite. Jos IP-osoitemerkkijono tulisi käyttäjältä sen sijaan, että se olisi kovakoodattu ohjelmaan ja siksi _voisi_ epäonnistua, käsittelisimme ehdottomasti `Result`:ia vankemmalla tavalla. Oletuksen mainitseminen, että tämä IP-osoite on kovakoodattu, kehottaa meitä muuttamaan `expect`:in paremmaksi virheenkäsittelykoodiksi, jos tulevaisuudessa tarvitsemme hakea IP-osoitteen jostain muusta lähteestä.

### Ohjeita virheenkäsittelyyn

On suositeltavaa, että koodisi panikoi, kun on mahdollista, että koodisi päätyy huonoon tilaan. Tässä kontekstissa _huono tila_ tarkoittaa tilannetta, jossa jokin oletus, takuu, sopimus tai invariantti on rikottu, kuten kun virheellisiä arvoja, ristiriitaisia arvoja tai puuttuvia arvoja välitetään koodillesi—plus yksi tai useampi seuraavista:

- Huono tila on jotain odottamatonta, toisin kuin jotain, mikä todennäköisesti tapahtuu satunnaisesti, kuten käyttäjä syöttää dataa väärässä muodossa.
- Koodisi tästä eteenpäin on luotettava siihen, ettei ole tässä huonossa tilassa, sen sijaan että tarkistaisi ongelman jokaisessa vaiheessa.
- Ei ole hyvää tapaa koodata tätä tietoa käyttämiisi tyyppeihin. Käymme läpi esimerkin siitä, mitä tarkoitamme kohdassa [”Tilojen ja käyttäytymisen koodaus tyypeillä”][encoding]<!-- ignore --> luvussa 18.

Jos joku kutsuu koodiasi ja välittää arvoja, jotka eivät ole järkeviä, on parasta palauttaa virhe, jos voit, jotta kirjastosi käyttäjä voi päättää, mitä tehdä kyseisessä tapauksessa. Jos kuitenkin jatkaminen voisi olla epäturvallista tai haitallista, paras valinta saattaa olla kutsua `panic!`:ia ja hälyttää kirjastosi käyttäjä heidän koodinsa bugista, jotta he voivat korjata sen kehityksen aikana. Vastaavasti `panic!` on usein sopivaa, jos kutsut ulkoista koodia, joka on hallintasi ulkopuolella ja palauttaa virheellisen tilan, jota et voi korjata.

Kun epäonnistuminen on odotettavissa, on sopivampaa palauttaa `Result` kuin kutsua `panic!`:ia. Esimerkkejä ovat jäsentäjälle annettu virheellinen data tai HTTP-pyyntö, joka palauttaa tilan, joka ilmaisee, että olet osunut nopeusrajoitukseen. Näissä tapauksissa `Result`:in palauttaminen ilmaisee, että epäonnistuminen on odotettu mahdollisuus, jonka kutsuvan koodin on päätettävä, miten käsitellä.

Kun koodisi suorittaa operaation, joka voi asettaa käyttäjän riskiin, jos sitä kutsutaan virheellisillä arvoilla, koodisi pitäisi ensin varmistaa, että arvot ovat kelvollisia, ja panikoida, jos arvot eivät ole kelvollisia. Tämä on pääasiassa turvallisuussyistä: Yritys käsitellä virheellistä dataa voi altistaa koodisi haavoittuvuuksille. Tämä on pääsyy, miksi standardikirjasto kutsuu `panic!`:ia, jos yrität muistin käyttöä alueen ulkopuolelta: Yritys käyttää muistia, joka ei kuulu nykyiseen tietorakenteeseen, on yleinen turvallisuusongelma. Funktioilla on usein _sopimuksia_: Niiden käyttäytymistä taataan vain, jos syötteet täyttävät tietyt vaatimukset. Panikointi, kun sopimus rikotaan, on järkevää, koska sopimusrikkomus osoittaa aina kutsupuolen bugia, eikä se ole sellainen virhe, jonka haluat kutsuvan koodin käsittelevän eksplisiittisesti. Itse asiassa ei ole järkevää tapaa kutsuvalle koodille palautua; kutsupuolen _ohjelmoijien_ on korjattava koodi. Funktion sopimukset, erityisesti kun rikkomus aiheuttaa paniikin, tulisi selittää funktion API-dokumentaatiossa.

Paljon virhetarkistuksia kaikissa funktioissasi olisi kuitenkin sanallista ja ärsyttävää. Onneksi voit käyttää Rustin tyyppijärjestelmää (ja siten kääntäjän tekemää tyyppitarkistusta) tekemään monia tarkistuksista puolestasi. Jos funktiollasi on tietty tyyppi parametrina, voit jatkaa koodisi logiikkaa tietäen, että kääntäjä on jo varmistanut, että sinulla on kelvollinen arvo. Esimerkiksi jos sinulla on tyyppi `Option`:in sijaan, ohjelmasi odottaa _jotain_ eikä _ei mitään_. Koodisi ei sitten tarvitse käsitellä kahta tapausta `Some`- ja `None`-varianteille: sillä on vain yksi tapaus, jossa arvo on varmasti olemassa. Koodi, joka yrittää välittää ei mitään funktiollesi, ei edes käänny, joten funktiosi ei tarvitse tarkistaa kyseistä tapausta ajonaikana. Toinen esimerkki on etumerkittömän kokonaislukutyypin, kuten `u32`:n, käyttö, joka varmistaa, että parametri ei ole koskaan negatiivinen.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-custom-types-for-validation"></a>

### Mukautetut tyypit validointiin

Viedään ajatus Rustin tyyppijärjestelmän käytöstä kelvollisen arvon varmistamiseksi askeleen pidemmälle ja katsotaan mukautetun tyypin luomista validointiin. Muista arvauspeli luvusta 2, jossa koodimme pyysi käyttäjää arvaamaan luvun välillä 1 ja 100. Emme koskaan validoineet, että käyttäjän arvaus oli näiden lukujen välillä ennen kuin tarkistimme sen salaisen lukuamme vastaan; validoimme vain, että arvaus oli positiivinen. Tässä tapauksessa seuraukset eivät olleet kovin vakavat: Tulosteemme ”Liian korkea” tai ”Liian matala” olisi silti oikein. Mutta olisi hyödyllinen parannus ohjata käyttäjää kohti kelvollisia arvauksia ja saada eri käyttäytyminen, kun käyttäjä arvaa luvun, joka on alueen ulkopuolella, verrattuna tilanteeseen, jossa käyttäjä kirjoittaa esimerkiksi kirjaimia numeroiden sijaan.

Yksi tapa tehdä tämä olisi jäsentää arvaus `i32`:ksi pelkän `u32`:n sijaan salliakseen mahdollisesti negatiiviset luvut, ja sitten lisätä tarkistus, että luku on alueella, näin:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-09-guess-out-of-range/src/main.rs:here}}
```

</Listing>

`if`-lauseke tarkistaa, onko arvomme alueen ulkopuolella, kertoo käyttäjälle ongelmasta ja kutsuu `continue`:a aloittaakseen silmukan seuraavan iteraation ja pyytääkseen uuden arvauksen. `if`-lausekkeen jälkeen voimme jatkaa `guess`:n ja salaisen luvun vertailuja tietäen, että `guess` on välillä 1 ja 100.

Tämä ei kuitenkaan ole ihanteellinen ratkaisu: Jos olisi ehdottoman kriittistä, että ohjelma toimisi vain arvoilla välillä 1 ja 100, ja sillä olisi monia funktioita tällä vaatimuksella, tällaisen tarkistuksen tekeminen jokaisessa funktiossa olisi työlästä (ja saattaisi vaikuttaa suorituskykyyn).

Sen sijaan voimme luoda uuden tyypin erilliseen moduuliin ja sijoittaa validoinnit funktioon, joka luo tyypin instanssin, sen sijaan että toistaisimme validoinnit kaikkialla. Näin on turvallista funktioiden käyttää uutta tyyppiä signatuureissaan ja luottaa saamiinsa arvoihin. Listaus 9-13 näyttää yhden tavan määritellä `Guess`-tyyppi, joka luo `Guess`-instanssin vain, jos `new`-funktio saa arvon välillä 1 ja 100.

<Listing number="9-13" caption="`Guess`-tyyppi, joka jatkaa vain arvoilla välillä 1 ja 100" file-name="src/guessing_game.rs">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-13/src/guessing_game.rs}}
```

</Listing>

Huomaa, että tämä koodi tiedostossa *src/guessing_game.rs* riippuu moduulimäärittelyn `mod guessing_game;` lisäämisestä tiedostoon *src/lib.rs*, jota emme ole näyttäneet tässä. Tämän uuden moduulin tiedostossa määrittelemme structin nimeltä `Guess`, jolla on kenttä nimeltä `value`, joka tallentaa `i32`:n. Tähän tallennetaan luku.

Sitten toteutamme assosioitun funktion nimeltä `new` tyypille `Guess`, joka luo `Guess`-arvojen instansseja. `new`-funktio on määritelty ottamaan yksi parametri nimeltä `value` tyyppiä `i32` ja palauttamaan `Guess`:in. `new`-funktion rungon koodi testaa `value`:n varmistaakseen, että se on välillä 1 ja 100. Jos `value` ei läpäise tätä testiä, kutsumme `panic!`:ia, mikä hälyttää kutsupuolen ohjelmoijan, että heillä on bugi korjattavana, koska `Guess`:in luominen `value`:lla tämän alueen ulkopuolella rikkoisi sopimuksen, johon `Guess::new` luottaa. Olosuhteet, joissa `Guess::new` saattaa panikoida, tulisi käsitellä sen julkisessa API-dokumentaatiossa; käsittelemme dokumentointikäytäntöjä, jotka ilmaisevat `panic!`:in mahdollisuuden luomassasi API-dokumentaatiossa luvussa 14. Jos `value` läpäisee testin, luomme uuden `Guess`:in, jonka `value`-kenttä on asetettu `value`-parametriin, ja palautamme `Guess`:in.

Seuraavaksi toteutamme metodin nimeltä `value`, joka lainaa `self`:ää, ei ota muita parametreja ja palauttaa `i32`:n. Tällaisia metodeja kutsutaan joskus _gettereiksi_, koska niiden tarkoitus on saada dataa kentistään ja palauttaa se. Tämä julkinen metodi on tarpeen, koska `Guess`-structin `value`-kenttä on yksityinen. On tärkeää, että `value`-kenttä on yksityinen, jotta `Guess`-structia käyttävä koodi ei saa asettaa `value`:a suoraan: `guessing_game`-moduulin ulkopuolinen koodi _täytyy_ käyttää `Guess::new`-funktiota luodakseen `Guess`-instanssin, varmistaen näin, ettei `Guess`:illä voi olla `value`:a, jota `Guess::new`-funktion ehtoja ei ole tarkistettu.

Funktio, jolla on parametri tai joka palauttaa vain lukuja välillä 1 ja 100, voi sitten ilmoittaa signatuurissaan, että se ottaa tai palauttaa `Guess`:in `i32`:n sijaan, eikä sen tarvitse tehdä lisätarkistuksia rungossaan.

## Yhteenveto

Rustin virheenkäsittelyominaisuudet on suunniteltu auttamaan sinua kirjoittamaan vankempaa koodia. `panic!`-makro ilmaisee, että ohjelmasi on tilassa, jota se ei voi käsitellä, ja antaa sinun kertoa prosessille pysähtyä sen sijaan, että yrittäisit jatkaa virheellisillä tai vääriä arvoilla. `Result`-enum käyttää Rustin tyyppijärjestelmää ilmaisemaan, että operaatiot voivat epäonnistua tavalla, josta koodisi voi palautua. Voit käyttää `Result`:ia kertomaan koodille, joka kutsuu koodiasi, että sen on käsiteltävä mahdollinen onnistuminen tai epäonnistuminen. `panic!`:in ja `Result`:in käyttö sopivissa tilanteissa tekee koodistasi luotettavamman väistämättömien ongelmien edessä.

Nyt kun olet nähnyt hyödyllisiä tapoja, joilla standardikirjasto käyttää geneerisiä tyyppejä `Option`- ja `Result`-enumien kanssa, puhumme siitä, miten geneeriset tyypit toimivat ja miten voit käyttää niitä koodissasi.

[encoding]: ch18-03-oo-design-patterns.html#encoding-states-and-behavior-as-types
