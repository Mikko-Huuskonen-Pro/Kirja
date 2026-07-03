## Liite C: Johdettavat traitit

Kirjan eri kohdissa olemme käsitelleet `derive`-attribuuttia, jonka voi lisätä
rakenne- tai luettelomäärittelyyn. `derive`-attribuutti luo koodia, joka toteuttaa
traitin oletustoteutuksellaan tyypille, johon olet lisännyt `derive`-syntaksin.

Tässä liitteessä tarjoamme viitteen kaikista standardikirjaston traiteista, joita voi
käyttää `derive`-attribuutin kanssa. Kukin osio käsittelee:

- Mitä operaattoreita ja metodeja tämän traitin johdattaminen mahdollistaa
- Mitä `derive`-attribuutin tarjoama toteutus tekee
- Mitä traitin toteuttaminen merkitsee tyypille
- Milloin traitin toteuttaminen on sallittua tai kiellettyä
- Esimerkkejä toiminnoista, jotka vaativat traitin

Jos haluat eri käyttäytymisen kuin `derive`-attribuutti tarjoaa, katso [standardikirjaston
dokumentaatiosta](../std/index.html)<!-- ignore --> kunkin traitin manuaalista toteutusta
varten.

Tässä luetellut traitit ovat ainoat standardikirjaston määrittelemät traitit, jotka voi
toteuttaa omille tyypeilleen `derive`-attribuutilla. Muilla standardikirjaston traiteilla ei
ole järkevää oletuskäyttäytymistä, joten ne täytyy toteuttaa tavalla, joka sopii
tavoitteeseesi.

Esimerkki traitista, jota ei voi johdattaa, on `Display`, joka käsittelee loppukäyttäjälle
tarkoitettua muotoilua. Sinun tulisi aina harkita sopivaa tapaa näyttää tyyppi
loppukäyttäjälle. Mitkä osat tyypistä loppukäyttäjän tulisi nähdä? Mitkä osat olisivat
hänelle olennaisia? Mikä tietomuoto olisi hänelle merkityksellisin? Rust-kääntäjällä ei ole
tätä näkemystä, joten se ei voi tarjota sinulle sopivaa oletuskäyttäytymistä.

Tässä liitteessä annettu luettelo johdettavista traiteista ei ole kattava: kirjastot voivat
toteuttaa `derive`-attribuutin omille traiteilleen, jolloin `derive`-attribuutilla
käytettävissä olevien traitien luettelo on aidosti avoin. `derive`-toteutus edellyttää
proseduraalisen makron käyttöä, jota käsitellään luvun 20 kohdassa [”Mukautetut `derive`-
makrot”][custom-derive-macros]<!-- ignore -->.

### `Debug` ohjelmoijan tulostusta varten

`Debug`-trait mahdollistaa virheenkorjausmuotoilun formaattijonoissa, jonka ilmaiset
lisäämällä `:?` `{}`-paikkamerkkien sisään.

`Debug`-traitin avulla voit tulostaa tyypin instansseja virheenkorjausta varten, jotta sinä
ja muut ohjelmoijat, jotka käyttävät tyyppiäsi, voitte tarkastella instanssia ohjelman
suorituksen tietyssä kohdassa.

`Debug`-trait vaaditaan esimerkiksi `assert_eq!`-makron käytössä. Tämä makro tulostaa
argumenteiksi annettujen instanssien arvot, jos yhtäsuuruusväite epäonnistuu, jotta
ohjelmoijat näkevät, miksi kaksi instanssia eivät olleet yhtä suuria.

### `PartialEq` ja `Eq` yhtäsuuruusvertailuihin

`PartialEq`-trait mahdollistaa tyypin instanssien vertailun yhtäsuuruuden tarkistamiseksi
ja `==`- sekä `!=`-operaattorien käytön.

`PartialEq`-traitin johdattaminen toteuttaa `eq`-metodin. Kun `PartialEq` johdetaan
rakenteille, kaksi instanssia on yhtä suuri vain, jos _kaikki_ kentät ovat yhtä suuria, ja
instanssit eivät ole yhtä suuria, jos _mikä tahansa_ kentistä ei ole yhtä suuri. Kun se
johdetaan luetteloille, jokainen variantti on yhtä suuri itsensä kanssa eikä yhtä suuri
muiden varianttien kanssa.

`PartialEq`-trait vaaditaan esimerkiksi `assert_eq!`-makron käytössä, joka tarvitsee
mahdollisuuden vertailla kahden instanssin yhtäsuuruutta.

`Eq`-traitilla ei ole metodeja. Sen tarkoitus on ilmaista, että jokainen annotoidun tyypin
arvo on yhtä suuri itsensä kanssa. `Eq`-traitia voi soveltaa vain tyyppeihin, jotka
toteuttavat myös `PartialEq`-traitin, vaikka kaikki `PartialEq`-traitin toteuttavat tyypit
eivät voi toteuttaa `Eq`-traitia. Yksi esimerkki tästä ovat liukulukutyypit: liukulukujen
toteutus sanoo, että kaksi ei-lukua (`NaN`) -arvoa eivät ole yhtä suuria toistensa kanssa.

Esimerkki tilanteesta, jossa `Eq` vaaditaan, on avaimet `HashMap<K, V>`-rakenteessa, jotta
`HashMap<K, V>` voi kertoa, ovatko kaksi avainta samat.

### `PartialOrd` ja `Ord` järjestysvertailuihin

`PartialOrd`-trait mahdollistaa tyypin instanssien vertailun lajittelua varten. Tyyppiä,
joka toteuttaa `PartialOrd`-traitin, voi käyttää `<`, `>`, `<=` ja `>=` -operaattoreiden
kanssa. `PartialOrd`-traitia voi soveltaa vain tyyppeihin, jotka toteuttavat myös
`PartialEq`-traitin.

`PartialOrd`-traitin johdattaminen toteuttaa `partial_cmp`-metodin, joka palauttaa
`Option<Ordering>`-arvon, joka on `None`, kun annetut arvot eivät tuota järjestystä.
Esimerkki arvosta, joka ei tuota järjestystä, vaikka useimmat kyseisen tyypin arvot ovat
vertailtavissa, on liukuluvun `NaN`-arvo. `partial_cmp`-metodin kutsuminen millä tahansa
liukuluvulla ja `NaN`-liukuluvulla palauttaa `None`.

Kun se johdetaan rakenteille, `PartialOrd` vertaa kahta instanssia vertaamalla kunkin
kentän arvoa siinä järjestyksessä, jossa kentät esiintyvät rakennemäärittelyssä. Kun se
johdetaan luetteloille, rakennemäärittelyssä aiemmin julistetut variantit katsotaan
myöhemmin lueteltuja variantteja pienemmiksi.

`PartialOrd`-trait vaaditaan esimerkiksi `rand`-paketin `gen_range`-metodissa, joka
tuottaa satunnaisen arvon välilausekkeen määrittämässä välissä.

`Ord`-traitin avulla tiedät, että annotoidun tyypin kahdelle mille tahansa arvolle on
olemassa kelvollinen järjestys. `Ord`-trait toteuttaa `cmp`-metodin, joka palauttaa
`Ordering`-arvon `Option<Ordering>`-arvon sijaan, koska kelvollinen järjestys on aina
mahdollinen. `Ord`-traitia voi soveltaa vain tyyppeihin, jotka toteuttavat myös
`PartialOrd`- ja `Eq`-traitit (ja `Eq` edellyttää `PartialEq`-traitia). Kun se johdetaan
rakenteille ja luetteloille, `cmp` käyttäytyy samalla tavalla kuin `partial_cmp`
`PartialOrd`-traitin johdetussa toteutuksessa.

Esimerkki tilanteesta, jossa `Ord` vaaditaan, on arvojen tallentaminen `BTreeSet<T>`-
rakenteeseen, joka säilyttää tietoa arvojen lajittelujärjestyksen perusteella.

### `Clone` ja `Copy` arvojen monistamiseen

`Clone`-trait mahdollistaa arvon eksplisiittisen syväkopion luomisen, ja monistusprosessi
voi sisältää mielivaltaisen koodin suorittamisen ja keon tietojen kopioimisen. Katso
lisätietoja `Clone`-traitista luvun 4 kohdasta [”Muuttujat ja tiedon vuorovaikutus
`Clone`-traitin kanssa”][variables-and-data-interacting-with-clone]<!-- ignore -->.

`Clone`-traitin johdattaminen toteuttaa `clone`-metodin, joka koko tyypille toteutettuna
kutsuu `clone`-metodia kunkin tyypin osan kohdalla. Tämä tarkoittaa, että kaikkien kenttien
tai arvojen tyypissä täytyy myös toteuttaa `Clone`, jotta `Clone` voidaan johdattaa.

Esimerkki tilanteesta, jossa `Clone` vaaditaan, on `to_vec`-metodin kutsuminen viipaleella.
Viipale ei omista sisältämiään tyypin instansseja, mutta `to_vec`-metodin palauttaman
vektorin täytyy omistaa instanssinsa, joten `to_vec` kutsuu `clone`-metodia jokaisen
kohteen kohdalla. Näin ollen viipaleessa säilytettävän tyypin täytyy toteuttaa `Clone`.

`Copy`-trait mahdollistaa arvon monistamisen kopioimalla vain pinossa säilytetyt bitit;
mielivaltaista koodia ei tarvita. Katso lisätietoja `Copy`-traitista luvun 4 kohdasta
[”Vain pinossa säilytettävä data: `Copy`”][stack-only-data-copy]<!-- ignore -->.

`Copy`-trait ei määrittele metodeja, jotta ohjelmoijat eivät voisi ylikuormittaa niitä ja
rikkoa oletusta, ettei mielivaltaista koodia suoriteta. Näin kaikki ohjelmoijat voivat
olettaa, että arvon kopioiminen on hyvin nopeaa.

Voit johdattaa `Copy`-traitin mille tahansa tyypille, jonka kaikki osat toteuttavat
`Copy`-traitin. `Copy`-traitin toteuttavan tyypin täytyy myös toteuttaa `Clone`, koska
`Copy`-traitin toteuttavalla tyypillä on triviaali `Clone`-toteutus, joka tekee saman
tehtävän kuin `Copy`.

`Copy`-traitia vaaditaan harvoin; `Copy`-traitin toteuttavilla tyypeillä on käytettävissä
optimointeja, joten sinun ei tarvitse kutsua `clone`-metodia, mikä tekee koodista
ytimekkäämpää.

Kaiken, mitä `Copy`-traitilla voi tehdä, voi myös saavuttaa `Clone`-traitilla, mutta koodi
voi olla hitaampaa tai joutua käyttämään `clone`-metodia joissakin kohdissa.

### `Hash` arvon kartoittamiseen kiinteäkokoiseen arvoon

`Hash`-trait mahdollistaa mielivaltaisen kokoisen tyypin instanssin kartoittamisen
kiinteäkokoiseen arvoon tiivistefunktion avulla. `Hash`-traitin johdattaminen toteuttaa
`hash`-metodin. Johdetussa `hash`-metodin toteutuksessa yhdistetään kunkin tyypin osan
`hash`-metodin kutsumisen tulos, mikä tarkoittaa, että kaikkien kenttien tai arvojen täytyy
myös toteuttaa `Hash`, jotta `Hash` voidaan johdattaa.

Esimerkki tilanteesta, jossa `Hash` vaaditaan, on avainten tallentaminen `HashMap<K, V>`-
rakenteeseen tietojen tehokkaaseen säilyttämiseen.

### `Default` oletusarvoille

`Default`-trait mahdollistaa tyypille oletusarvon luomisen. `Default`-traitin johdattaminen
toteuttaa `default`-funktion. Johdetussa `default`-funktion toteutuksessa kutsutaan
`default`-funktiota kunkin tyypin osan kohdalla, mikä tarkoittaa, että kaikkien kenttien
tai arvojen tyypissä täytyy myös toteuttaa `Default`, jotta `Default` voidaan johdattaa.

`Default::default`-funktiota käytetään yleisesti yhdessä rakennepäivityssyntaksin kanssa,
jota käsitellään luvun 5 kohdassa [”Instanssien luominen muista instansseista rakenne-
päivityssyntaksilla”][creating-instances-from-other-instances-with-struct-update-syntax]<!--
ignore -->. Voit mukauttaa muutamia rakenteen kenttiä ja asettaa sitten oletusarvon
lopuille kentille käyttämällä `..Default::default()`-syntaksia.

`Default`-trait vaaditaan, kun käytät `unwrap_or_default`-metodia `Option<T>`-instansseilla.
Jos `Option<T>` on `None`, `unwrap_or_default`-metodi palauttaa `Default::default`-funktion
tuloksen tyypille `T`, joka on tallennettuna `Option<T>`-rakenteeseen.

[creating-instances-from-other-instances-with-struct-update-syntax]: ch05-01-defining-structs.html#creating-instances-from-other-instances-with-struct-update-syntax
[stack-only-data-copy]: ch04-01-what-is-ownership.html#stack-only-data-copy
[variables-and-data-interacting-with-clone]: ch04-01-what-is-ownership.html#variables-and-data-interacting-with-clone
[custom-derive-macros]: ch20-05-macros.html#custom-derive-macros
