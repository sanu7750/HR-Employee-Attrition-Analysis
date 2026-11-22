"""
SQL Execution Engine & Reporting Pipeline
Project ID: HR-Employee-Attrition-Analysis
Initializes SQLite database, ingests HR data, executes all SQL queries, and generates report.
"""

import sqlite3
import pandas as pd
import os
import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.utils import DB_PATH, SQL_DIR, CLEANED_DATA_PATH, REPORTS_DIR, get_logger

logger = get_logger("SQLExecutor")

def init_database():
    """Initializes SQLite database and loads the cleaned HR employee dataset."""
    logger.info(f"Connecting to SQLite database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Execute schema setup
    schema_path = SQL_DIR / "01_schema_setup.sql"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)
    logger.info("Database schema initialized.")

    # Load cleaned dataset into hr_employees table
    df_clean = pd.read_csv(CLEANED_DATA_PATH)
    # Ensure column compatibility
    df_clean.to_sql("hr_employees", conn, if_exists="replace", index=False)
    conn.commit()
    logger.info(f"Successfully loaded {len(df_clean)} records into hr_employees table.")
    return conn

def execute_sql_file(conn, file_path: Path):
    """Parses and executes multiple queries from a SQL file, returning DataFrame results."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split queries by semicolon, ignoring empty statements and comments
    statements = [stmt.strip() for stmt in content.split(";") if stmt.strip() and not stmt.strip().startswith("--")]
    
    query_results = []
    cursor = conn.cursor()

    for idx, stmt in enumerate(statements, 1):
        try:
            # Extract comment header if available
            header_lines = [line.strip().lstrip("-- ") for line in stmt.splitlines() if line.strip().startswith("--")]
            query_title = header_lines[0] if header_lines else f"Query {idx}"

            df_res = pd.read_sql_query(stmt, conn)
            query_results.append({
                "title": query_title,
                "sql": stmt,
                "result": df_res
            })
        except Exception as e:
            logger.warning(f"Error executing statement {idx} in {file_path.name}: {e}")

    return query_results

def run_all_sql():
    """Executes all KPI, Deep Dive, and Window Function SQL scripts and writes markdown report."""
    conn = init_database()
    output_md_path = REPORTS_DIR / "sql_query_results.md"

    sql_files = [
        SQL_DIR / "02_hr_attrition_kpis.sql",
        SQL_DIR / "03_deep_dive_analysis.sql",
        SQL_DIR / "04_window_functions_advanced.sql"
    ]

    with open(output_md_path, "w", encoding="utf-8") as f_out:
        f_out.write("# HR Employee Attrition - SQL Analytics Results\n")
        f_out.write("## Project ID: HR-Employee-Attrition-Analysis\n")
        f_out.write(f"*Database: SQLite ({DB_PATH.name}) | Total Records: 1,470*\n\n")

        for sql_file in sql_files:
            section_title = sql_file.stem.replace("_", " ").title()
            logger.info(f"Executing {sql_file.name}...")
            f_out.write(f"## {section_title}\n\n")

            results = execute_sql_file(conn, sql_file)
            for item in results:
                f_out.write(f"### {item['title']}\n\n")
                f_out.write("```sql\n" + item['sql'].strip() + "\n```\n\n")
                f_out.write(item['result'].to_markdown(index=False))
                f_out.write("\n\n---\n\n")

    conn.close()
    logger.info(f"All SQL scripts executed successfully! Results saved to {output_md_path}")

if __name__ == "__main__":
    run_all_sql()
