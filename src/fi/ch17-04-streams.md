<!-- Old headings. Do not remove or links may break. -->

<a id="streams"></a>

## Streamit: futuret peräkkäin

Muista, miten käytimme async-kanavamme vastaanottajaa aiemmin tässä luvussa [”Viestinvälitys”][17-02-messages]<!-- ignore --> -osiossa. Async-`recv`-metodi tuottaa kohteiden sarjan ajan kuluessa. Tämä on esimerkki paljon yleisemmästä mallista, jota kutsutaan _streamiksi_. Monet käsitteet voidaan luontevasti esittää streaminä: jonoon tulevat kohteet, tiedostojärjestelmästä inkrementaalisesti haetut dataosuudet, kun koko aineisto on liian suuri tietokoneen muistille, tai verkossa ajan kuluessa saapuva data. Koska streamit ovat futureja, voimme käyttää niitä minkä tahansa muun futuren kanssa ja yhdistellä niitä mielenkiintoisilla tavoilla. Esimerkiksi voimme niputtaa tapahtumia välttääksemme liian monta verkkokutsua, asettaa aikarajoja pitkään kestävien operaatioiden sarjoille tai rajoittaa käyttöliittymätapahtumia turhan työn välttämiseksi.

Näimme kohteiden sarjan luvussa 13, kun tarkastelimme `Iterator`-traitiä [”Iterator-trait ja `next`-metodi”][iterator-trait]<!-- ignore --> -osiossa, mutta iteraattorien ja async-kanavan vastaanottajan välillä on kaksi eroa. Ensimmäinen ero on aika: iteraattorit ovat synkronisia, kun taas kanavan vastaanottaja on asynkroninen. Toinen ero on API. Kun työskentelemme suoraan `Iterator`:in kanssa, kutsumme sen synkronista `next`-metodia. `trpl::Receiver`-streamin kanssa kutsuimme sen sijaan asynkronista `recv`-metodia. Muuten nämä API:t tuntuvat hyvin samankaltaisilta, eikä tämä samankaltaisuus ole sattumaa. Stream on kuin asynkroninen iteraation muoto. Vaikka `trpl::Receiver` odottaa erityisesti viestien vastaanottamista, yleiskäyttöinen stream-API on paljon laajempi: se tarjoaa seuraavan kohteen samalla tavalla kuin `Iterator`, mutta asynkronisesti.

Iteraattorien ja streamien samankaltaisuus Rustissa tarkoittaa, että voimme itse asiassa luoda streamin mistä tahansa iteraattorista. Kuten iteraattorin kanssa, voimme työskennellä streamin kanssa kutsumalla sen `next`-metodia ja odottamalla tulosta, kuten listauksessa 17-21, joka ei vielä käänny.

<Listing number="17-21" caption="Streamin luominen iteraattorista ja sen arvojen tulostaminen" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-21/src/main.rs:stream}}
```

</Listing>

Aloitamme numerotaulukosta, jonka muunnamme iteraattoriksi ja jonka päällä kutsumme `map`:ia kaikkien arvojen kaksinkertaistamiseksi. Sitten muunnamme iteraattorin streamiksi `trpl::stream_from_iter`-funktiolla. Seuraavaksi käymme läpi streamin kohteita niiden saapuessa `while let` -silmukalla.

Valitettavasti kun yritämme suorittaa koodin, se ei käänny vaan ilmoittaa, ettei `next`-metodia ole saatavilla:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-21
cargo build
copy only the error output
-->

```text
error[E0599]: no method named `next` found for struct `tokio_stream::iter::Iter` in the current scope
  --> src/main.rs:10:40
   |
10 |         while let Some(value) = stream.next().await {
   |                                        ^^^^
   |
   = help: items from traits can only be used if the trait is in scope
help: the following traits which provide `next` are implemented but not in scope; perhaps you want to import one of them
   |
1  + use crate::trpl::StreamExt;
   |
1  + use futures_util::stream::stream::StreamExt;
   |
1  + use std::iter::Iterator;
   |
1  + use std::str::pattern::Searcher;
   |
help: there is a method `try_next` with a similar name
   |
10 |         while let Some(value) = stream.try_next().await {
   |                                        ~~~~~~~~
```

Kuten tämä tuloste selittää, kääntäjävirheen syy on se, että tarvitsemme oikean traitin näkyviin voidaksemme käyttää `next`-metodia. Keskustelumme perusteella saatat odottaa traitin olevan `Stream`, mutta se on itse asiassa `StreamExt`. Lyhenne sanasta _extension_ (laajennus), `Ext` on yleinen malli Rust-yhteisössä laajentaa yhtä traitiä toisella.

`Stream`-trait määrittelee matalan tason rajapinnan, joka yhdistää käytännössä `Iterator`- ja `Future`-traitit. `StreamExt` tarjoaa korkeamman tason API-joukon `Stream`:in päälle, mukaan lukien `next`-metodin ja muita apumetodeja, jotka ovat samankaltaisia kuin `Iterator`-traitin tarjoamat. `Stream` ja `StreamExt` eivät ole vielä osa Rustin standardikirjastoa, mutta useimmat ekosysteemin crate:t käyttävät samankaltaisia määrittelyjä.

Kääntäjävirheen korjaus on lisätä `use`-lause `trpl::StreamExt`:ille, kuten listauksessa 17-22.

<Listing number="17-22" caption="Iteraattorin käyttö onnistuneesti streamin pohjana" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-22/src/main.rs:all}}
```

</Listing>

Kun kaikki nämä palaset on yhdistetty, koodi toimii haluamallamme tavalla! Lisäksi, koska meillä on nyt `StreamExt` näkyvissä, voimme käyttää kaikkia sen apumetodeja, aivan kuten iteraattoreiden kanssa.

[17-02-messages]: ch17-02-concurrency-with-async.html#message-passing
[iterator-trait]: ch13-02-iterators.html#the-iterator-trait-and-the-next-method
