## Futures, Tasks ja Threads yhdessä

Kuten näimme [luvussa 16][ch16]<!-- ignore -->, säikeet tarjoavat yhden lähestymistavan samanaikaisuuteen. Olemme nähneet tässä luvussa toisen lähestymistavan: asyncin käytön futurejen ja streamien kanssa. Jos mietit, milloin valita toinen menetelmä toisen sijaan, vastaus on: se riippuu tilanteesta! Ja monissa tapauksissa valinta ei ole säikeet _tai_ async, vaan säikeet _ja_ async.

Monet käyttöjärjestelmät ovat tarjonneet säikeisiin perustuvia samanaikaisuusmalleja jo vuosikymmeniä, ja monet ohjelmointikielet tukevat niitä sen vuoksi. Nämä mallit eivät kuitenkaan ole ilman kompromissejaan. Monissa käyttöjärjestelmissä jokainen säie käyttää melko paljon muistia. Säikeet ovat myös vaihtoehto vain, kun käyttöjärjestelmäsi ja laitteistosi tukevat niitä. Toisin kuin tavallisissa pöytä- ja mobiilitietokoneissa, joissakin sulautetuissa järjestelmissä ei ole lainkaan käyttöjärjestelmää, joten niissä ei ole myöskään säikeitä.

Async-malli tarjoaa erilaisen — ja lopulta toisiaan täydentävän — joukon kompromisseja. Async-mallissa samanaikaiset operaatiot eivät vaadi omia säikeitään. Sen sijaan ne voivat suorittua tehtävinä, kuten kun käytimme `trpl::spawn_task`:ia käynnistämään työtä synkronisesta funktiosta streamit-osiossa. Tehtävä on samankaltainen kuin säie, mutta sen sijaan että käyttöjärjestelmä hallinnoisi sitä, kirjastotason koodi hallinnoi sitä: ajoympäristö.

On syy siihen, miksi säikeiden ja tehtävien luomisen API:t ovat niin samankaltaisia. Säikeet toimivat rajoina synkronisten operaatioiden joukoille; samanaikaisuus on mahdollista säikeiden _välillä_. Tehtävät toimivat rajoina _asynkronisten_ operaatioiden joukoille; samanaikaisuus on mahdollista sekä tehtävien _välillä_ että _sisällä_, koska tehtävä voi vaihtaa futurejen välillä rungossaan. Lopuksi futuret ovat Rustin hienojakoisin samanaikaisuuden yksikkö, ja jokainen future voi edustaa muiden futurejen puuta. Ajoympäristö — erityisesti sen executor — hallinnoi tehtäviä, ja tehtävät hallinnoivat futureja. Tässä suhteessa tehtävät muistuttavat kevyitä, ajoympäristön hallinnoimia säikeitä, joilla on lisäominaisuuksia, koska ajoympäristö eikä käyttöjärjestelmä hallinnoi niitä.

Tämä ei tarkoita, että async-tehtävät olisivat aina parempia kuin säikeet (tai päinvastoin). Samanaikaisuus säikeillä on joissakin suhteissa yksinkertaisempi ohjelmointimalli kuin samanaikaisuus `async`:illa. Se voi olla vahvuus tai heikkous. Säikeillä ei ole luontaista vastinetta futurelle; ne suorittuvat yksinkertaisesti loppuun ilman keskeytyksiä paitsi käyttöjärjestelmän itsensä aiheuttamia.

Ja käy ilmi, että säikeet ja tehtävät toimivat usein hyvin yhdessä, koska tehtävät voidaan (ainakin joissakin ajoympäristöissä) siirtää säikeiden välillä. Itse asiassa taustalla käyttämämme ajoympäristö — mukaan lukien `spawn_blocking`- ja `spawn_task`-funktiot — on oletuksena monisäikeinen! Monet ajoympäristöt käyttävät lähestymistapaa nimeltä _work stealing_ siirtääkseen tehtäviä läpinäkyvästi säikeiden välillä sen perusteella, miten säikeitä käytetään parhaillaan, parantaakseen järjestelmän kokonaissuorituskykyä. Tämä lähestymistapa vaatii itse asiassa sekä säikeitä _että_ tehtäviä, ja siten myös futureja.

Kun mietit, mitä menetelmää käyttää milloin, harkitse näitä nyrkkisääntöjä:

- Jos työ on _hyvin rinnakkaistettavissa_ (eli laskentarajoitteista), kuten joukon datan käsittely, jossa kukin osa voidaan käsitellä erikseen, säikeet ovat parempi valinta.
- Jos työ on _hyvin samanaikaista_ (eli I/O-rajoitteista), kuten viestien käsittely useista eri lähteistä, jotka voivat saapua eri välein tai eri taajuudella, async on parempi valinta.

Ja jos tarvitset sekä rinnakkaisuutta että samanaikaisuutta, sinun ei tarvitse valita säikeiden ja asyncin välillä. Voit käyttää niitä vapaasti yhdessä ja antaa kummankin tehdä sen osan, jossa se on parhaimmillaan. Esimerkiksi listaus 17-25 näyttää melko tyypillisen esimerkin tämänkaltaisesta yhdistelmästä oikean maailman Rust-koodissa.

<Listing number="17-25" caption="Viestien lähettäminen estävällä koodilla säikeessä ja viestien odottaminen async-lohkossa" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-25/src/main.rs:all}}
```

</Listing>

Aloitamme luomalla async-kanavan ja luomalla säikeen, joka ottaa omistukseen kanavan lähettäjäpuolen `move`-avainsanalla. Säikeen sisällä lähetämme numerot 1–10 nukkuen sekunnin välein. Lopuksi suoritamme async-lohkoon välitetyllä futurella `trpl::block_on`:illa kuten koko luvun ajan. Tässä futuressa odotamme näitä viestejä aivan kuten muissa viestinvälitysesimerkeissä.

Palataksesi luvun alussa käsiteltyyn skenaarioon, kuvittele suorittavasi joukon videon koodaustehäviä omistetulla säikeellä (koska videon koodaus on laskentarajoitteista), mutta ilmoittavasi käyttöliittymälle async-kanavalla, kun nämä operaatiot ovat valmiita. Tällaisia yhdistelmiä on lukemattomia oikean maailman käyttötapauksissa.

## Yhteenveto

Tämä ei ole viimeinen kerta, kun näet samanaikaisuutta tässä kirjassa. [Luvun 21][ch21]<!-- ignore --> projekti soveltaa näitä käsitteitä realistisemmassa tilanteessa kuin tässä käsitellyt yksinkertaisemmat esimerkit ja vertaa ongelmanratkaisua säikeillä sekä tehtävillä ja futureilla suoremmin.

Riippumatta siitä, minkä näistä lähestymistavoista valitset, Rust antaa työkalut turvallisen ja nopean samanaikaisen koodin kirjoittamiseen — olipa kyseessä suuren läpimenon web-palvelin tai sulautettu käyttöjärjestelmä.

Seuraavaksi puhumme idiomaattisista tavoista mallintaa ongelmia ja jäsentää ratkaisuja, kun Rust-ohjelmasi kasvavat. Lisäksi käsittelemme, miten Rustin idiomit liittyvät niihin, jotka saatat tuntea olio-ohjelmoinnista.

[ch16]: http://localhost:3000/ch16-00-concurrency.html
[combining-futures]: ch17-03-more-futures.html#building-our-own-async-abstractions
[streams]: ch17-04-streams.html#composing-streams
[ch21]: ch21-00-final-project-a-web-server.html
