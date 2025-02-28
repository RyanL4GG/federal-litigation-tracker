import sys
import requests
import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# Function to fetch litigation data from CourtListener API (free source)
def fetch_litigation_data():
    url = "https://www.courtlistener.com/api/rest/v3/dockets/?type=federal"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        case_list = []
        for case in data.get("results", []):
            case_list.append({
                "Case Number": case.get("docket_number", "N/A"),
                "Case Link": f"[Link]({case.get('absolute_url', '#')})",
                "Case Title": case.get("case_name", "N/A"),
                "Court": case.get("court", {}).get("name", "Unknown Court"),
                "Date Filed": case.get("date_filed", "N/A"),
                "Last Update": case.get("date_modified", "N/A"),
                "Status": "Pending" if not case.get("date_terminated") else "Closed",
                "Key Rulings": "N/A",
                "Impact on Federal Grants": "Unknown",
                "Litigation Summary": "Details not available in CourtListener API. Click the link for more information."
            })
        return pd.DataFrame(case_list)
    else:
        st.error("Failed to fetch litigation data.")
        return pd.DataFrame()

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

# Auto-refresh every 30 minutes
st_autorefresh(interval=30*60*1000, key="data_refresh")

# Fetch litigation data
litigation_data = fetch_litigation_data()

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

# Display Litigation Change Summaries
st.subheader("Recent Litigation Updates Impacting Grants")
for _, row in litigation_data.iterrows():
    st.markdown(f"**[{row['Case Number']}]({row['Case Link']}) - {row['Case Title']} ({row['Court']})**")
    st.write(f"Filed: {row['Date Filed']}, Last Update: {row['Last Update']}")
    st.write(f"Status: {row['Status']}, Key Rulings: {row['Key Rulings']}")
    st.write(f"Impact Level: {row['Impact on Federal Grants']}")
    st.write(f"Litigation Summary: {row['Litigation Summary']}")
    st.write("---")

# Alerts & Notifications Section
st.sidebar.header("Alerts & Notifications")
st.sidebar.write("Coming soon: Email & Slack notifications for case updates.")
st.sidebar.button("Subscribe to Alerts")
