## Polut kohteen viittaamiseen moduulipuussa

Näyttääksemme Rustille, mistä kohteen moduulipuussa löytyy, käytämme polkua samalla tavalla kuin käytämme polkua navigoidessamme tiedostojärjestelmässä. Kutsuaksemme funktiota meidän on tiedettävä sen polku.

Polku voi olla kahdessa muodossa:

- _Absoluuttinen polku_ on täydellinen polku, joka alkaa crate-juuresta; ulkoisen crate:n koodille absoluuttinen polku alkaa crate:n nimellä, ja nykyisen crate:n koodille se alkaa literaalilla `crate`.
- _Suhteellinen polku_ alkaa nykyisestä moduulista ja käyttää `self`-, `super`- tai nykyisen moduulin tunnistetta.

Sekä absoluuttisia että suhteellisia polkuja seuraa yksi tai useampi tunniste, jotka on erotettu kaksoispisteillä (`::`).

Palataan listaukseen 7-1 ja oletetaan, että haluamme kutsua `add_to_waitlist`-funktiota. Tämä on sama kuin kysyisi: Mikä on `add_to_waitlist`-funktion polku? Listaus 7-3 sisältää listauksen 7-1, josta on poistettu joitakin moduuleja ja funktioita.

Näytämme kaksi tapaa kutsua `add_to_waitlist`-funktiota uudesta funktiosta `eat_at_restaurant`, joka on määritelty crate-juuressa. Nämä polut ovat oikein, mutta on vielä toinen ongelma, joka estää tämän esimerkin kääntymisen sellaisenaan. Selitämme syyn hetken kuluttua.

`eat_at_restaurant`-funktio on osa kirjastocrate:amme julkista API:a, joten merkitsemme sen `pub`-avainsanalla. Kohdassa [”Polkujen paljastaminen `pub`-avainsanalla”][pub]<!-- ignore --> käsittelemme `pub`:ia tarkemmin.

<Listing number="7-3" file-name="src/lib.rs" caption="`add_to_waitlist`-funktion kutsuminen absoluuttisilla ja suhteellisilla poluilla">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-03/src/lib.rs}}
```

</Listing>

Ensimmäisellä kerralla kun kutsumme `add_to_waitlist`-funktiota funktiossa `eat_at_restaurant`, käytämme absoluuttista polkua. `add_to_waitlist`-funktio on määritelty samassa crate:ssa kuin `eat_at_restaurant`, mikä tarkoittaa, että voimme käyttää `crate`-avainsanaa absoluuttisen polun aloittamiseen. Sisällytämme sitten jokaisen peräkkäisen moduulin, kunnes pääsemme `add_to_waitlist`-funktioon. Voit kuvitella tiedostojärjestelmän, jolla on sama rakenne: Määrittäisimme polun `/front_of_house/hosting/add_to_waitlist` suorittaaksemme `add_to_waitlist`-ohjelman; `crate`-nimen käyttäminen crate-juuresta aloittamiseen on kuin `/`-merkin käyttäminen tiedostojärjestelmän juuresta aloittamiseen komentorivilläsi.

Toisella kerralla kun kutsumme `add_to_waitlist`-funktiota funktiossa `eat_at_restaurant`, käytämme suhteellista polkua. Polku alkaa `front_of_house`-moduulin nimellä, joka on määritelty samalla tasolla moduulipuussa kuin `eat_at_restaurant`. Tässä tiedostojärjestelmän vastine olisi polun `front_of_house/hosting/add_to_waitlist` käyttäminen. Moduulin nimellä aloittaminen tarkoittaa, että polku on suhteellinen.

Valinta suhteellisen tai absoluuttisen polun käytöstä on päätös, jonka teet projektisi perusteella, ja se riippuu siitä, siirrätkö todennäköisemmin kohteen määrittelykoodia erikseen vai yhdessä koodin kanssa, joka käyttää kohdetta. Esimerkiksi jos siirtäisimme `front_of_house`-moduulin ja `eat_at_restaurant`-funktion moduuliin nimeltä `customer_experience`, meidän pitäisi päivittää absoluuttinen polku `add_to_waitlist`-funktioon, mutta suhteellinen polku olisi edelleen kelvollinen. Jos kuitenkin siirtäisimme `eat_at_restaurant`-funktion erikseen moduuliin nimeltä `dining`, absoluuttinen polku `add_to_waitlist`-kutsuun pysyisi samana, mutta suhteellinen polku pitäisi päivittää. Yleinen mieltymyksemme on määrittää absoluuttiset polut, koska on todennäköisempää, että haluamme siirtää koodin määrittelyjä ja kohteiden kutsuja toisistaan riippumatta.

Yritetään kääntää listaus 7-3 ja selvitetään, miksi se ei vielä käänny! Virheet, jotka saamme, on näytetty listauksessa 7-4.

<Listing number="7-4" caption="Kääntäjän virheet listauksen 7-3 koodin rakentamisesta">

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-03/output.txt}}
```

</Listing>

Virheilmoitukset sanovat, että moduuli `hosting` on yksityinen. Toisin sanoen meillä on oikeat polut `hosting`-moduuliin ja `add_to_waitlist`-funktioon, mutta Rust ei anna meidän käyttää niitä, koska sillä ei ole pääsyä yksityisiin osiin. Rustissa kaikki kohteet (funktiot, metodit, structit, enumit, moduulit ja vakiot) ovat oletuksena yksityisiä emomoduuleilleen. Jos haluat tehdä kohteen, kuten funktion tai structin, yksityiseksi, laitat sen moduuliin.

Emomoduulin kohteet eivät voi käyttää alimoduuulien yksityisiä kohteita, mutta alimoduuulien kohteet voivat käyttää esi-isämoduuliensa kohteita. Tämä johtuu siitä, että alimoduuulit käärivät ja piilottavat toteutustietonsa, mutta alimoduuulit näkevät kontekstin, jossa ne on määritelty. Jatkaaksemme metaforaamme, ajattele yksityisyyssääntöjä kuin ravintolan takaosaa: Siellä tapahtuva on yksityistä ravintolan asiakkaille, mutta toimistopäälliköt näkevät ja voivat tehdä kaiken ravintolassa, jota he hallinnoivat.

Rust päätti, että moduulijärjestelmä toimii tällä tavalla, jotta sisäisten toteutustietojen piilottaminen on oletus. Näin tiedät, mitä sisäisen koodin osia voit muuttaa rikkomatta ulkoista koodia. Rust antaa kuitenkin mahdollisuuden paljastaa alimoduuulien koodin sisäisiä osia ulommille esi-isämoduuleille käyttämällä `pub`-avainsanaa kohteen tekemiseksi julkiseksi.

### Polkujen paljastaminen `pub`-avainsanalla

Palataan listauksen 7-4 virheeseen, joka kertoi, että `hosting`-moduuli on yksityinen. Haluamme, että emomoduulin `eat_at_restaurant`-funktiolla on pääsy alimoduuulin `add_to_waitlist`-funktioon, joten merkitsemme `hosting`-moduulin `pub`-avainsanalla, kuten listauksessa 7-5.

<Listing number="7-5" file-name="src/lib.rs" caption="`hosting`-moduulin määrittely `pub`:ksi sen käyttämiseksi funktiosta `eat_at_restaurant`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-05/src/lib.rs:here}}
```

</Listing>

Valitettavasti listauksen 7-5 koodi tuottaa edelleen kääntäjän virheitä, kuten listauksessa 7-6.

<Listing number="7-6" caption="Kääntäjän virheet listauksen 7-5 koodin rakentamisesta">

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-05/output.txt}}
```

</Listing>

Mitä tapahtui? `pub`-avainsanan lisääminen `mod hosting` -lauseen eteen tekee moduulista julkisen. Tämän muutoksen jälkeen, jos pääsemme `front_of_house`-moduuliin, pääsemme `hosting`-moduuliin. Mutta `hosting`-moduulin _sisältö_ on edelleen yksityistä; moduulin tekeminen julkiseksi ei tee sen sisällöstä julkista. `pub`-avainsana moduulissa sallii vain sen esi-isämoduulien koodin viitata siihen, ei päästä sen sisäiseen koodiin. Koska moduulit ovat säiliöitä, pelkällä moduulin tekemisellä julkiseksi emme voi tehdä paljon; meidän on mentävä pidemmälle ja valittava tehdä yksi tai useampi moduulin sisällä olevista kohteista julkisiksi.

Listauksen 7-6 virheet sanovat, että `add_to_waitlist`-funktio on yksityinen. Yksityisyyssäännöt koskevat structeja, enumeja, funktioita ja metodeja sekä moduuleja.

Tehdään myös `add_to_waitlist`-funktiosta julkinen lisäämällä `pub`-avainsana sen määrittelyn eteen, kuten listauksessa 7-7.

<Listing number="7-7" file-name="src/lib.rs" caption="`pub`-avainsanan lisääminen `mod hosting` - ja `fn add_to_waitlist` -lauseisiin sallii funktion kutsumisen funktiosta `eat_at_restaurant`.">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-07/src/lib.rs:here}}
```

</Listing>

Nyt koodi kääntyy! Nähdäksemme, miksi `pub`-avainsanan lisääminen sallii näiden polkujen käytön funktiossa `eat_at_restaurant` yksityisyyssääntöjen suhteen, tarkastellaan absoluuttista ja suhteellista polkua.

Absoluuttisessa polussa aloitamme `crate`:sta, crate:amme moduulipuun juuresta. `front_of_house`-moduuli on määritelty crate-juuressa. Vaikka `front_of_house` ei ole julkinen, koska `eat_at_restaurant`-funktio on määritelty samassa moduulissa kuin `front_of_house` (eli `eat_at_restaurant` ja `front_of_house` ovat sisaruksia), voimme viitata `front_of_house`-moduuliin funktiosta `eat_at_restaurant`. Seuraavaksi on `hosting`-moduuli, joka on merkitty `pub`:lla. Pääsemme `hosting`-moduulin emomoduuliin, joten pääsemme `hosting`-moduuliin. Lopuksi `add_to_waitlist`-funktio on merkitty `pub`:lla, ja pääsemme sen emomoduuliin, joten tämä funktiokutsu toimii!

Suhteellisessa polussa logiikka on sama kuin absoluuttisessa polussa paitsi ensimmäisessä vaiheessa: Sen sijaan, että aloittaisimme crate-juuresta, polku alkaa `front_of_house`-moduulista. `front_of_house`-moduuli on määritelty samassa moduulissa kuin `eat_at_restaurant`, joten suhteellinen polku, joka alkaa moduulista, jossa `eat_at_restaurant` on määritelty, toimii. Sitten, koska `hosting` ja `add_to_waitlist` on merkitty `pub`:lla, polun loppuosa toimii, ja tämä funktiokutsu on kelvollinen!

Jos aiot jakaa kirjastocrate:asi, jotta muut projektit voivat käyttää koodiasi, julkinen API:si on sopimus crate:si käyttäjien kanssa, joka määrittää, miten he voivat olla vuorovaikutuksessa koodisi kanssa. Julkisen API:n muutosten hallintaan liittyy monia näkökohtia, jotka helpottavat ihmisten riippuvuutta crate:stasi. Nämä näkökohdat ylittävät tämän kirjan laajuuden; jos olet kiinnostunut tästä aiheesta, katso [Rust API Guidelines -ohjeet][api-guidelines].

> #### Parhaat käytännöt paketeille, joissa on binääri ja kirjasto
>
> Mainitsimme, että paketti voi sisältää sekä _src/main.rs_ binääricrate-juuren että _src/lib.rs_ kirjastocrate-juuren, ja molemmilla crate:illa on oletuksena paketin nimi. Tyypillisesti paketit, joissa on tämä malli sisältäen sekä kirjasto- että binääricrate:n, sisältävät binääricrate:ssa vain tarpeeksi koodia käynnistääkseen suoritettavan, joka kutsuu kirjastocrate:ssa määriteltyä koodia. Tämä antaa muiden projektien hyötyä suurimmasta osasta paketin tarjoamaa toiminnallisuutta, koska kirjastocrate:n koodia voidaan jakaa.
>
> Moduulipuu tulisi määritellä tiedostossa _src/lib.rs_. Sitten mitä tahansa julkisia kohteita voidaan käyttää binääricrate:ssa aloittamalla polut paketin nimellä. Binääricrate:sta tulee kirjastocrate:n käyttäjä aivan kuten täysin ulkoinen crate käyttäisi kirjastocrate:a: se voi käyttää vain julkista API:a. Tämä auttaa suunnittelemaan hyvän API:n; et ole vain kirjoittaja, vaan myös asiakas!
>
> [Luvussa 12][ch12]<!-- ignore --> havainnollistamme tätä organisointikäytäntöä komentoriviohjelmalla, joka sisältää sekä binääri- että kirjastocrate:n.

### Suhteellisten polkujen aloittaminen `super`:lla

Voimme rakentaa suhteellisia polkuja, jotka alkavat emomoduulista nykyisen moduulin tai crate-juuren sijaan käyttämällä `super`-avainsanaa polun alussa. Tämä on kuin tiedostojärjestelmän polun aloittaminen `..`-syntaksilla, joka tarkoittaa siirtymistä emohakemistoon. `super`:n käyttäminen sallii meidän viitata kohteeseen, jonka tiedämme olevan emomoduulissa, mikä voi helpottaa moduulipuun uudelleenjärjestelyä, kun moduuli on läheisesti liittynyt emomoduuliin, mutta emomoduuli saatetaan joskus siirtää muualle moduulipuussa.

Harkitse listauksen 7-8 koodia, joka mallintaa tilannetta, jossa keittiömestari korjaa virheellisen tilauksen ja tuo sen henkilökohtaisesti asiakkaalle. `back_of_house`-moduulissa määritelty `fix_incorrect_order`-funktio kutsuu emomoduulissa määriteltyä `deliver_order`-funktiota määrittämällä polun `deliver_order`-funktioon aloittaen `super`:lla.

<Listing number="7-8" file-name="src/lib.rs" caption="Funktion kutsuminen suhteellisella polulla, joka alkaa `super`:lla">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-08/src/lib.rs}}
```

</Listing>

`fix_incorrect_order`-funktio on `back_of_house`-moduulissa, joten voimme käyttää `super`:a siirtyäksemme `back_of_house`-moduulin emomoduuliin, joka tässä tapauksessa on `crate`, juuri. Sieltä etsimme `deliver_order`-funktiota ja löydämme sen. Onnistui! Uskomme, että `back_of_house`-moduuli ja `deliver_order`-funktio pysyvät todennäköisesti samassa suhteessa toisiinsa ja siirtyvät yhdessä, jos päättäisimme järjestää crate:n moduulipuun uudelleen. Siksi käytimme `super`:a, jotta meillä olisi vähemmän paikkoja päivitettäväksi tulevaisuudessa, jos tämä koodi siirretään eri moduuliin.

### Structien ja enumien tekeminen julkisiksi

Voimme myös käyttää `pub`:ia structien ja enumien merkitsemiseen julkisiksi, mutta `pub`:n käytössä structien ja enumien kanssa on muutamia lisätietoja. Jos käytämme `pub`:ia struct-määrittelyn edessä, teemme structista julkisen, mutta structin kentät ovat edelleen yksityisiä. Voimme tehdä jokaisesta kentästä julkisen tai yksityisen tapauskohtaisesti. Listauksessa 7-9 olemme määritelleet julkisen `back_of_house::Breakfast`-structin, jossa on julkinen `toast`-kenttä mutta yksityinen `seasonal_fruit`-kenttä. Tämä mallintaa ravintolatilannetta, jossa asiakas voi valita aterian kanssa tulevan leivän tyypin, mutta keittiömestari päättää, mikä hedelmä seuraa ateriaa sen perusteella, mikä on sesongissa ja varastossa. Saatavilla olevat hedelmät vaihtuvat nopeasti, joten asiakkaat eivät voi valita hedelmää tai edes nähdä, minkä hedelmän he saavat.

<Listing number="7-9" file-name="src/lib.rs" caption="Struct, jossa on joitakin julkisia ja joitakin yksityisiä kenttiä">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-09/src/lib.rs}}
```

</Listing>

Koska `back_of_house::Breakfast`-structin `toast`-kenttä on julkinen, funktiossa `eat_at_restaurant` voimme kirjoittaa ja lukea `toast`-kenttää käyttämällä pistesyntaksia. Huomaa, ettemme voi käyttää `seasonal_fruit`-kenttää funktiossa `eat_at_restaurant`, koska `seasonal_fruit` on yksityinen. Kokeile poistaa kommentti riviltä, joka muuttaa `seasonal_fruit`-kentän arvoa, nähdäksesi minkä virheen saat!

Huomaa myös, että koska `back_of_house::Breakfast`-structilla on yksityinen kenttä, structin on tarjottava julkinen assosioitu funktio, joka luo `Breakfast`-instanssin (olemme nimenneet sen tässä `summer`). Jos `Breakfast`-structilla ei olisi tällaista funktiota, emme voisi luoda `Breakfast`-instanssia funktiossa `eat_at_restaurant`, koska emme voisi asettaa yksityisen `seasonal_fruit`-kentän arvoa funktiossa `eat_at_restaurant`.

Sitä vastoin, jos teemme enumista julkisen, kaikista sen varianteista tulee julkisia. Tarvitsemme vain `pub`-avainsanan `enum`-avainsanan edessä, kuten listauksessa 7-10.

<Listing number="7-10" file-name="src/lib.rs" caption="Enumin määrittely julkiseksi tekee kaikista sen varianteista julkisia.">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-10/src/lib.rs}}
```

</Listing>

Koska teimme `Appetizer`-enumista julkisen, voimme käyttää `Soup`- ja `Salad`-variantteja funktiossa `eat_at_restaurant`.

Enumit eivät ole kovin hyödyllisiä, elleivät niiden variantit ole julkisia; olisi ärsyttävää joutua merkitsemään kaikki enum-variantit `pub`:lla joka tapauksessa, joten enum-varianttien oletus on olla julkisia. Structit ovat usein hyödyllisiä ilman, että niiden kentät olisivat julkisia, joten struct-kentät noudattavat yleistä sääntöä, että kaikki on oletuksena yksityistä, ellei niitä ole merkitty `pub`:lla.

On vielä yksi tilanne, jossa `pub`:ia käytetään, jota emme ole käsitelleet, ja se on viimeinen moduulijärjestelmämme ominaisuus: `use`-avainsana. Käsittelemme `use`:a ensin erikseen, ja sitten näytämme, miten `pub` ja `use` yhdistetään.

[pub]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html#exposing-paths-with-the-pub-keyword
[api-guidelines]: https://rust-lang.github.io/api-guidelines/
[ch12]: ch12-00-an-io-project.html
