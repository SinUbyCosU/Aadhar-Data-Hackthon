# Aadhaar Data Analysis - Hackathon 2026

## What This Is

This project analyzes Aadhaar enrollment and update data to find patterns and solve real problems. We discovered that seasonal migration causes people to miss biometric updates, which can lead to losing access to government benefits.

**Start here:** Read [SIMPLE_EXPLANATION.md](SIMPLE_EXPLANATION.md) for a plain-language overview of what we found and why it matters.

## Key Documents

### Easy to Read
- **[SIMPLE_EXPLANATION.md](SIMPLE_EXPLANATION.md)** - The problem, solution, and impact explained simply (start here!)
- **[INSIGHTS.md](INSIGHTS.md)** - Key statistics and findings by state and district

### Detailed Analysis
- **[EXECUTIVE_BRIEF.md](EXECUTIVE_BRIEF.md)** - Summary for decision-makers
- **[STRATEGIC_POLICY_FRAMEWORK.md](STRATEGIC_POLICY_FRAMEWORK.md)** - Complete policy recommendations
- **[COMPREHENSIVE_TECHNICAL_REPORT.md](analysis_outputs/strategic_analysis/COMPREHENSIVE_TECHNICAL_REPORT.md)** - Full technical methodology

## What's Inside

```
├── analysis/                              # Python scripts for data analysis
│   ├── advanced_risk_analysis.py         # Main analysis - calculates risk scores
│   ├── generate_presentation_dashboard.py # Creates interactive charts
│   └── requirements.txt                  # List of needed software packages
├── analysis_outputs/strategic_analysis/   # Results and visualizations
├── api_data_aadhar_enrolment/            # Enrollment data (CSV files)
├── api_data_aadhar_demographic/          # Demographic data (CSV files)
└── api_data_aadhar_biometric/            # Biometric data (CSV files)
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Git

### Installation Steps
How to Run This

### What You Need
- Python 3.8 or newer
- Git

### Setup Steps

```powershell
# Download the code
# Install dependencies
pip install -r analysis/requirements.txt
```

## Usage

### 1. Generate National Insights Report
```powershell
python analysis/generate_insights.py
```
**Output:** `INSIGHTS.md` and `analysis_outputs/insights/insights_summary.json`

### 2. Run Advanced Risk Analysis
```powershell
python analysis/advanced_risk_analysis.py
```
**Output:** CERS scores, risk assessments, and intervention frameworks in `analysis_outputs/strategic_analysis/`

### 3. Create Interactive Dashboards
```powershell
python analysis/generate_presentation_dashboard.py
```
**Output:** HTML visualizations in `analysis_outputs/strategic_analysis/`

### 4. Comparative Dataset Analysis
```powershell
python analysis/multi_dataset_analysis.py
```
**Output:** Cross-dataset comparisons in `analysis_outputs/dashboard/`

### 5. Per-Dataset Deep Dive
```powershell
# Analyze specific datasets
python analysis/biometric_analysis.py "api_data_aadhar_biometric"
python analysis/biometric_analysis.py "api_data_aadhar_demographic"
python analysis/biometric_analysis.py "api_data_aadhar_enrolment"
```
**Output:** Interactive Plotly HTML charts in respective `analysis_outputs/` subdirectories

## Key Features

### Advanced Analytics
- **Citizen Exclusion Risk Score (CERS):** Novel predictive metric for identifying high-risk districts
- **Seasonal Migration Analysis:** Correlation between agricultural cycles and biometric update patterns
- **Statistical Validation:** Hypothesis testing with p-value < 0.05 significance threshold
- **Multi-component Risk Modeling:** Gap Risk, Migration Risk, Volatility Risk, Volume Pressure

### Visualizations
- Interactive Plotly HTML dashboards
- Geographic risk mapping
- Time series seasonal analysis
- Economic impact comparisons
- 3D PCA projections
- Sankey diagrams for state-district flows

### Policy Recommendations
- AI-driven mobile enrollment unit routing
- Proactive citizen alert systems
- District capacity building frameworks
- Seasonal resource allocation strategies

## Data Sources

This analysis processes the following datasets:
- **Enrolment Data:** 1,006,029 records across 985 districts
- **Demographic Data:** 2,071,700 records across 983 districts
- **Biometric Data:** 1,861,108 records across multiple districts
- **Total Records Analyzed:** 4,938,837

## Methodology

### Statistical Approach
- Feature engineering with 15+ derived variables
- Principal Component Analysis (PCA) for dimensionality reduction
- T-tests for seasonal significance testing
- Correlation analysis for pattern discovery
- Composite risk scoring algorithms

### Risk Assessment Framework
```
CERS = (Update Gap Risk × 40%) + 
       (Migration Risk × 25%) + 
       (Volatility Risk × 20%) + 
       (Volume Pressure × 15%)
```

## Results Summary

### Key Findings
- **2 Critical Risk Districts** (CERS > 70)
- **31 High Risk Districts** (CERS 50-70)
- **Statistical Significance:** p-value < 0.0001 for seasonal patterns
- **Average National CERS:** 23.50

### Economic Impact (National Scale Projection)
- **Investment Required:** ₹50 crore/year
- **Annual Savings:** ₹950 crore/year
- **Return on Investment:** 1,900%
- **Citizens Benefited:** 20 million

## Interactive Outputs

All HTML visualizations can be opened directly in a web browser:
- `comprehensive_dashboard.html` - Multi-panel overview
- `cers_risk_map.html` - Risk distribution scatter plot
- `seasonal_patterns.html` - Time series with harvest overlays
- `economic_comparison.html` - Cost-benefit analysis

## Technical Requirements

### Python Dependencies
```
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.13.0
plotly>=5.18.0
scikit-learn>=1.3.0
scipy>=1.11.0
```

See [requirements.txt](analysis/requirements.txt) for complete list.

## Configuration

The analysis can be customized by modifying constants in the Python scripts:
- `MAX_SAMPLE_ROWS_LIGHT` - Sample size for visualizations
- `RANDOM_STATE` - Reproducibility seed
- Risk score component weights in CERS calculation

## Contributing

This repository is part of the UIDAI Aadhaar Hackathon 2026 submission. For questions or collaboration inquiries, please refer to the technical documentation.

## Data Privacy & Ethics

- All analysis uses aggregated district-level data
- No personally identifiable information (PII) is processed
- Compliance with UIDAI data handling guidelines
- Geographic aggregation ensures citizen privacy

## License

This project is developed for the UIDAI Aadhaar Hackathon 2026.

## Acknowledgments

- UIDAI for providing comprehensive datasets
- Statistical validation using standard academic methodologies
- Visualization frameworks: Plotly, Matplotlib, Seaborn

## Contact & Support

For technical inquiries regarding methodology, implementation, or data analysis approaches, please refer to the comprehensive technical documentation included in this repository.

---

**Last Updated:** January 19, 2026  
**Analysis Period:** 2025 Calendar Year  
**Geographic Coverage:** 1,132 districts across India  
**Total Records Processed:** 4,938,837
