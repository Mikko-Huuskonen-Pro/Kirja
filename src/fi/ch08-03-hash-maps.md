## Avaimien tallentaminen liittyvine arvoineen hajautustaulukoissa

Viimeinen yleisistä kokoelmistamme on hajautustaulukko. Tyyppi `HashMap<K, V>` tallentaa avainten tyyppiä `K` olevien avainten ja arvojen tyyppiä `V` olevien arvojen välisen kuvauksen käyttämällä _hajautusfunktiota_, joka määrittää, miten nämä avaimet ja arvot sijoitetaan muistiin. Monet ohjelmointikielet tukevat tällaista tietorakennetta, mutta ne käyttävät usein eri nimeä, kuten _hash_, _map_, _object_, _hash table_, _dictionary_ tai _associative array_, mainitakseni muutamia.

Hajautustaulukot ovat hyödyllisiä, kun haluat hakea dataa ei indeksillä, kuten vektoreilla, vaan avaimella, joka voi olla minkä tahansa tyyppinen. Esimerkiksi pelissä voisit seurata kunkin joukkueen pistemäärää hajautustaulukossa, jossa jokainen avain on joukkueen nimi ja arvot ovat kunkin joukkueen pisteet. Joukkueen nimen perusteella voit hakea sen pistemäärän.

Käymme läpi hajautustaulukoiden perus-API:n tässä osiossa, mutta `HashMap<K, V>`:lle standardikirjaston määrittelemissä funktioissa piilee paljon muutakin hyödyllistä. Kuten aina, tarkista standardikirjaston dokumentaatio lisätietoja varten.

### Uuden hajautustaulukon luominen

Yksi tapa luoda tyhjä hajautustaulukko on käyttää `new`:ia ja lisätä elementtejä `insert`:illä. Listauksessa 8-20 seuraamme kahden joukkueen, joiden nimet ovat _Blue_ ja _Yellow_, pistemääriä. Blue-joukkue aloittaa 10 pisteellä ja Yellow-joukkue 50 pisteellä.

<Listing number="8-20" caption="Uuden hajautustaulukon luominen ja avainten ja arvojen lisääminen">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-20/src/main.rs:here}}
```

</Listing>

Huomaa, että meidän on ensin `use`:ttava `HashMap` standardikirjaston collections-osasta. Kolmesta yleisestä kokoelmastamme tämä on vähiten käytetty, joten sitä ei sisällytetä automaattisesti preludiin tuotuihin ominaisuuksiin. Hajautustaulukoilla on myös vähemmän tukea standardikirjastosta; ei ole esimerkiksi sisäänrakennettua makroa niiden rakentamiseen.

Kuten vektorit, hajautustaulukot tallentavat datansa kekoon. Tällä `HashMap`:illa on avaimia tyyppiä `String` ja arvoja tyyppiä `i32`. Kuten vektorit, hajautustaulukot ovat homogeenisia: kaikkien avainten on oltava samaa tyyppiä, ja kaikkien arvojen on oltava samaa tyyppiä.

### Hajautustaulukon arvojen käyttö

Voimme saada arvon hajautustaulukosta antamalla sen avaimen `get`-metodille, kuten listauksessa 8-21.

<Listing number="8-21" caption="Blue-joukkueen hajautustaulukkoon tallennetun pistemäärän käyttö">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-21/src/main.rs:here}}
```

</Listing>

Tässä `score`:lla on arvo, joka liittyy Blue-joukkueeseen, ja tulos on `10`. `get`-metodi palauttaa `Option<&V>`:n; jos hajautustaulukossa ei ole arvoa kyseiselle avaimelle, `get` palauttaa `None`:n. Tämä ohjelma käsittelee `Option`:in kutsumalla `copied`:ia saadakseen `Option<i32>`:n `Option<&i32>`:n sijaan, sitten `unwrap_or`:ia asettaakseen `score`:n nollaksi, jos `scores`:issa ei ole merkintää avaimelle.

Voimme käydä läpi jokaisen avain-arvo-parin hajautustaulukossa samalla tavalla kuin vektoreilla käyttämällä `for`-silmukkaa:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-03-iterate-over-hashmap/src/main.rs:here}}
```

Tämä koodi tulostaa jokaisen parin satunnaisessa järjestyksessä:

```text
Yellow: 50
Blue: 10
```

<!-- Old headings. Do not remove or links may break. -->

<a id="hash-maps-and-ownership"></a>

### Omistuksen hallinta hajautustaulukoissa

`Copy`-traitin toteuttaville tyypeille, kuten `i32`, arvot kopioidaan hajautustaulukkoon. Omistetuille arvoille, kuten `String`, arvot siirretään ja hajautustaulukko on niiden omistaja, kuten listauksessa 8-22 havainnollistetaan.

<Listing number="8-22" caption="Avainten ja arvojen omistajuuden hajautustaulukossa lisäämisen jälkeen">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-22/src/main.rs:here}}
```

</Listing>

Emme voi käyttää muuttujia `field_name` ja `field_value` sen jälkeen, kun ne on siirretty hajautustaulukkoon `insert`-kutsulla.

Jos lisäämme viittauksia arvoihin hajautustaulukkoon, arvoja ei siirretä hajautustaulukkoon. Arvojen, joihin viitteet osoittavat, on oltava kelvollisia vähintään niin kauan kuin hajautustaulukko on kelvollinen. Käsittelemme näitä ongelmia tarkemmin kohdassa [”Viittausten validointi elinaikoilla”][validating-references-with-lifetimes]<!-- ignore --> luvussa 10.

### Hajautustaulukon päivittäminen

Vaikka avain-arvo-parien määrä on kasvava, jokaisella yksilöllisellä avaimella voi olla vain yksi siihen liittyvä arvo kerrallaan (mutta ei päinvastoin: esimerkiksi sekä Blue- että Yellow-joukkueella voi olla arvo `10` tallennettuna `scores`-hajautustaulukkoon).

Kun haluat muuttaa dataa hajautustaulukossa, sinun on päätettävä, miten käsitellä tapaus, jossa avaimella on jo arvo. Voit korvata vanhan arvon uudella arvolla täysin sivuuttaen vanhan arvon. Voit pitää vanhan arvon ja jättää huomiotta uuden arvon, lisäten uuden arvon vain, jos avaimella _ei_ jo ole arvoa. Tai voit yhdistää vanhan arvon ja uuden arvon. Katsotaan, miten tehdä kukin näistä!

#### Arvon korvaaminen

Jos lisäämme avaimen ja arvon hajautustaulukkoon ja lisäämme sitten saman avaimen eri arvolla, avaimeen liittyvä arvo korvataan. Vaikka listauksen 8-23 koodi kutsuu `insert`:ia kahdesti, hajautustaulukossa on vain yksi avain-arvo-pari, koska lisäämme Blue-joukkueen avaimen arvon molemmilla kerroilla.

<Listing number="8-23" caption="Tiettyyn avaimeen tallennetun arvon korvaaminen">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-23/src/main.rs:here}}
```

</Listing>

Tämä koodi tulostaa `{"Blue": 25}`. Alkuperäinen arvo `10` on korvattu.

<!-- Old headings. Do not remove or links may break. -->

<a id="only-inserting-a-value-if-the-key-has-no-value"></a>

#### Avaimen ja arvon lisääminen vain, jos avaimella ei ole arvoa

On yleistä tarkistaa, onko tietyllä avaimella jo arvo hajautustaulukossa, ja sitten toimia seuraavasti: Jos avain on olemassa hajautustaulukossa, olemassa olevan arvon pitäisi pysyä ennallaan; jos avainta ei ole, lisää se ja sille arvo.

Hajautustaulukoilla on tähän erityinen API nimeltä `entry`, joka ottaa parametrina avaimen, jonka haluat tarkistaa. `entry`-metodin palautusarvo on enum nimeltä `Entry`, joka edustaa arvoa, joka saattaa olla olemassa tai ei. Oletetaan, että haluamme tarkistaa, onko Yellow-joukkueen avaimella arvo. Jos ei ole, haluamme lisätä arvon `50`, ja sama Blue-joukkueelle. `entry`-API:ta käyttäen koodi näyttää listaukselta 8-24.

<Listing number="8-24" caption="`entry`-metodin käyttö lisäämiseen vain, jos avaimella ei jo ole arvoa">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-24/src/main.rs:here}}
```

</Listing>

`Entry`:n `or_insert`-metodi on määritelty palauttamaan muuttuva viite vastaavan `Entry`-avaimen arvoon, jos kyseinen avain on olemassa, ja jos ei, se lisää parametrin uudeksi arvoksi tälle avaimelle ja palauttaa muuttuvan viitteen uuteen arvoon. Tämä tekniikka on paljon siistimpi kuin logiikan kirjoittaminen itse, ja lisäksi se toimii paremmin lainauskontrollerin kanssa.

Listauksen 8-24 koodin suorittaminen tulostaa `{"Yellow": 50, "Blue": 10}`. Ensimmäinen `entry`-kutsu lisää Yellow-joukkueen avaimen arvolla `50`, koska Yellow-joukkueella ei ole vielä arvoa. Toinen `entry`-kutsu ei muuta hajautustaulukkoa, koska Blue-joukkueella on jo arvo `10`.

#### Arvon päivittäminen vanhan arvon perusteella

Toinen yleinen käyttötapaus hajautustaulukoille on avaimen arvon hakeminen ja sen päivittäminen vanhan arvon perusteella. Esimerkiksi listaus 8-25 näyttää koodin, joka laskee, kuinka monta kertaa kukin sana esiintyy tekstissä. Käytämme hajautustaulukkoa, jossa sanat ovat avaimia, ja kasvatamme arvoa seurataksemme, kuinka monta kertaa olemme nähneet kyseisen sanan. Jos näemme sanan ensimmäistä kertaa, lisäämme ensin arvon `0`.

<Listing number="8-25" caption="Sanojen esiintymisten laskeminen hajautustaulukolla, joka tallentaa sanat ja laskurit">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-25/src/main.rs:here}}
```

</Listing>

Tämä koodi tulostaa `{"world": 2, "hello": 1, "wonderful": 1}`. Saatat nähdä samat avain-arvo-parit tulostettuna eri järjestyksessä: Muista kohdasta [”Hajautustaulukon arvojen käyttö”][access]<!-- ignore -->, että hajautustaulukon läpikäynti tapahtuu satunnaisessa järjestyksessä.

`split_whitespace`-metodi palauttaa iteraattorin aliviipaleista, jotka on erotettu välilyönneillä `text`:n arvosta. `or_insert`-metodi palauttaa muuttuvan viitteen (`&mut V`) määritellyn avaimen arvoon. Tässä tallennamme kyseisen muuttuvan viitteen `count`-muuttujaan, joten arvon asettamiseksi meidän on ensin dereferoitava `count` asteriskilla (`*`). Muuttuva viite poistuu laajuudesta `for`-silmukan lopussa, joten kaikki nämä muutokset ovat turvallisia ja lainaussääntöjen sallimia.

### Hajautusfunktiot

Oletuksena `HashMap` käyttää hajautusfunktiota nimeltä _SipHash_, joka voi tarjota vastustuskykyä hajautustaulukoihin liittyviä palvelunestohyökkäyksiä (DoS) vastaan[^siphash]<!-- ignore -->. Tämä ei ole nopein saatavilla oleva hajautusalgoritmi, mutta kompromissi paremman turvallisuuden ja suorituskyvyn laskun välillä on sen arvoinen. Jos profiloit koodisi ja huomaat, että oletushajautusfunktio on liian hidas tarkoituksiisi, voit vaihtaa toiseen funktioon määrittämällä eri hasherin. _Hasher_ on tyyppi, joka toteuttaa `BuildHasher`-traitin. Käsittelemme trait:eja ja niiden toteuttamista [luvussa 10][traits]<!-- ignore -->. Sinun ei välttämättä tarvitse toteuttaa omaa hasheria alusta; [crates.io](https://crates.io/)<!-- ignore --> -sivustolla on muiden Rust-käyttäjien jakamia kirjastoja, jotka tarjoavat hashereita toteuttaen monia yleisiä hajautusalgoritmeja.

[^siphash]: [https://en.wikipedia.org/wiki/SipHash](https://en.wikipedia.org/wiki/SipHash)

## Yhteenveto

Vektorit, merkkijonot ja hajautustaulukot tarjoavat paljon toiminnallisuutta, jota tarvitaan ohjelmissa, kun sinun on tallennettava, käytettävä ja muokattava dataa. Tässä on harjoituksia, joihin sinun pitäisi nyt olla valmis:

1. Annetulle kokonaislukulistalle käytä vektoria ja palauta mediaani (lajiteltuna arvo keskimmäisessä sijainnissa) ja moodi (arvo, joka esiintyy useimmin; hajautustaulukko on hyödyllinen tässä) listasta.
1. Muunna merkkijonot siansaksaksi. Jokaisen sanan ensimmäinen konsonantti siirretään sanan loppuun ja lisätään _ay_, joten _first_ muuttuu muotoon _irst-fay_. Vokaalilla alkaviin sanoihin lisätään loppuun _hay_ sen sijaan (_apple_ muuttuu muotoon _apple-hay_). Muista UTF-8-koodauksen yksityiskohdat!
1. Käyttämällä hajautustaulukkoa ja vektoreita luo tekstipohjainen käyttöliittymä, jonka avulla käyttäjä voi lisätä työntekijöiden nimiä osastoon yrityksessä; esimerkiksi ”Add Sally to Engineering” tai ”Add Amir to Sales.” Anna sitten käyttäjän hakea luettelo kaikista osaston henkilöistä tai kaikista yrityksen henkilöistä osastoittain, lajiteltuna aakkosjärjestykseen.

Standardikirjaston API-dokumentaatio kuvaa vektoreiden, merkkijonojen ja hajautustaulukoiden metodeja, jotka ovat hyödyllisiä näissä harjoituksissa!

Siirrymme monimutkaisempiin ohjelmiin, joissa operaatiot voivat epäonnistua, joten on täydellinen hetki käsitellä virheenkäsittelyä. Teemme sen seuraavaksi!

[validating-references-with-lifetimes]: ch10-03-lifetime-syntax.html#validating-references-with-lifetimes
[access]: #accessing-values-in-a-hash-map
[traits]: ch10-02-traits.html
