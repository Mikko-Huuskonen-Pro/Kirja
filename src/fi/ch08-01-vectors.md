## Arvojen listojen tallentaminen vektoreilla

Ensimmäinen kokoelmatyyppi, jota tarkastelemme, on `Vec<T>`, joka tunnetaan myös vektorina. Vektorit antavat sinun tallentaa useamman kuin yhden arvon yhteen tietorakenteeseen, joka sijoittaa kaikki arvot vierekkäin muistiin. Vektorit voivat tallentaa vain saman tyyppisiä arvoja. Ne ovat hyödyllisiä, kun sinulla on luettelo kohteita, kuten tiedoston tekstirivit tai ostoskorin tuotteiden hinnat.

### Uuden vektorin luominen

Luodaksesi uuden tyhjän vektorin kutsumme `Vec::new`-funktiota, kuten listauksessa 8-1.

<Listing number="8-1" caption="Uuden tyhjän vektorin luominen `i32`-tyyppisten arvojen tallentamiseksi">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-01/src/main.rs:here}}
```

</Listing>

Huomaa, että lisäsimme tähän tyyppimerkinnän. Koska emme lisää mitään arvoja tähän vektoriin, Rust ei tiedä, millaisia elementtejä aiot tallentaa. Tämä on tärkeä kohta. Vektorit on toteutettu geneerisillä tyypeillä; käsittelemme geneeristen tyyppien käyttöä omissa tyypeissäsi luvussa 10. Toistaiseksi tiedä, että standardikirjaston tarjoama `Vec<T>`-tyyppi voi tallentaa minkä tahansa tyypin. Kun luomme vektorin tietyn tyypin tallentamiseksi, voimme määrittää tyypin kulmasuluissa. Listauksessa 8-1 olemme kertoneet Rustille, että `v`:n `Vec<T>` tallentaa `i32`-tyyppisiä elementtejä.

Useammin luot `Vec<T>`:n alkuarvoilla, ja Rust päättelee tallennettavan arvon tyypin, joten harvoin tarvitset tehdä tämän tyyppimerkinnän. Rust tarjoaa kätevästi `vec!`-makron, joka luo uuden vektorin, joka tallentaa antamasi arvot. Listaus 8-2 luo uuden `Vec<i32>`:n, joka tallentaa arvot `1`, `2` ja `3`. Kokonaislukutyyppi on `i32`, koska se on oletuskokonaislukutyyppi, kuten käsittelimme [”Tietotyypit”][data-types]<!-- ignore --> -kohdassa luvussa 3.

<Listing number="8-2" caption="Uuden arvoja sisältävän vektorin luominen">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-02/src/main.rs:here}}
```

</Listing>

Koska olemme antaneet alkuperäiset `i32`-arvot, Rust voi päätellä, että `v`:n tyyppi on `Vec<i32>`, eikä tyyppimerkintää tarvita. Seuraavaksi tarkastelemme, miten vektoria muokataan.

### Vektorin päivittäminen

Luodaksesi vektorin ja lisätäksesi siihen elementtejä voimme käyttää `push`-metodia, kuten listauksessa 8-3.

<Listing number="8-3" caption="`push`-metodin käyttö arvojen lisäämiseksi vektoriin">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-03/src/main.rs:here}}
```

</Listing>

Kuten minkä tahansa muuttujan kanssa, jos haluamme pystyä muuttamaan sen arvoa, meidän on tehtävä se muuttuvaksi `mut`-avainsanalla, kuten käsittelimme luvussa 3. Sisällyttämämme luvut ovat kaikki `i32`-tyyppiä, ja Rust päättelee tämän datasta, joten `Vec<i32>`-merkintää ei tarvita.

### Vektorin elementtien lukeminen

On kaksi tapaa viitata vektoriin tallennettuun arvoon: indeksoinnilla tai `get`-metodilla. Seuraavissa esimerkeissä olemme merkinneet näiden funktioiden palauttamat arvot selkeyden vuoksi.

Listaus 8-4 näyttää molemmat tavat käyttää arvoa vektorissa, indeksointisyntaksilla ja `get`-metodilla.

<Listing number="8-4" caption="Indeksointisyntaksin ja `get`-metodin käyttö vektorin kohteen käyttämiseksi">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-04/src/main.rs:here}}
```

</Listing>

Huomaa muutamia yksityiskohtia. Käytämme indeksiarvoa `2` saadaksemme kolmannen elementin, koska vektorit indeksoidaan numerolla alkaen nollasta. `&`- ja `[]`-merkkien käyttö antaa meille viitteen elementtiin indeksiarvolla. Kun käytämme `get`-metodia indeksin välittämiseksi argumenttina, saamme `Option<&T>`:n, jota voimme käyttää `match`:in kanssa.

Rust tarjoaa nämä kaksi tapaa viitata elementtiin, jotta voit valita, miten ohjelma käyttäytyy, kun yrität käyttää indeksiarvoa olemassa olevien elementtien alueen ulkopuolella. Esimerkkinä katsotaan, mitä tapahtuu, kun meillä on viisi elementtiä sisältävä vektori ja yritämme sitten käyttää elementtiä indeksissä 100 kummallakin tekniikalla, kuten listauksessa 8-5.

<Listing number="8-5" caption="Yritys käyttää elementtiä indeksissä 100 vektorissa, jossa on viisi elementtiä">

```rust,should_panic,panics
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-05/src/main.rs:here}}
```

</Listing>

Kun suoritamme tämän koodin, ensimmäinen `[]`-metodi aiheuttaa ohjelman paniikin, koska se viittaa olemattomaan elementtiin. Tätä metodia kannattaa käyttää, kun haluat ohjelmasi kaatuvan, jos yritetään käyttää elementtiä vektorin lopun jälkeen.

Kun `get`-metodille välitetään indeksi, joka on vektorin ulkopuolella, se palauttaa `None`:n panikoimatta. Käyttäisit tätä metodia, jos elementin käyttäminen vektorin alueen ulkopuolella voi tapahtua satunnaisesti normaaleissa olosuhteissa. Koodissasi on sitten logiikka käsitellä joko `Some(&element)` tai `None`, kuten käsittelimme luvussa 6. Esimerkiksi indeksi voi tulla käyttäjältä, joka syöttää numeron. Jos he vahingossa syöttävät liian suuren numeron ja ohjelma saa `None`-arvon, voisit kertoa käyttäjälle, kuinka monta kohdetta nykyisessä vektorissa on, ja antaa heille uuden mahdollisuuden syöttää kelvollinen arvo. Se olisi käyttäjäystävällisempää kuin ohjelman kaatuminen kirjoitusvirheen vuoksi!

Kun ohjelmalla on kelvollinen viite, lainauskontrolleri valvoo omistus- ja lainaussääntöjä (käsiteltiin luvussa 4) varmistaakseen, että tämä viite ja kaikki muut viitteet vektorin sisältöön pysyvät kelvollisina. Muista sääntö, jonka mukaan et voi olla muuttuvia ja muuttumattomia viitteitä samassa laajuudessa. Tämä sääntö pätee listauksessa 8-6, jossa pidämme muuttumatonta viitettä vektorin ensimmäiseen elementtiin ja yritämme lisätä elementin loppuun. Tämä ohjelma ei toimi, jos yritämme myös viitata kyseiseen elementtiin myöhemmin funktiossa.

<Listing number="8-6" caption="Yritys lisätä elementti vektoriin samalla kun pidetään viitettä kohteeseen">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-06/src/main.rs:here}}
```

</Listing>

Tämän koodin kääntäminen tuottaa tämän virheen:

```console
{{#include ../listings/ch08-common-collections/listing-08-06/output.txt}}
```

Listauksen 8-6 koodi saattaa näyttää siltä, että sen pitäisi toimia: Miksi viitteen ensimmäiseen elementtiin pitäisi välittää muutoksista vektorin lopussa? Tämä virhe johtuu siitä, miten vektorit toimivat: Koska vektorit sijoittavat arvot vierekkäin muistiin, uuden elementin lisääminen vektorin loppuun saattaa vaatia uuden muistin varaamista ja vanhojen elementtien kopioimista uuteen tilaan, jos ei ole tarpeeksi tilaa sijoittaa kaikki elementit vierekkäin sinne, missä vektori on tällä hetkellä tallennettuna. Siinä tapauksessa viite ensimmäiseen elementtiin osoittaisi vapautettuun muistiin. Lainaussäännöt estävät ohjelmia päätymästä tällaiseen tilanteeseen.

> Huom: Lisätietoja `Vec<T>`-tyypin toteutustiedoista on kohdassa [”Rustonomicon”][nomicon].

### Vektorin arvojen läpikäynti

Käyttääksemme jokaista vektorin elementtiä vuorollaan, käymme läpi kaikki elementit sen sijaan, että käyttäisimme indeksejä yksi kerrallaan. Listaus 8-7 näyttää, miten käyttää `for`-silmukkaa saadaksesi muuttumattomia viitteitä jokaiseen `i32`-arvojen vektorin elementtiin ja tulostaaksesi ne.

<Listing number="8-7" caption="Jokaisen vektorin elementin tulostaminen käymällä elementit läpi `for`-silmukalla">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-07/src/main.rs:here}}
```

</Listing>

Voimme myös käydä läpi muuttuvia viitteitä jokaiseen muuttuvan vektorin elementtiin tehdäksemme muutoksia kaikkiin elementteihin. Listauksen 8-8 `for`-silmukka lisää `50` jokaiseen elementtiin.

<Listing number="8-8" caption="Muuttuvien viitteiden läpikäynti vektorin elementeissä">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-08/src/main.rs:here}}
```

</Listing>

Muuttaaksemme arvoa, johon muuttuva viite viittaa, meidän on käytettävä `*`-dereferointioperaattoria päästäksemme `i`:n arvoon ennen kuin voimme käyttää `+=`-operaattoria. Käsittelemme dereferointioperaattoria tarkemmin kohdassa [”Viittauksen seuraaminen arvoon”][deref]<!-- ignore --> luvussa 15.

Vektorin läpikäynti, olipa muuttumattomasti tai muuttuvasti, on turvallista lainauskontrollerin sääntöjen ansiosta. Jos yrittäisimme lisätä tai poistaa kohteita listauksen 8-7 ja listauksen 8-8 `for`-silmukoiden rungoissa, saisimme kääntäjän virheen, joka on samanlainen kuin listauksen 8-6 koodilla. `for`-silmukan pitämä viite vektoriin estää koko vektorin samanaikaisen muokkaamisen.

### Enumin käyttö useiden tyyppien tallentamiseen

Vektorit voivat tallentaa vain saman tyyppisiä arvoja. Tämä voi olla hankalaa; on ehdottomasti käyttötapauksia, joissa tarvitaan eri tyyppisten kohteiden luettelon tallentaminen. Onneksi enum-variantit on määritelty saman enum-tyypin alle, joten kun tarvitsemme yhden tyypin edustamaan eri tyyppisiä elementtejä, voimme määritellä ja käyttää enumia!

Esimerkiksi oletetaan, että haluamme saada arvoja taulukkolaskentataulukon riviltä, jossa jotkin rivin sarakkeet sisältävät kokonaislukuja, jotkut liukulukuja ja jotkut merkkijonoja. Voimme määritellä enumin, jonka variantit tallentavat eri arvotyyppejä, ja kaikki enum-variantit katsotaan samaksi tyypiksi: enumin tyypiksi. Sitten voimme luoda vektorin, joka tallentaa kyseisen enumin ja siten lopulta eri tyyppejä. Olemme havainnollistaneet tämän listauksessa 8-9.

<Listing number="8-9" caption="Enumin määrittely eri tyyppisten arvojen tallentamiseksi yhdessä vektorissa">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-09/src/main.rs:here}}
```

</Listing>

Rustin on tiedettävä käännösaikana, mitä tyyppejä vektorissa on, jotta se tietää tarkalleen, kuinka paljon muistia keossa tarvitaan jokaisen elementin tallentamiseen. Meidän on myös oltava eksplisiittisiä siitä, mitkä tyypit ovat sallittuja tässä vektorissa. Jos Rust sallisi vektorin sisältää mitä tahansa tyyppiä, olisi mahdollista, että yksi tai useampi tyypeistä aiheuttaisi virheitä vektorin elementeille suoritettavissa operaatioissa. Enumin ja `match`-lausekkeen käyttö tarkoittaa, että Rust varmistaa käännösaikana, että jokainen mahdollinen tapaus käsitellään, kuten käsittelimme luvussa 6.

Jos et tiedä kattavaa joukkoa tyyppejä, joita ohjelma saa ajonaikana tallennettavaksi vektoriin, enum-tekniikka ei toimi. Sen sijaan voit käyttää trait-objektia, jota käsittelemme luvussa 18.

Nyt kun olemme käsitelleet joitakin yleisimpiä tapoja käyttää vektoreita, muista tutustua [API-dokumentaatioon][vec-api]<!-- ignore --> kaikista hyödyllisistä metodeista, jotka standardikirjasto on määritellyt `Vec<T>`:lle. Esimerkiksi `push`:n lisäksi `pop`-metodi poistaa ja palauttaa viimeisen elementin.

### Vektorin pudottaminen pudottaa sen elementit

Kuten mikä tahansa muu `struct`, vektori vapautetaan, kun se poistuu laajuudesta, kuten listauksessa 8-10.

<Listing number="8-10" caption="Vektorin ja sen elementtien pudottamisen paikan näyttäminen">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-10/src/main.rs:here}}
```

</Listing>

Kun vektori pudotetaan, kaikki sen sisältö pudotetaan myös, eli sen sisältämät kokonaisluvut siivotaan. Lainauskontrolleri varmistaa, että viitteitä vektorin sisältöön käytetään vain niin kauan kuin vektori itse on kelvollinen.

Siirrytään seuraavaan kokoelmatyyppiin: `String`!

[data-types]: ch03-02-data-types.html#data-types
[nomicon]: ../nomicon/vec/vec.html
[vec-api]: ../std/vec/struct.Vec.html
[deref]: ch15-02-deref.html#following-the-pointer-to-the-value-with-the-dereference-operator
