# Power BI Dashboard Setup & Architecture Guide
## Project ID: HR-Employee-Attrition-Analysis

This comprehensive guide enables you to build a multi-page Power BI Executive Dashboard using the prepared datasets and DAX measures.

---

## 1. Data Ingestion & Data Model Setup

### Option A: Single Flat Model (Easiest & Recommended)
1. Open **Power BI Desktop**.
2. Click **Get Data** > **Text/CSV**.
3. Select `power_bi/data/HR_Analytics_PowerBI_Clean.csv`.
4. Click **Transform Data** (or Load directly).
5. Ensure data types are detected:
   - `MonthlyIncome`, `TotalWorkingYears`, `YearsAtCompany`, `Age`: **Whole Number** or **Decimal**
   - `Attrition`, `Department`, `JobRole`, `OverTime`: **Text**
   - `Attrition Rate %`: Set Data Format to **Percentage (1 decimal place)**.

### Option B: Star Schema Dimensional Model
If building an enterprise relational model:
- Load `power_bi/data/Fact_Attrition.csv` (Fact Table)
- Load `power_bi/data/Dim_Department.csv` (Dimension)
- Load `power_bi/data/Dim_JobRole.csv` (Dimension)
- Load `power_bi/data/Dim_Education.csv` (Dimension)
- In the **Model View**, establish the following 1-to-Many (`1:*`) Single-Direction relationships:
  - `Dim_Department[DepartmentID]` -> `Dim_JobRole[DepartmentID]`
  - `Dim_JobRole[JobRoleID]` -> `Fact_Attrition[JobRoleID]`
  - `Dim_Education[EducationLevel]` -> `Fact_Attrition[Education]`

---

## 2. Importing DAX Measures
1. In the **Modeling** tab, click **New Measure**.
2. Copy and paste each measure from `power_bi/DAX_Measures.dax`.
3. Create a dedicated measure table called `_KeyMeasures` by clicking **Enter Data** and naming the table `_KeyMeasures`.

---

## 3. Four-Page Dashboard Architecture

### Page 1: Executive KPI Overview (High-Level Snapshot)
- **Top Header KPI Cards**:
  - `Total Employees` (e.g. 1,470)
  - `Attrition Count` (e.g. 236)
  - `Attrition Rate %` (e.g. 16.1%)
  - `Active Headcount` (e.g. 1,234)
  - `Avg Monthly Income` (e.g. $6,503)
- **Visuals**:
  - **Donut Chart**: Attrition Split (`Legend: Attrition`, `Values: Total Employees`). Colors: Attrited (`#E05A47`), Active (`#1B365D`).
  - **Clustered Column Chart**: Attrition Rate % by `Department`.
  - **Horizontal Bar Chart**: Attrition Rate % by `JobRole` (sorted descending).
  - **Slicers (Top/Left Pane)**: Department, Gender, Overtime (Yes/No), Age Group.

### Page 2: Demographics & Career Trajectory
- **Visuals**:
  - **Stacked Bar Chart**: Headcount and Exits by `AgeGroup` (`<25`, `25-34`, `35-44`, etc.).
  - **Scatter Plot / Bubble Chart**: X-axis `TotalWorkingYears`, Y-axis `MonthlyIncome`, Legend `Attrition`.
  - **Clustered Bar Chart**: Attrition by `MaritalStatus` and `Gender`.
  - **Line Chart**: Attrition % across `YearsAtCompany` (Tenure Curve showing peak departure at Year 1-2).
  - **Table / Matrix**: `JobRole` vs `EducationField` with Conditional Background Formatting for Attrition Rate.

### Page 3: Compensation, Overtime & Burnout Diagnostics
- **Visuals**:
  - **Card**: `Overtime Attrition Rate %` vs `Non-Overtime Attrition Rate %` (Side-by-side callout).
  - **Grouped Bar Chart**: Attrition by `IncomeBracket` (<$3k, $3k-$5k, $5k-$8k, $8k-$12k, $12k+).
  - **100% Stacked Bar Chart**: `BusinessTravel` vs `Attrition`.
  - **Box & Whisker / Distribution Plot**: Monthly Income by `JobLevel` and `Attrition`.
  - **Gauge Chart**: `Average Work Life Balance` (Target: 3.5 / 4.0).

### Page 4: Flight Risk Predictor & Actionable Strategy
- **Visuals**:
  - **Card Callout**: `Total Estimated Turnover Cost` ($ Millions) & `Potential Turnover Savings (20% Reduction)`.
  - **Interactive Flight Risk Matrix**:
    - Filter: `OverTime = Yes` AND `OverallSatisfaction <= 2.5`.
    - Columns: `EmployeeNumber`, `Department`, `JobRole`, `MonthlyIncome`, `YearsAtCompany`, `YearsSinceLastPromotion`.
  - **Key Influencer Visual**: Analyze `Attrition = Yes`, Explained by `OverTime`, `MonthlyIncome`, `JobRole`, `JobSatisfaction`, `StockOptionLevel`.
  - **Smart Narrative / Text Box**: Executive HR Recommendations (Pay realignments, Overtime capping, Mentorship).

---

## 4. Visual Formatting & Color Standards

| Element | Color Name | Hex Code |
| :--- | :--- | :--- |
| **Primary Brand / Active Employees** | Navy Blue | `#1B365D` |
| **Attrition / Warning / Alert** | Coral Red | `#E05A47` |
| **Secondary Accent / Highlight** | Sky Blue | `#3498DB` |
| **Success / Retention** | Emerald Green | `#2ECC71` |
| **Background Fill** | Pure White / Light Slate | `#F8F9FA` |
| **Font Family** | Segoe UI Semibold | Standard Power BI |
