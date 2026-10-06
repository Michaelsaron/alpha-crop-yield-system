# A - Data Cleaning & Integration

## A1 Cleaning log
See `cleaning_log.csv`. It covers plot, weather, and price issues with counts, percentages, fixes and reasons.

## A2 Key standardization proof
Regions are standardized to Oromia, Amhara, SNNPR, Tigray, Somali. Crops are standardized to teff, wheat, maize, sorghum, barley (including `Tef` -> `teff`).

## A3 Join map and growing-season rule
See `join_map.png`. The plot table is the left table because every train/test plot must survive. Growing season = planting month + next 3 months.

## A4 Join audit

| join           |   rows_before |   rows_after |   match_rate_pct |   unmatched |   incomplete_weather_windows |
|:---------------|--------------:|-------------:|-----------------:|------------:|-----------------------------:|
| train->weather |         15090 |        15090 |              100 |           0 |                         2925 |
| test->weather  |          3750 |         3750 |              100 |           0 |                          748 |
| train->price   |         15090 |        15090 |              100 |           0 |                            0 |
| test->price    |          3750 |         3750 |              100 |           0 |                            0 |

## A5 Join proof
See `join_proof_3_plots.csv`, which lists the exact monthly weather rows used for three plots.

## A6 Feature engineering

| feature                     | formula                                | source         | why                                  |
|:----------------------------|:---------------------------------------|:---------------|:-------------------------------------|
| season_avg_temp_c           | mean(avg_temp_c over 4 months)         | weather        | captures thermal growing conditions  |
| season_rainfall_mm          | sum(monthly_rainfall_mm over 4 months) | weather        | captures seasonal water supply       |
| season_extreme_heat_days    | sum(extreme_heat_days over 4 months)   | weather        | captures heat stress                 |
| season_temp_deviation_c     | season temp - region/year typical      | weather        | captures anomaly                     |
| planting_month_num          | Jan=1 ... Dec=12                       | planting_month | numeric timing signal                |
| fertilizer_seed_interaction | fertilizer × improved_seed             | plot           | management interaction               |
| rainfall_gap_mm             | reported rainfall - station rainfall   | plot + weather | measurement/local climate difference |

## A7 Integrity checks

| check                            | result   | status   |
|:---------------------------------|:---------|:---------|
| train plot_id unique             | True     | PASS     |
| test plot_id unique              | True     | PASS     |
| train row count unchanged        | True     | PASS     |
| test row count unchanged         | True     | PASS     |
| allowed regions                  | True     | PASS     |
| allowed crops                    | True     | PASS     |
| yield nonnegative                | True     | PASS     |
| price positive                   | True     | PASS     |
| train/test feature columns align | True     | PASS     |

## A8 Master tables
Generated `master_train.csv`, `master_test.csv`, and `data_dictionary_master.csv`. Deterministic cleaning is applied equally; learned imputation/encoding/scaling is inside model pipelines and is fitted only on training folds/data to prevent leakage.
