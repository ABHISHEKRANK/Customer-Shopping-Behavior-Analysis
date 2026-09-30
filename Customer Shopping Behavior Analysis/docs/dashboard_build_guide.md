# Power BI Build Guide

Follow these steps to assemble the report from the assets in this repository (about 30 minutes). Requires **Power BI Desktop** (free, Windows).

## Step 1 | Load and transform the data

1. Open Power BI Desktop, then **Home > Transform data**.
2. **Manage Parameters > New Parameter**: name `FilePath`, type `Text`, value = the full local path to `data/raw/customer_shopping_behavior.csv`.
3. **New Source > Blank Query > Advanced Editor**. Paste the query from `powerbi/power_query/transform.m` (the section below "QUERY: Sales"). Rename the query **Sales**.
4. **Close & Apply**.

> Shortcut: import `data/processed/customer_shopping_behavior_clean.csv` directly if you prefer not to use Power Query. The result is identical.

## Step 2 | Model settings

Apply every setting in [`data_model.md`](data_model.md): sort-by-column rules, State data category, hidden helper columns, and number formats.

## Step 3 | Create measures

1. **Home > Enter Data**, create an empty table named `_Measures`, and load it.
2. Select `_Measures`, then **New measure**. Paste measures from `powerbi/dax/measures.dax` one by one.
3. Set formats: currency measures to `$#,0`, percentages to `0.0%`, `Average Rating` to 2 decimals.
4. Group measures into display folders (KPIs, Subscription, Discounts, Ranking, Customer Value, Titles).

## Step 4 | Apply the theme

**View > Themes > Browse for themes** and select `powerbi/theme/corporate_theme.json`.

## Step 5 | Build the pages

Canvas: 16:9, 1280 x 720. Reference images: `images/dashboard_page1_executive_overview.png`, `images/dashboard_page2_customer_insights.png`.

### Page 1 | Executive Overview

| Zone | Visual | Fields |
|---|---|---|
| Top row | 6 KPI cards | Total Revenue, Total Customers, Average Order Value, Average Rating, Subscriber Rate %, Discount Usage % |
| Left | Donut | Legend: Category, Values: Total Revenue |
| Centre | Column chart | Axis: Season (sorted), Values: Total Revenue; title: `Revenue Chart Title` |
| Right | Filled map or bar | Location, Total Revenue |
| Bottom left | Bar chart, Top N = 10 | Item Purchased, Total Revenue |
| Bottom right | Column chart | Age Group, Average Order Value |
| Slicers | Season, Category, Gender, Age Group | Sync slicers across pages |

### Page 2 | Customer Insights

| Zone | Visual | Fields |
|---|---|---|
| Top row | 6 KPI cards | Subscriber AOV, Non-Subscriber AOV, Discounted AOV, Full-Price AOV, Loyal Customer %, Female Customer % |
| Row 2 | Bar chart | Age Group, Total Customers |
| Row 2 | Column chart | Loyalty Segment, Total Customers |
| Row 2 | Column chart | Frequency Group, Total Customers |
| Bottom left | 100% stacked column | Subscription Status split for customers vs revenue |
| Bottom right | Bar chart | Item Purchased, Average Rating (bottom 8); conditional colour with `Rating Color` |

### Page 3 (optional) | Operations

Shipping Type and Payment Method bars (Total Revenue, Average Order Value), Size x Category matrix, Color top 10, and a Rating Band donut.

## Step 6 | Finishing touches

- Turn on **Sync slicers** for Season, Category and Gender across all pages.
- Add tooltips on KPI cards using `KPI Data Note`.
- Set page navigation buttons and a bookmark to reset all filters.
- Check **View > Mobile layout** for Page 1.
- Use **View > Performance analyzer** to confirm each visual renders in under 500 ms.

## Step 7 | Publish to the repository

1. Save as `powerbi/report/Customer_Shopping_Behavior.pbix`.
2. Take screenshots of every page (**File > Export > PDF** or Snipping Tool) and save them into `images/`, replacing the reference layouts. Update the image paths in `README.md` if the file names change.
3. Commit and push. A report on a dataset this small is typically only a few MB, well under GitHub's 100 MB file limit.
