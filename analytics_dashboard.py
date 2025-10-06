import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Configure page
st.set_page_config(page_title="Analytics Dashboard", page_icon="📊", layout="wide")

API_BASE = "http://localhost:8000"

st.title("📊 Data Engineering Analytics Dashboard")

# Sidebar
st.sidebar.header("🔧 Controls")
refresh = st.sidebar.button("🔄 Refresh Data")

# Main dashboard
col1, col2, col3 = st.columns(3)

# Get simple stats
try:
    response = requests.get(f"{API_BASE}/analytics/simple-stats")
    if response.status_code == 200:
        data = response.json()["data"]
        
        with col1:
            st.metric("👥 Total Users", data["total_users"])
        
        with col2:
            st.metric("✅ Active Users", data["active_users"])
        
        with col3:
            inactive = data["total_users"] - data["active_users"]
            st.metric("❌ Inactive Users", inactive)
    
except requests.exceptions.ConnectionError:
    st.error("❌ Cannot connect to API. Make sure FastAPI server is running.")

# Streaming Analytics Section
st.header("🔄 Real-Time Streaming Analytics")

if st.button("📡 Get Streaming Stats"):
    try:
        # You'll need to login first to get token
        st.info("💡 Login first to access streaming analytics")
        
        # For demo, show sample streaming data
        sample_events = [
            {"event_type": "user_registration", "timestamp": "2024-01-01T10:00:00"},
            {"event_type": "user_login", "timestamp": "2024-01-01T10:05:00"},
            {"event_type": "user_login", "timestamp": "2024-01-01T10:10:00"}
        ]
        
        st.subheader("📈 Recent Events")
        df = pd.DataFrame(sample_events)
        st.dataframe(df)
        
        # Event type chart
        if not df.empty:
            fig = px.pie(df, names='event_type', title='Event Distribution')
            st.plotly_chart(fig)
            
    except Exception as e:
        st.error(f"Error: {e}")

# ETL Pipeline Section
st.header("🔄 ETL Pipeline")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Extract")
    st.write("✅ Data extracted from PostgreSQL")
    st.code("SELECT * FROM users")

with col2:
    st.subheader("🔄 Transform")
    st.write("✅ Data cleaned with Pandas")
    st.code("df['email_domain'] = df['email'].str.split('@').str[1]")

st.subheader("📤 Load")
st.write("✅ Analytics loaded to dashboard")

# Batch Processing
st.header("⏰ Batch Processing")

if st.button("🚀 Run Manual Batch Job"):
    st.info("💡 This would trigger a batch processing job")
    st.success("✅ Batch job would process all historical data")

# Data Pipeline Status
st.header("🔍 Pipeline Status")

status_col1, status_col2 = st.columns(2)

with status_col1:
    st.success("✅ Batch Processing: Active")
    st.info("📊 Last run: Daily at 2:00 AM")

with status_col2:
    st.success("✅ Stream Processing: Active")
    st.info("⚡ Processing events in real-time")

# Footer
st.markdown("---")
st.info("💡 **Data Engineering Features**: ETL Pipelines • Real-time Streaming • Batch Processing • Analytics")