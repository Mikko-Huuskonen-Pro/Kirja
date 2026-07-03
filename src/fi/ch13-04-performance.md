<!-- Old headings. Do not remove or links may break. -->

<a id="comparing-performance-loops-vs-iterators"></a>

## Suorituskyky: silmukat vs. iteraattorit

Päättääksesi, käytätkö silmukoita vai iteraattoreita, sinun täytyy tietää, kumpi
toteutus on nopeampi: `search`-funktion versio eksplisiittisellä `for`-silmukalla vai
versio iteraattoreilla.

Suoritimme vertailun lataamalla koko Sir Arthur Conan Doylen teoksen _The Adventures of
Sherlock Holmes_ `String`-merkkijonoon ja etsimällä siitä sanan _the_. Tässä ovat
tulokset `for`-silmukkaa käyttävästä ja iteraattoreita käyttävästä `search`-versiosta:

```text
test bench_search_for  ... bench:  19,620,300 ns/iter (+/- 915,700)
test bench_search_iter ... bench:  19,234,900 ns/iter (+/- 657,200)
```

Molemmat toteutukset ovat suorituskyvyltään samanlaisia! Emme selitä vertailukoodia
tässä, koska tarkoitus ei ole todistaa kahden version vastaavuutta vaan saada yleinen
käsitys siitä, miten nämä kaksi toteutusta vertautuvat suorituskyvyn kannalta.

Kattavampaa vertailua varten kannattaa testata erilaisia tekstejä eri kokoluokissa
`contents`-parametrina, erilaisia sanoja ja eripituisia sanoja `query`-parametrina sekä
kaikenlaisia muita variaatioita. Pointti on tämä: iteraattorit ovat korkean tason
abstraktio, mutta ne käännetään suunnilleen samaan koodiin kuin jos olisit kirjoittanut
matalan tason koodin itse. Iteraattorit ovat yksi Rustin _nollakustannusisten
abstraktioiden_ muoto; tämä tarkoittaa, että abstraktion käyttö ei aiheuta ylimääräistä
ajonaikaista kuormitusta. Tämä on analoginen siihen, miten C++:n alkuperäinen suunnittelija
ja toteuttaja Bjarne Stroustrup määrittelee nollaylikuormituksen vuoden 2012 ETAPS-avainpuheessaan
”Foundations of C++”:

> In general, C++ implementations obey the zero-overhead principle: What you
> don’t use, you don’t pay for. And further: What you do use, you couldn’t hand
> code any better.

Monissa tapauksissa iteraattoreita käyttävä Rust-koodi käännetään samaan konekieleen,
jonka kirjoittaisit käsin. Optimoinnit, kuten silmukan purkaminen ja taulukon
indeksoinnin rajatarkistusten poistaminen, pätevät ja tekevät syntyneestä koodista erittäin
tehokasta. Nyt kun tiedät tämän, voit käyttää iteraattoreita ja sulkeisia pelotta! Ne
tekevät koodista korkeamman tason näköistä, mutta eivät aiheuta suorituskyvyn
rangaistusta.

## Yhteenveto

Sulkeiset ja iteraattorit ovat Rust-ominaisuuksia, jotka ovat saaneet vaikutteita
funktionaalisista ohjelmointikielistä. Ne auttavat ilmaisemaan korkean tason ideoita
selkeästi matalan tason suorituskyvyllä. Sulkeisten ja iteraattorien toteutukset on
suunniteltu niin, etteivät ne vaikuta ajonaikaiseen suorituskykyyn. Tämä on osa Rustin
tavoitetta tarjota nollakustannuksisia abstraktioita.

Nyt kun olemme parantaneet I/O-projektimme ilmaisukykyä, katsotaan lisää `cargo`-ominaisuuksia,
jotka auttavat jakamaan projektin maailmalle.
