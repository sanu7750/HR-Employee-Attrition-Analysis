-- ====================================================================
-- HR Employee Attrition Database Schema
-- Project ID: HR-Employee-Attrition-Analysis
-- Compatibility: SQLite, PostgreSQL, MySQL
-- ====================================================================

-- 1. Raw / Consolidated Staging Table
DROP TABLE IF EXISTS hr_employees;

CREATE TABLE hr_employees (
    EmployeeNumber INTEGER PRIMARY KEY,
    Age INTEGER NOT NULL,
    Attrition TEXT NOT NULL,
    BusinessTravel TEXT NOT NULL,
    DailyRate INTEGER,
    Department TEXT NOT NULL,
    DistanceFromHome INTEGER NOT NULL,
    Education INTEGER NOT NULL,
    EducationField TEXT NOT NULL,
    EnvironmentSatisfaction INTEGER NOT NULL,
    Gender TEXT NOT NULL,
    HourlyRate INTEGER,
    JobInvolvement INTEGER NOT NULL,
    JobLevel INTEGER NOT NULL,
    JobRole TEXT NOT NULL,
    JobSatisfaction INTEGER NOT NULL,
    MaritalStatus TEXT NOT NULL,
    MonthlyIncome INTEGER NOT NULL,
    MonthlyRate INTEGER,
    NumCompaniesWorked INTEGER NOT NULL,
    OverTime TEXT NOT NULL,
    PercentSalaryHike INTEGER NOT NULL,
    PerformanceRating INTEGER NOT NULL,
    RelationshipSatisfaction INTEGER NOT NULL,
    StockOptionLevel INTEGER NOT NULL,
    TotalWorkingYears INTEGER NOT NULL,
    TrainingTimesLastYear INTEGER NOT NULL,
    WorkLifeBalance INTEGER NOT NULL,
    YearsAtCompany INTEGER NOT NULL,
    YearsInCurrentRole INTEGER NOT NULL,
    YearsSinceLastPromotion INTEGER NOT NULL,
    YearsWithCurrManager INTEGER NOT NULL,
    -- Engineered columns
    Attrition_Numeric INTEGER,
    AgeGroup TEXT,
    IncomeBracket TEXT,
    TenureGroup TEXT,
    OverallSatisfaction REAL,
    PromotionStagnationRatio REAL,
    LoyaltyRatio REAL
);

-- Indexing for high-performance analytical queries
CREATE INDEX idx_hr_attrition ON hr_employees(Attrition);
CREATE INDEX idx_hr_dept ON hr_employees(Department);
CREATE INDEX idx_hr_role ON hr_employees(JobRole);
CREATE INDEX idx_hr_overtime ON hr_employees(OverTime);
CREATE INDEX idx_hr_joblevel ON hr_employees(JobLevel);
CREATE INDEX idx_hr_income ON hr_employees(MonthlyIncome);
