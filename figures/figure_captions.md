# Figure captions

## fig01_missingness.png
Shows the share of missing or `-999` invalid values in every raw-table column. **Takeaway:** the plot table contains the largest cleaning burden, so sentinel handling and train-fitted imputation are essential before modeling.

## fig02_before_after_cleaning.png
Compares raw and cleaned distributions for price and labor, two variables materially affected by data-quality fixes. **Takeaway:** unit correction and invalid-value handling remove artificial distortions without hand-editing the source files.

## fig03_yield_distribution.png
Shows observed yield distributions for all five crop types in tons/ha. **Takeaway:** crop-specific yield distributions differ enough that crop type is an important predictive feature.

## fig04_region_crop_heatmap.png
Shows mean yield (tons/ha) for every region × crop combination, with sample counts in each cell. **Takeaway:** yield varies jointly by geography and crop, supporting a model that can learn nonlinear interactions.

## fig05_correlation_heatmap.png
Shows Pearson correlations among yield, numeric plot variables, and engineered weather features. **Takeaway:** no single numeric feature explains yield alone; the signal is distributed across agronomic and weather information.

## fig06_climate_by_region.png
Shows monthly average temperature (°C) by region, with an example June–September growing-season window shaded. **Takeaway:** regional and seasonal climate patterns differ materially, supporting the growing-season weather join.

## fig07_yield_vs_season_temp.png
Shows binned mean yield against growing-season mean temperature for each crop. **Takeaway:** crop responses are not identical across temperature ranges, which favors flexible nonlinear models.

## fig08_price_trends.png
Shows cleaned average price in birr/quintal for each crop from 2021–2024. **Takeaway:** price changes affect revenue comparisons, but price remains excluded from the yield model to avoid leakage and causal confusion.

## fig09_revenue_by_crop_region.png
Shows estimated revenue per hectare in birr by crop and region. **Takeaway:** the most valuable crop-region combinations depend on both biological yield and market price, so revenue ranking is not the same as yield ranking.

## fig10_model_comparison.png
Shows validation RMSE (tons/ha) for all compared models, the mean-predictor baseline, and 5-fold CV uncertainty for LightGBM. **Takeaway:** LightGBM has the lowest validation error and remains stable across folds, supporting its selection as the final model.

## fig11_predicted_vs_actual_residuals.png
Shows held-out predicted versus actual yield and residuals versus predictions, both in tons/ha. **Takeaway:** predictions track observed yields closely overall, while the residual panel makes remaining large or systematic errors visible.

## fig12_feature_importance.png
Shows permutation importance for the top final-model features, with weather-derived features highlighted. **Takeaway:** engineered weather contributes measurable predictive information, supporting the assignment requirement and the weather-ablation result.
