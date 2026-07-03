## Hello, Cargo!

Cargo on Rustin build-järjestelmä ja paketinhallinta. Useimmat Rustaceanit käyttävät tätä työkalua
Rust-projektiensa hallintaan, koska Cargo hoitaa puolestasi monia tehtäviä, kuten koodisi kääntämisen,
koodisi tarvitsemien kirjastojen lataamisen ja näiden kirjastojen kääntämisen. (Kutsumme koodisi
tarvitsemia kirjastoja _riippuvuuksiksi_.)

Yksinkertaisimmilla Rust-ohjelmilla, kuten tähän asti kirjoittamallamme, ei ole riippuvuuksia. Jos
olisimme rakentaneet "Hello, world!" -projektin Cargolla, se käyttäisi vain Cargon osaa, joka hoitaa
koodisi kääntämisen. Kun kirjoitat monimutkaisempia Rust-ohjelmia, lisäät riippuvuuksia, ja jos
aloitat projektin Cargolla, riippuvuuksien lisääminen on paljon helpompaa.

Koska valtava enemmistö Rust-projekteista käyttää Cargo-työkalua, tämän kirjan loppuosa olettaa,
että käytät sitä myös. Cargo tulee Rustin mukana, jos käytit virallisia asennusohjelmia, joita
käsiteltiin [Asennus][installation]<!-- ignore --> -osiossa. Jos asensit Rustin jollain muulla
tavalla, tarkista, onko Cargo asennettu kirjoittamalla terminaaliisi:

```console
$ cargo --version
```

Jos näet versionumeron, sinulla on se! Jos näet virheen, kuten `command not found`, katso asennustapasi
dokumentaatiosta, miten Cargo asennetaan erikseen.

### Projektin luominen Cargolla

Luodaan uusi projekti Cargolla ja katsotaan, miten se eroaa alkuperäisestä "Hello, world!" -projektistamme.
Palaa _projects_-kansioosi (tai minne päätit tallentaa koodisi). Suorita sitten millä tahansa
käyttöjärjestelmällä seuraavat:

```console
$ cargo new hello_cargo
$ cd hello_cargo
```

Ensimmäinen komento luo uuden kansion ja projektin nimeltä _hello_cargo_. Olemme nimenneet projektimme
_hello_cargo_, ja Cargo luo tiedostonsa samannimiseen kansioon.

Siirry _hello_cargo_-kansioon ja listaa tiedostot. Näet, että Cargo on luonut meille kaksi tiedostoa
ja yhden kansion: _Cargo.toml_-tiedoston ja _src_-kansion, jonka sisällä on _main.rs_-tiedosto.

Se on myös alustanut uuden Git-repositorion _.gitignore_-tiedoston kera. Git-tiedostoja ei luoda,
jos suoritat `cargo new` olemassa olevassa Git-repositoriossa; voit ohittaa tämän käyttämällä
`cargo new --vcs=git`.

> Huom: Git on yleinen versionhallintajärjestelmä. Voit muuttaa `cargo new` -komennon käyttämään
> eri versionhallintajärjestelmää tai ei lainkaan versionhallintaa `--vcs`-lipulla. Suorita
> `cargo new --help` nähdäksesi käytettävissä olevat vaihtoehdot.

Avaa _Cargo.toml_ valitsemassasi tekstieditorissa. Sen pitäisi näyttää samankaltaiselta kuin Listauksen 1-2 koodi.

<Listing number="1-2" file-name="Cargo.toml" caption="`cargo new` -komennon luoman *Cargo.toml*-tiedoston sisältö">

```toml
[package]
name = "hello_cargo"
version = "0.1.0"
edition = "2024"

[dependencies]
```

</Listing>

Tämä tiedosto on [_TOML_][toml]<!-- ignore --> (_Tom's Obvious, Minimal Language_) -muodossa,
joka on Cargon konfiguraatiomuoto.

Ensimmäinen rivi `[package]` on osion otsikko, joka osoittaa, että seuraavat lausekkeet konfiguroivat
pakettia. Kun lisäämme tähän tiedostoon lisätietoa, lisäämme muita osioita.

Seuraavat kolme riviä asettavat konfiguraatiotiedot, joita Cargo tarvitsee ohjelmasi kääntämiseen:
nimen, version ja käytettävän Rust-editionin. Puhumme `edition`-avaimesta [Liitteessä E][appendix-e]<!-- ignore -->.

Viimeinen rivi `[dependencies]` on osion alku, johon voit listata projektisi riippuvuudet. Rustissa
koodipaketteja kutsutaan _crateiksi_. Emme tarvitse muita crateja tähän projektiin, mutta tarvitsemme
Luvun 2 ensimmäisessä projektissa, joten käytämme tätä riippuvuuksien osiota silloin.

Avaa nyt _src/main.rs_ ja katso:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    println!("Hello, world!");
}
```

Cargo on luonut sinulle "Hello, world!" -ohjelman, aivan kuten Listauksessa 1-1 kirjoittamamme!
Tähän asti erot projektimme ja Cargon luoman projektin välillä ovat, että Cargo sijoitti koodin
_src_-kansioon ja meillä on _Cargo.toml_-konfiguraatiotiedosto ylätason kansiossa.

Cargo odottaa lähdekooditiedostojesi olevan _src_-kansiossa. Ylätason projektikansio on vain README-tiedostoille,
lisenssitiedoille, konfiguraatiotiedostoille ja kaikelle muulle, mikä ei liity koodiisi. Cargon käyttö
auttaa järjestämään projektisi. Kaikella on paikkansa, ja kaikki on paikallaan.

Jos aloitit projektin, joka ei käytä Cargo-työkalua, kuten teimme "Hello, world!" -projektissa,
voit muuntaa sen Cargoa käyttäväksi projektiksi. Siirrä projektikoodi _src_-kansioon ja luo sopiva
_Cargo.toml_-tiedosto. Helppo tapa saada _Cargo.toml_-tiedosto on suorittaa `cargo init`, joka luo
sen automaattisesti.

### Cargo-projektin kääntäminen ja suorittaminen

Katsotaan nyt, mikä on erilaista, kun käännetään ja suoritetaan "Hello, world!" -ohjelma Cargolla!
_hello_cargo_-kansiostasi käänä projektisi kirjoittamalla seuraava komento:

```console
$ cargo build
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 2.85 secs
```

Tämä komento luo ajettavan tiedoston _target/debug/hello_cargo_ (tai _target\debug\hello_cargo.exe_
Windowsilla) nykyisen kansiosi sijaan. Koska oletuskäännös on debug-käännös, Cargo sijoittaa binäärin
kansioon nimeltä _debug_. Voit suorittaa ajettavan tiedoston tällä komennolla:

```console
$ ./target/debug/hello_cargo # or .\target\debug\hello_cargo.exe on Windows
Hello, world!
```

Jos kaikki menee hyvin, `Hello, world!` pitäisi tulostua terminaaliin. Ensimmäinen `cargo build`
-komennon suoritus saa myös Cargon luomaan uuden tiedoston ylätasolle: _Cargo.lock_. Tämä tiedosto
pitää kirjaa projektisi riippuvuuksien tarkoista versioista. Tällä projektilla ei ole riippuvuuksia,
joten tiedosto on hieman niukka. Sinun ei koskaan tarvitse muuttaa tätä tiedostoa manuaalisesti;
Cargo hallitsee sen sisältöä puolestasi.

Käänsimme juuri projektin `cargo build` -komennolla ja suoritimme sen `./target/debug/hello_cargo`
-komennolla, mutta voimme myös käyttää `cargo run` -komentoa kääntääksemme koodin ja suorittaaksemme
syntyneen ajettavan tiedoston yhdellä komennolla:

```console
$ cargo run
    Finished dev [unoptimized + debuginfo] target(s) in 0.0 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

`cargo run` -komennon käyttö on kätevämpää kuin muistaa suorittaa `cargo build` ja käyttää sitten
koko polkua binääriin, joten useimmat kehittäjät käyttävät `cargo run` -komentoa.

Huomaa, että tällä kertaa emme nähneet tulostetta, joka osoittaa Cargon kääntävän `hello_cargo`-projektia.
Cargo päätteli, että tiedostot eivät olleet muuttuneet, joten se ei kääntänyt uudelleen vaan suoritti
vain binäärin. Jos olisit muokannut lähdekoodiasi, Cargo olisi kääntänyt projektin uudelleen ennen
suorittamista, ja olisit nähnyt tämän tulosteen:

```console
$ cargo run
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.33 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

Cargo tarjoaa myös komennon nimeltä `cargo check`. Tämä komento tarkistaa nopeasti koodisi varmistaakseen,
että se kääntyy, mutta ei tuota ajettavaa tiedostoa:

```console
$ cargo check
   Checking hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.32 secs
```

Miksi et haluaisi ajettavaa tiedostoa? Usein `cargo check` on paljon nopeampi kuin `cargo build`,
koska se ohittaa ajettavan tiedoston tuottamisen. Jos tarkistat työtäsi jatkuvasti koodia kirjoittaessasi,
`cargo check` -komennon käyttö nopeuttaa prosessia, jolla saat tietää, kääntyykö projektisi edelleen!
Siksi monet Rustaceanit suorittavat `cargo check` -komennon säännöllisesti ohjelmaa kirjoittaessaan
varmistaakseen, että se kääntyy. Sitten he suorittavat `cargo build` -komennon, kun ovat valmiita
käyttämään ajettavaa tiedostoa.

Kerrataan, mitä olemme tähän mennessä oppineet Cargosta:

- Voimme luoda projektin `cargo new` -komennolla.
- Voimme kääntää projektin `cargo build` -komennolla.
- Voimme kääntää ja suorittaa projektin yhdellä askeleella `cargo run` -komennolla.
- Voimme kääntää projektin tuottamatta binääriä virheiden tarkistamiseksi `cargo check` -komennolla.
- Sen sijaan, että tallentaisimme käännöstuloksen samaan kansioon kuin koodimme, Cargo säilyttää sen
  _target/debug_-kansiossa.

Cargon käytön lisäetu on, että komennot ovat samat riippumatta siitä, millä käyttöjärjestelmällä
työskentelet. Tästä eteenpäin emme enää anna erityisiä ohjeita Linuxille ja macOS:lle verrattuna
Windowsiin.

### Julkaisua varten kääntäminen

Kun projektisi on vihdoin valmis julkaistavaksi, voit käyttää `cargo build --release` -komentoa
kääntääksesi sen optimoinneilla. Tämä komento luo ajettavan tiedoston _target/release_-kansioon
_target/debug_-kansion sijaan. Optimoinnit tekevät Rust-koodistasi nopeammin suoritettavan, mutta
niiden käyttöönotto pidentää ohjelmasi kääntämiseen kuluvaa aikaa. Siksi on kaksi eri profiilia:
yksi kehitystä varten, kun haluat kääntää nopeasti ja usein, ja toinen lopullisen ohjelman rakentamiseen,
jota et rakenna uudelleen toistuvasti ja joka suoritetaan mahdollisimman nopeasti. Jos vertailet
koodisi suoritusaikaa, muista suorittaa `cargo build --release` ja vertailla _target/release_-kansion
ajettavalla tiedostolla.

<!-- Old headings. Do not remove or links may break. -->
<a id="cargo-as-convention"></a>

### Cargon käytäntöjen hyödyntäminen

Yksinkertaisissa projekteissa Cargo ei tarjoa paljon lisäarvoa pelkän `rustc`-kääntäjän käyttöön
verrattuna, mutta se osoittaa arvonsa ohjelmiesi monimutkaistuessa. Kun ohjelmat kasvavat useiksi
tiedostoiksi tai tarvitsevat riippuvuuden, on paljon helpompaa antaa Cargon koordinoida käännös.

Vaikka `hello_cargo`-projekti on yksinkertainen, se käyttää nyt suurta osaa tosielämän työkaluista,
joita käytät Rust-urasi loppuosassa. Itse asiassa voit työskennellä olemassa olevien projektien
parissa käyttämällä seuraavia komentoja koodin hakemiseen Gitillä, siirtymiseen projektin kansioon
ja kääntämiseen:

```console
$ git clone example.org/someproject
$ cd someproject
$ cargo build
```

Lisätietoa Cargosta löydät [sen dokumentaatiosta][cargo].

## Yhteenveto

Olet jo päässyt hyvään alkuun Rust-matkallasi! Tässä luvussa opit:

- Rustin uusimman vakaan version asentamisen `rustup`-työkalulla.
- Päivittämisen uudempaan Rust-versioon.
- Paikallisesti asennetun dokumentaation avaamisen.
- "Hello, world!" -ohjelman kirjoittamisen ja suorittamisen suoraan `rustc`-kääntäjällä.
- Uuden projektin luomisen ja suorittamisen Cargon käytäntöjen mukaisesti.

Nyt on hyvä aika rakentaa laajempi ohjelma totuttuaksesi Rust-koodin lukemiseen ja kirjoittamiseen.
Luvussa 2 rakennamme arvauspeli-ohjelman. Jos haluat mieluummin aloittaa oppimalla, miten yleiset
ohjelmointikäsitteet toimivat Rustissa, katso Luku 3 ja palaa sitten Lukuun 2.

[installation]: ch01-01-installation.html#installation
[toml]: https://toml.io
[appendix-e]: appendix-05-editions.html
[cargo]: https://doc.rust-lang.org/cargo/
