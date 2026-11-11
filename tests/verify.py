"""Pruebas de consistencia del motor (python tests/verify.py)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, pandas as pd
from src import engine, metrics, config

ok = 0
grid = pd.date_range("2020-01-01", "2021-12-31", freq="D")
dtf = pd.Series(10.0, index=grid)
# 1) Tasa constante 10 % EA: 1 año = +10 % (rollover 90 d no altera la tasa EA)
p = engine.cdt_cohort_path(100, grid[0], grid, dtf)
assert abs(p.loc["2020-12-31"] / 100 - 1.1 ** (365 / 365)) < 1e-9; ok += 1
# 2) Retención 4 %: tasa neta EA = ((1+(1.1^(90/365)-1)*0.96)^(365/90))-1
pr = engine.cdt_cohort_path(100, grid[0], grid, dtf, 0.04)
net = (1 + (1.1 ** (90 / 365) - 1) * 0.96) ** (365 / 90) - 1
assert abs(pr.iloc[720] / 100 - (1 + net) ** (720 / 365)) < 1e-9; ok += 1  # 8 vencimientos exactos
# 3) Sin look-ahead: la tasa se fija al inicio del plazo
dtf2 = dtf.copy(); dtf2.loc["2020-02-01":] = 20.0
p2 = engine.cdt_cohort_path(100, grid[0], grid, dtf2)
assert abs(p2.loc["2020-03-30"] - 100 * 1.1 ** (89 / 365)) < 1e-9; ok += 1
# 4) XIRR de un flujo a tasa conocida
f = pd.Series([-100, 110.0], index=pd.to_datetime(["2020-01-01", "2020-12-31"]))
assert abs(metrics.xirr(f) - 0.1) < 1e-3 or abs(metrics.xirr(f) - (1.1 ** (365 / 365) - 1)) < 1e-3; ok += 1
# 5) Resultados: el DCA en COP y USD es el mismo portafolio medido en dos monedas
d = pd.read_csv(config.OUTPUT / "dca_resultados.csv")
trm = pd.read_json(config.OUTPUT / "resultados.json", typ="series")["trm_corte"]
for (v, s), g in d[d["estrategia"].isin(["CDT (DTF 90d)", "S&P 500 TR", "Core"])].groupby(["ventana", "estrategia"]):
    cop = g[g.moneda == "COP"].valor_final.iloc[0]; usd = g[g.moneda == "USD"].valor_final.iloc[0]
    assert abs(cop / usd - trm) < 1e-6 * trm, (v, s)
ok += 1
# 6) Aportes: USD 1.000 + 200 por mes adicional
for v, g in d[d.moneda == "USD"].groupby("ventana"):
    n = (g.aportado.iloc[0] - 1000) / 200
    assert n == int(n); ok += 1
print(f"{ok} pruebas OK")
