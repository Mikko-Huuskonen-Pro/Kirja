## Muuttujat ja muuttuvuus

Kuten mainittiin ["Arvojen tallentaminen muuttujilla"][storing-values-with-variables]<!-- ignore -->
-osiossa, muuttujat ovat oletuksena muuttumattomia. Tämä on yksi monista Rustin antamista vihjeistä
kirjoittaa koodia tavalla, joka hyödyntää Rustin tarjoamaa turvallisuutta ja helppoa rinnakkaisuutta.
Sinulla on kuitenkin edelleen mahdollisuus tehdä muuttujistasi muuttuvia. Tutkitaan, miten ja miksi
Rust kannustaa suosimaan muuttumattomuutta ja miksi joskus saatat haluta poiketa siitä.

Kun muuttuja on muuttumaton, kun arvo on sidottu nimeen, et voi muuttaa sitä arvoa. Havainnollistamiseksi
luo uusi projekti nimeltä _variables_ _projects_-kansioosi komennolla `cargo new variables`.

Avaa sitten uudessa _variables_-kansiossasi _src/main.rs_ ja korvaa sen koodi seuraavalla koodilla,
joka ei vielä käänny:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-01-variables-are-immutable/src/main.rs}}
```

Tallenna ja suorita ohjelma `cargo run` -komennolla. Sinun pitäisi saada virheilmoitus muuttumattomuusvirheestä,
kuten tässä tulosteessa:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-01-variables-are-immutable/output.txt}}
```

Tämä esimerkki näyttää, miten kääntäjä auttaa löytämään virheitä ohjelmissasi. Kääntäjävirheet voivat
olla turhauttavia, mutta todellisuudessa ne vain tarkoittavat, että ohjelmasi ei vielä turvallisesti
tee sitä, mitä haluat sen tekevän; ne _eivät_ tarkoita, ettet olisi hyvä ohjelmoija! Kokeneetkin
Rustaceanit saavat kääntäjävirheitä.

Sait virheilmoituksen `` cannot assign twice to immutable variable `x` `` koska yritit antaa toisen
arvon muuttumattomalle `x`-muuttujalle.

On tärkeää, että saamme käännösaikaisia virheitä, kun yritämme muuttaa arvoa, joka on merkitty
muuttumattomaksi, koska juuri tämä tilanne voi johtaa bugeihin. Jos yksi osa koodistamme toimii
olettaen, että arvo ei koskaan muutu, ja toinen osa koodistamme muuttaa sitä arvoa, on mahdollista,
että koodin ensimmäinen osa ei tee sitä, mitä se oli suunniteltu tekemään. Tällaisen bugin syy voi
olla vaikea jäljittää jälkikäteen, erityisesti kun koodin toinen osa muuttaa arvoa vain _joskus_.
Rust-kääntäjä takaa, että kun ilmoitat arvon olevan muuttumaton, se todella ei muutu, joten sinun
ei tarvitse seurata sitä itse. Koodisi on siten helpompi ymmärtää.

Mutta muuttuvuus voi olla hyvin hyödyllistä ja tehdä koodin kirjoittamisesta kätevämpää. Vaikka
muuttujat ovat oletuksena muuttumattomia, voit tehdä niistä muuttuvia lisäämällä `mut`-avainsanan
muuttujan nimen eteen, kuten teit [Luvussa 2][storing-values-with-variables]<!-- ignore -->. `mut`-avainsanan
lisääminen myös välittää aikomuksen koodin tuleville lukijoille osoittaen, että koodin muut osat
muuttavat tämän muuttujan arvoa.

Muutetaan esimerkiksi _src/main.rs_ seuraavaksi:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-02-adding-mut/src/main.rs}}
```

Kun suoritamme ohjelman nyt, saamme tämän:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-02-adding-mut/output.txt}}
```

Saamme muuttaa `x`:ään sidottua arvoa `5`:stä `6`:een, kun `mut` on käytössä. Lopulta päätös
muuttuvuuden käytöstä on sinun ja riippuu siitä, mikä on selkeintä kyseisessä tilanteessa.

<!-- Old headings. Do not remove or links may break. -->
<a id="constants"></a>

### Vakioiden julistaminen

Kuten muuttumattomat muuttujat, _vakiot_ ovat arvoja, jotka on sidottu nimeen eikä niitä saa muuttaa,
mutta vakioiden ja muuttujien välillä on muutamia eroja.

Ensinnäkin et saa käyttää `mut`-avainsanaa vakioiden kanssa. Vakiot eivät ole vain oletuksena
muuttumattomia—ne ovat aina muuttumattomia. Julistat vakiot `const`-avainsanalla `let`-avainsanan
sijaan, ja arvon tyyppi _täytyy_ annotoida. Käsittelemme tyyppejä ja tyyppiannotaatioita seuraavassa
osiossa ["Tietotyypit"][data-types]<!-- ignore -->, joten älä huoli yksityiskohdista vielä. Tiedä
vain, että sinun täytyy aina annotoida tyyppi.

Vakioita voidaan julistaa missä tahansa näkyvyysalueessa, mukaan lukien globaalissa näkyvyysalueessa,
mikä tekee niistä hyödyllisiä arvoille, jotka monien koodin osien tarvitsevat tietää.

Viimeinen ero on, että vakioille voidaan asettaa vain vakiolauseke, ei arvon tulos, joka voitaisiin
laskea vain ajonaikana.

Tässä on esimerkki vakion julistuksesta:

```rust
const THREE_HOURS_IN_SECONDS: u32 = 60 * 60 * 3;
```

Vakion nimi on `THREE_HOURS_IN_SECONDS`, ja sen arvo on 60 (sekuntien määrä minuutissa) kerrottuna
60:llä (minuuttien määrä tunnissa) kerrottuna 3:lla (tuntien määrä, jonka haluamme laskea tässä
ohjelmassa). Rustin nimeämiskäytäntö vakioille on käyttää kaikkia kirjaimia isoina ja alaviivoja
sanojen välissä. Kääntäjä pystyy arvioimaan rajoitetun joukon operaatioita käännösaikana, mikä
antaa meille mahdollisuuden kirjoittaa tämän arvon tavalla, joka on helpompi ymmärtää ja tarkistaa,
sen sijaan että asettaisimme vakion arvoksi 10 800. Katso [Rust Referencen osio vakioiden arvioinnista][const-eval]
lisätietoja siitä, mitä operaatioita voidaan käyttää vakioita julistaessa.

Vakiot ovat voimassa koko ohjelman ajon ajan niiden julistusalueella. Tämä ominaisuus tekee vakioista
hyödyllisiä sovellusalueesi arvoille, jotka useat ohjelman osat saattavat tarvita tietää, kuten
maksimipisteet, jotka mikä tahansa pelaaja voi ansaita, tai valon nopeus.

Kovakoodattujen arvojen nimeäminen vakioiksi koko ohjelmassasi on hyödyllistä välittääkseen arvon
merkityksen koodin tuleville ylläpitäjille. Se auttaa myös sillä, että sinun tarvitsee muuttaa
vain yhtä paikkaa koodissasi, jos kovakoodattua arvoa pitää päivittää tulevaisuudessa.

### Varjostaminen

Kuten näit arvauspeli-oppaassa [Luvussa 2][comparing-the-guess-to-the-secret-number]<!-- ignore -->,
voit julistaa uuden muuttujan samalla nimellä kuin aiempi muuttuja. Rustaceanit sanovat, että ensimmäinen
muuttuja _varjostetaan_ toisella, mikä tarkoittaa, että toinen muuttuja on se, jonka kääntäjä näkee,
kun käytät muuttujan nimeä. Käytännössä toinen muuttuja peittää ensimmäisen, ohjaten kaikki muuttujan
nimen käytöt itseensä, kunnes se itse varjostetaan tai näkyvyysalue päättyy. Voimme varjostaa muuttujan
käyttämällä samaa muuttujan nimeä ja toistamalla `let`-avainsanan käytön seuraavasti:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-03-shadowing/src/main.rs}}
```

Tämä ohjelma sitoo ensin `x`:n arvoon `5`. Sitten se luo uuden muuttujan `x` toistamalla `let x =`,
ottaen alkuperäisen arvon ja lisäten `1`, jolloin `x`:n arvo on `6`. Sitten sisäisessä näkyvyysalueessa,
joka luotiin aaltosulkeilla, kolmas `let`-lauseke varjostaa myös `x`:n ja luo uuden muuttujan,
kertomalla edellisen arvon kahdella antaakseen `x`:lle arvon `12`. Kun tämä näkyvyysalue päättyy,
sisäinen varjostaminen loppuu ja `x` palaa arvoon `6`. Kun suoritamme tämän ohjelman, se tulostaa
seuraavan:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-03-shadowing/output.txt}}
```

Varjostaminen eroaa muuttujan merkitsemisestä `mut`-avainsanalla, koska saamme käännösaikaisen
virheen, jos yritämme vahingossa antaa uuden arvon tälle muuttujalle käyttämättä `let`-avainsanaa.
Käyttämällä `let`-avainsanaa voimme suorittaa muutamia muunnoksia arvolle, mutta muuttuja on muuttumaton
näiden muunnosten jälkeen.

Toinen ero `mut`-avainsanan ja varjostamisen välillä on, että koska luomme käytännössä uuden muuttujan,
kun käytämme `let`-avainsanaa uudelleen, voimme muuttaa arvon tyyppiä mutta käyttää samaa nimeä.
Esimerkiksi ohjelmamme saattaa pyytää käyttäjää näyttämään, kuinka monta välilyöntiä hän haluaa
tekstin väliin syöttämällä välilyöntimerkkejä, ja sitten haluamme tallentaa tämän syötteen numerona:

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-04-shadowing-can-change-types/src/main.rs:here}}
```

Ensimmäinen `spaces`-muuttuja on merkkijonotyyppiä, ja toinen `spaces`-muuttuja on numerotyyppiä.
Varjostaminen säästää meidät keksimästä eri nimiä, kuten `spaces_str` ja `spaces_num`; sen sijaan
voimme käyttää uudelleen yksinkertaisempaa `spaces`-nimeä. Jos kuitenkin yritämme käyttää `mut`-avainsanaa
tähän, kuten tässä näytetään, saamme käännösaikaisen virheen:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-05-mut-cant-change-types/src/main.rs:here}}
```

Virhe sanoo, ettemme saa muuttaa muuttujan tyyppiä:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-05-mut-cant-change-types/output.txt}}
```

Nyt kun olemme tutkineet, miten muuttujat toimivat, katsotaan lisää tietotyyppejä, joita niillä voi olla.

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[data-types]: ch03-02-data-types.html#data-types
[storing-values-with-variables]: ch02-00-guessing-game-tutorial.html#storing-values-with-variables
[const-eval]: ../reference/const_eval.html
