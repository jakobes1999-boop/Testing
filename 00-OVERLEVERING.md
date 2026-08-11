# Overlevering: status og neste steg

> **Les dette først.** Notatet skal gjøre det mulig for en ny sesjon (eller en ny person) å ta over arbeidet uten å ha vært med underveis. Sist oppdatert: 11. august 2026.

---

## 0. Driftsmerknad — viktig

Den lokale arbeidskopien i `/home/user/Testing` ble **nullstilt én gang** under arbeidet (tomt git-repo, ingen filer), uten at noe var galt med selve arbeidet: alle commits var pushet til GitHub og ble hentet tilbake i sin helhet.

**Hvis filene mangler når du starter:**
```bash
git fetch origin claude/background-research-setup-tywjxq
git checkout -B claude/background-research-setup-tywjxq FETCH_HEAD
```
Remote (`github.com/jakobes1999-boop/Testing`) er sannheten. Commit og push ofte — ikke la arbeid ligge ucommittet.

---

## 1. Oppdraget

Norges Skiforbund (NSF) vedtok på Skitinget 2026 (**sak 11.3**) at Skistyret skal legge frem en **revidert skilisensordning innen 1. oktober 2026**. Et hurtigarbeidende utvalg er nedsatt (styresak 6/2026–2028). Dette repoet er kunnskapsgrunnlaget og forarbeidet til utvalgets rapport.

**Skistyrets fem prinsipper** (fra innstillingen i sak 11.3), som enhver anbefaling må måles mot:
tydelig minimumsordning · reduserte barrierer · frivillige tilleggsforsikringer · forenkling for arrangører · rolleavklaring mot offentlig helsevesen. Ordningen skal være **selvfinansiert**.

## 2. Problemet i fem punkter

1. **Prissjokk:** utvidet alpinlisens +173 % på to år (1 900 → 5 200 kr); langrenn og telemark fikk også hopp i 2024.
2. **Manglende differensiering:** én ordning på tvers av grener med svært ulik skaderisiko.
3. **Engangslisensen (300 kr) hevdes å være barriere for turrenn** — merk: dette er interessentenes påstand, *ikke* dokumentert kausalitet (se pkt. 6).
4. **Økonomisk ubalanse:** NSF subsidierer med 1,6 MNOK (2025), forventet 2 MNOK (2026), trass i selvfinansieringskravet. If-premien +40 %.
5. **Uavklart prinsipielt mandat:** dekningsomfanget har vokst uten prinsippavklaring; to overleger har offentlig kritisert at ordningen finansierer privat behandling for tilstander det offentlige dekker.

**Volumkontekst:** ~6 700 lisenser (2023/24) mot ~110 000 aktive medlemmer. Lisensinntekt 12,9 MNOK (2024). NSF har hatt størst medlemsfall av alle særforbund 2018–2024 (–25,6 %).

## 3. Repoets innhold

| Fil | Innhold |
|---|---|
| `README.md` | Innholdsfortegnelse |
| `01-datainnhentingsplan.md` | Spørsmål, datakategorier, kilder, tidslinje |
| `02-bestillingsliste-internt.md` | **Databestillinger** — pkt. 1–7 hovedbestilling, pkt. 8 restliste, pkt. 9 tillegg etter panelvurderingen |
| `03-syntese-modellalternativer.md` | Problembilde, rammer, **modell A–E** vurdert mot mandatet |
| `04-prinsipielle-vurderinger.md` | Teoriforankret analyse, **ni designprinsipper** |
| `05-rapportdisposisjon.md` | Skjelett for sluttrapporten + produksjonsplan |
| `06-epostutkast.md` | Fem ferdige e-poster (mangler bare navn/datoer) |
| `07-panelvurdering.md` | Tre uavhengige kvalitetsvurderinger: funn, rettelser, beslutningsporter |
| `bakgrunn/10–17` | Kildebelagte researchnotater (dagens ordning, ni særforbund, Norden/FIS/turrenn, statistikk, debatt, alpeland/USA, juridisk, litteratur) |
| `verktoy/lisenskalkulator.html` | Interaktiv scenariokalkulator (kalibrert mot 2025/26-satser) |

## 4. De fem modellene

- **A — Justert dagens ordning:** brattere grendifferensiering, lavere engangslisens, ungdomsrabatt, indeksert prisjustering. Rask, trygg, løser 3 av 5 problemer.
- **B — Obligatorisk minimum + frivillige tillegg** (fransk modell, FFS): billig obligatorisk kjerne (ansvar + akutt/redning + invaliditet/død), behandlingsdekning blir valgfri. *Materialets hovedhypotese.*
- **C — Todelt:** individuell lisens for konkurranse + arrangørkollektiv forsikring for turrenn (Vasaloppet-modellen).
- **D — Medlemskaps-/klubbmodell** (Sverige/Danmark): ingen individuell startlisens; kollektiv dekning via klubb/forbund. Langsiktig retning.
- **E — NIF-samordnet fellesforsikring:** pågående NIF-arbeid om synergier på tvers av særforbund. Primært en **koordineringsrisiko** — må avklares før modellvalg.

**Status for anbefalingen:** B (ev. B+C) er formulert som **hypotese med beslutningsporter**, ikke konklusjon. Feller meglersvarene premissene om opt-in-grad eller poolstørrelse, er **A riktig anbefaling**.

**Ekspertrådets dom** (`08-radsvurdering.html`, seks seter): ingen av setene mener B/C kan *tallfestes* til 1. oktober. Rådets anbefaling er å omramme leveransen fra «anbefalt modell» til **prinsippvedtak (Tinbergen-strukturen) + minimumsdifferensiert A som ettårsbro for 2026/27 + bundet to-trinnsløp med hardkodet dato for tallfestet B før 2027/28**. Merk mindretallsinnvendingen: en tredje prisjustering på tre år signaliserer at forbundet ikke har en plan, og «A som bro» endrer ingenting arkitektonisk.

**Tidslinjen er strammere enn planen antar:** det er 51 dager (7,3 uker) til fristen, og produksjonsplanen i `05-rapportdisposisjon.md` la interne data til uke 32 — som er passert. Ingen bestillinger er sendt. Dette er avgjørende for hva som realistisk kan leveres.

## 5. Kritisk sti — det som må skje nå

| Prioritet | Handling | Hvorfor |
|---|---|---|
| 1 | **Send e-post 1** (`06-epostutkast.md`) til generalsekretariatet | Tingprotokollen med utvalgets formelle mandat er ikke mottatt. Alt hviler på ordlyden. Samme e-post ber om status for forsikringsanbudet — som kan endre premiegrunnlaget midt i perioden. |
| 2 | **Send e-post 2** til NSF-økonomi og megler, supplert med pkt. 9.1–9.5 | Inneholder de to tallene som avgjør modellvalget: aktuarisk pris på isolert minimumsprodukt (B) og kollektiv turrennpolise per deltaker (C). |
| 3 | **Juristsjekk:** Skitinget eller Skistyret som vedtaksorgan? | Avgjør hvem innstillingen adresseres til. Se `bakgrunn/16`, spørsmål 1–2. |
| 4 | Innspillsrunde til kretser/grener (e-post 4) og arrangørintervjuer (e-post 5) | Må inkludere **små klubbarrangører**, ikke bare Birken. |
| 5 | Avklar **NIF-sporet** (restliste 8.5) | Kan gjøre en NSF-spesifikk arkitektur foreldet. |

**Merk:** e-post 2 er adressert til Söderberg & Partners, men meglerrollen fremgår *ikke* av forsikringsbeviset — bekreft før utsendelse (restliste 8.9).

## 6. Kjente svakheter i grunnlaget — ikke gjenta disse

Panelvurderingen (`07`) fant følgende. Rettet: ✔ · Åpent: ○

- ✔ **«6 700 helårslisenser»** — uverifisert om engangslisenser inngår; forbehold er gjeninnført. Ikke bruk tallet som kalibreringsgrunnlag uten forbehold.
- ✔ **«Engangslisensen svekker turrenn»** — nedgradert til interessentpåstand. Kondis' egen analyse av turrennfallet nevner *ikke* lisens, og ingen skirenn har forlatt terminlisten pga. lisenskravet.
- ✔ Regnefeil rettet (barn 6–12 år: −35 %, ikke «mer enn halvert»).
- ○ **Sprikende økonomitall:** underskuddet 4,2 MNOK oppgis for både 2019–2024 og 2021–2024; subsidiering oppgis som 1,2/1,0 MNOK (Vedlegg 7) og 1,6/2,0 MNOK (Skistyret). Trolig ulike definisjoner — **må avstemmes** mot Vedlegg 7 før tallene brukes i rapporten.
- ○ Aldersfordelingen summerer ikke til totalt aktive (gap 4,5–6 %), uforklart.
- ○ «+126 %» for langrenn hviler på delvis verifisert prisserie (740/2 600 → 650/2 400?).
- ○ USSS-priser fra søkeindeks; alpin skadefrekvens 0,96/1 000 skidager mangler datert primærkilde.

**Kalkulatoren kan ikke vedlegges rapporten som den står** (rådets deal-breaker): den antar stilltiende ~9 000 udokumenterte engangslisenser (antatt univers 15 700) og presenterer resultatet som «kalibrert»; lineær punktelastisitet ekstrapoleres mekanisk til store prissjokk (−69 % volum ved 173 % prisøkning, uten empirisk forankring); premien er to globale skalarer påført alle segmenter, så verktøyet kan strukturelt ikke representere antiseleksjon; admin som 5 % av brutto gir B/C en mekanisk fordel i alle scenarioer. Må bygges om eller nedgraderes til illustrasjon med eksplisitte forbehold.

**Modell C har ingen realistisk motpart nå** (rådets deal-breaker): Birken er i uavklart rettskonflikt med Norges Cykleforbund om eierskap til nøyaktig denne typen lisensinntekter. Å forhandle en kollektivmodell med dem på sju uker er ikke gjennomførbart. Presedensen fra 2014 — der Birken selv dekket lisenskostnaden for alle deltakere for å hindre kaos før sesongstart — viser hvor fort dette eskalerer.

**Underbelyste grupper** som må dekkes: toppidrett/landslag, para-utøvere og ledsagere, TD-er/funksjonærer, kretsenes inntektsandel, små dugnadsbaserte arrangører, utenlandske deltakere.

## 7. Fem premisser som må testes før modellvalg

1. **Blir opt-in-graden på frivillige tillegg høy nok** til å unngå ruinøs antiseleksjon? *Test:* håndballens faktiske LISE/Pluss/Super-fordeling (bestilling 9.3).
2. **Er lisensen faktisk en hoveddriver** for turrennfallet? *Test:* lisensundersøkelsen + deltakertall mot prisendringer.
3. **Skyldes premieøkningen produktstruktur eller reell skadeutvikling?** Hvis det siste, flytter B/C bare problemet. *Test:* Ifs egen begrunnelse (bestilling 9.5).
4. **Tåler ~6 700 lisenser differensiering** i gren × nivå × alder? *Test:* meglers vurdering av minste bærekraftige poolstørrelse (9.4).
5. **Kan små arrangører bære kollektivmodellen?** *Test:* arrangørdialog utover Birken.

## 8. Arbeidsmåte og konvensjoner

- **Alt skrives på norsk.** Faglig, nøkternt — Oslo Economics' husstil (skillen `oslo-economics-skrivestil` finnes).
- **Kildeføring:** URL til alt; usikre påstander merkes eksplisitt `[IKKE VERIFISERT]` / `[ANTAKELSE]`. Dette er strengt håndhevet — panelet fanget flere brudd.
- **Branch:** `claude/background-research-setup-tywjxq`. Commit på norsk, push etter hver leveranse.
- **Habilitet:** Oslo Economics' egen rapport for Kulturdepartementet (OE 2020-12, «Økonomi som barriere for idrettsdeltakelse») er en sentral kilde — tilknytningen bør opplyses ved bruk.

## 9. Hva som gjenstår faglig

Når dataene kommer: fyll rapportens kap. 4 og 7 (`05-rapportdisposisjon.md`), kjør scenarioene i kalkulatoren med reelle tall, og legg inn følsomhetsanalyse (lav/midt/høy for opt-in-grad og priselastisitet) samt break-even: minste opt-in-grad der B/C ikke krever fortsatt subsidiering.

Analyser som kan gjøres **før** dataene kommer: TAM-anslag for turrennsegmentet fra SSB × NSF-tall; prisbånd for minimumsproduktet fra nordiske referanser; back-of-envelope-proveny for modell C fra Birken-tidsserien × Vasaloppet-premier; sensitivitetskjøring med Wicker-elastisiteter mot dagens antatte.
