## Viittausten validointi elinikien avulla

Eliniät (*lifetimes*) ovat toinen geneeristen tyyppien laji, jota olemme jo
käyttäneet. Sen sijaan, että varmistaisimme tyypin käyttäytyvän haluamallamme
tavalla, eliniät varmistavat, että viittaukset ovat kelvollisia niin kauan kuin
tarvitsemme niitä.

Yksi yksityiskohta, jota emme käsitelleet luvun 4 osiossa [”Viittaukset ja
lainaaminen”][references-and-borrowing]<!-- ignore -->, on se, että jokaisella
Rustin viittauksella on elinikä, joka on alue, jolla viittaus on kelvollinen.
Useimmiten eliniät ovat implisiittisiä ja pääteltyjä, aivan kuten useimmiten
tyypit ovat pääteltyjä. Meidän täytyy ilmoittaa tyypit vain, kun useita tyyppejä
on mahdollista. Vastaavasti meidän täytyy merkitä eliniät, kun viittausten
eliniöillä voi olla useita eri suhteita. Rust vaatii meitä merkitsemään
suhteet geneeristen elinikäparametrien avulla varmistaakseen, että ajonaikana
käytetyt viittaukset ovat varmasti kelvollisia.

Elinikien merkitseminen ei ole edes käsite, jota useimmissa muissa
ohjelmointikielissä on, joten tämä tuntuu tutustumattomalta. Vaikka emme käsittele
eliniä kokonaisuudessaan tässä luvussa, käsittelemme yleisiä tapoja, joilla
voit kohdata elinikäsyntaksia, jotta voit tottua käsitteeseen.

<!-- Old headings. Do not remove or links may break. -->

<a id="preventing-dangling-references-with-lifetimes"></a>

### Riippuvat viittaukset

Elinikien pääasiallinen tarkoitus on estää riippuvia viittauksia (*dangling
references*), jotka, jos niiden olemassaolo sallittaisiin, saisivat ohjelman
viittaamaan muihin tietoihin kuin niihin, joihin sen on tarkoitus viitata.
Harkitse listauksen 10-16 ohjelmaa, jossa on ulompi ja sisempi näkyvyysalue.

<Listing number="10-16" caption="Yritys käyttää viittausta, jonka arvo on poistunut näkyvyysalueelta">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-16/src/main.rs}}
```

</Listing>

> Huom: Listausten 10-16, 10-17 ja 10-23 esimerkit ilmoittavat muuttujia
> antamatta niille alkuarvoa, joten muuttujan nimi on olemassa ulommalla
> näkyvyysalueella. Ensi silmäyksellä tämä saattaa vaikuttaa ristiriitaiselta
> Rustin null-arvojen puuttumisen kanssa. Jos kuitenkin yritämme käyttää
> muuttujaa ennen arvon antamista, saamme käännösvirheen, mikä osoittaa, että
> Rust todellakaan ei salli null-arvoja.

Ulompi näkyvyysalue ilmoittaa muuttujan nimeltä `r` ilman alkuarvoa, ja
sisempi näkyvyysalue ilmoittaa muuttujan nimeltä `x` alkuarvolla `5`. Sisemmällä
näkyvyysalueella yritämme asettaa `r`:n arvoksi viittauksen `x`:ään. Sitten
sisempi näkyvyysalue päättyy, ja yritämme tulostaa `r`:n arvon. Tämä koodi ei
käänny, koska arvo, johon `r` viittaa, on poistunut näkyvyysalueelta ennen kuin
yritämme käyttää sitä. Tässä on virheilmoitus:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-16/output.txt}}
```

Virheilmoitus sanoo, että muuttuja `x` ”does not live long enough”. Syy on, että
`x` on näkyvyysalueen ulkopuolella, kun sisempi näkyvyysalue päättyy rivillä 7.
Mutta `r` on silti kelvollinen ulommalla näkyvyysalueella; koska sen
näkyvyysalue on suurempi, sanomme, että se ”elää pidempään”. Jos Rust sallisi
tämän koodin toimia, `r` viittaisi muistiin, joka vapautettiin, kun `x` poistui
näkyvyysalueelta, eikä mikään, mitä yrittäisimme tehdä `r`:llä, toimisi
oikein. Miten Rust määrittää, että tämä koodi on virheellinen? Se käyttää
lainauskontrolleria.

### Lainauskontrolleri

Rustin kääntäjällä on _lainauskontrolleri_ (*borrow checker*), joka vertaa
näkyvyysalueita määrittääkseen, ovatko kaikki lainaukset kelvollisia. Listaus
10-17 näyttää saman koodin kuin listaus 10-16, mutta merkinnöillä, jotka
näyttävät muuttujien eliniät.

<Listing number="10-17" caption="Muuttujien `r` ja `x` eliniöiden merkinnät, nimiltään `'a` ja `'b`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-17/src/main.rs}}
```

</Listing>

Tässä olemme merkinneet `r`:n eliniän `'a`:lla ja `x`:n eliniän `'b`:llä. Kuten
näet, sisempi `'b`-lohko on paljon pienempi kuin ulompi `'a`-elinikälohko.
Käännösaikana Rust vertaa kahden eliniän kokoa ja näkee, että `r`:llä on elinikä
`'a`, mutta se viittaa muistiin, jonka elinikä on `'b`. Ohjelma hylätään, koska
`'b` on lyhyempi kuin `'a`: Viittauksen kohteella ei ole yhtä pitkää elinikää
kuin viittauksella.

Listaus 10-18 korjaa koodin niin, ettei siinä ole riippuvaa viittausta, ja se
kääntyy ilman virheitä.

<Listing number="10-18" caption="Kelvollinen viittaus, koska datalla on pidempi elinikä kuin viittauksella">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-18/src/main.rs}}
```

</Listing>

Tässä `x`:llä on elinikä `'b`, joka tässä tapauksessa on suurempi kuin `'a`. Tämä
tarkoittaa, että `r` voi viitata `x`:ään, koska Rust tietää, että `r`:n
viittaus on aina kelvollinen niin kauan kuin `x` on kelvollinen.

Nyt kun tiedät, missä viittausten eliniät ovat ja miten Rust analysoi eliniitä
varmistaakseen, että viittaukset ovat aina kelvollisia, tutkitaan geneerisiä
eliniä funktioiden parametreissa ja palautusarvoissa.

### Geneeriset eliniät funktioissa

Kirjoitamme funktion, joka palauttaa pidemmän kahdesta merkkijonoviipaleesta.
Tämä funktio ottaa kaksi merkkijonoviipaletta ja palauttaa yhden
merkkijonoviipaleen. Kun olemme toteuttaneet `longest`-funktion, listauksen
10-19 koodin pitäisi tulostaa `The longest string is abcd`.

<Listing number="10-19" file-name="src/main.rs" caption="`main`-funktio, joka kutsuu `longest`-funktiota löytääkseen pidemmän kahdesta merkkijonoviipaleesta">

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-19/src/main.rs}}
```

</Listing>

Huomaa, että haluamme funktion ottavan merkkijonoviipaleita, jotka ovat
viittauksia, eivät merkkijonoja, koska emme halua `longest`-funktion ottavan
parametriensa omistajuutta. Katso lisätietoja siitä, miksi listauksen 10-19
parametrit ovat haluamiamme, luvun 4 osiosta [”Merkkijonoviipaleet
parametreina”][string-slices-as-parameters]<!-- ignore -->.

Jos yritämme toteuttaa `longest`-funktion kuten listauksessa 10-20, se ei käänny.

<Listing number="10-20" file-name="src/main.rs" caption="`longest`-funktion toteutus, joka palauttaa pidemmän kahdesta merkkijonoviipaleesta mutta ei vielä käänny">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-20/src/main.rs:here}}
```

</Listing>

Sen sijaan saamme seuraavan virheen, joka käsittelee eliniitä:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-20/output.txt}}
```

Ohjeteksti paljastaa, että palautustyypillä täytyy olla geneerinen elinikäparametri,
koska Rust ei voi kertoa, viittaako palautettava viittaus `x`:ään vai `y`:ään.
Itse asiassa emme tiedä sitäkään, koska funktion rungon `if`-lohko palauttaa
viittauksen `x`:ään ja `else`-lohko viittauksen `y`:ään!

Kun määrittelemme tämän funktion, emme tiedä konkreettisia arvoja, jotka
annetaan tälle funktiolle, joten emme tiedä, suoritetaanko `if`- vai `else`-
tapaus. Emme myöskään tiedä viittausten konkreettisia eliniä, joten emme voi
tarkastella näkyvyysalueita kuten listauksissa 10-17 ja 10-18 määrittääksemme,
onko palauttamamme viittaus aina kelvollinen. Lainauskontrolleri ei voi
määrittää tätäkään, koska se ei tiedä, miten `x`:n ja `y`:n eliniät liittyvät
palautusarvon elinikään. Korjataksemme tämän virheen lisäämme geneerisiä
elinikäparametreja, jotka määrittelevät viittausten välisen suhteen, jotta
lainauskontrolleri voi suorittaa analyysinsä.

### Elinikämerkintöjen syntaksi

Elinikämerkinnät eivät muuta sitä, kuinka kauan mikään viittauksista elää.
Pikemminkin ne kuvaavat useiden viittausten eliniöiden välisiä suhteita
vaikuttamatta eliniöihin. Aivan kuten funktiot voivat hyväksyä minkä tahansa
tyypin, kun allekirjoitus määrittää geneerisen tyyppiparametrin, funktiot voivat
hyväksyä viittauksia millä tahansa eliniällä määrittämällä geneerisen
elinikäparametrin.

Elinikämerkinnöillä on hieman epätavallinen syntaksi: Elinikäparametrien
nimien täytyy alkaa heittomerkillä (`'`) ja ne ovat yleensä pieniä kirjaimia
ja hyvin lyhyitä, kuten geneeriset tyypit. Useimmat ihmiset käyttävät nimeä
`'a` ensimmäiselle elinikämerkinnälle. Sijoitamme elinikäparametrien
merkinnät `&`-merkin jälkeen viittauksessa käyttäen välilyöntiä erottamaan
merkinnän viittauksen tyypistä.

Tässä on joitakin esimerkkejä — viittaus `i32`:een ilman elinikäparametria,
viittaus `i32`:een, jolla on elinikäparametri nimeltä `'a`, ja muuttuva
viittaus `i32`:een, jolla on myös elinikä `'a`:

```rust,ignore
&i32        // a reference
&'a i32     // a reference with an explicit lifetime
&'a mut i32 // a mutable reference with an explicit lifetime
```

Yksi elinikämerkintä itsessään ei merkitse paljon, koska merkinnät on
tarkoitettu kertomaan Rustille, miten useiden viittausten geneeriset
elinikäparametrit liittyvät toisiinsa. Tarkastellaan, miten elinikämerkinnät
liittyvät toisiinsa `longest`-funktion yhteydessä.

<!-- Old headings. Do not remove or links may break. -->

<a id="lifetime-annotations-in-function-signatures"></a>

### Funktioiden allekirjoituksissa

Käyttääksemme elinikämerkintöjä funktioiden allekirjoituksissa meidän täytyy
ilmoittaa geneeriset elinikäparametrit kulmasulkeissa funktion nimen ja
parametrilistan välissä, aivan kuten teimme geneeristen tyyppiparametrien
kanssa.

Haluamme allekirjoituksen ilmaisevan seuraavan rajoituksen: Palautettu viittaus
on kelvollinen niin kauan kuin molemmat parametrit ovat kelvollisia. Tämä on
parametrien ja palautusarvon eliniöiden välinen suhde. Nimeämme eliniän `'a`:ksi
ja lisäämme sen jokaiseen viittaukseen, kuten listauksessa 10-21.

<Listing number="10-21" file-name="src/main.rs" caption="`longest`-funktion määrittely, joka määrittää, että kaikilla allekirjoituksen viittauksilla täytyy olla sama elinikä `'a`">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-21/src/main.rs:here}}
```

</Listing>

Tämän koodin pitäisi kääntyä ja tuottaa haluamamme tuloksen, kun käytämme sitä
listauksen 10-19 `main`-funktion kanssa.

Funktion allekirjoitus kertoo nyt Rustille, että jollekin eliniälle `'a` funktio
ottaa kaksi parametria, jotka molemmat ovat merkkijonoviipaleita, jotka elävät
vähintään yhtä kauan kuin elinikä `'a`. Funktion allekirjoitus kertoo myös
Rustille, että funktiosta palautettu merkkijonoviipale elää vähintään yhtä
kauan kuin elinikä `'a`. Käytännössä tämä tarkoittaa, että `longest`-funktion
palauttaman viittauksen elinikä on sama kuin funktioargumenttien viittaamien
arvojen eliniöistä lyhyempi. Nämä suhteet ovat ne, joita haluamme Rustin
käyttävän analysoidessaan tätä koodia.

Muista, että kun määrittelemme elinikäparametrit tässä funktion allekirjoituksessa,
emme muuta annettujen tai palautettujen arvojen eliniöitä. Pikemminkin
määrittelemme, että lainauskontrollerin täytyy hylätä kaikki arvot, jotka eivät
noudata näitä rajoituksia. Huomaa, että `longest`-funktion ei tarvitse tietää
tarkalleen, kuinka kauan `x` ja `y` elävät, vain että jokin näkyvyysalue voidaan
korvata `'a`:lla, joka tyydyttää tämän allekirjoituksen.

Kun merkitsemme eliniöitä funktioissa, merkinnät menevät funktion allekirjoitukseen,
ei funktion runkoon. Elinikämerkinnät tulevat osaksi funktion sopimusta, aivan
kuten allekirjoituksen tyypit. Funktioallekirjoitusten sisältäminen elinikäsopimus
tarkoittaa, että Rust-kääntäjän suorittama analyysi voi olla yksinkertaisempaa.
Jos on ongelma funktion merkinnöissä tai sen kutsumisessa, kääntäjän virheet
voivat osoittaa koodimme osan ja rajoitukset tarkemmin. Jos sen sijaan Rust-
kääntäjä tekisi enemmän päätelmiä siitä, mitä aioimme eliniöiden suhteilla,
kääntäjä saattaisi pystyä osoittamaan vain koodimme käytön monia askelia
ongelman syystä.

Kun annamme konkreettisia viittauksia `longest`-funktiolle, konkreettinen
elinikä, joka korvaa `'a`:n, on osa `x`:n näkyvyysalueesta, joka leikkaa `y`:n
näkyvyysalueen kanssa. Toisin sanoen geneerinen elinikä `'a` saa konkreettisen
eliniän, joka on yhtä suuri kuin `x`:n ja `y`:n eliniöistä lyhyempi. Koska
olemme merkinneet palautetun viittauksen samalla elinikäparametrilla `'a`,
palautettu viittaus on myös kelvollinen `x`:n ja `y`:n eliniöistä lyhyemmän
pituuden ajan.

Katsotaan, miten elinikämerkinnät rajoittavat `longest`-funktiota antamalla
viittauksia, joilla on eri konkreettiset eliniät. Listaus 10-22 on
suoraviivainen esimerkki.

<Listing number="10-22" file-name="src/main.rs" caption="`longest`-funktion käyttö viittauksilla `String`-arvoihin, joilla on eri konkreettiset eliniät">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-22/src/main.rs:here}}
```

</Listing>

Tässä esimerkissä `string1` on kelvollinen ulomman näkyvyysalueen loppuun asti,
`string2` on kelvollinen sisemmän näkyvyysalueen loppuun asti, ja `result`
viittaa johonkin, joka on kelvollinen sisemmän näkyvyysalueen loppuun asti.
Aja tämä koodi ja näet, että lainauskontrolleri hyväksyy sen; se kääntyy ja
tulostaa `The longest string is long string is long`.

Seuraavaksi kokeillaan esimerkkiä, joka näyttää, että `result`-viittauksen
elinikän täytyy olla kahden argumentin lyhyempi elinikä. Siirrämme `result`-
muuttujan ilmoituksen sisemmän näkyvyysalueen ulkopuolelle, mutta jätämme arvon
`result`-muuttujalle antamisen sisemmän näkyvyysalueen sisälle `string2`:n
kanssa. Sitten siirrämme `result`:ia käyttävän `println!`:n sisemmän
näkyvyysalueen ulkopuolelle, sen päättymisen jälkeen. Listauksen 10-23 koodi ei
käänny.

<Listing number="10-23" file-name="src/main.rs" caption="Yritys käyttää `result`-muuttujaa sen jälkeen, kun `string2` on poistunut näkyvyysalueelta">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-23/src/main.rs:here}}
```

</Listing>

Kun yritämme kääntää tämän koodin, saamme tämän virheen:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-23/output.txt}}
```

Virhe näyttää, että jotta `result` olisi kelvollinen `println!`-lauseelle,
`string2`:n täytyisi olla kelvollinen ulomman näkyvyysalueen loppuun asti. Rust
tietää tämän, koska olemme merkinneet funktioiden parametrien ja palautusarvojen
eliniät käyttämällä samaa elinikäparametria `'a`.

Ihmisinä voimme katsoa tätä koodia ja nähdä, että `string1` on pidempi kuin
`string2`, ja siksi `result` sisältää viittauksen `string1`:een. Koska `string1`
ei ole vielä poistunut näkyvyysalueelta, viittaus `string1`:een on silti
kelvollinen `println!`-lauseelle. Kääntäjä ei kuitenkaan näe, että viittaus on
kelvollinen tässä tapauksessa. Olemme kertoneet Rustille, että `longest`-
funktion palauttaman viittauksen elinikä on sama kuin annettujen viittausten
eliniöistä lyhyempi. Siksi lainauskontrolleri kieltää listauksen 10-23 koodin,
koska siinä voi olla virheellinen viittaus.

Kokeile suunnitella lisää kokeita, joissa vaihtelet `longest`-funktiolle
annettujen viittausten arvoja ja eliniöitä sekä sitä, miten palautettua
viittausta käytetään. Tee hypoteeseja siitä, läpäisevätkö kokeesi lainauskontrollerin
ennen kääntämistä; tarkista sitten, olitko oikeassa!

<!-- Old headings. Do not remove or links may break. -->

<a id="thinking-in-terms-of-lifetimes"></a>

### Suhteet

Tapa, jolla sinun täytyy määrittää elinikäparametrit, riippuu siitä, mitä
funktiosi tekee. Esimerkiksi, jos muuttaisimme `longest`-funktion toteutusta
palauttamaan aina ensimmäisen parametrin pidemmän merkkijonoviipaleen sijaan,
emme tarvitsisi määrittää elinikää `y`-parametrille. Seuraava koodi kääntyy:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-08-only-one-reference-with-lifetime/src/main.rs:here}}
```

</Listing>

Olemme määrittäneet elinikäparametrin `'a` parametrille `x` ja palautustyypille,
mutta emme parametrille `y`, koska `y`:n eliniällä ei ole mitään suhdetta `x`:n
tai palautusarvon elinikään.

Kun palautamme viittauksen funktiosta, palautustyypin elinikäparametrin täytyy
vastata jonkin parametrin elinikäparametria. Jos palautettu viittaus _ei_
viittaa mihinkään parametreista, sen täytyy viitata tässä funktiossa luotuun
arvoon. Tämä olisi kuitenkin riippuva viittaus, koska arvo poistuu
näkyvyysalueelta funktion lopussa. Harkitse tätä yritystä toteuttaa `longest`-
funktio, joka ei käänny:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-09-unrelated-lifetime/src/main.rs:here}}
```

</Listing>

Tässä, vaikka olemme määrittäneet elinikäparametrin `'a` palautustyypille, tämä
toteutus ei käänny, koska palautusarvon elinikä ei liity parametrien eliniöihin
ollenkaan. Tässä on virheilmoitus, jonka saamme:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-09-unrelated-lifetime/output.txt}}
```

Ongelma on, että `result` poistuu näkyvyysalueelta ja siivotaan `longest`-
funktion lopussa. Yritämme myös palauttaa viittauksen `result`:iin funktiosta.
Emme voi määrittää elinikäparametreja, jotka muuttaisivat riippuvaa viittausta,
eikä Rust anna meidän luoda riippuvaa viittausta. Tässä tapauksessa paras korjaus
olisi palauttaa omistettu tietotyyppi viittauksen sijaan, jolloin kutsuva
funktio on vastuussa arvon siivoamisesta.

Lopulta elinikäsyntaksi koskee eri parametrien ja funktioiden palautusarvojen
eliniöiden yhdistämistä. Kun ne on yhdistetty, Rustilla on tarpeeksi tietoa
salliakseen muistiturvalliset operaatiot ja kieltääkseen operaatiot, jotka
luoisivat riippuvia osoittimia tai muuten rikkoisivat muistiturvallisuutta.

<!-- Old headings. Do not remove or links may break. -->

<a id="lifetime-annotations-in-struct-definitions"></a>

### Struct-määrittelyissä

Tähän asti määrittelemämme structit säilyttävät kaikki omistettuja tyyppejä.
Voimme määritellä structeja säilyttämään viittauksia, mutta siinä tapauksessa
meidän täytyy lisätä elinikämerkintä jokaiseen viittaukseen structin
määrittelyssä. Listauksessa 10-24 on struct nimeltä `ImportantExcerpt`, joka
säilyttää merkkijonoviipaleen.

<Listing number="10-24" file-name="src/main.rs" caption="Struct, joka säilyttää viittauksen ja vaatii elinikämerkinnän">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-24/src/main.rs}}
```

</Listing>

Tällä structilla on yksi kenttä `part`, joka säilyttää merkkijonoviipaleen,
joka on viittaus. Kuten geneeristen tietotyyppien kanssa, ilmoitamme geneerisen
elinikäparametrin nimen kulmasulkeissa structin nimen jälkeen, jotta voimme
käyttää elinikäparametria struct-määrittelyn rungossa. Tämä merkintä tarkoittaa,
että `ImportantExcerpt`-instanssi ei voi elää pidempään kuin viittaus, jonka se
säilyttää `part`-kentässään.

Tässä `main`-funktio luo `ImportantExcerpt`-structin instanssin, joka säilyttää
viittauksen muuttujan `novel` omistaman `String`-arvon ensimmäiseen lauseeseen.
`novel`-datan on olemassa ennen `ImportantExcerpt`-instanssin luomista.
Lisäksi `novel` ei poistu näkyvyysalueelta ennen kuin `ImportantExcerpt`
poistuu näkyvyysalueelta, joten `ImportantExcerpt`-instanssin viittaus on
kelvollinen.

### Elinikien poisjättäminen

Olet oppinut, että jokaisella viittauksella on elinikä ja että sinun täytyy
määrittää elinikäparametrit funktioille tai structeille, jotka käyttävät
viittauksia. Meillä oli kuitenkin funktio listauksessa 4-9, joka näytetään
uudelleen listauksessa 10-25, ja se kääntyi ilman elinikämerkintöjä.

<Listing number="10-25" file-name="src/lib.rs" caption="Funktio, jonka määrittelimme listauksessa 4-9 ja joka kääntyi ilman elinikämerkintöjä, vaikka parametri ja palautustyyppi ovat viittauksia">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-25/src/main.rs:here}}
```

</Listing>

Syy, miksi tämä funktio kääntyy ilman elinikämerkintöjä, on historiallinen:
Rustin varhaisissa versioissa (ennen 1.0) tämä koodi ei olisi kääntynyt, koska
jokainen viittaus tarvitsi eksplisiittisen eliniän. Silloin funktion
allekirjoitus olisi kirjoitettu näin:

```rust,ignore
fn first_word<'a>(s: &'a str) -> &'a str {
```

Kun Rust-tiimi oli kirjoittanut paljon Rust-koodia, he huomasivat, että Rust-
ohjelmoijat kirjoittivat samoja elinikämerkintöjä yhä uudelleen tietyissä
tilanteissa. Nämä tilanteet olivat ennustettavia ja noudattivat muutamia
deterministisiä kuvioita. Kehittäjät ohjelmoivat nämä kuviot kääntäjän koodiin,
jotta lainauskontrolleri voisi päätellä eliniät näissä tilanteissa eikä
eksplisiittisiä merkintöjä tarvittaisi.

Tämä Rustin historia on merkityksellinen, koska on mahdollista, että lisää
deterministisiä kuvioita ilmestyy ja lisätään kääntäjään. Tulevaisuudessa
vähemmän elinikämerkintöjä saattaa olla tarpeen.

Kuviot, jotka on ohjelmoitu Rustin viittausten analyysiin, kutsutaan
_elinikien poisjättämissäännöiksi_ (*lifetime elision rules*). Nämä eivät ole
sääntöjä ohjelmoijille noudatettavaksi; ne ovat joukko erityisiä tapauksia,
joita kääntäjä harkitsee, ja jos koodisi sopii näihin tapauksiin, sinun ei
tarvitse kirjoittaa eliniöitä eksplisiittisesti.

Poisjättämissäännöt eivät tarjoa täyttä päätelmää. Jos viittausten eliniöistä
on vielä epäselvyyttä Rustin sovellettua sääntöjä, kääntäjä ei arvaa, mikä
jäljellä olevien viittausten elinikä pitäisi olla. Arvaamisen sijaan kääntäjä
antaa virheen, jonka voit ratkaista lisäämällä elinikämerkinnät.

Funktio- tai metodiparametrien eliniöitä kutsutaan _syöttöeliniöiksi_ (*input
lifetimes*), ja palautusarvojen eliniöitä _tuottoeliniöiksi_ (*output
lifetimes*).

Kääntäjä käyttää kolmea sääntöä selvittääkseen viittausten eliniöitä, kun
eksplisiittisiä merkintöjä ei ole. Ensimmäinen sääntö koskee syöttöeliniöitä,
ja toinen ja kolmas sääntö koskevat tuottoeliniöitä. Jos kääntäjä pääsee kolmen
säännön loppuun ja viittauksia on vielä, joiden eliniöitä se ei voi selvittää,
kääntäjä pysähtyy virheeseen. Nämä säännöt koskevat `fn`-määrittelyjä sekä
`impl`-lohkoja.

Ensimmäinen sääntö on, että kääntäjä määrittää elinikäparametrin jokaiselle
parametrille, joka on viittaus. Toisin sanoen funktio, jolla on yksi parametri,
saa yhden elinikäparametrin: `fn foo<'a>(x: &'a i32)`; funktio, jolla on kaksi
parametria, saa kaksi erillistä elinikäparametria: `fn foo<'a, 'b>(x: &'a i32,
y: &'b i32)`; ja niin edelleen.

Toinen sääntö on, että jos on täsmälleen yksi syöttöelinikäparametri, se
elinikä määritetään kaikille tuottoelinikäparametreille: `fn foo<'a>(x: &'a i32)
-> &'a i32`.

Kolmas sääntö on, että jos on useita syöttöelinikäparametreja, mutta yksi
niistä on `&self` tai `&mut self`, koska tämä on metodi, `self`:n elinikä
määritetään kaikille tuottoelinikäparametreille. Tämä kolmas sääntö tekee
metodeista paljon miellyttävämpiä lukea ja kirjoittaa, koska vähemmän symboleja
on tarpeen.

Olkoon me olemme kääntäjä. Sovelletaan näitä sääntöjä selvittääksemme
viittausten eliniöt `first_word`-funktion allekirjoituksessa listauksessa
10-25. Allekirjoitus alkaa ilman eliniöitä, jotka liittyvät viittauksiin:

```rust,ignore
fn first_word(s: &str) -> &str {
```

Sitten kääntäjä soveltaa ensimmäistä sääntöä, joka määrittää, että jokainen
parametri saa oman eliniänsä. Kutsumme sitä `'a`:ksi kuten tavallisesti, joten
nyt allekirjoitus on tämä:

```rust,ignore
fn first_word<'a>(s: &'a str) -> &str {
```

Toinen sääntö pätee, koska on täsmälleen yksi syöttöelinikä. Toinen sääntö
määrittää, että yhden syöttöparametrin elinikä määritetään tuottoelinikään,
joten allekirjoitus on nyt tämä:

```rust,ignore
fn first_word<'a>(s: &'a str) -> &'a str {
```

Nyt kaikilla viittauksilla tässä funktioallekirjoituksessa on eliniät, ja
kääntäjä voi jatkaa analyysiään ilman, että ohjelmoijan tarvitsee merkitä
eliniöitä tässä funktioallekirjoituksessa.

Katsotaan toista esimerkkiä käyttäen `longest`-funktiota, jolla ei ollut
elinikäparametreja, kun aloimme työskennellä sen kanssa listauksessa 10-20:

```rust,ignore
fn longest(x: &str, y: &str) -> &str {
```

Sovelletaan ensimmäistä sääntöä: Jokainen parametri saa oman eliniänsä. Tällä
kertaa meillä on kaksi parametria yhden sijaan, joten meillä on kaksi elinikää:

```rust,ignore
fn longest<'a, 'b>(x: &'a str, y: &'b str) -> &str {
```

Näet, että toinen sääntö ei päde, koska on useampi kuin yksi syöttöelinikä.
Kolmas sääntö ei myöskään päde, koska `longest` on funktio eikä metodi, joten
mikään parametreista ei ole `self`. Kun olemme käyneet läpi kaikki kolme
sääntöä, emme ole vieläkään selvittäneet palautustyypin elinikää. Tämän vuoksi
saimme virheen yrittäessämme kääntää listauksen 10-20 koodia: Kääntäjä kävi
läpi elinikien poisjättämissäännöt, mutta ei silti voinut selvittää kaikkia
viittausten eliniöitä allekirjoituksessa.

Koska kolmas sääntö pätee todella vain metodien allekirjoituksissa, katsomme
eliniöitä tässä yhteydessä seuraavaksi nähdäksemme, miksi kolmas sääntö
tarkoittaa, ettei meidän tarvitse merkitä eliniöitä metodien allekirjoituksissa
usein.

<!-- Old headings. Do not remove or links may break. -->

<a id="lifetime-annotations-in-method-definitions"></a>

### Metodimäärittelyissä

Kun toteutamme metodeja structille, jolla on eliniöitä, käytämme samaa syntaksia
kuin geneeristen tyyppiparametrien kanssa, kuten listauksessa 10-11. Missä
ilmoitamme ja käytämme elinikäparametreja riippuu siitä, liittyvätkö ne
structin kenttiin vai metodin parametreihin ja palautusarvoihin.

Structin kenttien elinikien nimet täytyy aina ilmoittaa `impl`-avainsanan
jälkeen ja sitten käyttää structin nimen jälkeen, koska nämä eliniät ovat osa
structin tyyppiä.

`impl`-lohkon sisällä olevissa metodien allekirjoituksissa viittaukset voivat
liittyä structin kenttien viittausten elinikään tai olla riippumattomia.
Lisäksi elinikien poisjättämissäännöt usein tekevät niin, ettei elinikämerkintöjä
tarvita metodien allekirjoituksissa. Katsotaan joitakin esimerkkejä käyttäen
structia nimeltä `ImportantExcerpt`, jonka määrittelimme listauksessa 10-24.

Ensin käytämme `level`-nimistä metodia, jonka ainoa parametri on viittaus
`self`:ään ja jonka palautusarvo on `i32`, joka ei ole viittaus mihinkään:

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-10-lifetimes-on-methods/src/main.rs:1st}}
```

Elinikäparametrin ilmoitus `impl`-avainsanan jälkeen ja sen käyttö tyypin nimen
jälkeen ovat pakollisia, mutta ensimmäisen poisjättämissäännön ansiosta emme
tarvitse merkitä viittauksen `self`:n elinikää.

Tässä on esimerkki, jossa kolmas elinikien poisjättämissääntö pätee:

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-10-lifetimes-on-methods/src/main.rs:3rd}}
```

On kaksi syöttöelinikää, joten Rust soveltaa ensimmäistä elinikien
poisjättämissääntöä ja antaa sekä `&self`:lle että `announcement`:ille omat
eliniänsä. Sitten, koska yksi parametreista on `&self`, palautustyyppi saa
`&self`:n eliniän, ja kaikki eliniät on huomioitu.

### Staattinen elinikä

Yksi erityinen elinikä, josta meidän täytyy keskustella, on `'static`, joka
merkitsee, että kyseinen viittaus _voi_ elää koko ohjelman keston. Kaikilla
merkkijonoliteraaleilla on `'static`-elinikä, jonka voimme merkitä näin:

```rust
let s: &'static str = "I have a static lifetime.";
```

Tämän merkkijonon teksti on tallennettu suoraan ohjelman binääritiedostoon,
joka on aina käytettävissä. Siksi kaikkien merkkijonoliteraalien elinikä on
`'static`.

Saatat nähdä virheilmoituksissa ehdotuksia käyttää `'static`-elinikää. Mutta
ennen kuin määrittelet `'static`-elinikää viittaukselle, mieti, elääkö
viittauksesi todella koko ohjelmasi eliniän ja haluatko sen elävän. Useimmiten
virheilmoitus, joka ehdottaa `'static`-elinikää, johtuu yrityksestä luoda
riippuva viittaus tai eliniöjen epäsuhtasta. Tällaisissa tapauksissa ratkaisu
on korjata nämä ongelmat, ei määrittää `'static`-elinikää.

<!-- Old headings. Do not remove or links may break. -->

<a id="generic-type-parameters-trait-bounds-and-lifetimes-together"></a>

## Geneeriset tyyppiparametrit, trait-rajat ja eliniät yhdessä

Katsotaan lyhyesti syntaksia geneeristen tyyppiparametrien, trait-rajojen ja
eliniöiden määrittelyyn yhdessä yhdessä funktiossa!

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-11-generics-traits-and-lifetimes/src/main.rs:here}}
```

Tämä on `longest`-funktio listauksesta 10-21, joka palauttaa pidemmän kahdesta
merkkijonoviipaleesta. Mutta nyt siinä on ylimääräinen parametri nimeltä `ann`
geneerisestä tyypistä `T`, joka voidaan täyttää millä tahansa tyypillä, joka
toteuttaa `Display`-traitin `where`-lausekkeen määrittämällä tavalla. Tämä
ylimääräinen parametri tulostetaan `{}`-merkinnällä, minkä vuoksi `Display`-
trait-raja on tarpeen. Koska eliniät ovat eräänlaisia geneerisiä tyyppejä,
elinikäparametrin `'a` ja geneerisen tyyppiparametrin `T` ilmoitukset menevät
samaan listaan kulmasulkeissa funktion nimen jälkeen.

## Yhteenveto

Käsittelimme paljon tässä luvussa! Nyt kun tiedät geneerisistä tyyppiparametreista,
traitteista ja trait-rajoista sekä geneerisistä elinikäparametreista, olet
valmis kirjoittamaan koodia ilman toistoa, joka toimii monissa eri tilanteissa.
Geneeriset tyyppiparametrit antavat sinun soveltaa koodia eri tyyppeihin.
Traitit ja trait-rajat varmistavat, että vaikka tyypit ovat geneerisiä, niillä
on koodin tarvitsema käyttäytyminen. Opit käyttämään elinikämerkintöjä
varmistaaksesi, ettei tämä joustava koodi sisällä riippuvia viittauksia. Ja
kaikki tämä analyysi tapahtuu käännösaikana, mikä ei vaikuta ajonaikaiseen
suorituskykyyn!

Usko tai älä, näistä luvussa käsittelemistämme aiheista on vielä paljon
opittavaa: Luku 18 käsittelee trait-olioita, jotka ovat toinen tapa käyttää
traitteja. On myös monimutkaisempia skenaarioita, joissa tarvitset elinikämerkintöjä
vain hyvin edistyneissä tilanteissa; niitä varten sinun kannattaa lukea
[Rust Reference][reference]. Mutta seuraavaksi opit kirjoittamaan testejä Rustissa,
jotta voit varmistaa, että koodisi toimii odotetulla tavalla.

[references-and-borrowing]: ch04-02-references-and-borrowing.html#references-and-borrowing
[string-slices-as-parameters]: ch04-03-slices.html#string-slices-as-parameters
[reference]: ../reference/trait-bounds.html
