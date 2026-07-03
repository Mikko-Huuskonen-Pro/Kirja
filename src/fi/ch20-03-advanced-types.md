## Edistyneet tyypit

Rustin tyyppijärjestelmässä on ominaisuuksia, joista olemme maininneet mutta joita emme ole vielä käsitelleet. Aloitamme käsittelemällä newtype-tyyppejä yleisesti ja tutkimalla, miksi ne ovat hyödyllisiä tyyppeinä. Siirrymme sitten tyyppialiasiin, ominaisuuteen, joka muistuttaa newtype-tyyppejä mutta hieman eri semantiikalla. Käsittelemme myös `!`-tyypin ja dynaamisesti mitoitetut tyypit.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-the-newtype-pattern-for-type-safety-and-abstraction"></a>

### Tyyppiturvallisuus ja abstraktio newtype-kuviolla

Tämä osio olettaa, että olet lukenut aiemman [”Ulkoisten traitien toteuttaminen newtype-kuviolla”][newtype]<!-- ignore --> -kohdan. Newtype-kuvio on hyödyllinen myös muissa tehtävissä kuin niissä, joita olemme tähän asti käsitelleet, mukaan lukien arvojen sekoittumisen estäminen staattisesti ja arvon yksiköiden ilmaiseminen. Näit esimerkin newtype-tyyppien käytöstä yksiköiden ilmaisemiseen listauksessa 20-16: muista, että `Millimeters`- ja `Meters`-rakenteet käärivät `u32`-arvot newtype-tyyppiin. Jos kirjoittaisimme funktion, jonka parametri on tyyppiä `Millimeters`, emme voisi kääntää ohjelmaa, joka yrittäisi vahingossa kutsua funktiota `Meters`- tai tavallisella `u32`-arvolla.

Voimme käyttää newtype-kuviota myös piilottaaksemme tyypin toteutuksen yksityiskohtia: uusi tyyppi voi tarjota julkisen API:n, joka eroaa sisäisen yksityisen tyypin API:sta.

Newtype-tyypit voivat myös piilottaa sisäisen toteutuksen. Esimerkiksi voisimme tarjota `People`-tyypin käärimään `HashMap<i32, String>`-rakenteen, joka tallentaa henkilön tunnuksen ja nimen. `People`-tyyppiä käyttävä koodi käyttäisi vain tarjoamaamme julkista API:a, kuten metodia nimen lisäämiseen `People`-kokoelmaan; koodin ei tarvitse tietää, että liitämme nimiin sisäisesti `i32`-tunnuksen. Newtype-kuvio on kevyt tapa saavuttaa kapselointi toteutuksen yksityiskohtien piilottamiseksi, josta puhuimme luvun 18 [”Toteutuksen yksityiskohdat piilottava kapselointi”][encapsulation-that-hides-implementation-details]<!-- ignore --> -kohdassa.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-type-synonyms-with-type-aliases"></a>

### Tyyppisynonyymit ja tyyppialiasit

Rust tarjoaa mahdollisuuden julistaa _tyyppialiasin_ antaakseen olemassa olevalle tyypille toisen nimen. Tätä varten käytämme `type`-avainsanaa. Esimerkiksi voimme luoda aliasin `Kilometers` tyypille `i32` näin:

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-04-kilometers-alias/src/main.rs:here}}
```

Nyt alias `Kilometers` on _synonyymi_ tyypille `i32`; toisin kuin listauksessa 20-16 luodut `Millimeters`- ja `Meters`-tyypit, `Kilometers` ei ole erillinen uusi tyyppi. `Kilometers`-tyypin arvoja käsitellään samoin kuin `i32`-tyypin arvoja:

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-04-kilometers-alias/src/main.rs:there}}
```

Koska `Kilometers` ja `i32` ovat sama tyyppi, voimme laskea yhteen molempien tyyppien arvoja ja välittää `Kilometers`-arvoja funktioille, jotka ottavat `i32`-parametreja. Tällä tavalla emme kuitenkaan saa tyyppitarkistuksen etuja, joita saamme aiemmin käsitellystä newtype-kuviosta. Toisin sanoen, jos sekoitamme `Kilometers`- ja `i32`-arvoja jossain, kääntäjä ei anna virhettä.

Tyyppisynonyymien pääasiallinen käyttötarkoitus on toiston vähentäminen. Esimerkiksi meillä voi olla pitkä tyyppi kuten tämä:

```rust,ignore
Box<dyn Fn() + Send + 'static>
```

Tämän pitkän tyypin kirjoittaminen funktiosignatuureissa ja tyyppimerkinnöissä koko koodissa voi olla työlästä ja virhealtista. Kuvittele projekti, joka on täynnä tällaista koodia kuten listauksessa 20-25.

<Listing number="20-25" caption="Pitkän tyypin käyttö monessa paikassa">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-25/src/main.rs:here}}
```

</Listing>

Tyyppialias tekee tästä koodista hallittavampaa vähentämällä toistoa. Listauksessa 20-26 olemme tuoneet aliasin nimeltä `Thunk` monimutkaiselle tyypille ja voimme korvata kaikki tyypin käytöt lyhyemmällä aliasilla `Thunk`.

<Listing number="20-26" caption="Tyyppialiasin `Thunk` käyttöönotto toiston vähentämiseksi">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-26/src/main.rs:here}}
```

</Listing>

Tätä koodia on paljon helpompi lukea ja kirjoittaa! Tyyppialiasille merkityksellisen nimen valinta auttaa myös viestimään aikomuksestasi (_thunk_ tarkoittaa koodia, joka arvioidaan myöhemmin, joten se on sopiva nimi tallennettavalle sulkeumalle).

Tyyppialiasit ovat myös yleisiä `Result<T, E>`-tyypin kanssa toiston vähentämiseksi. Harkitse standardikirjaston `std::io`-moduulia. I/O-operaatiot palauttavat usein `Result<T, E>`-tyypin käsitelläkseen tilanteita, joissa operaatiot eivät onnistu. Tässä kirjastossa on `std::io::Error`-rakenne, joka edustaa kaikkia mahdollisia I/O-virheitä. Monet `std::io`-moduulin funktiot palauttavat `Result<T, E>`-tyypin, jossa `E` on `std::io::Error`, kuten nämä `Write`-traitin funktiot:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-05-write-trait/src/lib.rs}}
```

`Result<..., Error>` toistuu paljon. Siksi `std::io`-moduulissa on tämä tyyppialiasin:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-06-result-alias/src/lib.rs:here}}
```

Koska tämä julistus on `std::io`-moduulissa, voimme käyttää täysin pätevää aliasia `std::io::Result<T>`; eli `Result<T, E>`-tyyppiä, jossa `E` on `std::io::Error`. `Write`-traitin funktiosignatuurit näyttävät lopulta tältä:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-06-result-alias/src/lib.rs:there}}
```

Tyyppialias auttaa kahdella tavalla: se helpottaa koodin kirjoittamista _ja_ tarjoaa yhtenäisen rajapinnan koko `std::io`-moduulissa. Koska se on alias, se on vain toinen `Result<T, E>`, mikä tarkoittaa, että voimme käyttää kaikkia `Result<T, E>`-tyypin metodeja sen kanssa sekä erityissyntaksia kuten `?`-operaattoria.

### Never-tyyppi, joka ei koskaan palaa

Rustissa on erityinen tyyppi nimeltä `!`, jota työteorian kielessä kutsutaan _tyhjäksi tyypiksi_, koska sillä ei ole arvoja. Kutsumme sitä mieluummin _never-tyypiksi_, koska se edustaa palautustyyppiä, kun funktio ei koskaan palaa. Tässä on esimerkki:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-07-never-type/src/lib.rs:here}}
```

Tämä koodi luetaan: ”funktio `bar` palauttaa never-tyypin.” Funktioita, jotka eivät koskaan palaavat, kutsutaan _hajautuviksi funktioiksi_. Emme voi luoda `!`-tyypin arvoja, joten `bar` ei voi koskaan palata.

Mutta mitä hyötyä on tyypistä, jonka arvoja ei voi koskaan luoda? Muista listauksen 2-5 koodi numeronarvauspelistä; olemme toistaneet osan siitä listauksessa 20-27.

<Listing number="20-27" caption="`match`-lauseke, jonka haara päättyy `continue`-lauseeseen">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-05/src/main.rs:ch19}}
```

</Listing>

Silloin ohitimme joitakin yksityiskohtia tässä koodissa. Luvun 6 [”`match`-ohjausrakenne”][the-match-control-flow-construct]<!-- ignore --> -kohdassa käsittelimme, että `match`-haarojen täytyy kaikkien palauttaa sama tyyppi. Esimerkiksi seuraava koodi ei toimi:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-08-match-arms-different-types/src/main.rs:here}}
```

Tässä koodissa `guess`-muuttujan tyypin pitäisi olla sekä kokonaisluku _että_ merkkijono, ja Rust vaatii, että `guess`-muuttujalla on vain yksi tyyppi. Mitä siis `continue` palauttaa? Miten saimme palauttaa `u32`-arvon yhdestä haarasta ja toisessa haarassa `continue`-lauseen listauksessa 20-27?

Kuten saatoit arvata, `continue`-lauseella on `!`-arvon tyyppi. Eli kun Rust laskee `guess`-muuttujan tyypin, se katsoo molemmat `match`-haarat: edellisessä arvo on `u32` ja jälkimmäisessä `!`-arvon tyyppi. Koska `!`-tyypillä ei voi koskaan olla arvoa, Rust päättelee, että `guess`-muuttujan tyyppi on `u32`.

Tätä käyttäytymistä kuvataan muodollisesti niin, että `!`-tyypin lausekkeet voidaan pakottaa mihin tahansa muuhun tyyppiin. Saamme päättää tämän `match`-haaran `continue`-lauseella, koska `continue` ei palauta arvoa; sen sijaan se siirtää ohjauksen silmukan alkuun, joten `Err`-tapauksessa emme koskaan sijoita arvoa `guess`-muuttujaan.

Never-tyyppi on hyödyllinen myös `panic!`-makron kanssa. Muista `unwrap`-funktio, jota kutsumme `Option<T>`-arvoilla saadaksemme arvon tai panikoidaksemme tämän määritelmän mukaisesti:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-09-unwrap-definition/src/lib.rs:here}}
```

Tässä koodissa tapahtuu sama kuin listauksen 20-27 `match`-lausekkeessa: Rust näkee, että `val` on tyyppiä `T` ja `panic!` on tyyppiä `!`, joten koko `match`-lausekkeen tulos on `T`. Tämä koodi toimii, koska `panic!` ei tuota arvoa; se lopettaa ohjelman. `None`-tapauksessa emme palauta arvoa `unwrap`-funktiosta, joten tämä koodi on kelvollinen.

Viimeinen lauseke, jolla on tyyppi `!`, on silmukka:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-10-loop-returns-never/src/main.rs:here}}
```

Tässä silmukka ei koskaan pääty, joten lausekkeen arvo on `!`. Tämä ei kuitenkaan pitäisi paikkaansa, jos sisällyttäisimme `break`-lauseen, koska silmukka päättyisi `break`-lauseeseen.

### Dynaamisesti mitoitetut tyypit ja `Sized`-trait

Rustin täytyy tietää tiettyjä yksityiskohtia tyypeistään, kuten kuinka paljon tilaa varata tietyn tyypin arvolle. Tämä jättää tyyppijärjestelmän yhden nurkan aluksi hieman hämmentäväksi: _dynaamisesti mitoitettujen tyyppien_ käsite. Joskus kutsutaan _DST-tyypeiksi_ tai _kokoon mitoittamattomiksi tyypeiksi_, nämä tyypit sallivat koodin kirjoittamisen arvoilla, joiden koon tiedämme vasta ajonaikana.

Syvennytään dynaamisesti mitoitetun tyypin `str` yksityiskohtiin, jota olemme käyttäneet koko kirjan ajan. Aivan oikein, ei `&str` vaan pelkkä `str` on DST. Monissa tapauksissa, kuten kun tallennamme käyttäjän syöttämää tekstiä, emme voi tietää merkkijonon pituutta ennen ajonaikaa. Tämä tarkoittaa, ettemme voi luoda `str`-tyyppistä muuttujaa emmekä ottaa `str`-tyyppistä argumenttia. Harkitse seuraavaa koodia, joka ei toimi:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-11-cant-create-str/src/main.rs:here}}
```

Rustin täytyy tietää, kuinka paljon muistia varata minkä tahansa tietyn tyypin arvolle, ja kaikkien saman tyypin arvojen täytyy käyttää saman verran muistia. Jos Rust sallisi tämän koodin kirjoittamisen, nämä kaksi `str`-arvoa tarvitsisivat saman verran tilaa. Niillä on kuitenkin eri pituudet: `s1` tarvitsee 12 tavua tallennustilaa ja `s2` tarvitsee 15. Siksi dynaamisesti mitoitetun tyypin muuttujaa ei voi luoda.

Mitä siis teemme? Tässä tapauksessa tiedät jo vastauksen: teemme `s1`:n ja `s2`:n tyypiksi merkkijonoviipaleen (`&str`) eikä `str`. Muista luvun 4 [”Merkkijonoviipaleet”][string-slices]<!-- ignore --> -kohdasta, että viipaleen tietorakenne tallentaa vain aloitusposition ja viipaleen pituuden. Vaikka `&T` on yksi arvo, joka tallentaa muistiosoitteen, jossa `T` sijaitsee, merkkijonoviipale on _kaksi_ arvoa: `str`:n osoite ja sen pituus. Näin ollen merkkijonoviipaleen arvon koon tiedämme käännösaikana: se on kaksi kertaa `usize`:n pituus. Eli tiedämme aina merkkijonoviipaleen koon riippumatta siitä, kuinka pitkä viipaleen viittaama merkkijono on. Yleisesti tämä on tapa, jolla dynaamisesti mitoitettuja tyyppejä käytetään Rustissa: niillä on ylimääräinen metatieto, joka tallentaa dynaamisen tiedon koon. Dynaamisesti mitoitettujen tyyppien kultainen sääntö on, että dynaamisesti mitoitettujen tyyppien arvot täytyy aina sijoittaa jonkinlaisen osoittimen taakse.

Voimme yhdistää `str`:n kaikenlaisiin osoittimiin: esimerkiksi `Box<str>` tai `Rc<str>`. Itse asiassa olet nähnyt tämän aiemmin, mutta eri dynaamisesti mitoitetulla tyypillä: traitit. Jokainen trait on dynaamisesti mitoitettu tyyppi, johon voimme viitata traitin nimellä. Luvun 18 [”Trait-olioiden käyttö yhteisen käyttäytymisen abstrahoimiseen”][using-trait-objects-to-abstract-over-shared-behavior]<!-- ignore --> -kohdassa mainitsimme, että traitien käyttämiseksi trait-olioina meidän täytyy sijoittaa ne osoittimen taakse, kuten `&dyn Trait` tai `Box<dyn Trait>` (`Rc<dyn Trait>` toimisi myös).

DST-tyyppien kanssa työskentelyyn Rust tarjoaa `Sized`-traitin määrittämään, tiedetäänkö tyypin koko käännösaikana. Tämä trait toteutetaan automaattisesti kaikelle, jonka koko tiedetään käännösaikana. Lisäksi Rust lisää implisiittisesti `Sized`-sidonnan jokaiseen geneeriseen funktioon. Eli geneerinen funktiomääritelmä kuten tämä:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-12-generic-fn-definition/src/lib.rs}}
```

käsitellään ikään kuin olisimme kirjoittaneet tämän:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-13-generic-implicit-sized-bound/src/lib.rs}}
```

Oletuksena geneeriset funktiot toimivat vain tyypeillä, joiden koko tunnetaan käännösaikana. Voit kuitenkin käyttää seuraavaa erityissyntaksia tämän rajoituksen lieventämiseksi:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-14-generic-maybe-sized/src/lib.rs}}
```

`?Sized`-trait-sidonta tarkoittaa ”`T` voi olla tai olla olematta `Sized`”, ja tämä merkintä ohittaa oletuksen, että geneeristen tyyppien täytyy olla koon tiedetty käännösaikana. `?Trait`-syntaksi tällä merkityksellä on saatavilla vain `Sized`-traitille, ei muille traitille.

Huomaa myös, että vaihdoimme `t`-parametrin tyypin `T`:stä `&T`:hen. Koska tyyppi ei välttämättä ole `Sized`, meidän täytyy käyttää sitä jonkinlaisen osoittimen kautta. Tässä tapauksessa valitsimme viitteen.

Seuraavaksi puhumme funktioista ja sulkeumista!

[encapsulation-that-hides-implementation-details]: ch18-01-what-is-oo.html#encapsulation-that-hides-implementation-details
[string-slices]: ch04-03-slices.html#string-slices
[the-match-control-flow-construct]: ch06-02-match.html#the-match-control-flow-construct
[using-trait-objects-to-abstract-over-shared-behavior]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[newtype]: ch20-02-advanced-traits.html#implementing-external-traits-with-the-newtype-pattern
