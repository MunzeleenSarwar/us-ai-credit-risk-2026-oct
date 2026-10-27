"""Extra credit risk models: Altman Z-prime, Springate, Zmijewski,
Merton distance to default, synthetic rating from interest coverage.
All money in USD millions, latest fiscal year, from saved financials."""
import pandas as pd, numpy as np, yfinance as yf, pathlib
from math import log, sqrt, erf
base = pathlib.Path(__file__).resolve().parents[1]
fin = pd.read_csv(base/"data"/"financials.csv")
lat = pd.read_csv(base/"data"/"latest.csv").set_index("ticker")
def norm_cdf(x): return 0.5*(1+erf(x/sqrt(2)))
def synthetic_rating(cov):
    bands = [(8.5,"AAA"),(6.5,"AA"),(5.5,"A+"),(4.25,"A"),(3.0,"A-"),(2.5,"BBB"),(2.0,"BB+"),(1.75,"BB"),(1.5,"B+"),(1.25,"B"),(0.8,"B-")]
    for cut, r in bands:
        if cov >= cut: return r
    return "CCC or lower"
rows = []
for tick, g in fin.sort_values("fiscal_year_end").groupby("ticker"):
    r = g.iloc[-1]; L = lat.loc[tick]
    ta, wc, re_, ebit, rev = r.total_assets, r.working_capital, r.retained_earnings, r.ebit, r.revenue
    eq, tl, cl = r.equity, r.total_liabilities, r.current_liabilities
    ni = r.net_income
    zprime = 6.56*(wc/ta) + 3.26*(re_/ta) + 6.72*(ebit/ta) + 1.05*(eq/tl) if ta and tl else np.nan
    pretax = ni  # proxy only if pretax missing; use EBIT as pretax proxy in Springate EBT term, stated in report
    springate = 1.03*(wc/ta) + 3.07*(ebit/ta) + 0.66*(ebit/cl) + 0.4*(rev/ta) if ta and cl else np.nan
    roa = ni/ta if ta else np.nan
    zm_score = -4.336 - 4.513*roa + 5.679*(tl/ta) + 0.004*(r.current_assets/cl) if ta and cl else np.nan
    zm_prob = 1/(1+np.exp(-zm_score)) if not np.isnan(zm_score) else np.nan
    # Merton: 1 year daily price volatility, market cap, default point = current liabilities + 0.5 x long term liabilities
    hist = yf.Ticker(tick).history(period="1y", auto_adjust=True)
    rets = np.log(hist["Close"]/hist["Close"].shift(1)).dropna()
    eq_vol = rets.std()*sqrt(252) if len(rets) > 50 else np.nan
    mcap = L.market_cap_usd_m
    V = mcap + tl
    sigma_a = eq_vol * (mcap/V) if V else np.nan
    default_point = cl + 0.5*(tl-cl)
    rf = 0.04
    dd = (log(V/default_point) + (rf - 0.5*sigma_a**2)) / sigma_a if sigma_a and default_point else np.nan
    edf = norm_cdf(-dd)*100 if not np.isnan(dd) else np.nan
    rows.append(dict(ticker=tick, company=r.company, fiscal_year_end=r.fiscal_year_end,
        altman_z=L.altman_z, altman_zprime=zprime, springate=springate,
        zmijewski_prob_pct=zm_prob*100 if not np.isnan(zm_prob) else np.nan,
        equity_vol_pct=eq_vol*100 if not np.isnan(eq_vol) else np.nan,
        asset_vol_pct=sigma_a*100 if not np.isnan(sigma_a) else np.nan,
        market_cap_usd_m=mcap, default_point_usd_m=default_point,
        merton_dd=dd, merton_edf_pct=edf,
        synthetic_rating=synthetic_rating(L.interest_coverage),
        ocf_to_debt=(r.operating_cash_flow/r.total_debt) if r.total_debt else np.nan,
        debt_to_assets=(r.total_debt/ta) if ta else np.nan,
        liabilities_to_assets=(tl/ta) if ta else np.nan))
df = pd.DataFrame(rows)
df.to_csv(base/"data"/"models.csv", index=False)
print(df[["ticker","altman_z","altman_zprime","springate","zmijewski_prob_pct","merton_dd","merton_edf_pct","synthetic_rating"]].to_string(index=False))
