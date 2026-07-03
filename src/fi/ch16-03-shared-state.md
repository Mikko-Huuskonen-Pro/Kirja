## Jaetun tilan rinnakkaisuus

Viestinvälitys on hyvä tapa hallita rinnakkaisuutta, mutta se ei ole ainoa tapa. Toinen menetelmä on, että useat säikeet pääsevät käsiksi samaan jaettuun dataan. Tarkastellaan Go-ohjelmointikielen dokumentaation iskulauseen osaa uudelleen: ”Älä kommunikoi jakamalla muistia.”

Miltä muistia jakamalla kommunikointi näyttäisi? Lisäksi, miksi viestinvälityksen kannattajat varoittavat muistinjaon käytöstä?

Eräänläisesti kanavat missä tahansa ohjelmointikielessä muistuttavat yksinomistajuutta, koska kun siirrät arvon kanavaa pitkin, sinun ei pitäisi enää käyttää sitä arvoa. Jaetun muistin rinnakkaisuus on kuin moniomistajuus: useat säikeet voivat käyttää samaa muistipaikkaa samanaikaisesti. Kuten näit luvussa 15, älykkäät osoittimet mahdollistivat moniomistajuuden, ja moniomistajuus voi lisätä monimutkaisuutta, koska näitä eri omistajia täytyy hallita. Rustin tyyppijärjestelmä ja omistajuussäännöt auttavat merkittävästi tämän hallinnan oikeaksi saamisessa. Esimerkkinä tarkastellaan mutekseja, yhtä yleisimmistä jaetun muistin rinnakkaisuuden primitiiveistä.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-mutexes-to-allow-access-to-data-from-one-thread-at-a-time"></a>

### Pääsyn hallinta mutekseilla

_Mutex_ on lyhenne sanasta _mutual exclusion_ (keskinäinen poissulkeminen), sillä muteksi sallii vain yhden säikeen käyttää tiettyä dataa milloin tahansa. Päästäkseen käsiksi muteksin suojaamaan dataan säikeen täytyy ensin ilmoittaa haluavansa pääsyn pyytämällä muteksin lukitusta. _Lukitus_ on muteksiin kuuluva tietorakenne, joka pitää kirjaa siitä, kuka tällä hetkellä omistaa yksinoikeudellisen pääsyn dataan. Tästä syystä muteksia kuvataan _suojaavan_ hallussaan olevaa dataa lukitusjärjestelmän avulla.

Mutekseilla on maine vaikeasti käytettävinä, koska sinun täytyy muistaa kaksi sääntöä:

1. Sinun täytyy yrittää hankkia lukitus ennen datan käyttöä.
2. Kun olet valmis muteksin suojaaman datan kanssa, sinun täytyy vapauttaa lukitus, jotta muut säikeet voivat hankkia lukituksen.

Todellisen maailman vertauskuva mutekseille on paneelikeskustelu konferenssissa, jossa on vain yksi mikrofoni. Ennen kuin paneelisti voi puhua, hänen täytyy pyytää tai ilmoittaa haluavansa käyttää mikrofonia. Kun hän saa mikrofonin, hän voi puhua niin kauan kuin haluaa ja antaa sitten mikrofonin seuraavalle paneelistille, joka pyytää puheenvuoroa. Jos paneelisti unohtaa luovuttaa mikrofonin, kun hän on valmis, kukaan muu ei voi puhua. Jos jaetun mikrofonin hallinta menee pieleen, paneeli ei toimi suunnitellusti!

Muteksien hallinta voi olla uskomattoman hankalaa saada oikein, minkä vuoksi niin monet ovat innostuneita kanavista. Rustin tyyppijärjestelmän ja omistajuussääntöjen ansiosta et kuitenkaan voi tehdä virheitä lukituksessa ja lukituksen vapauttamisessa.

#### `Mutex<T>`-tyypin API

Esimerkkinä muteksin käytöstä aloitetaan muteksin käyttäminen yksisäikeisessä kontekstissa, kuten listauksessa 16-12 näytetään.

<Listing number="16-12" file-name="src/main.rs" caption="`Mutex<T>`-tyypin API:n tutkiminen yksisäikeisessä kontekstissa yksinkertaisuuden vuoksi">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-12/src/main.rs}}
```

</Listing>

Kuten monien tyyppien kohdalla, luomme `Mutex<T>`-tyypin liitetyllä funktiolla `new`. Päästäksemme käsiksi muteksin sisällä olevaan dataan käytämme `lock`-metodia lukituksen hankkimiseksi. Tämä kutsu estää nykyisen säikeen, jotta se ei voi tehdä työtä ennen kuin on meidän vuoromme saada lukitus.

`lock`-kutsu epäonnistuisi, jos toinen säie, joka pitää lukitusta, panikoisi. Tällöin kukaan ei voisi koskaan saada lukitusta, joten olemme valinneet `unwrap`-metodin ja annamme tämän säikeen panikoida, jos olemme tällaisessa tilanteessa.

Kun olemme hankkineet lukituksen, voimme käsitellä paluuarvoa, jota tässä tapauksessa kutsutaan `num`-muuttujaksi, muuttuvana viitteenä muteksin sisällä olevaan dataan. Tyyppijärjestelmä varmistaa, että hankimme lukituksen ennen arvon käyttöä `m`:ssä. `m`:n tyyppi on `Mutex<i32>`, ei `i32`, joten meidän _täytyy_ kutsua `lock`-metodia voidaksemme käyttää `i32`-arvoa. Emme voi unohtaa; tyyppijärjestelmä ei anna meidän käyttää sisäistä `i32`-arvoa muuten.

`lock`-kutsu palauttaa tyypin nimeltä `MutexGuard`, joka on kääritty `LockResult`-tyyppiin ja jonka käsittelimme `unwrap`-kutsulla. `MutexGuard`-tyyppi toteuttaa `Deref`-traitin osoittaakseen sisäiseen dataamme; tyypillä on myös `Drop`-toteutus, joka vapauttaa lukituksen automaattisesti, kun `MutexGuard` poistuu laajuudesta, mikä tapahtuu sisemmän laajuuden lopussa. Näin emme vaaranna unohtaa lukituksen vapauttamista ja estää muteksin käyttöä muilla säikeillä, koska lukituksen vapauttaminen tapahtuu automaattisesti.

Lukituksen pudottamisen jälkeen voimme tulostaa muteksin arvon ja nähdä, että pystyimme muuttamaan sisäisen `i32`-arvon arvoksi `6`.

<!-- Old headings. Do not remove or links may break. -->

<a id="sharing-a-mutext-between-multiple-threads"></a>

#### Jaettu pääsy `Mutex<T>`-tyyppiin

Kokeillaan nyt jakaa arvo useiden säikeiden välillä `Mutex<T>`-tyypin avulla. Luomme 10 säiettä ja annamme niiden jokaisen kasvattaa laskurin arvoa yhdellä, jotta laskuri menee arvosta 0 arvoon 10. Listauksen 16-13 esimerkissä on kääntäjävirhe, ja käytämme sitä virhettä oppiaksemme lisää `Mutex<T>`-tyypin käytöstä ja siitä, miten Rust auttaa käyttämään sitä oikein.

<Listing number="16-13" file-name="src/main.rs" caption="Kymmenen säiettä, joista jokainen kasvattaa `Mutex<T>`-tyypin suojaamaa laskuria">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-13/src/main.rs}}
```

</Listing>

Luomme `counter`-muuttujan, joka sisältää `i32`-arvon `Mutex<T>`-tyypin sisällä, kuten teimme listauksessa 16-12. Seuraavaksi luomme 10 säiettä iteroiden lukuarvojen alueen yli. Käytämme `thread::spawn`-funktiota ja annamme kaikille säikeille saman sulkeisen: sellaisen, joka siirtää laskurin säikeeseen, hankkii lukituksen `Mutex<T>`-tyyppiin kutsumalla `lock`-metodia ja lisää sitten 1 muteksin arvoon. Kun säie on suorittanut sulkeisensa loppuun, `num` poistuu laajuudesta ja vapauttaa lukituksen, jotta toinen säie voi hankkia sen.

Pääsäikeessä keräämme kaikki liittymiskahvat. Sitten, kuten teimme listauksessa 16-2, kutsumme `join`-metodia jokaisella kahvalla varmistaaksemme, että kaikki säikeet päättyvät. Tässä vaiheessa pääsäie hankkii lukituksen ja tulostaa ohjelman tuloksen.

Vihjasimme, että tämä esimerkki ei käänny. Selvitetään nyt miksi!

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-13/output.txt}}
```

Virheilmoitus kertoo, että `counter`-arvo siirrettiin silmukan edellisessä iteraatiossa. Rust kertoo meille, ettemme voi siirtää `counter`-lukon omistajuutta useille säikeille. Korjataan kääntäjävirhe moniomistajuusmenetelmällä, josta puhuimme luvussa 15.

#### Moniomistajuus useilla säikeillä

Luvussa 15 annoimme arvon useille omistajille käyttämällä älykästä osoitinta `Rc<T>` viittauslaskennan arvon luomiseksi. Tehdään sama tässä ja katsotaan, mitä tapahtuu. Käärimme `Mutex<T>`-tyypin `Rc<T>`-tyyppiin listauksessa 16-14 ja kloonaamme `Rc<T>`-tyypin ennen omistajuuden siirtämistä säikeeseen.

<Listing number="16-14" file-name="src/main.rs" caption="Yritys käyttää `Rc<T>`-tyyppiä salliaksemme useiden säikeiden omistaa `Mutex<T>`-tyypin">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-14/src/main.rs}}
```

</Listing>

Käännetään jälleen ja saamme... erilaisia virheitä! Kääntäjä opettaa meille paljon:

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-14/output.txt}}
```

Vau, tuo virheilmoitus on hyvin pitkä! Tässä on tärkeä osa, johon kannattaa keskittyä: `` `Rc<Mutex<i32>>` cannot be sent between threads safely ``. Kääntäjä kertoo myös syyn: `` the trait `Send` is not implemented for `Rc<Mutex<i32>>` ``. Puhumme `Send`-traitista seuraavassa osiossa: se on yksi trateista, jotka varmistavat, että säikeiden kanssa käyttämämme tyypit on tarkoitettu rinnakkaisiin tilanteisiin.

Valitettavasti `Rc<T>` ei ole turvallinen jaettavaksi säikeiden välillä. Kun `Rc<T>` hallinnoi viittauslaskentaa, se lisää laskuria jokaisella `clone`-kutsulla ja vähentää laskuria, kun jokainen klooni pudotetaan. Se ei kuitenkaan käytä rinnakkaisuusprimitiivejä varmistaakseen, ettei toinen säie voi keskeyttää muutoksia laskuriin. Tämä voisi johtaa virheellisiin laskuriarvoihin – hienovaraisiin vikoihin, jotka puolestaan voisivat johtaa muistivuotoihin tai arvon pudottamiseen ennen kuin olemme valmiita sen kanssa. Tarvitsemme tyypin, joka on täsmälleen kuin `Rc<T>`, mutta joka tekee muutokset viittauslaskuriin säikeistä turvallisella tavalla.

#### Atominen viittauslaskenta `Arc<T>`-tyypillä

Onneksi `Arc<T>` _on_ `Rc<T>`:n kaltainen tyyppi, joka on turvallinen käyttää rinnakkaisissa tilanteissa. _a_ tarkoittaa _atomic_ (atominen), eli kyseessä on _atomisesti viittauslaskettu_ tyyppi. Atomit ovat eräänlainen rinnakkaisuusprimitiivi, jota emme käsittele tässä yksityiskohtaisesti: katso standardikirjaston dokumentaatio [`std::sync::atomic`][atomic]<!-- ignore --> -moduulista lisätietoja. Tässä vaiheessa sinun tarvitsee vain tietää, että atomit toimivat kuin primitiivityypit, mutta ne ovat turvallisia jaettavaksi säikeiden välillä.

Saatat sitten ihmetellä, miksi kaikki primitiivityypit eivät ole atomisia ja miksi standardikirjaston tyyppejä ei ole toteutettu käyttämään `Arc<T>`-tyyppiä oletuksena. Syy on, että säikeistettävyys tuo mukanaan suorituskykyrasitteen, jonka haluat maksaa vain, kun sitä todella tarvitset. Jos suoritat operaatioita arvoihin yhdessä säikeessä, koodisi voi toimia nopeammin, jos sen ei tarvitse pakottaa atomien tarjoamia takeita.

Palataan esimerkkiimme: `Arc<T>`- ja `Rc<T>`-tyypeillä on sama API, joten korjaamme ohjelmamme muuttamalla `use`-riviä, `new`-kutsua ja `clone`-kutsua. Listauksen 16-15 koodi kääntyy vihdoin ja toimii.

<Listing number="16-15" file-name="src/main.rs" caption="`Arc<T>`-tyypin käyttö `Mutex<T>`-tyypin käärimiseen omistajuuden jakamiseksi useiden säikeiden välillä">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-15/src/main.rs}}
```

</Listing>

Tämä koodi tulostaa seuraavan:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Result: 10
```

Onnistuimme! Laskimme arvosta 0 arvoon 10, mikä ei ehkä vaikuta kovin vaikuttavalta, mutta se opetti meille paljon `Mutex<T>`-tyypistä ja säikeistä turvallisuudesta. Voit myös käyttää tämän ohjelman rakennetta monimutkaisempiin operaatioihin kuin pelkkään laskurin kasvattamiseen. Tällä strategialla voit jakaa laskennan itsenäisiin osiin, jakaa nämä osat säikeille ja käyttää sitten `Mutex<T>`-tyyppiä, jotta jokainen säie päivittää lopputuloksen omalla osallaan.

Huomaa, että jos suoritat yksinkertaisia numeerisia operaatioita, standardikirjaston [`std::sync::atomic`-moduuli][atomic]<!-- ignore --> tarjoaa yksinkertaisempia tyyppejä kuin `Mutex<T>`-tyypit. Nämä tyypit tarjoavat turvallisen, rinnakkaisen, atomisen pääsyn primitiivityyppeihin. Valitsimme tässä esimerkissä `Mutex<T>`-tyypin primitiivityypin kanssa, jotta voimme keskittyä siihen, miten `Mutex<T>` toimii.

<!-- Old headings. Do not remove or links may break. -->

<a id="similarities-between-refcelltrct-and-mutextarct"></a>

### `RefCell<T>`/`Rc<T>`- ja `Mutex<T>`/`Arc<T>`-tyyppien vertailu

Saatat olla huomannut, että `counter` on muuttumaton, mutta pystyimme saamaan muuttuvan viitteen sen sisällä olevaan arvoon; tämä tarkoittaa, että `Mutex<T>` tarjoaa sisäisen mutabiliteetin, kuten `Cell`-perhe. Samalla tavalla kuin käytimme `RefCell<T>`-tyyppiä luvussa 15 salliaksemme sisällön mutatoimisen `Rc<T>`-tyypin sisällä, käytämme `Mutex<T>`-tyyppiä sisällön mutatoimiseen `Arc<T>`-tyypin sisällä.

Toinen huomioitava yksityiskohta on, että Rust ei voi suojella sinua kaikilta loogisilta virheiltä, kun käytät `Mutex<T>`-tyyppiä. Muista luvusta 15, että `Rc<T>`-tyypin käyttöön liittyi riski luoda viittauskiertoja, joissa kaksi `Rc<T>`-arvoa viittaa toisiinsa ja aiheuttaa muistivuotoja. Vastaavasti `Mutex<T>`-tyyppiin liittyy riski luoda _lukoittumisia_. Ne syntyvät, kun operaatio tarvitsee lukita kaksi resurssia ja kaksi säiettä on hankkinut kummankin lukituksen, jolloin ne odottavat toisiaan ikuisesti. Jos olet kiinnostunut lukoittumisista, kokeile luoda Rust-ohjelma, jossa on lukoittuminen; tutki sitten lukoittumisten lieventämisstrategioita mutekseille missä tahansa kielessä ja kokeile toteuttaa ne Rustissa. Standardikirjaston API-dokumentaatio `Mutex<T>`- ja `MutexGuard`-tyypeille tarjoaa hyödyllistä tietoa.

Päätämme tämän luvun keskustelemalla `Send`- ja `Sync`-traiteista ja siitä, miten voimme käyttää niitä mukautettujen tyyppien kanssa.

[atomic]: ../std/sync/atomic/index.html
