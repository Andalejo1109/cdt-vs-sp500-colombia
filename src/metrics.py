"""Métricas: XIRR, CAGR, drawdown, estadísticas de retornos anuales."""
import numpy as np
import pandas as pd
from scipy.optimize import brentq


def xirr(flows: pd.Series) -> float:
    """flows: índice fecha, aportes negativos y valor final positivo."""
    t = (flows.index - flows.index[0]).days.values / 365.0
    f = lambda r: np.sum(flows.values / (1 + r) ** t)
    return brentq(f, -0.99, 10.0)


def max_drawdown(s: pd.Series) -> float:
    s = s.dropna()
    return float((s / s.cummax() - 1).min())


def cagr(s: pd.Series) -> float:
    s = s.dropna()
    yrs = (s.index[-1] - s.index[0]).days / 365.25
    return float((s.iloc[-1] / s.iloc[0]) ** (1 / yrs) - 1)


def annual_returns(level: pd.Series, first_year=None) -> pd.Series:
    """Retorno por año calendario con el último dato de cada año (el primer año puede ser parcial)."""
    s = level.dropna()
    ye = s.groupby(s.index.year).last()
    prev = ye.shift(1)
    prev.iloc[0] = s.iloc[0]
    r = ye / prev - 1
    if first_year is not None:
        r = r[r.index >= first_year]
    return r


def summary_from_annual(r: pd.Series, level: pd.Series, full_years) -> dict:
    full = r.loc[[y for y in r.index if y in full_years]]
    return {
        "acumulado": float((1 + r).prod() - 1),
        "cagr": cagr(level),
        "volatilidad_anual": float(full.std(ddof=1)),
        "peor_año": f"{full.min():.1%} ({full.idxmin()})",
        "mejor_año": f"{full.max():.1%} ({full.idxmax()})",
        "años_negativos": f"{int((full < 0).sum())} de {len(full)}",
        "max_drawdown": max_drawdown(level),
    }
