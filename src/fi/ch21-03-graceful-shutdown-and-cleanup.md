## Hallittu sammutus ja siivous

Listauksen 21-20 koodi vastaa pyyntöihin asynkronisesti säikeiden poolin avulla, kuten aioimme. Saamme varoituksia `workers`-, `id`- ja `thread`-kentistä, joita emme käytä suoraan — ne muistuttavat meitä siitä, ettei siivousta tehdä. Kun pysäytämme pääsäikeen vähemmän tyylikkäällä <kbd>ctrl</kbd>-<kbd>C</kbd>-menetelmällä, kaikki muut säikeet pysähtyvät heti, vaikka ne olisivat keskellä pyynnön käsittelyä.

Seuraavaksi toteutamme `Drop`-traitin kutsumaan `join`-metodia jokaiselle poolin säikeelle, jotta ne voivat viimeistellä työnsä ennen sulkemista. Toteutamme myös tavan kertoa säikeille, etteivät ne enää hyväksy uusia pyyntöjä ja että ne sammuttavat toimintansa. Nähdäksemme koodin toiminnassa muokkaamme palvelinta hyväksymään vain kaksi pyyntöä ennen säikeiden poolin hallittua sammuttamista.

Yksi huomio matkan varrella: mikään tästä ei vaikuta sulkeumien suorittamiseen liittyvään koodiin, joten kaikki olisi sama, jos käyttäisimme säikeiden poolia async-runtimeen.

### `Drop`-traitin toteuttaminen `ThreadPool`-rakenteelle

Aloitetaan toteuttamalla `Drop` säikeiden poolille. Kun pooli pudotetaan, kaikkien säikeiden pitäisi liittyä (`join`) varmistaakseen, että ne viimeistelevät työnsä. Listausta 21-22 näyttää ensimmäisen yrityksen `Drop`-toteutuksesta; tämä koodi ei vielä aivan toimi.

<Listing number="21-22" file-name="src/lib.rs" caption="Jokaisen säikeen liittäminen, kun säikeiden pooli menee näkyvyysalueen ulkopuolelle">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-22/src/lib.rs:here}}
```

</Listing>

Ensin silmukoidaan säikeiden poolin jokaisen `Worker`-instanssin yli. Käytämme `&mut`, koska `self` on muuttuva viite ja meidän täytyy myös pystyä mutatoimaan `worker`-instanssia. Jokaiselle `worker`-instanssille tulostamme viestin, joka kertoo kyseisen `Worker`-instanssin sammuttuvan, ja kutsumme sitten `join`-metodia kyseisen `Worker`-instanssin säikeelle. Jos `join`-kutsu epäonnistuu, käytämme `unwrap`-metodia saadaksemme Rustin panikoimaan ja siirtymään hallitsemattomaan sammutukseen.

Tässä on virhe, jonka saamme kääntäessämme tämän koodin:

```console
{{#include ../listings/ch21-web-server/listing-21-22/output.txt}}
```

Virhe kertoo, ettei `join`-metodia voi kutsua, koska meillä on vain muuttuva lainaus jokaisesta `worker`-instanssista ja `join` ottaa argumenttinsa omistukseen. Ratkaistaksemme ongelman meidän täytyy siirtää säie `Worker`-instanssista, joka omistaa `thread`-kentän, jotta `join` voi kuluttaa säikeen. Yksi tapa tehdä tämä on sama lähestymistapa kuin listauksessa 18-15. Jos `Worker` sisältäisi `Option<thread::JoinHandle<()>>`-kentän, voisimme kutsua `take`-metodia `Option`-rakenteella siirtääksemme arvon `Some`-variantista ja jättääksemme tilalle `None`-variantin. Toisin sanoen käynnissä oleva `Worker` sisältäisi `Some`-variantin `thread`-kentässä, ja kun haluaisimme siivota `Worker`-instanssin, korvaisimme `Some`-variantin `None`-variantilla, jolloin `Worker`-instanssilla ei olisi enää säiettä suoritettavaksi.

Tämä tilanne kuitenkin ilmenisi _ainoastaan_ `Worker`-instanssin pudotuksen yhteydessä. Vastineeksi meidän pitäisi käsitellä `Option<thread::JoinHandle<()>>`-tyyppiä aina, kun käytämme `worker.thread`-kenttää. Idiomatista Rustia käyttää `Option`-tyyppiä melko paljon, mutta kun huomaat kääriväsi jotain, jonka tiedät aina olevan olemassa, `Option`-tyyppiin kiertotienä, on hyvä etsiä vaihtoehtoisia lähestymistapoja koodin selkeyttämiseksi ja virhealttiuden vähentämiseksi.

Tässä tapauksessa parempi vaihtoehto on olemassa: `Vec::drain`-metodi. Se ottaa alueparametrin määrittääkseen, mitkä alkiot poistetaan vektorista, ja palauttaa iteraattorin näistä alkioista. `..`-alue syntaksin välittäminen poistaa vektorista _jokaisen_ arvon.

Meidän täytyy siis päivittää `ThreadPool`-rakenteen `drop`-toteutus näin:

<Listing file-name="src/lib.rs">

```rust
{{#rustdoc_include ../listings/ch21-web-server/no-listing-04-update-drop-definition/src/lib.rs:here}}
```

</Listing>

Tämä ratkaisee kääntäjävirheen eikä vaadi muita muutoksia koodiimme. Huomaa, että koska `drop` voidaan kutsua panikoinnin aikana, `unwrap` voi myös panikoida ja aiheuttaa kaksinkertaisen paniikin, joka kaataa ohjelman heti ja keskeyttää käynnissä olevan siivouksen. Tämä on ok esimerkkiohjelmalle, mutta sitä ei suositella tuotantokoodissa.

### Signaalin lähettäminen säikeille lopettaakseen työjonon kuuntelun

Kaikkien tekemiemme muutosten jälkeen koodimme kääntyy ilman varoituksia. Huono uutinen on kuitenkin, ettei koodi vielä toimi haluamallamme tavalla. Avain on `Worker`-instanssien säikeiden suorittamien sulkeumien logiikassa: tällä hetkellä kutsumme `join`-metodia, mutta se ei sammuta säikeitä, koska ne silmukoivat ikuisesti etsien töitä. Jos yritämme pudottaa `ThreadPool`-rakenteen nykyisellä `drop`-toteutuksellamme, pääsäie jumittuu ikuisesti odottamaan ensimmäisen säikeen valmistumista.

Korjataksemme ongelman tarvitsemme muutoksen `ThreadPool`-rakenteen `drop`-toteutukseen ja sitten muutoksen `Worker`-silmukkaan.

Ensin muutamme `ThreadPool`-rakenteen `drop`-toteutusta pudottamaan `sender`-kentän eksplisiittisesti ennen säikeiden valmistumisen odottamista. Listausta 21-23 näyttää muutokset `ThreadPool`-rakenteeseen `sender`-kentän eksplisiittiseen pudottamiseen. Toisin kuin säikeen kohdalla, tarvitsemme tässä _Option_-tyypin, jotta voimme siirtää `sender`-kentän pois `ThreadPool`-rakenteesta `Option::take`-metodilla.

<Listing number="21-23" file-name="src/lib.rs" caption="`sender`-kentän eksplisiittinen pudottaminen ennen `Worker`-säikeiden liittämistä">

```rust,noplayground,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-23/src/lib.rs:here}}
```

</Listing>

`sender`-kentän pudottaminen sulkee kanavan, mikä ilmaisee, ettei enempää viestejä lähetetä. Kun näin tapahtuu, kaikki `recv`-kutsut, joita `Worker`-instanssit tekevät äärettömässä silmukassaan, palauttavat virheen. Listauksessa 21-24 muutamme `Worker`-silmukan poistumaan siististi silmukasta tässä tapauksessa, mikä tarkoittaa, että säikeet valmistuvat, kun `ThreadPool`-rakenteen `drop`-toteutus kutsuu niille `join`-metodia.

<Listing number="21-24" file-name="src/lib.rs" caption="Silmukasta eksplisiittinen poistuminen, kun `recv` palauttaa virheen">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-24/src/lib.rs:here}}
```

</Listing>

Nähdäksemme koodin toiminnassa muokataan `main`-funktiota hyväksymään vain kaksi pyyntöä ennen palvelimen hallittua sammuttamista, kuten listauksessa 21-25.

<Listing number="21-25" file-name="src/main.rs" caption="Palvelimen sammuttaminen kahden pyynnön käsittelyn jälkeen poistumalla silmukasta">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/listing-21-25/src/main.rs:here}}
```

</Listing>

Et haluaisi oikean maailman verkkopalvelimen sammuttavan toimintansa vain kahden pyynnön jälkeen. Tämä koodi vain demonstroi, että hallittu sammutus ja siivous toimivat.

`take`-metodi on määritelty `Iterator`-traitissa ja rajoittaa iteraation enintään kahteen ensimmäiseen alkioon. `ThreadPool` menee näkyvyysalueen ulkopuolelle `main`-funktion lopussa, ja `drop`-toteutus suoritetaan.

Käynnistä palvelin komennolla `cargo run` ja tee kolme pyyntöä. Kolmannen pyynnön pitäisi epäonnistua, ja terminaalissasi pitäisi näkyä suunnilleen seuraavanlainen tuloste:

<!-- manual-regeneration
cd listings/ch21-web-server/listing-21-25
cargo run
curl http://127.0.0.1:7878
curl http://127.0.0.1:7878
curl http://127.0.0.1:7878
third request will error because server will have shut down
copy output below
Can't automate because the output depends on making requests
-->

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.41s
     Running `target/debug/hello`
Worker 0 got a job; executing.
Shutting down.
Shutting down worker 0
Worker 3 got a job; executing.
Worker 1 disconnected; shutting down.
Worker 2 disconnected; shutting down.
Worker 3 disconnected; shutting down.
Worker 0 disconnected; shutting down.
Shutting down worker 1
Shutting down worker 2
Shutting down worker 3
```

Saatat nähdä eri järjestyksessä `Worker`-tunnisteita ja viestejä. Näemme viesteistä, miten koodi toimii: `Worker`-instanssit 0 ja 3 saivat kaksi ensimmäistä pyyntöä. Palvelin lopetti yhteyksien hyväksymisen toisen yhteyden jälkeen, ja `ThreadPool`-rakenteen `Drop`-toteutus alkaa suorittua ennen kuin `Worker 3` edes aloittaa työnsä. `sender`-kentän pudottaminen katkaisee yhteyden kaikkiin `Worker`-instansseihin ja käskee niitä sammuttamaan toimintansa. `Worker`-instanssit tulostavat kukin viestin katkaistessaan yhteyden, ja sitten säikeiden pooli kutsuu `join`-metodia odottaakseen jokaisen `Worker`-säikeen valmistumista.

Huomaa yksi mielenkiintoinen piirre tässä suorituksessa: `ThreadPool` pudotti `sender`-kentän, ja ennen kuin yksikään `Worker` sai virheen `recv`-kutsusta, yritimme liittää (`join`) `Worker 0`:aa. `Worker 0` ei ollut vielä saanut virhettä `recv`-kutsusta, joten pääsäie blokkaantui odottamaan `Worker 0`:n valmistumista. Sillä välin `Worker 3` vastaanotti työn, ja sitten kaikki säikeet saivat virheen. Kun `Worker 0` valmistui, pääsäie odotti loput `Worker`-instanssit valmiiksi. Silloin ne olivat kaikki poistuneet silmukoistaan ja pysähtyneet.

Onnittelut! Olemme nyt viimeistelleet projektimme; meillä on perusverkkopalvelin, joka käyttää säikeiden poolia vastatakseen asynkronisesti. Pystymme suorittamaan palvelimen hallitun sammutuksen, joka siivoaa kaikki poolin säikeet.

Tässä on koko koodi viitteeksi:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/no-listing-07-final-code/src/main.rs}}
```

</Listing>

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-07-final-code/src/lib.rs}}
```

</Listing>

Voimme tehdä täällä vielä enemmän! Jos haluat jatkaa projektin parantamista, tässä muutamia ideoita:

- Lisää dokumentaatiota `ThreadPool`-rakenteelle ja sen julkisille metodeille.
- Lisää testejä kirjaston toiminnallisuudelle.
- Muuta `unwrap`-kutsut vankemmaksi virheenkäsittelyksi.
- Käytä `ThreadPool`-rakennetta johonkin muuhun tehtävään kuin verkkopyyntöjen palvelemiseen.
- Etsi säikeiden pooli -crate [crates.io](https://crates.io/)-sivustolta ja toteuta samankaltainen verkkopalvelin cratea käyttäen. Vertaa sitten sen API:a ja vankkuutta toteuttamaamme säikeiden pooliin.

## Yhteenveto

Hyvin tehty! Olet päässyt kirjan loppuun! Haluamme kiittää sinua siitä, että liityit mukaan tälle Rust-kierrokselle. Olet nyt valmis toteuttamaan omia Rust-projektejasi ja auttamaan muiden projekteissa. Muista, että Rust-yhteisössä on tervetulleita rustilaisia, jotka auttavat mielellään kaikissa haasteissa Rust-matkallasi.
