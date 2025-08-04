# Johdanto

> Huom: Tämä kirjan versio on sama kuin [The Rust Programming Language][nsprust], 
> joka on saatavilla painettuna ja e-kirjana [No Starch Pressiltä][nsp] englanniksi.

[nsprust]: https://nostarch.com/rust-programming-language-2nd-edition
[nsp]: https://nostarch.com/

Tervetuloa _The Rust Programming Language_ -kirjaan, joka toimii johdantona Rustiin.
Rust-ohjelmointikieli auttaa kirjoittamaan nopeampaa ja luotettavampaa ohjelmistoa.
Ohjelmointikielissä korkean tason käytettävyys ja matalan tason hallinta ovat usein ristiriidassa keskenään; 
Rust haastaa tämän asetelman. Yhdistämällä tehokkaan teknisen suorituskyvyn ja erinomaisen 
kehittäjäkokemuksen Rust antaa sinulle mahdollisuuden hallita matalan tason yksityiskohtia (kuten muistin käyttöä) 
ilman perinteisesti siihen liittyvää vaivaa.

## Kenelle Rust on tarkoitettu?

Rust sopii monenlaisille kehittäjille ja käyttäjille. Tarkastellaan joitakin keskeisiä ryhmiä.

### Kehitystiimit

Rust osoittautuu tuottavaksi työkaluksi suurille kehitystiimeille, joiden jäsenillä on vaihteleva 
kokemus järjestelmätason ohjelmoinnista. Matalan tason koodi on altis monille hienovaraisille 
bugeille, jotka useimmissa muissa kielissä havaitaan vain laajamittaisella testaamisella ja 
kokeneiden kehittäjien huolellisella koodikatselmoinnilla. Rustin kääntäjä toimii portinvartijana, 
joka kieltäytyy kääntämästä koodia, jossa on tällaisia vaikeasti havaittavia virheitä, mukaan lukien rinnakkaisuusvirheet. 
Työskentelemällä yhdessä kääntäjän kanssa tiimi voi keskittyä ohjelman logiikkaan virheiden metsästämisen sijaan.

Rust tuo myös modernit kehitystyökalut järjestelmätason ohjelmointiin:

- Cargo, sisäänrakennettu riippuvuuksien hallinta- ja rakennustyökalu, tekee riippuvuuksien hallinnasta helppoa ja yhdenmukaista koko Rust-ekosysteemissä.
- Rustfmt-muotoilutyökalu varmistaa yhtenäisen koodityylin kehittäjien kesken.
- Rust-analyzer tarjoaa IDE-integraation, joka mahdollistaa koodintäydennyksen ja reaaliaikaiset virheilmoitukset.

Näiden työkalujen ja muun Rust-ekosysteemin avulla kehittäjät voivat olla tuottavia kirjoittaessaan järjestelmätason koodia.

### Opiskelijat

Rust on hyvä valinta opiskelijoille ja kaikille, jotka haluavat oppia järjestelmätason ohjelmoinnista. 
Rustin avulla monet ovat oppineet aiheista, kuten käyttöjärjestelmien kehittämisestä. Yhteisö on hyvin 
tervetullut ja innokas vastaamaan opiskelijoiden kysymyksiin. Rust-tiimit haluavat tehdä järjestelmätason 
ohjelmoinnin helpommin lähestyttäväksi yhä useammille ihmisille.

### Yritykset

Sadat yritykset, sekä suuret että pienet, käyttävät Rustia tuotannossa monenlaisiin tehtäviin, kuten:

- komentorivityökalut
- verkkopalvelut
- DevOps-työkalut
- sulautetut järjestelmät
- äänen ja videon analysointi ja transkoodaus
- kryptovaluutat
- bioinformatiikka
- hakukoneet
- IoT-sovellukset
- koneoppiminen
- merkittävät osat Firefox-selaimesta

### Avoimen lähdekoodin kehittäjät

Rust on myös niille, jotka haluavat rakentaa Rust-ohjelmointikieltä, sen yhteisöä, kehittäjätyökaluja ja kirjastoja. Olet tervetullut osallistumaan Rustin kehitykseen!

### Nopeutta ja vakautta arvostavat kehittäjät

Rust on tarkoitettu niille, jotka arvostavat sekä nopeutta että vakautta ohjelmointikielessä. Nopeudella tarkoitetaan sekä Rust-koodin suoritustehoa että ohjelmoinnin tehokkuutta. Rustin kääntäjä varmistaa vakauden uusien ominaisuuksien ja refaktoroinnin myötä. Tämä eroaa perinteisistä kielistä, joissa kehittäjät usein pelkäävät muokata haurasta perintökoodia.

Rust pyrkii yhdistämään turvallisuuden _ja_ tuottavuuden, nopeuden _ja_ helppokäyttöisyyden. Kokeile Rustia ja katso, sopiiko sen lähestymistapa sinulle.

## Kenelle tämä kirja on tarkoitettu?

Kirja olettaa, että olet kirjoittanut koodia jollakin ohjelmointikielellä aiemmin, mutta ei edellytä tietoa mistään tietystä kielestä. Kirja ei keskity perusohjelmointikäsitteisiin, joten jos olet täysin uusi ohjelmoinnissa, voi olla parempi aloittaa kirja, joka toimii yleisenä ohjelmointijohdantona.

## Miten tätä kirjaa kannattaa lukea?

<span id="ferris"></span>

Yleisesti ottaen tämä kirja on tarkoitettu luettavaksi järjestyksessä alusta loppuun. Myöhemmät luvut rakentuvat aiempien lukujen käsitteiden varaan, ja aiemmat luvut eivät välttämättä käsittele tiettyjä aiheita syvällisesti, vaan palaavat niihin myöhemmin.

Kirjassa on kahdenlaisia lukuja: käsitelukuja ja projektipohjaisia lukuja. Käsiteluvuissa opit Rustin eri ominaisuuksista, kun taas projektipohjaisissa luvuissa rakennamme yhdessä pieniä ohjelmia hyödyntäen aiemmin opittuja asioita. Luvut 2, 12 ja 21 ovat projektipohjaisia, kun taas muut ovat käsitelukuja.

Luku 1 opettaa, kuinka Rust asennetaan, miten kirjoitetaan "Hello, world!" -ohjelma ja miten käytetään Cargoa, Rustin pakettienhallintaa ja rakennustyökalua. Luku 2 toimii käytännön johdantona Rust-ohjelmointiin: siinä toteutetaan yksinkertainen arvauspeli. Tässä luvussa käsitteet esitellään korkealla tasolla, ja yksityiskohtiin palataan myöhemmissä luvuissa. Jos haluat aloittaa heti käytännön tekemisellä, Luku 2 on oikea paikka. Luku 3 käsittelee Rustin piirteitä, jotka muistuttavat muiden ohjelmointikielien ominaisuuksia, ja Luvussa 4 opit Rustin omistajuusmallin perusteet. Jos haluat oppia kaikki yksityiskohdat ensin, voit halutessasi ohittaa Luvun 2 ja siirtyä suoraan Lukuun 3, palaten myöhemmin Lukuun 2, kun haluat soveltaa oppimaasi käytännössä.

Luku 5 käsittelee rakenteita (structs) ja metodeja, ja Luku 6 esittelee luettelotyypit (enums), match-lauseet sekä if let -rakenteen. Näiden avulla voit luoda Rustissa omia tyyppejä.

Luvussa 7 opit Rustin moduulijärjestelmän sekä siihen liittyvät näkyvyyssäännöt, jotka auttavat jäsentämään koodiasi ja määrittämään, mikä osa siitä on julkinen API (Application Programming Interface). Luku 8 käsittelee Rustin vakiona tarjoamia kokoelmatietorakenteita, kuten vektoreita (vectors), merkkijonoja (strings) ja hajautustauluja (hash maps). Luku 9 käsittelee Rustin virheenkäsittelyfilosofiaa ja tekniikoita.

Luvussa 10 tutustut geneerisiin tyyppeihin (generics), rajapintoihin (traits) ja elinaikoihin (lifetimes), joiden avulla voit kirjoittaa koodia, joka toimii useille eri tyypeille. Luku 11 keskittyy testaamiseen – vaikka Rust tarjoaa vahvat turvallisuustakuut, testaus on silti tärkeää ohjelman loogisen oikeellisuuden varmistamiseksi. Luku 12 sisältää projektin, jossa toteutamme oman version grep-tyyppisestä komentorivityökalusta, joka etsii tekstiä tiedostoista. Tässä käytämme monia aiemmissa luvuissa opittuja konsepteja.

Luku 13 käsittelee sulkeumia (closures) ja iteraattoreita (iterators), jotka ovat peräisin funktionaalisista ohjelmointikielistä. Luku 14 syventyy Cargoon ja parhaisiin käytäntöihin kirjastojen jakamiseen muiden kanssa. Luku 15 käsittelee Rustin tarjoamia älyosoittimia (smart pointers) ja niiden taustalla olevia rajapintoja (traits).

Luvussa 16 käsittelemme rinnakkaisohjelmointia ja sitä, miten Rust auttaa ohjelmoimaan turvallisesti useilla säikeillä. Luvussa 17 laajennamme tätä käsittelemällä Rustin async ja await -syntaksia, jotka mahdollistavat kevyen rinnakkaisuuden.

Luvussa 18 vertaamme Rustin idiomeja olio-ohjelmointiin ja tarkastelemme, miten Rust eroaa perinteisestä olio-ohjelmoinnista.

Luku 19 toimii hakemistona Rustin mallien (patterns) ja mallivastaavuuden (pattern matching) käyttöön – nämä ovat tehokkaita tapoja ilmaista ohjelmalogiikkaa. Luku 20 kattaa edistyneitä aiheita, kuten unsafe Rust, makrot, elinaikoihin, rajapintoihin ja tyyppeihin liittyviä lisätietoja.



| Ferris                                                                                                           | Merkitys                                          |
| ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| <img src="img/ferris/does_not_compile.svg" class="ferris-explain" alt="Ferris with a question mark"/>            | Tämä koodi ei käänny!                      |
| <img src="img/ferris/panics.svg" class="ferris-explain" alt="Ferris throwing up their hands"/>                   | Tämä koodi panikoi!                                |
| <img src="img/ferris/not_desired_behavior.svg" class="ferris-explain" alt="Ferris with one claw up, shrugging"/> | Tämä koodi ei käyttäydy kuten sen pitäisi |


## Lähdekoodi

Tämän kirjan lähdetiedostot löytyvät [GitHubista][book].

[book]: https://github.com/rust-lang/book/tree/main/src
