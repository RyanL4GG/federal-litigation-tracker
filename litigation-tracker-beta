import sys

try:
    import streamlit as st
    import pandas as pd
except ModuleNotFoundError:
    sys.exit("Required module 'streamlit' not found. Install it using: pip install streamlit")

# Sample litigation data (expandable with real-time API integration)
litigation_data = pd.DataFrame([
    {"Case Number": "22-001", "Case Title": "State v. Federal Agency", "Court": "D.C. District Court",
     "Date Filed": "2024-02-10", "Last Update": "2025-02-25", "Status": "Active", 
     "Key Rulings": "Preliminary Injunction Issued", "Impact on Federal Grants": "High"},
    
    {"Case Number": "23-045", "Case Title": "Nonprofit v. EPA", "Court": "9th Circuit",
     "Date Filed": "2023-10-05", "Last Update": "2025-02-20", "Status": "Pending Decision",
     "Key Rulings": "Motion to Dismiss Denied", "Impact on Federal Grants": "Moderate"},
    
    {"Case Number": "24-102", "Case Title": "Company v. Department of Energy", "Court": "Federal Circuit",
     "Date Filed": "2024-01-15", "Last Update": "2025-02-22", "Status": "Active",
     "Key Rulings": "No Injunction", "Impact on Federal Grants": "Low"},
    
    {"Case Number": "21-378", "Case Title": "Advocacy Group v. HHS", "Court": "D.C. Circuit",
     "Date Filed": "2021-09-22", "Last Update": "2025-02-26", "Status": "Final Ruling",
     "Key Rulings": "Permanent Injunction Issued", "Impact on Federal Grants": "Severe"}
])

# Streamlit UI
st.set_page_config(page_title="Federal Litigation Tracker", layout="wide")
st.title("Federal Litigation Tracker")
st.write("Monitor federal lawsuits and key rulings affecting grant programs.")

# Filter by Impact Level
impact_filter = st.sidebar.selectbox("Filter by Grant Impact Level:", ["All", "Severe", "High", "Moderate", "Low"])
if impact_filter != "All":
    litigation_data = litigation_data[litigation_data["Impact on Federal Grants"] == impact_filter]

# Search Bar for Case Title or Number
search_query = st.sidebar.text_input("Search by Case Title or Number:")
if search_query:
    litigation_data = litigation_data[litigation_data.apply(lambda row: search_query.lower() in row.to_string().lower(), axis=1)]

# Display Data
st.dataframe(litigation_data, height=500)

# Email Alerts Section (Placeholder for Future Integration)
st.sidebar.header("Alerts & Notifications")
st.sidebar.write("Coming soon: Email & Slack notifications for case updates.")
