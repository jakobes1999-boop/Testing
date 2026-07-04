# Which Sport Gives a Male Child the Highest Expected Income Return?

**Scope:** male child growing up in an OECD country, with specific attention to **Norway** and **Toulouse, France**
**Method:** probability-weighted expected lifetime income, net of family-borne development costs and opportunity costs, with an explicit treatment of causality vs. selection
**Evidence base:** deep-research sweep of 22 sources → 108 extracted claims → 25 adversarially verified (3 independent refutation votes each): 24 confirmed, 1 refuted
**Date:** 2026-07-04

---

## 1. Executive summary

**Short answer: football (soccer), in both Norway and Toulouse — with rugby union a close, locally-specific second in Toulouse.** Football combines (a) the largest and deepest professional wage pyramid in the world (thousands of paid second-tier slots across Europe, so the "consolation prizes" are real), (b) the highest world-class earnings ceiling of any accessible sport, and (c) among the *lowest* family-borne development costs in both locations, because the club/academy system — not the family — finances the elite pathway.

**But the more important answer: the expected *net* return of every professional sports career is negative for almost every child who starts one.** Even among boys already selected into elite football academies at age 13–18, only ~6% ever sign any professional contract and ~3.5–4% reach a top division (Moran et al. 2024). The only peer-reviewed study that directly computes a probability-weighted break-even against foregone education (Pifer et al. 2020, MLB) finds that for a college graduate, only roughly the top ~32 draft picks in the entire country have positive expected value. And the causal literature (Section 8) shows the observed earnings premium of ex-athletes is almost entirely **selection, not causation** — so the sport itself should not be credited with raising the income of the ~95% who don't make it.

The rational family strategy is therefore: **choose football (or, in Toulouse, rugby), let the club system pay for development, treat the sport as consumption plus a low-cost lottery ticket, and never sacrifice education** — because education is what determines the income of the overwhelmingly likely branch of the decision tree.

---

## 2. The valuation framework

For each sport *s*, the expected net lifetime income return of starting it seriously in childhood is:

```
EV(s) = P₁(s)·W₁(s) + P₂(s)·W₂(s) + [1 − P₁ − P₂]·ΔW_fail(s) − C(s) − OC(s)
```

| Term | Meaning |
|---|---|
| P₁ | probability of reaching world-class level (top ~50–100 in world / top-5-league) |
| W₁ | incremental lifetime earnings at world-class level vs. normal career |
| P₂ | probability of reaching national/second-tier professional level |
| W₂ | incremental lifetime earnings at that tier |
| ΔW_fail | causal wage effect of the (failed) sports investment on a normal career |
| C | family-borne development cost to age ~18–22 |
| OC | opportunity cost of foregone education/work during the attempt |

Two verified results discipline every entry in this equation:

1. **Rosen's superstar theorem (AER 1981, verified 3-0):** in sports labor markets income is concentrated in a few individuals with markedly skewed distributions; the reward-to-talent function is convex, so small talent differences produce enormous earnings differences, and there are large income gaps between first-rank and second-rank performers even when consumers can barely tell them apart. Broadcast scale economies mean **a sport's top earnings scale with its media market size** — which is why football's W₁ dwarfs handball's or biathlon's. Consequence: EV is dominated by low-probability extreme outcomes, and P₁·W₁ is the term that differentiates sports.
2. **The causal literature (Section 8, verified 3-0):** ΔW_fail ≈ 0. The apparent wage premium of former youth/high-school athletes disappears under modest allowance for selection on unobservables. You cannot count on the sport "building character that pays."

---

## 3. The probabilities: verified conversion rates

These are the strongest-evidenced numbers in the entire analysis. All verified 3-0 unless noted.

### Football (most relevant to both Norway and Toulouse)
- **Academy → any professional contract: ~6.1%** (12 of 198 academy players aged 13.5–17.9 at two Madrid LaLiga club academies, 10-year longitudinal follow-up; Moran et al. 2024, *Int. J. Sports Science & Coaching*). **Academy → top division: ~3.5–4%.** Roughly **95% of teenage academy players never turn professional** — and these boys were already the selected elite.
- English youth-license holders → Premier League contract: **~0.012%** (≈180 of 1.5M licensed youth players; extracted, secondary source). England-wide reports put academy-entrant (from under-9) → pro conversion at **~0.5%**.
- **U17 national team → senior national team: 9.2–14.6%** across England, France, Germany, Italy, Spain (n = 9,527 players, 2002–2022; Brustio et al. 2024). Even **U21** internationals convert at under 40%. And 14–24% of senior internationals were *never* youth internationals — early selection is weakly predictive in both directions.

### US pipeline sports (NCAA Research, official methodology documents, verified 3-0)
- High school → NCAA: basketball 3.5% (1.0% Division I), American football 7.3%, soccer 5.6%, tennis 4.9%, golf 5.9%, ice hockey 12.3%.
- Draft-eligible NCAA → drafted: basketball ~1.0–1.2% (NBA), American football ~1.4% (NFL). Chained: **~1 in 2,400 US high-school basketball players reaches the NBA draft.**
- **Being drafted ≠ earning professional income** (verified 2-1): of 224 players taken in the 2025 NHL draft, only 5 had played an NHL game by 2025-26 (historically ~half of NHL draftees ever play one game).
- Per-participant odds of elite professional status (extracted from NCAA-based analysis, not separately verified): golf ~1 in 51,000, soccer ~1 in 55,000, **tennis ~1 in 82,000** — tennis has the worst conversion odds of the individual sports analyzed.

**Takeaway:** the probability of world-class status for a child who starts any of these sports is on the order of 10⁻⁴ to 10⁻⁵, and the probability of *any* professional income is on the order of 10⁻³ even conditional on being visibly talented in adolescence. No candidate sport escapes this by an order of magnitude; differences in P are second-order compared to differences in W₁ and C.

---

## 4. Earnings by tier (W₁ and W₂)

Verified where marked; the sport-specific salary figures below were extracted from the sources but were not among the 25 claims that went through full adversarial verification — treat as indicative.

| Sport | World-class (W₁ level) | National / 2nd tier (W₂ level) | Notes |
|---|---|---|---|
| **Football** | Top-5-league average wages are in the €1–4M/yr range (league-dependent); superstars far above | Hundreds of clubs pay full-time wages; Championship/Ligue 2/Eliteserien range roughly €50k–500k/yr | Deepest pyramid of paid slots in world sport; earnings peak at ~age 28 (Serie A: Lucifora & Simmons 2003; **Norwegian football: Thrane 2019**) |
| **Rugby union (Toulouse)** | **Top 14 average ≈ €240,000/yr**; ceiling ≈ €1.0–1.2M (Pollard, Russell) | **Pro D2 average ≈ €68,000/yr**; academy/junior contracts ≈ €16,000/yr; first senior pro contract ≈ €60,000 | Salary cap €10–11.3M per club and post-2020 15–20% pay cuts constrain growth; pyramid much shallower than football (~30 pro clubs in France) |
| **Handball** | French Starligue *average* ≈ €75,000/yr (€6,261/mo gross, 2025-26, falling 3% y/y); German Bundesliga pays more | Starligue *median* €5,000/mo; most players €4,000–6,000/mo | Even the "world-class" tier of handball pays like a good white-collar job, not a fortune |
| **Biathlon / cross-country (Norway)** | Single World Cup race win: **€20,000**; season-long overall World Cup title bonus: **€45,000**; total IBU prize pool ≈ €8.58M *for the entire sport* | IBU Cup (2nd tier) race win: **€3,000**; prize money reaches only top 30 (30th place: €250) | Prize income near zero below world top-30; stars rely on sponsorship (not quantified in surviving evidence) |
| **Tennis** | Top 50 players (~1% of ranked pros) capture ~60% of the $162M ATP prize pool | Of ~1,500 ATP players earning >$1,000, fewer than 300 clear $100k gross — before costs of ~$90–100k/yr for a top-200 player | Most pros take 3–5 years to turn *any* profit; the negative-cash-flow period extends past age 22 |
| **Basketball** | NBA: highest average salaries in world sport | European leagues pay modest wages outside EuroLeague; G-League/international routes are low-paid | For a European child the NBA path probability is far below even the US 1-in-2,400 figure |
| **Ice hockey** | NHL high; but draft→NHL conversion is weak (see §3) | Norwegian/European second tiers pay modestly | Also the 2nd most expensive childhood sport in Norway (§5) |

**Rosen's theorem, empirically visible:** in every sport the cliff between W₁ and W₂ is steep (tennis #1 vs #32 earnings gap ~1000%; biathlon €20,000/race vs €3,000/race one tier down; Top 14 €240k vs Pro D2 €68k). Football is the exception that matters: its second tier is still a genuinely good income, and it has *thousands* of such slots worldwide. Football maximizes not the jackpot alone but the **probability-weighted area under the whole prize curve**.

---

## 5. Family-borne costs (C) — the term that decides Norway

The Norwegian evidence here is unusually good: the cost data come from the Norwegian Sports Confederation (NIF) 2024 report *Kostnader og kostnadsdrivere for barne- og ungdomsidretten*, research by Prof. Dag Vidar Hanstad (NIH) **together with Oslo Economics**, commissioned by the Ministry of Culture. (Extracted from primary sources; not among the 25 adversarially verified claims.)

Median total annual family-borne cost in Norway (fees, equipment, travel, participation):

| Sport (Norway) | Age 9 | Age 15 | Notes |
|---|---|---|---|
| All sports (median) | NOK 2,805 | NOK 6,450 | Means ~NOK 3,658 / 9,440 — outliers pull means up |
| **Football** | NOK 3,350 | **NOK 7,125** | Cheap; club system carries the elite pathway |
| **Cross-country skiing** | — | **NOK 7,975 median / 11,702 mean** | Most expensive of surveyed sports at 15; equipment-dominated; travel costs jump from age 16 when national-level competition starts |
| **Ice hockey** | — | **≈ NOK 24,800 mean** | 2nd most expensive childhood sport |
| **Alpine skiing** | — | **≈ NOK 45,200 mean; extremes NOK 200,000–250,000/yr** | Most expensive; effectively requires family wealth |

Key cost facts:
- Parents finance on average **48%** of children's sport costs in Norway (under 30% in cross-country skiing's club layer, ~80% in some individual sports).
- Costs escalate sharply on the elite track: median travel/accommodation for 15-year-olds is NOK 1,500/yr, but international-level youth athletes reach **NOK 120,000/yr**.
- **Tennis** (globally): a top-200 professional spends **$90–100k/yr touring**, and typical pros run negative cash flow for 3–5 years — the family effectively pays W₂-level money for the *chance* of W₂.
- **Rugby in France inverts the sign of C**: academy players are *paid* (~€16,000/yr), and Stade Toulousain's academy is club-funded. For a talented Toulouse teenager the elite rugby pathway has approximately zero family cost and positive cash flow from ~17.
- French football academies (INSEP-style federation pathway) similarly carry most elite-track costs.

**Consequence:** in Norway, the traditional national sports (cross-country, biathlon, alpine) combine the *highest* family costs with the *smallest* prize pools — the worst possible EV combination. Football combines the lowest costs with the largest prizes.

---

## 6. Career length and post-career effects

- Careers are short and level-dependent (Jones et al. 2025, n = 4,117 English pros, **verified 3-0**): total career 14.8 years for EPL players with international caps, down to 6.2 years in League Two; **time at peak level is only ~7.5 years (EPL+intl), ~4.4 years (EPL), ~3 years below that**. At 5 years, under 20% of Championship-and-below players are still at their highest level.
- Retirement: EPL+intl outfielders retire at ~33.4 on average; **League Two at ~25.6** — a second-tier pro faces ~40 years of post-sport working life, so his lifetime income is dominated by his post-sport human capital, i.e., by the education the sport did or didn't crowd out.
- Earnings peak around **age 28** (Italian and **Norwegian** football alike).
- Post-career: former German elite athletes earn more than matched non-athletes (GSOEP nearest-neighbour matching), with a **larger premium for team-sport and male athletes** — but the design cannot rule out selection on unobservables, so this is not a causal return to the sport. Handball offers a concrete post-career ladder (Starligue head coaches average €7,713/mo — more than the median player).
- Norway and France both operate dual-career norms (school alongside academy), which mitigates — but does not eliminate — the opportunity-cost term OC. Pifer et al.'s break-even logic (below) shows OC is decisive.

---

## 7. The expected-value ranking

### The one directly comparable peer-reviewed benchmark (verified 3-0)

**Pifer, McLeod, Travis & Castleberry (2020, *Journal of Sports Economics*)** compute, for MLB draftees, the draft position at which expected six-year professional earnings equal the six-year income of same-age men by education level. Break-even: pick **~171** for pitchers with some college, but **~32 for college graduates**. Read that carefully: among the few hundred best baseball players in the United States in a given year — each of whom already beat ~10⁻⁴ odds — turning pro is a *losing* financial bet for most of them once the educational counterfactual is decent. For a child at the start of the pathway, the expected net return is unambiguously negative.

### Illustrative EV per sport

The table below chains the verified probabilities (§3), indicative wages (§4) and costs (§5) into a rough expected value **per boy who takes up the sport seriously at ~age 6–10**, in the spirit of the question. These are order-of-magnitude illustrations, not estimates — the caveats in §9 apply. W₁/W₂ are incremental lifetime sport earnings vs. a normal career; probabilities are per-starter (academy-conditional rates from §3 deflated by an assumed 1–3% chance of ever reaching academy/elite-track level).

| Sport | P₁ (world-class) | P₂ (national pro) | W₁ (incr., lifetime) | W₂ (incr., lifetime) | C + OC to 22 | **Illustrative EV** |
|---|---|---|---|---|---|---|
| **Football (NO & FR)** | ~1×10⁻⁴ | ~1.5×10⁻³ | ~€10–20M | ~€0.3–0.8M | ~€10–15k | **≈ +€1,500 to +€3,500** |
| **Rugby (Toulouse)** | ~1×10⁻⁴ | ~2×10⁻³ | ~€1.5–2.5M | ~€0.3–0.5M | ~€0 (club-funded, academy paid) | **≈ +€800 to +€1,200** |
| Ice hockey (NO) | ~3×10⁻⁵ | ~1×10⁻³ | ~€5–15M (NHL) | ~€0.2M | ~€30–60k | ≈ −€30k |
| Basketball (EU child) | ~2×10⁻⁵ | ~1×10⁻³ | ~€10–30M (NBA) | ~€0.15M | ~€10–20k | ≈ −€10k |
| Handball (NO/FR) | ~1×10⁻⁴ | ~2×10⁻³ | ~€0.8–1.5M | ~€0.15M | ~€10k | ≈ −€9k |
| XC ski / biathlon (NO) | ~5×10⁻⁵ | ~1×10⁻³ | ~€1–3M (mostly sponsorship) | ~€0.05M | ~€60–120k | ≈ −€60k to −€100k |
| Golf | ~2×10⁻⁵ | ~5×10⁻⁴ | ~€3–10M | ~€0.1M | ~€60–150k | ≈ −€60k to −€140k |
| Tennis | ~1.2×10⁻⁵ | ~5×10⁻⁴ | ~€5–15M | ~€0 (2nd tier ≈ break-even after costs) | ~€150–400k | **≈ −€150k to −€400k (worst)** |

**Ranking (highest to lowest expected income return):**

1. **Football** — everywhere in the OECD, including Norway and Toulouse. The only sport where the illustrative EV is even *plausibly* non-negative, and that is entirely because C ≈ 0 (club-funded pathway) and the second tier genuinely pays.
2. **Rugby union — in Toulouse specifically.** The pathway is free-to-positive cash flow (paid academy), Top 14 average pay is solid, and local density (Stade Toulousain) raises the effective P of a Toulouse child relative to the national average. Its ceiling (~€1.2M/yr, capped clubs, shrinking salary mass) keeps it below football.
3. Handball / ice hockey / basketball — middling wages or high costs; EV mildly negative.
4. Cross-country skiing & biathlon — **the worst mainstream choice in Norway on financial grounds**: highest family costs of the surveyed team/endurance sports, near-zero prize money below world top-30, tiny media market (Rosen's scale-economies point made flesh).
5. Tennis and golf — the worst overall: worst per-participant odds (tennis 1 in 82,000), enormous family-borne costs, and a second tier that *loses* money after touring expenses.
6. E-sports — no claims survived verification; no responsible estimate possible (openly flagged as an evidence gap).

**All EVs are small or negative relative to simply investing the same money and hours in education** — which is the real headline. Football "wins" the ranking mostly because it costs the family almost nothing to try.

---

## 8. Causality: does the sport *cause* higher income?

This was asked for explicitly, and the verified evidence is unusually clear. **No — the observed athlete income premium is overwhelmingly selection, not causation.**

- **Ransom & Ransom (2018, *Economics of Education Review*, verified 3-0):** across three US longitudinal surveys (NLSY79, NELS:88, Add Health), using Altonji–Elder–Taber/Krauth/Oster bounding methods, there is **no consistent causal evidence** that youth athletic participation improves education or labor-market outcomes. The descriptive premium (~15% higher male wages at 25) **goes to zero if selection on unobservables is only half as strong as selection on observables**.
- **Cabane & Clark (2015, Add Health, ~16,000 respondents, sibling fixed effects, verified 3-0):** mostly no significant sport–wage correlations by ages 24–32.
- **Barron, Ewing & Waddell (2000):** naive premium 14–19%; controls for ability/family cut it to ~7%; instrumenting participation kills the wage effect entirely. Athletics acts as a **signal** of pre-existing ability/industriousness, not as productivity-enhancing training.
- **Selection is visible inside the pipeline itself:** future pros were already statistically distinguishable at academy age (ball reception r = −0.44, dribbling r = −0.56, coach ratings); a strong relative-age effect (none of the 12 Madrid-academy pros were born in Q4; German Bundesliga youth selection favors early-born boys, yet late-born *survivors* out-earn — the signature of selection on ability); and in Norway there is a steep socioeconomic gradient *before* any elite tier (75% fixed sport participation in the top household-resource quintile vs. 53% in the bottom).
- **Ex-elite athletes** (German GSOEP matching) do earn more later in life, more so in team sports and for men — but the design cannot separate this from selection on talent, drive, and family background.

**Implications for the decision:**
1. Do not credit the sport with a positive ΔW_fail for the ~95–99.9% branch; set it ≈ 0.
2. Symmetrically, the evidence does not show large causal *harm* from participation either (educational attainment of athletes is higher, not lower) — provided the dual-career route is kept open. The catastrophic outcomes concentrate among those who *forgo education* for the attempt (Pifer et al.'s break-even) and among released academy players (documented identity-crisis/mental-health costs).
3. The child's underlying talent, height, family resources and drive — not the chosen sport — will determine both his athletic odds *and* his fallback income. Choice of sport moves C and the prize structure; it does not manufacture ability.

---

## 9. Caveats and evidence gaps

- **No verified claims survived** for rugby union, handball, skiing/biathlon, tennis, golf, cycling, athletics, or e-sports conversion rates — the §7 table fills those cells with extracted-but-unverified figures and stated assumptions. Component (4) of the question (pathway costs) rests on Norwegian primary reports that were fetched and extracted but not adversarially verified.
- Academy conversion rates come from two Madrid clubs (57% of the cohort untraced, assumed retired); career lengths from English leagues; transferability to Norway/France is plausible but untested.
- One claim was **refuted 0-3** and is excluded: that minor-league baseball pay is below most players' reservation wage / that young players systematically overestimate their odds.
- The hockey "5 of 224 drafted played an NHL game" figure is a first-season snapshot; ~half of NHL draftees eventually play at least one game.
- The causality literature is US-based and concerns *participation*, not elite professionalization; European replication is thin.
- Football wage skew has been rising (bigger jackpots, same near-zero odds); NIL-era changes shift US opportunity costs; salary figures are 2019–2026 vintages.
- Open questions: French Espoirs/Top 14 academy conversion rates; whether dual-career mandates in Norway/France neutralize the foregone-education penalty; whether the NCAA-scholarship route makes some US pathways positive-EV as a *subsidized education channel* even when the pro lottery is negative-EV.

---

## 10. Bottom line for this family

- **In Norway:** football. Lowest cost (median ~NOK 7,000/yr at 15), club-financed elite track, the deepest paid pyramid in world sport, and a Norwegian second tier that pays real wages. Avoid alpine/cross-country/biathlon *as an income strategy* — highest costs, smallest prizes (a World Cup race win pays €20,000; the second tier pays €3,000 a win).
- **In Toulouse:** football first, rugby a strong and locally rational second — the Stade Toulousain pathway is club-funded and pays academy players (~€16k) and young pros (~€60k), with a Top 14 average of ~€240k. Rugby's capped, shrinking salary mass keeps its ceiling an order of magnitude below football's.
- **In either place:** the expected financial value of the sports career itself is approximately zero to negative. The decision-theoretically dominant play is the cheap lottery ticket (football/rugby through the club system), full protection of the education track (which sets the income of the >99% branch and, per Pifer et al., determines whether even *success* is worth taking), and treating the sport's health, social and signaling benefits as the true, near-certain return.

---

## 11. Principal sources

**Peer-reviewed / primary (verified claims):**
- Moran et al. (2024), *Int. J. Sports Science & Coaching* — 10-year Spanish academy follow-up (6.1% pro, ~4% top tier). [SAGE](https://journals.sagepub.com/doi/10.1177/17479541241254767)
- Brustio et al. (2024), *Frontiers in Sports and Active Living* — U17→senior national-team conversion, 5 nations, n=9,527. [PMC11288826](https://pmc.ncbi.nlm.nih.gov/articles/PMC11288826/)
- NCAA Research — *Estimated Probability of Competing in Professional Athletics* (2020; 2026 update). [ncaa.org](https://www.ncaa.org/sports/2015/3/6/estimated-probability-of-competing-in-professional-athletics.aspx)
- Rosen (1981), "The Economics of Superstars," *American Economic Review* 71(5).
- Jones et al. (2025) — career length/survival, 4,117 English professionals. [PMC12392379](https://pmc.ncbi.nlm.nih.gov/articles/PMC12392379/)
- Pifer, McLeod, Travis & Castleberry (2020), *Journal of Sports Economics* — MLB draft break-even vs. foregone education; Simmons (2022) *JSE* review.
- Ransom & Ransom (2018), *Economics of Education Review* 64 — bounding causal estimates of HS sports.
- Cabane & Clark (2015), *Annals of Economics and Statistics* — sibling fixed effects, Add Health.
- Barron, Ewing & Waddell (2000), *Review of Economics and Statistics* — athlete wage premium, IV.

**Primary cost/context (extracted, not adversarially verified):**
- NIF (2024), *Kostnader og kostnadsdrivere for barne- og ungdomsidretten* — Hanstad (NIH) with Oslo Economics, for the Ministry of Culture.
- NIH (2024), *Barna og idretten* — participation and socioeconomic gradients.
- Starligue salary survey 2025-26 (handnews.fr); French rugby salaries (rugbydome.com); IBU prize money 2025/26 (etusuora.com); ATP prize concentration and touring costs (sigruntennis.com).
