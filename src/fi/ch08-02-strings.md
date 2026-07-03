## UTF-8-koodatun tekstin tallentaminen merkkijonoilla

Käsittelimme merkkijonoja luvussa 4, mutta tarkastelemme niitä nyt syvällisemmin. Uudet rustilaiset jäävät usein jumiin merkkijonoihin kolmen syyn yhdistelmän vuoksi: Rustin taipumus paljastaa mahdolliset virheet, merkkijonojen oleminen monimutkaisempia tietorakenteita kuin monet ohjelmoijat antavat niille tunnustusta, ja UTF-8. Nämä tekijät yhdistyvät tavalla, joka voi tuntua vaikealta, kun tulet muista ohjelmointikielistä.

Käsittelemme merkkijonoja kokoelmien yhteydessä, koska merkkijonot on toteutettu tavujen kokoelmana plus joitakin metodeja hyödyllisen toiminnallisuuden tarjoamiseksi, kun näitä tavuja tulkitaan tekstinä. Tässä osiossa käsittelemme `String`-tyypin operaatioita, joita jokaisella kokoelmatyypillä on, kuten luominen, päivittäminen ja lukeminen. Käsittelemme myös tapoja, joilla `String` eroaa muista kokoelmista, nimittäin sitä, miten `String`-tyyppiin indeksointi on monimutkaista ihmisten ja tietokoneiden eri tulkintojen vuoksi `String`-datasta.

<!-- Old headings. Do not remove or links may break. -->

<a id="what-is-a-string"></a>

### Merkkijonojen määrittely

Määrittelemme ensin, mitä tarkoitamme termillä _merkkijono_. Rustissa on vain yksi merkkijonotyyppi ydinkielessä, joka on merkkijonoviipale `str`, joka nähdään yleensä lainatussa muodossaan `&str`. Luvussa 4 käsittelimme merkkijonoviipaleita, jotka ovat viittauksia jossain muualla tallennettuun UTF-8-koodattuun merkkijonodataan. Merkkijonoliteraalit, esimerkiksi, tallennetaan ohjelman binääritiedostoon ja ovat siksi merkkijonoviipaleita.

`String`-tyyppi, jonka Rustin standardikirjasto tarjoaa eikä ydinkieli koodaa, on kasvava, muuttuva, omistettu, UTF-8-koodattu merkkijonotyyppi. Kun rustilaiset viittaavat Rustissa ”merkkijonoihin”, he saattavat viitata joko `String`- tai merkkijonoviipaletyyppiin `&str`, ei vain toiseen näistä tyypeistä. Vaikka tämä osio käsittelee pääasiassa `String`:ia, molempia tyyppejä käytetään runsaasti Rustin standardikirjastossa, ja sekä `String` että merkkijonoviipaleet ovat UTF-8-koodattuja.

### Uuden merkkijonon luominen

Monet samat operaatiot, jotka ovat saatavilla `Vec<T>`:n kanssa, ovat saatavilla myös `String`:in kanssa, koska `String` on itse asiassa toteutettu tavujen vektorin kääreenä joillakin ylimääräisillä takuilla, rajoituksilla ja ominaisuuksilla. Esimerkki funktiosta, joka toimii samalla tavalla `Vec<T>`:n ja `String`:in kanssa, on `new`-funktio instanssin luomiseen, kuten listauksessa 8-11.

<Listing number="8-11" caption="Uuden tyhjän `String`:in luominen">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-11/src/main.rs:here}}
```

</Listing>

Tämä rivi luo uuden tyhjän merkkijonon nimeltä `s`, johon voimme sitten ladata dataa. Usein meillä on joitakin alkudataa, joilla haluamme aloittaa merkkijonon. Tätä varten käytämme `to_string`-metodia, joka on saatavilla millä tahansa tyypillä, joka toteuttaa `Display`-traitin, kuten merkkijonoliteraalit. Listaus 8-12 näyttää kaksi esimerkkiä.

<Listing number="8-12" caption="`to_string`-metodin käyttö `String`:in luomiseksi merkkijonoliteraalista">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-12/src/main.rs:here}}
```

</Listing>

Tämä koodi luo merkkijonon, joka sisältää `initial contents`.

Voimme myös käyttää funktiota `String::from` luodaksemme `String`:in merkkijonoliteraalista. Listauksen 8-13 koodi on vastaava listauksen 8-12 koodille, joka käyttää `to_string`:ia.

<Listing number="8-13" caption="`String::from`-funktion käyttö `String`:in luomiseksi merkkijonoliteraalista">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-13/src/main.rs:here}}
```

</Listing>

Koska merkkijonoja käytetään niin moniin asioihin, voimme käyttää monia erilaisia geneerisiä API:ja merkkijonoille, mikä tarjoaa meille paljon vaihtoehtoja. Jotkut niistä saattavat vaikuttaa tarpeettomilta, mutta niillä kaikilla on paikkansa! Tässä tapauksessa `String::from` ja `to_string` tekevät saman asian, joten kumpi valitset on tyyli- ja luettavuuskysymys.

Muista, että merkkijonot ovat UTF-8-koodattuja, joten voimme sisällyttää niihin mitä tahansa oikein koodattua dataa, kuten listauksessa 8-14.

<Listing number="8-14" caption="Tervehdysten tallentaminen eri kielillä merkkijonoihin">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:here}}
```

</Listing>

Kaikki nämä ovat kelvollisia `String`-arvoja.

### Merkkijonon päivittäminen

`String` voi kasvaa kooltaan ja sen sisältö voi muuttua, aivan kuten `Vec<T>`:n sisältö, jos työnnät siihen lisää dataa. Lisäksi voit kätevästi käyttää `+`-operaattoria tai `format!`-makroa `String`-arvojen yhdistämiseen.

<!-- Old headings. Do not remove or links may break. -->

<a id="appending-to-a-string-with-push_str-and-push"></a>

#### Liittäminen `push_str`:lla tai `push`:lla

Voimme kasvattaa `String`:ia käyttämällä `push_str`-metodia liittääksemme merkkijonoviipaleen, kuten listauksessa 8-15.

<Listing number="8-15" caption="Merkkijonoviipaleen liittäminen `String`:iin `push_str`-metodilla">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-15/src/main.rs:here}}
```

</Listing>

Näiden kahden rivin jälkeen `s` sisältää `foobar`. `push_str`-metodi ottaa merkkijonoviipaleen, koska emme välttämättä halua ottaa parametrin omistusta. Esimerkiksi listauksen 8-16 koodissa haluamme pystyä käyttämään `s2`:ta sen sisällön liittämisen jälkeen `s1`:een.

<Listing number="8-16" caption="Merkkijonoviipaleen käyttö sen sisällön liittämisen jälkeen `String`:iin">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-16/src/main.rs:here}}
```

</Listing>

Jos `push_str`-metodi ottaisi `s2`:n omistuksen, emme voisi tulostaa sen arvoa viimeisellä rivillä. Tämä koodi kuitenkin toimii odotetusti!

`push`-metodi ottaa yhden merkin parametrina ja lisää sen `String`:iin. Listaus 8-17 lisää kirjaimen _l_ `String`:iin `push`-metodilla.

<Listing number="8-17" caption="Yhden merkin lisääminen `String`-arvoon `push`:lla">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-17/src/main.rs:here}}
```

</Listing>

Tuloksena `s` sisältää `lol`.

<!-- Old headings. Do not remove or links may break. -->

<a id="concatenation-with-the--operator-or-the-format-macro"></a>

#### Yhdistäminen `+`:lla tai `format!`:lla

Usein haluat yhdistää kaksi olemassa olevaa merkkijonoa. Yksi tapa tehdä se on käyttää `+`-operaattoria, kuten listauksessa 8-18.

<Listing number="8-18" caption="`+`-operaattorin käyttö kahden `String`-arvon yhdistämiseksi uudeksi `String`-arvoksi">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-18/src/main.rs:here}}
```

</Listing>

Merkkijono `s3` sisältää `Hello, world!`. Syy siihen, miksi `s1` ei ole enää kelvollinen lisäyksen jälkeen, ja syy siihen, miksi käytimme viitettä `s2`:een, liittyy metodin allekirjoitukseen, jota kutsutaan kun käytämme `+`-operaattoria. `+`-operaattori käyttää `add`-metodia, jonka allekirjoitus näyttää suunnilleen tältä:

```rust,ignore
fn add(self, s: &str) -> String {
```

Standardikirjastossa näet `add`:n määriteltynä geneerisillä tyypeillä ja assosioituilla tyypeillä. Tässä olemme korvanneet konkreettisilla tyypeillä, mikä tapahtuu kun kutsumme tätä metodia `String`-arvoilla. Käsittelemme geneerisiä tyyppejä luvussa 10. Tämä allekirjoitus antaa meille vihjeet, joita tarvitsemme `+`-operaattorin hankalien osien ymmärtämiseksi.

Ensinnäkin `s2`:lla on `&`, mikä tarkoittaa, että lisäämme viitteen toisesta merkkijonosta ensimmäiseen merkkijonoon. Tämä johtuu `add`-funktion `s`-parametrista: Voimme lisätä vain merkkijonoviipaleen `String`:iin; emme voi lisätä kahta `String`-arvoa yhteen. Mutta odota—`&s2`:n tyyppi on `&String`, ei `&str`, kuten `add`:n toisessa parametrissa määritellään. Miksi listaus 8-18 sitten kääntyy?

Syy siihen, miksi voimme käyttää `&s2`:ta `add`-kutsussa, on se, että kääntäjä voi pakottaa `&String`-argumentin muotoon `&str`. Kun kutsumme `add`-metodia, Rust käyttää dereferointipakkoa, joka tässä muuttaa `&s2`:n muotoon `&s2[..]`. Käsittelemme dereferointipakkoa tarkemmin luvussa 15. Koska `add` ei ota `s`-parametrin omistusta, `s2` on edelleen kelvollinen `String` tämän operaation jälkeen.

Toiseksi allekirjoituksesta näemme, että `add` ottaa `self`:n omistuksen, koska `self`:llä _ei_ ole `&`:ia. Tämä tarkoittaa, että `s1` listauksessa 8-18 siirretään `add`-kutsuun eikä ole enää kelvollinen sen jälkeen. Joten vaikka `let s3 = s1 + &s2;` näyttää siltä, että se kopioisi molemmat merkkijonot ja loisi uuden, tämä lause itse asiassa ottaa `s1`:n omistuksen, liittää kopion `s2`:n sisällöstä ja palauttaa tuloksen omistuksen. Toisin sanoen se näyttää tekevän paljon kopioita, mutta ei tee; toteutus on tehokkaampi kuin kopiointi.

Jos meidän on yhdistettävä useita merkkijonoja, `+`-operaattorin käyttäytyminen muuttuu hankalaksi:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-01-concat-multiple-strings/src/main.rs:here}}
```

Tässä vaiheessa `s` on `tic-tac-toe`. Kaikkien `+`- ja `"`-merkkien kanssa on vaikea nähdä, mitä tapahtuu. Monimutkaisempien merkkijonoyhdistelmien tekemiseen voimme sen sijaan käyttää `format!`-makroa:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-02-format/src/main.rs:here}}
```

Tämä koodi asettaa myös `s`:n arvoksi `tic-tac-toe`. `format!`-makro toimii kuten `println!`, mutta tulostaa tulosteen näytölle sen sijaan, että se palauttaa `String`:in sisällöllä. `format!`-makroa käyttävä versio on paljon helpompi lukea, ja `format!`-makron generoima koodi käyttää viitteitä, joten tämä kutsu ei ota omistusta mistään parametreistään.

### Merkkijonoon indeksointi

Monissa muissa ohjelmointikielissä yksittäisten merkkien käyttäminen merkkijonosta viittaamalla niihin indeksillä on kelvollinen ja yleinen operaatio. Jos kuitenkin yrität käyttää `String`:in osia indeksointisyntaksilla Rustissa, saat virheen. Harkitse kelvotonta koodia listauksessa 8-19.

<Listing number="8-19" caption="Yritys käyttää indeksointisyntaksia `String`:in kanssa">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-19/src/main.rs:here}}
```

</Listing>

Tämä koodi tuottaa seuraavan virheen:

```console
{{#include ../listings/ch08-common-collections/listing-08-19/output.txt}}
```

Virhe kertoo tarinan: Rust-merkkijonot eivät tue indeksointia. Mutta miksi ei? Vastataksemme tähän kysymykseen meidän on käsiteltävä, miten Rust tallentaa merkkijonot muistiin.

#### Sisäinen esitys

`String` on kääre `Vec<u8>`:n ympärillä. Katsotaan joitakin oikein koodattuja UTF-8-esimerkkimerkkijonojamme listauksesta 8-14. Ensin tämä:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:spanish}}
```

Tässä tapauksessa `len` on `4`, mikä tarkoittaa, että merkkijonoa `"Hola"` tallentava vektori on 4 tavua pitkä. Jokainen näistä kirjaimista vie 1 tavun UTF-8-koodauksessa. Seuraava rivi saattaa kuitenkin yllättää (huomaa, että tämä merkkijono alkaa kyrillisen isolla kirjaimella _Ze_, ei numerolla 3):

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:russian}}
```

Jos sinulta kysyttäisiin, kuinka pitkä merkkijono on, saatat sanoa 12. Itse asiassa Rustin vastaus on 24: se on tavujen määrä, joita tarvitaan ”Здравствуйте”:n koodaamiseen UTF-8:ssa, koska jokainen Unicode-skaalaarvo kyseisessä merkkijonossa vie 2 tavua tallennustilaa. Siksi indeksi merkkijonon tavuissa ei aina vastaa kelvollista Unicode-skaalaarvoa. Havainnollistaaksemme, harkitse tätä kelvotonta Rust-koodia:

```rust,ignore,does_not_compile
let hello = "Здравствуйте";
let answer = &hello[0];
```

Tiedät jo, että `answer` ei ole `З`, ensimmäinen kirjain. Kun `З` on koodattu UTF-8:ssa, ensimmäinen tavu on `208` ja toinen on `151`, joten näyttäisi siltä, että `answer`:n pitäisi olla `208`, mutta `208` ei ole kelvollinen merkki yksinään. `208`:n palauttaminen ei todennäköisesti ole sitä, mitä käyttäjä haluaisi, jos he pyytäisivät tämän merkkijonon ensimmäistä kirjainta; kuitenkin se on ainoa data, joka Rustilla on tavuindeksissä 0. Käyttäjät eivät yleensä halua tavuarvoa palautettavaksi, vaikka merkkijono sisältäisi vain latinalaisia kirjaimia: Jos `&"hi"[0]` olisi kelvollista koodia, joka palauttaisi tavuarvon, se palauttaisi `104`:n, ei `h`:ta.

Vastaus on siis, että odottamattoman arvon palauttamisen ja virheiden estämiseksi, joita ei ehkä huomata heti, Rust ei käännä tätä koodia lainkaan ja estää väärinkäsitykset varhaisessa kehitysvaiheessa.

<!-- Old headings. Do not remove or links may break. -->

<a id="bytes-and-scalar-values-and-grapheme-clusters-oh-my"></a>

#### Tavut, skaalaarvot ja grafeemiklusterit

Toinen kohta UTF-8:sta on, että Rustin näkökulmasta merkkijonoihin on itse asiassa kolme relevanttia tapaa katsoa: tavuina, skaalaarvoina ja grafeemiklustereina (lähin vastine sille, mitä kutsumme _kirjaimiksi_).

Jos katsomme hindinkielistä sanaa ”नमस्ते”, joka on kirjoitettu devanagari-kirjaimistolla, se tallennetaan `u8`-arvojen vektorina, joka näyttää tältä:

```text
[224, 164, 168, 224, 164, 174, 224, 164, 184, 224, 165, 141, 224, 164, 164,
224, 165, 135]
```

Se on 18 tavua ja näin tietokoneet lopulta tallentavat tämän datan. Jos katsomme niitä Unicode-skaalaarvoina, jotka ovat Rustin `char`-tyyppi, nämä tavut näyttävät tältä:

```text
['न', 'म', 'स', '्', 'त', 'े']
```

Tässä on kuusi `char`-arvoa, mutta neljäs ja kuudes eivät ole kirjaimia: ne ovat diakriittisiä merkkejä, jotka eivät ole järkeviä yksinään. Lopuksi, jos katsomme niitä grafeemiklustereina, saisimme sen, mitä ihminen kutsuisi hindinkielisen sanan neljäksi kirjaimiksi:

```text
["न", "म", "स्", "ते"]
```

Rust tarjoaa erilaisia tapoja tulkita raakaa merkkijonodataa, jota tietokoneet tallentavat, jotta jokainen ohjelma voi valita tarvitsemansa tulkinnan riippumatta siitä, millä ihmiskielellä data on.

Viimeinen syy siihen, miksi Rust ei salli meidän indeksoida `String`:iin saadaksemme merkin, on se, että indeksointi-operaatioiden odotetaan aina vievän vakiintuneen ajan (O(1)). Mutta tätä suorituskykyä ei ole mahdollista taata `String`:in kanssa, koska Rustin pitäisi käydä läpi sisältö alusta indeksiin määrittääkseen, kuinka monta kelvollista merkkiä siellä on.

### Merkkijonoviipaleiden leikkaaminen

Merkkijonoon indeksointi on usein huono idea, koska ei ole selvää, mikä merkkijonon indeksointi-operaation palautustyypin pitäisi olla: tavu, merkki, grafeemiklusteri vai merkkijonoviipale. Jos todella tarvitset käyttää indeksejä merkkijonoviipaleiden luomiseen, Rust pyytää sinua olemaan tarkempi.

Sen sijaan, että indeksoisit `[]`:lla yhdellä numerolla, voit käyttää `[]`:a alueella luodaksesi merkkijonoviipaleen, joka sisältää tiettyjä tavuja:

```rust
let hello = "Здравствуйте";

let s = &hello[0..4];
```

Tässä `s` on `&str`, joka sisältää merkkijonon ensimmäiset 4 tavua. Aiemmin mainitsimme, että jokainen näistä merkeistä oli 2 tavua, mikä tarkoittaa, että `s` on `Зд`.

Jos yrittäisimme leikata vain osan merkin tavuista jollakin kuten `&hello[0..1]`, Rust panikoisi ajonaikana samalla tavalla kuin jos virheellistä indeksiä käytettäisiin vektorissa:

```console
{{#include ../listings/ch08-common-collections/output-only-01-not-char-boundary/output.txt}}
```

Sinun pitäisi olla varovainen luodessasi merkkijonoviipaleita alueilla, koska se voi kaataa ohjelmasi.

<!-- Old headings. Do not remove or links may break. -->

<a id="methods-for-iterating-over-strings"></a>

### Merkkijonojen läpikäynti

Paras tapa käsitellä merkkijonon osia on olla eksplisiittinen siitä, haluatko merkkejä vai tavuja. Yksittäisille Unicode-skaalaarvoille käytä `chars`-metodia. `chars`:in kutsuminen merkkijonolla ”Зд” erottelee ja palauttaa kaksi `char`-tyyppistä arvoa, ja voit käydä tuloksen läpi käyttääksesi jokaista elementtiä:

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

Vaihtoehtoisesti `bytes`-metodi palauttaa jokaisen raakatuvun, mikä saattaa olla sopivaa toimialallesi:

```rust
for b in "Зд".bytes() {
    println!("{b}");
}
```

Tämä koodi tulostaa 4 tavua, jotka muodostavat tämän merkkijonon:

```text
208
151
208
180
```

Muista kuitenkin, että kelvolliset Unicode-skaalaarvot voivat koostua useammasta kuin yhdestä tavusta.

Grafeemiklusterien saaminen merkkijonoista, kuten devanagari-kirjaimistolla, on monimutkaista, joten standardikirjasto ei tarjoa tätä toiminnallisuutta. Crate:t ovat saatavilla osoitteessa [crates.io](https://crates.io/)<!-- ignore -->, jos tarvitset tätä toiminnallisuutta.

<!-- Old headings. Do not remove or links may break. -->

<a id="strings-are-not-so-simple"></a>

### Merkkijonojen monimutkaisuuden käsittely

Yhteenvetona, merkkijonot ovat monimutkaisia. Eri ohjelmointikielet tekevät erilaisia valintoja siitä, miten esittää tämä monimutkaisuus ohjelmoijalle. Rust on valinnut tehdä `String`-datan oikeasta käsittelystä oletuskäyttäytymisen kaikille Rust-ohjelmille, mikä tarkoittaa, että ohjelmoijien on pohdittava UTF-8-datan käsittelyä etukäteen. Tämä kompromissi paljastaa enemmän merkkijonojen monimutkaisuutta kuin on ilmeistä muissa ohjelmointikielissä, mutta se estää sinua käsittelemästä ei-ASCII-merkkeihin liittyviä virheitä myöhemmin kehityssykliäsi.

Hyvä uutinen on, että standardikirjasto tarjoaa paljon toiminnallisuutta, joka on rakennettu `String`- ja `&str`-tyyppien päälle auttamaan käsittelemään näitä monimutkaisia tilanteita oikein. Muista tutustua dokumentaatioon hyödyllisistä metodeista, kuten `contains` merkkijonon etsimiseen ja `replace` merkkijonon osien korvaamiseen toisella merkkijonolla.

Siirrytään hieman vähemmän monimutkaiseen asiaan: hajautustaulukot!
