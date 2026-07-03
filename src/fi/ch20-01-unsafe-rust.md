## Unsafe Rust

Kaikki koodi, josta olemme tähän asti puhuneet, on noudattanut Rustin muistiturvallisuustakuita käännösaikana. Rustissa on kuitenkin toinen, piilossa oleva kieli, joka ei pakota näitä muistiturvallisuustakuita: sitä kutsutaan _unsafe Rustiksi_, ja se toimii kuten tavallinen Rust, mutta antaa meille ylimääräisiä supervoimia.

Unsafe Rust on olemassa, koska luonteeltaan staattinen analyysi on konservatiivista. Kun kääntäjä yrittää selvittää, pitääkö koodi takuista kiinni, on parempi hylätä joitakin kelvollisia ohjelmia kuin hyväksyä joitakin virheellisiä ohjelmia. Vaikka koodi _saattaisi_ olla kunnossa, jos Rust-kääntäjällä ei ole tarpeeksi tietoa olla varma, se hylkää koodin. Näissä tapauksissa voit käyttää unsafe-koodia kertoaksesi kääntäjälle: ”Luota minuun, tiedän mitä teen.” Varo kuitenkin, että käytät unsafe Rustia omalla vastuullasi: jos käytät unsafe-koodia väärin, voi syntyä ongelmia muistiturvattomuuden vuoksi, kuten null-osoittimen dereferoinnin seurauksena.

Toinen syy sille, miksi Rustilla on unsafe-alter ego, on se, että taustalla oleva tietokonelaitteisto on luonnostaan turvaton. Jos Rust ei sallisi unsafe-operaatioita, et voisi tehdä tiettyjä tehtäviä. Rustin täytyy sallia matalan tason järjestelmäohjelmointi, kuten suora vuorovaikutus käyttöjärjestelmän kanssa tai jopa oman käyttöjärjestelmän kirjoittaminen. Matalan tason järjestelmäohjelmointi on yksi kielen tavoitteista. Tutkitaan, mitä unsafe Rustilla voi tehdä ja miten se tehdään.

<!-- Old headings. Do not remove or links may break. -->

<a id="unsafe-superpowers"></a>

### Unsafe-supervoimien käyttö

Siirtyäksesi unsafe Rustiin, käytä `unsafe`-avainsanaa ja aloita uusi lohko, joka sisältää unsafe-koodin. Unsafe Rustissa voit tehdä viisi asiaa, joita et voi tehdä safe Rustissa; kutsumme niitä _unsafe-supervoimiksi_. Näihin supervoimiin kuuluu kyky:

1. Dereferoida raakaosoitin.
1. Kutsua unsafe-funktiota tai -metodia.
1. Käyttää tai muokata muuttuvaa staattista muuttujaa.
1. Toteuttaa unsafe-trait.
1. Käyttää `union`-tyyppien kenttiä.

On tärkeää ymmärtää, että `unsafe` ei poista lainauskääntäjää eikä mitään Rustin muista turvatarkistuksista: jos käytät viitettä unsafe-koodissa, sitä tarkistetaan silti. `unsafe`-avainsana antaa pääsyn vain näihin viiteen ominaisuuteen, joita kääntäjä ei sitten tarkista muistiturvallisuuden osalta. Saat silti jonkin verran turvallisuutta unsafe-lohkon sisällä.

Lisäksi `unsafe` ei tarkoita, että lohkon sisällä oleva koodi olisi välttämättä vaarallista tai että siinä olisi varmasti muistiturvallisuusongelmia: tarkoitus on, että ohjelmoijana varmistat, että `unsafe`-lohkon sisällä oleva koodi käyttää muistia kelvollisella tavalla.

Ihmiset tekevät virheitä, mutta vaatimalla näiden viiden unsafe-operaation olevan `unsafe`-merkityissä lohkoissa tiedät, että muistiturvallisuuteen liittyvät virheet ovat `unsafe`-lohkossa. Pidä `unsafe`-lohkot pieninä; olet kiitollinen myöhemmin, kun tutkit muistivirheitä.

Erottaaksesi unsafe-koodin mahdollisimman paljon, on parasta sulkea se safe-abstraktioon ja tarjota safe-rajapinta; puhumme tästä myöhemmin luvussa, kun tarkastelemme unsafe-funktioita ja -metodeja. Osa standardikirjastosta on toteutettu safe-abstraktioina auditoidun unsafe-koodin päälle. Unsafe-koodin kääriminen safe-abstraktioon estää `unsafe`-käytön leviämästä kaikkiin paikkoihin, joissa sinä tai käyttäjäsi haluatte käyttää unsafe-koodilla toteutettua toiminnallisuutta, koska safe-abstraktion käyttö on turvallista.

Katsotaan kukin viidestä unsafe-supervoimasta vuorollaan. Tarkastelemme myös abstraktioita, jotka tarjoavat turvallisen rajapinnan unsafe-koodille.

### Raakaosoittimen dereferointi

Luvussa 4 [”Ripustuvat viitteet”][dangling-references]<!-- ignore
-->-kohdassa mainitsimme, että kääntäjä varmistaa viitteiden olevan aina kelvollisia. Unsafe Rustissa on kaksi uutta tyyppiä, _raakaosoittimet_, jotka muistuttavat viitteitä. Kuten viitteillä, raakaosoittimet voivat olla muuttumattomia tai muuttuvia, ja ne kirjoitetaan muodossa `*const T` ja `*mut T`. Asteriski ei ole dereferointioperaattori; se on osa tyyppinimeä. Raakaosoittimien kontekstissa _muuttumaton_ tarkoittaa, että osoitinta ei voi suoraan sijoittaa uudelleen dereferoinnin jälkeen.

Toisin kuin viitteet ja älyosoittimet, raakaosoittimet:

- Voivat sivuuttaa lainaussäännöt, kun samassa paikassa on sekä muuttumaton että muuttuva osoitin tai useita muuttuvia osoittimia
- Eivät takaa osoittavan kelvollista muistia
- Voivat olla null
- Eivät toteuta automaattista siivousta

Luopumalla siitä, että Rust pakottaa nämä takuut, voit luopua taatusta turvallisuudesta vastineeksi paremmasta suorituskyvystä tai kyvystä käyttää toista kieltä tai laitteistoa, joissa Rustin takuut eivät päde.

Listaus 20-1 näyttää, miten luodaan muuttumaton ja muuttuva raakaosoitin.

<Listing number="20-1" caption="Raakaosoittimien luominen raakalainaajaoperaattoreilla">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-01/src/main.rs:here}}
```

</Listing>

Huomaa, ettemme sisällytä `unsafe`-avainsanaa tähän koodiin. Raakaosoittimia voi luoda safe-koodissa; emme vain voi dereferoida raakaosoittimia unsafe-lohkon ulkopuolella, kuten näet pian.

Loimme raakaosoittimet raakalainaajaoperaattoreilla: `&raw const num` luo muuttumattoman raakaosoittimen `*const i32`, ja `&raw mut num` luo muuttuvan raakaosoittimen `*mut i32`. Koska loimme ne suoraan paikallisesta muuttujasta, tiedämme näiden raakaosoittimien olevan kelvollisia, mutta emme voi olettaa samaa mistä tahansa raakaosoittimesta.

Todistaaksemme tämän luomme seuraavaksi raakaosoittimen, jonka kelvollisuudesta emme ole yhtä varmoja, käyttämällä `as`-avainsanaa arvon tyypinmuunnokseen raakalainaajaoperaattorin sijaan. Listaus 20-2 näyttää, miten luodaan raakaosoitin mielivalpaiseen muistipaikkaan. Mielivaltaisen muistin käyttö on määrittelemätöntä käyttäytymistä: osoitteessa voi olla dataa tai ei, kääntäjä voi optimoida koodin niin ettei muistia käytetä lainkaan, tai ohjelma voi päättyä segmentation faultiin. Yleensä tällaiselle koodille ei ole hyvää syytä, varsinkaan kun voit käyttää raakalainaajaoperaattoria, mutta se on mahdollista.

<Listing number="20-2" caption="Raakaosoittimen luominen mielivaltaiseen muistiosoitteeseen">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-02/src/main.rs:here}}
```

</Listing>

Muista, että raakaosoittimia voi luoda safe-koodissa, mutta emme voi dereferoida raakaosoittimia ja lukea osoitettua dataa. Listauksessa 20-3 käytämme dereferointioperaattoria `*` raakaosoittimelle, mikä vaatii `unsafe`-lohkon.

<Listing number="20-3" caption="Raakaosoittimien dereferointi `unsafe`-lohkossa">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-03/src/main.rs:here}}
```

</Listing>

Osoittimen luominen ei tee haittaa; ongelma syntyy vasta, kun yritämme käyttää osoittimen arvoa, jolloin voimme joutua käsittelemään virheellistä arvoa.

Huomaa myös, että listauksissa 20-1 ja 20-3 loimme `*const i32`- ja `*mut i32` -raakaosoittimet, jotka molemmat osoittivat samaan muistipaikkaan, jossa `num` on tallennettuna. Jos yrittäisimme luoda muuttumattoman ja muuttuvan viitteen `num`-muuttujaan, koodi ei kääntyisi, koska Rustin omistussäännöt eivät salli muuttuvaa viitettä samanaikaisesti muuttumattomien viitteiden kanssa. Raakaosoittimilla voimme luoda muuttuvan ja muuttumattoman osoittimen samaan paikkaan ja muuttaa dataa muuttuvan osoittimen kautta, mikä voi synnyttää datakilpailun. Ole varovainen!

Kaikkien näiden vaarojen jälkeen, miksi käyttäisit raakaosoittimia? Yksi tärkeä käyttötapaus on vuorovaikutus C-koodin kanssa, kuten näet seuraavassa osiossa. Toinen tapaus on safe-abstraktioiden rakentaminen, joita lainauskääntäjä ei ymmärrä. Esittelemme unsafe-funktiot ja katsomme esimerkin safe-abstraktiosta, joka käyttää unsafe-koodia.

### Unsafe-funktion tai -metodin kutsuminen

Toinen operaatio, jonka voit tehdä unsafe-lohkossa, on unsafe-funktioiden kutsuminen. Unsafe-funktiot ja -metodit näyttävät täsmälleen tavallisilta funktioilta ja -metodeilta, mutta niillä on ylimääräinen `unsafe` ennen määritelmän loppuosaa. Tässä kontekstissa `unsafe` tarkoittaa, että funktiolla on vaatimuksia, jotka meidän täytyy täyttää kutsuessamme sitä, koska Rust ei voi taata niiden täyttymistä. Kutsumalla unsafe-funktiota `unsafe`-lohkossa sanomme, että olemme lukeneet funktion dokumentaation ja otamme vastuun sen sopimusten täyttämisestä.

Tässä on unsafe-funktio nimeltä `dangerous`, joka ei tee rungossaan mitään:

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-01-unsafe-fn/src/main.rs:here}}
```

Meidän täytyy kutsua `dangerous`-funktiota erillisessä `unsafe`-lohkossa. Jos yritämme kutsua `dangerous`-funktiota ilman `unsafe`-lohkoa, saamme virheen:

```console
{{#include ../listings/ch20-advanced-features/output-only-01-missing-unsafe/output.txt}}
```

`unsafe`-lohkossa vakuutamme Rustille, että olemme lukeneet funktion dokumentaation, ymmärrämme sen käytön ja olemme varmistaneet täyttävämme funktion sopimuksen.

Suorittaaksesi unsafe-operaatioita `unsafe`-funktion rungossa, sinun täytyy silti käyttää `unsafe`-lohkoa, kuten tavallisessa funktiossa, ja kääntäjä varoittaa, jos unohdat. Tämä auttaa pitämään `unsafe`-lohkot mahdollisimman pieninä, koska unsafe-operaatioita ei välttämättä tarvita koko funktion rungossa.

#### Turvallinen abstraktio unsafe-koodin päälle

Pelkästään se, että funktio sisältää unsafe-koodia, ei tarkoita, että koko funktio täytyy merkitä unsafeksi. Unsafe-koodin kääriminen safe-funktioon on itse asiassa yleinen abstraktio. Esimerkkinä tutkitaan standardikirjaston `split_at_mut`-funktiota, joka vaatii unsafe-koodia. Tutkimme, miten sen voisi toteuttaa. Tämä safe-metodi on määritelty muuttuville viipaleille: se ottaa yhden viipaleen ja jakaa sen kahteen annetun indeksin kohdalta. Listaus 20-4 näyttää `split_at_mut`-funktion käytön.

<Listing number="20-4" caption="Turvallisen `split_at_mut`-funktion käyttö">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-04/src/main.rs:here}}
```

</Listing>

Emme voi toteuttaa tätä funktiota pelkällä safe Rustilla. Yritys voisi näyttää listaukselta 20-5, joka ei kääntyisi. Yksinkertaisuuden vuoksi toteutamme `split_at_mut`-funktion funktiona eikä metodina ja vain `i32`-viipaleille eikä geneeriselle tyypille `T`.

<Listing number="20-5" caption="Yritys toteuttaa `split_at_mut` pelkällä safe Rustilla">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-05/src/main.rs:here}}
```

</Listing>

Funktio hakee ensin viipaleen kokonaispituuden. Sitten se varmistaa, että parametrina annettu indeksi on viipaleen sisällä tarkistamalla, onko se pienempi tai yhtä suuri kuin pituus. Väite tarkoittaa, että jos annamme indeksin, joka on suurempi kuin pituus, funktio panikoi ennen kuin yrittää käyttää sitä.

Sitten palautamme kaksi muuttuvaa viipaletta monikkona: toinen alkuperäisen viipaleen alusta `mid`-indeksiin ja toinen `mid`-indeksistä viipaleen loppuun.

Kun yritämme kääntää listauksen 20-5 koodin, saamme virheen:

```console
{{#include ../listings/ch20-advanced-features/listing-20-05/output.txt}}
```

Rustin lainauskääntäjä ei ymmärrä, että lainaamme viipaleen eri osia; se tietää vain, että lainaamme samaa viipaletta kahdesti. Viipaleen eri osien lainaaminen on periaatteessa ok, koska viipaleet eivät ole päällekkäin, mutta Rust ei ole tarpeeksi älykäs tietääkseen tämän. Kun tiedämme koodin olevan ok, mutta Rust ei, on aika turvautua unsafe-koodiin.

Listaus 20-6 näyttää, miten `unsafe`-lohkoa, raakaosoitinta ja unsafe-funktiokutsuja käytetään `split_at_mut`-toteutuksessa.

<Listing number="20-6" caption="Unsafe-koodin käyttö `split_at_mut`-funktion toteutuksessa">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-06/src/main.rs:here}}
```

</Listing>

Muista luvun 4 [”Viipaletyyppi”][the-slice-type]<!-- ignore --> -kohdasta, että viipale on osoitin dataan ja viipaleen pituus. Käytämme `len`-metodia viipaleen pituuden hakemiseen ja `as_mut_ptr`-metodia viipaleen raakaosoittimen käyttöön. Tässä tapauksessa, koska meillä on muuttuva viipale `i32`-arvoille, `as_mut_ptr` palauttaa raakaosoittimen tyypillä `*mut i32`, jonka tallensimme muuttujaan `ptr`.

Pidämme väitteen, että `mid`-indeksi on viipaleen sisällä. Sitten tulee unsafe-koodi: `slice::from_raw_parts_mut`-funktio ottaa raakaosoittimen ja pituuden ja luo viipaleen. Käytämme sitä luomaan viipaleen, joka alkaa `ptr`:stä ja on `mid` kohdetta pitkä. Sitten kutsumme `add`-metodia `ptr`:llä argumenttina `mid` saadaksemme raakaosoittimen, joka alkaa kohdasta `mid`, ja luomme viipaleen tuolla osoittimella ja jäljellä olevien kohteiden määrällä `mid`:n jälkeen.

Funktio `slice::from_raw_parts_mut` on unsafe, koska se ottaa raakaosoittimen ja täytyy luottaa osoittimen kelvollisuuteen. Raakaosoittimien `add`-metodi on myös unsafe, koska sen täytyy luottaa siirtymän kohdeosoitteen kelvollisuuteen. Siksi jouduimme laittamaan `unsafe`-lohkon `slice::from_raw_parts_mut`- ja `add`-kutsujen ympärille. Koodia ja väitettä, että `mid` on pienempi tai yhtä suuri kuin `len`, tarkastelemalla voimme päätellä, että kaikki `unsafe`-lohkossa käytetyt raakaosoittimet osoittavat kelvollista dataa viipaleen sisällä. Tämä on hyväksyttävä ja asianmukainen `unsafe`-käyttö.

Huomaa, ettemme tarvitse merkitä tuloksena olevaa `split_at_mut`-funktiota `unsafe`-funktioksi, ja voimme kutsua sitä safe Rustista. Olemme luoneet safe-abstraktion unsafe-koodille toteutuksella, joka käyttää `unsafe`-koodia turvallisesti, koska se luo vain kelvollisia osoittimia datasta, johon funktiolla on pääsy.

Vastakohtana listauksen 20-7 `slice::from_raw_parts_mut`-käyttö todennäköisesti kaataa ohjelman, kun viipaletta käytetään. Tämä koodi ottaa mielivaltaisen muistipaikan ja luo 10 000 kohdetta pitkän viipaleen.

<Listing number="20-7" caption="Viipaleen luominen mielivaltaisesta muistipaikasta">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-07/src/main.rs:here}}
```

</Listing>

Emme omista muistia tässä mielivaltaisessa paikassa, eikä ole takuuta, että luotu viipale sisältää kelvollisia `i32`-arvoja. `values`-viipaleen käyttäminen kuin se olisi kelvollinen viipale johtaa määrittelemättömään käyttäytymiseen.

#### `extern`-funktioiden käyttö ulkoisen koodin kutsumiseen

Joskus Rust-koodisi täytyy vuorovaikuttaa toisella kielellä kirjoitetun koodin kanssa. Tätä varten Rustissa on `extern`-avainsana, joka helpottaa _ulkomaisten funktioiden rajapinnan (FFI)_ luomista ja käyttöä; FFI on tapa, jolla ohjelmointikieli määrittelee funktioita ja sallii toisen (ulkomaisen) ohjelmointikielen kutsua niitä.

Listaus 20-8 näyttää, miten integroidaan C-standardikirjaston `abs`-funktio. `extern`-lohkoissa määriteltyjä funktioita on yleensä unsafe kutsua Rust-koodista, joten `extern`-lohkot täytyy myös merkitä `unsafe`-lohkoiksi. Syy on, että muut kielet eivät pakota Rustin sääntöjä ja takuita, eikä Rust voi tarkistaa niitä, joten turvallisuus on ohjelmoijan vastuulla.

<Listing number="20-8" file-name="src/main.rs" caption="Toisella kielellä määritellyn `extern`-funktion julistaminen ja kutsuminen">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-08/src/main.rs}}
```

</Listing>

`unsafe extern "C"`-lohkossa listaamme ulkoisten funktioiden nimet ja signatuurit, joita haluamme kutsua. `"C"`-osa määrittää, mitä _sovellusbinaarirajapintaa (ABI)_ ulkoinen funktio käyttää: ABI määrittää, miten funktiota kutsutaan assembly-tasolla. `"C"`-ABI on yleisin ja noudattaa C-ohjelmointikielen ABI:a. Tietoa kaikista Rustin tukemista ABI:sta on [Rustin viitteessä][ABI].

Jokainen `unsafe extern`-lohkossa julistettu kohde on implisiittisesti unsafe. Jotkin FFI-funktiot _ovat_ kuitenkin turvallisia kutsua. Esimerkiksi C-standardikirjaston `abs`-funktiolla ei ole muistiturvallisuusnäkökohtia, ja tiedämme sen toimivan millä tahansa `i32`:lla. Tällaisissa tapauksissa voimme käyttää `safe`-avainsanaa sanoaksemme, että tämä funktio on turvallinen kutsua vaikka se on `unsafe extern`-lohkossa. Kun teemme tämän muutoksen, sen kutsuminen ei enää vaadi `unsafe`-lohkoa, kuten listauksessa 20-9.

<Listing number="20-9" file-name="src/main.rs" caption="Funktion eksplisiittinen merkitseminen `safe`-funktioksi `unsafe extern`-lohkossa ja sen turvallinen kutsuminen">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-09/src/main.rs}}
```

</Listing>

Funktion merkitseminen `safe`-funktioksi ei itsessään tee siitä turvallista! Sen sijaan se on lupaus Rustille, että funktio on turvallinen. Sinun vastuullasi on edelleen varmistaa, että lupaus pitää!

#### Rust-funktioiden kutsuminen muista kielistä

Voimme myös käyttää `extern`-avainsanaa luodaksemme rajapinnan, jonka avulla muut kielet voivat kutsua Rust-funktioita. Sen sijaan, että luomme koko `extern`-lohkon, lisäämme `extern`-avainsanan ja määrittelemme käytettävän ABI:n juuri ennen `fn`-avainsanaa kyseiselle funktiolle. Lisäämme myös `#[unsafe(no_mangle)]`-annotaation kertoaksemme Rust-kääntäjälle, ettei sen pidä manglata tämän funktion nimeä. _Manglaus_ tarkoittaa, että kääntäjä muuttaa funktiolle antamamme nimen toiseksi, informatiivisemmaksi mutta vähemmän luettavaksi nimellä, jota muut käännösprosessin osat käyttävät. Jokainen ohjelmointikielen kääntäjä manglaa nimiä hieman eri tavalla, joten jotta Rust-funktiota voisi kutsua muista kielistä, meidän täytyy poistaa Rust-kääntäjän nimen manglaus. Tämä on unsafe, koska ilman sisäänrakennettua manglausta voi syntyä nimikolisioneita kirjastojen välillä, joten vastuullamme on varmistaa, että valitsemamme nimi on turvallinen viedä ilman manglausta.

Seuraavassa esimerkissä teemme `call_from_c`-funktion käytettäväksi C-koodista sen jälkeen, kun se on käännetty jaetulla kirjastolla ja linkitetty C:stä:

```
#[unsafe(no_mangle)]
pub extern "C" fn call_from_c() {
    println!("Just called a Rust function from C!");
}
```

Tämä `extern`-käyttö vaatii `unsafe`-merkinnän vain attribuutissa, ei `extern`-lohkossa.

### Muuttuvan staattisen muuttujan käyttö tai muokkaus

Tässä kirjassa emme ole vielä puhuneet globaaleista muuttujista, joita Rust tukee mutta jotka voivat olla ongelmallisia Rustin omistussääntöjen kanssa. Jos kaksi säiettä käyttää samaa muuttuvaa globaalia muuttujaa, voi syntyä datakilpailu.

Rustissa globaaleja muuttujia kutsutaan _staattisiksi_ muuttujiksi. Listaus 20-10 näyttää esimerkin staattisen muuttujan julistamisesta ja käytöstä, jonka arvo on merkkijonoviipale.

<Listing number="20-10" file-name="src/main.rs" caption="Muuttumattoman staattisen muuttujan määrittely ja käyttö">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-10/src/main.rs}}
```

</Listing>

Staattiset muuttujat muistuttavat vakioita, joista puhuimme luvun 3 [”Vakioiden julistaminen”][constants]<!-- ignore --> -kohdassa. Staattisten muuttujien nimet ovat käytännön mukaan `SCREAMING_SNAKE_CASE`-muodossa. Staattiset muuttujat voivat tallentaa vain viitteitä `'static`-elinaikaisella, mikä tarkoittaa, että Rust-kääntäjä voi päätellä elinaikaisuuden emmekä joudu merkitsemään sitä eksplisiittisesti. Muuttumattoman staattisen muuttujan käyttö on turvallista.

Hienovarainen ero vakioiden ja muuttumattomien staattisten muuttujien välillä on, että staattisen muuttujan arvolla on kiinteä osoite muistissa. Arvon käyttö käyttää aina samaa dataa. Vakioilla sen sijaan dataa saa monistaa aina kun niitä käytetään. Toinen ero on, että staattiset muuttujat voivat olla muuttuvia. Muuttuvan staattisen muuttujan käyttö ja muokkaus on _unsafe_. Listaus 20-11 näyttää, miten julistetaan, käytetään ja muokataan muuttuvaa staattista muuttujaa nimeltä `COUNTER`.

<Listing number="20-11" file-name="src/main.rs" caption="Muuttuvasta staattisesta muuttujasta lukeminen tai siihen kirjoittaminen on unsafe.">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-11/src/main.rs}}
```

</Listing>

Kuten tavallisilla muuttujilla, määrittelemme muuttuvuuden `mut`-avainsanalla. Kaiken `COUNTER`-muuttujaa lukevan tai kirjoittavan koodin täytyy olla `unsafe`-lohkossa. Listauksen 20-11 koodi kääntyy ja tulostaa `COUNTER: 3` odotetusti, koska se on yksisäikeinen. Usean säikeen käyttö `COUNTER`-muuttujalle johtaisi todennäköisesti datakilpailuihin, joten se on määrittelemätöntä käyttäytymistä. Siksi meidän täytyy merkitä koko funktio `unsafe`-funktioksi ja dokumentoida turvallisuusrajoitus, jotta kutsuja tietää, mitä saa ja ei saa tehdä turvallisesti.

Kun kirjoitamme unsafe-funktion, on idiomaattista kirjoittaa kommentti, joka alkaa `SAFETY`-sanalla ja selittää, mitä kutsujan täytyy tehdä kutsuakseen funktion turvallisesti. Vastaavasti kun suoritamme unsafe-operaation, on idiomaattista kirjoittaa kommentti, joka alkaa `SAFETY`-sanalla ja selittää, miten turvallisuussäännöt täyttyvät.

Lisäksi kääntäjä estää oletuksena yritykset luoda viitteitä muuttuvaan staattiseen muuttujaan kääntäjän lintin kautta. Sinun täytyy joko eksplisiittisesti poistua lintin suojauksesta lisäämällä `#[allow(static_mut_refs)]`-annotaatio tai käyttää muuttuvaa staattista muuttujaa raakaosoittimen kautta, joka on luotu raakalainaajaoperaattoreilla. Tämä koskee myös tapauksia, joissa viite luodaan näkymättömästi, kuten tämän listauksen `println!`-makrossa. Vaatimus, että viitteet muuttuviin staattisiin muuttujiin luodaan raakaosoittimien kautta, auttaa tekemään niiden käytön turvallisuusvaatimukset selkeämmiksi.

Globaalisti saatavilla olevan muuttuvan datan kanssa on vaikea varmistaa, ettei datakilpailuja synny, minkä vuoksi Rust pitää muuttuvia staattisia muuttujia unsafeina. Mahdollisuuksien mukaan on parempi käyttää luvussa 16 käsiteltyjä rinnakkaisuustekniikoita ja säieturvallisia älyosoittimia, jotta kääntäjä tarkistaa eri säikeiden datan käytön turvallisuuden.

### Unsafe-traitin toteuttaminen

Voimme käyttää `unsafe`-avainsanaa toteuttaaksemme unsafe-traitin. Trait on unsafe, kun ainakin yhdellä sen metodeista on invariantti, jota kääntäjä ei voi varmistaa. Julistamme traitin `unsafe`-traitiksi lisäämällä `unsafe`-avainsanan ennen `trait`-sanaa ja merkitsemme traitin toteutuksen myös unsafeksi, kuten listauksessa 20-12.

<Listing number="20-12" caption="Unsafe-traitin määrittely ja toteutus">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-12/src/main.rs:here}}
```

</Listing>

Käyttämällä `unsafe impl` lupaamme pitää kiinni invarianteista, joita kääntäjä ei voi varmistaa.

Esimerkkinä muista luvun 16 [”Laajennettava rinnakkaisuus `Send`- ja `Sync`-traiteilla”][send-and-sync]<!-- ignore --> -kohdasta `Send`- ja `Sync`-merkki-traitit: kääntäjä toteuttaa nämä traitit automaattisesti, jos tyypit koostuvat kokonaan muista tyypeistä, jotka toteuttavat `Send`- ja `Sync`-traitit. Jos toteutamme tyypin, joka sisältää tyypin, joka ei toteuta `Send`- tai `Sync`-traitia, kuten raakaosoittimia, ja haluamme merkitä tyypin `Send`- tai `Sync`-tyypiksi, meidän täytyy käyttää `unsafe`-avainsanaa. Rust ei voi varmistaa, että tyypimme täyttää takuut siitä, että sen voi lähettää säikeiden välillä tai käyttää useasta säikeestä; siksi meidän täytyy tehdä tarkistukset manuaalisesti ja ilmaista se `unsafe`-avainsanalla.

### Union-tyypin kenttien käyttö

Viimeinen toiminto, joka toimii vain `unsafe`-koodissa, on union-tyypin kenttien käyttö. _Union_ muistuttaa `struct`-rakennetta, mutta vain yhtä julistettua kenttää käytetään tietyssä instanssissa kerrallaan. Unioneja käytetään pääasiassa C-koodin unionien kanssa vuorovaikutukseen. Union-kenttien käyttö on unsafe, koska Rust ei voi taata, minkä tyyppistä dataa union-instanssissa on tällä hetkellä tallennettuna. Lisätietoa unioneista on [Rustin viitteessä][unions].

### Miri unsafe-koodin tarkistamiseen

Kun kirjoitat unsafe-koodia, saatat haluta varmistaa, että kirjoittamasi on todella turvallista ja oikein. Yksi parhaista tavoista on käyttää Miriä, virallista Rust-työkalua määrittelemättömän käyttäytymisen havaitsemiseen. Lainauskääntäjä on _staattinen_ työkalu, joka toimii käännösaikana, kun taas Miri on _dynaaminen_ työkalu, joka toimii ajonaikana. Se tarkistaa koodin ajamalla ohjelman tai sen testisarjan ja havaitsemalla, kun rikot sääntöjä, joita se ymmärtää Rustin toiminnasta.

Miri vaatii Rustin yöversion (josta puhumme lisää [liitteessä G: Miten Rust tehdään ja ”yö-Rust”][nightly]<!-- ignore -->). Voit asentaa sekä Rustin yöversion että Miri-työkalun komennolla `rustup +nightly component add miri`. Tämä ei muuta projektisi käyttämää Rust-versiota; se vain lisää työkalun järjestelmääsi käytettäväksi tarvittaessa. Voit ajaa Miriä projektilla komennoilla `cargo +nightly miri run` tai `cargo +nightly miri test`.

Esimerkkinä siitä, kuinka hyödyllinen tämä voi olla, katsotaan mitä tapahtuu, kun ajamme sen listauksen 20-7 koodilla.

```console
{{#include ../listings/ch20-advanced-features/listing-20-07/output.txt}}
```

Miri varoittaa oikein, että muunnamme kokonaisluvun osoittimeksi, mikä voi olla ongelma, mutta Miri ei voi päätellä, onko ongelmaa, koska se ei tiedä osoittimen alkuperää. Sitten Miri palauttaa virheen, koska listauksessa 20-7 on määrittelemätöntä käyttäytymistä ripustuvan osoittimen vuoksi. Mirin ansiosta tiedämme nyt, että määrittelemättömän käyttäytymisen riski on olemassa, ja voimme miettiä, miten koodin saa turvalliseksi. Joissakin tapauksissa Miri voi jopa ehdottaa virheiden korjaamista.

Miri ei havaitse kaikkea, mitä unsafe-koodissa voi mennä pieleen. Miri on dynaaminen analyysityökalu, joten se havaitsee vain ongelmat koodissa, joka todella ajetaan. Tämä tarkoittaa, että sinun täytyy käyttää sitä yhdessä hyvien testaustekniikoiden kanssa lisätäksesi luottamusta kirjoittamaasi unsafe-koodiin. Miri ei myöskään kata kaikkia mahdollisia tapoja, joilla koodi voi olla epäluotettavaa.

Toisin sanottuna: jos Miri _havaitsee_ ongelman, tiedät että siellä on bugi, mutta se, että Miri _ei havaitse_ bugia, ei tarkoita ettei ongelmaa olisi. Se voi kuitenkin havaita paljon. Kokeile ajaa sitä tämän luvun muilla unsafe-esimerkeillä ja katso mitä se sanoo!

Lisätietoa Miristä on [sen GitHub-repositoriossa][miri].

<!-- Old headings. Do not remove or links may break. -->

<a id="when-to-use-unsafe-code"></a>

### Unsafe-koodin oikea käyttö

Yhden edellä käsitellyistä viidestä supervoimasta käyttäminen `unsafe`-avainsanalla ei ole väärin eikä edes paheksuttavaa, mutta `unsafe`-koodin saaminen oikein on vaikeampaa, koska kääntäjä ei voi auttaa muistiturvallisuuden ylläpidossa. Kun sinulla on syy käyttää `unsafe`-koodia, voit tehdä niin, ja eksplisiittinen `unsafe`-merkintä helpottaa ongelmien lähteen jäljittämistä. Aina kun kirjoitat unsafe-koodia, voit käyttää Miriä varmistaaksesi luottamuksesi siihen, että koodi noudattaa Rustin sääntöjä.

Paljon syvällisempää tietoa unsafe Rustin tehokkaasta käytöstä löydät Rustin virallisesta `unsafe`-oppaasta, [The Rustonomiconista][nomicon].

[dangling-references]: ch04-02-references-and-borrowing.html#dangling-references
[ABI]: ../reference/items/external-blocks.html#abi
[constants]: ch03-01-variables-and-mutability.html#declaring-constants
[send-and-sync]: ch16-04-extensible-concurrency-sync-and-send.html
[the-slice-type]: ch04-03-slices.html#the-slice-type
[unions]: ../reference/items/unions.html
[miri]: https://github.com/rust-lang/miri
[editions]: appendix-05-editions.html
[nightly]: appendix-07-nightly-rust.html
[nomicon]: https://doc.rust-lang.org/nomicon/
