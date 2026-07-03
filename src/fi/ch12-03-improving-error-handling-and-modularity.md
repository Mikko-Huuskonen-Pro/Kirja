## Refaktorointi modulaarisuuden ja virheenkäsittelyn parantamiseksi

Parantaaksemme ohjelmaamme korjaamme neljä ongelmaa, jotka liittyvät ohjelman
rakenteeseen ja siihen, miten se käsittelee mahdollisia virheitä. Ensinnäkin
`main`-funktiomme suorittaa nyt kaksi tehtävää: se jäsentää argumentit ja lukee
tiedostoja. Ohjelmamme kasvaessa `main`-funktion käsittelemien erillisten
tehtävien määrä kasvaa. Kun funktio saa vastuita, siitä tulee vaikeampi
ymmärtää, vaikeampi testata ja vaikeampi muuttaa rikkomatta jotakin sen osista.
On parasta erottaa toiminnallisuus niin, että jokainen funktio on vastuussa
yhdestä tehtävästä.

Tämä ongelma liittyy myös toiseen ongelmaan: Vaikka `query` ja `file_path` ovat
ohjelmamme konfiguraatiomuuttujia, muuttujat kuten `contents` käytetään
ohjelman logiikan suorittamiseen. Mitä pidempi `main` tulee, sitä enemmän
muuttujia meidän täytyy tuoda näkyvyysalueelle; mitä enemmän muuttujia on
näkyvyysalueella, sitä vaikeampi on seurata kunkin tarkoitusta. On parasta
ryhmitellä konfiguraatiomuuttujat yhteen structiin selventämään niiden tarkoitusta.

Kolmas ongelma on, että olemme käyttäneet `expect`-metodia tulostaaksemme
virheviestin, kun tiedoston lukeminen epäonnistuu, mutta virheviesti tulostaa
vain `Should have been able to read the file`. Tiedoston lukeminen voi epäonnistua
monella tavalla: Esimerkiksi tiedosto voi puuttua tai meillä ei ehkä ole oikeutta
avata sitä. Tällä hetkellä tulostaisimme saman virheviestin kaikissa tilanteissa,
mikä ei antaisi käyttäjälle mitään tietoa!

Neljäs ongelma on, että käytämme `expect`-metodia virheen käsittelyyn, ja jos
käyttäjä ajaa ohjelmamme määrittämättä tarpeeksi argumentteja, hän saa Rustilta
`index out of bounds` -virheen, joka ei selitä ongelmaa selkeästi. Olisi parasta,
jos kaikki virheenkäsittelykoodi olisi yhdessä paikassa, jotta tulevat
ylläpitäjät voisivat konsultoida vain yhtä paikkaa, jos virheenkäsittelylogiikkaa
tarvitsee muuttaa. Kaiken virheenkäsittelykoodin pitäminen yhdessä paikassa
varmistaa myös, että tulostamme viestejä, jotka ovat merkityksellisiä
loppukäyttäjillemme.

Korjataan nämä neljä ongelmaa refaktoroimalla projektimme.

<!-- Old headings. Do not remove or links may break. -->

<a id="separation-of-concerns-for-binary-projects"></a>

### Huolenaiheiden erottaminen binääriprojekteissa

Useiden tehtävien vastuun jakaminen `main`-funktiolle on yleinen organisointiongelma
monissa binääriprojekteissa. Siksi monet Rust-ohjelmoijat pitävät hyödyllisenä
jakaa binääriohjelman erilliset huolenaiheet, kun `main`-funktio alkaa kasvaa
suureksi. Tämä prosessi sisältää seuraavat vaiheet:

- Jaa ohjelmasi _main.rs_- ja _lib.rs_-tiedostoihin ja siirrä ohjelmasi logiikka
  _lib.rs_-tiedostoon.
- Niin kauan kuin komentorivin jäsentämislogiikka on pieni, se voi pysyä
  `main`-funktiossa.
- Kun komentorivin jäsentämislogiikka alkaa monimutkaistua, erota se `main`-
  funktiosta muihin funktioihin tai tyyppeihin.

Tämän prosessin jälkeen `main`-funktiossa jäljellä olevat vastuut tulisi rajoittaa
seuraaviin:

- Komentorivin jäsentämislogiikan kutsuminen argumenttiarvoilla
- Muun konfiguraation asettaminen
- `run`-funktion kutsuminen _lib.rs_-tiedostossa
- Virheen käsittely, jos `run` palauttaa virheen

Tämä kuvio koskee huolenaiheiden erottamista: _main.rs_ hoitaa ohjelman ajamisen
ja _lib.rs_ hoitaa kaiken tehtävän logiikan. Koska et voi testata `main`-funktiota
suoraan, tämä rakenne antaa sinun testata kaiken ohjelmasi logiikan siirtämällä
sen pois `main`-funktiosta. `main`-funktiossa jäljelle jäävä koodi on tarpeeksi
pieni sen oikeellisuuden varmistamiseksi lukemalla. Työstetään ohjelmaamme
seuraamalla tätä prosessia.

#### Argumenttijäsentimen erottaminen

Erotamme argumenttien jäsentämiseen liittyvän toiminnallisuuden funktioon,
jonka `main` kutsuu. Listaus 12-5 näyttää uuden `main`-funktion alun, joka
kutsuu uutta `parse_config`-funktiota, jonka määrittelemme _src/main.rs_-tiedostossa.

<Listing number="12-5" file-name="src/main.rs" caption="`parse_config`-funktion erottaminen `main`-funktiosta">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-05/src/main.rs:here}}
```

</Listing>

Keräämme edelleen komentoriviargumentit vektoriin, mutta sen sijaan, että
määrittäisimme indeksin 1 argumenttiarvon muuttujalle `query` ja indeksin 2
argumenttiarvon muuttujalle `file_path` `main`-funktiossa, välitämme koko
vektorin `parse_config`-funktiolle. `parse_config`-funktio sisältää logiikan,
joka määrittää, mikä argumentti menee mihinkin muuttujaan, ja palauttaa arvot
takaisin `main`-funktiolle. Luomme edelleen `query`- ja `file_path`-muuttujat
`main`-funktiossa, mutta `main`-funktiolla ei ole enää vastuuta määrittää,
miten komentoriviargumentit ja muuttujat vastaavat toisiaan.

Tämä refaktorointi saattaa vaikuttaa liialliselta pienelle ohjelmallemme, mutta
refaktoroimme pienin, inkrementaalisin askelin. Tämän muutoksen jälkeen aja
ohjelma uudelleen varmistaaksesi, että argumenttien jäsentäminen toimii edelleen.
On hyvä tarkistaa edistyminen usein auttaaksesi tunnistamaan ongelmien syyn,
kun ne ilmenevät.

#### Konfiguraatioarvojen ryhmittely

Voimme tehdä vielä yhden pienen askeleen parantaaksemme `parse_config`-funktiota
edelleen. Tällä hetkellä palautamme monikon, mutta sitten hajotamme sen heti
uudelleen yksittäisiin osiin. Tämä on merkki siitä, että meillä ei ehkä ole
vielä oikeaa abstraktiota.

Toinen indikaattori, joka osoittaa parannettavaa tilaa, on `parse_config`-funktion
`config`-osa, joka viittaa siihen, että kaksi palauttamaamme arvoa liittyvät
toisiinsa ja ovat molemmat osa yhtä konfiguraatioarvoa. Emme tällä hetkellä
välittäne tätä merkitystä datan rakenteessa muuten kuin ryhmittelemällä kaksi
arvoa monikkoon; sijoitamme sen sijaan kaksi arvoa yhteen structiin ja annamme
kullekin structin kentälle merkityksellisen nimen. Näin tuleville tämän koodin
ylläpitäjille on helpompi ymmärtää, miten eri arvot liittyvät toisiinsa ja mikä
niiden tarkoitus on.

Listaus 12-6 näyttää parannukset `parse_config`-funktioon.

<Listing number="12-6" file-name="src/main.rs" caption="`parse_config`-funktion refaktorointi palauttamaan `Config`-structin instanssi">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-06/src/main.rs:here}}
```

</Listing>

Olemme lisänneet `Config`-nimisen structin, jolla on kentät nimeltä `query` ja
`file_path`. `parse_config`-funktion allekirjoitus ilmaisee nyt, että se palauttaa
`Config`-arvon. `parse_config`-funktion rungossa, jossa aiemmin palautimme
merkkijonoviipaleita, jotka viittaavat `String`-arvoihin `args`-vektorissa,
määrittelemme nyt `Config`-structin sisältämään omistettuja `String`-arvoja.
`args`-muuttuja `main`-funktiossa omistaa argumenttiarvot ja antaa vain
`parse_config`-funktion lainata niitä, mikä tarkoittaa, että rikkoisimme Rustin
lainaussääntöjä, jos `Config` yrittäisi ottaa `args`-vektorin arvojen omistajuuden.

On useita tapoja hallita `String`-dataa; helpoin, vaikkakin hieman tehoton tapa
on kutsua `clone`-metodia arvoille. Tämä tekee täyden kopion datasta `Config`-
instanssin omistettavaksi, mikä vie enemmän aikaa ja muistia kuin merkkijonodatan
viittauksen säilyttäminen. Datan kloonaaminen tekee kuitenkin koodistamme hyvin
suoraviivaisen, koska emme tarvitse hallita viittausten eliniöitä; tässä tilanteessa
pienen suorituskyvyn uhraaminen yksinkertaisuuden saavuttamiseksi on kannattava
kompromissi.

> ### `clone`-metodin kompromissit
>
> Monilla Rustaceaneilla on taipumus välttää `clone`-metodin käyttöä omistajuusongelmien
> korjaamiseen sen ajonaikaisen kustannuksen vuoksi. Luvussa 13 opit käyttämään
> tehokkaampia menetelmiä tämän tyyppisissä tilanteissa. Mutta toistaiseksi on
> ok kopioida muutama merkkijono jatkaaksesi edistymistä, koska teet nämä kopiot
> vain kerran ja tiedostopolku- ja hakumerkkijonosi ovat hyvin pieniä. On
> parempi olla hieman tehoton mutta toimiva ohjelma kuin yrittää hyperoptimoida
> koodia ensimmäisellä läpimenolla. Kun saat enemmän kokemusta Rustista, on
> helpompaa aloittaa tehokkaimmalla ratkaisulla, mutta toistaiseksi on täysin
> hyväksyttävää kutsua `clone`.

Olemme päivittäneet `main`-funktion niin, että se asettaa `parse_config`-funktion
palauttaman `Config`-instanssin muuttujaan nimeltä `config`, ja olemme päivittäneet
koodin, joka aiemmin käytti erillisiä `query`- ja `file_path`-muuttujia, käyttämään
sen sijaan `Config`-structin kenttiä.

Nyt koodimme välittää selkeämmin, että `query` ja `file_path` liittyvät toisiinsa
ja että niiden tarkoitus on määrittää, miten ohjelma toimii. Kaikki koodi, joka
käyttää näitä arvoja, tietää etsiä ne `config`-instanssista kentistä, jotka on
nimetty niiden tarkoituksen mukaan.

#### `Config`-structin konstruktorin luominen

Tähän asti olemme erottaneet komentoriviargumenttien jäsentämiseen liittyvän
logiikan `main`-funktiosta ja sijoittaneet sen `parse_config`-funktioon. Tämä
auttoi meitä näkemään, että `query`- ja `file_path`-arvot liittyivät toisiinsa,
ja tämän suhteen tulisi näkyä koodissamme. Lisäsimme sitten `Config`-structin
nimeämään `query`- ja `file_path`-arvojen liittyvän tarkoituksen ja pystyäksemme
palauttamaan arvojen nimet structin kenttien niminä `parse_config`-funktiosta.

Nyt kun `parse_config`-funktion tarkoitus on luoda `Config`-instanssi, voimme
muuttaa `parse_config`-funktion tavallisesta funktiosta `new`-nimiseksi funktioksi,
joka liittyy `Config`-structiin. Tämä muutos tekee koodista idiomaattisempaa.
Voimme luoda tyyppien instansseja standardikirjastossa, kuten `String`, kutsumalla
`String::new`. Vastaavasti muuttamalla `parse_config`-funktion `new`-funktioksi,
joka liittyy `Config`-structiin, voimme luoda `Config`-instansseja kutsumalla
`Config::new`. Listaus 12-7 näyttää tarvittavat muutokset.

<Listing number="12-7" file-name="src/main.rs" caption="`parse_config`-funktion muuttaminen `Config::new`-funktioksi">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-07/src/main.rs:here}}
```

</Listing>

Olemme päivittäneet `main`-funktion niin, että se kutsuu `parse_config`-funktion
sijaan `Config::new`-funktiota. Olemme muuttaneet `parse_config`-funktion nimen
`new`:ksi ja siirtäneet sen `impl`-lohkoon, joka liittää `new`-funktion `Config`-
structiin. Kokeile kääntää tämä koodi uudelleen varmistaaksesi, että se toimii.

### Virheenkäsittelyn korjaaminen

Työstetään nyt virheenkäsittelyn korjaamista. Muista, että yrittäminen käyttää
`args`-vektorin arvoja indeksissä 1 tai 2 aiheuttaa ohjelman paniikin, jos
vektori sisältää alle kolme kohdetta. Kokeile ajaa ohjelma ilman argumentteja;
se näyttää tältä:

```console
{{#include ../listings/ch12-an-io-project/listing-12-07/output.txt}}
```

Rivi `index out of bounds: the len is 1 but the index is 1` on ohjelmoijille
tarkoitettu virheilmoitus. Se ei auta loppukäyttäjiämme ymmärtämään, mitä heidän
pitäisi tehdä sen sijaan. Korjataan se nyt.

#### Virheviestin parantaminen

Listauksessa 12-8 lisäämme tarkistuksen `new`-funktioon, joka varmistaa, että
viipale on tarpeeksi pitkä ennen kuin käytämme indeksejä 1 ja 2. Jos viipale ei
ole tarpeeksi pitkä, ohjelma paniikkiutuu ja näyttää paremman virheviestin.

<Listing number="12-8" file-name="src/main.rs" caption="Tarkistuksen lisääminen argumenttien määrälle">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-08/src/main.rs:here}}
```

</Listing>

Tämä koodi on samanlainen kuin `Guess::new`-funktio, jonka kirjoitimme listauksessa
9-13, jossa kutsuimme `panic!`-makroa, kun `value`-argumentti oli kelvollisten
arvojen alueen ulkopuolella. Sen sijaan, että tarkistaisimme arvojen alueen
tässä, tarkistamme, että `args`-vektorin pituus on vähintään `3`, ja loput
funktiosta voivat toimia olettaen, että tämä ehto on täyttynyt. Jos `args`-
vektorissa on alle kolme kohdetta, tämä ehto on tosi, ja kutsumme `panic!`-
makroa lopettaaksemme ohjelman välittömästi.

Näillä muutamalla lisärivillä `new`-funktiossa ajetaan ohjelma uudelleen ilman
argumentteja nähdäksemme, miltä virhe näyttää nyt:

```console
{{#include ../listings/ch12-an-io-project/listing-12-08/output.txt}}
```

Tämä tuloste on parempi: Meillä on nyt järkevä virheilmoitus. Meillä on kuitenkin
myös ylimääräistä tietoa, jota emme halua antaa käyttäjillemme. Ehkä listauksessa
9-13 käyttämämme tekniikka ei ole paras käytettäväksi tässä: `panic!`-kutsu on
sopivampi ohjelmointiongelmaan kuin käyttöongelmaan, [kuten käsiteltiin luvussa
9][ch9-error-guidelines]<!-- ignore -->. Sen sijaan käytämme toista luvussa 9
oppimaamme tekniikkaa — [palautamme `Result`-arvon][ch9-result]<!-- ignore -->,
joka ilmaisee joko onnistumisen tai virheen.

<!-- Old headings. Do not remove or links may break. -->

<a id="returning-a-result-from-new-instead-of-calling-panic"></a>

#### `Result`-arvon palauttaminen `panic!`-kutsun sijaan

Voimme sen sijaan palauttaa `Result`-arvon, joka sisältää `Config`-instanssin
onnistumistapauksessa ja kuvaa ongelman virhetapauksessa. Muutamme myös funktion
nimen `new`:stä `build`:ksi, koska monet ohjelmoijat odottavat `new`-funktioiden
eivän koskaan epäonnistuvan. Kun `Config::build` kommunikoi `main`-funktion
kanssa, voimme käyttää `Result`-tyyppiä ilmaisemaan, että ongelma oli. Sitten
voimme muuttaa `main`-funktion muuntamaan `Err`-variantin käytännöllisemmäksi
virheeksi käyttäjillemme ilman ympäröivää tekstiä `thread 'main'` ja
`RUST_BACKTRACE` `panic!`-kutsun aiheuttamasta.

Listaus 12-9 näyttää muutokset, jotka meidän täytyy tehdä funktion palautusarvoon,
jota kutsumme nyt `Config::build`, ja funktion runkoon, joka tarvitaan `Result`-
arvon palauttamiseen. Huomaa, että tämä ei käänny ennen kuin päivitämme myös
`main`-funktion, minkä teemme seuraavassa listauksessa.

<Listing number="12-9" file-name="src/main.rs" caption="`Result`-arvon palauttaminen `Config::build`-funktiosta">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-09/src/main.rs:here}}
```

</Listing>

`build`-funktiomme palauttaa `Result`-arvon, jossa on `Config`-instanssi
onnistumistapauksessa ja merkkijonoliteraali virhetapauksessa. Virhearvomme
ovat aina merkkijonoliteraaleja, joilla on `'static`-elinikä.

Olemme tehneet kaksi muutosta funktion rungossa: Sen sijaan, että kutsuisimme
`panic!`-makroa, kun käyttäjä ei anna tarpeeksi argumentteja, palautamme nyt
`Err`-arvon, ja olemme käärittäneet `Config`-palautusarvon `Ok`-arvoon. Nämä
muutokset saavat funktion vastaamaan uutta tyyppiallekirjoitustaan.

`Err`-arvon palauttaminen `Config::build`-funktiosta antaa `main`-funktion
käsitellä `build`-funktion palauttaman `Result`-arvon ja lopettaa prosessin
siistimmin virhetapauksessa.

<!-- Old headings. Do not remove or links may break. -->

<a id="calling-confignew-and-handling-errors"></a>

#### `Config::build`-funktion kutsuminen ja virheiden käsittely

Käsitelläksemme virhetapauksen ja tulostaaksemme käyttäjäystävällisen viestin,
meidän täytyy päivittää `main` käsittelemään `Config::build`-funktion palauttama
`Result`, kuten listauksessa 12-10. Otamme myös vastuun komentorivityökalun
lopettamisesta nollasta poikkeavalla virhekoodilla pois `panic!`-makrosta ja
toteutamme sen käsin. Nollasta poikkeava poistumistila on käytäntö, jolla
signaaloidaan prosessille, joka kutsui ohjelmaamme, että ohjelma lopetti
virhetilassa.

<Listing number="12-10" file-name="src/main.rs" caption="Poistuminen virhekoodilla, jos `Config`-instanssin rakentaminen epäonnistuu">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-10/src/main.rs:here}}
```

</Listing>

Tässä listauksessa olemme käyttäneet metodia, jota emme ole käsitelleet
yksityiskohtaisesti: `unwrap_or_else`, joka on määritelty `Result<T, E>`-tyypille
standardikirjastossa. `unwrap_or_else`-metodin käyttö antaa meille määritellä
mukautetun, ei-`panic!`-virheenkäsittelyn. Jos `Result` on `Ok`-arvo, tämän
metodin käyttäytyminen on samanlainen kuin `unwrap`: Se palauttaa `Ok`-arvon
sisältämän sisäisen arvon. Jos arvo on kuitenkin `Err`-arvo, tämä metodi kutsuu
sulkeuman koodia, joka on anonyymi funktio, jonka määrittelemme ja välitämme
argumenttina `unwrap_or_else`-metodille. Käsittelemme sulkeumia yksityiskohtaisemmin
luvussa 13. Toistaiseksi sinun tarvitsee vain tietää, että `unwrap_or_else` välittää
`Err`-arvon sisäisen arvon, joka tässä tapauksessa on staattinen merkkijono
`"not enough arguments"`, jonka lisäsimme listauksessa 12-9, sulkeumaamme
argumentissa `err`, joka esiintyy pystyviivojen välissä. Sulkeuman koodi voi
sitten käyttää `err`-arvoa suorittaessaan.

Olemme lisänneet uuden `use`-rivin tuodaksemme `process`-moduulin standardikirjastosta
näkyviin. Sulkeuman koodi, joka suoritetaan virhetapauksessa, on vain kaksi
riviä: Tulostamme `err`-arvon ja kutsumme sitten `process::exit`. `process::exit`-
funktio pysäyttää ohjelman välittömästi ja palauttaa numeron, joka annettiin
poistumistilakoodina. Tämä on samanlaista kuin listauksessa 12-8 käyttämämme
`panic!`-pohjainen käsittely, mutta emme enää saa kaikkea ylimääräistä tulostetta.
Kokeillaan:

```console
{{#include ../listings/ch12-an-io-project/listing-12-10/output.txt}}
```

Hienoa! Tämä tuloste on paljon ystävällisempi käyttäjillemme.

<!-- Old headings. Do not remove or links may break. -->

<a id="extracting-logic-from-the-main-function"></a>

### Logiikan erottaminen `main`-funktiosta

Nyt kun olemme lopettaneet konfiguraation jäsentämisen refaktoroinnin, käännymme
ohjelman logiikan pariin. Kuten totesimme osiossa [”Huolenaiheiden erottaminen
binääriprojekteissa”](#separation-of-concerns-for-binary-projects)<!-- ignore -->,
erotamme `run`-nimisen funktion, joka sisältää kaiken logiikan, joka on tällä
hetkellä `main`-funktiossa eikä liity konfiguraation asettamiseen tai virheiden
käsittelyyn. Kun olemme valmiit, `main`-funktio on tiivis ja helppo varmistaa
tarkastelemalla, ja voimme kirjoittaa testejä kaikelle muulle logiikalle.

Listaus 12-11 näyttää pienen, inkrementaalisen parannuksen `run`-funktion
erottamisesta.

<Listing number="12-11" file-name="src/main.rs" caption="`run`-funktion erottaminen, joka sisältää loput ohjelman logiikasta">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-11/src/main.rs:here}}
```

</Listing>

`run`-funktio sisältää nyt kaiken jäljellä olevan logiikan `main`-funktiosta
alkaen tiedoston lukemisesta. `run`-funktio ottaa `Config`-instanssin argumenttina.

<!-- Old headings. Do not remove or links may break. -->

<a id="returning-errors-from-the-run-function"></a>

#### Virheiden palauttaminen `run`-funktiosta

Kun jäljellä oleva ohjelman logiikka on erotettu `run`-funktioon, voimme
parantaa virheenkäsittelyä, kuten teimme `Config::build`-funktiossa listauksessa
12-9. Sen sijaan, että sallisimme ohjelman paniikin kutsumalla `expect`-metodia,
`run`-funktio palauttaa `Result<T, E>`-arvon, kun jokin menee pieleen. Tämä
antaa meille mahdollisuuden koota virheenkäsittelylogiikkaa edelleen `main`-
funktioon käyttäjäystävällisellä tavalla. Listaus 12-12 näyttää muutokset,
jotka meidän täytyy tehdä `run`-funktion allekirjoitukseen ja runkoon.

<Listing number="12-12" file-name="src/main.rs" caption="`run`-funktion muuttaminen palauttamaan `Result`">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-12/src/main.rs:here}}
```

</Listing>

Olemme tehneet kolme merkittävää muutosta. Ensinnäkin muutimme `run`-funktion
palautustyypiksi `Result<(), Box<dyn Error>>`. Tämä funktio palautti aiemmin
yksikkötyypin `()`, ja säilytämme sen `Ok`-tapauksen palautusarvona.

Virhetyypiksi käytimme trait-oliota `Box<dyn Error>` (ja toimme `std::error::Error`-
moduulin näkyviin `use`-lauseella tiedoston alussa). Käsittelemme trait-olioita
luvussa 18. Toistaiseksi tiedä vain, että `Box<dyn Error>` tarkoittaa, että
funktio palauttaa tyypin, joka toteuttaa `Error`-traitin, mutta emme tarvitse
määrittää, mikä tietty tyyppi palautusarvo on. Tämä antaa meille joustavuutta
palauttaa virhearvoja, jotka voivat olla eri tyyppejä eri virhetapauksissa.
`dyn`-avainsana on lyhenne sanasta _dynamic_.

Toiseksi olemme poistaneet `expect`-kutsun `?`-operaattorin hyväksi, kuten
puhuimme luvussa 9. Sen sijaan, että `panic!` virheessä, `?` palauttaa virhearvon
nykyisestä funktiosta kutsujan käsiteltäväksi.

Kolmanneksi `run`-funktio palauttaa nyt `Ok`-arvon onnistumistapauksessa.
Olemme ilmoittaneet `run`-funktion onnistumistyypiksi `()` allekirjoituksessa,
mikä tarkoittaa, että meidän täytyy kääriä yksikkötyypin arvo `Ok`-arvoon. Tämä
`Ok(())`-syntaksi saattaa aluksi näyttää hieman oudolta. Mutta `()`-tyypin
käyttö tällä tavalla on idiomaattinen tapa ilmaista, että kutsumme `run`-funktiota
vain sen sivuvaikutuksia varten; se ei palauta arvoa, jota tarvitsemme.

Kun ajat tämän koodin, se kääntyy mutta näyttää varoituksen:

```console
{{#include ../listings/ch12-an-io-project/listing-12-12/output.txt}}
```

Rust kertoo, että koodimme ohitti `Result`-arvon ja `Result`-arvo saattaa
ilmaista, että virhe tapahtui. Mutta emme tarkista, tapahtuiko virhe, ja
kääntäjä muistuttaa, että meillä oli todennäköisesti tarkoitus olla virheenkäsittelykoodia
tässä! Korjataan tämä ongelma nyt.

#### `run`-funktion palauttamien virheiden käsittely `main`-funktiossa

Tarkistamme virheet ja käsittelemme ne tekniikalla, joka on samanlainen kuin
`Config::build`-funktion kanssa listauksessa 12-10, mutta pienellä erolla:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/no-listing-01-handling-errors-in-main/src/main.rs:here}}
```

Käytämme `if let` -lausetta `unwrap_or_else`-metodin sijaan tarkistaaksemme,
palauttaako `run` `Err`-arvon, ja kutsumme `process::exit(1)`, jos se palauttaa.
`run`-funktio ei palauta arvoa, jota haluamme `unwrap`-metodilla purkaa samalla
tavalla kuin `Config::build` palauttaa `Config`-instanssin. Koska `run` palauttaa
`()` onnistumistapauksessa, välitämme vain virheen havaitsemisesta, joten emme
tarvitse `unwrap_or_else`-metodia palauttamaan purettua arvoa, joka olisi vain
`()`.

`if let` - ja `unwrap_or_else`-funktioiden rungot ovat samat molemmissa
tapauksissa: Tulostamme virheen ja poistumme.

### Koodin jakaminen kirjastocrateen

`minigrep`-projektimme näyttää hyvältä tähän asti! Jaamme nyt _src/main.rs_-
tiedoston ja siirrämme osan koodista _src/lib.rs_-tiedostoon. Näin voimme testata
koodia ja meillä on _src/main.rs_-tiedosto, jolla on vähemmän vastuita.

Määritellään tekstin hakemiseen liittyvä koodi _src/lib.rs_-tiedostossa
_src/main.rs_-tiedoston sijaan, jolloin voimme (tai kuka tahansa `minigrep`-
kirjastomme käyttäjä) kutsua hakufunktiota useammissa konteksteissa kuin
`minigrep`-binäärimme.

Ensin määritellään `search`-funktion allekirjoitus _src/lib.rs_-tiedostossa,
kuten listauksessa 12-13, rungolla, joka kutsuu `unimplemented!`-makroa. Selitämme
allekirjoituksen yksityiskohtaisemmin, kun täytämme toteutuksen.

<Listing number="12-13" file-name="src/lib.rs" caption="`search`-funktion määrittely *src/lib.rs*-tiedostossa">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-13/src/lib.rs}}
```

</Listing>

Olemme käyttäneet `pub`-avainsanaa funktiomäärittelyssä merkitsemään `search`-
funktion osaksi kirjastocratemme julkista API:a. Meillä on nyt kirjastocrate,
jota voimme käyttää binääricratestamme ja jota voimme testata!

Meidän täytyy nyt tuoda _src/lib.rs_-tiedostossa määritelty koodi binääricraten
näkyvyysalueelle _src/main.rs_-tiedostossa ja kutsua sitä, kuten listauksessa 12-14.

<Listing number="12-14" file-name="src/main.rs" caption="`minigrep`-kirjastocraten `search`-funktion käyttö *src/main.rs*-tiedostossa">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-14/src/main.rs:here}}
```

</Listing>

Lisäämme `use minigrep::search` -rivin tuodaksemme `search`-funktion kirjastocratesta
binääricraten näkyvyysalueelle. Sitten `run`-funktiossa tiedoston sisällön
tulostamisen sijaan kutsumme `search`-funktiota ja välitämme `config.query`-
arvon ja `contents`-arvon argumentteina. Sitten `run` käyttää `for`-silmukkaa
tulostaakseen jokaisen `search`-funktion palauttaman rivin, joka vastasi
hakua. Tämä on myös hyvä hetki poistaa `println!`-kutsut `main`-funktiosta,
jotka näyttivät haun ja tiedostopolun, jotta ohjelmamme tulostaa vain
hakutulokset (jos virheitä ei tapahdu).

Huomaa, että hakufunktio kerää kaikki tulokset vektoriin, jonka se palauttaa
ennen kuin mitään tulostusta tapahtuu. Tämä toteutus voi olla hidas näyttämään
tuloksia suurten tiedostojen haussa, koska tuloksia ei tulosteta niiden
löytyessä; käsittelemme mahdollisen korjauksen iteraattoreiden avulla luvussa 13.

Huh! Sitä oli paljon työtä, mutta olemme asettaneet itsellemme pohjan menestykseen
tulevaisuudessa. Nyt on paljon helpompaa käsitellä virheitä, ja olemme tehneet
koodista modulaarisempaa. Lähes kaikki työmme tehdään tästä eteenpäin _src/lib.rs_-
tiedostossa.

Hyödynnetään tätä uutta modulaarisuutta tekemällä jotain, mikä olisi ollut
vaikeaa vanhalla koodilla mutta on helppoa uudella koodilla: Kirjoitamme testejä!

[ch13]: ch13-00-functional-features.html
[ch9-custom-types]: ch09-03-to-panic-or-not-to-panic.html#creating-custom-types-for-validation
[ch9-error-guidelines]: ch09-03-to-panic-or-not-to-panic.html#guidelines-for-error-handling
[ch9-result]: ch09-02-recoverable-errors-with-result.html
[ch18]: ch18-00-oop.html
[ch9-question-mark]: ch09-02-recoverable-errors-with-result.html#a-shortcut-for-propagating-errors-the--operator
