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
print("=== 2) Aarlig opsjonsverdi av full fleksibilitet vs. avtalen ===")
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
print(f"=== 3) Kapitalisert verdi, 4 % rente, 40 aar (annuitetsfaktor {ann:.2f}) ===")
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
