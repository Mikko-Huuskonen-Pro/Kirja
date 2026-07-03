## Kumoavuus: voiko malli epäonnistua vastaamaan

Malleja on kahdessa muodossa: kumottavia ja kiistämättömiä. Mallit, jotka
vastaavat mitä tahansa mahdollista välitettyä arvoa, ovat _kiistämättömiä_.
Esimerkki olisi `x` lausekkeessa `let x = 5;`, koska `x` vastaa mitä tahansa
eikä siksi voi epäonnistua vastaamaan. Mallit, jotka voivat epäonnistua
vastaamaan joitakin mahdollisia arvoja, ovat _kumottavia_. Esimerkki olisi
`Some(x)` lausekkeessa `if let Some(x) = a_value`, koska jos muuttujan
`a_value` arvo on `None` eikä `Some`, malli `Some(x)` ei vastaa.

Funktioiden parametrit, `let`-lauseet ja `for`-silmukat hyväksyvät vain
kiistämättömiä malleja, koska ohjelma ei voi tehdä mitään järkevää, kun
arvot eivät vastaa. `if let`- ja `while let` -lausekkeet sekä `let...else`-
lause hyväksyvät kumottavia ja kiistämättömiä malleja, mutta kääntäjä
varoittaa kiistämättömistä malleista, koska ne on määritelmän mukaan
tarkoitettu käsittelemään mahdollista epäonnistumista: ehdollisen rakenteen
toiminta perustuu kykyyn käyttäytyä eri tavalla onnistumisen ja epäonnistumisen
mukaan.

Yleensä sinun ei tarvitse huolehtia erosta kumottavien ja kiistämättömien
mallien välillä; sinun täytyy kuitenkin tuntea kumoavuuden käsite, jotta
voit reagoida, kun näet sen virheilmoituksessa. Näissä tapauksissa sinun
täytyy muuttaa joko mallia tai rakennetta, jossa käytät mallia, riippuen
koodin tarkoitetusta käyttäytymisestä.

Katsotaan esimerkkiä siitä, mitä tapahtuu, kun yritämme käyttää kumottavaa
mallia siellä, missä Rust vaatii kiistämätöntä mallia, ja päinvastoin.
Listaus 19-8 näyttää `let`-lauseen, mutta malliksi olemme määrittäneet
`Some(x)`, kumottavan mallin. Kuten saattaa odottaa, tämä koodi ei käänny.

<Listing number="19-8" caption="Yritys käyttää kumottavaa mallia `let`-lauseessa">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-08/src/main.rs:here}}
```

</Listing>

Jos `some_option_value` olisi `None`-arvo, se ei vastaisi mallia `Some(x)`,
mikä tarkoittaa, että malli on kumottava. `let`-lause voi kuitenkin hyväksyä
vain kiistämättömän mallin, koska koodilla ei ole mitään järkevää tekemistä
`None`-arvolla. Käännösaikana Rust valittaa, että olemme yrittäneet käyttää
kumottavaa mallia siellä, missä kiistämätön malli vaaditaan:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-08/output.txt}}
```

Koska emme kattaneet (emmekä voineet kattaa!) jokaista kelvollista arvoa
mallilla `Some(x)`, Rust oikeutetusti tuottaa kääntäjävirheen.

Jos meillä on kumottava malli siellä, missä kiistämätön malli tarvitaan,
voimme korjata sen muuttamalla mallia käyttävää koodia: `let`-lauseen sijaan
voimme käyttää `let...else`-lausetta. Jos malli ei vastaa, aaltosulkeiden
sisällä oleva koodi käsittelee arvon. Listaus 19-9 näyttää, miten listauksen
19-8 koodi korjataan.

<Listing number="19-9" caption="`let...else`-lauseen ja lohkon käyttö kumottavien mallien kanssa `let`-lauseen sijaan">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-09/src/main.rs:here}}
```

</Listing>

Olemme antaneet koodille ulospääsyn! Tämä koodi on täysin kelvollinen, vaikka
se tarkoittaakin, ettemme voi käyttää kiistämätöntä mallia ilman varoitusta.
Jos annamme `let...else`-lauseelle mallin, joka vastaa aina, kuten `x`, kuten
listauksessa 19-10, kääntäjä antaa varoituksen.

<Listing number="19-10" caption="Yritys käyttää kiistämätöntä mallia `let...else`-lauseessa">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-10/src/main.rs:here}}
```

</Listing>

Rust valittaa, ettei `let...else`-lauseen käyttäminen kiistämättömän mallin
kanssa ole järkevää:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-10/output.txt}}
```

Tästä syystä match-haarojen täytyy käyttää kumottavia malleja, paitsi
viimeisessä haarassa, joka vastaa jäljellä olevia arvoja kiistämättömällä
mallilla. Rust sallii kiistämättömän mallin käytön `match`-lausekkeessa,
jossa on vain yksi haara, mutta tämä syntaksi ei ole erityisen hyödyllinen
ja sen voisi korvata yksinkertaisemmalla `let`-lauseella.

Nyt kun tiedät, missä malleja käytetään ja mikä on ero kumottavien ja
kiistämättömien mallien välillä, käydään läpi kaikki syntaksi, jota voimme
käyttää mallien luomiseen.
