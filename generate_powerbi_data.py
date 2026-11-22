"""
Power BI Data Preparation Module
Project ID: HR-Employee-Attrition-Analysis
Generates enriched dimensional tables (Star Schema) and flat analytics datasets for Power BI.
"""

import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.utils import CLEANED_DATA_PATH, POWERBI_DATA_DIR, get_logger

logger = get_logger("PowerBIPrep")

def generate_powerbi_tables():
    """Builds and exports Power BI Star Schema and enriched flat datasets."""
    logger.info("Generating Power BI datasets...")
    df = pd.read_csv(CLEANED_DATA_PATH)

    # 1. Human-Readable Label Mappings
    edu_map = {1: '1 - Below College', 2: '2 - College', 3: '3 - Bachelor', 4: '4 - Master', 5: '5 - Doctor'}
    sat_map = {1: '1 - Low', 2: '2 - Medium', 3: '3 - High', 4: '4 - Very High'}
    wlb_map = {1: '1 - Bad', 2: '2 - Good', 3: '3 - Better', 4: '4 - Best'}
    perf_map = {3: '3 - Excellent', 4: '4 - Outstanding'}

    df_pbi = df.copy()
    df_pbi['Education_Label'] = df_pbi['Education'].map(edu_map)
    df_pbi['EnvironmentSatisfaction_Label'] = df_pbi['EnvironmentSatisfaction'].map(sat_map)
    df_pbi['JobSatisfaction_Label'] = df_pbi['JobSatisfaction'].map(sat_map)
    df_pbi['RelationshipSatisfaction_Label'] = df_pbi['RelationshipSatisfaction'].map(sat_map)
    df_pbi['WorkLifeBalance_Label'] = df_pbi['WorkLifeBalance'].map(wlb_map)
    df_pbi['PerformanceRating_Label'] = df_pbi['PerformanceRating'].map(perf_map)
    
    # Financial impact calculation: Average cost to replace = 1.25 * Annual Salary
    df_pbi['EstimatedReplacementCost'] = (df_pbi['MonthlyIncome'] * 12 * 1.25).round(0)

    # Export Flattened Power BI Ready Dataset
    flat_path = POWERBI_DATA_DIR / "HR_Analytics_PowerBI_Clean.csv"
    df_pbi.to_csv(flat_path, index=False)
    logger.info(f"Saved primary flat Power BI dataset to {flat_path}")

    # 2. Star Schema Dimension 1: Dim_Department
    depts = df_pbi[['Department']].drop_duplicates().reset_index(drop=True)
    depts['DepartmentID'] = range(1, len(depts) + 1)
    dept_path = POWERBI_DATA_DIR / "Dim_Department.csv"
    depts.to_csv(dept_path, index=False)
    logger.info(f"Saved Dim_Department to {dept_path}")

    # 3. Star Schema Dimension 2: Dim_JobRole
    roles = df_pbi[['JobRole', 'Department']].drop_duplicates().reset_index(drop=True)
    roles['JobRoleID'] = range(1, len(roles) + 1)
    roles = roles.merge(depts, on='Department')
    role_path = POWERBI_DATA_DIR / "Dim_JobRole.csv"
    roles[['JobRoleID', 'JobRole', 'DepartmentID']].to_csv(role_path, index=False)
    logger.info(f"Saved Dim_JobRole to {role_path}")

    # 4. Star Schema Dimension 3: Dim_Education
    edu_df = pd.DataFrame({
        'EducationLevel': [1, 2, 3, 4, 5],
        'EducationName': ['Below College', 'College', 'Bachelor Degree', 'Master Degree', 'Doctorate'],
        'StandardYears': [12, 14, 16, 18, 21]
    })
    edu_path = POWERBI_DATA_DIR / "Dim_Education.csv"
    edu_df.to_csv(edu_path, index=False)
    logger.info(f"Saved Dim_Education to {edu_path}")

    # 5. Star Schema Fact Table: Fact_Attrition
    fact_cols = [
        'EmployeeNumber', 'Age', 'Attrition', 'Attrition_Numeric',
        'BusinessTravel', 'DailyRate', 'DistanceFromHome', 'Education',
        'EducationField', 'EnvironmentSatisfaction', 'Gender', 'HourlyRate',
        'JobInvolvement', 'JobLevel', 'JobRole', 'JobSatisfaction',
        'MaritalStatus', 'MonthlyIncome', 'MonthlyRate', 'NumCompaniesWorked',
        'OverTime', 'PercentSalaryHike', 'PerformanceRating',
        'RelationshipSatisfaction', 'StockOptionLevel', 'TotalWorkingYears',
        'TrainingTimesLastYear', 'WorkLifeBalance', 'YearsAtCompany',
        'YearsInCurrentRole', 'YearsSinceLastPromotion', 'YearsWithCurrManager',
        'OverallSatisfaction', 'PromotionStagnationRatio', 'LoyaltyRatio',
        'EstimatedReplacementCost'
    ]
    fact_df = df_pbi[fact_cols].copy()
    fact_df = fact_df.merge(roles[['JobRole', 'JobRoleID', 'DepartmentID']], on='JobRole', how='left')
    fact_path = POWERBI_DATA_DIR / "Fact_Attrition.csv"
    fact_df.to_csv(fact_path, index=False)
    logger.info(f"Saved Fact_Attrition to {fact_path}")

if __name__ == '__main__':
    generate_powerbi_tables()
