"""Parámetros del estudio CDT vs S&P 500 vs core (Colombia, 2000-2026)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "cache"
OUTPUT = ROOT / "output"
REFS = ROOT / "refs"

# Fechas
DATA_START = "1999-12-01"
END_EXCLUSIVE = "2026-11-11"     # última sesión cerrada usada: 2026-11-10 (hoy 11-nov intradía se excluye)
DCA_START_FULL = "2000-01-01"    # primer día hábil NYSE del mes -> 2000-01-03
DCA_START_CORE = "2003-05-01"    # primer mes completo con todos los ETF del core (EEM desde 2003-04-14)

# Aportes (USD; en el escenario COP se convierten a la TRM del día)
INITIAL_USD = 1_000.0
MONTHLY_USD = 200.0

# CDT: renovación a 90 días a la DTF vigente al inicio de cada plazo (sin look-ahead)
CDT_TERM_DAYS = 90
RETENTION_SCENARIOS = {
    "bruto": None,                 # sin retención
    "ret4": 0.04,                  # 4 % plano (DUR 1625/2016 art. 1.2.4.2.83; Decreto 2418/2013)
    "ret_hist": "hist",            # 7 % hasta 2013-10-31, 4 % desde 2013-11-01
}
RET_HIST_SWITCH = "2013-11-01"

# Core de Alejandro (pesos de hoy aplicados al pasado -> selección retrospectiva)
CORE_WEIGHTS = {"SPYG": 0.31, "SMH": 0.22, "BRK-B": 0.20, "EMG": 0.20, "VTI": 0.07}
EM_SPLICE_DATE = "2012-10-25"    # EEM hasta 2012-10-24, IEMG desde aquí
COST_BPS = 5.0                   # por lado, sobre el monto negociado en cada rebalanceo/aporte

SP_TR = "^SP500TR"
SP_PRICE = "^GSPC"
TICKERS = [SP_TR, SP_PRICE, "SPY", "SPYG", "SMH", "BRK-B", "IEMG", "EEM", "VTI"]

# Fuentes
URL_DTF_DAILY = "https://totoro.banrep.gov.co/nsi-jax-ws/rest/data/ESTAT,DF_DTF_DAILY_HIST,1.0/all/ALL/"
URL_DTF_MONTHLY = "https://totoro.banrep.gov.co/nsi-jax-ws/rest/data/ESTAT,DF_DTF_MONTHLY_HIST,1.0/all/ALL/"
URL_TRM = "https://totoro.banrep.gov.co/nsi-jax-ws/rest/data/ESTAT,DF_TRM_DAILY_HIST,1.0/all/ALL/"
URL_TRM_CHECK = "https://www.datos.gov.co/resource/32sa-8pi3.json"
URL_SFC_CAPTACION = "https://www.datos.gov.co/resource/axk9-g2nh.json"
URL_IPC_DANE = "https://www.dane.gov.co/files/operaciones/IPC/oct2026/anex-IPC-Indices-oct2026.xlsx"
URL_IPC_OECD = ("https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_PRICES@DF_PRICES_ALL,1.0/"
                "COL.M.N.CPI.IX._T.N._Z?startPeriod=1999-11&endPeriod=2004-12")
URL_CPI_US = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCSL"
