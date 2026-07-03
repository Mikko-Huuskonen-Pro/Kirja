## Unsafe Rust

Kaikki koodi, josta olemme keskustelleet tähän asti, on saanut Rustin muistiturvallisuustakuut pakotettuna käännösaikana. Rustissa on kuitenkin toinen kieli sen sisällä, joka ei pakota näitä muistiturvallisuustakuuja: sitä kutsutaan _unsafe Rustiksi_, ja se toimii aivan kuten tavallinen Rust, mutta antaa meille ylimääräisiä supervoimia.

Unsafe Rust on olemassa, koska luonteensa vuoksi staattinen analyysi on konservatiivista. Kun kääntäjä yrittää määrittää, pitääkö koodi takuut voimassa, on parempi hylätä joitakin kelvollisia ohjelmia kuin hyväksyä joitakin virheellisiä ohjelmia. Vaikka koodi _saattaisi_ olla kunnossa, jos Rustin kääntäjällä ei ole tarpeeksi tietoa olla varma, se hylkää koodin. Näissä tapauksissa voit käyttää unsafe-koodia kertoaksesi kääntäjälle: ”Luota minuun, tiedän mitä teen.” Varo kuitenkin, että käytät unsafe Rustia omalla vastuullasi: jos käytät unsafe-koodia väärin, ongelmia voi syntyä muistiturvattomuuden vuoksi, kuten null-osoittimen dereferoinnista.

Toinen syy siihen, miksi Rustilla on unsafe-vaihtoehto, on se, että taustalla oleva tietokonelaitteisto on luonnostaan unsafe. Jos Rust ei sallisi unsafe-operaatioita, et voisi tehdä tiettyjä tehtäviä. Rustin täytyy sallia matalan tason järjestelmäohjelmointi, kuten suora vuorovaikutus käyttöjärjestelmän kanssa tai jopa oman käyttöjärjestelmän kirjoittaminen. Matalan tason järjestelmäohjelmointi on yksi kielen tavoitteista. Tutkitaan, mitä voimme tehdä unsafe Rustilla ja miten se tehdään.

### Unsafe-supervoimat

Vaihtaaksesi unsafe Rustiin, käytä `unsafe`-avainsanaa ja aloita sitten uusi lohko, joka sisältää unsafe-koodin. Voit tehdä viisi toimintoa unsafe Rustissa, joita et voi tehdä safe Rustissa, ja joita kutsumme _unsafe-supervoimiksi_. Nämä supervoimat sisältävät mahdollisuuden:

- Dereferoida raakaviittaus
- Kutsua unsafe-funktiota tai -metodia
- Käyttää tai muokata muuttuvaa staattista muuttujaa
- Toteuttaa unsafe-traitin
- Käyttää `union`-rakenteen kenttiä

On tärkeää ymmärtää, että `unsafe` ei sammuta lainantarkistinta tai poista käytöstä mitään muita Rustin turvatarkistuksia: jos käytät viittausta unsafe-koodissa, sitä tarkistetaan edelleen. `unsafe`-avainsana antaa sinulle pääsyn vain näihin viiteen ominaisuuteen, joita kääntäjä ei sitten tarkista muistiturvallisuuden osalta. Saat silti jonkin verran turvallisuutta unsafe-lohkon sisällä.

Lisäksi `unsafe` ei tarkoita, että lohkon sisällä oleva koodi olisi välttämättä vaarallista tai että siinä olisi varmasti muistiturvallisuusongelmia: tarkoitus on, että ohjelmoijana varmistat, että `unsafe`-lohkon sisällä oleva koodi käyttää muistia kelvollisella tavalla.

Ihmiset tekevät virheitä, ja virheitä tapahtuu, mutta vaatimalla näiden viiden unsafe-operaation olevan `unsafe`-annotoituissa lohkoissa tiedät, että kaikki muistiturvallisuuteen liittyvät virheet täytyy olla `unsafe`-lohkossa. Pidä `unsafe`-lohkot pieninä; olet kiitollinen myöhemmin, kun tutkit muistibugeja.

Eristääksemme unsafe-koodin mahdollisimman paljon, on parasta sulkea unsafe-koodi turvallisen abstraktion sisään ja tarjota turvallinen API, josta puhumme myöhemmin luvussa tarkastellessamme unsafe-funktioita ja -metodeja. Osa standardikirjastosta on toteutettu turvallisina abstraktioina auditoidun unsafe-koodin päälle. Unsafe-koodin kääriminen turvalliseen abstraktioon estää `unsafe`:n käytön vuotamasta kaikkiin paikkoihin, joissa sinä tai käyttäjäsi saattaisitte haluta käyttää unsafe-koodilla toteutettua toiminnallisuutta, koska turvallisen abstraktion käyttö on turvallista.

Katsotaan kukin viidestä unsafe-supervoimasta vuorollaan. Tarkastelemme myös joitakin abstraktioita, jotka tarjoavat turvallisen rajapinnan unsafe-koodille.

### Raakaviittauksen dereferointi

Luvussa 4 [”Roikkuvat viittaukset”][dangling-references]<!-- ignore --> -osiossa mainitsimme, että kääntäjä varmistaa viittausten olevan aina kelvollisia. Unsafe Rustissa on kaksi uutta tyyppiä nimeltä _raakaviittaukset_, jotka ovat samankaltaisia kuin viittaukset. Kuten viittauksilla, raakaviittaukset voivat olla muuttumattomia tai muutettavia ja kirjoitetaan muodossa `*const T` ja `*mut T`. Asteriski ei ole dereferointioperaattori; se on osa tyypin nimeä. Raakaviittausten yhteydessä _muuttumaton_ tarkoittaa, että osoitinta ei voi suoraan osoittaa dereferoinnin jälkeen.

Toisin kuin viittaukset ja älykkäät osoittimet, raakaviittaukset:

- Voivat jättää huomiotta lainaussäännöt pitämällä sekä muuttumattomia että muutettavia osoittimia tai useita muutettavia osoittimia samaan paikkaan
- Eivät ole taattu osoittamaan kelvollista muistia
- Voivat olla null
- Eivät toteuta automaattista siivousta

Luopumalla Rustin näiden takuujen pakottamisesta voit luopua taatusta turvallisuudesta vastineeksi paremmasta suorituskyvystä tai mahdollisuudesta käyttää toista kieltä tai laitteistoa, jossa Rustin takuut eivät päde.

Listausta 20-1 näyttää, miten luodaan muuttumaton ja muutettava raakaviittaus.

<Listing number="20-1" caption="Raakaviittausten luominen raaka-laina-operaattoreilla">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-01/src/main.rs:here}}
```

</Listing>

Huomaa, ettemme sisällytä `unsafe`-avainsanaa tähän koodiiin. Voimme luoda raakaviittauksia safe-koodissa; emme vain voi dereferoida raakaviittauksia `unsafe`-lohkon ulkopuolella, kuten näet hetken kuluttua.

Olemme luoneet raakaviittauksia käyttämällä raaka-laina-operaattoreita: `&raw const num` luo muuttumattoman raakaviittauksen `*const i32`, ja `&raw mut num` luo muutettavan raakaviittauksen `*mut i32`. Koska loimme ne suoraan paikallisesta muuttujasta, tiedämme näiden tiettyjen raakaviittausten olevan kelvollisia, mutta emme voi olettaa samaa mistä tahansa raakaviittauksesta.

Osoittaaksemme tämän luomme seuraavaksi raakaviittauksen, jonka kelvollisuudesta emme voi olla yhtä varmoja, käyttämällä `as`-operaattoria arvon muuntamiseen raakaviittausoperaattoreiden sijaan. Listausta 20-2 näyttää, miten luodaan raakaviittaus mielivaltaiseen muistipaikkaan. Mielivaltaisen muistin käyttö on määrittelemätöntä: siinä osoitteessa saattaa olla dataa tai ei, kääntäjä saattaa optimoida koodin niin, ettei muistia käytetä lainkaan, tai ohjelma saattaa kaatua segmentointivirheeseen. Yleensä ei ole hyvää syytä kirjoittaa tällaista koodia, varsinkaan kun voit käyttää raaka-laina-operaattoria sen sijaan, mutta se on mahdollista.

<Listing number="20-2" caption="Raakaviittauksen luominen mielivaltaiseen muistiosoitteeseen">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-02/src/main.rs:here}}
```

</Listing>

Muista, että voimme luoda raakaviittauksia safe-koodissa, mutta emme voi _dereferoida_ raakaviittauksia ja lukea osoitettua dataa. Listauksessa 20-3 käytämme dereferointioperaattoria `*` raakaviittauksella, mikä vaatii `unsafe`-lohkon.

<Listing number="20-3" caption="Raakaviittausten dereferointi `unsafe`-lohkossa">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-03/src/main.rs:here}}
```

</Listing>

Osoittimen luominen ei tee haittaa; vasta kun yritämme käyttää arvoa, johon se osoittaa, saatamme joutua käsittelemään virheellistä arvoa.

Huomaa myös, että listauksissa 20-1 ja 20-3 loimme `*const i32`- ja `*mut i32`-raakaviittaukset, jotka molemmat osoittivat samaan muistipaikkaan, jossa `num` on tallennettu. Jos sen sijaan yrittäisimme luoda muuttumattoman ja muutettavan viittauksen `num`:iin, koodi ei olisi kääntynyt, koska Rustin omistajuussäännöt eivät salli muutettavaa viittausta samaan aikaan kuin mitään muuttumattomia viittauksia. Raakaviittauksilla voimme luoda muutettavan ja muuttumattoman osoittimen samaan paikkaan ja muuttaa dataa muutettavan osoittimen kautta, mikä saattaa luoda datakilpailutilanteen. Ole varovainen!

Kaikkien näiden vaarojen vuoksi, miksi käyttäisit koskaan raakaviittauksia? Yksi tärkeä käyttötapaus on C-koodin kanssa vuorovaikutus, kuten näet seuraavassa osiossa [”Unsafe-funktion tai -metodin kutsuminen.”](#calling-an-unsafe-function-or-method)<!-- ignore --> Toinen tapaus on turvallisten abstraktioiden rakentaminen, joita lainantarkistin ei ymmärrä. Esittelemme unsafe-funktiot ja katsomme sitten esimerkkiä turvallisesta abstraktiosta, joka käyttää unsafe-koodia.

### Unsafe-funktion tai -metodin kutsuminen

Toinen operaatiotyyppi, jonka voit suorittaa `unsafe`-lohkossa, on unsafe-funktioiden kutsuminen. Unsafe-funktiot ja -metodit näyttävät täsmälleen samalta kuin tavalliset funktiot ja metodit, mutta niillä on ylimääräinen `unsafe` ennen määrittelyn loppuosaa. Tässä yhteydessä `unsafe`-avainsana osoittaa, että funktiolla on vaatimuksia, jotka meidän täytyy täyttää kutsuessamme tätä funktiota, koska Rust ei voi taata täyttäneemme näitä vaatimuksia. Kutsumalla unsafe-funktiota `unsafe`-lohkossa sanomme, että olemme lukeneet tämän funktion dokumentaation ja otamme vastuun funktion sopimusten täyttämisestä.

Tässä on unsafe-funktio nimeltä `dangerous`, joka ei tee mitään rungossaan:

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-01-unsafe-fn/src/main.rs:here}}
```

Meidän täytyy kutsua `dangerous`-funktiota erillisessä `unsafe`-lohkossa. Jos yritämme kutsua `dangerous`-funktiota ilman `unsafe`-lohkoa, saamme virheen:

```console
{{#include ../listings/ch20-advanced-features/output-only-01-missing-unsafe/output.txt}}
```

`unsafe`-lohkolla vakuutamme Rustille, että olemme lukeneet funktion dokumentaation, ymmärrämme miten sitä käytetään oikein ja olemme varmistaneet täyttävämme funktion sopimuksen.

Suorittaaksesi unsafe-operaatioita unsafe-funktion rungossa, sinun täytyy silti käyttää `unsafe`-lohkoa aivan kuten tavallisen funktion sisällä, ja kääntäjä varoittaa, jos unohdat. Tämä auttaa pitämään `unsafe`-lohkot mahdollisimman pieninä, koska unsafe-operaatioita ei välttämättä tarvita koko funktion rungossa.

#### Turvallisen abstraktion luominen unsafe-koodin päälle

Pelkästään se, että funktio sisältää unsafe-koodia, ei tarkoita, että meidän täytyisi merkitä koko funktio unsafeksi. Itse asiassa unsafe-koodin kääriminen turvalliseen funktioon on yleinen abstraktio. Esimerkkinä tutkitaan standardikirjaston `split_at_mut`-funktiota, joka vaatii unsafe-koodia. Tutkimme, miten voisimme toteuttaa sen. Tämä turvallinen metodi on määritelty muutettaville viipaleille: se ottaa yhden viipaleen ja jakaa sen kahteen jakamalla viipaleen argumenttina annetussa indeksissä. Listausta 20-4 näyttää, miten käyttää `split_at_mut`-funktiota.

<Listing number="20-4" caption="Turvallisen `split_at_mut`-funktion käyttö">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-04/src/main.rs:here}}
```

</Listing>

Emme voi toteuttaa tätä funktiota käyttämällä vain safe Rustia. Yritys saattaisi näyttää listaukselta 20-5, joka ei käänny. Yksinkertaisuuden vuoksi toteutamme `split_at_mut`-funktion funktiona metodin sijaan ja vain `i32`-arvojen viipaleille geneerisen tyypin `T` sijaan.

<Listing number="20-5" caption="Yritys toteuttaa `split_at_mut` käyttämällä vain safe Rustia">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-05/src/main.rs:here}}
```

</Listing>

Tämä funktio saa ensin viipaleen kokonaispituuden. Sitten se varmistaa, että parametrina annettu indeksi on viipaleen sisällä tarkistamalla, onko se pienempi tai yhtä suuri kuin pituus. Väite tarkoittaa, että jos välitämme indeksin, joka on suurempi kuin pituus, jossa viipale jaetaan, funktio panikoi ennen kuin yrittää käyttää kyseistä indeksiä.

Sitten palautamme kaksi muutettavaa viipaletta tuplessa: toinen alkuperäisen viipaleen alusta `mid`-indeksiin ja toinen `mid`:stä viipaleen loppuun.

Kun yritämme kääntää listauksen 20-5 koodin, saamme virheen.

```console
{{#include ../listings/ch20-advanced-features/listing-20-05/output.txt}}
```

Rustin lainantarkistin ei ymmärrä, että lainaamme viipaleen eri osia; se tietää vain, että lainaamme samaa viipaletta kahdesti. Viipaleen eri osien lainaaminen on periaatteessa ok, koska kaksi viipaletta eivät ole päällekkäin, mutta Rust ei ole tarpeeksi älykäs tietääkseen tämän. Kun tiedämme koodin olevan kunnossa, mutta Rust ei tiedä, on aika turvautua unsafe-koodiin.

Listausta 20-6 näyttää, miten käyttää `unsafe`-lohkoa, raakaviittausta ja joitakin unsafe-funktiokutsuja saadaksemme `split_at_mut`-toteutuksen toimimaan.

<Listing number="20-6" caption="Unsafe-koodin käyttö `split_at_mut`-funktion toteutuksessa">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-06/src/main.rs:here}}
```

</Listing>

Muista [”Viipaletyyppi”][the-slice-type]<!-- ignore --> -osio luvusta 4, että viipaleet ovat osoitin dataan ja viipaleen pituus. Käytämme `len`-metodia saadaksemme viipaleen pituuden ja `as_mut_ptr`-metodia päästäksemme viipaleen raakaviittaukseen. Tässä tapauksessa, koska meillä on muutettava viipale `i32`-arvoille, `as_mut_ptr` palauttaa raakaviittauksen tyypillä `*mut i32`, jonka olemme tallentaneet muuttujaan `ptr`.

Pidämme väitteen, että `mid`-indeksi on viipaleen sisällä. Sitten pääsemme unsafe-koodiin: `slice::from_raw_parts_mut`-funktio ottaa raakaviittauksen ja pituuden, ja se luo viipaleen. Käytämme tätä funktiota luodaksemme viipaleen, joka alkaa `ptr`:stä ja on `mid` alkiota pitkä. Sitten kutsumme `add`-metodia `ptr`:llä argumenttina `mid` saadaksemme raakaviittauksen, joka alkaa `mid`:stä, ja luomme viipaleen käyttämällä tuota osoitinta ja jäljellä olevien alkioiden määrää `mid`:n jälkeen pituutena.

Funktio `slice::from_raw_parts_mut` on unsafe, koska se ottaa raakaviittauksen ja täytyy luottaa tämän osoittimen olevan kelvollinen. `add`-metodi raakaviittauksilla on myös unsafe, koska sen täytyy luottaa, että siirtymän kohde on myös kelvollinen osoitin. Siksi meidän täytyi laittaa `unsafe`-lohko `slice::from_raw_parts_mut`- ja `add`-kutsujemme ympärille, jotta voimme kutsua niitä. Katsomalla koodia ja lisäämällä väitteen, että `mid`:n täytyy olla pienempi tai yhtä suuri kuin `len`, voimme todeta, että kaikki `unsafe`-lohkossa käytetyt raakaviittaukset ovat kelvollisia osoittimia dataan viipaleen sisällä. Tämä on hyväksyttävä ja asianmukainen `unsafe`:n käyttö.

Huomaa, ettemme tarvitse merkitä tuloksena olevaa `split_at_mut`-funktiota `unsafe`:ksi, ja voimme kutsua tätä funktiota safe Rustista. Olemme luoneet turvallisen abstraktion unsafe-koodille toteutuksella, joka käyttää `unsafe`-koodia turvallisella tavalla, koska se luo vain kelvollisia osoittimia datasta, johon tämä funktio pääsee käsiksi.

Sitä vastoin `slice::from_raw_parts_mut`-funktion käyttö listauksessa 20-7 kaatuisi todennäköisesti, kun viipaletta käytetään. Tämä koodi ottaa mielivaltaisen muistipaikan ja luo 10 000 alkion viipaleen.

<Listing number="20-7" caption="Viipaleen luominen mielivaltaisesta muistipaikasta">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-07/src/main.rs:here}}
```

</Listing>

Emme omista dataa tässä mielivaltaisessa paikassa, eikä ole takuuta, että tämän koodin luoma viipale sisältää kelvollisia `i32`-arvoja. Yritys käyttää `values`-muuttujaa kelvollisena viipaleena johtaa määrittelemättömään käyttäytymiseen.

#### `extern`-funktioiden käyttö ulkoisen koodin kutsumiseen

Joskus Rust-koodisi saattaa joutua vuorovaikutukseen toisella kielellä kirjoitetun koodin kanssa. Tätä varten Rustissa on `extern`-avainsana, joka helpottaa _ulkomaisen funktion rajapinnan (FFI)_ luomista ja käyttöä. FFI on tapa, jolla ohjelmointikieli määrittelee funktiot ja mahdollistaa eri (ulkomaisen) ohjelmointikielen kutsuman näitä funktioita.

Listausta 20-8 demonstroi integraation asettamista C-standardikirjaston `abs`-funktion kanssa. `extern`-lohkossa määritellyt funktiot ovat yleensä unsafe kutsua Rust-koodista, joten ne täytyy myös merkitä `unsafe`:ksi. Syy on, että muut kielet eivät pakota Rustin sääntöjä ja takuuja, eikä Rust voi tarkistaa niitä, joten vastuu turvallisuudesta on ohjelmoijalla.

<Listing number="20-8" file-name="src/main.rs" caption="Toisella kielellä määritellyn `extern`-funktion julistaminen ja kutsuminen">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-08/src/main.rs}}
```

</Listing>

`unsafe extern "C"` -lohkon sisällä listaamme toisen kielen ulkoisten funktioiden nimet ja allekirjoitukset, joita haluamme kutsua. `"C"`-osa määrittelee, mitä _sovellusbinaarirajapintaa (ABI)_ ulkoinen funktio käyttää: ABI määrittelee, miten funktiota kutsutaan konekielitasolla. `"C"`-ABI on yleisin ja noudattaa C-ohjelmointikielen ABI:tä.

Tällä tietyllä funktiolla ei ole muistiturvallisuusnäkökohtia. Itse asiassa tiedämme, että mikä tahansa `abs`-kutsu on aina turvallinen mille tahansa `i32`:lle, joten voimme käyttää `safe`-avainsanaa sanoaksemme, että tämä tietty funktio on turvallinen kutsua, vaikka se on `unsafe extern` -lohkossa. Kun teemme tuon muutoksen, sen kutsuminen ei enää vaadi `unsafe`-lohkoa, kuten listauksessa 20-9.

<Listing number="20-9" file-name="src/main.rs" caption="Funktion eksplisiittinen merkitseminen `safe`:ksi `unsafe extern` -lohkon sisällä ja sen turvallinen kutsuminen">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-09/src/main.rs}}
```

</Listing>

Funktion merkitseminen `safe`:ksi ei itsessään tee siitä turvallista! Sen sijaan se on kuin lupaus, jonka annat Rustille, että se _on_ turvallinen. Sinun vastuullasi on edelleen varmistaa, että lupaus pidetään!

> #### Rust-funktioiden kutsuminen muista kielistä
>
> Voimme myös käyttää `extern`-avainsanaa rajapinnan luomiseen, joka sallii muiden kielten kutsua Rust-funktioita. Sen sijaan, että loisimme koko `extern`-lohkon, lisäämme `extern`-avainsanan ja määrittelemme käytettävän ABI:n juuri ennen asiaankuuluvan funktion `fn`-avainsanaa. Meidän täytyy myös lisätä `#[unsafe(no_mangle)]`-annotaatio kertoaksemme Rustin kääntäjälle, ettei sen pidä muuttaa tämän funktion nimeä. _Nimen muuttaminen_ tarkoittaa, että kääntäjä muuttaa antamamme funktion nimen eri nimeksi, joka sisältää enemmän tietoa käännösprosessin muille osille mutta on vähemmän ihmisen luettava. Jokainen ohjelmointikielen kääntäjä muuttaa nimiä hieman eri tavalla, joten jotta Rust-funktiota voidaan nimetä muista kielistä, meidän täytyy poistaa Rustin kääntäjän nimen muuttaminen käytöstä. Tämä on unsafe, koska nimiristiriitoja voi syntyä kirjastojen välillä ilman sisäänrakennettua nimen muuttamista, joten vastuullamme on varmistaa, että vientiin käyttämämme nimi on turvallinen viedä ilman nimen muuttamista.
>
> Seuraavassa esimerkissä teemme `call_from_c`-funktion käytettäväksi C-koodista sen jälkeen, kun se on käännetty jaetusta kirjastosta ja linkitetty C:stä:
>
> ```rust
> #[unsafe(no_mangle)]
> pub extern "C" fn call_from_c() {
>     println!("Just called a Rust function from C!");
> }
> ```
>
> Tämä `extern`-käyttö ei vaadi `unsafe`:a.

### Muuttuvan staattisen muuttujan käyttö tai muokkaus

Tässä kirjassa emme ole vielä puhuneet _globaaleista muuttujista_, joita Rust tukee mutta jotka voivat olla ongelmallisia Rustin omistajuussääntöjen kanssa. Jos kaksi säiettä käyttää samaa muuttuvaa globaalia muuttujaa, se voi aiheuttaa datakilpailutilanteen.

Rustissa globaaleja muuttujia kutsutaan _staattisiksi muuttujiksi_. Listausta 20-10 näyttää esimerkin staattisen muuttujan julistamisesta ja käytöstä merkkijonon viipaleen arvona.

<Listing number="20-10" file-name="src/main.rs" caption="Muuttumattoman staattisen muuttujan määrittely ja käyttö">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-10/src/main.rs}}
```

</Listing>

Staattiset muuttujat ovat samankaltaisia kuin vakiot, joita käsittelimme [”Vakiot”][differences-between-variables-and-constants]<!-- ignore --> -osiossa luvussa 3. Staattisten muuttujien nimet ovat käytännön mukaan `SCREAMING_SNAKE_CASE`-muodossa. Staattiset muuttujat voivat tallentaa vain viittauksia `'static`-elinikäparametrilla, mikä tarkoittaa, että Rustin kääntäjä voi selvittää elinikäparametrin emmekä tarvitse annotoida sitä eksplisiittisesti. Muuttumattoman staattisen muuttujan käyttö on turvallista.

Hienovarainen ero vakioiden ja muuttumattomien staattisten muuttujien välillä on, että staattisten muuttujien arvoilla on kiinteä osoite muistissa. Arvon käyttö käyttää aina samoja dataa. Vakioilla sen sijaan sallitaan datan kopiointi aina kun niitä käytetään. Toinen ero on, että staattiset muuttujat voivat olla muutettavia. Muuttuvan staattisen muuttujan käyttö ja muokkaus on _unsafe_. Listausta 20-11 näyttää, miten julistaa, käyttää ja muokata muuttuvaa staattista muuttujaa nimeltä `COUNTER`.

<Listing number="20-11" file-name="src/main.rs" caption="Muuttuvasta staattisesta muuttujasta lukeminen tai siihen kirjoittaminen on unsafe">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-11/src/main.rs}}
```

</Listing>

Kuten tavallisten muuttujien kanssa, määrittelemme muutettavuuden `mut`-avainsanalla. Kaiken koodin, joka lukee tai kirjoittaa `COUNTER`-muuttujaan, täytyy olla `unsafe`-lohkossa. Listauksen 20-11 koodi kääntyy ja tulostaa `COUNTER: 3` kuten odotamme, koska se on yksisäikeinen. Useiden säikeiden käyttö `COUNTER`-muuttujaan johtaisi todennäköisesti datakilpailutilanteisiin, joten se on määrittelemätöntä käyttäytymistä. Siksi meidän täytyy merkitä koko funktio `unsafe`:ksi ja dokumentoida turvallisuusrajoitus, jotta kuka tahansa funktiota kutsuva tietää, mitä saa ja ei saa tehdä turvallisesti.

Aina kun kirjoitamme unsafe-funktion, on idiomaattista kirjoittaa kommentti, joka alkaa `SAFETY`:llä ja selittää, mitä kutsupuolen täytyy tehdä kutsuakseen funktion turvallisesti. Vastaavasti aina kun suoritamme unsafe-operaation, on idiomaattista kirjoittaa kommentti, joka alkaa `SAFETY`:llä selittääksemme, miten turvallisuussäännöt täyttyvät.

Lisäksi kääntäjä ei salli sinun luoda viittauksia muuttuvaan staattiseen muuttujaan. Voit käyttää sitä vain raakaviittauksen kautta, joka on luotu jollakin raaka-laina-operaattoreista. Tämä koskee myös tapauksia, joissa viittaus luodaan näkymättömästi, kuten kun sitä käytetään tämän koodilistan `println!`-kutsussa. Vaatimus, että viittauksia muuttuviin staattisiin muuttujiin voidaan luoda vain raakaviittausten kautta, auttaa tekemään niiden käytön turvallisuusvaatimuksista ilmeisempiä.

Muuttuvan datan kanssa, joka on globaalisti käytettävissä, on vaikea varmistaa, ettei datakilpailutilanteita ole, minkä vuoksi Rust pitää muuttuvia staattisia muuttujia unsafeina. Mahdollisuuksien mukaan on parempi käyttää luvussa 16 käsiteltyjä rinnakkaisuustekniikoita ja säieturvallisia älykkäitä osoittimia, jotta kääntäjä tarkistaa eri säikeistä käytetyn datan turvallisuuden.

### Unsafe-traitin toteuttaminen

Voimme käyttää `unsafe`:a toteuttaaksemme unsafe-traitin. Trait on unsafe, kun vähintään yhdellä sen metodeista on jokin invariantti, jota kääntäjä ei voi varmistaa. Julistamme traitin `unsafe`:ksi lisäämällä `unsafe`-avainsanan ennen `trait`-avainsanaa ja merkitsemme traitin toteutuksen myös `unsafe`:ksi, kuten listauksessa 20-12.

<Listing number="20-12" caption="Unsafe-traitin määrittely ja toteuttaminen">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-12/src/main.rs}}
```

</Listing>

Käyttämällä `unsafe impl`:ia lupaamme, että pidämme yllä invariantteja, joita kääntäjä ei voi varmistaa.

Esimerkkinä muista `Sync`- ja `Send`-merkki-traitit, joita käsittelimme [”Laajennettava rinnakkaisuus `Sync`- ja `Send`-traiteilla”][extensible-concurrency-with-the-sync-and-send-traits]<!-- ignore --> -osiossa luvussa 16: kääntäjä toteuttaa nämä traitit automaattisesti, jos tyypimme koostuvat kokonaan `Send`- ja `Sync`-tyypeistä. Jos toteutamme tyypin, joka sisältää tyypin, joka ei ole `Send` tai `Sync`, kuten raakaviittauksia, ja haluamme merkitä tyypin `Send`- tai `Sync`-tyypiksi, meidän täytyy käyttää `unsafe`:a. Rust ei voi varmistaa, että tyypimme täyttää takuut, joiden mukaan se voidaan turvallisesti lähettää säikeiden välillä tai käyttää useista säikeistä; siksi meidän täytyy tehdä nämä tarkistukset manuaalisesti ja ilmaista se `unsafe`:lla.

### `union`-rakenteen kenttien käyttö

Viimeinen toiminto, joka toimii vain `unsafe`:lla, on `union`-rakenteen kenttien käyttö. `union` on samankaltainen kuin `struct`, mutta vain yhtä julistettua kenttää käytetään tietyssä instanssissa kerrallaan. Unioneja käytetään pääasiassa rajapintaan C-koodin unionien kanssa. Union-kenttien käyttö on unsafe, koska Rust ei voi taata union-instanssissa tällä hetkellä tallennetun datan tyyppiä. Voit lukea lisää unioneista [Rust Reference][reference] -dokumentaatiosta.

### Miri unsafe-koodin tarkistamiseen

Kun kirjoitat unsafe-koodia, saatat haluta tarkistaa, että kirjoittamasi on todella turvallista ja oikein. Yksi parhaista tavoista tehdä se on käyttää [Miriä][miri], virallista Rust-työkalua määrittelemättömän käyttäytymisen havaitsemiseen. Kun taas lainantarkistin on _staattinen_ työkalu, joka toimii käännösaikana, Miri on _dynaaminen_ työkalu, joka toimii ajonaikana. Se tarkistaa koodisi suorittamalla ohjelmasi tai sen testisarjan ja havaitsemalla, kun rikot sääntöjä, joita se ymmärtää Rustin toiminnasta.

Mirin käyttö vaatii Rustin yökohtaisen (nightly) version (josta puhumme lisää [liitteessä G: Miten Rust tehdään ja ”Nightly Rust”][nightly]). Voit asentaa sekä Rustin yökohtaisen version että Miri-työkalun kirjoittamalla `rustup +nightly component add miri`. Tämä ei muuta Rust-versiota, jota projektisi käyttää; se vain lisää työkalun järjestelmääsi, jotta voit käyttää sitä halutessasi. Voit ajaa Mirin projektilla kirjoittamalla `cargo +nightly miri run` tai `cargo +nightly miri test`.

Esimerkkinä siitä, kuinka hyödyllinen tämä voi olla, tarkastele mitä tapahtuu, kun ajamme sitä listauksen 20-11 koodilla:

```console
{{#include ../listings/ch20-advanced-features/listing-20-11/output.txt}}
```

Se huomaa hyödyllisesti ja oikein, että meillä on jaettuja viittauksia muutettavaan dataan, ja varoittaa siitä. Tässä tapauksessa se ei kerro, miten ongelma korjataan, mutta se tarkoittaa, että tiedämme mahdollisen ongelman olevan olemassa ja voimme miettiä, miten varmistaa turvallisuus. Muissa tapauksissa se voi kertoa, että jokin koodi on _varmasti_ väärin, ja antaa suosituksia korjaukseen.

Miri ei havaitse _kaikkea_, mitä saatat tehdä väärin kirjoittaessasi unsafe-koodia. Ensinnäkin, koska se on dynaaminen tarkistus, se havaitsee vain ongelmat koodissa, joka todella suoritetaan. Tämä tarkoittaa, että sinun täytyy käyttää sitä yhdessä hyvien testaustekniikoiden kanssa kasvattaaksesi luottamustasi kirjoittamaasi unsafe-koodiin. Toiseksi se ei kata kaikkia tapoja, joilla koodisi voi olla epäsoundi. Jos Miri _havaitsee_ ongelman, tiedät että siellä on bugi, mutta pelkästään se, ettei Miri _havaitse_ bugia, ei tarkoita ettei ongelmaa olisi. Miri voi kuitenkin havaita paljon. Kokeile ajaa sitä tämän luvun muilla unsafe-koodin esimerkeillä ja katso mitä se sanoo!

### Milloin käyttää unsafe-koodia

Yhden viidestä käsitellystä toiminnosta (supervoimasta) käyttäminen `unsafe`:lla ei ole väärin eikä edes paheksuttavaa. Mutta unsafe-koodin saaminen oikein on hankalampaa, koska kääntäjä ei voi auttaa ylläpitämään muistiturvallisuutta. Kun sinulla on syy käyttää unsafe-koodia, voit tehdä niin, ja eksplisiittinen `unsafe`-annotaatio helpottaa ongelmien lähteen jäljittämistä, kun niitä ilmenee. Aina kun kirjoitat unsafe-koodia, voit käyttää Miriä auttaaksesi olemaan varmempi siitä, että kirjoittamasi koodi noudattaa Rustin sääntöjä.

Paljon syvempää tutkimusta siitä, miten työskennellä tehokkaasti unsafe Rustin kanssa, löydät Rustin virallisesta aiheoppaasta, [Rustonomiconista][nomicon].

[dangling-references]: ch04-02-references-and-borrowing.html#dangling-references
[differences-between-variables-and-constants]: ch03-01-variables-and-mutability.html#constants
[extensible-concurrency-with-the-sync-and-send-traits]: ch16-04-extensible-concurrency-sync-and-send.html#extensible-concurrency-with-the-sync-and-send-traits
[the-slice-type]: ch04-03-slices.html#the-slice-type
[reference]: ../reference/items/unions.html
[miri]: https://github.com/rust-lang/miri
[editions]: appendix-05-editions.html
[nightly]: appendix-07-nightly-rust.html
[nomicon]: https://doc.rust-lang.org/nomicon/
