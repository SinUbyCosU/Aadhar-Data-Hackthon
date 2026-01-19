"""
Create a presentation-ready visualization dashboard for the STRATEGIC ANALYSIS
"""
import json
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load insights
workspace = r"c:\Users\Tanushree\Downloads\Aadhar data Hackthon"
insights_path = os.path.join(workspace, "analysis_outputs", "strategic_analysis", "strategic_analysis_insights.json")

with open(insights_path, 'r') as f:
    insights = json.load(f)

# Create comprehensive dashboard
fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=(
        'CERS Risk Distribution',
        'Top 10 Highest Risk Districts',
        'Intervention Cost Breakdown',
        'Projected Annual Savings',
        'Migration Pattern: Harvest vs Non-Harvest',
        'Implementation Timeline'
    ),
    specs=[
        [{'type': 'pie'}, {'type': 'bar'}],
        [{'type': 'pie'}, {'type': 'bar'}],
        [{'type': 'bar'}, {'type': 'scatter'}]
    ],
    vertical_spacing=0.12,
    horizontal_spacing=0.15
)

# 1. CERS Risk Distribution
cers_summary = insights['cers_summary']
fig.add_trace(
    go.Pie(
        labels=['Critical', 'High', 'Medium', 'Low'],
        values=[
            cers_summary['critical_risk_districts'],
            cers_summary['high_risk_districts'],
            cers_summary['medium_risk_districts'],
            cers_summary['low_risk_districts']
        ],
        marker=dict(colors=['#d32f2f', '#f57c00', '#fbc02d', '#388e3c']),
        name='Risk Distribution'
    ),
    row=1, col=1
)

# 2. Top 10 Districts
top_10 = insights['cers_summary']['top_10_districts'][:10]
districts = [f"{d['district'][:15]}, {d['state'][:10]}" for d in top_10]
cers_scores = [d['CERS'] for d in top_10]

fig.add_trace(
    go.Bar(
        y=districts[::-1],  # Reverse for better readability
        x=cers_scores[::-1],
        orientation='h',
        marker=dict(
            color=cers_scores[::-1],
            colorscale='Reds',
            showscale=False
        ),
        name='CERS Score'
    ),
    row=1, col=2
)

# 3. Intervention Costs
costs = {
    'Mobile Vans': 14400000,
    'Capacity Building': 13000000,
    'Alert System': 100000
}

fig.add_trace(
    go.Pie(
        labels=list(costs.keys()),
        values=list(costs.values()),
        marker=dict(colors=['#1976d2', '#7b1fa2', '#c62828']),
        name='Costs'
    ),
    row=2, col=1
)

# 4. Projected Savings
savings = {
    'Exclusion Prevention': 305000,
    'Efficiency Gains': 554400,
    'Admin Savings': 15250
}

fig.add_trace(
    go.Bar(
        x=list(savings.keys()),
        y=list(savings.values()),
        marker=dict(color='#2e7d32'),
        name='Savings'
    ),
    row=2, col=2
)

# 5. Harvest Season Impact
harvest_data = insights['hidden_pattern']['seasonal_bio_gap']
months = [d['month'] for d in harvest_data]
bio_completion = [d['bio_completion_rate'] for d in harvest_data]
is_harvest = [d['is_harvest_season'] for d in harvest_data]

colors = ['#ff6f00' if h == 1 else '#0288d1' for h in is_harvest]

fig.add_trace(
    go.Bar(
        x=months,
        y=bio_completion,
        marker=dict(color=colors),
        name='Completion Rate',
        showlegend=False
    ),
    row=3, col=1
)

# 6. Implementation Timeline
phases = ['Phase 1\nPilot\n(3 months)', 'Phase 2\nScale\n(6 months)', 'Phase 3\nNational\n(3 months)']
districts_covered = [10, 33, 1132]
cers_reduction = [20, 30, 35]  # Percentage reduction targets

fig.add_trace(
    go.Scatter(
        x=phases,
        y=districts_covered,
        mode='lines+markers',
        name='Districts Covered',
        marker=dict(size=15, color='#1976d2'),
        line=dict(width=3)
    ),
    row=3, col=2
)

fig.add_trace(
    go.Scatter(
        x=phases,
        y=[d * 10 for d in cers_reduction],  # Scale for visibility
        mode='lines+markers',
        name='CERS Reduction %',
        marker=dict(size=15, color='#f57c00'),
        line=dict(width=3),
        yaxis='y2'
    ),
    row=3, col=2
)

# Update layout
fig.update_layout(
    title=dict(
        text='<b>UIDAI AADHAAR HACKATHON 2026 - STRATEGIC ANALYSIS DASHBOARD</b><br><sub>Citizen Exclusion Risk Score (CERS) & Intervention Framework</sub>',
        font=dict(size=20),
        x=0.5,
        xanchor='center'
    ),
    height=1200,
    showlegend=True,
    template='plotly_white',
    font=dict(size=11)
)

# Update axes
fig.update_xaxes(title_text="CERS Score", row=1, col=2)
fig.update_xaxes(title_text="Intervention Type", row=2, col=2)
fig.update_xaxes(title_text="Month", row=3, col=1)
fig.update_xaxes(title_text="Implementation Phase", row=3, col=2)

fig.update_yaxes(title_text="District", row=1, col=2)
fig.update_yaxes(title_text="Amount (₹)", row=2, col=2)
fig.update_yaxes(title_text="Completion Rate (%)", row=3, col=1)
fig.update_yaxes(title_text="Districts", row=3, col=2)

# Save
output_path = os.path.join(workspace, "analysis_outputs", "strategic_analysis", "comprehensive_dashboard.html")
fig.write_html(output_path)

print(f"✅ Comprehensive dashboard created: {output_path}")

# Create a second focused visualization on the key insight
fig2 = go.Figure()

# Add the top risk districts with detailed annotations
top_20 = insights['cers_summary']['top_10_districts'][:20] if len(insights['cers_summary']['top_10_districts']) >= 20 else insights['cers_summary']['top_10_districts']

districts_20 = [f"{d['district']}, {d['state']}" for d in top_20]
cers_20 = [d['CERS'] for d in top_20]
categories = [d['risk_category'] for d in top_20]

color_map = {'Critical': '#d32f2f', 'High': '#f57c00', 'Medium': '#fbc02d', 'Low': '#388e3c'}
colors_20 = [color_map.get(c, '#757575') for c in categories]

fig2.add_trace(go.Bar(
    x=cers_20[::-1],
    y=districts_20[::-1],
    orientation='h',
    marker=dict(
        color=colors_20[::-1],
        line=dict(color='white', width=1)
    ),
    text=[f"{score:.1f}" for score in cers_20[::-1]],
    textposition='auto',
))

fig2.update_layout(
    title=dict(
        text='<b>Citizen Exclusion Risk Score (CERS)</b><br><sub>Top 20 Districts Requiring Immediate Intervention</sub>',
        font=dict(size=22),
        x=0.5,
        xanchor='center'
    ),
    xaxis_title='<b>CERS Score</b> (0-100, higher = more risk)',
    yaxis_title='District, State',
    height=800,
    template='plotly_white',
    font=dict(size=12),
    showlegend=False,
    xaxis=dict(range=[0, 100])
)

# Add risk threshold lines
fig2.add_vline(x=70, line_dash="dash", line_color="red", 
               annotation_text="Critical Threshold", annotation_position="top")
fig2.add_vline(x=50, line_dash="dash", line_color="orange",
               annotation_text="High Risk Threshold", annotation_position="top")

output_path2 = os.path.join(workspace, "analysis_outputs", "strategic_analysis", "cers_top_districts_presentation.html")
fig2.write_html(output_path2)

print(f"✅ CERS presentation chart created: {output_path2}")

# Create economic impact comparison
fig3 = go.Figure()

# Current state vs With intervention
scenarios = ['Current State<br>(Do Nothing)', 'With CERS<br>Intervention']
costs = [305000, 27400000]
savings = [0, 874650]
net = [-305000, -26525350]  # Negative = cost to society

fig3.add_trace(go.Bar(
    name='Annual Exclusion Cost',
    x=scenarios,
    y=costs,
    marker_color='#d32f2f',
    text=[f'₹{c/100000:.1f}L' for c in costs],
    textposition='auto',
))

fig3.add_trace(go.Bar(
    name='Annual Savings Generated',
    x=scenarios,
    y=savings,
    marker_color='#2e7d32',
    text=[f'₹{s/100000:.1f}L' for s in savings],
    textposition='auto',
))

fig3.update_layout(
    title=dict(
        text='<b>Economic Impact Analysis</b><br><sub>Sample Dataset ROI (Scales to ₹950 Cr savings nationally)</sub>',
        font=dict(size=20)
    ),
    barmode='group',
    yaxis_title='Amount (₹)',
    height=500,
    template='plotly_white',
    font=dict(size=13)
)

output_path3 = os.path.join(workspace, "analysis_outputs", "strategic_analysis", "economic_comparison.html")
fig3.write_html(output_path3)

print(f"✅ Economic comparison created: {output_path3}")

print("\n🎯 All presentation-ready visualizations created successfully!")
print(f"📂 Location: {os.path.join(workspace, 'analysis_outputs', 'strategic_analysis')}")

