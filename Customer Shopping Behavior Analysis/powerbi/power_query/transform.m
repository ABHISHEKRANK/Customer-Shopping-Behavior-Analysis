// =============================================================================
// Customer Shopping Behavior | Power Query (M) transformation
// -----------------------------------------------------------------------------
// HOW TO USE
//   1. Power BI Desktop > Home > Transform data > Manage Parameters > New
//      Name: FilePath | Type: Text | Current Value: full path to
//      data\raw\customer_shopping_behavior.csv on your machine.
//   2. Home > New Source > Blank Query > Advanced Editor.
//   3. Paste the query below (everything under "QUERY: Sales"), rename it "Sales".
//
// This logic mirrors scripts/data_preparation.py so both paths give the same result.
// =============================================================================

// ---- QUERY: Sales -----------------------------------------------------------
let
    // 1. Load raw CSV -----------------------------------------------------------
    Source = Csv.Document(
        File.Contents(FilePath),
        [Delimiter = ",", Columns = 18, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),

    // 2. Set data types (explicit culture avoids decimal-separator issues) ------
    ChangedTypes = Table.TransformColumnTypes(
        PromotedHeaders,
        {
            {"Customer ID", Int64.Type},
            {"Age", Int64.Type},
            {"Gender", type text},
            {"Item Purchased", type text},
            {"Category", type text},
            {"Purchase Amount (USD)", Currency.Type},
            {"Location", type text},
            {"Size", type text},
            {"Color", type text},
            {"Season", type text},
            {"Review Rating", type number},
            {"Subscription Status", type text},
            {"Shipping Type", type text},
            {"Discount Applied", type text},
            {"Promo Code Used", type text},
            {"Previous Purchases", Int64.Type},
            {"Payment Method", type text},
            {"Frequency of Purchases", type text}
        },
        "en-US"
    ),

    // 3. Text hygiene -----------------------------------------------------------
    TrimmedText = Table.TransformColumns(
        ChangedTypes,
        {{"Gender", Text.Trim, type text}, {"Category", Text.Trim, type text},
         {"Location", Text.Trim, type text}, {"Season", Text.Trim, type text}},
        null, MissingField.Ignore
    ),

    // 4. Remove redundant column ('Promo Code Used' is identical to 'Discount Applied')
    RemovedRedundant = Table.RemoveColumns(TrimmedText, {"Promo Code Used"}),

    // 5. Age Group ---------------------------------------------------------------
    AddAgeGroup = Table.AddColumn(
        RemovedRedundant, "Age Group",
        each if [Age] <= 25 then "18-25"
        else if [Age] <= 35 then "26-35"
        else if [Age] <= 45 then "36-45"
        else if [Age] <= 55 then "46-55"
        else "56+",
        type text
    ),

    // 6. Purchase Tier (+ sort key) ---------------------------------------------
    AddPurchaseTier = Table.AddColumn(
        AddAgeGroup, "Purchase Tier",
        each if [#"Purchase Amount (USD)"] < 40 then "Low"
        else if [#"Purchase Amount (USD)"] < 80 then "Medium"
        else "High",
        type text
    ),
    AddPurchaseTierSort = Table.AddColumn(
        AddPurchaseTier, "Purchase Tier Sort",
        each if [Purchase Tier] = "Low" then 1 else if [Purchase Tier] = "Medium" then 2 else 3,
        Int64.Type
    ),

    // 7. Loyalty Segment (+ sort key) -------------------------------------------
    AddLoyalty = Table.AddColumn(
        AddPurchaseTierSort, "Loyalty Segment",
        each if [Previous Purchases] <= 10 then "New (1-10)"
        else if [Previous Purchases] <= 25 then "Occasional (11-25)"
        else if [Previous Purchases] <= 40 then "Regular (26-40)"
        else "Loyal (41+)",
        type text
    ),
    AddLoyaltySort = Table.AddColumn(
        AddLoyalty, "Loyalty Sort",
        each if [Previous Purchases] <= 10 then 1
        else if [Previous Purchases] <= 25 then 2
        else if [Previous Purchases] <= 40 then 3
        else 4,
        Int64.Type
    ),

    // 8. Rating Band (blank ratings are NOT imputed) ----------------------------
    AddRatingBand = Table.AddColumn(
        AddLoyaltySort, "Rating Band",
        each if [Review Rating] = null then "Not Rated"
        else if [Review Rating] < 3 then "Low (<3.0)"
        else if [Review Rating] < 4 then "Moderate (3.0-3.9)"
        else "High (4.0+)",
        type text
    ),

    // 9. Standardise purchase frequency -----------------------------------------
    //    Bi-Weekly = Fortnightly, Quarterly = Every 3 Months
    FrequencyMap = [
        Weekly = {"Weekly", 1},
        #"Bi-Weekly" = {"Fortnightly", 2},
        Fortnightly = {"Fortnightly", 2},
        Monthly = {"Monthly", 3},
        Quarterly = {"Quarterly", 4},
        #"Every 3 Months" = {"Quarterly", 4},
        Annually = {"Annually", 5}
    ],
    AddFrequencyGroup = Table.AddColumn(
        AddRatingBand, "Frequency Group",
        each Record.Field(FrequencyMap, [Frequency of Purchases]){0}, type text
    ),
    AddFrequencySort = Table.AddColumn(
        AddFrequencyGroup, "Frequency Sort",
        each Record.Field(FrequencyMap, [Frequency of Purchases]){1}, Int64.Type
    ),

    // 10. Season sort key (Spring > Summer > Fall > Winter) ---------------------
    AddSeasonSort = Table.AddColumn(
        AddFrequencySort, "Season Sort",
        each if [Season] = "Spring" then 1
        else if [Season] = "Summer" then 2
        else if [Season] = "Fall" then 3
        else 4,
        Int64.Type
    )
in
    AddSeasonSort
