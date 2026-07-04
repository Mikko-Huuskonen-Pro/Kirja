# Rust-ohjelmointikieli

![Build Status](https://github.com/rust-lang/book/workflows/CI/badge.svg)


This is an unofficial Finnish translation of The Rust Programming Language.

Tämä on epävirallinen suomenkielinen käännös teoksesta The Rust Programming Language.

Julkaistu versio: https://mikko-huuskonen-pro.github.io/Kirja/

Tämä arkisto sisältää The Rust Programming Language -kirjan lähdekoodin.

Alla olevan tekstin linkit vievät Rust the book:n sivuille. src/fi .md tiedostot käännetty tekoälyllä, pidemmät tiedostot pielessä, lyhyemmät ok. Työvaiheet

1. src/fi läpikäynti, OK! viimeisenä muutoksena niihin jotka katsottu läpi ja ok. Tässä tarkastuksessa menee aikaa, src kansiossa alkuperäiset eng tiedostot johon verrataan.

2.Tekniset viittaukset kuntoon, jotta hakee käännetyistä tiedot siirretään fi--->src kansioon eng tilalle ja eng omaan kansioon.

3. Julkistetaan kirja, oma page sille

4. Kuittaus https://github.com/rust-lang/book/issues/4268

[Kirja on saatavilla painettuna englanniksi No Starch Pressin kautta][nostarch].

[nostarch]: https://nostarch.com/rust-programming-language-2nd-edition

Voit myös lukea kirjan englannin kielellä ilmaiseksi verkossa. Tarkista kirjan versio uusimmasta [stable], [beta], tai [nightly] Rust-julkaisusta. Huomaa, että näiden versioiden virheitä on saatettu jo korjata tässä arkistossa, koska julkaisut päivittyvät harvemmin.


[stable]: https://doc.rust-lang.org/stable/book/
[beta]: https://doc.rust-lang.org/beta/book/
[nightly]: https://doc.rust-lang.org/nightly/book/

Lataa kaikki kirjassa esiintyvät koodilistaukset [releases]-osiosta.

[releases]: https://github.com/rust-lang/book/releases

## Vaatimukset

Kirjan kokoaminen vaatii [mdBook]-työkalun, mieluiten version mitä
rust-lang/rust käyttää tässä [tässä tiedostossa][rust-mdbook]. Saat sen täältä:

[mdBook]: https://github.com/rust-lang/mdBook
[rust-mdbook]: https://github.com/rust-lang/rust/blob/HEAD/src/tools/rustbook/Cargo.toml

```bash
$ cargo install mdbook --locked --version <version_num>
```

Kirja käyttää myös kahta mdbook-lisäosaa, jotka ovat osa tätä arkistoa. Jos et asenna niitä, saat varoituksia rakennusvaiheessa, ja lopputulos ei näytä oikealta, mutta voit silti koota kirjan. Ota lisäosat käyttöön asentamalla ne näin:

```bash
$ cargo install --locked --path packages/mdbook-trpl
```

## Kokoaminen

Kootaksesi kirjan suorita:

```bash
$ mdbook build
```

Lopputulos löytyy `book`-hakemistosta. Voit avata sen selaimessasi:

_Firefox:_

```bash
$ firefox book/index.html                       # Linux
$ open -a "Firefox" book/index.html             # OS X
$ Start-Process "firefox.exe" .\book\index.html # Windows (PowerShell)
$ start firefox.exe .\book\index.html           # Windows (Cmd)
```

_Chrome:_

```bash
$ google-chrome book/index.html                 # Linux
$ open -a "Google Chrome" book/index.html       # OS X
$ Start-Process "chrome.exe" .\book\index.html  # Windows (PowerShell)
$ start chrome.exe .\book\index.html            # Windows (Cmd)
```

Suorita kirjan testit seuraavasti:

```bash
$ cd packages/trpl
$ mdbook test --library-path packages/trpl/target/debug/deps
```

## Osallistuminen

Haluaisimme apuasi! Katso [CONTRIBUTING.md][contrib] -tiedosto saadaksesi lisätietoa siitä, millaista tukea etsimme.

[contrib]: https://github.com/rust-lang/book/blob/main/CONTRIBUTING.md

Koska kirja julkaistaan myös [painettuna][nostarch], ja haluamme pitää verkossa olevan version mahdollisimman lähellä painettua versiota, saattaa kestää odotettua kauemmin, ennen kuin käsittelemme ongelmia tai vetopyyntöjä.

Olemme tähän mennessä tehneet suurempia päivityksiä [Rust Editions](https://doc.rust-lang.org/edition-guide/)-julkaisujen yhteydessä. Näiden isompien päivitysten välillä teemme vain virheenkorjauksia. Jos ongelmasi tai vetopyyntösi ei ole selkeä virheenkorjaus, se saattaa odottaa seuraavaa suurta päivitystä – tämä voi tarkoittaa kuukausia tai jopa vuosia. Kiitos kärsivällisyydestäsi!

### Käännökset

Haluaisimme apua kirjan kääntämisessä! Katso [Translations]-tunniste liittyäksesi käynnissä oleviin käännösprojekteihin. Jos haluat aloittaa uuden kielen käännöksen, avaa uusi issue! Odotamme [mdbook support] monikielistä tukea ennen kuin voimme yhdistää käännöksiä virallisesti, mutta voit silti aloittaa työn.

[Translations]: https://github.com/rust-lang/book/issues?q=is%3Aopen+is%3Aissue+label%3ATranslations
[mdbook support]: https://github.com/rust-lang/mdBook/issues/5

## Oikoluku

Voit tarkistaa lähdetiedostojen oikeinkirjoituksen käyttämällä spellcheck.sh-skriptiä, joka löytyy ci-hakemistosta. Se käyttää oikeiden sanojen sanastoa, joka on tallennettu ci/dictionary.txt-tiedostoon.

Jos skripti tuottaa väärän positiivisen virheen (esim. käytit sanaa BTreeMap, jota skripti ei tunnista), lisää kyseinen sana ci/dictionary.txt-tiedostoon (pidä sanat aakkosjärjestyksessä).
