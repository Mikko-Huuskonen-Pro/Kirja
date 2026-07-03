
<!-- Old headings. Do not remove or links may break. -->

<a id="yielding"></a>

### Ohjauksen luovuttaminen ajoympäristölle

Muista [”Ensimmäinen async-ohjelmamme”][async-program]<!-- ignore --> -osiosta, että jokaisessa odotuspisteessä Rust antaa ajoympäristölle mahdollisuuden keskeyttää tehtävä ja vaihtaa toiseen, jos odotettava future ei ole valmis. Päinvastoin pätee myös: Rust keskeyttää async-lohkot ja palauttaa ohjauksen ajoympäristölle _vain_ odotuspisteessä. Kaikki odotuspisteiden välillä on synkronista.

Tämä tarkoittaa, että jos teet paljon työtä async-lohkossa ilman odotuspistettä, kyseinen future estää muita futureja etenemästä. Tätä kutsutaan joskus tilanteeksi, jossa yksi future _nälkiinnyttää_ muita futureja. Joissakin tapauksissa se ei ole suuri ongelma. Jos kuitenkin teet jonkinlaista kallista alustusta tai pitkään kestävää työtä, tai jos sinulla on future, joka jatkaa tiettyä tehtävää loputtomasti, sinun täytyy miettiä, milloin ja missä luovutat ohjauksen takaisin ajoympäristölle.

Simuloidaan pitkään kestävää operaatiota havainnollistaaksemme nälkiinnytysongelmaa ja tutkitaan sitten, miten se ratkaistaan. Listaus 17-14 esittelee `slow`-funktion.

<Listing number="17-14" caption="`thread::sleep`:in käyttö hitaiden operaatioiden simulointiin" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-14/src/main.rs:slow}}
```

</Listing>

Tämä koodi käyttää `std::thread::sleep`:ia `trpl::sleep`:in sijaan, joten `slow`:in kutsuminen estää nykyisen säikeen tietyn määrän millisekunteja. Voimme käyttää `slow`:ia todellisten maailman operaatioiden sijaisena, jotka ovat sekä pitkään kestäviä että estäviä.

Listauksessa 17-15 käytämme `slow`:ia emuloimaan tämänkaltaisen CPU-rajoitteisen työn tekemistä parissa futurea.

<Listing number="17-15" caption="`slow`-funktion kutsuminen hitaiden operaatioiden simulointiin" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-15/src/main.rs:slow-futures}}
```

</Listing>

Kumpikin future palauttaa ohjauksen ajoympäristölle vasta _sen jälkeen_, kun se on suorittanut joukon hitaita operaatioita. Jos suoritat tämän koodin, näet tämän tulosteen:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-15/
cargo run
copy just the output
-->

```text
'a' started.
'a' ran for 30ms
'a' ran for 10ms
'a' ran for 20ms
'b' started.
'b' ran for 75ms
'b' ran for 10ms
'b' ran for 15ms
'b' ran for 350ms
'a' finished.
```

Kuten listauksessa 17-5, jossa kilpailutimme kahta URL-osoitetta hakevia futureja `trpl::select`:illa, `select` päättyy edelleen heti, kun `a` on valmis. `slow`-kutsujen välillä ei kuitenkaan ole vuorottelua kahden futuren välillä. `a`-future tekee kaiken työnsä, kunnes `trpl::sleep`-kutsua odotetaan, sitten `b`-future tekee kaiken työnsä, kunnes sen oma `trpl::sleep`-kutsu odotetaan, ja lopuksi `a`-future valmistuu. Jotta molemmat futuret voisivat edetä hitaiden tehtäviensä välillä, tarvitsemme odotuspisteitä, jotta voimme luovuttaa ohjauksen takaisin ajoympäristölle. Tarvitsemme siis jotain, mitä voimme odottaa!

Näemme tämänkaltaisen luovutuksen jo listauksessa 17-15: jos poistaisimme `a`-futuren lopun `trpl::sleep`:in, se valmistuisi ilman, että `b`-future suorittuisi _lainkaan_. Kokeillaan käyttää `trpl::sleep`-funktiota lähtökohtana operaatioiden vuorottelulle etenemisessä, kuten listauksessa 17-16.

<Listing number="17-16" caption="`trpl::sleep`:in käyttö operaatioiden vuorottelun sallimiseksi etenemisessä" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-16/src/main.rs:here}}
```

</Listing>

Olemme lisänneet `trpl::sleep`-kutsuja odotuspisteillä jokaisen `slow`-kutsun väliin. Nyt kahden futuren työ on vuoroteltua:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-16
cargo run
copy just the output
-->

```text
'a' started.
'a' ran for 30ms
'b' started.
'b' ran for 75ms
'a' ran for 10ms
'b' ran for 10ms
'a' ran for 20ms
'b' ran for 15ms
'a' finished.
```

`a`-future suorittaa edelleen hetken ennen ohjauksen luovuttamista `b`:lle, koska se kutsuu `slow`:ia ennen kuin koskaan kutsuu `trpl::sleep`:ia, mutta sen jälkeen futuret vaihtavat vuorotellen aina, kun jompikumpi osuu odotuspisteeseen. Tässä tapauksessa teimme sen jokaisen `slow`-kutsun jälkeen, mutta voimme jakaa työn millä tavalla meille sopii.

Emme kuitenkaan todella halua _nukkua_ tässä: haluamme edetä niin nopeasti kuin voimme. Meidän täytyy vain luovuttaa ohjaus takaisin ajoympäristölle. Voimme tehdä sen suoraan käyttämällä `trpl::yield_now`-funktiota. Listauksessa 17-17 korvaamme kaikki `trpl::sleep`-kutsut `trpl::yield_now`:illa.

<Listing number="17-17" caption="`yield_now`:in käyttö operaatioiden vuorottelun sallimiseksi etenemisessä" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-17/src/main.rs:yields}}
```

</Listing>

Tämä koodi on sekä selkeämpi todellisesta tarkoituksesta että voi olla merkittävästi nopeampi kuin `sleep`:in käyttö, koska `sleep`:in käyttämien ajastimien tarkkuudella on usein rajoja. Käyttämämme `sleep`-versio nukkuu aina vähintään millisekunnin, vaikka välittäisimme sille yhden nanosekunnin `Duration`:in. Modernit tietokoneet ovat _nopeita_: ne voivat tehdä paljon yhdessä millisekunnissa!

Tämä tarkoittaa, että async voi olla hyödyllinen jopa laskentarajoitteisille tehtäville, riippuen siitä, mitä muuta ohjelmasi tekee, koska se tarjoaa hyödyllisen työkalun ohjelman eri osien välisten suhteiden jäsentämiseen (mutta async-tilakoneen yläkulun hinnalla). Tämä on eräänlaista _yhteistoiminnallista moniajoa_, jossa jokaisella futurella on valta päättää, milloin se luovuttaa ohjauksen odotuspisteiden kautta. Jokaisella futurella on siten myös vastuu välttää liian pitkää estämistä. Joissakin Rust-pohjaisissa sulautetuissa käyttöjärjestelmissä tämä on _ainoa_ moniajon laji!

Oikeassa koodissa et yleensä vuorottele funktiokutsuja ja odotuspisteitä jokaisella rivillä, tietenkään. Vaikka ohjauksen luovuttaminen tällä tavalla on suhteellisen edullista, se ei ole ilmaista. Monissa tapauksissa laskentarajoitteisen tehtävän pilkkominen voi hidastaa sitä merkittävästi, joten joskus on parempi _kokonaissuorituskyvyn_ kannalta antaa operaation estää hetkeksi. Mittaa aina nähdäksesi, missä koodisi todelliset suorituskykypullonkaulat ovat. Taustalla oleva dynamiikka on kuitenkin tärkeä pitää mielessä, jos _näet_ paljon työtä tapahtuvan peräkkäin, kun odotit sen tapahtuvan samanaikaisesti!

### Omien async-abstraktioiden rakentaminen

Voimme myös yhdistellä futureja luodaksemme uusia malleja. Esimerkiksi voimme rakentaa `timeout`-funktion async-rakennuspalikoilla, joita meillä jo on. Kun olemme valmiita, tulos on toinen rakennuspalikka, jota voisimme käyttää luomaan vielä lisää async-abstraktioita.

Listaus 17-18 näyttää, miten odotamme tämän `timeout`:in toimivan hitaan futuren kanssa.

<Listing number="17-18" caption="Kuvitellun `timeout`:imme käyttö hitaan operaation suorittamiseen aikarajalla" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-18/src/main.rs:here}}
```

</Listing>

Toteutetaan tämä! Aloitetaan miettimällä `timeout`:in API:ta:

- Sen täytyy olla itse async-funktio, jotta voimme odottaa sitä.
- Sen ensimmäisen parametrin pitäisi olla suoritettava future. Voimme tehdä siitä geneerisen, jotta se toimii minkä tahansa futuren kanssa.
- Sen toinen parametri on enimmäisodotusaika. Jos käytämme `Duration`:ia, sen on helppo välittää eteenpäin `trpl::sleep`:ille.
- Sen pitäisi palauttaa `Result`. Jos future valmistuu onnistuneesti, `Result` on `Ok` futuren tuottamalla arvolla. Jos aikaraja umpeutuu ensin, `Result` on `Err` odotetulla kestolla.

Listaus 17-19 näyttää tämän määrittelyn.

<!-- This is not tested because it intentionally does not compile. -->

<Listing number="17-19" caption="`timeout`:in signatuurin määrittely" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-19/src/main.rs:declaration}}
```

</Listing>

Tämä täyttää tyyppitavoitteemme. Mietitään nyt tarvittavaa _käyttäytymistä_: haluamme kilpailuttaa välitetyn futuren keston kanssa. Voimme käyttää `trpl::sleep`:ia luodaksemme ajastinfuturen kestosta ja `trpl::select`:ia suorittaaksemme tämän ajastimen kutsujan välittämän futuren kanssa.

Listauksessa 17-20 toteutamme `timeout`:in tekemällä `match`:in `trpl::select`:in odottamisen tulokseen.

<Listing number="17-20" caption="`timeout`:in määrittely `select`:illä ja `sleep`:illä" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-20/src/main.rs:implementation}}
```

</Listing>

`trpl::select`:in toteutus ei ole reilu: se pollaa argumentteja aina siinä järjestyksessä, jossa ne välitetään (muut `select`-toteutukset valitsevat satunnaisesti, mitä argumenttia pollataan ensin). Välitämme siis `future_to_try`:n `select`:ille ensin, jotta sillä on mahdollisuus valmistua, vaikka `max_time` olisi hyvin lyhyt kesto. Jos `future_to_try` valmistuu ensin, `select` palauttaa `Left`:in `future_to_try`:n tuloksella. Jos `timer` valmistuu ensin, `select` palauttaa `Right`:in ajastimen `()`-tuloksella.

Jos `future_to_try` onnistuu ja saamme `Left(output)`:in, palautamme `Ok(output)`:in. Jos `sleep`-ajastin umpeutuu sen sijaan ja saamme `Right(())`:in, jätämme `()`:n huomiotta `_`:llä ja palautamme sen sijaan `Err(max_time)`:in.

Näin meillä on toimiva `timeout`, joka on rakennettu kahdesta muusta async-apurista. Jos suoritamme koodimme, se tulostaa epäonnistumistilan aikarajan jälkeen:

```text
Failed after 2 seconds
```

Koska futuret yhdistyvät muihin futureihin, voit rakentaa todella tehokkaita työkaluja pienemmistä async-rakennuspalikoista. Esimerkiksi voit käyttää samaa lähestymistapaa yhdistääksesi aikarajoja uudelleenyrityksiin ja käyttää niitä vuorostaan verkko-operaatioihin (kuten listauksessa 17-5).

Käytännössä työskentelet yleensä suoraan `async`:in ja `await`:in kanssa ja toissijaisesti funktioiden kuten `select`:in ja makrojen kuten `join!`:n kanssa hallitaksesi, miten uloimmat futuret suoritetaan.

Olemme nyt nähneet useita tapoja työskennellä usean futuren kanssa samanaikaisesti. Seuraavaksi katsomme, miten voimme työskennellä usean futuren kanssa peräkkäin ajan kuluessa _streamien_ avulla.

[async-program]: ch17-01-futures-and-syntax.html#our-first-async-program
