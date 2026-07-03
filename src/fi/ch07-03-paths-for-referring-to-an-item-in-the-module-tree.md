## Polut kohteen viittaamiseen moduulipuussa

Näyttääksemme Rustille, mistä kohde löytyy moduulipuussa, käytämme polkua samalla tavalla kuin käytämme polkua tiedostojärjestelmässä navigoidessamme. Kutsuaksemme funktiota meidän täytyy tietää sen polku.

Polulla voi olla kaksi muotoa:

- _Absoluuttinen polku_ on täysi polku, joka alkaa crate-juuresta; ulkoisen craten koodille absoluuttinen polku alkaa craten nimellä, ja nykyisen craten koodille se alkaa literaalilla `crate`.
- _Suhteellinen polku_ alkaa nykyisestä moduulista ja käyttää `self`:ää, `super`:ia tai tunnistetta nykyisessä moduulissa.

Molempia absoluuttisia ja suhteellisia polkuja seuraa yksi tai useampi tunniste, jotka on erotettu kaksoispisteillä (`::`).

Palatkaamme Listaukseen 7-1 ja sanokaamme, että haluamme kutsua `add_to_waitlist`-funktiota. Tämä on sama kuin kysyisi: mikä on `add_to_waitlist`-funktion polku? Listausta 7-3 sisältää Listauksen 7-1, josta on poistettu joitakin moduuleja ja funktioita.

Näytämme kaksi tapaa kutsua `add_to_waitlist`-funktiota uudesta funktiosta, `eat_at_restaurant`, joka on määritelty crate-juuressa. Nämä polut ovat oikein, mutta on jäljellä toinen ongelma, joka estää tämän esimerkin kääntymisen sellaisenaan. Selitämme miksi hetken kuluttua.

`eat_at_restaurant`-funktio on osa kirjastocratemme julkista API:a, joten merkitsemme sen `pub`-avainsanalla. [”Polkujen paljastaminen `pub`-avainsanalla”][pub]<!-- ignore --> -osiossa käsittelemme `pub`:ia tarkemmin.

<Listing number="7-3" file-name="src/lib.rs" caption="`add_to_waitlist`-funktion kutsuminen absoluuttisia ja suhteellisia polkuja käyttäen">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-03/src/lib.rs}}
```

</Listing>

Ensimmäisellä kerralla kun kutsumme `add_to_waitlist`-funktiota `eat_at_restaurant`:ssa, käytämme absoluuttista polkua. `add_to_waitlist`-funktio on määritelty samassa cratessa kuin `eat_at_restaurant`, mikä tarkoittaa, että voimme käyttää `crate`-avainsanaa aloittaaksemme absoluuttisen polun. Sisällytämme sitten jokaisen peräkkäisen moduulin, kunnes pääsemme `add_to_waitlist`:iin. Voit kuvitella tiedostojärjestelmän samalla rakenteella: määrittäisimme polun `/front_of_house/hosting/add_to_waitlist` suorittaaksemme `add_to_waitlist`-ohjelman; `crate`-nimen käyttö aloittaaksemme crate-juuresta on kuin `/`:n käyttö aloittaaksemme tiedostojärjestelmän juuresta komentorivilläsi.

Toisella kerralla kun kutsumme `add_to_waitlist`:ia `eat_at_restaurant`:ssa, käytämme suhteellista polkua. Polku alkaa `front_of_house`:sta, moduulin nimestä, joka on määritelty samalla tasolla moduulipuussa kuin `eat_at_restaurant`. Tässä tiedostojärjestelmän vastine olisi polun `front_of_house/hosting/add_to_waitlist` käyttö. Moduulin nimellä aloittaminen tarkoittaa, että polku on suhteellinen.

Valinta suhteellisen tai absoluuttisen polun käytöstä on päätös, jonka teet projektisi perusteella, ja se riippuu siitä, siirrätkö todennäköisemmin kohteen määrittelykoodia erillään vai yhdessä koodin kanssa, joka käyttää kohdetta. Esimerkiksi, jos siirtäisimme `front_of_house`-moduulin ja `eat_at_restaurant`-funktion moduuliin nimeltä `customer_experience`, meidän täytyisi päivittää absoluuttinen polku `add_to_waitlist`:iin, mutta suhteellinen polku olisi edelleen kelvollinen. Jos kuitenkin siirtäisimme `eat_at_restaurant`-funktion erillään moduuliin nimeltä `dining`, absoluuttinen polku `add_to_waitlist`-kutsuun pysyisi samana, mutta suhteellinen polku täytyisi päivittää. Yleinen mieltymyksemme on määrittää absoluuttiset polut, koska on todennäköisempää, että haluamme siirtää koodimäärittelyjä ja kohteen kutsuja toisistaan riippumatta.

Yritetään kääntää Listausta 7-3 ja selvitetään, miksi se ei vielä käänny! Virheet, jotka saamme, on esitetty Listauksessa 7-4.

<Listing number="7-4" caption="Kääntäjävirheet Listauksen 7-3 koodin kääntämisestä">

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-03/output.txt}}
```

</Listing>

Virheilmoitukset sanovat, että moduuli `hosting` on yksityinen. Toisin sanoen meillä on oikeat polut `hosting`-moduulille ja `add_to_waitlist`-funktiolle, mutta Rust ei anna meidän käyttää niitä, koska sillä ei ole pääsyä yksityisiin osiin. Rustissa kaikki kohteet (funktiot, metodit, rakenteet, enumit, moduulit ja vakiot) ovat oletuksena yksityisiä emomoduuleilleen. Jos haluat tehdä kohteesta kuten funktiosta tai rakenteesta yksityisen, laitat sen moduuliin.

Emomoduulin kohteet eivät voi käyttää lapsimoduulien yksityisiä kohteita, mutta lapsimoduulien kohteet voivat käyttää esi-isämoduuliensa kohteita. Tämä johtuu siitä, että lapsimoduulit käärivät ja piilottavat toteutuksensa yksityiskohdat, mutta lapsimoduulit näkevät kontekstin, jossa ne on määritelty. Jatkaaksemme metaforaamme, ajattele yksityisyyssääntöjä kuin ravintolan takaosastoa: siellä tapahtuva on yksityistä ravintolan asiakkaille, mutta toimistopäälliköt näkevät ja voivat tehdä kaiken ravintolassa, jota he operoivat.

Rust valitsi moduulijärjestelmän toimivan näin, jotta sisäisten toteutuksen yksityiskohtien piilottaminen on oletus. Näin tiedät, mitä sisäisen koodin osia voit muuttaa rikkomatta ulkoista koodia. Rust antaa kuitenkin mahdollisuuden paljastaa lapsimoduulien koodin sisäisiä osia ulkoisille esi-isämoduuleille käyttämällä `pub`-avainsanaa tehdäksesi kohteen julkiseksi.

### Polkujen paljastaminen `pub`-avainsanalla

Palataan Listauksen 7-4 virheeseen, joka kertoi, että `hosting`-moduuli on yksityinen. Haluamme, että emomoduulin `eat_at_restaurant`-funktiolla on pääsy `add_to_waitlist`-funktioon lapsimoduulissa, joten merkitsemme `hosting`-moduulin `pub`-avainsanalla, kuten Listauksessa 7-5 on esitetty.

<Listing number="7-5" file-name="src/lib.rs" caption="`hosting`-moduulin julistaminen `pub`:iksi sen käyttämiseksi `eat_at_restaurant`:sta">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-05/src/lib.rs:here}}
```

</Listing>

Valitettavasti Listauksen 7-5 koodi tuottaa edelleen kääntäjävirheitä, kuten Listauksessa 7-6 on esitetty.

<Listing number="7-6" caption="Kääntäjävirheet Listauksen 7-5 koodin kääntämisestä">

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-05/output.txt}}
```

</Listing>

Mitä tapahtui? `pub`-avainsanan lisääminen `mod hosting`:n eteen tekee moduulista julkisen. Tämän muutoksen jälkeen, jos pääsemme `front_of_house`:iin, pääsemme `hosting`:iin. Mutta `hosting`:in _sisältö_ on edelleen yksityistä; moduulin tekeminen julkiseksi ei tee sen sisällöstä julkista. `pub`-avainsana moduulissa antaa vain sen esi-isämoduulien koodin viitata siihen, ei käyttää sen sisäistä koodia. Koska moduulit ovat säiliöitä, emme voi tehdä paljon pelkällä moduulin tekemisellä julkiseksi; meidän täytyy mennä pidemmälle ja valita tehdä yhdestä tai useammasta moduulin sisällä olevasta kohteesta julkisia.

Listauksen 7-6 virheet sanovat, että `add_to_waitlist`-funktio on yksityinen. Yksityisyyssäännöt pätevät rakenteisiin, enumeihin, funktioihin ja metodeihin sekä moduuleihin.

Tehdään myös `add_to_waitlist`-funktiosta julkinen lisäämällä `pub`-avainsana sen määrittelyn eteen, kuten Listauksessa 7-7.

<Listing number="7-7" file-name="src/lib.rs" caption="`pub`-avainsanan lisääminen `mod hosting`:iin ja `fn add_to_waitlist`:iin antaa meille mahdollisuuden kutsua funktiota `eat_at_restaurant`:sta">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-07/src/lib.rs:here}}
```

</Listing>

Nyt koodi kääntyy! Nähdäksemme, miksi `pub`-avainsanan lisääminen antaa meidän käyttää näitä polkuja `eat_at_restaurant`:ssa yksityisyyssääntöjen suhteen, katsotaan absoluuttista ja suhteellista polkua.

Absoluuttisessa polussa aloitamme `crate`:sta, cratemme moduulipuun juuresta. `front_of_house`-moduuli on määritelty crate-juuressa. Vaikka `front_of_house` ei ole julkinen, koska `eat_at_restaurant`-funktio on määritelty samassa moduulissa kuin `front_of_house` (eli `eat_at_restaurant` ja `front_of_house` ovat sisaruksia), voimme viitata `front_of_house`:iin `eat_at_restaurant`:sta. Seuraavaksi on `hosting`-moduuli, joka on merkitty `pub`:illa. Pääsemme `hosting`:in emomoduuliin, joten pääsemme `hosting`:iin. Lopuksi `add_to_waitlist`-funktio on merkitty `pub`:illa ja pääsemme sen emomoduuliin, joten tämä funktiokutsu toimii!

Suhteellisessa polussa logiikka on sama kuin absoluuttisessa polussa paitsi ensimmäinen askel: sen sijaan, että aloittaisimme crate-juuresta, polku alkaa `front_of_house`:sta. `front_of_house`-moduuli on määritelty samassa moduulissa kuin `eat_at_restaurant`, joten suhteellinen polku, joka alkaa moduulista, jossa `eat_at_restaurant` on määritelty, toimii. Sitten, koska `hosting` ja `add_to_waitlist` on merkitty `pub`:illa, loppu polusta toimii, ja tämä funktiokutsu on kelvollinen!

Jos aiot jakaa kirjastocratesi, jotta muut projektit voivat käyttää koodiasi, julkinen API on sopimuksesi craten käyttäjien kanssa, joka määrittää, miten he voivat olla vuorovaikutuksessa koodisi kanssa. Julkisen API:n muutosten hallintaan liittyy monia näkökohtia, jotta craten käyttäminen olisi helpompaa. Nämä näkökohdat ovat tämän kirjan laajuuden ulkopuolella; jos olet kiinnostunut tästä aiheesta, katso [The Rust API Guidelines][api-guidelines].

> #### Parhaat käytännöt paketeille, joissa on binääri ja kirjasto
>
> Mainitsimme, että paketti voi sisältää sekä _src/main.rs_-binääricrate-juuren että _src/lib.rs_-kirjastocrate-juuren, ja molemmilla crateilla on oletuksena paketin nimi. Tyypillisesti paketit, joissa on tämä malli sisältäen sekä kirjasto- että binääricraten, sisältävät binääricratessa vain tarpeeksi koodia käynnistääkseen suoritettavan, joka kutsuu kirjastocraten koodia. Tämä antaa muiden projektien hyötyä suurimmasta osasta paketin tarjoamaa toiminnallisuutta, koska kirjastocraten koodia voidaan jakaa.
>
> Moduulipuu pitäisi määritellä _src/lib.rs_:ssä. Sitten mitkä tahansa julkiset kohteet voidaan käyttää binääricratessa aloittamalla polut paketin nimellä. Binääricratesta tulee kirjastocraten käyttäjä aivan kuten täysin ulkoinen crate käyttäisi kirjastocratetta: se voi käyttää vain julkista API:a. Tämä auttaa sinua suunnittelemaan hyvän API:n; et ole vain tekijä, olet myös asiakas!
>
> Luvussa 12<!-- ignore --> demonstroimme tätä organisointikäytäntöä komentorivi-ohjelmalla, joka sisältää sekä binääri- että kirjastocraten.

### Suhteellisten polkujen aloittaminen `super`:lla

Voimme rakentaa suhteellisia polkuja, jotka alkavat emomoduulista nykyisen moduulin tai crate-juuren sijaan, käyttämällä `super`:ia polun alussa. Tämä on kuin tiedostojärjestelmäpolun aloittaminen `..`-syntaksilla. `super`:n käyttö antaa meille mahdollisuuden viitata kohteeseen, jonka tiedämme olevan emomoduulissa, mikä voi helpottaa moduulipuun uudelleenjärjestelyä, kun moduuli liittyy läheisesti emomoduuliin, mutta emomoduuli saatetaan siirtää muualle moduulipuussa jonain päivänä.

Harkitse Listauksen 7-8 koodia, joka mallintaa tilannetta, jossa kokki korjaa virheellisen tilauksen ja tuo sen henkilökohtaisesti asiakkaalle. `back_of_house`-moduulissa määritelty `fix_incorrect_order`-funktio kutsuu emomoduulissa määriteltyä `deliver_order`-funktiota määrittämällä polun `deliver_order`:iin aloittaen `super`:lla.

<Listing number="7-8" file-name="src/lib.rs" caption="Funktion kutsuminen suhteellisella polulla, joka alkaa `super`:lla">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-08/src/lib.rs}}
```

</Listing>

`fix_incorrect_order`-funktio on `back_of_house`-moduulissa, joten voimme käyttää `super`:ia siirtyäksemme `back_of_house`:n emomoduuliin, joka tässä tapauksessa on `crate`, juuri. Sieltä etsimme `deliver_order`:ia ja löydämme sen. Onnistui! Uskomme, että `back_of_house`-moduuli ja `deliver_order`-funktio pysyvät todennäköisesti samassa suhteessa toisiinsa ja siirretään yhdessä, jos päätämme järjestellä craten moduulipuuta uudelleen. Siksi käytimme `super`:ia, jotta meillä olisi vähemmän paikkoja päivittää koodia tulevaisuudessa, jos tämä koodi siirretään eri moduuliin.

### Rakenteiden ja enumien tekeminen julkisiksi

Voimme myös käyttää `pub`:ia merkitsemään rakenteet ja enumit julkisiksi, mutta `pub`:in käytössä rakenteiden ja enumien kanssa on muutamia ylimääräisiä yksityiskohtia. Jos käytämme `pub`:ia ennen rakennemäärittelyä, teemme rakenteesta julkisen, mutta rakenteen kentät ovat edelleen yksityisiä. Voimme tehdä jokaisesta kentästä julkisen tai ei tapauskohtaisesti. Listauksessa 7-9 olemme määritelleet julkisen `back_of_house::Breakfast`-rakenteen julkisella `toast`-kentällä mutta yksityisellä `seasonal_fruit`-kentällä. Tämä mallintaa ravintolatilannetta, jossa asiakas voi valita aterian kanssa tulevan leivän tyypin, mutta kokki päättää, mikä hedelmä seuraa ateriaa sen perusteella, mikä on sesongissa ja varastossa. Saatavilla olevat hedelmät vaihtuvat nopeasti, joten asiakkaat eivät voi valita hedelmää tai edes nähdä, minkä hedelmän he saavat.

<Listing number="7-9" file-name="src/lib.rs" caption="Rakenne, jossa on joitakin julkisia ja joitakin yksityisiä kenttiä">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-09/src/lib.rs}}
```

</Listing>

Koska `toast`-kenttä `back_of_house::Breakfast`-rakenteessa on julkinen, `eat_at_restaurant`:ssa voimme kirjoittaa ja lukea `toast`-kenttää käyttämällä pistesyntaksia. Huomaa, ettemme voi käyttää `seasonal_fruit`-kenttää `eat_at_restaurant`:ssa, koska `seasonal_fruit` on yksityinen. Kokeile poistaa kommentti riviltä, joka muokkaa `seasonal_fruit`-kentän arvoa, nähdäksesi minkä virheen saat!

Huomaa myös, että koska `back_of_house::Breakfast`:lla on yksityinen kenttä, rakenteen täytyy tarjota julkinen liittyvä funktio, joka rakentaa `Breakfast`-instanssin (olemme nimenneet sen tässä `summer`:iksi). Jos `Breakfast`:lla ei olisi tällaista funktiota, emme voisi luoda `Breakfast`-instanssia `eat_at_restaurant`:ssa, koska emme voisi asettaa yksityisen `seasonal_fruit`-kentän arvoa `eat_at_restaurant`:ssa.

Sitä vastoin, jos teemme enumista julkisen, kaikki sen variantit ovat sitten julkisia. Tarvitsemme vain `pub`:in `enum`-avainsanan eteen, kuten Listauksessa 7-10 on esitetty.

<Listing number="7-10" file-name="src/lib.rs" caption="Enumin merkitseminen julkiseksi tekee kaikista sen varianteista julkisia.">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-10/src/lib.rs}}
```

</Listing>

Koska teimme `Appetizer`-enumista julkisen, voimme käyttää `Soup`- ja `Salad`-variantteja `eat_at_restaurant`:ssa.

Enumit eivät ole kovin hyödyllisiä, elleivät niiden variantit ole julkisia; olisi ärsyttävää joutua merkitsemään kaikki enum-variantit `pub`:illa joka tapauksessa, joten enum-varianttien oletus on olla julkisia. Rakenteet ovat usein hyödyllisiä ilman, että niiden kentät ovat julkisia, joten rakennekentät noudattavat yleistä sääntöä, että kaikki on oletuksena yksityistä, ellei niitä ole merkitty `pub`:illa.

On vielä yksi tilanne, jossa `pub` on mukana, jota emme ole käsitelleet, ja se on viimeinen moduulijärjestelmämme ominaisuus: `use`-avainsana. Käsittelemme `use`:n erikseen ensin, ja sitten näytämme, miten yhdistää `pub` ja `use`.

[pub]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html#exposing-paths-with-the-pub-keyword
[api-guidelines]: https://rust-lang.github.io/api-guidelines/
[ch12]: ch12-00-an-io-project.html
