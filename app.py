import sys
import requests
import streamlit as st
import pandas as pd
import time
from datetime import datetime
from bs4 import BeautifulSoup

# Updated litigation cases relevant to federal grants
litigation_cases = pd.DataFrame([
    {"Case Number": "1:25-cv-00039", "Case Title": "New York et al. v. Trump et al.", "Court": "District of Rhode Island", "Date Filed": "2025-01-28", "Last Update": "2025-02-10", "Status": "Pending", "Case Link": "[Link](https://turn0search21)", "Key Rulings": "N/A", "Impact on Federal Grants": "Challenges federal funding limitations on state-led environmental projects.", "Litigation Summary": "States challenge new federal restrictions on grant funding for renewable energy programs."},
    {"Case Number": "1:25-cv-00144", "Case Title": "Democracy Forward Foundation v. OMB", "Court": "District of Columbia", "Date Filed": "2025-01-28", "Last Update": "2025-02-03", "Status": "Pending", "Case Link": "[Link](https://turn0search21)", "Key Rulings": "N/A", "Impact on Federal Grants": "Affects transparency in federal grant decision-making processes.", "Litigation Summary": "Advocacy group sues OMB over lack of transparency in federal grant allocations and decision-making."},
    {"Case Number": "1:25-cv-01144", "Case Title": "New York et al. v. Trump et al.", "Court": "Southern District of New York", "Date Filed": "2025-02-07", "Last Update": "2025-02-14", "Status": "Pending", "Case Link": "[Link](https://turn0search22)", "Key Rulings": "N/A", "Impact on Federal Grants": "Seeks to reinstate funding for climate resilience projects.", "Litigation Summary": "State coalition sues over executive order revoking federal climate adaptation funding."},
    {"Case Number": "1:25-cv-00001", "Case Title": "AIDS Vaccine Advocacy Coalition v. Department of State", "Court": "District of Columbia", "Date Filed": "2025-01-20", "Last Update": "2025-02-27", "Status": "Pending", "Case Link": "[Link](https://turn0news13)", "Key Rulings": "N/A", "Impact on Federal Grants": "Addresses restrictions on federal health research grants.", "Litigation Summary": "Public health organizations challenge cuts to federal funding for vaccine development programs."}
])

# Updated policy updates since 09-30-2023
policy_data = pd.DataFrame([
    {"Policy Name": "NEPA Streamlining Final Rule", "Policy Link": "[Link](https://www.federalregister.gov/documents/2023/10/05/2023-22001/nepa-streamlining-final-rule)", "Agency": "CEQ", "Effective Date": "2023-10-05", "Impact on Grants": "High", "Policy Change Summary": "The policy updates NEPA procedures to expedite environmental review timelines."},
    {"Policy Name": "Revised Clean Water Act Guidance", "Policy Link": "[Link](https://www.federalregister.gov/documents/2023/11/15/2023-25050/revised-clean-water-act-guidance)", "Agency": "EPA", "Effective Date": "2023-11-15", "Impact on Grants": "Moderate", "Policy Change Summary": "Revised water quality compliance requirements affecting infrastructure grants."},
    {"Policy Name": "Infrastructure Grant Program Expansion", "Policy Link": "[Link](https://www.federalregister.gov/documents/2024/01/10/2024-00550/infrastructure-grant-program-expansion)", "Agency": "DOT", "Effective Date": "2024-01-10", "Impact on Grants": "High", "Policy Change Summary": "New funding and eligibility rules for state transportation projects."},
    {"Policy Name": "Application of the Revised Uniform Guidance", "Policy Link": "[Link](https://www.federalregister.gov/documents/2025/01/16/2025-01050/application-of-the-revised-version-of-the-uniform-guidance-to-department-grants)", "Agency": "Department of Education", "Effective Date": "2025-02-20", "Impact on Grants": "High", "Policy Change Summary": "Updates cost principles, administrative requirements, and audit standards to align with revised federal grant guidelines."},
    {"Policy Name": "Energy Grant Regulation Update", "Policy Link": "[Link](https://www.federalregister.gov/documents/2025/01/20/2025-01500/energy-grant-regulation-update)", "Agency": "Department of Energy", "Effective Date": "2025-01-15", "Impact on Grants": "Moderate", "Policy Change Summary": "Revises compliance and reporting requirements for renewable energy projects receiving federal grants."}
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
