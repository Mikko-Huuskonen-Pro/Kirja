<!-- Old headings. Do not remove or links may break. -->

<a id="the-match-control-flow-operator"></a>

## `match`-ohjausrakenne

Rustissa on erittäin tehokas ohjausrakenne nimeltä `match`, jonka avulla voit verrata arvoa sarjaan kuvioita ja suorittaa sitten koodia sen perusteella, mikä
kuvio täsmää. Kuviot voivat koostua kirjaimellisista arvoista, muuttujien nimistä, jokerimerkeistä ja monista muista asioista; [Luku
19][ch19-00-patterns]<!-- ignore --> käsittelee kaikki erilaiset kuviotyypit ja niiden toiminnan. `match`-lausekkeen voima tulee kuvioiden ilmaisukyvystä
ja siitä, että kääntäjä varmistaa kaikkien mahdollisten tapausten käsitellyn.

Voit ajatella `match`-lauseketta kolikonlajittelukoneena: kolikot liukuvat radalla, jossa on erikokoisia reikiä, ja jokainen kolikko putoaa ensimmäiseen
reikään, johon se mahtuu. Samalla tavalla arvot käyvät läpi `match`-lausekkeen jokaisen kuvion, ja ensimmäiseen kuvioon, johon arvo ”mahtuu”, arvo putoaa
liittyvään koodilohkoon suoritusta varten.

Puhutaanpa kolikoista — käytetään niitä esimerkkinä `match`-lausekkeen kanssa! Voimme kirjoittaa funktion, joka ottaa tuntemattoman Yhdysvaltain kolikon ja
määrittää samankaltaisella tavalla kuin laskuri, mikä kolikko se on, ja palauttaa sen arvon senteissä, kuten Listauksessa 6-3 on esitetty.

<Listing number="6-3" caption="Enum ja `match`-lauseke, jonka kuviot ovat enumin variantteja">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-03/src/main.rs:here}}
```

</Listing>

Puretaan `value_in_cents`-funktion `match`-lauseke. Ensin listaamme `match`-avainsanan ja sitten lausekkeen, joka tässä tapauksessa on arvo `coin`. Tämä
näyttää hyvin samalta kuin ehtolauseke `if`:n kanssa, mutta ero on suuri: `if`:ssä ehdon täytyy evaluoitua totuusarvoksi, mutta tässä se voi olla mikä tahansa
tyyppi. Tässä esimerkissä `coin`-muuttujan tyyppi on ensimmäisellä rivillä määritelty `Coin`-enum.

Seuraavaksi tulevat `match`-haarat. Haaralla on kaksi osaa: kuvio ja jokin koodi. Ensimmäisellä haaralla on kuvio, joka on arvo `Coin::Penny`, ja sitten
`=>`-operaattori, joka erottaa kuvion ja suoritettavan koodin. Tässä tapauksessa koodi on vain arvo `1`. Jokainen haara erotetaan seuraavasta pilkulla.

Kun `match`-lauseke suoritetaan, se vertaa tulosarvoa kunkin haaran kuvioon järjestyksessä. Jos kuvio täsmää arvoon, kyseiseen kuvioon liittyvä koodi
suoritetaan. Jos kuvio ei täsmää arvoon, suoritus jatkuu seuraavaan haaraan, aivan kuten kolikonlajittelukoneessa. Meillä voi olla niin monta haaraa kuin
tarvitsemme: Listauksessa 6-3 `match`-lausekkeessamme on neljä haaraa.

Kuhunkin haaraan liittyvä koodi on lauseke, ja vastaavan haaran lausekkeen tulosarvo on koko `match`-lausekkeen palauttama arvo.

Emme yleensä käytä aaltosulkeita, jos haaran koodi on lyhyt, kuten Listauksessa 6-3, jossa jokainen haara palauttaa vain arvon. Jos haluat suorittaa useita
koodirivejä haarassa, sinun täytyy käyttää aaltosulkeita, ja haaraa seuraava pilkku on silloin valinnainen. Esimerkiksi seuraava koodi tulostaa ”Lucky penny!”
aina, kun metodia kutsutaan `Coin::Penny`-arvolla, mutta palauttaa silti lohkon viimeisen arvon, `1`:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-08-match-arm-multiple-lines/src/main.rs:here}}
```

### Arvoihin sitoutuvat kuviot

Toinen hyödyllinen ominaisuus `match`-haaroissa on, että ne voivat sitoutua kuvioon täsmäävien arvojen osiin. Näin voimme poimia arvoja enum-varianttien
sisältä.

Esimerkkinä muutetaan yksi enum-varianteistamme pitämään dataa sisällään. Vuosina 1999–2008 Yhdysvaltain rahapaja lyö 25 sentin kolikoita, joissa oli eri
suunnitelma jokaiselle 50 osavaltiolle toisella puolella. Mikään muu kolikko ei saanut osavaltiosuunnitelmia, joten vain 25 sentin kolikoilla on tämä
ylimääräinen arvo. Voimme lisätä tämän tiedon `enum`-määrittelyymme muuttamalla `Quarter`-variantin sisältämään `UsState`-arvon, kuten Listauksessa 6-4 on
tehty.

<Listing number="6-4" caption="`Coin`-enum, jossa `Quarter`-variantti sisältää myös `UsState`-arvon">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-04/src/main.rs:here}}
```

</Listing>

Kuvitellaan, että ystävä yrittää kerätä kaikki 50 osavaltion 25 sentin kolikkoa. Kun lajittelemme irtonaisia kolikoita tyypin mukaan, mainitsemme myös
jokaisen 25 sentin kolikon osavaltion nimen, jotta ystävä voi lisätä sen kokoelmaansa, jos sitä ei vielä ole.

Tämän koodin `match`-lausekkeessa lisäämme muuttujan nimeltä `state` kuvioon, joka täsmää `Coin::Quarter`-variantin arvoihin. Kun `Coin::Quarter` täsmää,
`state`-muuttuja sitoutuu kyseisen 25 sentin kolikon osavaltion arvoon. Sitten voimme käyttää `state`:a kyseisen haaran koodissa näin:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-09-variable-in-pattern/src/main.rs:here}}
```

Jos kutsuisimme `value_in_cents(Coin::Quarter(UsState::Alaska))`, `coin` olisi `Coin::Quarter(UsState::Alaska)`. Kun vertaamme tätä arvoa jokaiseen
`match`-haaraan, mikään ei täsmää ennen kuin pääsemme `Coin::Quarter(state)`-haaraan. Tällöin `state`-sidonta on arvo `UsState::Alaska`. Voimme sitten käyttää
tätä sidontaa `println!`-lausekkeessa ja poimia näin sisäisen osavaltioarvon `Coin`-enumin `Quarter`-variantista.

<!-- Old headings. Do not remove or links may break. -->

<a id="matching-with-optiont"></a>

### `Option<T>`-kuvio `match`-lausekkeessa

Edellisessä osiossa halusimme saada sisäisen `T`-arvon `Some`-tapauksesta käytettäessä `Option<T>`:tä; voimme käsitellä `Option<T>`:tä myös `match`-lausekkeella,
kuten teimme `Coin`-enumin kanssa! Sen sijaan, että vertaisimme kolikoita, vertaamme `Option<T>`:n variantteja, mutta `match`-lausekkeen toimintatapa pysyy
samana.

Oletetaan, että haluamme kirjoittaa funktion, joka ottaa `Option<i32>`:n ja lisää 1 sisällä olevaan arvoon, jos arvo on olemassa. Jos arvoa ei ole, funktion
pitäisi palauttaa `None`-arvo eikä yrittää suorittaa mitään operaatioita.

Tämä funktio on hyvin helppo kirjoittaa `match`-lausekkeen ansiosta, ja se näyttää Listaukselta 6-5.

<Listing number="6-5" caption="Funktio, joka käyttää `match`-lauseketta `Option<i32>`:llä">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:here}}
```

</Listing>

Tarkastellaan `plus_one`-funktion ensimmäistä suoritusta tarkemmin. Kun kutsumme `plus_one(five)`, muuttujalla `x` `plus_one`-funktion rungossa on arvo
`Some(5)`. Vertaamme sitten sitä jokaiseen `match`-haaraan:

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:first_arm}}
```

`Some(5)`-arvo ei täsmää kuvioon `None`, joten jatkamme seuraavaan haaraan:

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:second_arm}}
```

Täsmääkö `Some(5)` kuvioon `Some(i)`? Kyllä! Meillä on sama variantti. `i` sitoutuu `Some`:n sisältämään arvoon, joten `i` saa arvon `5`. Haaran koodi
suoritetaan sitten, joten lisäämme 1 arvoon `i` ja luomme uuden `Some`-arvon, jonka sisällä on yhteensä `6`.

Tarkastellaan nyt Listauksen 6-5 toista `plus_one`-kutsua, jossa `x` on `None`. Siirrymme `match`-lausekkeeseen ja vertaamme ensimmäiseen haaraan:

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:first_arm}}
```

Se täsmää! Lisättävää arvoa ei ole, joten ohjelma pysähtyy ja palauttaa `None`-arvon `=>`-merkin oikealla puolella. Koska ensimmäinen haara täsmäsi, muita
haaroja ei verrata.

`match`-lausekkeen ja enumien yhdistäminen on hyödyllistä monissa tilanteissa. Näet tämän kuvion paljon Rust-koodissa: `match` enumia vasten, sitoa muuttuja
sisällä olevaan dataan ja suorita sitten koodia sen perusteella. Se on aluksi hieman hankalaa, mutta kun tottuu siihen, toivot sitä kaikissa kielissä. Se on
jatkuvasti käyttäjien suosikki.

### `match`-lausekkeet ovat tyhjentäviä

`match`-lausekkeesta on vielä yksi puoli, josta meidän täytyy puhua: haarojen kuvioiden täytyy kattaa kaikki mahdollisuudet. Harkitse tätä versiota
`plus_one`-funktiostamme, jossa on bugi eikä se käänny:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-10-non-exhaustive-match/src/main.rs:here}}
```

Emme käsitelleet `None`-tapausta, joten tämä koodi aiheuttaa bugin. Onneksi Rust osaa havaita tämän bugin. Jos yritämme kääntää tämän koodin, saamme tämän
virheen:

```console
{{#include ../listings/ch06-enums-and-pattern-matching/no-listing-10-non-exhaustive-match/output.txt}}
```

Rust tietää, ettemme käsitelleet kaikkia mahdollisia tapauksia, ja tietää jopa, minkä kuvion unohdimme! `match`-lausekkeet Rustissa ovat _tyhjentäviä_: meidän
täytyy käsitellä jokainen mahdollisuus, jotta koodi on kelvollinen. Erityisesti `Option<T>`:n tapauksessa, kun Rust estää meitä unohtamasta `None`-tapauksen
käsittelyn eksplisiittisesti, se suojaa meitä olettamasta, että meillä on arvo, vaikka se saattaa olla null, mikä tekee aiemmin käsitellystä miljardin
dollarin virheestä mahdottoman.

### Yleiskuviot ja `_`-paikkamerkki

Enumien avulla voimme myös tehdä erityistoimia muutamalle tietylle arvolle, mutta kaikille muille arvoille tehdä yhden oletustoiminnon. Kuvitellaan, että
toteutamme pelin, jossa jos heität noppaa ja saat 3, pelaajasi ei liiku vaan saa uuden hienon hatun. Jos heität 7, pelaajasi menettää hienon hatun. Kaikille
muille arvoille pelaajasi liikkuu pelilaudalla sen verran tilaa kuin noppa osoittaa. Tässä on `match`, joka toteuttaa tämän logiikan nopan heittotuloksella
kovakoodattuna satunnaisen arvon sijaan, ja kaikki muu logiikka edustettu funktioina ilman runkoa, koska niiden toteuttaminen ei kuulu tämän esimerkin
piiriin:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-15-binding-catchall/src/main.rs:here}}
```

Ensimmäisillä kahdella haaralla kuviot ovat kirjaimellisia arvoja `3` ja `7`. Viimeisellä haaralla, joka kattaa kaikki muut mahdolliset arvot, kuvio on
muuttuja, jonka olemme valinneet nimeksi `other`. `other`-haaran koodi käyttää muuttujaa välittämällä sen `move_player`-funktiolle.

Tämä koodi kääntyy, vaikka emme listanneet kaikkia mahdollisia `u8`-arvoja, koska viimeinen kuvio täsmää kaikkiin arvoihin, joita ei ole erikseen listattu.
Tämä yleiskuvio täyttää vaatimuksen, että `match` on tyhjentävä. Huomaa, että yleiskuvion täytyy olla viimeisenä, koska kuvioita evaluoidaan järjestyksessä.
Jos yleiskuvio olisi aiemmin, muut haarat eivät koskaan suorittuisi, joten Rust varoittaa meitä, jos lisäämme haaroja yleiskuvion jälkeen!

Rustissa on myös kuvio, jota voimme käyttää, kun haluamme yleiskuvion mutta emme halua _käyttää_ yleiskuvion arvoa: `_` on erityinen kuvio, joka täsmää
mihin tahansa arvoon eikä sido sitä arvoon. Tämä kertoo Rustille, ettei meidän tarvitse arvoa, joten Rust ei varoita meitä käyttämättömästä muuttujasta.

Muutetaan pelin sääntöjä: nyt, jos heität mitä tahansa muuta kuin 3 tai 7, sinun täytyy heittää uudelleen. Emme enää tarvitse yleiskuvion arvoa, joten voimme
muuttaa koodimme käyttämään `_`-merkkiä `other`-nimisen muuttujan sijaan:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-16-underscore-catchall/src/main.rs:here}}
```

Tämä esimerkki täyttää myös tyhjentävyysvaatimuksen, koska sivuutamme eksplisiittisesti kaikki muut arvot viimeisessä haarassa; emme ole unohtaneet mitään.

Lopuksi muutamme pelin sääntöjä vielä kerran niin, ettei vuorollasi tapahdu mitään, jos heität mitä tahansa muuta kuin 3 tai 7. Voimme ilmaista tämän
käyttämällä yksikköarvoa (tyhjä tuplatyyppi, josta mainittiin [”Tuplatyyppi”][tuples]<!-- ignore --> -osiossa) koodina, joka liittyy `_`-haaraan:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-17-underscore-unit/src/main.rs:here}}
```

Tässä kerromme Rustille eksplisiittisesti, ettei meidän tarvitse käyttää mitään muuta arvoa, joka ei täsmää aiemman haaran kuvioon, emmekä halua suorittaa
mitään koodia tässä tapauksessa.

Kuvioista ja täsmäyksestä on lisää, mitä käsittelemme [Luvussa 19][ch19-00-patterns]<!-- ignore -->. Toistaiseksi siirrymme `if let`-syntaksiin, joka voi olla
hyödyllinen tilanteissa, joissa `match`-lauseke on hieman puhelias.

[tuples]: ch03-02-data-types.html#the-tuple-type
[ch19-00-patterns]: ch19-00-patterns.html
