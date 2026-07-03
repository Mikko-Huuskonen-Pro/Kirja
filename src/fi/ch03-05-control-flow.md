## Ohjausrakenteet

Mahdollisuus suorittaa koodia riippuen siitä, onko ehto `true`, ja mahdollisuus suorittaa koodia toistuvasti, kun ehto on `true`, ovat perusrakennuspalikoita useimmissa ohjelmointikielissä. Yleisimmät rakenteet, jotka antavat hallita Rust-koodin suoritusvirtaa, ovat `if`-lausekkeet ja silmukat.

### `if`-lausekkeet

`if`-lauseke antaa haarauttaa koodiasi ehtojen mukaan. Annat ehdon ja sanot sitten: "Jos tämä ehto täyttyy, suorita tämä koodilohko. Jos ehto ei täyty, älä suorita tätä koodilohkoa."

Luo uusi projekti nimeltä _branches_ _projects_-kansioosi tutkiaksesi `if`-lauseketta. Kirjoita _src/main.rs_-tiedostoon seuraava:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-26-if-true/src/main.rs}}
```

Kaikki `if`-lausekkeet alkavat avainsanalla `if`, jota seuraa ehto. Tässä tapauksessa ehto tarkistaa, onko muuttujan `number` arvo pienempi kuin 5. Sijoitamme koodilohkon, joka suoritetaan, jos ehto on `true`, heti ehdon jälkeen aaltosulkeiden sisään. `if`-lausekkeiden ehtoihin liittyviä koodilohkoja kutsutaan joskus _haaroiksi_, aivan kuten `match`-lausekkeiden haaroiksi, joita käsittelimme ["Arvauksen vertaaminen salaisnumeroon"][comparing-the-guess-to-the-secret-number]<!-- ignore --> -osiossa Luvussa 2.

Valinnaisesti voimme myös sisällyttää `else`-lausekkeen, kuten teimme tässä, antaaksemme ohjelmalle vaihtoehtoisen koodilohkon suoritettavaksi, jos ehto evaluoituu `false`:ksi. Jos et anna `else`-lauseketta ja ehto on `false`, ohjelma ohittaa `if`-lohkon ja siirtyy seuraavaan koodinpalaan.

Kokeile suorittaa tämä koodi; sinun pitäisi nähdä seuraava tuloste:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-26-if-true/output.txt}}
```

Kokeillaan muuttaa `number`-muuttujan arvoksi sellainen, joka tekee ehdosta `false`, ja katsotaan, mitä tapahtuu:

```rust,ignore
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-27-if-false/src/main.rs:here}}
```

Suorita ohjelma uudelleen ja katso tuloste:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-27-if-false/output.txt}}
```

On myös syytä huomata, että tämän koodin ehdon _täytyy_ olla `bool`. Jos ehto ei ole `bool`, saamme virheen. Kokeile esimerkiksi suorittaa seuraava koodi:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-28-if-condition-must-be-bool/src/main.rs}}
```

`if`-ehto evaluoituu tällä kertaa arvoksi `3`, ja Rust heittää virheen:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-28-if-condition-must-be-bool/output.txt}}
```

Virhe osoittaa, että Rust odotti `bool`-tyyppiä mutta sai kokonaisluvun. Toisin kuin kielet kuten Ruby ja JavaScript, Rust ei automaattisesti yritä muuntaa ei-totuusarvoisia tyyppejä totuusarvoiksi. Sinun täytyy olla eksplisiittinen ja antaa `if`:lle aina totuusarvo ehtona. Jos haluamme `if`-koodilohkon suorittuvan vain, kun luku ei ole yhtä suuri kuin `0`, voimme muuttaa `if`-lausekkeen seuraavaksi:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-29-if-not-equal-0/src/main.rs}}
```

Tämän koodin suorittaminen tulostaa `number was something other than zero`.

#### Useiden ehtojen käsittely `else if`:llä

Voit käyttää useita ehtoja yhdistämällä `if`- ja `else`-lausekkeet `else if` -lausekkeeseen. Esimerkiksi:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-30-else-if/src/main.rs}}
```

Tällä ohjelmalla on neljä mahdollista polkua. Suoritettuasi sen sinun pitäisi nähdä seuraava tuloste:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-30-else-if/output.txt}}
```

Kun tämä ohjelma suoritetaan, se tarkistaa jokaisen `if`-lausekkeen vuorollaan ja suorittaa ensimmäisen rungon, jonka ehto evaluoituu `true`:ksi. Huomaa, että vaikka 6 on jaollinen 2:lla, emme näe tulostetta `number is divisible by 2`, emmekä `number is not divisible by 4, 3, or 2` -tekstiä `else`-lohkosta. Tämä johtuu siitä, että Rust suorittaa vain ensimmäisen `true`-ehdon lohkon, eikä tarkista loputkaan sen jälkeen.

Liian monen `else if` -lausekkeen käyttö voi sotkea koodiasi, joten jos sinulla on useampi kuin yksi, saatat haluta refaktoroida koodisi. Luku 6 kuvaa tehokkaan Rust-haarautumisrakenteen nimeltä `match` näihin tapauksiin.

#### `if`:n käyttö `let`-lausekkeessa

Koska `if` on lauseke, voimme käyttää sitä `let`-lausekkeen oikealla puolella sijoittaaksemme tuloksen muuttujaan, kuten Listauksessa 3-2.

<Listing number="3-2" file-name="src/main.rs" caption="`if`-lausekkeen tuloksen sijoittaminen muuttujaan">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-02/src/main.rs}}
```

</Listing>

`number`-muuttuja sidotaan arvoon `if`-lausekkeen tuloksen perusteella. Suorita tämä koodi nähdäksesi, mitä tapahtuu:

```console
{{#include ../listings/ch03-common-programming-concepts/listing-03-02/output.txt}}
```

Muista, että koodilohkot evaluoituvat viimeiseen lausekkeeseensa, ja numerot itsessään ovat myös lausekkeita. Tässä tapauksessa koko `if`-lausekkeen arvo riippuu siitä, mikä koodilohko suoritetaan. Tämä tarkoittaa, että arvojen, joilla on potentiaalia olla tuloksia kustakin `if`-haarasta, täytyy olla sama tyyppi; Listauksessa 3-2 sekä `if`- että `else`-haaran tulokset olivat `i32`-kokonaislukuja. Jos tyypit eivät täsmää, kuten seuraavassa esimerkissä, saamme virheen:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-31-arms-must-return-same-type/src/main.rs}}
```

Kun yritämme kääntää tämän koodin, saamme virheen. `if`- ja `else`-haaroilla on yhteensopimattomat arvotyypit, ja Rust osoittaa tarkalleen, mistä ongelma löytyy ohjelmasta:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-31-arms-must-return-same-type/output.txt}}
```

`if`-lohkon lauseke evaluoituu kokonaisluvuksi, ja `else`-lohkon lauseke evaluoituu merkkijonoksi. Tämä ei toimi, koska muuttujilla täytyy olla yksi tyyppi, ja Rustin täytyy tietää varmasti käännösaikana, mikä `number`-muuttujan tyyppi on. `number`-muuttujan tyypin tunteminen antaa kääntäjälle mahdollisuuden tarkistaa, että tyyppi on kelvollinen kaikkialla, missä käytämme `number`-muuttujaa. Rust ei pystyisi siihen, jos `number`-muuttujan tyyppi määräytyisi vasta ajonaikana; kääntäjä olisi monimutkaisempi ja antaisi vähemmän takeita koodista, jos sen täytyisi seurata useita hypoteettisia tyyppejä mille tahansa muuttujalle.

### Toisto silmukoilla

On usein hyödyllistä suorittaa koodilohkoa useammin kuin kerran. Tätä tehtävää varten Rust tarjoaa useita _silmukoita_, jotka suorittavat silmukan rungon koodin loppuun ja alkavat sitten heti alusta. Kokeillaksemme silmukoita luodaan uusi projekti nimeltä _loops_.

Rustissa on kolmelaista silmukkaa: `loop`, `while` ja `for`. Kokeillaan kutakin.

#### Koodin toistaminen `loop`:lla

`loop`-avainsana käskee Rustia suorittamaan koodilohkon uudelleen ja uudelleen joko ikuisesti tai kunnes kerrot sille eksplisiittisesti lopettamaan.

Esimerkkinä muuta _loops_-kansiosi _src/main.rs_-tiedosto näyttämään tältä:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-loop/src/main.rs}}
```

Kun suoritamme tämän ohjelman, näemme `again!` tulostuvan yhä uudelleen, kunnes pysäytämme ohjelman manuaalisesti. Useimmat terminaalit tukevat näppäinyhdistelmää <kbd>ctrl</kbd>-<kbd>C</kbd> keskeyttääkseen ohjelman, joka on jumissa jatkuvassa silmukassa. Kokeile:

<!-- manual-regeneration
cd listings/ch03-common-programming-concepts/no-listing-32-loop
cargo run
CTRL-C
-->

```console
$ cargo run
   Compiling loops v0.1.0 (file:///projects/loops)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.08s
     Running `target/debug/loops`
again!
again!
again!
again!
^Cagain!
```

Symboli `^C` edustaa kohtaa, jossa painoit <kbd>ctrl</kbd>-<kbd>C</kbd>.

Saatat tai et näe sanaa `again!` tulostuvan `^C`:n jälkeen riippuen siitä, missä koodissa silmukka oli, kun se vastaanotti keskeytystsignaalin.

Onneksi Rust tarjoaa myös tavan poistua silmukasta koodilla. Voit sijoittaa `break`-avainsanan silmukan sisään kertoaksesi ohjelmalle, milloin lopettaa silmukan suorittaminen. Muistathan, että teimme tämän arvauspelissä ["Lopettaminen oikean arvauksen jälkeen"][quitting-after-a-correct-guess]<!-- ignore --> -osiossa Luvussa 2 poistuaksemme ohjelmasta, kun käyttäjä voitti pelin arvaamalla oikean numeron.

Käytimme myös `continue`-avainsanaa arvauspelissä, joka silmukassa käskee ohjelmaa ohittamaan kaiken jäljellä olevan koodin tässä iteraatiossa ja siirtymään seuraavaan iteraatioon.

#### Arvojen palauttaminen silmukoista

Yksi `loop`-silmukan käyttötarkoitus on yrittää uudelleen operaatiota, jonka tiedät saattavan epäonnistua, kuten tarkistaa, onko säie suorittanut työnsä loppuun. Saatat myös tarvita välittää kyseisen operaation tuloksen silmukasta koodisi loppuosan. Voit tehdä tämän lisäämällä palautettavan arvon `break`-lausekkeen jälkeen, jota käytät silmukan pysäyttämiseen; tämä arvo palautetaan silmukasta, jotta voit käyttää sitä, kuten tässä:

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-33-return-value-from-loop/src/main.rs}}
```

Ennen silmukkaa julistamme muuttujan nimeltä `counter` ja alustamme sen arvoon `0`. Sitten julistamme muuttujan nimeltä `result` pitämään silmukasta palautettavan arvon. Jokaisella silmukan iteraatiolla lisäämme `1`:n `counter`-muuttujaan ja tarkistamme sitten, onko `counter` yhtä suuri kuin `10`. Kun se on, käytämme `break`-avainsanaa arvolla `counter * 2`. Silmukan jälkeen käytämme puolipistettä lopettaaksemme lausekkeen, joka sijoittaa arvon `result`:iin. Lopuksi tulostamme `result`:in arvon, joka tässä tapauksessa on `20`.

Voit myös `return`-palata silmukan sisältä. Vaikka `break` poistuu vain nykyisestä silmukasta, `return` poistuu aina nykyisestä funktiosta.

<!-- Old headings. Do not remove or links may break. -->
<a id="loop-labels-to-disambiguate-between-multiple-loops"></a>

#### Erottelu silmukkamerkinnöillä

Jos sinulla on silmukoita silmukoiden sisällä, `break` ja `continue` koskevat sisintä silmukkaa kyseisessä kohdassa. Voit valinnaisesti määrittää _silmukkamerkinnän_ silmukalle, jota voit sitten käyttää `break`- tai `continue`-avainsanojen kanssa määrittääksesi, että nämä avainsanat koskevat merkittyä silmukkaa sisimmän silmukan sijaan. Silmukkamerkintöjen täytyy alkaa yksittäisellä heittomerkillä. Tässä on esimerkki kahdella sisäkkäisellä silmukalla:

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-5-loop-labels/src/main.rs}}
```

Ulompi silmukka on merkitty `'counting_up`, ja se laskee ylöspäin 0:sta 2:een. Sisempi silmukka ilman merkintää laskee alaspäin 10:stä 9:ään. Ensimmäinen `break`, joka ei määritä merkintää, poistuu vain sisemmästä silmukasta. `break 'counting_up;` -lauseke poistuu ulommasta silmukasta. Tämä koodi tulostaa:

```console
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-5-loop-labels/output.txt}}
```

<!-- Old headings. Do not remove or links may break. -->
<a id="conditional-loops-with-while"></a>

#### Ehdollisten silmukoiden virtaviivaistaminen while:lla

Ohjelman täytyy usein arvioida ehto silmukan sisällä. Niin kauan kuin ehto on `true`, silmukka suoritetaan. Kun ehto ei enää ole `true`, ohjelma kutsuu `break`:ia pysäyttääkseen silmukan. Tällaisen käyttäytymisen voi toteuttaa yhdistelmällä `loop`, `if`, `else` ja `break`; voit kokeilla sitä nyt ohjelmassa, jos haluat. Tämä malli on kuitenkin niin yleinen, että Rustissa on siihen sisäänrakennettu kielenrakenne nimeltä `while`-silmukka. Listauksessa 3-3 käytämme `while`-silmukkaa silmukan suorittamiseen kolme kertaa, laskemalla alas joka kerta, ja sitten silmukan jälkeen tulostamaan viestin ja poistumaan.

<Listing number="3-3" file-name="src/main.rs" caption="`while`-silmukan käyttö koodin suorittamiseen, kun ehto evaluoituu `true`:ksi">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-03/src/main.rs}}
```

</Listing>

Tämä rakenne poistaa paljon sisäkkäisyyttä, joka olisi tarpeen, jos käyttäisit `loop`, `if`, `else` ja `break`, ja se on selkeämpi. Niin kauan kuin ehto evaluoituu `true`:ksi, koodi suoritetaan; muuten silmukasta poistutaan.

#### Kokoelman läpikäynti `for`-silmukalla

Voit valita käyttää `while`-rakennetta silmukan läpikäymiseen kokoelman elementtien yli, kuten taulukon. Esimerkiksi Listauksen 3-4 silmukka tulostaa jokaisen elementin taulukossa `a`.

<Listing number="3-4" file-name="src/main.rs" caption="Kokoelman jokaisen elementin läpikäynti `while`-silmukalla">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-04/src/main.rs}}
```

</Listing>

Tässä koodi laskee ylöspäin taulukon elementtien läpi. Se alkaa indeksistä `0` ja silmukoi, kunnes se saavuttaa taulukon viimeisen indeksin (eli kun `index < 5` ei enää ole `true`). Tämän koodin suorittaminen tulostaa jokaisen elementin taulukossa:

```console
{{#include ../listings/ch03-common-programming-concepts/listing-03-04/output.txt}}
```

Kaikki viisi taulukon arvoa ilmestyvät terminaaliin odotetusti. Vaikka `index` saavuttaa arvon `5` jossain vaiheessa, silmukka lopettaa suorittamisen ennen kuin yrittää hakea kuudetta arvoa taulukosta.

Tämä lähestymistapa on virhealtis; voisimme saada ohjelman panikoimaan, jos indeksiarvo tai testiehto on virheellinen. Esimerkiksi jos muuttaisit `a`-taulukon määritelmää sisältämään neljä elementtiä mutta unohtaisit päivittää ehdon `while index < 4`:ksi, koodi panikoisi. Se on myös hidas, koska kääntäjä lisää ajonaikaista koodia tarkistamaan jokaisella silmukan iteraatiolla, onko indeksi taulukon rajojen sisällä.

Tiiviimpänä vaihtoehtona voit käyttää `for`-silmukkaa ja suorittaa koodia jokaiselle kokoelman kohteelle. `for`-silmukka näyttää Listauksen 3-5 koodilta.

<Listing number="3-5" file-name="src/main.rs" caption="Kokoelman jokaisen elementin läpikäynti `for`-silmukalla">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-05/src/main.rs}}
```

</Listing>

Kun suoritamme tämän koodin, näemme saman tulosteen kuin Listauksessa 3-4. Tärkeämpää on, että olemme nyt lisänneet koodin turvallisuutta ja poistaneet bugien mahdollisuuden, jotka voisivat johtua taulukon lopun ylittämisestä tai liian vähäisestä etenemisestä ja joidenkin kohteiden ohittamisesta. Konekoodi, joka generoidaan `for`-silmukoista, voi myös olla tehokkaampaa, koska indeksiä ei tarvitse verrata taulukon pituuteen jokaisella iteraatiolla.

Käyttämällä `for`-silmukkaa sinun ei tarvitse muistaa muuttaa muuta koodia, jos muutat taulukon arvojen määrää, toisin kuin Listauksessa 3-4 käytetyllä menetelmällä.

`for`-silmukoiden turvallisuus ja tiiviys tekevät niistä yleisimmin käytetyn silmukkarakenteen Rustissa. Jopa tilanteissa, joissa haluat suorittaa koodia tietyn määrän kertoja, kuten Listauksen 3-3 `while`-silmukassa käytetyssä lähtölaskentaesimerkissä, useimmat Rustaceanit käyttäisivät `for`-silmukkaa. Tapa tehdä se olisi käyttää standardikirjaston tarjoamaa `Range`-tyyppiä, joka generoi kaikki numerot peräkkäin yhdestä numerosta toiseen numeroon asti.

Tässä on, miltä lähtölaskenta näyttäisi `for`-silmukalla ja toisella menetelmällä, josta emme ole vielä puhuneet, `rev`:llä kääntääksemme alueen:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-34-for-range/src/main.rs}}
```

Tämä koodi on hieman siistimpi, eikö?

## Yhteenveto

Sinä teit sen! Tämä oli laaja luku: Opit muuttujista, skaari- ja yhdistelmätietotyypeistä, funktioista, kommenteista, `if`-lausekkeista ja silmukoista! Harjoitellaksesi tässä luvussa käsiteltyjä käsitteitä, kokeile rakentaa ohjelmia, jotka:

- Muuntavat lämpötiloja Fahrenheit- ja Celsius-asteiden välillä.
- Generoivat *n*:nnen Fibonacci-luvun.
- Tulostavat joululaulun "The Twelve Days of Christmas" -laulun sanat hyödyntäen laulun toistoa.

Kun olet valmis jatkamaan, puhumme Rustin käsitteestä, jota _ei_ yleensä ole muissa ohjelmointikielissä: omistajuudesta.

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[quitting-after-a-correct-guess]: ch02-00-guessing-game-tutorial.html#quitting-after-a-correct-guess
