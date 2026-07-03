## Olio-ohjelmoinnin suunnittelumallin toteuttaminen

_Tila-malli_ on olio-ohjelmoinnin suunnittelumalli. Mallin ydin on, että määrittelemme joukon tiloja, joissa arvo voi olla sisäisesti.
Tilat edustetaan joukolla _tilaobjekteja_, ja arvon käyttäytyminen muuttuu sen tilan mukaan. Käymme läpi esimerkin blogikirjoitus-structista,
jolla on kenttä tilan säilyttämiseen; tila on tilaobjekti joukosta ”luonnos”, ”tarkistettavana” tai ”julkaistu”.

Tilaobjektit jakavat toiminnallisuutta: Rustissa käytämme tietysti structeja ja traitteja objektien ja perinnän sijaan.
Jokainen tilaobjekti vastaa omasta käyttäytymisestään ja siitä, milloin sen tulisi muuttua toiseen tilaan.
Tilaa säilyttävä arvo ei tiedä mitään eri tilojen käyttäytymisestä tai siitä, milloin siirtyä tilojen välillä.

Tilamallin etu on, että kun ohjelman liiketoimintavaatimukset muuttuvat, emme tarvitse muuttaa tilaa säilyttävän arvon koodia
tai arvoa käyttävän koodin koodia. Meidän täytyy päivittää vain yhden tilaobjektin sisällä oleva koodi muuttaaksemme sen sääntöjä
tai ehkä lisätä lisää tilaobjekteja.

Ensin toteutamme tilamallin perinteisemmällä olio-ohjelmointitavalla, sitten käytämme Rustiin luontevampaa lähestymistapaa.
Aloitetaan blogikirjoituksen työnkulun vaiheittainen toteuttaminen tilamallilla.

Lopullinen toiminnallisuus näyttää tältä:

1. Blogikirjoitus alkaa tyhjänä luonnoksena.
2. Kun luonnos on valmis, kirjoituksesta pyydetään tarkistusta.
3. Kun kirjoitus hyväksytään, se julkaistaan.
4. Vain julkaistut blogikirjoitukset palauttavat tulostettavaa sisältöä, joten hyväksymättömiä kirjoituksia ei voi vahingossa julkaista.

Mikä tahansa muu kirjoitukseen tehty muutos ei saa vaikutusta. Esimerkiksi jos yritämme hyväksyä luonnosblogikirjoituksen
ennen kuin olemme pyytäneet tarkistusta, kirjoituksen pitäisi pysyä julkaisemattomana luonnoksena.

Listaus 18-11 näyttää tämän työnkulun koodimuodossa: tämä on esimerkki `blog`-nimisen kirjastocraten API:n käytöstä.
Tämä ei vielä käänny, koska emme ole toteuttaneet `blog`-cratea.

<Listing number="18-11" file-name="src/main.rs" caption="Koodi, joka havainnollistaa haluamaamme `blog`-craten käyttäytymistä">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-11/src/main.rs:all}}
```

</Listing>

Haluamme antaa käyttäjän luoda uuden luonnosblogikirjoituksen `Post::new`-funktiolla. Haluamme antaa lisätä tekstiä blogikirjoitukseen.
Jos yritämme saada kirjoituksen sisällön heti hyväksynnän edellä, emme saa tekstiä, koska kirjoitus on vielä luonnos.
Olemme lisänneet koodiin `assert_eq!`-makron havainnollistustarkoituksessa. Erinomainen yksikkötesti tälle olisi varmistaa,
että luonnosblogikirjoitus palauttaa tyhjän merkkijonon `content`-metodista, mutta emme kirjoita testejä tälle esimerkille.

Seuraavaksi haluamme mahdollistaa kirjoituksen tarkistuspyynnön, ja haluamme `content`-metodin palauttavan tyhjän merkkijonon
tarkistusta odottaessa. Kun kirjoitus hyväksytään, se julkaistaan, eli kirjoituksen teksti palautetaan, kun `content`-metodia kutsutaan.

Huomaa, että ainoa tyyppi, jonka kanssa olemme vuorovaikutuksessa craten kanssa, on `Post`-tyyppi. Tämä tyyppi käyttää tilamallia
ja säilyttää arvon, joka on yksi kolmesta tilaobjektista edustaen eri tiloja, joissa kirjoitus voi olla — luonnos, tarkistusta odottava tai julkaistu.
Siirtyminen tilasta toiseen hallitaan sisäisesti `Post`-tyypin sisällä. Tilat muuttuvat vastauksena kirjastomme käyttäjien `Post`-instanssille
kutsumiin metodeihin, mutta heidän ei tarvitse hallita tilamuutoksia suoraan. Lisäksi käyttäjät eivät voi tehdä virheitä tilojen kanssa,
kuten julkaista kirjoitusta ennen kuin se on tarkistettu.

### `Post`-tyypin määrittely ja uuden instanssin luominen luonnostilassa

Aloitetaan kirjaston toteutus! Tiedämme tarvitsevamme julkisen `Post`-structin, joka säilyttää sisältöä, joten aloitamme
structin määrittelystä ja siihen liittyvästä julkisesta `new`-funktiosta uuden `Post`-instanssin luomiseksi, kuten Listauksessa 18-12 näytetään.
Teemme myös yksityisen `State`-traitin, joka määrittelee käyttäytymisen, joka kaikilla `Post`-tyypin tilaobjekteilla täytyy olla.

Sitten `Post` säilyttää `Box<dyn State>`-trait-objektin `Option<T>`-tyypin sisällä yksityisessä `state`-kentässä tilan säilyttämiseksi.
Näet hetken kuluttua, miksi `Option<T>` on tarpeen.

<Listing number="18-12" file-name="src/lib.rs" caption="`Post`-structin määrittely ja `new`-funktio uuden `Post`-instanssin luomiseksi, `State`-trait ja `Draft`-struct">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-12/src/lib.rs}}
```

</Listing>

`State`-trait määrittelee eri kirjoitustilojen jakaman käyttäytymisen. Tilaobjektit ovat `Draft`, `PendingReview` ja `Published`,
ja ne kaikki toteuttavat `State`-traitin. Toistaiseksi traitilla ei ole metodeja, ja aloitamme määrittelemällä vain `Draft`-tilan,
koska haluamme kirjoituksen alkavan luonnoksena.

Kun luomme uuden `Post`-instanssin, asetamme sen `state`-kentän `Some`-arvoksi, joka sisältää `Box`-tyypin.
Tämä `Box` osoittaa uuteen `Draft`-struct-instanssiin. Tämä varmistaa, että aina kun luomme uuden `Post`-instanssin,
se alkaa luonnoksena. Koska `Post`-structin `state`-kenttä on yksityinen, `Post`-instanssia ei voi luoda missään muussa tilassa!
`Post::new`-funktiossa asetamme `content`-kentän uudeksi, tyhjäksi `String`-tyypiksi.

### Kirjoituksen sisällön tekstin säilyttäminen

Näimme Listauksessa 18-11, että haluamme pystyä kutsumaan `add_text`-metodia ja välittämään sille `&str`-tyypin,
joka lisätään blogikirjoituksen tekstisisällöksi. Toteutamme tämän metodina sen sijaan, että paljastaisimme `content`-kentän `pub`-määritteellä,
jotta voimme myöhemmin toteuttaa metodin, joka hallitsee `content`-kentän datan lukemista. `add_text`-metodi on melko suoraviivainen,
joten lisätään toteutus Listauksessa 18-13 `impl Post` -lohkoon:

<Listing number="18-13" file-name="src/lib.rs" caption="`add_text`-metodin toteuttaminen tekstin lisäämiseksi kirjoituksen `content`-kenttään">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-13/src/lib.rs:here}}
```

</Listing>

`add_text`-metodi ottaa muuttuvan viitteen `self`:ään, koska muutamme `Post`-instanssia, jolle kutsumme `add_text`-metodia.
Sitten kutsumme `push_str`-metodia `content`-kentän `String`-tyypillä ja välitämme `text`-argumentin lisättäväksi tallennettuun `content`-kenttään.
Tämä käyttäytyminen ei riipu kirjoituksen tilasta, joten se ei ole osa tilamallia. `add_text`-metodi ei vuorovaikuta `state`-kentän kanssa lainkaan,
mutta se on osa käyttäytymistä, jota haluamme tukea.

### Luonnoskirjoituksen sisällön tyhjyyden varmistaminen

Vaikka olemme kutsuneet `add_text`-metodia ja lisänneet sisältöä kirjoitukseemme, haluamme silti `content`-metodin palauttavan
tyhjän merkkijonoviipaleen, koska kirjoitus on vielä luonnostilassa, kuten Listauksen 18-11 rivillä 7 näytetään.
Toteutetaan toistaiseksi `content`-metodi yksinkertaisimmalla tavalla, joka täyttää tämän vaatimuksen: palauttamalla aina tyhjä merkkijonoviipale.
Muutamme tämän myöhemmin, kun toteutamme kyvyn muuttaa kirjoituksen tilaa, jotta se voidaan julkaista.
Toistaiseksi kirjoitukset voivat olla vain luonnostilassa, joten kirjoituksen sisällön pitäisi aina olla tyhjä.
Listaus 18-14 näyttää tämän paikkamerkkitoteutuksen:

<Listing number="18-14" file-name="src/lib.rs" caption="Paikkamerkkitoteutuksen lisääminen `Post`-tyypin `content`-metodille, joka palauttaa aina tyhjän merkkijonoviipaleen">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-14/src/lib.rs:here}}
```

</Listing>

Tämän `content`-metodin lisäämisen jälkeen kaikki Listauksessa 18-11 riville 7 asti toimii tarkoitetulla tavalla.

### Kirjoituksen tarkistuspyyntö muuttaa sen tilaa

Seuraavaksi meidän täytyy lisätä toiminnallisuus kirjoituksen tarkistuksen pyytämiseen, mikä pitäisi muuttaa sen tilan `Draft`-tilasta `PendingReview`-tilaan.
Listaus 18-15 näyttää tämän koodin:

<Listing number="18-15" file-name="src/lib.rs" caption="`request_review`-metodien toteuttaminen `Post`-tyypille ja `State`-traitille">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-15/src/lib.rs:here}}
```

</Listing>

Annamme `Post`-tyypille julkisen `request_review`-metodin, joka ottaa muuttuvan viitteen `self`:ään. Sitten kutsumme sisäistä
`request_review`-metodia `Post`-tyypin nykyiselle tilalle, ja tämä toinen `request_review`-metodi kuluttaa nykyisen tilan ja palauttaa uuden tilan.

Lisäämme `request_review`-metodin `State`-traitiin; kaikkien traitin toteuttavien tyyppien täytyy nyt toteuttaa `request_review`-metodi.
Huomaa, että metodin ensimmäisenä parametrina on `self: Box<Self>` `self`:n, `&self`:n tai `&mut self`:n sijaan.
Tämä syntaksi tarkoittaa, että metodi on kelvollinen vain, kun sitä kutsutaan tyyppiä `Box`-tyypin sisältävällä `Box`-rakenteella.
Tämä syntaksi ottaa omistajuuden `Box<Self>`-rakenteesta mitätöiden vanhan tilan, jotta `Post`-tyypin tila-arvo voi muuttua uudeksi tilaksi.

Vanhan tilan kuluttamiseksi `request_review`-metodin täytyy ottaa omistajuus tila-arvosta. Tässä `Post`-structin `state`-kentän `Option` tulee kuvaan:
kutsumme `take`-metodia ottamaan `Some`-arvon `state`-kentästä ja jättämään tilalle `None`, koska Rust ei salli tyhjiä kenttiä structeissa.
Tämä antaa meidän siirtää `state`-arvon `Post`-tyypistä lainaamisen sijaan. Sitten asetamme kirjoituksen `state`-arvon tämän operaation tulokseksi.

Meidän täytyy asettaa `state` väliaikaisesti `None`-arvoksi sen sijaan, että asettaisimme sen suoraan koodilla kuten
`self.state = self.state.request_review();` saadaksemme omistajuuden `state`-arvosta. Tämä varmistaa, ettei `Post` voi käyttää vanhaa `state`-arvoa
sen jälkeen, kun olemme muuttaneet sen uudeksi tilaksi.

`Draft`-tyypin `request_review`-metodi palauttaa uuden, laatikon sisällä olevan instanssin uudesta `PendingReview`-structista,
joka edustaa tilaa, jossa kirjoitus odottaa tarkistusta. `PendingReview`-struct toteuttaa myös `request_review`-metodin,
mutta ei tee muunnoksia. Sen sijaan se palauttaa itsensä, koska kun pyydämme tarkistusta kirjoitukselle, joka on jo `PendingReview`-tilassa,
sen pitäisi pysyä `PendingReview`-tilassa.

Nyt voimme alkaa nähdä tilamallin edut: `Post`-tyypin `request_review`-metodi on sama riippumatta sen `state`-arvosta.
Jokainen tila vastaa omista säännöistään.

Jätämme `Post`-tyypin `content`-metodin ennalleen palauttaen tyhjän merkkijonoviipaleen. Voimme nyt olla `Post`-instanssin kanssa
`PendingReview`-tilassa sekä `Draft`-tilassa, mutta haluamme saman käyttäytymisen `PendingReview`-tilassa.
Listaus 18-11 toimii nyt riville 10 asti!

<!-- Old headings. Do not remove or links may break. -->

<a id="adding-the-approve-method-that-changes-the-behavior-of-content"></a>

### `approve`-metodin lisääminen `content`-metodin käyttäytymisen muuttamiseksi

`approve`-metodi on samanlainen kuin `request_review`-metodi: se asettaa `state`-arvon arvoksi, jonka nykyinen tila sanoo sen pitävän,
kun tila hyväksytään, kuten Listauksessa 18-16 näytetään:

<Listing number="18-16" file-name="src/lib.rs" caption="`approve`-metodin toteuttaminen `Post`-tyypille ja `State`-traitille">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-16/src/lib.rs:here}}
```

</Listing>

Lisäämme `approve`-metodin `State`-traitiin ja uuden structin, joka toteuttaa `State`-traitin: `Published`-tilan.

Samalla tavalla kuin `PendingReview`-tyypin `request_review` toimii, jos kutsumme `approve`-metodia `Draft`-tyypillä, sillä ei ole vaikutusta,
koska `approve` palauttaa `self`:n. Kun kutsumme `approve`-metodia `PendingReview`-tyypillä, se palauttaa uuden, laatikon sisällä olevan
instanssin `Published`-structista. `Published`-struct toteuttaa `State`-traitin, ja sekä `request_review`- että `approve`-metodit
palauttavat itsensä, koska kirjoituksen pitäisi pysyä `Published`-tilassa näissä tapauksissa.

Nyt meidän täytyy päivittää `Post`-tyypin `content`-metodi. Haluamme `content`-metodin palauttaman arvon riippuvan `Post`-tyypin nykyisestä tilasta,
joten annamme `Post`-tyypin delegoida `content`-metodille, joka on määritelty sen `state`-kentässä, kuten Listauksessa 18-17 näytetään:

<Listing number="18-17" file-name="src/lib.rs" caption="`Post`-tyypin `content`-metodin päivittäminen delegoimaan `State`-tyypin `content`-metodille">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-17/src/lib.rs:here}}
```

</Listing>

Koska tavoitteena on pitää kaikki nämä säännöt `State`-traitin toteuttavien structien sisällä, kutsumme `content`-metodia `state`-kentän arvolla
ja välitämme kirjoitusinstanssin (eli `self`) argumenttina. Sitten palautamme arvon, joka palautuu `state`-arvon `content`-metodin käytöstä.

Kutsumme `as_ref`-metodia `Option`-tyypillä, koska haluamme viitteen `Option`-tyypin sisällä olevaan arvoon omistajuuden sijaan.
Koska `state` on `Option<Box<dyn State>>`, kun kutsumme `as_ref`-metodia, palautuu `Option<&Box<dyn State>>`.
Jos emme kutsuisi `as_ref`-metodia, saisimme virheen, koska emme voi siirtää `state`-arvoa funktion parametrin lainatusta `&self`:stä.

Sitten kutsumme `unwrap`-metodia, joka emme tiedä koskaan kaatuvan, koska tiedämme `Post`-tyypin metodien varmistavan,
että `state` sisältää aina `Some`-arvon, kun nämä metodit ovat valmiita. Tämä on yksi tapauksista, joista puhuimme Luvun 9
[”Tapaukset, joissa sinulla on enemmän tietoa kuin kääntäjällä”][more-info-than-rustc]<!-- ignore --> -osiossa,
kun tiedämme `None`-arvon olevan mahdoton, vaikka kääntäjä ei pysty sitä ymmärtämään.

Tässä vaiheessa, kun kutsumme `content`-metodia `&Box<dyn State>`-tyypillä, deref-pakotus vaikuttaa `&`- ja `Box`-rakenteisiin,
joten `content`-metodia kutsutaan lopulta tyypillä, joka toteuttaa `State`-traitin. Tämä tarkoittaa, että meidän täytyy lisätä `content`
`State`-traitin määrittelyyn, ja sinne sijoitamme logiikan sille, mitä sisältöä palautetaan riippuen siitä, mikä tila meillä on,
kuten Listauksessa 18-18 näytetään:

<Listing number="18-18" file-name="src/lib.rs" caption="`content`-metodin lisääminen `State`-traitiin">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-18/src/lib.rs:here}}
```

</Listing>

Lisäämme `content`-metodille oletustoteutuksen, joka palauttaa tyhjän merkkijonoviipaleen. Tämä tarkoittaa, että emme tarvitse
toteuttaa `content`-metodia `Draft`- ja `PendingReview`-structeille. `Published`-struct korvaa `content`-metodin ja palauttaa arvon `post.content`-kentässä.

Huomaa, että tarvitsemme elinajan annotaatiot tälle metodille, kuten käsittelimme Luvussa 10. Otamme viitteen `post`-argumenttiin
ja palautamme viitteen osaan kyseistä `post`-argumenttia, joten palautetun viitteen elinikä liittyy `post`-argumentin elinikään.

Ja olemme valmiita — koko Listaus 18-11 toimii nyt! Olemme toteuttaneet tilamallin blogikirjoituksen työnkulun säännöillä.
Sääntöihin liittyvä logiikka sijaitsee tilaobjekteissa sen sijaan, että se olisi hajautettu `Post`-tyypin ympäri.

> #### Miksi ei enumia?
>
> Olet ehkä miettinyt, miksi emme käyttäneet `enum`-tyyppiä eri mahdollisten kirjoitustilojen variantteina.
> Se on varmasti mahdollinen ratkaisu, kokeile sitä ja vertaa lopputuloksia nähdäksesi kumman pidät parempana!
> Yksi enumin käytön haittapuoli on, että jokaisessa paikassa, joka tarkistaa enum-arvon, tarvitaan `match`-lauseke tai vastaava
> käsittelemään jokainen mahdollinen variantti. Tämä voi tulla toistuvammaksi kuin tämä trait-objektiratkaisu.

### Tilamallin kompromissit

Olemme osoittaneet, että Rust pystyy toteuttamaan olio-ohjelmoinnin tilamallin kapseloimaan erilaisen käyttäytymisen, jonka kirjoituksen pitäisi
olla kussakin tilassa. `Post`-tyypin metodit eivät tiedä mitään eri käyttäytymisistä. Koodin järjestelyllä meidän tarvitsee katsoa vain yhteen paikkaan
tietääksemme eri tavat, joilla julkaistu kirjoitus voi käyttäytyä: `Published`-structin `State`-traitin toteutus.

Jos loisimme vaihtoehtoisen toteutuksen, joka ei käyttäisi tilamallia, voisimme sen sijaan käyttää `match`-lausekkeita `Post`-tyypin metodeissa
tai jopa `main`-koodissa, joka tarkistaa kirjoituksen tilan ja muuttaa käyttäytymistä näissä paikoissa. Tämä tarkoittaisi, että meidän täytyisi
katsoa useita paikkoja ymmärtääksemme kaikki julkaistun kirjoituksen tilan vaikutukset! Tämä kasvaisi vain sitä enemmän, mitä enemmän tiloja lisäisimme:
jokainen näistä `match`-lausekkeista tarvitsisi uuden haaran.

Tilamallin avulla `Post`-metodeissa ja paikoissa, joissa käytämme `Post`-tyyppiä, ei tarvita `match`-lausekkeita,
ja uuden tilan lisäämiseksi meidän tarvitsisi vain lisätä uusi struct ja toteuttaa trait-metodit kyseiselle structille.

Tilamallia käyttävä toteutus on helppo laajentaa lisätoiminnallisuudella. Nähdäksesi tilamallia käyttävän koodin ylläpidon yksinkertaisuuden,
kokeile muutamia näistä ehdotuksista:

- Lisää `reject`-metodi, joka muuttaa kirjoituksen tilan `PendingReview`-tilasta takaisin `Draft`-tilaan.
- Vaadi kaksi `approve`-kutsua ennen kuin tila voidaan muuttaa `Published`-tilaksi.
- Salli käyttäjien lisätä tekstisisältöä vain, kun kirjoitus on `Draft`-tilassa.
  Vihje: anna tilaobjektin vastata siitä, mikä sisällössä voi muuttua, mutta älä anna sen vastata `Post`-tyypin muokkaamisesta.

Yksi tilamallin haittapuoli on, että koska tilat toteuttavat siirtymät tilojen välillä, jotkin tilat ovat toisiinsa kytkettyjä.
Jos lisäisimme uuden tilan `PendingReview`- ja `Published`-tilojen väliin, kuten `Scheduled`, meidän täytyisi muuttaa `PendingReview`-tyypin koodia
siirtymään `Scheduled`-tilaan `Published`-tilan sijaan. Olisi vähemmän työtä, jos `PendingReview`-tyypin ei tarvitsisi muuttua uuden tilan lisäämisen yhteydessä,
mutta se tarkoittaisi siirtymistä toiseen suunnittelumalliin.

Toinen haittapuoli on, että olemme monistaneet logiikkaa. Monistuksen poistamiseksi voisimme yrittää tehdä oletustoteutuksia
`request_review`- ja `approve`-metodeille `State`-traitissa, jotka palauttavat `self`:n; tämä ei kuitenkaan olisi dyn-yhteensopivaa,
koska trait ei tiedä, mikä konkreettinen `self` tarkalleen on. Haluamme pystyä käyttämään `State`-tyyppiä trait-objektina,
joten sen metodien täytyy olla dyn-yhteensopivia.

Muuta monistusta ovat samanlaiset `request_review`- ja `approve`-metodien toteutukset `Post`-tyypillä.
Molemmat metodit delegoivat saman metodin toteutukselle `state`-kentän `Option`-tyypin arvossa ja asettavat `state`-kentän uudeksi arvoksi tuloksen.
Jos `Post`-tyypillä olisi paljon metodeja, jotka noudattaisivat tätä mallia, voisimme harkita makron määrittelyä toiston poistamiseksi
(katso Luvun 20 [”Makrot”][macros]<!-- ignore --> -osio).

Toteuttamalla tilamallin täsmälleen niin kuin se on määritelty olio-ohjelmointikielille, emme hyödynnä Rustin vahvuuksia niin täysin kuin voisimme.
Katsotaan joitakin muutoksia, joita voimme tehdä `blog`-crateen ja jotka voivat tehdä virheellisistä tiloista ja siirtymistä käännösaikaisia virheitä.

#### Tilojen ja käyttäytymisen koodaaminen tyyppeinä

Näytämme, miten tilamallia voi ajatella uudelleen saadakseen erilaisen kompromissijoukon. Sen sijaan, että kapseloisimme tilat ja siirtymät
kokonaan niin, ettei ulkopuolinen koodi tiedä niistä mitään, koodaamme tilat eri tyyppeihin. Näin ollen Rustin tyyppitarkistusjärjestelmä
estää yritykset käyttää luonnoskirjoituksia siellä, missä vain julkaistut kirjoitukset ovat sallittuja, antamalla kääntäjävirheen.

Tarkastellaan Listauksen 18-11 `main`-funktion ensimmäistä osaa:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-11/src/main.rs:here}}
```

</Listing>

Sallimme edelleen uusien kirjoitusten luomisen luonnostilassa `Post::new`-funktiolla ja tekstin lisäämisen kirjoituksen sisältöön.
Sen sijaan, että luonnoskirjoituksella olisi `content`-metodi, joka palauttaa tyhjän merkkijonon, teemme niin, ettei luonnoskirjoituksilla ole `content`-metodia lainkaan.
Näin, jos yritämme saada luonnoskirjoituksen sisällön, saamme kääntäjävirheen, joka kertoo metodin olevan olematon.
Näin on mahdotonta vahingossa näyttää luonnoskirjoituksen sisältöä tuotannossa, koska tuollainen koodi ei edes käänny.
Listaus 18-19 näyttää `Post`-structin ja `DraftPost`-structin määrittelyn sekä metodit kummallekin:

<Listing number="18-19" file-name="src/lib.rs" caption="`Post` `content`-metodilla ja `DraftPost` ilman `content`-metodia">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-19/src/lib.rs}}
```

</Listing>

Sekä `Post`- että `DraftPost`-structeilla on yksityinen `content`-kenttä, joka säilyttää blogikirjoituksen tekstin.
Structeilla ei ole enää `state`-kenttää, koska siirrämme tilan koodauksen structien tyyppeihin. `Post`-struct edustaa julkaistua kirjoitusta,
ja sillä on `content`-metodi, joka palauttaa `content`-kentän.

Meillä on edelleen `Post::new`-funktio, mutta sen sijaan, että se palauttaisi `Post`-instanssin, se palauttaa `DraftPost`-instanssin.
Koska `content` on yksityinen eikä ole funktioita, jotka palauttavat `Post`-tyypin, `Post`-instanssia ei voi luoda juuri nyt.

`DraftPost`-structilla on `add_text`-metodi, joten voimme lisätä tekstiä `content`-kenttään kuten aiemmin,
mutta huomaa, että `DraftPost`-tyypillä ei ole määritelty `content`-metodia! Nyt ohjelma varmistaa, että kaikki kirjoitukset alkavat luonnoskirjoituksina
ja luonnoskirjoituksilla ei ole sisältöä näytettäväksi. Mikä tahansa yritys kiertää nämä rajoitukset johtaa kääntäjävirheeseen.

#### Siirtymien toteuttaminen muunnoksina eri tyyppeihin

Miten siis saamme julkaistun kirjoituksen? Haluamme pakottaa säännön, että luonnoskirjoitus täytyy tarkistaa ja hyväksyä ennen julkaisemista.
Tarkistusta odottavan tilan kirjoituksella ei pitäisi vieläkään näyttää sisältöä. Toteutamme nämä rajoitukset lisäämällä toisen structin,
`PendingReviewPost`-structin, määrittelemällä `request_review`-metodin `DraftPost`-tyypille palauttamaan `PendingReviewPost`-tyypin
ja määrittelemällä `approve`-metodin `PendingReviewPost`-tyypille palauttamaan `Post`-tyypin, kuten Listauksessa 18-20 näytetään:

<Listing number="18-20" file-name="src/lib.rs" caption="`PendingReviewPost`, joka luodaan kutsumalla `request_review`-metodia `DraftPost`-tyypillä, ja `approve`-metodi, joka muuttaa `PendingReviewPost`-tyypin julkaistuksi `Post`-tyypiksi">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-20/src/lib.rs:here}}
```

</Listing>

`request_review`- ja `approve`-metodit ottavat omistajuuden `self`:stä kuluttaen `DraftPost`- ja `PendingReviewPost`-instanssit
ja muuntaen ne `PendingReviewPost`- ja julkaistuksi `Post`-instanssiksi. Näin meillä ei jää `DraftPost`-instansseja jäljelle
sen jälkeen, kun olemme kutsuneet niille `request_review`-metodia, ja niin edelleen. `PendingReviewPost`-structilla ei ole määritelty
`content`-metodia, joten sen sisällön lukeminen johtaa kääntäjävirheeseen kuten `DraftPost`-tyypillä. Koska ainoa tapa saada julkaistu
`Post`-instanssi, jolla on määritelty `content`-metodi, on kutsua `approve`-metodia `PendingReviewPost`-tyypillä, ja ainoa tapa saada
`PendingReviewPost` on kutsua `request_review`-metodia `DraftPost`-tyypillä, olemme nyt koodanneet blogikirjoituksen työnkulun tyyppijärjestelmään.

Meidän täytyy kuitenkin tehdä pieniä muutoksia `main`-funktioon. `request_review`- ja `approve`-metodit palauttavat uusia instansseja
sen sijaan, että ne muokkaisivat structia, jolle niitä kutsutaan, joten meidän täytyy lisätä enemmän `let post =` -varjostussijoituksia
tallennettavaksi palautetut instanssit. Emme myöskään voi pitää varmistuksia siitä, että luonnos- ja tarkistusta odottavien kirjoitusten
sisällöt ovat tyhjiä merkkijonoja, emmekä tarvitse niitä: emme voi enää kääntää koodia, joka yrittää käyttää kirjoitusten sisältöä näissä tiloissa.
Päivitetty koodi `main`-funktiossa näytetään Listauksessa 18-21:

<Listing number="18-21" file-name="src/main.rs" caption="Muutokset `main`-funktioon blogikirjoituksen työnkulun uuden toteutuksen käyttämiseksi">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-21/src/main.rs}}
```

</Listing>

Muutokset, jotka meidän täytyi tehdä `main`-funktioon `post`-muuttujan uudelleensijoittamiseksi, tarkoittavat, että tämä toteutus ei aivan
noudata enää olio-ohjelmoinnin tilamallia: siirtymät tilojen välillä eivät ole enää täysin kapseloitu `Post`-toteutuksen sisällä.
Saamamme kuitenkin hyödyn siitä, että virheelliset tilat ovat nyt mahdottomia tyyppijärjestelmän ja käännösaikana tapahtuvan tyyppitarkistuksen ansiosta!
Tämä varmistaa, että tietyt bugit, kuten julkaisemattoman kirjoituksen sisällön näyttäminen, löydetään ennen kuin ne päätyvät tuotantoon.

Kokeile tämän osion alussa ehdotettuja tehtäviä `blog`-crateen Listauksen 18-21 jälkeisessä tilassa ja pohdi, mitä mieltä olet tämän version koodin suunnittelusta.
Huomaa, että jotkin tehtävistä saattavat olla jo valmiita tässä suunnittelussa.

Olemme nähneet, että vaikka Rust pystyy toteuttamaan olio-ohjelmoinnin suunnittelumalleja, Rustissa on saatavilla myös muita malleja,
kuten tilan koodaaminen tyyppijärjestelmään. Näillä malleilla on erilaiset kompromissit. Vaikka olisit hyvin perehtynyt olio-ohjelmoinnin malleihin,
ongelman uudelleenajattelu Rustin ominaisuuksien hyödyntämiseksi voi tarjota etuja, kuten joidenkin bugien estämisen käännösaikana.
Olio-ohjelmoinnin mallit eivät aina ole paras ratkaisu Rustissa tiettyjen ominaisuuksien, kuten omistajuuden, vuoksi,
joita olio-ohjelmointikielillä ei ole.

## Yhteenveto

Riippumatta siitä, pidätkö Rustia olio-ohjelmointikielenä tämän luvun lukemisen jälkeen, tiedät nyt, että voit käyttää trait-objekteja
saadaksesi joitakin olio-ohjelmoinnin ominaisuuksia Rustissa. Dynaaminen dispatch voi antaa koodillesi joustavuutta pienellä suorituskyvyn hinnalla.
Voit käyttää tätä joustavuutta olio-ohjelmoinnin mallien toteuttamiseen, jotka voivat auttaa koodisi ylläpidettävyydessä.
Rustissa on myös muita ominaisuuksia, kuten omistajuus, joita olio-ohjelmointikielillä ei ole. Olio-ohjelmoinnin malli ei aina ole
paras tapa hyödyntää Rustin vahvuuksia, mutta se on käytettävissä oleva vaihtoehto.

Seuraavaksi tarkastelemme kuvioita, jotka ovat toinen Rustin ominaisuuksista ja mahdollistavat paljon joustavuutta.
Olemme katsoneet niitä lyhyesti läpi kirjan, mutta emme ole vielä nähneet niiden täyttä potentiaalia. Mennään!

[more-info-than-rustc]: ch09-03-to-panic-or-not-to-panic.html#cases-in-which-you-have-more-information-than-the-compiler
[macros]: ch20-05-macros.html#macros
