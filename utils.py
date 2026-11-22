"""
Utility functions and configuration for HR Employee Attrition Analysis.
Project ID: HR-Employee-Attrition-Analysis
"""

import os
import sys
import logging
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_PATH = DATA_DIR / "raw" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
CLEANED_DATA_PATH = PROCESSED_DATA_DIR / "hr_attrition_cleaned.csv"
ENCODED_DATA_PATH = PROCESSED_DATA_DIR / "hr_attrition_encoded.csv"
MODEL_DATA_PATH = PROCESSED_DATA_DIR / "model_ready_features.csv"

DATABASE_DIR = BASE_DIR / "database"
DB_PATH = DATABASE_DIR / "hr_attrition.db"

SQL_DIR = BASE_DIR / "sql"
REPORTS_DIR = BASE_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
MODELS_DIR = BASE_DIR / "models"
POWERBI_DATA_DIR = BASE_DIR / "power_bi" / "data"

# Ensure essential directories exist
for folder in [PROCESSED_DATA_DIR, DATABASE_DIR, FIGURES_DIR, MODELS_DIR, POWERBI_DATA_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# Logger Configuration
def get_logger(name: str = "HR_Analytics") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            fmt="[%(asctime)s] %(levelname)s - %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger

# Palette Constants for Consistent Visuals
COLORS = {
    "primary": "#1B365D",      # Deep Navy
    "secondary": "#E05A47",    # Coral Red (Attrition = Yes)
    "neutral_dark": "#2C3E50", # Dark Slate
    "neutral_light": "#ECF0F1",# Light Gray
    "accent_blue": "#3498DB",  # Blue (Attrition = No)
    "accent_green": "#2ECC71", # Emerald Green
    "warning_yellow": "#F39C12"
}
