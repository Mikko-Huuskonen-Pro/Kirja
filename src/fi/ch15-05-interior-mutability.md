## `RefCell<T>` ja sisäisen mutabiliteetin malli

_Sisäinen mutabiliteetti_ on Rustin suunnittelumalli, joka sallii datan muuttamisen
vaikka dataan olisi muuttumattomia viittauksia; normaalisti lainaussäännöt kieltävät
tämän. Datan muuttamiseksi malli käyttää `unsafe`-koodia tietorakenteen sisällä
taivuttaakseen Rustin tavanomaisia sääntöjä, jotka hallitsevat muuttamista ja lainaamista.
Unsafe-koodi kertoo kääntäjälle, että tarkistamme säännöt käsin sen sijaan, että
luottaisimme kääntäjään niiden tarkistamisessa; käsittelemme unsafe-koodia tarkemmin
Luvussa 20.

Voimme käyttää sisäisen mutabiliteetin mallia käyttäviä tyyppejä vain, kun voimme
varmistaa, että lainaussääntöjä noudatetaan ajonaikana, vaikka kääntäjä ei voi sitä
taata. Mukana oleva `unsafe`-koodi kääritään sitten turvalliseen API:in, ja ulompi
tyyppi on silti muuttumaton.

Tutkitaan tätä käsitettä katsomalla `RefCell<T>`-tyyppiä, joka noudattaa sisäisen
mutabiliteetin mallia.

### Lainaussääntöjen pakottaminen ajonaikana `RefCell<T>`:llä

Toisin kuin `Rc<T>`, `RefCell<T>`-tyyppi edustaa yksittäistä omistajuutta sen sisältämään
dataan. Mikä siis tekee `RefCell<T>`:stä erilaisen kuin esimerkiksi `Box<T>`? Muista
Luvussa 4 opitut lainaussäännöt:

- Milloin tahansa sinulla voi olla _joko_ (mutta ei molempia) yksi muuttuva viite
  tai mikä tahansa määrä muuttumattomia viitteitä.
- Viitteiden on aina oltava kelvollisia.

Viitteillä ja `Box<T>`:llä lainaussääntöjen invariantit pakotetaan käännösaikana.
`RefCell<T>`:llä nämä invariantit pakotetaan _ajonaikana_. Viitteillä, jos rikot nämä
säännöt, saat käännösvirheen. `RefCell<T>`:llä, jos rikot nämä säännöt, ohjelmasi
kaatuu paniikkiin ja päättyy.

Käännösaikaisen lainaussääntöjen tarkistuksen etuja ovat, että virheet havaitaan
aikaisemmin kehitysprosessissa, eikä suorituskykyyn ole vaikutusta, koska kaikki
analyysi tehdään etukäteen. Näistä syistä lainaussääntöjen tarkistaminen käännösaikana
on paras valinta useimmissa tapauksissa, minkä vuoksi se on Rustin oletus.

Ajonaikaisen lainaussääntöjen tarkistuksen etu on, että tiettyjä muistiturvallisia
tilanteita sallitaan, joissa käännösaikaiset tarkistukset olisivat kieltäneet ne.
Staattinen analyysi, kuten Rustin kääntäjä, on luonnostaan konservatiivinen. Joitakin
koodin ominaisuuksia on mahdotonta havaita analysoimalla koodia: kuuluisin esimerkki
on pysähtymisongelma (Halting Problem), joka on tämän kirjan ulkopuolella mutta on
mielenkiintoinen tutkimuskohde.

Koska jotkin analyysit ovat mahdottomia, jos Rustin kääntäjä ei voi olla varma, että
koodi noudattaa omistajuussääntöjä, se saattaa hylätä oikean ohjelman; tällä tavalla
se on konservatiivinen. Jos Rust hyväksyisi virheellisen ohjelman, käyttäjät eivät
voisi luottaa Rustin antamiin takuisiin. Jos Rust kuitenkin hylkää oikean ohjelman,
ohjelmoijaa vaivataan, mutta mitään katastrofaalista ei voi tapahtua. `RefCell<T>`-tyyppi
on hyödyllinen, kun olet varma, että koodisi noudattaa lainaussääntöjä, mutta kääntäjä
ei pysty ymmärtämään ja takaamaan sitä.

Samoin kuin `Rc<T>`, `RefCell<T>` on vain yksisäikeisiin tilanteisiin, ja se antaa
käännösaikaisen virheen, jos yrität käyttää sitä monisäikeisessä kontekstissa. Puhumme
siitä, miten saada `RefCell<T>`:n toiminnallisuus monisäikeisessä ohjelmassa Luvussa 16.

Tässä yhteenveto syistä valita `Box<T>`, `Rc<T>` tai `RefCell<T>`:

- `Rc<T>` mahdollistaa useita omistajia samalle datalle; `Box<T>`:llä ja `RefCell<T>`:llä
  on yksittäiset omistajat.
- `Box<T>` sallii muuttumattomat tai muuttuvat lainaukset, jotka tarkistetaan käännösaikana;
  `Rc<T>` sallii vain muuttumattomat lainaukset, jotka tarkistetaan käännösaikana;
  `RefCell<T>` sallii muuttumattomat tai muuttuvat lainaukset, jotka tarkistetaan ajonaikana.
- Koska `RefCell<T>` sallii muuttuvat lainaukset, jotka tarkistetaan ajonaikana, voit
  muuttaa `RefCell<T>`:n sisällä olevaa arvoa vaikka `RefCell<T>` olisi muuttumaton.

Arvon sisällä olevan arvon muuttaminen muuttumattomassa arvossa on _sisäisen mutabiliteetin_
malli. Katsotaan tilannetta, jossa sisäinen mutabiliteetti on hyödyllinen, ja tutkitaan,
miten se on mahdollista.

### Sisäinen mutabiliteetti: muuttuva lainaus muuttumattomaan arvoon

Lainaussääntöjen seuraus on, että kun sinulla on muuttumaton arvo, et voi lainata sitä
muuttuvasti. Esimerkiksi tämä koodi ei käänny:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/no-listing-01-cant-borrow-immutable-as-mutable/src/main.rs}}
```

Jos yrittäisit kääntää tämän koodin, saisit seuraavan virheen:

```console
{{#include ../listings/ch15-smart-pointers/no-listing-01-cant-borrow-immutable-as-mutable/output.txt}}
```

On kuitenkin tilanteita, joissa olisi hyödyllistä, että arvo muuttaisi itseään metodeissaan
mutta näyttäisi muuttumattomalta muulle koodille. Arvon metodien ulkopuolella oleva koodi
ei voisi muuttaa arvoa. `RefCell<T>`:n käyttö on yksi tapa saada sisäinen mutabiliteetti,
mutta `RefCell<T>` ei kierrä lainaussääntöjä kokonaan: kääntäjän lainaustarkistin sallii
tämän sisäisen mutabiliteetin, ja lainaussäännöt tarkistetaan ajonaikana käännösaian sijaan.
Jos rikot sääntöjä, saat `panic!`:n käännösvirheen sijaan.

Käydään läpi käytännön esimerkki, jossa voimme käyttää `RefCell<T>`:tä muuttamaan
muuttumatonta arvoa, ja katsotaan, miksi se on hyödyllistä.

#### Sisäisen mutabiliteetin käyttötapaus: mock-oliot

Joskus testauksen aikana ohjelmoija käyttää yhtä tyyppiä toisen tilalla havaitakseen
tiettyä käyttäytymistä ja varmistaakseen, että se on toteutettu oikein. Tätä paikkamerkkityyppiä
kutsutaan _testikakaksi_ (`test double`). Ajattele sitä elokuvan ”sijaisnäyttelijän”
(`stunt double`) merkityksessä, jossa henkilö astuu esiin ja korvaa näyttelijän tekemään
tietyn hankalan kohtauksen. Testikakut korvaavat muita tyyppejä testejä ajettaessa.
_Mock-oliot_ ovat erityisiä testikakkujen tyyppejä, jotka tallentavat testin aikana
tapahtuvat asiat, jotta voit varmistaa, että oikeat toiminnot tapahtuivat.

Rustissa ei ole olioita samassa merkityksessä kuin muissa kielissä, eikä Rustissa ole
mock-olioiden toiminnallisuutta sisäänrakennettuna standardikirjastoon kuten joissakin
muissa kielissä. Voit kuitenkin ehdottomasti luoda structin, joka palvelee samoja tarkoituksia
kuin mock-olio.

Tässä on skenaario, jota testaamme: luomme kirjaston, joka seuraa arvoa suhteessa
enimmäisarvoon ja lähettää viestejä sen mukaan, kuinka lähellä enimmäisarvoa nykyinen
arvo on. Tätä kirjastoa voitaisiin käyttää esimerkiksi seuraamaan käyttäjän kiintiötä
sallittujen API-kutsujen määrälle.

Kirjastomme tarjoaa vain toiminnallisuuden seurata, kuinka lähellä enimmäisarvoa arvo
on ja mitä viestejä pitäisi lähettää milloinkin. Kirjastoamme käyttäviltä sovelluksilta
odotetaan viestien lähetysmekanismin tarjoamista: sovellus voisi näyttää viestin sovelluksessa,
lähettää sähköpostin, lähettää tekstiviestin tai tehdä jotain muuta. Kirjaston ei tarvitse
tietää tuota yksityiskohtaa. Sen tarvitsee vain jotain, joka toteuttaa tarjoamamme
traitin nimeltä `Messenger`. Listauksessa 15-20 on kirjaston koodi:

<Listing number="15-20" file-name="src/lib.rs" caption="Kirjasto, joka seuraa kuinka lähellä arvo on enimmäisarvoa ja varoittaa, kun arvo on tietyillä tasoilla">

```rust,noplayground
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-20/src/lib.rs}}
```

</Listing>

Yksi tärkeä osa tässä koodissa on, että `Messenger`-traitilla on yksi metodi nimeltä
`send`, joka ottaa muuttumattoman viitteen `self`:ään ja viestin tekstin. Tämä trait
on rajapinta, jonka mock-oliomme täytyy toteuttaa, jotta mockia voidaan käyttää samalla
tavalla kuin oikeaa oliota. Toinen tärkeä osa on, että haluamme testata `LimitTracker`:n
`set_value`-metodin käyttäytymistä. Voimme muuttaa `value`-parametrille välittämäämme
arvoa, mutta `set_value` ei palauta mitään, josta voisimme tehdä väittämiä. Haluamme
voida sanoa, että jos luomme `LimitTracker`:in jollain, joka toteuttaa `Messenger`-traitin,
ja tietyllä `max`-arvolla, kun välitämme eri lukuja `value`:lle, messengerille kerrotaan
lähettää sopivat viestit.

Tarvitsemme mock-olion, joka `send`-kutsun sijaan ei lähetä sähköpostia tai tekstiviestiä,
vaan vain seuraa viestejä, joita sille kerrotaan lähettää. Voimme luoda uuden mock-olioinstanssin,
luoda `LimitTracker`:in, joka käyttää mock-oliota, kutsua `set_value`-metodia `LimitTracker`:lla
ja tarkistaa, että mock-oliolla on odottamamme viestit. Listauksessa 15-21 on yritys
toteuttaa mock-olio juuri tätä varten, mutta lainaustarkistin ei salli sitä:

<Listing number="15-21" file-name="src/lib.rs" caption="Yritys toteuttaa `MockMessenger`, jota lainaustarkistin ei salli">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-21/src/lib.rs:here}}
```

</Listing>

Tämä testikoodi määrittelee `MockMessenger`-structin, jolla on `sent_messages`-kenttä
`Vec<String>`-arvojen kanssa seuratakseen viestejä, joita sille kerrotaan lähettää.
Määrittelemme myös assosioituneen funktion `new`, jotta uusien `MockMessenger`-arvojen
luominen tyhjällä viestiluettelolla on kätevää. Toteutamme sitten `Messenger`-traitin
`MockMessenger`:lle, jotta voimme antaa `MockMessenger`:in `LimitTracker`:ille. `send`-metodin
määrittelyssä otamme parametrina välitetyn viestin ja tallennamme sen `MockMessenger`:in
`sent_messages`-luetteloon.

Testissä testaamme, mitä tapahtuu, kun `LimitTracker`:lle kerrotaan asettamaan `value`
joksikin, joka on yli 75 prosenttia `max`-arvosta. Ensin luomme uuden `MockMessenger`:in,
joka alkaa tyhjällä viestiluettelolla. Sitten luomme uuden `LimitTracker`:in ja annamme
sille viitteen uuteen `MockMessenger`:iin ja `max`-arvon 100. Kutsumme `set_value`-metodia
`LimitTracker`:lla arvolla 80, joka on yli 75 prosenttia luvusta 100. Sitten varmistamme,
että `MockMessenger`:in seuraamassa viestiluettelossa pitäisi nyt olla yksi viesti.

Tässä testissä on kuitenkin yksi ongelma, kuten tässä näytetään:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-21/output.txt}}
```

Emme voi muokata `MockMessenger`:ia seurataksemme viestejä, koska `send`-metodi ottaa
muuttumattoman viitteen `self`:ään. Emme myöskään voi noudattaa virhetekstin ehdotusta
käyttää `&mut self`:ää sekä `impl`-metodissa että `trait`-määrittelyssä. Emme halua
muuttaa `Messenger`-traitia pelkästään testauksen vuoksi. Sen sijaan meidän täytyy löytää
tapa saada testikoodimme toimimaan oikein olemassa olevan suunnittelumme kanssa.

Tämä on tilanne, jossa sisäinen mutabiliteetti voi auttaa! Tallennamme `sent_messages`:in
`RefCell<T>`:n sisään, ja sitten `send`-metodi voi muokata `sent_messages`:ia tallentaakseen
näkemämme viestit. Listauksessa 15-22 näkyy, miltä se näyttää:

<Listing number="15-22" file-name="src/lib.rs" caption="`RefCell<T>`:n käyttö sisäisen arvon muuttamiseen, kun ulompi arvo katsotaan muuttumattomaksi">

```rust,noplayground
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-22/src/lib.rs:here}}
```

</Listing>

`sent_messages`-kenttä on nyt tyyppiä `RefCell<Vec<String>>` `Vec<String>`:n sijaan.
`new`-funktiossa luomme uuden `RefCell<Vec<String>>`-instanssin tyhjän vektorin ympärille.

`send`-metodin toteutuksessa ensimmäinen parametri on silti muuttumaton lainaus `self`:stä,
mikä vastaa trait-määrittelyä. Kutsumme `borrow_mut`:ia `RefCell<Vec<String>>`:ssa
`self.sent_messages`:issa saadaksemme muuttuvan viitteen `RefCell<Vec<String>>`:n sisällä
olevaan arvoon, joka on vektori. Sitten voimme kutsua `push`:ia vektorin muuttuvalla
viitteellä seurataksemme testin aikana lähetettyjä viestejä.

Viimeinen muutos, jonka meidän täytyy tehdä, on väittämässä: nähdäksemme, kuinka monta
alkiota sisäisessä vektorissa on, kutsumme `borrow`:ia `RefCell<Vec<String>>`:ssa saadaksemme
muuttumattoman viitteen vektoriin.

Nyt kun olet nähnyt, miten `RefCell<T>`:tä käytetään, kaivaudutaan siihen, miten se toimii!

#### Lainausten seuranta ajonaikana `RefCell<T>`:llä

Kun luomme muuttumattomia ja muuttuvia viitteitä, käytämme `&`- ja `&mut`-syntaksia.
`RefCell<T>`:llä käytämme `borrow`- ja `borrow_mut`-metodeja, jotka kuuluvat `RefCell<T>`:n
turvalliseen API:in. `borrow`-metodi palauttaa älykkään osoittimen tyypin `Ref<T>`, ja
`borrow_mut` palauttaa älykkään osoittimen tyypin `RefMut<T>`. Molemmat tyypit toteuttavat
`Deref`:in, joten voimme käsitellä niitä kuten tavallisia viitteitä.

`RefCell<T>` seuraa, kuinka monta `Ref<T>`- ja `RefMut<T>`-älykästä osoitinta on tällä
hetkellä aktiivisia. Joka kerta kun kutsumme `borrow`:ia, `RefCell<T>` kasvattaa laskuriaan
siitä, kuinka monta muuttumatonta lainausta on aktiivisia. Kun `Ref<T>`-arvo poistuu
laajuudesta, muuttumattomien lainausten määrä vähenee yhdellä. Aivan kuten käännösaikaiset
lainaussäännöt, `RefCell<T>` sallii meidän olla monta muuttumatonta lainausta tai yksi
muuttuva lainaus milloin tahansa.

Jos yritämme rikkoa näitä sääntöjä, sen sijaan että saisimme käännösvirheen kuten viitteillä,
`RefCell<T>`:n toteutus kaatuu ajonaikana. Listauksessa 15-23 on muokattu `send`-toteutus
Listauksesta 15-22. Yritämme tarkoituksella luoda kaksi muuttuvaa lainausta aktiivisiksi
samaan laajuuteen havainnollistaaksemme, että `RefCell<T>` estää meitä tekemästä tätä
ajonaikana.

<Listing number="15-23" file-name="src/lib.rs" caption="Kahden muuttuvan viitteen luominen samaan laajuuteen nähdäksemme, että `RefCell<T>` kaatuu paniikkiin">

```rust,ignore,panics
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-23/src/lib.rs:here}}
```

</Listing>

Luomme muuttujan `one_borrow` `borrow_mut`:ista palautetulle `RefMut<T>`-älykkäälle osoittimelle.
Sitten luomme toisen muuttuvan lainauksen samalla tavalla muuttujaan `two_borrow`. Tämä
tekee kaksi muuttuvaa viitettä samaan laajuuteen, mikä ei ole sallittua. Kun ajamme
kirjastomme testit, Listauksen 15-23 koodi kääntyy ilman virheitä, mutta testi epäonnistuu:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-23/output.txt}}
```

Huomaa, että koodi kaatui viestillä `already borrowed: BorrowMutError`. Näin `RefCell<T>`
käsittelee lainaussääntöjen rikkomukset ajonaikana.

Valinta lainausvirheiden havaitsemisesta ajonaikana käännösaian sijaan, kuten teimme
tässä, tarkoittaa, että virheet saatetaan löytää myöhemmin kehitysprosessissa: mahdollisesti
vasta kun koodi on otettu tuotantoon. Lisäksi koodiin tulee pieni suorituskykyrangaistus
lainausten seurannasta ajonaikana käännösaian sijaan. `RefCell<T>`:n käyttö mahdollistaa
kuitenkin mock-olion kirjoittamisen, joka voi muokata itseään seuratakseen näkemiään
viestejä kontekstissa, jossa vain muuttumattomat arvot ovat sallittuja. Voit käyttää
`RefCell<T>`:tä sen kompromisseista huolimatta saadaksesi enemmän toiminnallisuutta kuin
tavalliset viitteet tarjoavat.

### Useita omistajia muuttuvalla datalle yhdistämällä `Rc<T>` ja `RefCell<T>`

Yleinen tapa käyttää `RefCell<T>`:tä on yhdistelmässä `Rc<T>`:n kanssa. Muista, että
`Rc<T>` antaa sinulle useita omistajia jollekin datalle, mutta se antaa vain muuttumattoman
pääsyn kyseiseen dataan. Jos sinulla on `Rc<T>`, joka sisältää `RefCell<T>`:n, voit
saada arvon, jolla voi olla useita omistajia _ja_ jota voit muuttaa!

Esimerkiksi muista cons-listan esimerkki Listauksessa 15-18, jossa käytimme `Rc<T>`:tä
salliaksemme useiden listojen jakaa toisen listan omistajuuden. Koska `Rc<T>` sisältää
vain muuttumattomia arvoja, emme voi muuttaa mitään listojen arvoista, kun olemme luoneet
ne. Lisätään `RefCell<T>` saadaksemme kyky muuttaa listojen arvoja. Listauksessa 15-24
näytetään, että käyttämällä `RefCell<T>`:tä `Cons`-määrittelyssä voimme muokata kaikissa
listoissa tallennettua arvoa:

<Listing number="15-24" file-name="src/main.rs" caption="`Rc<RefCell<i32>>`:n käyttö muokattavan `List`:n luomiseen">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-24/src/main.rs}}
```

</Listing>

Luomme arvon, joka on `Rc<RefCell<i32>>`-instanssi, ja tallennamme sen muuttujaan
`value`, jotta pääsemme siihen suoraan myöhemmin. Sitten luomme `List`:n `a`:ssa
`Cons`-variantilla, joka sisältää `value`:n. Meidän täytyy kloonata `value`, jotta sekä
`a` että `value` omistavat sisäisen arvon `5` sen sijaan, että omistajuus siirtyisi
`value`:sta `a`:han tai `a` lainaisi `value`:sta.

Käärimme listan `a` `Rc<T>`:hen, jotta kun luomme listat `b` ja `c`, ne voivat molemmat
viitata `a`:han, kuten teimme Listauksessa 15-18.

Kun olemme luoneet listat `a`:ssa, `b`:ssä ja `c`:ssä, haluamme lisätä 10 arvoon `value`:ssa.
Teemme tämän kutsumalla `borrow_mut`:ia `value`:lla, joka käyttää automaattista dereferointiominaisuutta,
josta puhuimme Luvussa 5 (katso [”Missä on `->`-operaattori?”][wheres-the---operator]<!-- ignore -->)
dereferoidakseen `Rc<T>`:n sisäiseen `RefCell<T>`-arvoon. `borrow_mut`-metodi palauttaa
`RefMut<T>`-älykkään osoittimen, ja käytämme dereferenssioperaattoria sen päällä ja
muutamme sisäistä arvoa.

Kun tulostamme `a`:n, `b`:n ja `c`:n, näemme, että niillä kaikilla on muokattu arvo
15 eikä 5:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-24/output.txt}}
```

Tämä tekniikka on melko siisti! Käyttämällä `RefCell<T>`:tä meillä on ulospäin muuttumaton
`List`-arvo. Mutta voimme käyttää `RefCell<T>`:n metodeja, jotka tarjoavat pääsyn sen
sisäiseen mutabiliteettiin, jotta voimme muokata dataamme tarvittaessa. Lainaussääntöjen
ajonaikaiset tarkistukset suojaavat meitä datakilpailuilta, ja joskus on syytä vaihtaa
hieman nopeutta tämän joustavuuden vuoksi tietorakenteissamme. Huomaa, että `RefCell<T>`
ei toimi monisäikeisessä koodissa! `Mutex<T>` on `RefCell<T>`:n säieystävällinen versio,
ja käsittelemme `Mutex<T>`:tä Luvussa 16.

[wheres-the---operator]: ch05-03-method-syntax.html#wheres-the---operator
