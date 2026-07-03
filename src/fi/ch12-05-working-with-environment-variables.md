## Työskentely ympäristömuuttujien kanssa

Parannamme `minigrep`-binääriä lisäämällä ylimääräisen ominaisuuden: kirjainkoon
huomioimattoman haun vaihtoehdon, jonka käyttäjä voi kytkeä päälle ympäristömuuttujan
avulla. Voisimme tehdä tästä ominaisuuden komentorivivalinnan ja vaatia käyttäjän
syöttämään sen joka kerta, kun haluaa sen käyttöön, mutta tekemällä siitä
ympäristömuuttujan sallimme käyttäjiemme asettaa ympäristömuuttujan kerran ja
kaikki heidän hakunsa ovat kirjainkosta riippumattomia kyseisessä terminaali-
istunnossa.

<!-- Old headings. Do not remove or links may break. -->
<a id="writing-a-failing-test-for-the-case-insensitive-search-function"></a>

### Epäonnistuvan testin kirjoittaminen kirjainkosta riippumattomalle haulle

Lisäämme ensin uuden `search_case_insensitive`-funktion `minigrep`-kirjastoon,
jota kutsutaan, kun ympäristömuuttujalla on arvo. Jatkamme TDD-prosessia, joten
ensimmäinen askel on taas kirjoittaa epäonnistuva testi. Lisäämme uuden testin
uudelle `search_case_insensitive`-funktiolle ja nimeämme vanhan testimme uudelleen
`one_result`:sta `case_sensitive`:ksi selventääksemme kahden testin eroja, kuten
listauksessa 12-20.

<Listing number="12-20" file-name="src/lib.rs" caption="Uuden epäonnistuvan testin lisääminen lisäämällemme kirjainkosta riippumattomalle funktiolle">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-20/src/lib.rs:here}}
```

</Listing>

Huomaa, että olemme muokanneet myös vanhan testin `contents`-arvoa. Olemme
lisänneet uuden rivin tekstillä `"Duct tape."` käyttäen isoa _D_:tä, joka ei
pitäisi vastata hakua `"duct"`, kun haemme kirjainkoon huomioivasti. Vanhan testin
muuttaminen tällä tavalla auttaa varmistamaan, ettei vahingossa riko jo
toteuttamaamme kirjainkoon huomioivaa hakutoiminnallisuutta. Tämän testin pitäisi
läpäistä nyt ja jatkossakin läpäistä työskennellessämme kirjainkosta riippumattoman
haun parissa.

Uusi testi kirjainkosta _riippumattomalle_ haulle käyttää hakuaan `"rUsT"`.
`search_case_insensitive`-funktiossa, jonka olemme lisäämässä, haun `"rUsT"`
pitäisi vastata riviä, joka sisältää `"Rust:"` isolla _R_:llä, ja riviä
`"Trust me."` vaikka molemmat eroavat kirjainkoosta hausta. Tämä on epäonnistuva
testimme, ja se ei käänny, koska emme ole vielä määritelleet `search_case_insensitive`-
funktiota. Voit vapaasti lisätä luurangon toteutuksen, joka palauttaa aina tyhjän
vektorin, samalla tavalla kuin teimme `search`-funktiolle listauksessa 12-16
nähdäksesi testin kääntyvän ja epäonnistuvan.

### `search_case_insensitive`-funktion toteuttaminen

`search_case_insensitive`-funktio, joka näytetään listauksessa 12-21, on lähes
sama kuin `search`-funktio. Ainoa ero on, että muutamme `query`-merkkijonon ja
jokaisen `line`-rivin pieniksi kirjaimiksi, jotta riippumatta syöteargumenttien
kirjainkoosta ne ovat samaa kirjainkokoa, kun tarkistamme, sisältääkö rivi haun.

<Listing number="12-21" file-name="src/lib.rs" caption="`search_case_insensitive`-funktion määrittely, joka muuttaa haun ja rivin pieniksi kirjaimiksi ennen vertailua">

```rust,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-21/src/lib.rs:here}}
```

</Listing>

Ensin muutamme `query`-merkkijonon pieniksi kirjaimiksi ja tallennamme sen
uuteen muuttujaan samalla nimellä varjostaen alkuperäisen `query`-arvon. `query`-
merkkijonon `to_lowercase`-kutsu on tarpeen, jotta riippumatta siitä, onko
käyttäjän hakusi `"rust"`, `"RUST"`, `"Rust"` vai `"rUsT"`, käsittelemme haun
kuin se olisi `"rust"` ja olemme kirjainkoosta riippumattomia. Vaikka `to_lowercase`
käsittelee perus-Unicodea, se ei ole 100-prosenttisen tarkka. Jos kirjoittaisimme
oikean sovelluksen, tekisimme täällä hieman enemmän työtä, mutta tämä osio koskee
ympäristömuuttujia, ei Unicodea, joten jätämme sen tähän.

Huomaa, että `query` on nyt `String` eikä merkkijonoviipale, koska `to_lowercase`-
kutsu luo uutta dataa sen sijaan, että viittaisi olemassa olevaan dataan. Sanotaan,
että haku on `"rUsT"` esimerkkinä: Tuo merkkijonoviipale ei sisällä pientä `u`:ta
tai `t`:tä käytettäväksi, joten meidän täytyy varata uusi `String`, joka sisältää
`"rust"`. Kun välitämme `query`-arvon argumenttina `contains`-metodille nyt,
meidän täytyy lisätä etumerkki, koska `contains`-metodin allekirjoitus on
määritelty ottamaan merkkijonoviipale.

Seuraavaksi lisäämme `to_lowercase`-kutsun jokaiselle `line`-riville muuttaaksemme
kaikki merkit pieniksi kirjaimiksi. Nyt kun olemme muuttaneet `line`- ja `query`-
arvot pieniksi kirjaimiksi, löydämme osumia riippumatta haun kirjainkoosta.

Katsotaan, läpäisevätkö nämä toteutukset testit:

```console
{{#include ../listings/ch12-an-io-project/listing-12-21/output.txt}}
```

Hienoa! Ne läpäisivät. Kutsutaan nyt uutta `search_case_insensitive`-funktiota
`run`-funktiosta. Ensin lisäämme konfiguraatiovaihtoehdon `Config`-structiin
vaihtaaksemme kirjainkoon huomioivan ja kirjainkosta riippumattoman haun välillä.
Tämän kentän lisääminen aiheuttaa kääntäjävirheitä, koska emme alusta tätä
kenttää vielä missään:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-22/src/main.rs:here}}
```

Lisäsimme `ignore_case`-kentän, joka säilyttää totuusarvon. Seuraavaksi `run`-
funktion täytyy tarkistaa `ignore_case`-kentän arvo ja käyttää sitä päättääkseen,
kutsutaanko `search`- vai `search_case_insensitive`-funktiota, kuten listauksessa
12-22. Tämä ei vielä käänny.

<Listing number="12-22" file-name="src/main.rs" caption="Joko `search`- tai `search_case_insensitive`-funktion kutsuminen `config.ignore_case`-arvon perusteella">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-22/src/main.rs:there}}
```

</Listing>

Lopuksi meidän täytyy tarkistaa ympäristömuuttuja. Ympäristömuuttujien kanssa
työskentelyyn liittyvät funktiot ovat `env`-moduulissa standardikirjastossa,
joka on jo näkyvyysalueella _src/main.rs_-tiedoston alussa. Käytämme `env`-
moduulin `var`-funktiota tarkistaaksemme, onko ympäristömuuttujalle nimeltä
`IGNORE_CASE` asetettu jokin arvo, kuten listauksessa 12-23.

<Listing number="12-23" file-name="src/main.rs" caption="Minkä tahansa arvon tarkistaminen `IGNORE_CASE`-nimisessä ympäristömuuttujassa">

```rust,ignore,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-23/src/main.rs:here}}
```

</Listing>

Tässä luomme uuden muuttujan `ignore_case`. Asettaaksemme sen arvon kutsumme
`env::var`-funktiota ja välitämme sille `IGNORE_CASE`-ympäristömuuttujan nimen.
`env::var`-funktio palauttaa `Result`-arvon, joka on onnistunut `Ok`-variantti,
joka sisältää ympäristömuuttujan arvon, jos ympäristömuuttuja on asetettu
mihin tahansa arvoon. Se palauttaa `Err`-variantin, jos ympäristömuuttujaa ei
ole asetettu.

Käytämme `Result`-arvon `is_ok`-metodia tarkistaaksemme, onko ympäristömuuttuja
asetettu, mikä tarkoittaa, että ohjelman pitäisi tehdä kirjainkosta riippumaton
haku. Jos `IGNORE_CASE`-ympäristömuuttujaa ei ole asetettu mihinkään, `is_ok`
palauttaa `false` ja ohjelma suorittaa kirjainkoon huomioivan haun. Emme välitä
ympäristömuuttujan _arvosta_, vain siitä, onko se asetettu vai ei, joten
tarkistamme `is_ok`-metodilla `unwrap`-, `expect`- tai muiden `Result`-arvoon
liittyvien metodien sijaan.

Välitämme `ignore_case`-muuttujan arvon `Config`-instanssille, jotta `run`-
funktio voi lukea sen arvon ja päättää, kutsutaanko `search_case_insensitive`-
vai `search`-funktiota, kuten toteutimme listauksessa 12-22.

Kokeillaan! Ensin ajamme ohjelmamme ilman asetettua ympäristömuuttujaa ja haulla
`to`, joka pitäisi vastata mitä tahansa riviä, joka sisältää sanan _to_ kaikilla
pienillä kirjaimilla:

```console
{{#include ../listings/ch12-an-io-project/listing-12-23/output.txt}}
```

Näyttää siltä, että se toimii edelleen! Ajetaan nyt ohjelma `IGNORE_CASE`-
ympäristömuuttujalla asetettuna arvoon `1` mutta samalla haulla `to`:

```console
$ IGNORE_CASE=1 cargo run -- to poem.txt
```

Jos käytät PowerShelliä, sinun täytyy asettaa ympäristömuuttuja ja ajaa ohjelma
erillisinä komentoina:

```console
PS> $Env:IGNORE_CASE=1; cargo run -- to poem.txt
```

Tämä saa `IGNORE_CASE`:n pysymään voimassa loppuun asti komentotulkki-istunnossasi.
Sen voi poistaa `Remove-Item`-cmdletillä:

```console
PS> Remove-Item Env:IGNORE_CASE
```

Meidän pitäisi saada rivit, jotka sisältävät _to_-sanoja, joissa voi olla isoja
kirjaimia:

<!-- manual-regeneration
cd listings/ch12-an-io-project/listing-12-23
IGNORE_CASE=1 cargo run -- to poem.txt
can't extract because of the environment variable
-->

```console
Are you nobody, too?
How dreary to be somebody!
To tell your name the livelong day
To an admiring bog!
```

Erinomaista, saimme myös rivejä, jotka sisältävät _To_-sanoja! `minigrep`-ohjelmamme
voi nyt tehdä kirjainkosta riippumatonta hakua ympäristömuuttujan ohjaamana. Nyt
tiedät, miten hallita vaihtoehtoja, jotka on asetettu joko komentoriviargumenttien
tai ympäristömuuttujien avulla.

Jotkut ohjelmat sallivat argumentit _ja_ ympäristömuuttujat samalle konfiguraatiolle.
Näissä tapauksissa ohjelmat päättävät, kumpi on etusijalla. Harjoitukseksi
itsenäisesti kokeile hallita kirjainkoon huomiointia joko komentoriviargumentin
tai ympäristömuuttujan avulla. Päätä, pitäisikö komentoriviargumentin vai
ympäristömuuttujan olla etusijalla, jos ohjelma ajetaan toisen asetettuna
kirjainkoon huomioivaksi ja toisen kirjainkoon huomioimattomaksi.

`std::env`-moduuli sisältää paljon hyödyllisiä ominaisuuksia ympäristömuuttujien
käsittelyyn: Tutustu sen dokumentaatioon nähdäksesi, mitä on saatavilla.
