-- ====================================================================
-- HR Advanced Analytical SQL (Window Functions, Rankings, Cohorts)
-- Project ID: HR-Employee-Attrition-Analysis
-- Compatibility: SQLite 3.25+, PostgreSQL, MySQL 8.0+
-- ====================================================================

-- Window 1: Departmental Salary Comparison (Difference from Department Average)
-- Identifies employees paid significantly below their department benchmark
WITH DeptStats AS (
    SELECT 
        EmployeeNumber,
        Department,
        JobRole,
        JobLevel,
        MonthlyIncome,
        Attrition,
        AVG(MonthlyIncome) OVER (PARTITION BY Department, JobLevel) AS Dept_Level_Avg_Salary,
        ROUND(MonthlyIncome - AVG(MonthlyIncome) OVER (PARTITION BY Department, JobLevel), 2) AS Salary_Difference_From_Avg,
        ROUND(100.0 * (MonthlyIncome - AVG(MonthlyIncome) OVER (PARTITION BY Department, JobLevel)) / 
              AVG(MonthlyIncome) OVER (PARTITION BY Department, JobLevel), 1) AS Pct_Difference_From_Avg
    FROM hr_employees
)
SELECT 
    EmployeeNumber,
    Department,
    JobRole,
    JobLevel,
    MonthlyIncome,
    ROUND(Dept_Level_Avg_Salary, 0) AS BenchMark_Salary,
    Salary_Difference_From_Avg,
    Pct_Difference_From_Avg,
    Attrition
FROM DeptStats
WHERE Pct_Difference_From_Avg < -15.0
ORDER BY Pct_Difference_From_Avg ASC
LIMIT 15;

-- Window 2: Ranking Job Roles by Attrition Severity within Each Department
WITH RoleAttrition AS (
    SELECT 
        Department,
        JobRole,
        COUNT(*) AS Role_Count,
        SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS Role_Exits,
        ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS Attrition_Rate_Pct
    FROM hr_employees
    GROUP BY Department, JobRole
)
SELECT 
    Department,
    JobRole,
    Role_Count,
    Role_Exits,
    Attrition_Rate_Pct,
    DENSE_RANK() OVER (PARTITION BY Department ORDER BY Attrition_Rate_Pct DESC) AS Dept_Risk_Rank,
    DENSE_RANK() OVER (ORDER BY Attrition_Rate_Pct DESC) AS Overall_Company_Rank
FROM RoleAttrition;

-- Window 3: Quartile Analysis of Compensation by Department
SELECT 
    EmployeeNumber,
    Department,
    JobRole,
    MonthlyIncome,
    NTILE(4) OVER (PARTITION BY Department ORDER BY MonthlyIncome) AS Salary_Quartile,
    Attrition
FROM hr_employees
LIMIT 20;

-- Window 4: Cumulative Tenure Distribution & Running Attrition Totals
WITH TenureAggregation AS (
    SELECT 
        YearsAtCompany,
        COUNT(*) AS Employees_At_Tenure,
        SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS Exits_At_Tenure
    FROM hr_employees
    GROUP BY YearsAtCompany
)
SELECT 
    YearsAtCompany,
    Employees_At_Tenure,
    Exits_At_Tenure,
    SUM(Employees_At_Tenure) OVER (ORDER BY YearsAtCompany) AS Cumulative_Employees,
    SUM(Exits_At_Tenure) OVER (ORDER BY YearsAtCompany) AS Cumulative_Exits,
    ROUND(100.0 * SUM(Exits_At_Tenure) OVER (ORDER BY YearsAtCompany) / 
          SUM(Employees_At_Tenure) OVER (ORDER BY YearsAtCompany), 2) AS Cumulative_Attrition_Rate_Pct
FROM TenureAggregation
ORDER BY YearsAtCompany ASC
LIMIT 15;
