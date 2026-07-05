# 🐄 KUBOWLING 🎳

*Tidenes mulighet for å spille bowling med kyr.*

En liten fysikk-simulator inspirert av et helt reelt jorde: kyr som beiter i en
bratt bakke, med et skur nederst. Spark en ku og se den trille nedover og velte
resten — bowling med kyr.

## Slik spiller du

Åpne `index.html` i en nettleser (ingen avhengigheter, alt er én fil).

- **Dra over en ku og slipp** for å sparke den i valgt retning og styrke.
- **Trykk kort på en ku** for et standard spark utfor bakken.
- Kyr som ligger med beina i været kan sparkes igjen.
- Velt alle 7 for **STRIKE!**
- «Nye kyr» setter opp jordet på nytt.

## Fysikken

Egenskrevet 2D-fysikk på `<canvas>`: tyngdekraft, terreng som høydefelt med
normal-/tangentdekomponering, rullefriksjon, restitusjon, ku-mot-ku-støt og
kjedereaksjoner nedover bakken. Pluss syntetiske «MØØ»-lyder via WebAudio.

Ingen kyr ble skadet under utviklingen.
