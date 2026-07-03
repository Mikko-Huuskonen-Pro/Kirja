<!-- Old headings. Do not remove or links may break. -->
<a id="developing-the-librarys-functionality-with-test-driven-development"></a>

## Toiminnallisuuden lisääminen testivetoisella kehityksellä

Nyt kun hakulogiikka on _src/lib.rs_-tiedostossa erillään `main`-funktiosta,
on paljon helpompaa kirjoittaa testejä koodimme ydintoiminnallisuudelle. Voimme
kutsua funktioita suoraan eri argumenteilla ja tarkistaa palautusarvot kutsumatta
binääriämme komentoriviltä.

Tässä osiossa lisäämme hakulogiikan `minigrep`-ohjelmaan käyttäen testivetoista
kehitysprosessia (*test-driven development*, TDD) seuraavilla vaiheilla:

1. Kirjoita testi, joka epäonnistuu, ja aja se varmistaaksesi, että se epäonnistuu
   odottamastasi syystä.
2. Kirjoita tai muokkaa juuri tarpeeksi koodia, jotta uusi testi läpäisee.
3. Refaktoroi juuri lisäämäsi tai muuttamasi koodi ja varmista, että testit
   jatkavat läpäisemistä.
4. Toista vaiheesta 1!

Vaikka se on vain yksi monista tavoista kirjoittaa ohjelmistoa, TDD voi auttaa
ohjaamaan koodin suunnittelua. Testin kirjoittaminen ennen koodia, joka saa
testin läpäisemään, auttaa ylläpitämään korkeaa testikattavuutta koko prosessin
ajan.

Testivetoisesti toteutamme toiminnallisuuden, joka todella etsii hakumerkkijonoa
tiedoston sisällöstä ja tuottaa listan riveistä, jotka vastaavat hakua. Lisäämme
tämän toiminnallisuuden `search`-nimiseen funktioon.

### Epäonnistuvan testin kirjoittaminen

_src/lib.rs_-tiedostossa lisäämme `tests`-moduulin testifunktiolla, kuten teimme
luvussa 11. Testifunktio määrittää käyttäytymisen, jonka haluamme `search`-
funktiolla olevan: Se ottaa haun ja haettavan tekstin ja palauttaa vain rivit
tekstistä, jotka sisältävät haun. Listaus 12-15 näyttää tämän testin.

<Listing number="12-15" file-name="src/lib.rs" caption="Epäonnistuvan testin luominen `search`-funktiolle toiminnallisuudelle, jota toivoisimme olevan">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-15/src/lib.rs:here}}
```

</Listing>

Tämä testi etsii merkkijonoa `"duct"`. Haettava teksti on kolme riviä, joista
vain yksi sisältää `"duct"` (huomaa, että kenoviiva avaavan lainausmerkin
jälkeen kertoo Rustille olla laittamasta rivinvaihtomerkkiä tämän merkkijonoliteraalin
sisällön alkuun). Varmistamme, että `search`-funktion palauttama arvo sisältää
vain odottamamme rivin.

Jos ajamme tämän testin, se epäonnistuu tällä hetkellä, koska `unimplemented!`-
makro paniikkiutuu viestillä ”not implemented”. TDD-periaatteiden mukaisesti
otamme pienen askeleen lisäämällä juuri tarpeeksi koodia, jotta testi ei paniikkiudu
funktiota kutsuttaessa määrittelemällä `search`-funktion palauttamaan aina tyhjän
vektorin, kuten listauksessa 12-16. Sitten testin pitäisi kääntyä ja epäonnistua,
koska tyhjä vektori ei vastaa vektoria, joka sisältää rivin `"safe, fast,
productive."`.

<Listing number="12-16" file-name="src/lib.rs" caption="Juuri tarpeeksi `search`-funktion määrittelyä, jotta sen kutsuminen ei paniikkiudu">

```rust,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-16/src/lib.rs:here}}
```

</Listing>

Keskustellaan nyt, miksi meidän täytyy määrittää eksplisiittinen elinikä `'a`
`search`-funktion allekirjoituksessa ja käyttää sitä `contents`-argumentin ja
palautusarvon kanssa. Muista luvussa 10, että elinikäparametrit määrittävät,
mikä argumentin elinikä on yhdistetty palautusarvon elinikään. Tässä tapauksessa
ilmaisemme, että palautetun vektorin pitäisi sisältää merkkijonoviipaleita,
jotka viittaavat `contents`-argumentin viipaleisiin (eivät `query`-argumentin
viipaleisiin).

Toisin sanoen kerromme Rustille, että `search`-funktion palauttama data elää
niin kauan kuin `search`-funktiolle `contents`-argumentissa annettu data. Tämä
on tärkeää! Viipaleen _viittaaman_ datan täytyy olla kelvollista, jotta viittaus
on kelvollinen; jos kääntäjä olettaisi tekevämme merkkijonoviipaleita `query`-
argumentista `contents`-argumentin sijaan, se tekisi turvallisuustarkistuksensa
väärin.

Jos unohdamme elinikämerkinnät ja yritämme kääntää tämän funktion, saamme tämän
virheen:

```console
{{#include ../listings/ch12-an-io-project/output-only-02-missing-lifetimes/output.txt}}
```

Rust ei voi tietää, kumpaa kahdesta parametrista tarvitsemme tulosteeseen, joten
meidän täytyy kertoa se eksplisiittisesti. Huomaa, että ohjeteksti ehdottaa
saman elinikäparametrin määrittämistä kaikille parametreille ja tulostyypille,
mikä on virheellistä! Koska `contents` on parametri, joka sisältää kaiken
tekstimme ja haluamme palauttaa osat siitä tekstistä, jotka vastaavat, tiedämme,
että vain `contents` tulisi yhdistää palautusarvoon elinikäsyntaksilla.

Muut ohjelmointikielet eivät vaadi argumenttien yhdistämistä palautusarvoihin
allekirjoituksessa, mutta tästä käytännöstä tulee helpompaa ajan myötä. Saatat
haluta verrata tätä esimerkkiä luvun 10 osion [”Viittausten validointi
elinien avulla”][validating-references-with-lifetimes]<!-- ignore --> esimerkkeihin.

### Testin läpäisevän koodin kirjoittaminen

Tällä hetkellä testimme epäonnistuu, koska palautamme aina tyhjän vektorin.
Korjataksemme sen ja toteuttaaksemme `search`-funktion, ohjelmamme täytyy seurata
näitä vaiheita:

1. Käy läpi jokainen rivi sisällöstä.
2. Tarkista, sisältääkö rivi hakumerkkijonomme.
3. Jos sisältää, lisää se palautettavien arvojen listaan.
4. Jos ei sisällä, älä tee mitään.
5. Palauta vastaavien tulosten lista.

Työstetään jokainen vaihe, alkaen rivien läpikäynnistä.

#### Rivien läpikäynti `lines`-metodilla

Rustissa on hyödyllinen metodi merkkijonojen rivi riviltä -iterointiin, sopivasti
nimeltä `lines`, joka toimii kuten listauksessa 12-17. Huomaa, että tämä ei vielä
käänny.

<Listing number="12-17" file-name="src/lib.rs" caption="Jokaisen rivin läpikäynti `contents`-parametrissa">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-17/src/lib.rs:here}}
```

</Listing>

`lines`-metodi palauttaa iteraattorin. Käsittelemme iteraattoreita syvällisesti
luvussa 13. Mutta muista, että näit tämän iteraattorin käyttötavan listauksessa
3-5, jossa käytimme `for`-silmukkaa iteraattorin kanssa suorittaaksemme koodia
jokaiselle kokoelman kohteelle.

#### Haun etsiminen jokaiselta riviltä

Seuraavaksi tarkistamme, sisältääkö nykyinen rivi hakumerkkijonomme. Onneksi
merkkijonoilla on hyödyllinen metodi nimeltä `contains`, joka tekee tämän
meille! Lisää `contains`-metodin kutsu `search`-funktioon, kuten listauksessa
12-18. Huomaa, että tämä ei vielä käänny.

<Listing number="12-18" file-name="src/lib.rs" caption="Toiminnallisuuden lisääminen tarkistamaan, sisältääkö rivi `query`-merkkijonon">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-18/src/lib.rs:here}}
```

</Listing>

Tällä hetkellä rakennamme toiminnallisuutta. Saadaksemme koodin kääntymään
meidän täytyy palauttaa arvo rungosta, kuten ilmaisimme funktion allekirjoituksessa.

#### Vastaavien rivien tallentaminen

Viimeistelläksemme tämän funktion tarvitsemme tavan tallentaa vastaavat rivit,
jotka haluamme palauttaa. Voimme tehdä muuttuvan vektorin ennen `for`-silmukkaa
ja kutsua `push`-metodia tallentaaksemme `line`-rivin vektoriin. `for`-silmukan
jälkeen palautamme vektorin, kuten listauksessa 12-19.

<Listing number="12-19" file-name="src/lib.rs" caption="Vastaavien rivien tallentaminen, jotta voimme palauttaa ne">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-19/src/lib.rs:here}}
```

</Listing>

Nyt `search`-funktion pitäisi palauttaa vain rivit, jotka sisältävät `query`-merkkijonon,
ja testimme pitäisi läpäistä. Ajetaan testi:

```console
{{#include ../listings/ch12-an-io-project/listing-12-19/output.txt}}
```

Testimme läpäisi, joten tiedämme, että se toimii!

Tässä vaiheessa voisimme harkita refaktorointimahdollisuuksia hakufunktion
toteutuksessa pitäen testit läpäisevinä säilyttääksemme saman toiminnallisuuden.
Hakufunktion koodi ei ole liian huono, mutta se ei hyödynnä iteraattoreiden
hyödyllisiä ominaisuuksia. Palaamme tähän esimerkkiin luvussa 13, jossa tutkimme
iteraattoreita yksityiskohtaisesti, ja katsomme, miten sitä voisi parantaa.

Nyt koko ohjelman pitäisi toimia! Kokeillaan sitä, ensin sanalla, joka pitäisi
palauttaa täsmälleen yksi rivi Emily Dickinsonin runosta: _frog_.

```console
{{#include ../listings/ch12-an-io-project/no-listing-02-using-search-in-run/output.txt}}
```

Siistiä! Kokeillaan sitten sanaa, joka vastaa useita rivejä, kuten _body_:

```console
{{#include ../listings/ch12-an-io-project/output-only-03-multiple-matches/output.txt}}
```

Ja lopuksi varmistetaan, ettei saamme rivejä, kun etsimme sanaa, jota ei ole
missään runossa, kuten _monomorphization_:

```console
{{#include ../listings/ch12-an-io-project/output-only-04-no-matches/output.txt}}
```

Erinomaista! Olemme rakentaneet oman pienen version klassisesta työkalusta ja
oppineet paljon sovellusten rakentamisesta. Olemme myös oppineet hieman tiedoston
syöttöä ja tulostusta, eliniöitä, testausta ja komentorivin jäsentämistä.

Viimeistelläksemme tämän projektin demonstroimme lyhyesti, miten työskennellä
ympäristömuuttujien kanssa ja miten tulostaa vakiovirheeseen, molemmat hyödyllisiä
kirjoitettaessa komentoriviohjelmia.

[validating-references-with-lifetimes]: ch10-03-lifetime-syntax.html#validating-references-with-lifetimes
[ch11-anatomy]: ch11-01-writing-tests.html#the-anatomy-of-a-test-function
[ch10-lifetimes]: ch10-03-lifetime-syntax.html
[ch3-iter]: ch03-05-control-flow.html#looping-through-a-collection-with-for
[ch13-iterators]: ch13-02-iterators.html
