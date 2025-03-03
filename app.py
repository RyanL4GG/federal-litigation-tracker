import sys
import requests
import streamlit as st
import pandas as pd
import time
from datetime import datetime
from bs4 import BeautifulSoup

# List of predefined lawsuits to track
litigation_cases = pd.DataFrame([
    {"Case Number": "1:25-cv-00039", "Case Title": "New York et al. v. Trump et al.", "Court": "District of Rhode Island", "Date Filed": "2025-01-28", "Last Update": "2025-02-10", "Status": "Pending", "Case Link": "[Link](https://turn0search21)"},
    {"Case Number": "1:25-cv-00144", "Case Title": "Democracy Forward Foundation v. OMB", "Court": "District of Columbia", "Date Filed": "2025-01-28", "Last Update": "2025-02-03", "Status": "Pending", "Case Link": "[Link](https://turn0search21)"},
    {"Case Number": "1:25-cv-01144", "Case Title": "New York et al. v. Trump et al.", "Court": "Southern District of New York", "Date Filed": "2025-02-07", "Last Update": "2025-02-14", "Status": "Pending", "Case Link": "[Link](https://turn0search22)"},
    {"Case Number": "1:25-cv-00001", "Case Title": "AIDS Vaccine Advocacy Coalition v. Department of State", "Court": "District of Columbia", "Date Filed": "2025-01-20", "Last Update": "2025-02-27", "Status": "Pending", "Case Link": "[Link](https://turn0news13)"},
    {"Case Number": "1:25-cv-00333", "Case Title": "National Association of Diversity Officers in Higher Education et al. v. Trump et al.", "Court": "District of Maryland", "Date Filed": "2025-02-01", "Last Update": "2025-02-21", "Status": "Preliminary Injunction Granted", "Case Link": "[Link](https://turn0search1)"},
    {"Case Number": "1:25-cv-00471", "Case Title": "National Urban League v. Trump", "Court": "District of Columbia", "Date Filed": "2025-02-19", "Last Update": "2025-02-28", "Status": "Pending", "Case Link": "[Link](https://turn0search1)"}
])

# Function to fetch latest case updates
def fetch_case_updates(case_number):
    search_url = f"https://www.courtlistener.com/?q={case_number}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract latest case status (example logic, adjust based on page structure)
        status_element = soup.find('div', class_='status')
        last_update_element = soup.find('div', class_='last-update')
        
        latest_status = status_element.text.strip() if status_element else "Unknown"
        last_update = last_update_element.text.strip() if last_update_element else "Unknown"
        
        return latest_status, last_update
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch updates for case {case_number}: {e}")
        return "Error", "N/A"

# Function to update case statuses
def update_cases():
    for index, row in litigation_cases.iterrows():
        latest_status, last_update = fetch_case_updates(row["Case Number"])
        litigation_cases.at[index, "Status"] = latest_status
        litigation_cases.at[index, "Last Update"] = last_update

# Streamlit UI
st.set_page_config(page_title="Federal Litigation Tracker", layout="wide")
st.title("Federal Litigation Tracker")
st.write("Monitor federal lawsuits, key rulings, and policy changes affecting grant programs.")

# Auto-refresh every 30 minutes to fetch latest updates
if "last_refresh" not in st.session_state or time.time() - st.session_state["last_refresh"] > 1800:
    update_cases()
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
