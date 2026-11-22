# Machine Learning Model Performance Evaluation Report
## Project ID: HR-Employee-Attrition-Analysis

### 1. Executive Summary & Model Selection
The primary goal of the predictive modeling pipeline is to proactively identify employees at elevated risk of voluntary departure before resignations occur. Four candidate classifiers were evaluated using 5-fold stratified cross-validation and an independent hold-out test set (20%).

**Top Selected Model**: `Logistic Regression` achieved an **ROC-AUC of 0.9962** and balanced recall.

### 2. Comprehensive Model Benchmark Table

| Model               |   Accuracy |   Precision |   Recall |   F1_Score |   ROC_AUC |   CV_Recall_Mean |   CV_ROC_AUC_Mean |
|:--------------------|-----------:|------------:|---------:|-----------:|----------:|-----------------:|------------------:|
| Logistic Regression |     0.9694 |      0.8519 |   0.9787 |     0.9109 |    0.9962 |           0.9947 |            0.9981 |
| Gradient Boosting   |     0.932  |      0.8649 |   0.6809 |     0.7619 |    0.9686 |           0.6353 |            0.9682 |
| Random Forest       |     0.9048 |      0.6863 |   0.7447 |     0.7143 |    0.9481 |           0.7836 |            0.9564 |
| Decision Tree       |     0.8197 |      0.4605 |   0.7447 |     0.5691 |    0.8446 |           0.8148 |            0.858  |

### 3. Detailed Classification Report (Best Model)

```text
              precision    recall  f1-score   support

      Stayed     0.9958    0.9676    0.9815       247
    Attrited     0.8519    0.9787    0.9109        47

    accuracy                         0.9694       294
   macro avg     0.9238    0.9732    0.9462       294
weighted avg     0.9728    0.9694    0.9702       294

```

### 4. Confusion Matrix Breakdown
- **True Negatives (Correctly Identified Retained Employees)**: 239
- **False Positives (Retained Flagged as Attrition Risk)**: 8
- **False Negatives (Missed Attrition Exits)**: 1
- **True Positives (Successfully Flagged Attrition Risks)**: 46

### 5. Business Value & Cost-Benefit Alignment
- **Cost of False Negatives (FN)**: An unpredicted voluntary exit incurs substantial turnover costs (typically 50% to 150% of annual salary in recruiting, onboarding, and productivity downtime).
- **Cost of False Positives (FP)**: Low cost (conducting stay interviews, manager check-ins, or career development touchpoints).
- **Recommendation**: Operating at a calibrated decision threshold that maximizes Recall ensures HR catches 80%+ of flight risks early.

### 6. Top Predictive Drivers of Attrition
- **MonthlyIncome**: Score 0.1358
- **OverTime_Yes**: Score 0.1140
- **IncomeBracket**: Score 0.0792
- **OverallSatisfaction**: Score 0.0559
- **JobLevel**: Score 0.0536
- **TotalWorkingYears**: Score 0.0448
- **JobSatisfaction**: Score 0.0378
