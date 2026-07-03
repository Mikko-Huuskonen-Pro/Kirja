## Liite D: Hyödylliset kehitystyökalut

Tässä liitteessä käsittelemme joitakin hyödyllisiä kehitystyökaluja, joita Rust-projekti
tarjoaa. Käymme läpi automaattisen muotoilun, nopeita tapoja soveltaa varoitusten korjauksia,
linterin ja integraation IDE:iden kanssa.

### Automaattinen muotoilu `rustfmt`-työkalulla

`rustfmt`-työkalu muotoilee koodisi yhteisön koodityylin mukaisesti. Monet yhteistyöhankkeet
käyttävät `rustfmt`-työkalua estääkseen kiistoja siitä, mitä tyyliä Rust-kirjoituksessa
käytetään: kaikki muotoilevat koodinsa työkalulla.

Rust-asennukset sisältävät `rustfmt`-työkalun oletuksena, joten järjestelmässäsi pitäisi jo
olla ohjelmat `rustfmt` ja `cargo-fmt`. Nämä kaksi komentoa vastaavat `rustc`- ja `cargo`-
komentoja siinä mielessä, että `rustfmt` tarjoaa tarkemman hallinnan ja `cargo-fmt` ymmärtää
Cargoa käyttävän projektin käytännöt. Muotoillaksesi minkä tahansa Cargo-projektin, anna
seuraava komento:

```console
$ cargo fmt
```

Tämän komennon suorittaminen muotoilee kaiken nykyisen paketin Rust-koodin. Sen pitäisi muuttaa
vain koodityyliä, ei koodin semantiikkaa. Lisätietoja `rustfmt`-työkalusta löytyy [sen
dokumentaatiosta][rustfmt].

### Koodin korjaaminen `rustfix`-työkalulla

`rustfix`-työkalu sisältyy Rust-asennuksiin ja voi automaattisesti korjata kääntäjän
varoituksia, joilla on selkeä korjaustapa, joka todennäköisesti on se, mitä haluat. Olet
todennäköisesti nähnyt kääntäjän varoituksia aiemmin. Esimerkiksi tarkastele tätä koodia:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    let mut x = 42;
    println!("{x}");
}
```

Tässä määrittelemme muuttujan `x` muuttuvaksi, mutta emme koskaan muuta sitä. Rust varoittaa
siitä:

```console
$ cargo build
   Compiling myprogram v0.1.0 (file:///projects/myprogram)
warning: variable does not need to be mutable
 --> src/main.rs:2:9
  |
2 |     let mut x = 0;
  |         ----^
  |         |
  |         help: remove this `mut`
  |
  = note: `#[warn(unused_mut)]` on by default
```

Varoitus ehdottaa, että poistamme `mut`-avainsanan. Voimme soveltaa ehdotusta automaattisesti
`rustfix`-työkalulla suorittamalla komennon `cargo fix`:

```console
$ cargo fix
    Checking myprogram v0.1.0 (file:///projects/myprogram)
      Fixing src/main.rs (1 fix)
    Finished dev [unoptimized + debuginfo] target(s) in 0.59s
```

Kun katsomme tiedostoa _src/main.rs_ uudelleen, huomaamme, että `cargo fix` on muuttanut koodin:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    let x = 42;
    println!("{x}");
}
```

Muuttuja `x` on nyt muuttumaton, eikä varoitusta enää näy.

Voit myös käyttää `cargo fix` -komentoa siirtääksesi koodiasi eri Rust-editionien välillä.
Editioneista kerrotaan [liitteessä E][editions]<!-- ignore -->.

### Lisää linttauksia Clippyllä

Clippy-työkalu on kokoelma linttauksia, jotka analysoivat koodiasi, jotta voit havaita yleisiä
virheitä ja parantaa Rust-koodiasi. Clippy sisältyy vaki Rust-asennuksiin.

Suorittaaksesi Clippyn linttauksia missä tahansa Cargo-projektissa, anna seuraava komento:

```console
$ cargo clippy
```

Esimerkiksi oletetaan, että kirjoitat ohjelman, joka käyttää matemaattisen vakion likiarvoa,
kuten piitä, kuten tämä ohjelma tekee:

<Listing file-name="src/main.rs">

```rust
fn main() {
    let x = 3.1415;
    let r = 8.0;
    println!("the area of the circle is {}", x * r * r);
}
```

</Listing>

Tämän projektin `cargo clippy` -suoritus tuottaa tämän virheen:

```text
error: approximate value of `f{32, 64}::consts::PI` found
 --> src/main.rs:2:13
  |
2 |     let x = 3.1415;
  |             ^^^^^^
  |
  = note: `#[deny(clippy::approx_constant)]` on by default
  = help: consider using the constant directly
  = help: for further information visit https://rust-lang.github.io/rust-clippy/master/index.html#approx_constant
```

Tämä virhe kertoo, että Rustissa on jo tarkempi `PI`-vakio määriteltynä ja että ohjelmasi
olisi oikeampi, jos käyttäisit vakiota likiarvon sijaan. Muuttaisit sitten koodisi käyttämään
`PI`-vakiota.

Seuraava koodi ei tuota Clippyltä virheitä tai varoituksia:

<Listing file-name="src/main.rs">

```rust
fn main() {
    let x = std::f64::consts::PI;
    let r = 8.0;
    println!("the area of the circle is {}", x * r * r);
}
```

</Listing>

Lisätietoja Clippystä löytyy [sen dokumentaatiosta][clippy].

### IDE-integraatio `rust-analyzer`-työkalulla

IDE-integraation helpottamiseksi Rust-yhteisö suosittelee [`rust-analyzer`][rust-analyzer]<!--
ignore --> -työkalun käyttöä. Tämä työkalu on joukko kääntäjäkeskeisiä apuohjelmia, jotka
käyttävät [Language Server Protocol][lsp]<!-- ignore --> -määritystä, joka on spesifikaatio
IDE:iden ja ohjelmointikielten väliselle viestinnälle. Erilaiset asiakkaat voivat käyttää
`rust-analyzer`-työkalua, kuten [Visual Studio Coden Rust-analyzer-liitännäinen][vscode].

Vieraile `rust-analyzer`-projektin [kotisivulla][rust-analyzer]<!-- ignore --> saadaksesi
asennusohjeet ja asenna sitten kielipalvelintuki omaan IDE:esi. IDE:si saa ominaisuuksia,
kuten automaattisen täydennyksen, siirtymisen määrittelyyn ja rivinsisäiset virheet.

[rustfmt]: https://github.com/rust-lang/rustfmt
[editions]: appendix-05-editions.md
[clippy]: https://github.com/rust-lang/rust-clippy
[rust-analyzer]: https://rust-analyzer.github.io
[lsp]: http://langserver.org/
[vscode]: https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer
