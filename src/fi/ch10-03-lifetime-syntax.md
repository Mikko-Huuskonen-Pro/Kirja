## Viitteiden validointi elinikien avulla

Elinikä on toinen geneerinen käsite, jota olemme jo käyttäneet. Sen sijaan, että se varmistaisi, että tyypillä on haluamamme käyttäytyminen, elinikä varmistaa, että viittaukset ovat voimassa niin kauan kuin niitä tarvitsemme.

Yksi yksityiskohta, jota emme käsitelleet [”Viittaukset ja lainaaminen”][references-and-borrowing]<!-- ignore --> -osiossa luvussa 4, on se, että jokaisella viittauksella Rustissa on _elinikä_, joka on alue, jonka ajan viittaus on voimassa. Useimmiten elinikä on implisiittinen ja päätelty, aivan kuten useimmiten tyypitkin päätellään. Meidän täytyy annotoida tyypit vain, kun useat tyypit ovat mahdollisia. Samalla tavalla meidän täytyy annotoida elinikä, kun viittausten elinikät voivat liittyä toisiinsa useilla eri tavoilla. Rust vaatii meitä annotoimaan suhteet geneeristen elinikäparametrien avulla varmistaakseen, että ajonaikaisesti käytetyt viittaukset ovat varmasti kelvollisia.

Elinikien annotointi ei ole edes käsite, jota useimmissa muissa ohjelmointikielissä on, joten tämä tuntuu tutulta. Vaikka emme käsittele elinikää kokonaisuudessaan tässä luvussa, käsittelemme yleisiä tapoja, joilla saatat kohdata elinikäsyntaksia, jotta voit tottua käsitteeseen.

### Roikkuvien viittausten estäminen elinikien avulla

Elinikien pääasiallinen tarkoitus on estää _roikkuvat viittaukset_, jotka saavat ohjelman viittaamaan dataan, johon sen ei ole tarkoitus viitata. Tarkastellaan listauksen 10-16 ohjelmaa, jossa on ulompi ja sisempi alue.

<Listing number="10-16" caption="Yritys käyttää viittausta, jonka arvo on poistunut alueelta">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-16/src/main.rs}}
```

</Listing>

> Huom: Esimerkit listauksissa 10-16, 10-17 ja 10-23 määrittelevät muuttujia antamatta niille alkuarvoa, joten muuttujan nimi on olemassa ulommalla alueella. Ensi silmäyksellä tämä saattaa näyttää ristiriitaiselta Rustin null-arvojen puuttumisen kanssa. Jos kuitenkin yritämme käyttää muuttujaa ennen arvon antamista, saamme käännösvirheen, mikä osoittaa, ettei Rust todellakaan salli null-arvoja.

Ulompi alue määrittelee muuttujan nimeltä `r` ilman alkuarvoa, ja sisempi alue määrittelee muuttujan nimeltä `x` alkuarvolla `5`. Sisemmällä alueella yritämme asettaa `r`:n arvoksi viittauksen `x`:ään. Sitten sisempi alue päättyy, ja yritämme tulostaa `r`:n arvon. Tämä koodi ei käänny, koska arvo, johon `r` viittaa, on poistunut alueelta ennen kuin yritämme käyttää sitä. Tässä on virheilmoitus:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-16/output.txt}}
```

Virheilmoitus sanoo, että muuttuja `x` ”ei elä tarpeeksi pitkään.” Syy on, että `x` on alueen ulkopuolella, kun sisempi alue päättyy rivillä 7. Mutta `r` on edelleen voimassa ulommalla alueella; koska sen alue on suurempi, sanomme sen ”elävän pidempään.” Jos Rust sallisi tämän koodin toimia, `r` viittaisi muistiin, joka vapautettiin kun `x` poistui alueelta, eikä mikään, mitä yrittäisimme tehdä `r`:llä, toimisi oikein. Miten Rust määrittää, että tämä koodi on virheellinen? Se käyttää lainantarkistinta.

### Lainantarkistin

Rustin kääntäjällä on _lainantarkistin_, joka vertaa alueita määrittääkseen, ovatko kaikki lainat kelvollisia. Listausta 10-17 näyttää saman koodin kuin listaus 10-16, mutta annotaatioilla, jotka näyttävät muuttujien elinikät.

<Listing number="10-17" caption="Muuttujien `r` ja `x` elinikien annotaatiot, nimiltään `'a` ja `'b`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-17/src/main.rs}}
```

</Listing>

Tässä olemme annotoineet `r`:n elinikäksi `'a` ja `x`:n elinikäksi `'b`. Kuten näet, sisempi `'b`-lohko on paljon pienempi kuin ulompi `'a`-elinikälohko. Käännösaikana Rust vertaa näiden kahden elinikän kokoa ja näkee, että `r`:llä on elinikä `'a`, mutta se viittaa muistiin, jonka elinikä on `'b`. Ohjelma hylätään, koska `'b` on lyhyempi kuin `'a`: viittauksen kohde ei elä niin kauan kuin viittaus.

Listausta 10-18 korjaa koodin niin, ettei siinä ole roikkuvaa viittausta, ja se kääntyy ilman virheitä.

<Listing number="10-18" caption="Kelvollinen viittaus, koska datalla on pidempi elinikä kuin viittauksella">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-18/src/main.rs}}
```

</Listing>

Tässä `x`:llä on elinikä `'b`, joka tässä tapauksessa on suurempi kuin `'a`. Tämä tarkoittaa, että `r` voi viitata `x`:ään, koska Rust tietää, että `r`:n viittaus on aina voimassa niin kauan kuin `x` on voimassa.

Nyt kun tiedät, missä viittausten elinikät ovat ja miten Rust analysoi elinikää varmistaakseen viittausten olevan aina kelvollisia, tutkitaan geneerisiä elinikäparametreja ja palautusarvoja funktioiden yhteydessä.

### Geneeriset elinikäparametrit funktioissa

Kirjoitamme funktion, joka palauttaa pidemmän kahdesta merkkijonon viipaleesta. Tämä funktio ottaa kaksi merkkijonon viipaletta ja palauttaa yhden merkkijonon viipaleen. Kun olemme toteuttaneet `longest`-funktion, listauksen 10-19 koodin pitäisi tulostaa `The longest string is abcd`.

<Listing number="10-19" file-name="src/main.rs" caption="`main`-funktio, joka kutsuu `longest`-funktiota löytääkseen pidemmän kahdesta merkkijonon viipaleesta">

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-19/src/main.rs}}
```

</Listing>

Huomaa, että haluamme funktion ottavan merkkijonon viipaleita, jotka ovat viittauksia, eivätkä merkkijonoja, koska emme halua `longest`-funktion ottavan parametriensa omistajuutta. Katso [”Merkkijonon viipaleet parametreina”][string-slices-as-parameters]<!-- ignore --> -osio luvussa 4 lisäkeskustelua siitä, miksi listauksen 10-19 parametrit ovat haluamiamme.

Jos yritämme toteuttaa `longest`-funktion kuten listauksessa 10-20, se ei käänny.

<Listing number="10-20" file-name="src/main.rs" caption="`longest`-funktion toteutus, joka palauttaa pidemmän kahdesta merkkijonon viipaleesta mutta ei vielä käänny">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-20/src/main.rs:here}}
```

</Listing>

Sen sijaan saamme seuraavan virheen, joka puhuu elinikästä:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-20/output.txt}}
```

Ohjeteksti paljastaa, että palautustyypillä täytyy olla geneerinen elinikäparametri, koska Rust ei voi kertoa, viittaako palautettava viittaus `x`:ään vai `y`:hyn. Itse asiassa emme tiedä sitäkään, koska funktion rungon `if`-lohko palauttaa viittauksen `x`:ään ja `else`-lohko viittauksen `y`:hyn!

Kun määrittelemme tämän funktion, emme tiedä konkreettisia arvoja, jotka välitetään funktioon, joten emme tiedä, suoritetaanko `if`- tai `else`-tapaus. Emme myöskään tiedä viittausten konkreettisia elinikäjä, joten emme voi tarkastella alueita kuten listauksissa 10-17 ja 10-18 määrittääksemme, onko palauttamamme viittaus aina kelvollinen. Lainantarkistin ei voi määrittää tätäkään, koska se ei tiedä, miten `x`:n ja `y`:n elinikät liittyvät palautusarvon elinikään. Korjataksemme tämän virheen lisäämme geneeriset elinikäparametrit, jotka määrittelevät viittausten välisen suhteen, jotta lainantarkistin voi suorittaa analyysinsä.

### Elinikäannotaation syntaksi

Elinikäannotaatiot eivät muuta sitä, kuinka kauan mikään viittauksista elää. Sen sijaan ne kuvaavat useiden viittausten eliniköiden välisiä suhteita vaikuttamatta elinikään. Aivan kuten funktiot voivat hyväksyä minkä tahansa tyypin, kun allekirjoituksessa määritellään geneerinen tyyppiparametri, funktiot voivat hyväksyä viittauksia millä tahansa elinikällä määrittelemällä geneerisen elinikäparametrin.

Elinikäannotaatioilla on hieman epätavallinen syntaksi: elinikäparametrien nimien täytyy alkaa heittomerkillä (`'`) ja ne ovat yleensä pieniä kirjaimia ja hyvin lyhyitä, kuten geneeriset tyypit. Useimmat ihmiset käyttävät nimeä `'a` ensimmäiselle elinikäannotaatiolle. Sijoitamme elinikäparametrien annotaatiot viittauksen `&`-merkin jälkeen käyttäen välilyöntiä erottamaan annotaation viittauksen tyypistä.

Tässä on joitakin esimerkkejä: viittaus `i32`-tyyppiin ilman elinikäparametria, viittaus `i32`-tyyppiin, jolla on elinikäparametri nimeltä `'a`, ja muokattava viittaus `i32`-tyyppiin, jolla on myös elinikä `'a`.

```rust,ignore
&i32        // a reference
&'a i32     // a reference with an explicit lifetime
&'a mut i32 // a mutable reference with an explicit lifetime
```

Yksittäisellä elinikäannotaatiolla ei ole paljon merkitystä, koska annotaatioiden tarkoitus on kertoa Rustille, miten useiden viittausten geneeriset elinikäparametrit liittyvät toisiinsa. Tarkastellaan, miten elinikäannotaatiot liittyvät toisiinsa `longest`-funktion yhteydessä.

### Elinikäannotaatiot funktioallekirjoituksissa

Käyttääksemme elinikäannotaatioita funktioallekirjoituksissa meidän täytyy määritellä geneeriset _elinikä_ parametrit kulmasulkeissa funktion nimen ja parametrilistan välissä, aivan kuten teimme geneeristen _tyyppi_ parametrien kanssa.

Haluamme allekirjoituksen ilmaisevan seuraavan rajoitteen: palautettu viittaus on voimassa niin kauan kuin molemmat parametrit ovat voimassa. Tämä on parametrien ja palautusarvon eliniköiden välinen suhde. Nimeämme elinikäparametrin `'a`:ksi ja lisäämme sen jokaiseen viittaukseen, kuten listauksessa 10-21.

<Listing number="10-21" file-name="src/main.rs" caption="`longest`-funktion määrittely, joka määrittelee kaikkien allekirjoituksen viittausten olevan saman elinikäparametrin `'a`">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-21/src/main.rs:here}}
```

</Listing>

Tämän koodin pitäisi kääntyä ja tuottaa haluamamme tuloksen, kun käytämme sitä listauksen 10-19 `main`-funktion kanssa.

Funktioallekirjoitus kertoo nyt Rustille, että jollekin elinikäparametrille `'a` funktio ottaa kaksi parametria, jotka molemmat ovat merkkijonon viipaleita, jotka elävät vähintään elinikäparametrin `'a` verran. Funktioallekirjoitus kertoo myös Rustille, että funktiosta palautettu merkkijonon viipale elää vähintään elinikäparametrin `'a` verran. Käytännössä tämä tarkoittaa, että `longest`-funktion palauttaman viittauksen elinikä on sama kuin funktioargumenttien viittaamien arvojen eliniköistä lyhyempi. Nämä suhteet ovat se, mitä haluamme Rustin käyttävän analysoidessaan tätä koodia.

Muista, että kun määrittelemme elinikäparametrit tässä funktioallekirjoituksessa, emme muuta minkään välitetyn tai palautetun arvon elinikää. Sen sijaan määrittelemme, että lainantarkistimen pitäisi hylätä arvot, jotka eivät noudata näitä rajoituksia. Huomaa, että `longest`-funktion ei tarvitse tietää tarkalleen, kuinka kauan `x` ja `y` elävät, vain että jokin alue voidaan korvata `'a`:lla, joka tyydyttää tämän allekirjoituksen.

Kun annotoimme elinikäjä funktioissa, annotaatiot menevät funktioallekirjoitukseen, eivät funktion runkoon. Elinikäannotaatiot tulevat osaksi funktion sopimusta, aivan kuten allekirjoituksen tyypit. Kun funktioallekirjoitukset sisältävät elinikäsopimuksen, Rustin kääntäjän analyysi voi olla yksinkertaisempaa. Jos funktion annotoinnissa tai sen kutsumisessa on ongelma, kääntäjän virheet voivat osoittaa tarkemmin koodin osaan ja rajoituksiin. Jos sen sijaan Rustin kääntäjä tekisi enemmän päätelmiä siitä, mitä tarkoitimme eliniköiden suhteilla, kääntäjä saattaisi pystyä osoittamaan vain koodin käyttökohtaan monta askelta ongelman syystä.

Kun välitämme konkreettisia viittauksia `longest`-funktiolle, konkreettinen elinikä, joka korvaa `'a`:n, on se osa `x`:n alueesta, joka limittyy `y`:n alueen kanssa. Toisin sanoen geneerinen elinikä `'a` saa konkreettisen elinikäparametrin, joka on yhtä suuri kuin `x`:n ja `y`:n eliniköistä lyhyempi. Koska olemme annotoineet palautetun viittauksen samalla elinikäparametrilla `'a`, palautettu viittaus on myös voimassa `x`:n ja `y`:n eliniköistä lyhyemmän ajan.

Katsotaan, miten elinikäannotaatiot rajoittavat `longest`-funktiota välittämällä viittauksia, joilla on eri konkreettiset elinikäparametrit. Listausta 10-22 on suoraviivainen esimerkki.

<Listing number="10-22" file-name="src/main.rs" caption="`longest`-funktion käyttö viittauksilla `String`-arvoihin, joilla on eri konkreettiset elinikäparametrit">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-22/src/main.rs:here}}
```

</Listing>

Tässä esimerkissä `string1` on voimassa ulomman alueen loppuun, `string2` on voimassa sisemmän alueen loppuun, ja `result` viittaa johonkin, joka on voimassa sisemmän alueen loppuun. Suorita tämä koodi ja näet lainantarkistimen hyväksyvän sen; se kääntyy ja tulostaa `The longest string is long string is long`.

Kokeillaan seuraavaksi esimerkkiä, joka osoittaa, että `result`-viittauksen elinikäparametrin täytyy olla argumenttien elinikäparametreista lyhyempi. Siirrämme `result`-muuttujan määrittelyn sisemmän alueen ulkopuolelle, mutta jätämme arvon osoittamisen `result`-muuttujalle sisemmälle alueelle `string2`:n kanssa. Siirrämme sitten `println!`-kutsun, joka käyttää `result`-muuttujaa, sisemmän alueen ulkopuolelle, sen jälkeen kun sisempi alue on päättynyt. Listauksen 10-23 koodi ei käänny.

<Listing number="10-23" file-name="src/main.rs" caption="Yritys käyttää `result`-muuttujaa sen jälkeen, kun `string2` on poistunut alueelta">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-23/src/main.rs:here}}
```

</Listing>

Kun yritämme kääntää tämän koodin, saamme tämän virheen:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-23/output.txt}}
```

Virhe osoittaa, että jotta `result` olisi kelvollinen `println!`-lausekkeelle, `string2`:n täytyisi olla voimassa ulomman alueen loppuun. Rust tietää tämän, koska annotoimme funktioiden parametrien ja palautusarvojen elinikäparametrit samalla elinikäparametrilla `'a`.

Ihmisenä voimme katsoa tätä koodia ja nähdä, että `string1` on pidempi kuin `string2`, ja siksi `result` sisältää viittauksen `string1`:een. Koska `string1` ei ole vielä poistunut alueelta, viittaus `string1`:een on edelleen kelvollinen `println!`-lausekkeelle. Kääntäjä ei kuitenkaan näe viittauksen olevan kelvollinen tässä tapauksessa. Olemme kertoneet Rustille, että `longest`-funktion palauttaman viittauksen elinikäparametri on sama kuin välitettyjen viittausten elinikäparametreista lyhyempi. Siksi lainantarkistin kieltää listauksen 10-23 koodin mahdollisesti virheellisenä viittauksena.

Kokeile suunnitella lisää kokeita, joissa vaihtelet `longest`-funktiolle välitettyjen viittausten arvoja ja elinikäparametreja sekä sitä, miten palautettua viittausta käytetään. Tee hypoteeseja siitä, läpäisevätkö kokeesi lainantarkistimen ennen kuin käännät; tarkista sitten, olitko oikeassa!

### Ajattelu elinikäparametrien näkökulmasta

Tapa, jolla sinun täytyy määritellä elinikäparametrit, riippuu siitä, mitä funktiosi tekee. Jos esimerkiksi muuttaisimme `longest`-funktion toteutusta palauttamaan aina ensimmäisen parametrin pidemmän merkkijonon viipaleen sijaan, emme tarvitsisi elinikäparametria `y`-parametrille. Seuraava koodi kääntyy:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-08-only-one-reference-with-lifetime/src/main.rs:here}}
```

</Listing>

Olemme määritelleet elinikäparametrin `'a` parametrille `x` ja palautustyypille, mutta emme parametrille `y`, koska `y`:n elinikäparametrilla ei ole mitään suhdetta `x`:n tai palautusarvon elinikäparametriin.

Kun palautamme viittauksen funktiosta, palautustyypin elinikäparametrin täytyy vastata jonkin parametrin elinikäparametria. Jos palautettu viittaus _ei_ viittaa johonkin parametreista, sen täytyy viitata tässä funktiossa luotuun arvoon. Tämä olisi kuitenkin roikkuva viittaus, koska arvo poistuu alueelta funktion lopussa. Tarkastele tätä yritystä toteuttaa `longest`-funktio, joka ei käänny:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-09-unrelated-lifetime/src/main.rs:here}}
```

</Listing>

Tässä, vaikka olemme määritelleet elinikäparametrin `'a` palautustyypille, tämä toteutus ei käänny, koska palautusarvon elinikäparametrilla ei ole mitään tekemistä parametrien elinikäparametrien kanssa. Tässä on virheilmoitus, jonka saamme:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-09-unrelated-lifetime/output.txt}}
```

Ongelma on, että `result` poistuu alueelta ja siivotaan `longest`-funktion lopussa. Yritämme myös palauttaa viittauksen `result`-muuttujaan funktiosta. Emme voi määritellä elinikäparametreja, jotka muuttaisivat roikkuvaa viittausta, eikä Rust anna meidän luoda roikkuvaa viittausta. Tässä tapauksessa paras korjaus olisi palauttaa omistettu datatyyppi viittauksen sijaan, jolloin kutsupuolen funktio on vastuussa arvon siivoamisesta.

Lopulta elinikäsyntaksi liittyy eri funktioiden parametrien ja palautusarvojen elinikäparametrien yhdistämiseen. Kun ne on yhdistetty, Rustilla on tarpeeksi tietoa salliakseen muistiturvalliset operaatiot ja kieltääkseen operaatiot, jotka luovat roikkuvia osoittimia tai muuten rikkovat muistiturvallisuutta.

### Elinikäannotaatiot rakenteen määrittelyissä

Tähän asti määrittelemämme rakenteet ovat sisältäneet omistettuja tyyppejä. Voimme määritellä rakenteita, jotka sisältävät viittauksia, mutta siinä tapauksessa meidän täytyy lisätä elinikäannotaatio jokaiseen viittaukseen rakenteen määrittelyssä. Listauksessa 10-24 on rakenne nimeltä `ImportantExcerpt`, joka sisältää merkkijonon viipaleen.

<Listing number="10-24" file-name="src/main.rs" caption="Rakenne, joka sisältää viittauksen ja vaatii elinikäannotaation">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-24/src/main.rs}}
```

</Listing>

Tällä rakenteella on yksi kenttä `part`, joka sisältää merkkijonon viipaleen eli viittauksen. Kuten geneeristen datatyyppien kanssa, määrittelemme geneerisen elinikäparametrin nimen kulmasulkeissa rakenteen nimen jälkeen, jotta voimme käyttää elinikäparametria rakenteen rungon määrittelyssä. Tämä annotaatio tarkoittaa, että `ImportantExcerpt`-instanssi ei voi elää pidempään kuin viittaus, jonka se sisältää `part`-kentässään.

Tässä `main`-funktiossa luodaan `ImportantExcerpt`-rakenteen instanssi, joka sisältää viittauksen `novel`-muuttujan omistaman `String`-arvon ensimmäiseen lauseeseen. `novel`-muuttujan data on olemassa ennen `ImportantExcerpt`-instanssin luomista. Lisäksi `novel` ei poistu alueelta ennen kuin `ImportantExcerpt` poistuu alueelta, joten `ImportantExcerpt`-instanssin viittaus on kelvollinen.

### Elinikäparametrien päättely

Olet oppinut, että jokaisella viittauksella on elinikäparametri ja että sinun täytyy määritellä elinikäparametrit funktioille tai rakenteille, jotka käyttävät viittauksia. Meillä oli kuitenkin funktio listauksessa 4-9, joka näytetään uudelleen listauksessa 10-25, ja se kääntyi ilman elinikäannotaatioita.

<Listing number="10-25" file-name="src/lib.rs" caption="Funktio, jonka määrittelimme listauksessa 4-9 ja joka kääntyi ilman elinikäannotaatioita, vaikka parametri ja palautustyyppi ovat viittauksia">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-25/src/main.rs:here}}
```

</Listing>

Syy siihen, miksi tämä funktio kääntyy ilman elinikäannotaatioita, on historiallinen: Rustin varhaisissa versioissa (ennen 1.0) tämä koodi ei olisi kääntynyt, koska jokainen viittaus tarvitsi eksplisiittisen elinikäparametrin. Silloin funktioallekirjoitus olisi kirjoitettu näin:

```rust,ignore
fn first_word<'a>(s: &'a str) -> &'a str {
```

Kun Rust-tiimi oli kirjoittanut paljon Rust-koodia, he huomasivat Rust-ohjelmoijien syöttävän samoja elinikäannotaatioita yhä uudelleen tietyissä tilanteissa. Nämä tilanteet olivat ennustettavia ja noudattivat muutamia deterministisiä kaavoja. Kehittäjät ohjelmoivat nämä kaavat kääntäjän koodiin, jotta lainantarkistin voisi päätellä elinikäparametrit näissä tilanteissa eikä tarvitsisi eksplisiittisiä annotaatioita.

Tämä Rustin historia on relevanttia, koska on mahdollista, että lisää deterministisiä kaavoja löytyy ja lisätään kääntäjään. Tulevaisuudessa elinikäannotaatioita saatetaan tarvita vielä vähemmän.

Kääntäjän viittausanalyysiin ohjelmoituja kaavoja kutsutaan _elinikäparametrien päättelysäännöiksi_. Nämä eivät ole sääntöjä ohjelmoijille noudatettavaksi; ne ovat joukko erityistapauksia, joita kääntäjä harkitsee, ja jos koodisi sopii näihin tapauksiin, sinun ei tarvitse kirjoittaa elinikäparametreja eksplisiittisesti.

Päättelysäännöt eivät tarjoa täyttä päättelyä. Jos viittausten elinikäparametreista on edelleen epäselvyyttä sen jälkeen, kun Rust on soveltanut sääntöjä, kääntäjä ei arvaa jäljellä olevien viittausten elinikäparametreja. Sen sijaan kääntäjä antaa virheen, jonka voit ratkaista lisäämällä elinikäannotaatiot.

Funktio- tai metodiparametrien elinikäparametreja kutsutaan _tuloelinikäparametreiksi_, ja palautusarvojen elinikäparametreja _tulostuselinikäparametreiksi_.

Kääntäjä käyttää kolmea sääntöä selvittääkseen viittausten elinikäparametrit, kun eksplisiittisiä annotaatioita ei ole. Ensimmäinen sääntö koskee tuloelinikäparametreja, ja toinen ja kolmas sääntö koskevat tulostuselinikäparametreja. Jos kääntäjä pääsee kolmen säännön loppuun ja viittauksia on vielä, joiden elinikäparametreja se ei voi selvittää, kääntäjä pysähtyy virheeseen. Nämä säännöt koskevat `fn`-määrittelyjä sekä `impl`-lohkoja.

Ensimmäinen sääntö on, että kääntäjä määrittää elinikäparametrin jokaiselle viittausparametrille. Toisin sanoen funktio, jolla on yksi parametri, saa yhden elinikäparametrin: `fn foo<'a>(x: &'a i32)`; funktio, jolla on kaksi parametria, saa kaksi erillistä elinikäparametria: `fn foo<'a, 'b>(x: &'a i32, y: &'b i32)`; ja niin edelleen.

Toinen sääntö on, että jos on täsmälleen yksi tuloelinikäparametri, se elinikäparametri määritetään kaikille tulostuselinikäparametreille: `fn foo<'a>(x: &'a i32) -> &'a i32`.

Kolmas sääntö on, että jos on useita tuloelinikäparametreja, mutta yksi niistä on `&self` tai `&mut self`, koska kyseessä on metodi, `self`:n elinikäparametri määritetään kaikille tulostuselinikäparametreille. Tämä kolmas sääntö tekee metodeista paljon miellyttävämpiä lukea ja kirjoittaa, koska vähemmän symboleja tarvitaan.

Oletetaan olevamme kääntäjä. Sovelletaan näitä sääntöjä selvittääksemme viittausten elinikäparametrit `first_word`-funktion allekirjoituksessa listauksessa 10-25. Allekirjoitus alkaa ilman elinikäparametreja, jotka liittyisivät viittauksiin:

```rust,ignore
fn first_word(s: &str) -> &str {
```

Sitten kääntäjä soveltaa ensimmäistä sääntöä, joka määrittelee, että jokainen parametri saa oman elinikäparametrinsa. Kutsumme sitä tavalliseen tapaan `'a`:ksi, joten allekirjoitus on nyt tämä:

```rust,ignore
fn first_word<'a>(s: &'a str) -> &str {
```

Toinen sääntö pätee, koska on täsmälleen yksi tuloelinikäparametri. Toinen sääntö määrittelee, että yhden tuloelinikäparametrin elinikäparametri määritetään tulostuselinikäparametrille, joten allekirjoitus on nyt tämä:

```rust,ignore
fn first_word<'a>(s: &'a str) -> &'a str {
```

Nyt kaikilla viittauksilla tässä funktioallekirjoituksessa on elinikäparametrit, ja kääntäjä voi jatkaa analyysiään ilman, että ohjelmoijan täytyy annotoida elinikäparametreja tässä funktioallekirjoituksessa.

Katsotaan toista esimerkkiä, tällä kertaa `longest`-funktiosta, jolla ei ollut elinikäparametreja, kun aloimme työskennellä sen kanssa listauksessa 10-20:

```rust,ignore
fn longest(x: &str, y: &str) -> &str {
```

Sovelletaan ensimmäistä sääntöä: jokainen parametri saa oman elinikäparametrinsa. Tällä kertaa meillä on kaksi parametria yhden sijaan, joten meillä on kaksi elinikäparametria:

```rust,ignore
fn longest<'a, 'b>(x: &'a str, y: &'b str) -> &str {
```

Näet, että toinen sääntö ei päde, koska on useampi kuin yksi tuloelinikäparametri. Kolmas sääntö ei myöskään päde, koska `longest` on funktio eikä metodi, joten mikään parametreistä ei ole `self`. Kun olemme käyneet läpi kaikki kolme sääntöä, emme ole vieläkään selvittäneet palautustyypin elinikäparametria. Tämän vuoksi saimme virheen yrittäessämme kääntää listauksen 10-20 koodia: kääntäjä kävi läpi elinikäparametrien päättelysäännöt, mutta ei voinut silti selvittää kaikkia viittausten elinikäparametreja allekirjoituksessa.

Koska kolmas sääntö pätee todella vain metodien allekirjoituksissa, katsomme elinikäparametreja siinä yhteydessä seuraavaksi nähdäksemme, miksi kolmas sääntö tarkoittaa, ettei meidän tarvitse annotoida elinikäparametreja metodien allekirjoituksissa kovin usein.

### Elinikäannotaatiot metodimäärittelyissä

Kun toteutamme metodeja rakenteelle, jolla on elinikäparametreja, käytämme samaa syntaksia kuin geneeristen tyyppiparametrien kanssa, kuten listauksessa 10-11. Missä määrittelemme ja käytämme elinikäparametreja riippuu siitä, liittyvätkö ne rakenteen kenttiin vai metodin parametreihin ja palautusarvoihin.

Rakenteen kenttien elinikäparametrien nimet täytyy aina määritellä `impl`-avainsanan jälkeen ja sitten käyttää rakenteen nimen jälkeen, koska nämä elinikäparametrit ovat osa rakenteen tyyppiä.

`impl`-lohkon sisällä olevissa metodien allekirjoituksissa viittaukset voivat liittyä rakenteen kenttien viittausten elinikäparametreihin tai olla riippumattomia. Lisäksi elinikäparametrien päättelysäännöt usein tekevät elinikäannotaatiot tarpeettomiksi metodien allekirjoituksissa. Katsotaan esimerkkejä käyttäen `ImportantExcerpt`-rakennetta, jonka määrittelimme listauksessa 10-24.

Ensin käytämme metodia nimeltä `level`, jonka ainoa parametri on viittaus `self`:ään ja jonka palautusarvo on `i32`, joka ei ole viittaus mihinkään:

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-10-lifetimes-on-methods/src/main.rs:1st}}
```

Elinikäparametrin määrittely `impl`-avainsanan jälkeen ja sen käyttö tyypin nimen jälkeen ovat pakollisia, mutta emme tarvitse annotoida `self`-viittauksen elinikäparametria ensimmäisen päättelysäännön vuoksi.

Tässä on esimerkki, jossa kolmas elinikäparametrien päättelysääntö pätee:

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-10-lifetimes-on-methods/src/main.rs:3rd}}
```

On kaksi tuloelinikäparametria, joten Rust soveltaa ensimmäistä elinikäparametrien päättelysääntöä ja antaa sekä `&self`:lle että `announcement`:ille omat elinikäparametrinsa. Sitten, koska yksi parametreistä on `&self`, palautustyypille määritetään `&self`:n elinikäparametri, ja kaikki elinikäparametrit on huomioitu.

### Staattinen elinikäparametri

Yksi erityinen elinikäparametri, josta meidän täytyy puhua, on `'static`, joka tarkoittaa, että kyseinen viittaus _voi_ elää koko ohjelman keston. Kaikilla merkkijonoliteraaleilla on `'static`-elinikäparametri, jonka voimme annotoida seuraavasti:

```rust
let s: &'static str = "I have a static lifetime.";
```

Tämän merkkijonon teksti on tallennettu suoraan ohjelman binaariin, joka on aina saatavilla. Siksi kaikkien merkkijonoliteraalien elinikäparametri on `'static`.

Saatat nähdä virheilmoituksissa ehdotuksia käyttää `'static`-elinikäparametria. Ennen kuin määrittelet `'static`-elinikäparametrin viittaukselle, mieti, elääkö viittauksesi todella koko ohjelmasi elinikäparametrin ajan ja haluatko sen elävän niin. Useimmiten virheilmoitus, joka ehdottaa `'static`-elinikäparametria, johtuu roikkuvan viittauksen luomisyrityksestä tai elinikäparametrien yhteensopimattomuudesta. Tällaisissa tapauksissa ratkaisu on korjata nämä ongelmat, ei määritellä `'static`-elinikäparametria.

## Geneeriset tyyppiparametrit, trait-rajat ja elinikäparametrit yhdessä

Katsotaan lyhyesti syntaksia, jolla määritellään geneeriset tyyppiparametrit, trait-rajat ja elinikäparametrit samassa funktiossa!

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-11-generics-traits-and-lifetimes/src/main.rs:here}}
```

Tämä on `longest`-funktio listauksesta 10-21, joka palauttaa pidemmän kahdesta merkkijonon viipaleesta. Mutta nyt siinä on ylimääräinen parametri nimeltä `ann` geneerisellä tyypillä `T`, joka voidaan täyttää millä tahansa tyypillä, joka toteuttaa `Display`-traitin `where`-lausekkeen määrittämällä tavalla. Tämä ylimääräinen parametri tulostetaan `{}`-merkinnällä, minkä vuoksi `Display`-trait-raja on tarpeen. Koska elinikäparametrit ovat eräänlainen geneerisyys, elinikäparametrin `'a` ja geneerisen tyyppiparametrin `T` määrittelyt menevät samaan listaan kulmasulkeissa funktion nimen jälkeen.

## Yhteenveto

Käsittelimme paljon tässä luvussa! Nyt kun tiedät geneerisistä tyyppiparametreista, traeiteista ja trait-rajoista sekä geneerisistä elinikäparametreista, olet valmis kirjoittamaan toistamatonta koodia, joka toimii monissa eri tilanteissa. Geneeriset tyyppiparametrit antavat sinun soveltaa koodia eri tyyppeihin. Traitit ja trait-rajat varmistavat, että vaikka tyypit ovat geneerisiä, niillä on koodin tarvitsema käyttäytyminen. Opit käyttämään elinikäannotaatioita varmistaaksesi, ettei tämä joustava koodi sisällä roikkuvia viittauksia. Ja kaikki tämä analyysi tapahtuu käännösaikana, mikä ei vaikuta suorituskykyyn!

Usko tai älä, aiheista, joita käsittelimme tässä luvussa, on vielä paljon opittavaa: luku 18 käsittelee trait-objekteja, jotka ovat toinen tapa käyttää traeiteja. On myös monimutkaisempia tilanteita, joissa tarvitset elinikäannotaatioita vain hyvin edistyneissä skenaarioissa; niitä varten sinun pitäisi lukea [Rust Reference][reference]. Mutta seuraavaksi opit kirjoittamaan testejä Rustissa varmistaaksesi, että koodisi toimii haluamallasi tavalla.

[references-and-borrowing]: ch04-02-references-and-borrowing.html#references-and-borrowing
[string-slices-as-parameters]: ch04-03-slices.html#string-slices-as-parameters
[reference]: ../reference/index.html
