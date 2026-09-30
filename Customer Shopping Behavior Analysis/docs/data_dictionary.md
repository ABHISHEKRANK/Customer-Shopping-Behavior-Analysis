# Data Dictionary

**Source file:** `data/raw/customer_shopping_behavior.csv`
**Grain:** one row per customer (3,900 rows, `Customer ID` is unique)
**Time dimension:** none. The dataset has no transaction date, so time-based analysis (trends, YoY, MoM) is out of scope. `Season` is used as the only calendar proxy.

## Raw columns

| Column | Type | Description | Notes |
|---|---|---|---|
| Customer ID | Integer | Unique customer identifier | 1-3900, no duplicates |
| Age | Integer | Customer age in years | 18-70 |
| Gender | Text | Male / Female | 68% Male, 32% Female |
| Item Purchased | Text | Product bought | 25 distinct items |
| Category | Text | Product category | Clothing, Accessories, Footwear, Outerwear |
| Purchase Amount (USD) | Integer | Value of the purchase in USD | 20-100 |
| Location | Text | US state | 50 states |
| Size | Text | Product size | S, M, L, XL |
| Color | Text | Product color | 25 colors |
| Season | Text | Season of purchase | Spring, Summer, Fall, Winter |
| Review Rating | Decimal | Customer rating, 1-5 scale | Observed range 2.5-5.0. **37 blanks (0.95%)** |
| Subscription Status | Text | Yes / No | 27% subscribed |
| Shipping Type | Text | Delivery method | 6 options |
| Discount Applied | Text | Yes / No | 43% used a discount |
| Promo Code Used | Text | Yes / No | **Identical to Discount Applied on every row, so it is dropped** |
| Previous Purchases | Integer | Number of prior purchases | 1-50 |
| Payment Method | Text | Payment type | 6 options |
| Frequency of Purchases | Text | Self-reported buying cadence | 7 raw values, see quality notes |

## Engineered columns

| Column | Logic | Purpose |
|---|---|---|
| Age Group | 18-25, 26-35, 36-45, 46-55, 56+ | Demographic segmentation |
| Purchase Tier | Low (< $40), Medium ($40-$79), High ($80+) | Basket value segmentation |
| Loyalty Segment | New (1-10), Occasional (11-25), Regular (26-40), Loyal (41+) previous purchases | Loyalty analysis |
| Rating Band | Low (< 3.0), Moderate (3.0-3.9), High (4.0+), Not Rated | Satisfaction analysis |
| Frequency Group | Standardised cadence (Weekly, Fortnightly, Monthly, Quarterly, Annually) | Removes duplicate labels |
| Season Sort, Frequency Sort, Loyalty Sort, Purchase Tier Sort | Numeric sort keys | Used with **Sort by column** so visuals show logical order, not alphabetical |

## Data quality log

| # | Finding | Decision |
|---|---|---|
| 1 | 37 missing `Review Rating` values (mostly Clothing: 19) | Kept blank. Averages ignore blanks; no imputation, to avoid inventing customer opinions. Flagged as "Not Rated". |
| 2 | `Promo Code Used` equals `Discount Applied` in 100% of rows | Dropped the duplicate column. |
| 3 | `Bi-Weekly` and `Fortnightly` mean the same cadence; so do `Quarterly` and `Every 3 Months` | Merged into `Frequency Group`; raw column retained for traceability. |
| 4 | No transaction date | No time-series analysis; documented as a limitation. |
| 5 | No cost, margin, or discount-amount fields | Profitability and discount ROI cannot be measured; documented as a limitation. |
| 6 | Customer ID is unique, so one row = one customer | "Revenue" is total captured purchase value; `Average Order Value` therefore equals revenue per customer. |
