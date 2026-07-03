<!-- Old headings. Do not remove or links may break. -->

<a id="defining-modules-to-control-scope-and-privacy"></a>

## Laajuuden ja yksityisyyden hallinta moduuleilla

Tässä osiossa käsittelemme moduuleja ja moduulijärjestelmän muita osia, nimittäin _polkuja_, joiden avulla voit nimetä kohteita; `use`-avainsanaa, joka tuo polun laajuuteen; ja `pub`-avainsanaa, jolla kohteet tehdään julkisiksi. Käsittelemme myös `as`-avainsanaa, ulkoisia paketteja ja glob-operaattoria.

### Moduulien pikaopas

Ennen kuin siirrymme moduulien ja polkujen yksityiskohtiin, tässä on nopea viite siitä, miten moduulit, polut, `use`-avainsana ja `pub`-avainsana toimivat kääntäjässä ja miten useimmat kehittäjät järjestävät koodinsa. Käymme läpi esimerkkejä jokaisesta näistä säännöistä koko luvun ajan, mutta tämä on hyvä paikka muistuttaa itseään moduulien toiminnasta.

- **Aloita crate-juuresta**: Kun crate käännetään, kääntäjä etsii ensin crate-juuritiedostosta (yleensä _src/lib.rs_ kirjastocrate:lle ja _src/main.rs_ binääricrate:lle) käännettävää koodia.
- **Moduulien määrittely**: Crate-juuritiedostossa voit määritellä uusia moduuleja; oletetaan, että määrittelet ”garden”-moduulin komennolla `mod garden;`. Kääntäjä etsii moduulin koodia näistä paikoista:
  - Inline, aaltosulkeissa, jotka korvaavat `mod garden` -lauseen lopussa olevan puolipisteen
  - Tiedostosta _src/garden.rs_
  - Tiedostosta _src/garden/mod.rs_
- **Alimoduulien määrittely**: Missä tahansa tiedostossa paitsi crate-juuressa voit määritellä alimoduuuleja. Esimerkiksi voit määritellä `mod vegetables;` tiedostossa _src/garden.rs_. Kääntäjä etsii alimoduuulin koodia emomoduulin nimisestä hakemistosta näistä paikoista:
  - Inline, suoraan `mod vegetables` -lauseen jälkeen aaltosulkeissa puolipisteen sijaan
  - Tiedostosta _src/garden/vegetables.rs_
  - Tiedostosta _src/garden/vegetables/mod.rs_
- **Polut moduulien koodiin**: Kun moduuli on osa crate:asi, voit viitata kyseisen moduulin koodiin mistä tahansa muualta samassa crate:ssa, kunhan yksityisyyssäännöt sen sallivat, käyttämällä polkua koodiin. Esimerkiksi `Asparagus`-tyyppi garden-moduulin vegetables-alimoduuulissa löytyy polusta `crate::garden::vegetables::Asparagus`.
- **Yksityinen vs. julkinen**: Moduulin sisällä oleva koodi on oletuksena yksityistä emomoduuleilleen. Tehdäksesi moduulin julkiseksi, määrittele se komennolla `pub mod` `mod`-komennon sijaan. Tehdäksesi julkisen moduulin kohteet myös julkisiksi, käytä `pub`-avainsanaa niiden määrittelyjen edessä.
- **`use`-avainsana**: Laajuudessa `use`-avainsana luo oikoteitä kohteille vähentääkseen pitkien polkujen toistoa. Missä tahansa laajuudessa, jossa voidaan viitata `crate::garden::vegetables::Asparagus`-polkuun, voit luoda oikotien komennolla `use crate::garden::vegetables::Asparagus;`, ja sen jälkeen sinun tarvitsee vain kirjoittaa `Asparagus` käyttääksesi kyseistä tyyppiä laajuudessa.

Tässä luomme binääricrate:n nimeltä `backyard`, joka havainnollistaa näitä sääntöjä. Crate:n hakemisto, joka myös on nimeltään _backyard_, sisältää nämä tiedostot ja hakemistot:

```text
backyard
├── Cargo.lock
├── Cargo.toml
└── src
    ├── garden
    │   └── vegetables.rs
    ├── garden.rs
    └── main.rs
```

Tässä tapauksessa crate-juuritiedosto on _src/main.rs_, ja se sisältää:

<Listing file-name="src/main.rs">

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/main.rs}}
```

</Listing>

`pub mod garden;` -rivi kertoo kääntäjälle sisällyttää koodi, jonka se löytää tiedostosta _src/garden.rs_, joka on:

<Listing file-name="src/garden.rs">

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/garden.rs}}
```

</Listing>

Tässä `pub mod vegetables;` tarkoittaa, että koodi tiedostosta _src/garden/vegetables.rs_ sisällytetään myös. Kyseinen koodi on:

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/garden/vegetables.rs}}
```

Siirrytään nyt näiden sääntöjen yksityiskohtiin ja havainnollistetaan niitä käytännössä!

### Liittyvän koodin ryhmittely moduuleihin

_Moduulit_ antavat meille mahdollisuuden järjestää koodia crate:n sisällä luettavuuden ja helpon uudelleenkäytön vuoksi. Moduulit antavat myös hallita kohteiden _yksityisyyttä_, koska moduulin sisällä oleva koodi on oletuksena yksityistä. Yksityiset kohteet ovat sisäisiä toteutustietoja, jotka eivät ole ulkopuolisen käytön saatavilla. Voimme valita tehdä moduulit ja niiden sisällä olevat kohteet julkisiksi, mikä paljastaa ne ulkoisen koodin käytettäväksi ja riippuvuudeksi.

Esimerkkinä kirjoitetaan kirjastocrate, joka tarjoaa ravintolan toiminnallisuuden. Määrittelemme funktioiden signatuurit, mutta jätämme niiden rungot tyhjiksi keskittyäksemme koodin organisointiin ravintolan toteutuksen sijaan.

Ravintola-alalla ravintolan osia kutsutaan etu- ja takaosaksi. _Etuosassa_ asiakkaat ovat; se kattaa paikat, joissa emännät istuttavat asiakkaat, tarjoilijat ottavat tilaukset ja maksut, ja baarimestarit valmistavat juomia. _Takaosassa_ keitit ja kokit työskentelevät keittiössä, tiskinpesijät siivoavat, ja esimiehet tekevät hallinnollista työtä.

Rakentaaksemme crate:amme tällä tavalla voimme järjestää sen funktiot sisäkkäisiin moduuleihin. Luo uusi kirjasto nimeltä `restaurant` suorittamalla `cargo new restaurant --lib`. Syötä sitten listauksen 7-1 koodi tiedostoon _src/lib.rs_ määritelläksesi moduuleja ja funktiosignatuureja; tämä koodi on etuosan osio.

<Listing number="7-1" file-name="src/lib.rs" caption="`front_of_house`-moduuli, joka sisältää muita moduuleja, jotka sisältävät funktioita">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-01/src/lib.rs}}
```

</Listing>

Määrittelemme moduulin `mod`-avainsanalla, jota seuraa moduulin nimi (tässä tapauksessa `front_of_house`). Moduulin runko menee sitten aaltosulkeiden sisään. Moduulien sisällä voimme sijoittaa muita moduuleja, kuten tässä tapauksessa moduulit `hosting` ja `serving`. Moduulit voivat myös sisältää määrittelyjä muille kohteille, kuten structeille, enumeille, vakioille, trait:eille ja kuten listauksessa 7-1 funktioille.

Moduuleja käyttämällä voimme ryhmitellä liittyvät määrittelyt yhteen ja nimetä, miksi ne liittyvät toisiinsa. Tätä koodia käyttävät ohjelmoijat voivat navigoida koodissa ryhmien perusteella sen sijaan, että heidän pitäisi lukea läpi kaikki määrittelyt, mikä helpottaa heille relevanttien määrittelyjen löytämistä. Tähän koodiin uutta toiminnallisuutta lisäävät ohjelmoijat tietävät, mihin sijoittaa koodin pitääkseen ohjelman järjestyksessä.

Aiemmin mainitsimme, että _src/main.rs_ ja _src/lib.rs_ kutsutaan _crate-juuriksi_. Niiden nimen syy on se, että kummankin näistä kahdesta tiedostosta sisältö muodostaa moduulin nimeltä `crate` crate:n moduulirakenteen juuressa, jota kutsutaan _moduulipuuksi_.

Listaus 7-2 näyttää moduulipuun listauksen 7-1 rakenteelle.

<Listing number="7-2" caption="Moduulipuu listauksen 7-1 koodille">

```text
crate
 └── front_of_house
     ├── hosting
     │   ├── add_to_waitlist
     │   └── seat_at_table
     └── serving
         ├── take_order
         ├── serve_order
         └── take_payment
```

</Listing>

Tämä puu näyttää, miten jotkin moduulit sisäkkäistyvät muihin moduuleihin; esimerkiksi `hosting` sisäkkäistyy `front_of_house`-moduuliin. Puu näyttää myös, että jotkin moduulit ovat _sisaruksia_, eli ne on määritelty samassa moduulissa; `hosting` ja `serving` ovat sisaruksia, jotka on määritelty `front_of_house`-moduulissa. Jos moduuli A on moduulin B sisällä, sanomme, että moduuli A on moduulin B _lapsi_ ja moduuli B on moduulin A _vanhempi_. Huomaa, että koko moduulipuu on juurrutettu implisiittiseen moduuliin nimeltä `crate`.

Moduulipuu saattaa muistuttaa tietokoneesi tiedostojärjestelmän hakemistopuuta; tämä on erittäin osuva vertaus! Aivan kuten hakemistot tiedostojärjestelmässä, käytät moduuleja koodisi organisointiin. Ja aivan kuten tiedostot hakemistossa, tarvitsemme tavan löytää moduulimme.
