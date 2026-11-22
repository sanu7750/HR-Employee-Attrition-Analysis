@echo off
title HR Employee Attrition Intelligence Pipeline
color 0B

echo ==============================================================================
echo       HR EMPLOYEE ATTRITION & WORKFORCE INTELLIGENCE SYSTEM
echo       Project ID: HR-Employee-Attrition-Analysis
echo ==============================================================================
echo.
echo [1/2] Executing Master Data Science, SQL and Power BI Pipeline...
python scripts\run_all.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Pipeline encountered an error. Please check your Python environment.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/2] Launching Interactive Streamlit Analytics Web Application...
echo The dashboard will automatically open in your default browser at http://localhost:8501
echo Press Ctrl+C in this terminal window to stop the server when finished.
echo.
streamlit run app.py

pause
