"""Charts for US AI credit risk. Colours are for charts only."""
import pandas as pd, numpy as np, matplotlib.pyplot as plt, pathlib
base = pathlib.Path(__file__).resolve().parents[1]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
lat = pd.read_csv(base/"data"/"latest.csv")
order = ["NVDA","GOOGL","MSFT","TSM","ASML","AMD","META","PLTR","AVGO","ORCL"]
lat = lat.set_index("ticker").loc[order].reset_index()

fig, ax = plt.subplots(figsize=(10,5.5))
ax.barh(lat.company, lat.debt_ebitda, color="#1f4e79")
ax.set_title("Total debt divided by EBITDA, latest fiscal year")
ax.set_xlabel("Times EBITDA"); ax.grid(axis="x", alpha=0.3); fig.tight_layout()
fig.savefig(base/"charts"/"debt_ebitda.png", dpi=200); plt.close(fig)

fig, ax = plt.subplots(figsize=(10,5.5))
ax.barh(lat.company, lat.net_debt/1000, color="#2e7d32")
ax.set_title("Net debt in USD billions, latest fiscal year (below zero means net cash)")
ax.set_xlabel("USD billions"); ax.grid(axis="x", alpha=0.3); fig.tight_layout()
fig.savefig(base/"charts"/"net_debt.png", dpi=200); plt.close(fig)

fig, ax = plt.subplots(figsize=(10,5.5))
ax.barh(lat.company, lat.interest_coverage, color="#7b4a12")
ax.set_xscale("log")
ax.set_title("Interest coverage, latest fiscal year (log scale, times)")
ax.set_xlabel("EBIT divided by interest expense, log scale"); ax.grid(axis="x", alpha=0.3)
for i, v in enumerate(lat.interest_coverage): ax.text(v*1.1, i, f"{v:.1f}x", va="center")
fig.tight_layout(); fig.savefig(base/"charts"/"interest_coverage.png", dpi=200); plt.close(fig)

m = pd.read_csv(base/"data"/"metrics.csv")
fig, ax = plt.subplots(figsize=(10,5.5))
for tick in order:
    g = m[m.ticker == tick].sort_values("fiscal_year_end")
    g = g[g.debt_ebitda.between(0, 10)]
    ax.plot(range(1, len(g)+1), g.debt_ebitda, marker="o", label=tick)
ax.set_title("Debt divided by EBITDA, oldest to latest fiscal year (5 years)")
ax.set_xlabel("Fiscal year, oldest to latest"); ax.set_ylabel("Times EBITDA")
ax.grid(alpha=0.3); ax.legend(ncol=5, fontsize=8); fig.tight_layout()
fig.savefig(base/"charts"/"debt_ebitda_trend.png", dpi=200); plt.close(fig)
mod = pd.read_csv(base/"data"/"models.csv").set_index("ticker").loc[order].reset_index()
fig, ax = plt.subplots(figsize=(10,5.5))
ax.barh(mod.company, mod.zmijewski_prob_pct, color="#8b1a1a")
ax.set_title("Zmijewski modelled probability, latest fiscal year (percent, model output, not a real default chance)")
ax.set_xlabel("%"); ax.grid(axis="x", alpha=0.3); fig.tight_layout()
fig.savefig(base/"charts"/"zmijewski_prob.png", dpi=200); plt.close(fig)

fig, ax = plt.subplots(figsize=(10,5.5))
ax.barh(mod.company, mod.merton_dd, color="#1f4e79")
ax.set_title("Merton distance to default, latest fiscal year (higher means safer)")
ax.set_xlabel("Standard deviations above the default point"); ax.grid(axis="x", alpha=0.3); fig.tight_layout()
fig.savefig(base/"charts"/"merton_dd.png", dpi=200); plt.close(fig)
print("charts done")
