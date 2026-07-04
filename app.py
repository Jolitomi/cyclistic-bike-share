import streamlit as st
import pandas as pd
import plotly.express as px

# Page layout setup
st.set_page_config(
    page_title="Cyclistic Conversion Strategy Dashboard",
    page_icon="🚴",
    layout="wide"
)

# Minimalist High-End Theme Configuration
st.markdown("""
    <style>
    .main { background-color: #FAF9F6; }
    h1, h2, h3 { color: #111111; font-family: 'Helvetica Neue', Arial, sans-serif; }
    .metric-box { background-color: #FFFFFF; padding: 20px; border-radius: 6px; border: 1px solid #E5E5E0; }
    div[data-testid="stMetricValue"] { font-size: 2rem; font-weight: 700; color: #111111; }
    </style>
""", unsafe_allow_html=True)

# --- DATA LOADING (SUPER FAST & LIGHTWEIGHT) ---
@st.cache_data
def load_summary_data():
    hourly = pd.read_csv("data/hourly_summary.csv")
    weekly = pd.read_csv("data/weekly_summary.csv")
    metrics = pd.read_csv("data/metrics_summary.csv")
    
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    if 'day_of_week' in weekly.columns:
        weekly['day_of_week'] = pd.Categorical(weekly['day_of_week'], categories=days_order, ordered=True)
        
    return hourly, weekly, metrics

try:
    hourly_df, weekly_df, metrics_df = load_summary_data()
except FileNotFoundError:
    st.error("🚨 Summary CSV files not found.")
    st.stop()

# --- HEADER & CONTEXT ---
st.title("🚴 Cyclistic Executive Analytics Dashboard")
st.markdown("### *Data Insights & Strategic Framework for Casual-to-Member Conversion*")
st.markdown("---")

# --- CORE STRATEGIC INSIGHTS ARCHITECTURE ---
st.header("🎯 Executive Summary: The Conversion Strategy")
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Behavioral Diagnosis")
    st.markdown("""
    The data reveals distinct behavioral identities between user groups:
    * **Annual Members** exhibit high-frequency, predictable utility usage concentrated tightly around **weekday commute spikes (8 AM and 5 PM)**.
    * **Casual Riders** utilize the fleet for long-duration, recreational trips heavily weighted toward **weekends and summer months**.
    
    *Strategy:* We should not market yearly memberships as a 'daily commute utility' to casual riders. Instead, market it as a **'Premium Access Pass'** that unlocks unlimited weekend exploration and avoids high single-use duration fees.
    """)

with col_right:
    st.subheader("Top 3 Targeted Marketing Directives")
    st.markdown("""
    1. **The 'Weekend Warrior' Package:** Launch a seasonal campaign targeting high-volume weekend casual riders right before summer peaks, framing annual membership as the most economical leisure asset.
    2. **Triggered App Notifications at Tipping Points:** Implement digital triggers in the user app. When a casual rider completes a trip exceeding 25 minutes, automatically show a calculated comparison of how much they would save as an annual member.
    3. **Digital Commuter Target:** Geofence advertisements near major financial and corporate hubs during weekday peak windows where casual riders mimic member paths but pay single-ride pricing.
    """)

st.markdown("---")

# --- AGGREGATED BEHAVIORAL KPIs ---
st.header("📊 Deep-Dive Behavioral Metrics")
col1, col2, col3 = st.columns(3)

# Extract pre-computed metrics
casual_metrics = metrics_df[metrics_df['member_casual'] == 'casual'].iloc[0]
member_metrics = metrics_df[metrics_df['member_casual'] == 'member'].iloc[0]

with col1:
    st.metric(
        label="Casual vs. Member Avg Trip Length", 
        value=f"{round(casual_metrics['avg_ride_length'], 1)}m vs {round(member_metrics['avg_ride_length'], 1)}m",
        delta=f"+{round(casual_metrics['avg_ride_length'] - member_metrics['avg_ride_length'], 1)} mins longer for Casuals",
        delta_color="inverse"
    )
with col2:
    st.metric(
        label="Total Casual Trips to Convert", 
        value=f"{int(casual_metrics['total_trips']):,}"
    )
with col3:
    st.metric(
        label="Total Active Member Trips", 
        value=f"{int(member_metrics['total_trips']):,}"
    )

st.markdown(" ")

# --- ACTIONABLE INTERACTIVE VISUALIZATIONS ---
st.header("📈 Key Visual Proofs for Stakeholders")
tab1, tab2 = st.tabs(["🕒 Hourly Commuter Footprint", "🗓️ Weekly Ride Distributions"])

with tab1:
    st.subheader("Hourly Trip Demand: Utility Commuters vs. Leisure Riders")
    fig_hour = px.line(
        hourly_df, 
        x="hour", 
        y="total_rides", 
        color="member_casual",
        color_discrete_map={'member': '#111111', 'casual': '#D4AF37'}, # Elegant Slate Black & Matte Gold
        labels={"hour": "Hour of Day (24h format)", "total_rides": "Total Volume of Rides", "member_casual": "User Segment"}
    )
    fig_hour.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(tickmode='linear', tick0=0, dtick=2), hovermode="x unified"
    )
    st.plotly_chart(fig_hour, use_container_width=True)

with tab2:
    st.subheader("Weekly Volume Patterns")
    fig_week = px.bar(
        weekly_df, 
        x="day_of_week", 
        y="total_rides", 
        color="member_casual", 
        barmode="group",
        color_discrete_map={'member': '#111111', 'casual': '#D4AF37'},
        labels={"day_of_week": "Day of the Week", "total_rides": "Number of Rides", "member_casual": "User Segment"}
    )
    fig_week.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_week, use_container_width=True)

st.markdown("---")
st.caption("Cyclistic Business Intelligence Framework | Designed for Executive Presentation")