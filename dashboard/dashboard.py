import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time

# Configure Streamlit page
st.set_page_config(
    page_title="Cloud Auto Scaling Dashboard",
    page_icon="☁️",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .status-good { color: #00C851; }
    .status-warning { color: #ffbb33; }
    .status-critical { color: #ff4444; }
</style>
""", unsafe_allow_html=True)

def get_traffic_prediction(hour=None, minute=None):
    """Get traffic prediction from API"""
    try:
        if hour is not None and minute is not None:
            url = f"http://localhost:5000/predict/{hour}/{minute}"
        else:
            url = "http://localhost:5000/predict"
        
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return None

def get_server_status_color(servers):
    """Get color based on server count"""
    if servers <= 2:
        return "status-good"
    elif servers <= 4:
        return "status-warning"
    else:
        return "status-critical"

def generate_hourly_predictions():
    """Generate predictions for each hour of the day"""
    predictions = []
    current_time = datetime.now()
    
    for hour in range(24):
        data = get_traffic_prediction(hour, 0)
        if data:
            predictions.append({
                'hour': hour,
                'time': f"{hour:02d}:00",
                'traffic': data['predicted_traffic'],
                'servers': data['required_servers']
            })
        else:
            # Fallback data if API fails
            predictions.append({
                'hour': hour,
                'time': f"{hour:02d}:00",
                'traffic': 0,
                'servers': 1
            })
    
    return pd.DataFrame(predictions)

def main():
    """Main dashboard function"""
    st.title("☁️ Cloud Auto Scaling Dashboard")
    st.markdown("---")
    
    # Sidebar for controls
    st.sidebar.title("Controls")
    
    # Auto-refresh option
    auto_refresh = st.sidebar.checkbox("Auto Refresh (5 seconds)")
    refresh_interval = 5 if auto_refresh else None
    
    # Manual refresh button
    if st.sidebar.button("🔄 Refresh Now"):
        st.rerun()
    
    # Main content area
    col1, col2, col3 = st.columns(3)
    
    # Get current prediction
    current_data = get_traffic_prediction()
    
    if current_data:
        # Display key metrics
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>📊 Current Traffic</h3>
                <h2>{}</h2>
                <p>requests</p>
            </div>
            """.format(current_data['predicted_traffic']), unsafe_allow_html=True)
        
        with col2:
            server_color = get_server_status_color(current_data['required_servers'])
            st.markdown(f"""
            <div class="metric-card">
                <h3>🖥️ Required Servers</h3>
                <h2 class="{server_color}">{current_data['required_servers']}</h2>
                <p>servers</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>⏰ Current Time</h3>
                <h2>{current_data.get('current_time', 'N/A')}</h2>
                <p>prediction time</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Prediction section
    st.markdown("## 🔮 Traffic Prediction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Predict for Specific Time")
        hour = st.slider("Hour", 0, 23, datetime.now().hour)
        minute = st.slider("Minute", 0, 59, datetime.now().minute)
        
        if st.button("Get Prediction"):
            prediction_data = get_traffic_prediction(hour, minute)
            if prediction_data:
                st.success(f"""
                **Prediction for {hour:02d}:{minute:02d}:**
                - Traffic: {prediction_data['predicted_traffic']} requests
                - Servers: {prediction_data['required_servers']} servers
                """)
    
    with col2:
        st.subheader("System Health")
        health_response = requests.get("http://localhost:5000/health", timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            st.success("✅ System is healthy")
            st.write(f"- Model loaded: {'Yes' if health_data['model_loaded'] else 'No'}")
            st.write(f"- Last check: {health_data['timestamp']}")
        else:
            st.error("❌ System health check failed")
    
    # Hourly predictions chart
    st.markdown("## 📈 24-Hour Traffic Forecast")
    
    if st.button("Generate 24-Hour Forecast"):
        with st.spinner("Generating predictions..."):
            predictions_df = generate_hourly_predictions()
            
            # Create two charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Traffic chart
                fig_traffic = px.line(
                    predictions_df, 
                    x='time', 
                    y='traffic',
                    title='Predicted Traffic by Hour',
                    labels={'traffic': 'Requests', 'time': 'Hour of Day'}
                )
                fig_traffic.update_layout(showlegend=False)
                st.plotly_chart(fig_traffic, use_container_width=True)
            
            with col2:
                # Server chart
                fig_servers = px.bar(
                    predictions_df,
                    x='time',
                    y='servers',
                    title='Required Servers by Hour',
                    labels={'servers': 'Servers', 'time': 'Hour of Day'},
                    color='servers',
                    color_continuous_scale='RdYlGn_r'
                )
                fig_servers.update_layout(showlegend=False)
                st.plotly_chart(fig_servers, use_container_width=True)
    
    # System logs section
    st.markdown("## 📋 System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("API Endpoints")
        st.code("""
GET /predict              - Current prediction
GET /predict/<h>/<m>      - Specific time prediction
GET /health               - System health
        """)
    
    with col2:
        st.subheader("Scaling Rules")
        st.code("""
Traffic < 200   → 1 server
Traffic < 500   → 2 servers  
Traffic < 800   → 3 servers
Traffic < 1000  → 4 servers
Traffic ≥ 1000  → 5 servers
        """)
    
    # Auto-refresh logic
    if auto_refresh:
        time.sleep(refresh_interval)
        st.rerun()

if __name__ == "__main__":
    main()
