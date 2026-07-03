## Tiivis ohjausrakenne `if let`- ja `let...else`-rakenteilla

`if let`-syntaksi antaa yhdistää `if`- ja `let`-rakenteet vähemmän puhelijaan tapaan käsitellä arvoja, jotka täsmäävät yhteen kuvioon, ja sivuuttaa loput.
Harkitse Listauksen 6-6 ohjelmaa, joka täsmää `Option<u8>`-arvon `config_max`-muuttujassa, mutta haluaa suorittaa koodia vain, jos arvo on `Some`-variantti.

<Listing number="6-6" caption="`match`, joka välittää vain `Some`-arvon suorittamisesta koodia">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-06/src/main.rs:here}}
```

</Listing>

Jos arvo on `Some`, tulostamme `Some`-variantin arvon sitomalla arvon muuttujaan `max` kuviossa. Emme halua tehdä mitään `None`-arvolla. `match`-lausekkeen
tyydyttämiseksi meidän täytyy lisätä `_ => ()` yhden variantin käsittelyn jälkeen, mikä on ärsyttävää ylimääräistä koodia.

Sen sijaan voisimme kirjoittaa tämän lyhyemmällä tavalla käyttämällä `if let`-rakennetta. Seuraava koodi käyttäytyy samoin kuin Listauksen 6-6 `match`:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-12-if-let/src/main.rs:here}}
```

`if let`-syntaksi ottaa kuvion ja lausekkeen, jotka erotetaan yhtäsuuruusmerkillä. Se toimii samalla tavalla kuin `match`, jossa lauseke annetaan `match`:lle
ja kuvio on sen ensimmäinen haara. Tässä tapauksessa kuvio on `Some(max)`, ja `max` sitoutuu `Some`:n sisällä olevaan arvoon. Voimme sitten käyttää `max`:ia
`if let`-lohkon rungossa samalla tavalla kuin käytimme `max`:ia vastaavassa `match`-haarassa. `if let`-lohkon koodi suoritetaan vain, jos arvo täsmää kuvioon.

`if let` tarkoittaa vähemmän kirjoittamista, vähemmän sisennystä ja vähemmän ylimääräistä koodia. Menetät kuitenkin `match`-lausekkeen pakottaman tyhjentävän
tarkistuksen, joka varmistaa, ettei sinun unohda käsitellä mitään tapauksia. Valinta `match`- ja `if let`-rakenteiden välillä riippuu siitä, mitä teet
tietyssä tilanteessa, ja siitä, onko tiiviys sopiva kompromissi tyhjentävän tarkistuksen menettämisestä.

Toisin sanoen voit ajatella `if let`:iä syntaksisokerina `match`-lausekkeelle, joka suorittaa koodia, kun arvo täsmää yhteen kuvioon, ja sitten sivuuttaa kaikki
muut arvot.

Voimme liittää `else`-haaran `if let`-rakenteeseen. `else`-haaraan liittyvä koodilohko on sama kuin koodilohko, joka menisi `_`-tapaukseen `match`-lausekkeessa,
joka vastaa `if let`- ja `else`-rakennetta. Muista Listauksen 6-4 `Coin`-enumin määrittely, jossa `Quarter`-variantti sisälsi myös `UsState`-arvon. Jos
haluaisimme laskea kaikki ei-25-senttiset kolikot ja samalla ilmoittaa 25 sentin kolikoiden osavaltiot, voisimme tehdä sen `match`-lausekkeella näin:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-13-count-and-announce-match/src/main.rs:here}}
```

Tai voisimme käyttää `if let`- ja `else`-lauseketta näin:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-14-count-and-announce-if-let-else/src/main.rs:here}}
```

## Pysyminen ”onnellisella polulla” `let...else`-rakenteella

Yleinen kuvio on suorittaa laskenta, kun arvo on läsnä, ja palauttaa oletusarvo muuten. Jatkamalla kolikkoesimerkkiämme `UsState`-arvolla, jos haluaisimme
sanoa jotain hauskaa riippuen siitä, kuinka vanha 25 sentin kolikon osavaltio on, voisimme lisätä `UsState`-rakenteeseen metodin, joka tarkistaa osavaltion
iän, näin:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-07/src/main.rs:state}}
```

Sitten voisimme käyttää `if let`:iä täsmätäksemme kolikon tyyppiin ja esitelläksemme `state`-muuttujan ehdon rungon sisällä, kuten Listauksessa 6-7.

<Listing number="6-7" caption="Tarkistus, oliko osavaltio olemassa vuonna 1900, käyttämällä ehtorakenteita `if let`:n sisällä">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-07/src/main.rs:describe}}
```

</Listing>

Se hoitaa asian, mutta on siirtänyt työn `if let`-lausekkeen runkoon, ja jos tehtävä on monimutkaisempi, voi olla vaikea seurata, miten ylätason haarat
liittyvät toisiinsa. Voisimme myös hyödyntää sitä, että lausekkeet tuottavat arvon, joko tuottaaksemme `state`:n `if let`:stä tai palauttaaksemme aikaisin,
kuten Listauksessa 6-8. (Voit tehdä jotain vastaavaa myös `match`-lausekkeella.)

<Listing number="6-8" caption="`if let`:n käyttö arvon tuottamiseen tai aikaisen paluun tekemiseen">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-08/src/main.rs:describe}}
```

</Listing>

Tämä on kuitenkin omalla tavallaan hieman ärsyttävää seurata! Yksi `if let`-haara tuottaa arvon, ja toinen palaa kokonaan funktiosta.

Tämän yleisen kuvion ilmaisemiseksi miellyttävämmällä tavalla Rustissa on `let...else`. `let...else`-syntaksi ottaa kuvion vasemmalle puolelle ja lausekkeen
oikealle puolelle, hyvin samankaltaisesti kuin `if let`, mutta siinä ei ole `if`-haaraa, vain `else`-haara. Jos kuvio täsmää, se sitoo arvon kuviosta
ulompaan näkyvyysalueeseen. Jos kuvio _ei_ täsmää, ohjelma siirtyy `else`-haaraan, jonka täytyy palata funktiosta.

Listauksessa 6-9 näet, miltä Listaus 6-8 näyttää, kun `if let` korvataan `let...else`-rakenteella.

<Listing number="6-9" caption="`let...else`:n käyttö funktion kulun selkeyttämiseen">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-09/src/main.rs:describe}}
```

</Listing>

Huomaa, että näin pysytään ”onnellisella polulla” funktion päärungossa ilman merkittävästi erilaista ohjausrakennetta kahdelle haaralle, kuten `if let` teki.

Jos ohjelmassasi on logiikkaa, joka on liian puheliasta ilmaistavaksi `match`-lausekkeella, muista, että `if let` ja `let...else` ovat myös Rust-työkalupakissasi.

## Yhteenveto

Olemme nyt käsitelleet, miten enumien avulla luodaan mukautettuja tyyppejä, jotka voivat olla yksi joukosta lueteltuja arvoja. Olemme näyttäneet, miten
standardikirjaston `Option<T>`-tyyppi auttaa käyttämään tyyppijärjestelmää virheiden estämiseen. Kun enum-arvoilla on dataa sisällään, voit käyttää `match`- tai
`if let`-rakennetta poimiaksesi ja käyttääksesi näitä arvoja riippuen siitä, kuinka monta tapausta sinun täytyy käsitellä.

Rust-ohjelmasi voivat nyt ilmaista sovellusalueesi käsitteitä rakenteiden ja enumien avulla. Mukautettujen tyyppien luominen API:isi käyttöön varmistaa
tyyppiturvallisuuden: kääntäjä varmistaa, että funktiosi saavat vain sellaisia arvoja, joita kukin funktio odottaa.

Jotta voit tarjota käyttäjillesi hyvin organisoidun ja suoraviivaisen API:n, joka paljastaa juuri sen, mitä käyttäjät tarvitsevat, siirrytään nyt Rustin moduuleihin.
