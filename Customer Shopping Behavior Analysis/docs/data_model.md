# Data Model

## Design

The source is a single, already-denormalised customer table with one row per customer, no dates, and no natural lookup keys. A single fact table plus a dedicated measures table is the appropriate model here; splitting into artificial dimensions would add joins without adding analytical value.

```
+---------------------------+
|        _Measures          |   Empty table that only holds DAX measures
+---------------------------+   (no relationships)

+-------------------------------------------------------------+
|                          Sales                              |
|-------------------------------------------------------------|
| Customer ID (PK)     | Age | Age Group | Gender             |
| Item Purchased | Category | Size | Color | Season            |
| Purchase Amount (USD) | Purchase Tier                       |
| Location (US state)  | Review Rating | Rating Band          |
| Subscription Status | Discount Applied                      |
| Shipping Type | Payment Method                              |
| Previous Purchases | Loyalty Segment                        |
| Frequency of Purchases | Frequency Group                  |
| *Sort keys: Season, Frequency, Loyalty, Purchase Tier*      |
+-------------------------------------------------------------+
```

## Required model settings

| Setting | Column | Value |
|---|---|---|
| Sort by column | Season | Season Sort |
| Sort by column | Frequency Group | Frequency Sort |
| Sort by column | Loyalty Segment | Loyalty Sort |
| Sort by column | Purchase Tier | Purchase Tier Sort |
| Data category | Location | State or Province |
| Summarization | Customer ID, Age, Previous Purchases, sort keys | Don't summarize |
| Hidden | All four `* Sort` columns, `Customer ID` | Hide in report view |
| Format | Purchase Amount (USD) | Currency, 0 decimals |
| Format | Review Rating | Decimal, 1 place |

## Why not a star schema?

A star schema pays off when there are multiple fact tables, conformed dimensions, or a date table. Here, attributes such as Category or Gender are already low-cardinality columns on a 3,900-row table, so a flat model is faster and easier to maintain. If transaction dates and a product master are added in future, the recommended evolution is `Fact_Sales`, `Dim_Customer`, `Dim_Product`, `Dim_Date`, and `Dim_Location`.
