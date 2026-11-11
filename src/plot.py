"""Gráficos (nombres de archivo estables)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mt
import numpy as np
from . import config

C = {"CDT": "#2E86AB", "SP": "#E07A1F", "SPC": "#C0392B", "CORE": "#27AE60", "AP": "#7F8C8D"}
FOOT = "Fuentes: BanRep (DTF 90 días, TRM), DANE (IPC), Yahoo Finance (^SP500TR, ETF). Análisis educativo, no es recomendación."


def _style(ax):
    ax.grid(alpha=.25); ax.spines[["top", "right"]].set_visible(False)


def annual_bars(ar, last):
    fig, ax = plt.subplots(figsize=(15, 6.5))
    x = np.arange(len(ar)); w = .27
    ax.bar(x - w, ar["cdt_cop"] * 100, w, color=C["CDT"], label="CDT 90 días (DTF, COP)")
    ax.bar(x, ar["sp500tr_usd"] * 100, w, color=C["SP"], label="S&P 500 TR (USD)")
    ax.bar(x + w, ar["sp500tr_cop"] * 100, w, color=C["SPC"], label="S&P 500 TR en COP (con TRM)")
    ax.plot(x, ar["inflacion_col"] * 100, "k--", lw=1.2, marker=".", label="Inflación Colombia (IPC DANE)")
    lab = [str(y) if y < last.year else f"{y}\nYTD*" for y in ar.index]
    ax.set_xticks(x, lab, fontsize=8); ax.axhline(0, color="k", lw=.8)
    ax.yaxis.set_major_formatter(mt.PercentFormatter())
    ax.set_title("Retorno año a año: CDT vs S&P 500 (2000–2026)", fontsize=14, weight="bold")
    ax.legend(ncol=4, loc="upper left", fontsize=9, frameon=False); _style(ax)
    fig.text(.01, .01, f"*2026 hasta {last:%d-%m-%Y}. " + FOOT, fontsize=8, color="#555")
    fig.tight_layout(rect=(0, .03, 1, 1)); fig.savefig(config.OUTPUT / "cdt_vs_sp500_retornos_anuales.png", dpi=160); plt.close(fig)


def dca_curves(curves, cur, path, last):
    fig, axes = plt.subplots(1, 2, figsize=(16, 6.5))
    unit = 1e6 if cur == "cop" else 1e3
    ulab = "millones de COP" if cur == "cop" else "miles de USD"
    for ax, (lab, sim) in zip(axes, curves.items()):
        v = sim[cur] / unit
        ap = sim[f"flows_{cur}"].cumsum().reindex(v.index, method="ffill") / unit
        ax.plot(v.index, v["S&P 500 TR"], color=C["SP"], lw=1.6, label=f"S&P 500 TR: {v['S&P 500 TR'].iloc[-1]:,.0f}")
        ax.plot(v.index, v["CDT (DTF 90d)"], color=C["CDT"], lw=1.6, label=f"CDT 90 días: {v['CDT (DTF 90d)'].iloc[-1]:,.0f}")
        if "Core" in v:
            ax.plot(v.index, v["Core"], color=C["CORE"], lw=1.6, label=f"Core Alejandro: {v['Core'].iloc[-1]:,.0f}")
        ax.plot(ap.index, ap, color=C["AP"], lw=1.2, ls="--", label=f"Aportado: {ap.iloc[-1]:,.0f}")
        ax.set_yscale("log"); ax.set_ylabel(ulab + " (escala log)")
        ax.yaxis.set_major_formatter(mt.FuncFormatter(lambda y, _: f"{y:,.0f}" if y >= 1 else f"{y:,.2f}"))
        ttl = "Desde ene-2000" if lab == "2000-hoy" else "Desde may-2003 (con core)"
        ax.set_title(f"{ttl}: USD 1.000 + USD 200/mes", fontsize=12, weight="bold")
        ax.legend(loc="upper left", fontsize=9, frameon=False); _style(ax)
    sub = ("Inversionista colombiano: aporta en pesos a la TRM del día; S&P y core valorados en COP con la TRM"
           if cur == "cop" else "Todo medido en dólares (el CDT se convierte a USD con la TRM)")
    fig.suptitle(f"Patrimonio acumulado en {'pesos' if cur == 'cop' else 'dólares'}: CDT vs S&P 500 vs core — {sub}",
                 fontsize=12)
    fig.text(.01, .01, f"Corte {last:%d-%m-%Y}. Sin impuestos ni comisiones del CDT; core con 5 pb por lado. " + FOOT,
             fontsize=8, color="#555")
    fig.tight_layout(rect=(0, .03, 1, .95)); fig.savefig(path, dpi=160); plt.close(fig)


def rolling(roll, path, rr):
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    for ax, yrs in zip(axes, (5, 10)):
        g = roll[yrs] * 100
        ax.plot(g.index, g["S&P 500 TR COP"], color=C["SPC"], lw=1.5, label="S&P 500 TR en COP")
        ax.plot(g.index, g["CDT COP"], color=C["CDT"], lw=1.5, label="CDT 90 días (COP)")
        ax.plot(g.index, g["Core COP"], color=C["CORE"], lw=1.2, alpha=.85, label="Core (COP, desde 2003)")
        ax.axhline(0, color="k", lw=.8)
        p = rr[(rr["ventana_años"] == yrs) & (rr["comparación"] == "S&P 500 TR COP vs CDT COP")].iloc[0]
        ax.set_title(f"Retorno anual compuesto en ventanas de {yrs} años\nS&P en COP le gana al CDT en "
                     f"{p['pct_gana_bolsa']:.0%} de {p['n_ventanas']} ventanas", fontsize=12, weight="bold")
        ax.yaxis.set_major_formatter(mt.PercentFormatter()); ax.set_xlabel("Fin de la ventana")
        ax.legend(fontsize=9, frameon=False, loc="lower right"); _style(ax)
    fig.text(.01, .01, "Inversión única con inicio cada mes. " + FOOT, fontsize=8, color="#555")
    fig.tight_layout(rect=(0, .03, 1, 1)); fig.savefig(path, dpi=160); plt.close(fig)
