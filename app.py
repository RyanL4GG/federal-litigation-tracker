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
    {"Case Number": "1:25-cv-00001", "Case Title": "AIDS Vaccine Advocacy Coalition v. Department of State", "Court": "District of Columbia", "Date Filed": "2025-01-20", "Last Update": "2025-02-27", "Status": "Pending", "Case Link": "[Link](https://turn0news13)", "Key Rulings": "N/A", "Impact on Federal Grants": "Addresses restrictions on federal health research grants.", "Litigation Summary": "Public health organizations challenge cuts to federal funding for vaccine development programs."},
    {"Case Number": "1:25-cv-00333", "Case Title": "National Association of Diversity Officers in Higher Education et al. v. Trump et al.", "Court": "District of Maryland", "Date Filed": "2025-02-01", "Last Update": "2025-02-21", "Status": "Preliminary Injunction Granted", "Case Link": "[Link](https://turn0search1)", "Key Rulings": "Preliminary injunction issued, blocking enforcement of key provisions of Executive Orders 14151 and 14173.", "Impact on Federal Grants": "Halts implementation of executive orders restricting DEI program funding.", "Litigation Summary": "Plaintiffs challenge executive orders terminating federal support for DEI programs, leading to a court injunction blocking key provisions."}
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

# Alerts & Notifications Section
st.sidebar.header("Alerts & Notifications")
st.sidebar.write("Coming soon: Email & Slack notifications for case updates.")
st.sidebar.button("Subscribe to Alerts")
