# D - Modeling & Evaluation

## D1 Baselines

| model         |   RMSE |    MAE |      R2 |   train_seconds |
|:--------------|-------:|-------:|--------:|----------------:|
| Ridge         | 0.899  | 0.6714 |  0.5952 |          0.0402 |
| Mean baseline | 1.4131 | 1.1042 | -0.0001 |          0.0388 |

## D2 Model comparison

| model                  |   RMSE |    MAE |      R2 |   train_seconds |
|:-----------------------|-------:|-------:|--------:|----------------:|
| LightGBM               | 0.46   | 0.3354 |  0.894  |          0.8695 |
| Hist Gradient Boosting | 0.4748 | 0.344  |  0.8871 |          0.7808 |
| Random Forest          | 0.5225 | 0.3832 |  0.8633 |          5.3808 |
| Ridge                  | 0.899  | 0.6714 |  0.5952 |          0.0402 |
| Mean baseline          | 1.4131 | 1.1042 | -0.0001 |          0.0388 |

Winner before tuning: **LightGBM**.

## D3 Cross-validation
Final tuned LightGBM 5-fold RMSE: **0.4690 +/- 0.0114**. Runner-up Hist Gradient Boosting: **0.4737 +/- 0.0116**.

## D4 Out-of-time check
Train 2021-2023, validate 2024: RMSE **0.4845**, MAE **0.3519**, R2 **0.8859**.

## D5 Weather ablation
Without weather: RMSE **0.4899**, MAE **0.3558**, R2 **0.8798**. With weather: RMSE **0.4593**, MAE **0.3356**, R2 **0.8943**. Adding weather **reduced RMSE by 0.0306 t/ha (6.2%)**, from 0.4899 to 0.4593, so the weather join clearly helped.

## D6 Hyperparameter tuning
RandomizedSearchCV: 5 trials, 5-fold CV. Best parameters: `{'model__reg_lambda': 3, 'model__reg_alpha': 0.5, 'model__num_leaves': 47, 'model__n_estimators': 500, 'model__min_child_samples': 10, 'model__learning_rate': 0.035}`. Before tuning LightGBM validation RMSE: **0.4600**; after: **0.4593**.

## D7 Error analysis
See `error_by_crop.csv`, `error_by_region.csv`, and `top10_errors.csv`. We also inspect error against altitude and season temperature.

## D8 Response to findings
D7 showed that several of the largest misses were extreme over/under-predictions, so we tested clipping predictions to the 0.5th–99.5th percentile of the **training-target** range (thresholds learned from training only). Validation RMSE worsened from **0.4593 to 0.4620 t/ha**, so clipping **did not help** and was rejected. We kept the tuned LightGBM unchanged; its tree structure already handles nonlinear altitude/temperature effects without adding a manual transform.

## D9 Plain-language metric
For a farm cooperative manager: our final model has **RMSE = 0.459 tons/ha** (about **16.6% of the mean yield of 2.76 tons/ha**) and **MAE = 0.336 tons/ha** (about **12.1%**). In everyday terms, the typical prediction misses actual yield by about **0.34 tons/ha**; using the average cleaned price of about **4,630 birr/quintal**, that MAE corresponds to roughly **15,537 birr per hectare** of revenue difference (0.336 × 10 × 4,630).
