"""
Data Loader Module for HR Employee Attrition Analysis.
Handles loading raw and processed datasets with validation and type integrity.
"""

import pandas as pd
import os
from pathlib import Path
from src.utils import RAW_DATA_PATH, CLEANED_DATA_PATH, ENCODED_DATA_PATH, get_logger

logger = get_logger("DataLoader")

def load_raw_data(file_path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Loads the raw HR Employee Attrition dataset from CSV."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Raw data file not found at: {file_path}. Please run dataset generation first.")
    
    logger.info(f"Loading raw dataset from {file_path}...")
    df = pd.read_csv(file_path)
    logger.info(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns successfully.")
    return df

def load_cleaned_data(file_path: Path = CLEANED_DATA_PATH) -> pd.DataFrame:
    """Loads cleaned and feature-engineered dataset."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Cleaned data file not found at: {file_path}. Please run data preprocessing first.")
    
    logger.info(f"Loading cleaned dataset from {file_path}...")
    df = pd.read_csv(file_path)
    logger.info(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns.")
    return df

def load_encoded_data(file_path: Path = ENCODED_DATA_PATH) -> pd.DataFrame:
    """Loads encoded model-ready dataset."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Encoded data file not found at: {file_path}. Please run data preprocessing first.")
    
    logger.info(f"Loading encoded dataset from {file_path}...")
    df = pd.read_csv(file_path)
    return df

def get_data_dictionary() -> dict:
    """Returns metadata description for HR Attrition dataset attributes."""
    return {
        "Age": "Employee age in years (18-60)",
        "Attrition": "Target variable: Employee voluntary departure ('Yes', 'No')",
        "BusinessTravel": "Frequency of travel required for business (Non-Travel, Travel_Rarely, Travel_Frequently)",
        "DailyRate": "Daily billing or compensation rate ($100-$1500)",
        "Department": "Business department (Sales, Research & Development, Human Resources)",
        "DistanceFromHome": "Commute distance in miles from residence to office (1-29 miles)",
        "Education": "Highest education level (1: Below College, 2: College, 3: Bachelor, 4: Master, 5: Doctor)",
        "EducationField": "Major or field of study",
        "EnvironmentSatisfaction": "Work environment satisfaction score (1: Low to 4: Very High)",
        "Gender": "Gender (Female, Male)",
        "HourlyRate": "Hourly pay rate ($30-$100)",
        "JobInvolvement": "Degree of psychological identification with job (1: Low to 4: Very High)",
        "JobLevel": "Hierarchy job tier level (1: Entry to 5: Executive)",
        "JobRole": "Official job title and role designation",
        "JobSatisfaction": "Job satisfaction score (1: Low to 4: Very High)",
        "MaritalStatus": "Marital status (Single, Married, Divorced)",
        "MonthlyIncome": "Gross monthly compensation in USD ($1,009 to $19,999)",
        "MonthlyRate": "Monthly billing or operational rate ($2,000 to $27,000)",
        "NumCompaniesWorked": "Number of previous corporate employers",
        "OverTime": "Exempt overtime requirements ('Yes', 'No')",
        "PercentSalaryHike": "Percentage salary increase last year (11% to 25%)",
        "PerformanceRating": "Appraisal rating (3: Excellent, 4: Outstanding)",
        "RelationshipSatisfaction": "Peer and supervisor relationship satisfaction (1: Low to 4: Very High)",
        "StockOptionLevel": "Company equity allocation tier (0: None to 3: High)",
        "TotalWorkingYears": "Total cumulative career working experience in years",
        "TrainingTimesLastYear": "Number of professional training sessions attended last year (0 to 6)",
        "WorkLifeBalance": "Work-life balance assessment (1: Bad to 4: Best)",
        "YearsAtCompany": "Tenure with current organization in years",
        "YearsInCurrentRole": "Tenure in current job role in years",
        "YearsSinceLastPromotion": "Years elapsed since last promotion in years",
        "YearsWithCurrManager": "Years reporting to current direct manager in years"
    }

if __name__ == "__main__":
    df = load_raw_data()
    print("Columns:", df.columns.tolist())
    print("Head:\n", df.head(2))
