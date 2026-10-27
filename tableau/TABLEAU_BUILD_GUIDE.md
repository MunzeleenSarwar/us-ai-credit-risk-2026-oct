# Credit Risk Board: Tableau build guide

Companies, strongest to weakest: NVIDIA, Alphabet, Microsoft, TSMC, ASML, AMD, Meta, Palantir, Broadcom, Oracle.
Source: the latest year in data/latest.csv and data/models.csv. This board does not claim any company will default.

## Files in this folder
- tableau_credit_risk_latest.csv: one row per company, with the raw inputs Tableau needs for calculations. Use this for the shock slider.
- tableau_credit_risk_heatmap_long.csv: one row per company per metric, ready for a heatmap. Use this for the main heatmap.
- tableau_credit_risk_stress_scenarios.csv: precomputed shocks at 0, 10, 20, 30 and 50 percent. Use this if you do not want to build the parameter yet.
- tableau_credit_risk_history.csv: 40 rows, 4 usable years per company. The earliest year in the source metrics file is blank for every company and was skipped, so do not present this as 5 full years.

## 1. Heatmap sheet
Connect to tableau_credit_risk_heatmap_long.csv.
- Rows: Company, sorted by rank_strongest_to_weakest, lowest number at the top.
- Columns: Metric, in this order: Debt / EBITDA, Interest coverage, Altman Z, Altman Z-prime.
- Colour: risk_band. Do not colour by the raw value.
- Label: value.
- Tooltip: company, metric, value, risk_band.

Why colour by band: two values would wash out everything else if you colour by raw value. NVIDIA interest coverage is 547.1x and Palantir Altman Z is 190.91. The capped column, value_for_colour_capped, is there if you prefer a numeric colour scale: coverage capped at 50, Altman Z capped at 20, Z-prime capped at 10, Debt / EBITDA capped at 5. The label still shows the true value.

Risk bands used in the files:
- Debt / EBITDA: Low at 1 or below, Watch from 1 to 3, High above 3.
- Interest coverage: Strong at 10 or above, Watch from 4 to 10, Weak below 4.
- Altman Z: Safe above 2.99, Grey zone from 1.81 to 2.99, Distress zone below 1.81.
- Altman Z-prime: Safe above 2.6, Grey zone from 1.1 to 2.6, Distress zone below 1.1.

What the heatmap should show at first glance:
- Oracle is the only High debt company at 4.67x, with coverage of 5.3x and Altman Z of 1.61 in the distress zone.
- Broadcom is next at 1.88x debt and 8.1x coverage.
- NVIDIA is lowest debt at 0.08x with 547.1x coverage.
- Altman Z alone is weak for cash-rich tech companies. That is why Z-prime is on the same board as a cross-check, and why the report also uses Springate, Zmijewski, Merton distance to default and a synthetic rating.

## 2. Earnings shock slider
Connect to tableau_credit_risk_latest.csv.
Create a parameter called Earnings shock, as a float, from 0 to 0.5, step 0.1, shown as a percent. Set the default to 0.3 so the board opens on the 30 percent case you asked for.

Create these calculated fields, exactly:
- Stressed EBITDA = [ebitda_usd_m] * (1 - [Earnings shock])
- Stressed EBIT = [ebit_usd_m] * (1 - [Earnings shock])
- Stressed interest coverage = [Stressed EBIT] / [interest_expense_usd_m]
- Stressed Debt / EBITDA = [total_debt_usd_m] / [Stressed EBITDA]

Rules for the shock, stated on the dashboard:
- Only earnings fall. Debt and interest expense stay fixed.
- At 30 percent, Oracle coverage falls from 5.3x to 3.7x and Oracle debt rises from 4.67x to 6.67x EBITDA. Every other company still covers interest more than 4 times at 30 percent.
- At 20 percent, Oracle is at 5.84x debt and 4.24x coverage. At 50 percent, Oracle is at 9.34x debt and 2.65x coverage.

Build two small tables or bar charts from those fields, one for stressed coverage and one for stressed debt, sorted so Oracle and Broadcom sit at the risky end. Add the parameter control to the dashboard so moving it updates both charts.

## 3. Dashboard layout, top to bottom
- Title: US AI Companies: Credit Risk Board
- One line under the title: 10 companies, latest fiscal year, debt and interest held fixed in the shock.
- KPI row: weakest company (Oracle, 4.67x debt, 5.3x coverage, Z 1.61), second weakest (Broadcom, 1.88x debt, 8.1x coverage), strongest (NVIDIA, 0.08x debt, 547.1x coverage).
- Main heatmap.
- Shock slider on the right, with the two stressed charts below the heatmap.
- A notes box: Altman Z is weak for cash-rich tech, fiscal year ends differ by company, TSMC and ASML figures were converted to USD in the source project, and no default is predicted.

## 4. Publishing later
This tableau folder is ready to add to the AI credit risk GitHub repo together with the report and Python files, when you create that repo. Do not publish the Tableau workbook to Tableau Public until you have checked that you are happy for all of these company figures to be public. The source data is public company financial data, not personal data.
