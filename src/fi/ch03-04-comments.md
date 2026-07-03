## Kommentit

Kaikki ohjelmoijat pyrkivät tekemään koodistaan helposti ymmärrettävää, mutta joskus tarvitaan lisäselitystä. Näissä tapauksissa ohjelmoijat jättävät _kommentteja_ lähdekoodiinsa, joita kääntäjä ohittaa, mutta joita lähdekoodia lukevat ihmiset saattavat pitää hyödyllisinä.

Tässä on yksinkertainen kommentti:

```rust
// hello, world
```

Rustissa idiomaattinen kommenttityyli aloittaa kommentin kahdella kauttaviivalla, ja kommentti jatkuu rivin loppuun. Kommenteille, jotka ulottuvat useammalle riville, sinun täytyy sisällyttää `//` jokaiselle riville, näin:

```rust
// So we're doing something complicated here, long enough that we need
// multiple lines of comments to do it! Whew! Hopefully, this comment will
// explain what's going on.
```

Kommentit voidaan myös sijoittaa koodia sisältävien rivien loppuun:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-24-comments-end-of-line/src/main.rs}}
```

Mutta näet ne useammin tässä muodossa, kommentti erillisellä rivillä sen koodin yläpuolella, jota se selittää:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-25-comments-above-line/src/main.rs}}
```

Rustissa on myös toinenlaisia kommentteja, dokumentaatiokommentteja, joita käsittelemme ["Craten julkaiseminen Crates.io:hon"][publishing]<!-- ignore --> -osiossa Luvussa 14.

[publishing]: ch14-02-publishing-to-crates-io.html
