## Yksisäikeisen verkkopalvelimen rakentaminen

Aloitamme saamalla yksisäikeisen verkkopalvelimen toimimaan. Ennen kuin aloitamme, katsotaan nopea yleiskatsaus verkkopalvelimien rakentamiseen liittyvistä protokollista. Näiden protokollien yksityiskohdat ylittävät tämän kirjan laajuuden, mutta lyhyt yleiskatsaus antaa tarvitsemasi tiedon.

Verkkopalvelimiin liittyvät kaksi pääprotokollaa ovat _Hypertext Transfer Protocol_ (_HTTP_) ja _Transmission Control Protocol_ (_TCP_). Molemmat protokollat ovat _pyyntö-vastaus_-protokollia, mikä tarkoittaa, että _asiakas_ aloittaa pyynnöt ja _palvelin_ kuuntelee pyyntöjä ja antaa vastauksen asiakkaalle. Näiden pyyntöjen ja vastausten sisältö määritellään protokollien toimesta.

TCP on alemmantasoinen protokolla, joka kuvaa yksityiskohdat siitä, miten tieto siirtyy palvelimelta toiselle, mutta ei määrittele, mitä tämä tieto on. HTTP rakentuu TCP:n päälle määrittelemällä pyyntöjen ja vastausten sisällön. Teknisesti HTTP on mahdollista käyttää muiden protokollien kanssa, mutta valtavassa enemmistössä tapauksista HTTP lähettää datansa TCP:n yli. Työskentelemme TCP:n ja HTTP-pyyntöjen ja -vastausten raakatavujen kanssa.

### TCP-yhteyden kuunteleminen

Verkkopalvelimemme täytyy kuunnella TCP-yhteyttä, joten se on ensimmäinen osa, jota työstämme. Standardikirjasto tarjoaa `std::net`-moduulin, joka antaa meille mahdollisuuden tehdä tämän. Tehdään uusi projekti tavalliseen tapaan:

```console
$ cargo new hello
     Created binary (application) `hello` project
$ cd hello
```

Syötä nyt listauksen 21-1 koodi _src/main.rs_-tiedostoon aloittaaksesi. Tämä koodi kuuntelee paikallista osoitetta `127.0.0.1:7878` saapuvia TCP-streameja varten. Kun se saa saapuvan streamin, se tulostaa `Connection established!`.

<Listing number="21-1" file-name="src/main.rs" caption="Saapuvien streamien kuunteleminen ja viestin tulostaminen streamin vastaanotosta">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-01/src/main.rs}}
```

</Listing>

`TcpListener`-rakenteen avulla voimme kuunnella TCP-yhteyksiä osoitteessa `127.0.0.1:7878`. Osoitteessa kaksoispisteen edeltävä osa on IP-osoite, joka edustaa tietokonettasi (tämä on sama jokaisella tietokoneella eikä edusta kirjoittajien tietokonetta erityisesti), ja `7878` on portti. Olemme valinneet tämän portin kahdesta syystä: HTTP:tä ei yleensä hyväksytä tällä portilla, joten palvelimemme ei todennäköisesti ole ristiriidassa muiden koneellasi mahdollisesti ajavien verkkopalvelimien kanssa, ja 7878 on _rust_ kirjoitettuna puhelinnäppäimistöllä.

Tässä skenaariossa `bind`-funktio toimii kuten `new`-funktio siinä mielessä, että se palauttaa uuden `TcpListener`-instanssin. Funktiota kutsutaan `bind`-nimiseksi, koska verkkoyhteyksissä porttiin yhdistämistä kuuntelemista varten kutsutaan ”porttiin sitomiseksi” (_binding to a port_).

`bind`-funktio palauttaa `Result<T, E>`-arvon, mikä osoittaa, että sitominen voi epäonnistua. Esimerkiksi porttiin 80 yhdistäminen vaatii järjestelmänvalvojan oikeudet (ei-järjestelmänvalvojat voivat kuunnella vain portteja, jotka ovat suurempia kuin 1023), joten jos yrittäisimme yhdistää porttiin 80 ilman järjestelmänvalvojan oikeuksia, sitominen ei toimisi. Sitominen ei myöskään toimisi, jos esimerkiksi ajaisimme kaksi ohjelman instanssia ja siten kaksi ohjelmaa kuuntelisi samaa porttia. Koska kirjoitamme peruspalvelimen vain oppimistarkoituksiin, emme huolehdi tällaisten virheiden käsittelystä; sen sijaan käytämme `unwrap`-metodia lopettaaksemme ohjelman, jos virheitä tapahtuu.

`TcpListener`-rakenteen `incoming`-metodi palauttaa iteraattorin, joka antaa meille streamien sarjan (tarkemmin sanottuna `TcpStream`-tyyppisten streamien). Yksittäinen _stream_ edustaa avointa yhteyttä asiakkaan ja palvelimen välillä. _Yhteys_ on nimi koko pyyntö-vastaus-prosessille, jossa asiakas yhdistää palvelimeen, palvelin tuottaa vastauksen ja palvelin sulkee yhteyden. Näin ollen luemme `TcpStream`-rakenteesta nähdäksemme, mitä asiakas lähetti, ja kirjoitamme sitten vastauksemme streamiin lähettääksemme dataa takaisin asiakkaalle. Kaiken kaikkiaan tämä `for`-silmukka käsittelee jokaisen yhteyden vuorollaan ja tuottaa meille streamien sarjan käsiteltäväksi.

Tällä hetkellä streamin käsittelymme koostuu `unwrap`-metodin kutsumisesta lopettaaksemme ohjelman, jos streamissä on virheitä; jos virheitä ei ole, ohjelma tulostaa viestin. Lisäämme lisää toiminnallisuutta onnistumistapaukselle seuraavassa listauksessa. Syy, miksi saatamme saada virheitä `incoming`-metodista, kun asiakas yhdistää palvelimeen, on se, että emme itse asiassa iteroi yhteyksien yli. Sen sijaan iteromme _yhteysyritysten_ yli. Yhteys ei välttämättä onnistu monesta syystä, joista monet ovat käyttöjärjestelmäkohtaisia. Esimerkiksi monilla käyttöjärjestelmillä on raja samanaikaisesti avoimien yhteyksien määrälle; uudet yhteysyritykset tämän rajan yli tuottavat virheen, kunnes jotkut avoimista yhteyksistä suljetaan.

Kokeillaan ajaa tämä koodi! Kutsu `cargo run` -komentoa terminaalissa ja lataa sitten _127.0.0.1:7878_ verkkoselaimessa. Selaimen pitäisi näyttää virheilmoitus, kuten ”Connection reset”, koska palvelin ei tällä hetkellä lähetä mitään dataa takaisin. Mutta kun katsot terminaaliasi, sinun pitäisi nähdä useita viestejä, jotka tulostettiin, kun selain yhdisti palvelimeen!

```text
     Running `target/debug/hello`
Connection established!
Connection established!
Connection established!
```

Joskus näet useita viestejä tulostettuna yhdestä selainpyynnöstä; syy voi olla se, että selain tekee pyynnön sivulle sekä pyynnön muille resursseille, kuten _favicon.ico_-kuvakkeelle, joka näkyy selaimen välilehdessä.

Voi myös olla, että selain yrittää yhdistää palvelimeen useita kertoja, koska palvelin ei vastaa millään datalla. Kun `stream` menee näkyvyysalueen ulkopuolelle ja pudotetaan silmukan lopussa, yhteys suljetaan osana `drop`-toteutusta. Selaimet käsittelevät joskus suljettuja yhteyksiä yrittämällä uudelleen, koska ongelma saattaa olla tilapäinen. Tärkeä tekijä on, että olemme onnistuneesti saaneet käsitteen TCP-yhteydestä!

Muista pysäyttää ohjelma painamalla <kbd>ctrl</kbd>-<kbd>c</kbd>, kun olet valmis tietyn koodiversion ajamisen kanssa. Käynnistä sitten ohjelma uudelleen kutsumalla `cargo run` -komentoa jokaisen koodimuutoksen jälkeen varmistaaksesi, että ajat uusinta koodia.

### Pyynnön lukeminen

Toteutetaan toiminnallisuus pyynnön lukemiseksi selaimesta! Erottaaksemme ensin yhteyden saamisen ja sitten toimenpiteen tekemisen yhteydellä, aloitamme uuden funktion yhteyksien käsittelyyn. Tässä uudessa `handle_connection`-funktiossa luemme dataa TCP-streamistä ja tulostamme sen nähdäksemme selaimen lähettämän datan. Muuta koodi näyttämään listaukselta 21-2.

<Listing number="21-2" file-name="src/main.rs" caption="Lukeminen `TcpStream`-rakenteesta ja datan tulostaminen">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-02/src/main.rs}}
```

</Listing>

Tuomme `std::io::prelude`- ja `std::io::BufReader`-moduulit näkyvyysalueelle saadaksemme käyttöön traitit ja tyypit, joiden avulla voimme lukea streamistä ja kirjoittaa siihen. `main`-funktion `for`-silmukassa sen sijaan, että tulostaisimme viestin siitä, että saimme yhteyden, kutsumme nyt uutta `handle_connection`-funktiota ja välitämme sille `stream`-parametrin.

`handle_connection`-funktiossa luomme uuden `BufReader`-instanssin, joka käärii viitteen streamiin. `BufReader` lisää puskurointia hallitsemalla `std::io::Read`-traitin metodikutsuja puolestamme.

Luomme muuttujan nimeltä `http_request` kerätäksemme selaimen palvelimellemme lähettämän pyynnön rivit. Ilmaisemme, että haluamme kerätä nämä rivit vektoriin lisäämällä `Vec<_>`-tyyppiannotaation.

`BufReader` toteuttaa `std::io::BufRead`-traitin, joka tarjoaa `lines`-metodin. `lines`-metodi palauttaa iteraattorin tyyppiä `Result<String, std::io::Error>` jakamalla datastreamin aina kun se näkee rivinvaihtotavun. Saadaksemme jokaisen `String`-arvon, käytämme `map`- ja `unwrap`-metodeja jokaiselle `Result`-arvolle. `Result` voi olla virhe, jos data ei ole kelvollista UTF-8:aa tai jos streamin lukemisessa oli ongelma. Taaskin tuotantoohjelman pitäisi käsitellä nämä virheet tyylikkäämmin, mutta valitsemme yksinkertaisuuden vuoksi lopettaa ohjelman virhetapauksessa.

Selain ilmaisee HTTP-pyynnön päättymisen lähettämällä kaksi rivinvaihtomerkkiä peräkkäin, joten saadaksemme yhden pyynnön streamistä otamme rivejä, kunnes saamme rivin, joka on tyhjä merkkijono. Kun olemme keränneet rivit vektoriin, tulostamme ne käyttämällä kaunista debug-muotoilua nähdäksemme, mitä ohjeita verkkoselain lähettää palvelimellemme.

Kokeillaan tätä koodia! Käynnistä ohjelma ja tee pyyntö verkkoselaimessa uudelleen. Huomaa, että saamme edelleen virhesivun selaimessa, mutta ohjelman tulosteen terminaalissa pitäisi nyt näyttää suunnilleen tältä:

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
    Finished dev [unoptimized + debuginfo] target(s) in 0.42s
     Running `target/debug/hello`
Request: [
    "GET / HTTP/1.1",
    "Host: 127.0.0.1:7878",
    "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language: en-US,en;q=0.5",
    "Accept-Encoding: gzip, deflate, br",
    "DNT: 1",
    "Connection: keep-alive",
    "Upgrade-Insecure-Requests: 1",
    "Sec-Fetch-Dest: document",
    "Sec-Fetch-Mode: navigate",
    "Sec-Fetch-Site: none",
    "Sec-Fetch-User: ?1",
    "Cache-Control: max-age=0",
]
```

Selaimestasi riippuen saatat saada hieman erilaisen tulosteen. Nyt kun tulostamme pyyntödataa, voimme nähdä, miksi saamme useita yhteyksiä yhdestä selainpyynnöstä katsomalla polkua `GET`-rivin jälkeen. Jos toistuvat yhteydet pyytävät kaikki _/_, tiedämme, että selain yrittää hakea _/_ toistuvasti, koska se ei saa vastausta ohjelmastamme.

Puretaan tämä pyyntödata ymmärtääksemme, mitä selain pyytää ohjelmaltamme.

### Tarkempi katsaus HTTP-pyyntöön

HTTP on tekstipohjainen protokolla, ja pyyntö on tässä muodossa:

```text
Method Request-URI HTTP-Version CRLF
headers CRLF
message-body
```

Ensimmäinen rivi on _pyyntörivi_, joka sisältää tietoa siitä, mitä asiakas pyytää. Pyyntörivin ensimmäinen osa ilmaisee käytetyn _metodin_, kuten `GET` tai `POST`, joka kuvaa, miten asiakas tekee tämän pyynnön. Asiakkaamme käytti `GET`-pyyntöä, mikä tarkoittaa, että se pyytää tietoa.

Pyyntörivin seuraava osa on _/_, joka ilmaisee _uniform resource identifierin_ (_URI_), jota asiakas pyytää: URI on melkein, mutta ei aivan, sama kuin _uniform resource locator_ (_URL_). Ero URI:n ja URL:n välillä ei ole tärkeä tämän luvun tarkoituksiin, mutta HTTP-spesifikaatio käyttää termiä URI, joten voimme ajatella _URL_:n sijasta _URI_:ta.

Viimeinen osa on asiakkaan käyttämä HTTP-versio, ja sitten pyyntörivi päättyy CRLF-sekvenssiin. (CRLF tulee sanoista _carriage return_ ja _line feed_, jotka ovat peräisin kirjoituskonetyöaikojen termeistä!) CRLF-sekvenssi voidaan kirjoittaa myös muodossa `\r\n`, missä `\r` on carriage return ja `\n` on line feed. _CRLF-sekvenssi_ erottaa pyyntörivin pyynnön lopusta datasta. Huomaa, että kun CRLF tulostetaan, näemme uuden rivin alkavan `\r\n`:n sijaan.

Katsomalla pyyntörividataa, jonka saimme ohjelman ajosta tähän asti, näemme, että `GET` on metodi, _/_ on pyynnön URI ja `HTTP/1.1` on versio.

Pyyntörivin jälkeen jäljellä olevat rivit alkaen `Host:`-rivistä eteenpäin ovat otsakkeita. `GET`-pyynnöillä ei ole runkoa.

Kokeile tehdä pyyntö eri selaimesta tai pyytää eri osoitetta, kuten _127.0.0.1:7878/test_, nähdäksesi, miten pyyntödata muuttuu.

Nyt kun tiedämme, mitä selain pyytää, lähetetään takaisin dataa!

### Vastauksen kirjoittaminen

Toteutamme datan lähettämisen asiakkaan pyyntöön vastaamiseksi. Vastaukset ovat seuraavassa muodossa:

```text
HTTP-Version Status-Code Reason-Phrase CRLF
headers CRLF
message-body
```

Ensimmäinen rivi on _tilarivi_, joka sisältää vastauksessa käytetyn HTTP-version, numeerisen tilakoodin, joka tiivistää pyynnön tuloksen, ja syy-lausekkeen, joka antaa tekstikuvauksen tilakoodista. CRLF-sekvenssin jälkeen tulevat otsakkeet, toinen CRLF-sekvenssi ja vastauksen runko.

Tässä on esimerkkivastaus, joka käyttää HTTP-versiota 1.1, tilakoodia 200, syy-lauseketta OK, ei otsakkeita eikä runkoa:

```text
HTTP/1.1 200 OK\r\n\r\n
```

Tilakoodi 200 on standardi onnistumisvastaus. Teksti on pieni onnistunut HTTP-vastaus. Kirjoitetaan tämä streamiin vastaukseksemme onnistuneeseen pyyntöön! `handle_connection`-funktiosta poistetaan `println!`, joka tulosti pyyntödataa, ja korvataan se listauksen 21-3 koodilla.

<Listing number="21-3" file-name="src/main.rs" caption="Pienen onnistuneen HTTP-vastauksen kirjoittaminen streamiin">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-03/src/main.rs:here}}
```

</Listing>

Ensimmäinen uusi rivi määrittelee `response`-muuttujan, joka sisältää onnistumisviestin datan. Sitten kutsumme `as_bytes`-metodia `response`-muuttujalla muuntaaksemme merkkijonodatan tavuiksi. `stream`-rakenteen `write_all`-metodi ottaa `&[u8]`-tyypin ja lähettää nämä tavut suoraan yhteyden kautta. Koska `write_all`-operaatio voi epäonnistua, käytämme `unwrap`-metodia virhetuloksen kohdalla kuten aiemmin. Taaskin todellisessa sovelluksessa lisäisit virheenkäsittelyn tähän.

Näillä muutoksilla ajetaan koodimme ja tehdään pyyntö. Emme enää tulosta mitään dataa terminaaliin, joten emme näe mitään tulostetta muuten kuin Cargolta. Kun lataat _127.0.0.1:7878_ verkkoselaimessa, sinun pitäisi saada tyhjä sivu virheen sijaan. Olet juuri käsin koodannut HTTP-pyynnön vastaanottamisen ja vastauksen lähettämisen!

### Oikean HTML:n palauttaminen

Toteutetaan toiminnallisuus enemmän kuin tyhjän sivun palauttamiseksi. Luo uusi tiedosto _hello.html_ projektihakemistosi juureen, ei _src_-hakemistoon. Voit syöttää mitä tahansa HTML:ää; listausta 21-4 näyttää yhden mahdollisuuden.

<Listing number="21-4" file-name="hello.html" caption="Esimerkki-HTML-tiedosto vastauksessa palautettavaksi">

```html
{{#include ../listings/ch21-web-server/listing-21-05/hello.html}}
```

</Listing>

Tämä on minimaalinen HTML5-dokumentti otsikolla ja tekstillä. Palauttaaksemme tämän palvelimelta pyynnön vastaanotosta, muokkaamme `handle_connection`-funktiota kuten listauksessa 21-5 näytetään lukemaan HTML-tiedosto, lisäämään se vastauksen rungoksi ja lähettämään sen.

<Listing number="21-5" file-name="src/main.rs" caption="*hello.html*-tiedoston sisällön lähettäminen vastauksen rungoksi">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-05/src/main.rs:here}}
```

</Listing>

Olemme lisänneet `fs`-moduulin `use`-lauseeseen tuodaksemme standardikirjaston tiedostojärjestelmämoduulin näkyvyysalueelle. Koodin tiedoston sisällön lukemiseksi merkkijonoon pitäisi näyttää tutulta; käytimme sitä lukiessamme tiedoston sisältöä I/O-projektissamme listauksessa 12-4.

Seuraavaksi käytämme `format!`-makroa lisätäksemme tiedoston sisällön onnistumisvastauksen rungoksi. Varmistaaksemme kelvollisen HTTP-vastauksen lisäämme `Content-Length`-otsakkeen, joka on asetettu vastausrukkimme kooksi, tässä tapauksessa `hello.html`-tiedoston kooksi.

Aja tämä koodi `cargo run` -komennolla ja lataa _127.0.0.1:7878_ selaimessasi; sinun pitäisi nähdä HTML renderöitynä!

Tällä hetkellä sivuutamme `http_request`-muuttujan pyyntödatan ja lähetämme HTML-tiedoston sisällön takaisin ehdottomasti. Tämä tarkoittaa, että jos yrität pyytää _127.0.0.1:7878/something-else_ selaimessasi, saat silti saman HTML-vastauksen. Tällä hetkellä palvelimemme on hyvin rajallinen eikä tee sitä, mitä useimmat verkkopalvelimet tekevät. Haluamme mukauttaa vastauksiamme pyynnön mukaan ja lähettää HTML-tiedoston takaisin vain hyvin muotoillulle pyynnölle osoitteeseen _/_.

### Pyynnön validointi ja valikoiva vastaaminen

Tällä hetkellä verkkopalvelimemme palauttaa tiedoston HTML:n riippumatta siitä, mitä asiakas pyysi. Lisätään toiminnallisuus tarkistaaksemme, pyytääkö selain _/_, ennen kuin palautamme HTML-tiedoston, ja palautamme virheen, jos selain pyytää jotain muuta. Tätä varten meidän täytyy muokata `handle_connection`-funktiota, kuten listauksessa 21-6. Tämä uusi koodi tarkistaa vastaanotetun pyynnön sisällön sitä vastaan, miltä pyyntö osoitteeseen _/_ näyttää, ja lisää `if`- ja `else`-lohkot käsittelemään pyyntöjä eri tavoin.

<Listing number="21-6" file-name="src/main.rs" caption="Pyyntöjen käsittely osoitteeseen */* eri tavalla kuin muiden pyyntöjen">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-06/src/main.rs:here}}
```

</Listing>

Katsomme vain HTTP-pyynnön ensimmäistä riviä, joten sen sijaan, että lukisimme koko pyynnön vektoriin, kutsumme `next`-metodia saadaksemme ensimmäisen kohteen iteraattorista. Ensimmäinen `unwrap` hoitaa `Option`-arvon ja lopettaa ohjelman, jos iteraattorilla ei ole kohteita. Toinen `unwrap` käsittelee `Result`-arvon ja sillä on sama vaikutus kuin listauksessa 21-2 lisätyllä `map`-kutsun `unwrap`-metodilla.

Seuraavaksi tarkistamme `request_line`-muuttujan nähdäksemme, vastaako se GET-pyyntöä polkuun _/_. Jos vastaa, `if`-lohko palauttaa HTML-tiedostomme sisällön.

Jos `request_line` ei vastaa GET-pyyntöä polkuun _/_, olemme saaneet jonkin muun pyynnön. Lisäämme hetken kuluttua koodia `else`-lohkoon vastataksemme kaikkiin muihin pyyntöihin.

Aja tämä koodi nyt ja pyydä _127.0.0.1:7878_; sinun pitäisi saada HTML _hello.html_-tiedostosta. Jos teet minkä tahansa muun pyynnön, kuten _127.0.0.1:7878/something-else_, saat yhteysvirheen, kuten listauksissa 21-1 ja 21-2 ajettaessa.

Lisätään nyt listauksen 21-7 koodi `else`-lohkoon palauttaaksemme vastauksen tilakoodilla 404, joka ilmaisee, että pyynnön sisältöä ei löytynyt. Palautamme myös HTML:ää sivulle, joka renderöidään selaimessa ilmaisten vastauksen loppukäyttäjälle.

<Listing number="21-7" file-name="src/main.rs" caption="Vastaaminen tilakoodilla 404 ja virhesivulla, jos mitään muuta kuin */* pyydettiin">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-07/src/main.rs:here}}
```

</Listing>

Tässä vastauksessamme on tilarivi tilakoodilla 404 ja syy-lausekkeella `NOT FOUND`. Vastauksen runko on HTML _404.html_-tiedostossa. Sinun täytyy luoda _404.html_-tiedosto _hello.html_-tiedoston viereen virhesivua varten; voit vapaasti käyttää mitä tahansa HTML:ää tai käyttää esimerkki-HTML:ää listauksessa 21-8.

<Listing number="21-8" file-name="404.html" caption="Esimerkkisisältö sivulle, joka lähetetään takaisin 404-vastauksen mukana">

```html
{{#include ../listings/ch21-web-server/listing-21-07/404.html}}
```

</Listing>

Näillä muutoksilla käynnistä palvelimesi uudelleen. Pyyntö _127.0.0.1:7878_ pitäisi palauttaa _hello.html_-tiedoston sisällön, ja mikä tahansa muu pyyntö, kuten _127.0.0.1:7878/foo_, pitäisi palauttaa virhe-HTML _404.html_-tiedostosta.

### Pieni refaktorointi

Tällä hetkellä `if`- ja `else`-lohkoissa on paljon toistoa: molemmat lukevat tiedostoja ja kirjoittavat tiedostojen sisällön streamiin. Ainoat erot ovat tilarivissä ja tiedostonimessä. Tehdään koodista ytimekkäämpää erottamalla nämä erot erillisiin `if`- ja `else`-riveihin, jotka määrittävät tilarivin ja tiedostonimen arvot muuttujiin; voimme sitten käyttää näitä muuttujia ehdottomasti koodissa tiedoston lukemiseen ja vastauksen kirjoittamiseen. Listausta 21-9 näyttää tuloksena olevan koodin suurten `if`- ja `else`-lohkojen korvaamisen jälkeen.

<Listing number="21-9" file-name="src/main.rs" caption="`if`- ja `else`-lohkojen refaktorointi sisältämään vain koodin, joka eroaa kahden tapauksen välillä">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-09/src/main.rs:here}}
```

</Listing>

Nyt `if`- ja `else`-lohkot palauttavat vain sopivat arvot tilariville ja tiedostonimelle monikossa; käytämme sitten destrukturointia määrittääksemme nämä kaksi arvoa `status_line`- ja `filename`-muuttujiin käyttämällä kuviota `let`-lausekkeessa, kuten luvussa 19 käsiteltiin.

Aiemmin toistuva koodi on nyt `if`- ja `else`-lohkojen ulkopuolella ja käyttää `status_line`- ja `filename`-muuttujia. Tämä tekee kahden tapauksen erosta helpommin nähtävän, ja se tarkoittaa, että meillä on vain yksi paikka päivittää koodia, jos haluamme muuttaa tiedoston lukemisen ja vastauksen kirjoittamisen toimintaa. Listauksen 21-9 koodin käyttäytyminen on sama kuin listauksen 21-7.

Hienoa! Meillä on nyt yksinkertainen verkkopalvelin noin 40 rivillä Rust-koodia, joka vastaa yhteen pyyntöön sisältösivulla ja kaikkiin muihin pyyntöihin 404-vastauksella.

Tällä hetkellä palvelimemme toimii yhdessä säikeessä, mikä tarkoittaa, että se voi palvella vain yhtä pyyntöä kerrallaan. Tarkastellaan, miten tämä voi olla ongelma simuloimalla hitaita pyyntöjä. Korjaamme sitten sen, jotta palvelimemme voi käsitellä useita pyyntöjä samanaikaisesti.
