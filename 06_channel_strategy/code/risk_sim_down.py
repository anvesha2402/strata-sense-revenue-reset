# Monte Carlo: how likely is the channel to lose money (substitution lens) and to hit 25%?
import numpy as np, json
rng = np.random.default_rng(6); N = 20000
signed = {"FY27": 11, "FY28": 13, "FY29": 7}          # partners signed/reactivated to get 8 / 9 / 5 activated at ~70%
ramp = [0.15, 0.60, 1.0]; years = ["FY27", "FY28", "FY29"]
fixed = {"FY27": 3.94, "FY28": 5.46, "FY29": 6.5}
save = {"FY27": 1.64*0.60-0.164, "FY28": 1.64*0.65-0.170, "FY29": 1.64*0.70-0.176}   # substitution saving per ₹1
newlogo = {"FY27": 46.5, "FY28": 62.1, "FY29": 78.0}
res = {y: [] for y in years}
for _ in range(N):
    p_act = rng.beta(4.5, 5.5)                     # activation rate, mean 0.70 (history: 4 of 14 active = 0.29, before selection rules)
    shock = rng.lognormal(0, 0.25)             # common factor: market, product, Helix pressure
    existing = 2.26 * rng.uniform(0.7, 1.1)    # P02/P09/P12/P13 + restricted P05/P11 after Inject 3
    cohorts = []
    for k, y in enumerate(years):
        n = rng.binomial(signed[y], p_act)
        prod = rng.lognormal(np.log(0.45), 0.6, n) * shock    # median ₹1.0 cr, mean ≈ ₹1.2 cr
        cohorts.append((k, prod))
        tot = existing * 1.1**k + sum(p.sum() * ramp[k - c] for c, p in cohorts)
        res[y].append(tot)
out = {}
for y in years:
    a = np.array(res[y]); be = fixed[y] / save[y]
    out[y] = {"p10": float(np.percentile(a, 10)), "p50": float(np.percentile(a, 50)), "p90": float(np.percentile(a, 90)),
              "breakeven_total_arr": be, "p_loss": float((a < be).mean()), "p_share25": float((a / newlogo[y] >= 0.25).mean()), "median_share": float(np.median(a) / newlogo[y])}
json.dump(out, open("out/risk_sim_downside.json", "w"), indent=1); print(json.dumps(out, indent=1))
