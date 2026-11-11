"""Descarga y caché parquet de todas las series (BanRep, DANE, OCDE, FRED, Yahoo)."""
import io
import re
import subprocess
import pandas as pd
from . import config

C = config.CACHE
META = C / "fuentes_descarga.csv"
_meta_rows = []


def _log(name, url, rows, start, end, note=""):
    _meta_rows.append({"serie": name, "url": url, "filas": rows, "desde": start, "hasta": end,
                       "descargado_bogota": pd.Timestamp.now(tz="America/Bogota").strftime("%Y-%m-%d %H:%M"),
                       "nota": note})


def _curl(url, accept=None, insecure=False, timeout=180, ua=True) -> bytes:
    # curl: el certificado de totoro/suameca no valida en algunos entornos -> -k solo para BanRep
    cmd = ["curl", "-sSL", "--retry", "3", "-m", str(timeout)] + (["-A", "Mozilla/5.0"] if ua else [])
    if insecure:
        cmd.append("-k")
    if accept:
        cmd += ["-H", f"Accept: {accept}"]
    out = subprocess.run(cmd + [url], capture_output=True, check=True)
    return out.stdout


def _sdmx_series(url) -> pd.Series:
    xml = _curl(url, insecure=True).decode("utf-8")
    obs = re.findall(r'<generic:ObsDimension value="([^"]+)"\s*/><generic:ObsValue value="([^"]+)"\s*/>', xml)
    if not obs:
        raise RuntimeError(f"SDMX vacío: {url}")
    idx = [pd.Timestamp(d) if "-" in d and len(d) == 7 else pd.to_datetime(d, format="%Y%m%d") for d, _ in obs]
    return pd.Series([float(v) for _, v in obs], index=pd.DatetimeIndex(idx)).sort_index()


def _cached(name, fn, refresh):
    f = C / f"{name}.parquet"
    if f.exists() and not refresh:
        return pd.read_parquet(f)
    df = fn()
    df.to_parquet(f)
    return df


def dtf_daily(refresh=False) -> pd.Series:
    """DTF 90 días EA (%), BanRep, por día de vigencia (valor semanal constante lun-dom)."""
    def f():
        s = _sdmx_series(config.URL_DTF_DAILY)
        _log("DTF 90 días diaria (vigencia)", config.URL_DTF_DAILY, len(s), s.index.min().date(), s.index.max().date(),
             "BanRep SDMX DF_DTF_DAILY_HIST; % EA")
        return s.to_frame("dtf_ea")
    return _cached("dtf_daily", f, refresh)["dtf_ea"]


def dtf_monthly(refresh=False) -> pd.Series:
    def f():
        s = _sdmx_series(config.URL_DTF_MONTHLY)
        _log("DTF 90 días mensual", config.URL_DTF_MONTHLY, len(s), s.index.min().date(), s.index.max().date(),
             "BanRep SDMX DF_DTF_MONTHLY_HIST; % EA promedio mensual")
        return s.to_frame("dtf_ea")
    return _cached("dtf_monthly", f, refresh)["dtf_ea"]


def trm(refresh=False) -> pd.Series:
    """TRM COP/USD por día calendario de vigencia (BanRep SDMX); verificada contra datos.gov.co."""
    def f():
        s = _sdmx_series(config.URL_TRM)
        chk = pd.read_json(io.BytesIO(_curl(config.URL_TRM_CHECK + "?$order=vigenciadesde%20DESC&$limit=400")))
        chk["d"] = pd.to_datetime(chk["vigenciadesde"]).dt.tz_localize(None)
        diff = (chk.set_index("d")["valor"].astype(float) - s.reindex(chk["d"]).values).abs().max()
        assert diff < 0.01, f"TRM SDMX vs datos.gov.co difiere {diff}"
        _log("TRM COP/USD", config.URL_TRM, len(s), s.index.min().date(), s.index.max().date(),
             f"BanRep SDMX DF_TRM_DAILY_HIST; cruce con datos.gov.co 32sa-8pi3 (400 obs, dif. máx {diff:.4f})")
        return s.to_frame("trm")
    return _cached("trm", f, refresh)["trm"]


def ipc_col(refresh=False) -> pd.Series:
    """IPC Colombia mensual base dic-2018=100. DANE 2003-2026; 1999-11..2002-12 empalmado con OCDE (fuente DANE)."""
    def f():
        xls = config.REFS / "anex-IPC-Indices-oct2026.xlsx"
        if not xls.exists():
            config.REFS.mkdir(exist_ok=True)
            xls.write_bytes(_curl(config.URL_IPC_DANE))
        raw = pd.read_excel(xls, header=None)
        hdr = raw.index[raw.iloc[:, 0].astype(str).str.strip().eq("Mes")][0]
        years = raw.iloc[hdr, 1:].dropna()
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
                 "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        vals = {}
        for i, m in enumerate(meses):
            row = raw.index[raw.iloc[:, 0].astype(str).str.strip().eq(m)][0]
            for col, y in years.items():
                v = raw.iloc[row, col]
                if pd.notna(v) and str(v).strip() != "":
                    vals[pd.Timestamp(int(float(y)), i + 1, 1)] = float(v)
        dane = pd.Series(vals).sort_index()
        oecd = pd.read_csv(io.BytesIO(_curl(config.URL_IPC_OECD, accept="application/vnd.sdmx.data+csv; charset=utf-8")))
        oecd = pd.Series(oecd["OBS_VALUE"].values, index=pd.to_datetime(oecd["TIME_PERIOD"])).sort_index()
        ov = oecd.index.intersection(dane.index)
        ratio = dane[ov] / oecd[ov]
        k = ratio.loc["2003-01-01"]
        pre = oecd[oecd.index < dane.index.min()] * k
        s = pd.concat([pre, dane]).sort_index()
        _log("IPC Colombia (DANE)", config.URL_IPC_DANE, len(dane), dane.index.min().date(), dane.index.max().date(),
             "Anexo índices oct-2026, base dic-2018=100, publicado 9-nov-2026")
        _log("IPC Colombia 1999-11..2002-12 (OCDE, fuente DANE)", config.URL_IPC_OECD, len(pre),
             pre.index.min().date(), pre.index.max().date(),
             f"Empalme por razón en 2003-01; ratio DANE/OCDE solape 2003-2004 rango {ratio.min():.4f}-{ratio.max():.4f}")
        return s.to_frame("ipc")
    return _cached("ipc_col", f, refresh)["ipc"]


def cpi_us(refresh=False) -> pd.Series:
    def f():
        d = pd.read_csv(io.BytesIO(_curl(config.URL_CPI_US, ua=False, timeout=60)))
        s = pd.Series(d.iloc[:, 1].astype(float).values, index=pd.to_datetime(d.iloc[:, 0]))
        s = s[s.index >= "1999-01-01"]
        _log("CPI EE.UU. CPIAUCSL (BLS vía FRED)", config.URL_CPI_US, len(s), s.index.min().date(), s.index.max().date(),
             "SA, 1982-84=100")
        return s.to_frame("cpi")
    return _cached("cpi_us", f, refresh)["cpi"]


def prices(refresh=False) -> pd.DataFrame:
    def f():
        import yfinance as yf
        out = []
        for t in config.TICKERS:
            raw = yf.download(t, start=config.DATA_START, end=config.END_EXCLUSIVE, auto_adjust=True,
                              actions=False, progress=False, threads=False)
            c = raw["Close"]
            c = c.iloc[:, 0] if isinstance(c, pd.DataFrame) else c
            c = c.astype(float).rename(t)
            assert (c.dropna() > 0).all()
            out.append(c)
            _log(f"Yahoo {t}", f"https://finance.yahoo.com/quote/{t}/history", int(c.notna().sum()),
                 c.dropna().index.min().date(), c.dropna().index.max().date(),
                 f"cierre ajustado (auto_adjust=True), yfinance {yf.__version__}")
        p = pd.concat(out, axis=1).sort_index()
        p.index = pd.DatetimeIndex(p.index).tz_localize(None)
        return p
    return _cached("yahoo_adj_close", f, refresh)


def superfin_cdt_latest(refresh=False) -> pd.DataFrame:
    """Tasas de emisión de CDT por entidad (Superfinanciera, formato 441) para la última semana disponible."""
    def f():
        q = ("?$where=uca='1' AND fechacorte>='2026-11-01T00:00:00' AND subcuenta in('70','130')"
             "&$limit=5000")
        d = pd.read_json(io.BytesIO(_curl(config.URL_SFC_CAPTACION + q.replace(" ", "%20").replace("'", "%27"))))
        d["fechacorte"] = pd.to_datetime(d["fechacorte"]).dt.tz_localize(None)
        d["plazo"] = d["subcuenta"].astype(str).map({"70": "90 días", "130": "360 días"})
        _log("Superfinanciera tasas de captación CDT por entidad", config.URL_SFC_CAPTACION, len(d),
             d["fechacorte"].min().date(), d["fechacorte"].max().date(), "datos.gov.co axk9-g2nh, UCA 1")
        return d[["fechacorte", "tipoentidad", "nombreentidad", "plazo", "tasa", "monto"]]
    return _cached("superfin_cdt_nov2026", f, refresh)


def load_all(refresh=False):
    C.mkdir(exist_ok=True)
    data = dict(dtf=dtf_daily(refresh), dtf_m=dtf_monthly(refresh), trm=trm(refresh), ipc=ipc_col(refresh),
                cpi=cpi_us(refresh), px=prices(refresh), sfc=superfin_cdt_latest(refresh))
    if _meta_rows:
        pd.DataFrame(_meta_rows).to_csv(META, index=False)
    return data
