## `RefCell<T>` ja sisäisen muuttuvuuden malli

_Sisäinen muuttuvuus_ on Rustissa suunnittelumalli, joka sallii datan muuttamisen, vaikka dataan olisi muuttumattomia viittauksia; normaalisti lainausperiaatteet kieltävät tämän toiminnon. Datan muuttamiseksi malli käyttää `unsafe`-koodia tietorakenteen sisällä taivuttaakseen Rustin tavallisia sääntöjä, jotka hallitsevat muuttamista ja lainaamista. `Unsafe`-koodi ilmaisee kääntäjälle, että tarkistamme säännöt käsin sen sijaan, että luottaisimme kääntäjään niiden tarkistamisessa; käsittelemme `unsafe`-koodia tarkemmin luvussa 20.

Voimme käyttää sisäisen muuttuvuuden mallia noudattavia tyyppejä vain, kun voimme varmistaa, että lainausperiaatteita noudatetaan ajonaikana, vaikka kääntäjä ei voi sitä taata. Mukana oleva `unsafe`-koodi kääritään sitten turvalliseen API:in, ja ulompi tyyppi on edelleen muuttumaton.

Tutustutaan tähän käsitteeseen tarkastelemalla `RefCell<T>`-tyyppiä, joka noudattaa sisäisen muuttuvuuden mallia.

<!-- Old headings. Do not remove or links may break. -->

<a id="enforcing-borrowing-rules-at-runtime-with-refcellt"></a>

### Lainausperiaatteiden pakottaminen ajonaikana

Toisin kuin `Rc<T>`, `RefCell<T>`-tyyppi edustaa yksittäistä omistajuutta pitämänsä datan yli. Mikä siis tekee `RefCell<T>`:stä erilaisen kuin esimerkiksi `Box<T>`? Muistathan luvussa 4 opitut lainausperiaatteet:

- Milloin tahansa sinulla voi olla _joko_ yksi muuttuva viittaus _tai_ mikä tahansa määrä muuttumattomia viittauksia (mutta ei molempia).
- Viittausten täytyy aina olla voimassa.

Viittausten ja `Box<T>`:n kanssa lainausperiaatteiden invariantit pakotetaan käännösaikana. `RefCell<T>`:n kanssa nämä invariantit pakotetaan _ajonaikana_. Viittausten kanssa sääntöjen rikkominen tuottaa kääntäjävirheen. `RefCell<T>`:n kanssa sääntöjen rikkominen saa ohjelman panikoimaan ja päättymään.

Lainausperiaatteiden tarkistamisen käännösaikana etuja ovat, että virheet havaitaan aikaisemmin kehitysprosessissa eikä ajonaikaisella suorituskyvyllä ole vaikutusta, koska kaikki analyysi tehdään etukäteen. Näistä syistä lainausperiaatteiden tarkistaminen käännösaikana on paras valinta useimmissa tapauksissa, minkä vuoksi se on Rustin oletus.

Lainausperiaatteiden tarkistamisen ajonaikana etuna on, että tietyt muistiturvalliset skenaariot sallitaan, vaikka käännösaikaiset tarkistukset olisivat kieltäneet ne. Staattinen analyysi, kuten Rustin kääntäjä, on luonnostaan konservatiivinen. Joitakin koodin ominaisuuksia on mahdotonta havaita analysoimalla koodia: tunnetuin esimerkki on pysähtymisongelma, joka on tämän kirjan ulkopuolella mutta mielenkiintoinen tutkimuskohde.

Koska osa analyysistä on mahdotonta, jos Rustin kääntäjä ei voi olla varma, että koodi noudattaa omistajuussääntöjä, se saattaa hylätä oikean ohjelman; tällä tavalla se on konservatiivinen. Jos Rust hyväksyisi virheellisen ohjelman, käyttäjät eivät voisi luottaa Rustin antamiin takuisiin. Jos Rust hylkää oikean ohjelman, ohjelmoijaa haitataan, mutta mitään katastrofaalista ei voi tapahtua. `RefCell<T>`-tyyppi on hyödyllinen, kun olet varma, että koodisi noudattaa lainausperiaatteita, mutta kääntäjä ei pysty ymmärtämään ja takaamaan sitä.

Samoin kuin `Rc<T>`, `RefCell<T>` on tarkoitettu vain yksisäikeisiin skenaarioihin ja antaa kääntäjävirheen, jos yrität käyttää sitä monisäikeisessä kontekstissa. Käsittelemme, miten `RefCell<T>`:n toiminnallisuus saadaan monisäikeisessä ohjelmassa luvussa 16.

Tässä on yhteenveto syistä valita `Box<T>`, `Rc<T>` tai `RefCell<T>`:

- `Rc<T>` mahdollistaa saman datan usean omistajan; `Box<T>`:llä ja `RefCell<T>`:llä on yksi omistaja.
- `Box<T>` sallii muuttumattomat tai muuttuvat lainaukset, jotka tarkistetaan käännösaikana; `Rc<T>` sallii vain muuttumattomat lainaukset, jotka tarkistetaan käännösaikana; `RefCell<T>` sallii muuttumattomat tai muuttuvat lainaukset, jotka tarkistetaan ajonaikana.
- Koska `RefCell<T>` sallii muuttuvat lainaukset, jotka tarkistetaan ajonaikana, voit muuttaa `RefCell<T>`:n sisällä olevaa arvoa, vaikka `RefCell<T>` itse olisi muuttumaton.

Arvon muuttaminen muuttumattoman arvon sisällä on sisäisen muuttuvuuden malli. Katsotaan tilannetta, jossa sisäinen muuttuvuus on hyödyllinen, ja tarkastellaan, miten se on mahdollista.

<!-- Old headings. Do not remove or links may break. -->

<a id="interior-mutability-a-mutable-borrow-to-an-immutable-value"></a>

### Sisäisen muuttuvuuden käyttö

Lainausperiaatteiden seuraauksena, kun sinulla on muuttumaton arvo, et voi lainata sitä muuttuvasti. Esimerkiksi tämä koodi ei käännä:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/no-listing-01-cant-borrow-immutable-as-mutable/src/main.rs}}
```

Jos yrittäisit kääntää tämän koodin, saisit seuraavan virheen:

```console
{{#include ../listings/ch15-smart-pointers/no-listing-01-cant-borrow-immutable-as-mutable/output.txt}}
```

On kuitenkin tilanteita, joissa olisi hyödyllistä, että arvo muuttaisi itseään metodeissaan mutta näyttäisi muuttumattomalta muulle koodille. Arvon metodien ulkopuolella oleva koodi ei voisi muuttaa arvoa. `RefCell<T>`:n käyttö on yksi tapa saada sisäinen muuttuvuus, mutta `RefCell<T>` ei kierrä lainausperiaatteita kokonaan: kääntäjän lainaustarkistin sallii tämän sisäisen muuttuvuuden, ja lainausperiaatteet tarkistetaan ajonaikana käännösaikaan sijaan. Jos rikot säännöt, saat `panic!`:n kääntäjävirheen sijaan.

Käydään läpi käytännön esimerkki, jossa voimme käyttää `RefCell<T>`:tä muuttamaan muuttumatonta arvoa, ja katsotaan, miksi se on hyödyllistä.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-use-case-for-interior-mutability-mock-objects"></a>

#### Testaus mock-olioilla

Joskus testauksen aikana ohjelmoija käyttää yhtä tyyppiä toisen tilalla havaitakseen tiettyä käyttäytymistä ja varmistaakseen, että se on toteutettu oikein. Tätä paikkamerkkityyppiä kutsutaan _test double_:ksi. Ajattele sitä elokuvatuotannon stunt-tuplana, jossa henkilö astuu esiin ja korvaa näyttelijän tekemään erityisen hankalan kohtauksen. Test double:t korvaavat muita tyyppejä testejä ajettaessa. _Mock-oliot_ ovat erityisiä test double -tyyppejä, jotka tallentavat testin aikana tapahtuneet asiat, jotta voit varmistaa, että oikeat toiminnot tapahtuivat.

Rustissa ei ole olioita samassa mielessä kuin muissa kielissä, eikä Rustissa ole mock-olioiden toiminnallisuutta sisäänrakennettuna standardikirjastoon kuten joissakin muissa kielissä. Voit kuitenkin ehdottomasti luoda structin, joka palvelee samoja tarkoituksia kuin mock-olio.

Tässä on skenaario, jota testaamme: luomme kirjaston, joka seuraa arvoa suhteessa enimmäisarvoon ja lähettää viestejä sen mukaan, kuinka lähellä enimmäisarvoa nykyinen arvo on. Tätä kirjastoa voitaisiin käyttää esimerkiksi seuraamaan käyttäjän API-kutsukiintiötä.

Kirjastomme tarjoaa vain toiminnallisuuden seurata, kuinka lähellä enimmäisarvoa arvo on, ja mitä viestejä pitäisi lähettää milloin. Kirjastoa käyttävien sovellusten odotetaan tarjoavan viestien lähetysmekanismin: sovellus voisi näyttää viestin käyttäjälle suoraan, lähettää sähköpostin, tekstiviestin tai tehdä jotain muuta. Kirjaston ei tarvitse tietää yksityiskohtia. Sille riittää jokin, joka toteuttaa tarjoamamme traitin nimeltä `Messenger`. Listauksessa 15-20 on kirjaston koodi.

<Listing number="15-20" file-name="src/lib.rs" caption="Kirjasto, joka seuraa kuinka lähellä arvo on enimmäisarvoa ja varoittaa, kun arvo on tietyillä tasoilla">

```rust,noplayground
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-20/src/lib.rs}}
```

</Listing>

Yksi tärkeä osa tässä koodissa on, että `Messenger`-traitilla on yksi metodi nimeltä `send`, joka ottaa muuttumattoman viittauksen `self`:iin ja viestin tekstin. Tämä trait on rajapinta, jonka mock-oliomme täytyy toteuttaa, jotta mockia voidaan käyttää samalla tavalla kuin oikeaa oliota. Toinen tärkeä osa on, että haluamme testata `LimitTracker`:in `set_value`-metodin käyttäytymistä. Voimme muuttaa `value`-parametrille välittämäämme arvoa, mutta `set_value` ei palauta mitään, josta voisimme tehdä väitteitä. Haluamme voida sanoa, että jos luomme `LimitTracker`:in jollakin, joka toteuttaa `Messenger`-traitin, ja tietyllä `max`-arvolla, messengerille kerrotaan lähettämään asianmukaiset viestit, kun välitämme eri lukuja `value`:lle.

Tarvitsemme mock-olion, joka sähköpostin tai tekstiviestin lähettämisen sijaan, kun kutsumme `send`:iä, vain seuraa sille kerrottuja viestejä. Voimme luoda uuden mock-olioinstanssin, luoda `LimitTracker`:in, joka käyttää mock-oliota, kutsua `LimitTracker`:in `set_value`-metodia ja tarkistaa sitten, että mock-oliolla on odottamamme viestit. Listauksessa 15-21 on yritys toteuttaa mock-olio juuri tätä varten, mutta lainaustarkistin ei salli sitä.

<Listing number="15-21" file-name="src/lib.rs" caption="Yritys toteuttaa `MockMessenger`, jota lainaustarkistin ei salli">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-21/src/lib.rs:here}}
```

</Listing>

Tämä testikoodi määrittelee `MockMessenger`-structin, jolla on `sent_messages`-kenttä `Vec<String>`-arvolla seuratakseen sille kerrottuja viestejä. Määrittelemme myös assosioituneen funktion `new`, jotta uusien `MockMessenger`-arvojen luominen tyhjällä viestilistalla on kätevää. Toteutamme sitten `Messenger`-traitin `MockMessenger`:lle, jotta voimme antaa `MockMessenger`:in `LimitTracker`:ille. `send`-metodin määrittelyssä otamme parametrina välitetyn viestin ja tallennamme sen `MockMessenger`:in `sent_messages`-listaan.

Testissä testaamme, mitä tapahtuu, kun `LimitTracker`:ille kerrotaan asettamaan `value` joksikin, joka on yli 75 prosenttia `max`-arvosta. Ensin luomme uuden `MockMessenger`:in, joka alkaa tyhjällä viestilistalla. Sitten luomme uuden `LimitTracker`:in ja annamme sille viittauksen uuteen `MockMessenger`:iin ja `max`-arvon `100`. Kutsumme `LimitTracker`:in `set_value`-metodia arvolla `80`, joka on yli 75 prosenttia luvusta 100. Sitten väitämme, että `MockMessenger`:in seuraamalla viestilistalla pitäisi nyt olla yksi viesti.

Tässä testissä on kuitenkin yksi ongelma, kuten tässä näytetään:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-21/output.txt}}
```

Emme voi muokata `MockMessenger`:ia seurataksemme viestejä, koska `send`-metodi ottaa muuttumattoman viittauksen `self`:iin. Emme myöskään voi noudattaa virheilmoituksen ehdotusta käyttää `&mut self`:iä sekä `impl`-metodissa että traitin määrittelyssä. Emme halua muuttaa `Messenger`-traitia pelkästään testauksen vuoksi. Sen sijaan meidän täytyy löytää tapa saada testikoodimme toimimaan oikein olemassa olevan suunnittelumme kanssa.

Tämä on tilanne, jossa sisäinen muuttuvuus voi auttaa! Tallennamme `sent_messages`:in `RefCell<T>`:n sisään, ja sitten `send`-metodi voi muokata `sent_messages`:ia tallentaakseen näkemämme viestit. Listauksessa 15-22 näytetään, miltä se näyttää.

<Listing number="15-22" file-name="src/lib.rs" caption="`RefCell<T>`:n käyttö sisäisen arvon muuttamiseen, vaikka ulompi arvo katsotaan muuttumattomaksi">

```rust,noplayground
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-22/src/lib.rs:here}}
```

</Listing>

`sent_messages`-kenttä on nyt tyyppiä `RefCell<Vec<String>>` `Vec<String>`:n sijaan. `new`-funktiossa luomme uuden `RefCell<Vec<String>>`-instanssin tyhjän vektorin ympärille.

`send`-metodin toteutuksessa ensimmäinen parametri on edelleen muuttumaton lainaus `self`:stä, mikä vastaa traitin määrittelyä. Kutsumme `borrow_mut`:ia `self.sent_messages`:in `RefCell<Vec<String>>`:ssa saadaksemme muuttuvan viittauksen `RefCell<Vec<String>>`:n sisällä olevaan arvoon, joka on vektori. Sitten voimme kutsua `push`:ia vektorin muuttuvalla viittauksella seurataksemme testin aikana lähetettyjä viestejä.

Viimeinen muutos, jonka meidän täytyy tehdä, on väitteessä: nähdäksemme, kuinka monta kohdetta sisäisessä vektorissa on, kutsumme `borrow`:ia `RefCell<Vec<String>>`:ssa saadaksemme muuttumattoman viittauksen vektoriin.

Nyt kun olet nähnyt, miten `RefCell<T>`:tä käytetään, syvennytään siihen, miten se toimii!

<!-- Old headings. Do not remove or links may break. -->

<a id="keeping-track-of-borrows-at-runtime-with-refcellt"></a>

#### Lainausten seuranta ajonaikana

Kun luomme muuttumattomia ja muuttuvia viittauksia, käytämme vastaavasti `&`- ja `&mut`-syntaksia. `RefCell<T>`:n kanssa käytämme `borrow`- ja `borrow_mut`-metodeja, jotka kuuluvat `RefCell<T>`:n turvalliseen API:in. `borrow`-metodi palauttaa älykkään osoittimen tyypin `Ref<T>`, ja `borrow_mut` palauttaa älykkään osoittimen tyypin `RefMut<T>`. Molemmat tyypit toteuttavat `Deref`:in, joten voimme käsitellä niitä kuin tavallisia viittauksia.

`RefCell<T>` seuraa, kuinka monta `Ref<T>`- ja `RefMut<T>`-älykästä osoitinta on parhaillaan aktiivisia. Joka kerta kun kutsumme `borrow`:ia, `RefCell<T>` kasvattaa aktiivisten muuttumattomien lainausten määrää. Kun `Ref<T>`-arvo poistuu näkyvyysalueelta, muuttumattomien lainausten määrä pienenee yhdellä. Aivan kuten käännösaikaiset lainausperiaatteet, `RefCell<T>` sallii useita muuttumattomia lainauksia tai yhden muuttuvan lainauksen milloin tahansa.

Jos yritämme rikkoa näitä sääntöjä, `RefCell<T>`:n toteutus panikoi ajonaikana sen sijaan, että saisimme kääntäjävirheen kuten viittausten kanssa. Listauksessa 15-23 on muutos listauksen 15-22 `send`-toteutukseen. Yritämme tarkoituksella luoda kaksi aktiivista muuttuvaa lainausta samaan näkyvyysalueeseen havainnollistaaksemme, että `RefCell<T>` estää meitä tekemästä tätä ajonaikana.

<Listing number="15-23" file-name="src/lib.rs" caption="Kahden muuttuvan viittauksen luominen samaan näkyvyysalueeseen nähdäksemme, että `RefCell<T>` panikoi">

```rust,ignore,panics
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-23/src/lib.rs:here}}
```

</Listing>

Luomme muuttujan `one_borrow` `borrow_mut`:ista palautetulle `RefMut<T>`-älykkäälle osoittimelle. Sitten luomme toisen muuttuvan lainauksen samalla tavalla muuttujaan `two_borrow`. Tämä tekee kaksi muuttuvaa viittausta samaan näkyvyysalueeseen, mikä ei ole sallittua. Kun ajamme kirjastomme testit, listauksen 15-23 koodi kääntyy ilman virheitä, mutta testi epäonnistuu:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-23/output.txt}}
```

Huomaa, että koodi panikoi viestillä `already borrowed: BorrowMutError`. Näin `RefCell<T>` käsittelee lainausperiaatteiden rikkomukset ajonaikana.

Valinta lainausvirheiden havaitsemiseen ajonaikana käännösaikaan sijaan, kuten tässä teimme, tarkoittaa, että saatat löytää virheitä koodissasi myöhemmin kehitysprosessissa: mahdollisesti vasta kun koodi on otettu tuotantoon. Lisäksi koodisi kärsii pienestä ajonaikaisesta suorituskykyrangaistuksesta lainausten seurannan vuoksi ajonaikana käännösaikaan sijaan. `RefCell<T>`:n käyttö mahdollistaa kuitenkin mock-olion kirjoittamisen, joka voi muokata itseään seuratakseen näkemiään viestejä kontekstissa, jossa vain muuttumattomat arvot ovat sallittuja. Voit käyttää `RefCell<T>`:tä sen kompromissien huolimatta saadaksesi enemmän toiminnallisuutta kuin tavalliset viittaukset tarjoavat.

<!-- Old headings. Do not remove or links may break. -->

<a id="having-multiple-owners-of-mutable-data-by-combining-rc-t-and-ref-cell-t"></a>
<a id="allowing-multiple-owners-of-mutable-data-with-rct-and-refcellt"></a>

### Muuttuvan datan usean omistajan salliminen

Yleinen tapa käyttää `RefCell<T>`:tä on yhdessä `Rc<T>`:n kanssa. Muistathan, että `Rc<T>` sallii usean omistajan datalle, mutta antaa vain muuttumattoman pääsyn kyseiseen dataan. Jos sinulla on `Rc<T>`, joka pitää `RefCell<T>`:tä, voit saada arvon, jolla voi olla useita omistajia _ja_ jota voit muuttaa!

Muistathan esimerkiksi listauksen 15-18 cons-listan esimerkin, jossa käytimme `Rc<T>`:tä salliaksemme useiden listojen jakaa toisen listan omistajuuden. Koska `Rc<T>` pitää vain muuttumattomia arvoja, emme voi muuttaa mitään listojen arvoista, kun olemme luoneet ne. Lisätään `RefCell<T>` sen kykyä muuttaa listojen arvoja. Listauksessa 15-24 näytetään, että käyttämällä `RefCell<T>`:tä `Cons`-määrittelyssä voimme muokata kaikissa listoissa tallennettua arvoa.

<Listing number="15-24" file-name="src/main.rs" caption="`Rc<RefCell<i32>>`:n käyttö muokattavan `List`:in luomiseen">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-24/src/main.rs}}
```

</Listing>

Luomme arvon, joka on `Rc<RefCell<i32>>`-instanssi, ja tallennamme sen muuttujaan nimeltä `value`, jotta voimme käyttää sitä suoraan myöhemmin. Sitten luomme `List`:in `a`:ssa `Cons`-variantilla, joka pitää `value`:a. Meidän täytyy kloonata `value`, jotta sekä `a` että `value` omistavat sisäisen arvon `5` sen sijaan, että siirtäisimme omistajuuden `value`:sta `a`:han tai että `a` lainaisi `value`:sta.

Käärimme listan `a` `Rc<T>`:hen, jotta kun luomme listat `b` ja `c`, ne voivat molemmat viitata `a`:han, kuten teimme listauksessa 15-18.

Kun olemme luoneet listat `a`:ssa, `b`:ssä ja `c`:ssä, haluamme lisätä `value`:n arvoon 10. Teemme tämän kutsumalla `borrow_mut`:ia `value`:lla, joka käyttää automaattista dereferointiominaisuutta, josta puhuimme kohdassa [„Missä on `->`-operaattori?”][wheres-the---operator]<!-- ignore --> luvussa 5, dereferoidakseen `Rc<T>`:n sisäiseen `RefCell<T>`-arvoon. `borrow_mut`-metodi palauttaa `RefMut<T>`-älykkään osoittimen, ja käytämme dereferointioperaattoria sen päällä ja muutamme sisäistä arvoa.

Kun tulostamme `a`:n, `b`:n ja `c`:n, näemme, että niillä kaikilla on muokattu arvo `15` arvon `5` sijaan:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-24/output.txt}}
```

Tämä tekniikka on melko näppärä! `RefCell<T>`:n avulla meillä on ulospäin muuttumaton `List`-arvo. Mutta voimme käyttää `RefCell<T>`:n metodeja, jotka tarjoavat pääsyn sen sisäiseen muuttuvuuteen, jotta voimme muokata dataamme tarvittaessa. Lainausperiaatteiden ajonaikaiset tarkistukset suojaavat meitä datakilpailuilta, ja joskus on syytä vaihtaa hieman nopeutta tämän joustavuuden vuoksi tietorakenteissamme. Huomaa, että `RefCell<T>` ei toimi monisäikeisessä koodissa! `Mutex<T>` on `RefCell<T>`:n säieturvallinen versio, ja käsittelemme `Mutex<T>`:tä luvussa 16.

[wheres-the---operator]: ch05-03-method-syntax.html#wheres-the---operator
