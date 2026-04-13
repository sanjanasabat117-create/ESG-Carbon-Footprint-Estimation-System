import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Page config
st.set_page_config(page_title="Carbon Insight - Executive Dashboard", layout="wide", page_icon="🌱")

# DB Connection
DB_PATH = os.path.join(os.path.dirname(__file__), '../../data/database.sqlite')

def get_data(query, params=None):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

# Styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    h1, h2, h3 {
        color: #1e3a8a;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🌱 Carbon Insight: Executive Emissions Dashboard")
st.subheader("High-Fidelity ESG Progress Tracking & Decarbonization Strategy")
st.divider()

# Sidebar Filters
st.sidebar.header("Reporting Parameters")
units_df = get_data("SELECT unit_name FROM business_units")
selected_unit = st.sidebar.multiselect("Business Units", units_df['unit_name'].tolist(), default=units_df['unit_name'].tolist())

# Load Primary Dataset
query = f"""
    SELECT ce.*, bu.unit_name, bu.region, bu.industry_segment 
    FROM calculated_emissions ce
    JOIN business_units bu ON ce.unit_id = bu.unit_id
    WHERE bu.unit_name IN ({','.join(['?']*len(selected_unit))})
"""
df = get_data(query, params=selected_unit) if selected_unit else pd.DataFrame()

if df.empty:
    st.warning("No data selected. Please adjust filters.")
else:
    # Key Metrics
    total_emissions = df['t_co2e'].sum()
    scope_1 = df[df['scope'] == 1]['t_co2e'].sum()
    scope_2 = df[df['scope'] == 2]['t_co2e'].sum()
    scope_3 = df[df['scope'] == 3]['t_co2e'].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Emissions", f"{total_emissions:,.2f} tCO2e", delta="-4.2% YoY")
    col2.metric("Scope 1 (Direct)", f"{scope_1:,.2f} tCO2e")
    col3.metric("Scope 2 (Indirect)", f"{scope_2:,.2f} tCO2e")
    col4.metric("Scope 3 (Value Chain)", f"{scope_3:,.2f} tCO2e")

    st.divider()

    # row 1: Trend & Scope Breakdown
    row1_1, row1_2 = st.columns([2, 1])

    with row1_1:
        st.write("### Emissions Trend by Month")
        df['month'] = pd.to_datetime(df['activity_date']).dt.strftime('%Y-%m')
        trend_df = df.groupby(['month', 'scope']).sum().reset_index()
        fig_trend = px.area(trend_df, x='month', y='t_co2e', color='scope', 
                          color_discrete_sequence=px.colors.sequential.Viridis,
                          labels={'scope': 'GHG Scope', 't_co2e': 'tCO2e'})
        fig_trend.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_trend, use_container_width=True)

    with row1_2:
        st.write("### Scope Distribution")
        scope_pie = px.pie(df, values='t_co2e', names='scope', hole=0.4,
                         color_discrete_sequence=['#1e3a8a', '#3b82f6', '#93c5fd'])
        scope_pie.update_layout(margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(scope_pie, use_container_width=True)

    st.divider()

    # Row 2: Category Analysis (Scientific Look)
    st.write("### Category Deep-Dive (Seaborn Statistical Analysis)")
    fig_sb, ax_sb = plt.subplots(figsize=(10, 4))
    sns.barplot(data=df, x='category', y='t_co2e', hue='scope', ax=ax_sb, palette='viridis')
    plt.xticks(rotation=45)
    plt.title("Emissions Intensity by Activity Category")
    st.pyplot(fig_sb)

    st.divider()

    # Row 3: Decarbonization Modeler
    st.write("### 🎯 Strategic Decarbonization Modeler")
    st.info("Identify impact of strategic shifts on your carbon footprint.")
    
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        renew_perc = st.slider("Switch to Renewable Energy (Scope 2 Reduction %)", 0, 100, 20)
        ev_perc = st.slider("Transition Fleet to EV (Scope 1 Mobile reduction %)", 0, 100, 10)
    
    # Calculate reduction
    reduced_s2 = scope_2 * (renew_perc / 100)
    # Filter for mobile combustion in scope 1
    mobile_mask = df['category'].str.contains('Mobile', case=False)
    mobile_emissions = df[mobile_mask]['t_co2e'].sum()
    reduced_s1_mobile = mobile_emissions * (ev_perc / 100)
    
    total_reduction = reduced_s2 + reduced_s1_mobile
    new_total = total_emissions - total_reduction

    with m_col2:
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = new_total,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Projected Annual tCO2e"},
            delta = {'reference': total_emissions, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
            gauge = {
                'axis': {'range': [0, total_emissions]},
                'bar': {'color': "#10b981"},
                'steps': [
                    {'range': [0, total_emissions*0.5], 'color': "#d1fae5"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': total_emissions*0.95}
            }
        ))
        st.plotly_chart(fig_gauge, use_container_width=True)

    st.success(f"Estimated Annual Reduction: **{total_reduction:,.2f} tCO2e** via selected initiatives.")
