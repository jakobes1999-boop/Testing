"""
Gruyère-unntaket og «elitistisk» osteimport: en difference-in-differences-analyse
av tollomleggingen for hard og halvhard ost 1.1.2013.

Kjør:  python3 analyse.py        (fra mappen gruyere-did/)
Krever: pandas, numpy, statsmodels, matplotlib

Rådata ligger i data/ og er dokumentert i data/README.md. Skriptet leser bare rådata,
og alle tabeller og figurer i results/ og figures/ blir laget på nytt hver gang det kjøres.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RES = ROOT / "results"
FIG = ROOT / "figures"
RES.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)

RNG = np.random.default_rng(20130101)
REFORM_YEAR = 2013
ANTICIPATION_YEAR = 2012
REF_YEAR = 2011
WINDOW = (2008, 2019)

# Tollsatser utenfor kvote (Stortingets tollvedtak for 2013)
SPECIFIC_TARIFF = 27.15  # kr/kg – før reformen for all hard ost, etter reformen for de navngitte ostene
AD_VALOREM = 2.77        # 277 % – etter reformen for annen hard/halvhard ost

# Varenumre
HARD_PRE = ["04069091_2001", "04069099_2001"]
NAMED = ["04069092_2013"]
TAXED = ["04069097_2013", "04069098_2013"]
HARD = HARD_PRE + NAMED + TAXED

PRODUCT_GROUPS = {
    "Hard/halvhard ost": HARD,
    "Fersk ost": ["04061001_2007", "04061009_2007"],
    "Blåmuggost": ["04064001_2001", "04064005_2001", "04064008_2001", "04064009_2001", "04064007_2020"],
    "Feta": ["04069030_2001"],
    "Camembert": ["04069082_2001"],
    "Brie": ["04069084_2001"],
    "Annen hvitmuggost": ["04069089_2001"],
    "Revet ost": ["04062000_1988"],
    "Smelteost": ["04063000_1988"],
}
CONTROLS = ["Fersk ost", "Blåmuggost", "Feta", "Camembert", "Brie", "Annen hvitmuggost"]
SPILLOVER = ["Revet ost", "Smelteost"]

# Diagramfarger (referansepalett fra dataviz, lys modus)
C1, C2, C3, C4 = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"

plt.rcParams.update({
    "font.size": 10, "axes.edgecolor": INK2, "axes.labelcolor": INK2, "xtick.color": INK2,
    "ytick.color": INK2, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False, "lines.linewidth": 2,
    "figure.dpi": 150, "savefig.bbox": "tight", "legend.frameon": False,
})


# --------------------------------------------------------------------------------------
# Innlesing
# --------------------------------------------------------------------------------------
def read_wide(path, idcols):
    d = pd.read_csv(path, dtype={c: str for c in idcols})
    m = d.melt(id_vars=idcols, var_name="k", value_name="v")
    m[["var", "per"]] = m["k"].str.split(" ", expand=True)
    out = m.pivot_table(index=idcols + ["per"], columns="var", values="v", aggfunc="sum").reset_index()
    out.columns.name = None
    return out


tot = read_wide(DATA / "ssb_08801_import_varenr_total.csv", ["Varekoder", "ImpEks"])
tot["year"] = tot["per"].astype(int)
land = read_wide(DATA / "ssb_08801_import_hardost_land.csv", ["Varekoder", "ImpEks", "Land"])
land["year"] = land["per"].astype(int)
mnd = read_wide(DATA / "ssb_08799_import_mnd_2011_2014.csv", ["Varekoder", "ImpEks"])
mnd["month"] = pd.PeriodIndex(mnd["per"].str.replace("M", "-"), freq="M")
kpi = pd.read_csv(DATA / "ssb_14700_kpi_ost_mat.csv")

# Kontroll: summen over landene skal dekke totalen
cov = (land.groupby(["Varekoder", "year"])["Mengde1"].sum()
       / tot.set_index(["Varekoder", "year"])["Mengde1"]).dropna()
cov = cov[np.isfinite(cov)]
assert cov.between(0.97, 1.0001).all(), "Landutvalget dekker ikke totalen"

# Kontroll: månedstall skal summere til årstall
chk = mnd.assign(year=mnd["month"].dt.year).groupby(["Varekoder", "year"])["Mengde1"].sum()
assert (chk == tot.set_index(["Varekoder", "year"]).loc[chk.index, "Mengde1"]).all()


# --------------------------------------------------------------------------------------
# Hjelpefunksjoner
# --------------------------------------------------------------------------------------
def wild_cluster_bootstrap(formula, data, coef, cluster, weights=None, B=9999):
    """Wild cluster bootstrap-t (Webb-vekter) med restriksjonen H0: coef = 0 pålagt.
    Cameron, Gelbach & Miller (2008); Webb (2023). Returnerer p-verdi."""
    def fit(d):
        if weights is None:
            return smf.ols(formula, d).fit(cov_type="cluster", cov_kwds={"groups": d[cluster]})
        return smf.wls(formula, d, weights=d[weights]).fit(cov_type="cluster", cov_kwds={"groups": d[cluster]})

    full = fit(data)
    t_obs = full.tvalues[coef]
    restricted = formula.replace(f"+ {coef}", "")
    r = (smf.ols(restricted, data) if weights is None
         else smf.wls(restricted, data, weights=data[weights])).fit()
    yhat, u = r.fittedvalues, r.resid
    y = formula.split("~")[0].strip()
    clusters = data[cluster].unique()
    webb = np.array([-np.sqrt(1.5), -1, -np.sqrt(0.5), np.sqrt(0.5), 1, np.sqrt(1.5)])
    t_star = np.empty(B)
    d = data.copy()
    for b in range(B):
        w = dict(zip(clusters, RNG.choice(webb, len(clusters))))
        d[y] = yhat + u * d[cluster].map(w)
        t_star[b] = fit(d).tvalues[coef]
    return float(np.mean(np.abs(t_star) >= abs(t_obs)))


def ppml(formula, data):
    return smf.glm(formula, data, family=sm.families.Poisson()).fit(
        cov_type="cluster", cov_kwds={"groups": data["Land"].astype("category").cat.codes})


def pct(b):
    return 100 * (np.exp(b) - 1)


lines = []  # nøkkeltall til results/nokkeltall.md


def log(s=""):
    print(s)
    lines.append(s)


# --------------------------------------------------------------------------------------
# 0. Prisvirkningen ved grensen (tollkile), basert på enhetsverdier i 2013
# --------------------------------------------------------------------------------------
t13 = tot[tot["year"] == 2013].set_index("Varekoder")
p_named = t13.loc[NAMED, "Verdi"].sum() / t13.loc[NAMED, "Mengde1"].sum()
p_taxed = t13.loc[TAXED, "Verdi"].sum() / t13.loc[TAXED, "Mengde1"].sum()
pre_rel = (p_named + SPECIFIC_TARIFF) / (p_taxed + SPECIFIC_TARIFF)
post_rel = (p_named + SPECIFIC_TARIFF) / (p_taxed * (1 + AD_VALOREM))
breakeven = SPECIFIC_TARIFF / AD_VALOREM

log("## 0. Tollkilen ved grensen (import utenfor kvote)")
log(f"Enhetsverdi 2013, navngitte oster (9092): {p_named:.1f} kr/kg")
log(f"Enhetsverdi 2013, annen hard ost (9097+9098): {p_taxed:.1f} kr/kg")
log(f"Tollbelastet pris, annen hard ost: før {p_taxed + SPECIFIC_TARIFF:.0f} kr/kg, etter {p_taxed * (1 + AD_VALOREM):.0f} kr/kg "
    f"({100 * (p_taxed * (1 + AD_VALOREM) / (p_taxed + SPECIFIC_TARIFF) - 1):.0f} %)")
log(f"Relativ pris navngitt/annen: før {pre_rel:.2f}, etter {post_rel:.2f} "
    f"(endring {100 * (post_rel / pre_rel - 1):.0f} %)")
log(f"Prosenttollen er høyere enn kronetollen for alle oster med tollverdi over {breakeven:.2f} kr/kg")
log()

# --------------------------------------------------------------------------------------
# 1. Produktpanel: hard ost mot upåvirkede ostekategorier
# --------------------------------------------------------------------------------------
rows = []
for g, codes in PRODUCT_GROUPS.items():
    s = tot[tot["Varekoder"].isin(codes)].groupby("year")[["Mengde1", "Verdi"]].sum()
    s["group"] = g
    rows.append(s.reset_index())
prod = pd.concat(rows)
prod = prod[prod["year"].between(*WINDOW)].copy()
prod["ln_kg"] = np.log(prod["Mengde1"])
prod["ln_uv"] = np.log(prod["Verdi"] / prod["Mengde1"])
prod["post"] = (prod["year"] >= REFORM_YEAR).astype(int)
prod["antic"] = (prod["year"] == ANTICIPATION_YEAR).astype(int)
prod.to_csv(RES / "panel_produkt.csv", index=False)


def product_did(df, treated, outcome):
    d = df[df["group"].isin(CONTROLS + [treated])].copy()
    d["D"] = (d["group"] == treated).astype(int) * d["post"]
    d["A"] = (d["group"] == treated).astype(int) * d["antic"]
    m = smf.ols(f"{outcome} ~ C(group) + C(year) + A + D", d).fit()
    return m.params["D"], m.params["A"]


log("## 1. Produkt-DiD: hard/halvhard ost mot seks upåvirkede ostekategorier, 2008–2019")
prod_res = []
for outcome, lab in [("ln_kg", "log mengde (kg)"), ("ln_uv", "log enhetsverdi (kr/kg)")]:
    for treated in ["Hard/halvhard ost"] + SPILLOVER:
        b, a = product_did(prod, treated, outcome)
        # Placebo-/randomiseringsinferens: hver kontrollkategori behandles som om den var «behandlet»
        plac = []
        for c in CONTROLS:
            dd = prod[prod["group"].isin(CONTROLS)].copy()
            dd["D"] = (dd["group"] == c).astype(int) * dd["post"]
            dd["A"] = (dd["group"] == c).astype(int) * dd["antic"]
            plac.append(smf.ols(f"{outcome} ~ C(group) + C(year) + A + D", dd).fit().params["D"])
        plac = np.array(plac)
        p_ri = (1 + np.sum(np.abs(plac) >= abs(b))) / (1 + len(plac))
        prod_res.append(dict(utfall=lab, behandlet=treated, beta=b, effekt_pst=pct(b),
                             antisipasjon_2012=a, antisipasjon_pst=pct(a),
                             p_randomisering=p_ri, placebo_min=plac.min(), placebo_max=plac.max()))
        log(f"{lab:26s} {treated:18s} β={b:+.3f} ({pct(b):+.0f} %), 2012: {pct(a):+.0f} %, "
            f"RI-p={p_ri:.2f}, placebo-β i [{plac.min():+.2f}, {plac.max():+.2f}]")
pd.DataFrame(prod_res).to_csv(RES / "did_produkt.csv", index=False)
log()

# Hendelsesstudie for produktpanelet
d = prod[prod["group"].isin(CONTROLS + ["Hard/halvhard ost"])].copy()
d["T"] = (d["group"] == "Hard/halvhard ost").astype(int)
years = [y for y in range(WINDOW[0], WINDOW[1] + 1) if y != REF_YEAR]
for y in years:
    d[f"T_{y}"] = d["T"] * (d["year"] == y)
es_prod = smf.ols("ln_kg ~ C(group) + C(year) + " + " + ".join(f"T_{y}" for y in years), d).fit()
es_prod_coef = pd.Series({y: es_prod.params[f"T_{y}"] for y in years})
es_prod_coef[REF_YEAR] = 0.0
es_prod_coef = es_prod_coef.sort_index()

# --------------------------------------------------------------------------------------
# 2. Landpanel: eksponering for 277 %-tollen etter opprinnelsesland
# --------------------------------------------------------------------------------------
hard_c = land[land["Varekoder"].isin(HARD)].groupby(["Land", "year"])[["Mengde1", "Verdi"]].sum().reset_index()
named_c = land[land["Varekoder"].isin(NAMED)].groupby(["Land", "year"])["Mengde1"].sum().unstack()
pre_mean = hard_c[hard_c["year"].between(2008, 2011)].groupby("Land")["Mengde1"].mean()
base = hard_c[hard_c["year"].between(2010, 2011)].groupby("Land")["Mengde1"].mean()
sample = pre_mean[pre_mean >= 20_000].index.tolist()

expo = pd.DataFrame({
    "import_hard_2010_11_kg": base.reindex(sample),
    "navngitt_2013_kg": named_c[2013].reindex(sample).fillna(0),
})
expo["navngitt_andel"] = (expo["navngitt_2013_kg"] / expo["import_hard_2010_11_kg"]).clip(upper=1)
expo["eksponering"] = 1 - expo["navngitt_andel"]
# Alternativt mål (etter reformen, endogent): navngitt andel av hard ost i 2013–2014
h1314 = hard_c[hard_c["year"].isin([2013, 2014])].groupby("Land")["Mengde1"].sum()
n1314 = named_c[[2013, 2014]].sum(axis=1)
expo["eksponering_alt"] = 1 - (n1314 / h1314).reindex(sample).fillna(0)
expo = expo.sort_values("eksponering")
expo.to_csv(RES / "eksponering_land.csv")

cp = hard_c[hard_c["Land"].isin(sample) & hard_c["year"].between(*WINDOW)].copy()
cp = cp.merge(expo[["eksponering", "eksponering_alt", "import_hard_2010_11_kg"]], left_on="Land", right_index=True)
cp["post"] = (cp["year"] >= REFORM_YEAR).astype(int)
cp["antic"] = (cp["year"] == ANTICIPATION_YEAR).astype(int)
cp["ExP"] = cp["eksponering"] * cp["post"]
cp["ExA"] = cp["eksponering"] * cp["antic"]
cp["ExP_alt"] = cp["eksponering_alt"] * cp["post"]
cp["ExA_alt"] = cp["eksponering_alt"] * cp["antic"]
cp["kg"] = cp["Mengde1"]
cp["w"] = cp["import_hard_2010_11_kg"] / cp["import_hard_2010_11_kg"].mean()
cp.to_csv(RES / "panel_land.csv", index=False)

log("## 2. Land-DiD: eksponering = 1 − navngitt andel (navngitt import 2013 / hard ost 2010–11)")
for c, r in expo.iterrows():
    log(f"  {c}: hard ost 2010–11 {r.import_hard_2010_11_kg / 1000:7.0f} t, navngitt 2013 "
        f"{r.navngitt_2013_kg / 1000:6.0f} t, eksponering {r.eksponering:.2f} (alt. {r.eksponering_alt:.2f})")

country_res = []
m_ppml = ppml("kg ~ C(Land) + C(year) + ExA + ExP", cp)
# Randomiseringsinferens: permuter eksponering mellom land
ri = []
for _ in range(2000):
    perm = dict(zip(sample, RNG.permutation(expo.loc[sample, "eksponering"].values)))
    dd = cp.copy()
    e = dd["Land"].map(perm)
    dd["ExP"], dd["ExA"] = e * dd["post"], e * dd["antic"]
    ri.append(ppml("kg ~ C(Land) + C(year) + ExA + ExP", dd).params["ExP"])
ri = np.array(ri)
p_ri = np.mean(np.abs(ri) >= abs(m_ppml.params["ExP"]))
country_res.append(dict(modell="PPML, mengde (kg)", beta=m_ppml.params["ExP"], se_cluster=m_ppml.bse["ExP"],
                        effekt_pst=pct(m_ppml.params["ExP"]), p_cluster=m_ppml.pvalues["ExP"], p_ri=p_ri,
                        antisipasjon_pst=pct(m_ppml.params["ExA"])))

m_ppml_alt = ppml("kg ~ C(Land) + C(year) + ExA_alt + ExP_alt", cp)
country_res.append(dict(modell="PPML, mengde, eksponering målt 2013–14 (endogen)", beta=m_ppml_alt.params["ExP_alt"],
                        se_cluster=m_ppml_alt.bse["ExP_alt"], effekt_pst=pct(m_ppml_alt.params["ExP_alt"]),
                        p_cluster=m_ppml_alt.pvalues["ExP_alt"], p_ri=np.nan,
                        antisipasjon_pst=pct(m_ppml_alt.params["ExA_alt"])))

pos = cp[cp["kg"] > 0].copy()
pos["ln_kg"] = np.log(pos["kg"])
pos["ln_uv"] = np.log(pos["Verdi"] / pos["kg"])
for outcome, lab in [("ln_kg", "OLS log mengde"), ("ln_uv", "OLS log enhetsverdi")]:
    for wt in [None, "w"]:
        f = f"{outcome} ~ C(Land) + C(year) + ExA + ExP"
        m = (smf.ols(f, pos) if wt is None else smf.wls(f, pos, weights=pos[wt])).fit(
            cov_type="cluster", cov_kwds={"groups": pos["Land"]})
        p_wcb = wild_cluster_bootstrap(f, pos, "ExP", "Land", weights=wt, B=1999)
        country_res.append(dict(modell=f"{lab}{', vektet' if wt else ''}", beta=m.params["ExP"],
                                se_cluster=m.bse["ExP"], effekt_pst=pct(m.params["ExP"]),
                                p_cluster=m.pvalues["ExP"], p_wcb=p_wcb, antisipasjon_pst=pct(m.params["ExA"])))
# Robusthet: landspesifikke lineære trender og «ett land utelatt» (jackknife)
cp["trend"] = cp["year"] - REF_YEAR
m_tr = ppml("kg ~ C(Land) + C(year) + C(Land):trend + ExA + ExP", cp)
country_res.append(dict(modell="PPML, mengde, landspesifikke trender", beta=m_tr.params["ExP"],
                        se_cluster=m_tr.bse["ExP"], effekt_pst=pct(m_tr.params["ExP"]),
                        p_cluster=m_tr.pvalues["ExP"], antisipasjon_pst=pct(m_tr.params["ExA"])))
m_nb = ppml("kg ~ C(Land) + C(year) + ExP", cp[cp["year"] != ANTICIPATION_YEAR])
country_res.append(dict(modell="PPML, mengde, uten 2012", beta=m_nb.params["ExP"],
                        se_cluster=m_nb.bse["ExP"], effekt_pst=pct(m_nb.params["ExP"]),
                        p_cluster=m_nb.pvalues["ExP"]))
jk = {c: ppml("kg ~ C(Land) + C(year) + ExA + ExP", cp[cp["Land"] != c]).params["ExP"] for c in sample}
pd.Series(jk, name="beta_uten_land").to_csv(RES / "jackknife_land.csv")
log("Jackknife (PPML, ett land utelatt): " + ", ".join(f"uten {c}: {pct(b):+.0f} %" for c, b in jk.items()))
country_res = pd.DataFrame(country_res)
country_res.to_csv(RES / "did_land.csv", index=False)
for _, r in country_res.iterrows():
    extra = f", RI-p={r.p_ri:.3f}" if pd.notna(r.get("p_ri")) else ""
    extra += f", WCB-p={r.p_wcb:.3f}" if pd.notna(r.get("p_wcb")) else ""
    log(f"{r.modell:48s} β={r.beta:+.3f} (SE {r.se_cluster:.3f}) → {r.effekt_pst:+.0f} % ved full eksponering; "
        f"klynge-p={r.p_cluster:.3f}{extra}" + (f"; 2012: {r.antisipasjon_pst:+.0f} %" if pd.notna(r.antisipasjon_pst) else ""))
log()

# Hendelsesstudie, PPML
for y in years:
    cp[f"E_{y}"] = cp["eksponering"] * (cp["year"] == y)
es_c = ppml("kg ~ C(Land) + C(year) + " + " + ".join(f"E_{y}" for y in years), cp)
es_c_coef = pd.DataFrame({"b": [es_c.params[f"E_{y}"] for y in years],
                          "se": [es_c.bse[f"E_{y}"] for y in years]}, index=years)
es_c_coef.loc[REF_YEAR] = [0.0, 0.0]
es_c_coef = es_c_coef.sort_index()
es_c_coef.to_csv(RES / "hendelsesstudie_land.csv")
pre_test = es_c.wald_test(" , ".join(f"E_{y} = 0" for y in [2008, 2009, 2010]), scalar=True)
log(f"Felles test av førperiode-koeffisienter (2008–2010) i landhendelsesstudien: "
    f"χ²={pre_test.statistic:.2f}, p={pre_test.pvalue:.3f} (få klynger: tolk med forsiktighet)")
log()

# --------------------------------------------------------------------------------------
# 3. Sammensetning etter reformen: andelen «elitisk» ost
# --------------------------------------------------------------------------------------
comp = tot[tot["Varekoder"].isin(NAMED + TAXED) & tot["year"].between(2013, 2021)]
comp = comp.assign(kat=np.where(comp["Varekoder"].isin(NAMED), "navngitt", "annen")).groupby(
    ["year", "kat"])[["Mengde1", "Verdi"]].sum().unstack()
share = pd.DataFrame({
    "navngitt_tonn": comp[("Mengde1", "navngitt")] / 1000,
    "annen_tonn": comp[("Mengde1", "annen")] / 1000,
    "navngitt_andel_kg": comp[("Mengde1", "navngitt")] / comp["Mengde1"].sum(axis=1),
    "navngitt_andel_verdi": comp[("Verdi", "navngitt")] / comp["Verdi"].sum(axis=1),
    "enhetsverdi_navngitt": comp[("Verdi", "navngitt")] / comp[("Mengde1", "navngitt")],
    "enhetsverdi_annen": comp[("Verdi", "annen")] / comp[("Mengde1", "annen")],
})
ch = land[land["Varekoder"].isin(NAMED) & (land["Land"] == "CH")].set_index("year")["Mengde1"]
share["sveits_navngitt_tonn"] = ch.reindex(share.index) / 1000
share.to_csv(RES / "sammensetning_2013_2021.csv")
g = lambda s: 100 * ((s.loc[2019] / s.loc[2013]) ** (1 / 6) - 1)
log("## 3. Sammensetning etter reformen")
log(f"Navngitt andel av hard ost (kg): {share.navngitt_andel_kg.loc[2013]:.1%} (2013) → "
    f"{share.navngitt_andel_kg.loc[2019]:.1%} (2019) → {share.navngitt_andel_kg.loc[2021]:.1%} (2021)")
log(f"Årlig vekst 2013–2019: navngitte {g(share.navngitt_tonn):.1f} %, annen hard ost {g(share.annen_tonn):.1f} %, "
    f"sveitsiske navngitte (≈ Gruyère/Appenzeller) {g(share.sveits_navngitt_tonn):.1f} %")
log()

# --------------------------------------------------------------------------------------
# 4. Antisipasjon (hamstring) høsten 2012 og omklassifisering til smelteost
# --------------------------------------------------------------------------------------
mm = mnd.copy()
mm["kat"] = np.where(mm["Varekoder"] == "04063000_1988", "Smelteost", "Hard/halvhard ost")
mm = mm.groupby(["month", "kat"])["Mengde1"].sum().unstack()
mm.index = mm.index.to_timestamp()
mm.to_csv(RES / "maned_2011_2014.csv")
h = mm["Hard/halvhard ost"]
yoy = h.loc["2012"].values / h.loc["2011"].values - 1
base_growth = h.loc["2012-01":"2012-09"].sum() / h.loc["2011-01":"2011-09"].sum() - 1
excess = (h.loc["2012-10":"2012-12"].values - h.loc["2011-10":"2011-12"].values * (1 + base_growth)).sum()
deficit = (h.loc["2013-01":"2013-03"].values - h.loc["2012-01":"2012-03"].values * (1 + base_growth)).sum()
log("## 4. Antisipasjon og omklassifisering")
log(f"Vekst jan–sep 2012 mot 2011: {100 * base_growth:+.1f} %. Vekst okt–des 2012: "
    f"{100 * (h.loc['2012-10':'2012-12'].sum() / h.loc['2011-10':'2011-12'].sum() - 1):+.1f} %")
log(f"Overskuddsimport okt–des 2012 utover trend: {excess / 1000:.0f} tonn; "
    f"avvik fra trend jan–mar 2013: {deficit / 1000:.0f} tonn")
s = mm["Smelteost"]
log(f"Smelteost, gj.snitt per måned: 2011–2012 {s.loc['2011':'2012'].mean() / 1000:.0f} t, "
    f"jan–apr 2013 {s.loc['2013-01':'2013-04'].mean() / 1000:.0f} t, "
    f"mai 2013–des 2014 {s.loc['2013-05':'2014-12'].mean() / 1000:.0f} t")
log()

# --------------------------------------------------------------------------------------
# 5. Konsumpris: KPI ost relativt til KPI matvarer (avbrutt tidsserie)
# --------------------------------------------------------------------------------------
k = kpi.pivot(index="maned", columns="gruppe", values="kpi_2025eq100")
k.index = pd.PeriodIndex(k.index, freq="M")
kd = pd.DataFrame({"rel": 100 * np.log(k["01.1.4.5"] / k["01.1"])})
kd["t"] = np.arange(len(kd))
kd["post"] = (kd.index.year >= REFORM_YEAR).astype(int)
kd["mnd"] = kd.index.month
its = smf.ols("rel ~ t + C(mnd) + post", kd).fit(cov_type="HAC", cov_kwds={"maxlags": 12})
its_short = smf.ols("rel ~ t + C(mnd) + post", kd[(kd.index.year >= 2010) & (kd.index.year <= 2015)]).fit(
    cov_type="HAC", cov_kwds={"maxlags": 12})
log("## 5. KPI ost relativt til KPI matvarer (log-diff ×100), nivåskift fra jan 2013")
log(f"2008–2019: {its.params['post']:+.2f} (HAC-SE {its.bse['post']:.2f}, p={its.pvalues['post']:.2f})")
log(f"2010–2015: {its_short.params['post']:+.2f} (HAC-SE {its_short.bse['post']:.2f}, p={its_short.pvalues['post']:.2f})")
log()

(RES / "nokkeltall.md").write_text("# Nøkkeltall (generert av analyse.py)\n\n" + "\n".join(lines) + "\n")

# --------------------------------------------------------------------------------------
# Figurer
# --------------------------------------------------------------------------------------
def reform_line(ax, x=2012.5):
    ax.axvline(x, color=INK2, lw=1, ls="--")
    ax.text(x + 0.1, ax.get_ylim()[0], " 277 % fra 1.1.2013", va="bottom", ha="left", color=INK2, fontsize=8)


# Figur 1: indekserte importvolumer
fig, ax = plt.subplots(figsize=(7, 4))
idx = prod.pivot(index="year", columns="group", values="Mengde1")
idx = 100 * idx / idx.loc[REF_YEAR]
ctrl = np.exp(np.log(idx[CONTROLS]).mean(axis=1))
ax.plot(idx.index, idx["Hard/halvhard ost"], color=C1, marker="o", ms=4, label="Hard/halvhard ost (behandlet)")
ax.plot(idx.index, ctrl, color=C2, marker="o", ms=4, label="Upåvirkede oster (geom. snitt av 6)")
ax.plot(idx.index, idx["Smelteost"], color=C3, marker="o", ms=4, label="Smelteost (mulig omklassifisering)")
ax.set_ylabel("Importvolum, indeks 2011 = 100")
ax.set_title("Figur 1. Importvolum etter ostekategori", loc="left", color=INK)
reform_line(ax)
ax.legend(loc="upper left")
fig.savefig(FIG / "fig1_volum_indeks.png")
plt.close(fig)

# Figur 2: hendelsesstudier
fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), sharey=False)
ax = axes[0]
ax.axhline(0, color=INK2, lw=0.8)
ax.plot(es_prod_coef.index, es_prod_coef.values, color=C1, marker="o", ms=5)
ax.set_title("A. Produkt-DiD: hard ost mot kontrolloster", loc="left", color=INK, fontsize=10)
ax.set_ylabel("Koeffisient (log-poeng), 2011 = 0")
reform_line(ax)
ax = axes[1]
ax.axhline(0, color=INK2, lw=0.8)
ax.fill_between(es_c_coef.index, es_c_coef.b - 1.96 * es_c_coef.se, es_c_coef.b + 1.96 * es_c_coef.se,
                color=C1, alpha=0.15, lw=0)
ax.plot(es_c_coef.index, es_c_coef.b, color=C1, marker="o", ms=5)
ax.set_title("B. Land-DiD (PPML): eksponering × år", loc="left", color=INK, fontsize=10)
reform_line(ax)
fig.suptitle("Figur 2. Hendelsesstudier", x=0.06, ha="left", color=INK)
fig.savefig(FIG / "fig2_hendelsesstudier.png")
plt.close(fig)

# Figur 3: eksponering mot endring i import
chg = cp.groupby(["Land", cp["year"].between(2014, 2016)])["kg"].sum().unstack()
pre = cp[cp["year"].between(2010, 2011)].groupby("Land")["kg"].mean()
post = cp[cp["year"].between(2014, 2016)].groupby("Land")["kg"].mean()
dl = 100 * np.log(post / pre)
fig, ax = plt.subplots(figsize=(6.5, 4))
ax.axhline(0, color=INK2, lw=0.8)
sizes = 20 + 400 * expo["import_hard_2010_11_kg"] / expo["import_hard_2010_11_kg"].max()
ax.scatter(expo["eksponering"], dl.reindex(expo.index), s=sizes, color=C1, edgecolor="white", linewidth=1.5, zorder=3)
offsets = {"IT": (8, 6), "ES": (8, -12)}
for c in expo.index:
    ax.annotate(c, (expo.loc[c, "eksponering"], dl[c]), xytext=offsets.get(c, (6, 4)),
                textcoords="offset points", color=INK, fontsize=9)
ax.set_xlabel("Eksponering for 277 %-tollen (1 − navngitt andel)")
ax.set_ylabel("Endring i import av hard ost, log-poeng ×100\n(snitt 2014–16 mot 2010–11)")
ax.set_title("Figur 3. Opprinnelsesland: eksponering og importendring", loc="left", color=INK)
fig.savefig(FIG / "fig3_eksponering_land.png")
plt.close(fig)

# Figur 4: sammensetning etter reformen
fig, ax = plt.subplots(figsize=(7, 3.8))
ax.plot(share.index, 100 * share["navngitt_andel_kg"], color=C1, marker="o", ms=4, label="Andel av mengde (kg)")
ax.plot(share.index, 100 * share["navngitt_andel_verdi"], color=C2, marker="o", ms=4, label="Andel av verdi (kr)")
ax.set_ylabel("Prosent av import av hard/halvhard ost")
ax.set_title("Figur 4. De 14 navngitte ostenes andel av importen av hard ost, 2013–2021", loc="left", color=INK)
ax.legend(loc="upper left")
fig.savefig(FIG / "fig4_navngitt_andel.png")
plt.close(fig)

# Figur 5: månedlig import 2011–2014
fig, ax = plt.subplots(figsize=(8, 3.8))
ax.plot(mm.index, mm["Hard/halvhard ost"] / 1000, color=C1, label="Hard/halvhard ost")
ax.plot(mm.index, mm["Smelteost"] / 1000, color=C3, label="Smelteost")
ax.axvline(pd.Timestamp("2013-01-01"), color=INK2, lw=1, ls="--")
ax.set_ylabel("Tonn per måned")
ax.set_title("Figur 5. Månedlig import 2011–2014: hamstring og omklassifisering", loc="left", color=INK)
ax.legend(loc="upper left")
fig.savefig(FIG / "fig5_maned.png")
plt.close(fig)

# Figur 6: KPI
fig, ax = plt.subplots(figsize=(7, 3.6))
kk = kd["rel"].copy()
kk.index = kk.index.to_timestamp()
ax.plot(kk.index, kk.rolling(12, center=True).mean(), color=C1, label="12-mnd glidende snitt")
ax.plot(kk.index, kk, color=C1, alpha=0.3, lw=1, label="Månedlig")
ax.axvline(pd.Timestamp("2013-01-01"), color=INK2, lw=1, ls="--")
ax.set_ylabel("100 × log(KPI ost / KPI mat)")
ax.set_title("Figur 6. Konsumprisen på ost relativt til matvarer", loc="left", color=INK)
ax.legend(loc="lower right")
fig.savefig(FIG / "fig6_kpi.png")
plt.close(fig)

print("\nFerdig. Resultater i results/, figurer i figures/.")
