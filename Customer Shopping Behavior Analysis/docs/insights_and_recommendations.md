# Insights & Recommendations

All figures are calculated from `data/raw/customer_shopping_behavior.csv` (3,900 customers).

## Headline numbers

| Metric | Value |
|---|---|
| Total revenue | $233,081 |
| Customers | 3,900 |
| Average order value | $59.76 |
| Average review rating | 3.75 / 5 (n = 3,863) |
| Subscriber rate | 27.0% |
| Discount usage | 43.0% |

## Key findings

**1. Clothing and Accessories carry the business.**
Clothing generates 44.7% of revenue ($104K) and Accessories 31.8% ($74K). Together they account for over three quarters of sales. Outerwear is the smallest category at 7.9% and also has the lowest average order value ($57.17 vs about $60 elsewhere).

**2. Fall is the strongest season; Summer is the weakest.**
Fall leads with $60,018 (25.7% of revenue) and the highest average order value ($61.56). Summer trails at $55,777 (23.9%). The gap is around 7.6% between best and worst season, so seasonality is present but mild.

**3. Discounts do not increase basket size.**
43% of customers used a discount, contributing $99,411 (42.7% of revenue). However, discounted customers spend slightly *less* on average ($59.28) than full-price customers ($60.13). Discounting appears to reward existing demand rather than lift spend.

**4. Subscribers are not spending more.**
Subscribers are 27.0% of customers and 26.9% of revenue, with an average order value of $59.49 versus $59.87 for non-subscribers. The subscription programme currently shows no measurable spend uplift in this data.

**5. The customer base skews male and older.**
68% of customers are male and 28.3% are aged 56+, the single largest age segment. Female customers show a marginally higher average order value ($60.25 vs $59.54).

**6. Sales are geographically diffuse.**
Montana, Illinois, California, Idaho, and Nevada lead, but even the top state contributes only about 2.5% of revenue. There is no dominant regional market.

**7. Ratings are moderate and a few products lag.**
The average rating is 3.75. Shirts (3.62), Jeans (3.65), and Blouses (3.68) have the lowest average ratings, while Shirt and Blouse are also among the top revenue items, so quality issues on high-volume products carry outsized risk.

## Recommendations

| Priority | Recommendation | Evidence |
|---|---|---|
| High | Review quality and sizing feedback for Shirts, Jeans, and Blouses | Lowest ratings on top-selling items |
| High | Rework subscription benefits (for example, tiered perks tied to basket size) | No AOV lift from subscribers |
| Medium | Test targeted rather than blanket discounts | Discounts do not raise AOV; 43% of customers use them |
| Medium | Plan Fall inventory and campaigns earlier; run Summer promotions | Fall leads on revenue and AOV; Summer lags |
| Medium | Grow the Outerwear category through bundling with Clothing | Smallest share and lowest AOV |
| Low | Develop marketing aimed at female and younger (18-35) customers | Underrepresented segments |

## Analytical caveats

- **Values are very evenly distributed.** Most segment-level differences in average order value are within $1 to $3. Treat the recommendations as hypotheses to test, not proven conclusions.
- **No dates.** Growth, retention, and seasonality over time cannot be measured; `Season` is the only time proxy.
- **No cost or discount-amount fields.** Profitability, margin, and true discount ROI cannot be assessed.
- **One row per customer.** Revenue reflects captured purchase value per customer rather than a full transaction history.
