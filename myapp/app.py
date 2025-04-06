import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, time
import time as tm

# Page configuration
st.set_page_config(
    page_title="Duty Scheduler System",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .sidebar .sidebar-content {
        background-color: #343a40;
        color: white;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    .stSelectbox>div>div>select {
        border-radius: 5px;
    }
    .metric-card {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.image("https://via.placeholder.com/150x50?text=Company+Logo", width=150)
    st.title("Navigation")
    app_mode = st.radio(
        "Select a page",
        [
            "Dashboard Overview",
            "Linked Duty Scheduler",
            "Unlinked Duty Scheduler",
            "Route Management (GIS Map)",
            "Reports & Analytics",
            "Real-Time Monitor",
            "User Management & Settings"
        ]
    )
    
    st.markdown("---")
    st.markdown("### User Profile")
    st.image("https://via.placeholder.com/100?text=User", width=100)
    st.write("Admin User")
    st.write("Last login: Today")
    st.button("Logout")

# Sample data generation functions
def generate_dummy_schedule():
    data = {
        "Duty ID": ["D001", "D002", "D003", "D004", "D005"],
        "Driver": ["John Doe", "Jane Smith", "Mike Johnson", "Sarah Williams", "David Brown"],
        "Vehicle": ["VH001", "VH002", "VH003", "VH004", "VH005"],
        "Start Time": ["08:00", "10:00", "12:00", "14:00", "16:00"],
        "End Time": ["10:00", "12:00", "14:00", "16:00", "18:00"],
        "Status": ["Completed", "In Progress", "Scheduled", "Scheduled", "Scheduled"],
        "Route": ["Route A", "Route B", "Route C", "Route D", "Route E"]
    }
    return pd.DataFrame(data)

def generate_dummy_metrics():
    return {
        "total_duties": 24,
        "completed_duties": 18,
        "ongoing_duties": 3,
        "scheduled_duties": 3,
        "utilization_rate": 85
    }

def generate_dummy_users():
    return pd.DataFrame({
        "User ID": [1, 2, 3, 4, 5],
        "Name": ["Admin User", "Manager 1", "Manager 2", "Driver 1", "Driver 2"],
        "Role": ["Admin", "Manager", "Manager", "Driver", "Driver"],
        "Last Active": ["Today", "Today", "Yesterday", "Today", "2 days ago"],
        "Status": ["Active", "Active", "Active", "Active", "Inactive"]
    })

# Dashboard Overview
if app_mode == "Dashboard Overview":
    st.title("📊 Dashboard Overview")
    
    # Metrics row
    metrics = generate_dummy_metrics()
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Duties", metrics["total_duties"])
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Completed Duties", metrics["completed_duties"], "+2 from yesterday")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Ongoing Duties", metrics["ongoing_duties"])
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Scheduled Duties", metrics["scheduled_duties"])
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col5:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Utilization Rate", f"{metrics['utilization_rate']}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts row
    st.markdown("## Performance Metrics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Duty Completion Trend")
        data = pd.DataFrame({
            "Date": pd.date_range(start="2023-01-01", periods=30),
            "Completed": np.random.randint(5, 15, size=30),
            "Scheduled": np.random.randint(5, 15, size=30)
        })
        fig = px.line(data, x="Date", y=["Completed", "Scheduled"], 
                     title="Duty Completion Trend", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Duty Status Distribution")
        status_data = pd.DataFrame({
            "Status": ["Completed", "In Progress", "Scheduled", "Cancelled"],
            "Count": [18, 3, 3, 0]
        })
        fig = px.pie(status_data, values="Count", names="Status", 
                     title="Duty Status Distribution", hole=0.3)
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent activities
    st.markdown("## Recent Activities")
    schedule_df = generate_dummy_schedule()
    st.dataframe(schedule_df, use_container_width=True)

# Linked Duty Scheduler
elif app_mode == "Linked Duty Scheduler":
    st.title("⏱ Linked Duty Scheduler")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### Current Linked Schedule")
        schedule_df = generate_dummy_schedule()
        st.dataframe(schedule_df, use_container_width=True)
    
    with col2:
        st.markdown("### Create New Linked Duty")
        with st.form("new_linked_duty"):
            driver = st.selectbox("Driver", ["John Doe", "Jane Smith", "Mike Johnson", "Sarah Williams"])
            vehicle = st.selectbox("Vehicle", ["VH001", "VH002", "VH003", "VH004"])
            route = st.selectbox("Route", ["Route A", "Route B", "Route C", "Route D"])
            start_time = st.time_input("Start Time", time(8, 0))
            end_time = st.time_input("End Time", time(17, 0))
            
            submitted = st.form_submit_button("Create Linked Duty")
            if submitted:
                st.success("Linked duty created successfully!")
                tm.sleep(1)
                st.rerun()

# Unlinked Duty Scheduler
elif app_mode == "Unlinked Duty Scheduler":
    st.title("⏱ Unlinked Duty Scheduler")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### Available Duties")
        duties_df = pd.DataFrame({
            "Duty ID": ["UD001", "UD002", "UD003", "UD004"],
            "Type": ["Delivery", "Maintenance", "Inspection", "Transfer"],
            "Location": ["Warehouse A", "Depot B", "Site C", "Hub D"],
            "Time Window": ["08:00-10:00", "11:00-13:00", "14:00-16:00", "09:00-12:00"],
            "Priority": ["High", "Medium", "Low", "High"]
        })
        st.dataframe(duties_df, use_container_width=True)
    
    with col2:
        st.markdown("### Assign Duty")
        with st.form("assign_duty"):
            duty_id = st.selectbox("Select Duty", duties_df["Duty ID"])
            driver = st.selectbox("Assign Driver", ["John Doe", "Jane Smith", "Mike Johnson"])
            vehicle = st.selectbox("Assign Vehicle", ["VH001", "VH002", "VH003"])
            
            submitted = st.form_submit_button("Assign Duty")
            if submitted:
                st.success(f"Duty {duty_id} assigned successfully!")
                tm.sleep(1)
                st.rerun()

# Route Management (GIS Map)
elif app_mode == "Route Management (GIS Map)":
    st.title("🗺 Route Management (GIS Map)")
    
    # Simulated GIS map (using static image in this prototype)
    st.image("https://maps.googleapis.com/maps/api/staticmap?center=24.7136,46.6753&zoom=11&size=800x400&maptype=roadmap&key=AIzaSyA-5Zi-xyz", 
             caption="Interactive GIS Map - Would show routes and vehicles in a real implementation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Route Information")
        routes_df = pd.DataFrame({
            "Route ID": ["R001", "R002", "R003"],
            "Name": ["City Center Loop", "Industrial Zone", "Suburban Circuit"],
            "Distance (km)": [15.2, 22.5, 18.7],
            "Avg. Duration": ["45 min", "1h 10min", "55 min"],
            "Stops": [8, 5, 6]
        })
        st.dataframe(routes_df, use_container_width=True)
    
    with col2:
        st.markdown("### Create/Edit Route")
        with st.form("route_form"):
            route_name = st.text_input("Route Name")
            route_type = st.selectbox("Route Type", ["Delivery", "Pickup", "Service", "Mixed"])
            distance = st.number_input("Distance (km)", min_value=0.1, step=0.1)
            stops = st.number_input("Number of Stops", min_value=1, step=1)
            
            submitted = st.form_submit_button("Save Route")
            if submitted:
                st.success("Route saved successfully!")

# Reports & Analytics
elif app_mode == "Reports & Analytics":
    st.title("📈 Reports & Analytics")
    
    tab1, tab2, tab3 = st.tabs(["Performance Reports", "Driver Analytics", "Vehicle Utilization"])
    
    with tab1:
        st.markdown("### Duty Performance Report")
        date_range = st.date_input("Select Date Range", 
                                 [datetime(2023, 1, 1), datetime(2023, 1, 31)])
        
        # Generate sample performance data
        performance_data = pd.DataFrame({
            "Date": pd.date_range(start=date_range[0], end=date_range[1]),
            "Completed": np.random.randint(5, 20, size=len(pd.date_range(start=date_range[0], end=date_range[1]))),
            "On Time": np.random.randint(3, 15, size=len(pd.date_range(start=date_range[0], end=date_range[1]))),
            "Delayed": np.random.randint(0, 5, size=len(pd.date_range(start=date_range[0], end=date_range[1])))
        })
        
        fig = px.bar(performance_data, x="Date", y=["Completed", "On Time", "Delayed"],
                     title="Duty Performance Over Time", barmode="group")
        st.plotly_chart(fig, use_container_width=True)
        
        st.download_button(
            "Download Report",
            performance_data.to_csv(index=False).encode('utf-8'),
            "duty_performance_report.csv",
            "text/csv"
        )
    
    with tab2:
        st.markdown("### Driver Performance")
        driver_data = pd.DataFrame({
            "Driver": ["John Doe", "Jane Smith", "Mike Johnson", "Sarah Williams"],
            "Completed Duties": [24, 22, 18, 15],
            "On Time %": [92, 95, 88, 85],
            "Avg. Rating": [4.8, 4.9, 4.5, 4.3],
            "Distance Driven (km)": [450, 420, 380, 320]
        })
        st.dataframe(driver_data, use_container_width=True)
        
        fig = px.bar(driver_data, x="Driver", y="Completed Duties", 
                     title="Duties Completed by Driver")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### Vehicle Utilization")
        vehicle_data = pd.DataFrame({
            "Vehicle": ["VH001", "VH002", "VH003", "VH004"],
            "Utilization %": [85, 78, 92, 65],
            "Distance (km)": [520, 480, 610, 390],
            "Maintenance Due": ["No", "Yes", "No", "Yes"]
        })
        st.dataframe(vehicle_data, use_container_width=True)
        
        fig = px.pie(vehicle_data, values="Utilization %", names="Vehicle",
                     title="Vehicle Utilization Distribution")
        st.plotly_chart(fig, use_container_width=True)

# Real-Time Monitor
elif app_mode == "Real-Time Monitor":
    st.title("📡 Real-Time Monitor")
    
    # Simulate real-time updates
    if 'refresh_count' not in st.session_state:
        st.session_state.refresh_count = 0
    
    def update_data():
        st.session_state.refresh_count += 1
        return pd.DataFrame({
            "Vehicle": ["VH001", "VH002", "VH003", "VH004"],
            "Status": ["On Route", "Idle", "On Route", "Maintenance"],
            "Location": ["Lat: 24.71, Long: 46.68", "Depot", "Lat: 24.75, Long: 46.70", "Workshop"],
            "Last Update": [datetime.now().strftime("%H:%M:%S")]*4,
            "Speed (km/h)": [45, 0, 60, 0],
            "Driver": ["John Doe", "N/A", "Jane Smith", "N/A"]
        })
    
    realtime_data = update_data()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### Vehicle Status")
        st.dataframe(realtime_data, use_container_width=True)
        
        # Simulated map with vehicle positions
        st.image("https://maps.googleapis.com/maps/api/staticmap?center=24.7136,46.6753&zoom=12&size=800x400&maptype=roadmap&markers=color:red%7C24.71,46.68&markers=color:blue%7C24.75,46.70&key=AIzaSyA-5Zi-xyz",
                 caption="Real-time vehicle locations (simulated)")
    
    with col2:
        st.markdown("### Monitor Controls")
        if st.button("Refresh Data"):
            realtime_data = update_data()
            st.rerun()
        
        st.markdown("### Alerts")
        alert_container = st.container()
        with alert_container:
            if st.session_state.refresh_count % 3 == 0:
                st.warning("Vehicle VH002 due for maintenance")
            if st.session_state.refresh_count % 5 == 0:
                st.error("Vehicle VH004 delayed by 30 minutes")

# User Management & Settings Panel
elif app_mode == "User Management & Settings":
    st.title("⚙️ User Management & Settings")
    
    tab1, tab2, tab3 = st.tabs(["User Management", "System Settings", "My Profile"])
    
    with tab1:
        st.markdown("### User List")
        users_df = generate_dummy_users()
        st.dataframe(users_df, use_container_width=True)
        
        st.markdown("### Add New User")
        with st.form("new_user_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name")
                username = st.text_input("Username")
            with col2:
                role = st.selectbox("Role", ["Admin", "Manager", "Driver", "Viewer"])
                status = st.selectbox("Status", ["Active", "Inactive"])
            
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            submitted = st.form_submit_button("Create User")
            if submitted:
                if password == confirm_password:
                    st.success("User created successfully!")
                else:
                    st.error("Passwords do not match!")
    
    with tab2:
        st.markdown("### System Configuration")
        with st.form("system_settings"):
            st.markdown("#### General Settings")
            timezone = st.selectbox("Timezone", ["UTC", "GMT+3 (Riyadh)", "GMT+8 (Singapore)"])
            date_format = st.selectbox("Date Format", ["YYYY-MM-DD", "DD/MM/YYYY", "MM/DD/YYYY"])
            
            st.markdown("#### Notification Settings")
            email_notifications = st.checkbox("Enable Email Notifications", True)
            push_notifications = st.checkbox("Enable Push Notifications", True)
            
            st.markdown("#### Data Retention")
            retention_period = st.slider("Data Retention Period (months)", 1, 36, 12)
            
            submitted = st.form_submit_button("Save Settings")
            if submitted:
                st.success("System settings updated successfully!")
    
    with tab3:
        st.markdown("### My Profile")
        col1, col2 = st.columns(2)
        
        with col1:
            st.image("https://via.placeholder.com/150?text=User", width=150)
            st.file_uploader("Change Profile Picture", type=["jpg", "png"])
        
        with col2:
            with st.form("profile_form"):
                name = st.text_input("Name", "Admin User")
                email = st.text_input("Email", "admin@company.com")
                phone = st.text_input("Phone", "+966 50 123 4567")
                
                st.markdown("### Change Password")
                current_password = st.text_input("Current Password", type="password")
                new_password = st.text_input("New Password", type="password")
                confirm_password = st.text_input("Confirm New Password", type="password")
                
                submitted = st.form_submit_button("Update Profile")
                if submitted:
                    if new_password == confirm_password:
                        st.success("Profile updated successfully!")
                    else:
                        st.error("New passwords do not match!")
