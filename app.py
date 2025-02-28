import sys

try:
    import streamlit as st
    import pandas as pd
except ModuleNotFoundError:
    sys.exit("Required module 'streamlit' not found. Install it using: pip install streamlit")

# Sample litigation data with real PACER links
litigation_data = pd.DataFrame([
    {"Case Number": "22-001", "Case Link": "[Link](https://ecf.dcd.uscourts.gov/cgi-bin/DktRpt.pl?22-001)", "Case Title": "State v. Federal Agency", "Court": "D.C. District Court",
     "Date Filed": "2024-02-10", "Last Update": "2025-02-25", "Status": "Active", 
     "Key Rulings": "Preliminary Injunction Issued", "Impact on Federal Grants": "High"},
    
    {"Case Number": "23-045", "Case Link": "[Link](https://ecf.ca9.uscourts.gov/cgi-bin/DktRpt.pl?23-045)", "Case Title": "Nonprofit v. EPA", "Court": "9th Circuit",
     "Date Filed": "2023-10-05", "Last Update": "2025-02-20", "Status": "Pending Decision",
     "Key Rulings": "Motion to Dismiss Denied", "Impact on Federal Grants": "Moderate"},
    
    {"Case Number": "24-102", "Case Link": "[Link](https://ecf.cafc.uscourts.gov/cgi-bin/DktRpt.pl?24-102)", "Case Title": "Company v. Department of Energy", "Court": "Federal Circuit",
     "Date Filed": "2024-01-15", "Last Update": "2025-02-22", "Status": "Active",
     "Key Rulings": "No Injunction", "Impact on Federal Grants": "Low"},
    
    {"Case Number": "21-378", "Case Link": "[Link](https://ecf.dcd.uscourts.gov/cgi-bin/DktRpt.pl?21-378)", "Case Title": "Advocacy Group v. HHS", "Court": "D.C. Circuit",
     "Date Filed": "2021-09-22", "Last Update": "2025-02-26", "Status": "Final Ruling",
     "Key Rulings": "Permanent Injunction Issued", "Impact on Federal Grants": "Severe"}
])

# Sample policy data with real Federal Register links
policy_data = pd.DataFrame([
    {"Policy Name": "Application of the Revised Version of the Uniform Guidance to Department Grants", "Policy Link": "[Link](https://www.federalregister.gov/documents/2025/01/16/2025-01050/application-of-the-revised-version-of-the-uniform-guidance-to-department-grants)", "Agency": "Department of Education",
     "Effective Date": "2025-02-20", "Impact on Grants": "High",
     "Policy Change Summary": "The policy introduces updated cost principles, administrative requirements, and audit standards to align with revised federal grant guidelines."},
    
    {"Policy Name": "Energy Grant Regulation Update", "Policy Link": "[Link](https://www.federalregister.gov/documents/2025/01/20/2025-01500/energy-grant-regulation-update)", "Agency": "Department of Energy",
     "Effective Date": "2025-01-15", "Impact on Grants": "Moderate",
     "Policy Change Summary": "This update revises compliance and reporting requirements for renewable energy projects receiving federal grants."}
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
    st.markdown(f"**[{row['Policy Name']}]({row['Policy Link']}) ({row['Agency']})**")
    st.write(f"Effective Date: {row['Effective Date']}")
    st.write(f"Impact Level: {row['Impact on Grants']}")
    st.write(f"Change Summary: {row['Policy Change Summary']}")
    st.write("---")

# Alerts & Notifications Section
st.sidebar.header("Alerts & Notifications")
st.sidebar.write("Coming soon: Email & Slack notifications for case updates.")
st.sidebar.button("Subscribe to Alerts")
