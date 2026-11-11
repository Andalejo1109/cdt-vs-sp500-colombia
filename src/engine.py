"""Motores: índice CDT (rollover 90 d), índice core (rebalanceo mensual) y simulación DCA."""
import numpy as np
import pandas as pd
from . import config


def contribution_dates(trading_days: pd.DatetimeIndex, start: str) -> pd.DatetimeIndex:
    """Primer día hábil NYSE de cada mes desde `start`."""
    td = trading_days[trading_days >= start]
    s = pd.Series(td, index=td)
    return pd.DatetimeIndex(s.groupby([td.year, td.month]).min().values)


def _retention_rate(scn, date):
    if scn is None:
        return 0.0
    if scn == "hist":
        return 0.07 if date < pd.Timestamp(config.RET_HIST_SWITCH) else 0.04
    return float(scn)


def cdt_cohort_path(amount, t0, grid, dtf, retention=None, term=config.CDT_TERM_DAYS):
    """Valor de un CDT abierto en t0 y renovado cada `term` días a la DTF vigente al inicio de cada plazo.

    Dentro del plazo el valor se causa a la tasa pactada (interés compuesto diario EA, base 365).
    La retención (si aplica) se descuenta del interés al vencimiento de cada plazo; un plazo
    en curso se valora causado y neto de esa retención."""
    out = np.full(len(grid), np.nan)
    v, start = float(amount), pd.Timestamp(t0)
    end_all = grid[-1]
    while start <= end_all:
        r = dtf.asof(start) / 100.0
        stop = start + pd.Timedelta(days=term)
        m = (grid >= start) & (grid < stop)
        tax = _retention_rate(retention, stop)
        if m.any():
            acc = v * ((1 + r) ** (((grid[m] - start).days.values) / 365.0) - 1)
            out[m] = v + acc * (1 - tax)          # causado neto de la retención que se aplicará al vencer
        interest = v * ((1 + r) ** (term / 365.0) - 1)
        v += interest * (1 - tax)
        start = stop
    return pd.Series(out, index=grid)


def cdt_index(grid, dtf, start, retention=None):
    return cdt_cohort_path(1.0, pd.Timestamp(start), grid[grid >= start], dtf, retention)


def em_spliced(px: pd.DataFrame) -> tuple[pd.Series, dict]:
    """Serie emergente: EEM hasta 2012-10-24, IEMG desde 2012-10-25 (encadenada por retornos)."""
    eem, iemg = px["EEM"], px["IEMG"]
    r_eem, r_iemg = eem.pct_change(fill_method=None), iemg.pct_change(fill_method=None)
    sw = pd.Timestamp(config.EM_SPLICE_DATE)
    r = pd.concat([r_eem[r_eem.index < sw], r_iemg[r_iemg.index >= sw]])
    r = r[r.index >= eem.first_valid_index()].fillna(0.0)
    lvl = (1 + r).cumprod() * eem.dropna().iloc[0]
    ov = pd.concat([r_eem, r_iemg], axis=1).dropna()
    stats = {"solape_desde": ov.index.min().date().isoformat(), "solape_hasta": ov.index.max().date().isoformat(),
             "n_dias": len(ov), "corr_diaria": round(ov.corr().iloc[0, 1], 4),
             "corr_mensual": round((1 + ov).resample("ME").prod().sub(1).corr().iloc[0, 1], 4),
             "dif_cagr_anual": None}
    yrs = (ov.index[-1] - ov.index[0]).days / 365.25
    g = (1 + ov).prod() ** (1 / yrs) - 1
    stats["cagr_eem_solape"] = round(g.iloc[0], 4)
    stats["cagr_iemg_solape"] = round(g.iloc[1], 4)
    stats["dif_cagr_anual"] = round(g.iloc[1] - g.iloc[0], 4)
    return lvl.rename("EMG"), stats


def core_prices(px):
    emg, stats = em_spliced(px)
    cp = pd.concat([px[["SPYG", "SMH", "BRK-B", "VTI"]], emg], axis=1)
    start = max(cp[c].first_valid_index() for c in cp.columns)
    cp = cp[cp.index >= start].ffill()
    assert cp.notna().all().all()
    return cp, stats


def core_index(cp: pd.DataFrame, rebal_dates, cost_bps=config.COST_BPS) -> pd.Series:
    """Índice del core (sin aportes): rebalanceo a pesos objetivo en `rebal_dates`, costo por lado."""
    w = pd.Series(config.CORE_WEIGHTS)[cp.columns]
    units = None
    vals = []
    rset = set(rebal_dates)
    for d, p in cp.iterrows():
        if units is None:
            v = 1.0
            units = w * v * (1 - cost_bps / 1e4) / p
        else:
            v = float((units * p).sum())
            if d in rset:
                cur = units * p
                tgt = w * v
                cost = (tgt - cur).abs().sum() * cost_bps / 1e4
                v -= cost
                units = w * v / p
        vals.append(v)
    return pd.Series(vals, index=cp.index, name="core")


def simulate_dca(px, trm, dtf, start, retention=None, include_core=True, cp=None):
    """Simula USD 1.000 + USD 200/mes. Devuelve valores diarios en COP por estrategia y los flujos."""
    grid = px.index[px.index >= start]
    cdates = contribution_dates(px.index, start)
    usd = pd.Series(config.MONTHLY_USD, index=cdates)
    usd.iloc[0] = config.INITIAL_USD
    trm_d = trm.reindex(grid, method="ffill")
    cop = usd * trm.reindex(cdates, method="ffill")

    # CDT en COP: una cohorte por aporte
    cdt = pd.Series(0.0, index=grid)
    for d, a in cop.items():
        cdt = cdt.add(cdt_cohort_path(a, d, grid[grid >= d], dtf, retention), fill_value=0.0)

    # S&P 500 TR en USD (unidades del índice, sin costos ni comisión de fondo)
    sp = px[config.SP_TR].reindex(grid).ffill()
    units = (usd / sp.reindex(cdates)).reindex(grid).fillna(0).cumsum()
    sp_usd = units * sp

    out = {"CDT (DTF 90d)": cdt / trm_d, "S&P 500 TR": sp_usd}

    if include_core:
        w = pd.Series(config.CORE_WEIGHTS)[cp.columns]
        cpg = cp.reindex(grid).ffill()
        u = pd.Series(0.0, index=cp.columns)
        vals, cost_tot = [], 0.0
        cset = set(cdates)
        for d, p in cpg.iterrows():
            v = float((u * p).sum())
            if d in cset:
                v_new = v + usd[d]
                tgt = w * v_new
                cost = (tgt - u * p).abs().sum() * config.COST_BPS / 1e4
                cost_tot += cost
                v_new -= cost
                u = w * v_new / p
                v = v_new
            vals.append(v)
        out["Core"] = pd.Series(vals, index=grid)
    vals_usd = pd.DataFrame(out)
    vals_cop = vals_usd.mul(trm_d, axis=0)
    return {"usd": vals_usd, "cop": vals_cop, "flows_usd": usd, "flows_cop": cop, "trm": trm_d}
