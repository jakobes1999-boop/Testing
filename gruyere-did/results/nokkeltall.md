# Nøkkeltall (generert av analyse.py)

## 0. Tollkilen ved grensen (import utenfor kvote)
Enhetsverdi 2013, navngitte oster (9092): 105.6 kr/kg
Enhetsverdi 2013, annen hard ost (9097+9098): 58.2 kr/kg
Tollbelastet pris, annen hard ost: før 85 kr/kg, etter 220 kr/kg (157 %)
Relativ pris navngitt/annen: før 1.55, etter 0.60 (endring -61 %)
Prosenttollen er høyere enn kronetollen for alle oster med tollverdi over 9.80 kr/kg

## 1. Produkt-DiD: hard/halvhard ost mot seks upåvirkede ostekategorier, 2008–2019
log mengde (kg)            Hard/halvhard ost  β=-0.073 (-7 %), 2012: +11 %, RI-p=1.00, placebo-β i [-0.27, +0.28]
log mengde (kg)            Revet ost          β=+0.356 (+43 %), 2012: +1 %, RI-p=0.14, placebo-β i [-0.27, +0.28]
log mengde (kg)            Smelteost          β=+1.022 (+178 %), 2012: -6 %, RI-p=0.14, placebo-β i [-0.27, +0.28]
log enhetsverdi (kr/kg)    Hard/halvhard ost  β=+0.114 (+12 %), 2012: +2 %, RI-p=0.43, placebo-β i [-0.12, +0.12]
log enhetsverdi (kr/kg)    Revet ost          β=-0.033 (-3 %), 2012: +4 %, RI-p=0.71, placebo-β i [-0.12, +0.12]
log enhetsverdi (kr/kg)    Smelteost          β=-0.274 (-24 %), 2012: +12 %, RI-p=0.14, placebo-β i [-0.12, +0.12]

## 2. Land-DiD: eksponering = 1 − navngitt andel (navngitt import 2013 / hard ost 2010–11)
  IT: hard ost 2010–11     329 t, navngitt 2013    388 t, eksponering 0.00 (alt. 0.10)
  ES: hard ost 2010–11      75 t, navngitt 2013     92 t, eksponering 0.00 (alt. 0.21)
  CH: hard ost 2010–11      39 t, navngitt 2013     34 t, eksponering 0.15 (alt. 0.32)
  FR: hard ost 2010–11     318 t, navngitt 2013    113 t, eksponering 0.64 (alt. 0.70)
  GB: hard ost 2010–11     411 t, navngitt 2013     32 t, eksponering 0.92 (alt. 0.93)
  DK: hard ost 2010–11     488 t, navngitt 2013     19 t, eksponering 0.96 (alt. 0.97)
  NL: hard ost 2010–11     247 t, navngitt 2013      8 t, eksponering 0.97 (alt. 0.98)
  SE: hard ost 2010–11      71 t, navngitt 2013      2 t, eksponering 0.98 (alt. 0.95)
  DE: hard ost 2010–11     181 t, navngitt 2013      0 t, eksponering 1.00 (alt. 1.00)
  EE: hard ost 2010–11      86 t, navngitt 2013      0 t, eksponering 1.00 (alt. 1.00)
Jackknife (PPML, ett land utelatt): uten CH: -55 %, uten DE: -57 %, uten DK: -56 %, uten EE: -52 %, uten ES: -54 %, uten FR: -55 %, uten GB: -48 %, uten IT: -54 %, uten NL: -62 %, uten SE: -55 %
PPML, mengde (kg)                                β=-0.794 (SE 0.235) → -55 % ved full eksponering; klynge-p=0.001, RI-p=0.059; 2012: +15 %
PPML, mengde, eksponering målt 2013–14 (endogen) β=-0.895 (SE 0.268) → -59 % ved full eksponering; klynge-p=0.001; 2012: +19 %
OLS log mengde                                   β=-1.184 (SE 0.511) → -69 % ved full eksponering; klynge-p=0.021, WCB-p=0.071; 2012: -18 %
OLS log mengde, vektet                           β=-0.947 (SE 0.304) → -61 % ved full eksponering; klynge-p=0.002, WCB-p=0.089; 2012: +10 %
OLS log enhetsverdi                              β=+0.105 (SE 0.098) → +11 % ved full eksponering; klynge-p=0.283, WCB-p=0.334; 2012: +4 %
OLS log enhetsverdi, vektet                      β=+0.123 (SE 0.107) → +13 % ved full eksponering; klynge-p=0.253, WCB-p=0.306; 2012: +6 %
PPML, mengde, landspesifikke trender             β=-0.522 (SE 0.144) → -41 % ved full eksponering; klynge-p=0.000; 2012: +31 %
PPML, mengde, uten 2012                          β=-0.795 (SE 0.235) → -55 % ved full eksponering; klynge-p=0.001

Felles test av førperiode-koeffisienter (2008–2010) i landhendelsesstudien: χ²=7.23, p=0.065 (få klynger: tolk med forsiktighet)

## 3. Sammensetning etter reformen
Navngitt andel av hard ost (kg): 30.3% (2013) → 33.8% (2019) → 35.9% (2021)
Årlig vekst 2013–2019: navngitte 7.6 %, annen hard ost 4.8 %, sveitsiske navngitte (≈ Gruyère/Appenzeller) 2.9 %

## 4. Antisipasjon og omklassifisering
Vekst jan–sep 2012 mot 2011: +17.5 %. Vekst okt–des 2012: +21.4 %
Overskuddsimport okt–des 2012 utover trend: 28 tonn; avvik fra trend jan–mar 2013: -194 tonn
Smelteost, gj.snitt per måned: 2011–2012 28 t, jan–apr 2013 21 t, mai 2013–des 2014 76 t

## 5. KPI ost relativt til KPI matvarer (log-diff ×100), nivåskift fra jan 2013
2008–2019: +1.36 (HAC-SE 2.00, p=0.50)
2010–2015: -0.49 (HAC-SE 1.57, p=0.75)

## 6. Egenpriselastisitet for import av annen hard ost (Wald: PPML-β / Δln pris)
  andel innenfor kvote 0.00: Δln P = 0.94, ε = -0.84 (95 % KI -1.33 til -0.35)
  andel innenfor kvote 0.25: Δln P = 0.82, ε = -0.96 (95 % KI -1.52 til -0.41)
  andel innenfor kvote 0.50: Δln P = 0.66, ε = -1.20 (95 % KI -1.90 til -0.51)
  andel innenfor kvote 0.75: Δln P = 0.42, ε = -1.91 (95 % KI -3.02 til -0.80)

## 7. Norsk mot importert ost (Armington)
Import av ost (SSB): 2024 20041 t, 2025 20693 t (Landbruksdirektoratet: 20 041 t og 20 683 t; avviket i 2025 skyldes trolig revisjoner)
Hoppet over: manuelt_norsk_ost.csv har 1 år med norsk ost (minst 10 trengs). Fyll inn fra Landbruksdirektoratets Markedsrapport.

