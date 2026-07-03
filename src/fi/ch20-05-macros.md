## Makrot

Olemme käyttäneet makroja kuten `println!` koko kirjan ajan, mutta emme ole täysin tutkineet, mikä makro on ja miten se toimii. Termi _makro_ viittaa Rustin ominaisuusperheeseen — deklaratiivisiin makroihin `macro_rules!`-avainsanalla ja kolmeen proseduraalisen makron lajiin:

- Mukautetut `#[derive]`-makrot, jotka määrittävät `derive`-attribuutilla lisättävän koodin rakenteille ja luettelotyypeille
- Attribuuttimaiset makrot, jotka määrittelevät mukautettuja attribuutteja käytettäväksi millä tahansa kohteella
- Funktiomaiset makrot, jotka näyttävät funktiokutsuilta mutta toimivat argumenttina annetuilla tokeneilla

Käsittelemme kukin näistä vuorollaan, mutta ensin katsotaan, miksi tarvitsemme makroja, kun meillä on jo funktiot.

### Ero makrojen ja funktioiden välillä

Pohjimmiltaan makrot ovat tapa kirjoittaa koodia, joka kirjoittaa muuta koodia; tätä kutsutaan _metaprogrammoinniksi_. Liitteessä C käsittelemme `derive`-attribuuttia, joka luo eri traitien toteutuksia puolestasi. Olemme myös käyttäneet `println!`- ja `vec!`-makroja koko kirjan ajan. Kaikki nämä makrot _laajenevat_ tuottaakseen enemmän koodia kuin mitä olet kirjoittanut manuaalisesti.

Metaprogrammointi on hyödyllistä vähentämään kirjoitettavan ja ylläpidettävän koodin määrää, mikä on myös yksi funktioiden rooleista. Makroilla on kuitenkin lisävoimia, joita funktioilla ei ole.

Funktiosignatuurissa täytyy julistaa funktion parametrien määrä ja tyypit. Makrot sen sijaan voivat ottaa muuttuvan määrän parametreja: voimme kutsua `println!("hello")` yhdellä argumentilla tai `println!("hello {}", name)` kahdella argumentilla. Lisäksi makrot laajennetaan ennen kuin kääntäjä tulkitsee koodin merkityksen, joten makro voi esimerkiksi toteuttaa traitin tietylle tyypille. Funktio ei voi, koska sitä kutsutaan ajonaikana ja trait täytyy toteuttaa käännösaikana.

Makron toteuttamisen haittapuoli funktion sijaan on, että makromääritelmät ovat monimutkaisempia kuin funktiomääritelmät, koska kirjoitat Rust-koodia, joka kirjoittaa Rust-koodia. Tämän epäsuoran viittauksen vuoksi makromääritelmiä on yleensä vaikeampi lukea, ymmärtää ja ylläpitää kuin funktiomääritelmiä.

Toinen tärkeä ero makrojen ja funktioiden välillä on, että makrot täytyy määritellä tai tuoda näkyvyysalueelle _ennen_ kuin kutsut niitä tiedostossa, toisin kuin funktiot, jotka voi määritellä missä tahansa ja kutsua missä tahansa.

<!-- Old headings. Do not remove or links may break. -->

<a id="declarative-macros-with-macro_rules-for-general-metaprogramming"></a>

### Deklaratiiviset makrot yleiseen metaprogrammointiin

Yleisin makrojen muoto Rustissa on _deklaratiivinen makro_. Niitä kutsutaan joskus myös ”makroiksi esimerkin mukaan”, ”`macro_rules!`-makroiksi” tai yksinkertaisesti ”makroiksi”. Ytimessään deklaratiiviset makrot sallivat kirjoittaa jotain, mikä muistuttaa Rustin `match`-lauseketta. Kuten luvussa 6 käsiteltiin, `match`-lausekkeet ovat ohjausrakenteita, jotka ottavat lausekkeen, vertaavat lausekkeen tulosarvoa kuvioihin ja suorittavat sitten kuvioon liittyvän koodin. Makrot vertaavat myös arvoa kuvioihin, joihin liittyy tietty koodi: tässä tilanteessa arvo on makrolle välitetty kirjaimellinen Rust-lähdekoodi; kuviot verrataan kyseisen lähdekoodin rakenteeseen; ja kuhunkin kuvioon liittyvä koodi korvaa makrolle välitetyn koodin, kun kuvio täsmää. Kaikki tämä tapahtuu käännöksen aikana.

Makron määrittelyssä käytetään `macro_rules!`-rakennetta. Tutkitaan `macro_rules!`-käyttöä katsomalla, miten `vec!`-makro on määritelty. Luvussa 8 käsittelimme `vec!`-makron käyttöä uuden vektorin luomiseen tietyillä arvoilla. Esimerkiksi seuraava makro luo uuden vektorin, joka sisältää kolme kokonaislukua:

```rust
let v: Vec<u32> = vec![1, 2, 3];
```

Voisimme käyttää `vec!`-makroa myös kahden kokonaisluvun vektorin tai viiden merkkijonoviipaleen vektorin luomiseen. Emme voisi tehdä samaa funktiolla, koska emme tietäisi etukäteen arvojen määrää tai tyyppiä.

Listaus 20-35 näyttää hieman yksinkertaistetun `vec!`-makron määritelmän.

<Listing number="20-35" file-name="src/lib.rs" caption="Yksinkertaistettu `vec!`-makron määritelmä">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-35/src/lib.rs}}
```

</Listing>

> Huom: Standardikirjaston todellinen `vec!`-makron määritelmä sisältää koodia oikean muistimäärän varaamiseksi etukäteen. Tämä koodi on optimointi, jota emme sisällytä tähän esimerkin yksinkertaistamiseksi.

`#[macro_export]`-annotaatio osoittaa, että tämä makro tulisi olla käytettävissä aina, kun makron määrittelevä krate tuodaan näkyvyysalueelle. Ilman tätä annotaatiota makroa ei voi tuoda näkyvyysalueelle.

Aloitamme makromääritelmän `macro_rules!`-avainsanalla ja määrittelemämme makron nimellä _ilman_ huutomerkkiä. Nimeä, tässä tapauksessa `vec`, seuraa aaltosulkeet, jotka merkitsevät makromääritelmän runkoa.

`vec!`-rungon rakenne muistuttaa `match`-lausekkeen rakennetta. Tässä on yksi haara kuviolla `( $( $x:expr ),* )`, jota seuraa `=>` ja tähän kuvioon liittyvä koodilohko. Jos kuvio täsmää, siihen liittyvä koodilohko emitoidaan. Koska tämä on ainoa kuvio tässä makrossa, on vain yksi kelvollinen täsmäystapa; mikä tahansa muu kuvio johtaa virheeseen. Monimutkaisemmilla makroilla on useampia haaroja.

Kelvollinen kuviosyntaksi makromääritelmissä eroaa luvussa 19 käsitellystä kuviosyntaksista, koska makrokuviot täsmätään Rust-koodin rakenteeseen eikä arvoihin. Käydään läpi, mitä listauksen 20-35 kuvion osat tarkoittavat; täydellisestä makrokuviosyntaksista katso [Rustin viite][ref].

Ensin käytämme sulkeita koko kuvion ympärillä. Käytämme dollarimerkkiä (`$`) julistaaksemme muuttujan makrojärjestelmässä, joka sisältää kuvioon täsmäävän Rust-koodin. Dollarimerkki tekee selväksi, että kyseessä on makromuuttuja eikä tavallinen Rust-muuttuja. Seuraavaksi tulee sulkeet, jotka sieppaavat kuvioon täsmäävät arvot käytettäväksi korvaavassa koodissa. `$()`-sisällä on `$x:expr`, joka täsmää mihin tahansa Rust-lausekkeeseen ja antaa lausekkeelle nimen `$x`.

`$()`-jälkeinen pilkku osoittaa, että jokaisen `$()`-sisällön täsmäävän koodin instanssin välissä täytyy olla kirjaimellinen pilkkuerotin. `*` määrittää, että kuvio täsmää nolla tai useampaan edeltävään osaan.

Kun kutsumme tätä makroa `vec![1, 2, 3];`-kutsulla, `$x`-kuvio täsmää kolme kertaa lausekkeisiin `1`, `2` ja `3`.

Katsotaan nyt tähän haaraan liittyvän rungon kuviota: `temp_vec.push()` `$()*`-sisällä generoidaan jokaiselle `$()`-kuvioon täsmäävälle osalle nolla tai useamman kerran riippuen siitä, montako kertaa kuvio täsmää. `$x` korvataan jokaisella täsmäävällä lausekkeella. Kun kutsumme tätä makroa `vec![1, 2, 3];`-kutsulla, tämän makrokutsun korvaava generoitu koodi on seuraava:

```rust,ignore
{
    let mut temp_vec = Vec::new();
    temp_vec.push(1);
    temp_vec.push(2);
    temp_vec.push(3);
    temp_vec
}
```

Olemme määritelleet makron, joka voi ottaa minkä tahansa määrän argumentteja minkä tahansa tyypillä ja generoida koodin vektorin luomiseksi määritellyillä elementeillä.

Lisätietoa makrojen kirjoittamisesta löydät verkkodokumentaatiosta tai muista lähteistä, kuten Daniel Keepin aloittamasta ja Lukas Wirthin jatkamasta [”The Little Book of Rust Macros”][tlborm] -oppaasta.

### Proseduraaliset makrot koodin generointiin attribuuteista

Makrojen toinen muoto on proseduraalinen makro, joka toimii enemmän kuin funktio (ja on eräänlaista proseduuria). _Proseduraaliset makrot_ ottavat koodia syötteenä, käsittelevät sitä ja tuottavat koodia tulosteena sen sijaan, että täsmäisivät kuvioihin ja korvaisivat koodin muulla koodilla kuten deklaratiiviset makrot. Kolme proseduraalisen makron lajia ovat mukautettu `derive`, attribuuttimainen ja funktiomainen, ja ne kaikki toimivat samankaltaisesti.

Proseduraalisia makroja luodessa määritelmien täytyy sijaita omassa kratessaan erityisellä kratetyypillä. Tämä johtuu monimutkaisista teknisistä syistä, joita toivomme poistavamme tulevaisuudessa. Listauksessa 20-36 näytämme, miten proseduraalinen makro määritellään, jossa `some_attribute` on paikkamerkki tietyn makrolajin käytölle.

<Listing number="20-36" file-name="src/lib.rs" caption="Esimerkki proseduraalisen makron määrittelystä">

```rust,ignore
use proc_macro::TokenStream;

#[some_attribute]
pub fn some_name(input: TokenStream) -> TokenStream {
}
```

</Listing>

Proseduraalisen makron määrittelevä funktio ottaa `TokenStream`-syötteen ja tuottaa `TokenStream`-tulosteen. `TokenStream`-tyyppi on määritelty Rustin mukana tulevassa `proc_macro`-kratessa ja edustaa tokenien jonoa. Tämä on makron ydin: makron käsittelemä lähdekoodi muodostaa syöte-`TokenStream`-arvon, ja makron tuottama koodi on tuloste-`TokenStream`. Funktioon on liitetty myös attribuutti, joka määrittää, minkä lajista proseduraalista makroa luomme. Samassa kratessa voi olla useita proseduraalisen makron lajeja.

Katsotaan eri proseduraalisen makron lajeja. Aloitamme mukautetulla `derive`-makrolla ja selitämme sitten pienet erot, jotka tekevät muista lajeista erilaisia.

<!-- Old headings. Do not remove or links may break. -->

<a id="how-to-write-a-custom-derive-macro"></a>

### Mukautetut `derive`-makrot

Luodaan krate nimeltä `hello_macro`, joka määrittelee traitin nimeltä `HelloMacro` yhdellä assosioituneella funktiolla nimeltä `hello_macro`. Sen sijaan, että pakottaisimme käyttäjät toteuttamaan `HelloMacro`-traitin jokaiselle tyypeilleen, tarjoamme proseduraalisen makron, jotta käyttäjät voivat merkitä tyypin attribuutilla `#[derive(HelloMacro)]` saadakseen oletustoteutuksen `hello_macro`-funktiolle. Oletustoteutus tulostaa `Hello, Macro! My name is TypeName!`, jossa `TypeName` on tyyppi, jolle trait on määritelty. Toisin sanoen kirjoitamme kraten, jonka avulla toinen ohjelmoija voi kirjoittaa listauksen 20-37 kaltaista koodia käyttäen kratettamme.

<Listing number="20-37" file-name="src/main.rs" caption="Koodi, jonka kratettamme käyttäjä voi kirjoittaa proseduraalista makroamme käyttäen">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-37/src/main.rs}}
```

</Listing>

Tämä koodi tulostaa `Hello, Macro! My name is Pancakes!`, kun olemme valmiita. Ensimmäinen askel on luoda uusi kirjastokrate näin:

```console
$ cargo new hello_macro --lib
```

Seuraavaksi listauksessa 20-38 määrittelemme `HelloMacro`-traitin ja sen assosioituneen funktion.

<Listing file-name="src/lib.rs" number="20-38" caption="Yksinkertainen trait, jota käytämme `derive`-makron kanssa">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-38/hello_macro/src/lib.rs}}
```

</Listing>

Meillä on trait ja sen funktio. Tässä vaiheessa kratettamme käyttäjä voisi toteuttaa traitin saavuttaakseen halutun toiminnallisuuden, kuten listauksessa 20-39.

<Listing number="20-39" file-name="src/main.rs" caption="Miltä näyttäisi, jos käyttäjät kirjoittaisivat `HelloMacro`-traitin manuaalisen toteutuksen">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-39/pancakes/src/main.rs}}
```

</Listing>

Heidän täytyisi kuitenkin kirjoittaa toteutuslohko jokaiselle tyypille, jota haluavat käyttää `hello_macro`-funktion kanssa; haluamme säästää heidät tältä työltä.

Lisäksi emme voi vielä tarjota `hello_macro`-funktiolle oletustoteutusta, joka tulostaisi tyypin nimen, jolle trait on toteutettu: Rustilla ei ole reflektio-ominaisuuksia, joten se ei voi hakea tyypin nimeä ajonaikana. Tarvitsemme makron generoimaan koodia käännösaikana.

Seuraava askel on määritellä proseduraalinen makro. Kirjoitushetkellä proseduraalisten makrojen täytyy olla omassa kratessaan. Tämä rajoitus saattaa poistua tulevaisuudessa. Kratien ja makrokratien rakentelun käytäntö on seuraava: kratelle nimeltä `foo` mukautettu `derive`-proseduraalinen makrokrate kutsutaan `foo_derive`. Aloitetaan uusi krate nimeltä `hello_macro_derive` `hello_macro`-projektimme sisällä:

```console
$ cargo new hello_macro_derive --lib
```

Kaksi kratettamme ovat tiiviisti sidoksissa, joten luomme proseduraalisen makrokrateen `hello_macro`-kraten hakemistoon. Jos muutamme `hello_macro`-kraten trait-määritelmää, meidän täytyy muuttaa myös `hello_macro_derive`-kraten proseduraalisen makron toteutusta. Kaksi kratetta täytyy julkaista erikseen, ja näitä kratteja käyttävien ohjelmoijien täytyy lisätä molemmat riippuvuuksiksi ja tuoda ne näkyvyysalueelle. Voisimme sen sijaan tehdä `hello_macro`-kratesta riippuvaisen `hello_macro_derive`-kratesta ja uudelleenviedä proseduraalisen makron koodin. Tämä projektirakenne kuitenkin mahdollistaa `hello_macro`-kraten käytön, vaikka käyttäjä ei haluaisi `derive`-toiminnallisuutta.

Meidän täytyy julistaa `hello_macro_derive`-krate proseduraaliseksi makrokrateeksi. Tarvitsemme myös toiminnallisuutta `syn`- ja `quote`-krateista, kuten näet pian, joten meidän täytyy lisätä ne riippuvuuksiksi. Lisää seuraava `hello_macro_derive`-kraten _Cargo.toml_-tiedostoon:

<Listing file-name="hello_macro_derive/Cargo.toml">

```toml
{{#include ../listings/ch20-advanced-features/listing-20-40/hello_macro/hello_macro_derive/Cargo.toml:6:12}}
```

</Listing>

Aloittaaksesi proseduraalisen makron määrittelyn, laita listauksen 20-40 koodi `hello_macro_derive`-kraten _src/lib.rs_-tiedostoon. Huomaa, että tämä koodi ei kääntyisi ennen kuin lisäät määritelmän `impl_hello_macro`-funktiolle.

<Listing number="20-40" file-name="hello_macro_derive/src/lib.rs" caption="Koodi, jota useimmat proseduraaliset makrokratet tarvitsevat Rust-koodin käsittelyyn">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-40/hello_macro/hello_macro_derive/src/lib.rs}}
```

</Listing>

Huomaa, että olemme jakaneet koodin `hello_macro_derive`-funktioon, joka vastaa `TokenStream`-arvon jäsentämisestä, ja `impl_hello_macro`-funktioon, joka vastaa syntaksipuun muuntamisesta: tämä tekee proseduraalisen makron kirjoittamisesta kätevämpää. Ulomman funktion (`hello_macro_derive` tässä tapauksessa) koodi on sama lähes jokaisessa näkemässäsi tai luomassasi proseduraalisessa makrokrateessa. Sisemmän funktion (`impl_hello_macro` tässä tapauksessa) rungon koodi on erilainen proseduraalisen makron tarkoituksen mukaan.

Olemme tuoneet kolme uutta kratetta: `proc_macro`, [`syn`][syn]<!-- ignore --> ja [`quote`][quote]<!-- ignore -->. `proc_macro`-krate tulee Rustin mukana, joten emme tarvinneet lisätä sitä _Cargo.toml_-tiedoston riippuvuuksiin. `proc_macro`-krate on kääntäjän API, jonka avulla voimme lukea ja käsitellä Rust-koodia omasta koodistamme.

`syn`-krate jäsentää Rust-koodia merkkijonosta tietorakenteeksi, jolla voimme suorittaa operaatioita. `quote`-krate muuntaa `syn`-tietorakenteet takaisin Rust-koodiksi. Nämä kratet tekevät paljon yksinkertaisemmaksi jäsentää mitä tahansa Rust-koodia, jota haluamme käsitellä: täydellisen Rust-koodin parserin kirjoittaminen ei ole yksinkertainen tehtävä.

`hello_macro_derive`-funktiota kutsutaan, kun kirjastomme käyttäjä määrittää `#[derive(HelloMacro)]` tyypille. Tämä on mahdollista, koska olemme merkinneet `hello_macro_derive`-funktion `proc_macro_derive`-attribuutilla ja määrittäneet nimen `HelloMacro`, joka vastaa traitimme nimeä; tämä on käytäntö, jota useimmat proseduraaliset makrot noudattavat.

`hello_macro_derive`-funktio muuntaa ensin `input`-arvon `TokenStream`-tyypistä tietorakenteeksi, jota voimme sitten tulkita ja käsitellä. Tässä `syn` tulee mukaan. `syn`-kraten `parse`-funktio ottaa `TokenStream`-arvon ja palauttaa `DeriveInput`-rakenteen, joka edustaa jäsennettyä Rust-koodia. Listaus 20-41 näyttää oleelliset osat `DeriveInput`-rakenteesta, jonka saamme jäsentämällä merkkijonon `struct Pancakes;`.

<Listing number="20-41" caption="`DeriveInput`-instanssi, jonka saamme jäsentäessämme listauksen 20-37 makroattribuutilla varustetun koodin">

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

Tämän rakenteen kentät osoittavat, että jäsentämämme Rust-koodi on yksikkörakenne, jonka `ident` (_identifier_, eli nimi) on `Pancakes`. Rakenteessa on lisää kenttiä kaikenlaisen Rust-koodin kuvaamiseen; katso [`syn`-dokumentaatiosta `DeriveInput`][syn-docs] lisätietoja.

Määrittelemme pian `impl_hello_macro`-funktion, jossa rakennamme uutta Rust-koodia, jonka haluamme sisällyttää. Mutta ennen sitä huomaa, että `derive`-makromme tuloste on myös `TokenStream`. Palautettu `TokenStream` lisätään kratettamme käyttäjien kirjoittamaan koodiin, joten kun he kääntävät kratensa, he saavat lisätoiminnallisuuden, jonka tarjoamme muokatussa `TokenStream`-arvossa.

Saatoit huomata, että kutsumme `unwrap`-funktiota aiheuttaaksemme `hello_macro_derive`-funktion panikoinnin, jos `syn::parse`-funktion kutsu epäonnistuu. Proseduraalisen makromme täytyy panikoida virheissä, koska `proc_macro_derive`-funktioiden täytyy palauttaa `TokenStream` eikä `Result` proseduraalisen makro-API:n mukaisesti. Olemme yksinkertaistaneet tämän esimerkin käyttämällä `unwrap`-funktiota; tuotantokoodissa sinun pitäisi antaa tarkempia virheilmoituksia siitä, mikä meni pieleen, käyttämällä `panic!`- tai `expect`-makroa.

Nyt kun meillä on koodi, joka muuntaa annotoidun Rust-koodin `TokenStream`-arvosta `DeriveInput`-instanssiksi, generoidaan koodi, joka toteuttaa `HelloMacro`-traitin annotoidulle tyypille, kuten listauksessa 20-42.

<Listing number="20-42" file-name="hello_macro_derive/src/lib.rs" caption="`HelloMacro`-traitin toteutus jäsennetyn Rust-koodin avulla">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-42/hello_macro/hello_macro_derive/src/lib.rs:here}}
```

</Listing>

Saamme `Ident`-rakenteen instanssin, joka sisältää annotoidun tyypin nimen (tunnisteen), käyttämällä `ast.ident`. Listauksen 20-41 rakenne osoittaa, että kun ajamme `impl_hello_macro`-funktion listauksen 20-37 koodilla, saamamme `ident` sisältää `ident`-kentän arvolla `"Pancakes"`. Näin ollen listauksen 20-42 `name`-muuttuja sisältää `Ident`-rakenteen instanssin, joka tulostettuna on merkkijono `"Pancakes"`, listauksen 20-37 rakenteen nimi.

`quote!`-makro sallii määritellä Rust-koodin, jonka haluamme palauttaa. Kääntäjä odottaa jotain erilaista kuin `quote!`-makron suoran suorituksen tulos, joten meidän täytyy muuntaa se `TokenStream`-tyypiksi. Teemme tämän kutsumalla `into`-metodia, joka kuluttaa tämän välisen esityksen ja palauttaa vaaditun `TokenStream`-tyypin arvon.

`quote!`-makrossa on myös erittäin hienoja mallipohjamekanismeja: voimme kirjoittaa `#name`, ja `quote!` korvaa sen `name`-muuttujan arvolla. Voit jopa tehdä toistoa samankaltaisesti kuin tavallisissa makroissa. Katso [`quote`-kraten dokumentaatiosta][quote-docs] perusteellinen johdanto.

Haluamme proseduraalisen makromme generoivan `HelloMacro`-traitin toteutuksen käyttäjän annotoimalle tyypille, jonka saamme `#name`-avulla. Trait-toteutuksessa on yksi funktio `hello_macro`, jonka runko sisältää haluamamme toiminnallisuuden: tulostaa `Hello, Macro! My name is` ja sitten annotoidun tyypin nimen.

Tässä käytetty `stringify!`-makro on sisäänrakennettu Rustiin. Se ottaa Rust-lausekkeen, kuten `1 + 2`, ja muuntaa lausekkeen käännösaikana merkkijonoliteraaliksi, kuten `"1 + 2"`. Tämä eroaa `format!`- tai `println!`-makroista, jotka arvioivat lausekkeen ja muuntavat tuloksen `String`-tyypiksi. On mahdollista, että `#name`-syöte on tulostettava lauseke, joten käytämme `stringify!`-makroa. `stringify!`-makron käyttö säästää myös allokaation muuntamalla `#name`:n merkkijonoliteraaliksi käännösaikana.

Tässä vaiheessa `cargo build` pitäisi onnistua sekä `hello_macro`- että `hello_macro_derive`-krateissa. Kytketään nämä kratet listauksen 20-37 koodiin ja katsotaan proseduraalista makroa käytännössä! Luo uusi binääriprojekti _projects_-hakemistoosi komennolla `cargo new pancakes`. Meidän täytyy lisätä `hello_macro` ja `hello_macro_derive` riippuvuuksiksi `pancakes`-kraten _Cargo.toml_-tiedostoon. Jos julkaiset `hello_macro`- ja `hello_macro_derive`-versiosi [crates.io](https://crates.io/)<!-- ignore --> -sivustolle, ne olisivat tavallisia riippuvuuksia; jos et, voit määrittää ne `path`-riippuvuuksiksi seuraavasti:

```toml
{{#include ../listings/ch20-advanced-features/no-listing-21-pancakes/pancakes/Cargo.toml:6:8}}
```

Laita listauksen 20-37 koodi _src/main.rs_-tiedostoon ja aja `cargo run`: sen pitäisi tulostaa `Hello, Macro! My name is Pancakes!`. Proseduraalisen makron `HelloMacro`-trait-toteutus sisällytettiin ilman, että `pancakes`-kraten täytyi toteuttaa sitä; `#[derive(HelloMacro)]` lisäsi trait-toteutuksen.

Seuraavaksi tutkitaan, miten muut proseduraalisen makron lajit eroavat mukautetuista `derive`-makroista.

### Attribuuttimaiset makrot

Attribuuttimaiset makrot muistuttavat mukautettuja `derive`-makroja, mutta sen sijaan, että ne generoisivat koodia `derive`-attribuutille, ne sallivat uusien attribuuttien luomisen. Ne ovat myös joustavampia: `derive` toimii vain rakenteille ja luettelotyypeille; attribuutteja voi käyttää myös muissa kohteissa, kuten funktioissa. Tässä on esimerkki attribuuttimaisen makron käytöstä. Oletetaan, että sinulla on `route`-attribuutti, joka annotoi funktioita web-sovelluskehyksen käytössä:

```rust,ignore
#[route(GET, "/")]
fn index() {
```

Tämän `#[route]`-attribuutin määrittelisi kehys proseduraalisena makrona. Makromääritelmäfunktion signatuuri näyttäisi tältä:

```rust,ignore
#[proc_macro_attribute]
pub fn route(attr: TokenStream, item: TokenStream) -> TokenStream {
```

Tässä meillä on kaksi `TokenStream`-tyyppistä parametria. Ensimmäinen on attribuutin sisältö: `GET, "/"` -osa. Toinen on kohteen runko, johon attribuutti on liitetty: tässä tapauksessa `fn index() {}` ja funktion rungon loppuosa.

Muuten attribuuttimaiset makrot toimivat samalla tavalla kuin mukautetut `derive`-makrot: luot kraten `proc-macro`-kratetyypillä ja toteutat funktion, joka generoi haluamasi koodin!

### Funktiomaiset makrot

Funktiomaiset makrot määrittelevät makroja, jotka näyttävät funktiokutsuilta. Samankaltaisesti kuin `macro_rules!`-makrot, ne ovat joustavampia kuin funktiot; esimerkiksi ne voivat ottaa tuntemattoman määrän argumentteja. `macro_rules!`-makroja voi kuitenkin määritellä vain aiemmin käsitellyllä match-tyylisellä syntaksilla [”Deklaratiiviset makrot yleiseen metaprogrammointiin”][decl]<!-- ignore --> -osiossa. Funktiomaiset makrot ottavat `TokenStream`-parametrin, ja niiden määritelmä käsittelee sitä Rust-koodilla kuten muutkin proseduraalisen makron lajit. Esimerkki funktiomaisesta makrosta on `sql!`-makro, jota voisi kutsua näin:

```rust,ignore
let sql = sql!(SELECT * FROM posts WHERE id=1);
```

Tämä makro jäsentäisi sen sisällä olevan SQL-lausekkeen ja tarkistaisi sen syntaktisen oikeellisuuden, mikä on paljon monimutkaisempaa käsittelyä kuin `macro_rules!`-makro pystyy tekemään. `sql!`-makro määriteltäisiin näin:

```rust,ignore
#[proc_macro]
pub fn sql(input: TokenStream) -> TokenStream {
```

Tämä määritelmä muistuttaa mukautetun `derive`-makron signatuuria: saamme sulkeiden sisällä olevat tokenit ja palautamme koodin, jonka haluamme generoida.

## Yhteenveto

Huh! Nyt sinulla on Rust-ominaisuuksia työkalupakissasi, joita et todennäköisesti käytä usein, mutta tiedät niiden olevan saatavilla hyvin erityisissä tilanteissa. Olemme esitelleet useita monimutkaisia aiheita, jotta kun kohtaat niitä virheilmoitusten ehdotuksissa tai muiden koodissa, tunnistat nämä käsitteet ja syntaksin. Käytä tätä lukua viitteenä ratkaisujen löytämiseen.

Seuraavaksi laitamme kaiken, mistä olemme puhuneet koko kirjan ajan, käytäntöön ja teemme vielä yhden projektin!

[ref]: ../reference/macros-by-example.html
[tlborm]: https://veykril.github.io/tlborm/
[syn]: https://crates.io/crates/syn
[quote]: https://crates.io/crates/quote
[syn-docs]: https://docs.rs/syn/2.0/syn/struct.DeriveInput.html
[quote-docs]: https://docs.rs/quote
[decl]: #declarative-macros-with-macro_rules-for-general-metaprogramming
