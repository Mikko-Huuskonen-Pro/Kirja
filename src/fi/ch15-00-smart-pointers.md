# Älykkäät osoittimet

Osoitin on yleinen käsite muuttujalle, joka sisältää muistiosoitteen. Tämä osoite
viittaa johonkin muuhun dataan tai ”osoittaa” sitä. Rustin yleisin osoitintyyppi on
viite, josta opit luvussa 4. Viitteet merkitään `&`-symbolilla ja lainaavat arvoa,
johon ne viittaavat. Niillä ei ole erityisiä ominaisuuksia datan viittaamisen lisäksi,
eikä niihin liity ylimääräistä kuormitusta.

_Älykkäät osoittimet_ puolestaan ovat datarakenteita, jotka käyttäytyvät osoittimien
tavoin mutta sisältävät myös lisämetatietoa ja -ominaisuuksia. Älykkäiden osoittimien
käsite ei ole Rustille ainutlaatuinen: ne ovat peräisin C++:sta ja esiintyvät muissakin
kielissä. Rustissa on standardikirjastossa useita älykkäitä osoittimia, jotka tarjoavat
toiminnallisuutta viitteiden tarjoaman lisäksi. Tutustumme yleiseen käsitteeseen
tarkastelemalla muutamia eri esimerkkejä älykkäistä osoittimista, mukaan lukien
_viitelaskennallinen_ älykäs osoitintyyppi. Tämä osoitin mahdollistaa usean omistajan
sallimisen pitämällä kirjaa omistajien määrästä ja vapauttamalla datan, kun omistajia ei
enää ole.

Rustissa omistajuuden ja lainauksen käsitteiden vuoksi viitteiden ja älykkäiden
osoittimien välillä on lisäero: vaikka viitteet lainaavat dataa, älykkäät osoittimet
omistavat usein datan, johon ne viittaavat.

Älykkäät osoittimet toteutetaan yleensä rakenteina. Tavallisesta rakenteesta poiketen
älykkäät osoittimet toteuttavat `Deref`- ja `Drop`-traitit. `Deref`-traitin avulla
älykkään osoittimen instanssi voi käyttäytyä viitteen tavoin, jolloin koodisi voi toimia
sekä viitteiden että älykkäiden osoittimien kanssa. `Drop`-traitin avulla voit
mukauttaa koodia, joka suoritetaan, kun älykkään osoittimen instanssi poistuu
näkyvyysalueeltaan. Tässä luvussa käsittelemme molempia traitteja ja selitämme, miksi ne
ovat tärkeitä älykkäille osoittimille.

Koska älykkäiden osoittimien malli on yleinen suunnittelumalli, jota käytetään
Rustissa usein, tämä luku ei kata kaikkia olemassa olevia älykkäitä osoittimia. Monilla
kirjastoilla on omia älykkäitä osoittimiaan, ja voit kirjoittaa omasikin. Käsittelemme
yleisimmät standardikirjaston älykkäät osoittimet:

- `Box<T>` arvojen allokointiin pinomuistiin
- `Rc<T>`, viitelaskennallinen tyyppi, joka mahdollistaa usean omistajuuden
- `Ref<T>` ja `RefMut<T>`, joihin pääsee `RefCell<T>`-tyypin kautta; tyyppi pakottaa
  lainaussäännöt ajonaikana käännösaikan sijaan

Lisäksi käsittelemme _sisäisen muuttuvuuden_ mallin, jossa muuttumaton tyyppi tarjoaa
rajapinnan sisäisen arvon muuttamiseen. Käsittelemme myös viitesyklejä: miten ne voivat
vuotaa muistia ja miten niitä voi estää.

Aloitetaan!
