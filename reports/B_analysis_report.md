# B - Data Analysis Report

## B1.1 Revenue per hectare by crop

| crop_type   |   mean_yield |   mean_revenue_per_ha |
|:------------|-------------:|----------------------:|
| teff        |         2    |                153349 |
| wheat       |         2.8  |                135500 |
| maize       |         3.9  |                114497 |
| barley      |         2.47 |                110196 |
| sorghum     |         2.61 |                 83292 |

**Interpretation:** Highest mean revenue/ha: teff. Highest mean yield crop: maize.

## B1.2 Price trend 2021-2024

| crop_type   |   price_2021 |   price_2024 |   absolute_change |   percent_change |
|:------------|-------------:|-------------:|------------------:|-----------------:|
| barley      |       3946.8 |       4977.8 |            1031   |            26.12 |
| maize       |       2602.2 |       3233.2 |             631   |            24.25 |
| sorghum     |       2688.8 |       3492.4 |             803.6 |            29.89 |
| teff        |       6885   |       8575.3 |            1690.3 |            24.55 |
| wheat       |       4305   |       5557.4 |            1252.4 |            29.09 |

**Interpretation:** Fastest price growth: sorghum (29.9%).

## B2.1 Yield by region

| region   |   mean |   median |   std |
|:---------|-------:|---------:|------:|
| Tigray   |  3.131 |    2.932 | 1.309 |
| Amhara   |  3.129 |    3.021 | 1.231 |
| Oromia   |  3.073 |    2.893 | 1.292 |
| SNNPR    |  3.041 |    2.741 | 1.472 |
| Somali   |  1.464 |    1.294 | 0.771 |

**Interpretation:** Highest average: Tigray; most variable: SNNPR.

## B2.2 Yield by crop type

| crop_type   |   mean |   median |   std |
|:------------|-------:|---------:|------:|
| maize       |  3.904 |    3.781 | 1.584 |
| wheat       |  2.802 |    2.692 | 1.411 |
| sorghum     |  2.611 |    2.514 | 0.974 |
| barley      |  2.467 |    2.376 | 1.158 |
| teff        |  2.003 |    2.001 | 0.988 |

**Interpretation:** Highest average-yield crop: maize; lowest: teff.

## B2.3 Region x crop pivot

| region   |   barley |   maize |   sorghum |   teff |   wheat |
|:---------|---------:|--------:|----------:|-------:|--------:|
| Amhara   |    3.187 |   3.829 |     2.495 |  2.479 |   3.598 |
| Oromia   |    2.675 |   4.45  |     2.955 |  2.288 |   3.12  |
| SNNPR    |    2.289 |   4.797 |     3.106 |  2.104 |   2.668 |
| Somali   |    1.123 |   2.32  |     1.793 |  0.831 |   1.281 |
| Tigray   |    3.01  |   4.074 |     2.709 |  2.332 |   3.463 |

**Interpretation:** Best combination: ('SNNPR', 'maize'); worst: ('Somali', 'teff'). This may reflect climate, altitude, soil and management differences.

## B2.4 Improved seed, by crop

| crop_type   |     0 |     1 |   gap_t_ha |   pct_gap |
|:------------|------:|------:|-----------:|----------:|
| barley      | 2.305 | 2.727 |      0.422 |    18.296 |
| maize       | 3.612 | 4.394 |      0.783 |    21.667 |
| sorghum     | 2.442 | 2.889 |      0.447 |    18.309 |
| teff        | 1.844 | 2.263 |      0.419 |    22.746 |
| wheat       | 2.596 | 3.133 |      0.537 |    20.665 |

**Interpretation:** Largest absolute gap: maize (0.78 t/ha).

## B2.5 Pest/disease, by crop

| crop_type   |   0.0 |   1.0 |   gap_t_ha |   pct_gap |
|:------------|------:|------:|-----------:|----------:|
| barley      | 2.624 | 1.917 |     -0.706 |   -26.922 |
| maize       | 4.187 | 2.972 |     -1.215 |   -29.029 |
| sorghum     | 2.771 | 2.026 |     -0.745 |   -26.896 |
| teff        | 2.13  | 1.568 |     -0.562 |   -26.366 |
| wheat       | 2.98  | 2.191 |     -0.788 |   -26.456 |

**Interpretation:** Largest absolute gap: maize (-1.22 t/ha).

## B3.1 Fertilizer response

| fert_band         |   overall_mean |
|:------------------|---------------:|
| (0.497, 19.707]   |          2.427 |
| (19.707, 33.827]  |          2.676 |
| (33.827, 53.225]  |          2.856 |
| (53.225, 898.848] |          3.096 |

**Interpretation:** Mean yield changes from 2.43 to 3.10 t/ha across fertilizer bands; crop-specific patterns should be read with the figure/table.

## B3.2 Altitude by crop

|                                                           |   mean |   count |
|:----------------------------------------------------------|-------:|--------:|
| ('barley', Interval(52.76, 816.853, closed='right'))      |  2.871 |      10 |
| ('barley', Interval(816.853, 1577.902, closed='right'))   |  0.205 |       4 |
| ('barley', Interval(1577.902, 2338.951, closed='right'))  |  1.618 |     442 |
| ('barley', Interval(2338.951, 3100.0, closed='right'))    |  2.62  |    2478 |
| ('maize', Interval(52.76, 816.853, closed='right'))       |  2.346 |     152 |
| ('maize', Interval(816.853, 1577.902, closed='right'))    |  4.19  |    2025 |
| ('maize', Interval(1577.902, 2338.951, closed='right'))   |  3.542 |     874 |
| ('maize', Interval(2338.951, 3100.0, closed='right'))     |  0.713 |       8 |
| ('sorghum', Interval(52.76, 816.853, closed='right'))     |  1.828 |     252 |
| ('sorghum', Interval(816.853, 1577.902, closed='right'))  |  2.806 |    2145 |
| ('sorghum', Interval(1577.902, 2338.951, closed='right')) |  2.268 |     602 |
| ('sorghum', Interval(2338.951, 3100.0, closed='right'))   |  0.662 |       7 |
| ('teff', Interval(52.76, 816.853, closed='right'))        |  2.504 |      14 |
| ('teff', Interval(816.853, 1577.902, closed='right'))     |  0.985 |     237 |
| ('teff', Interval(1577.902, 2338.951, closed='right'))    |  2.25  |    2041 |
| ('teff', Interval(2338.951, 3100.0, closed='right'))      |  1.627 |     723 |
| ('wheat', Interval(52.76, 816.853, closed='right'))       |  3.139 |      11 |
| ('wheat', Interval(816.853, 1577.902, closed='right'))    |  0.135 |      11 |
| ('wheat', Interval(1577.902, 2338.951, closed='right'))   |  2.083 |     707 |
| ('wheat', Interval(2338.951, 3100.0, closed='right'))     |  3.029 |    2347 |

**Interpretation:** Cells with count <30 should not be trusted; all counts are shown for that check.

## B3.3 Planting month

| planting_month   |   barley |   maize |   sorghum |   teff |   wheat |
|:-----------------|---------:|--------:|----------:|-------:|--------:|
| Aug              |    2.576 |   3.875 |     2.618 |  2.02  |   2.805 |
| Feb              |    2.241 |   4.118 |     2.729 |  1.852 |   2.495 |
| Jul              |    2.573 |   3.846 |     2.526 |  2.107 |   2.932 |
| Jun              |    2.657 |   3.725 |     2.475 |  2.071 |   3.078 |
| Mar              |    2.313 |   3.956 |     2.701 |  1.96  |   2.687 |

**Interpretation:** Overall planting-month range is 0.12 t/ha.

## B3.4 Distance to market

| dist_band      |   yield_tons_per_ha |
|:---------------|--------------------:|
| (0.499, 3.435] |               2.769 |
| (3.435, 8.232] |               2.73  |
| (8.232, 16.43] |               2.775 |
| (16.43, 90.0]  |               2.777 |

**Interpretation:** Pearson correlation = 0.005. Keep/drop should be based on validation; correlation alone does not prove causation.

## B4.1 Yield trend

|   survey_year |   Amhara |   Oromia |   SNNPR |   Somali |   Tigray |
|--------------:|---------:|---------:|--------:|---------:|---------:|
|          2021 |    3.146 |    3.041 |   2.864 |    1.283 |    3.159 |
|          2022 |    3.08  |    3.031 |   3.024 |    1.671 |    3.139 |
|          2023 |    3.105 |    3.132 |   3.161 |    1.415 |    3.155 |
|          2024 |    3.181 |    3.089 |   3.105 |    1.478 |    3.068 |

**Interpretation:** Compare year-to-year movement with the much larger plot-level spread before calling it a trend.

## B4.2 Weather anomalies

| region   |   survey_year |   temp |   yield_mean |   region_4yr_temp |   temp_anomaly |
|:---------|--------------:|-------:|-------------:|------------------:|---------------:|
| Amhara   |          2021 | 16.736 |        3.146 |            16.785 |         -0.049 |
| Amhara   |          2022 | 18.312 |        3.08  |            16.785 |          1.528 |
| Amhara   |          2023 | 15.506 |        3.105 |            16.785 |         -1.279 |
| Amhara   |          2024 | 16.585 |        3.181 |            16.785 |         -0.2   |
| Oromia   |          2021 | 19.131 |        3.041 |            18.864 |          0.267 |
| Oromia   |          2022 | 19.715 |        3.031 |            18.864 |          0.852 |
| Oromia   |          2023 | 18.505 |        3.132 |            18.864 |         -0.359 |
| Oromia   |          2024 | 18.104 |        3.089 |            18.864 |         -0.76  |
| SNNPR    |          2021 | 21.389 |        2.864 |            20.146 |          1.243 |
| SNNPR    |          2022 | 19.713 |        3.024 |            20.146 |         -0.433 |
| SNNPR    |          2023 | 19.683 |        3.161 |            20.146 |         -0.463 |
| SNNPR    |          2024 | 19.798 |        3.105 |            20.146 |         -0.348 |
| Somali   |          2021 | 30.145 |        1.283 |            28.396 |          1.75  |
| Somali   |          2022 | 25.919 |        1.671 |            28.396 |         -2.476 |
| Somali   |          2023 | 28.796 |        1.415 |            28.396 |          0.4   |
| Somali   |          2024 | 28.722 |        1.478 |            28.396 |          0.326 |
| Tigray   |          2021 | 17.594 |        3.159 |            17.737 |         -0.143 |
| Tigray   |          2022 | 16.344 |        3.139 |            17.737 |         -1.393 |
| Tigray   |          2023 | 16.706 |        3.155 |            17.737 |         -1.031 |
| Tigray   |          2024 | 20.303 |        3.068 |            17.737 |          2.567 |

**Interpretation:** Most unusual region-year: Tigray 2024, temperature anomaly +2.57 C.

## B4.3 Plot-reported vs station rainfall

| metric                 |   value |
|:-----------------------|--------:|
| correlation            |   0.007 |
| mean_abs_difference_mm | 501.355 |
| mean_plot_reported_mm  | 856.491 |
| mean_station_season_mm | 371.574 |

**Interpretation:** Differences are plausible because plot reports are local/self-reported while the station table is regional and monthly aggregated.
