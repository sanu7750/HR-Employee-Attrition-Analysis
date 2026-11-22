# 👥 HR Employee Attrition Analysis & Workforce Intelligence
### Enterprise People Analytics, Statistical Diagnostics, Machine Learning & Power BI Dashboard

![Project Status](https://img.shields.io/badge/Status-Complete-success.svg)
![Project ID](https://img.shields.io/badge/Project%20ID-HR--Employee--Attrition--Analysis-blue.svg)
![Python](https://img.shields.io/badge/Python-3.13+-3776AB.svg?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B.svg?logo=streamlit&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-Star_Schema-F2C811.svg?logo=powerbi&logoColor=black)
![Database](https://img.shields.io/badge/Database-SQLite-003B57.svg?logo=sqlite&logoColor=white)

---

## 📌 Executive Overview

Voluntary employee turnover imposes an enormous financial and operational toll on modern organizations. Replacing a single corporate employee typically costs **75% to 150% of their base annual salary** due to recruitment campaigns, onboarding cycles, lost institutional domain knowledge, and decreased team productivity.

This repository delivers an **end-to-end People Analytics solution** for **1,470 employees across 35 multi-dimensional features**, featuring:
* **Interactive Web Application**: Streamlit dashboard with KPI analytics, deep-dive slicers, SQL query console, and a real-time flight risk simulator.
* **Predictive ML Classifiers**: Balanced Logistic Regression, Random Forest, Gradient Boosting, and Decision Trees (achieving **96.9% accuracy** and **97.9% recall** on hold-out data).
* **Enterprise SQL Analytics**: Complete SQLite relational database with DDL schemas, KPI queries, cohort diagnostics, and window functions.
* **Power BI Dashboard Bundle**: Star-schema dimension and fact tables, 30+ production DAX measures, and step-by-step UI design guidelines.
* **Pre-executed Jupyter Notebook**: Complete analysis notebook pre-rendered with inline plots and statistical hypothesis tests.

---

## 📊 Key Executive Findings & Metrics

```
+---------------------------------------------------------------------------------------+
|                               EXECUTIVE HEADLINE KPIS                                 |
+----------------------+--------------------+--------------------+----------------------+
| Total Headcount      | Voluntary Exits    | Active Headcount   | Baseline Attrition   |
| 1,470 Employees      | 236 Departures     | 1,234 Retained     | 16.05%               |
+----------------------+--------------------+--------------------+----------------------+
| Avg Salary (Stayed)  | Avg Salary (Left)  | Avg Tenure         | Turnover Exposure    |
| $6,833 / month       | $4,787 / month     | 7.0 Years          | $17.14 Million       |
+----------------------+--------------------+--------------------+----------------------+
```

1. **The Overtime Hazard ($\chi^2 = 87.2, p < 0.0001$)**: Employees working mandatory overtime suffer a **30.5% attrition rate**, nearly triple the **10.4% rate** of their non-overtime peers.
2. **The 24-Month Flight Window**: Over **41.5%** of all voluntary resignations occur within the first 2 years of company tenure.
3. **Compensation & Role Disparities**: Sales Representatives (**39.8% attrition**) and Laboratory Technicians (**23.9% attrition**) face severe turnover due to entry-level pay compression ($30% salary gap vs retained staff).
4. **Managerial Tenure Buffer**: Turnover drops from **28.4%** down to **9.1%** once an employee reports to the same manager for more than 2 years.

---

## 📁 Repository Structure

```
E:\HR Employee Attrition Analysis\
│
├── data\
│   ├── raw\
│   │   └── WA_Fn-UseC_-HR-Employee-Attrition.csv        # 1,470 rows, 35 attributes benchmark
│   └── processed\
│       ├── hr_attrition_cleaned.csv                    # Cleaned dataset with engineered features
│       ├── hr_attrition_encoded.csv                    # One-hot encoded feature matrix
│       └── model_ready_features.csv                    # Feature vector for ML modeling
│
├── database\
│   └── hr_attrition.db                                 # Populated SQLite database
│
├── sql\
│   ├── 01_schema_setup.sql                             # DDL table creation and indexing
│   ├── 02_hr_attrition_kpis.sql                        # 10 core executive KPI queries
│   ├── 03_deep_dive_analysis.sql                       # 5 diagnostic cohort queries
│   └── 04_window_functions_advanced.sql                # Window functions, rankings & quartiles
│
├── src\
│   ├── __init__.py
│   ├── data_loader.py                                  # Data ingestion & schema definitions
│   ├── data_preprocessing.py                           # Cleaning, ratios, binning & encoding
│   ├── eda_analysis.py                                 # Visualizations & statistical tests
│   ├── model_training.py                               # Model benchmarks & artifact persistence
│   └── utils.py                                        # Paths, loggers, styling constants
│
├── notebooks\
│   └── HR_Employee_Attrition_Analysis.ipynb            # Pre-executed Jupyter Notebook
│
├── power_bi\
│   ├── data\
│   │   ├── HR_Analytics_PowerBI_Clean.csv              # Enriched flat Power BI dataset
│   │   ├── Fact_Attrition.csv                          # Fact table
│   │   ├── Dim_Department.csv                          # Dimension: Departments
│   │   ├── Dim_JobRole.csv                             # Dimension: Roles
│   │   └── Dim_Education.csv                           # Dimension: Education Tiers
│   ├── DAX_Measures.dax                                # 30+ production DAX measures
│   ├── Dashboard_Design_Specification.md               # Theme, layout grid & canvas specs
│   └── PowerBI_Dashboard_Setup_Guide.md                # 4-page Power BI construction guide
│
├── reports\
│   ├── HR_Attrition_Executive_Report.md                # 10-page executive advisory report
│   ├── Model_Performance_Evaluation.md                 # Machine Learning benchmark report
│   ├── Statistical_Summary.md                          # Chi-Square & T-test findings
│   ├── sql_query_results.md                            # Formatted SQL execution tables
│   └── figures\                                        # Publication-quality charts
│       ├── 01_attrition_overview.png
│       ├── 02_attrition_by_department_and_role.png
│       ├── 03_attrition_by_overtime_and_travel.png
│       ├── 04_monthly_income_and_joblevel.png
│       ├── 05_satisfaction_metrics_heatmap.png
│       ├── 06_feature_correlation_matrix.png
│       ├── 07_tenure_and_career_path.png
│       ├── 08_feature_importance.png
│       ├── 09_roc_auc_curves.png
│       └── 10_confusion_matrix.png
│
├── models\
│   ├── best_attrition_model.pkl                        # Serialized best model pipeline
│   ├── scaler.pkl                                      # Fitted standard scaler
│   └── feature_columns.json                            # 54 feature column definitions
│
├── scripts\
│   ├── generate_dataset.py                             # Benchmark data generator
│   ├── build_notebook.py                               # Automated notebook builder
│   ├── run_sql_queries.py                              # SQL execution & report generator
│   └── run_all.py                                      # Master pipeline orchestrator
│
├── app.py                                              # Interactive Streamlit Web Application
├── requirements.txt                                    # Python dependencies
├── run_project.bat                                     # One-click Windows launcher
└── README.md                                           # Comprehensive documentation
```

---

## 🚀 How to Run the Project

### Option 1: One-Click Execution (Windows Batch)
Simply double-click:
```cmd
run_project.bat
```
*This script runs the entire pipeline end-to-end and immediately launches the interactive web application in your default browser.*

---

### Option 2: Launch the Interactive Streamlit Web Application
Navigate to the project folder and launch the web dashboard:
```bash
cd "E:\HR Employee Attrition Analysis"
streamlit run app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your web browser.
* **Tab 1**: Executive KPI Dashboard with interactive Plotly visuals.
* **Tab 2**: Deep-Dive Diagnostic Analytics (Overtime, Income, Satisfaction).
* **Tab 3**: Interactive Flight Risk Simulator (Adjust employee sliders to calculate live departure probability).
* **Tab 4**: Interactive SQL Query Console (Run SQL queries against the local database).

---

### Option 3: Run the Master End-to-End Pipeline via Python
To regenerate all datasets, rerun machine learning models, execute SQL queries, and rebuild all reports:
```bash
cd "E:\HR Employee Attrition Analysis"
python scripts\run_all.py
```

---

### Option 4: Open the Pre-Executed Jupyter Notebook
Inspect the full narrative, inline plots, and statistical testing cells:
```bash
cd "E:\HR Employee Attrition Analysis"
jupyter lab notebooks/HR_Employee_Attrition_Analysis.ipynb
# Or
jupyter notebook notebooks/HR_Employee_Attrition_Analysis.ipynb
```

---

### Option 5: Build the Power BI Dashboard
1. Open **Power BI Desktop**.
2. Click **Get Data** > **Text/CSV** and select:
   `E:\HR Employee Attrition Analysis\power_bi\data\HR_Analytics_PowerBI_Clean.csv`
3. Open `power_bi/DAX_Measures.dax` and copy the DAX measures into your model.
4. Follow the comprehensive setup steps in [PowerBI_Dashboard_Setup_Guide.md](file:///E:/HR%20Employee%20Attrition%20Analysis/power_bi/PowerBI_Dashboard_Setup_Guide.md).

---

## 🤖 Machine Learning Model Benchmark

Four candidate models were evaluated using 5-fold stratified cross-validation and an independent hold-out test set (294 employees):

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Logistic Regression (Balanced)** | **96.94%** | **85.19%** | **97.87%** | **0.9109** | **0.9962** |
| **Gradient Boosting** | 93.20% | 86.49% | 68.09% | 0.7619 | 0.9686 |
| **Random Forest (Balanced)** | 90.48% | 68.63% | 74.47% | 0.7143 | 0.9481 |
| **Decision Tree (Balanced)** | 81.97% | 46.05% | 74.47% | 0.5691 | 0.8446 |

> **Why Logistic Regression was selected**: In workforce attrition management, **False Negatives** (failing to catch an employee who quits) carry a massive financial penalty ($1.25x salary), whereas **False Positives** carry negligible cost (a supportive manager 1-on-1). Logistic Regression with balanced weighting achieved **97.87% recall**, successfully flagging nearly every flight risk.

---

## 💡 Strategic People Analytics Recommendations

1. **Mandatory Overtime Ceiling (Immediate - 30 Days)**: Cap consecutive overtime weeks to curtail burnout, which currently drives a 30.5% attrition spike.
2. **First-Year Flight Triage (Immediate - 30 Days)**: Introduce 90-day structured peer onboarding mentorship to address the early-career cliff.
3. **Compensation Parity (Medium-Term - 90 Days)**: Re-index entry-level Sales Representative and Laboratory Technician compensation to the 50th market percentile.
4. **Promotion Velocity (Long-Term - 180 Days)**: Establish transparent 24-month career checkpoints so high performers without promotions receive structured advancement paths.

---

## 📄 License & Attribution
* **Project ID**: `HR-Employee-Attrition-Analysis`
* Built for enterprise workforce diagnostic analytics and talent retention optimization.
