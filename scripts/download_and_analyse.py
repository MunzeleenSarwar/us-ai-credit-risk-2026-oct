"""Download annual financials for 10 US-listed AI stocks via yfinance and
compute plain credit risk metrics. All money in USD millions unless stated."""
import pandas as pd, numpy as np, yfinance as yf, pathlib, json
base = pathlib.Path(__file__).resolve().parents[1]
TICKERS = {
 "NVDA": "NVIDIA", "MSFT": "Microsoft", "GOOGL": "Alphabet", "META": "Meta",
 "AVGO": "Broadcom", "TSM": "TSMC", "AMD": "AMD", "PLTR": "Palantir",
 "ORCL": "Oracle", "ASML": "ASML",
}
def get(df, row):
    if df is None or row not in df.index: return np.nan
    return df.loc[row]
rows = []
for tick, name in TICKERS.items():
    t = yf.Ticker(tick)
    bs, inc, cf = t.balance_sheet, t.financials, t.cashflow
    years = sorted(set(bs.columns) | set(inc.columns), reverse=True)
    for y in years:
        ystr = str(y)[:10]
        def v(df, row):
            if df is None or row not in df.index or y not in df.columns: return np.nan
            return df.loc[row, y]
        rev = v(inc, "Total Revenue"); ebit = v(inc, "EBIT"); ebitda = v(inc, "EBITDA")
        intexp = v(inc, "Interest Expense")
        if pd.isna(intexp): intexp = -v(inc, "Net Interest Income") if not pd.isna(v(inc, "Net Interest Income")) else np.nan
        if intexp is not None and intexp < 0: intexp = abs(intexp)
        debt = v(bs, "Total Debt"); cash = v(bs, "Cash Cash Equivalents And Short Term Investments")
        ca = v(bs, "Current Assets"); cl = v(bs, "Current Liabilities")
        ta = v(bs, "Total Assets"); eq = v(bs, "Stockholders Equity")
        wc = v(bs, "Working Capital"); re_ = v(bs, "Retained Earnings")
        tl = ta - eq if not pd.isna(ta) and not pd.isna(eq) else np.nan
        ocf = v(cf, "Operating Cash Flow"); fcf = v(cf, "Free Cash Flow")
        rows.append(dict(ticker=tick, company=name, fiscal_year_end=ystr,
            revenue=rev, ebit=ebit, ebitda=ebitda, interest_expense=intexp,
            net_income=v(inc, "Net Income"), total_debt=debt, cash=cash,
            current_assets=ca, current_liabilities=cl, total_assets=ta,
            equity=eq, working_capital=wc, retained_earnings=re_,
            total_liabilities=tl, operating_cash_flow=ocf, free_cash_flow=fcf))
df = pd.DataFrame(rows)
for c in df.columns[3:]:
    df[c] = df[c] / 1e6  # millions in reporting currency
# yfinance reports TSMC in TWD and ASML in EUR, despite info currency USD.
# Convert money columns to USD so cross-company amounts compare, using
# FX closes on 26 Oct 2026: TWD 32.562 per USD, EUR 1.1178 USD per EUR.
# Ratios are currency free and are unchanged by this conversion.
fx = {"TSM": 1/32.562, "ASML": 1.1178}
for tick, f in fx.items():
    cols = [c for c in df.columns if c not in ("ticker","company","fiscal_year_end")]
    df.loc[df.ticker == tick, cols] = df.loc[df.ticker == tick, cols] * f
df["reporting_currency"] = df.ticker.map({"TSM": "TWD", "ASML": "EUR"}).fillna("USD")
df.to_csv(base/"data"/"financials.csv", index=False)

m = df.copy()
m["debt_ebitda"] = m.total_debt / m.ebitda
m["net_debt_ebitda"] = (m.total_debt - m.cash) / m.ebitda
m["interest_coverage"] = m.ebit / m.interest_expense
m["current_ratio"] = m.current_assets / m.current_liabilities
m["cash_to_debt"] = m.cash / m.total_debt
m["debt_to_equity"] = m.total_debt / m.equity
m["fcf_to_debt"] = m.free_cash_flow / m.total_debt
m["net_debt"] = m.total_debt - m.cash
m.to_csv(base/"data"/"metrics.csv", index=False)

# Latest year per company, plus market cap for Altman Z
latest = []
for tick, g in m.sort_values("fiscal_year_end").groupby("ticker"):
    r = g.iloc[-1]
    info = yf.Ticker(tick).info
    mcap = info.get("marketCap", np.nan) / 1e6 if info.get("marketCap") else np.nan
    z = np.nan
    if pd.notna(r.total_assets) and r.total_assets:
        z = (1.2*(r.working_capital/r.total_assets) + 1.4*(r.retained_earnings/r.total_assets)
             + 3.3*(r.ebit/r.total_assets) + 0.6*(mcap/r.total_liabilities if pd.notna(r.total_liabilities) and r.total_liabilities else np.nan)
             + 1.0*(r.revenue/r.total_assets))
    latest.append(dict(ticker=tick, company=r.company, fiscal_year_end=r.fiscal_year_end,
        market_cap_usd_m=mcap, altman_z=z, **{k: r[k] for k in ["revenue","ebit","ebitda","interest_expense","total_debt","net_debt","cash","debt_ebitda","net_debt_ebitda","interest_coverage","current_ratio","cash_to_debt","debt_to_equity","fcf_to_debt"]}))
lat = pd.DataFrame(latest)
lat.to_csv(base/"data"/"latest.csv", index=False)
print(lat[["ticker","fiscal_year_end","total_debt","debt_ebitda","interest_coverage","current_ratio","altman_z"]].to_string())
print("years per ticker:\n", df.groupby("ticker").size())
