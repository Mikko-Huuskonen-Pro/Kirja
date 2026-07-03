<!-- Old headings. Do not remove or links may break. -->

<a id="extensible-concurrency-with-the-sync-and-send-traits"></a>
<a id="extensible-concurrency-with-the-send-and-sync-traits"></a>

## Laajennettava rinnakkaisuus `Send`- ja `Sync`-traitien avulla

Mielenkiintoista kyllä, lähes kaikki rinnakkaisuusominaisuudet, joista olemme puhuneet tässä luvussa, ovat olleet osa standardikirjastoa, eivät kieltä. Rinnakkaisuuden käsittelyn vaihtoehdot eivät rajoitu kieleen tai standardikirjastoon; voit kirjoittaa omia rinnakkaisuusominaisuuksiasi tai käyttää muiden kirjoittamia.

Kielen sisään upotettuja rinnakkaisuuskäsitteitä ovat kuitenkin muun muassa `std::marker`-traitit `Send` ja `Sync`.

<!-- Old headings. Do not remove or links may break. -->

<a id="allowing-transference-of-ownership-between-threads-with-send"></a>

### Omistajuuden siirtäminen säikeiden välillä

`Send`-merkkaustraitti osoittaa, että tätä traitia toteuttavan tyypin arvojen omistajuus voidaan siirtää säikeiden välillä. Lähes jokainen Rustin tyyppi toteuttaa `Send`-traitin, mutta on olemassa poikkeuksia, kuten `Rc<T>`: tämä ei voi toteuttaa `Send`-traitia, koska jos kloonaisit `Rc<T>`-arvon ja yrittäisit siirtää kloonin omistajuuden toiseen säikeeseen, molemmat säikeet saattaisivat päivittää viittauslaskuria samanaikaisesti. Tästä syystä `Rc<T>` on toteutettu käytettäväksi yksisäikeisissä tilanteissa, joissa et halua maksaa säikeistettävyyteen liittyvää suorituskykyrasitetta.

Rustin tyyppijärjestelmä ja trait-rajoitukset varmistavat siis, ettei voi vahingossa lähettää `Rc<T>`-arvoa säikeiden välillä turvattomasti. Kun yritimme tehdä tämän listauksessa 16-14, saimme virheen `` the trait `Send` is not implemented for `Rc<Mutex<i32>>` ``. Kun vaihdoimme `Arc<T>`-tyyppiin, joka toteuttaa `Send`-traitin, koodi kääntyi.

Mikä tahansa tyyppi, joka koostuu kokonaan `Send`-tyypeistä, merkitään automaattisesti myös `Send`-traitilla. Lähes kaikki primitiivityypit ovat `Send`, lukuun ottamatta raakaviittauksia, joita käsittelemme luvussa 20.

<!-- Old headings. Do not remove or links may break. -->

<a id="allowing-access-from-multiple-threads-with-sync"></a>

### Pääsy useista säikeistä

`Sync`-merkkaustraitti osoittaa, että tätä traitia toteuttavaan tyyppiin on turvallista viitata useista säikeistä. Toisin sanoen mikä tahansa tyyppi `T` toteuttaa `Sync`-traitin, jos `&T` (muuttumaton viittaus tyyppiin `T`) toteuttaa `Send`-traitin, eli viittaus voidaan lähettää turvallisesti toiseen säikeeseen. Samoin kuin `Send`-traitin kohdalla, primitiivityypit toteuttavat kaikki `Sync`-traitin, ja tyypit, jotka koostuvat kokonaan `Sync`-traitia toteuttavista tyypeistä, toteuttavat myös `Sync`-traitin.

Älykäs osoitin `Rc<T>` ei myöskään toteuta `Sync`-traitia samoista syistä kuin se ei toteuta `Send`-traitia. `RefCell<T>`-tyyppi (josta puhuimme luvussa 15) ja siihen liittyvä `Cell<T>`-tyyppien perhe eivät toteuta `Sync`-traitia. `RefCell<T>`-tyypin ajonaikainen lainanvalvonta ei ole säikeistä turvallista. Älykäs osoitin `Mutex<T>` toteuttaa `Sync`-traitin ja sitä voidaan käyttää jakamaan pääsy useille säikeille, kuten näit [”Jaettu pääsy `Mutex<T>`-tyyppiin”][shared-access]<!-- ignore --> -osiossa.

### `Send`- ja `Sync`-traitien manuaalinen toteuttaminen on turvatonta

Koska tyypit, jotka koostuvat kokonaan muista tyypeistä, jotka toteuttavat `Send`- ja `Sync`-traitit, toteuttavat automaattisesti myös `Send`- ja `Sync`-traitit, emme tarvitse toteuttaa näitä traiteja manuaalisesti. Merkkaustraiteina niillä ei ole edes toteutettavia metodeja. Ne ovat hyödyllisiä vain rinnakkaisuuteen liittyvien invarianttien pakottamiseen.

Näiden traitien manuaalinen toteuttaminen edellyttää turvattoman Rust-koodin kirjoittamista. Käsittelemme turvattoman Rust-koodin käyttöä luvussa 20; toistaiseksi tärkeää tietää on, että uusien rinnakkaisuustyyppien rakentaminen, jotka eivät koostu `Send`- ja `Sync`-osista, vaatii huolellista pohdintaa turvallisuustakuujen ylläpitämiseksi. [”The Rustonomicon”][nomicon] sisältää lisätietoa näistä takuista ja niiden ylläpidosta.

## Yhteenveto

Tämä ei ole viimeinen kerta, kun kohtaamme rinnakkaisuuden tässä kirjassa: seuraava luku keskittyy asynkroniseen ohjelmointiin, ja luvun 21 projekti käyttää tämän luvun käsitteitä realistisemmassa tilanteessa kuin tässä käsitellyt pienemmät esimerkit.

Kuten aiemmin mainittiin, koska hyvin vähän siitä, miten Rust käsittelee rinnakkaisuutta, on osa kieltä, monet rinnakkaisuusratkaisut toteutetaan kirjastoina. Nämä kehittyvät nopeammin kuin standardikirjasto, joten kannattaa etsiä verkosta ajankohtaisia, huippuluokan kirjastoja monisäikeisiin tilanteisiin.

Rustin standardikirjasto tarjoaa kanavia viestinvälitykseen ja älykkäitä osoitintyyppejä, kuten `Mutex<T>` ja `Arc<T>`, jotka ovat turvallisia käyttää rinnakkaisissa konteksteissa. Tyyppijärjestelmä ja lainanvalvonta varmistavat, että näitä ratkaisuja käyttävä koodi ei päädy tietokilpailutilanteisiin tai virheellisiin viittauksiin. Kun saat koodisi kääntymään, voit olla varma, että se toimii useilla säikeillä ilman muiden kielten yleisiä vaikeasti jäljitettäviä vikoja. Rinnakkaisohjelmointi ei ole enää käsite, jota kannattaa pelätä: eteenpäin ja tee ohjelmistasi rinnakkaisia – pelottomasti!

[shared-access]: ch16-03-shared-state.html#shared-access-to-mutext
[nomicon]: ../nomicon/index.html
