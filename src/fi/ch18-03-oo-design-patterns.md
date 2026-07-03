## Oliopohjaisen suunnittelumallin toteuttaminen

_tilamalli_ on oliopohjainen suunnittelumalli. Mallin ydin on, että määrittelemme joukon tiloja, joissa arvo voi sisäisesti olla. Tilat edustetaan joukolla _tilaolioita_, ja arvon käyttäytyminen muuttuu sen tilan mukaan. Käymme läpi esimerkin blogikirjoitus-rakenteesta, jolla on kenttä tilan säilyttämiseen; tila on tilaolio joukosta ”luonnos”, ”tarkistus” tai ”julkaistu”.

Tilaoliot jakavat toiminnallisuutta: Rustissa käytämme tietysti rakenteita ja traitteja objektien ja periytymisen sijaan. Jokainen tilaolio vastaa omasta käyttäytymisestään ja siitä, milloin sen pitäisi siirtyä toiseen tilaan. Arvo, joka sisältää tilaolion, ei tiedä tilojen eri käyttäytymisestä tai siirtymisajankohdista.

Tilamallin etu on, että kun ohjelman liiketoimintavaatimukset muuttuvat, emme joudu muuttamaan tilaa sisältävän arvon koodia tai arvoa käyttävän koodin koodia. Meidän tarvitsee päivittää vain yhden tilaolion sisäinen koodi muuttaaksemme sen sääntöjä tai ehkä lisätäksemme uusia tilaolioita.

Ensin toteutamme tilamallin perinteisemmällä oliopohjaisella tavalla. Sitten käytämme lähestymistapaa, joka on luontevampi Rustissa. Aloitetaan toteuttamaan blogikirjoituksen työnkulkua vaiheittain tilamallia käyttäen.

Lopullinen toiminnallisuus näyttää tältä:

1. Blogikirjoitus alkaa tyhjänä luonnoksena.
1. Kun luonnos on valmis, kirjoituksen tarkistus pyydetään.
1. Kun kirjoitus hyväksytään, se julkaistaan.
1. Vain julkaistut blogikirjoitukset palauttavat tulostettavaa sisältöä, jotta hyväksymättömät kirjoitukset eivät voi vahingossa julkaista.

Mikä tahansa muu kirjoitukseen tehty muutosyritys ei saa vaikuttaa mihinkään. Jos esimerkiksi yritämme hyväksyä luonnoskirjoituksen ennen kuin olemme pyytäneet tarkistusta, kirjoituksen pitäisi pysyä julkaisemattomana luonnoksena.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-traditional-object-oriented-attempt"></a>

### Perinteisen oliopohjaisen tyylin yritys

Samaan ongelmaan on äärettömän monta tapaa rakentaa koodi, jokaisella eri kompromisseilla. Tämän osion toteutus on perinteisempää oliopohjaista tyyliä, joka on mahdollista kirjoittaa Rustissa, mutta ei hyödynnä kaikkia Rustin vahvuuksia. Myöhemmin esittelemme toisen ratkaisun, joka käyttää edelleen oliopohjaista suunnittelumallia mutta on rakennettu tavalla, joka saattaa näyttää vähemmän tutulta oliopohjaista kokemusta omaaville ohjelmoijille. Vertailemme kahta ratkaisua kokeaksemme kompromissit, kun Rust-koodia suunnitellaan eri tavalla kuin muiden kielten koodia.

Listaus 18-11 näyttää tämän työnkulun koodimuodossa: tämä on esimerkki `blog`-nimisen kirjastokrateen API:n käytöstä. Tämä ei vielä käänny, koska emme ole toteuttaneet `blog`-kratea.

<Listing number="18-11" file-name="src/main.rs" caption="Koodi, joka demonstroi haluttua käyttäytymistä, jonka haluamme `blog`-krateen">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-11/src/main.rs:all}}
```

</Listing>

Haluamme antaa käyttäjän luoda uuden luonnosblogikirjoituksen `Post::new`-funktiolla. Haluamme sallia tekstin lisäämisen blogikirjoitukseen. Jos yritämme hakea kirjoituksen sisältöä heti, ennen hyväksyntää, emme saa tekstiä, koska kirjoitus on vielä luonnos. Olemme lisänneet koodiin `assert_eq!`-makron demonstrointitarkoituksessa. Erinomainen yksikkötesti tälle olisi varmistaa, että luonnosblogikirjoitus palauttaa tyhjän merkkijonon `content`-metodista, mutta emme kirjoita testejä tähän esimerkkiin.

Seuraavaksi haluamme mahdollistaa kirjoituksen tarkistuksen pyytämisen ja haluamme, että `content` palauttaa tyhjän merkkijonon odottaessaan tarkistusta. Kun kirjoitus saa hyväksynnän, se julkaistaan, eli kirjoituksen teksti palautetaan kun `content` kutsutaan.

Huomaa, että ainoa tyyppi, jonka kanssa olemme vuorovaikutuksessa kratesta, on `Post`-tyyppi. Tämä tyyppi käyttää tilamallia ja sisältää arvon, joka on yksi kolmesta tilaoliosta edustaen eri tiloja, joissa kirjoitus voi olla — luonnos, tarkistus tai julkaistu. Siirtyminen tilasta toiseen hallitaan sisäisesti `Post`-tyypin sisällä. Tilat muuttuvat vastauksena kirjastomme käyttäjien `Post`-instanssilla kutsumiin metodeihin, mutta heidän ei tarvitse hallita tilamuutoksia suoraan. Lisäksi käyttäjät eivät voi tehdä virheitä tilojen kanssa, kuten julkaista kirjoitusta ennen tarkistusta.

<!-- Old headings. Do not remove or links may break. -->

<a id="defining-post-and-creating-a-new-instance-in-the-draft-state"></a>

#### `Post`-rakenteen määrittely ja uuden instanssin luominen

Aloitetaan kirjaston toteutus! Tiedämme tarvitsevamme julkisen `Post`-rakenteen, joka sisältää sisältöä, joten aloitamme rakenteen määritelmästä ja siihen liittyvästä julkisesta `new`-funktiosta `Post`-instanssin luomiseen, kuten listauksessa 18-12 näytetään. Teemme myös yksityisen `State`-traitin, joka määrittelee käyttäytymisen, joka kaikilla `Post`-rakenteen tilaolioilla täytyy olla.

Sitten `Post` sisältää trait-olion `Box<dyn State>` `Option<T>`-tyypin sisällä yksityisessä `state`-kentässä tilaolion säilyttämiseen. Näet hetken kuluttua, miksi `Option<T>` on tarpeen.

<Listing number="18-12" file-name="src/lib.rs" caption="`Post`-rakenteen määritelmä ja `new`-funktio uuden `Post`-instanssin luomiseen, `State`-trait ja `Draft`-rakenne">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-12/src/lib.rs}}
```

</Listing>

`State`-trait määrittelee eri kirjoitustilojen jakaman käyttäytymisen. Tilaoliot ovat `Draft`, `PendingReview` ja `Published`, ja ne kaikki toteuttavat `State`-traitin. Toistaiseksi traitilla ei ole metodeja, ja aloitamme määrittelemällä vain `Draft`-tilan, koska siinä tilassa kirjoituksen pitää alkaa.

Kun luomme uuden `Post`-instanssin, asetamme sen `state`-kentän `Some`-arvoksi, joka sisältää `Box`-osoittimen. Tämä `Box` osoittaa uuteen `Draft`-rakenteen instanssiin. Tämä varmistaa, että aina kun luomme uuden `Post`-instanssin, se alkaa luonnoksena. Koska `Post`-rakenteen `state`-kenttä on yksityinen, `Post`-instanssia ei voi luoda missään muussa tilassa! `Post::new`-funktiossa asetamme `content`-kentän uudeksi tyhjäksi `String`-arvoksi.

#### Kirjoituksen sisällön tekstin tallentaminen

Näimme listauksessa 18-11, että haluamme pystyä kutsumaan `add_text`-nimistä metodia ja välittämään sille `&str`-viitteen, joka lisätään blogikirjoituksen tekstisisällöksi. Toteutamme tämän metodina sen sijaan, että paljastaisimme `content`-kentän `pub`-avainsanalla, jotta voimme myöhemmin toteuttaa metodin, joka hallitsee `content`-kentän datan lukemista. `add_text`-metodi on melko suoraviivainen, joten lisätään toteutus listauksessa 18-13 `impl Post` -lohkoon.

<Listing number="18-13" file-name="src/lib.rs" caption="`add_text`-metodin toteutus tekstin lisäämiseksi kirjoituksen `content`-kenttään">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-13/src/lib.rs:here}}
```

</Listing>

`add_text`-metodi ottaa muuttuvan viitteen `self`:ään, koska muutamme `Post`-instanssia, jolla kutsumme `add_text`-metodia. Kutsumme sitten `push_str`-metodia `content`-kentän `String`-arvolla ja välitämme `text`-argumentin lisättäväksi tallennettuun `content`-arvoon. Tämä käyttäytyminen ei riipu kirjoituksen tilasta, joten se ei ole osa tilamallia. `add_text`-metodi ei ole lainkaan vuorovaikutuksessa `state`-kentän kanssa, mutta se on osa käyttäytymistä, jota haluamme tukea.

<!-- Old headings. Do not remove or links may break. -->

<a id="ensuring-the-content-of-a-draft-post-is-empty"></a>

#### Luonnoskirjoituksen sisällön tyhjyyden varmistaminen

Vaikka olisimme kutsuneet `add_text`-metodia ja lisänneet sisältöä kirjoitukseen, haluamme silti `content`-metodin palauttavan tyhjän merkkijonoviitteen, koska kirjoitus on vielä luonnostilassa, kuten listauksen 18-11 ensimmäinen `assert_eq!` osoittaa. Toteutetaan toistaiseksi `content`-metodi yksinkertaisimmalla tavalla, joka täyttää tämän vaatimuksen: palauttamalla aina tyhjän merkkijonoviitteen. Muutamme tämän myöhemmin, kun toteutamme kyvykkyyden muuttaa kirjoituksen tilaa julkaistavaksi. Toistaiseksi kirjoitukset voivat olla vain luonnostilassa, joten kirjoituksen sisällön pitäisi aina olla tyhjä. Listaus 18-14 näyttää tämän väliaikaisen toteutuksen.

<Listing number="18-14" file-name="src/lib.rs" caption="Väliaikaisen toteutuksen lisääminen `content`-metodille `Post`-rakenteella, joka palauttaa aina tyhjän merkkijonoviitteen">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-14/src/lib.rs:here}}
```

</Listing>

Tämän lisätyn `content`-metodin myötä kaikki listauksessa 18-11 ensimmäiseen `assert_eq!`-kutsuun asti toimii tarkoitetulla tavalla.

<!-- Old headings. Do not remove or links may break. -->

<a id="requesting-a-review-of-the-post-changes-its-state"></a>
<a id="requesting-a-review-changes-the-posts-state"></a>

#### Tarkistuksen pyytäminen, joka muuttaa kirjoituksen tilaa

Seuraavaksi meidän täytyy lisätä toiminnallisuus kirjoituksen tarkistuksen pyytämiseen, mikä pitäisi muuttaa sen tilan `Draft`-tilasta `PendingReview`-tilaan. Listaus 18-15 näyttää tämän koodin.

<Listing number="18-15" file-name="src/lib.rs" caption="`request_review`-metodien toteutus `Post`-rakenteella ja `State`-traitilla">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-15/src/lib.rs:here}}
```

</Listing>

Annamme `Post`-rakenteelle julkisen `request_review`-nimisen metodin, joka ottaa muuttuvan viitteen `self`:ään. Kutsumme sitten sisäistä `request_review`-metodia `Post`-rakenteen nykyisellä tilalla, ja tämä toinen `request_review`-metodi kuluttaa nykyisen tilan ja palauttaa uuden tilan.

Lisäämme `request_review`-metodin `State`-traitiin; kaikkien traitin toteuttavien tyyppien täytyy nyt toteuttaa `request_review`-metodi. Huomaa, että metodin ensimmäisenä parametrina on `self: Box<Self>` sen sijaan, että olisi `self`, `&self` tai `&mut self`. Tämä syntaksi tarkoittaa, että metodi on kelvollinen vain kun sitä kutsutaan `Box`-osoittimella, joka sisältää tyypin. Tämä syntaksi ottaa omistajuuden `Box<Self>`-arvosta, mitätöiden vanhan tilan, jotta `Post`-rakenteen tilan arvo voi muuttua uudeksi tilaksi.

Vanhan tilan kuluttamiseksi `request_review`-metodin täytyy ottaa omistajuus tilan arvosta. Tässä `Post`-rakenteen `state`-kentän `Option` tulee kuvaan: kutsumme `take`-metodia ottamaan `Some`-arvon `state`-kentästä ja jättämään sen paikalle `None`-arvon, koska Rust ei salli tyhjäksi jääneitä kenttiä rakenteissa. Näin voimme siirtää `state`-arvon pois `Post`-rakenteesta lainaamisen sijaan. Asetamme sitten kirjoituksen `state`-arvon tämän operaation tulokseksi.

Meidän täytyy asettaa `state` väliaikaisesti `None`-arvoksi sen sijaan, että asettaisimme sen suoraan koodilla kuten `self.state = self.state.request_review();` saadaksemme omistajuuden `state`-arvosta. Tämä varmistaa, että `Post` ei voi käyttää vanhaa `state`-arvoa sen jälkeen, kun olemme muuttaneet sen uudeksi tilaksi.

`Draft`-rakenteen `request_review`-metodi palauttaa uuden, laatikkoon pakatun instanssin uudesta `PendingReview`-rakenteesta, joka edustaa tilaa, jossa kirjoitus odottaa tarkistusta. `PendingReview`-rakenne toteuttaa myös `request_review`-metodin, mutta ei tee muunnoksia. Sen sijaan se palauttaa itsensä, koska kun pyydämme tarkistusta kirjoitukselle, joka on jo `PendingReview`-tilassa, sen pitäisi pysyä `PendingReview`-tilassa.

Nyt voimme alkaa nähdä tilamallin edut: `Post`-rakenteen `request_review`-metodi on sama riippumatta sen `state`-arvosta. Jokainen tila vastaa omista säännöistään.

Jätämme `Post`-rakenteen `content`-metodin ennalleen palauttaen tyhjän merkkijonoviitteen. Voimme nyt olla `Post`-instanssi `PendingReview`-tilassa sekä `Draft`-tilassa, mutta haluamme saman käyttäytymisen `PendingReview`-tilassa. Listaus 18-11 toimii nyt toiseen `assert_eq!`-kutsuun asti!

<!-- Old headings. Do not remove or links may break. -->

<a id="adding-the-approve-method-that-changes-the-behavior-of-content"></a>
<a id="adding-approve-to-change-the-behavior-of-content"></a>

#### `approve`-metodin lisääminen `content`-metodin käyttäytymisen muuttamiseksi

`approve`-metodi on samanlainen kuin `request_review`-metodi: se asettaa `state`-kentän arvoksi sen, jonka nykyinen tila sanoo sen pitävän olla kun tila hyväksytään, kuten listauksessa 18-16 näytetään.

<Listing number="18-16" file-name="src/lib.rs" caption="`approve`-metodin toteutus `Post`-rakenteella ja `State`-traitilla">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-16/src/lib.rs:here}}
```

</Listing>

Lisäämme `approve`-metodin `State`-traitiin ja uuden rakenteen, joka toteuttaa `State`-traitin, `Published`-tilan.

Samalla tavalla kuin `PendingReview`-rakenteen `request_review` toimii, jos kutsumme `approve`-metodia `Draft`-rakenteella, sillä ei ole vaikutusta, koska `approve` palauttaa `self`:n. Kun kutsumme `approve`-metodia `PendingReview`-rakenteella, se palauttaa uuden, laatikkoon pakatun instanssin `Published`-rakenteesta. `Published`-rakenne toteuttaa `State`-traitin, ja sekä `request_review`- että `approve`-metodille se palauttaa itsensä, koska kirjoituksen pitäisi pysyä `Published`-tilassa näissä tapauksissa.

Nyt meidän täytyy päivittää `Post`-rakenteen `content`-metodi. Haluamme `content`-metodin palauttaman arvon riippuvan `Post`-rakenteen nykyisestä tilasta, joten annamme `Post`-rakenteen delegoida `content`-metodille, joka on määritelty sen `state`-kentässä, kuten listauksessa 18-17 näytetään.

<Listing number="18-17" file-name="src/lib.rs" caption="`Post`-rakenteen `content`-metodin päivittäminen delegoimaan `State`-traitin `content`-metodille">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-17/src/lib.rs:here}}
```

</Listing>

Koska tavoitteena on pitää kaikki nämä säännöt `State`-traitin toteuttavien rakenteiden sisällä, kutsumme `content`-metodia `state`-kentän arvolla ja välitämme kirjoitusinstanssin (eli `self`) argumenttina. Palautamme sitten arvon, jonka `state`-arvon `content`-metodin käyttö palauttaa.

Kutsumme `as_ref`-metodia `Option`-tyypillä, koska haluamme viitteen `Option`-tyypin sisällä olevaan arvoon omistajuuden sijaan. Koska `state` on `Option<Box<dyn State>>`, kun kutsumme `as_ref`-metodia, palautuu `Option<&Box<dyn State>>`. Jos emme kutsuisi `as_ref`-metodia, saisimme virheen, koska emme voi siirtää `state`-arvoa pois funktion parametrin lainatusta `&self`-viitteestä.

Kutsumme sitten `unwrap`-metodia, joka emme tiedä koskaan panikoivan, koska tiedämme `Post`-rakenteen metodien varmistavan, että `state` sisältää aina `Some`-arvon kun nämä metodit ovat valmiit. Tämä on yksi tapauksista, joista puhuimme luvun 9 [”Kun sinulla on enemmän tietoa kuin kääntäjällä”][more-info-than-rustc]<!-- ignore --> -osiossa, kun tiedämme `None`-arvon olevan mahdoton, vaikka kääntäjä ei pysty sitä ymmärtämään.

Tässä vaiheessa, kun kutsumme `content`-metodia `&Box<dyn State>`-arvolla, dereferointipakotus vaikuttaa `&`- ja `Box`-osoittimiin, joten `content`-metodia kutsutaan lopulta tyypillä, joka toteuttaa `State`-traitin. Tämä tarkoittaa, että meidän täytyy lisätä `content` `State`-traitin määritelmään, ja sinne asetamme logiikan sille, mitä sisältöä palautetaan riippuen siitä, mikä tila meillä on, kuten listauksessa 18-18 näytetään.

<Listing number="18-18" file-name="src/lib.rs" caption="`content`-metodin lisääminen `State`-traitiin">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-18/src/lib.rs:here}}
```

</Listing>

Lisäämme `content`-metodille oletustoteutuksen, joka palauttaa tyhjän merkkijonoviitteen. Tämä tarkoittaa, että emme tarvitse toteuttaa `content`-metodia `Draft`- ja `PendingReview`-rakenteille. `Published`-rakenne ylikirjoittaa `content`-metodin ja palauttaa arvon `post.content`-kentästä. Vaikka kätevää, `State`-traitin `content`-metodin käyttäminen `Post`-rakenteen sisällön määrittämiseen hämärtää rajaa `State`-traitin ja `Post`-rakenteen vastuiden välillä.

Huomaa, että tarvitsemme elinaikaannotaatiot tälle metodille, kuten käsittelimme luvussa 10. Otamme viitteen `post`-argumenttiin ja palautamme viitteen osaan kyseisestä `post`-argumentista, joten palautetun viitteen elinaika liittyy `post`-argumentin elinaikaan.

Ja olemme valmiit — koko listaus 18-11 toimii nyt! Olemme toteuttaneet tilamallin blogikirjoituksen työnkulun säännöillä. Sääntöihin liittyvä logiikka asuu tilaolioissa sen sijaan, että se olisi hajautettu ympäri `Post`-rakennetta.

> ### Miksi ei luettelotyyppiä?
>
> Olet ehkä miettinyt, miksi emme käyttäneet luettelotyyppiä eri mahdollisilla kirjoitustiloilla variantteina. Se on varmasti mahdollinen ratkaisu; kokeile sitä ja vertaa lopputuloksia nähdäksesi kumman pidät parempana! Yksi luettelotyypin käytön haittapuoli on, että jokaisessa paikassa, joka tarkistaa luettelotyypin arvon, tarvitaan `match`-lauseke tai vastaava käsittelemään jokainen mahdollinen variantti. Tämä voi tulla toistuvammaksi kuin tämä trait-olio-ratkaisu.

<!-- Old headings. Do not remove or links may break. -->

<a id="trade-offs-of-the-state-pattern"></a>

#### Tilamallin arviointi

Olemme osoittaneet, että Rust pystyy toteuttamaan oliopohjaisen tilamallin kapseloimaan erilaiset käyttäytymiset, joita kirjoituksella pitäisi olla kussakin tilassa. `Post`-rakenteen metodit eivät tiedä eri käyttäytymisistä. Koodin organisoinnin ansiosta meidän tarvitsee katsoa vain yhteen paikkaan tietääksemme eri tavat, joilla julkaistu kirjoitus voi käyttäytyä: `Published`-rakenteen `State`-traitin toteutus.

Jos loisimme vaihtoehtoisen toteutuksen, joka ei käyttäisi tilamallia, voisimme sen sijaan käyttää `match`-lausekkeita `Post`-rakenteen metodeissa tai jopa `main`-koodissa, joka tarkistaa kirjoituksen tilan ja muuttaa käyttäytymistä näissä paikoissa. Tämä tarkoittaisi, että meidän pitäisi katsoa useita paikkoja ymmärtääksemme kaikki seuraukset siitä, että kirjoitus on julkaistussa tilassa.

Tilamallin kanssa `Post`-rakenteen metodit ja paikat, joissa käytämme `Post`-rakennetta, eivät tarvitse `match`-lausekkeita, ja uuden tilan lisäämiseksi meidän tarvitsee vain lisätä uusi rakenne ja toteuttaa trait-metodit kyseiselle rakenteelle yhdessä paikassa.

Tilamallia käyttävä toteutus on helppo laajentaa lisätoiminnallisuudella. Nähdäksesi tilamallia käyttävän koodin ylläpidon yksinkertaisuuden, kokeile muutamia näistä ehdotuksista:

- Lisää `reject`-metodi, joka muuttaa kirjoituksen tilan `PendingReview`-tilasta takaisin `Draft`-tilaan.
- Vaadi kaksi `approve`-kutsua ennen kuin tila voi muuttua `Published`-tilaksi.
- Salli käyttäjien lisätä tekstisisältöä vain kun kirjoitus on `Draft`-tilassa.
  Vihje: anna tilaolion vastata siitä, mikä sisällössä saattaa muuttua, mutta älä anna sen vastata `Post`-rakenteen muokkaamisesta.

Yksi tilamallin haittapuoli on, että koska tilat toteuttavat siirtymät tilojen välillä, jotkin tilat ovat kytkettyjä toisiinsa. Jos lisäisimme uuden tilan `PendingReview`- ja `Published`-tilojen väliin, kuten `Scheduled`, meidän pitäisi muuttaa `PendingReview`-rakenteen koodia siirtymään `Scheduled`-tilaan sen sijaan. Olisi vähemmän työtä, jos `PendingReview`-rakenteen ei tarvitsisi muuttua uuden tilan lisäämisen yhteydessä, mutta se tarkoittaisi siirtymistä toiseen suunnittelumalliin.

Toinen haittapuoli on, että olemme monistaneet logiikkaa. Monistuksen poistamiseksi voisimme yrittää tehdä oletustoteutukset `request_review`- ja `approve`-metodeille `State`-traitissa, jotka palauttavat `self`:n. Tämä ei kuitenkaan toimisi: kun käytämme `State`-traitia trait-oliona, trait ei tiedä tarkalleen, mikä konkreettinen `self` on, joten palautustyyppi ei ole tiedossa käännösaikana. (Tämä on yksi dyn-yhteensopivuussäännöistä, joista mainittiin aiemmin.)

Muuta monistusta ovat samanlaiset `request_review`- ja `approve`-metodien toteutukset `Post`-rakenteella. Molemmat metodit käyttävät `Option::take`-metodia `Post`-rakenteen `state`-kentällä, ja jos `state` on `Some`, ne delegoivat käärityn arvon saman metodin toteutukselle ja asettavat `state`-kentän uudeksi arvoksi tuloksen. Jos `Post`-rakenteella olisi paljon tämän kaavan mukaisia metodeja, voisimme harkita makron määrittelyä toiston poistamiseksi (katso luvun 20 [”Makrot”][macros]<!-- ignore --> -osio).

Toteuttamalla tilamallin täsmälleen niin kuin se on määritelty oliopohjaisille kielille, emme hyödynnä Rustin vahvuuksia niin täysin kuin voisimme. Katsotaan muutoksia, joita voimme tehdä `blog`-krateen, jotta virheelliset tilat ja siirtymät muuttuvat käännösaikaisiksi virheiksi.

### Tilojen ja käyttäytymisen koodaus tyyppeinä

Näytämme, miten tilamalli voidaan ajatella uudelleen saadaksemme erilaisen joukon kompromisseja. Sen sijaan, että kapseloisimme tilat ja siirtymät kokonaan niin, ettei ulkopuolinen koodi tiedä niistä mitään, koodaamme tilat eri tyyppeihin. Näin Rustin tyyppitarkistusjärjestelmä estää yritykset käyttää luonnoskirjoituksia paikoissa, joissa sallitaan vain julkaistut kirjoitukset, antamalla kääntäjävirheen.

Tarkastellaan listauksen 18-11 `main`-funktion ensimmäistä osaa:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-11/src/main.rs:here}}
```

</Listing>

Sallimme edelleen uusien kirjoitusten luomisen luonnostilassa `Post::new`-funktiolla ja tekstin lisäämisen kirjoituksen sisältöön. Sen sijaan, että luonnoskirjoituksella olisi `content`-metodi, joka palauttaa tyhjän merkkijonon, teemme niin, ettei luonnoskirjoituksilla ole `content`-metodia lainkaan. Näin, jos yritämme hakea luonnoskirjoituksen sisältöä, saamme kääntäjävirheen, joka kertoo metodin olevan olematon. Näin on mahdotonta vahingossa näyttää luonnoskirjoituksen sisältöä tuotannossa, koska sellainen koodi ei edes käänny. Listaus 18-19 näyttää `Post`- ja `DraftPost`-rakenteiden määritelmät sekä metodit kummallekin.

<Listing number="18-19" file-name="src/lib.rs" caption="`Post`-rakenne `content`-metodilla ja `DraftPost`-rakenne ilman `content`-metodia">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-19/src/lib.rs}}
```

</Listing>

Sekä `Post`- että `DraftPost`-rakenteilla on yksityinen `content`-kenttä, joka tallentaa blogikirjoituksen tekstin. Rakenteilla ei ole enää `state`-kenttää, koska siirrämme tilan koodauksen rakenteiden tyyppeihin. `Post`-rakenne edustaa julkaistua kirjoitusta, ja sillä on `content`-metodi, joka palauttaa `content`-kentän arvon.

Meillä on edelleen `Post::new`-funktio, mutta sen sijaan, että se palauttaisi `Post`-instanssin, se palauttaa `DraftPost`-instanssin. Koska `content` on yksityinen eikä ole funktioita, jotka palauttavat `Post`-tyypin, `Post`-instanssia ei voi luoda tällä hetkellä.

`DraftPost`-rakenteella on `add_text`-metodi, joten voimme lisätä tekstiä `content`-kenttään kuten ennenkin, mutta huomaa, että `DraftPost`-rakenteella ei ole määritelty `content`-metodia! Nyt ohjelma varmistaa, että kaikki kirjoitukset alkavat luonnoskirjoituksina, eikä luonnoskirjoituksilla ole sisältöään näytettävissä. Mikä tahansa yritys kiertää nämä rajoitukset johtaa kääntäjävirheeseen.

<!-- Old headings. Do not remove or links may break. -->

<a id="implementing-transitions-as-transformations-into-different-types"></a>

Miten siis saamme julkaistun kirjoituksen? Haluamme pakottaa säännön, että luonnoskirjoituksen täytyy tarkistaa ja hyväksyä ennen julkaisemista. Tarkistusta odottavan tilan kirjoituksen ei pitäisi silti näyttää sisältöä. Toteutamme nämä rajoitukset lisäämällä toisen rakenteen, `PendingReviewPost`, määrittelemällä `request_review`-metodin `DraftPost`-rakenteelle palauttamaan `PendingReviewPost`-rakenteen ja määrittelemällä `approve`-metodin `PendingReviewPost`-rakenteelle palauttamaan `Post`-rakenteen, kuten listauksessa 18-20 näytetään.

<Listing number="18-20" file-name="src/lib.rs" caption="`PendingReviewPost`, joka luodaan kutsumalla `request_review`-metodia `DraftPost`-rakenteella, ja `approve`-metodi, joka muuttaa `PendingReviewPost`-rakenteen julkaistuksi `Post`-rakenteeksi">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-20/src/lib.rs:here}}
```

</Listing>

`request_review`- ja `approve`-metodit ottavat omistajuuden `self`:stä, kuluttaen `DraftPost`- ja `PendingReviewPost`-instanssit ja muuttaen ne `PendingReviewPost`- ja julkaistuksi `Post`-rakenteeksi. Näin meillä ei jää jäljelle `DraftPost`-instansseja sen jälkeen, kun olemme kutsuneet niillä `request_review`-metodia, ja niin edelleen. `PendingReviewPost`-rakenteella ei ole määritelty `content`-metodia, joten sen sisällön lukeminen johtaa kääntäjävirheeseen, kuten `DraftPost`-rakenteella. Koska ainoa tapa saada julkaistu `Post`-instanssi, jolla on määritelty `content`-metodi, on kutsua `approve`-metodia `PendingReviewPost`-rakenteella, ja ainoa tapa saada `PendingReviewPost` on kutsua `request_review`-metodia `DraftPost`-rakenteella, olemme nyt koodanneet blogikirjoituksen työnkulun tyyppijärjestelmään.

Meidän täytyy kuitenkin tehdä pieniä muutoksia `main`-funktioon. `request_review`- ja `approve`-metodit palauttavat uusia instansseja sen sijaan, että muokkaisivat rakennetta, jolla niitä kutsutaan, joten meidän täytyy lisätä enemmän `let post =` -varjostusmäärityksiä tallentaaksemme palautetut instanssit. Emme myöskään voi tehdä väitteitä luonnos- ja tarkistusta odottavien kirjoitusten sisällöstä tyhjinä merkkijonoina, emmekä tarvitse niitä: emme voi enää kääntää koodia, joka yrittää käyttää kirjoitusten sisältöä näissä tiloissa. Päivitetty koodi `main`-funktiossa on listauksessa 18-21.

<Listing number="18-21" file-name="src/main.rs" caption="Muutokset `main`-funktioon käyttämään blogikirjoituksen työnkulun uutta toteutusta">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-21/src/main.rs}}
```

</Listing>

Muutokset, jotka meidän piti tehdä `main`-funktioon `post`-muuttujan uudelleenmääritykseen, tarkoittavat, että tämä toteutus ei aivan seuraa oliopohjaista tilamallia enää: siirtymät tilojen välillä eivät ole enää täysin kapseloitu `Post`-rakenteen toteutuksen sisällä. Saamme kuitenkin sen, että virheelliset tilat ovat nyt mahdottomia tyyppijärjestelmän ja käännösaikaisen tyyppitarkistuksen ansiosta! Tämä varmistaa, että tietyt bugit, kuten julkaisemattoman kirjoituksen sisällön näyttäminen, löydetään ennen kuin ne päätyvät tuotantoon.

Kokeile tämän osion alussa ehdotettuja tehtäviä `blog`-krateen sellaisena kuin se on listauksen 18-21 jälkeen ja pohdi, mitä mieltä olet tämän version koodin suunnittelusta. Huomaa, että jotkin tehtävistä saattavat olla jo valmiita tässä suunnittelussa.

Olemme nähneet, että vaikka Rust pystyy toteuttamaan oliopohjaisia suunnittelumalleja, myös muut mallit, kuten tilan koodaus tyyppijärjestelmään, ovat saatavilla Rustissa. Näillä malleilla on erilaiset kompromissit. Vaikka olisit hyvin perehtynyt oliopohjaisiin malleihin, ongelman uudelleenajattelu Rustin ominaisuuksien hyödyntämiseksi voi tarjota etuja, kuten joidenkin bugien estämisen käännösaikana. Oliopohjaiset mallit eivät aina ole paras ratkaisu Rustissa tiettyjen ominaisuuksien, kuten omistajuuden, vuoksi, joita oliopohjaisilla kielillä ei ole.

## Yhteenveto

Riippumatta siitä, pidätkö Rustia oliopohjaisena kielenä tämän luvun lukemisen jälkeen, tiedät nyt, että voit käyttää trait-olioita saadaksesi joitakin oliopohjaisia ominaisuuksia Rustissa. Dynaaminen dispatch voi antaa koodillesi joustavuutta pienen ajonaikaisen suorituskyvyn kustannuksella. Voit käyttää tätä joustavuutta oliopohjaisten mallien toteuttamiseen, jotka voivat auttaa koodisi ylläpidettävyydessä. Rustissa on myös muita ominaisuuksia, kuten omistajuus, joita oliopohjaisilla kielillä ei ole. Oliopohjainen malli ei aina ole paras tapa hyödyntää Rustin vahvuuksia, mutta se on käytettävissä oleva vaihtoehto.

Seuraavaksi katsomme kuvioita, jotka ovat toinen Rustin ominaisuuksista mahdollistamassa paljon joustavuutta. Olemme vilkaisseet niitä lyhyesti läpi kirjan, mutta emme ole vielä nähneet niiden täyttä potentiaalia. Mennään!

[more-info-than-rustc]: ch09-03-to-panic-or-not-to-panic.html#cases-in-which-you-have-more-information-than-the-compiler
[macros]: ch20-05-macros.html#macros
