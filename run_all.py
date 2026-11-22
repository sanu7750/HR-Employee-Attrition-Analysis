"""
Master Pipeline Orchestrator
Project ID: HR-Employee-Attrition-Analysis
Executes all project stages end-to-end:
1. Dataset Verification
2. Data Preprocessing & Feature Engineering
3. Exploratory Data Analysis & Statistical Testing
4. Machine Learning Model Training & Evaluation
5. Database Ingestion & SQL Query Execution
6. Power BI Star Schema Data Export
"""

import sys
import os
import time
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.utils import get_logger

logger = get_logger("MasterOrchestrator")

def run_master_pipeline():
    start_time = time.time()
    print("=" * 80)
    print("  HR EMPLOYEE ATTRITION ANALYSIS - END-TO-END PIPELINE EXECUTION")
    print("  Project ID: HR-Employee-Attrition-Analysis")
    print("=" * 80)

    # Step 1: Dataset Verification & Generation
    print("\n[Step 1/6] Verifying Raw Dataset...")
    from scripts.generate_dataset import generate_hr_dataset
    raw_csv = BASE_DIR / "data" / "raw" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
    if not raw_csv.exists():
        logger.info("Raw CSV missing. Generating benchmark dataset...")
        generate_hr_dataset(str(raw_csv))
    else:
        logger.info(f"Verified raw dataset exists ({raw_csv.stat().st_size:,} bytes).")

    # Step 2: Preprocessing & Feature Engineering
    print("\n[Step 2/6] Running Data Preprocessing & Feature Engineering...")
    from src.data_preprocessing import run_preprocessing_pipeline
    df_clean, df_encoded, model_df = run_preprocessing_pipeline()
    logger.info(f"Cleaned ({df_clean.shape}), Encoded ({df_encoded.shape}), Model Ready ({model_df.shape})")

    # Step 3: EDA & Statistical Testing
    print("\n[Step 3/6] Generating EDA Visualizations & Statistical Tests...")
    from src.eda_analysis import run_eda_pipeline
    chi_df, num_df = run_eda_pipeline()
    logger.info("All 7 EDA figures and Statistical_Summary.md generated.")

    # Step 4: Machine Learning Model Training
    print("\n[Step 4/6] Training & Benchmarking Machine Learning Models...")
    from src.model_training import train_and_evaluate_models
    results_df, best_model_name = train_and_evaluate_models()
    logger.info(f"Top model '{best_model_name}' trained and serialized.")

    # Step 5: Database Setup & SQL Analytics
    print("\n[Step 5/6] Setting Up Database & Executing Enterprise SQL Queries...")
    from scripts.run_sql_queries import run_all_sql
    run_all_sql()
    logger.info("SQLite database populated and SQL analytics results saved.")

    # Step 6: Power BI Data Export
    print("\n[Step 6/6] Generating Star Schema Datasets for Power BI...")
    from power_bi.generate_powerbi_data import generate_powerbi_tables
    generate_powerbi_tables()
    logger.info("Power BI flat file and dimensional tables generated.")

    elapsed = time.time() - start_time
    print("\n" + "=" * 80)
    print(f"  ALL PIPELINE STAGES COMPLETED SUCCESSFULLY IN {elapsed:.2f} SECONDS!")
    print("=" * 80)
    print("\nTo launch the interactive Streamlit Web Application:")
    print("  streamlit run app.py")
    print("\nTo view the Power BI resources:")
    print("  Open power_bi/PowerBI_Dashboard_Setup_Guide.md")
    print("=" * 80)

if __name__ == "__main__":
    run_master_pipeline()
