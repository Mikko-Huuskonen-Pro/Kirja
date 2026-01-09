# Rust-ohjelmointikieli

[The Rust Programming Language](title-page.md)
[Foreword](foreword.md)
[Johdanto](ch00-00-introduction.md)

## Aloittaminen

- [Aloittaminen](ch01-00-getting-started.md)
  - [Asennus](ch01-01-installation.md)
  - [Hei, maailma!](ch01-02-hello-world.md)
  - [Hei, Cargo!](ch01-03-hello-cargo.md)

- [Arvauspelin ohjelmointi](ch02-00-guessing-game-tutorial.md)

- [Yleiset ohjelmointikäsitteet](ch03-00-common-programming-concepts.md)
  - [Muuttujat ja muuttumattomuus](ch03-01-variables-and-mutability.md)
  - [Tietotyypit](ch03-02-data-types.md)
  - [Funktiot](ch03-03-how-functions-work.md)
  - [Kommentit](ch03-04-comments.md)
  - [Ohjausrakenne](ch03-05-control-flow.md)

- [Omistajuuden ymmärtäminen](ch04-00-understanding-ownership.md)
  - [Mikä on omistajuus?](ch04-01-what-is-ownership.md)
  - [Viitteet ja lainaus](ch04-02-references-and-borrowing.md)
  - [Viipale-tyyppi](ch04-03-slices.md)

- [Rakenteiden käyttö tietojen järjestämiseen](ch05-00-structs.md)
  - [Rakenteiden määrittäminen ja instanssien luominen](ch05-01-defining-structs.md)
  - [Esimerkkiohjelma rakenteiden käytöstä](ch05-02-example-structs.md)
  - [Metodisyntaksi](ch05-03-method-syntax.md)

- [Enumit ja mallienmukaisuus](ch06-00-enums.md)
  - [Enumin määrittäminen](ch06-01-defining-an-enum.md)
  - [`match`-ohjausrakenteen konstruktio](ch06-02-match.md)
  - [Ytimekäs ohjausrakenne `if let`- ja `let else`-lauseilla](ch06-03-if-let.md)

## Perus-Rust-osaaminen

- [Kasvavien projektien hallinta paketeilla, cratella ja moduuleilla](ch07-00-managing-growing-projects-with-packages-crates-and-modules.md)
  - [Paketit ja cratet](ch07-01-packages-and-crates.md)
  - [Moduulien määrittäminen laajuuden ja yksityisyyden hallitsemiseksi](ch07-02-defining-modules-to-control-scope-and-privacy.md)
  - [Polut moduulipuun kohteen viittaamiseen](ch07-03-paths-for-referring-to-an-item-in-the-module-tree.md)
  - [Polkujen tuominen näkyvyysalueeseen `use`-avainsanalla](ch07-04-bringing-paths-into-scope-with-the-use-keyword.md)
  - [Moduulien erottaminen eri tiedostoihin](ch07-05-separating-modules-into-different-files.md)

- [Yleiset kokoelmat](ch08-00-common-collections.md)
  - [Arvojen listojen tallentaminen vektoreilla](ch08-01-vectors.md)
  - [UTF-8-koodattujen tekstien tallentaminen merkkijonoilla](ch08-02-strings.md)
  - [Avainten tallentaminen liittyvine arvoineen hajautustaulukoissa](ch08-03-hash-maps.md)

- [Virheenkäsittely](ch09-00-error-handling.md)
  - [Palautumattomat virheet `panic!`-komennolla](ch09-01-unrecoverable-errors-with-panic.md)
  - [Palautuvat virheet `Result`-tyypillä](ch09-02-recoverable-errors-with-result.md)
  - [`panic!` vai ei `panic!`?](ch09-03-to-panic-or-not-to-panic.md)

- [Geneeriset tyypit, traitit ja eliniät](ch10-00-generics.md)
  - [Geneeriset tietotyypit](ch10-01-syntax.md)
  - [Traitit: jaetun käyttäytymisen määrittäminen](ch10-02-traits.md)
  - [Viitteiden vahvistaminen eliniillä](ch10-03-lifetime-syntax.md)

- [Automaattisten testien kirjoittaminen](ch11-00-testing.md)
  - [Miten testejä kirjoitetaan](ch11-01-writing-tests.md)
  - [Testien suorituksen hallinta](ch11-02-running-tests.md)
  - [Testien organisointi](ch11-03-test-organization.md)

- [I/O-projekti: Komentoriviohjelman rakentaminen](ch12-00-an-io-project.md)
  - [Komentoriviargumenttien hyväksyminen](ch12-01-accepting-command-line-arguments.md)
  - [Tiedoston lukeminen](ch12-02-reading-a-file.md)
  - [Refaktorointi: parempi modulariteetti ja virheenkäsittely](ch12-03-improving-error-handling-and-modularity.md)
  - [Kirjaston toiminnallisuuden kehittäminen testivetoista kehitystä käyttäen](ch12-04-testing-the-librarys-functionality.md)
  - [Ympäristömuuttujien käyttö](ch12-05-working-with-environment-variables.md)
  - [Virheilmoitusten kirjoittaminen standardivirheeseen standarditulosteen sijaan](ch12-06-writing-to-stderr-instead-of-stdout.md)

## Rust-ajattelu

- [Funktionaaliset ominaisuudet: Iteraattorit ja sulkeiset](ch13-00-functional-features.md)
  - [Sulkeiset: anonyymit funktiot, jotka sieppaavat ympäristönsä](ch13-01-closures.md)
  - [Kohteiden sarjojen käsittely iteraattoreilla](ch13-02-iterators.md)
  - [I/O-projektimme parantaminen](ch13-03-improving-our-io-project.md)
  - [Suorituskyvyn vertailu: silmukat vs. iteraattorit](ch13-04-performance.md)

- [Lisää Cargo:sta ja Crates.io:sta](ch14-00-more-about-cargo.md)
  - [Rakenteiden mukauttaminen julkaisuprofiileilla](ch14-01-release-profiles.md)
  - [Craten julkaiseminen Crates.io:hon](ch14-02-publishing-to-crates-io.md)
  - [Cargo-työtilat](ch14-03-cargo-workspaces.md)
  - [Binäärien asentaminen Crates.io:sta `cargo install`-komennolla](ch14-04-installing-binaries.md)
  - [Cargon laajentaminen mukautetuilla komennoilla](ch14-05-extending-cargo.md)

- [Älykkäät osoittimet](ch15-00-smart-pointers.md)
  - [`Box<T>`:n käyttö osoittamaan pinomuistin tietoihin](ch15-01-box.md)
  - [Älykkäiden osoittimien käsitteleminen tavallisina viitteinä `Deref`-traitin avulla](ch15-02-deref.md)
  - [Koodin suorittaminen siivouksessa `Drop`-traitin avulla](ch15-03-drop.md)
  - [`Rc<T>`, viitelaskennallinen älykäs osoitin](ch15-04-rc.md)
  - [`RefCell<T>` ja sisäisen muuttuvuuden malli](ch15-05-interior-mutability.md)
  - [Viitesyklit voivat vuotaa muistia](ch15-06-reference-cycles.md)

- [Turvallinen rinnakkaisuus](ch16-00-concurrency.md)
  - [Säikeiden käyttö koodin samanaikaiseen suorittamiseen](ch16-01-threads.md)
  - [Viestien välityksen käyttö tietojen siirtämiseen säikeiden välillä](ch16-02-message-passing.md)
  - [Jaetun tilan rinnakkaisuus](ch16-03-shared-state.md)
  - [Laajennettava rinnakkaisuus `Sync`- ja `Send`-traitien avulla](ch16-04-extensible-concurrency-sync-and-send.md)

- [Asynkronisen ohjelmoinnin perusteet: Async, Await, Futures ja Streams](ch17-00-async-await.md)
  - [Futures ja async-syntaksi](ch17-01-futures-and-syntax.md)
  - [Rinnakkaisuuden soveltaminen async:lla](ch17-02-concurrency-with-async.md)
  - [Työskentely minkä tahansa määrän futuresien kanssa](ch17-03-more-futures.md)
  - [Streams: Futures peräkkäin](ch17-04-streams.md)
  - [Lähempi tarkastelu async-traitteihin](ch17-05-traits-for-async.md)
  - [Futures, tehtävät ja säikeet](ch17-06-futures-tasks-threads.md)

- [Rustin oliopohjaiset ohjelmointiominaisuudet](ch18-00-oop.md)
  - [Oliopohjaisten kielten ominaisuudet](ch18-01-what-is-oo.md)
  - [Trait-objektien käyttö, jotka sallivat eri tyyppisten arvojen käytön](ch18-02-trait-objects.md)
  - [Oliopohjaisen suunnittelumallin toteuttaminen](ch18-03-oo-design-patterns.md)

## Kehittyneet aiheet

- [Mallit ja mallinmukaisuus](ch19-00-patterns.md)
  - [Kaikki paikat, joissa malleja voidaan käyttää](ch19-01-all-the-places-for-patterns.md)
  - [Kumoavuus: voiko malli epäonnistua vastaamaan](ch19-02-refutability.md)
  - [Mallin syntaksi](ch19-03-pattern-syntax.md)

- [Kehittyneet ominaisuudet](ch20-00-advanced-features.md)
  - [Turvaton Rust](ch20-01-unsafe-rust.md)
  - [Kehittyneet traitit](ch20-02-advanced-traits.md)
  - [Kehittyneet tyypit](ch20-03-advanced-types.md)
  - [Kehittyneet funktiot ja sulkeiset](ch20-04-advanced-functions-and-closures.md)
  - [Makrot](ch20-05-macros.md)

- [Loppuprojekti: Monisäikeisen verkkopalvelimen rakentaminen](ch21-00-final-project-a-web-server.md)
  - [Yksisäikeisen verkkopalvelimen rakentaminen](ch21-01-single-threaded.md)
  - [Yksisäikeisen palvelimen muuttaminen monisäikeiseksi palvelimeksi](ch21-02-multithreaded.md)
  - [Siisti sammutus ja siivous](ch21-03-graceful-shutdown-and-cleanup.md)

- [Liite](appendix-00.md)
  - [A - Keywords](appendix-01-keywords.md)
  - [B - Operators and Symbols](appendix-02-operators.md)
  - [C - Derivable Traits](appendix-03-derivable-traits.md)
  - [D - Useful Development Tools](appendix-04-useful-development-tools.md)
  - [E - Editions](appendix-05-editions.md)
  - [F - Translations of the Book](appendix-06-translation.md)
  - [G - How Rust is Made and “Nightly Rust”](appendix-07-nightly-rust.md)
