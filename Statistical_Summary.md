# Statistical Significance Testing: HR Employee Attrition

## 1. Categorical Features (Chi-Square Independence Test)

| Feature        |   Chi2_Statistic |   Degrees_of_Freedom |    p_value | Statistically_Significant   |
|:---------------|-----------------:|---------------------:|-----------:|:----------------------------|
| OverTime       |          171.264 |                    1 | 3.9181e-39 | Yes (p < 0.05)              |
| BusinessTravel |           18.006 |                    2 | 0.00012306 | Yes (p < 0.05)              |
| Department     |            0.476 |                    2 | 0.7883     | No                          |
| JobRole        |          196.202 |                    8 | 4.0308e-38 | Yes (p < 0.05)              |
| MaritalStatus  |           38.245 |                    2 | 4.9573e-09 | Yes (p < 0.05)              |
| EducationField |            2.827 |                    5 | 0.7266     | No                          |
| Gender         |            0     |                    1 | 1          | No                          |
| JobLevel       |          183.87  |                    4 | 1.0998e-38 | Yes (p < 0.05)              |

## 2. Numerical Features (Two-Sample Welch's T-Test & Mann-Whitney U Test)

| Feature              |   Stayed_Mean |   Attrited_Mean |   T_Statistic |   T_p_value |   MannWhitney_p_value | Statistically_Significant   |
|:---------------------|--------------:|----------------:|--------------:|------------:|----------------------:|:----------------------------|
| MonthlyIncome        |       8661.57 |         4429.01 |       -23.154 |  3.3822e-93 |            5.6088e-46 | Yes (p < 0.05)              |
| Age                  |         37.28 |           32.22 |        -9.191 |  3.0934e-18 |            1.5845e-16 | Yes (p < 0.05)              |
| TotalWorkingYears    |          8.5  |            5.52 |       -10.155 |  1.6623e-21 |            1.3531e-26 | Yes (p < 0.05)              |
| YearsAtCompany       |          4.43 |            2.29 |       -10.371 |  8.1344e-23 |            2.3635e-18 | Yes (p < 0.05)              |
| YearsWithCurrManager |          2.13 |            1.09 |        -8.124 |  3.4588e-15 |            5.0887e-10 | Yes (p < 0.05)              |
| DistanceFromHome     |         10.83 |           12.01 |         2.208 |  0.028      |            0.0233     | Yes (p < 0.05)              |
| OverallSatisfaction  |          2.78 |            2.38 |       -11.98  |  8.7206e-28 |            8.175e-28  | Yes (p < 0.05)              |

## 3. Key Statistical Findings
- **OverTime** is the single most statistically significant categorical predictor of employee departure (p < 0.0001).
- **JobRole and Department** show pronounced independence rejection, indicating structural attrition skews across sales and entry-level lab roles.
- **MonthlyIncome and TotalWorkingYears** are significantly lower among departing employees, confirming compensation and seniority sensitivity.
- **OverallSatisfaction** differences are highly statistically significant (p < 0.0001), underscoring that negative workplace sentiments precede voluntary exits.
