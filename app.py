import sys
import requests
import streamlit as st
import pandas as pd
import time

# Function to fetch litigation data from CourtListener API (free source)
def fetch_litigation_data():
    url = "https://www.courtlistener.com/api/rest/v3/dockets/?type=federal"
    headers = {"User-Agent": "Litigation-Tracker/1.0"}  # User-Agent to prevent blocking
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an error for HTTP errors
        data = response.json()
        st.write("Raw API Response:", data)  # Debugging step to check API response
        if "results" in data and len(data["results"]) > 0:
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
            st.warning("No recent litigation cases found.")
            return pd.DataFrame(columns=["Case Number", "Case Link", "Case Title", "Court", "Date Filed", "Last Update", "Status", "Key Rulings", "Impact on Federal Grants", "Litigation Summary"])
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch litigation data: {e}")
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

# Auto-refresh using a loop
if "last_refresh" not in st.session_state or time.time() - st.session_state["last_refresh"] > 1800:
    litigation_data = fetch_litigation_data()
    st.session_state["litigation_data"] = litigation_data
    st.session_state["last_refresh"] = time.time()
else:
    litigation_data = st.session_state["litigation_data"]

# Sidebar Filters
st.sidebar.header("Filters")
impact_filter = st.sidebar.selectbox("Filter by Grant Impact Level:", ["All", "Severe", "High", "Moderate", "Low"])
if impact_filter != "All" and not litigation_data.empty:
    litigation_data = litigation_data[litigation_data["Impact on Federal Grants"] == impact_filter]

search_query = st.sidebar.text_input("Search by Case Title or Number:")
if search_query and not litigation_data.empty:
    litigation_data = litigation_data[litigation_data.apply(lambda row: search_query.lower() in row.to_string().lower(), axis=1)]

# Display Litigation Data in Table
st.subheader("Litigation Cases")
if litigation_data.empty:
    st.write("No litigation cases available at this time.")
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
if litigation_data.empty:
    st.write("No litigation updates available.")
else:
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
