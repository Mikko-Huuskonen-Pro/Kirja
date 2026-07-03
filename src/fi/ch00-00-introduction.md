# Johdanto

> Huom: Tämä kirjan painos on sama kuin [The Rust Programming
> Language][nsprust], joka on saatavilla painettuna ja e-kirjana [No Starch
> Press][nsp] -kustantajalta.

[nsprust]: https://nostarch.com/rust-programming-language-3rd-edition
[nsp]: https://nostarch.com/

Tervetuloa lukemaan _The Rust Programming Language_ -kirjaa, joka on johdatus Rust-ohjelmointikieleen.
Rust-ohjelmointikieli auttaa sinua kirjoittamaan nopeampaa ja luotettavampaa ohjelmistoa.
Korkean tason ergonomia ja matalan tason hallinta ovat usein ristiriidassa ohjelmointikielten
suunnittelussa; Rust haastaa tämän ristiriidan. Tasapainottamalla tehokasta teknistä
kapasiteettia ja erinomaista kehittäjäkokemusta Rust antaa sinulle mahdollisuuden hallita
matalan tason yksityiskohtia (kuten muistin käyttöä) ilman perinteisesti näihin liittyvää
vaivannäköä.

## Kenelle Rust sopii

Rust sopii monille ihmisille monista syistä. Katsotaan muutamia tärkeimpiä ryhmiä.

### Kehittäjätiimit

Rust on osoittautunut tuottavaksi työkaluksi suurten kehittäjätiimien yhteistyöhön,
joissa on eri tasoisia järjestelmäohjelmoinnin osaamista. Matalan tason koodi on altis
monille hienovaraisille bugeille, jotka useimmissa muissa kielissä havaitaan vasta
laajan testauksen ja kokeneiden kehittäjien huolellisen koodikatselmuksen kautta. Rustissa
kääntäjä toimii portinvartijana kieltäytymällä kääntämästä koodia, jossa on näitä vaikeasti
havaittavia bugeja, mukaan lukien rinnakkaisuusbugeja. Työskennellessään kääntäjän rinnalla
tiimi voi keskittyä ohjelman logiikkaan sen sijaan, että jahtaisi bugeja.

Rust tuo myös nykyaikaiset kehittäjätyökalut järjestelmäohjelmoinnin maailmaan:

- Cargo, mukana tuleva riippuvuuksien hallintatyökalu ja build-työkalu, tekee
  riippuvuuksien lisäämisestä, kääntämisestä ja hallinnasta vaivatonta ja yhtenäistä
  koko Rust-ekosysteemissä.
- `rustfmt`-muotoilutyökalu varmistaa yhtenäisen koodaustyylin eri kehittäjien välillä.
- Rust Language Server tarjoaa integroidun kehitysympäristön (IDE) tuen koodin
  täydennykselle ja rivikohtaisille virheilmoituksille.

Käyttämällä näitä ja muita Rust-ekosysteemin työkaluja kehittäjät voivat olla tuottavia
kirjoittaessaan järjestelmätason koodia.

### Opiskelijat

Rust sopii opiskelijoille ja niille, jotka ovat kiinnostuneita oppimaan järjestelmäkäsitteistä.
Rustin avulla monet ovat oppineet aiheita, kuten käyttöjärjestelmien kehitystä. Yhteisö on
erittäin vieraanvarainen ja vastaa mielellään opiskelijoiden kysymyksiin. Tämän kirjan kaltaisten
ponnistusten kautta Rust-tiimit haluavat tehdä järjestelmäkäsitteistä helpommin saavutettavia
useammille ihmisille, erityisesti ohjelmointiin vasta tutustuville.

### Yritykset

Satoja yrityksiä, suuria ja pieniä, käyttää Rustia tuotannossa monenlaisiin tehtäviin,
mukaan lukien komentorivityökalut, web-palvelut, DevOps-työkalut, sulautetut laitteet,
äänen ja videon analysointi ja transkoodaus, kryptovaluutat, bioinformatiikka, hakukoneet,
esineiden internet -sovellukset, koneoppiminen ja jopa merkittäviä osia Firefox-selaimesta.

### Avoimen lähdekoodin kehittäjät

Rust on niille, jotka haluavat rakentaa Rust-ohjelmointikieltä, yhteisöä, kehittäjätyökaluja
ja kirjastoja. Haluaisimme mielellämme sinun osallistuvan Rust-kielen kehitykseen.

### Nopeutta ja vakautta arvostavat

Rust on niille, jotka kaipaavat nopeutta ja vakautta kielessä. Nopeudella tarkoitamme sekä
sitä, kuinka nopeasti Rust-koodi voi suorittua, että sitä, kuinka nopeasti Rustin avulla voi
kirjoittaa ohjelmia. Rust-kääntäjän tarkistukset varmistavat vakauden ominaisuuksien lisäysten
ja refaktoroinnin aikana. Tämä eroaa hauraasta legacy-koodista kielissä, joissa näitä tarkistuksia
ei ole ja jota kehittäjät usein pelkäävät muokata. Pyrkimällä nollakustannuksisiin abstraktioihin—
korkean tason ominaisuuksiin, jotka kääntyvät matalan tason koodiksi yhtä nopeasti kuin käsin
kirjoitettu koodi—Rust pyrkii tekemään turvallisesta koodista myös nopeaa koodia.

Rust-kieli toivoo tukevansa monia muitakin käyttäjiä; tässä mainitut ovat vain joitakin
suurimpia sidosryhmiä. Kaiken kaikkiaan Rustin suurin tavoite on poistaa kompromissit, jotka
ohjelmoijat ovat hyväksyneet vuosikymmeniä, tarjoamalla turvallisuuden _ja_ tuottavuuden,
nopeuden _ja_ ergonomian. Kokeile Rustia ja katso, toimivatko sen valinnat sinulle.

## Kenelle tämä kirja on tarkoitettu

Tämä kirja olettaa, että olet kirjoittanut koodia toisella ohjelmointikielellä, mutta se ei
tee oletuksia siitä, millä kielellä. Olemme pyrkineet tekemään materiaalista laajasti
saavutettavaa erilaisista ohjelmointitaustoista tuleville. Emme käytä paljon aikaa siihen,
mitä ohjelmointi _on_ tai miten siitä ajatellaan. Jos olet täysin uusi ohjelmoinnissa, saat
paremman hyödyn kirjasta, joka on erityisesti suunnattu ohjelmoinnin johdatukseksi.

## Kuinka käyttää tätä kirjaa

Yleensä tämä kirja olettaa, että luet sen järjestyksessä alusta loppuun. Myöhemmät luvut
rakentuvat aiempien lukujen käsitteiden varaan, ja aiemmat luvut eivät välttämättä syvenny
tiettyyn aiheeseen, vaan palaavat siihen myöhemmässä luvussa.

Löydät tästä kirjasta kahta lajia lukuja: käsite- ja projektilukuja. Käsite-luvuissa opit
Rustin jonkin puolen. Projektiluvuissa rakennamme yhdessä pieniä ohjelmia soveltaen tähän
mennessä oppimaasi. Luvut 2, 12 ja 21 ovat projektilukuja; muut ovat käsite-lukuja.

**Luku 1** selittää, miten Rust asennetaan, miten kirjoitetaan "Hello, world!" -ohjelma ja
miten käytetään Cargo-työkalua, Rustin paketinhallintaa ja build-työkalua. **Luku 2** on
käytännönläheinen johdatus Rust-ohjelman kirjoittamiseen, jossa rakennat arvauspeliä. Tässä
käsittelemme asioita korkealla tasolla, ja myöhemmät luvut tarjoavat lisätietoa. Jos haluat
päästä heti käsiksi koodiin, Luku 2 on oikea paikka. Jos olet erityisen huolellinen oppija,
joka haluaa oppia jokaisen yksityiskohdan ennen seuraavaan siirtymistä, voit ohittaa Luvun 2
ja siirtyä suoraan **Lukuun 3**, joka käsittelee Rustin ominaisuuksia, jotka ovat samankaltaisia
kuin muissa ohjelmointikielissä; voit sitten palata Lukuun 2, kun haluat työskennellä projektin
parissa soveltaen oppimaasi.

**Luvussa 4** opit Rustin omistajuusjärjestelmästä. **Luku 5** käsittelee structeja ja metodeja.
**Luku 6** käsittelee enumeja, `match`-lausekkeita sekä `if let`- ja `let...else`-ohjausrakenteita.
Käytät structeja ja enumeja mukautettujen tyyppien luomiseen.

**Luvussa 7** opit Rustin moduulijärjestelmästä ja yksityisyysäännöistä koodin ja sen julkisen
sovellusohjelmointirajapinnan (API) järjestämiseen. **Luku 8** käsittelee joitakin yleisiä
kokoelmien tietorakenteita, joita standardikirjasto tarjoaa: vektoreita, merkkijonoja ja
hash-taulukoita. **Luku 9** tutkii Rustin virheenkäsittelyfilosofiaa ja -tekniikoita.

**Luku 10** syventyy geneerisyyteen, traitteihin ja elinikäihin, jotka antavat sinulle mahdollisuuden
määritellä koodia, joka soveltuu useille tyypeille. **Luku 11** käsittelee testausta, joka on
tarpeen Rustin turvallisuustakuista huolimatta varmistamaan ohjelmasi logiikan oikeellisuus.
**Luvussa 12** rakennamme oman toteutuksemme osasta `grep`-komentorivityökalun toiminnallisuudesta,
joka etsii tekstiä tiedostoista. Tähän käytämme monia aiemmissa luvuissa käsittelemiämme käsitteitä.

**Luku 13** tutkii sulkeumia ja iteraattoreita: Rustin ominaisuuksia, jotka tulevat funktionaalisista
ohjelmointikielistä. **Luvussa 14** tarkastelemme Cargo-työkalua tarkemmin ja puhumme parhaista
käytännöistä kirjastojesi jakamiseen muiden kanssa. **Luku 15** käsittelee älykkäitä osoittimia,
joita standardikirjasto tarjoaa, ja traitteja, jotka mahdollistavat niiden toiminnallisuuden.

**Luvussa 16** käymme läpi erilaisia rinnakkaisohjelmoinnin malleja ja puhumme siitä, miten Rust
auttaa sinua ohjelmoimaan useissa säikeissä pelottomasti. **Luvussa 17** rakennamme tämän päälle
tutkien Rustin async- ja await-syntaksia sekä tehtäviä, futureja ja streameja ja niiden
mahdollistamaa kevyttä rinnakkaisuusmallia.

**Luku 18** tarkastelee, miten Rustin idiomit vertautuvat tuttuihin olio-ohjelmoinnin periaatteisiin.
**Luku 19** on viite kuvioihin ja kuvioiden täsmäyttämiseen, jotka ovat tehokkaita tapoja ilmaista
ideoita Rust-ohjelmissa. **Luku 20** sisältää valikoiman edistyneitä aiheita, mukaan lukien unsafe
Rust, makrot ja lisätietoa elinikäistä, traitteista, tyypeistä, funktioista ja sulkeumista.

**Luvussa 21** viimeistelemme projektin, jossa toteutamme matalan tason monisäikeisen web-palvelimen!

Lopuksi joissakin liitteissä on hyödyllistä tietoa kielestä viitemuotoisemmassa muodossa.
**Liite A** käsittelee Rustin avainsanoja, **Liite B** Rustin operaattoreita ja symboleja,
**Liite C** standardikirjaston tarjoamia johdettavia traitteja, **Liite D** hyödyllisiä
kehitystyökaluja ja **Liite E** selittää Rustin editioneja. **Liitteestä F** löydät kirjan
käännökset, ja **Liitteessä G** käsittelemme, miten Rustia tehdään ja mitä nightly Rust on.

Tätä kirjaa voi lukea monella tavalla: jos haluat hypätä eteenpäin, tee se! Saatat joutua
palaamaan aiempiin lukuihin, jos kohtaat hämmennystä. Tee kuitenkin miten parhaalta tuntuu.

<span id="ferris"></span>

Tärkeä osa Rustin oppimista on oppia lukemaan kääntäjän näyttämiä virheilmoituksia: ne
ohjaavat sinua kohti toimivaa koodia. Siksi tarjoamme monia esimerkkejä, jotka eivät käänny,
sekä kääntäjän näyttämän virheilmoituksen kussakin tilanteessa. Huomaa, että jos kirjoitat
ja suoritat satunnaisen esimerkin, se ei välttämättä käänny! Varmista, että luet ympäröivän
tekstin nähdäksesi, onko esimerkki, jota yrität suorittaa, tarkoitettu virheeseen. Useimmissa
tilanteissa ohjaamme sinut oikeaan versioon koodista, joka ei käänny. Ferris auttaa myös
erottamaan koodin, joka ei ole tarkoitettu toimimaan:

| Ferris                                                                                                           | Merkitys                                          |
| ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| <img src="img/ferris/does_not_compile.svg" class="ferris-explain" alt="Ferris with a question mark"/>            | Tämä koodi ei käänny!                            |
| <img src="img/ferris/panics.svg" class="ferris-explain" alt="Ferris throwing up their hands"/>                   | Tämä koodi panikoi!                              |
| <img src="img/ferris/not_desired_behavior.svg" class="ferris-explain" alt="Ferris with one claw up, shrugging"/> | Tämä koodi ei tuota haluttua käyttäytymistä.     |

Useimmissa tilanteissa ohjaamme sinut oikeaan versioon koodista, joka ei käänny.

## Lähdekoodi

Tämän kirjan lähdekooditiedostot löytyvät [GitHubista][book].

[book]: https://github.com/rust-lang/book/tree/main/src
