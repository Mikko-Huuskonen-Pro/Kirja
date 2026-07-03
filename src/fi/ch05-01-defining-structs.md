## Rakenteiden määrittely ja instanssien luominen

Rakenteet ovat samankaltaisia kuin tuplat, joita käsiteltiin [”Tuplatyyppi”][tuples]<!-- ignore --> -osiossa, siinä mielessä, että molemmat pitävät useita toisiinsa liittyviä arvoja. Kuten tuplissa, rakenteen osat voivat olla eri tyyppejä. Toisin kuin tuplissa, rakenteessa nimeät jokaisen datan osan, jotta arvojen merkitys on selvä. Näiden nimien lisääminen tarkoittaa, että rakenteet ovat joustavampia kuin tuplat: sinun ei tarvitse luottaa datan järjestykseen määrittääksesi tai käyttääksesi instanssin arvoja.

Määrittääksesi rakenteen, kirjoitat avainsanan `struct` ja nimeät koko rakenteen. Rakenteen nimen pitäisi kuvata yhdessä ryhmiteltyjen datan osien merkitystä. Sitten aaltosulkeiden sisällä määrittelemme datan osien nimet ja tyypit, joita kutsumme _kentiksi_. Esimerkiksi Listausta 5-1 näyttää rakenteen, joka tallentaa tietoja käyttäjätilistä.

<Listing number="5-1" file-name="src/main.rs" caption="`User`-rakenteen määrittely">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-01/src/main.rs:here}}
```

</Listing>

Käyttääksemme rakennetta sen määrittelyn jälkeen, luomme kyseisen rakenteen _instanssin_ määrittämällä konkreettiset arvot jokaiselle kentälle. Luomme instanssin ilmoittamalla rakenteen nimen ja lisäämällä aaltosulkeet, jotka sisältävät _avain: arvo_ -pareja, joissa avaimet ovat kenttien nimiä ja arvot ovat dataa, jonka haluamme tallentaa näihin kenttiin. Emme tarvitse määrittää kenttiä samassa järjestyksessä, jossa ilmoitimme ne rakenteessa. Toisin sanoen rakenteen määrittely on kuin yleinen malli tyypille, ja instanssit täyttävät mallin tietyllä datalla luodakseen tyypin arvoja. Esimerkiksi voimme ilmoittaa tietyn käyttäjän kuten Listauksessa 5-2 on esitetty.

<Listing number="5-2" file-name="src/main.rs" caption="`User`-rakenteen instanssin luominen">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-02/src/main.rs:here}}
```

</Listing>

Saadaksemme tietyn arvon rakenteesta, käytämme pistesyntaksia. Esimerkiksi käyttääksemme tämän käyttäjän sähköpostiosoitetta, käytämme `user1.email`. Jos instanssi on muuttuva, voimme muuttaa arvoa käyttämällä pistesyntaksia ja sijoittamalla tiettyyn kenttään. Listausta 5-3 näyttää, miten muutetaan `email`-kentän arvoa muuttuvassa `User`-instanssissa.

<Listing number="5-3" file-name="src/main.rs" caption="`email`-kentän arvon muuttaminen `User`-instanssissa">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-03/src/main.rs:here}}
```

</Listing>

Huomaa, että koko instanssin täytyy olla muuttuva; Rust ei salli meidän merkitä vain tiettyjä kenttiä muuttuviksi. Kuten minkä tahansa lausekkeen kanssa, voimme rakentaa uuden instanssin rakenteesta funktion rungon viimeisenä lausekkeena palauttaaksemme implisiittisesti kyseisen uuden instanssin.

Listausta 5-4 näyttää `build_user`-funktion, joka palauttaa `User`-instanssin annetulla sähköpostilla ja käyttäjänimellä. `active`-kenttä saa arvon `true`, ja `sign_in_count` saa arvon `1`.

<Listing number="5-4" file-name="src/main.rs" caption="`build_user`-funktio, joka ottaa sähköpostin ja käyttäjänimen ja palauttaa `User`-instanssin">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-04/src/main.rs:here}}
```

</Listing>

On järkevää nimetä funktion parametrit samalla nimellä kuin rakenteen kentät, mutta `email`- ja `username`-kenttien ja -muuttujien toistaminen on hieman työlästä. Jos rakenteella olisi enemmän kenttiä, jokaisen nimen toistaminen olisi vieläkin ärsyttävämpää. Onneksi on kätevä lyhenne!

<!-- Old heading. Do not remove or links may break. -->

<a id="using-the-field-init-shorthand-when-variables-and-fields-have-the-same-name"></a>

### Kentän alustuksen lyhenteen käyttö

Koska parametrien nimet ja rakenteen kenttien nimet ovat täsmälleen samat Listauksessa 5-4, voimme käyttää _kentän alustuksen lyhenne_-syntaksia kirjoittaaksemme `build_user`-funktion uudelleen niin, että se käyttäytyy täsmälleen samalla tavalla, mutta ilman `username`- ja `email`-toistoa, kuten Listauksessa 5-5 on esitetty.

<Listing number="5-5" file-name="src/main.rs" caption="`build_user`-funktio, joka käyttää kentän alustuksen lyhennettä, koska `username`- ja `email`-parametreilla on sama nimi kuin rakenteen kentillä">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-05/src/main.rs:here}}
```

</Listing>

Tässä luomme uuden `User`-rakenteen instanssin, jolla on kenttä nimeltä `email`. Haluamme asettaa `email`-kentän arvoksi `build_user`-funktion `email`-parametrin arvon. Koska `email`-kentällä ja `email`-parametrilla on sama nimi, meidän tarvitsee kirjoittaa vain `email` eikä `email: email`.

### Instanssien luominen toisista instansseista rakenteen päivityssyntaksilla

On usein hyödyllistä luoda uusi instanssi rakenteesta, joka sisältää suurimman osan arvoista toisesta instanssista, mutta muuttaa joitakin. Voit tehdä tämän käyttämällä _rakenteen päivityssyntaksia_.

Ensin Listauksessa 5-6 näytämme, miten luodaan uusi `User`-instanssi `user2`:ssa tavallisesti ilman päivityssyntaksia. Asetamme uuden arvon `email`-kentälle, mutta käytämme muuten samoja arvoja `user1`:stä, jonka loimme Listauksessa 5-2.

<Listing number="5-6" file-name="src/main.rs" caption="Uuden `User`-instanssin luominen käyttäen kaikkia paitsi yhtä arvoa `user1`:stä">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-06/src/main.rs:here}}
```

</Listing>

Käyttämällä rakenteen päivityssyntaksia voimme saavuttaa saman vaikutuksen vähemmällä koodilla, kuten Listauksessa 5-7 on esitetty. `..`-syntaksi määrittää, että jäljellä olevilla kentillä, joita ei ole eksplisiittisesti asetettu, pitäisi olla sama arvo kuin annetun instanssin kentillä.

<Listing number="5-7" file-name="src/main.rs" caption="Rakenteen päivityssyntaksin käyttö uuden `email`-arvon asettamiseksi `User`-instanssille, mutta muiden arvojen käyttämiseksi `user1`:stä">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-07/src/main.rs:here}}
```

</Listing>

Listauksen 5-7 koodi luo myös instanssin `user2`:ssa, jolla on eri arvo `email`-kentälle, mutta samat arvot `username`-, `active`- ja `sign_in_count`-kentille `user1`:stä. `..user1` täytyy tulla viimeisenä määrittämään, että jäljellä olevat kentät saavat arvonsa `user1`:n vastaavista kentistä, mutta voimme valita määrittää arvoja niin monelle kentälle kuin haluamme missä tahansa järjestyksessä riippumatta kenttien järjestyksestä rakenteen määrittelyssä.

Huomaa, että rakenteen päivityssyntaksi käyttää `=`-merkkiä kuten sijoituslauseke; tämä johtuu siitä, että se siirtää datan, kuten näimme [”Muuttujat ja data vuorovaikutuksessa siirron kanssa”][move]<!-- ignore --> -osiossa. Tässä esimerkissä emme voi enää käyttää `user1`:tä `user2`:n luomisen jälkeen, koska `user1`:n `username`-kentän `String` siirrettiin `user2`:een. Jos olisimme antaneet `user2`:lle uudet `String`-arvot sekä `email`- että `username`-kentille, ja siten käyttäneet vain `active`- ja `sign_in_count`-arvoja `user1`:stä, `user1` olisi edelleen kelvollinen `user2`:n luomisen jälkeen. Sekä `active` että `sign_in_count` ovat tyyppejä, jotka toteuttavat `Copy`-traitin, joten [”Vain pinossa oleva data: Copy”][copy]<!-- ignore --> -osiossa käsittelemämme käyttäytyminen pätee. Voimme edelleen käyttää `user1.email` tässä esimerkissä, koska sen arvoa _ei_ siirretty pois.

### Tuple-rakenteiden käyttö nimeämättömillä kentillä eri tyyppien luomiseksi

Rust tukee myös rakenteita, jotka näyttävät samankaltaisilta kuin tuplat, ja joita kutsutaan _tuple-rakenteiksi_. Tuple-rakenteilla on rakenteen nimen tuoma lisämerkitys, mutta niillä ei ole nimiä liitettynä kenttiinsä; niillä on vain kenttien tyypit. Tuple-rakenteet ovat hyödyllisiä, kun haluat antaa koko tuplalle nimen ja tehdä tuplasta eri tyypin kuin muista tuplista, ja kun jokaisen kentän nimeäminen kuten tavallisessa rakenteessa olisi puhelias tai tarpeeton.

Määrittääksesi tuple-rakenteen, aloita `struct`-avainsanalla ja rakenteen nimellä, jota seuraa tuplan tyypit. Esimerkiksi tässä määrittelemme ja käytämme kahta tuple-rakennetta nimeltä `Color` ja `Point`:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-01-tuple-structs/src/main.rs}}
```

</Listing>

Huomaa, että `black`- ja `origin`-arvot ovat eri tyyppejä, koska ne ovat eri tuple-rakenteiden instansseja. Jokainen määrittelemäsi rakenne on oma tyypinsä, vaikka rakenteen kentät saattaisivat olla samoja tyyppejä. Esimerkiksi funktio, joka ottaa parametrin tyypillä `Color`, ei voi ottaa `Point`-argumenttia, vaikka molemmat tyypit koostuvat kolmesta `i32`-arvosta. Muuten tuple-rakenneinstanssit ovat samankaltaisia kuin tuplat siinä mielessä, että voit purkaa ne yksittäisiin osiinsa, ja voit käyttää `.`-merkkiä, jota seuraa indeksi, päästäksesi yksittäiseen arvoon. Toisin kuin tuplat, tuple-rakenteet vaativat sinua nimeämään rakenteen tyypin, kun purat ne. Esimerkiksi kirjoittaisimme `let Point(x, y, z) = point`.

### Yksikkömäiset rakenteet ilman kenttiä

Voit myös määritellä rakenteita, joilla ei ole lainkaan kenttiä! Näitä kutsutaan _yksikkömäisiksi rakenteiksi_, koska ne käyttäytyvät samankaltaisesti kuin `()`, yksikkötyyppi, josta mainitsimme [”Tuplatyyppi”][tuples]<!-- ignore --> -osiossa. Yksikkömäiset rakenteet voivat olla hyödyllisiä, kun sinun täytyy toteuttaa trait jollekin tyypille, mutta sinulla ei ole dataa, jonka haluaisit tallentaa itse tyyppiin. Käsittelemme traitteja Luvussa 10. Tässä on esimerkki yksikkörakenteen nimeltä `AlwaysEqual` ilmoittamisesta ja instanssin luomisesta:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-04-unit-like-structs/src/main.rs}}
```

</Listing>

Määrittääksemme `AlwaysEqual`:in, käytämme `struct`-avainsanaa, haluamaamme nimeä ja sitten puolipistettä. Ei tarvetta aaltosulkeille tai sulkeille! Sitten voimme saada `AlwaysEqual`-instanssin `subject`-muuttujaan samalla tavalla: käyttämällä määrittelemäämme nimeä ilman aaltosulkeita tai sulkeita. Kuvittele, että myöhemmin toteutamme käyttäytymistä tälle tyypille siten, että jokainen `AlwaysEqual`-instanssi on aina yhtä suuri kuin minkä tahansa muun tyypin instanssi, ehkä testaustarkoituksiin tunnetun tuloksen saamiseksi. Emme tarvitsisi dataa toteuttaaksemme tuota käyttäytymistä! Näet Luvussa 10, miten määritellä traitteja ja toteuttaa ne mille tahansa tyypille, mukaan lukien yksikkömäiset rakenteet.

> ### Rakenteen datan omistajuus
>
> `User`-rakenteen määrittelyssä Listauksessa 5-1 käytimme omistettua `String`-tyyppiä `&str`-merkkijonoviipaletyypin sijaan. Tämä on tarkoituksellinen valinta, koska haluamme jokaisen tämän rakenteen instanssin omistavan kaiken datansa ja datan olevan kelvollinen niin kauan kuin koko rakenne on kelvollinen.
>
> On myös mahdollista, että rakenteet tallentavat viittauksia muualla omistettuun dataan, mutta se vaatii _elinaikojen_ käyttöä, Rust-ominaisuutta, jota käsittelemme Luvussa 10. Elinaika varmistavat, että rakenteen viittaama data on kelvollinen niin kauan kuin rakenne on. Sanotaan, että yrität tallentaa viittauksen rakenteeseen määrittämättä elinaikoja, kuten seuraavassa; tämä ei toimi:
>
> <Listing file-name="src/main.rs">
>
> <!-- CAN'T EXTRACT SEE https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust,ignore,does_not_compile
> struct User {
>     active: bool,
>     username: &str,
>     email: &str,
>     sign_in_count: u64,
> }
>
> fn main() {
>     let user1 = User {
>         active: true,
>         username: "someusername123",
>         email: "someone@example.com",
>         sign_in_count: 1,
>     };
> }
> ```
>
> </Listing>
>
> Kääntäjä valittaa, että se tarvitsee elinaikamäärittimet:
>
> ```console
> $ cargo run
>    Compiling structs v0.1.0 (file:///projects/structs)
> error[E0106]: missing lifetime specifier
>  --> src/main.rs:3:15
>   |
> 3 |     username: &str,
>   |               ^ expected named lifetime parameter
>   |
> help: consider introducing a named lifetime parameter
>   |
> 1 ~ struct User<'a> {
> 2 |     active: bool,
> 3 ~     username: &'a str,
>   |
>
> error[E0106]: missing lifetime specifier
>  --> src/main.rs:4:12
>   |
> 4 |     email: &str,
>   |            ^ expected named lifetime parameter
>   |
> help: consider introducing a named lifetime parameter
>   |
> 1 ~ struct User<'a> {
> 2 |     active: bool,
> 3 |     username: &str,
> 4 ~     email: &'a str,
>   |
>
> For more information about this error, try `rustc --explain E0106`.
> error: could not compile `structs` (bin "structs") due to 2 previous errors
> ```
>
> Luvussa 10 käsittelemme, miten korjata nämä virheet, jotta voit tallentaa viittauksia rakenteisiin, mutta toistaiseksi korjaamme tällaiset virheet käyttämällä omistettuja tyyppejä kuten `String` viittausten kuten `&str` sijaan.

<!-- manual-regeneration
for the error above
after running update-rustc.sh:
pbcopy < listings/ch05-using-structs-to-structure-related-data/no-listing-02-reference-in-struct/output.txt
paste above
add `> ` before every line -->

[tuples]: ch03-02-data-types.html#the-tuple-type
[move]: ch04-01-what-is-ownership.html#variables-and-data-interacting-with-move
[copy]: ch04-01-what-is-ownership.html#stack-only-data-copy
