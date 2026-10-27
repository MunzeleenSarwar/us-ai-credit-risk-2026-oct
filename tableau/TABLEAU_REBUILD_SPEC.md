# Polished rebuild spec: US AI Companies Credit Risk Board

Problem with the first published version, found by live inspection 26 Oct 2026: Dashboard 1 was one small heatmap in the top-left, most of the canvas blank white, company column truncated, no KPI tiles, filters, second chart type or layout design, and the shock view was only a plain text table. The heatmap data itself was correct, all 40 cells rendered.

## New dashboard layout, fill the whole canvas
Top, full width:
- Title: US AI Companies: Credit Risk Board
- Subtitle: 10 US-listed AI companies, strongest to weakest. Debt and interest are held fixed in the shock view, only earnings fall.
- Company filter, applied to the heatmap, ranked bars, scatter and trend views. Default: all companies.

Second row, KPI tiles, three tiles across:
- Weakest: Oracle, 4.67x debt to EBITDA, 5.3x coverage, Altman Z 1.61 distress zone.
- Watch: Broadcom, 1.88x debt, 8.1x coverage.
- Strongest: NVIDIA, 0.08x debt, 547.1x coverage.
Source file: tableau_dashboard_kpi.csv, or a text tile built from tableau_credit_risk_latest.csv.

Third row, main area:
- Left, large: heatmap, Company rows sorted by rank strongest to weakest, Metric columns Debt / EBITDA, Interest coverage, Altman Z, Altman Z-prime, colour by risk_band, label by true value. Make the company column wide enough that no name is truncated to Comp..
- Right: ranked horizontal bars for Debt / EBITDA, highest at the top, Oracle first, with values labelled. Colour by risk band if possible, otherwise a single clear colour with Oracle highlighted by the label.

Fourth row:
- Left: scatter, x = Debt / EBITDA, y = Interest coverage, bubble size = market cap from tableau_credit_risk_latest.csv, bubble label = company. Oracle should stand out in the high debt, low coverage corner. Cap the y axis or use the capped coverage value for display if NVIDIA 547.1x flattens the rest, and say so in the tooltip.
- Right: trend lines over the 4 usable years in tableau_credit_risk_history.csv, one line per company or a company filter, for Debt / EBITDA. Note in the dashboard: earliest year in the source was blank and was skipped, so this is 4 years, not 5.

Fifth row:
- Shock chart, not a table: bars for stressed Debt / EBITDA at 30 percent earnings shock, from tableau_credit_risk_stress_scenarios.csv filtered to 30 percent, and a second bar or label for stressed coverage. Oracle must read 6.67x debt and 3.7x coverage. Add the shock rule in text: only earnings fall, debt and interest stay fixed.

Bottom, full width:
- Notes box, plain language: Altman Z is weak for cash-rich tech companies, so use Z-prime as a cross-check. No company is predicted to default. Fiscal year ends differ by company. TSMC and ASML figures were converted to USD in the source project.

## Design rules for this rebuild
- Fill the canvas, no large blank white area. No truncated company names.
- Every chart must have a title, axis labels and values, not just a table of numbers.
- Colour by risk band on the heatmap and ranked bars where possible.
- Keep the confirmed viz name and description unchanged: US AI Companies: Credit Risk Board, and the description confirmed on 26 Oct 2026.
- Do not save publicly yet. Build the new dashboard, then stop and ask for confirmation before overwriting the published viz.
