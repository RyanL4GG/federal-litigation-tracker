import sys
import requests
import streamlit as st
import pandas as pd
import time
from datetime import datetime
from bs4 import BeautifulSoup

# Hardcoded litigation cases (to avoid reliance on APIs)
litigation_cases = pd.DataFrame([
    {"Case Number": "1:24-cv-00001", "Case Title": "Environmental Defense Fund v. EPA", "Court": "D.C. District Court", "Date Filed": "2024-01-20", "Last Update": "2024-02-15", "Status": "Pending", "Case Link": "[Link](https://example.com/case1)"},
    {"Case Number": "2:24-cv-00002", "Case Title": "Sierra Club v. FERC", "Court": "9th Circuit Court", "Date Filed": "2024-01-22", "Last Update": "2024-02-18", "Status": "Pending", "Case Link": "[Link](https://example.com/case2)"},
    {"Case Number": "3:24-cv-00003", "Case Title": "Natural Resources Defense Council v. DOI", "Court": "Southern District of New York", "Date Filed": "2024-01-25", "Last Update": "2024-02-10", "Status": "Pending", "Case Link": "[Link](https://example.com/case3)"},
    {"Case Number": "4:24-cv-00004", "Case Title": "WildEarth Guardians v. USFS", "Court": "D.C. Circuit Court", "Date Filed": "2024-01-28", "Last Update": "2024-02-12", "Status": "Pending", "Case Link": "[Link](https://example.com/case4)"}
])

# Hardcoded policy updates since 09-30-2023
policy_data = pd.DataFrame([
    {"Policy Name": "NEPA Streamlining Final Rule", "Policy Link": "[Link](https://www.federalregister.gov/documents/2023/10/05/2023-22001/nepa-streamlining-final-rule)", "Agency": "CEQ", "Effective Date": "2023-10-05", "Impact on Grants": "High", "Policy Change Summary": "The policy updates NEPA procedures to expedite environmental review timelines."},
    {"Policy Name": "Revised Clean Water Act Guidance", "Policy Link": "[Link](https://www.federalregister.gov/documents/2023/11/15/2023-25050/revised-clean-water-act-guidance)", "Agency": "EPA", "Effective Date": "2023-11-15", "Impact on Grants": "Moderate", "Policy Change Summary": "Revised water quality compliance requirements affecting infrastructure grants."},
    {"Policy Name": "Infrastructure Grant Program Expansion", "Policy Link": "[Link](https://www.federalregister.gov/documents/2024/01/10/2024-00550/infrastructure-grant-program-expansion)", "Agency": "DOT", "Effective Date": "2024-01-10", "Impact on Grants": "High", "Policy Change Summary": "New funding and eligibility rules for state transportation projects."}
])

# Streamlit UI
st.set_page_config(page_title="Federal Litigation Tracker", layout="wide")
st.title("Federal Litigation Tracker")
st.write("Monitor federal lawsuits, key rulings, and policy changes affecting grant programs.")

# Auto-refresh every 30 minutes
if "last_refresh" not in st.session_state or time.time() - st.session_state["last_refresh"] > 1800:
    st.session_state["case_data"] = litigation_cases
    st.session_state["last_refresh"] = time.time()
else:
    litigation_cases = st.session_state["case_data"]

# Display Litigation Cases
st.subheader("Litigation Cases")
st.dataframe(litigation_cases)

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
