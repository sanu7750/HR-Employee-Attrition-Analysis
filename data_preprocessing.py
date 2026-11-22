"""
Data Preprocessing & Feature Engineering Module
Project ID: HR-Employee-Attrition-Analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path
from src.utils import (
    RAW_DATA_PATH, CLEANED_DATA_PATH, ENCODED_DATA_PATH, 
    MODEL_DATA_PATH, get_logger
)
from src.data_loader import load_raw_data

logger = get_logger("DataPreprocessing")

def clean_and_engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw data, removes zero-variance columns, and creates rich HR business features.
    """
    logger.info("Starting data cleaning and feature engineering...")
    df_clean = df.copy()

    # 1. Drop redundant / zero-variance / uninformative columns
    drop_cols = ['EmployeeCount', 'StandardHours', 'Over18']
    existing_drops = [c for c in drop_cols if c in df_clean.columns]
    if existing_drops:
        df_clean = df_clean.drop(columns=existing_drops)
        logger.info(f"Dropped constant columns: {existing_drops}")

    # 2. Binary target indicator
    df_clean['Attrition_Numeric'] = df_clean['Attrition'].map({'Yes': 1, 'No': 0}).astype(int)

    # 3. Categorical Binning & Business Groupings
    # Age Groups
    age_bins = [17, 25, 35, 45, 55, 65]
    age_labels = ['<25', '25-34', '35-44', '45-54', '55+']
    df_clean['AgeGroup'] = pd.cut(df_clean['Age'], bins=age_bins, labels=age_labels, right=False)

    # Income Brackets
    income_bins = [0, 3000, 5000, 8000, 12000, 30000]
    income_labels = ['Under $3K', '$3K-$5K', '$5K-$8K', '$8K-$12K', '$12K+']
    df_clean['IncomeBracket'] = pd.cut(df_clean['MonthlyIncome'], bins=income_bins, labels=income_labels)

    # Tenure Groups
    tenure_bins = [-1, 1, 3, 6, 10, 50]
    tenure_labels = ['<1 Year', '1-3 Years', '4-6 Years', '7-10 Years', '10+ Years']
    df_clean['TenureGroup'] = pd.cut(df_clean['YearsAtCompany'], bins=tenure_bins, labels=tenure_labels)

    # Distance Tier
    df_clean['CommuteTier'] = pd.cut(
        df_clean['DistanceFromHome'], 
        bins=[-1, 5, 15, 35], 
        labels=['Near (<=5 mi)', 'Moderate (6-15 mi)', 'Far (>15 mi)']
    )

    # 4. Domain-Specific HR Ratios & Composite Scores
    # Composite Satisfaction Score (Scale 1 to 4)
    df_clean['OverallSatisfaction'] = (
        df_clean['EnvironmentSatisfaction'] +
        df_clean['JobSatisfaction'] +
        df_clean['RelationshipSatisfaction'] +
        df_clean['WorkLifeBalance']
    ) / 4.0

    # Career Stagnation Ratio (Years since last promotion relative to tenure)
    df_clean['PromotionStagnationRatio'] = (
        df_clean['YearsSinceLastPromotion'] / (df_clean['YearsAtCompany'] + 1)
    ).round(3)

    # Organizational Loyalty Ratio (Years at company relative to total working years)
    df_clean['LoyaltyRatio'] = (
        df_clean['YearsAtCompany'] / (df_clean['TotalWorkingYears'] + 1)
    ).round(3)

    # Manager Stability Ratio
    df_clean['ManagerStabilityRatio'] = (
        df_clean['YearsWithCurrManager'] / (df_clean['YearsAtCompany'] + 1)
    ).round(3)

    # High Burnout Risk Flag (OverTime = Yes AND BusinessTravel = Travel_Frequently)
    df_clean['BurnoutRiskFlag'] = (
        (df_clean['OverTime'] == 'Yes') & (df_clean['BusinessTravel'] == 'Travel_Frequently')
    ).astype(int)

    # Low Compensation Satisfaction Proxy
    df_clean['LowIncomeJobLevelRatio'] = (
        df_clean['MonthlyIncome'] / (df_clean['JobLevel'] * 3000)
    ).round(3)

    logger.info(f"Cleaned dataset shape: {df_clean.shape}")
    return df_clean

def encode_dataset(df_clean: pd.DataFrame) -> pd.DataFrame:
    """
    Applies one-hot encoding to categorical features for Machine Learning models.
    """
    logger.info("Encoding categorical features for modeling...")
    df_encoded = df_clean.copy()

    # Drop identifier and target strings not used directly in feature matrix
    ignore_cols = ['EmployeeNumber', 'Attrition']
    # Also ignore helper bin categoricals in the raw numeric encoding if they duplicate original columns
    categorical_cols = [
        'BusinessTravel', 'Department', 'EducationField', 'Gender',
        'JobRole', 'MaritalStatus', 'OverTime'
    ]

    # One-Hot Encode nominal variables
    df_encoded = pd.get_dummies(
        df_encoded, 
        columns=categorical_cols, 
        drop_first=True, 
        dtype=int
    )

    # Ensure all columns are numeric
    # For bin columns, convert to categorical codes or drop
    bin_cols = ['AgeGroup', 'IncomeBracket', 'TenureGroup', 'CommuteTier']
    for c in bin_cols:
        if c in df_encoded.columns:
            df_encoded[c] = df_encoded[c].cat.codes

    logger.info(f"Encoded dataset shape: {df_encoded.shape}")
    return df_encoded

def run_preprocessing_pipeline():
    """Executes the full data preprocessing, feature engineering, and file export pipeline."""
    df_raw = load_raw_data(RAW_DATA_PATH)
    
    # Clean and Engineer
    df_clean = clean_and_engineer_features(df_raw)
    df_clean.to_csv(CLEANED_DATA_PATH, index=False)
    logger.info(f"Cleaned data saved to {CLEANED_DATA_PATH}")

    # Encode for ML
    df_encoded = encode_dataset(df_clean)
    df_encoded.to_csv(ENCODED_DATA_PATH, index=False)
    logger.info(f"Encoded data saved to {ENCODED_DATA_PATH}")

    # Prepare model-ready feature matrix (X and y)
    feature_cols = [c for c in df_encoded.columns if c not in ['Attrition_Numeric', 'Attrition', 'EmployeeNumber']]
    model_df = df_encoded[feature_cols + ['Attrition_Numeric']]
    model_df.to_csv(MODEL_DATA_PATH, index=False)
    logger.info(f"Model-ready data saved to {MODEL_DATA_PATH} ({model_df.shape[1]} columns)")

    return df_clean, df_encoded, model_df

if __name__ == '__main__':
    run_preprocessing_pipeline()
