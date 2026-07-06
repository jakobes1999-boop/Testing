# 🐄 KUBOWLING 🎳

*Tidenes mulighet for å spille bowling med kyr.*

En liten fysikk-simulator inspirert av et helt reelt jorde: kyr som beiter i en
bratt bakke, med et skur nederst. Spark en ku og se den trille nedover og velte
resten — bowling med kyr.

## Slik spiller du

Åpne `index.html` i en nettleser (ingen avhengigheter, alt er én fil).

Velg perspektiv med knappen oppe til høyre:

- **3. person** — klassisk sidevisning av hele bakken.
- **1. person** — du står øverst i bakken, akkurat der bildet ble tatt, med
  den store Simmentalen rett foran deg. Kyrne beiter **sidelengs** over
  jordet, så du må time sparket til de står på linje. Dra oppover for å
  sparke kua nedover bakken, sidelengs for skru.

- **Dra over en ku og slipp** for å sparke den i valgt retning og styrke.
- **Trykk kort på en ku** for et standard spark utfor bakken.
- Du har bare **3 spark** — kyrne er tunge, vandrer rundt, og en liten
  bakketopp midtveis dreper farten. Bruk kjedereaksjoner!
- Kyr som ligger med beina i været kan sparkes igjen (koster et spark).
- Velt alle 7 for **STRIKE!** Går du tom for spark: **BOM!**
- «Nye kyr» setter opp jordet på nytt.

## Fysikken

Egenskrevet 2D-fysikk på `<canvas>`: tyngdekraft, terreng som høydefelt med
normal-/tangentdekomponering, rullefriksjon (terminalfarten til en rullende ku
ligger under veltegrensen, så bare ferske spark velter), restitusjon,
ku-mot-ku-støt og kjedereaksjoner nedover bakken. Grafikken er prosedural i
skumringslys: teksturert gress, lagvis skog, værbitt skur og kyr med raser
fra bildet. Pluss syntetiske «MØØ»-lyder via WebAudio.

Ingen kyr ble skadet under utviklingen.
