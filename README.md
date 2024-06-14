# Rakettmotor

Oppgavebesvarelse for muntlig praksis eksamen programmering og modellering X vår 2024.


## Oppgaven
Verdier er hentet inn for skyvekraften _F_ til en rakettmotor, disse ligger i en fil kalt `rakettdata.csv`
Du skal modellere akselerasjonen, farten og posisjonen til en rakett som bruker denne motoren og blir skutt rett opp.
Rakettens masse er typisk 100 g og tyngdens akselerasjon regnes som 9,81 m/s^2.
Tegn grafer og forklar hva du har gjort. Finn også ut hvor høyt raketten kommer.

Ting du må tenke på og som du kan vurdere å ta med i oppgaven:
- Verdiene i csv-filen må renses, dvs det er noen av verdiene som ikke gir mening og må ekskluderes.
- Programmet skal ikke krasje hvis noen verdier endres til å være urealistiske.
- Hvordan kan du endre problemstillingen til å ta med luftmotstand? Blir grafene veldig annerledes da?
- Anta at massen til rakettmotoren er 20 g når den begynner og mister 10 gram masse i løpet av tidsrommet motoren virker. Hvordan kan eventuelt dette påvirke framdriften av raketten?
- Du kan vurdere å la raketten skytes ut på skrå, hvor langt og hvor høyt vil raketten nå avhengig av vinkel? Tegn grafer.


## Programmet
For å kjøre programmet, kjør `src/main.py` filen. 