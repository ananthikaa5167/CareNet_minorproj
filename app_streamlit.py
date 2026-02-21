import streamlit as st
import pandas as pd
from algorithm.routing_algorithm import route_vulnerability_case
from data.sample_inputs import ngos
from auth import init_db, register_user, login_user
from database import (
    init_case_table,
    insert_case,
    fetch_cases,
    assign_volunteer,
    update_case_status
)

# ---------- CONFIG ----------
st.set_page_config(page_title="CareNet", layout="wide")
init_db()
init_case_table()

# ---------- SESSION ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None

# =====================================================
# LOGIN
# =====================================================
if not st.session_state.logged_in:

    st.title("CareNet Login")
    menu = st.radio("Select Option", ["Login", "Register"])

    if menu == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            role = login_user(username, password)
            if role:
                st.session_state.logged_in = True
                st.session_state.role = role
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid credentials")

    else:
        username = st.text_input("New Username")
        password = st.text_input("New Password", type="password")
        role = st.selectbox("Role", ["admin", "volunteer", "reporter"])

        if st.button("Register"):
            if register_user(username, password, role):
                st.success("Registered successfully")
            else:
                st.error("Username exists")

    st.stop()

# =====================================================
# DASHBOARD
# =====================================================
role = st.session_state.role
username = st.session_state.username

st.sidebar.title("CareNet")

if role == "admin":
    pages = ["Home", "Routing", "Reports", "Analytics"]
elif role == "volunteer":
    pages = ["Home", "My Cases"]
else:
    pages = ["Home", "Routing"]

module = st.sidebar.radio("Navigate", pages)

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None
    st.rerun()

# ================= HOME =================
if module == "Home":
    st.title("CareNet Control Center")
    st.write("AI‑assisted platform for routing and managing cases.")

# ================= ROUTING =================
elif module == "Routing":
    st.header("Route Case")

    lat = st.number_input("Latitude", value=12.97)
    lon = st.number_input("Longitude", value=80.22)
    condition = st.selectbox("Condition", ["injured", "hungry", "alone"])
    delay = st.slider("Delay", 1, 10, 2)

    if st.button("Route Case"):
        report = {"id": 1, "lat": lat, "lon": lon,
                  "condition": condition, "time_delay": delay}

        result = route_vulnerability_case(report, ngos)

        insert_case(
            lat,
            lon,
            condition,
            delay,
            result["priority_score"],
            result["assigned_ngo"],
            "Pending"
        )

        st.success("Case Routed")
        st.write(result)

# ================= ADMIN CASE MANAGEMENT =================
elif module == "Reports":
    st.header("Case Management")

    data = fetch_cases()

    if data:
        df = pd.DataFrame(data, columns=[
            "ID","Latitude","Longitude","Condition","Delay",
            "Priority","NGO","Volunteer","Status"
        ])
        st.dataframe(df)

        st.subheader("Update Case")

        case_id = st.selectbox("Case ID", df["ID"])
        volunteer = st.text_input("Assign Volunteer")
        status = st.selectbox("Status", ["Pending", "In Progress", "Resolved"])

        col1, col2 = st.columns(2)

        if col1.button("Assign"):
            assign_volunteer(case_id, volunteer)
            st.success("Volunteer assigned")
            st.rerun()

        if col2.button("Update Status"):
            update_case_status(case_id, status)
            st.success("Status updated")
            st.rerun()

# ================= VOLUNTEER DASHBOARD =================
elif module == "My Cases":
    st.header("My Assigned Cases")

    data = fetch_cases()

    if data:
        df = pd.DataFrame(data, columns=[
            "ID","Latitude","Longitude","Condition","Delay",
            "Priority","NGO","Volunteer","Status"
        ])

        my_cases = df[df["Volunteer"] == username]

        if not my_cases.empty:
            st.dataframe(my_cases)

            st.subheader("Workflow Status")

            for _, row in my_cases.iterrows():
                st.write(f"### Case {row['ID']}")
                st.progress(
                    33 if row["Status"] == "Pending"
                    else 66 if row["Status"] == "In Progress"
                    else 100
                )
                st.write(f"Current Status: **{row['Status']}**")
        else:
            st.info("No assigned cases")

# ================= ANALYTICS =================
elif module == "Analytics":
    st.header("System Analytics")

    data = fetch_cases()

    if data:
        df = pd.DataFrame(data, columns=[
            "ID","Latitude","Longitude","Condition","Delay",
            "Priority","NGO","Volunteer","Status"
        ])

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Cases", len(df))
        col2.metric("Avg Priority", round(df["Priority"].mean(),2))
        col3.metric("Resolved %",
                    f"{(df['Status']=='Resolved').mean()*100:.1f}%")

        st.subheader("Cases by Condition")
        st.bar_chart(df["Condition"].value_counts())

        st.subheader("Status Distribution")
        st.bar_chart(df["Status"].value_counts())

    else:
        st.info("No data yet")