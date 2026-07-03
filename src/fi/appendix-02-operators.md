## Liite B: Operaattorit ja symbolit

Tämä liite sisältää Rustin syntaksin sanaston, mukaan lukien operaattorit ja muut symbolit,
jotka esiintyvät yksinään tai polkujen, geneeristen tyyppien, trait-rajojen, makrojen,
attribuuttien, kommenttien, tuplejen ja hakasulkeiden yhteydessä.

### Operaattorit

Taulukko B-1 sisältää Rustin operaattorit, esimerkin siitä, miltä operaattori näyttäisi
kontekstissa, lyhyen selityksen ja tiedon siitä, onko operaattori ylikuormitettavissa. Jos
operaattori on ylikuormitettavissa, luettelossa on myös siihen liittyvä trait, jota käytetään
operaattorin ylikuormittamiseen.

<span class="caption">Taulukko B-1: Operaattorit</span>

| Operator                  | Example                                                 | Explanation                                                           | Overloadable?  |
| ------------------------- | ------------------------------------------------------- | --------------------------------------------------------------------- | -------------- |
| `!`                       | `ident!(...)`, `ident!{...}`, `ident![...]`             | Makron laajennus                                                      |                |
| `!`                       | `!expr`                                                 | Bittinen tai looginen komplementti                                    | `Not`          |
| `!=`                      | `expr != expr`                                          | Eriarvoisuusvertailu                                                  | `PartialEq`    |
| `%`                       | `expr % expr`                                           | Jakojäännös                                                           | `Rem`          |
| `%=`                      | `var %= expr`                                           | Jakojäännös ja sijoitus                                               | `RemAssign`    |
| `&`                       | `&expr`, `&mut expr`                                    | Lainaaminen                                                           |                |
| `&`                       | `&type`, `&mut type`, `&'a type`, `&'a mut type`        | Lainatun osoittimen tyyppi                                            |                |
| `&`                       | `expr & expr`                                           | Bittinen JA                                                           | `BitAnd`       |
| `&=`                      | `var &= expr`                                           | Bittinen JA ja sijoitus                                               | `BitAndAssign` |
| `&&`                      | `expr && expr`                                          | Oikosulkeva looginen JA                                               |                |
| `*`                       | `expr * expr`                                           | Kertolasku                                                            | `Mul`          |
| `*=`                      | `var *= expr`                                           | Kertolasku ja sijoitus                                                | `MulAssign`    |
| `*`                       | `*expr`                                                 | Dereferenssi                                                          | `Deref`        |
| `*`                       | `*const type`, `*mut type`                              | Raaka osoitin                                                         |                |
| `+`                       | `trait + trait`, `'a + trait`                           | Yhdistetty tyyppirajoite                                              |                |
| `+`                       | `expr + expr`                                           | Yhteenlasku                                                           | `Add`          |
| `+=`                      | `var += expr`                                           | Yhteenlasku ja sijoitus                                               | `AddAssign`    |
| `,`                       | `expr, expr`                                            | Argumenttien ja elementtien erotin                                     |                |
| `-`                       | `- expr`                                                | Aritmeettinen negaatio                                                | `Neg`          |
| `-`                       | `expr - expr`                                           | Vähennyslasku                                                         | `Sub`          |
| `-=`                      | `var -= expr`                                           | Vähennyslasku ja sijoitus                                             | `SubAssign`    |
| `->`                      | `fn(...) -> type`, <code>&vert;...&vert; -> type</code> | Funktion ja sulkeuman paluuarvon tyyppi                               |                |
| `.`                       | `expr.ident`                                            | Kentän käyttö                                                         |                |
| `.`                       | `expr.ident(expr, ...)`                                 | Metodikutsu                                                           |                |
| `.`                       | `expr.0`, `expr.1`, and so on                           | Tuplen indeksointi                                                    |                |
| `..`                      | `..`, `expr..`, `..expr`, `expr..expr`                  | Oikealta avoin väli-literaali                                         | `PartialOrd`   |
| `..=`                     | `..=expr`, `expr..=expr`                                | Oikealta suljettu väli-literaali                                      | `PartialOrd`   |
| `..`                      | `..expr`                                                | Rakenneliteraalin päivityssyntaksi                                    |                |
| `..`                      | `variant(x, ..)`, `struct_type { x, .. }`               | ”Ja loput” -kuviosidonta                                              |                |
| `...`                     | `expr...expr`                                           | (Vanhentunut, käytä `..=` sijaan) Kuviossa: suljettu välikuvio        |                |
| `/`                       | `expr / expr`                                           | Jakolasku                                                             | `Div`          |
| `/=`                      | `var /= expr`                                           | Jakolasku ja sijoitus                                                 | `DivAssign`    |
| `:`                       | `pat: type`, `ident: type`                              | Rajoitteet                                                            |                |
| `:`                       | `ident: expr`                                           | Rakennekentän alustus                                                 |                |
| `:`                       | `'a: loop {...}`                                        | Silmukan label                                                        |                |
| `;`                       | `expr;`                                                 | Lauseen ja kohteen pääte                                              |                |
| `;`                       | `[...; len]`                                            | Osa kiinteäkokoista taulukkosyntaksia                                 |                |
| `<<`                      | `expr << expr`                                          | Siirto vasemmalle                                                     | `Shl`          |
| `<<=`                     | `var <<= expr`                                          | Siirto vasemmalle ja sijoitus                                         | `ShlAssign`    |
| `<`                       | `expr < expr`                                           | Pienempi kuin -vertailu                                               | `PartialOrd`   |
| `<=`                      | `expr <= expr`                                          | Pienempi tai yhtä suuri kuin -vertailu                                | `PartialOrd`   |
| `=`                       | `var = expr`, `ident = type`                            | Sijoitus/ekvivalenssi                                                 |                |
| `==`                      | `expr == expr`                                          | Yhtäsuuruusvertailu                                                   | `PartialEq`    |
| `=>`                      | `pat => expr`                                           | Osa `match`-haaran syntaksia                                          |                |
| `>`                       | `expr > expr`                                           | Suurempi kuin -vertailu                                               | `PartialOrd`   |
| `>=`                      | `expr >= expr`                                          | Suurempi tai yhtä suuri kuin -vertailu                                | `PartialOrd`   |
| `>>`                      | `expr >> expr`                                          | Siirto oikealle                                                       | `Shr`          |
| `>>=`                     | `var >>= expr`                                          | Siirto oikealle ja sijoitus                                           | `ShrAssign`    |
| `@`                       | `ident @ pat`                                           | Kuviosidonta                                                          |                |
| `^`                       | `expr ^ expr`                                           | Bittinen eksklusiivinen TAI                                            | `BitXor`       |
| `^=`                      | `var ^= expr`                                           | Bittinen eksklusiivinen TAI ja sijoitus                                | `BitXorAssign` |
| <code>&vert;</code>       | <code>pat &vert; pat</code>                             | Kuviovaihtoehdot                                                      |                |
| <code>&vert;</code>       | <code>expr &vert; expr</code>                           | Bittinen TAI                                                          | `BitOr`        |
| <code>&vert;=</code>      | <code>var &vert;= expr</code>                           | Bittinen TAI ja sijoitus                                              | `BitOrAssign`  |
| <code>&vert;&vert;</code> | <code>expr &vert;&vert; expr</code>                     | Oikosulkeva looginen TAI                                              |                |
| `?`                       | `expr?`                                                 | Virheen propagointi                                                   |                |

### Muut kuin operaattorisymbolit

Seuraavissa taulukoissa on kaikki symbolit, jotka eivät toimi operaattoreina; toisin sanoen
ne eivät käyttäydy kuten funktio- tai metodikutsu.

Taulukko B-2 näyttää symbolit, jotka esiintyvät yksinään ja ovat kelvollisia monissa
eri paikoissa.

<span class="caption">Taulukko B-2: Itsenäinen syntaksi</span>

| Symbol                                                                 | Explanation                                                            |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `'ident`                                                               | Nimetty elinikä tai silmukan label                                     |
| Digits immediately followed by `u8`, `i32`, `f64`, `usize`, and so on  | Tietyn tyypin numeerinen literaali                                     |
| `"..."`                                                                | Merkkijonoliteraali                                                    |
| `r"..."`, `r#"..."#`, `r##"..."##`, and so on                          | Raaka merkkijonoliteraali; escape-merkkejä ei käsitellä                |
| `b"..."`                                                               | Tavumerkkijonoliteraali; muodostaa tavutaulukon merkkijonon sijaan     |
| `br"..."`, `br#"..."#`, `br##"..."##`, and so on                       | Raaka tavumerkkijonoliteraali; raa'an ja tavumerkkijonoliteraalin yhdistelmä |
| `'...'`                                                                | Merkkiliteraali                                                        |
| `b'...'`                                                               | ASCII-tavuliteraali                                                    |
| <code>&vert;...&vert; expr</code>                                      | Sulkeuma                                                               |
| `!`                                                                    | Aina tyhjä pohjatyyppi divergoiville funktioille                       |
| `_`                                                                    | ”Ohitettu” kuviosidonta; käytetään myös kokonaislukuliteraalien luettavuuteen |

Taulukko B-3 näyttää symbolit, jotka esiintyvät polun yhteydessä moduulihierarkian
kautta kohteeseen.

<span class="caption">Taulukko B-3: Polkuun liittyvä syntaksi</span>

| Symbol                                  | Explanation                                                                                                  |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------|
| `ident::ident`                          | Nimiavaruuspolku                                                                                             |
| `::path`                                | Polku suhteessa paketin juureen (eli eksplisiittisesti absoluuttinen polku)                                  |
| `self::path`                            | Polku suhteessa nykyiseen moduuliin (eli eksplisiittisesti suhteellinen polku)                               |
| `super::path`                           | Polku suhteessa nykyisen moduulin ylämoduuliin                                                               |
| `type::ident`, `<type as trait>::ident` | Assosioituneet vakiot, funktiot ja tyypit                                                                    |
| `<type>::...`                           | Assosioitu kohde tyypille, jota ei voi nimetä suoraan (esimerkiksi `<&T>::...`, `<[T]>::...`, and so on)   |
| `trait::method(...)`                    | Metodikutsun poistaminen moniselitteisyydestä nimeämällä sen määrittävä trait                                |
| `type::method(...)`                     | Metodikutsun poistaminen moniselitteisyydestä nimeämällä tyyppi, jolle se on määritelty                     |
| `<type as trait>::method(...)`          | Metodikutsun poistaminen moniselitteisyydestä nimeämällä trait ja tyyppi                                     |

Taulukko B-4 näyttää symbolit, jotka esiintyvät geneeristen tyyppiparametrien käytön
yhteydessä.

<span class="caption">Taulukko B-4: Geneeriset tyypit</span>

| Symbol                         | Explanation                                                                                                                                         |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `path<...>`                    | Määrittää parametrit geneeriselle tyypille tyypissä (esimerkiksi `Vec<u8>`)                                                                         |
| `path::<...>`, `method::<...>` | Määrittää parametrit geneeriselle tyypille, funktiolle tai metodille lausekkeessa; usein kutsutaan _turbofishiksi_ (esimerkiksi `"42".parse::<i32>()`) |
| `fn ident<...> ...`            | Määrittele geneerinen funktio                                                                                                                       |
| `struct ident<...> ...`        | Määrittele geneerinen rakenne                                                                                                                       |
| `enum ident<...> ...`          | Määrittele geneerinen luettelo                                                                                                                      |
| `impl<...> ...`                | Määrittele geneerinen toteutus                                                                                                                      |
| `for<...> type`                | Korkeamman asteen elinkaarirajat                                                                                                                    |
| `type<ident=type>`             | Geneerinen tyyppi, jossa yhdellä tai useammalla assosioituneella tyypillä on tietyt sijoitukset (esimerkiksi `Iterator<Item=T>`)                    |

Taulukko B-5 näyttää symbolit, jotka esiintyvät geneeristen tyyppiparametrien rajoittamisen
yhteydessä trait-rajoilla.

<span class="caption">Taulukko B-5: Trait-rajoitteet</span>

| Symbol                        | Explanation                                                                                                                                |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `T: U`                        | Geneerinen parametri `T` rajoitettu tyyppeihin, jotka toteuttavat `U`-traitin                                                              |
| `T: 'a`                       | Geneerisen tyypin `T` täytyy elää eliniän `'a` yli (eli tyyppi ei voi transitiivisesti sisältää viitteitä, joiden elinikä on lyhyempi kuin `'a`) |
| `T: 'static`                  | Geneerinen tyyppi `T` ei sisällä lainattuja viitteitä muita kuin `'static`-viitteitä                                                       |
| `'b: 'a`                      | Geneerisen eliniän `'b` täytyy elää eliniän `'a` yli                                                                                       |
| `T: ?Sized`                   | Salli geneerisen tyyppiparametrin olla dynaamisesti mitoitettu tyyppi                                                                      |
| `'a + trait`, `trait + trait` | Yhdistetty tyyppirajoite                                                                                                                   |

Taulukko B-6 näyttää symbolit, jotka esiintyvät makrojen kutsumisen tai määrittelyn sekä
kohteelle määritettyjen attribuuttien yhteydessä.

<span class="caption">Taulukko B-6: Makrot ja attribuutit</span>

| Symbol                                      | Explanation        |
| ------------------------------------------- | ------------------ |
| `#[meta]`                                   | Ulompi attribuutti |
| `#![meta]`                                  | Sisempi attribuutti |
| `$ident`                                    | Makron substituutio |
| `$ident:kind`                               | Makron metamuuttuja |
| `$(...)...`                                 | Makron toisto    |
| `ident!(...)`, `ident!{...}`, `ident![...]` | Makrokutsu       |

Taulukko B-7 näyttää symbolit, joilla luodaan kommentteja.

<span class="caption">Taulukko B-7: Kommentit</span>

| Symbol     | Explanation             |
| ---------- | ----------------------- |
| `//`       | Rivikommentti           |
| `//!`      | Sisempi rividokumentaatiokommentti |
| `///`      | Ulompi rividokumentaatiokommentti |
| `/*...*/`  | Lohkokommentti          |
| `/*!...*/` | Sisempi lohkodokumentaatiokommentti |
| `/**...*/` | Ulompi lohkodokumentaatiokommentti |

Taulukko B-8 näyttää kontekstit, joissa kaarisulkeita käytetään.

<span class="caption">Taulukko B-8: Kaarisulkeet</span>

| Symbol                   | Explanation                                                                                 |
| ------------------------ | ------------------------------------------------------------------------------------------- |
| `()`                     | Tyhjä tuple (eli unit), sekä literaali että tyyppi                                          |
| `(expr)`                 | Sulkeistettu lauseke                                                                        |
| `(expr,)`                | Yksielementtinen tuple-lauseke                                                              |
| `(type,)`                | Yksielementtinen tuple-tyyppi                                                               |
| `(expr, ...)`            | Tuple-lauseke                                                                               |
| `(type, ...)`            | Tuple-tyyppi                                                                                |
| `expr(expr, ...)`        | Funktiokutsulauseke; käytetään myös tuple-`struct`- ja tuple-`enum`-varianttien alustamiseen |

Taulukko B-9 näyttää kontekstit, joissa aaltosulkeita käytetään.

<span class="caption">Taulukko B-9: Aaltosulkeet</span>

| Context      | Explanation      |
| ------------ | ---------------- |
| `{...}`      | Lohkolauseke     |
| `Type {...}` | Rakenneliteraali |

Taulukko B-10 näyttää kontekstit, joissa hakasulkeita käytetään.

<span class="caption">Taulukko B-10: Hakasulkeet</span>

| Context                                            | Explanation                                                                                                                   |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `[...]`                                            | Taulukkoliteraali                                                                                                             |
| `[expr; len]`                                      | Taulukkoliteraali, joka sisältää `len` kappaletta `expr`-lauseketta                                                            |
| `[type; len]`                                      | Taulukkotyyppi, joka sisältää `len` kappaletta `type`-tyyppiä                                                                 |
| `expr[expr]`                                       | Kokoelman indeksointi; ylikuormitettavissa (`Index`, `IndexMut`)                                                              |
| `expr[..]`, `expr[a..]`, `expr[..b]`, `expr[a..b]` | Kokoelman indeksointi, joka esittää kokoelman viipalointia käyttäen `Range`-, `RangeFrom`-, `RangeTo`- tai `RangeFull`-tyyppiä ”indeksinä” |
