# Credit Risk Analysis: 10 AI Companies

## Question
Which of 10 US-listed AI companies carry the most credit risk, and how much room do they have if earnings fall?

## Answer in one paragraph
Most of the group carries very little credit risk. Eight of the ten hold more cash than debt, or debt below one year of EBITDA. Broadcom and Oracle are the watchlist names. Oracle is weakest, with debt at 4.67 times EBITDA and interest coverage of 5.3 times. NVIDIA is strongest, with debt at 0.08 times EBITDA and interest coverage of 547.1 times. Even if earnings fell 30%, every company in the group would still cover interest more than 3 times, but Oracle debt would rise to 6.67 times EBITDA.

## Tableau dashboard
Interactive dashboard on Tableau Public: [US AI Companies: Credit Risk Board](https://public.tableau.com/app/profile/munzeleen.sarwar/viz/USAICompaniesCreditRiskBoard/Dashboard1)

It shows the heatmap of debt to EBITDA, interest coverage, Altman Z and Altman Z-prime, ranked debt bars, a debt versus coverage scatter sized by market cap, 4-year debt trend lines, KPI information for Oracle, Broadcom and NVIDIA, and a 30 percent earnings shock bar chart. The Tableau-ready data and build guides are in tableau/ in this repo.

## Companies
NVIDIA (NVDA), Microsoft (MSFT), Alphabet (GOOGL), Meta (META), Broadcom (AVGO), TSMC (TSM), AMD (AMD), Palantir (PLTR), Oracle (ORCL), ASML (ASML). TSMC is Taiwan based and ASML is Netherlands based, both listed in the US.

## Files
- US_AI_Credit_Risk_Report.pdf: 10 page report, plain language, expanded with Altman Z-prime, Springate, Zmijewski, Merton distance to default and synthetic rating.
- US_AI_Credit_Risk_Model.xlsx: latest, models, trend, financials, method.
- US_AI_Credit_Risk_Notebook.ipynb: recomputation notebook.
- data/: financials, metrics, latest, models.
- charts/: debt to EBITDA, net debt, interest coverage, trend.
- scripts/: download and analysis, extra models, charts, Excel, report.
- tableau/: Tableau-ready heatmap, latest, stress scenario and history files, KPI file, build guide and rebuild spec for the dashboard linked above.

## Method and limits
Annual statements from yfinance, 5 fiscal years per company. Fiscal year ends differ. Money converted to USD, TSMC from Taiwan dollars at 32.562 per USD and ASML from euros at 1.1178 USD per euro, closes 26 Oct 2026. Altman Z uses current market capitalisation and is weak for cash rich technology companies, so it is not used alone for the ranking. This project is an investigation, not a credit rating and not personal investment advice.
