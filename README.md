# Restaurant Performance Intelligence

Interactive BI case study using the public **tips** teaching dataset distributed by seaborn.

## Business question
How do recorded bills and weighted tipping rates vary by day, service period, and party size?

## Dashboard
Open [index.html](index.html) in a browser. No install or account required. Day, Service period, and Party size filters update four KPIs and two charts. Hover on chart marks for exact values.

## Findings from the supplied sample
- Across **244 checks**, recorded bills total **$4,827.77** and tips total **$731.58**.
- Weighted tip rate is **15.15%** (total tips divided by total bills), distinct from the mean of row-level percentages.
- This sample cannot support conclusions about revenue trends, profit, or staffing because it has no transaction dates or cost data.

## Model and metric definitions
Grain: one check. `total_bill` is treated as bill amount excluding the separate `tip` field. Recorded bill total is the sum of bills; tip total is separate; average check is total bills divided by checks. Day bars sum bills in selected records. Party-size bars use `SUM(tip) / SUM(total_bill)`, not an unweighted mean of check ratios. Currency is shown as dollars consistent with the source's common use; the public sample is for demonstration.

## Source and reproducibility
[seaborn-data tips.csv](https://github.com/mwaskom/seaborn-data/blob/master/tips.csv), Git blob SHA `1280a10886c1f858b29c1be1740619cdef3d6be1`. Run `python build_data.py` to regenerate `data.js` after verifying the pinned source. The dataset is a small, nonrepresentative teaching sample; it may have been modified relative to its original source.

## Portfolio skills
Semantic metric definitions, weighted rates, dimensional slicing, data provenance, and analysis limits.
