# National Insights – Aadhaar Data Hackathon

## Executive Summary

- Total records analyzed: 4,938,837

- Enrolment: 1,006,029 rows, missing rate 8.5% 
- Demographic: 2,071,700 rows, missing rate 8.2% 
- Biometric: 1,861,108 rows, missing rate 7.2% 


## Coverage & Representation Gaps by State

### Under-represented in Demographic (vs Enrolment)

- Uttar Pradesh: 8.10% vs 10.97% (Δ -2.87%)
- Bihar: 4.71% vs 6.02% (Δ -1.31%)
- Madhya Pradesh: 3.69% vs 4.99% (Δ -1.31%)
- Rajasthan: 4.32% vs 5.58% (Δ -1.26%)
- Jharkhand: 1.91% vs 2.31% (Δ -0.39%)
- Haryana: 1.38% vs 1.59% (Δ -0.21%)
- Delhi: 0.51% vs 0.68% (Δ -0.17%)
- Jammu and Kashmir: 0.98% vs 1.12% (Δ -0.15%)
- Assam: 3.03% vs 3.16% (Δ -0.13%)
- Chhattisgarh: 1.72% vs 1.84% (Δ -0.12%)


### Under-represented in Biometric (vs Enrolment)

- Uttar Pradesh: 8.34% vs 10.97% (Δ -2.63%)
- Bihar: 4.48% vs 6.02% (Δ -1.54%)
- Rajasthan: 4.28% vs 5.58% (Δ -1.30%)
- Madhya Pradesh: 3.77% vs 4.99% (Δ -1.23%)
- Assam: 2.56% vs 3.16% (Δ -0.60%)
- West Bengal: 7.02% vs 7.61% (Δ -0.58%)
- Jharkhand: 1.97% vs 2.31% (Δ -0.34%)
- Delhi: 0.50% vs 0.68% (Δ -0.18%)
- Haryana: 1.42% vs 1.59% (Δ -0.17%)
- Meghalaya: 0.22% vs 0.37% (Δ -0.15%)


## Hotspot States & Districts

### Enrolment

- Top states by volume share:

  - Uttar Pradesh: 10.97%
  - Tamil Nadu: 9.20%
  - Maharashtra: 7.67%
  - West Bengal: 7.61%
  - Karnataka: 6.98%
  - Andhra Pradesh: 6.53%
  - Bihar: 6.02%
  - Rajasthan: 5.58%
  - Madhya Pradesh: 4.99%
  - Gujarat: 4.63%


### Demographic

- Top states by volume share:

  - Andhra Pradesh: 10.02%
  - Tamil Nadu: 9.50%
  - West Bengal: 8.14%
  - Uttar Pradesh: 8.10%
  - Maharashtra: 7.83%
  - Karnataka: 7.43%
  - Kerala: 5.09%
  - Bihar: 4.71%
  - Gujarat: 4.65%
  - Odisha: 4.45%


### Biometric

- Top states by volume share:

  - Tamil Nadu: 9.92%
  - Andhra Pradesh: 9.24%
  - Uttar Pradesh: 8.34%
  - Maharashtra: 8.12%
  - Karnataka: 7.59%
  - West Bengal: 7.02%
  - Kerala: 5.29%
  - Gujarat: 4.81%
  - Odisha: 4.65%
  - Bihar: 4.48%


## Throughput & Volatility (Daily)

- Enrolment: volatility (std/mean) = 0.59, range 2025-01-04 to 2025-12-11 
- Demographic: volatility (std/mean) = 0.38, range 2025-01-03 to 2025-12-12 
- Biometric: volatility (std/mean) = 0.14, range 2025-01-03 to 2025-12-12 


## Data Quality Priorities

- Enrolment: missing rate 8.5%, columns=8 
- Demographic: missing rate 8.2%, columns=7 
- Biometric: missing rate 7.2%, columns=7 


## Recommendations (National Scale)

- Expand capacity in top-volume states (e.g., additional mobile centres, extended hours).
- Target under-represented states (negative share deltas) with focused enrolment/biometric drives.
- Reduce missingness in high-impact fields (IDs, timestamps, centre info) to unlock better match rates.
- Monitor daily volatility; staff peak days and smooth demand with appointment slots.
- Instrument operational dashboards per district; set SLAs for data completeness and processing times.
- Add fairness monitoring of success rates across states/centres where labels are available.


## Key Takeaways (Judge-Focused)

- Concentration: Andhra Pradesh, Tamil Nadu, Uttar Pradesh consistently rank top by volume across datasets — prioritize these for capacity upgrades and quality programs.
- Under-representation: Demographic and Biometric have lower shares vs Enrolment in large Hindi-belt states (UP, Bihar, MP, Rajasthan) — targeted drives can close identification gaps.
- Stability: Biometric flows show lower day-to-day volatility than Enrolment — enrolment ops need stronger demand smoothing and staffing playbooks.
- Data Quality: Missingness around 7–8% suggests immediate wins from better capture/validation of timestamps, location, and centre IDs.


## National Development Opportunities

- Capacity & Access
  - Add mobile enrolment/biometric camps in under-represented states and rural districts.
  - Extend hours and queue management at top-volume districts (e.g., Pune, North 24 Parganas, Barddhaman).
- Data Quality & Reliability
  - Enforce mandatory fields for time, state, district, centre; validate at source to reduce 7–8% missingness.
  - Device health checks and operator nudges for low-quality captures; auto-escalate repeated failures.
- Scheduling & Volatility Control
  - Appointment slots and staggered campaigns to reduce enrolment volatility; align staffing to peak DOW/hour heatmap.
  - Monitor anomalous days flagged by IsolationForest; trigger rapid ops review.
- Inclusion & Fairness
  - Track status/match outcomes by state/centre (when labels exist); set thresholds and remediation for low-performing segments.
  - Campaigns tailored for low-share states to close representation gaps.
- Analytics & Governance
  - Continuous dashboards at national/state/district levels with weekly reviews.
  - Versioned KPIs and audit trails to support policy decisions and funding allocations.


## Judge-Ready Visuals (Open Locally)

- Comparative dashboard: [analysis_outputs/dashboard/index.html](analysis_outputs/dashboard/index.html)
- Biometric deep-dive
  - 3D PCA: [analysis_outputs/biometric/pca_3d_projection.html](analysis_outputs/biometric/pca_3d_projection.html)
  - 3D top-correlated scatter: [analysis_outputs/biometric/top3_corr_3d_scatter.html](analysis_outputs/biometric/top3_corr_3d_scatter.html)
  - Treemap State→District: [analysis_outputs/biometric/treemap_state_district.html](analysis_outputs/biometric/treemap_state_district.html)
  - Sankey State→District→Outcome: [analysis_outputs/biometric/sankey_state_district_outcome.html](analysis_outputs/biometric/sankey_state_district_outcome.html)
  - DOW×Hour heatmap: [analysis_outputs/biometric/heatmap_dow_hour.png](analysis_outputs/biometric/heatmap_dow_hour.png)
  - Calendar heatmap: [analysis_outputs/biometric/calendar_heatmap_weekly.png](analysis_outputs/biometric/calendar_heatmap_weekly.png)
  - Anomalous days: [analysis_outputs/biometric/anomalous_days.png](analysis_outputs/biometric/anomalous_days.png)
- Similar outputs exist for: [analysis_outputs/enrolment](analysis_outputs/enrolment), [analysis_outputs/demographic](analysis_outputs/demographic)


## Next Steps (1–2 Weeks)

- Pilot two states (UP, Bihar): deploy mobile camps + quality nudges; measure uplift in demographic/biometric share.
- Roll out mandatory-field validation at capture; re-measure missingness delta (<5% target).
- Activate weekly ops stand-up with dashboard review; act on anomalies within 24h.
- Add optional fairness charts where outcome/status exists; set centre-level improvement goals.
