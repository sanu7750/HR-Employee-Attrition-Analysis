# Power BI Dashboard UI Design & Layout Specification
## Project ID: HR-Employee-Attrition-Analysis

### Canvas Dimensions & Grid System
- **Aspect Ratio**: 16:9 Standard Canvas (1280 x 720 px or 1920 x 1080 px)
- **Grid Layout**: 4 columns x 3 rows with a consistent 12px padding between cards.
- **Card Containers**: White `#FFFFFF` card shapes with 8px rounded corners and subtle drop shadows (`Blur: 10px, Color: #000000 8%`).

### Theme Palette (JSON Theme file definition)
Save as `HR_Analytics_Theme.json` in Power BI:
```json
{
  "name": "HR_Attrition_Theme",
  "dataColors": [
    "#1B365D",
    "#E05A47",
    "#3498DB",
    "#2ECC71",
    "#F39C12",
    "#9B59B6",
    "#34495E",
    "#16A085"
  ],
  "background": "#F8F9FA",
  "foreground": "#1B365D",
  "tableAccent": "#1B365D"
}
```

### Visual Element Mapping

| Page | Visual Container | Position | Data Fields | Visual Type |
| :--- | :--- | :--- | :--- | :--- |
| **P1** | KPI Strip | Top 15% | Total Staff, Exits, Attrition %, Active Staff | Multi-Row Card / Individual Big Number Cards |
| **P1** | Department Breakdown | Center Left | `Department`, `Attrition Rate %` | Clustered Column Chart |
| **P1** | Role Ranking | Center Right | `JobRole`, `Attrition Rate %` | Horizontal Stacked Bar |
| **P2** | Age Demographics | Top Left | `AgeGroup`, `Attrition Count` | Column Chart |
| **P2** | Career Progression | Bottom Right | `YearsSinceLastPromotion`, `YearsAtCompany` | Scatter / Line Plot |
| **P3** | Overtime Diagnostic | Left Column | `OverTime`, `Attrition Rate %` | 100% Stacked Bar |
| **P3** | Income Analysis | Right Column | `JobLevel`, `MonthlyIncome`, `Attrition` | Clustered Box Plot |
| **P4** | High Flight Risk Table | Bottom 50% | `EmployeeNumber`, `Role`, `MonthlyIncome` | Interactive Filtered Table |
