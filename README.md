# Ethiopian Smallholder Crop-Yield Challenge — Alpha Team

End-to-end Qiyas AI Hackathon solution: cleaning, weather integration, analysis, 12 figures, leakage-safe modeling, evaluation, final submission and Streamlit demo.

## Alpha Team
1. Saron Hailemichael
2. Abdi Mudesir
3. Meftuha Kedir
4. Wissam Jemal
5. Yedidya Solomon
6. Kidist Dagnachaew

Team roster is also provided in `alpha_team_members.csv`.

## Start here (learning order)
1. `notebooks/01_cleaning_and_integration.ipynb` - understand raw data, cleaning, weather/price joins, features, checks.
2. `notebooks/02_analysis_report.ipynb` - all 14 required analysis questions and interpretation.
3. `notebooks/03_visualizations.ipynb` - all 12 required figures and what each means.
4. `notebooks/04_modeling_and_evaluation.ipynb` - encoding, scaling, leakage-safe pipelines, baselines, 3+ model families, 5-fold CV, out-of-time test, weather ablation, tuning and errors. **Spend most study time here for model accuracy.**
5. `app/app.py` - final Streamlit demo.
6. `presentation/alpha_team_crop_yield_ai_slides.pptx` - 5-slide presentation.

## Data leakage rules used
- Test labels are never available or inferred.
- Price is excluded from model features; it is used only for revenue analysis/demo.
- Learned imputation, encoding and scaling are inside sklearn Pipelines and fitted on training data/folds only.
- Test data is used only once for final prediction.
- Model choice/tuning uses train validation/CV only.

## Final model results
Validation RMSE: **0.4593 t/ha**, MAE: **0.3356**, R2: **0.8943**. 5-fold CV RMSE: **0.4690 +/- 0.0114**.

## Run
```bash
pip install -r requirements.txt
jupyter lab
# then run notebooks 01 -> 04
streamlit run app/app.py
```

## Submission
`submission/team_crop_champions_submission.csv` contains exactly 3,750 plot IDs in template order and numeric predictions.

## Streamlit Community Cloud Deployment

This project is deployed on Streamlit Community Cloud.

**Live Application:**  
https://alpha-crop-yield-system-u8xcqcmlsyerdkrth4hwzf.streamlit.app/

The application is deployed directly from the GitHub repository using:

- Branch: `main`
- Main file: `app/app.py`
- Python version: `3.12`

Updates pushed to the GitHub repository are automatically reflected in the deployed application.

```bash
streamlit run app/app.py --server.address 0.0.0.0 --server.port $PORT --server.headless true
```

The Streamlit app automatically looks up weather and market price from `app/assets/`; the user never types those values. Price is used only to calculate revenue, not as a yield-model feature.

## Final quality check
Run the automated project checker before submission:

```bash
python tests/final_project_test.py
```

It checks required files, processed data, figures, model loading, submission validity, presentation slide count, Alpha Team roster and Python syntax. A Markdown report is written to `reports/automatic_test_report.md`.


Our Crop Yield Prediction System is now deployed and accessible at: https://alpha-crop-yield-system-u8xcqcmlsyerdkrth4hwzf.streamlit.app/