"""Credit risk report for 10 US-listed AI companies. Black text only.
Charts may use colour. No first person. Name only on the title line."""
import pandas as pd, pathlib
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.lib import colors
base = pathlib.Path(__file__).resolve().parents[1]
styles = getSampleStyleSheet()
body = ParagraphStyle("body", parent=styles["Normal"], fontName="Helvetica", fontSize=10.5, leading=15, textColor=colors.black, spaceAfter=6)
h1 = ParagraphStyle("h1", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=colors.black, spaceBefore=12, spaceAfter=8)
h2 = ParagraphStyle("h2", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=12.5, leading=16, textColor=colors.black, spaceBefore=10, spaceAfter=6)
small = ParagraphStyle("small", parent=styles["Normal"], fontName="Helvetica", fontSize=9, leading=12, textColor=colors.black, spaceAfter=4)
cell = ParagraphStyle("cell", parent=styles["Normal"], fontName="Helvetica", fontSize=9, leading=12, textColor=colors.black)
cellhead = ParagraphStyle("cellhead", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=colors.black)
def P(t, s=body): return Paragraph(t, s)
def tbl(data, widths):
    wrapped = [[Paragraph(str(c), cellhead if r == 0 else cell) for c in row] for r, row in enumerate(data)]
    t = Table(wrapped, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.HexColor("#DDDDDD")), ("TEXTCOLOR", (0,0), (-1,-1), colors.black), ("GRID", (0,0), (-1,-1), 0.4, colors.black), ("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 5), ("RIGHTPADDING", (0,0), (-1,-1), 5), ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4)]))
    return t
def heat_tbl(data, widths, bg):
    wrapped = [[Paragraph(str(c), cellhead if r == 0 else cell) for c in row] for r, row in enumerate(data)]
    t = Table(wrapped, colWidths=widths, repeatRows=1)
    style = [("BACKGROUND", (0,0), (-1,0), colors.HexColor("#DDDDDD")), ("TEXTCOLOR", (0,0), (-1,-1), colors.black), ("GRID", (0,0), (-1,-1), 0.4, colors.black), ("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 5), ("RIGHTPADDING", (0,0), (-1,-1), 5), ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4)]
    for (ri, ci), col in bg.items():
        style.append(("BACKGROUND", (ci,ri), (ci,ri), col))
    t.setStyle(TableStyle(style))
    return t
GREEN = colors.HexColor("#C6EFCE"); YELLOW = colors.HexColor("#FFEB9C"); RED = colors.HexColor("#FFC7CE")
def img(name, w=170*mm): return Image(str(base/"charts"/name), width=w, height=w*0.55)
lat = pd.read_csv(base/"data"/"latest.csv").set_index("ticker")
order = ["NVDA","GOOGL","MSFT","TSM","ASML","AMD","META","PLTR","AVGO","ORCL"]
names = {"NVDA":"NVIDIA","GOOGL":"Alphabet","MSFT":"Microsoft","TSM":"TSMC","ASML":"ASML","AMD":"AMD","META":"Meta","PLTR":"Palantir","AVGO":"Broadcom","ORCL":"Oracle"}
def fmt(x, d=2):
    return "n/a" if pd.isna(x) else f"{x:.{d}f}"
story = []
story.append(P("Credit Risk Analysis: 10 AI Companies", h1))
story.append(P("Munzeleen Sarwar", body))
story.append(P("Annual financial statements from yfinance, 5 fiscal years per company, latest fiscal year ends in 2025 or 2026. This report is an investigation, not personal investment advice and not a credit rating.", small))
story.append(P("Summary", h1))
story.append(P("Most of these companies carry very little credit risk on the numbers in this report. Eight of the ten hold more cash than debt, or debt that is less than one year of EBITDA. Two companies stand out as weaker: Broadcom, with debt at 1.88 times EBITDA and interest coverage of 8.1 times, and Oracle, with debt at 4.67 times EBITDA and interest coverage of 5.3 times. Oracle is the clear watchlist name. No company in this group looks close to default on these measures, but Oracle and Broadcom would feel a rise in interest costs or a fall in earnings first. Adding four more credit models in this expanded version does not change that conclusion. Oracle is flagged by every model, Broadcom by most models, and no other company is flagged by more than two models."))
story.append(P("What credit risk means, in plain terms", h1))
story.append(P("Credit risk is the risk that a company cannot pay what it owes, on time. This report checks that risk in four simple ways. First, debt compared with earnings: if debt is many times earnings, the company needs many good years to repay it. Second, earnings compared with interest: if earnings cover interest only a few times, a bad year can make interest hard to pay. Third, cash compared with debt: cash on hand can repay debt even if earnings fall. Fourth, short term assets compared with short term bills: this shows whether the company can pay bills due soon. A fifth check, the Altman Z score, is included with a warning, because it was built for manufacturers and gives very high scores for cash rich technology companies."))
story.append(P("Ranking, latest fiscal year", h1))
rows = [["Rank","Company","Debt / EBITDA","Interest coverage","Current ratio","Cash / debt","Free cash flow / debt","Net debt, USD billions"]]
for i, tick in enumerate(order, 1):
    r = lat.loc[tick]
    rows.append([str(i), f"{names[tick]} ({tick})", fmt(r.debt_ebitda), f"{fmt(r.interest_coverage,1)}x", fmt(r.current_ratio), fmt(r.cash_to_debt), fmt(r.fcf_to_debt), fmt(r.net_debt/1000)])
rank_bg = {}
for ri, tick in enumerate(order, 1):
    r = lat.loc[tick]
    rank_bg[(ri,2)] = GREEN if r.debt_ebitda < 1 else (YELLOW if r.debt_ebitda <= 2 else RED)
    rank_bg[(ri,3)] = GREEN if r.interest_coverage > 20 else (YELLOW if r.interest_coverage >= 8 else RED)
    rank_bg[(ri,4)] = GREEN if r.current_ratio > 1.5 else (YELLOW if r.current_ratio >= 1.0 else RED)
    rank_bg[(ri,5)] = GREEN if r.cash_to_debt > 1 else (YELLOW if r.cash_to_debt >= 0.5 else RED)
    rank_bg[(ri,6)] = GREEN if r.fcf_to_debt > 1 else (YELLOW if r.fcf_to_debt >= 0.3 else RED)
story.append(heat_tbl(rows, [12*mm, 32*mm, 22*mm, 26*mm, 20*mm, 20*mm, 20*mm, 18*mm], rank_bg))
story.append(P("Heatmap key for this table: green is strong, yellow is borderline, red is weak. Net debt is not coloured, because an absolute money amount alone is not a risk signal without earnings and cash to compare it with. Debt divided by EBITDA: below 1.0 green, 1.0 to 2.0 yellow, above 2.0 red. Interest coverage: above 20 times green, 8 to 20 times yellow, below 8 times red. Current ratio: above 1.5 green, 1.0 to 1.5 yellow, below 1.0 red. Cash divided by debt: above 1.0 green, 0.5 to 1.0 yellow, below 0.5 red. Free cash flow divided by debt: above 1.0 green, 0.3 to 1.0 yellow, below 0.3 red.", small))
story.append(P("Ranking is a judgement from the five measures above plus profit history. It is not a formula result and not a credit rating. Palantir is ranked eighth even though its debt is only 0.16 times EBITDA, because its interest coverage is only 6.2 times, its profit history is short, and EBITDA was negative in one of the five years. A small debt can still be risky if earnings are thin or new."))
story.append(img("debt_ebitda.png"))
story.append(P("Oracle debt is 156,189 million USD in the latest year, against EBITDA of about 33,400 million USD. Broadcom debt is 65,136 million USD. By contrast, NVIDIA debt is 11,040 million USD against EBITDA of about 144,600 million USD, which is why its debt divided by EBITDA is only 0.08."))
story.append(img("net_debt.png"))
story.append(P("Net debt is total debt minus cash and short term investments. A negative number means the company holds more cash than debt. Seven companies are in net cash on this measure. Meta is close to zero net debt, at 2,305 million USD. Broadcom net debt is 48,958 million USD and Oracle net debt is 124,295 million USD. Those two are the only companies that would need future earnings, not cash on hand, to repay all debt."))
story.append(img("interest_coverage.png"))
story.append(P("Interest coverage uses a log scale because the range is very wide, from 5.3 times for Oracle to 547.1 times for NVIDIA. On a normal scale, Oracle and Broadcom would be invisible next to NVIDIA and Alphabet. The log scale keeps every bar readable, but the reader should still compare the printed numbers, not just the bar lengths."))
story.append(P("Company notes", h1))
story.append(P("Oracle, watchlist. Debt divided by EBITDA rose from 4.35 in the year to May 2025 to 4.67 in the year to May 2026. Interest coverage is 5.3 times, the lowest in the group. Current ratio is 1.12, also the lowest in the group. Free cash flow in the latest year was negative compared with debt, at minus 0.15 times debt, which means free cash flow alone did not cover debt in that year. None of this means Oracle cannot pay its bills. It means Oracle has the least room in this group if earnings fall or interest costs rise."))
story.append(P("Broadcom, watchlist, second weakest. Debt divided by EBITDA fell from 2.83 to 1.88 over the last two years, which is an improvement, but it is still far above the rest of the group apart from Oracle. Interest coverage is 8.1 times. Free cash flow divided by debt is 0.41, so free cash flow would take about two and a half years to repay all debt, if it stayed at the latest level and no other cash was used."))
story.append(P("NVIDIA, strongest. Debt divided by EBITDA fell from 2.01 in the year to January 2023 to 0.08 in the latest year, as earnings grew much faster than debt. Cash of 62,556 million USD is more than five times debt. Interest coverage of 547.1 times reflects very small interest expense compared with earnings, not a calculation error."))
story.append(P("Alphabet, Microsoft, TSMC and ASML, strong. All four have debt below 0.40 times EBITDA and interest coverage above 55 times, except ASML at 97.4 times with a lower current ratio of 1.26. Microsoft current ratio is 1.23, which is low for this group, but its cash of 76,651 million USD is above its debt of 56,826 million USD, so short term risk still looks low."))
story.append(P("AMD and Meta, strong with a note. AMD debt is 0.53 times EBITDA, coverage is 32.6 times, and cash is above debt. Meta debt is 0.79 times EBITDA and coverage is 74.8 times, but Meta net debt is slightly positive, unlike most peers, because cash of 81,592 million USD is just below debt of 83,897 million USD. That gap is small and does not change the overall view."))
story.append(P("Palantir, low debt but young earnings. Debt is only 229 million USD and cash is 7,177 million USD. Interest coverage of 6.2 times is the second lowest in the group, because earnings are still small compared with larger peers. The company is therefore ranked below stronger earners despite almost no debt."))
story.append(P("Trend over five years", h1))
story.append(img("debt_ebitda_trend.png"))
story.append(P("Debt divided by EBITDA fell for most companies over the five years, because earnings grew faster than debt. The two exceptions are Oracle, which stayed near 4.3 to 4.8 times, and Broadcom, which stayed near 1.9 to 2.8 times. Palantir is not shown in one early year because EBITDA was negative then, so debt divided by EBITDA has no useful meaning for that year. Fiscal year ends differ, so the horizontal axis runs from oldest to latest fiscal year for each company, not a single calendar year."))
story.append(P("Stress test: earnings fall 30%", h1))
srows = [["Company","Interest coverage now","Interest coverage if EBIT falls 30%","Debt / EBITDA now","Debt / EBITDA if EBITDA falls 30%"]]
for tick in order:
    r = lat.loc[tick]
    srows.append([f"{names[tick]} ({tick})", f"{fmt(r.interest_coverage,1)}x", f"{fmt(r.interest_coverage*0.7,1)}x", fmt(r.debt_ebitda), fmt(r.debt_ebitda/0.7)])
stress_bg = {}
for ri, tick in enumerate(order, 1):
    r = lat.loc[tick]
    for ci, val in [(1, r.interest_coverage), (2, r.interest_coverage*0.7)]:
        stress_bg[(ri,ci)] = GREEN if val > 20 else (YELLOW if val >= 8 else RED)
    for ci, val in [(3, r.debt_ebitda), (4, r.debt_ebitda/0.7)]:
        stress_bg[(ri,ci)] = GREEN if val < 1 else (YELLOW if val <= 2 else RED)
story.append(heat_tbl(srows, [34*mm, 34*mm, 42*mm, 28*mm, 32*mm], stress_bg))
story.append(P("Heatmap key for this table: same bands as the ranking table. Interest coverage above 20 times green, 8 to 20 times yellow, below 8 times red. Debt divided by EBITDA below 1.0 green, 1.0 to 2.0 yellow, above 2.0 red.", small))
story.append(P("This stress test changes only earnings. Debt, interest and cash are held fixed. Even after a 30% fall in earnings, every company except Oracle still covers interest more than 4 times, and Oracle covers interest 3.7 times. Debt divided by EBITDA for Oracle rises to 6.67 times in that case, which would be the main concern, not interest payment itself. This test is simple on purpose. A real stress test would also change interest rates, cash flow, and access to new borrowing."))
story.append(P("Altman Z score, with a warning", h1))
zrows = [["Company","Altman Z, latest year","Usual reading"]]
for tick in order:
    r = lat.loc[tick]; z = r.altman_z
    reading = "Safe" if z > 2.99 else ("Grey" if z >= 1.81 else "Distress")
    zrows.append([f"{names[tick]} ({tick})", fmt(z), reading])
z_bg = {}
for ri, tick in enumerate(order, 1):
    z = lat.loc[tick].altman_z
    z_bg[(ri,1)] = GREEN if z > 2.99 else (YELLOW if z >= 1.81 else RED)
story.append(heat_tbl(zrows, [50*mm, 50*mm, 70*mm], z_bg))
story.append(P("Heatmap key for this table: above 2.99 green, 1.81 to 2.99 yellow, below 1.81 red, matching the usual Altman Z zones.", small))
story.append(P("On this score alone, only Oracle falls in the distress zone, at 1.61, and every other company looks safe. That result should not be taken at face value. The score gives a large boost to companies with a very high market value compared with liabilities, which is true for Palantir at 190.91 and NVIDIA at 68.05. Market value can fall fast, while debt does not. That is why the ranking in this report uses debt, coverage, cash and cash flow first, and the Z score only as a secondary check."))
story.append(P("More credit models: do they agree?", h1))
story.append(P("A single credit model is not sufficient evidence on its own. Each model uses different inputs, applies different weights, and is sensitive to different weaknesses. The results below therefore estimate five further measures independently, in addition to the Altman Z score reported above, and compare them. Agreement across models carries more weight than any one score alone. Disagreement is also informative, as it shows where a result depends on a particular method rather than on the underlying balance sheet."))
story.append(P("Altman Z-prime", h2))
story.append(P("Altman Z-prime replaces market value of equity with book equity. It is therefore less affected by a high share price than the original Altman Z score. The usual reading is above 2.6 safe, 1.1 to 2.6 grey, and below 1.1 distress."))
story.append(P("Springate", h2))
story.append(P("The Springate score combines working capital, earnings, earnings relative to current liabilities, and sales. A score below 0.862 is read as a fail. It places more weight on short term obligations than Altman Z-prime, which makes it a useful check on liquidity pressure."))
story.append(P("Zmijewski", h2))
story.append(P("The Zmijewski model estimates a probability from return on assets, liabilities relative to assets, and the current ratio. The output is a modelled probability, not an observed default rate. It is most useful for ranking companies, and for showing which balance sheets the model treats as stretched."))
story.append(P("Merton distance to default", h2))
story.append(P("The Merton distance to default measures how many standard deviations asset value sits above the default point. It uses share price volatility over the past year, market value, and liabilities. A higher distance indicates greater safety. The default point used here is current liabilities plus half of long term liabilities, and the assumed risk free rate is 4.0%."))
story.append(P("Synthetic rating from interest coverage", h2))
story.append(P("A synthetic rating maps interest coverage to a rating label using a standard coverage table. It is not an agency rating, and it reflects coverage alone. It is included because it translates a coverage ratio into a form that is directly comparable across companies, not because it replaces a full rating assessment."))
story.append(P("Why a synthetic rating can mislead", h2))
story.append(P("A synthetic rating is based on interest coverage alone, so it can mislead in several ways. First, it ignores total debt. Oracle maps to A on coverage of 5.3 times, yet its debt is 4.67 times EBITDA and its net debt is 124,295 million USD. Coverage shows that interest for the current year can be paid. It does not show how long repayment of the full debt would take. Second, the rating bands compress large differences at the top. NVIDIA, with coverage of 547.1 times, and Microsoft, with coverage of 55.4 times, both map to AAA, even though the gap between them is tenfold."))
story.append(P("Third, coverage uses earnings, not cash. Earnings can be boosted by non-cash items or by a one-off gain, while cash flow remains weak. Fourth, interest expense can be unusually low when debt was borrowed at low fixed rates, or when interest earned on cash exceeds interest paid. Coverage then looks strong, even if refinancing at higher rates would change the picture. Fifth, coverage says nothing about when debt comes due. Two companies with the same coverage face very different risk if one must refinance next year and the other in ten years. Sixth, coverage does not adjust for cash on hand, short term bills, or what is normal for the industry. For those reasons, the synthetic rating in this report is used only as a cross-check. When it disagrees with the other models, as it does for Oracle, the disagreement itself is treated as a warning."))
story.append(P("Scope note: Ohlson score", h2))
story.append(P("A full Ohlson score was not estimated. It requires a national output price index and prior year indicator variables that are not present in the yfinance statements used for this report. Estimating those inputs would introduce assumptions that could not be verified from the data, so the score was omitted rather than approximated."))
mod = pd.read_csv(base/"data"/"models.csv").set_index("ticker")
mrows = [["Company","Z-prime","Springate","Zmijewski probability","Merton distance","Synthetic rating"]]
for tick in order:
    r = mod.loc[tick]
    mrows.append([f"{names[tick]} ({tick})", fmt(r.altman_zprime), fmt(r.springate), f"{fmt(r.zmijewski_prob_pct,1)}%", fmt(r.merton_dd), r.synthetic_rating])
wrapped_m = [[Paragraph(str(c), cellhead if r == 0 else cell) for c in row] for r, row in enumerate(mrows)]
heat = Table(wrapped_m, colWidths=[34*mm, 22*mm, 22*mm, 38*mm, 26*mm, 28*mm], repeatRows=1)
heat_style = [("BACKGROUND", (0,0), (-1,0), colors.HexColor("#DDDDDD")), ("TEXTCOLOR", (0,0), (-1,-1), colors.black), ("GRID", (0,0), (-1,-1), 0.4, colors.black), ("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 5), ("RIGHTPADDING", (0,0), (-1,-1), 5), ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4)]
GREEN = colors.HexColor("#C6EFCE"); YELLOW = colors.HexColor("#FFEB9C"); RED = colors.HexColor("#FFC7CE"); ORANGE = colors.HexColor("#FCE4D6")
for ri, tick in enumerate(order, 1):
    r = mod.loc[tick]
    heat_style.append(("BACKGROUND", (1,ri), (1,ri), GREEN if r.altman_zprime > 2.6 else (YELLOW if r.altman_zprime >= 1.1 else RED)))
    heat_style.append(("BACKGROUND", (2,ri), (2,ri), GREEN if r.springate > 1.0 else (YELLOW if r.springate >= 0.862 else RED)))
    heat_style.append(("BACKGROUND", (3,ri), (3,ri), GREEN if r.zmijewski_prob_pct < 6 else (YELLOW if r.zmijewski_prob_pct < 20 else RED)))
    heat_style.append(("BACKGROUND", (4,ri), (4,ri), GREEN if r.merton_dd > 8 else (YELLOW if r.merton_dd >= 5 else RED)))
    heat_style.append(("BACKGROUND", (5,ri), (5,ri), {"AAA": GREEN, "AA": YELLOW, "A+": ORANGE, "A": RED}.get(r.synthetic_rating, YELLOW)))
heat.setStyle(TableStyle(heat_style))
story.append(heat)
story.append(P("Heatmap key: green indicates a safe result on that measure, yellow indicates a borderline or elevated result, and red indicates a distress or high risk result. Orange is used for the A+ synthetic rating, between yellow and red. Colours are a visual guide only. The numbers in each cell, not the colours, are the evidence.", small))
story.append(P("Results", h2))
story.append(P("On Altman Z-prime, only Oracle falls in the distress zone, at 0.89. Broadcom, at 2.66, sits just inside the safe zone, close to the boundary. On Springate, only Oracle falls below the cutoff, at 0.79. AMD, at 0.88, is the next closest to a fail. On Zmijewski, Oracle is far ahead at 53.3%, followed by ASML at 15.3% and Broadcom at 12.4%, with every other company below 6%. On Merton distance to default, Oracle is lowest at 4.15, followed by AMD at 6.22 and ASML at 6.78. In absolute terms, Merton default probabilities remain very small for all ten companies, with Oracle highest at 0.0017%. The Merton result therefore ranks relative risk; it does not indicate an expected default for any company in the group."))
story.append(img("zmijewski_prob.png"))
story.append(P("Zmijewski is driven mainly by liabilities compared with assets and by return on assets. Oracle liabilities are high compared with assets, which is why its probability jumps. ASML at 15.3% is a warning about reading one model alone: ASML has low debt divided by EBITDA at 0.35 and interest coverage of 97.4 times, so its balance sheet does not look risky in the earlier sections. Its Zmijewski probability is higher because liabilities, including operating liabilities, are a larger share of assets. That is a model sensitivity, not a separate crisis."))
story.append(img("merton_dd.png"))
story.append(P("Synthetic rating maps interest coverage to a rating label, using a standard coverage table. It is not an agency rating. Oracle maps to A, Palantir to A+, Broadcom to AA, and the rest to AAA. That mapping flatters Oracle, because coverage alone ignores how much debt Oracle carries. Oracle actual agency ratings are lower than A in practice, which shows why coverage alone cannot be used as a rating. The synthetic rating is useful only to show that, even on the friendliest coverage-only view, Oracle and Palantir still rank lowest."))
story.append(P("Composite view: which stocks are highest credit risk?", h1))
story.append(P("The table below summarises the signal count for each company. A signal is counted when a company is among the weakest three on a measure, or when it falls below a model cutoff. Borderline results, such as a score just above a cutoff, are shown separately and are not counted as clear signals. This keeps the comparison transparent: the reader can see how many independent measures point the same way, rather than relying on a single score."))
story.append(tbl([
["Company","Clear signals","Borderline signals","Main signals","Assessment"],
["Oracle (ORCL)","8","0","Debt, coverage, Altman Z, Z-prime, Springate, Zmijewski, Merton, synthetic rating","Highest credit risk"],
["Broadcom (AVGO)","4","1","Debt, coverage, Zmijewski, synthetic rating; Z-prime near the safe boundary","Second highest"],
["Palantir (PLTR)","2","0","Coverage and synthetic rating; debt is very low","Third, earnings driven"],
["AMD (AMD)","1","1","Merton distance; Springate near its cutoff","Low, model sensitive"],
["ASML (ASML)","1","1","Zmijewski; Merton distance","Low, model sensitive"],
["NVIDIA, Alphabet, Microsoft, TSMC, Meta","0","0","No clear or borderline signals on these measures","Low"],
], [32*mm, 20*mm, 24*mm, 52*mm, 42*mm]))
story.append(P("Oracle stands apart. Every measure points in the same direction, which is a stronger result than any single model on its own. The concern is not one weak ratio. It is the combination of high debt, low coverage, a distress score on both Altman measures, a Springate fail, the highest Zmijewski probability, and the lowest Merton distance."))
story.append(P("Broadcom ranks second, but the gap to Oracle is large. Its debt and coverage results are weaker than the rest of the group, and its Zmijewski probability and synthetic rating confirm that position. Its Z-prime score, however, remains just inside the safe zone, which tempers the result. Broadcom is therefore a watchlist name, not a distress case on these measures."))
story.append(P("Palantir ranks third for a different reason. Its debt is very low, so leverage is not the concern. Earnings are thin relative to the rest of the group, which is reflected in interest coverage of 6.2 times and a synthetic rating of A+. That is an earnings strength question, not a debt burden question, and the two should not be treated as the same risk."))
story.append(P("The middle of the ranking is model sensitive. AMD and ASML each show one or two model-specific signals, while remaining strong on debt, coverage, cash and cash flow. That pattern is consistent with method differences, rather than with a broad deterioration in credit quality. NVIDIA, Alphabet, Microsoft, TSMC and Meta show no clear or borderline signals on these measures. NVIDIA remains the lowest risk company in the group, followed by Alphabet and Microsoft. Altman Z scores for cash rich companies, including Palantir and NVIDIA, remain inflated by market value and should not be read on their own."))
story.append(P("Limits and method", h1))
story.append(P("Data are yfinance annual statements, 5 fiscal years per company. Fiscal year ends differ: for example, Microsoft ends in June, NVIDIA in January, and most others in December. Money is converted to USD. TSMC statements are in Taiwan dollars, converted at 32.562 Taiwan dollars per US dollar. ASML statements are in euros, converted at 1.1178 US dollars per euro. Both rates are closes on 26 October 2026. Ratios do not depend on currency, so the conversion only affects cross-company money amounts. Interest expense is taken from the income statement. Where a company reports net interest income instead, the absolute value is used as a proxy for interest cost, which can overstate coverage for companies that earn more interest than they pay. Market capitalisation for the Z score is the current value at download, not the value at each past year end. Merton distance to default uses share price volatility over the past year and an assumed 4.0% risk free rate, and its default point is current liabilities plus half of long term liabilities. Springate uses EBIT as a proxy for earnings before tax where a separate pretax figure was not used. Zmijewski probabilities are model outputs, not observed default rates. This report does not use credit ratings, bond yields, or default data, and it does not predict default. Past financial strength does not guarantee future payment."))
story.append(P("Sources", h1))
story.append(P("yfinance annual balance sheet, income statement and cash flow statement for NVDA, MSFT, GOOGL, META, AVGO, TSM, AMD, PLTR, ORCL and ASML. Market capitalisation from yfinance. FX closes for Taiwan dollars and euros from yfinance on 26 October 2026. Scripts, data and the Excel model are in the project folder, so every number can be recomputed from the financials file."))
doc = SimpleDocTemplate(str(base/"US_AI_Credit_Risk_Report.pdf"), pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=18*mm, bottomMargin=18*mm, title="Credit Risk Analysis: 10 AI Companies", author="Munzeleen Sarwar")
doc.build(story)
print("report done")
