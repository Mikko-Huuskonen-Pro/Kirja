## Ohjausrakenne

Kyky suorittaa koodia riippuen siitä, onko ehto `true`, ja suorittaa koodia toistuvasti niin kauan
kuin ehto on `true`, ovat perusrakennuspalikoita useimmissa ohjelmointikielissä. Yleisimmät
rakenteet, joilla voit hallita Rust-koodin suorituksen kulkua, ovat `if`-lausekkeet ja silmukat.

### `if`-lausekkeet

`if`-lauseke antaa sinun haarauttaa koodiasi ehtojen perusteella. Annat ehdon ja määrität:
”Jos tämä ehto täyttyy, suorita tämä koodilohko. Jos ehto ei täyty, älä suorita tätä koodilohkoa.”

Luo uusi projekti nimeltä _branches_ hakemistoon _projects_ tutkiaksesi `if`-lauseketta. Syötä
tiedostoon _src/main.rs_ seuraava:

<span class="filename">Tiedostonimi: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-26-if-true/src/main.rs}}
```

Kaikki `if`-lausekkeet alkavat avainsanalla `if`, jota seuraa ehto. Tässä tapauksessa ehto
tarkistaa, onko muuttujan `number` arvo alle 5. Sijoitamme koodilohkon, joka suoritetaan, jos ehto
on `true`, heti ehdon jälkeen aaltosulkeiden sisään. `if`-lausekkeiden ehtoihin liittyviä
koodilohkoja kutsutaan joskus _haaroiksi_, aivan kuten `match`-lausekkeiden haaroja, joita
käsittelimme [”Arvauksen vertaaminen salaisuuteen”][comparing-the-guess-to-the-secret-number]<!--
ignore --> -osiossa luvussa 2.

Valinnaisesti voimme myös sisällyttää `else`-lausekkeen, minkä valitsimme tehdä tässä, antaaksemme
ohjelmalle vaihtoehtoisen koodilohkon suoritettavaksi, jos ehto evaluoituu arvoksi `false`. Jos et
anna `else`-lauseketta ja ehto on `false`, ohjelma vain ohittaa `if`-lohkon ja siirtyy seuraavaan
kohtaan.

Kokeile suorittaa tämä koodi; sinun pitäisi nähdä seuraava tuloste:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-26-if-true/output.txt}}
```

Kokeillaan muuttaa `number`-muuttujan arvoksi sellainen, joka tekee ehdosta `false`, ja katsotaan,
mitä tapahtuu:

```rust,ignore
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-27-if-false/src/main.rs:here}}
```

Suorita ohjelma uudelleen ja katso tuloste:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-27-if-false/output.txt}}
```

On myös syytä huomata, että tämän koodin ehdon _täytyy_ olla `bool`. Jos ehto ei ole `bool`, saamme
virheen. Kokeile esimerkiksi suorittaa seuraava koodi:

<span class="filename">Tiedostonimi: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-28-if-condition-must-be-bool/src/main.rs}}
```

`if`-ehto evaluoituu tällä kertaa arvoksi `3`, ja Rust antaa virheen:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-28-if-condition-must-be-bool/output.txt}}
```

Virhe osoittaa, että Rust odotti `bool`-tyyppiä mutta sai kokonaisluvun. Toisin kuin kielet kuten
Ruby ja JavaScript, Rust ei yritä automaattisesti muuntaa ei-totuusarvoisia tyyppejä totuusarvoiksi.
Sinun täytyy olla eksplisiittinen ja antaa `if`-lausekkeelle aina totuusarvo ehtona. Jos haluamme,
että `if`-koodilohko suoritetaan vain, kun luku ei ole yhtä suuri kuin `0`, voimme muuttaa
`if`-lausekkeen seuraavaksi:

<span class="filename">Tiedostonimi: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-29-if-not-equal-0/src/main.rs}}
```

Tämän koodin suorittaminen tulostaa `number was something other than zero`.

#### Useiden ehtojen käsittely `else if`-rakenteella

Voit käyttää useita ehtoja yhdistämällä `if`- ja `else`-lausekkeet `else if` -lausekkeeseen.
Esimerkiksi:

<span class="filename">Tiedostonimi: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-30-else-if/src/main.rs}}
```

Tällä ohjelmalla on neljä mahdollista polkua. Sen suorittamisen jälkeen sinun pitäisi nähdä
seuraava tuloste:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-30-else-if/output.txt}}
```

Kun tämä ohjelma suoritetaan, se tarkistaa jokaisen `if`-lausekkeen vuorollaan ja suorittaa ensimmäisen
rungon, jonka ehto evaluoituu arvoksi `true`. Huomaa, että vaikka 6 on jaollinen kahdella, emme näe
tulostetta `number is divisible by 2`, emmekä `number is not divisible by 4, 3, or 2` -tekstiä
`else`-lohkosta. Se johtuu siitä, että Rust suorittaa vain ensimmäisen `true`-ehdon lohkon, ja kun
se löytää sellaisen, se ei edes tarkista loput.

Liian monen `else if` -lausekkeen käyttö voi sotkea koodiasi, joten jos sinulla on useampi kuin yksi,
saatat haluta refaktoroida koodiasi. Luku 6 kuvaa tehokkaan Rustin haarautumisrakenteen nimeltä
`match` näitä tapauksia varten.

#### `if`-lausekkeen käyttö `let`-lauseessa

Koska `if` on lauseke, voimme käyttää sitä `let`-lauseen oikealla puolella sijoittaaksemme tuloksen
muuttujaan, kuten listauksessa 3-2.

<Listing number="3-2" file-name="src/main.rs" caption="`if`-lausekkeen tuloksen sijoittaminen muuttujaan">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-02/src/main.rs}}
```

</Listing>

Muuttuja `number` sidotaan arvoon `if`-lausekkeen tuloksen perusteella. Suorita tämä koodi nähdäksesi,
mitä tapahtuu:

```console
{{#include ../listings/ch03-common-programming-concepts/listing-03-02/output.txt}}
```

Muista, että koodilohkot evaluoituvat viimeiseen lausekkeeseensa, ja luvut itsessään ovat myös
lausekkeita. Tässä tapauksessa koko `if`-lausekkeen arvo riippuu siitä, mikä koodilohko suoritetaan.
Tämä tarkoittaa, että arvojen, joilla on potentiaalia olla tuloksia kustakin `if`-lausekkeen haarasta,
täytyy olla sama tyyppi; listauksessa 3-2 sekä `if`-haaran että `else`-haaran tulokset olivat
`i32`-kokonaislukuja. Jos tyypit eivät täsmää, kuten seuraavassa esimerkissä, saamme virheen:

<span class="filename">Tiedostonimi: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-31-arms-must-return-same-type/src/main.rs}}
```

Kun yritämme kääntää tämän koodin, saamme virheen. `if`- ja `else`-haaroilla on yhteensopimattomat
arvotyypit, ja Rust osoittaa tarkalleen, mistä ongelma löytyy ohjelmasta:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-31-arms-must-return-same-type/output.txt}}
```

`if`-lohkon lauseke evaluoituu kokonaisluvuksi, ja `else`-lohkon lauseke evaluoituu merkkijonoksi.
Tämä ei toimi, koska muuttujilla täytyy olla yksi tyyppi, ja Rustin täytyy tietää käännösaikana
varmasti, mikä tyyppi `number`-muuttujalla on. `number`-muuttujan tyypin tunteminen antaa kääntäjälle
mahdollisuuden varmistaa, että tyyppi on kelvollinen kaikkialla, missä käytämme `number`-muuttujaa.
Rust ei pystyisi tekemään sitä, jos `number`-muuttujan tyyppi määräytyisi vasta suorituksen aikana;
kääntäjä olisi monimutkaisempi ja antaisi vähemmän takeita koodista, jos sen täytyisi seurata useita
hypoteettisia tyyppejä mille tahansa muuttujalle.

### Toisto silmukoilla

On usein hyödyllistä suorittaa koodilohko useammin kuin kerran. Tätä tehtävää varten Rust tarjoaa
useita _silmukoita_, jotka suorittavat silmukan rungon sisällä olevan koodin loppuun ja alkavat
sitten heti alusta. Kokeillaksemme silmukoita luodaan uusi projekti nimeltä _loops_.

Rustissa on kolmenlaisia silmukoita: `loop`, `while` ja `for`. Kokeillaan kutakin.

#### Koodin toistaminen `loop`-silmukalla

`loop`-avainsana käskee Rustia suorittamaan koodilohkoa yhä uudelleen ikuisesti tai kunnes käsket
sitä eksplisiittisesti lopettamaan.

Esimerkkinä muuta _loops_-hakemiston _src/main.rs_-tiedosto näyttämään tältä:

<span class="filename">Tiedostonimi: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-loop/src/main.rs}}
```

Kun suoritamme tämän ohjelman, näemme `again!` tulostettuna yhä uudelleen, kunnes pysäytämme ohjelman
manuaalisesti. Useimmat terminaalit tukevat näppäinyhdistelmää <kbd>ctrl</kbd>-<kbd>c</kbd>
keskeyttääkseen ohjelman, joka on jumissa jatkuvassa silmukassa. Kokeile sitä:

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

Symboli `^C` edustaa kohtaa, jossa painoit <kbd>ctrl</kbd>-<kbd>c</kbd>. Saatat nähdä tai et näe
sanaa `again!` tulostettuna `^C`:n jälkeen riippuen siitä, missä kohdassa silmukkaa koodi oli, kun
se sai keskeytyssignaalin.

Onneksi Rust tarjoaa myös tavan poistua silmukasta koodilla. Voit sijoittaa `break`-avainsanan
silmukan sisään kertoaksesi ohjelmalle, milloin lopettaa silmukan suorittaminen. Muistathan, että
teimme tämän arvauspelissä [”Lopettaminen oikean arvauksen jälkeen”][quitting-after-a-correct-guess]<!-- ignore
--> -osiossa luvussa 2 poistuaksemme ohjelmasta, kun käyttäjä voitti pelin arvaamalla oikean luvun.

Käytimme myös `continue`-avainsanaa arvauspelissä, mikä silmukassa käskee ohjelmaa ohittamaan
jäljellä olevan koodin tässä silmukan iteraatiossa ja siirtymään seuraavaan iteraatioon.

#### Arvojen palauttaminen silmukoista

Yksi `loop`-silmukan käyttötarkoituksista on yrittää uudelleen operaatiota, jonka tiedät voivan
epäonnistua, kuten tarkistaa, onko säie suorittanut tehtävänsä. Saatat myös tarvita operaation
tuloksen välittämistä silmukasta muulle koodillesi. Voit tehdä tämän lisäämällä palautettavan arvon
`break`-lausekkeen jälkeen, jota käytät silmukan pysäyttämiseen; kyseinen arvo palautetaan silmukasta,
jotta voit käyttää sitä, kuten tässä näytetään:

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-33-return-value-from-loop/src/main.rs}}
```

Ennen silmukkaa määrittelemme muuttujan nimeltä `counter` ja alustamme sen arvoon `0`. Sitten
määrittelemme muuttujan nimeltä `result` pitämään silmukasta palautettavaa arvoa. Jokaisella
silmukan iteraatiolla lisäämme `1`:n `counter`-muuttujaan ja tarkistamme sitten, onko `counter`
yhtä suuri kuin `10`. Kun se on, käytämme `break`-avainsanaa arvolla `counter * 2`. Silmukan jälkeen
käytämme puolipistettä lopettaaksemme lauseen, joka sijoittaa arvon muuttujaan `result`. Lopuksi
tulostamme `result`-muuttujan arvon, joka tässä tapauksessa on `20`.

Voit myös `return`-palauttaa silmukan sisältä. Vaikka `break` poistuu vain nykyisestä silmukasta,
`return` poistuu aina nykyisestä funktiosta.

#### Silmukkaetiketit useiden silmukoiden erottamiseen

Jos sinulla on silmukoita silmukoiden sisällä, `break` ja `continue` koskevat kyseisen kohdan
sisintä silmukkaa. Voit valinnaisesti määrittää _silmukkaetiketin_ silmukalle, jota voit sitten
käyttää `break`- tai `continue`-avainsanojen kanssa määrittääksesi, että nämä avainsanat koskevat
merkittyä silmukkaa sisimmän silmukan sijaan. Silmukkaetikettien täytyy alkaa yksittäisellä
heittomerkillä. Tässä on esimerkki kahdesta sisäkkäisestä silmukasta:

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-5-loop-labels/src/main.rs}}
```

Ulompi silmukka on merkitty etiketillä `'counting_up`, ja se laskee ylöspäin 0:sta 2:een.
Sisempi silmukka ilman etikettiä laskee alaspäin 10:stä 9:ään. Ensimmäinen `break`, joka ei määritä
etikettiä, poistuu vain sisemmästä silmukasta. Lauseke `break 'counting_up;` poistuu ulommasta
silmukasta. Tämä koodi tulostaa:

```console
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-5-loop-labels/output.txt}}
```

#### Ehdolliset silmukat `while`-silmukalla

Ohjelman täytyy usein evaluoida ehtoa silmukan sisällä. Niin kauan kuin ehto on `true`, silmukka
suoritetaan. Kun ehto ei enää ole `true`, ohjelma kutsuu `break`-avainsanaa pysäyttäen silmukan.
On mahdollista toteuttaa tämänkaltainen käyttäytyminen yhdistelmällä `loop`-, `if`-, `else`- ja
`break`-rakenteita; voit kokeilla sitä nyt ohjelmassa, jos haluat. Tämä malli on kuitenkin niin
yleinen, että Rustissa on sisäänrakennettu kielen rakenne sille, nimeltä `while`-silmukka.
Listauksessa 3-3 käytämme `while`-silmukkaa silmukan suorittamiseen kolme kertaa, laskemalla
joka kerta alaspäin, ja tulostamme sitten viestin ja poistumme.

<Listing number="3-3" file-name="src/main.rs" caption="`while`-silmukan käyttö koodin suorittamiseen niin kauan kuin ehto on tosi">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-03/src/main.rs}}
```

</Listing>

Tämä rakenne poistaa paljon sisäkkäisyyttä, joka olisi tarpeen, jos käyttäisit `loop`-, `if`-,
`else`- ja `break`-rakenteita, ja se on selkeämpi. Niin kauan kuin ehto evaluoituu arvoksi `true`,
koodi suoritetaan; muuten silmukasta poistutaan.

#### Kokoelman läpikäynti `for`-silmukalla

Voit myös käyttää `while`-rakennetta kokoelman, kuten taulukon, elementtien läpikäyntiin.
Esimerkiksi listauksen 3-4 silmukka tulostaa jokaisen taulukon `a` elementin.

<Listing number="3-4" file-name="src/main.rs" caption="Kokoelman jokaisen elementin läpikäynti `while`-silmukalla">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-04/src/main.rs}}
```

</Listing>

Tässä koodi laskee taulukon elementtien läpi. Se alkaa indeksistä `0` ja silmukoi, kunnes se saavuttaa
taulukon viimeisen indeksin (eli kun `index < 5` ei enää ole `true`). Tämän koodin suorittaminen
tulostaa jokaisen taulukon elementin:

```console
{{#include ../listings/ch03-common-programming-concepts/listing-03-04/output.txt}}
```

Kaikki viisi taulukon arvoa ilmestyvät terminaaliin odotetusti. Vaikka `index` saavuttaa jossain
vaiheessa arvon `5`, silmukka lopettaa suorittamisen ennen kuin yrittää hakea kuudetta arvoa
taulukosta.

Tämä lähestymistapa on kuitenkin virhealtis; voisimme saada ohjelman panikoimaan, jos indeksiarvo
tai testiehto on virheellinen. Esimerkiksi jos muuttaisit taulukon `a` määrittelyä sisältämään neljä
elementtiä mutta unohtaisit päivittää ehdoksi `while index < 4`, koodi panikoisi. Se on myös hidas,
koska kääntäjä lisää suoritusaikaista koodia tarkistamaan jokaisella silmukan iteraatiolla, onko
indeksi taulukon rajojen sisällä.

Tiiviimpänä vaihtoehtona voit käyttää `for`-silmukkaa ja suorittaa koodia jokaiselle kokoelman
kohteelle. `for`-silmukka näyttää listauksen 3-5 koodilta.

<Listing number="3-5" file-name="src/main.rs" caption="Kokoelman jokaisen elementin läpikäynti `for`-silmukalla">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-05/src/main.rs}}
```

</Listing>

Kun suoritamme tämän koodin, näemme saman tulosteen kuin listauksessa 3-4. Tärkeämpää on, että olemme
nyt lisänneet koodin turvallisuutta ja poistaneet mahdollisuuden virheille, jotka voisivat johtua
taulukon lopun ylittämisestä tai liian vähäisestä etenemisestä ja joidenkin kohteiden ohittamisesta.

Käyttämällä `for`-silmukkaa sinun ei tarvitse muistaa muuttaa muuta koodia, jos muutat taulukon
arvojen määrää, toisin kuin listauksessa 3-4 käytetyllä menetelmällä.

`for`-silmukoiden turvallisuus ja tiiviys tekevät niistä yleisimmin käytetyn silmukkarakenteen
Rustissa. Jopa tilanteissa, joissa haluat suorittaa koodia tietyn määrän kertoja, kuten
lähtölaskennassa, joka käytti `while`-silmukkaa listauksessa 3-3, useimmat rustilaiset käyttäisivät
`for`-silmukkaa. Tapa tehdä se olisi käyttää vakiokirjaston tarjoamaa _Range_-tyyppiä, joka generoi
kaikki luvut peräkkäin yhdestä luvusta toiseen lukuun asti.

Tältä lähtölaskenta näyttäisi käyttäen `for`-silmukkaa ja toista menetelmää, josta emme ole vielä
puhuneet, `rev`-metodia, kääntääkseen alueen:

<span class="filename">Tiedostonimi: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-34-for-range/src/main.rs}}
```

Tämä koodi on hieman siistimpi, eikö olekin?

## Yhteenveto

Sinä teit sen! Tämä oli suuri luku: opit muuttujista, skaari- ja yhdistetyistä tietotyypeistä,
funktioista, kommenteista, `if`-lausekkeista ja silmukoista! Harjoitellaksesi tässä luvussa
käsittelemiämme käsitteitä kokeile rakentaa ohjelmia, jotka tekevät seuraavaa:

- Muuntavat lämpötiloja Fahrenheitin ja Celsiusin välillä.
- Generoivat *n*:nnen Fibonacci-luvun.
- Tulostavat joululaulun ”The Twelve Days of Christmas” sanat hyödyntäen laulun toistoa.

Kun olet valmis jatkamaan, puhumme Rustin käsitteestä, jota _ei_ yleensä ole muissa
ohjelmointikielissä: omistajuudesta.

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[quitting-after-a-correct-guess]: ch02-00-guessing-game-tutorial.html#quitting-after-a-correct-guess
