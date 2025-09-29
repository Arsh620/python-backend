import streamlit as st
import requests
import json

# Configure page
st.set_page_config(page_title="User Management", page_icon="👤")

# API base URL
API_BASE = "http://localhost:8000"

st.title("👤 User Management System")

# Sidebar for navigation
page = st.sidebar.selectbox("Choose Action", ["Register", "Login", "Dashboard"])

if page == "Register":
    st.header("📝 Register New User")
    
    with st.form("register_form"):
        email = st.text_input("Email")
        username = st.text_input("Username")
        full_name = st.text_input("Full Name")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Register"):
            if email and username and password:
                try:
                    response = requests.post(f"{API_BASE}/auth/register", 
                                           json={
                                               "email": email,
                                               "username": username,
                                               "full_name": full_name,
                                               "password": password
                                           })
                    
                    if response.status_code == 201:
                        result = response.json()
                        st.success("✅ Registration successful!")
                        st.json(result)
                    else:
                        st.error(f"❌ Registration failed: {response.json().get('detail', 'Unknown error')}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to API. Make sure FastAPI server is running.")
            else:
                st.warning("⚠️ Please fill all required fields")

elif page == "Login":
    st.header("🔐 Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Login"):
            if username and password:
                try:
                    response = requests.post(f"{API_BASE}/auth/login",
                                           json={
                                               "username": username,
                                               "password": password
                                           })
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ Login successful!")
                        
                        # Store token in session state
                        st.session_state.token = result["data"]["access_token"]
                        st.session_state.user = result["data"]["user"]
                        
                        st.json(result)
                    else:
                        st.error(f"❌ Login failed: {response.json().get('detail', 'Invalid credentials')}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to API. Make sure FastAPI server is running.")
            else:
                st.warning("⚠️ Please enter username and password")

elif page == "Dashboard":
    st.header("📊 Dashboard")
    
    if "token" in st.session_state:
        st.success(f"Welcome, {st.session_state.user['username']}!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👤 Your Profile")
            st.write(f"**ID:** {st.session_state.user['id']}")
            st.write(f"**Email:** {st.session_state.user['email']}")
            st.write(f"**Username:** {st.session_state.user['username']}")
            st.write(f"**Full Name:** {st.session_state.user['full_name']}")
            st.write(f"**Status:** {'Active' if st.session_state.user['is_active'] else 'Inactive'}")
        
        with col2:
            st.subheader("🔑 Token Info")
            st.code(st.session_state.token[:50] + "...")
            
        if st.button("🚪 Logout"):
            del st.session_state.token
            del st.session_state.user
            st.rerun()
    else:
        st.warning("⚠️ Please login first")
        st.info("👈 Use the sidebar to navigate to Login page")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("💡 Make sure FastAPI server is running on localhost:8000")