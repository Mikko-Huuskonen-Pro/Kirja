## Hello, World!

Nyt kun olet asentanut Rustin, on aika kirjoittaa ensimmäinen Rust-ohjelmasi. Uutta kieltä
opiskellessa on perinteistä kirjoittaa pieni ohjelma, joka tulostaa tekstin `Hello, world!`
näytölle, joten teemme saman tässä!

> Huom: Tämä kirja olettaa perustuntemusta komentorivistä. Rust ei aseta erityisiä vaatimuksia
> editorillesi, työkaluillesi tai koodisi sijainnille, joten jos haluat käyttää IDE:tä komentorivin
> sijaan, käytä vapaasti suosikki-IDE:täsi. Monilla IDE:illä on nyt jonkin verran Rust-tukea;
> katso IDE:n dokumentaatiosta yksityiskohdat. Rust-tiimi on keskittynyt erinomaisen IDE-tuen
> mahdollistamiseen `rust-analyzer`-työkalun kautta. Katso [Liite D][devtools]<!-- ignore -->
> lisätietoja varten.

<!-- Old headings. Do not remove or links may break. -->
<a id="creating-a-project-directory"></a>

### Projektikansion luominen

Aloitat luomalla kansion Rust-koodillesi. Rustille ei ole väliä, missä koodisi sijaitsee, mutta
tämän kirjan harjoituksia ja projekteja varten suosittelemme _projects_-kansion luomista
kotihakemistoosi ja kaikkien projektiesi säilyttämistä siellä.

Avaa terminaali ja kirjoita seuraavat komennot luodaksesi _projects_-kansion ja "Hello, world!"
-projektin kansion _projects_-kansion sisään.

Linuxissa, macOS:ssä ja PowerShellissä Windowsilla kirjoita tämä:

```console
$ mkdir ~/projects
$ cd ~/projects
$ mkdir hello_world
$ cd hello_world
```

Windows CMD:ssä kirjoita tämä:

```cmd
> mkdir "%USERPROFILE%\projects"
> cd /d "%USERPROFILE%\projects"
> mkdir hello_world
> cd hello_world
```

<!-- Old headings. Do not remove or links may break. -->
<a id="writing-and-running-a-rust-program"></a>

### Rust-ohjelman perusteet

Seuraavaksi luo uusi lähdekooditiedosto ja kutsu sitä _main.rs_. Rust-tiedostot päättyvät aina
_.rs_-päätteeseen. Jos käytät tiedostonimessä useampaa sanaa, käytä niiden erottamiseen alaviivaa.
Käytä esimerkiksi _hello_world.rs_ eikä _helloworld.rs_.

Avaa juuri luomasi _main.rs_-tiedosto ja kirjoita siihen Listauksen 1-1 koodi.

<Listing number="1-1" file-name="main.rs" caption="Ohjelma, joka tulostaa `Hello, world!`">

```rust
fn main() {
    println!("Hello, world!");
}
```

</Listing>

Tallenna tiedosto ja palaa terminaali-ikkunaan _~/projects/hello_world_-kansiossa. Linuxissa tai
macOS:ssä kirjoita seuraavat komennot tiedoston kääntämiseksi ja suorittamiseksi:

```console
$ rustc main.rs
$ ./main
Hello, world!
```

Windowsissa kirjoita komento `.\main` `./main`-komennon sijaan:

```powershell
> rustc main.rs
> .\main
Hello, world!
```

Käyttöjärjestelmästä riippumatta merkkijono `Hello, world!` pitäisi tulostua terminaaliin. Jos et
näe tätä tulostetta, katso [Vianmääritys][troubleshooting]<!-- ignore --> -osio asennusluvusta
saadaksesi apua.

Jos `Hello, world!` tulostui, onnittelut! Olet virallisesti kirjoittanut Rust-ohjelman. Se tekee
sinusta Rust-ohjelmoijan—tervetuloa!

<!-- Old headings. Do not remove or links may break. -->

<a id="anatomy-of-a-rust-program"></a>

### Rust-ohjelman rakenne

Käydään tämä "Hello, world!" -ohjelma läpi yksityiskohtaisesti. Tässä on ensimmäinen palanen:

```rust
fn main() {

}
```

Nämä rivit määrittelevät funktion nimeltä `main`. `main`-funktio on erityinen: se on aina ensimmäinen
koodi, joka suoritetaan jokaisessa ajettavassa Rust-ohjelmassa. Tässä ensimmäinen rivi julistaa
`main`-nimisen funktion, jolla ei ole parametreja eikä se palauta mitään. Jos parametreja olisi,
ne olisivat sulkeissa (`()`).

Funktion runko on kääritty `{}`-merkkeihin. Rust vaatii aaltosulkeet kaikkien funktioiden runkojen
ympärille. On hyvä tyyli sijoittaa avaava aaltosulje samalle riville funktion julistuksen kanssa
ja jättää niiden väliin yksi välilyönti.

> Huom: Jos haluat noudattaa yhtenäistä tyyliä Rust-projekteissa, voit käyttää automaattista
> muotoilutyökalua nimeltä `rustfmt` muotoillaksesi koodisi tietyssä tyylissä (lisätietoa
> `rustfmt`-työkalusta [Liitteessä D][devtools]<!-- ignore -->). Rust-tiimi on sisällyttänyt
> tämän työkalun standardiin Rust-jakeluun, kuten `rustc`-kääntäjäkin, joten sen pitäisi olla jo
> asennettuna tietokoneellesi!

`main`-funktion rungossa on seuraava koodi:

```rust
println!("Hello, world!");
```

Tämä rivi tekee kaiken työn tässä pienessä ohjelmassa: se tulostaa tekstiä näytölle. Tässä on
kolme tärkeää yksityiskohtaa.

Ensinnäkin `println!` kutsuu Rust-makroa. Jos se olisi kutsunut funktiota, se kirjoitettaisiin
`println` (ilman `!`-merkkiä). Rust-makrot ovat tapa kirjoittaa koodia, joka generoi koodia
laajentaakseen Rustin syntaksia, ja käsittelemme niitä tarkemmin [Luvussa 20][ch20-macros]<!-- ignore -->.
Toistaiseksi sinun tarvitsee vain tietää, että `!`-merkin käyttö tarkoittaa, että kutsut makroa
tavallisen funktion sijaan ja että makrot eivät aina noudata samoja sääntöjä kuin funktiot.

Toiseksi näet merkkijonon `"Hello, world!"`. Välitämme tämän merkkijonon argumenttina `println!`-makrolle,
ja merkkijono tulostetaan näytölle.

Kolmanneksi päätteemme rivin puolipisteellä (`;`), joka osoittaa, että tämä lauseke on ohi ja
seuraava on valmis alkamaan. Useimmat Rust-koodin rivit päättyvät puolipisteeseen.

<!-- Old headings. Do not remove or links may break. -->
<a id="compiling-and-running-are-separate-steps"></a>

### Kääntäminen ja suorittaminen

Suoritit juuri juuri luomasi ohjelman, joten tarkastellaan prosessin jokaista vaihetta.

Ennen Rust-ohjelman suorittamista sinun on käännettävä se Rust-kääntäjällä kirjoittamalla `rustc`-komento
ja välittämällä sille lähdekooditiedostosi nimi, näin:

```console
$ rustc main.rs
```

Jos sinulla on C- tai C++-tausta, huomaat, että tämä on samankaltaista kuin `gcc` tai `clang`.
Onnistuneen kääntämisen jälkeen Rust tuottaa binäärisen ajettavan tiedoston.

Linuxissa, macOS:ssä ja PowerShellissä Windowsilla näet ajettavan tiedoston kirjoittamalla `ls`-komennon
komentorivilläsi:

```console
$ ls
main  main.rs
```

Linuxissa ja macOS:ssä näet kaksi tiedostoa. PowerShellissä Windowsilla näet samat kolme tiedostoa
kuin CMD:ssä. CMD:ssä Windowsilla kirjoittaisit seuraavan:

```cmd
> dir /B %= the /B option says to only show the file names =%
main.exe
main.pdb
main.rs
```

Tämä näyttää lähdekooditiedoston _.rs_-päätteellä, ajettavan tiedoston (_main.exe_ Windowsilla,
mutta _main_ kaikilla muilla alustoilla) ja Windowsilla käytettäessä tiedoston, joka sisältää
virheenkorjaustietoja _.pdb_-päätteellä. Tästä eteenpäin suoritat _main_- tai _main.exe_-tiedoston
näin:

```console
$ ./main # or .\main on Windows
```

Jos _main.rs_ on "Hello, world!" -ohjelmasi, tämä rivi tulostaa `Hello, world!` terminaaliisi.

Jos olet tottunut dynaamiseen kieleen, kuten Rubyyn, Pythoniin tai JavaScriptiin, et ehkä ole
tottunut kääntämisen ja ohjelman suorittamisen erottamiseen eri vaiheiksi. Rust on _etukäteen
käännettävä_ kieli, mikä tarkoittaa, että voit kääntää ohjelman ja antaa ajettavan tiedoston
jollekin toiselle, ja he voivat suorittaa sen vaikka heillä ei olisi Rustia asennettuna. Jos
annat jollekulle _.rb_-, _.py_- tai _.js_-tiedoston, he tarvitsevat Ruby-, Python- tai JavaScript-toteutuksen
asennettuna (vastaavasti). Mutta näissä kielissä tarvitset vain yhden komennon ohjelmasi kääntämiseen
ja suorittamiseen. Kaikki on kompromissi kielen suunnittelussa.

Pelkkä kääntäminen `rustc`-kääntäjällä riittää yksinkertaisiin ohjelmiin, mutta projektisi kasvaessa
haluat hallita kaikkia vaihtoehtoja ja helpottaa koodisi jakamista. Seuraavaksi esittelemme sinulle
Cargo-työkalun, joka auttaa kirjoittamaan tosielämän Rust-ohjelmia.

[troubleshooting]: ch01-01-installation.html#troubleshooting
[devtools]: appendix-04-useful-development-tools.html
[ch20-macros]: ch20-05-macros.html
