## Refaktorointi modulariteetin ja virheenkäsittelyn parantamiseksi

Parantaaksemme ohjelmaamme korjaamme neljä ongelmaa, jotka liittyvät ohjelman rakenteeseen ja siihen, miten se käsittelee mahdollisia virheitä. Ensinnäkin `main`-funktiomme suorittaa nyt kaksi tehtävää: se jäsentää argumentit ja lukee tiedostoja. Ohjelman kasvaessa `main`-funktion käsittelemien erillisten tehtävien määrä kasvaa. Kun funktio saa lisää vastuita, sitä on vaikeampi ymmärtää, vaikeampi testata ja vaikeampi muuttaa rikkomatta jotakin sen osista. On parasta erottaa toiminnallisuus niin, että jokainen funktio vastaa yhdestä tehtävästä.

Tämä ongelma liittyy myös toiseen ongelmaan: vaikka `query` ja `file_path` ovat ohjelman konfiguraatiomuuttujia, muuttujat kuten `contents` käytetään ohjelman logiikan suorittamiseen. Mitä pidempi `main` on, sitä enemmän muuttujia meidän täytyy tuoda näkyvyysalueelle; mitä enemmän muuttujia on näkyvyysalueella, sitä vaikeampaa on pitää kirjaa kunkin tarkoituksesta. On parasta ryhmitellä konfiguraatiomuuttujat yhteen rakenteeseen, jotta niiden tarkoitus on selvä.

Kolmas ongelma on se, että olemme käyttäneet `expect`-kutsua tulostaaksemme virheilmoituksen, kun tiedoston lukeminen epäonnistuu, mutta virheilmoitus tulostaa vain `Should have been able to read the file`. Tiedoston lukeminen voi epäonnistua monella tavalla: esimerkiksi tiedosto voi puuttua tai meillä ei ehkä ole oikeutta avata sitä. Tällä hetkellä tulostaisimme saman virheilmoituksen kaikissa tilanteissa, mikä ei antaisi käyttäjälle mitään hyödyllistä tietoa!

Neljäs ongelma on se, että käytämme `expect`-kutsua virheen käsittelyyn, ja jos käyttäjä ajaa ohjelman määrittämättä tarpeeksi argumentteja, hän saa Rustilta `index out of bounds` -virheen, joka ei selkeästi selitä ongelmaa. Olisi parasta, jos kaikki virheenkäsittelykoodi olisi yhdessä paikassa, jotta tulevat ylläpitäjät voisivat tarvittaessa muuttaa virheenkäsittelylogiikkaa yhdestä paikasta. Kun kaikki virheenkäsittelykoodi on yhdessä paikassa, varmistamme myös, että tulostamme viestejä, jotka ovat merkityksellisiä loppukäyttäjillemme.

Korjataan nämä neljä ongelmaa refaktoroimalla projektimme.

### Vastuujen erottelu binääriprojekteissa

Organisatorinen ongelma useiden tehtävien vastuiden antamisesta `main`-funktiolle on yleinen monissa binääriprojekteissa. Tämän vuoksi Rust-yhteisö on kehittänyt ohjeita binääriohjelman erillisten huolenaiheiden jakamiseen, kun `main` alkaa kasvaa liian suureksi. Tämä prosessi sisältää seuraavat vaiheet:

- Jaa ohjelmasi _main.rs_- ja _lib.rs_-tiedostoihin ja siirrä ohjelman logiikka _lib.rs_-tiedostoon.
- Niin kauan kuin komentoriviargumenttien jäsentämislogiikka on pieni, se voi pysyä _main.rs_-tiedostossa.
- Kun komentoriviargumenttien jäsentämislogiikka alkaa monimutkaistua, erota se _main.rs_-tiedostosta ja siirrä se _lib.rs_-tiedostoon.

`main`-funktiossa jäljelle jäävät vastuut tämän prosessin jälkeen pitäisi rajoittua seuraaviin:

- Komentoriviargumenttien jäsentämislogiikan kutsuminen argumenttiarvoilla
- Muun konfiguraation asettaminen
- `run`-funktion kutsuminen _lib.rs_-tiedostossa
- Virheen käsittely, jos `run` palauttaa virheen

Tämä malli koskee huolenaiheiden erottamista: _main.rs_ hoitaa ohjelman ajamisen ja _lib.rs_ hoitaa kaiken käsiteltävän tehtävän logiikan. Koska et voi testata `main`-funktiota suoraan, tämä rakenne antaa sinun testata kaiken ohjelman logiikan siirtämällä sen funktioihin _lib.rs_-tiedostossa. _main.rs_-tiedostoon jäävä koodi on tarpeeksi pieni sen oikeellisuuden varmistamiseksi lukemalla. Muokataan ohjelmaamme noudattamalla tätä prosessia.

#### Argumenttien jäsentäjän erottaminen

Erotamme argumenttien jäsentämiseen liittyvän toiminnallisuuden funktioon, jota `main` kutsuu valmistautuakseen siirtämään komentoriviargumenttien jäsentämislogiikan _src/lib.rs_-tiedostoon. Listausta 12-5 näyttää uuden `main`-funktion alun, joka kutsuu uutta `parse_config`-funktiota, jonka määrittelemme toistaiseksi _src/main.rs_-tiedostossa.

<Listing number="12-5" file-name="src/main.rs" caption="`parse_config`-funktion erottaminen `main`-funktiosta">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-05/src/main.rs:here}}
```

</Listing>

Keräämme edelleen komentoriviargumentit vektoriin, mutta sen sijaan, että määrittäisimme indeksin 1 argumenttiarvon muuttujalle `query` ja indeksin 2 argumenttiarvon muuttujalle `file_path` `main`-funktiossa, välitämme koko vektorin `parse_config`-funktiolle. `parse_config`-funktio sisältää sitten logiikan, joka määrittää, mikä argumentti menee mihinkin muuttujaan, ja palauttaa arvot takaisin `main`-funktiolle. Luomme edelleen `query`- ja `file_path`-muuttujat `main`-funktiossa, mutta `main` ei enää vastaa siitä, miten komentoriviargumentit ja muuttujat vastaavat toisiaan.

Tämä refaktorointi saattaa tuntua liialliselta pienelle ohjelmallemme, mutta refaktoroimme pienin, inkrementaalisin askelin. Tämän muutoksen jälkeen aja ohjelma uudelleen varmistaaksesi, että argumenttien jäsentäminen toimii edelleen. On hyvä tarkistaa edistymisesi usein, jotta ongelmien syy on helpompi tunnistaa, kun ne ilmenevät.

#### Konfiguraatioarvojen ryhmittely

Voimme tehdä vielä yhden pienen parannuksen `parse_config`-funktioon. Tällä hetkellä palautamme monikon, mutta hajotamme sen heti uudelleen erillisiin osiin. Tämä on merkki siitä, että meillä ei ehkä ole vielä oikeaa abstraktiota.

Toinen merkki siitä, että parannettavaa on, on `parse_config`-nimen `config`-osa, joka viittaa siihen, että palauttamamme kaksi arvoa liittyvät toisiinsa ja ovat molemmat osa yhtä konfiguraatioarvoa. Emme tällä hetkellä välitä tätä merkitystä datan rakenteessa muuten kuin ryhmittelemällä kaksi arvoa monikkoon; sijoitamme sen sijaan kaksi arvoa yhteen struct-rakenteeseen ja annamme jokaiselle struct-kentälle merkityksellisen nimen. Näin tulevien tämän koodin ylläpitäjien on helpompi ymmärtää, miten eri arvot liittyvät toisiinsa ja mikä niiden tarkoitus on.

Listausta 12-6 näyttää parannukset `parse_config`-funktioon.

<Listing number="12-6" file-name="src/main.rs" caption="`parse_config`-funktion refaktorointi palauttamaan `Config`-structin instanssi">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-06/src/main.rs:here}}
```

</Listing>

Olemme lisänneet `Config`-nimisen struct-rakenteen, jolla on kentät `query` ja `file_path`. `parse_config`-funktion signatuuri ilmaisee nyt, että se palauttaa `Config`-arvon. `parse_config`-funktion rungossa, jossa aiemmin palautimme merkkijonoviipaleita, jotka viittasivat `String`-arvoihin `args`-vektorissa, määrittelemme nyt `Config`-rakenteen sisältämään omistettuja `String`-arvoja. `args`-muuttuja `main`-funktiossa omistaa argumenttiarvot ja antaa `parse_config`-funktion vain lainata niitä, mikä tarkoittaa, että rikkoisimme Rustin lainaussääntöjä, jos `Config` yrittäisi ottaa omistajuuden `args`-vektorin arvoista.

On useita tapoja hallita `String`-dataa; helpoin, vaikkakin hieman tehottomampi tapa on kutsua `clone`-metodia arvoilla. Tämä tekee täydellisen kopion datasta `Config`-instanssin omistettavaksi, mikä vie enemmän aikaa ja muistia kuin viitteen tallentaminen merkkijonodataan. Datan kloonaaminen tekee koodistamme kuitenkin hyvin suoraviivaisen, koska meidän ei tarvitse hallita viitteiden elinaikoja; tässä tilanteessa hieman suorituskyvyn uhraaminen yksinkertaisuuden vuoksi on kannattava kompromissi.

> ### `clone`-käytön kompromissit
>
> Monilla rustaceaneilla on taipumus välttää `clone`-käyttöä omistajuusongelmien korjaamiseen sen ajonaikaisen kustannuksen vuoksi. [Luvussa 13][ch13]<!-- ignore --> opit tehokkaampia tapoja tämänkaltaisissa tilanteissa. Mutta toistaiseksi on ihan ok kopioida muutama merkkijono jatkaaksesi edistymistä, koska teet nämä kopiot vain kerran ja tiedostopolku- ja hakumerkkijonosi ovat hyvin pieniä. On parempi olla toimiva ohjelma, joka on hieman tehoton, kuin yrittää hyperoptimoida koodia ensimmäisellä yrityksellä. Kun saat enemmän kokemusta Rustista, on helpompaa aloittaa tehokkaimmalla ratkaisulla, mutta toistaiseksi on täysin hyväksyttävää kutsua `clone`-metodia.

Olemme päivittäneet `main`-funktion niin, että se sijoittaa `parse_config`-funktion palauttaman `Config`-instanssin muuttujaan nimeltä `config`, ja olemme päivittäneet koodin, joka aiemmin käytti erillisiä `query`- ja `file_path`-muuttujia, käyttämään nyt `Config`-structin kenttiä.

Nyt koodimme välittää selkeämmin, että `query` ja `file_path` liittyvät toisiinsa ja että niiden tarkoitus on määrittää, miten ohjelma toimii. Kaikki koodi, joka käyttää näitä arvoja, tietää etsiä ne `config`-instanssista kentistä, jotka on nimetty niiden tarkoituksen mukaan.

#### `Config`-rakenteen konstruktorin luominen

Tähän asti olemme erottaneet komentoriviargumenttien jäsentämiseen liittyvän logiikan `main`-funktiosta ja sijoittaneet sen `parse_config`-funktioon. Tämä auttoi meitä näkemään, että `query`- ja `file_path`-arvot liittyivät toisiinsa, ja tämän suhteen pitäisi näkyä koodissamme. Lisäsimme sitten `Config`-struct-rakenteen nimeämään `query`- ja `file_path`-arvojen yhteisen tarkoituksen ja voidaksemme palauttaa arvojen nimet struct-kenttien niminä `parse_config`-funktiosta.

Nyt kun `parse_config`-funktion tarkoitus on luoda `Config`-instanssi, voimme muuttaa `parse_config`-funktion tavallisesta funktiosta `new`-nimiseksi funktioksi, joka liittyy `Config`-struct-rakenteeseen. Tämä muutos tekee koodista idiomaattisemman. Voimme luoda tyyppien instansseja standardikirjastossa, kuten `String`, kutsumalla `String::new`-metodia. Vastaavasti muuttamalla `parse_config`-funktion `new`-funktioksi, joka liittyy `Config`-rakenteeseen, voimme luoda `Config`-instansseja kutsumalla `Config::new`-metodia. Listausta 12-7 näyttää tarvittavat muutokset.

<Listing number="12-7" file-name="src/main.rs" caption="`parse_config`-funktion muuttaminen `Config::new`-metodiksi">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-07/src/main.rs:here}}
```

</Listing>

Olemme päivittäneet `main`-funktion kohdassa, jossa kutsuimme `parse_config`-funktiota, kutsumaan sen sijaan `Config::new`-metodia. Olemme muuttaneet `parse_config`-funktion nimen `new`-nimeksi ja siirtäneet sen `impl`-lohkoon, joka liittää `new`-funktion `Config`-rakenteeseen. Kokeile kääntää tämä koodi uudelleen varmistaaksesi, että se toimii.

### Virheenkäsittelyn korjaaminen

Nyt työskentelemme virheenkäsittelyn korjaamiseksi. Muista, että `args`-vektorin arvojen käyttäminen indeksissä 1 tai 2 aiheuttaa ohjelman paniikin, jos vektorissa on alle kolme kohdetta. Kokeile ajaa ohjelma ilman argumentteja; se näyttää suunnilleen tältä:

```console
{{#include ../listings/ch12-an-io-project/listing-12-07/output.txt}}
```

Rivi `index out of bounds: the len is 1 but the index is 1` on ohjelmoijille tarkoitettu virheilmoitus. Se ei auta loppukäyttäjiämme ymmärtämään, mitä heidän pitäisi tehdä sen sijaan. Korjataan se nyt.

#### Virheilmoituksen parantaminen

Listauksessa 12-8 lisäämme `new`-funktioon tarkistuksen, joka varmistaa, että viipale on tarpeeksi pitkä ennen indeksien 1 ja 2 käyttöä. Jos viipale ei ole tarpeeksi pitkä, ohjelma panikoi ja näyttää paremman virheilmoituksen.

<Listing number="12-8" file-name="src/main.rs" caption="Tarkistuksen lisääminen argumenttien määrälle">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-08/src/main.rs:here}}
```

</Listing>

Tämä koodi on samankaltainen kuin [listauksessa 9-13 kirjoittamamme `Guess::new`-funktio][ch9-custom-types]<!-- ignore -->, jossa kutsuimme `panic!`-makroa, kun `value`-argumentti oli kelvollisten arvojen alueen ulkopuolella. Sen sijaan, että tarkistaisimme arvoalueen täällä, tarkistamme, että `args`-vektorin pituus on vähintään `3`, ja funktion loppuosa voi toimia olettaen, että tämä ehto on täyttynyt. Jos `args`-vektorissa on alle kolme kohdetta, tämä ehto on tosi ja kutsumme `panic!`-makroa lopettaaksemme ohjelman välittömästi.

Näillä muutamilla lisärivillä `new`-funktiossa ajetaan ohjelma uudelleen ilman argumentteja ja katsotaan, miltä virhe näyttää nyt:

```console
{{#include ../listings/ch12-an-io-project/listing-12-08/output.txt}}
```

Tämä tuloste on parempi: meillä on nyt järkevä virheilmoitus. Meillä on kuitenkin myös ylimääräistä tietoa, jota emme halua antaa käyttäjillemme. Ehkä listauksessa 9-13 käyttämämme tekniikka ei ole paras tähän: `panic!`-kutsu sopii paremmin ohjelmointiongelmaan kuin käyttöongelmaan, [kuten luvussa 9 keskusteltiin][ch9-error-guidelines]<!-- ignore -->. Sen sijaan käytämme toista luvussa 9 oppimaasi tekniikkaa — [palautamme `Result`-arvon][ch9-result]<!-- ignore -->, joka ilmaisee joko onnistumisen tai virheen.

<!-- Old headings. Do not remove or links may break. -->

<a id="returning-a-result-from-new-instead-of-calling-panic"></a>

#### `Result`-arvon palauttaminen `panic!`-kutsun sijaan

Voimme sen sijaan palauttaa `Result`-arvon, joka sisältää `Config`-instanssin onnistumistapauksessa ja kuvaa ongelman virhetapauksessa. Muutamme myös funktion nimen `new`-nimestä `build`-nimeksi, koska monet ohjelmoijat odottavat `new`-funktioiden eivät koskaan epäonnistuvan. Kun `Config::build` kommunikoi `main`-funktion kanssa, voimme käyttää `Result`-tyyppiä ilmaisemaan, että ongelma ilmeni. Sitten voimme muuttaa `main`-funktion muuntamaan `Err`-variantin käytännöllisemmäksi virheeksi käyttäjillemme ilman `thread 'main'`- ja `RUST_BACKTRACE`-tekstiä, jonka `panic!`-kutsu aiheuttaa.

Listausta 12-9 näyttää muutokset, jotka meidän täytyy tehdä funktion, jota kutsumme nyt `Config::build`-metodiksi, paluuarvoon ja funktion runkoon, jotta se palauttaa `Result`-arvon. Huomaa, että tämä ei käänny ennen kuin päivitämme myös `main`-funktion, minkä teemme seuraavassa listauksessa.

<Listing number="12-9" file-name="src/main.rs" caption="`Result`-arvon palauttaminen `Config::build`-metodista">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-09/src/main.rs:here}}
```

</Listing>

`build`-funktiomme palauttaa `Result`-arvon, jossa on `Config`-instanssi onnistumistapauksessa ja merkkijonoliteraali virhetapauksessa. Virhearvomme ovat aina `'static`-elinaikaisia merkkijonoliteraaleja.

Olemme tehneet kaksi muutosta funktion rungossa: sen sijaan, että kutsuisimme `panic!`-makroa, kun käyttäjä ei anna tarpeeksi argumentteja, palautamme nyt `Err`-arvon, ja olemme käärineet `Config`-paluuarvon `Ok`-arvoon. Nämä muutokset saavat funktion vastaamaan uutta tyyppisignatuuriaan.

`Err`-arvon palauttaminen `Config::build`-metodista antaa `main`-funktion käsitellä `build`-funktion palauttaman `Result`-arvon ja lopettaa prosessin siistimmin virhetapauksessa.

<!-- Old headings. Do not remove or links may break. -->

<a id="calling-confignew-and-handling-errors"></a>

#### `Config::build`-metodin kutsuminen ja virheiden käsittely

Käsitelläksemme virhetapauksen ja tulostaaksemme käyttäjäystävällisen viestin, meidän täytyy päivittää `main`-funktio käsittelemään `Config::build`-metodin palauttama `Result`-arvo, kuten listauksessa 12-10. Otamme myös vastuun komentorivityökalun lopettamisesta nollasta poikkeavalla virhekoodilla pois `panic!`-kutsulta ja toteutamme sen itse. Nollasta poikkeava poistumistila on käytäntö, jolla ilmoitetaan prosessille, joka kutsui ohjelmaamme, että ohjelma lopetti virhetilassa.

<Listing number="12-10" file-name="src/main.rs" caption="Poistuminen virhekoodilla, jos `Config`-rakenteen luominen epäonnistuu">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-10/src/main.rs:here}}
```

</Listing>

Tässä listauksessa olemme käyttäneet metodia, jota emme ole käsitelleet yksityiskohtaisesti: `unwrap_or_else`, joka on määritelty `Result<T, E>`-tyypille standardikirjastossa. `unwrap_or_else`-käyttö antaa meille mahdollisuuden määritellä mukautetun, ei-`panic!`-pohjaisen virheenkäsittelyn. Jos `Result` on `Ok`-arvo, tämän metodin käyttäytyminen on samankaltaista kuin `unwrap`: se palauttaa `Ok`-arvon sisältämän sisäisen arvon. Jos arvo on kuitenkin `Err`-arvo, tämä metodi kutsuu _sulkeen_ koodia, joka on anonyymi funktio, jonka määrittelemme ja välitämme argumenttina `unwrap_or_else`-metodille. Käsittelemme sulkeita tarkemmin [luvussa 13][ch13]<!-- ignore -->. Toistaiseksi sinun tarvitsee vain tietää, että `unwrap_or_else` välittää `Err`-arvon sisäisen arvon, joka tässä tapauksessa on listauksessa 12-9 lisäämämme staattinen merkkijono `"not enough arguments"`, sulkeellemme argumentissa `err`, joka esiintyy pystyviivojen välissä. Sulkeen koodi voi sitten käyttää `err`-arvoa suorittaessaan.

Olemme lisänneet uuden `use`-rivin tuomaan `process`-moduulin standardikirjastosta näkyvyysalueelle. Sulkeessa ajettava koodi virhetapauksessa on vain kaksi riviä: tulostamme `err`-arvon ja kutsumme sitten `process::exit`-funktiota. `process::exit`-funktio lopettaa ohjelman välittömästi ja palauttaa argumenttina annetun poistumistilakoodin. Tämä on samankaltaista kuin listauksessa 12-8 käyttämämme `panic!`-pohjainen käsittely, mutta emme enää saa kaikkea ylimääräistä tulostetta. Kokeillaan:

```console
{{#include ../listings/ch12-an-io-project/listing-12-10/output.txt}}
```

Hienoa! Tämä tuloste on paljon ystävällisempi käyttäjillemme.

### Logiikan erottaminen `main`-funktiosta

Nyt kun olemme saaneet konfiguraation jäsentämisen refaktoroinnin valmiiksi, käännymme ohjelman logiikan pariin. Kuten totesimme [”Vastuujen erottelu binääriprojekteissa”](#separation-of-concerns-for-binary-projects)<!-- ignore --> -osiossa, erotamme `run`-nimisen funktion, joka sisältää kaiken logiikan, joka on tällä hetkellä `main`-funktiossa mutta ei liity konfiguraation asettamiseen tai virheiden käsittelyyn. Kun olemme valmiit, `main` on ytimekäs ja helppo tarkistaa lukemalla, ja voimme kirjoittaa testejä kaikelle muulle logiikalle.

Listausta 12-11 näyttää erotetun `run`-funktion. Toistaiseksi teemme vain pienen, inkrementaalisen parannuksen erottamalla funktion. Määrittelemme funktion edelleen _src/main.rs_-tiedostossa.

<Listing number="12-11" file-name="src/main.rs" caption="`run`-funktion erottaminen, joka sisältää loput ohjelman logiikasta">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-11/src/main.rs:here}}
```

</Listing>

`run`-funktio sisältää nyt kaiken jäljellä olevan logiikan `main`-funktiosta alkaen tiedoston lukemisesta. `run`-funktio ottaa `Config`-instanssin argumenttina.

#### Virheiden palauttaminen `run`-funktiosta

Kun jäljellä oleva ohjelman logiikka on erotettu `run`-funktioon, voimme parantaa virheenkäsittelyä, kuten teimme `Config::build`-metodilla listauksessa 12-9. Sen sijaan, että antaisimme ohjelman panikoida kutsumalla `expect`-metodia, `run`-funktio palauttaa `Result<T, E>`-arvon, kun jokin menee pieleen. Tämä antaa meille mahdollisuuden koota virheenkäsittelylogiikkaa edelleen `main`-funktioon käyttäjäystävällisellä tavalla. Listausta 12-12 näyttää muutokset, jotka meidän täytyy tehdä `run`-funktion signatuuriin ja runkoon.

<Listing number="12-12" file-name="src/main.rs" caption="`run`-funktion muuttaminen palauttamaan `Result`-arvo">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-12/src/main.rs:here}}
```

</Listing>

Olemme tehneet kolme merkittävää muutosta. Ensinnäkin olemme muuttaneet `run`-funktion paluutyypin `Result<(), Box<dyn Error>>`-tyypiksi. Tämä funktio palautti aiemmin yksikkötyypin `()`, ja pidämme sen `Ok`-tapauksen palautusarvona.

Virhetyypiksi käytimme _trait-objektia_ `Box<dyn Error>` (ja olemme tuoneet `std::error::Error`-traitin näkyvyysalueelle `use`-lauseella tiedoston alussa). Käsittelemme trait-objekteja [luvussa 18][ch18]<!-- ignore -->. Toistaiseksi riittää tietää, että `Box<dyn Error>` tarkoittaa, että funktio palauttaa tyypin, joka toteuttaa `Error`-traitin, mutta meidän ei tarvitse määrittää, mikä tietty tyyppi palautusarvo on. Tämä antaa meille joustavuutta palauttaa eri tyyppisiä virhearvoja eri virhetapauksissa. `dyn`-avainsana on lyhenne sanasta _dynamic_.

Toiseksi olemme poistaneet `expect`-kutsun ja käyttäneet sen sijaan `?`-operaattoria, kuten [luvussa 9][ch9-question-mark]<!-- ignore --> käsiteltiin. Sen sijaan, että `panic!` virheen sattuessa, `?` palauttaa virhearvon nykyisestä funktiosta kutsujan käsiteltäväksi.

Kolmanneksi `run`-funktio palauttaa nyt `Ok`-arvon onnistumistapauksessa. Olemme määritelleet `run`-funktion onnistumistyypiksi `()` signatuurissa, mikä tarkoittaa, että meidän täytyy kääriä yksikkötyyppiarvo `Ok`-arvoon. Tämä `Ok(())`-syntaksi saattaa aluksi näyttää hieman oudolta, mutta `()`-tyypin käyttö tällä tavalla on idiomaattinen tapa ilmaista, että kutsumme `run`-funktiota vain sen sivuvaikutuksia varten; se ei palauta arvoa, jota tarvitsemme.

Kun ajat tämän koodin, se kääntyy mutta näyttää varoituksen:

```console
{{#include ../listings/ch12-an-io-project/listing-12-12/output.txt}}
```

Rust kertoo meille, että koodimme jätti huomiotta `Result`-arvon ja `Result`-arvo saattaa ilmaista, että virhe tapahtui. Mutta emme tarkista, tapahtuiko virhe, ja kääntäjä muistuttaa meitä, että meidän piti todennäköisesti olla virheenkäsittelykoodia täällä! Korjataan tämä ongelma nyt.

#### `run`-funktion palauttamien virheiden käsittely `main`-funktiossa

Tarkistamme virheet ja käsittelemme ne tekniikalla, joka on samankaltainen kuin `Config::build`-metodilla listauksessa 12-10, mutta pienellä erolla:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/no-listing-01-handling-errors-in-main/src/main.rs:here}}
```

Käytämme `if let`-lausetta `unwrap_or_else`-metodin sijaan tarkistaaksemme, palauttaako `run` `Err`-arvon, ja kutsumme `process::exit(1)`-funktiota, jos se palauttaa. `run`-funktio ei palauta arvoa, jota haluaisimme `unwrap`-metodilla purkaa samalla tavalla kuin `Config::build` palauttaa `Config`-instanssin. Koska `run` palauttaa `()` onnistumistapauksessa, välitämme vain virheen havaitsemisesta, joten emme tarvitse `unwrap_or_else`-metodia palauttamaan purettua arvoa, joka olisi vain `()`.

`if let`-lausekkeen ja `unwrap_or_else`-funktioiden rungot ovat molemmissa tapauksissa samat: tulostamme virheen ja lopetamme.

### Koodin jakaminen kirjastokrateiksi

`minigrep`-projektimme näyttää hyvältä tähän asti! Nyt jaamme _src/main.rs_-tiedoston ja siirrämme osan koodista _src/lib.rs_-tiedostoon. Näin voimme testata koodia ja meillä on _src/main.rs_-tiedosto, jolla on vähemmän vastuita.

Siirretään kaikki koodi, joka ei ole `main`-funktiossa, _src/main.rs_-tiedostosta _src/lib.rs_-tiedostoon:

- `run`-funktion määritelmä
- Asiaankuuluvat `use`-lauseet
- `Config`-rakenteen määritelmä
- `Config::build`-funktion määritelmä

_src/lib.rs_-tiedoston sisällössä pitäisi olla listauksessa 12-13 näytetyt signatuurit (olemme jättäneet funktioiden rungot pois lyhyyden vuoksi). Huomaa, että tämä ei käänny ennen kuin muokkaamme _src/main.rs_-tiedostoa listauksessa 12-14.

<Listing number="12-13" file-name="src/lib.rs" caption="`Config`- ja `run`-siirto *src/lib.rs*-tiedostoon">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-13/src/lib.rs:here}}
```

</Listing>

Olemme käyttäneet runsaasti `pub`-avainsanaa: `Config`-rakenteessa, sen kentissä ja `build`-metodissa sekä `run`-funktiossa. Meillä on nyt kirjastokrate, jolla on julkinen API, jota voimme testata!

Nyt meidän täytyy tuoda koodi, jonka siirsimme _src/lib.rs_-tiedostoon, binäärikrateen näkyvyysalueelle _src/main.rs_-tiedostossa, kuten listauksessa 12-14.

<Listing number="12-14" file-name="src/main.rs" caption="`minigrep`-kirjastokrateen käyttö *src/main.rs*-tiedostossa">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-14/src/main.rs:here}}
```

</Listing>

Lisäämme `use minigrep::Config`-rivin tuomaan `Config`-tyypin kirjastokrateesta binäärikrateen näkyvyysalueelle, ja etuliitämme `run`-funktion crate-nimellämme. Nyt kaiken toiminnallisuuden pitäisi olla yhdistetty ja toimia. Aja ohjelma `cargo run` -komennolla ja varmista, että kaikki toimii oikein.

Huh! Sitä oli paljon työtä, mutta olemme asettaneet itsellemme pohjan tulevaisuuden menestykseen. Nyt virheiden käsittely on paljon helpompaa, ja olemme tehneet koodista modulaarisempaa. Lähes kaikki työmme tehdään tästä lähtien _src/lib.rs_-tiedostossa.

Hyödynnetään tätä uutta modulaarisuutta tekemällä jotain, mikä olisi ollut vaikeaa vanhalla koodilla mutta on helppoa uudella koodilla: kirjoitamme testejä!

[ch13]: ch13-00-functional-features.html
[ch9-custom-types]: ch09-03-to-panic-or-not-to-panic.html#creating-custom-types-for-validation
[ch9-error-guidelines]: ch09-03-to-panic-or-not-to-panic.html#guidelines-for-error-handling
[ch9-result]: ch09-02-recoverable-errors-with-result.html
[ch18]: ch18-00-oop.html
[ch9-question-mark]: ch09-02-recoverable-errors-with-result.html#a-shortcut-for-propagating-errors-the--operator
