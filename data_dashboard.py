import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Data Engineering Dashboard", 
    page_icon="📊", 
    layout="wide"
)

API_BASE = "http://localhost:8000"

st.title("📊 Advanced Data Engineering Dashboard")
st.markdown("**Real-time analytics powered by Pandas & FastAPI**")

# Sidebar controls
st.sidebar.header("🔧 Dashboard Controls")
auto_refresh = st.sidebar.checkbox("Auto Refresh (30s)")
if st.sidebar.button("🔄 Refresh Now") or auto_refresh:
    st.rerun()

# Main dashboard layout
col1, col2, col3, col4 = st.columns(4)

# Fetch basic stats
try:
    response = requests.get(f"{API_BASE}/analytics/simple-stats")
    if response.status_code == 200:
        stats = response.json()["data"]
        
        with col1:
            st.metric("👥 Total Users", stats["total_users"])
        with col2:
            st.metric("✅ Active Users", stats["active_users"])
        with col3:
            inactive = stats["total_users"] - stats["active_users"]
            st.metric("❌ Inactive Users", inactive)
        with col4:
            completion_rate = (stats["active_users"] / stats["total_users"] * 100) if stats["total_users"] > 0 else 0
            st.metric("📈 Activation Rate", f"{completion_rate:.1f}%")

except Exception as e:
    st.error(f"❌ API Connection Error: {e}")

# Advanced Analytics Section
st.header("🔬 Advanced Pandas Analytics")

tab1, tab2, tab3, tab4 = st.tabs(["📊 User Analytics", "🎯 Segmentation", "🔮 Predictions", "📈 Time Series"])

with tab1:
    st.subheader("User Analytics (Pandas Powered)")
    
    try:
        response = requests.get(f"{API_BASE}/pandas/user-analytics")
        if response.status_code == 200:
            data = response.json()
            analytics = data["pandas_analytics"]
            
            # Metrics row
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Profile Completion", f"{analytics['completion_rate']:.1f}%")
            with col2:
                st.metric("Avg Account Age", f"{analytics['avg_account_age']:.0f} days")
            with col3:
                st.metric("Email Domains", len(analytics['email_domains']))
            
            # Email domains chart
            if analytics['email_domains']:
                domain_df = pd.DataFrame(list(analytics['email_domains'].items()), 
                                       columns=['Domain', 'Users'])
                fig = px.pie(domain_df, values='Users', names='Domain', 
                           title='User Distribution by Email Domain')
                st.plotly_chart(fig, use_container_width=True)
            
            # Sample data table
            if 'sample_data' in data:
                st.subheader("📋 Sample User Data")
                sample_df = pd.DataFrame(data['sample_data'])
                st.dataframe(sample_df, use_container_width=True)
                
    except Exception as e:
        st.error(f"Error loading user analytics: {e}")

with tab2:
    st.subheader("🎯 Advanced User Segmentation")
    
    try:
        response = requests.get(f"{API_BASE}/advanced/user-segmentation")
        if response.status_code == 200:
            data = response.json()
            
            if 'user_segments' in data:
                # Segments visualization
                segments_df = pd.DataFrame(list(data['user_segments'].items()), 
                                         columns=['Segment', 'Count'])
                fig = px.bar(segments_df, x='Segment', y='Count', 
                           title='User Segments Distribution')
                st.plotly_chart(fig, use_container_width=True)
            
            if 'domain_insights' in data:
                # Domain insights
                st.subheader("📧 Domain Analysis")
                domain_data = []
                for domain, metrics in data['domain_insights'].items():
                    domain_data.append({
                        'Domain': domain,
                        'Users': metrics['user_count'],
                        'Completion Rate': f"{metrics['completion_rate']:.1f}%",
                        'Avg Age (days)': f"{metrics['avg_age_days']:.0f}"
                    })
                
                if domain_data:
                    st.dataframe(pd.DataFrame(domain_data), use_container_width=True)
                
    except Exception as e:
        st.error(f"Error loading segmentation: {e}")

with tab3:
    st.subheader("🔮 Predictive Analytics")
    
    try:
        response = requests.get(f"{API_BASE}/advanced/predictive-insights")
        if response.status_code == 200:
            data = response.json()
            insights = data.get('predictive_insights', {})
            
            # Churn analysis
            if 'churn_analysis' in insights:
                churn_df = pd.DataFrame(list(insights['churn_analysis'].items()), 
                                      columns=['Risk Level', 'Users'])
                fig = px.bar(churn_df, x='Risk Level', y='Users', 
                           title='Churn Risk Analysis', 
                           color='Risk Level',
                           color_discrete_map={
                               'Low Risk': 'green',
                               'Medium Risk': 'orange', 
                               'High Risk': 'red'
                           })
                st.plotly_chart(fig, use_container_width=True)
            
            # Feature importance
            if 'feature_importance' in insights:
                st.subheader("🎯 ML Feature Importance")
                for feature, importance in insights['feature_importance'].items():
                    st.write(f"**{feature}**: {importance}")
                    
    except Exception as e:
        st.error(f"Error loading predictions: {e}")

with tab4:
    st.subheader("📈 Time Series Analysis")
    
    try:
        response = requests.get(f"{API_BASE}/advanced/time-series-analysis")
        if response.status_code == 200:
            data = response.json()
            ts_data = data.get('time_series_insights', {})
            
            # Daily activity trend
            if 'daily_activity' in ts_data:
                daily_df = pd.DataFrame(list(ts_data['daily_activity'].items()), 
                                      columns=['Date', 'Activities'])
                daily_df['Date'] = pd.to_datetime(daily_df['Date'])
                
                fig = px.line(daily_df, x='Date', y='Activities', 
                            title='Daily Activity Trend')
                st.plotly_chart(fig, use_container_width=True)
            
            # Hourly pattern
            if 'hourly_pattern' in ts_data:
                hourly_df = pd.DataFrame(list(ts_data['hourly_pattern'].items()), 
                                       columns=['Hour', 'Activities'])
                hourly_df['Hour'] = hourly_df['Hour'].astype(int)
                
                fig = px.bar(hourly_df, x='Hour', y='Activities', 
                           title='Activity Pattern by Hour')
                st.plotly_chart(fig, use_container_width=True)
            
            # Key insights
            col1, col2, col3 = st.columns(3)
            with col1:
                if 'trend' in ts_data:
                    st.metric("📈 Trend", ts_data['trend'].title())
            with col2:
                if 'peak_hour' in ts_data and ts_data['peak_hour']:
                    st.metric("⏰ Peak Hour", f"{ts_data['peak_hour']}:00")
            with col3:
                if 'peak_day' in ts_data:
                    st.metric("📅 Peak Day", ts_data['peak_day'])
                    
    except Exception as e:
        st.error(f"Error loading time series: {e}")

# Real-time Events Section
st.header("⚡ Real-time Event Streaming")

try:
    response = requests.get(f"{API_BASE}/analytics/streaming-stats")
    if response.status_code == 200:
        streaming_data = response.json()["data"]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🔄 Total Events", streaming_data.get("total_events_processed", 0))
        with col2:
            st.metric("⚡ Last 5 Min", streaming_data.get("events_last_5_minutes", 0))
        with col3:
            st.metric("📊 Queue Size", streaming_data.get("queue_size", 0))
        
        # Event types
        if 'event_types' in streaming_data and streaming_data['event_types']:
            events_df = pd.DataFrame(list(streaming_data['event_types'].items()), 
                                   columns=['Event Type', 'Count'])
            fig = px.pie(events_df, values='Count', names='Event Type', 
                       title='Recent Event Types Distribution')
            st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error loading streaming stats: {e}")

# Footer
st.markdown("---")
st.markdown("**🚀 Powered by FastAPI + Pandas + Streamlit | Real-time Data Engineering Dashboard**")

# Auto-refresh
if auto_refresh:
    import time
    time.sleep(30)
    st.rerun()