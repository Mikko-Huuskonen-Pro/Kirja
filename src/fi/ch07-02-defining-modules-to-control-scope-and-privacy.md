## Moduulien määrittäminen laajuuden ja yksityisyyden hallitsemiseksi

Tässä osiossa käsittelemme moduuleja ja muita moduulijärjestelmän osia,
eli _polkuja_ (paths), joiden avulla voit nimetä kohteita; `use`-avainsanaa, joka
tuo polun näkyvyysalueeseen; ja `pub`-avainsanaa, joka tekee kohteet julkisiksi.
Käsittelemme myös `as`-avainsanaa, ulkoisia paketteja ja glob-operaattoria.

### Moduulien pikaopas

Ennen kuin siirrymme moduulien ja polkujen yksityiskohtiin, tässä on nopea
viite siitä, miten moduulit, polut, `use`-avainsana ja `pub`-avainsana toimivat
kääntäjässä ja miten useimmat kehittäjät järjestävät koodinsa. Käymme läpi
esimerkkejä näistä säännöistä tämän luvun aikana, mutta tämä on hyvä paikka
viitata muistutuksena siitä, miten moduulit toimivat.

- **Aloita crate-juuresta**: Kun kääntäjä kääntää craten, se etsii ensin
  koodia kääntääkseen crate-juuritiedostosta (yleensä _src/lib.rs_ kirjastocratelle tai
  _src/main.rs_ binääricratelle).
- **Moduulien määrittäminen**: Crate-juuritiedostossa voit määrittää uusia moduuleja;
  esimerkiksi voit määrittää "garden"-moduulin komennolla `mod garden;`. Kääntäjä etsii
  moduulin koodia näistä paikoista:
  - Inline, aaltosulkeiden sisällä, jotka korvaavat `mod garden`-komennon
    jälkeisen puolipisteen
  - Tiedostossa _src/garden.rs_
  - Tiedostossa _src/garden/mod.rs_
- **Alimoduulien määrittäminen**: Missä tahansa muussa tiedostossa kuin crate-juurissa voit
  määrittää alimoduuleja. Esimerkiksi voit määrittää `mod vegetables;` tiedostossa
  _src/garden.rs_. Kääntäjä etsii alimoduulin koodia vanhemman moduulin nimeämästä
  hakemistosta näistä paikoista:
  - Inline, suoraan `mod vegetables`-komennon jälkeen, aaltosulkeiden sisällä
    puolipisteen sijaan
  - Tiedostossa _src/garden/vegetables.rs_
  - Tiedostossa _src/garden/vegetables/mod.rs_
- **Polut moduulien koodiin**: Kun moduuli on osa crateasi, voit viitata
  siinä olevaan koodiin mistä tahansa muusta paikasta samassa cratessa, niin kauan
  kuin yksityisyyssäännöt sen sallivat, käyttämällä koodin polkua. Esimerkiksi
  `Asparagus`-tyyppi puutarhan vihannemoduulissa löytyisi polusta
  `crate::garden::vegetables::Asparagus`.
- **Yksityinen vs. julkinen**: Moduulin sisällä oleva koodi on yksityistä sen
  vanhempien moduulien näkökulmasta oletusarvoisesti. Tehdäksesi moduulin julkiseksi,
  määritä se `pub mod`-komennolla `mod`-komennon sijaan. Tehdäksesi julkisen moduulin
  sisällä olevat kohteet julkisiksi, käytä `pub`-avainsanaa ennen niiden määrittelyjä.
- **`use`-avainsana**: Näkyvyysalueen sisällä `use`-avainsana luo oikoteitä
  kohteisiin vähentääkseen pitkien polkujen toistoa. Missä tahansa näkyvyysalueessa,
  joka voi viitata `crate::garden::vegetables::Asparagus`-tyyppiin, voit luoda
  oikotien komennolla `use crate::garden::vegetables::Asparagus;` ja sen jälkeen
  sinun tarvitsee vain kirjoittaa `Asparagus` käyttääksesi kyseistä tyyppiä
  näkyvyysalueessa.

Tässä luomme binääricraten nimeltä `backyard`, joka havainnollistaa näitä sääntöjä.
Craten hakemisto, myös nimeltään `backyard`, sisältää nämä tiedostot ja
hakemistot:

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

Crate-juuritiedosto on tässä tapauksessa _src/main.rs_, ja se sisältää:

<Listing file-name="src/main.rs">

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/main.rs}}
```

</Listing>

Rivi `pub mod garden;` kertoo kääntäjälle sisällyttää koodin, jonka se löytää
tiedostosta _src/garden.rs_, joka on:

<Listing file-name="src/garden.rs">

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/garden.rs}}
```

</Listing>

Tässä `pub mod vegetables;` tarkoittaa, että myös tiedoston _src/garden/vegetables.rs_
koodi sisällytetään. Tuo koodi on:

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/garden/vegetables.rs}}
```

Siirrytään nyt näiden sääntöjen yksityiskohtiin ja demonstroidaan niitä käytännössä!

### Liittyvän koodin ryhmittely moduuleihin

_Moduulit_ (Modules) antavat meille mahdollisuuden järjestää koodi craten sisällä
luettavuuden ja helpon uudelleenkäytön vuoksi. Moduulit antavat meille myös
mahdollisuuden hallita kohteiden _yksityisyyttä_ (privacy), koska moduulin sisällä
oleva koodi on yksityistä oletusarvoisesti. Yksityiset kohteet ovat sisäisiä
toteutusyksityiskohtia, jotka eivät ole saatavilla ulkoiseen käyttöön. Voimme
valita tehdä moduulit ja niiden sisällä olevat kohteet julkisiksi, mikä paljastaa
ne sallien ulkoisen koodin käyttää ja riippua niistä.

Esimerkkinä kirjoitamme kirjastocraten, joka tarjoaa ravintolan toiminnallisuuden.
Määrittelemme funktioiden allekirjoitukset, mutta jätämme niiden rungot tyhjiksi
keskittyäksemme koodin järjestelyyn ravintolan toteutuksen sijaan.

Ravintola-alalla joitakin ravintolan osia kutsutaan _etualueeksi_ (front of house)
ja toisia _takapihoiksi_ (back of house). Etualue on siellä, missä asiakkaat ovat;
tämä kattaa paikat, joissa isännät istuttavat asiakkaat, tarjoilijat ottavat
tilauksia ja maksuja, ja baarimikot tekevät juomia. Takapihoilla kokit ja keittäjät
työskentelevät keittiössä, tiskarit siivoavat, ja johtajat tekevät hallinnollista työtä.

Järjestääksemme craten tällä tavalla, voimme järjestää sen funktiot sisäkkäisiin
moduuleihin. Luo uusi kirjasto nimeltä `restaurant` suorittamalla `cargo new
restaurant --lib`. Syötä sitten koodi Listauksesta 7-1 tiedostoon _src/lib.rs_
määrittääksesi joitakin moduuleja ja funktioiden allekirjoituksia; tämä koodi on
etualueen osio.

<Listing number="7-1" file-name="src/lib.rs" caption="`front_of_house`-moduuli, joka sisältää muita moduuleja, jotka puolestaan sisältävät funktioita">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-01/src/lib.rs}}
```

</Listing>

Määrittelemme moduulin `mod`-avainsanalla, jota seuraa moduulin nimi
(tässä tapauksessa `front_of_house`). Moduulin runko menee sitten aaltosulkeiden
sisään. Moduulien sisällä voimme sijoittaa muita moduuleja, kuten tässä tapauksessa
moduulit `hosting` ja `serving`. Moduulit voivat myös sisältää määrittelyjä muille
kohteille, kuten rakenteille (structs), luettelotyypeille (enums), vakioille,
traiteille ja—kuten Listauksessa 7-1—funktioille.

Käyttämällä moduuleja voimme ryhmitellä liittyvät määrittelyt yhteen ja nimetä,
miksi ne liittyvät toisiinsa. Ohjelmoijat, jotka käyttävät tätä koodia, voivat
navigoida koodissa ryhmien perusteella sen sijaan, että heidän täytyisi lukea
läpi kaikki määrittelyt, mikä helpottaa heidän löytääkseen heille relevantit
määrittelyt. Ohjelmoijat, jotka lisäävät uutta toiminnallisuutta tähän koodiin,
tietäisivät, mihin sijoittaa koodi pitääkseen ohjelman järjestäytyneenä.

Aiemmin mainitsimme, että _src/main.rs_ ja _src/lib.rs_ kutsutaan crate-juuriksi.
Nimen syy on, että kummankin näistä kahdesta tiedostosta sisältö muodostaa moduulin
nimeltä `crate` craten moduulirakenteen juuressa, joka tunnetaan nimellä
_moduulipuu_ (module tree).

Listaus 7-2 näyttää moduulipuun Listauksen 7-1 rakenteelle.

<Listing number="7-2" caption="Moduulipuu Listauksen 7-1 koodille">

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

Tämä puu näyttää, miten jotkut moduulit pesiytyvät muiden moduulien sisään; esimerkiksi
`hosting` pesiytyy `front_of_house`-moduulin sisään. Puu näyttää myös, että jotkut
moduulit ovat _sisarusmoduuleja_ (siblings), mikä tarkoittaa, että ne on määritelty
samassa moduulissa; `hosting` ja `serving` ovat sisarusmoduuleja, jotka on määritelty
`front_of_house`-moduulin sisällä. Jos moduuli A on moduulin B sisällä, sanomme,
että moduuli A on moduulin B _lapsi_ ja että moduuli B on moduulin A _vanhempi_.
Huomaa, että koko moduulipuu on juurettu implisiittisen `crate`-nimisen moduulin alle.

Moduulipuu saattaa muistuttaa tietokoneesi tiedostojärjestelmän hakemistopuuta;
tämä on erittäin osuva vertaus! Aivan kuten hakemistot tiedostojärjestelmässä,
käytät moduuleja järjestääksesi koodisi. Ja aivan kuten tiedostot hakemistossa,
tarvitsemme tavan löytää moduulimme.
