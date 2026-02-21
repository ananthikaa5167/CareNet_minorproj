import streamlit as st
import pandas as pd
from algorithm.routing_algorithm import route_vulnerability_case
from data.sample_inputs import ngos
from auth import init_db, register_user, login_user

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="CareNet Dashboard", layout="wide")
init_db()

# ---------- ADVANCED UI STYLES ----------
st.markdown("""
<style>

/* Background gradient */
.stApp {
    background: linear-gradient(135deg, #020617, #0f172a);
    color: #e5e7eb;
}

/* Title gradient */
.main-title {
    font-size: 44px;
    font-weight: 700;
    background: linear-gradient(90deg,#22c55e,#3b82f6,#a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Glass card */
.card {
    padding: 24px;
    border-radius: 18px;
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    transition: all 0.25s ease;
}

/* Hover animation */
.card:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 20px 40px rgba(0,0,0,0.6);
}

/* Buttons */
.stButton>button {
    border-radius: 12px;
    background: linear-gradient(90deg,#22c55e,#3b82f6);
    color: white;
    border: none;
    padding: 0.6em 1.2em;
    font-weight: 600;
}
.stButton>button:hover {
    background: linear-gradient(90deg,#16a34a,#2563eb);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(15,23,42,0.9);
    backdrop-filter: blur(10px);
}

</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

# =====================================================
# 🔐 LOGIN & REGISTER PAGE
# =====================================================
if not st.session_state.logged_in:

    st.markdown('<p class="main-title">CareNet Login</p>', unsafe_allow_html=True)

    menu = st.radio("Select Option", ["Login", "Register"])

    if menu == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            role = login_user(username, password)
            if role:
                st.session_state.logged_in = True
                st.session_state.role = role
                st.rerun()
            else:
                st.error("Invalid credentials")

    else:
        st.subheader("Register New User")
        username = st.text_input("New Username")
        password = st.text_input("New Password", type="password")
        role = st.selectbox("Role", ["admin", "volunteer", "reporter"])

        if st.button("Register"):
            if register_user(username, password, role):
                st.success("Registered successfully")
            else:
                st.error("Username already exists")

    st.stop()

# =====================================================
# 🧭 DASHBOARD
# =====================================================
role = st.session_state.role

st.sidebar.title("🧭 CareNet")

if role == "admin":
    pages = ["Home", "Routing", "NGOs", "Reports", "Volunteers", "Analytics"]
elif role == "volunteer":
    pages = ["Home", "Routing", "Reports"]
else:
    pages = ["Home", "Routing"]

module = st.sidebar.radio("Navigate", pages)

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.role = None
    st.rerun()

# ================= HOME =================
if module == "Home":

    st.markdown('<p class="main-title">CareNet Control Center</p>', unsafe_allow_html=True)
    st.write("AI‑assisted coordination platform for community welfare and assistance routing.")

    if role == "admin":
        st.subheader("👩‍💼 Admin Overview")

        col1, col2, col3 = st.columns(3)
        col1.markdown('<div class="card">📊 Analytics Dashboard<br><small>Monitor system performance</small></div>', unsafe_allow_html=True)
        col2.markdown('<div class="card">📄 Case Management<br><small>Track all reports</small></div>', unsafe_allow_html=True)
        col3.markdown('<div class="card">👥 User Administration<br><small>Manage volunteers & reporters</small></div>', unsafe_allow_html=True)

    elif role == "volunteer":
        st.subheader("🤝 Volunteer Panel")

        col1, col2 = st.columns(2)
        col1.markdown('<div class="card">🚑 Active Assignments<br><small>View cases needing help</small></div>', unsafe_allow_html=True)
        col2.markdown('<div class="card">📍 Nearby Requests<br><small>Locate assistance areas</small></div>', unsafe_allow_html=True)

    else:
        st.subheader("🧑‍🤝‍🧑 Reporter Panel")

        col1, col2 = st.columns(2)
        col1.markdown('<div class="card">📝 Submit Case<br><small>Report vulnerable individuals</small></div>', unsafe_allow_html=True)
        col2.markdown('<div class="card">📊 Track Requests<br><small>Monitor report status</small></div>', unsafe_allow_html=True)

# ================= ROUTING =================
elif module == "Routing":
    st.header("🚑 Vulnerability Routing")

    lat = st.number_input("Latitude", value=12.9716)
    lon = st.number_input("Longitude", value=80.2200)
    condition = st.selectbox("Condition", ["injured", "hungry", "alone"])
    time_delay = st.slider("Time Delay (hours)", 1, 10, 2)

    if st.button("Route Case"):
        report = {
            "id": 1,
            "lat": lat,
            "lon": lon,
            "condition": condition,
            "time_delay": time_delay
        }

        result = route_vulnerability_case(report, ngos)

        st.success("Routing Completed")
        st.metric("Priority Score", result["priority_score"])
        st.write("Assigned NGO:", result["assigned_ngo"])
        st.write("Status:", result["status"])
        st.map(pd.DataFrame([{"lat": lat, "lon": lon}]))

# ================= NGOs =================
elif module == "NGOs":
    st.header("🏥 NGO Directory")
    ngo_df = pd.DataFrame(ngos)
    st.dataframe(ngo_df)
    st.map(ngo_df)

# ================= REPORTS =================
elif module == "Reports":
    st.header("📄 Case Reports")

    reports = [
        {"Case ID": 1, "Condition": "Injured", "Priority": "High"},
        {"Case ID": 2, "Condition": "Hungry", "Priority": "Medium"}
    ]

    st.table(pd.DataFrame(reports))

# ================= VOLUNTEERS =================
elif module == "Volunteers":
    st.header("🤝 Volunteer Module")

    name = st.text_input("Volunteer Name")
    skill = st.text_input("Skill")

    if st.button("Add Volunteer"):
        st.success(f"{name} added successfully!")

# ================= ANALYTICS =================
elif module == "Analytics":
    st.header("📊 Evaluation Metrics")

    data = {
        "Condition": ["injured", "hungry", "alone", "injured", "hungry"],
        "Priority": [9, 6, 4, 8, 5],
        "Status": ["ASSIGNED", "ASSIGNED", "ASSIGNED", "ASSIGNED", "ASSIGNED"]
    }

    df = pd.DataFrame(data)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Cases", len(df))
    col2.metric("Average Priority", round(df["Priority"].mean(), 2))
    col3.metric("Routing Success Rate", f"{(df['Status']=='ASSIGNED').mean()*100:.1f}%")

    st.subheader("Priority Distribution")
    st.bar_chart(df["Priority"])

    st.subheader("Condition Distribution")
    st.bar_chart(df["Condition"].value_counts())