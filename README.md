# CDT vs S&P 500 en Colombia (2000–2026): ¿13 % "seguro" o bolsa?

> *"¿Para qué invierto en bolsa si el CDT me da 13 % este año y el S&P 500 da 10 %?"*

Este repositorio compara, con datos oficiales, el **CDT a 90 días** (DTF del Banco de la República) con el **S&P 500 con dividendos reinvertidos** y con el **core** de mi portafolio, entre 2000 y 2026. Revisa tres cosas que el comentario no tiene en cuenta: el **retorno acumulado**, la **historia de las tasas de los CDT** y la **variabilidad de la bolsa**. También simula a alguien que invierte **USD 1.000 al inicio y USD 200 al mes** desde enero de 2000.

**Corte de datos:** 10-nov-2026, el último cierre completo de Wall Street. TRM de ese día: $3.269,88.

## Aviso

Es un análisis **educativo**, no una recomendación de inversión. Los resultados son históricos y no garantizan nada a futuro. El core se arma con los **pesos de hoy aplicados al pasado**, así que tiene sesgo de selección retrospectiva: nadie sabía en 2003 que esos activos iban a salir tan bien.

## Reglas del ejercicio

| Elemento | Regla |
|---|---|
| CDT | DTF a 90 días (% EA), BanRep. Cada aporte abre un CDT que se **renueva cada 90 días a la DTF vigente al inicio de cada plazo**, sin mirar el futuro. Dentro del plazo el interés se causa día a día. Sin comisiones. |
| S&P 500 | Índice **^SP500TR**, retorno total con dividendos reinvertidos, en USD (Yahoo). No descuenta la comisión de un fondo: SPY cobra 0,0945 % al año. |
| Core | SPYG 31 %, SMH 22 %, BRK-B 20 %, IEMG 20 % y VTI 7 % (precio ajustado de Yahoo). Se rebalancea cada mes el día del aporte, con costo de 5 pb por lado sobre lo negociado. IEMG nace en oct-2012, así que antes se usa **EEM** (desde 14-abr-2003). En el solape la correlación diaria es 0,997 y la mensual 0,998, e IEMG rindió 0,63 pp más al año. El core arranca el **14-abr-2003**, cuando ya existen todos sus componentes. |
| Aportes | USD 1.000 el primer día hábil de ene-2000 (o de may-2003) y USD 200 el primer día hábil de cada mes. |
| Moneda (escenario principal) | **Inversionista colombiano en pesos.** Aporta el equivalente en COP a la TRM del día. El CDT rinde en COP; el S&P y el core se valoran en COP con la TRM del día, así que incluyen el efecto de la devaluación o revaluación. |
| Moneda (escenario secundario) | Todo medido en USD: el CDT se convierte con la TRM. |
| Retornos reales | Se descuenta el IPC de Colombia (DANE) en COP y el CPI de EE.UU. (FRED) en USD. |
| Impuestos | El escenario base es **bruto**. La sensibilidad aplica una **retención en la fuente del 4 %** sobre los rendimientos del CDT (DUR 1625/2016, art. 1.2.4.2.83) y otra con la histórica: 7 % hasta oct-2013 y 4 % desde el Decreto 2418/2013. Las ganancias en bolsa en el exterior tributan distinto y **no se modelan**. |

## Hallazgo principal

### 1) Simulación: USD 1.000 + USD 200/mes (escenario en pesos)

| Desde | Estrategia | Aportado (COP) | Valor final (COP) | Veces lo aportado | XIRR nominal | XIRR real (IPC) | Máx. caída del patrimonio |
|---|---|---:|---:|---:|---:|---:|---:|
| ene-2000 | CDT 90 días | $181,7 M | **$449,6 M** | 2,47× | 6,66 % | 1,42 % | 0 % |
| ene-2000 | CDT con retención 4 % | $181,7 M | $431,7 M | 2,38× | 6,39 % | 1,16 % | 0 % |
| ene-2000 | S&P 500 TR | $181,7 M | **$1.302,9 M** | 7,17× | 13,17 % | 7,69 % | −37,7 % |
| may-2003 | CDT 90 días | $163,7 M | $354,1 M | 2,16× | 6,61 % | 1,35 % | 0 % |
| may-2003 | S&P 500 TR | $163,7 M | $1.039,1 M | 6,35× | 14,31 % | 8,82 % | −33,5 % |
| may-2003 | **Core** | $163,7 M | **$1.366,0 M** | 8,34× | 16,14 % | 10,58 % | −38,7 % |

En dólares el aporte es el mismo, USD 65.400 desde 2000 y USD 57.400 desde 2003:

| Desde | Estrategia | Valor final (USD) | XIRR (USD) | Máx. caída del patrimonio (USD) |
|---|---|---:|---:|---:|
| ene-2000 | CDT 90 días | 137.486 | 5,04 % | −38,3 % |
| ene-2000 | S&P 500 TR | 398.461 | 11,40 % | −47,9 % |
| may-2003 | CDT 90 días | 108.280 | 4,97 % | −36,2 % |
| may-2003 | S&P 500 TR | 317.781 | 12,46 % | −43,2 % |
| may-2003 | Core | 417.746 | 14,26 % | −47,8 % |

**El CDT sí fue adelante durante mucho tiempo.** En la simulación desde 2000 (en pesos), el patrimonio en CDT superó al del S&P de oct-2000 a jul-2014, salvo un mes. Fueron casi 14 años, por la crisis puntocom, la de 2008 y la revaluación del peso entre 2003 y 2012. El S&P lo pasó en 2014 y la ventaja se amplió después. Contra el core (desde 2003), el CDT fue adelante en varios tramos entre 2004 y sep-2013.

Los aportes en COP son nominales: $181,7 M de distintos años equivalen a unos **$361,5 M en pesos de oct-2026**. El "valor final" del CDT es bruto, salvo en la fila con retención.

### 2) Retornos anuales: resumen 2000–2026

| Serie | Acumulado | CAGR | CAGR real aprox. | Volatilidad anual | Peor año | Mejor año | Años negativos | Máx. drawdown |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| CDT 90 días (COP) | +522 % | 7,0 % | 1,6 % | 3,0 % | 2,0 % (2021) | 13,4 % (2023) | 0 de 26 | 0 % |
| S&P 500 TR (USD) | +735 % | 8,2 % | — | 18,0 % | −37,0 % (2008) | 32,4 % (2013) | 6 de 26 | −55,3 % |
| S&P 500 TR (COP) | +1.357 % | 10,5 % | 4,9 % | 19,4 % | −29,8 % (2008) | 49,3 % (2021) | 6 de 26 | −45,5 % |
| CDT medido en USD | +256 % | 4,8 % | — | 14,8 % | −20,7 % (2015) | 42,7 % (2023) | 11 de 26 | −46,5 % |
| Core (COP, desde 14-abr-2003) | +2.106 % | 14,0 % | 8,2 % | 20,6 % | −33,2 % (2008) | 48,4 % (2024) | 4 de 22 | −46,6 % |

Para comparar en el mismo periodo, desde el **14-abr-2003**: CDT 6,5 %, S&P 500 TR en COP 12,1 % y core en COP 14,0 % de CAGR.

En la tabla, "CAGR real aprox." descuenta el IPC de Colombia hasta oct-2026: 5,4 % anual desde dic-1999 y 4,9 % desde abr-2003. La volatilidad y los peores y mejores años usan solo años completos: 2000–2025, y 2004–2025 para el core.

### 3) Tabla año a año

| Año | DTF prom. EA | CDT (COP) | S&P TR (USD) | S&P TR (COP) | Core (COP) | Inflación COL | Devaluación TRM |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2000 | 12,1 % | 12,9 % | −9,1 % | 8,1 % | — | 8,8 % | 19,0 % |
| 2001 | 12,4 % | 12,7 % | −11,9 % | −9,4 % | — | 7,6 % | 2,8 % |
| 2002 | 8,9 % | 9,5 % | −22,1 % | −2,6 % | — | 7,0 % | 25,0 % |
| 2003 | 7,8 % | 7,8 % | 28,7 % | 24,8 % | 33,7 %* | 6,5 % | −3,0 % |
| 2004 | 7,8 % | 7,9 % | 10,9 % | −4,6 % | −10,9 % | 5,5 % | −14,0 % |
| 2005 | 7,0 % | 7,2 % | 4,9 % | 0,3 % | 5,2 % | 4,8 % | −4,4 % |
| 2006 | 6,3 % | 6,2 % | 15,8 % | 13,5 % | 10,7 % | 4,5 % | −2,0 % |
| 2007 | 8,0 % | 7,7 % | 5,5 % | −5,1 % | 3,9 % | 5,7 % | −10,0 % |
| 2008 | 9,7 % | 9,3 % | −37,0 % | −29,8 % | −33,2 % | 7,7 % | 11,4 % |
| 2009 | 6,1 % | 7,0 % | 26,5 % | 15,2 % | 27,0 % | 2,0 % | −8,9 % |
| 2010 | 3,7 % | 3,9 % | 15,1 % | 7,7 % | 11,2 % | 3,2 % | −6,4 % |
| 2011 | 4,2 % | 4,0 % | 2,1 % | 3,6 % | −3,0 % | 3,7 % | 1,5 % |
| 2012 | 5,4 % | 5,3 % | 16,0 % | 5,6 % | 4,7 % | 2,4 % | −9,0 % |
| 2013 | 4,2 % | 4,4 % | 32,4 % | 44,3 % | 36,2 % | 1,9 % | 9,0 % |
| 2014 | 4,1 % | 4,0 % | 13,7 % | 41,2 % | 44,6 % | 3,7 % | 24,2 % |
| 2015 | 4,6 % | 4,3 % | 1,4 % | 33,5 % | 26,7 % | 6,8 % | 31,6 % |
| 2016 | 6,8 % | 6,4 % | 12,0 % | 6,7 % | 12,0 % | 5,7 % | −4,7 % |
| 2017 | 6,0 % | 6,2 % | 21,8 % | 21,2 % | 29,6 % | 4,1 % | −0,6 % |
| 2018 | 4,7 % | 4,8 % | −4,4 % | 4,1 % | 3,8 % | 3,2 % | 8,9 % |
| 2019 | 4,5 % | 4,5 % | 31,5 % | 32,6 % | 32,0 % | 3,8 % | 0,8 % |
| 2020 | 3,4 % | 3,8 % | 18,4 % | 24,0 % | 33,4 % | 1,6 % | 4,7 % |
| 2021 | 2,1 % | 2,0 % | 28,7 % | 49,3 % | 46,6 % | 5,6 % | 16,0 % |
| 2022 | 8,5 % | 7,1 % | −18,1 % | −1,1 % | −5,1 % | 13,1 % | 20,8 % |
| 2023 | 13,2 % | 13,4 % | 26,3 % | 0,3 % | 4,8 % | 9,3 % | −20,5 % |
| 2024 | 10,2 % | 10,7 % | 25,0 % | 44,2 % | 48,4 % | 5,2 % | 15,4 % |
| 2025 | 9,0 % | 9,0 % | 17,9 % | 0,4 % | 9,1 % | 5,1 % | −14,8 % |
| 2026 (YTD**) | 10,0 % | 8,2 % | 10,9 % | −3,5 % | 2,3 % | 5,9 % | −13,0 % |

\* El core de 2003 es parcial: va del 14-abr al 31-dic de 2003.
\*\* El año 2026 llega hasta el 10-nov. La DTF promedio cubre ene–oct y la inflación es el año corrido a octubre (DANE: 5,94 %).

En 13 de los 27 años el CDT le ganó al S&P 500 medido en pesos: 2000–2002, 2004, 2005, 2007, 2008, 2011, 2018, 2022, 2023, 2025 y 2026 YTD. En casi todos coinciden una caída de la bolsa o una **revaluación del peso**.

### 4) Ventanas rodantes (inversión única que empieza cada mes)

| Ventana | Comparación | Ventanas | % en que gana la bolsa | Peor CAGR de la bolsa | Mejor CAGR de la bolsa | Rango del CDT |
|---|---|---:|---:|---:|---:|---:|
| 5 años | S&P TR en COP vs CDT | 264 | 61 % | −7,6 % | 28,9 % | 4,0–10,1 % |
| 5 años | Core en COP vs CDT | 224 | 73 % | −6,8 % | 29,4 % | 4,0–9,7 % |
| 10 años | S&P TR en COP vs CDT | 204 | 71 % | −3,7 % | 25,5 % | 4,5–8,8 % |
| 10 años | Core en COP vs CDT | 164 | 90 % | +3,0 % | 26,1 % | 4,5–7,0 % |

Ojo: en la ventana de 5 años más reciente, de nov-2021 a nov-2026, el **CDT (9,7 %) le gana al S&P en COP (7,6 %)**, porque el peso se revaluó en 2023, 2025 y 2026.

### 5) Momentos de estrés

| Periodo | CDT (COP) | S&P TR (USD) | S&P TR (COP) | Core (COP) |
|---|---:|---:|---:|---:|
| 2000–2002 (puntocom) | +39,3 % | −37,6 % | −4,6 % | — |
| 2008 | +9,3 % | −37,0 % | −29,8 % | −33,2 % |
| Caída covid (20-feb a 23-mar-2020) | +0,4 % | −33,8 % | −20,8 % | −17,7 % |
| 2020, año completo | +3,8 % | +18,4 % | +24,0 % | +33,4 % |
| 2022 | +7,1 % | −18,1 % | −1,1 % | −5,1 % |

En las crisis la devaluación del peso amortigua la caída del S&P medido en COP: el dólar suele subir cuando la bolsa cae.

### 6) ¿Es cierto el "13 % vs 10 %"?

| Dato | Valor | Fuente |
|---|---:|---|
| DTF 90 días vigente (9 al 15 de nov-2026) | **10,79 % EA** | BanRep |
| CDT a 90 días, promedio ponderado del sistema (3 al 9 de nov-2026) | 10,74 % EA. La entidad más alta paga 12,50 % | Superfinanciera (datos.gov.co) |
| CDT a 360 días, promedio ponderado del sistema (3 al 9 de nov-2026) | 12,24 % EA. Las más altas pagan 13,2–13,3 % (RCI 13,30 %, Pichincha 13,28 %) y el 22,5 % de las 40 entidades paga 13 % o más | Superfinanciera (datos.gov.co) |
| Rendimiento real de un CDT a 90 días renovado en 2026 (YTD al 10-nov) | 8,2 % | Cálculo propio con la DTF |
| S&P 500 en 2026 (solo precio, ^GSPC, YTD) | 9,9 % | Yahoo |
| S&P 500 TR en 2026 (USD, YTD) | 10,9 % | Yahoo |
| **S&P 500 TR en 2026 medido en pesos (YTD)** | **−3,5 %** | Yahoo + TRM: de 3.757,08 a 3.269,88, −13,0 % |

**Veredicto:** el 13 % existe, pero en CDT a 360 días de algunas entidades, no como tasa típica: el promedio del sistema es 12,2 % a un año y 10,8 % a 90 días. Además, es la tasa que se pacta **hoy** para el próximo año, no lo que un CDT rindió en 2026. El "10 %" del S&P es correcto **en dólares**. En pesos, el S&P **pierde** en 2026 porque el peso se revaluó 13 %. Así que este año, en pesos, tu amigo tiene razón. El problema es sacar una conclusión de largo plazo con un solo año.

## Gráficos

![Retornos anuales CDT vs S&P 500](output/cdt_vs_sp500_retornos_anuales.png)

![Patrimonio DCA en pesos](output/cdt_vs_sp500_dca_cop.png)

![Patrimonio DCA en dólares](output/cdt_vs_sp500_dca_usd.png)

![Ventanas rodantes 5 y 10 años](output/cdt_vs_sp500_ventanas_rodantes.png)

## Cómo leer los gráficos

- `output/cdt_vs_sp500_retornos_anuales.png`: barras por año con el CDT (azul), el S&P en USD (naranja) y el S&P en COP (rojo), más la inflación de Colombia (línea punteada). El CDT nunca es negativo; el S&P va de −37 % a +49 %.
- `output/cdt_vs_sp500_dca_cop.png`: el patrimonio en pesos, en escala logarítmica, con la línea gris de lo aportado. A la izquierda arranca en 2000 y a la derecha en 2003, con el core. Se ve el tramo en que el CDT iba adelante.
- `output/cdt_vs_sp500_dca_usd.png`: lo mismo medido en dólares. Ahí el CDT también tiene caídas, por la devaluación.
- `output/cdt_vs_sp500_ventanas_rodantes.png`: el CAGR de 5 y de 10 años según la fecha en que termina cada ventana.

## Stack

Python 3.13: pandas, numpy, scipy (XIRR), matplotlib, yfinance y pyarrow (caché parquet).

```
src/config.py    parámetros, pesos, URLs de las fuentes
src/data.py      descarga y caché parquet (BanRep SDMX, DANE, OCDE, FRED, Yahoo, Superfinanciera)
src/engine.py    CDT con renovación cada 90 días, empalme EEM→IEMG, índice del core, simulación DCA
src/metrics.py   XIRR, CAGR, drawdown, resumen anual
src/plot.py      gráficos con nombres de archivo estables
main.py          orquesta todo y escribe output/
tests/verify.py  pruebas del motor
analisis.ipynb   notebook ejecutado con tablas y gráficos
```

## Cómo correr

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python main.py             # la primera vez descarga todo a cache/ (no versionado); luego usa la caché
python main.py --refresh   # vuelve a descargar todas las fuentes
python tests/verify.py
```

## Metodología

1. **DTF**: BanRep SDMX `DF_DTF_DAILY_HIST`, que es la serie diaria por vigencia: semanal y constante de lunes a domingo. Se usa la DTF y no la "tasa CDT 90 días total sistema" porque es la serie oficial más larga y homogénea desde 1984. Además, la DTF **es** el promedio ponderado de las captaciones por CDT a 90 días de bancos, corporaciones financieras y compañías de financiamiento. Para el promedio anual se usa la serie mensual `DF_DTF_MONTHLY_HIST`.
2. **CDT**: el valor en el día *t* de un plazo que empezó en *t₀* a la tasa *r* es V·(1+r)^((t−t₀)/365). Cada 90 días se capitaliza y se renueva a la DTF vigente ese día. Con retención, el interés de cada plazo se multiplica por (1−4 %).
3. **TRM**: BanRep SDMX `DF_TRM_DAILY_HIST`, cruzada con datos.gov.co `32sa-8pi3` en 400 observaciones con diferencia de 0,00.
4. **IPC Colombia**: anexo de índices del DANE de oct-2026 (2003–2026, base dic-2018=100). Para nov-1999 a dic-2002 se usa la serie de la OCDE, cuya fuente es el DANE, empalmada por razón en ene-2003; la razón en el solape es estable, entre 0,8555 y 0,8557. Verificación: inflación de 2000 = 8,75 %, de 2001 = 7,65 % y de 2002 = 6,99 %, iguales a las oficiales.
5. **XIRR** con fechas reales de los flujos. El XIRR real expresa cada aporte en pesos de oct-2026 con el IPC.
6. **Máxima caída del patrimonio**: la caída desde el pico del valor de la cuenta, que incluye los aportes. Por eso es menor que el drawdown del índice, que también se reporta.

## Limitaciones

- **Selección retrospectiva del core**: SMH y SPYG se eligieron conociendo la década tecnológica, así que el resultado del core es optimista.
- **La DTF es un promedio**. Un ahorrador real puede conseguir más, por ejemplo con CDT a 360 días o en entidades pequeñas, o menos, por ejemplo con montos bajos en bancos grandes. No se modela el seguro de Fogafín ni el riesgo de cada entidad.
- **El 2026 es parcial**, y la inflación de 2026 va hasta octubre.
- **Impuestos**: no se modela el componente inflacionario no gravado de los rendimientos financieros, ni el impuesto de renta final, ni el tratamiento de dividendos o ganancias en el exterior. Tampoco los costos de enviar dólares al exterior: spread cambiario, comisiones de giro y de bróker.
- **^SP500TR** no es un fondo invertible. Un ETF real resta su comisión anual y, para un no residente en EE.UU., la retención del 30 % sobre los dividendos (15 % con tratado; Colombia no tiene tratado con EE.UU.). Eso reduciría el S&P y el core en cerca de 0,4–0,5 pp al año, una **estimación no modelada**.
- Antes de 2011 SMH era un HOLDRS. Se usa el precio ajustado de Yahoo tal como viene.

## Fuentes (descargadas el 11-nov-2026)

Ver `output/fuentes_descarga.csv`.

- BanRep SDMX, DTF diaria: https://totoro.banrep.gov.co/nsi-jax-ws/rest/data/ESTAT,DF_DTF_DAILY_HIST,1.0/all/ALL/ · DTF mensual: `DF_DTF_MONTHLY_HIST` · TRM: `DF_TRM_DAILY_HIST`. Guía técnica: https://suameca.banrep.gov.co/archivos/webservices/documento_tecnico_ws_consumo_sdmx_dtf.pdf
- TRM, cruce: https://www.datos.gov.co/resource/32sa-8pi3.json
- Superfinanciera, tasas de captación por entidad: https://www.datos.gov.co/resource/axk9-g2nh.json
- DANE IPC: https://www.dane.gov.co/files/operaciones/IPC/oct2026/anex-IPC-Indices-oct2026.xlsx
- OCDE, IPC de Colombia 1999–2002: https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_PRICES@DF_PRICES_ALL,1.0/COL.M.N.CPI.IX._T.N._Z
- FRED CPIAUCSL: https://fred.stlouisfed.org/series/CPIAUCSL
- Yahoo Finance: ^SP500TR, ^GSPC, SPYG, SMH, BRK-B, IEMG, EEM, VTI
- Retención del 4 % sobre títulos de renta fija: DUR 1625/2016, art. 1.2.4.2.83 (https://estatuto.co/dur/1.2.4.2.83)

## Autor

**Andrés Alejandro Rodríguez Lozano**, economista y científico de datos.
Web: [andalejo1109.github.io](https://andalejo1109.github.io) · eToro: [@Andalejo1109](https://www.etoro.com/people/andalejo1109)

## Licencia

MIT. Ver `LICENSE`.
