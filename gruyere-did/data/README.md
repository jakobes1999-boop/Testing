# Datadokumentasjon

Alle rådatafiler er uttrekk fra SSBs statistikkbank (PxWebApi v2), hentet via SSB-MCP 3. oktober 2026.
Rådatafilene røres ikke; all bearbeiding skjer i `../analyse.py`.

## 1. `ssb_08801_import_varenr_total.csv`

```
Kilde: SSB tabell 08801 «Utenrikshandel med varer, etter varenummer (HS) og land 1988–2025»
Filtre: Varekoder = 04069091_2001, 04069099_2001, 04069092_2013, 04069097_2013, 04069098_2013,
        04061001_2007, 04061009_2007, 04062000_1988, 04063000_1988, 04064001_2001, 04064005_2001,
        04064008_2001, 04064009_2001, 04064007_2020, 04069030_2001, 04069082_2001, 04069084_2001,
        04069089_2001; ImpEks = 1 (import); Land = eliminert (sum alle land);
        ContentsCode = Mengde1 (kg), Verdi (kr); Tid = 2008–2025
Enhet: kg og kroner, løpende priser (statistisk verdi, CIF)
Uttaksdato: 2026-10-03
```

## 2. `ssb_08801_import_hardost_land.csv`

```
Kilde: SSB tabell 08801 (som over)
Filtre: Varekoder = 04069091_2001, 04069099_2001, 04069092_2013, 04069097_2013, 04069098_2013;
        ImpEks = 1; Land = CH, FR, IT, DK, NL, DE, SE, ES, GB, IE, BE, AT, FI, PL, GR, US, LT, PT,
        CY, IS, NZ, CA, EE, LV; ContentsCode = Mengde1, Verdi; Tid = 2008–2021
Enhet: kg og kroner, løpende priser
Uttaksdato: 2026-10-03
Bearbeiding: Rader der alle verdier er 0 er utelatt fra filen (de tilsvarer null import).
```

Kontroll: summen over de 24 landene utgjør 98–100 % av totalen per varenummer og år, og 100,0 % for
de fleste år.

## 3. `ssb_08799_import_mnd_2011_2014.csv`

```
Kilde: SSB tabell 08799 «Utenrikshandel med varer, etter varenummer (HS) og land 1988M01–2026M08»
Filtre: Varekoder = 04069091_2001, 04069099_2001, 04069092_2013, 04069097_2013, 04069098_2013,
        04063000_1988; ImpEks = 1; Land = eliminert; ContentsCode = Mengde1 (kg);
        Tid = 2011M01–2014M12
Enhet: kg
Uttaksdato: 2026-10-03
```

Kontroll: månedssummene er identiske med årstallene i tabell 08801 for alle varenumre og år.

## 4. `ssb_14700_kpi_ost_mat.csv`

```
Kilde: SSB tabell 14700 «Konsumprisindeks (KPI), etter vare- og tjenestegruppe (2025=100)»
Filtre: VareTjenesteGrp = 01.1.4.5 (Ost), 01.1 (Matvarer); ContentsCode = KpiIndMnd;
        Tid = 2008M01–2019M12
Enhet: indeks, 2025 = 100
Uttaksdato: 2026-10-03
```

## Brudd i varenummerserien (viktig)

Tolltariffen for 0406.90 ble delt opp på nytt 1.1.2013:

| Periode   | Varenummer | Innhold | Tollsats utenfor kvote |
|-----------|-----------|---------|------------------------|
| 2001–2012 | 04069091  | Annen hard/halvhard ost, upasteurisert | 27,15 kr/kg |
| 2001–2012 | 04069099  | Annen hard/halvhard ost, pasteurisert  | 27,15 kr/kg |
| 2013–2021 | 04069092  | 14 navngitte oster (Gruyère, Parmigiano Reggiano, Comté, Appenzeller …) | 27,15 kr/kg (uendret) |
| 2013–2021 | 04069097  | Annen hard/halvhard ost, upasteurisert, i.e.n. | 277 % |
| 2013–2021 | 04069098  | Annen hard/halvhard ost, pasteurisert, i.e.n.  | 277 % |
| 2022–     | 04069093/97/98 | Ny inndeling, utvidet navneliste | – |

Summen 9091 + 9099 (før) og 9092 + 9097 + 9098 (etter) dekker samme varer og gir en konsistent
serie for «hard og halvhard ost». Gruyère og de andre navngitte ostene kan **ikke** skilles ut før 2013.
Hovedvinduet slutter i 2019 fordi pandemien og omkodingen i 2022 ellers ville gitt nye brudd i serien.

## 5. `ssb_08799_import_hardost_land_mnd_2022_2026.csv`

```
Kilde: SSB tabell 08799 (månedlig)
Filtre: Varekoder = 04069093_2022, 04069097_2022, 04069098_2022; ImpEks = 1; Land = CH, IT, FR;
        ContentsCode = Mengde1 (kg), Verdi (kr); Tid = 2022M01–2026M08
Enhet: kg og kroner, løpende priser
Uttaksdato: 2026-10-03
Formål: kontroll av om tollen på Gruyère/navngitte oster ble endret rundt 2024 (ingen brudd funnet).
```

## Ikke tilgjengelig: norsk osteproduksjon

SSB tabell 10455 (Prodcom 10.51.40.xx, ost) er prikket («:») fra og med 2010. Mengde norsk ost må
hentes fra Landbruksdirektoratets Markedsrapport eller Helsedirektoratets «Utviklingen i norsk kosthold».

## 6. `ssb_08801_import_eksport_hardost_2022_2025.csv`

```
Kilde: SSB tabell 08801
Filtre: Varekoder = 04069093_2022, 04069097_2022, 04069098_2022; ImpEks = 1, 2;
        Land = eliminert; ContentsCode = Mengde1, Verdi; Tid = 2022–2025
Uttaksdato: 2026-10-03
```

Rimelighetskontroll: samlet osteimport (alle 0406-varenumre) er 20 041 t i 2024 og 20 693 t i 2025.
Landbruksdirektoratets Markedsrapport oppgir 20 041 t og 20 683 t.

KPI-filen (`ssb_14700_kpi_ost_mat.csv`) er utvidet til 2008M01–2026M08 og omfatter nå også 00 (KPI totalt).
Årsgjennomsnittet for 2025 er 100,0 for alle tre gruppene, slik det skal være med 2025 = 100.

## 7. `manuelt_norsk_ost.csv` (manuell kilde, må fylles inn)

Norsk ost solgt i Norge (tonn per år) fra Landbruksdirektoratets Markedsrapport. Nettstedet er ikke
tilgjengelig fra analysemiljøet. Armington-modulen i `analyse.py` kjører når minst 10 år er fylt inn.

## 8. `ssb_08801_import_hardost_land_2022_2025.csv`

```
Kilde: SSB tabell 08801
Filtre: Varekoder = 04069093_2022, 04069097_2022, 04069098_2022; ImpEks = 1;
        Land = CH, FR, IT, DK, NL, DE, SE, ES, GB, EE; ContentsCode = Mengde1, Verdi; Tid = 2022–2025
Uttaksdato: 2026-10-03
Bearbeiding: Rader der alle verdier er 0 er utelatt (EE, 04069093).
```

Brudd: fra 2020 ble blåmuggliknende oster med Penicillium roqueforti-marmorering flyttet til 0406.40, og
fra 2022 ble navnelisten utvidet. Summen av hard ost per land (9093 + 9097 + 9098) er derfor ikke helt
sammenlignbar med 2008–2019. Forlengelsen til 2025 brukes bare som robusthetssjekk.
