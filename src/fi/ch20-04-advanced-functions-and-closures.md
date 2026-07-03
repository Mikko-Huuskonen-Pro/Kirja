## Edistyneet funktiot ja sulkeumat

Tämä osio tutkii edistyneitä ominaisuuksia, jotka liittyvät funktioihin ja sulkeumiin, mukaan lukien funktio-osoittimet ja sulkeumien palauttaminen.

### Funktio-osoittimet

Olemme puhuneet sulkeumien välittämisestä funktioille; voit myös välittää tavallisia funktioita funktioille! Tämä tekniikka on hyödyllinen, kun haluat välittää jo määrittelemäsi funktion uuden sulkeuman määrittelemisen sijaan. Funktiot pakotetaan tyypiksi `fn` (pienellä _f_:llä), älä sekoita sitä `Fn`-sulkeumatraitiin. `fn`-tyyppiä kutsutaan _funktio-osoittimeksi_. Funktioiden välittäminen funktio-osoittimilla sallii funktioiden käytön argumentteina muille funktioille.

Syntaksi parametrin määrittämiseksi funktio-osoittimeksi on samankaltainen kuin sulkeumilla, kuten listauksessa 20-28, jossa olemme määritelleet funktion `add_one`, joka lisää 1 parametrilleen. Funktio `do_twice` ottaa kaksi parametria: funktio-osoittimen mihin tahansa funktioon, joka ottaa `i32`-parametrin ja palauttaa `i32`:n, sekä yhden `i32`-arvon. Funktio `do_twice` kutsuu funktiota `f` kahdesti välittäen sille `arg`-arvon ja laskee sitten kaksi funktiokutsun tulosta yhteen. `main`-funktio kutsuu `do_twice`-funktiota argumenteilla `add_one` ja `5`.

<Listing number="20-28" file-name="src/main.rs" caption="`fn`-tyypin käyttö funktio-osoittimen hyväksymiseksi argumenttina">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-28/src/main.rs}}
```

</Listing>

Tämä koodi tulostaa `The answer is: 12`. Määrittelemme, että `do_twice`-funktion parametri `f` on `fn`, joka ottaa yhden `i32`-tyyppisen parametrin ja palauttaa `i32`:n. Voimme sitten kutsua `f`:ää `do_twice`-funktion rungossa. `main`-funktiossa voimme välittää funktion nimen `add_one` ensimmäisenä argumenttina `do_twice`-funktiolle.

Toisin kuin sulkeumat, `fn` on tyyppi eikä trait, joten määrittelemme `fn`:n suoraan parametrityypiksi sen sijaan, että julistaisimme geneerisen tyyppiparametrin yhdellä `Fn`-traiteista trait-sidonnana.

Funktio-osoittimet toteuttavat kaikki kolme sulkeumatraitia (`Fn`, `FnMut` ja `FnOnce`), mikä tarkoittaa, että voit aina välittää funktio-osoittimen argumenttina funktiolle, joka odottaa sulkeumaa. On parasta kirjoittaa funktiot käyttämällä geneeristä tyyppiä ja yhtä sulkeumatraitia, jotta funktiosi voivat hyväksyä joko funktioita tai sulkeumia.

Siitä huolimatta yksi esimerkki tilanteesta, jossa haluat hyväksyä vain `fn`:n eikä sulkeumia, on vuorovaikutus ulkoisen koodin kanssa, jolla ei ole sulkeumia: C-funktiot voivat ottaa funktioita argumentteina, mutta C:ssä ei ole sulkeumia.

Esimerkkinä tilanteesta, jossa voisit käyttää joko rivillä määriteltyä sulkeumaa tai nimettyä funktiota, katsotaan standardikirjaston `Iterator`-traitin tarjoaman `map`-metodin käyttöä. Käyttääksemme `map`-metodia muuntaaksemme numerovektorin merkkijonovektoriksi, voisimme käyttää sulkeumaa, kuten listauksessa 20-29.

<Listing number="20-29" caption="Sulkeuman käyttö `map`-metodin kanssa numeroiden muuntamiseksi merkkijonoiksi">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-29/src/main.rs:here}}
```

</Listing>

Tai voisimme nimetä funktion `map`-metodin argumentiksi sulkeuman sijaan. Listaus 20-30 näyttää, miltä tämä näyttäisi.

<Listing number="20-30" caption="`String::to_string`-funktion käyttö `map`-metodin kanssa numeroiden muuntamiseksi merkkijonoiksi">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-30/src/main.rs:here}}
```

</Listing>

Huomaa, että meidän täytyy käyttää täysin pätevää syntaksia, josta puhuimme [”Edistyneet traitit”][advanced-traits]<!-- ignore --> -osiossa, koska useita samannimisiä funktioita on saatavilla.

Tässä käytämme `ToString`-traitissa määriteltyä `to_string`-funktiota, jonka standardikirjasto on toteuttanut kaikille `Display`-traitin toteuttaville tyypeille.

Muista luvun 6 [”Luettelotyyppien arvot”][enum-values]<!-- ignore --> -kohdasta, että jokaisesta määrittelemästämme luettelotyypin variantista tulee myös alustusfunktio. Voimme käyttää näitä alustusfunktioita funktio-osoittimina, jotka toteuttavat sulkeumatraitit, mikä tarkoittaa, että voimme määrittää alustusfunktiot argumenteiksi metodeille, jotka ottavat sulkeumia, kuten listauksessa 20-31.

<Listing number="20-31" caption="Luettelotyypin alustajan käyttö `map`-metodin kanssa `Status`-instanssien luomiseksi numeroista">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-31/src/main.rs:here}}
```

</Listing>

Tässä luomme `Status::Value`-instansseja jokaisesta `u32`-arvosta välillä, jolla `map` kutsutaan, käyttämällä `Status::Value`-variantin alustusfunktiota. Jotkut pitävät tästä tyylistä ja jotkut sulkeumista. Ne kääntyvät samaan koodiin, joten käytä kumpaa tahansa tyyliä, joka on sinulle selkeämpi.

### Sulkeumien palauttaminen

Sulkeumat edustetaan traitteina, mikä tarkoittaa, että et voi palauttaa sulkeumia suoraan. Useimmissa tapauksissa, joissa haluaisit palauttaa traitin, voit sen sijaan käyttää traitin toteuttavaa konkreettista tyyppiä funktion paluuarvona. Sulkeumien kanssa et kuitenkaan voi yleensä tehdä niin, koska niillä ei ole palautettavaa konkreettista tyyppiä; et saa käyttää funktio-osoitinta `fn` paluutyyppinä, jos sulkeuma sieppaa arvoja näkyvyysalueestaan.

Sen sijaan käytät normaalisti luvussa 10 opittua `impl Trait` -syntaksia. Voit palauttaa minkä tahansa funktiotyypin käyttämällä `Fn`-, `FnOnce`- ja `FnMut`-traitteja. Esimerkiksi listauksen 20-32 koodi kääntyy aivan hyvin.

<Listing number="20-32" caption="Sulkeuman palauttaminen funktiosta `impl Trait` -syntaksia käyttäen">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-32/src/lib.rs}}
```

</Listing>

Kuten totesimme luvun 13 [”Sulkeumatyyppien päättely ja merkitseminen”][closure-types]<!-- ignore --> -kohdassa, jokainen sulkeuma on myös oma erillinen tyypkinsä. Jos sinun täytyy työskennellä useiden saman signatuurin mutta eri toteutuksen funktioiden kanssa, tarvitset niille trait-olion. Harkitse, mitä tapahtuu, jos kirjoitat listauksen 20-33 kaltaista koodia.

<Listing file-name="src/main.rs" number="20-33" caption="`Vec<T>`-vektorin luominen sulkeumista, jotka on määritelty funktioilla, jotka palauttavat `impl Fn` -tyyppejä">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-33/src/main.rs}}
```

</Listing>

Tässä meillä on kaksi funktiota, `returns_closure` ja `returns_initialized_closure`, jotka molemmat palauttavat `impl Fn(i32) -> i32`. Huomaa, että ne palauttamat sulkeumat ovat erilaisia, vaikka ne toteuttavat saman tyypin. Jos yritämme kääntää tämän, Rust kertoo, ettei se toimi:

```text
{{#include ../listings/ch20-advanced-features/listing-20-33/output.txt}}
```

Virheilmoitus kertoo, että aina kun palautamme `impl Trait` -tyypin, Rust luo ainutlaatuisen _läpinäkymättömän tyypin_, tyypin, jonka yksityiskohtiin emme voi kurkistaa emmekä voi arvata, minkä tyypin Rust luo kirjoittaaksemme sen itse. Vaikka nämä funktiot palauttavat sulkeumia, jotka toteuttavat saman traitin `Fn(i32) -> i32`, Rustin luomat läpinäkymättömät tyypit ovat erilaisia. (Tämä on samankaltaista kuin se, miten Rust tuottaa erilaisia konkreettisia tyyppejä eri async-lohkoille, vaikka niillä olisi sama tulostyyppi, kuten näimme luvun 17 [”`Pin`-tyyppi ja `Unpin`-trait”][future-types]<!-- ignore --> -kohdassa.) Olemme nähneet ratkaisun tähän ongelmaan jo useita kertoja: voimme käyttää trait-oliota, kuten listauksessa 20-34.

<Listing number="20-34" caption="`Vec<T>`-vektorin luominen sulkeumista, jotka on määritelty funktioilla, jotka palauttavat `Box<dyn Fn>` -tyypin, jotta niillä on sama tyyppi">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-34/src/main.rs:here}}
```

</Listing>

Tämä koodi kääntyy aivan hyvin. Lisätietoa trait-olioista on luvun 18 [”Trait-olioiden käyttö yhteisen käyttäytymisen abstrahoimiseen”][trait-objects]<!-- ignore --> -kohdassa.

Seuraavaksi katsotaan makroja!

[advanced-traits]: ch20-02-advanced-traits.html#advanced-traits
[enum-values]: ch06-01-defining-an-enum.html#enum-values
[closure-types]: ch13-01-closures.html#closure-type-inference-and-annotation
[future-types]: ch17-03-more-futures.html
[trait-objects]: ch18-02-trait-objects.html
