# Asynkronisen ohjelmoinnin perusteet: Async, Await, Futures ja Streams

Monet tietokoneelle antamamme tehtävät voivat kestää kauan. Olisi mukavaa, jos voisimme tehdä jotain muuta samalla, kun odotamme näiden pitkien prosessien valmistumista. Modernit tietokoneet tarjoavat kaksi tekniikkaa useamman kuin yhden toiminnon työstämiseen samanaikaisesti: rinnakkaisuuden ja samanaikaisuuden. Ohjelmien logiikka on kuitenkin kirjoitettu pääosin lineaarisesti. Haluaisimme pystyä määrittelemään, mitä operaatioita ohjelman tulisi suorittaa ja missä kohdissa funktio voisi pysähtyä ja jokin ohjelman toinen osa voisi sen sijaan suorittua, ilman että meidän tarvitsee etukäteen määritellä tarkasti jokaisen koodinpätkän suoritusjärjestystä ja -tapaa. _Asynkroninen ohjelmointi_ on abstraktio, jonka avulla voimme ilmaista koodimme mahdollisina pysäytyskohtina ja lopullisina tuloksina, ja joka hoitaa koordinoinnin yksityiskohdat puolestamme.

Tämä luku rakentuu luvun 16 säikeiden käytön päälle rinnakkaisuudessa ja samanaikaisuudessa esittelemällä vaihtoehtoisen tavan koodin kirjoittamiseen: Rustin futuret, streamit sekä `async`- ja `await`-syntaksi, joiden avulla voimme ilmaista, miten operaatiot voivat olla asynkronisia, ja kolmannen osapuolen crate:t, jotka toteuttavat asynkroniset ajoympäristöt: koodia, joka hallinnoi ja koordinoi asynkronisten operaatioiden suoritusta.

Tarkastellaan esimerkkiä. Oletetaan, että viet perhejuhlasta tekemääsi videota, mikä voi kestää minuuteista tunteihin. Videon vienti käyttää niin paljon CPU- ja GPU-tehoa kuin se voi. Jos sinulla olisi vain yksi CPU-ydin ja käyttöjärjestelmäsi ei keskeyttäisi vientiä ennen kuin se valmistuu — eli jos se suorittaisi viennin _synkronisesti_ — et voisi tehdä mitään muuta tietokoneellasi, kun tehtävä on käynnissä. Se olisi varsin turhauttava kokemus. Onneksi tietokoneesi käyttöjärjestelmä voi — ja tekee — keskeyttää viennin tarpeeksi usein näkymättömästi, jotta voit tehdä muuta työtä samanaikaisesti.

Oletetaan sitten, että lataat jonkun toisen jakamaa videota, mikä voi myös kestää kauan, mutta ei vie yhtä paljon CPU-aikaa. Tässä tapauksessa CPU:n täytyy odottaa, että data saapuu verkosta. Vaikka voit alkaa lukea dataa heti, kun se alkaa saapua, voi kestää jonkin aikaa, ennen kuin kaikki on perillä. Vaikka data olisi kokonaan paikalla, suuren videon lataaminen voi kestää ainakin sekunnin tai kaksi. Se ei ehkä kuulosta paljolta, mutta modernille prosessorille se on hyvin pitkä aika: se voi suorittaa miljardeja operaatioita sekunnissa. Taas käyttöjärjestelmäsi keskeyttää ohjelmasi näkymättömästi, jotta CPU voi tehdä muuta työtä odottaessaan verkkokutsun valmistumista.

Videon vienti on esimerkki _CPU-rajoitteisesta_ tai _laskentarajoitteisesta_ operaatiosta. Se on rajoitettu tietokoneen mahdollisella datankäsittelynopeudella CPU:ssa tai GPU:ssa ja sillä, kuinka suuren osan tästä nopeudesta operaatio voi käyttää. Videon lataus on esimerkki _I/O-rajoitteisesta_ operaatiosta, koska se on rajoitettu tietokoneen _syötteen ja tulosteen_ nopeudella; se voi edetä vain niin nopeasti kuin data voidaan lähettää verkon yli.

Molemmissa esimerkeissä käyttöjärjestelmän näkymättömät keskeytykset tarjoavat eräänlaisen samanaikaisuuden. Tämä samanaikaisuus tapahtuu kuitenkin vain koko ohjelman tasolla: käyttöjärjestelmä keskeyttää yhden ohjelman, jotta muut ohjelmat voivat tehdä työtä. Monissa tapauksissa, koska ymmärrämme ohjelmiamme paljon tarkemmin kuin käyttöjärjestelmä, voimme havaita samanaikaisuuden mahdollisuuksia, joita käyttöjärjestelmä ei näe.

Esimerkiksi jos rakennamme työkalua tiedostolatausten hallintaan, meidän pitäisi pystyä kirjoittamaan ohjelma niin, että yhden latauksen aloittaminen ei lukitse käyttöliittymää, ja käyttäjien pitäisi pystyä aloittamaan useita latauksia samanaikaisesti. Monet käyttöjärjestelmän verkko-API:t ovat kuitenkin _estäviä_; eli ne estävät ohjelman etenemisen, kunnes käsiteltävä data on täysin valmiina.

> Huom: Tämä on tapa, jolla _useimmat_ funktiokutsut toimivat, jos asiaa miettii. Termiä _estävä_ (blocking) käytetään kuitenkin yleensä tiedostoihin, verkkoon tai tietokoneen muihin resursseihin liittyvistä funktiokutsuista, koska näissä tapauksissa yksittäinen ohjelma hyötyisi siitä, että operaatio olisi _ei-estävä_.

Voisimme välttää pääsäikeen estämisen luomalla erillisen säikeen jokaisen tiedoston lataamiseen. Näiden säikeiden käyttämien järjestelmäresurssien yläraja muodostuisi kuitenkin lopulta ongelmaksi. Olisi parempi, jos kutsu ei estäisi alun perinkään, vaan voisimme määritellä joukon tehtäviä, jotka haluamme ohjelman suorittavan, ja antaa ajoympäristön valita parhaan järjestyksen ja tavan niiden suorittamiseen.

Juuri tämän Rustin _async_-abstraktio (lyhenne sanasta _asynchronous_, eli asynkroninen) tarjoaa. Tässä luvussa opit kaiken asyncista seuraavien aiheiden kautta:

- Kuinka käyttää Rustin `async`- ja `await`-syntaksia ja suorittaa asynkronisia funktioita ajoympäristössä
- Kuinka käyttää async-mallia ratkaisemaan joitain samoja haasteita, joita tarkastelimme luvussa 16
- Kuinka monisäikeisyys ja async tarjoavat toisiaan täydentäviä ratkaisuja, joita voi monissa tapauksissa yhdistellä

Ennen kuin näemme, miten async toimii käytännössä, meidän täytyy kuitenkin tehdä lyhyt poikkeus ja käsitellä rinnakkaisuuden ja samanaikaisuuden erot.

## Rinnakkaisuus ja samanaikaisuus

Olemme tähän mennessä käsitelleet rinnakkaisuutta ja samanaikaisuutta lähes synonyymeinä. Nyt meidän täytyy erottaa ne tarkemmin, koska erot tulevat esiin, kun alamme työskennellä.

Ajatellaan eri tapoja, joilla tiimi voi jakaa työn ohjelmistoprojektissa. Voit antaa yhdelle jäsenelle useita tehtäviä, antaa jokaiselle jäsenelle yhden tehtävän tai käyttää näiden kahden lähestymistavan yhdistelmää.

Kun yksittäinen henkilö työskentelee usean eri tehtävän parissa ennen kuin yksikään niistä on valmis, kyseessä on _samanaikaisuus_. Yksi tapa toteuttaa samanaikaisuus on samankaltainen kuin kaksi eri projektia checkoutattuna tietokoneellesi: kun kyllästyt tai jäät jumiin yhdessä projektissa, vaihdat toiseen. Olet vain yksi ihminen, joten et voi edistää molempia tehtäviä täsmälleen samalla hetkellä, mutta voit moniajaa ja edistää yhtä kerrallaan vaihtamalla niiden välillä (katso kuva 17-1).

<figure>

<img src="img/trpl17-01.svg" class="center" alt="A diagram with stacked boxes labeled Task A and Task B, with diamonds in them representing subtasks. Arrows point from A1 to B1, B1 to A2, A2 to B2, B2 to A3, A3 to A4, and A4 to B3. The arrows between the subtasks cross the boxes between Task A and Task B." />

<figcaption>Kuva 17-1: Samanaikainen työnkulku, jossa vaihdetaan tehtävän A ja tehtävän B välillä</figcaption>

</figure>

Kun tiimi jakaa tehtäväryhmän niin, että jokainen jäsen ottaa yhden tehtävän ja työskentelee sen parissa yksin, kyseessä on _rinnakkaisuus_. Jokainen tiimin jäsen voi edistyä täsmälleen samanaikaisesti (katso kuva 17-2).

<figure>

<img src="img/trpl17-02.svg" class="center" alt="A diagram with stacked boxes labeled Task A and Task B, with diamonds in them representing subtasks. Arrows point from A1 to A2, A2 to A3, A3 to A4, B1 to B2, and B2 to B3. No arrows cross between the boxes for Task A and Task B." />

<figcaption>Kuva 17-2: Rinnakkainen työnkulku, jossa tehtävän A ja tehtävän B työ etenee itsenäisesti</figcaption>

</figure>

Molemmissa työnkuluissa saatat joutua koordinoimaan eri tehtävien välillä. Ehkä luulit, että yhdelle henkilölle annettu tehtävä on täysin riippumaton muiden työstä, mutta se vaatiikin toisen tiimin jäsenen tehtävän valmistumisen ensin. Osa työstä voitiin tehdä rinnakkain, mutta osa oli itse asiassa _sarjallista_: se voitiin tehdä vain sarjana, yksi tehtävä toisen jälkeen, kuten kuvassa 17-3.

<figure>

<img src="img/trpl17-03.svg" class="center" alt="A diagram with stacked boxes labeled Task A and Task B, with diamonds in them representing subtasks. In Task A, arrows point from A1 to A2, from A2 to a pair of thick vertical lines like a “pause” symbol, and from that symbol to A3. In task B, arrows point from B1 to B2, from B2 to B3, from B3 to A3, and from B3 to B4." />

<figcaption>Kuva 17-3: Osittain rinnakkainen työnkulku, jossa tehtävän A ja tehtävän B työ etenee itsenäisesti, kunnes tehtävä A3 on estynyt tehtävän B3 tulosten takia.</figcaption>

</figure>

Vastaavasti saatat huomata, että yksi omista tehtävistäsi riippuu toisesta omasta tehtävästäsi. Nyt samanaikainen työsi on myös muuttunut sarjalliseksi.

Rinnakkaisuus ja samanaikaisuus voivat myös leikata toisiinsa. Jos huomaat, että kollega on jumissa, kunnes saat yhden tehtävistäsi valmiiksi, keskityt todennäköisesti kaikki ponnistelusi siihen tehtävään ”vapauttaaksesi” kollegasi. Sinä ja työkaverisi ette enää voi työskennellä rinnakkain, ettekä myöskään samanaikaisesti omien tehtävienne parissa.

Sama perusdynamiikka tulee esiin ohjelmistoissa ja laitteistossa. Koneella, jossa on yksi CPU-ydin, CPU voi suorittaa vain yhden operaation kerrallaan, mutta se voi silti työskennellä samanaikaisesti. Työkaluja kuten säikeitä, prosesseja ja asyncia käyttäen tietokone voi keskeyttää yhden toiminnon ja vaihtaa muihin ennen kuin se palaa lopulta takaisin ensimmäiseen. Koneella, jossa on useita CPU-ytimiä, se voi myös tehdä työtä rinnakkain. Yksi ydin voi suorittaa yhtä tehtävää, kun toinen ydin suorittaa täysin erillistä tehtävää, ja nämä operaatiot tapahtuvat todella samanaikaisesti.

Async-koodin suorittaminen Rustissa tapahtuu yleensä samanaikaisesti. Riippuen laitteistosta, käyttöjärjestelmästä ja käyttämästämme async-ajoympäristöstä (ajoympäristöistä puhumme pian lisää), tämä samanaikaisuus voi myös hyödyntää rinnakkaisuutta taustalla.

Nyt sukellamme siihen, miten async-ohjelmointi Rustissa oikeasti toimii.
