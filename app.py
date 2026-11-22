"""
HR Employee Attrition Analytics & Prediction Web Application
Project ID: HR-Employee-Attrition-Analysis
Built with Streamlit, Plotly, Pandas, and Scikit-Learn
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import json
import sqlite3
import os
import sys
from pathlib import Path

# Setup Path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from src.utils import (
    CLEANED_DATA_PATH, DB_PATH, MODELS_DIR, COLORS
)

# Page Configuration
st.set_page_config(
    page_title="HR Employee Attrition Intelligence",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Dashboard Aesthetic
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1B365D;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #5C768D;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #1B365D;
    }
    .badge-pill {
        display: inline-block;
        padding: 4px 12px;
        background-color: #EBF3FB;
        color: #1B365D;
        font-weight: 600;
        border-radius: 16px;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv(CLEANED_DATA_PATH)
    return df

@st.cache_resource
def load_ml_assets():
    model_bundle = joblib.load(MODELS_DIR / "best_attrition_model.pkl")
    scaler = joblib.load(MODELS_DIR / "scaler.pkl")
    with open(MODELS_DIR / "feature_columns.json", "r") as f:
        feature_cols = json.load(f)
    return model_bundle, scaler, feature_cols

try:
    df_raw = load_data()
    model_bundle, scaler, feature_cols = load_ml_assets()
    best_model = model_bundle["model"]
    use_scaled = model_bundle["use_scaled"]
except Exception as e:
    st.error(f"Error loading system assets: {e}. Please ensure data preprocessing and model training scripts have run.")
    st.stop()

# -------------------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------------------
st.sidebar.image("https://images.unsplash.com/photo-1521791136064-7986c2920216?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3", use_container_width=True)
st.sidebar.markdown("### 🎛️ Analytics Slicers")

# Filter: Department
dept_options = ["All"] + sorted(df_raw['Department'].dropna().unique().tolist())
selected_dept = st.sidebar.selectbox("Department", dept_options)

# Filter: Job Role
if selected_dept != "All":
    available_roles = sorted(df_raw[df_raw['Department'] == selected_dept]['JobRole'].unique().tolist())
else:
    available_roles = sorted(df_raw['JobRole'].dropna().unique().tolist())
selected_role = st.sidebar.selectbox("Job Role", ["All"] + available_roles)

# Filter: OverTime
ot_filter = st.sidebar.radio("Overtime Requirement", ["All", "Yes", "No"], horizontal=True)

# Filter: Age Range
min_age = int(df_raw['Age'].min())
max_age = int(df_raw['Age'].max())
selected_age_range = st.sidebar.slider("Age Bracket", min_age, max_age, (min_age, max_age))

# Apply Filters
filtered_df = df_raw.copy()
if selected_dept != "All":
    filtered_df = filtered_df[filtered_df['Department'] == selected_dept]
if selected_role != "All":
    filtered_df = filtered_df[filtered_df['JobRole'] == selected_role]
if ot_filter != "All":
    filtered_df = filtered_df[filtered_df['OverTime'] == ot_filter]
filtered_df = filtered_df[(filtered_df['Age'] >= selected_age_range[0]) & (filtered_df['Age'] <= selected_age_range[1])]

# -------------------------------------------------------------
# TOP HEADER
# -------------------------------------------------------------
col_title, col_badge = st.columns([3, 1])
with col_title:
    st.markdown('<p class="main-header">HR Employee Attrition & Retention Intelligence</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Diagnostic Analytics, Workforce Risk Modeling & Strategic Retention Pipeline</p>', unsafe_allow_html=True)
with col_badge:
    st.markdown('<div style="text-align: right;"><span class="badge-pill">Project ID: HR-Employee-Attrition-Analysis</span></div>', unsafe_allow_html=True)

# KPI Metric Row
total_count = len(filtered_df)
attrited_count = int(filtered_df['Attrition_Numeric'].sum())
attrition_rate = (attrited_count / total_count * 100) if total_count > 0 else 0
avg_salary = filtered_df['MonthlyIncome'].mean() if total_count > 0 else 0
avg_tenure = filtered_df['YearsAtCompany'].mean() if total_count > 0 else 0

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
with kpi1:
    st.metric("Total Headcount", f"{total_count:,}")
with kpi2:
    st.metric("Voluntary Exits", f"{attrited_count:,}", delta=f"{attrition_rate:.1f}% Attrition", delta_color="inverse")
with kpi3:
    st.metric("Attrition Rate", f"{attrition_rate:.1f}%", delta="Benchmark 16.1%", delta_color="off")
with kpi4:
    st.metric("Avg Monthly Income", f"${avg_salary:,.0f}")
with kpi5:
    st.metric("Avg Company Tenure", f"{avg_tenure:.1f} Yrs")

st.markdown("---")

# -------------------------------------------------------------
# MAIN DASHBOARD TABS
# -------------------------------------------------------------
tab_exec, tab_diag, tab_predict, tab_sql = st.tabs([
    "📊 Executive KPI Dashboard", 
    "🔍 Deep-Dive Diagnostic Analytics", 
    "🎯 Predictive Flight Risk Simulator",
    "💾 SQL Query Console & Database"
])

# -------------------------------------------------------------
# TAB 1: EXECUTIVE KPI DASHBOARD
# -------------------------------------------------------------
with tab_exec:
    st.subheader("Workforce Attrition Overview")
    row1_c1, row1_c2 = st.columns([1, 2])

    with row1_c1:
        # Donut Chart: Overall Attrition Ratio
        attr_counts = filtered_df['Attrition'].value_counts()
        fig_donut = go.Figure(data=[go.Pie(
            labels=attr_counts.index,
            values=attr_counts.values,
            hole=0.55,
            marker_colors=[COLORS['accent_blue'], COLORS['secondary']],
            textinfo='label+percent'
        )])
        fig_donut.update_layout(
            title_text="Attrition Proportion",
            margin=dict(t=40, b=20, l=20, r=20),
            height=340,
            showlegend=False
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with row1_c2:
        # Bar Chart: Attrition Rate by Department
        dept_grp = filtered_df.groupby('Department')['Attrition_Numeric'].agg(['count', 'mean']).reset_index()
        dept_grp['rate'] = dept_grp['mean'] * 100
        fig_dept = px.bar(
            dept_grp,
            x='Department',
            y='rate',
            color='rate',
            color_continuous_scale='Reds',
            text=dept_grp['rate'].apply(lambda x: f"{x:.1f}%"),
            title="Attrition Rate (%) by Department",
            labels={'rate': 'Attrition Rate (%)'}
        )
        fig_dept.update_layout(height=340, margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig_dept, use_container_width=True)

    st.subheader("Job Role Attrition Severity Ranking")
    role_grp = filtered_df.groupby('JobRole')['Attrition_Numeric'].agg(['count', 'sum', 'mean']).reset_index()
    role_grp['rate'] = (role_grp['mean'] * 100).round(1)
    role_grp = role_grp.sort_values(by='rate', ascending=True)

    fig_role = px.bar(
        role_grp,
        x='rate',
        y='JobRole',
        orientation='h',
        color='rate',
        color_continuous_scale='Blues',
        text='rate',
        title="Job Roles Ranked by Attrition Rate (%)",
        labels={'rate': 'Attrition Rate (%)', 'JobRole': 'Job Role'}
    )
    fig_role.update_layout(height=420, margin=dict(t=40, b=20, l=20, r=20))
    st.plotly_chart(fig_role, use_container_width=True)

# -------------------------------------------------------------
# TAB 2: DEEP DIVE DIAGNOSTIC ANALYTICS
# -------------------------------------------------------------
with tab_diag:
    st.subheader("Turnover Drivers & Environmental Stress Factors")
    col_d1, col_d2 = st.columns(2)

    with col_d1:
        # Overtime vs Non-Overtime
        ot_stat = filtered_df.groupby('OverTime')['Attrition_Numeric'].mean().reset_index()
        ot_stat['rate'] = ot_stat['Attrition_Numeric'] * 100
        fig_ot = px.bar(
            ot_stat,
            x='OverTime',
            y='rate',
            color='OverTime',
            color_discrete_map={'Yes': COLORS['secondary'], 'No': COLORS['accent_blue']},
            text=ot_stat['rate'].apply(lambda x: f"{x:.1f}%"),
            title="Overtime Impact: Attrition Rate (%)",
            labels={'rate': 'Attrition Rate (%)'}
        )
        fig_ot.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig_ot, use_container_width=True)

    with col_d2:
        # Business Travel Frequency
        travel_stat = filtered_df.groupby('BusinessTravel')['Attrition_Numeric'].mean().reset_index()
        travel_stat['rate'] = travel_stat['BusinessTravel'].map(
            lambda t: filtered_df[filtered_df['BusinessTravel'] == t]['Attrition_Numeric'].mean() * 100
        )
        fig_travel = px.bar(
            travel_stat,
            x='BusinessTravel',
            y='rate',
            color='rate',
            color_continuous_scale='Purples',
            text=travel_stat['rate'].apply(lambda x: f"{x:.1f}%"),
            title="Travel Intensity vs Attrition Rate (%)",
            labels={'rate': 'Attrition Rate (%)'}
        )
        fig_travel.update_layout(height=350)
        st.plotly_chart(fig_travel, use_container_width=True)

    col_d3, col_d4 = st.columns(2)
    with col_d3:
        # Monthly Income Distribution Boxplot
        fig_inc = px.box(
            filtered_df,
            x='JobLevel',
            y='MonthlyIncome',
            color='Attrition',
            color_discrete_map={'No': COLORS['accent_blue'], 'Yes': COLORS['secondary']},
            title="Monthly Income by Job Level & Attrition Status"
        )
        fig_inc.update_layout(height=380)
        st.plotly_chart(fig_inc, use_container_width=True)

    with col_d4:
        # Tenure at Company vs Manager
        fig_scatter = px.scatter(
            filtered_df,
            x='YearsAtCompany',
            y='YearsWithCurrManager',
            color='Attrition',
            color_discrete_map={'No': COLORS['accent_blue'], 'Yes': COLORS['secondary']},
            title="Company Tenure vs Years With Current Manager",
            opacity=0.7
        )
        fig_scatter.update_layout(height=380)
        st.plotly_chart(fig_scatter, use_container_width=True)

# -------------------------------------------------------------
# TAB 3: PREDICTIVE FLIGHT RISK SIMULATOR
# -------------------------------------------------------------
with tab_predict:
    st.subheader("Interactive Employee Flight Risk Assessment Simulator")
    st.markdown("Adjust an employee's profile attributes below to evaluate their **real-time voluntary departure probability** using our trained Machine Learning classification model.")

    with st.form("risk_prediction_form"):
        f_col1, f_col2, f_col3 = st.columns(3)
        
        with f_col1:
            st.markdown("##### 👤 Employee Profile")
            inp_age = st.slider("Age", 18, 65, 32)
            inp_dept = st.selectbox("Department", ['Sales', 'Research & Development', 'Human Resources'])
            inp_gender = st.selectbox("Gender", ['Male', 'Female'])
            inp_marital = st.selectbox("Marital Status", ['Single', 'Married', 'Divorced'])
            inp_dist = st.slider("Distance from Home (Miles)", 1, 30, 8)
            inp_edu_field = st.selectbox("Education Field", ['Life Sciences', 'Medical', 'Marketing', 'Technical Degree', 'Human Resources', 'Other'])

        with f_col2:
            st.markdown("##### 💼 Role & Compensation")
            inp_role = st.selectbox("Job Role", [
                'Sales Executive', 'Research Scientist', 'Laboratory Technician',
                'Manufacturing Director', 'Healthcare Representative', 'Manager',
                'Sales Representative', 'Research Director', 'Human Resources'
            ])
            inp_job_level = st.slider("Job Level (1 to 5)", 1, 5, 2)
            inp_income = st.number_input("Monthly Income ($)", min_value=1000, max_value=25000, value=4500, step=250)
            inp_overtime = st.selectbox("Mandatory Overtime", ['Yes', 'No'])
            inp_travel = st.selectbox("Business Travel", ['Travel_Rarely', 'Travel_Frequently', 'Non-Travel'])
            inp_stocks = st.slider("Stock Option Level", 0, 3, 0)

        with f_col3:
            st.markdown("##### 🌟 Satisfaction & Tenure")
            inp_job_sat = st.slider("Job Satisfaction (1-4)", 1, 4, 2)
            inp_env_sat = st.slider("Environment Satisfaction (1-4)", 1, 4, 2)
            inp_wlb = st.slider("Work-Life Balance (1-4)", 1, 4, 2)
            inp_rel_sat = st.slider("Relationship Satisfaction (1-4)", 1, 4, 3)
            inp_involvement = st.slider("Job Involvement (1-4)", 1, 4, 2)
            inp_tenure = st.slider("Years at Company", 0, 30, 3)
            inp_mgr_years = st.slider("Years with Current Manager", 0, 20, 1)
            inp_promo_years = st.slider("Years Since Last Promotion", 0, 15, 1)
            inp_twy = st.slider("Total Working Years", 0, 40, 7)

        submit_btn = st.form_submit_button("🚀 Calculate Flight Risk Score", use_container_width=True)

    if submit_btn:
        # Construct single-row DataFrame matching the model feature pipeline
        row_dict = {
            'Age': inp_age,
            'DailyRate': 800,
            'DistanceFromHome': inp_dist,
            'Education': 3,
            'EnvironmentSatisfaction': inp_env_sat,
            'HourlyRate': 65,
            'JobInvolvement': inp_involvement,
            'JobLevel': inp_job_level,
            'JobSatisfaction': inp_job_sat,
            'MonthlyIncome': inp_income,
            'MonthlyRate': 14000,
            'NumCompaniesWorked': 2,
            'PercentSalaryHike': 15,
            'PerformanceRating': 3,
            'RelationshipSatisfaction': inp_rel_sat,
            'StockOptionLevel': inp_stocks,
            'TotalWorkingYears': inp_twy,
            'TrainingTimesLastYear': 2,
            'WorkLifeBalance': inp_wlb,
            'YearsAtCompany': inp_tenure,
            'YearsInCurrentRole': max(0, inp_tenure - 1),
            'YearsSinceLastPromotion': inp_promo_years,
            'YearsWithCurrManager': inp_mgr_years,
            # Engineered Features
            'OverallSatisfaction': (inp_env_sat + inp_job_sat + inp_rel_sat + inp_wlb) / 4.0,
            'PromotionStagnationRatio': inp_promo_years / (inp_tenure + 1),
            'LoyaltyRatio': inp_tenure / (inp_twy + 1),
            'ManagerStabilityRatio': inp_mgr_years / (inp_tenure + 1),
            'BurnoutRiskFlag': 1 if (inp_overtime == 'Yes' and inp_travel == 'Travel_Frequently') else 0,
            'LowIncomeJobLevelRatio': inp_income / (inp_job_level * 3000),
            # Bin category codes
            'AgeGroup': 1 if inp_age < 35 else 2,
            'IncomeBracket': 1 if inp_income < 5000 else 2,
            'TenureGroup': 1 if inp_tenure < 4 else 2,
            'CommuteTier': 0 if inp_dist <= 5 else (1 if inp_dist <= 15 else 2)
        }

        # Initialize full vector with zeros
        input_vector = pd.DataFrame(0, index=[0], columns=feature_cols)
        for k, v in row_dict.items():
            if k in input_vector.columns:
                input_vector.at[0, k] = v

        # Apply One-Hot columns
        oh_cols = [
            f"BusinessTravel_{inp_travel}",
            f"Department_{inp_dept}",
            f"EducationField_{inp_edu_field}",
            f"Gender_{inp_gender}",
            f"JobRole_{inp_role}",
            f"MaritalStatus_{inp_marital}",
            f"OverTime_{inp_overtime}"
        ]
        for col in oh_cols:
            if col in input_vector.columns:
                input_vector.at[0, col] = 1

        # Predict
        if use_scaled:
            features_transformed = scaler.transform(input_vector)
            prob = best_model.predict_proba(features_transformed)[0][1]
        else:
            prob = best_model.predict_proba(input_vector)[0][1]

        prob_pct = prob * 100

        st.markdown("---")
        res_col1, res_col2 = st.columns([1, 2])
        with res_col1:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob_pct,
                title={'text': "Attrition Risk Score (%)", 'font': {'size': 20}},
                number={'suffix': "%"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#1B365D"},
                    'steps': [
                        {'range': [0, 30], 'color': "#2ECC71"},
                        {'range': [30, 65], 'color': "#F39C12"},
                        {'range': [65, 100], 'color': "#E05A47"}
                    ]
                }
            ))
            fig_gauge.update_layout(height=280, margin=dict(t=30, b=10, l=20, r=20))
            st.plotly_chart(fig_gauge, use_container_width=True)

        with res_col2:
            if prob_pct >= 65:
                st.error(f"⚠️ **HIGH RETENTION RISK DETECTED ({prob_pct:.1f}%)**")
                st.markdown("""
                **Immediate Recommended Interventions:**
                - **Overtime Mitigation**: Employee is facing high workload stress; review project allocations and cap mandatory overtime.
                - **Immediate Stay Interview**: Schedule a 1-on-1 check-in within 7 business days to assess career friction and sentiment.
                - **Compensation Audit**: Cross-reference market salary bands to ensure competitive pay parity.
                """)
            elif prob_pct >= 30:
                st.warning(f"⚡ **MODERATE RETENTION RISK ({prob_pct:.1f}%)**")
                st.markdown("""
                **Proactive Retention Measures:**
                - **Manager Touchpoint**: Enhance communication cadence and clear roadblocks with their direct manager.
                - **Career Development Path**: Explore promotion timeline or lateral skill development opportunities.
                """)
            else:
                st.success(f"✅ **LOW RETENTION RISK ({prob_pct:.1f}%)**")
                st.markdown("""
                **Maintenance Best Practices:**
                - Employee displays strong engagement and stability indicators.
                - Continue regular recognition, annual performance appraisals, and leadership development.
                """)

# -------------------------------------------------------------
# TAB 4: SQL QUERY CONSOLE & DATABASE
# -------------------------------------------------------------
with tab_sql:
    st.subheader("Interactive SQL Analytical Console")
    st.markdown("Run enterprise SQL queries against the local SQLite database (`database/hr_attrition.db`) in real-time.")

    prebuilt_queries = {
        "Executive KPI Overview": """
SELECT 
    COUNT(*) AS Total_Employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS Total_Attrition,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS Attrition_Rate_Pct,
    ROUND(AVG(MonthlyIncome), 2) AS Avg_Monthly_Income,
    ROUND(AVG(YearsAtCompany), 1) AS Avg_Tenure_Years
FROM hr_employees;
        """,
        "Department Attrition Breakdown": """
SELECT 
    Department,
    COUNT(*) AS Total_Staff,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS Attrition_Count,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS Attrition_Rate_Pct,
    ROUND(AVG(MonthlyIncome), 2) AS Avg_Monthly_Income
FROM hr_employees
GROUP BY Department
ORDER BY Attrition_Rate_Pct DESC;
        """,
        "Overtime Impact Analysis": """
SELECT 
    OverTime,
    COUNT(*) AS Total_Count,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS Attrition_Count,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS Attrition_Rate_Pct,
    ROUND(AVG(MonthlyIncome), 2) AS Avg_Monthly_Income
FROM hr_employees
GROUP BY OverTime;
        """,
        "Salary Quartiles Window Function": """
SELECT 
    EmployeeNumber,
    Department,
    JobRole,
    MonthlyIncome,
    NTILE(4) OVER (PARTITION BY Department ORDER BY MonthlyIncome) AS Salary_Quartile,
    Attrition
FROM hr_employees
LIMIT 25;
        """
    }

    selected_query_label = st.selectbox("Choose Pre-Built Query", list(prebuilt_queries.keys()))
    default_sql = prebuilt_queries[selected_query_label].strip()

    custom_sql = st.text_area("SQL Statement", value=default_sql, height=180)

    if st.button("▶️ Execute Query"):
        try:
            conn = sqlite3.connect(DB_PATH)
            sql_df = pd.read_sql_query(custom_sql, conn)
            conn.close()
            st.success(f"Query returned {len(sql_df)} records.")
            st.dataframe(sql_df, use_container_width=True)
            
            # CSV Download
            csv_data = sql_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Result CSV",
                data=csv_data,
                file_name="hr_sql_result.csv",
                mime="text/csv"
            )
        except Exception as err:
            st.error(f"SQL Execution Error: {err}")
