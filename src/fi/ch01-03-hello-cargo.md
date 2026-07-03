## Hello, Cargo!

Cargo on Rustin rakennusjärjestelmä ja pakettienhallintaohjelma. Suurin osa Rust-kehittäjistä käyttää tätä työkalua
Rust-projektiensa hallintaan, koska Cargo hoitaa monia tehtäviä puolestasi,
kuten koodisi kääntämisen, koodisi tarvitsemien kirjastojen lataamisen ja
näiden kirjastojen kääntämisen. (Kirjastoja, joita koodisi tarvitsee, kutsutaan
_riippuvuuksiksi_.)

Yksinkertaisimmat Rust-ohjelmat, kuten tähän mennessä kirjoittamamme, eivät sisällä
mitään riippuvuuksia. Jos olisimme rakentaneet ”Hello, world!” -projektin Cargolla, se
käyttäisi vain Cargon osaa, joka hoitaa koodisi kääntämisen. Kun kirjoitat
monimutkaisempia Rust-ohjelmia, lisäät riippuvuuksia, ja jos aloitat projektin
Cargoa käyttäen, riippuvuuksien lisääminen on paljon helpompaa.

Koska valtaosa Rust-projekteista käyttää Cargoa, tämän kirjan loppuosa
olettaa, että käytät Cargoa myös. Cargo asennetaan Rustin mukana, jos
käytit virallisia asennusohjelmia, joita käsiteltiin
[”Asennus”][installation]<!-- ignore --> -osiossa. Jos asensit Rustin
jollain muulla tavalla, tarkista, onko Cargo asennettu, kirjoittamalla
seuraava terminaaliin:

```console
$ cargo --version
```

Jos näet versionumeron, se on asennettu! Jos näet virheen, kuten `command
not found`, katso asennusmenetelmäsi dokumentaatiosta,
miten Cargo asennetaan erikseen.

### Projektin luominen Cargolla

Luodaan uusi projekti Cargoa käyttäen ja katsotaan, miten se eroaa
alkuperäisestä ”Hello, world!” -projektistamme. Siirry takaisin _projects_-
hakemistoosi (tai minne tahansa päätit tallentaa koodisi). Suorita sitten
mikä tahansa käyttöjärjestelmä huomioon ottaen seuraava:

```console
$ cargo new hello_cargo
$ cd hello_cargo
```

Ensimmäinen komento luo uuden hakemiston ja projektin nimeltä _hello_cargo_.
Olemme nimenneet projektimme _hello_cargo_, ja Cargo luo sen tiedostot
saman nimiseen hakemistoon.

Siirry _hello_cargo_-hakemistoon ja listaa tiedostot. Näet, että Cargo
on luonut meille kaksi tiedostoa ja yhden hakemiston: _Cargo.toml_-tiedoston ja
_src_-hakemiston, jonka sisällä on _main.rs_-tiedosto.

Se on myös alustanut uuden Git-repositorion sekä _.gitignore_-tiedoston.
Git-tiedostoja ei luoda, jos suoritat `cargo new` -komennon olemassa olevassa Git-
repositoriossa; voit ohittaa tämän käyttämällä `cargo new --vcs=git`.

> Huom: Git on yleinen versionhallintajärjestelmä. Voit muuttaa `cargo new` -komennon
> käyttämään eri versionhallintajärjestelmää tai ei lainkaan versionhallintaa
> `--vcs`-lipulla. Suorita `cargo new --help` nähdäksesi käytettävissä olevat vaihtoehdot.

Avaa _Cargo.toml_ haluamassasi tekstieditorissa. Sen pitäisi näyttää samankaltaiselta
kuin Listauksen 1-2 koodi.

<Listing number="1-2" file-name="Cargo.toml" caption="Komennolla `cargo new` luodun *Cargo.toml*-tiedoston sisältö">

```toml
[package]
name = "hello_cargo"
version = "0.1.0"
edition = "2024"

[dependencies]
```

</Listing>

Tämä tiedosto on [_TOML_][toml]<!-- ignore -->-muodossa (_Tom’s Obvious, Minimal
Language_), joka on Cargon asetustiedostomuoto.

Ensimmäinen rivi, `[package]`, on osio-otsikko, joka osoittaa, että
seuraavat lauseet määrittävät paketin. Kun lisäämme tähän tiedostoon lisää tietoa,
lisäämme muita osioita.

Seuraavat kolme riviä asettavat konfiguraatiotiedot, joita Cargo tarvitsee
ohjelmasi kääntämiseen: nimen, version ja käytettävän Rust-version. Käsittelemme
`edition`-avainta [liitteessä E][appendix-e]<!-- ignore -->.

Viimeinen rivi, `[dependencies]`, on osion alku, johon voit listata
projektisi riippuvuudet. Rustissa koodipaketteja kutsutaan
_crateiksi_. Emme tarvitse muita crateja tässä projektissa, mutta tarvitsemme
luvun 2 ensimmäisessä projektissa, joten käytämme tätä riippuvuuksien osiota silloin.

Avaa nyt _src/main.rs_ ja katso sitä:

<span class="filename">Tiedostonimi: src/main.rs</span>

```rust
fn main() {
    println!("Hello, world!");
}
```

Cargo on luonut sinulle ”Hello, world!” -ohjelman, aivan kuten
Listauksessa 1-1 kirjoittamamme! Tähän mennessä projektimme ja Cargon luoman
projektin erot ovat, että Cargo sijoitti koodin _src_-hakemistoon
ja meillä on _Cargo.toml_-asetustiedosto ylätason hakemistossa.

Cargo odottaa, että lähdekooditiedostosi sijaitsevat _src_-hakemistossa.
Ylätason projektihakemisto on vain README-tiedostoille, lisenssitiedoille,
asetustiedostoille ja kaikelle muulle, mikä ei liity koodiisi. Cargon käyttö
auttaa järjestämään projektisi. Kaikella on paikkansa, ja
kaikki on omalla paikallaan.

Jos aloitit projektin, joka ei käytä Cargoa, kuten teimme ”Hello,
world!” -projektissa, voit muuntaa sen Cargoa käyttäväksi projektiksi. Siirrä
projektikoodi _src_-hakemistoon ja luo sopiva _Cargo.toml_-
tiedosto. Yksi helppo tapa saada _Cargo.toml_-tiedosto on suorittaa `cargo init`, joka
luo sen automaattisesti.

### Cargo-projektin rakentaminen ja suorittaminen

Katsotaan nyt, mikä on erilaista, kun rakennamme ja suoritamme ”Hello, world!” -
ohjelman Cargolla! _hello_cargo_-hakemistostasi rakenna projektisi
kirjoittamalla seuraava komento:

```console
$ cargo build
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 2.85 secs
```

Tämä komento luo suoritettavan tiedoston hakemistoon _target/debug/hello_cargo_ (tai
_target\debug\hello_cargo.exe_ Windowsissa) nykyisen hakemiston sijaan.
Koska oletusrakenne on debug-rakenne, Cargo sijoittaa binäärin
_debug_-nimiseen hakemistoon. Voit suorittaa suoritettavan tällä komennolla:

```console
$ ./target/debug/hello_cargo # tai .\target\debug\hello_cargo.exe Windowsissa
Hello, world!
```

Jos kaikki menee hyvin, `Hello, world!` pitäisi tulostua terminaaliin. `cargo
build` -komennon ensimmäinen suoritus saa myös Cargon luomaan uuden tiedoston ylätasolle:
_Cargo.lock_. Tämä tiedosto pitää kirjaa projektisi riippuvuuksien tarkoista versioista. Tässä projektissa ei ole riippuvuuksia, joten
tiedosto on hieman niukka. Sinun ei koskaan tarvitse muuttaa tätä tiedostoa käsin; Cargo
hallitsee sen sisältöä puolestasi.

Rakensimme juuri projektin komennolla `cargo build` ja suoritimme sen komennolla
`./target/debug/hello_cargo`, mutta voimme myös käyttää `cargo run` -komentoa kääntääksemme
koodin ja suorittaaksemme syntyneen suoritettavan yhdellä komennolla:

```console
$ cargo run
    Finished dev [unoptimized + debuginfo] target(s) in 0.0 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

`cargo run` -komennon käyttö on kätevämpää kuin muistaa suorittaa `cargo
build` ja käyttää sitten koko polkua binääriin, joten useimmat kehittäjät käyttävät `cargo
run` -komentoa.

Huomaa, että tällä kertaa emme nähneet tulostetta, joka osoittaisi Cargon kääntävän
`hello_cargo`-projektia. Cargo päätteli, että tiedostoja ei ollut muutettu, joten se ei
kääntänyt uudelleen vaan suoritti vain binäärin. Jos olisit muokannut lähdekoodiasi, Cargo
olisi kääntänyt projektin uudelleen ennen suorittamista, ja olisit nähnyt tämän
tulosteen:

```console
$ cargo run
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.33 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

Cargo tarjoaa myös komennon nimeltä `cargo check`. Tämä komento tarkistaa nopeasti
koodisi varmistaakseen, että se kääntyy, mutta ei tuota suoritettavaa:

```console
$ cargo check
   Checking hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.32 secs
```

Miksi et haluaisi suoritettavaa? Usein `cargo check` on paljon nopeampi kuin
`cargo build`, koska se ohittaa suoritettavan tuottamisen. Jos tarkistat
jatkuvasti työtäsi koodia kirjoittaessasi, `cargo check` -komennon käyttö
nopeuttaa prosessia, jolla saat tietää, kääntyykö projektisi vielä! Siksi
monet Rust-kehittäjät suorittavat `cargo check` -komennon säännöllisesti kirjoittaessaan
ohjelmaansa varmistaakseen, että se kääntyy. Sitten he suorittavat `cargo build` -komennon, kun ovat
valmiita käyttämään suoritettavaa.

Kerrataan, mitä olemme tähän mennessä oppineet Cargosta:

- Voimme luoda projektin komennolla `cargo new`.
- Voimme rakentaa projektin komennolla `cargo build`.
- Voimme rakentaa ja suorittaa projektin yhdellä askeleella komennolla `cargo run`.
- Voimme rakentaa projektin tuottamatta binääriä virheiden tarkistamiseksi komennolla
  `cargo check`.
- Sen sijaan, että tallentaisimme rakennuksen tuloksen samaan hakemistoon kuin koodimme,
  Cargo tallentaa sen _target/debug_-hakemistoon.

Cargon käytön lisäetu on, että komennot ovat samat riippumatta
siitä, millä käyttöjärjestelmällä työskentelet. Tästä eteenpäin emme enää
anna erillisiä ohjeita Linuxille ja macOS:lle verrattuna Windowsiin.

### Julkaisuversion rakentaminen

Kun projektisi on vihdoin valmis julkaistavaksi, voit käyttää `cargo build
--release` -komentoa kääntääksesi sen optimoinneilla. Tämä komento luo
suoritettavan tiedoston hakemistoon _target/release_ hakemiston _target/debug_ sijaan. Optimoinnit
saavat Rust-koodisi toimimaan nopeammin, mutta niiden käyttöönotto pidentää aikaa, jonka
ohjelmasi kääntäminen kestää. Siksi on kaksi eri profiilia: yksi
kehitystä varten, kun haluat kääntää nopeasti ja usein, ja toinen
lopullisen ohjelman rakentamiseen, jonka annat käyttäjälle ja jota ei rakenneta
uudelleen toistuvasti ja joka toimii mahdollisimman nopeasti. Jos vertailet
koodisi suoritusaikaa, muista suorittaa `cargo build --release` ja vertailla
suoritettavaa hakemistossa _target/release_.

### Cargo käytäntönä

Yksinkertaisissa projekteissa Cargo ei tarjoa paljon lisäarvoa pelkän
`rustc`-komennon käyttöön verrattuna, mutta se osoittaa arvonsa, kun ohjelmasi monimutkaistuvat.
Kun ohjelmat kasvavat useisiin tiedostoihin tai tarvitsevat riippuvuuden, on paljon helpompaa
antaa Cargon koordinoida rakennusta.

Vaikka `hello_cargo`-projekti on yksinkertainen, se käyttää nyt suurta osaa oikeista
työkaluista, joita käytät loppu Rust-urasi ajan. Itse asiassa työskennelläksesi minkä tahansa
olemassa olevan projektin parissa voit käyttää seuraavia komentoja tarkistaaksesi koodin
Gitillä, siirtyäksesi kyseisen projektin hakemistoon ja rakentaaksesi:

```console
$ git clone example.org/someproject
$ cd someproject
$ cargo build
```

Lisätietoja Cargosta löydät [sen dokumentaatiosta][cargo].

## Yhteenveto

Olet jo päässyt hyvään alkuun Rust-matkallasi! Tässä luvussa
olet oppinut:

- Asentamaan uusimman vakaan Rust-version komennolla `rustup`
- Päivittämään uudempaan Rust-versioon
- Avaamaan paikallisesti asennetun dokumentaation
- Kirjoittamaan ja suorittamaan ”Hello, world!” -ohjelman suoraan komennolla `rustc`
- Luomaan ja suorittamaan uuden projektin Cargon käytäntöjen mukaisesti

Nyt on hyvä hetki rakentaa laajempi ohjelma totuttuaksesi Rust-koodin lukemiseen
ja kirjoittamiseen. Luvussa 2 rakennamme arvauspeli-ohjelman.
Jos haluat mieluummin aloittaa oppimalla, miten yleiset ohjelmointikäsitteet toimivat
Rustissa, katso luku 3 ja palaa sitten lukuun 2.

[installation]: ch01-01-installation.html#installation
[toml]: https://toml.io
[appendix-e]: appendix-05-editions.html
[cargo]: https://doc.rust-lang.org/cargo/
