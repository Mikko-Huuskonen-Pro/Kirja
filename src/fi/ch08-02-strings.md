## UTF-8-koodatun tekstin tallentaminen merkkijonoihin

Käsittelimme merkkijonoja luvussa 4, mutta tarkastelemme niitä nyt syvällisemmin.
Rustia opettelevat kehittäjät jäävät usein jumiin merkkijonojen kanssa kolmen
syyn yhdistelmän vuoksi: Rustin taipumus paljastaa mahdollisia virheitä, se että
merkkijonot ovat monimutkaisempia tietorakenteita kuin monet ohjelmoijat antavat
niille kunniaa, ja UTF-8. Nämä tekijät yhdistyvät tavalla, joka voi tuntua
vaikealta, kun tulet muista ohjelmointikielistä.

Käsittelemme merkkijonoja kokoelmien yhteydessä, koska merkkijonot on
toteutettu tavujen kokoelmana sekä joitakin metodeja, jotka tarjoavat hyödyllistä
toiminnallisuutta, kun nuo tavut tulkitaan tekstinä. Tässä osiossa käymme läpi
`String`-tyypin operaatiot, joita jokaisella kokoelmatyypillä on, kuten
luominen, päivittäminen ja lukeminen. Käsittelemme myös tavat, joilla `String`
eroaa muista kokoelmista, eli sitä, miten `String`-datan indeksointi on
monimutkaista sen vuoksi, miten ihmiset ja tietokoneet tulkitsevat
`String`-dataa.

### Mikä on merkkijono?

Määrittelemme ensin, mitä tarkoitamme termillä _merkkijono_. Rustissa on vain
yksi merkkijonotyyppi kieliytimessä, ja se on merkkijonoviipale `str`, jota
nähdään yleensä lainattuna muotona `&str`. Luvussa 4 käsittelimme
_merkkijonoviipaleita_, jotka ovat viittauksia jossain muualla tallennettuun
UTF-8-koodattuun merkkijonodataan. Merkkijonoliteraalit, esimerkiksi, on
tallennettu ohjelman binaariin ja ovat siksi merkkijonoviipaleita.

`String`-tyyppi, jonka Rustin standardikirjasto tarjoaa eikä kieliydin koodaa
sisään, on kasvava, muuttuva, omistettu, UTF-8-koodattu merkkijonotyyppi. Kun
Rust-kehittäjät viittaavat Rustin "merkkijonoihin", he saattavat tarkoittaa
joko `String`- tai merkkijonoviipaletyyppiä `&str`, ei vain yhtä näistä
tyypeistä. Vaikka tämä osio käsittelee pääosin `String`-tyyppiä, molempia
tyyppejä käytetään runsaasti Rustin standardikirjastossa, ja sekä `String` että
merkkijonoviipaleet ovat UTF-8-koodattuja.

### Uuden merkkijonon luominen

Monet samat operaatiot, jotka ovat käytettävissä `Vec<T>`-tyypillä, ovat
käytettävissä myös `String`-tyypillä, koska `String` on itse asiassa toteutettu
kääreenä tavuvektorin ympärillä joillakin ylimääräisillä takeilla, rajoituksilla
ja ominaisuuksilla. Esimerkki funktiosta, joka toimii samalla tavalla
`Vec<T>`- ja `String`-tyypeillä, on `new`-funktio instanssin luomiseen, kuten
listauksessa 8-11.

<Listing number="8-11" caption="Uuden, tyhjän `String`-olion luominen">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-11/src/main.rs:here}}
```

</Listing>

Tämä rivi luo uuden, tyhjän merkkijonon nimeltä `s`, johon voimme sitten ladata
dataa. Usein meillä on joitakin alkudataa, joilla haluamme aloittaa
merkkijonon. Siihen käytämme `to_string`-metodia, joka on käytettävissä
millä tahansa tyypillä, joka toteuttaa `Display`-traitin, kuten
merkkijonoliteraalit tekevät. Listaus 8-12 näyttää kaksi esimerkkiä.

<Listing number="8-12" caption="`to_string`-metodin käyttö `String`-olion luomiseen merkkijonoliteraalista">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-12/src/main.rs:here}}
```

</Listing>

Tämä koodi luo merkkijonon, joka sisältää `initial contents`.

Voimme myös käyttää funktiota `String::from` luodaksemme `String`-olion
merkkijonoliteraalista. Listauksen 8-13 koodi on vastaava kuin listauksen 8-12
koodi, joka käyttää `to_string`-metodia.

<Listing number="8-13" caption="`String::from`-funktion käyttö `String`-olion luomiseen merkkijonoliteraalista">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-13/src/main.rs:here}}
```

</Listing>

Koska merkkijonoja käytetään niin moniin asioihin, voimme käyttää monia erilaisia
geneerisiä rajapintoja merkkijonoille, mikä tarjoaa meille paljon vaihtoehtoja.
Joistakin ne saattavat tuntua päällekkäisiltä, mutta jokaisella on paikkansa!
Tässä tapauksessa `String::from` ja `to_string` tekevät saman asian, joten
kumpaa valitsetkin, on tyyli- ja luettavuuskysymys.

Muista, että merkkijonot ovat UTF-8-koodattuja, joten voimme sisällyttää niihin
mitä tahansa oikein koodattua dataa, kuten listauksessa 8-14.

<Listing number="8-14" caption="Tervehdyksien tallentaminen eri kielillä merkkijonoihin">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:here}}
```

</Listing>

Kaikki nämä ovat kelvollisia `String`-arvoja.

### Merkkijonon päivittäminen

`String` voi kasvaa koossa ja sen sisältö voi muuttua, aivan kuten `Vec<T>`-tyypin
sisältö, jos työnnät siihen lisää dataa. Lisäksi voit kätevästi käyttää
`+`-operaattoria tai `format!`-makroa yhdistääksesi `String`-arvoja.

#### Merkkijonon jatkaminen `push_str`- ja `push`-metodeilla

Voimme kasvattaa `String`-oliota käyttämällä `push_str`-metodia liittääksemme
merkkijonoviipaleen, kuten listauksessa 8-15.

<Listing number="8-15" caption="Merkkijonoviipaleen liittäminen `String`-olioon `push_str`-metodilla">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-15/src/main.rs:here}}
```

</Listing>

Näiden kahden rivin jälkeen `s` sisältää `foobar`. `push_str`-metodi ottaa
merkkijonoviipaleen, koska emme välttämättä halua ottaa parametrin omistusta.
Esimerkiksi listauksen 8-16 koodissa haluamme pystyä käyttämään `s2`:ta sen
sisällön liittämisen jälkeen `s1`:een.

<Listing number="8-16" caption="Merkkijonoviipaleen käyttö sen sisällön liittämisen jälkeen `String`-olioon">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-16/src/main.rs:here}}
```

</Listing>

Jos `push_str`-metodi ottaisi `s2`:n omistuksen, emme voisi tulostaa sen arvoa
viimeisellä rivillä. Tämä koodi kuitenkin toimii odotetulla tavalla!

`push`-metodi ottaa yhden merkin parametrina ja lisää sen `String`-olioon.
Listaus 8-17 lisää kirjaimen _l_ `String`-olioon `push`-metodilla.

<Listing number="8-17" caption="Yhden merkin lisääminen `String`-arvoon `push`-metodilla">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-17/src/main.rs:here}}
```

</Listing>

Tuloksena `s` sisältää `lol`.

#### Yhdistäminen `+`-operaattorilla tai `format!`-makrolla

Usein haluat yhdistää kaksi olemassa olevaa merkkijonoa. Yksi tapa tehdä se on
käyttää `+`-operaattoria, kuten listauksessa 8-18.

<Listing number="8-18" caption="`+`-operaattorin käyttö kahden `String`-arvon yhdistämiseen uudeksi `String`-arvoksi">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-18/src/main.rs:here}}
```

</Listing>

Merkkijono `s3` sisältää `Hello, world!`. Syy siihen, miksi `s1` ei ole enää
kelvollinen yhteenlaskun jälkeen, ja syy siihen, miksi käytimme viitettä
`s2`:een, liittyy metodin allekirjoitukseen, jota kutsutaan kun käytämme
`+`-operaattoria. `+`-operaattori käyttää `add`-metodia, jonka allekirjoitus
näyttää suunnilleen tältä:

```rust,ignore
fn add(self, s: &str) -> String {
```

Standardikirjastossa näet `add`-metodin määriteltynä geneerisillä tyypeillä ja
assosioiduilla tyypeillä. Tässä olemme korvanneet konkreettisilla tyypeillä,
mitä tapahtuu kun kutsumme tätä metodia `String`-arvoilla. Käsittelemme
geneerisiä tyyppejä luvussa 10. Tämä allekirjoitus antaa meille vihjeet, joita
tarvitsemme ymmärtääksemme `+`-operaattorin hankalat kohdat.

Ensinnäkin `s2`:lla on `&`, mikä tarkoittaa, että lisäämme _viittauksen_
toisesta merkkijonosta ensimmäiseen merkkijonoon. Tämä johtuu `add`-funktion
`s`-parametrista: voimme lisätä vain `&str`-tyypin `String`-olioon; emme voi
lisätä kahta `String`-arvoa yhteen. Mutta odota—tyyppi `&s2` on `&String`, ei
`&str`, kuten `add`-metodin toinen parametri määrittää. Miksi listaus 8-18
sitten kääntyy?

Syy siihen, miksi voimme käyttää `&s2`:ta `add`-kutsussa, on se, että kääntäjä
voi _pakottaa_ `&String`-argumentin muotoon `&str`. Kun kutsumme `add`-metodia,
Rust käyttää _deref-pakotusta_ (*deref coercion*), joka tässä muuttaa `&s2`:n
muotoon `&s2[..]`. Käsittelemme deref-pakotusta syvällisemmin luvussa 15. Koska
`add` ei ota `s`-parametrin omistusta, `s2` on edelleen kelvollinen `String`
tämän operaation jälkeen.

Toiseksi näemme allekirjoituksesta, että `add` ottaa `self`:n omistuksen, koska
`self`:llä _ei_ ole `&`-merkintää. Tämä tarkoittaa, että listauksen 8-18 `s1`
siirtyy `add`-kutsuun eikä ole enää kelvollinen sen jälkeen. Vaikka
`let s3 = s1 + &s2;` näyttää siltä, että se kopioisi molemmat merkkijonot ja
loisi uuden, tämä lause itse asiassa ottaa `s1`:n omistuksen, liittää kopion
`s2`:n sisällöstä ja palauttaa tuloksen omistuksen. Toisin sanoen se näyttää
tekevän paljon kopioita, mutta ei tee; toteutus on tehokkaampi kuin kopiointi.

Jos meidän täytyy yhdistää useita merkkijonoja, `+`-operaattorin käyttäytyminen
käy hankalaksi:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-01-concat-multiple-strings/src/main.rs:here}}
```

Tässä vaiheessa `s` on `tic-tac-toe`. Kaikkien `+`- ja `"`-merkkien kanssa on
vaikea nähdä, mitä tapahtuu. Monimutkaisempien yhdistämistapojen kohdalla
voimme sen sijaan käyttää `format!`-makroa:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-02-format/src/main.rs:here}}
```

Tämä koodi asettaa myös `s`:n arvoksi `tic-tac-toe`. `format!`-makro toimii
kuten `println!`, mutta tulostaa tulosteen ruudulle sen sijaan, että se palauttaa
`String`-olion sisällöllä. `format!`-makroa käyttävä koodiversio on paljon
helpompi lukea, ja `format!`-makron generoima koodi käyttää viittauksia, joten
tämä kutsu ei ota minkään parametreistaan omistusta.

### Merkkijonojen indeksointi

Monissa muissa ohjelmointikielissä yksittäisiin merkkeihin merkkijonossa
viittaaminen indeksillä on kelvollinen ja yleinen operaatio. Jos kuitenkin
yrität käyttää indeksointisyntaksia `String`-olion osiin Rustissa, saat
virheen. Harkitse kelvotonta koodia listauksessa 8-19.

<Listing number="8-19" caption="Indeksointisyntaksin yrittäminen `String`-olion kanssa">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-19/src/main.rs:here}}
```

</Listing>

Tämä koodi johtaa seuraavaan virheeseen:

```console
{{#include ../listings/ch08-common-collections/listing-08-19/output.txt}}
```

Virhe ja huomautus kertovat tarinan: Rustin merkkijonot eivät tue indeksointia.
Mutta miksi ei? Vastataksemme siihen kysymykseen meidän täytyy käsitellä, miten
Rust tallentaa merkkijonot muistiin.

#### Sisäinen esitys

`String` on kääre `Vec<u8>`-tyypin ympärillä. Katsotaan joitakin oikein
koodattuja UTF-8-esimerkkimerkkijonojamme listauksesta 8-14. Ensin tämä:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:spanish}}
```

Tässä tapauksessa `len` on `4`, mikä tarkoittaa, että merkkijonoa `"Hola"`
tallentava vektori on 4 tavua pitkä. Jokainen näistä kirjaimista vie yhden tavun
UTF-8-koodauksessa. Seuraava rivi saattaa kuitenkin yllättää (huomaa, että tämä
merkkijono alkaa kyrillisen isolla kirjaimella _Ze_, ei numerolla 3):

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:russian}}
```

Jos sinulta kysyttäisiin, kuinka pitkä merkkijono on, saatat sanoa 12. Itse
asiassa Rustin vastaus on 24: se on tavujen määrä, joita tarvitaan
"Здравствуйте"-merkkijonon koodaamiseen UTF-8:ssa, koska jokainen Unicode-skaalaarvo
tässä merkkijonossa vie 2 tavua tallennustilaa. Siksi indeksi merkkijonon
tavuihin ei aina vastaa kelvollista Unicode-skaalaarvoa. Havainnollistukseksi
harkitse tätä kelvotonta Rust-koodia:

```rust,ignore,does_not_compile
let hello = "Здравствуйте";
let answer = &hello[0];
```

Tiedät jo, että `answer` ei ole `З`, ensimmäinen kirjain. UTF-8-koodauksessa
`З`:n ensimmäinen tavu on `208` ja toinen on `151`, joten näyttäisi siltä, että
`answer`:n pitäisi olla `208`, mutta `208` ei ole kelvollinen merkki yksinään.
`208`:n palauttaminen ei todennäköisesti ole sitä, mitä käyttäjä haluaisi, jos
hän pyytäisi tämän merkkijonon ensimmäistä kirjainta; kuitenkin se on ainoa
data, joka Rustilla on tavuindeksissä 0. Käyttäjät eivät yleensä halua tavuarvoa
palautettavaksi, vaikka merkkijono sisältäisi vain latinalaisia kirjaimia: jos
`&"hi"[0]` olisi kelvollista koodia, joka palauttaisi tavuarvon, se palauttaisi
`104`:n, ei `h`:ta.

Vastaus on siis, että odottamattoman arvon palauttamisen ja virheiden
välttämiseksi, joita ei ehkä huomata heti, Rust ei käännä tätä koodia lainkaan
ja estää väärinkäsitykset varhaisessa kehitysvaiheessa.

#### Tavut, skaalaarvot ja grafeemiklusterit! Voi ei!

Toinen huomio UTF-8:sta on, että merkkijonoihin on itse asiassa kolme
olennaista tapaa katsoa Rustin näkökulmasta: tavuina, skaalaarvoina ja
grafeemiklustereina (lähin vastine sille, mitä kutsumme _kirjaimiksi_).

Jos katsomme hindinkielistä sanaa "नमस्ते" devanagari-kirjoituksella, se
tallennetaan `u8`-arvojen vektorina, joka näyttää tältä:

```text
[224, 164, 168, 224, 164, 174, 224, 164, 184, 224, 165, 141, 224, 164, 164,
224, 165, 135]
```

Se on 18 tavua ja näin tietokoneet lopulta tallentavat tämän datan. Jos
katsomme niitä Unicode-skaalaarvoina, joita Rustin `char`-tyyppi edustaa, nuo
tavut näyttävät tältä:

```text
['न', 'म', 'स', '्', 'त', 'े']
```

Tässä on kuusi `char`-arvoa, mutta neljäs ja kuudes eivät ole kirjaimia: ne
ovat diakriittisiä merkkejä, joilla ei ole järkeä yksinään. Lopuksi, jos
katsomme niitä grafeemiklustereina, saamme sen, mitä ihminen kutsuisi
hindinkielisen sanan neljäksi kirjaimiksi:

```text
["न", "म", "स्", "ते"]
```

Rust tarjoaa erilaisia tapoja tulkita raakaa merkkijonodataa, jota tietokoneet
tallentavat, jotta jokainen ohjelma voi valita tarvitsemansa tulkinnan
riippumatta siitä, millä ihmiskielellä data on.

Viimeinen syy siihen, miksi Rust ei salli indeksointia `String`-olioon merkin
saamiseksi, on se, että indeksointioperointien odotetaan aina vievän vakioajan
(O(1)). Mutta tällaista suorituskykyä ei voi taata `String`-tyypillä, koska
Rustin täytyisi käydä sisältö läpi alusta indeksiin määrittääkseen, kuinka monta
kelvollista merkkiä siinä on.

### Merkkijonojen viipaleet

Indeksointi merkkijonoon on usein huono idea, koska ei ole selvää, mikä
merkkijonon indeksointioperoinnin paluutyyppi pitäisi olla: tavu, merkki,
grafeemiklusteri vai merkkijonoviipale. Jos todella tarvitset käyttää indeksejä
merkkijonoviipaleiden luomiseen, Rust pyytää sinua olemaan tarkempi.

Sen sijaan, että indeksoisit `[]`-syntaksilla yhdellä numerolla, voit käyttää
`[]`-syntaksia väliarvolla luodaksesi merkkijonoviipaleen, joka sisältää
tietyt tavut:

```rust
let hello = "Здравствуйте";

let s = &hello[0..4];
```

Tässä `s` on `&str`, joka sisältää merkkijonon ensimmäiset neljä tavua.
Aiemmin mainitsimme, että jokainen näistä merkeistä oli kaksi tavua, mikä
tarkoittaa, että `s` on `Зд`.

Jos yrittäisimme viipaloida vain osan merkin tavuista esimerkiksi
`&hello[0..1]`:llä, Rust panikoi ajonaikana samalla tavalla kuin jos
vektorissa käytettäisiin kelvotonta indeksiä:

```console
{{#include ../listings/ch08-common-collections/output-only-01-not-char-boundary/output.txt}}
```

Sinun pitäisi olla varovainen luodessasi merkkijonoviipaleita väliarvoilla,
koska se voi kaataa ohjelmasi.

### Merkkijonojen läpikäyntimetodit

Paras tapa käsitellä merkkijonon osia on olla eksplisiittinen siitä, haluatko
merkkejä vai tavuja. Yksittäisiä Unicode-skaalaarvoja varten käytä `chars`-metodia.
`chars`-metodin kutsuminen merkkijonolla "Зд" erottelee ja palauttaa kaksi
`char`-tyyppistä arvoa, ja voit iteroida tuloksen läpi päästäksesi käsiksi
jokaiseen alkioon:

```rust
for c in "Зд".chars() {
    println!("{c}");
}
```

Tämä koodi tulostaa seuraavan:

```text
З
д
```

Vaihtoehtoisesti `bytes`-metodi palauttaa jokaisen raakatavu, mikä saattaa olla
sopivaa sinun käyttöalueellesi:

```rust
for b in "Зд".bytes() {
    println!("{b}");
}
```

Tämä koodi tulostaa neljä tavua, joista tämä merkkijono koostuu:

```text
208
151
208
180
```

Muista kuitenkin, että kelvolliset Unicode-skaalaarvot voivat koostua useammasta
kuin yhdestä tavusta.

Grafeemiklusterien saaminen merkkijonoista, kuten devanagari-kirjoituksessa, on
monimutkaista, joten standardikirjasto ei tarjoa tätä toiminnallisuutta.
Crates.io-sivustolta löytyy [crates.io](https://crates.io/)<!-- ignore --> -paketteja,
jos tarvitset tätä toiminnallisuutta.

### Merkkijonot eivät ole niin yksinkertaisia

Yhteenvetona merkkijonot ovat monimutkaisia. Eri ohjelmointikielet tekevät
erilaisia valintoja siitä, miten tämä monimutkaisuus esitetään ohjelmoijalle.
Rust on valinnut tehdä `String`-datan oikeasta käsittelystä oletuskäyttäytymisen
kaikille Rust-ohjelmille, mikä tarkoittaa, että ohjelmoijien täytyy miettiä
UTF-8-datan käsittelyä etukäteen enemmän. Tämä kompromissi paljastaa enemmän
merkkijonojen monimutkaisuutta kuin muissa ohjelmointikielissä näkyy, mutta se
estää sinua joutumasta käsittelemään ei-ASCII-merkkeihin liittyviä virheitä
myöhemmin kehityssyklin aikana.

Hyvä uutinen on, että standardikirjasto tarjoaa paljon toiminnallisuutta, joka
perustuu `String`- ja `&str`-tyyppeihin auttamaan näiden monimutkaisten
tilanteiden oikeassa käsittelyssä. Muista tutustua dokumentaatioon hyödyllisistä
metodeista, kuten `contains` merkkijonosta etsimiseen ja `replace` merkkijonon
osien korvaamiseen toisella merkkijonolla.

Siirrytään hieman vähemmän monimutkaiseen asiaan: hajautustauluihin!
