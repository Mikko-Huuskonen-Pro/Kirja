## Liite A: Avainsanat

Seuraavissa luetteloissa on avainsanoja, jotka Rust-kieli on varannut nykyiseen tai
tulevaan käyttöön. Sellaisenaan niitä ei voi käyttää tunnisteina (paitsi raakatunnisteina,
kuten käsitellään kohdassa [”Raakatunnisteet”][raw-identifiers]<!-- ignore -->).
_Tunnisteet_ ovat funktioiden, muuttujien, parametrien, rakenteiden kenttien, moduulien,
pakettien, vakioiden, makrojen, staattisten arvojen, attribuuttien, tyyppien, traitien
tai elinikien nimiä.

[raw-identifiers]: #raw-identifiers

### Tällä hetkellä käytössä olevat avainsanat

Seuraavassa on luettelo tällä hetkellä käytössä olevista avainsanoista ja niiden
toiminnallisuudesta.

- **`as`**: Suorittaa primitiivisen tyypinmuunnoksen, poistaa moniselitteisyyden sen
  traitin osalta, joka sisältää kohteen, tai uudelleennimeää kohteita `use`-lauseissa.
- **`async`**: Palauttaa `Future`-olion estämättä nykyistä säiettä.
- **`await`**: Keskeyttää suorituksen, kunnes `Future`-olion tulos on valmis.
- **`break`**: Poistuu silmukasta välittömästi.
- **`const`**: Määrittää vakioita tai vakioraakaosoittimia.
- **`continue`**: Jatkaa seuraavaan silmukkaiteraatioon.
- **`crate`**: Moduulipolussa viittaa paketin juureen.
- **`dyn`**: Dynaaminen lähetys trait-oliolle.
- **`else`**: Varavaihtoehto `if`- ja `if let` -ohjausrakenteille.
- **`enum`**: Määrittää luettelon.
- **`extern`**: Linkittää ulkoisen funktion tai muuttujan.
- **`false`**: Totuusarvon epätosi-literaali.
- **`fn`**: Määrittää funktion tai funktio-osoitintyypin.
- **`for`**: Käy läpi iteraattorin kohteita, toteuttaa traitin tai määrittää korkeamman
  asteen eliniän.
- **`if`**: Haarautuu ehdollisen lausekkeen tuloksen perusteella.
- **`impl`**: Toteuttaa sisäänrakennettua tai trait-toiminnallisuutta.
- **`in`**: Osa `for`-silmukan syntaksia.
- **`let`**: Sitoo muuttujan.
- **`loop`**: Toistaa silmukkaa ehdottomasti.
- **`match`**: Vertaa arvoa kuvioihin.
- **`mod`**: Määrittää moduulin.
- **`move`**: Saattaa sulkeuman ottamaan omistukseen kaikista kaappauksistaan.
- **`mut`**: Ilmaisee muuttuvuutta viittauksissa, raakaosoittimissa tai kuviosidonnissa.
- **`pub`**: Ilmaisee julkisen näkyvyyden rakenteiden kentissä, `impl`-lohkoissa tai
  moduuleissa.
- **`ref`**: Sitoo viittauksena.
- **`return`**: Palaa funktiosta.
- **`Self`**: Tyyppialias tyypille, jota määritellään tai toteutetaan.
- **`self`**: Metodin kohde tai nykyinen moduuli.
- **`static`**: Globaali muuttuja tai koko ohjelman suorituksen kestävä elinikä.
- **`struct`**: Määrittää rakenteen.
- **`super`**: Nykyisen moduulin ylämoduuli.
- **`trait`**: Määrittää traitin.
- **`true`**: Totuusarvon tosi-literaali.
- **`type`**: Määrittää tyyppialiasin tai assosioituneen tyypin.
- **`union`**: Määrittää [unionin][union]<!-- ignore -->; on avainsana vain
  unioni-määrittelyssä.
- **`unsafe`**: Merkitsee turvatonta koodia, funktiota, traitia tai toteutusta.
- **`use`**: Tuo symboleja näkyvyysalueelle.
- **`where`**: Ilmaisee tyyppiä rajoittavia lausekkeita.
- **`while`**: Toistaa silmukkaa ehdollisesti lausekkeen tuloksen perusteella.

[union]: ../reference/items/unions.html

### Tulevaisuutta varten varatut avainsanat

Seuraavilla avainsanoilla ei ole vielä toiminnallisuutta, mutta Rust on varannut ne
mahdollista tulevaa käyttöä varten:

- `abstract`
- `become`
- `box`
- `do`
- `final`
- `gen`
- `macro`
- `override`
- `priv`
- `try`
- `typeof`
- `unsized`
- `virtual`
- `yield`

### Raakatunnisteet

_Raakatunnisteet_ ovat syntaksia, jonka avulla avainsanoja voi käyttää paikoissa, joissa
niitä ei normaalisti sallittaisi. Raakatunniste muodostetaan lisäämällä avainsanan eteen
`r#`.

Esimerkiksi `match` on avainsana. Jos yrität kääntää seuraavan funktion, joka käyttää
`match`-sanaa nimenään:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,does_not_compile
fn match(needle: &str, haystack: &str) -> bool {
    haystack.contains(needle)
}
```

saat tämän virheen:

```text
error: expected identifier, found keyword `match`
 --> src/main.rs:4:4
  |
4 | fn match(needle: &str, haystack: &str) -> bool {
  |    ^^^^^ expected identifier, found keyword
```

Virhe kertoo, että avainsanaa `match` ei voi käyttää funktion tunnisteena. Käyttääksesi
`match`-sanaa funktion nimenä, sinun täytyy käyttää raakatunnistesyntaksia näin:

<span class="filename">Filename: src/main.rs</span>

```rust
fn r#match(needle: &str, haystack: &str) -> bool {
    haystack.contains(needle)
}

fn main() {
    assert!(r#match("foo", "foobar"));
}
```

Tämä koodi kääntyy ilman virheitä. Huomaa `r#`-etuliite funktion nimessä sekä sen
määrittelyssä että siinä kohdassa, jossa funktiota kutsutaan `main`-funktiossa.

Raakatunnisteet mahdollistavat minkä tahansa sanan käytön tunnisteena, vaikka sana olisi
varattu avainsana. Tämä antaa enemmän vapautta valita tunnistenimiä ja helpottaa
integraatiota ohjelmiin, jotka on kirjoitettu kielellä, jossa nämä sanat eivät ole
avainsanoja. Lisäksi raakatunnisteet mahdollistavat kirjastojen käytön, jotka on kirjoitettu
eri Rust-editionilla kuin mitä pakettisi käyttää. Esimerkiksi `try` ei ole avainsana
editionissa 2015, mutta on editioneissa 2018, 2021 ja 2024. Jos riippuvuutesi on kirjoitettu
editionilla 2015 ja siinä on `try`-funktio, sinun täytyy käyttää raakatunnistesyntaksia,
tässä tapauksessa `r#try`, kutsuessasi kyseistä funktiota koodistasi myöhemmissä
editioneissa. Katso lisätietoja editioneista [liitteestä E][appendix-e]<!-- ignore -->.

[appendix-e]: appendix-05-editions.html
