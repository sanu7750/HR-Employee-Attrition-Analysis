-- ====================================================================
-- HR Deep Dive Diagnostic Queries
-- Project ID: HR-Employee-Attrition-Analysis
-- ====================================================================

-- Diagnostic 1: Promotion Stagnation vs Turnover
-- Analyzes whether employees who haven't been promoted in 3+ years exit at higher rates
SELECT 
    CASE 
        WHEN YearsSinceLastPromotion = 0 THEN 'Recent (<1 Yr)'
        WHEN YearsSinceLastPromotion BETWEEN 1 AND 2 THEN 'Moderate (1-2 Yrs)'
        WHEN YearsSinceLastPromotion BETWEEN 3 AND 5 THEN 'Stagnant (3-5 Yrs)'
        ELSE 'Severely Stagnant (6+ Yrs)'
    END AS Promotion_Cohort,
    COUNT(*) AS Headcount,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS Exits,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS Attrition_Rate_Pct,
    ROUND(AVG(MonthlyIncome), 0) AS Avg_Monthly_Income
FROM hr_employees
GROUP BY Promotion_Cohort
ORDER BY Attrition_Rate_Pct DESC;

-- Diagnostic 2: Manager Tenure Stability & Retention
-- "Employees leave bad managers, not companies": Examines manager relationship tenure
SELECT 
    CASE 
        WHEN YearsWithCurrManager = 0 THEN 'New Manager (<1 Yr)'
        WHEN YearsWithCurrManager BETWEEN 1 AND 2 THEN 'Settling (1-2 Yrs)'
        WHEN YearsWithCurrManager BETWEEN 3 AND 6 THEN 'Established (3-6 Yrs)'
        ELSE 'Long-Term (7+ Yrs)'
    END AS Manager_Tenure_Bracket,
    COUNT(*) AS Employee_Count,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS Exits,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS Attrition_Rate_Pct
FROM hr_employees
GROUP BY Manager_Tenure_Bracket
ORDER BY Attrition_Rate_Pct DESC;

-- Diagnostic 3: High Flight Risk Multi-Factor Segment
-- Identifies critical employees with Overtime + Travel Frequently + Low Satisfaction
SELECT 
    EmployeeNumber,
    Department,
    JobRole,
    MonthlyIncome,
    OverTime,
    BusinessTravel,
    OverallSatisfaction,
    YearsAtCompany,
    Attrition
FROM hr_employees
WHERE OverTime = 'Yes' 
  AND BusinessTravel = 'Travel_Frequently' 
  AND OverallSatisfaction <= 2.5
ORDER BY MonthlyIncome ASC;

-- Diagnostic 4: Marital Status & Work-Life Balance Interaction
SELECT 
    MaritalStatus,
    WorkLifeBalance,
    COUNT(*) AS Headcount,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS Exits,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS Attrition_Rate_Pct
FROM hr_employees
GROUP BY MaritalStatus, WorkLifeBalance
ORDER BY MaritalStatus, WorkLifeBalance;

-- Diagnostic 5: Job Level vs Career Loyalty
SELECT 
    JobLevel,
    COUNT(*) AS Headcount,
    ROUND(AVG(YearsAtCompany), 1) AS Avg_Company_Tenure,
    ROUND(AVG(TotalWorkingYears), 1) AS Avg_Career_Years,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS Attrition_Rate_Pct,
    ROUND(AVG(MonthlyIncome), 0) AS Avg_Monthly_Income
FROM hr_employees
GROUP BY JobLevel
ORDER BY JobLevel ASC;
