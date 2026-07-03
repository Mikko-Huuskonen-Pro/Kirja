## Funktiot

Funktiot ovat yleisiä Rust-koodissa. Olet jo nähnyt yhden tärkeimmistä kielen funktioista: `main`-funktion, joka on monien ohjelmien käynnistyspiste. Olet myös nähnyt `fn`-avainsanan, jonka avulla voit julistaa uusia funktioita.

Rust-koodi käyttää _käärmeenpolku-tyyliä_ (_snake case_) funktioiden ja muuttujien nimien perinteisenä tyylinä, jossa kaikki kirjaimet ovat pieniä ja alaviivat erottavat sanat. Tässä on ohjelma, joka sisältää esimerkin funktion määrittelystä:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-16-functions/src/main.rs}}
```

Määrittelemme funktion Rustissa kirjoittamalla `fn` ja sen jälkeen funktion nimen ja joukon sulkeita. Aaltosulkeet kertovat kääntäjälle, missä funktion runko alkaa ja päättyy.

Voimme kutsua mitä tahansa määrittelemäämme funktiota kirjoittamalla sen nimen ja joukon sulkeita. Koska `another_function` on määritelty ohjelmassa, sitä voidaan kutsua `main`-funktion sisältä. Huomaa, että määrittelimme `another_function`-funktion _main_-funktion _jälkeen_ lähdekoodissa; olisimme voineet määritellä sen ennenkin. Rust ei välitä, missä määrittelet funktiosi, vain siitä, että ne on määritelty jossakin näkyvyysalueessa, jonka kutsuja näkee.

Aloitetaan uusi binääriprojekti nimeltä _functions_ tutkiaksemme funktioita tarkemmin. Sijoita `another_function`-esimerkki _src/main.rs_-tiedostoon ja suorita se. Sinun pitäisi nähdä seuraava tuloste:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-16-functions/output.txt}}
```

Rivit suoritetaan siinä järjestyksessä, jossa ne esiintyvät `main`-funktiossa. Ensin "Hello, world!" -viesti tulostetaan, sitten `another_function` kutsutaan ja sen viesti tulostetaan.

### Parametrit

Voimme määritellä funktioita, joilla on _parametreja_, jotka ovat erityisiä muuttujia, jotka ovat osa funktion allekirjoitusta. Kun funktiolla on parametreja, voit antaa sille konkreettisia arvoja näille parametreille. Teknisesti konkreettisia arvoja kutsutaan _argumenteiksi_, mutta arkikeskusteluissa ihmiset käyttävät usein sanoja _parametri_ ja _argumentti_ vaihdellen joko funktion määritelmän muuttujille tai konkreettisille arvoille, jotka välitetään funktiota kutsuttaessa.

Tässä versiossa `another_function`-funktiosta lisäämme parametrin:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-17-functions-with-parameters/src/main.rs}}
```

Kokeile suorittaa tämä ohjelma; sinun pitäisi saada seuraava tuloste:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-17-functions-with-parameters/output.txt}}
```

`another_function`-funktion julistuksessa on yksi parametri nimeltä `x`. `x`:n tyyppi on määritelty `i32`:ksi. Kun välitämme `5`:n `another_function`-funktiolle, `println!`-makro asettaa `5`:n muotoilumerkkijonon aaltosulkeisiin, jotka sisältävät `x`:n.

Funktion allekirjoituksissa sinun _täytyy_ julistaa kunkin parametrin tyyppi. Tämä on tarkoituksellinen päätös Rustin suunnittelussa: Tyyppiannotaatioiden vaatiminen funktioiden määritelmissä tarkoittaa, että kääntäjä tuskin koskaan tarvitsee sinua käyttämään niitä muualla koodissa selvittääkseen, mitä tyyppiä tarkoitat. Kääntäjä pystyy myös antamaan hyödyllisempiä virheilmoituksia, jos se tietää, mitä tyyppejä funktio odottaa.

Kun määrittelet useita parametreja, erota parametrijulistukset pilkuilla, näin:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-18-functions-with-multiple-parameters/src/main.rs}}
```

Tämä esimerkki luo funktion nimeltä `print_labeled_measurement` kahdella parametrilla. Ensimmäinen parametri on nimeltä `value` ja on `i32`. Toinen on nimeltä `unit_label` ja on tyyppiä `char`. Funktio tulostaa sitten tekstiä, joka sisältää sekä `value`- että `unit_label`-arvot.

Kokeillaan suorittaa tämä koodi. Korvaa _functions_-projektisi _src/main.rs_-tiedoston ohjelma edellä olevalla esimerkillä ja suorita se `cargo run` -komennolla:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-18-functions-with-multiple-parameters/output.txt}}
```

Koska kutsuimme funktiota arvolla `5` `value`-parametrille ja `'h'` `unit_label`-parametrille, ohjelman tuloste sisältää nämä arvot.

### Lausekkeet ja lauseet

Funktioiden rungot koostuvat sarjasta lauseita, jotka valinnaisesti päättyvät lausekkeeseen. Tähän mennessä käsittelemämme funktiot eivät ole sisältäneet päättyvää lauseketta, mutta olet nähnyt lausekkeen osana lausetta. Koska Rust on lausekepohjainen kieli, tämä on tärkeä ero ymmärtää. Muissa kielissä ei ole samoja erotteluja, joten katsotaan, mitä lauseet ja lausekkeet ovat ja miten niiden erot vaikuttavat funktioiden runkoihin.

- _Lauseet_ ovat ohjeita, jotka suorittavat jonkin toiminnon eivätkä palauta arvoa.
- _Lausekkeet_ evaluoituvat tulosarvoksi.

Katsotaan joitakin esimerkkejä.

Olemme itse asiassa jo käyttäneet lauseita ja lausekkeita. Muuttujan luominen ja arvon antaminen sille `let`-avainsanalla on lause. Listauksessa 3-1 `let y = 6;` on lause.

<Listing number="3-1" file-name="src/main.rs" caption="`main`-funktion julistus, joka sisältää yhden lauseen">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-01/src/main.rs}}
```

</Listing>

Funktioiden määritelmät ovat myös lauseita; koko edellinen esimerkki on itsessään lause. (Kuten näemme pian, funktion kutsuminen ei ole lause, vaikka se olisikin.)

Lauseet eivät palauta arvoja. Siksi et voi sijoittaa `let`-lausetta toiseen muuttujaan, kuten seuraava koodi yrittää; saat virheen:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-19-statements-vs-expressions/src/main.rs}}
```

Kun suoritat tämän ohjelman, saamasi virhe näyttää tältä:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-19-statements-vs-expressions/output.txt}}
```

`let y = 6` -lause ei palauta arvoa, joten `x`:llä ei ole mitään, mihin sitoutua. Tämä eroaa siitä, mitä tapahtuu muissa kielissä, kuten C:ssä ja Rubyssä, joissa sijoitus palauttaa sijoituksen arvon. Näissä kielissä voit kirjoittaa `x = y = 6` ja molemmilla `x`:llä ja `y`:llä on arvo `6`; näin ei ole Rustissa.

Lausekkeet evaluoituvat arvoksi ja muodostavat suurimman osan muusta koodista, jonka kirjoitat Rustissa. Harkitse matemaattista operaatiota, kuten `5 + 6`, joka on lauseke, joka evaluoituu arvoksi `11`. Lausekkeet voivat olla osa lauseita: Listauksessa 3-1 `6` lauseessa `let y = 6;` on lauseke, joka evaluoituu arvoksi `6`. Funktion kutsuminen on lauseke. Makron kutsuminen on lauseke. Uusi näkyvyysalueen lohko, joka luodaan aaltosulkeilla, on lauseke, esimerkiksi:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-20-blocks-are-expressions/src/main.rs}}
```

Tämä lauseke:

```rust,ignore
{
    let x = 3;
    x + 1
}
```

on lohko, joka tässä tapauksessa evaluoituu arvoksi `4`. Tämä arvo sidotaan `y`:hyn osana `let`-lausetta. Huomaa `x + 1` -rivi ilman puolipistettä lopussa, toisin kuin useimmat tähän mennessä näkemäsi rivit. Lausekkeet eivät sisällä päättyvää puolipistettä. Jos lisäät puolipisteen lausekkeen loppuun, muutat sen lauseeksi, eikä se sitten palauta arvoa. Pidä tämä mielessä, kun tutkit funktioiden paluuarvoja ja lausekkeita seuraavaksi.

### Funktiot paluuarvoilla

Funktiot voivat palauttaa arvoja koodille, joka kutsuu niitä. Emme nimeä paluuarvoja, mutta meidän täytyy julistaa niiden tyyppi nuolen (`->`) jälkeen. Rustissa funktion paluuarvo on synonyymi funktion rungon lohkon viimeisen lausekkeen arvolle. Voit palata aikaisin funktiosta `return`-avainsanalla ja määrittämällä arvon, mutta useimmat funktiot palauttavat viimeisen lausekkeen implisiittisesti. Tässä on esimerkki funktiosta, joka palauttaa arvon:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-21-function-return-values/src/main.rs}}
```

`five`-funktiossa ei ole funktiokutsuja, makroja eikä edes `let`-lauseita—vain numero `5` itsestään. Se on täysin kelvollinen funktio Rustissa. Huomaa, että funktion paluutyyppi on myös määritelty `-> i32`:ksi. Kokeile suorittaa tämä koodi; tulosteen pitäisi näyttää tältä:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-21-function-return-values/output.txt}}
```

`5` `five`-funktiossa on funktion paluuarvo, minkä vuoksi paluutyyppi on `i32`. Tarkastellaan tätä tarkemmin. Kaksi tärkeää asiaa: Ensinnäkin rivi `let x = five();` osoittaa, että käytämme funktion paluuarvoa muuttujan alustamiseen. Koska `five`-funktio palauttaa `5`:n, tämä rivi on sama kuin seuraava:

```rust
let x = 5;
```

Toiseksi `five`-funktiolla ei ole parametreja ja se määrittelee paluuarvon tyypin, mutta funktion runko on yksinäinen `5` ilman puolipistettä, koska se on lauseke, jonka arvon haluamme palauttaa.

Katsotaan toista esimerkkiä:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-22-function-parameter-and-return/src/main.rs}}
```

Tämän koodin suorittaminen tulostaa `The value of x is: 6`. Mutta mitä tapahtuu, jos laitamme puolipisteen rivin loppuun, joka sisältää `x + 1`, muuttaen sen lausekkeesta lauseeksi?

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-23-statements-dont-return-values/src/main.rs}}
```

Tämän koodin kääntäminen tuottaa virheen seuraavasti:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-23-statements-dont-return-values/output.txt}}
```

Päävirheilmoitus `mismatched types` paljastaa tämän koodin ydinongelman. `plus_one`-funktion määritelmä sanoo, että se palauttaa `i32`:n, mutta lauseet eivät evaluoidu arvoksi, mikä ilmaistaan `()`:lla, yksikkötyypillä. Siksi mitään ei palauteta, mikä on ristiriidassa funktion määritelmän kanssa ja johtaa virheeseen. Tässä tulosteessa Rust tarjoaa viestin, joka saattaa auttaa korjaamaan ongelman: Se ehdottaa puolipisteen poistamista, mikä korjaisi virheen.
