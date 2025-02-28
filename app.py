import sys
import requests
import streamlit as st
import pandas as pd
import time
from datetime import datetime
from bs4 import BeautifulSoup

# Load GovInfo API key from Streamlit secrets
API_KEY = st.secrets["GOVINFO_API_KEY"] if "GOVINFO_API_KEY" in st.secrets else None
if not API_KEY:
    st.error("Missing or invalid GovInfo API key. Please add a valid key to your Streamlit secrets.")
    sys.exit()

# Function to fetch litigation data from GovInfo API with retry logic
def fetch_govinfo_data(start_date):
    url = f"https://api.govinfo.gov/collections/USCOURTS/{start_date}?api_key={API_KEY}"
    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('packages', [])
        except requests.exceptions.HTTPError as http_err:
            st.warning(f"GovInfo API attempt {attempt + 1} failed: {http_err}")
            time.sleep(2 ** attempt)  # Exponential backoff
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch litigation data from GovInfo: {e}")
            return []
    st.error("GovInfo API is currently unavailable. Using alternative data sources.")
    return []

# Function to scrape RECAP Archive with session-based access
def scrape_recap_data(case_number):
    search_url = f"https://www.courtlistener.com/recap/?q={case_number}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://www.google.com",
    }
    session = requests.Session()
    session.headers.update(headers)
    
    try:
        time.sleep(2)  # Delay to avoid bot detection
        response = session.get(search_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        case_title = soup.find('h3').text if soup.find('h3') else "N/A"
        case_court = soup.find('div', class_='court').text if soup.find('div', class_='court') else "N/A"
        case_status = soup.find('div', class_='status').text if soup.find('div', class_='status') else "Unknown"
        case_link = response.url
        
        return {
            'Case Number': case_number,
            'Case Title': case_title,
            'Court': case_court,
            'Status': case_status,
            'Case Link': f"[Link]({case_link})"
        }
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch RECAP data: {e}")
        return {}

# Function to fetch and display grant policy updates
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

start_date = '2024-01-20'
case_number = 'specific_case_number'
case_data = fetch_govinfo_data(start_date)
case_df = pd.DataFrame(case_data)

# Auto-refresh every 30 minutes
if "last_refresh" not in st.session_state or time.time() - st.session_state["last_refresh"] > 1800:
    st.session_state["case_data"] = case_df
    st.session_state["last_refresh"] = time.time()
else:
    case_df = st.session_state["case_data"]

# Display Litigation Cases
st.subheader("Litigation Cases")
if case_df.empty:
    st.write("No litigation cases available at this time.")
st.dataframe(case_df)

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
