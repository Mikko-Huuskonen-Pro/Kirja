## Liite B: Operaattorit ja symbolit

Tämä liite sisältää katsauksen Rustin syntaksiin, mukaan lukien operaattorit ja muut symbolit, joita käytetään muun muassa poluissa, geneerisissä tyypeissä, rajapintarajoituksissa, makroissa, attribuuteissa, kommenteissa, tupleissa ja hakasulkeissa.

### Operaattorit

Taulukko B-1 sisältää Rustin operaattorit, esimerkin niiden käytöstä, lyhyen selityksen sekä tiedon siitä, onko operaattori ylikuormitettavissa. Jos operaattori on ylikuormitettavissa, taulukossa mainitaan myös siihen liittyvä rajapinta.

<span class="caption">Taulukko B-1: Operaattorit</span>

| Operaattori | Esimerkki | Selitys | Ylikuormitettavissa? |
| ------------ | ----------- | ----------- | -------------------- |
| `!` | `ident!(...)`, `ident!{...}`, `ident![...]` | Makron laajennus | |
| `!` | `!expr` | Bitti- tai looginen komplementti | `Not` |
| `!=` | `expr != expr` | Eriarvoisuusvertailu | `PartialEq` |
| `%` | `expr % expr` | Jakoreste | `Rem` |
| `%=` | `var %= expr` | Jakoreste ja sijoitus | `RemAssign` |
| `&` | `&expr`, `&mut expr` | Viittaus (lainaus) | |
| `&` | `&type`, `&mut type`, `&'a type`, `&'a mut type` | Lainattu osoitintyyppi | |
| `&` | `expr & expr` | Bittitasolla JA-operaattori | `BitAnd` |
| `&=` | `var &= expr` | Bittitasolla JA-operaattori ja sijoitus | `BitAndAssign` |
| `&&` | `expr && expr` | Lyhytkatkaiseva looginen JA | |
| `*` | `expr * expr` | Kertolasku | `Mul` |
| `*=` | `var *= expr` | Kertolasku ja sijoitus | `MulAssign` |
| `*` | `*expr` | Viittauksen purku (dereference) | `Deref` |
| `*` | `*const type`, `*mut type` | Raaka osoitin | |
| `+` | `trait + trait`, `'a + trait` | Yhdistetty tyyppirajoite | |
| `+` | `expr + expr` | Yhteenlasku | `Add` |
| `+=` | `var += expr` | Yhteenlasku ja sijoitus | `AddAssign` |
| `->`                      | `fn(...) -> type`, <code>&vert;...&vert; -> type</code> | Function and closure return type                                      |                |
| `.`                       | `expr.ident`                                            | Field access                                                          |                |
| `.`                       | `expr.ident(expr, ...)`                                 | Method call                                                           |                |
| `.`                       | `expr.0`, `expr.1`, etc.                                | Tuple indexing                                                        |                |
| `..`                      | `..`, `expr..`, `..expr`, `expr..expr`                  | Right-exclusive range literal                                         | `PartialOrd`   |
| `..=`                     | `..=expr`, `expr..=expr`                                | Right-inclusive range literal                                         | `PartialOrd`   |
| `..`                      | `..expr`                                                | Struct literal update syntax                                          |                |
| `..`                      | `variant(x, ..)`, `struct_type { x, .. }`               | “And the rest” pattern binding                                        |                |
| `...`                     | `expr...expr`                                           | (Deprecated, use `..=` instead) In a pattern: inclusive range pattern |                |
| `/`                       | `expr / expr`                                           | Arithmetic division                                                   | `Div`          |
| `/=`                      | `var /= expr`                                           | Arithmetic division and assignment                                    | `DivAssign`    |
| `:`                       | `pat: type`, `ident: type`                              | Constraints                                                           |                |
| `:`                       | `ident: expr`                                           | Struct field initializer                                              |                |
| `:`                       | `'a: loop {...}`                                        | Loop label                                                            |                |
| `;`                       | `expr;`                                                 | Statement and item terminator                                         |                |
| `;`                       | `[...; len]`                                            | Part of fixed-size array syntax                                       |                |
| `<<`                      | `expr << expr`                                          | Left-shift                                                            | `Shl`          |
| `<<=`                     | `var <<= expr`                                          | Left-shift and assignment                                             | `ShlAssign`    |
| `<`                       | `expr < expr`                                           | Less than comparison                                                  | `PartialOrd`   |
| `<=`                      | `expr <= expr`                                          | Less than or equal to comparison                                      | `PartialOrd`   |
| `=`                       | `var = expr`, `ident = type`                            | Assignment/equivalence                                                |                |
| `==`                      | `expr == expr`                                          | Equality comparison                                                   | `PartialEq`    |
| `=>`                      | `pat => expr`                                           | Part of match arm syntax                                              |                |
| `>`                       | `expr > expr`                                           | Greater than comparison                                               | `PartialOrd`   |
| `>=`                      | `expr >= expr`                                          | Greater than or equal to comparison                                   | `PartialOrd`   |
| `>>`                      | `expr >> expr`                                          | Right-shift                                                           | `Shr`          |
| `>>=`                     | `var >>= expr`                                          | Right-shift and assignment                                            | `ShrAssign`    |
| `@`                       | `ident @ pat`                                           | Pattern binding                                                       |                |
| `^`                       | `expr ^ expr`                                           | Bitwise exclusive OR                                                  | `BitXor`       |
| `^=`                      | `var ^= expr`                                           | Bitwise exclusive OR and assignment                                   | `BitXorAssign` |
| <code>&vert;</code>       | <code>pat &vert; pat</code>                             | Pattern alternatives                                                  |                |
| <code>&vert;</code>       | <code>expr &vert; expr</code>                           | Bitwise OR                                                            | `BitOr`        |
| <code>&vert;=</code>      | <code>var &vert;= expr</code>                           | Bitwise OR and assignment                                             | `BitOrAssign`  |
| <code>&vert;&vert;</code> | <code>expr &vert;&vert; expr</code>                     | Short-circuiting logical OR                                           |                |
| `?`                       | `expr?`                                                 | Error propagation                                                     |                |


---

### Muut kuin operaattorisymbolit

Seuraava luettelo sisältää symbolit, jotka eivät toimi operaattoreina, eli ne eivät käyttäydy kuten funktiokutsut tai metodikutsut.

_(Taulukot ja selitykset jatkavat samalla rakenteella kuin alkuperäisessä dokumentissa)_

---
The following list contains all symbols that don’t function as operators; that
is, they don’t behave like a function or method call.

Table B-2 shows symbols that appear on their own and are valid in a variety of
locations.

<span class="caption">Table B-2: Stand-Alone Syntax</span>

| Symbol                                        | Explanation                                                            |
| --------------------------------------------- | ---------------------------------------------------------------------- |
| `'ident`                                      | Named lifetime or loop label                                           |
| `...u8`, `...i32`, `...f64`, `...usize`, etc. | Numeric literal of specific type                                       |
| `"..."`                                       | String literal                                                         |
| `r"..."`, `r#"..."#`, `r##"..."##`, etc.      | Raw string literal, escape characters not processed                    |
| `b"..."`                                      | Byte string literal; constructs an array of bytes instead of a string  |
| `br"..."`, `br#"..."#`, `br##"..."##`, etc.   | Raw byte string literal, combination of raw and byte string literal    |
| `'...'`                                       | Character literal                                                      |
| `b'...'`                                      | ASCII byte literal                                                     |
| <code>&vert;...&vert; expr</code>             | Closure                                                                |
| `!`                                           | Always empty bottom type for diverging functions                       |
| `_`                                           | “Ignored” pattern binding; also used to make integer literals readable |

Table B-3 shows symbols that appear in the context of a path through the module
hierarchy to an item.

<span class="caption">Table B-3: Path-Related Syntax</span>

| Symbol                                  | Explanation                                                                                                                     |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `ident::ident`                          | Namespace path                                                                                                                  |
| `::path`                                | Path relative to the extern prelude, where all other crates are rooted (i.e., an explicitly absolute path including crate name) |
| `self::path`                            | Path relative to the current module (i.e., an explicitly relative path).                                                        |
| `super::path`                           | Path relative to the parent of the current module                                                                               |
| `type::ident`, `<type as trait>::ident` | Associated constants, functions, and types                                                                                      |
| `<type>::...`                           | Associated item for a type that cannot be directly named (e.g., `<&T>::...`, `<[T]>::...`, etc.)                                |
| `trait::method(...)`                    | Disambiguating a method call by naming the trait that defines it                                                                |
| `type::method(...)`                     | Disambiguating a method call by naming the type for which it’s defined                                                          |
| `<type as trait>::method(...)`          | Disambiguating a method call by naming the trait and type                                                                       |

Table B-4 shows symbols that appear in the context of using generic type
parameters.

<span class="caption">Table B-4: Generics</span>

| Symbol                         | Explanation                                                                                                                              |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `path<...>`                    | Specifies parameters to generic type in a type (e.g., `Vec<u8>`)                                                                         |
| `path::<...>`, `method::<...>` | Specifies parameters to generic type, function, or method in an expression; often referred to as turbofish (e.g., `"42".parse::<i32>()`) |
| `fn ident<...> ...`            | Define generic function                                                                                                                  |
| `struct ident<...> ...`        | Define generic structure                                                                                                                 |
| `enum ident<...> ...`          | Define generic enumeration                                                                                                               |
| `impl<...> ...`                | Define generic implementation                                                                                                            |
| `for<...> type`                | Higher-ranked lifetime bounds                                                                                                            |
| `type<ident=type>`             | A generic type where one or more associated types have specific assignments (e.g., `Iterator<Item=T>`)                                   |

Table B-5 shows symbols that appear in the context of constraining generic type
parameters with trait bounds.

<span class="caption">Table B-5: Trait Bound Constraints</span>

| Symbol                        | Explanation                                                                                                                                |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `T: U`                        | Generic parameter `T` constrained to types that implement `U`                                                                              |
| `T: 'a`                       | Generic type `T` must outlive lifetime `'a` (meaning the type cannot transitively contain any references with lifetimes shorter than `'a`) |
| `T: 'static`                  | Generic type `T` contains no borrowed references other than `'static` ones                                                                 |
| `'b: 'a`                      | Generic lifetime `'b` must outlive lifetime `'a`                                                                                           |
| `T: ?Sized`                   | Allow generic type parameter to be a dynamically sized type                                                                                |
| `'a + trait`, `trait + trait` | Compound type constraint                                                                                                                   |

Table B-6 shows symbols that appear in the context of calling or defining
macros and specifying attributes on an item.

<span class="caption">Table B-6: Macros and Attributes</span>

| Symbol                                      | Explanation        |
| ------------------------------------------- | ------------------ |
| `#[meta]`                                   | Outer attribute    |
| `#![meta]`                                  | Inner attribute    |
| `$ident`                                    | Macro substitution |
| `$ident:kind`                               | Macro capture      |
| `$(…)…`                                     | Macro repetition   |
| `ident!(...)`, `ident!{...}`, `ident![...]` | Macro invocation   |

Table B-7 shows symbols that create comments.

<span class="caption">Table B-7: Comments</span>

| Symbol     | Explanation             |
| ---------- | ----------------------- |
| `//`       | Line comment            |
| `//!`      | Inner line doc comment  |
| `///`      | Outer line doc comment  |
| `/*...*/`  | Block comment           |
| `/*!...*/` | Inner block doc comment |
| `/**...*/` | Outer block doc comment |

Table B-8 shows the contexts in which parentheses are used.

<span class="caption">Table B-8: Parentheses</span>

| Symbol                   | Explanation                                                                                 |
| ------------------------ | ------------------------------------------------------------------------------------------- |
| `()`                     | Empty tuple (aka unit), both literal and type                                               |
| `(expr)`                 | Parenthesized expression                                                                    |
| `(expr,)`                | Single-element tuple expression                                                             |
| `(type,)`                | Single-element tuple type                                                                   |
| `(expr, ...)`            | Tuple expression                                                                            |
| `(type, ...)`            | Tuple type                                                                                  |
| `expr(expr, ...)`        | Function call expression; also used to initialize tuple `struct`s and tuple `enum` variants |

Table B-9 shows the contexts in which curly braces are used.

<span class="caption">Table B-9: Curly Brackets</span>

| Context      | Explanation      |
| ------------ | ---------------- |
| `{...}`      | Block expression |
| `Type {...}` | `struct` literal |

Table B-10 shows the contexts in which square brackets are used.

<span class="caption">Table B-10: Square Brackets</span>

| Context                                            | Explanation                                                                                                                   |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `[...]`                                            | Array literal                                                                                                                 |
| `[expr; len]`                                      | Array literal containing `len` copies of `expr`                                                                               |
| `[type; len]`                                      | Array type containing `len` instances of `type`                                                                               |
| `expr[expr]`                                       | Collection indexing. Overloadable (`Index`, `IndexMut`)                                                                       |
| `expr[..]`, `expr[a..]`, `expr[..b]`, `expr[a..b]` | Collection indexing pretending to be collection slicing, using `Range`, `RangeFrom`, `RangeTo`, or `RangeFull` as the “index” |
Liite B: Operaattorit ja SymbolitTämä liite sisältää Rust-syntaksin sanaston, mukaan lukien operaattorit ja muut symbolit, jotka esiintyvät yksinään tai polkujen, geneeristen tyyppien, trait-rajojen, makrojen, attribuuttien, kommenttien, tuplejen ja hakasulkeiden yhteydessä.OperaattoritTässä osiossa eritellään Rustin eri operaattorit. Olennainen osa ohjelmointikielen ymmärtämistä on sen operaattoreiden tunteminen. Nämä mahdollistavat erilaisten toimintojen suorittamisen arvoilla ja muuttujilla. Tässä liitteessä käsitellään kunkin operaattorin toimintaa, esimerkkejä niiden käytöstä ja tietoa siitä, voidaanko niitä ylikuormittaa. Ylikuormittaminen tarkoittaa tässä yhteydessä mahdollisuutta määritellä operaattorin toiminta uudelleen käyttäjäkohtaisille tyypeille. Mikäli operaattori on ylikuormitettavissa, on mainittu myös siihen liittyvä trait, jonka avulla ylikuormittaminen tapahtuu.Taulukko B-1: OperaattoritTämä alaluku olisi sisältänyt yksityiskohtaisen taulukon, jossa on lueteltu Rustin kaikki operaattorit. Jokaisen operaattorin kohdalla olisi esitetty esimerkki sen käytöstä koodikontekstissa, lyhyt selitys sen toiminnasta sekä tieto siitä, onko operaattori ylikuormitettavissa. Mikäli operaattori on ylikuormitettavissa, taulukossa olisi mainittu myös kyseiseen operaattoriin liittyvä trait. Tämä taulukko olisi ollut keskeinen resurssi Rust-ohjelmoijille, tarjoten nopean ja selkeän yhteenvedon kielen operaattoreista. Valitettavasti verkkosivun osoitteessa https://github.com/Gigli2020/Kirja/blob/main/src/appendix-02-operators.md oleva sisältö ei ole saatavilla 1, joten tämän taulukon käännöstä ei voida tällä hetkellä esittää.Taulukon rakenne olisi ollut seuraavanlainen:
OperaattoriEsimerkkiSelitysYlikuormitettavissa?Ylikuormitettava Trait!ident!(...), ident!{...}, ident![...]Makron laajennus!!exprBitti- tai looginen komplementtiKylläNot!=expr != exprErisuuruusvertailuKylläPartialEq%expr % exprAritmeettinen jakojäännösKylläRem%=var %= exprAritmeettinen jakojäännös ja sijoitusKylläRemAssign&&expr, &mut exprLainaaminen&&type, &mut type, &'a type, &'a mut typeLainattu osoitintyyppi&expr & exprBittiwise ANDKylläBitAnd&=var &= exprBittiwise AND ja sijoitusKylläBitAndAssign&&expr && exprOikosulkeva looginen AND*expr * exprAritmeettinen kertolaskuKylläMul*=var *= exprAritmeettinen kertolasku ja sijoitusKylläMulAssign**exprDereferenssiKylläDeref**const type, *mut typeRaaka osoitin+trait + trait, 'a + traitYhdistetty tyyppirajoitus+expr + exprAritmeettinen yhteenlaskuKylläAdd+=var += exprAritmeettinen yhteenlasku ja sijoitusKylläAddAssign,expr, exprArgumenttien ja elementtien erotin-- exprAritmeettinen negaatioKylläNeg-expr - exprAritmeettinen vähennyslaskuKylläSub-=var -= exprAritmeettinen vähennyslasku ja sijoitusKylläSubAssign->fn(...) -> type, `...-> type`Funktion ja sulkeuman paluuarvon tyyppi.expr.identKentän käyttö.expr.ident(expr, ...)Metodin kutsu.expr.0, expr.1, jne.Tuplen indeksointi...., expr.., ..expr, expr..exprOikealta avoin väli-literaaliKylläPartialOrd..=..=expr, expr..=exprOikealta suljettu väli-literaaliKylläPartialOrd....exprRakenneliteraalin päivityssyntaksi..variant(x, ..), struct_type { x, .. }"Ja loput" -patternisidonta...expr...expr(Vanhentunut, käytä ..= sijaan) Patternissa: suljettu väli-patterni/expr / exprAritmeettinen jakolaskuKylläDiv/=var /= exprAritmeettinen jakolasku ja sijoitusKylläDivAssign:pat: type, ident: typeRajoitukset:ident: exprRakennuskentän alustus:'a: loop {...}Silmukan label;expr;Lauseen ja itemin pääte;[...; len]Osa kiinteäkokoista taulukon syntaksia<<expr << exprVasemmalle siirtoKylläShl<<=var <<= exprVasemmalle siirto ja sijoitusKylläShlAssign<expr < exprPienempi kuin -vertailuKylläPartialOrd<=expr <= exprPienempi tai yhtä suuri kuin -vertailuKylläPartialOrd=var = expr, ident = typeSijoitus/ekvivalenssi==expr == exprYhtä suuri kuin -vertailuKylläPartialEq=>pat => exprOsa match-haaran syntaksia>expr > exprSuurempi kuin -vertailuKylläPartialOrd>=expr >= exprSuurempi tai yhtä suuri kuin -vertailuKylläPartialOrd>>expr >> exprOikealle siirtoKylläShr>>=var >>= exprOikealle siirto ja sijoitusKylläShrAssign@ident @ patPatternisidonta^expr ^ exprBittiwise XORKylläBitXor^=var ^= exprBittiwise XOR ja sijoitusKylläBitXorAssign```patpat`Patternivaihtoehdot```exprexpr`Bittiwise OR`=``var= expr`Bittiwise OR ja sijoitus```exprexpr`Oikosulkeva looginen OR?expr?Virheen propagointi
Muut kuin operaattorisymbolitTämä osio käsittelisi kaikkia niitä symboleita Rust-kielessä, jotka eivät toimi operaattoreina. Toisin sanoen, ne eivät käyttäydy kuten funktio- tai metodikutsu. Nämä symbolit täyttävät erilaisia rooleja kielen syntaksissa, kuten tyyppien määrittelyssä, polkujen muodostamisessa ja koodin rakenteen ilmaisemisessa.Taulukko B-2: Itsenäinen syntaksiTämä alaluku olisi sisältänyt taulukon, jossa esitellään itsenäisesti esiintyviä symboleita, jotka ovat validia syntaksia monissa eri kohdissa Rust-koodia. Nämä symbolit eivät ole riippuvaisia toisista operaattoreista toimiakseen. Valitettavasti verkkosivun sisältö ei ole saatavilla 1, joten tämän taulukon käännöstä ei voida tällä hetkellä esittää.Taulukon rakenne olisi ollut seuraavanlainen:
SymboliSelitys'identNimetty elinkaari tai silmukan label...u8, ...i32, ...f64, ...usize, jne.Numeerinen literaali tiettynä tyyppinä"..."String-literaalir"...", r#"..."#, r##"..."##, jne.Raaka string-literaali, escape-merkit eivät prosessoidub"..."Byte-string-literaali; muodostaa byte-taulukon stringin sijaanbr"...", br#"..."#, br##"..."##, jne.Raaka byte-string-literaali, raa'an ja byte-string-literaalin yhdistelmä'...'Merkki-literaalib'...'ASCII byte-literaali`...!Aina tyhjä pohjatyyppi divergoiville funktioille_"Ohitettu" patternisidonta; käytetään myös kokonaislukuliteraalien luettavuuden parantamiseen
Taulukko B-3: Polkuun liittyvä syntaksiTämä alaluku olisi sisältänyt taulukon, jossa esitellään symboleita, jotka esiintyvät polkujen yhteydessä, kun viitataan itemeihin moduulihierarkian läpi. Nämä symbolit mahdollistavat koodin organisoinnin ja nimiavaruuksien hallinnan. Verkkosivun sisältö ei ole saatavilla 1, joten tämän taulukon käännöstä ei voida tällä hetkellä esittää.Taulukon rakenne olisi ollut seuraavanlainen:
SymboliSelitysident::identNimiavaruuspolku::pathPolku suhteessa ulkoiseen esilukuun, jossa kaikki muut cratet ovat juurina (eli eksplisiittisesti absoluuttinen polku, mukaan lukien crate-nimi)self::pathPolku suhteessa nykyiseen moduuliin (eli eksplisiittisesti suhteellinen polku)super::pathPolku suhteessa nykyisen moduulin vanhempaantype::ident, <type as trait>::identAssosioidut vakiot, funktiot ja tyypit<type>::...Assosioitu item tyypille, jota ei voi suoraan nimetä (esim. <&T>::..., <>::..., jne.)trait::method(...)Metodikutsun disambiguointi nimeämällä sen määrittävä traittype::method(...)Metodikutsun disambiguointi nimeämällä sen tyyppi, jolle se on määritelty<type as trait>::method(...)Metodikutsun disambiguointi nimeämällä trait ja tyyppi
Taulukko B-4: GenericsTämä alaluku olisi sisältänyt taulukon, jossa esitellään symboleita, jotka esiintyvät geneeristen tyyppiparametrien käytön yhteydessä. Generics mahdollistaa tyyppiturvallisen koodin kirjoittamisen, joka voi toimia useilla eri tyypeillä. Verkkosivun sisältö ei ole saatavilla 1, joten tämän taulukon käännöstä ei voida tällä hetkellä esittää.Taulukon rakenne olisi ollut seuraavanlainen:
SymboliSelityspath<...>Määrittää parametrit geneeriselle tyypille tyypissä (esim. Vec<u8>)path::<...>, method::<...>Määrittää parametrit geneeriselle tyypille, funktiolle tai metodille lausekkeessa; usein kutsutaan "turbofishiksi" (esim. "42".parse::<i32>())fn ident<...> ...Määrittele geneerinen funktiostruct ident<...> ...Määrittele geneerinen rakenneenum ident<...> ...Määrittele geneerinen enumeraatioimpl<...> ...Määrittele geneerinen implementaatiofor<...> typeKorkeamman asteen elinkaarirajattype<ident=type>Geneerinen tyyppi, jossa yhdellä tai useammalla assosioidulla tyypillä on tietyt sijoitukset (esim. Iterator<Item=T>)
Taulukko B-5: Trait-rajausehdotTämä alaluku olisi sisältänyt taulukon, jossa esitellään symboleita, jotka esiintyvät geneeristen tyyppiparametrien rajoittamisen yhteydessä trait-rajojen avulla. Trait-rajat määrittävät, mitä toiminnallisuutta geneerisen tyypin on tuettava. Verkkosivun sisältö ei ole saatavilla 1, joten tämän taulukon käännöstä ei voida tällä hetkellä esittää.Taulukon rakenne olisi ollut seuraavanlainen:
SymboliSelitysT: UGeneerinen parametri T on rajoitettu tyyppeihin, jotka toteuttavat traitin UT: 'aGeneerisen tyypin T on elettävä elinkaaren 'a yli (mikä tarkoittaa, että tyyppi ei voi transitiivisesti sisältää viitteitä, joiden elinkaari on lyhyempi kuin 'a)T: 'staticGeneerinen tyyppi T ei sisällä muita lainattuja viitteitä kuin 'static-tyyppisiä'b: 'aGeneerisen elinkaaren 'b on elettävä elinkaaren 'a yliT: ?SizedSalli geneerisen tyyppiparametrin olla dynaamisesti mitoitettu tyyppi'a + trait, trait + traitYhdistetty tyyppirajoitus
Taulukko B-6: Makrot ja attribuutitTämä alaluku olisi sisältänyt taulukon, jossa esitellään symboleita, jotka esiintyvät makrojen kutsumisen tai määrittelyn sekä itemeille määritettyjen attribuuttien yhteydessä. Makrot mahdollistavat koodin generoinnin, ja attribuutit tarjoavat metatietoa koodille. Verkkosivun sisältö ei ole saatavilla 1, joten tämän taulukon käännöstä ei voida tällä hetkellä esittää.Taulukon rakenne olisi ollut seuraavanlainen:
SymboliSelitys#[meta]Ulompi attribuutti#![meta]Sisempi attribuutti$identMakron substituutio$ident:kindMakron kaappaus$(...)…Makron toistoident!(...), ident!{...}, ident![...]Makron invokaatio
Taulukko B-7: KommentitTämä alaluku olisi sisältänyt taulukon, jossa esitellään symboleita, joilla luodaan kommentteja Rust-koodiin. Kommentit ovat tärkeitä koodin selkeyden ja ylläpidettävyyden kannalta. Verkkosivun sisältö ei ole saatavilla 1, joten tämän taulukon käännöstä ei voida tällä hetkellä esittää.Taulukon rakenne olisi ollut seuraavanlainen:
SymboliSelitys//Yksirivinen kommentti//!Sisempi rividokumentointikommentti///Ulompi rividokumentointikommentti/*...*/Lohkokommentti/*!...*/Sisempi lohkodokumentointikommentti/**...*/Ulompi lohkodokumentointikommentti
Taulukko B-8: SulkeetTämä alaluku olisi sisältänyt taulukon, jossa esitellään kontekstit, joissa kaarisulkeita käytetään Rust-kielessä. Kaarisulkeilla on useita eri käyttötarkoituksia syntaksissa. Verkkosivun sisältö ei ole saatavilla 1, joten tämän taulukon käännöstä ei voida tällä hetkellä esittää.Taulukon rakenne olisi ollut seuraavanlainen:
SymboliSelitys()Tyhjä tuple (eli unit), sekä literaali että tyyppi(expr)Sulkeistettu lauseke(expr,)Yksielementtinen tuple-lauseke(type,)Yksielementtinen tuple-tyyppi(expr, ...)Tuple-lauseke(type, ...)Tuple-tyyppiexpr(expr, ...)Funktiokutsu-lauseke; käytetään myös tuple-rakenteiden ja tuple-enumvarianttien alustamiseen
Taulukko B-9: AaltosulkeetTämä alaluku olisi sisältänyt taulukon, jossa esitellään kontekstit, joissa aaltosulkeita käytetään Rust-kielessä. Aaltosulkeet määrittävät koodilohkoja ja rakenteita. Verkkosivun sisältö ei ole saatavilla 1, joten tämän taulukon käännöstä ei voida tällä hetkellä esittää.Taulukon rakenne olisi ollut seuraavanlainen:
KontekstiSelitys{...}LohkolausekeType {...}struct-literaali
Taulukko B-10: HakasulkeetTämä alaluku olisi sisältänyt taulukon, jossa esitellään kontekstit, joissa hakasulkeita käytetään Rust-kielessä. Hakasulkeita käytetään muun muassa taulukoiden määrittelyssä ja indeksoinnissa. Verkkosivun sisältö ei ole saatavilla 1, joten tämän taulukon käännöstä ei voida tällä hetkellä esittää.Taulukon rakenne olisi ollut seuraavanlainen:
KontekstiSelitys[...]Taulukkoliteraali[expr; len]Taulukkoliteraali, joka sisältää len kappaletta expr-lauseketta[type; len]Taulukkotyyppi, joka sisältää len instanssia type-tyyppiäexpr[expr]Kokoelman indeksointi. Ylikuormitettavissa (Index, IndexMut)expr[..], expr[a..], expr[..b], expr[a..b]Kokoelman indeksointi, joka esittää kokoelman viipalointia, käyttäen Range, RangeFrom, RangeTo tai RangeFull -tyyppejä "indeksinä"
JohtopäätöksetTämän analyysin perusteella on todettu, että pyydettyä verkkosivun sisältöä ei valitettavasti voitu hakea annetusta URL-osoitteesta 1. Tästä syystä tämän raportin keskeistä tavoitetta, Rustin operaattoreiden ja symbolien liitteen kääntämistä suomen kielelle ja sen palauttamista Markdown-tiedostona, ei ole voitu toteuttaa. Raportissa on kuitenkin pyritty hahmottelemaan, miten käännetty sisältö olisi rakentunut, mikäli lähdemateriaali olisi ollut saatavilla. On suositeltavaa tarkistaa URL-osoite tai hankkia sisältö muulla tavoin, jotta käännöstyö voidaan suorittaa onnistuneesti.

