-- ====================================================================
-- HR Employee Attrition KPI Queries
-- Project ID: HR-Employee-Attrition-Analysis
-- ====================================================================

-- KPI 1: Company-Wide Executive Summary Overview
-- Calculates Total Headcount, Total Exits, Overall Attrition Rate %, Active Headcount, and Average Salary
SELECT 
    COUNT(*) AS Total_Employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS Total_Attrition,
    SUM(CASE WHEN Attrition = 'No' THEN 1 ELSE 0 END) AS Active_Employees,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS Attrition_Rate_Pct,
    ROUND(AVG(MonthlyIncome), 2) AS Avg_Monthly_Income,
    ROUND(AVG(Age), 1) AS Avg_Age,
    ROUND(AVG(YearsAtCompany), 1) AS Avg_Tenure_Years
FROM hr_employees;

-- KPI 2: Department-Level Breakdown
-- Evaluates headcount distribution and turnover rates by business unit
SELECT 
    Department,
    COUNT(*) AS Total_Staff,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS Attrition_Count,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS Attrition_Rate_Pct,
    ROUND(AVG(MonthlyIncome), 2) AS Avg_Monthly_Income,
    ROUND(AVG(OverallSatisfaction), 2) AS Avg_Overall_Satisfaction
FROM hr_employees
GROUP BY Department
ORDER BY Attrition_Rate_Pct DESC;

-- KPI 3: Job Role Attrition Ranking
-- Identifies highest-flight-risk job roles across the company
SELECT 
    JobRole,
    Department,
    COUNT(*) AS Role_Headcount,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS Role_Attrition,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS Attrition_Rate_Pct,
    ROUND(AVG(MonthlyIncome), 0) AS Avg_Monthly_Income,
    ROUND(AVG(WorkLifeBalance), 2) AS Avg_WorkLifeBalance
FROM hr_employees
GROUP BY JobRole, Department
ORDER BY Attrition_Rate_Pct DESC;

-- KPI 4: Overtime Impact Comparison
-- Quantifies the exact turnover risk multiplier caused by mandatory/exempt overtime
SELECT 
    OverTime,
    COUNT(*) AS Total_Count,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS Attrition_Count,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS Attrition_Rate_Pct,
    ROUND(AVG(MonthlyIncome), 2) AS Avg_Monthly_Income,
    ROUND(AVG(WorkLifeBalance), 2) AS Avg_WorkLifeBalance
FROM hr_employees
GROUP BY OverTime;

-- KPI 5: Business Travel Frequency Analysis
-- Measures the attrition correlation with business travel intensity
SELECT 
    BusinessTravel,
    COUNT(*) AS Total_Count,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS Attrition_Count,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS Attrition_Rate_Pct,
    ROUND(AVG(JobSatisfaction), 2) AS Avg_Job_Satisfaction
FROM hr_employees
GROUP BY BusinessTravel
ORDER BY Attrition_Rate_Pct DESC;

-- KPI 6: Monthly Income Tier (Salary Band) Attrition
SELECT 
    IncomeBracket,
    COUNT(*) AS Headcount,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS Exits,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS Attrition_Rate_Pct
FROM hr_employees
WHERE IncomeBracket IS NOT NULL
GROUP BY IncomeBracket
ORDER BY Attrition_Rate_Pct DESC;

-- KPI 7: Age Cohort Analysis
SELECT 
    AgeGroup,
    COUNT(*) AS Headcount,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS Exits,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS Attrition_Rate_Pct,
    ROUND(AVG(MonthlyIncome), 0) AS Avg_Monthly_Income
FROM hr_employees
WHERE AgeGroup IS NOT NULL
GROUP BY AgeGroup
ORDER BY AgeGroup ASC;

-- KPI 8: Workplace Satisfaction Comparison: Stayed vs Left
SELECT 
    Attrition,
    COUNT(*) AS Employee_Count,
    ROUND(AVG(JobSatisfaction), 2) AS Avg_Job_Satisfaction,
    ROUND(AVG(EnvironmentSatisfaction), 2) AS Avg_Environment_Satisfaction,
    ROUND(AVG(RelationshipSatisfaction), 2) AS Avg_Relationship_Satisfaction,
    ROUND(AVG(WorkLifeBalance), 2) AS Avg_WorkLife_Balance,
    ROUND(AVG(OverallSatisfaction), 2) AS Avg_Composite_Satisfaction
FROM hr_employees
GROUP BY Attrition;

-- KPI 9: Commute Distance Tier Impact
SELECT 
    CASE 
        WHEN DistanceFromHome <= 5 THEN '1. Near (1-5 mi)'
        WHEN DistanceFromHome <= 15 THEN '2. Moderate (6-15 mi)'
        ELSE '3. Far (16+ mi)'
    END AS Commute_Category,
    COUNT(*) AS Total_Staff,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS Exits,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS Attrition_Rate_Pct
FROM hr_employees
GROUP BY Commute_Category
ORDER BY Commute_Category ASC;

-- KPI 10: Stock Option Level vs Retention
SELECT 
    StockOptionLevel,
    COUNT(*) AS Total_Employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS Attrition_Count,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS Attrition_Rate_Pct,
    ROUND(AVG(MonthlyIncome), 0) AS Avg_Monthly_Income
FROM hr_employees
GROUP BY StockOptionLevel
ORDER BY StockOptionLevel ASC;
