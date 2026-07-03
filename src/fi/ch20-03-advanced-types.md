## Kehittyneitä tyyppejä

Rustin tyyppijärjestelmässä on joitakin ominaisuuksia, joita olemme tähän asti maininneet, mutta joita emme ole vielä käsitelleet. Aloitamme käsittelemällä newtype-kuvioita yleisesti ja tarkastelemalla, miksi newtypet ovat hyödyllisiä tyyppeinä. Siirrymme sitten tyyppialiasseihin, ominaisuuteen, joka on samanlainen kuin newtypet mutta hieman erilaisella semantiikalla. Käsittelemme myös `!`-tyyppiä ja dynaamisesti kokoisia tyyppejä.

### Newtype-kuvion käyttäminen tyyppiturvallisuuteen ja abstraktioon

Tämä osio olettaa, että olet lukenut aiemman osion [”Newtype-mallin käyttö ulkoisten traitien toteuttamiseen ulkoisille tyypeille.”][using-the-newtype-pattern]<!--
ignore --> Newtype-kuvio on hyödyllinen myös tehtäviin, joita emme ole vielä käsitelleet, mukaan lukien arvojen sekoittumisen staattinen estäminen ja arvon yksiköiden ilmaiseminen. Näitä arvojen yksiköiden ilmaisemiseen liittyvää newtype-käyttöä esitettiin Listauksessa 20-16: muistathan, että `Millimeters`- ja `Meters`-rakenteet käärivät `u32`-arvot newtypeen. Jos kirjoittaisimme funktion, jonka parametrin tyyppi on `Millimeters`, emme voisi kääntää ohjelmaa, joka yrittäisi vahingossa kutsua kyseistä funktiota `Meters`-tyyppisellä arvolla tai pelkällä `u32`:lla.

Voimme käyttää newtype-kuviota myös piilottamaan tyypin toteutustietoja: uusi tyyppi voi tarjota julkisen rajapinnan, joka eroaa yksityisen sisätyypin rajapinnasta.

Newtypet voivat myös piilottaa sisäisen toteutuksen. Esimerkiksi voisimme tarjota `People`-tyypin käärimään `HashMap<i32, String>`-rakenteen, joka tallentaa henkilön tunnuksen liitettynä hänen nimeensä. `People`-tyyppiä käyttävä koodi vuorovaikuttaisi vain tarjoamamme julkisen rajapinnan kanssa, kuten metodin, joka lisää nimirivin `People`-kokoelmaan; kyseisen koodin ei tarvitsisi tietää, että liitämme nimiin sisäisesti `i32`-tunnuksen. Newtype-kuvio on kevyt tapa saavuttaa kapselointi toteutustietojen piilottamiseksi, josta käsittelimme [”Kapselointi, joka piilottaa toteutustiedot”][encapsulation-that-hides-implementation-details]<!--
ignore --> -osiossa Luvussa 18.

### Tyyppisynonyymien luominen tyyppialiasseilla

Rust tarjoaa mahdollisuuden julistaa _tyyppialiasin_ antaakseen olemassa olevalle tyypille toisen nimen. Tätä varten käytämme `type`-avainsanaa. Esimerkiksi voimme luoda aliasin `Kilometers` tyypille `i32` näin:

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-04-kilometers-alias/src/main.rs:here}}
```

Nyt alias `Kilometers` on _synonyymi_ tyypille `i32`; toisin kuin Listauksessa 20-16 luodut `Millimeters`- ja `Meters`-tyypit, `Kilometers` ei ole erillinen, uusi tyyppi. Arvoja, joiden tyyppi on `Kilometers`, käsitellään samalla tavalla kuin arvoja, joiden tyyppi on `i32`:

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-04-kilometers-alias/src/main.rs:there}}
```

Koska `Kilometers` ja `i32` ovat sama tyyppi, voimme laskea yhteen molempien tyyppien arvoja ja välittää `Kilometers`-arvoja funktioille, jotka ottavat `i32`-parametreja. Tällä menetelmällä emme kuitenkaan saa tyyppitarkistuksen etuja, joita saamme aiemmin käsitellystä newtype-kuviosta. Toisin sanoen, jos sekoitamme `Kilometers`- ja `i32`-arvoja jossakin, kääntäjä ei anna meille virhettä.

Tyyppisynonyymien pääasiallinen käyttötapaus on toiston vähentäminen. Esimerkiksi meillä saattaa olla pitkä tyyppi, kuten tämä:

```rust,ignore
Box<dyn Fn() + Send + 'static>
```

Tämän pitkän tyypin kirjoittaminen funktiomerkintöihin ja tyyppihuomautuksiin koko koodissa voi olla työlästä ja virhealtista. Kuvittele projekti, joka on täynnä Listauksen 20-25 kaltaista koodia.

<Listing number="20-25" caption="Pitkän tyypin käyttö monessa paikassa">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-25/src/main.rs:here}}
```

</Listing>

Tyyppialias tekee tästä koodista hallittavampaa vähentämällä toistoa. Listauksessa 20-26 olemme ottaneet käyttöön aliasin nimeltä `Thunk` pitkälle tyypille ja voimme korvata kaikki tyypin käytöt lyhyemmällä aliasilla `Thunk`.

<Listing number="20-26" caption="Tyyppialiasin `Thunk` käyttöönotto toiston vähentämiseksi">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-26/src/main.rs:here}}
```

</Listing>

Tätä koodia on paljon helpompi lukea ja kirjoittaa! Tyyppialiasille merkityksellisen nimen valitseminen voi auttaa myös viestimään aikomuksestasi (_thunk_ on sana koodille, joka arvioidaan myöhemmin, joten se on sopiva nimi tallennettavalle sulkeiselle).

Tyyppialiasseja käytetään myös yleisesti `Result<T, E>`-tyypin kanssa toiston vähentämiseksi. Harkitse standardikirjaston `std::io`-moduulia. I/O-operaatiot palauttavat usein `Result<T, E>`-tyypin käsitelläkseen tilanteita, joissa operaatiot eivät onnistu. Tässä kirjastossa on `std::io::Error`-rakenne, joka edustaa kaikkia mahdollisia I/O-virheitä. Monet `std::io`-moduulin funktioista palauttavat `Result<T, E>`-tyypin, jossa `E` on `std::io::Error`, kuten nämä `Write`-traitin funktiot:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-05-write-trait/src/lib.rs}}
```

`Result<..., Error>` toistuu paljon. Siksi `std::io`-moduulissa on tämä tyyppialiasjulistus:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-06-result-alias/src/lib.rs:here}}
```

Koska tämä julistus on `std::io`-moduulissa, voimme käyttää täysin määriteltyä aliasia `std::io::Result<T>`; eli `Result<T, E>`, jossa `E` on täytetty arvolla `std::io::Error`. `Write`-traitin funktiomerkinnät näyttävät lopulta tältä:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-06-result-alias/src/lib.rs:there}}
```

Tyyppialias auttaa kahdella tavalla: se tekee koodin kirjoittamisesta helpompaa _ja_ antaa meille yhtenäisen rajapinnan koko `std::io`-moduulissa. Koska se on alias, se on vain toinen `Result<T, E>`, mikä tarkoittaa, että voimme käyttää sen kanssa kaikkia `Result<T, E>`-tyypille toimivia metodeja sekä erityissyntaksia, kuten `?`-operaattoria.

### Never-tyyppi, joka ei koskaan palauta

Rustissa on erityinen tyyppi nimeltä `!`, joka tunnetaan tyypinteoriassa _tyhjänä tyypinä_, koska sillä ei ole arvoja. Kutsumme sitä mieluummin _never-tyypiksi_, koska se on paluutyypin paikalla, kun funktio ei koskaan palauta. Tässä esimerkki:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-07-never-type/src/lib.rs:here}}
```

Tämä koodi luetaan ”funktio `bar` palauttaa never”. Funktioita, jotka eivät koskaan palauta, kutsutaan _divergoiviksi funktioiksi_. Emme voi luoda arvoja tyypille `!`, joten `bar` ei voi koskaan palauttaa.

Mutta mitä hyötyä on tyypistä, jolle et voi koskaan luoda arvoja? Muista Listauksen 2-5 koodi, osa numeronarvailupelistä; olemme toistaneet osan siitä tässä Listauksessa 20-27.

<Listing number="20-27" caption="`match`, jossa haara päättyy `continue`en">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-05/src/main.rs:ch19}}
```

</Listing>

Tuolloin ohitimme tässä koodissa joitakin yksityiskohtia. [”`match`-ohjausrakenne”][the-match-control-flow-operator]<!-- ignore --> -osiossa Luvussa 6 käsittelimme, että `match`-haarojen on kaikkien palautettava sama tyyppi. Esimerkiksi seuraava koodi ei toimi:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-08-match-arms-different-types/src/main.rs:here}}
```

Muuttujan `guess` tyypin tässä koodissa pitäisi olla kokonaisluku _ja_ merkkijono, ja Rust vaatii, että `guess`illä on vain yksi tyyppi. Mitä `continue` sitten palauttaa? Miten saimme palauttaa `u32`:n yhdestä haarasta ja toisessa haarassa Listauksessa 20-27 päättyä `continue`en?

Kuten saatoit arvata, `continue`lla on `!`-arvo. Eli kun Rust laskee muuttujan `guess` tyypin, se katsoo molempia match-haaroja, joista ensimmäisessä on `u32`-arvo ja jälkimmäisessä `!`-arvo. Koska `!` ei voi koskaan saada arvoa, Rust päättää, että `guess`in tyyppi on `u32`.

Tämän käyttäytymisen muodollinen kuvaus on, että `!`-tyyppiset lausekkeet voidaan pakottaa mihin tahansa muuhun tyyppiin. Saamme päättää tämän `match`-haaran `continue`lla, koska `continue` ei palauta arvoa; sen sijaan se siirtää ohjauksen takaisin silmukan alkuun, joten `Err`-tapauksessa emme koskaan anna arvoa muuttujalle `guess`.

Never-tyyppi on hyödyllinen myös `panic!`-makron kanssa. Muista `unwrap`-funktio, jota kutsumme `Option<T>`-arvoilla tuottaaksemme arvon tai panikoidaksemme tällä määritelmällä:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-09-unwrap-definition/src/lib.rs:here}}
```

Tässä koodissa tapahtuu sama kuin Listauksen 20-27 `match`issa: Rust näkee, että `val`illa on tyyppi `T` ja `panic!`illa on tyyppi `!`, joten koko `match`-lausekkeen tulos on `T`. Tämä koodi toimii, koska `panic!` ei tuota arvoa; se lopettaa ohjelman. `None`-tapauksessa emme palauta arvoa `unwrap`ista, joten tämä koodi on kelvollinen.

Yksi viimeinen lauseke, jolla on tyyppi `!`, on `loop`:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-10-loop-returns-never/src/main.rs:here}}
```

Tässä silmukka ei koskaan pääty, joten `!` on lausekkeen arvo. Tämä ei kuitenkaan pitäisi paikkaansa, jos sisällyttäisimme `break`in, koska silmukka päättyisi, kun se saavuttaisi `break`in.

### Dynaamisesti kokoiset tyypit ja `Sized`-trait

Rustin täytyy tietää tiettyjä yksityiskohtia tyypeistään, kuten kuinka paljon tilaa varata tietyn tyypin arvolle. Tämä jättää tyyppijärjestelmän yhden nurkan aluksi hieman hämmentäväksi: _dynaamisesti kokoisten tyyppien_ käsite. Joskus _DST:iksi_ tai _kokoon mitoittamattomiksi tyypeiksi_ kutsuttujen tyyppien avulla voimme kirjoittaa koodia käyttäen arvoja, joiden koon tiedämme vasta ajonaikana.

Syvennytään dynaamisesti kokoisen tyypin nimeltä `str` yksityiskohtiin, jota olemme käyttäneet koko kirjassa. Aivan oikein, ei `&str`, vaan pelkkä `str` on DST. Emme voi tietää, kuinka pitkä merkkijono on, ennen ajonaikaa, mikä tarkoittaa, että emme voi luoda muuttujaa tyypille `str`, emmekä voi ottaa parametria tyypille `str`. Harkitse seuraavaa koodia, joka ei toimi:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-11-cant-create-str/src/main.rs:here}}
```

Rustin täytyy tietää, kuinka paljon muistia varata mille tahansa tietyn tyypin arvolle, ja kaikkien tietyn tyypin arvojen on käytettävä samaa määrää muistia. Jos Rust sallisi tämän koodin kirjoittamisen, nämä kaksi `str`-arvoa pitäisi viedä saman verran tilaa. Mutta niillä on eri pituudet: `s1` tarvitsee 12 tavua tallennustilaa ja `s2` tarvitsee 15. Siksi dynaamisesti kokoisen tyypin arvoa sisältävää muuttujaa ei voi luoda.

Mitä teemme siis? Tässä tapauksessa tiedät jo vastauksen: teemme `s1`:n ja `s2`:n tyypeistä `&str` eikä `str`. Muista [”Merkkijonoviipaleet”][string-slices]<!-- ignore --> -osio Luvusta 4, jossa viipalerakenne tallentaa vain viipaleen aloitusposition ja pituuden. Vaikka `&T` on yksittäinen arvo, joka tallentaa muistiosoitteen, jossa `T` sijaitsee, `&str` on _kaksi_ arvoa: `str`:n osoite ja sen pituus. Näin voimme tietää `&str`-arvon koon käännösaikana: se on kaksi kertaa `usize`:n pituus. Eli tiedämme aina `&str`:n koon riippumatta siitä, kuinka pitkä sen viittaama merkkijono on. Yleisesti ottaen näin dynaamisesti kokoisia tyyppejä käytetään Rustissa: niillä on ylimääräinen metatieto, joka tallentaa dynaamisen tiedon koon. Dynaamisesti kokoisten tyyppien kultainen sääntö on, että dynaamisesti kokoisten tyyppien arvot on aina sijoitettava jonkinlaisen osoittimen taakse.

Voimme yhdistää `str`:n kaikenlaisiin osoittimiin: esimerkiksi `Box<str>` tai `Rc<str>`. Itse asiassa olet nähnyt tämän aiemmin, mutta eri dynaamisesti kokoisella tyypillä: traitit. Jokainen trait on dynaamisesti kokoinen tyyppi, johon voimme viitata traitin nimellä. [”Trait-objektien käyttö, jotka sallivat eri tyyppisten arvojen käytön”][using-trait-objects-that-allow-for-values-of-different-types]<!-- ignore
--> -osiossa Luvussa 18 mainitsimme, että käyttääksemme traitteja trait-objekteina meidän on sijoitettava ne osoittimen taakse, kuten `&dyn Trait` tai `Box<dyn Trait>` (`Rc<dyn Trait>` toimisi myös).

DST:iden kanssa työskentelyyn Rust tarjoaa `Sized`-traitin määrittämään, tiedetäänkö tyypin koko käännösaikana. Tämä trait toteutetaan automaattisesti kaikelle, jonka koko tiedetään käännösaikana. Lisäksi Rust lisää implisiittisesti `Sized`-rajoituksen jokaiseen geneeriseen funktioon. Eli geneerinen funktiomäärittely, kuten tämä:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-12-generic-fn-definition/src/lib.rs}}
```

käsitellään itse asiassa ikään kuin olisimme kirjoittaneet tämän:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-13-generic-implicit-sized-bound/src/lib.rs}}
```

Oletusarvoisesti geneeriset funktiot toimivat vain tyypeillä, joiden koko tunnetaan käännösaikana. Voit kuitenkin käyttää seuraavaa erityissyntaksia tämän rajoituksen lieventämiseksi:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-14-generic-maybe-sized/src/lib.rs}}
```

`?Sized`-traitrajoitus tarkoittaa ”`T` voi olla tai olla olematta `Sized`”, ja tämä merkintä ohittaa oletuksen, että geneeristen tyyppien on oltava tunnetun kokoisia käännösaikana. `?Trait`-syntaksi tällä merkityksellä on käytettävissä vain `Sized`-traitille, ei millekään muulle traitille.

Huomaa myös, että vaihdoimme parametrin `t` tyypin `T`:stä `&T`:hen. Koska tyyppi ei välttämättä ole `Sized`, meidän täytyy käyttää sitä jonkinlaisen osoittimen taakse. Tässä tapauksessa olemme valinneet viitteen.

Seuraavaksi puhumme funktioista ja sulkeisista!

[encapsulation-that-hides-implementation-details]: ch18-01-what-is-oo.html#encapsulation-that-hides-implementation-details
[string-slices]: ch04-03-slices.html#string-slices
[the-match-control-flow-operator]: ch06-02-match.html#the-match-control-flow-operator
[using-trait-objects-that-allow-for-values-of-different-types]: ch18-02-trait-objects.html#using-trait-objects-that-allow-for-values-of-different-types
[using-the-newtype-pattern]: ch20-02-advanced-traits.html#using-the-newtype-pattern-to-implement-external-traits-on-external-types
