import sys

try:
    import streamlit as st
    import pandas as pd
except ModuleNotFoundError:
    sys.exit("Required module 'streamlit' not found. Install it using: pip install streamlit")

# Sample litigation data (expandable with real-time API integration)
litigation_data = pd.DataFrame([
    {"Case Number": "[22-001](https://example.com/litigation-22-001)", "Case Title": "State v. Federal Agency", "Court": "D.C. District Court",
     "Date Filed": "2024-02-10", "Last Update": "2025-02-25", "Status": "Active", 
     "Key Rulings": "Preliminary Injunction Issued", "Impact on Federal Grants": "High"},
    
    {"Case Number": "[23-045](https://example.com/litigation-23-045)", "Case Title": "Nonprofit v. EPA", "Court": "9th Circuit",
     "Date Filed": "2023-10-05", "Last Update": "2025-02-20", "Status": "Pending Decision",
     "Key Rulings": "Motion to Dismiss Denied", "Impact on Federal Grants": "Moderate"},
    
    {"Case Number": "[24-102](https://example.com/litigation-24-102)", "Case Title": "Company v. Department of Energy", "Court": "Federal Circuit",
     "Date Filed": "2024-01-15", "Last Update": "2025-02-22", "Status": "Active",
     "Key Rulings": "No Injunction", "Impact on Federal Grants": "Low"},
    
    {"Case Number": "[21-378](https://example.com/litigation-21-378)", "Case Title": "Advocacy Group v. HHS", "Court": "D.C. Circuit",
     "Date Filed": "2021-09-22", "Last Update": "2025-02-26", "Status": "Final Ruling",
     "Key Rulings": "Permanent Injunction Issued", "Impact on Federal Grants": "Severe"}
])

policy_data = pd.DataFrame([
    {"Policy Name": "[New Federal Grant Policy](https://example.com/policy-education)", "Agency": "Department of Education",
     "Effective Date": "2025-02-20", "Impact on Grants": "High",
     "Policy Change Summary": "Increased funding allocation and stricter eligibility criteria for grant recipients."},
    
    {"Policy Name": "[Energy Grant Regulation Update](https://example.com/policy-energy)", "Agency": "Department of Energy",
     "Effective Date": "2025-01-15", "Impact on Grants": "Moderate",
     "Policy Change Summary": "Updated reporting requirements for renewable energy projects receiving federal grants."}
])

# Streamlit UI
st.set_page_config(page_title="Federal Litigation Tracker", layout="wide")
st.title("Federal Litigation Tracker")
st.write("Monitor federal lawsuits, key rulings, and policy changes affecting grant programs.")

# Sidebar Filters
st.sidebar.header("Filters")
impact_filter = st.sidebar.selectbox("Filter by Grant Impact Level:", ["All", "Severe", "High", "Moderate", "Low"])
if impact_filter != "All":
    litigation_data = litigation_data[litigation_data["Impact on Federal Grants"] == impact_filter]

search_query = st.sidebar.text_input("Search by Case Title or Number:")
if search_query:
    litigation_data = litigation_data[litigation_data.apply(lambda row: search_query.lower() in row.to_string().lower(), axis=1)]

# Display Litigation Data in Table
st.subheader("Litigation Cases")
st.dataframe(litigation_data)

# Display Policy Data in Table
st.subheader("Grant Policy Updates")
st.dataframe(policy_data)

# Display Policy Change Summaries
st.subheader("Recent Policy Changes Impacting Grants")
for _, row in policy_data.iterrows():
    st.markdown(f"**{row['Policy Name']} ({row['Agency']})**")
    st.write(f"Effective Date: {row['Effective Date']}")
    st.write(f"Impact Level: {row['Impact on Grants']}")
    st.write(f"Change Summary: {row['Policy Change Summary']}")
    st.write("---")

# Alerts & Notifications Section
st.sidebar.header("Alerts & Notifications")
st.sidebar.write("Coming soon: Email & Slack notifications for case updates.")
st.sidebar.button("Subscribe to Alerts")
