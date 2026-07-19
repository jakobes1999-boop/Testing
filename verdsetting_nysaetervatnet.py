"""Verdsetting av intensjonsavtalen om sommervannstand i Nysætervatnet.

Kilder for parametere:
- NVE via Sykkylven kommunes brev til NVE 29.06.2026 (PS-41/26): Fausa II,
  brutto fallhøyde 330 m, 7 MW, middel årsproduksjon 40,5 GWh, slukeevne 2,5 m3/s,
  konsesjon 8. mai 1952 (reg.nr. 151).
- Wikipedia/NVE: Nysætervatnet areal 2,36 km2, magasinvolum 15,6 mill. m3,
  reguleringshøyde 11 m.
- NRK 27.05.2026: intensjonsavtale Sykkylven kommune-Tussa: maks 1,5 m
  nedtapping om sommeren; vinteren 2025/26 tappet 5,5 m; konsesjonen tillater
  det dobbelte.
- Brukers figur (NN2000): HRV/dam fullt 337,63 m, avtalegrense 336,12 m,
  observert bunn vår 2026 ca. 331,5 m; NO3-pris 19 ore/kWh for kabelen
  (26.09.2025), 113 ore/kWh etter; vinterpriser Q1-2026 ca. 150-200 ore.
- R-109/21: kalkulasjonsrente 4 % (forste 40 ar).
"""

# ------------------------- Fysiske parametere -------------------------
HRV = 337.63            # m NN2000, dam fullt
AVTALE_M = 1.5          # maks sommernedtapping etter intensjonsavtalen (m)
REG_HOYDE = 11.0        # total reguleringshoyde etter konsesjon (m)
AREAL_HRV = 2.36e6      # m2 ved HRV
MAG_VOL = 15.6e6        # m3 totalt magasinvolum over 11 m

FALL = 330.0            # m brutto fall Fausa II
ETA = 0.85              # totalvirkningsgrad inkl. falltap (antakelse, 0.80-0.88)
RHO_G = 9.81 * 1000     # N/m3

AARSPROD = 40.5         # GWh middel arsproduksjon (NVE)

# Lineaer hypsometri: A(d) = A0 - k*d, kalibrert mot totalt magasinvolum
A0 = AREAL_HRV
k = 2 * (A0 * REG_HOYDE - MAG_VOL) / REG_HOYDE**2  # m2 per m nedtapping

def volum(d1, d2):
    """Vann (m3) mellom nedtappingsdybde d1 og d2 under HRV."""
    return A0 * (d2 - d1) - k * (d2**2 - d1**2) / 2

def energi_gwh(d1, d2):
    """Energi (GWh) i vannet mellom d1 og d2, med falltapskorrigert hoyde."""
    d_mid = (d1 + d2) / 2
    fall_eff = FALL - d_mid          # senket vannstand gir lavere fall
    v = volum(d1, d2)
    joule = v * RHO_G * fall_eff * ETA
    return joule / 3.6e12            # J -> GWh

kwh_per_m3 = RHO_G * FALL * ETA / 3.6e6
print(f"Hypsometri: areal HRV {A0/1e6:.2f} km2, areal LRV {(A0-k*11)/1e6:.2f} km2")
print(f"Energiekvivalent ved fullt magasin: {kwh_per_m3:.2f} kWh/m3")
print(f"Kontroll totalvolum: {volum(0,11)/1e6:.1f} mill m3 (fasit 15,6)")
print()

# ------------------------- Vannmengder og energi -------------------------
v_sommerlager = volum(0, AVTALE_M)          # tillatt etter avtalen
v_beskyttet   = volum(AVTALE_M, REG_HOYDE)  # bandet avtalen verner
e_beskyttet   = energi_gwh(AVTALE_M, REG_HOYDE)

for d_obs, navn in [(5.5, "medieomtalt 5,5 m"), (6.1, "figur ca. 331,5 -> 6,1 m")]:
    v_mer = volum(AVTALE_M, d_obs)
    e_mer = energi_gwh(AVTALE_M, d_obs)
    print(f"Mertapping 1,5->{d_obs} m ({navn}): {v_mer/1e6:.1f} mill m3 = {e_mer:.1f} GWh"
          f" ({e_mer/AARSPROD*100:.0f} % av arsproduksjonen)")

print(f"Tillatt sommerlager 0->1,5 m: {v_sommerlager/1e6:.1f} mill m3")
print(f"Hele beskyttet band 1,5->11 m: {v_beskyttet/1e6:.1f} mill m3 = {e_beskyttet:.1f} GWh")
print()

# ------------------------- Priser (NO3, brukers figur) -------------------------
P_FOR = 0.19        # kr/kWh for kabelen
P_ETTER = 1.13      # kr/kWh snitt etter kabelen
P_VINTER = 1.60     # kr/kWh typisk Q1-2026 (figur 150-200 ore)
P_SOMMER_E = 1.00   # kr/kWh antatt sommer/hostpris etter kabelen (figur Q2-26)

E_MER = energi_gwh(AVTALE_M, 5.5)   # sentralt: 5,5 m som omtalt

print("=== 1) Hendelsesverdi vinteren 2025/26 (mertapping 1,5->5,5 m) ===")
brutto = E_MER * 1e6 * P_ETTER  # kWh * kr/kWh -> kr; GWh*1e6 = 1000*MWh... NB
# 1 GWh = 1e6 kWh * 1000? Nei: 1 GWh = 1e9 Wh = 1e6 kWh. OK.
print(f"Energi: {E_MER:.1f} GWh")
print(f"Bruttoverdi til snittpris etter kabel (113 ore): {E_MER*1e6*P_ETTER/1e6:.1f} MNOK")
print(f"Meirverdi vs. aa produsere samme vann til sommerpris (160-100 ore): "
      f"{E_MER*1e6*(P_VINTER-P_SOMMER_E)/1e6:.1f} MNOK")
print(f"Meirverdi hvis alternativet var forkabel-prisniva (113-19 ore): "
      f"{E_MER*1e6*(P_ETTER-P_FOR)/1e6:.1f} MNOK")
print(f"Ovre grense - vann som ellers ville gaatt til flomtap (113 ore): "
      f"{E_MER*1e6*P_ETTER/1e6:.1f} MNOK")
print()

# ------------------------- 2) Aarlig opsjonsverdi -------------------------
print("=== 2) [HISTORISK - erstattet av seksjon 8/9] Aarlig opsjonsverdi ===")
# For kabelen: sesongspread ~10-15 ore, dyp tapping aktuelt ~1 av 3 aar
for navn, spread, sanns, e in [
    ("For kabelen (19 ore-regime)", 0.125, 1/3, E_MER),
    ("Etter kabelen, lavt (spread 40 ore, 50% av aar)", 0.40, 0.5, E_MER),
    ("Etter kabelen, sentralt (spread 60 ore, 75% av aar)", 0.60, 0.75, E_MER),
    ("Etter kabelen, hoyt (spread 80 ore, hvert aar, full dybde)", 0.80, 1.0, e_beskyttet),
]:
    aarlig = e * 1e6 * spread * sanns / 1e6
    print(f"{navn}: {aarlig:.1f} MNOK/aar")
print()

# ------------------------- 3) Naaverdi (R-109/21) -------------------------
r = 0.04
T = 40
ann = (1 - (1 + r) ** -T) / r
print(f"=== 3) [HISTORISK - erstattet av seksjon 8/9] Kapitalisert verdi (faktor {ann:.2f}) ===")
for navn, aarlig in [("For kabelen", 0.24), ("Etter kabelen, lavt", 1.1),
                     ("Etter kabelen, sentralt", 2.5), ("Etter kabelen, hoyt", 7.3)]:
    print(f"{navn}: {aarlig:.1f} MNOK/aar -> naaverdi {aarlig*ann:.0f} MNOK")
print()

# ------------------------- 4) Hva avtalen beskytter -------------------------
print("=== 4) Illustrasjon: verneverdien for hytteeiere (kapitalisert) ===")
N_HYTTER = 700
for verdi, andel in [(3.0, 0.03), (3.0, 0.05), (3.0, 0.08)]:
    print(f"{N_HYTTER} hytter x {verdi:.1f} MNOK x {andel*100:.0f} % amenity-verdi: "
          f"{N_HYTTER*verdi*andel:.0f} MNOK")

# ------------------------- 5) Konsesjonsverdi og windfall -------------------------
# Verifisert mot: Tussa aarsrapport 2023 (fusjon vedtatt 27.01.2023, Ampere Finans,
# konsern-EK ca. 4,3 mrd kr, Stranda kommune 3,6 %), KT-melding 21.04.2023.
# Grunnrenteskatt: generatorytelse 5,0+3,5+0,85 = 9,35 MVA < 10 MVA -> fritatt.
# Konsesjonskraft: inntil 10 % av kraftgrunnlaget til om lag sjoelvkost (~13 oere).
print("=== 5) Konsesjonsverdi for Tussa (etter skatt, 40 aar / evig) ===")
PROD, OPEX, ESKATT, SKATT = 40.5e6, 0.10, 1.0e6, 0.22
ann40, evig = (1 - 1.04 ** -40) / 0.04, 1 / 0.04
for navn, P in [("44 oere (fusjonsregimet, NO3-snitt 2023)", 0.44),
                ("80 oere (etter kobling, forsiktig)", 0.80),
                ("113 oere (etter kobling, observert snitt)", 1.13)]:
    kk = 0.10 * PROD * max(P - 0.13, 0)
    cf = (PROD * (P - OPEX) - ESKATT - kk) * (1 - SKATT)
    print(f"{navn}: {cf*ann40/1e6:.0f} MNOK ({cf*evig/1e6:.0f} evig)")

print()
print("=== 6) Fusjonsoppgjoer og fordeling av windfall ===")
print(f"Stranda kommunes oppgjoer: 3,6 % x 4,3 mrd = {0.036*4300:.0f} MNOK (hele holdingselskapet)")
for P in (0.80, 1.13):
    up = 0.90 * PROD * (P - 0.44) * (1 - SKATT) * ann40
    print(f"Windfall Fausa ved {P*100:.0f} oere: {up/1e6:.0f} MNOK; Strandas 3,6 %: {0.036*up/1e6:.0f} MNOK")

# ------------------------- 7) Robusthetsbaand (foersteprinsipp-revisjon) ---------
# Energiekvivalent 0,72-0,81 kWh/m3 (eta 0,80-0,90). Massebalanse-kontroll:
# 40,5 GWh / 0,76 = 53 mill m3/aar tilsig-behov; slukeevne 2,5 m3/s = 79 mill m3/aar;
# nedboerfelt 31-40 km2 x 1,3-1,7 m avrenning = 40-68 mill m3/aar -> konsistent.
# Hypsometri-baand for mertapping 1,5->5,5 m: lineaer 7,0 / kvadratisk 7,7 /
# konstant areal 9,4 mill m3 -> 5,0-7,5 GWh; lineaer antakelse er konservativ.

# ------------------------- 8) Reberegning etter raadets kritikk -------------------
# Konsistent verdistruktur (metodikerens innvending: hendelsesgevinst og avtale-
# kostnad maa bygge paa samme logikk). Vannet gaar ikke tapt - verdien av aa tappe
# dypt er (i) full kraftverdi for andelen alfa som ellers ville gaatt i flomtap
# ved vaarflom (slukeevne 2,5 m3/s << flomtilsig), og (ii) prisdifferansen
# vinter/senere for resten som bare flyttes i tid.
print("=== 8) Reberegnede verdier (konsistent modell) ===")
ANN = (1 - 1.04 ** -40) / 0.04

def hendelsesverdi(E_gwh, alfa, p_vinter, p_senere):
    """MNOK: E * [alfa*P_vinter + (1-alfa)*(P_vinter-P_senere)]"""
    return E_gwh * (alfa * p_vinter + (1 - alfa) * (p_vinter - p_senere))

# alfa-grunnlag: vaartilsig apr-jun ~21-27 mill m3, slukekapasitet samme periode
# ~19,7 mill m3, ekstra lagringsrom ved dyp tapping 7,1 mill m3 -> alfa ~0,2-0,6
lav  = hendelsesverdi(5.0, 0.2, 1.10, 0.80)
sen  = hendelsesverdi(5.3, 0.4, 1.15, 0.80)
hoy  = hendelsesverdi(7.5, 0.6, 1.30, 0.85)
ren_spread = hendelsesverdi(5.0, 0.0, 1.10, 0.80)  # metodikerens spesialtilfelle
print(f"Hendelsesverdi 2025/26: {lav:.1f}-{hoy:.1f} MNOK, sentralt {sen:.1f}"
      f" (rent tidsskift, alfa=0: {ren_spread:.1f})")

# Avtalekostnad = bindingssannsynlighet x hendelsesverdi i bindende aar.
# p_bind: sommerkravet binder vinterdisponeringen bare naar hoye vinterpriser
# moeter usikker gjenfylling (toerr vaar); empirisk 2 av 4 siste aar.
for navn, p, g in [("lavt", 0.30, lav), ("sentralt", 0.45, sen), ("hoyt", 0.60, hoy)]:
    print(f"Avtalekostnad {navn}: {p:.2f} x {g:.1f} = {p*g:.1f} MNOK/aar"
          f" -> naaverdi {p*g*ANN:.0f} MNOK")

# Verneverdi, marginal (to kanaler):
# K1 forventet bruksverditap: 700 hytter x p(skadet sommer) x tap per sesong,
#    der aarlig amenity-stroem = 4 % av 3-8 % av 3,0 MNOK hytteverdi.
for p_skade, tap_andel in [(0.2, 0.3), (0.3, 0.45), (0.4, 0.6)]:
    aarlig_amenity = 0.04 * 0.055 * 3.0e6          # sentralt 6 600 kr/aar
    tap = 700 * p_skade * tap_andel * aarlig_amenity
    print(f"Vern K1 (bruk): p={p_skade}, tap {tap_andel:.0%}: {tap/1e6:.2f} MNOK/aar"
          f" -> naaverdi {tap*ANN/1e6:.0f} MNOK")
# K2 kapitalisert regimerisiko: 3-8 % av hytteverdi = 60-170 MNOK (oevre anker).
print("Vern K2 (kapitalisert regimerisiko): 60-170 MNOK; sentral samlet vurdering 40-90 MNOK")

# ------------------------- 9) Korreksjoner etter ekstern verifikasjon -------------
# (i) Eierandel: Tussa aarsrapport 2023, note 26 (layout-korrigert uttrekk):
#     Stranda kommune 6,6 % eigar- og stemmeandel - IKKE 3,6 % som foerst lest.
# (ii) Konsistent horisont: R-109/21 gir 4 % (aar 0-40), 3 % (40-75), 2 % (75+).
#      Forlenget faktor for varig realstroem: 19,79 + 4,48 + 3,70 = 27,97.
# (iii) Konsistent skattebasis: eiertall etter 22 % skatt (som konsesjonsverdien).
# (iv) alfa-intervall utvidet til 0,8 hoyt: massebalansen gir alfa naer 1 ved
#      50 % vaartilsigsandel, saa 0,6 var for lavt som tak.
print("=== 9) Korrigerte hovedtall (etter skatt der eier er perspektivet) ===")
A40 = (1 - 1.04 ** -40) / 0.04
A75 = A40 + ((1 - 1.03 ** -35) / 0.03) * 1.04 ** -40
AEV = A75 + (1 / 0.02) * (1.04 ** -40) * (1.03 ** -35)
print(f"Diskonteringsfaktorer: 40 aar {A40:.2f}, 75 aar {A75:.2f}, evig {AEV:.2f}")

T = 0.22
scen = [("lavt", 5.0, 0.2, 1.10, 0.80, 0.30),
        ("sentralt", 5.3, 0.4, 1.15, 0.80, 0.45),
        ("hoyt", 7.5, 0.8, 1.30, 0.85, 0.60)]
for navn, E, a, pv, ps, pb in scen:
    G = E * (a * pv + (1 - a) * (pv - ps))          # foer skatt, MNOK
    Gt = G * (1 - T)
    aarlig = pb * Gt
    print(f"{navn}: hendelsesverdi {G:.1f} foer / {Gt:.1f} etter skatt; "
          f"avtalekostnad {aarlig:.2f}/aar -> {aarlig*A40:.0f} MNOK (40 aar) / {aarlig*AEV:.0f} (evig)")

print()
print("Vern K1 (bruksverditap, evig faktor):")
for p_sk, tap in [(0.2, 0.3), (0.3, 0.45), (0.4, 0.6)]:
    aarlig = 700 * p_sk * tap * (0.04 * 0.055 * 3.0e6) / 1e6
    print(f"  p={p_sk}, tap {tap:.0%}: {aarlig*A40:.0f} MNOK (40 aar) / {aarlig*AEV:.0f} (evig)")
print("Vern K2 (kapitalisert regimerisiko, evig av natur): 63-168 MNOK")
print("K1 og K2 er ALTERNATIVE verdsettingskanaler - aldri additive.")
print()

print("Konsesjonsverdi paa NVEs prisbane (dokumenterer notatets nedre verdier):")
PROD2, OPEX2, ESK2 = 40.5e6, 0.10, 1.0e6
for P in (0.60, 0.67, 0.80, 1.13):
    kk = 0.10 * PROD2 * (P - 0.13)
    cf = (PROD2 * (P - OPEX2) - ESK2 - kk) * (1 - T)
    print(f"  {P*100:.0f} oere: {cf*A40/1e6:.0f} MNOK (40 aar) / {cf*AEV/1e6:.0f} (evig)")
print()

print("Fusjon og fordeling, korrigert eierandel 6,6 %:")
print(f"  Stranda kommunes oppgjoer: 6,6 % x 4,3 mrd = {0.066*4300:.0f} MNOK")
for P in (0.67, 0.80, 1.13):
    up = 0.90 * PROD2 * (P - 0.44) * (1 - T) * A40
    print(f"  Windfall Fausa {P*100:.0f} oere: {up/1e6:.0f} MNOK; Strandas 6,6 %: {0.066*up/1e6:.0f} MNOK")
sentral_aarlig = 0.45 * 5.3 * (0.4*1.15 + 0.6*0.35) * (1 - T)
print(f"\nAvtalekostnad som andel av konsesjonsverdi: "
      f"{sentral_aarlig*A40/380:.1%} (40 aar/380) - {sentral_aarlig*AEV/480:.1%} (evig/480)")

# ------------------------- 10) NVE-verifiserte parametre (runde 2) ----------------
# Kilde: NVE vannkraftdatabase-API (GetHydroPowerPlantsInOperation), verifisert direkte:
# Fausa II (VannKraftverkID 81): MaksYtelse 7,0 MW; MidProd_91_20 = 40,536 GWh
# (loeser "40,5 vs 37/42": NVEs referanseproduksjon 1991-2020); BruttoFallhoyde 330 m;
# Slukeevne 2,5 m3/s; EnEkv 0,678 kWh/m3 (implisitt virkningsgrad ~75 %, UNDER vaart
# tidligere baand 0,72-0,81 -> alle energitall justeres ned ~11 %).
# Konsesjoner: KdbID 9 (overfoering Svartaaa/Auskargrova - forklarer 40 vs 31 km2
# nedboerfelt), KdbID 145 (originalkonsesjon 24. juni 1938: KUN 2 m regulering,
# manoevrering "efter Stranda Elektrisitetsverks behov", konsesjonskraft til
# selvkost + 6 % rente + 20 %), KdbID 151 (1952: ytterligere regulering til 11 m).
print("=== 10) Justerte hovedtall med NVEs energiekvivalent 0,678 kWh/m3 ===")
ENEKV = 0.678
for navn, v in [("lineaer", 7.04), ("kvadratisk", 7.74), ("konstant areal", 9.44)]:
    print(f"Mertapping 1,5->5,5 m, {navn}: {v:.2f} mill m3 = {v*ENEKV:.1f} GWh")
scen10 = [("lavt", 4.8, 0.2, 1.10, 0.80, 0.30),
          ("sentralt", 5.0, 0.4, 1.15, 0.80, 0.45),
          ("hoyt", 6.4, 0.8, 1.30, 0.85, 0.60)]
for navn, E, a, pv, ps, pb in scen10:
    G = E * (a * pv + (1 - a) * (pv - ps)); Gt = G * 0.78; aarlig = pb * Gt
    print(f"{navn}: hendelsesverdi {Gt:.1f} etter skatt; avtalekostnad "
          f"{aarlig*19.79:.0f} MNOK (40 aar) / {aarlig*27.97:.0f} (evig)")
print("-> Avtalekostnad 10-95 MNOK, sentralt 23-33; ca. 6 % av konsesjonsverdien.")
print()
print("Codex runde 2 (FORELOEPIG, proxyhydrologi - LP-magasinmodell, etter skatt):")
print("  Sommergulv 1,5 m: 20,4 / 28,8 MNOK (40 aar / forlenget R-109)")
print("  Full pakke (sommer+vinterregime): 38,5 / 54,4 MNOK; +standstill: 40,2 / 56,1")
print("  Monte Carlo: P(vern > full pakke) = 32 % (50/50 kanal); K1: 3 %; K2: 60 %")
print("  Konvergens: LP-sommergulv 20-29 vs identitetsmetoden 23-33 - konsistent.")
