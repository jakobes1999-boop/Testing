# Norge – England · Live odds-dashbord

Et selvstendig dashbord (én HTML-fil, ingen avhengigheter) som viser forventet
resultat for VM-kvartfinalen Norge–England 11. juli 2026, basert på live
markedsodds.

## Bruk

Åpne `index.html` i en nettleser. Siden henter odds og stilling automatisk
hvert 30. sekund fra ESPNs åpne scoreboard-API (odds fra DraftKings, som har
`Access-Control-Allow-Origin: *`, så det fungerer også fra `file://`).

## Hva vises

- **Live stilling og kampklokke**
- **Forventet resultat**: mest sannsynlige utfall fra markedets 1X2-odds
  (margin fjernet ved normalisering), pluss mest sannsynlige sluttresultat og
  forventet antall mål fra en Poisson-modell for gjenstående mål, kalibrert
  mot markedssannsynlighetene gitt stillingen nå
- **Sannsynlighetstiles og 100 %-stablet fordeling** for Norge / uavgjort / England
- **Linjediagram** over hvordan vinnersannsynlighetene utvikler seg gjennom
  kampen (historikken lagres i `localStorage`)
- **Oddstabell** med åpningsodds, gjeldende amerikansk og desimalodds,
  implisitt sannsynlighet og sannsynlighet uten bookmakermargin

Odds er markedspriser, ikke fasit.
