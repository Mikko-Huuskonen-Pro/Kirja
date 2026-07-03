## Asennus

Ensimmäinen askel on Rustin asentaminen. Lataamme Rustin `rustup`-työkalun kautta, joka on
komentorivityökalu Rust-versioiden ja niihin liittyvien työkalujen hallintaan. Tarvitset
internet-yhteyden latausta varten.

> Huom: Jos et halua käyttää `rustup`-työkalua jostain syystä, katso [muut Rustin asennustavat][otherinstall] -sivulta lisää vaihtoehtoja.

Seuraavat vaiheet asentavat uusimman vakaan version Rust-kääntäjästä. Rustin vakaustakuut
varmistavat, että kaikki tämän kirjan esimerkit, jotka kääntyvät, kääntyvät edelleen myös
uudemmissa Rust-versioissa. Tuloste voi hieman erota versioiden välillä, koska Rust parantaa
virheilmoituksia ja varoituksia säännöllisesti. Toisin sanoen, mikä tahansa näillä ohjeilla
asennettu uudempi vakaa Rust-versio toimii odotetusti tämän kirjan sisällön kanssa.

> ### Komentorivimerkinnät
>
> Tässä luvussa ja koko kirjassa näytämme terminaalissa käytettäviä komentoja. Rivit, jotka
> sinun pitäisi kirjoittaa terminaaliin, alkavat merkillä `$`. Sinun ei tarvitse kirjoittaa
> `$`-merkkiä; se on komentorivin kehote, joka osoittaa kunkin komennon alun. Rivit, jotka eivät
> ala `$`-merkillä, näyttävät yleensä edellisen komennon tulosteen. Lisäksi PowerShell-esimerkeissä
> käytetään `>`-merkkiä `$`-merkin sijasta.

### `rustup`-asennus Linuxilla tai macOS:llä

Jos käytät Linuxia tai macOS:ää, avaa terminaali ja kirjoita seuraava komento:

```console
$ curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh
```

Komento lataa skriptin ja käynnistää `rustup`-työkalun asennuksen, joka asentaa uusimman vakaan
Rust-version. Sinua saatetaan pyytää salasanaasi. Jos asennus onnistuu, näet seuraavan rivin:

```text
Rust is installed now. Great!
```

Tarvitset myös _linkkerin_, joka on ohjelma, jota Rust käyttää yhdistääkseen kääntämänsä
tulosteet yhdeksi tiedostoksi. Sinulla on todennäköisesti jo sellainen. Jos saat linkkerivirheitä,
sinun pitäisi asentaa C-kääntäjä, joka yleensä sisältää linkkerin. C-kääntäjä on hyödyllinen myös
siksi, että jotkin yleiset Rust-paketit riippuvat C-koodista ja tarvitsevat C-kääntäjän.

macOS:llä voit hankkia C-kääntäjän suorittamalla:

```console
$ xcode-select --install
```

Linux-käyttäjien tulisi yleensä asentaa GCC tai Clang jakelunsa dokumentaation mukaisesti.
Esimerkiksi Ubuntussa voit asentaa `build-essential`-paketin.

### `rustup`-asennus Windowsilla

Windowsissa siirry osoitteeseen [https://www.rust-lang.org/tools/install][install]<!-- ignore
--> ja seuraa Rustin asennusohjeita. Asennuksen aikana sinua pyydetään asentamaan Visual Studio.
Se tarjoaa linkkerin ja natiivit kirjastot, joita ohjelmien kääntäminen tarvitsee. Jos tarvitset
lisäapua tässä vaiheessa, katso
[https://rust-lang.github.io/rustup/installation/windows-msvc.html][msvc]<!-- ignore -->.

Tämän kirjan loppuosa käyttää komentoja, jotka toimivat sekä _cmd.exe_:ssä että PowerShellissä.
Jos on erityisiä eroja, selitämme, kumpaa käyttää.

### Vianmääritys

Voit tarkistaa, onko Rust asennettu oikein, avaamalla komentorivin ja kirjoittamalla:

```console
$ rustc --version
```

Sinun pitäisi nähdä versionumero, commit-hash ja commit-päivämäärä uusimmalle julkaistulle
vakaalle versiolle seuraavassa muodossa:

```text
rustc x.y.z (abcabcabc yyyy-mm-dd)
```

Jos näet nämä tiedot, Rust on asennettu onnistuneesti! Jos et näe niitä, tarkista, että Rust on
`%PATH%`-järjestelmämuuttujassasi seuraavasti.

Windows CMD:ssä käytä:

```console
> echo %PATH%
```

PowerShellissä käytä:

```powershell
> echo $env:Path
```

Linuxissa ja macOS:ssä käytä:

```console
$ echo $PATH
```

Jos kaikki on oikein ja Rust ei silti toimi, voit saada apua monista paikoista. Ota selvää,
miten voit olla yhteydessä muihin Rustaceaneihin (leikkisä lempinimi, jolla kutsumme itseämme)
[yhteisösivulta][community].

### Päivittäminen ja poistaminen

Kun Rust on asennettu `rustup`-työkalun kautta, uuteen julkaistuun versioon päivittäminen on
helppoa. Suorita komentorivillä seuraava päivitysskripti:

```console
$ rustup update
```

Poistaaksesi Rustin ja `rustup`-työkalun, suorita seuraava poistoskripti komentorivillä:

```console
$ rustup self uninstall
```

<!-- Old headings. Do not remove or links may break. -->
<a id="local-documentation"></a>

### Paikallisen dokumentaation lukeminen

Rustin asennuksen mukana tulee paikallinen kopio dokumentaatiosta, joten voit lukea sitä
offline-tilassa. Avaa paikallinen dokumentaatio selaimessasi komennolla `rustup doc`.

Aina kun standardikirjasto tarjoaa tyypin tai funktion etkä ole varma, mitä se tekee tai miten
sitä käytetään, käytä sovellusohjelmointirajapinnan (API) dokumentaatiota selvittääksesi!

<!-- Old headings. Do not remove or links may break. -->
<a id="text-editors-and-integrated-development-environments"></a>

### Tekstieditorien ja IDE:iden käyttö

Tämä kirja ei tee oletuksia siitä, mitä työkaluja käytät Rust-koodin kirjoittamiseen. Melkein
mikä tahansa tekstieditori hoitaa homman! Monet tekstieditorit ja integroidut kehitysympäristöt
(IDE) tarjoavat kuitenkin sisäänrakennettua Rust-tukea. Löydät melko ajantasaisen listan
monista editoreista ja IDE:istä [työkalusivulta][tools] Rustin verkkosivustolla.

### Tämän kirjan käyttö offline-tilassa

Useissa esimerkeissä käytämme Rust-paketteja standardikirjaston ulkopuolelta. Työskennelläksesi
näiden esimerkkien parissa tarvitset joko internet-yhteyden tai olet ladannut riippuvuudet
etukäteen. Ladataksesi riippuvuudet etukäteen voit suorittaa seuraavat komennot. (Selitämme
myöhemmin tarkemmin, mikä `cargo` on ja mitä kukin komento tekee.)

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch02-00-guessing-game-tutorial.md
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
* ch14-03-cargo-workspaces.md
-->

```console
$ cargo new get-dependencies
$ cd get-dependencies
$ cargo add rand@0.10.1 trpl@0.2.0
```

Tämä tallentaa näiden pakettien lataukset välimuistiin, joten sinun ei tarvitse ladata niitä
myöhemmin. Kun olet suorittanut tämän komennon, sinun ei tarvitse säilyttää `get-dependencies`-kansiota.
Jos olet suorittanut tämän komennon, voit käyttää `--offline`-lippua kaikissa `cargo`-komennoissa
kirjan loppuosassa käyttääksesi näitä välimuistissa olevia versioita verkon käytön sijaan.

[otherinstall]: https://forge.rust-lang.org/infra/other-installation-methods.html
[install]: https://www.rust-lang.org/tools/install
[msvc]: https://rust-lang.github.io/rustup/installation/windows-msvc.html
[community]: https://www.rust-lang.org/community
[tools]: https://www.rust-lang.org/tools
