## Mikä on omistajuus?

_Omistajuus_ on joukko sääntöjä, jotka määräävät, miten Rust-ohjelma hallitsee muistia.
Kaikki ohjelmat joutuvat hallitsemaan muistinkäyttöään suorituksen aikana.
Joissakin kielissä on roskienkerääjä, joka säännöllisesti vapauttaa käyttämättömän muistin ohjelman suorittaessa;
toisissa kielissä ohjelmoijan on itse varattava ja vapautettava muisti manuaalisesti.
Rust käyttää kolmatta lähestymistapaa: muisti hallitaan omistajuusjärjestelmällä, jonka sääntöjä kääntäjä tarkistaa.
Jos sääntöjä rikotaan, ohjelma ei käänny.
Omistajuuden ominaisuudet eivät hidasta ohjelman suorittamista.

Koska omistajuus on monille ohjelmoijille uusi käsite, sen omaksuminen vie aikaa.
Hyvä uutinen on, että mitä enemmän harjoittelet Rustia ja sen omistajuussääntöjä,
sitä helpommaksi turvallisen ja tehokkaan koodin kirjoittaminen tulee.
Jatka harjoittelua!

Kun ymmärrät omistajuuden, sinulla on vahva pohja Rustin ainutlaatuisten ominaisuuksien ymmärtämiselle.
Tässä luvussa opit omistajuudesta käyttämällä esimerkkejä hyvin yleisestä tietorakenteesta:
merkkijonoista.

> ### Pino ja keko
>
> Monissa ohjelmointikielissä ei tarvitse ajatella pinon ja keon käyttöä kovin usein.
> Järjestelmäohjelmointikielessä kuten Rustissa sen sijaan sillä, onko arvo pinossa vai keossa,
> on vaikutusta kielen käyttäytymiseen ja siihen, miksi tiettyjä päätöksiä täytyy tehdä.
> Omistajuuden osia kuvataan myöhemmin tässä luvussa pinon ja keon suhteessa,
> joten tässä on lyhyt selitys valmistautumiseksi.
>
> Sekä pino että keko ovat osia muistista, joita koodisi voi käyttää suorituksen aikana,
> mutta ne on rakennettu eri tavoin. Pino tallentaa arvot siinä järjestyksessä, jossa ne saapuvat,
> ja poistaa arvot päinvastaisessa järjestyksessä. Tätä kutsutaan _viimeisenä sisään, ensimmäisenä ulos_ -periaatteeksi.
> Ajattele lautasten pinoa: kun lisäät lautasia, laitat ne pinon päälle, ja kun tarvitset lautasen,
> otat yhden pinon päältä. Lautasten lisääminen tai poistaminen pinon keskeltä tai pohjalta ei toimisi yhtä hyvin!
> Tietojen lisäämistä kutsutaan _työntämiseksi pinolle_, ja tietojen poistamista _poistamiseksi pinolta_.
> Kaikilla pinolla säilytetyillä tiedoilla täytyy olla tunnettu, kiinteä koko.
> Tiedot, joiden koko ei ole tiedossa käännösaikana tai joiden koko voi muuttua, täytyy sen sijaan tallentaa kekoon.
>
> Keko on vähemmän jäsennelty: kun laitat tietoa kekoon, pyydät tietyn määrän tilaa.
> Muistin allokoija etsii keosta riittävän tyhjän kohdan, merkitsee sen käytössä olevaksi
> ja palauttaa _osoittimen_, joka on kyseisen sijainnin osoite. Tätä prosessia kutsutaan
> _allokoinniksi keossa_, ja sitä lyhennetään joskus pelkäksi _allokoinniksi_
> (arvojen työntäminen pinolle ei katsota allokoinniksi).
> Koska osoitin kekoon on tunnetun, kiinteän kokoinen, voit tallentaa osoittimen pinolle,
> mutta kun tarvitset varsinaiset tiedot, sinun täytyy seurata osoitinta.
> Ajattele ravintolaa: kun saavut, kerrot ryhmäsi koon, ja isäntä etsii tyhjän pöydän,
> johon kaikki mahtuvat, ja ohjaa teidät sinne. Jos joku ryhmästäsi saapuu myöhässä,
> hän voi kysyä, mihin olette istuneet, löytääkseen teidät.
>
> Pinolle työntäminen on nopeampaa kuin allokointi keossa, koska allokoijan ei tarvitse
> etsiä paikkaa uusille tiedoille; paikka on aina pinon huipulla.
> Verrattuna siihen allokointi keossa vaatii enemmän työtä, koska allokoijan täytyy ensin
> löytää riittävän suuri tila tiedoille ja sitten tehdä kirjanpitoa seuraavaa allokointia varten.
>
> Kekoon tallennettujen tietojen käyttö on hitaampaa kuin pinolla olevien tietojen käyttö,
> koska sinun täytyy seurata osoitinta päästäksesi perille. Nykyaikaiset prosessorit ovat nopeampia,
> jos ne eivät hyppivät muistissa niin paljon. Jatkamalla vertauskuvaa: ajattele tarjoilijaa,
> joka ottaa tilauksia useilta pöydiltä. Tehokkainta on ottaa kaikki tilaukset yhdeltä pöydältä
> ennen siirtymistä seuraavaan. Tilauksen ottaminen pöydältä A, sitten pöydältä B, sitten taas A:sta
> ja taas B:stä olisi paljon hitaampi prosessi. Samoin prosessori tekee työnsä paremmin,
> jos se käsittelee tietoja, jotka ovat lähellä toisiaan (kuten pinolla) eivätkä kauempana (kuten keossa voi olla).
>
> Kun koodisi kutsuu funktiota, funktiolle välitetyt arvot (mukaan lukien mahdollisesti osoittimet
> keon tietoihin) ja funktion paikalliset muuttujat työnnetään pinolle.
> Kun funktio päättyy, nämä arvot poistetaan pinolta.
>
> Seuranta siitä, mitkä koodin osat käyttävät mitäkin keon tietoja, keon päällekkäisten tietojen
> määrän minimointi ja käyttämättömien keon tietojen siivoaminen, jotta tila ei lopu,
> ovat kaikki ongelmia, joita omistajuus ratkaisee. Kun ymmärrät omistajuuden, sinun ei tarvitse
> ajatella pinon ja keon käyttöä kovin usein, mutta tieto siitä, että omistajuuden pääasiallinen
> tarkoitus on hallita keon tietoja, auttaa ymmärtämään, miksi se toimii niin kuin se toimii.

### Omistajuussäännöt

Ensinnäkin tarkastellaan omistajuuden sääntöjä. Muista nämä säännöt, kun käsittelemme niitä havainnollistavia esimerkkejä:

- Jokaisella arvolla Rustissa on _omistaja_.
- Vain yksi omistaja voi olla kerrallaan.
- Kun omistaja poistuu näkyvyysalueelta, arvo poistetaan.

### Muuttujan näkyvyysalue

Nyt kun olemme käyneet läpi Rustin perussyntaksia, emme sisällytä kaikkiin esimerkkeihin `fn main() {` -koodia,
joten jos seuraat mukana, varmista, että sijoitat seuraavat esimerkit `main`-funktion sisään manuaalisesti.
Näin esimerkkimme ovat hieman tiiviimpiä, jotta voimme keskittyä varsinaisiin yksityiskohtiin
eikä pohjakoodiin.

Ensimmäisenä omistajuusesimerkkinä tarkastelemme joidenkin muuttujien _näkyvyysaluetta_.
Näkyvyysalue on ohjelman osa, jossa kohde on voimassa. Tarkastele seuraavaa muuttujaa:

```rust
let s = "hello";
```

Muuttuja `s` viittaa merkkijonoliteraaliin, jossa merkkijonon arvo on kovakoodattu ohjelman tekstiin.
Muuttuja on voimassa siitä hetkestä, jolloin se on määritelty, nykyisen _näkyvyysalueen_ loppuun asti.
Listaus 4-1 näyttää ohjelman, jossa kommenteissa on merkitty, missä muuttuja `s` olisi voimassa.

<Listing number="4-1" caption="Muuttuja ja näkyvyysalue, jolla se on voimassa">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-01/src/main.rs:here}}
```

</Listing>

Toisin sanoen tässä on kaksi tärkeää ajankohtaa:

- Kun `s` _tulee_ näkyvyysalueelle, se on voimassa.
- Se pysyy voimassa, kunnes se _poistuu_ näkyvyysalueelta.

Tässä vaiheessa näkyvyysalueen ja muuttujien voimassaolon välinen suhde on samanlainen kuin muissa ohjelmointikielissä.
Rakennamme tämän ymmärryksen päälle esittelemällä `String`-tyypin.

### `String`-tyyppi

Omistajuussääntöjen havainnollistamiseksi tarvitsemme monimutkaisemman tietotyypin kuin ne,
jotka käsittelimme Luvun 3 [”Tietotyypit”][data-types]<!-- ignore --> -osiossa.
Aiemmin käsitellyt tyypit ovat tunnetun kokoisia, ne voidaan tallentaa pinolle ja poistaa pinolta,
kun niiden näkyvyysalue päättyy, ja ne voidaan nopeasti ja helposti kopioida uudeksi, riippumattomaksi
instanssiksi, jos koodin toinen osa tarvitsee saman arvon eri näkyvyysalueella.
Haluamme kuitenkin tarkastella kekoon tallennettuja tietoja ja tutkia, miten Rust tietää,
milloin siivota nämä tiedot, ja `String`-tyyppi on erinomainen esimerkki.

Keskitymme `String`-tyypin osiin, jotka liittyvät omistajuuteen. Nämä näkökohdat pätevät myös
muihin monimutkaisiin tietotyyppeihin, olivatpa ne standardikirjaston tarjoamia tai itse luomiasi.
Käsittelemme `String`-tyyppiä tarkemmin [Luvussa 8][ch8]<!-- ignore -->.

Olemme jo nähneet merkkijonoliteraaleja, joissa merkkijonoarvo on kovakoodattu ohjelmaamme.
Merkkijonoliteraalit ovat käteviä, mutta ne eivät sovi kaikkiin tilanteisiin, joissa haluamme käyttää tekstiä.
Yksi syy on, että ne ovat muuttumattomia. Toinen on, että kaikkia merkkijonoarvoja ei voida tietää,
kun kirjoitamme koodiamme: esimerkiksi jos haluamme ottaa käyttäjän syötteen ja tallentaa sen?
Näihin tilanteisiin Rustissa on toinen merkkijonotyyppi, `String`. Tämä tyyppi hallitsee kekoon allokoituja tietoja
ja voi siksi tallentaa tekstimäärän, joka ei ole tiedossa käännösaikana. Voit luoda `String`-tyypin
merkkijonoliteraalista `from`-funktiolla näin:

```rust
let s = String::from("hello");
```

Kaksoispiste `::` -operaattori antaa meidän nimetä tämän tietyn `from`-funktion `String`-tyypin alle
sen sijaan, että käyttäisimme jotain nimeä kuten `string_from`. Käsittelemme tätä syntaksia tarkemmin
Luvun 5 [”Metodit”][methods]<!-- ignore --> -osiossa ja kun puhumme nimiavaruuksista moduuleilla
Luvun 7 [”Polut viittaamiseen moduulipuun kohteeseen”][paths-module-tree]<!-- ignore --> -osiossa.

Tämänkaltainen merkkijono _voidaan_ muuttaa:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-01-can-mutate-string/src/main.rs:here}}
```

Eli mikä ero täällä on? Miksi `String` voidaan muuttaa mutta literaaleja ei?
Ero on siinä, miten nämä kaksi tyyppiä käsittelevät muistia.

### Muisti ja allokointi

Merkkijonoliteraalin tapauksessa tiedämme sisällön käännösaikana, joten teksti kovakoodataan suoraan
lopulliseen suoritettavaan tiedostoon. Siksi merkkijonoliteraalit ovat nopeita ja tehokkaita.
Nämä ominaisuudet johtuvat kuitenkin merkkijonoliteraalin muuttumattomuudesta.
Valitettavasti emme voi laittaa muistipätkää binääritiedostoon jokaiselle tekstiosalle,
jonka koko ei ole tiedossa käännösaikana ja jonka koko voi muuttua ohjelman suorituksen aikana.

`String`-tyypin tapauksessa muuttuvan, kasvavan tekstin tukemiseksi meidän täytyy allokoida kekoon
tietty määrä muistia, joka ei ole tiedossa käännösaikana, sisällön säilyttämiseksi. Tämä tarkoittaa:

- Muisti täytyy pyytää muistin allokoijalta suorituksen aikana.
- Tarvitsemme tavan palauttaa tämä muisti allokoijalle, kun olemme valmiita `String`-tyypin kanssa.

Ensimmäisen osan teemme itse: kun kutsumme `String::from`, sen toteutus pyytää tarvitsemansa muistin.
Tämä on melkein yleispätevää kaikissa ohjelmointikielissä.

Toinen osa on kuitenkin erilainen. Kielissä, joissa on _roskienkerääjä (GC)_,
GC seuraa ja siivoaa muistin, jota ei enää käytetä, emmekä meidän tarvitse ajatella sitä.
Useimmissa kielissä ilman GC:tä vastuullamme on tunnistaa, milloin muistia ei enää käytetä,
ja kutsua koodia vapauttamaan se eksplisiittisesti, aivan kuten teimme pyytäessämme sitä.
Tämän tekeminen oikein on historiallisesti ollut vaikea ohjelmointiongelma.
Jos unohdamme, tuhlaamme muistia. Jos teemme sen liian aikaisin, meillä on virheellinen muuttuja.
Jos teemme sen kahdesti, sekin on bugi. Meidän täytyy yhdistää täsmälleen yksi `allocate` täsmälleen yhteen `free`-kutsuun.

Rust valitsee eri polun: muisti palautetaan automaattisesti, kun muuttujan, joka omistaa sen, näkyvyysalue päättyy.
Tässä on versio näkyvyysalueesimerkistämme Listauksesta 4-1 käyttäen `String`-tyyppiä merkkijonoliteraalin sijaan:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-02-string-scope/src/main.rs:here}}
```

On luonnollinen kohta, jossa voimme palauttaa `String`-tyypin tarvitseman muistin allokoijalle:
kun `s` poistuu näkyvyysalueelta. Kun muuttuja poistuu näkyvyysalueelta, Rust kutsuu erityistä funktiota puolestamme.
Tätä funktiota kutsutaan [`drop`][drop]<!-- ignore --> -funktioksi, ja siihen `String`-tyypin tekijä voi sijoittaa
koodin muistin palauttamiseksi. Rust kutsuu `drop`-funktiota automaattisesti sulkevassa aaltosulussa.

> Huom: C++:ssa tätä resurssien vapauttamisen mallia kohteen elinkaaren lopussa kutsutaan joskus
> _Resource Acquisition Is Initialization (RAII)_ -malliksi. Rustin `drop`-funktio on tuttu sinulle,
> jos olet käyttänyt RAII-malleja.

Tällä mallilla on syvällinen vaikutus siihen, miten Rust-koodia kirjoitetaan.
Se saattaa vaikuttaa yksinkertaiselta nyt, mutta koodin käyttäytyminen voi olla odottamatonta
monimutkaisemmissa tilanteissa, kun haluamme useiden muuttujien käyttävän kekoon allokoimiamme tietoja.
Tutkitaan joitakin näistä tilanteista nyt.

<!-- Old heading. Do not remove or links may break. -->

<a id="ways-variables-and-data-interact-move"></a>

#### Muuttujien ja tietojen vuorovaikutus siirron (move) kautta

Useat muuttujat voivat vuorovaikuttaa samojen tietojen kanssa eri tavoin Rustissa.
Tarkastellaan esimerkkiä kokonaisluvulla Listauksessa 4-2.

<Listing number="4-2" caption="Kokonaisluvun arvon `x` sitominen muuttujaan `y`">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-02/src/main.rs:here}}
```

</Listing>

Voimme todennäköisesti arvata, mitä tämä tekee: ”sido arvo `5` muuttujaan `x`; tee sitten kopio arvosta `x`:ssä ja sido se muuttujaan `y`.”
Meillä on nyt kaksi muuttujaa, `x` ja `y`, ja molemmat ovat `5`. Näin todellakin tapahtuu, koska kokonaisluvut
ovat yksinkertaisia arvoja tunnetulla, kiinteällä koolla, ja nämä kaksi `5`-arvoa työnnetään pinolle.

Tarkastellaan nyt `String`-versiota:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-03-string-move/src/main.rs:here}}
```

Tämä näyttää hyvin samankaltaiselta, joten voisimme olettaa, että se toimisi samalla tavalla:
toinen rivi tekisi kopion arvosta `s1`:ssä ja sitoisi sen `s2`:een. Mutta näin ei aivan tapahdu.

Katso Kuvaa 4-1 nähdäksesi, mitä `String`-tyypille tapahtuu konepellin alla. `String` koostuu kolmesta osasta,
jotka näkyvät vasemmalla: osoitin muistiin, joka sisältää merkkijonon sisällön, pituus ja kapasiteetti.
Tämä tietoryhmä tallennetaan pinolle. Oikealla on keon muisti, joka sisältää sisällön.

<img alt="Two tables: the first table contains the representation of s1 on the
stack, consisting of its length (5), capacity (5), and a pointer to the first
value in the second table. The second table contains the representation of the
string data on the heap, byte by byte." src="img/trpl04-01.svg" class="center"
style="width: 50%;" />

<span class="caption">Kuva 4-1: `String`-tyypin esitys muistissa, kun se sisältää arvon `"hello"` ja on sidottu `s1`:een</span>

Pituus on se, kuinka paljon muistia tavussa `String`-tyypin sisältö tällä hetkellä käyttää.
Kapasiteetti on kokonaismäärä muistia tavuina, jonka `String` on saanut allokoijalta.
Ero pituuden ja kapasiteetin välillä on merkityksellinen, mutta ei tässä kontekstissa,
joten toistaiseksi kapasiteetin voi jättää huomiotta.

Kun sidomme `s1`:n `s2`:een, `String`-tyypin tiedot kopioidaan, eli kopioimme pinolla olevan osoittimen,
pituuden ja kapasiteetin. Emme kopioi keon tietoja, joihin osoitin viittaa. Toisin sanoen
tietojen esitys muistissa näyttää Kuvalta 4-2.

<img alt="Three tables: tables s1 and s2 representing those strings on the
stack, respectively, and both pointing to the same string data on the heap."
src="img/trpl04-02.svg" class="center" style="width: 50%;" />

<span class="caption">Kuva 4-2: Muuttujan `s2` esitys muistissa, jolla on kopio `s1`:n osoittimesta, pituudesta ja kapasiteetista</span>

Esitys _ei_ näytä Kuvalta 4-3, miltä muisti näyttäisi, jos Rust kopioisi myös keon tiedot.
Jos Rust tekisi näin, operaatio `s2 = s1` voisi olla erittäin kallis suorituskyvyn kannalta,
jos keon tiedot olisivat suuria.

<img alt="Four tables: two tables representing the stack data for s1 and s2,
and each points to its own copy of string data on the heap."
src="img/trpl04-03.svg" class="center" style="width: 50%;" />

<span class="caption">Kuva 4-3: Toinen mahdollisuus sille, mitä `s2 = s1` voisi tehdä, jos Rust kopioisi myös keon tiedot</span>

Aiemmin sanoin, että kun muuttuja poistuu näkyvyysalueelta, Rust kutsuu automaattisesti `drop`-funktion
ja siivoaa kyseisen muuttujan keon muistin. Kuva 4-2 kuitenkin näyttää molempien tietojen osoittimien
osoittavan samaan sijaintiin. Tämä on ongelma: kun `s2` ja `s1` poistuvat näkyvyysalueelta,
ne yrittävät molemmat vapauttaa saman muistin. Tätä kutsutaan _kaksoisvapautus_-virheeksi,
ja se on yksi aiemmin mainituista muistiturvallisuusbugeista. Muistin vapauttaminen kahdesti
voi johtaa muistin korruptoitumiseen, mikä voi puolestaan johtaa tietoturva-aukkoja.

Muistiturvallisuuden varmistamiseksi rivin `let s2 = s1;` jälkeen Rust pitää `s1`:tä
enää voimassa olemattomana. Siksi Rustin ei tarvitse vapauttaa mitään, kun `s1` poistuu näkyvyysalueelta.
Katso, mitä tapahtuu, kun yrität käyttää `s1`:tä `s2`:n luomisen jälkeen; se ei toimi:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-04-cant-use-after-move/src/main.rs:here}}
```

Saat virheen, joka on tämänkaltainen, koska Rust estää sinua käyttämästä mitätöityä viitettä:

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-04-cant-use-after-move/output.txt}}
```

Jos olet kuullut termit _pinnallinen kopiointi_ ja _syvä kopiointi_ työskennellessäsi muiden kielten kanssa,
käsite osoittimen, pituuden ja kapasiteetin kopioimisesta kopioimatta tietoja kuulostaa todennäköisesti
pinnalliselta kopioinnilta. Koska Rust myös mitätöi ensimmäisen muuttujan, sitä ei kutsuta pinnalliseksi
kopioinniksi vaan _siirroksi_ (move). Tässä esimerkissä sanoisimme, että `s1` _siirrettiin_ `s2`:een.
Eli mitä todella tapahtuu, näkyy Kuvassa 4-4.

<img alt="Three tables: tables s1 and s2 representing those strings on the
stack, respectively, and both pointing to the same string data on the heap.
Table s1 is grayed out be-cause s1 is no longer valid; only s2 can be used to
access the heap data." src="img/trpl04-04.svg" class="center" style="width:
50%;" />

<span class="caption">Kuva 4-4: Esitys muistissa sen jälkeen, kun `s1` on mitätöity</span>

Tämä ratkaisee ongelmamme! Kun vain `s2` on voimassa, se yksin vapauttaa muistin poistuessaan näkyvyysalueelta, ja olemme valmiita.

Lisäksi tässä on implisiittinen suunnittelupäätös: Rust ei koskaan luo automaattisesti tietojesi ”syviä” kopioita.
Siksi voidaan olettaa, että mikä tahansa _automaattinen_ kopiointi on suorituskyvyn kannalta edullista.

#### Näkyvyysalue ja sijoitus

Tämän käänteinen on totta myös näkyvyysalueen, omistajuuden ja `drop`-funktion kautta vapautetun muistin suhteen.
Kun sijoitat täysin uuden arvon olemassa olevaan muuttujaan, Rust kutsuu `drop`-funktion ja vapauttaa alkuperäisen arvon muistin välittömästi.
Tarkastele esimerkiksi tätä koodia:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-04b-replacement-drop/src/main.rs:here}}
```

Määrittelemme aluksi muuttujan `s` ja sidomme sen `String`-tyyppiin arvolla `"hello"`.
Sitten luomme heti uuden `String`-tyypin arvolla `"ahoy"` ja sijoitamme sen `s`:ään.
Tässä vaiheessa mikään ei enää viittaa alkuperäiseen keon arvoon.

<img alt="One table s representing the string value on the stack, pointing to
the second piece of string data (ahoy) on the heap, with the original string
data (hello) grayed out because it cannot be accessed anymore."
src="img/trpl04-05.svg"
class="center"
style="width: 50%;"
/>

<span class="caption">Kuva 4-5: Esitys muistissa sen jälkeen, kun alkuperäinen arvo on korvattu kokonaan.</span>

Alkuperäinen merkkijono poistuu siis välittömästi näkyvyysalueelta. Rust suorittaa `drop`-funktion sille,
ja sen muisti vapautetaan heti. Kun tulostamme arvon lopussa, se on `"ahoy, world!"`.

<!-- Old heading. Do not remove or links may break. -->

<a id="ways-variables-and-data-interact-clone"></a>

#### Muuttujien ja tietojen vuorovaikutus kloonauksen (clone) kautta

Jos _haluamme_ kopioida `String`-tyypin keon tiedot syvästi, eikä vain pinon tietoja,
voimme käyttää yleistä `clone`-metodia. Käsittelemme metodisyntaksia Luvussa 5,
mutta koska metodit ovat yleisiä monissa ohjelmointikielissä, olet todennäköisesti nähnyt ne aiemmin.

Tässä on esimerkki `clone`-metodista käytössä:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-05-clone/src/main.rs:here}}
```

Tämä toimii hyvin ja tuottaa eksplisiittisesti Kuvassa 4-3 näytetyn käyttäytymisen, jossa keon tiedot _todella_ kopioidaan.

Kun näet `clone`-kutsun, tiedät, että jotain mielivaltaista koodia suoritetaan ja se koodi voi olla kallista.
Se on visuaalinen merkki siitä, että jotain erilaista on meneillään.

#### Vain pinolla olevat tiedot: Copy

Meillä on vielä yksi mutka, josta emme ole puhuneet. Tämä koodi kokonaisluvuilla — osa näytettiin Listauksessa 4-2 — toimii ja on kelvollinen:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-06-copy/src/main.rs:here}}
```

Mutta tämä koodi näyttää ristiriitaiselta sen suhteen, mitä juuri opimme: meillä ei ole `clone`-kutsua,
mutta `x` on silti voimassa eikä sitä siirretty `y`:hyn.

Syy on, että tyypit kuten kokonaisluvut, joiden koko on tiedossa käännösaikana, tallennetaan kokonaan pinolle,
joten varsinaisten arvojen kopiot ovat nopeita tehdä. Tämä tarkoittaa, ettei ole syytä estää `x`:ää
olemassa muuttujan `y` luomisen jälkeen. Toisin sanoen syvän ja pinnallisen kopioinnin välillä ei ole eroa tässä,
joten `clone`-kutsu ei tekisi mitään erilaista tavalliseen pinnalliseen kopiointiin verrattuna, ja voimme jättää sen pois.

Rustissa on erityinen annotaatio nimeltä `Copy`-trait, jonka voimme sijoittaa pinolla tallennettuihin tyyppeihin,
kuten kokonaisluvut (puhumme traiteista tarkemmin [Luvussa 10][traits]<!-- ignore -->).
Jos tyyppi toteuttaa `Copy`-traitin, sitä käyttävät muuttujat eivät siirry vaan kopioidaan triviaalisti,
joten ne ovat edelleen voimassa toiseen muuttujaan sijoittamisen jälkeen.

Rust ei anna meidän annotoida tyyppiä `Copy`:lla, jos tyyppi tai jokin sen osista on toteuttanut `Drop`-traitin.
Jos tyypille täytyy tapahtua jotain erityistä, kun arvo poistuu näkyvyysalueelta, ja lisäämme `Copy`-annotaation kyseiseen tyyppiin,
saamme käännösaikaisen virheen. Opit lisäämään `Copy`-annotaation omaan tyyppiisi traitin toteuttamiseksi
liitteessä C kohdassa [”Johdettavat traitit”][derivable-traits]<!-- ignore -->.

Mitä tyypit toteuttavat `Copy`-traitin? Voit tarkistaa tietyn tyypin dokumentaatiosta varmuuden vuoksi,
mutta yleissääntönä mikä tahansa yksinkertaisten skalaariarvojen ryhmä voi toteuttaa `Copy`:n,
eikä mikään, mikä vaatii allokointia tai on jonkinlainen resurssi, voi toteuttaa `Copy`:tä.
Tässä on joitakin `Copy`:n toteuttavia tyyppejä:

- Kaikki kokonaislukutyypit, kuten `u32`.
- Totuusarvotyyppi `bool` arvoilla `true` ja `false`.
- Kaikki liukulukutyypit, kuten `f64`.
- Merkkityyppi `char`.
- Tuplet, jos ne sisältävät vain tyyppejä, jotka myös toteuttavat `Copy`:n. Esimerkiksi
  `(i32, i32)` toteuttaa `Copy`:n, mutta `(i32, String)` ei.

### Omistajuus ja funktiot

Arvon välittämisen mekaniikka funktiolle on samanlainen kuin arvon sijoittaminen muuttujaan.
Muuttujan välittäminen funktiolle siirtää tai kopioi sen, aivan kuten sijoitus. Listaus 4-3 sisältää esimerkin,
jossa on annotaatioita siitä, missä muuttujat tulevat näkyvyysalueelle ja poistuvat sieltä.

<Listing number="4-3" file-name="src/main.rs" caption="Funktiot omistajuus- ja näkyvyysaluekommentein">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-03/src/main.rs}}
```

</Listing>

Jos yrittäisimme käyttää `s`:tä `takes_ownership`-kutsun jälkeen, Rust antaisi käännösaikaisen virheen.
Nämä staattiset tarkistukset suojaavat meitä virheiltä. Kokeile lisätä `main`-funktioon koodia, joka käyttää `s`:tä ja `x`:ää,
nähdäksesi missä voit käyttää niitä ja missä omistajuussäännöt estävät sen.

### Paluuarvot ja näkyvyysalue

Paluuarvot voivat myös siirtää omistajuutta. Listaus 4-4 näyttää esimerkin funktiosta, joka palauttaa arvon,
samankaltaisilla annotaatioilla kuin Listauksessa 4-3.

<Listing number="4-4" file-name="src/main.rs" caption="Paluuarvojen omistajuuden siirtäminen">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-04/src/main.rs}}
```

</Listing>

Muuttujan omistajuus noudattaa samaa kaavaa joka kerta: arvon sijoittaminen toiseen muuttujaan siirtää sen.
Kun muuttuja, joka sisältää keon tietoja, poistuu näkyvyysalueelta, `drop` siivoaa arvon,
ellei tietojen omistajuutta ole siirretty toiseen muuttujaan.

Vaikka tämä toimii, omistajuuden ottaminen ja palauttaminen jokaisella funktiolla on hieman työlästä.
Entä jos haluamme antaa funktion käyttää arvoa ottamatta omistajuutta? On ärsyttävää, että kaiken mitä välitämme sisään
täytyy myös välittää takaisin, jos haluamme käyttää sitä uudelleen, lisäksi mihin tahansa funktion rungosta tulevaan dataan,
jonka haluamme ehkä palauttaa.

Rust antaa meidän palauttaa useita arvoja tuplen avulla, kuten Listauksessa 4-5 näytetään.

<Listing number="4-5" file-name="src/main.rs" caption="Parametrien omistajuuden palauttaminen">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-05/src/main.rs}}
```

</Listing>

Mutta tämä on liikaa seremoniaa ja työtä käsitteelle, jonka pitäisi olla yleinen.
Onneksi Rustissa on ominaisuus arvon käyttämiseen siirtämättä omistajuutta, nimeltä _viitteet_.

[data-types]: ch03-02-data-types.html#data-types
[ch8]: ch08-02-strings.html
[traits]: ch10-02-traits.html
[derivable-traits]: appendix-03-derivable-traits.html
[methods]: ch05-03-method-syntax.html#methods
[paths-module-tree]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html
[drop]: ../std/ops/trait.Drop.html#tymethod.drop
