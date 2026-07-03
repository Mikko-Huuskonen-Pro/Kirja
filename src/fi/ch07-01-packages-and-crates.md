## Paketit ja crate:t

Moduulijärjestelmän ensimmäiset osat, joita käsittelemme, ovat paketit ja crate:t.

_Crate_ on pienin määrä koodia, jota Rust-kääntäjä käsittelee kerrallaan. Vaikka käyttäisit `rustc`-komentoa `cargo`-komennon sijaan ja antaisit yhden lähdekooditiedoston (kuten teimme jo [”Rust-ohjelman perusteet”][basics]<!-- ignore
-->-kohdassa luvussa 1), kääntäjä pitää kyseistä tiedostoa crate:na. Crate:t voivat sisältää moduuleja, ja moduulit voidaan määritellä muissa tiedostoissa, jotka käännetään crate:n mukana, kuten tulemme näkemään seuraavissa osioissa.

Crate voi olla jommassakummassa muodossa: binääricrate tai kirjastocrate.
_Binääricrate:t_ ovat ohjelmia, jotka voidaan kääntää ajettavaksi suoritettavaksi tiedostoksi, kuten komentoriviohjelma tai palvelin. Jokaisella on oltava `main`-funktio, joka määrittää, mitä tapahtuu suoritettavan käynnistyessä. Kaikki tähän mennessä luomamme crate:t ovat olleet binääricrate:ja.

_Kirjastocrate:illa_ ei ole `main`-funktiota, eivätkä ne käänny suoritettaviksi tiedostoiksi. Sen sijaan ne määrittelevät toiminnallisuutta, joka on tarkoitettu jaettavaksi useiden projektien kesken. Esimerkiksi `rand`-crate, jota käytimme [luvussa 2][rand]<!-- ignore -->, tarjoaa toiminnallisuutta satunnaisten lukujen generointiin. Useimmiten kun rustilaiset sanovat ”crate”, he tarkoittavat kirjastocrate:a, ja he käyttävät sanaa ”crate” vaihdettavasti yleisen ohjelmointikäsitteen ”kirjasto” kanssa.

_Crate-juuri_ on lähdekooditiedosto, josta Rust-kääntäjä aloittaa ja joka muodostaa crate:si juurimoduulin (käsittelemme moduuleja perusteellisesti kohdassa [”Laajuuden ja yksityisyyden hallinta moduuleilla”][modules]<!-- ignore -->).

_Paketti_ on yhden tai useamman crate:n kokoelma, joka tarjoaa tietyn toiminnallisuuden. Paketti sisältää _Cargo.toml_-tiedoston, joka kuvaa, miten nämä crate:t rakennetaan. Cargo on itse asiassa paketti, joka sisältää binääricrate:n komentorivityökalulle, jota olet käyttänyt koodisi kääntämiseen. Cargo-paketti sisältää myös kirjastocrate:n, josta binääricrate riippuu. Muut projektit voivat riippua Cargo-kirjastocrate:sta käyttääkseen samaa logiikkaa, jota Cargo-komentorivityökalu käyttää.

Paketti voi sisältää niin monta binääricrate:a kuin haluat, mutta enintään yhden kirjastocrate:n. Paketissa on oltava vähintään yksi crate, olipa se kirjasto- tai binääricrate.

Käydään läpi, mitä tapahtuu, kun luomme paketin. Ensin annamme komennon `cargo new my-project`:

```console
$ cargo new my-project
     Created binary (application) `my-project` package
$ ls my-project
Cargo.toml
src
$ ls my-project/src
main.rs
```

Kun olemme suorittaneet `cargo new my-project`, käytämme `ls`-komentoa nähdäksemme, mitä Cargo luo. _my-project_-hakemistossa on _Cargo.toml_-tiedosto, joka muodostaa paketin. Siellä on myös _src_-hakemisto, joka sisältää _main.rs_-tiedoston. Avaa _Cargo.toml_ tekstieditorissasi ja huomaa, ettei siinä mainita _src/main.rs_:ää. Cargo noudattaa käytäntöä, jonka mukaan _src/main.rs_ on binääricrate:n crate-juuri, jolla on sama nimi kuin paketilla. Vastaavasti Cargo tietää, että jos pakettihakemisto sisältää _src/lib.rs_:n, paketti sisältää kirjastocrate:n, jolla on sama nimi kuin paketilla, ja _src/lib.rs_ on sen crate-juuri. Cargo välittää crate-juuritiedostot `rustc`-kääntäjälle kirjaston tai binäärin rakentamiseksi.

Tässä meillä on paketti, joka sisältää vain _src/main.rs_:n, eli se sisältää vain binääricrate:n nimeltä `my-project`. Jos paketti sisältää sekä _src/main.rs_:n että _src/lib.rs_:n, siinä on kaksi crate:a: binääri ja kirjasto, molemmilla sama nimi kuin paketilla. Paketissa voi olla useita binääricrate:ja sijoittamalla tiedostoja _src/bin_-hakemistoon: jokainen tiedosto on erillinen binääricrate.

[basics]: ch01-02-hello-world.html#rust-program-basics
[modules]: ch07-02-defining-modules-to-control-scope-and-privacy.html
[rand]: ch02-00-guessing-game-tutorial.html#generating-a-random-number
