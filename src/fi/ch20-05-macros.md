## Makrot

Olemme käyttäneet makroja kuten `println!` läpi tämän kirjan, mutta emme ole täysin tutkineet, mikä makro on ja miten se toimii.
Termi _makro_ viittaa Rustin ominaisuusperheeseen: _deklaratiiviset_ makrot `macro_rules!`-rakenteella ja kolmelaista _proseduraalista_ makroa:

- Mukautetut `#[derive]`-makrot, jotka määrittävät `derive`-attribuutilla lisättävän koodin structeille ja enumeille
- Attribuuttimaiset makrot, jotka määrittelevät mukautettuja attribuutteja käytettäviksi millä tahansa kohteella
- Funktiomaiset makrot, jotka näyttävät funktiokutsuilta mutta toimivat argumenteina annetuilla tokeneilla

Käsittelemme jokaisen näistä vuorollaan, mutta ensin katsotaan, miksi tarvitsemme makroja, kun meillä on jo funktiot.

### Ero makrojen ja funktioiden välillä

Pohjimmiltaan makrot ovat tapa kirjoittaa koodia, joka kirjoittaa muuta koodia, mikä tunnetaan nimellä _metaprogrammointi_.
Liitteessä C käsittelemme `derive`-attribuuttia, joka luo erilaisten traitien toteutuksia puolestasi.
Olemme myös käyttäneet `println!`- ja `vec!`-makroja läpi kirjan. Kaikki nämä makrot _laajenevat_ tuottaakseen enemmän koodia
kuin mitä olet kirjoittanut manuaalisesti.

Metaprogrammointi on hyödyllistä vähentämään kirjoitettavan ja ylläpidettävän koodin määrää, mikä on myös yksi funktioiden tehtävistä.
Makroilla on kuitenkin joitakin lisävoimia, joita funktioilla ei ole.

Funktion signatuurissa täytyy ilmoittaa parametrien määrä ja tyyppi. Makrot puolestaan voivat ottaa vaihtelevan määrän parametreja:
voimme kutsua `println!("hello")` yhdellä argumentilla tai `println!("hello {}", name)` kahdella argumentilla.
Lisäksi makrot laajenevat ennen kuin kääntäjä tulkitsee koodin merkityksen, joten makro voi esimerkiksi toteuttaa traitin annetulle tyypille.
Funktio ei voi, koska sitä kutsutaan suorituksen aikana ja trait täytyy toteuttaa käännösaikana.

Makron toteuttamisen haittapuoli funktion sijaan on, että makromäärittelyt ovat monimutkaisempia kuin funktiomäärittelyt,
koska kirjoitat Rust-koodia, joka kirjoittaa Rust-koodia. Tämän epäsuoruuden vuoksi makromäärittelyt ovat yleensä
vaikeampia lukea, ymmärtää ja ylläpitää kuin funktiomäärittelyt.

Toinen tärkeä ero makrojen ja funktioiden välillä on, että makrot täytyy määritellä tai tuoda näkyvyysalueelle _ennen_
kuin kutsut niitä tiedostossa, toisin kuin funktiot, jotka voi määritellä missä tahansa ja kutsua missä tahansa.

### Deklaratiiviset makrot `macro_rules!`-rakenteella yleiseen metaprogrammointiin

Yleisin makrojen muoto Rustissa on _deklaratiivinen makro_. Näitä kutsutaan joskus myös ”makroiksi esimerkin kautta”,
”`macro_rules!`-makroiksi” tai pelkästään ”makroiksi”. Ytimessään deklaratiiviset makrot antavat kirjoittaa jotain,
mikä muistuttaa Rustin `match`-lauseketta. Kuten käsittelimme Luvussa 6, `match`-lausekkeet ovat ohjausrakenteita,
jotka ottavat lausekkeen, vertaavat lausekkeen tulosarvoa kuvioihin ja suorittavat sitten kuvioon liittyvän koodin.
Makrot vertaavat myös arvoa kuhunkin tiettyyn koodiin liittyviin kuvioihin: tässä tilanteessa arvo on makrolle välitetty
kirjaimellinen Rust-lähdekoodi; kuviot verrataan kyseisen lähdekoodin rakenteeseen; ja kuhunkin kuvioon liittyvä koodi,
kun se täsmää, korvaa makrolle välitetyn koodin. Kaikki tämä tapahtuu käännöksen aikana.

Makron määrittelyssä käytetään `macro_rules!`-rakennetta. Tutkitaan `macro_rules!`-rakenteen käyttöä katsomalla,
miten `vec!`-makro on määritelty. Luku 8 käsitteli `vec!`-makron käyttöä uuden vektorin luomiseen tietyillä arvoilla.
Esimerkiksi seuraava makro luo uuden vektorin, joka sisältää kolme kokonaislukua:

```rust
let v: Vec<u32> = vec![1, 2, 3];
```

Voimme käyttää `vec!`-makroa myös kahden kokonaisluvun vektorin tai viiden merkkijonoviipaleen vektorin luomiseen.
Emme voisi tehdä samaa funktiolla, koska emme tietäisi etukäteen arvojen määrää tai tyyppiä.

Listaus 20-29 näyttää hieman yksinkertaistetun `vec!`-makron määrittelyn.

<Listing number="20-29" file-name="src/lib.rs" caption="Yksinkertaistettu versio `vec!`-makron määrittelystä">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-29/src/lib.rs}}
```

</Listing>

> Huom: Standardikirjaston todellinen `vec!`-makron määrittely sisältää koodia oikean muistimäärän varaamiseksi etukäteen.
> Tuo koodi on optimointi, jota emme sisällytä tähän esimerkin yksinkertaistamiseksi.

`#[macro_export]`-annotaatio ilmaisee, että tämä makro tulisi olla käytettävissä aina, kun makron määrittelevä crate tuodaan näkyvyysalueelle.
Ilman tätä annotaatiota makroa ei voi tuoda näkyvyysalueelle.

Aloitamme sitten makromäärittelyn `macro_rules!`-rakenteella ja määrittelemämme makron nimellä _ilman_ huutomerkkiä.
Nimi, tässä tapauksessa `vec`, on seurattu aaltosulkeilla, jotka ilmaisevat makromäärittelyn rungon.

`vec!`-makron rungon rakenne on samanlainen kuin `match`-lausekkeen rakenne. Tässä meillä on yksi haara kuviolla `( $( $x:expr ),* )`,
jota seuraa `=>` ja tähän kuvioon liittyvä koodilohko. Jos kuvio täsmää, siihen liittyvä koodilohko emitoidaan.
Koska tämä on ainoa kuvio tässä makrossa, on vain yksi kelvollinen täsmäystapa; mikä tahansa muu kuvio johtaa virheeseen.
Monimutkaisemmilla makroilla on useampi kuin yksi haara.

Kelvollinen kuviosyntaksi makromäärittelyissä eroaa Luvussa 19 käsitellystä kuviosyntaksista, koska makrokuviot täsmätään
Rust-koodin rakenteeseen arvojen sijaan. Käydään läpi, mitä Listauksen 20-29 kuvion osat tarkoittavat; täydellisestä makrokuviosyntaksista
katso [Rust Reference][ref].

Ensin käytämme sulkeita kattamaan koko kuvion. Käytämme dollarimerkkiä (`$`) ilmoittamaan muuttujan makrojärjestelmässä,
joka sisältää kuvioon täsmäävän Rust-koodin. Dollarimerkki tekee selväksi, että kyseessä on makromuuttuja tavallisen Rust-muuttujan sijaan.
Seuraavaksi tulee sulkeet, jotka kaappaavat arvot, jotka täsmäävät sulkeiden sisällä olevaan kuvioon, korvauskoodin käyttöön.
`$()`-rakenteen sisällä on `$x:expr`, joka täsmää mihin tahansa Rust-lausekkeeseen ja antaa lausekkeelle nimen `$x`.

`$()`-rakenteen jälkeen oleva pilkku ilmaisee, että literaalinen pilkkuerotin täytyy esiintyä jokaisen `$()`-rakenteen sisällä olevaan
koodiin täsmäävän instanssin välissä. `*` määrittää, että kuvio täsmää nolla tai useampaan kertaan siihen, mikä edeltää `*`-merkkiä.

Kun kutsumme tätä makroa `vec![1, 2, 3];`, `$x`-kuvio täsmää kolme kertaa lausekkeisiin `1`, `2` ja `3`.

Katsotaan nyt kuviota tämän haaran rungossa olevan koodin yhteydessä: `temp_vec.push()` `$()*`-rakenteen sisällä generoidaan
jokaiselle `$()`-kuvion osalle, joka täsmää, nolla tai useampi kertaa riippuen siitä, kuinka monta kertaa kuvio täsmää.
`$x` korvataan jokaisella täsmäävällä lausekkeella. Kun kutsumme tätä makroa `vec![1, 2, 3];`, tämän makrokutsun korvaava generoitu koodi on seuraava:

```rust,ignore
{
    let mut temp_vec = Vec::new();
    temp_vec.push(1);
    temp_vec.push(2);
    temp_vec.push(3);
    temp_vec
}
```

Olemme määritelleet makron, joka voi ottaa minkä tahansa määrän argumentteja minkä tahansa tyypin ja generoida koodin vektorin luomiseksi määritellyillä alkioilla.

Opi lisää makrojen kirjoittamisesta verkko-dokumentaatiosta tai muista lähteistä, kuten Daniel Keepin aloittamasta ja Lukas Wirthin jatkamasta
[”The Little Book of Rust Macros”][tlborm] -oppaasta.

### Proseduraaliset makrot koodin generointiin attribuuteista

Makrojen toinen muoto on _proseduraalinen makro_, joka toimii enemmän funktion tavoin (ja on eräänlaista proseduuria).
Proseduraaliset makrot ottavat koodia syötteenä, käsittelevät sitä ja tuottavat koodia tulosteena sen sijaan,
että ne täsmäisivät kuvioihin ja korvaisivat koodin muulla koodilla kuten deklaratiiviset makrot.
Kolme proseduraalisen makron lajia ovat mukautettu derive, attribuuttimainen ja funktiomaiset, ja kaikki toimivat samankaltaisesti.

Proseduraalisia makroja luotaessa määrittelyjen täytyy sijaita omassa cratessaan erityisellä crate-tyypillä.
Tämä johtuu monimutkaisista teknisistä syistä, joita toivomme poistavamme tulevaisuudessa. Listauksessa 20-30 näytämme,
miten proseduraalinen makro määritellään, jossa `some_attribute` on paikkamerkki tietyn makrolajin käytölle.

<Listing number="20-30" file-name="src/lib.rs" caption="Esimerkki proseduraalisen makron määrittelystä">

```rust,ignore
use proc_macro;

#[some_attribute]
pub fn some_name(input: TokenStream) -> TokenStream {
}
```

</Listing>

Proseduraalisen makron määrittelevä funktio ottaa `TokenStream`-tyypin syötteenä ja tuottaa `TokenStream`-tyypin tulosteena.
`TokenStream`-tyyppi on määritelty Rustin mukana tulevassa `proc_macro`-cratessa ja edustaa tokenien jonoa.
Tämä on makron ydin: lähdekoodi, jolla makro toimii, muodostaa syöte-`TokenStream`-tyypin,
ja makron tuottama koodi on tuloste-`TokenStream`-tyyppi. Funktioon on liitetty attribuutti, joka määrittää,
minkälaisen proseduraalisen makron luomme. Samassa cratessa voi olla useita proseduraalisen makron lajeja.

Katsotaan eri proseduraalisen makron lajeja. Aloitamme mukautetulla derive-makrolla ja selitämme sitten pienet erot,
jotka tekevät muista muodoista erilaisia.

### Mukautetun `derive`-makron kirjoittaminen

Luodaan crate nimeltä `hello_macro`, joka määrittelee traitin nimeltä `HelloMacro` yhdellä liitetyllä funktiolla nimeltä `hello_macro`.
Sen sijaan, että pakottaisimme käyttäjiämme toteuttamaan `HelloMacro`-traitin jokaiselle tyypeilleen, tarjoamme proseduraalisen makron,
jotta käyttäjät voivat annotoida tyypin `#[derive(HelloMacro)]`-attribuutilla saadakseen oletustoteutuksen `hello_macro`-funktiolle.
Oletustoteutus tulostaa `Hello, Macro! My name is TypeName!`, jossa `TypeName` on tyypin nimi, jolle tämä trait on määritelty.
Toisin sanoen kirjoitamme craten, joka mahdollistaa toisen ohjelmoijan kirjoittaa Listauksen 20-31 kaltaista koodia käyttäen crateamme.

<Listing number="20-31" file-name="src/main.rs" caption="Koodi, jonka crateamme käyttäjä voi kirjoittaa proseduraalista makroamme käyttäen">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-31/src/main.rs}}
```

</Listing>

Tämä koodi tulostaa `Hello, Macro! My name is Pancakes!`, kun olemme valmiita. Ensimmäinen askel on luoda uusi kirjastocrate näin:

```console
$ cargo new hello_macro --lib
```

Seuraavaksi määrittelemme `HelloMacro`-traitin ja sen liitetyn funktion:

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-20-impl-hellomacro-for-pancakes/hello_macro/src/lib.rs}}
```

</Listing>

Meillä on trait ja sen funktio. Tässä vaiheessa crateamme käyttäjä voisi toteuttaa traitin saavuttaakseen halutun toiminnallisuuden näin:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-20-impl-hellomacro-for-pancakes/pancakes/src/main.rs}}
```

Heidän täytyisi kuitenkin kirjoittaa toteutuslohko jokaiselle tyypille, jota he haluavat käyttää `hello_macro`-funktion kanssa;
haluamme säästää heidät tältä työltä.

Lisäksi emme voi vielä tarjota `hello_macro`-funktiolle oletustoteutusta, joka tulostaisi tyypin nimen, jolle trait on toteutettu:
Rustilla ei ole reflektio-ominaisuuksia, joten se ei voi etsiä tyypin nimeä suorituksen aikana. Tarvitsemme makron generoimaan koodia käännösaikana.

Seuraava askel on määritellä proseduraalinen makro. Kirjoitushetkellä proseduraalisten makrojen täytyy olla omassa cratessaan.
Tämä rajoitus saattaa poistua tulevaisuudessa. Cratejen ja makrocratejen rakentelun käytäntö on seuraava:
crate nimeltä `foo` käyttää mukautetun derive-proseduraalisen makron cratena nimeä `foo_derive`.
Aloitetaan uusi crate nimeltä `hello_macro_derive` `hello_macro`-projektimme sisällä:

```console
$ cargo new hello_macro_derive --lib
```

Kaksi crateamme liittyy tiiviisti toisiinsa, joten luomme proseduraalisen makrocraten `hello_macro`-craten hakemistoon.
Jos muutamme `hello_macro`-craten trait-määrittelyä, meidän täytyy muuttaa myös `hello_macro_derive`-craten proseduraalisen makron toteutusta.
Kaksi cratea täytyy julkaista erikseen, ja näitä crateja käyttävien ohjelmoijien täytyy lisätä molemmat riippuvuuksiksi
ja tuoda molemmat näkyvyysalueelle. Voisimme sen sijaan antaa `hello_macro`-craten käyttää `hello_macro_derive`-cratea riippuvuutena
ja uudelleenviedä proseduraalisen makron koodin. Projektin rakenne kuitenkin mahdollistaa ohjelmoijien käyttää `hello_macro`-cratea,
vaikka he eivät haluaisi `derive`-toiminnallisuutta.

Meidän täytyy ilmoittaa `hello_macro_derive`-crate proseduraalisen makron cratena. Tarvitsemme myös toiminnallisuutta
`syn`- ja `quote`-crateista, kuten näet hetken kuluttua, joten ne täytyy lisätä riippuvuuksiksi. Lisää seuraava
`hello_macro_derive`-craten _Cargo.toml_-tiedostoon:

<Listing file-name="hello_macro_derive/Cargo.toml">

```toml
{{#include ../listings/ch20-advanced-features/listing-20-32/hello_macro/hello_macro_derive/Cargo.toml:6:12}}
```

</Listing>

Aloittaaksesi proseduraalisen makron määrittelyn, sijoita Listauksen 20-32 koodi `hello_macro_derive`-craten _src/lib.rs_-tiedostoon.
Huomaa, että tämä koodi ei käänny, ennen kuin lisäämme määrittelyn `impl_hello_macro`-funktiolle.

<Listing number="20-32" file-name="hello_macro_derive/src/lib.rs" caption="Koodi, jota useimmat proseduraalisen makron cratet tarvitsevat Rust-koodin käsittelyyn">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-32/hello_macro/hello_macro_derive/src/lib.rs}}
```

</Listing>

Huomaa, että olemme jakaneet koodin `hello_macro_derive`-funktioon, joka vastaa `TokenStream`-tyypin jäsentämisestä,
ja `impl_hello_macro`-funktioon, joka vastaa syntaksipuun muuntamisesta: tämä tekee proseduraalisen makron kirjoittamisesta kätevämpää.
Ulomman funktion (`hello_macro_derive` tässä tapauksessa) koodi on sama lähes jokaisessa näkemässäsi tai luomassasi proseduraalisen makron cratessa.
Sisemmän funktion rungossa (`impl_hello_macro` tässä tapauksessa) määrittelemäsi koodi on erilainen proseduraalisen makron tarkoituksen mukaan.

Olemme esitelleet kolme uutta cratea: `proc_macro`, [`syn`] ja [`quote`]. `proc_macro`-crate tulee Rustin mukana,
joten sitä ei tarvinnut lisätä _Cargo.toml_-tiedoston riippuvuuksiin. `proc_macro`-crate on kääntäjän API,
jonka avulla voimme lukea ja käsitellä Rust-koodia omasta koodistamme.

`syn`-crate jäsentää Rust-koodin merkkijonosta tietorakenteeksi, jolla voimme suorittaa operaatioita.
`quote`-crate muuntaa `syn`-tietorakenteet takaisin Rust-koodiksi. Nämä cratet yksinkertaistavat merkittävästi
minkä tahansa Rust-koodin jäsentämistä, jota saatamme haluta käsitellä: täydellisen jäsentimen kirjoittaminen Rust-koodille ei ole yksinkertainen tehtävä.

`hello_macro_derive`-funktiota kutsutaan, kun kirjastomme käyttäjä määrittää `#[derive(HelloMacro)]`-attribuutin tyypille.
Tämä on mahdollista, koska olemme merkinneet `hello_macro_derive`-funktion `proc_macro_derive`-attribuutilla
ja määrittäneet nimen `HelloMacro`, joka vastaa traitimme nimeä; tämä on käytäntö, jota useimmat proseduraaliset makrot noudattavat.

`hello_macro_derive`-funktio muuntaa ensin `input`-arvon `TokenStream`-tyypistä tietorakenteeksi, jota voimme sitten tulkita ja käsitellä.
Tässä `syn` tulee kuvaan. `syn`-craten `parse`-funktio ottaa `TokenStream`-tyypin ja palauttaa `DeriveInput`-structin,
joka edustaa jäsennettyä Rust-koodia. Listaus 20-33 näyttää olennaiset osat `DeriveInput`-structista,
jonka saamme jäsentämällä merkkijonon `struct Pancakes;`:

<Listing number="20-33" caption="`DeriveInput`-instanssi, jonka saamme jäsentäessämme Listauksen 20-31 makroattribuutin sisältävän koodin">

```rust,ignore
DeriveInput {
    // --snip--

    ident: Ident {
        ident: "Pancakes",
        span: #0 bytes(95..103)
    },
    data: Struct(
        DataStruct {
            struct_token: Struct,
            fields: Unit,
            semi_token: Some(
                Semi
            )
        }
    )
}
```

</Listing>

Tämän structin kentät osoittavat, että jäsentämämme Rust-koodi on yksikköstruct tunnisteella (`ident`, tunnistin eli nimi) `Pancakes`.
Structilla on lisää kenttiä erilaisten Rust-koodien kuvaamiseen; katso [`syn`-dokumentaatio `DeriveInput`-structille][syn-docs] lisätietoja.

Määrittelemme pian `impl_hello_macro`-funktion, jossa rakennamme uutta Rust-koodia, jonka haluamme sisällyttää. Ennen sitä huomaa,
että derive-makromme tuloste on myös `TokenStream`-tyyppi. Palautettu `TokenStream`-tyyppi lisätään crateamme käyttäjien kirjoittamaan koodiin,
joten kun he kääntävät craten, he saavat lisätoiminnallisuuden, jonka tarjoamme muokatussa `TokenStream`-tyypissä.

Saatat huomata, että kutsumme `unwrap`-metodia aiheuttaaksemme `hello_macro_derive`-funktion kaatumisen,
jos `syn::parse`-funktion kutsu epäonnistuu tässä. Proseduraalisen makromme täytyy kaatua virheissä,
koska `proc_macro_derive`-funktioiden täytyy palauttaa `TokenStream` `Result`-tyypin sijaan proseduraalisen makron API:n mukaisuuden vuoksi.
Olemme yksinkertaistaneet tämän esimerkin käyttämällä `unwrap`-metodia; tuotantokoodissa sinun pitäisi antaa tarkempia virheilmoituksia
siitä, mikä meni pieleen, käyttämällä `panic!`- tai `expect`-makroa.

Nyt kun meillä on koodi, joka muuntaa annotoidun Rust-koodin `TokenStream`-tyypistä `DeriveInput`-instanssiksi,
generoidaan koodi, joka toteuttaa `HelloMacro`-traitin annotoidulle tyypille, kuten Listauksessa 20-34 näytetään.

<Listing number="20-34" file-name="hello_macro_derive/src/lib.rs" caption="`HelloMacro`-traitin toteuttaminen jäsennetyn Rust-koodin avulla">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-34/hello_macro/hello_macro_derive/src/lib.rs:here}}
```

</Listing>

Saamme `Ident`-struct-instanssin, joka sisältää annotoidun tyypin nimen (tunnisteen), käyttämällä `ast.ident`-kenttää.
Listauksen 20-33 struct osoittaa, että kun ajamme `impl_hello_macro`-funktion Listauksen 20-31 koodille,
saamamme `ident` sisältää `ident`-kentän arvolla `"Pancakes"`. Näin ollen Listauksen 20-34 `name`-muuttuja sisältää `Ident`-struct-instanssin,
joka tulostettaessa on merkkijono `"Pancakes"`, Listauksen 20-31 structin nimi.

`quote!`-makro antaa meidän määritellä Rust-koodin, jonka haluamme palauttaa. Kääntäjä odottaa jotain erilaista kuin `quote!`-makron
suorituksen suora tulos, joten meidän täytyy muuntaa se `TokenStream`-tyypiksi. Teemme tämän kutsumalla `into`-metodia,
joka kuluttaa tämän välisen esityksen ja palauttaa vaaditun `TokenStream`-tyypin arvon.

`quote!`-makro tarjoaa myös erittäin hienoja mallipohjamekaniikkoja: voimme kirjoittaa `#name`, ja `quote!` korvaa sen muuttujan `name` arvolla.
Voit jopa tehdä toistoa samankaltaisesti kuin tavalliset makrot. Katso [quote-craten dokumentaatio][quote-docs] perusteellinen johdanto.

Haluamme proseduraalisen makromme generoivan `HelloMacro`-traitin toteutuksen käyttäjän annotoimalle tyypille, jonka saamme `#name`-rakenteella.
Traitin toteutuksessa on yksi funktio `hello_macro`, jonka runko sisältää tarjoamamme toiminnallisuuden: tulostaa `Hello, Macro! My name is`
ja sitten annotoidun tyypin nimen.

Tässä käytetty `stringify!`-makro on sisäänrakennettu Rustiin. Se ottaa Rust-lausekkeen, kuten `1 + 2`, ja muuntaa lausekkeen käännösaikana
merkkijonoliteraaliksi, kuten `"1 + 2"`. Tämä eroaa `format!`- tai `println!`-makroista, jotka evaluoivat lausekkeen ja muuntavat tuloksen `String`-tyypiksi.
On mahdollista, että `#name`-syöte on lauseke, joka tulostetaan kirjaimellisesti, joten käytämme `stringify!`-makroa.
`stringify!`-makron käyttö säästää myös allokoinnin muuntamalla `#name`:n merkkijonoliteraaliksi käännösaikana.

Tässä vaiheessa `cargo build` pitäisi onnistua sekä `hello_macro`- että `hello_macro_derive`-crateissa. Kytketään nämä cratet
Listauksen 20-31 koodiin nähdäksemme proseduraalisen makron toiminnassa! Luo uusi binääriprojekti _projects_-hakemistoosi
komennolla `cargo new pancakes`. Meidän täytyy lisätä `hello_macro` ja `hello_macro_derive` riippuvuuksiksi `pancakes`-craten _Cargo.toml_-tiedostoon.
Jos julkaiset `hello_macro`- ja `hello_macro_derive`-versiosi [crates.io](https://crates.io/)-sivustolle, ne olisivat tavallisia riippuvuuksia;
jos et, voit määrittää ne `path`-riippuvuuksiksi seuraavasti:

```toml
{{#include ../listings/ch20-advanced-features/no-listing-21-pancakes/pancakes/Cargo.toml:7:9}}
```

Sijoita Listauksen 20-31 koodi _src/main.rs_-tiedostoon ja aja `cargo run`: sen pitäisi tulostaa `Hello, Macro! My name is Pancakes!`
`HelloMacro`-traitin toteutus proseduraalisesta makrosta sisällytettiin ilman, että `pancakes`-craten täytyi toteuttaa sitä;
`#[derive(HelloMacro)]` lisäsi traitin toteutuksen.

Seuraavaksi tutkitaan, miten muut proseduraalisen makron lajit eroavat mukautetuista derive-makroista.

### Attribuuttimaiset makrot

Attribuuttimaiset makrot ovat samanlaisia kuin mukautetut derive-makrot, mutta sen sijaan, että ne generoisivat koodia `derive`-attribuutille,
ne antavat luoda uusia attribuutteja. Ne ovat myös joustavampia: `derive` toimii vain structeille ja enumeille;
attribuutteja voi soveltaa myös muihin kohteisiin, kuten funktioihin. Tässä on esimerkki attribuuttimaisen makron käytöstä:
oletetaan, että sinulla on `route`-niminen attribuutti, joka annotoi funktioita web-sovelluskehyksen käytössä:

```rust,ignore
#[route(GET, "/")]
fn index() {
```

Tämä `#[route]`-attribuutti olisi kehyksen määrittelemä proseduraalinen makro. Makromäärittelyfunktion signatuuri näyttäisi tältä:

```rust,ignore
#[proc_macro_attribute]
pub fn route(attr: TokenStream, item: TokenStream) -> TokenStream {
```

Tässä meillä on kaksi `TokenStream`-tyypin parametria. Ensimmäinen on attribuutin sisällölle: `GET, "/"` -osa.
Toinen on kohteen runko, johon attribuutti on liitetty: tässä tapauksessa `fn index() {}` ja funktion rungon loppuosa.

Muuten attribuuttimaiset makrot toimivat samalla tavalla kuin mukautetut derive-makrot: luot craten `proc-macro`-crate-tyypillä
ja toteutat funktion, joka generoi haluamasi koodin!

### Funktiomaiset makrot

Funktiomaiset makrot määrittelevät makroja, jotka näyttävät funktiokutsuilta. Samankaltaisesti kuin `macro_rules!`-makrot,
ne ovat joustavampia kuin funktiot; esimerkiksi ne voivat ottaa tuntemattoman määrän argumentteja. `macro_rules!`-makroja voi kuitenkin
määritellä vain käyttämällä aiemmin käsittelemäämme `match`-tyylistä syntaksia
[”Deklaratiiviset makrot `macro_rules!`-rakenteella yleiseen metaprogrammointiin”][decl]<!-- ignore --> -osiossa.
Funktiomaiset makrot ottavat `TokenStream`-parametrin, ja niiden määrittely käsittelee tuota `TokenStream`-tyyppiä Rust-koodilla
samalla tavalla kuin muut kaksi proseduraalisen makron tyyppiä. Esimerkki funktiomaisesta makrosta on `sql!`-makro,
jota voisi kutsua näin:

```rust,ignore
let sql = sql!(SELECT * FROM posts WHERE id=1);
```

Tämä makro jäsentäisi sen sisällä olevan SQL-lausekkeen ja tarkistaisi, että se on syntaktisesti oikein, mikä on paljon monimutkaisempaa
käsittelyä kuin `macro_rules!`-makro pystyy tekemään. `sql!`-makro määriteltäisiin näin:

```rust,ignore
#[proc_macro]
pub fn sql(input: TokenStream) -> TokenStream {
```

Tämä määrittely on samanlainen kuin mukautetun derive-makron signatuuri: saamme sulkeiden sisällä olevat tokenit ja palautamme generoimamme koodin.

## Yhteenveto

Huh! Nyt sinulla on työkalupakissa joitakin Rust-ominaisuuksia, joita et todennäköisesti käytä usein,
mutta tiedät, että ne ovat saatavilla hyvin erityisissä tilanteissa. Olemme esitelleet useita monimutkaisia aiheita,
jotta kun kohtaat niitä virheilmoitusten ehdotuksissa tai muiden ihmisten koodissa, tunnistat nämä käsitteet ja syntaksin.
Käytä tätä lukua viitteenä ratkaisujen löytämiseen.

Seuraavaksi otamme käyttöön kaiken, mitä olemme käsitelleet läpi kirjan, ja teemme vielä yhden projektin!

[ref]: ../reference/macros-by-example.html
[tlborm]: https://veykril.github.io/tlborm/
[`syn`]: https://crates.io/crates/syn
[`quote`]: https://crates.io/crates/quote
[syn-docs]: https://docs.rs/syn/2.0/syn/struct.DeriveInput.html
[quote-docs]: https://docs.rs/quote
[decl]: #declarative-macros-with-macro_rules-for-general-metaprogramming
