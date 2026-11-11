"""CDT (DTF 90 días) vs S&P 500 TR vs core de Alejandro, 2000-2026. Ejecutar: python main.py [--refresh]"""
import json
import sys
import numpy as np
import pandas as pd
from src import config, data, engine, metrics, plot

OUT = config.OUTPUT
OUT.mkdir(exist_ok=True)
pct = lambda x: round(100 * x, 2)


def build():
    d = data.load_all(refresh="--refresh" in sys.argv)
    px, trm, dtf, dtf_m, ipc, cpi, sfc = d["px"], d["trm"], d["dtf"], d["dtf_m"], d["ipc"], d["cpi"], d["sfc"]
    px = px[px[config.SP_TR].notna()]
    last = px.index[-1]
    res = {"fecha_corte": last.date().isoformat(), "trm_corte": float(trm.asof(last))}

    # ---------- Niveles (índices) ----------
    y0 = px.index[px.index.year == 1999][-1]                        # 1999-12-31
    cal = pd.date_range(y0, last, freq="D")
    cdt_cal = engine.cdt_index(cal, dtf, y0)                        # COP, calendario
    cdt_td = cdt_cal.reindex(px.index[px.index >= y0])               # en días hábiles NYSE
    trm_td = trm.reindex(px.index, method="ffill")
    sp_usd = px[config.SP_TR][px.index >= y0]
    sp_cop = sp_usd * trm_td.reindex(sp_usd.index)
    cdt_usd = cdt_td / trm_td.reindex(cdt_td.index)
    cp, em_stats = engine.core_prices(px)
    rebal = engine.contribution_dates(px.index, cp.index[0] + pd.Timedelta(days=1))
    core_usd = engine.core_index(cp, rebal)
    core_cop = core_usd * trm_td.reindex(core_usd.index)
    res["core_inicio"] = core_usd.index[0].date().isoformat()
    res["em_splice"] = em_stats

    # ---------- Tabla anual ----------
    yrs = range(2000, last.year + 1)
    full_years = list(range(2000, last.year))
    ar = pd.DataFrame(index=yrs)
    ar["dtf_promedio_ea"] = dtf_m.groupby(dtf_m.index.year).mean().reindex(yrs) / 100
    ar["cdt_cop"] = metrics.annual_returns(cdt_cal, 2000)
    ar["sp500tr_usd"] = metrics.annual_returns(sp_usd, 2000)
    ar["sp500tr_cop"] = metrics.annual_returns(sp_cop, 2000)
    ar["core_usd"] = metrics.annual_returns(core_usd).reindex(yrs)
    ar["core_cop"] = metrics.annual_returns(core_cop).reindex(yrs)
    ar["cdt_usd"] = metrics.annual_returns(cdt_usd, 2000)
    ipc_ye = ipc.groupby(ipc.index.year).last()
    ar["inflacion_col"] = (ipc_ye / ipc_ye.shift(1) - 1).reindex(yrs)
    cpi_ye = cpi.groupby(cpi.index.year).last()
    ar["inflacion_eeuu"] = (cpi_ye / cpi_ye.shift(1) - 1).reindex(yrs)
    trm_ye = trm_td.groupby(trm_td.index.year).last()
    ar["devaluacion_trm"] = (trm_ye / trm_ye.shift(1) - 1).reindex(yrs)
    ar["cdt_real_cop"] = (1 + ar["cdt_cop"]) / (1 + ar["inflacion_col"]) - 1
    ar["sp500tr_real_cop"] = (1 + ar["sp500tr_cop"]) / (1 + ar["inflacion_col"]) - 1
    ar["core_real_cop"] = (1 + ar["core_cop"]) / (1 + ar["inflacion_col"]) - 1
    ar["sp500tr_real_usd"] = (1 + ar["sp500tr_usd"]) / (1 + ar["inflacion_eeuu"]) - 1
    ar["gana_cdt_vs_sp_cop"] = ar["cdt_cop"] > ar["sp500tr_cop"]
    ar.index.name = "año"
    ar.to_csv(OUT / "retornos_anuales.csv", float_format="%.6f")

    levels = {"CDT COP": cdt_cal, "S&P 500 TR USD": sp_usd, "S&P 500 TR COP": sp_cop, "CDT USD": cdt_usd,
              "Core USD (desde 2003)": core_usd, "Core COP (desde 2003)": core_cop}
    rmap = {"CDT COP": "cdt_cop", "S&P 500 TR USD": "sp500tr_usd", "S&P 500 TR COP": "sp500tr_cop",
            "CDT USD": "cdt_usd", "Core USD (desde 2003)": "core_usd", "Core COP (desde 2003)": "core_cop"}
    summ = {}
    for k, lv in levels.items():
        r = ar[rmap[k]].dropna()
        fy = [y for y in full_years if y >= (2004 if "Core" in k else 2000)]
        summ[k] = metrics.summary_from_annual(r, lv, fy)   # core: acumulado/CAGR desde 2003-04-14; stats en años completos 2004+
    # Mismo periodo 2003-hoy para todos (desde el inicio del core)
    c0 = core_usd.index[0]
    for k, lv in [("CDT COP 2003-hoy", cdt_cal), ("S&P 500 TR COP 2003-hoy", sp_cop),
                  ("S&P 500 TR USD 2003-hoy", sp_usd), ("Core COP 2003-hoy", core_cop), ("Core USD 2003-hoy", core_usd)]:
        s = lv[lv.index >= c0]
        summ[k] = {"acumulado": float(s.iloc[-1] / s.iloc[0] - 1), "cagr": metrics.cagr(s),
                   "max_drawdown": metrics.max_drawdown(s)}
    sm = pd.DataFrame(summ).T
    sm.to_csv(OUT / "resumen_retornos.csv")
    res["resumen_retornos"] = summ

    # ---------- Subperiodos de estrés ----------
    def per(lv, a, b):
        s = lv[(lv.index >= a) & (lv.index <= b)]
        if len(s) == 0 or s.index[0] > pd.Timestamp(a) + pd.Timedelta(days=10):
            return np.nan
        base = lv[lv.index < a]
        b0 = base.iloc[-1] if len(base) else s.iloc[0]
        return float(s.iloc[-1] / b0 - 1)
    periods = {"2000-2002 (puntocom)": ("2000-01-01", "2002-12-31"), "2008 (crisis financiera)": ("2008-01-01", "2008-12-31"),
               "2020 (covid, año)": ("2020-01-01", "2020-12-31"), "feb-mar 2020 (caída covid)": ("2020-02-20", "2020-03-23"),
               "2022 (tasas/inflación)": ("2022-01-01", "2022-12-31")}
    sub = pd.DataFrame({k: {n: per(lv, a, b) for n, lv in levels.items()} for k, (a, b) in periods.items()}).T
    sub.to_csv(OUT / "subperiodos_estres.csv", float_format="%.6f")

    # ---------- DCA ----------
    dca_rows, dca_curves = [], {}
    for label, start, core in [("2000-hoy", config.DCA_START_FULL, False), ("2003-hoy", config.DCA_START_CORE, True)]:
        sim = engine.simulate_dca(px, trm, dtf, start, None, include_core=core, cp=cp)
        dca_curves[label] = sim
        for cur in ["cop", "usd"]:
            vals, fl = sim[cur], sim[f"flows_{cur}"]
            ap = fl.cumsum().reindex(vals.index, method="ffill")
            for s in vals.columns:
                v = vals[s]
                flows = pd.concat([-fl, pd.Series({last: v.iloc[-1]})]).groupby(level=0).sum()
                row = {"ventana": label, "moneda": cur.upper(), "estrategia": s, "aportado": fl.sum(),
                       "valor_final": v.iloc[-1], "multiplo": v.iloc[-1] / fl.sum(), "xirr": metrics.xirr(flows),
                       "max_dd_patrimonio": metrics.max_drawdown(v),
                       "max_caida_vs_aportado": float((v / ap - 1).min())}
                if cur == "cop":
                    defl = ipc.asof(last) / ipc.reindex(fl.index.to_period("M").to_timestamp(), method="ffill").values
                    rf = pd.concat([-fl * defl, pd.Series({last: v.iloc[-1]})]).groupby(level=0).sum()
                    row["xirr_real_cop"] = metrics.xirr(rf)
                    row["aportado_pesos_oct2026"] = float((fl * defl).sum())
                dca_rows.append(row)
        # CDT con retención (sensibilidad)
        for scn, rt in config.RETENTION_SCENARIOS.items():
            if rt is None:
                continue
            fl = sim["flows_cop"]
            v = pd.Series(0.0, index=sim["cop"].index)
            for dd, a in fl.items():
                v = v.add(engine.cdt_cohort_path(a, dd, v.index[v.index >= dd], dtf, rt), fill_value=0)
            flows = pd.concat([-fl, pd.Series({last: v.iloc[-1]})]).groupby(level=0).sum()
            defl = ipc.asof(last) / ipc.reindex(fl.index.to_period("M").to_timestamp(), method="ffill").values
            rf = pd.concat([-fl * defl, pd.Series({last: v.iloc[-1]})]).groupby(level=0).sum()
            dca_rows.append({"ventana": label, "moneda": "COP", "estrategia": f"CDT (DTF 90d) {scn}", "aportado": fl.sum(),
                             "valor_final": v.iloc[-1], "multiplo": v.iloc[-1] / fl.sum(), "xirr": metrics.xirr(flows),
                             "max_dd_patrimonio": metrics.max_drawdown(v), "max_caida_vs_aportado": 0.0,
                             "xirr_real_cop": metrics.xirr(rf), "aportado_pesos_oct2026": float((fl * defl).sum())})
    dca = pd.DataFrame(dca_rows)
    dca.to_csv(OUT / "dca_resultados.csv", index=False, float_format="%.6f")

    # ¿Cuándo iba ganando el CDT en el DCA (COP)?
    c = dca_curves["2000-hoy"]["cop"]
    m = c.resample("ME").last()
    lead = m["CDT (DTF 90d)"] > m["S&P 500 TR"]
    res["dca_meses_cdt_adelante_pct"] = float(lead.mean())
    res["dca_ultimo_mes_cdt_adelante"] = lead[lead].index.max().strftime("%Y-%m") if lead.any() else None
    runs = (lead != lead.shift()).cumsum()
    res["dca_tramos_cdt_adelante"] = [f"{g.index.min():%Y-%m}..{g.index.max():%Y-%m}" for _, g in m[lead].groupby(runs[lead])]
    c3 = dca_curves["2003-hoy"]["cop"].resample("ME").last()
    l3 = c3["CDT (DTF 90d)"] > c3["Core"]
    res["dca2003_tramos_cdt_adelante_core"] = [f"{g.index.min():%Y-%m}..{g.index.max():%Y-%m}" for _, g in c3[l3].groupby(((l3 != l3.shift()).cumsum())[l3])]

    # ---------- Ventanas rodantes (suma única, CAGR) ----------
    mlev = pd.DataFrame({"CDT COP": cdt_cal, "S&P 500 TR COP": sp_cop, "Core COP": core_cop,
                         "S&P 500 TR USD": sp_usd, "CDT USD": cdt_usd}).ffill().resample("ME").last()
    roll, roll_rows = {}, []
    for yrs_ in (5, 10):
        n = 12 * yrs_
        g = (mlev / mlev.shift(n)) ** (1 / yrs_) - 1
        roll[yrs_] = g
        for a, b in [("S&P 500 TR COP", "CDT COP"), ("Core COP", "CDT COP"), ("S&P 500 TR USD", "CDT USD")]:
            x = g[[a, b]].dropna()
            roll_rows.append({"ventana_años": yrs_, "comparación": f"{a} vs {b}", "n_ventanas": len(x),
                              "pct_gana_bolsa": float((x[a] > x[b]).mean()),
                              "peor_cagr_bolsa": float(x[a].min()), "mejor_cagr_bolsa": float(x[a].max()),
                              "peor_cagr_cdt": float(x[b].min()), "mejor_cagr_cdt": float(x[b].max()),
                              "pct_bolsa_negativa": float((x[a] < 0).mean()),
                              "primera_ventana_fin": x.index.min().strftime("%Y-%m"),
                              "ultima_ventana_fin": x.index.max().strftime("%Y-%m")})
    rr = pd.DataFrame(roll_rows)
    rr.to_csv(OUT / "ventanas_rodantes.csv", index=False, float_format="%.6f")

    # ---------- Verificación del dato del amigo ----------
    y25 = px.index[px.index.year == 2025][-1]
    ver = {
        "dtf_vigente": {"tasa_ea": float(dtf.asof(pd.Timestamp("2026-11-11"))), "vigencia": "2026-11-09..2026-11-15",
                        "dtf_mensual_oct2026": float(dtf_m.iloc[-1])},
        "sp500_precio_ytd_usd": float(px[config.SP_PRICE].iloc[-1] / px[config.SP_PRICE].loc[y25] - 1),
        "sp500_tr_ytd_usd": float(px[config.SP_TR].iloc[-1] / px[config.SP_TR].loc[y25] - 1),
        "sp500_tr_ytd_cop": float(sp_cop.iloc[-1] / sp_cop.loc[y25] - 1),
        "trm_31dic2025": float(trm.asof(y25)), "trm_corte": float(trm.asof(last)),
        "sp500_tr_12m_usd": float(px[config.SP_TR].iloc[-1] / px[config.SP_TR].asof(last - pd.DateOffset(years=1)) - 1),
        "cdt_ytd_cop_modelo": float(cdt_cal.iloc[-1] / cdt_cal.loc[pd.Timestamp("2025-12-31")] - 1),
        "inflacion_col_anual_oct2026": float(ipc.iloc[-1] / ipc.loc["2025-10-01"] - 1),
    }
    s = sfc[sfc["fechacorte"] >= "2026-11-03"].copy()
    s["tasa"] = s["tasa"].astype(float); s["monto"] = s["monto"].astype(float)
    s = s[s["tasa"] > 0]
    for plazo, g in s.groupby("plazo"):
        ent = g.groupby("nombreentidad").apply(lambda x: np.average(x["tasa"], weights=x["monto"]), include_groups=False)
        ver[f"sfc_cdt_{plazo}"] = {"promedio_ponderado_sistema": float(np.average(g["tasa"], weights=g["monto"])),
                                   "entidades": int(ent.size), "max_entidad": f"{ent.idxmax()} {ent.max():.2f}%",
                                   "pct_entidades_>=13": float((ent >= 13).mean()),
                                   "top5": {k: round(v, 2) for k, v in ent.nlargest(5).items()},
                                   "semana": f"{g['fechacorte'].min().date()}..{g['fechacorte'].max().date()}"}
    res["verificacion_amigo"] = ver
    (OUT / "resultados.json").write_text(json.dumps(res, indent=2, ensure_ascii=False, default=str))

    plot.annual_bars(ar, last)
    plot.dca_curves(dca_curves, "cop", OUT / "cdt_vs_sp500_dca_cop.png", last)
    plot.dca_curves(dca_curves, "usd", OUT / "cdt_vs_sp500_dca_usd.png", last)
    plot.rolling(roll, OUT / "cdt_vs_sp500_ventanas_rodantes.png", rr)
    return dict(ar=ar, sm=sm, sub=sub, dca=dca, rr=rr, res=res)


if __name__ == "__main__":
    r = build()
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
    print((r["ar"].drop(columns="gana_cdt_vs_sp_cop") * 100).round(2))
    print(r["sm"]); print(r["sub"].round(4)); print(r["dca"].round(4)); print(r["rr"].round(4))
    print(json.dumps(r["res"], indent=1, ensure_ascii=False, default=str))
