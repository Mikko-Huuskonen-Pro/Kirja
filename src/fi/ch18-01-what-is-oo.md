## Oliopohjaisten kielten ominaisuudet

Ohjelmointiyhteisössä ei ole yksimielisyyttä siitä, mitä ominaisuuksia kielen täytyy sisältää ollakseen oliopohjainen. Rustiin on vaikuttanut monia ohjelmointiparadigmoja, mukaan lukien OOP; esimerkiksi tutkimme luvussa 13 funktionaalisen ohjelmoinnin tuomia ominaisuuksia. Voidaan väittää, että OOP-kielet jakavat tiettyjä yhteisiä piirteitä — nimittäin oliot, kapseloinnin ja periytymisen. Katsotaan, mitä kukin näistä ominaisuuksista tarkoittaa ja tukeeko Rust sitä.

### Oliot sisältävät tietoa ja käyttäytymistä

Kirja _Design Patterns: Elements of Reusable Object-Oriented Software_ Erich Gammalta, Richard Helmiltä, Ralph Johnsonilta ja John Vlissidesilta (Addison-Wesley, 1994), jota kutsutaan puhekielessä _The Gang of Four_ -kirjaksi, on oliopohjaisten suunnittelumallien luettelo. Se määrittelee OOP:n näin:

> Oliopohjaiset ohjelmat koostuvat olioista. **Olio** yhdistää sekä tiedon että sitä käsittelevät proseduurit. Näitä proseduurien kutsutaan tyypillisesti **metodeiksi** tai **operaatioiksi**.

Tämän määritelmän perusteella Rust on oliopohjainen: rakenteet ja luettelotyypit sisältävät tietoa, ja `impl`-lohkot tarjoavat metodeja rakenteille ja luettelotyypeille. Vaikka rakenteita ja luettelotyyppejä metodeineen ei _kutsutakaan_ olioiksi, ne tarjoavat saman toiminnallisuuden Gang of Fourin olion määritelmän mukaan.

### Kapselointi piilottaa toteutuksen yksityiskohdat

Toinen OOP:hen yleisesti liitettävä piirre on _kapseloinnin_ idea, joka tarkoittaa, että olion toteutuksen yksityiskohdat eivät ole käytettävissä sitä käyttävälle koodille. Ainoa tapa olla vuorovaikutuksessa olion kanssa on sen julkinen rajapinta; olion käyttäjän koodin ei pitäisi pystyä kurkistamaan olion sisään ja muuttamaan tietoa tai käyttäytymistä suoraan. Näin ohjelmoija voi muuttaa ja refaktoroida olion sisäisyyksiä ilman, että olion käyttäjän koodia tarvitsee muuttaa.

Käsittelimme kapseloinnin hallintaa luvussa 7: voimme käyttää `pub`-avainsanaa päättääksemme, mitkä moduulit, tyypit, funktiot ja metodit koodissamme ovat julkisia, ja oletuksena kaikki muu on yksityistä. Voimme esimerkiksi määritellä rakenteen `AveragedCollection`, jolla on kenttä `i32`-arvojen vektorille. Rakenteella voi olla myös kenttä, joka sisältää vektorin arvojen keskiarvon, eli keskiarvoa ei tarvitse laskea aina tarvittaessa. Toisin sanoen `AveragedCollection` välimuistittaa lasketun keskiarvon puolestamme. Listauksessa 18-1 on `AveragedCollection`-rakenteen määritelmä.

<Listing number="18-1" file-name="src/lib.rs" caption="`AveragedCollection`-rakenne, joka ylläpitää kokonaislukulistaa ja kokoelman kohteiden keskiarvoa">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-01/src/lib.rs}}
```

</Listing>

Rakenne on merkitty `pub`-avainsanalla, jotta muu koodi voi käyttää sitä, mutta rakenteen kentät pysyvät yksityisinä. Tämä on tässä tapauksessa tärkeää, koska haluamme varmistaa, että aina kun listaan lisätään tai siitä poistetaan arvo, myös keskiarvo päivittyy. Teemme tämän toteuttamalla rakenteelle metodit `add`, `remove` ja `average`, kuten listauksessa 18-2 näytetään.

<Listing number="18-2" file-name="src/lib.rs" caption="Julkisten metodien `add`, `remove` ja `average` toteutukset `AveragedCollection`-rakenteelle">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-02/src/lib.rs:here}}
```

</Listing>

Julkiset metodit `add`, `remove` ja `average` ovat ainoat tavat käyttää tai muokata tietoa `AveragedCollection`-instanssissa. Kun `add`-metodilla lisätään kohde `list`-kenttään tai `remove`-metodilla poistetaan kohde, kummankin toteutus kutsuu yksityistä `update_average`-metodia, joka päivittää myös `average`-kentän.

Jätämme `list`- ja `average`-kentät yksityisiksi, jotta ulkopuolinen koodi ei voi lisätä tai poistaa kohteita suoraan `list`-kentästä; muuten `average`-kenttä voisi mennä epäsynkkaan, kun `list` muuttuu. `average`-metodi palauttaa `average`-kentän arvon, jolloin ulkopuolinen koodi voi lukea keskiarvon mutta ei muuttaa sitä.

Koska olemme kapseloineet `AveragedCollection`-rakenteen toteutuksen yksityiskohdat, voimme helposti muuttaa esimerkiksi tietorakennetta tulevaisuudessa. Voisimme esimerkiksi käyttää `list`-kentässä `HashSet<i32>`-tyyppiä `Vec<i32>`-tyypin sijaan. Niin kauan kuin julkisten metodien `add`, `remove` ja `average` allekirjoitukset pysyvät samoina, `AveragedCollection`-tyyppiä käyttävän koodin ei tarvitse muuttua. Jos tekisimme `list`-kentästä julkisen, näin ei välttämättä olisi: `HashSet<i32>`- ja `Vec<i32>`-tyypeillä on eri metodit kohteiden lisäämiseen ja poistamiseen, joten ulkopuolinen koodi todennäköisesti joutuisi muuttumaan, jos se muokkaisi `list`-kenttää suoraan.

Jos kapselointi on pakollinen ominaisuus, jotta kieli katsottaisiin oliopohjaiseksi, Rust täyttää tämän vaatimuksen. Mahdollisuus käyttää `pub`-avainsanaa tai olla käyttämättä sitä eri koodin osissa mahdollistaa toteutuksen yksityiskohtien kapseloinnin.

### Periytyminen tyyppijärjestelmänä ja koodin jakamisena

_Periytyminen_ on mekanismi, jossa olio voi periä elementtejä toisen olion määritelmästä ja siten saada yläluokan tiedot ja käyttäytymisen ilman, että niitä tarvitsee määritellä uudelleen.

Jos kielen täytyy sisältää periytyminen ollakseen oliopohjainen, Rust ei ole sellainen kieli. Rakenteen, joka perii yläluokan kentät ja metoditoteutukset, määrittelyyn ei ole tapaa ilman makron käyttöä.

Jos olet tottunut käyttämään periytymistä ohjelmointityökalupakissasi, voit kuitenkin käyttää Rustissa muita ratkaisuja riippuen siitä, miksi alun perin tavoittelit periytymistä.

Valitsisit periytymisen kahdesta pääsyystä. Toinen on koodin uudelleenkäyttö: voit toteuttaa tietyn käyttäytymisen yhdelle tyypille, ja periytyminen mahdollistaa saman toteutuksen käytön eri tyypille. Voit tehdä tämän rajatusti Rust-koodissa käyttämällä trait-metodien oletustoteutuksia, jotka näimme listauksessa 10-14, kun lisäsimme oletustoteutuksen `summarize`-metodille `Summary`-traitissa. Jokaisella `Summary`-traitin toteuttavalla tyypillä olisi `summarize`-metodi käytettävissä ilman lisäkoodia. Tämä muistuttaa tilannetta, jossa yläluokalla on metodin toteutus ja sitä perivällä alaluokalla on sama metodin toteutus. Voimme myös ylikirjoittaa `summarize`-metodin oletustoteutuksen, kun toteutamme `Summary`-traitin, mikä muistuttaa alaluokan ylikirjoittavan yläluokalta perityn metodin toteutuksen.

Toinen syy periytymisen käyttöön liittyy tyyppijärjestelmään: mahdollistaa alatyypin käytön samoissa paikoissa kuin ylätyyppiä. Tätä kutsutaan myös _polymorfismiksi_, mikä tarkoittaa, että voit korvata useita olioita toisillaan ajonaikana, jos niillä on tiettyjä yhteisiä ominaisuuksia.

> ### Polymorfismi
>
> Monille ihmisille polymorfismi on synonyymi periytymiselle. Se on kuitenkin yleisempi käsite, joka viittaa koodiin, joka voi toimia useiden eri tyyppien datan kanssa. Periytymisessä nämä tyypit ovat yleensä alaluokkia.
>
> Rust käyttää sen sijaan geneerisyyttä abstrahoimaan eri mahdollisia tyyppejä ja trait-sidontoja asettaakseen rajoituksia sille, mitä näiden tyyppien täytyy tarjota. Tätä kutsutaan joskus _rajoitetuksi parametriseksi polymorfismiksi_.

Rust on valinnut erilaiset kompromissit tarjoamatta periytymistä. Periytyminen on usein vaarassa jakaa enemmän koodia kuin on tarpeen. Alaluokkien ei pitäisi aina jakaa kaikkia yläluokan ominaisuuksia, mutta periytymisessä ne tekevät niin. Tämä voi tehdä ohjelman suunnittelusta vähemmän joustavaa. Se tuo myös mahdollisuuden kutsua alaluokkien metodeja, jotka eivät ole järkeviä tai aiheuttavat virheitä, koska metodit eivät sovellu alaluokkaan. Lisäksi jotkin kielet sallivat vain _yksinkertaisen periytymisen_ (eli alaluokka voi periä vain yhdestä luokasta), mikä rajoittaa entisestään ohjelman suunnittelun joustavuutta.

Näistä syistä Rust ottaa erilaisen lähestymistavan ja käyttää trait-olioita periytymisen sijaan polymorfismin saavuttamiseksi ajonaikana. Katsotaan, miten trait-oliot toimivat.
