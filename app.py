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

# Function to fetch litigation data from GovInfo API
def fetch_govinfo_data(start_date):
    url = f"https://api.govinfo.gov/collections/USCOURTS/{start_date}?api_key={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('packages', [])
    except requests.exceptions.HTTPError as http_err:
        st.error(f"GovInfo API error: {http_err}")
        return []
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch litigation data from GovInfo: {e}")
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

# Function to scrape PACER data with headers
def scrape_pacer_data(case_number):
    search_url = f"https://www.pacermonitor.com/search/case?q={case_number}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://www.google.com",
    }
    try:
        time.sleep(2)  # Delay to avoid bot detection
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        case_title = soup.find('h1').text if soup.find('h1') else "N/A"
        case_court = soup.find('span', class_='court').text if soup.find('span', class_='court') else "N/A"
        case_status = soup.find('div', class_='status').text if soup.find('div', class_='status') else "Unknown"
        case_link = response.url
        
        return {
            'Case Number': case_number,
            'PACER Case Title': case_title,
            'PACER Court': case_court,
            'PACER Status': case_status,
            'PACER Link': f"[Link]({case_link})"
        }
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch PACER data: {e}")
        return {}

# Function to integrate multiple data sources
def integrate_case_data(start_date, case_number):
    govinfo_data = fetch_govinfo_data(start_date)
    recap_data = scrape_recap_data(case_number)
    pacer_data = scrape_pacer_data(case_number)
    combined_data = []
    
    for case in govinfo_data:
        gov_case_number = case.get('case_number', 'Unknown')
        
        if gov_case_number == case_number:
            combined_case = {
                'Case Number': gov_case_number,
                'Case Title': case.get('title', 'Unknown Title'),
                'Court': case.get('court', 'Unknown Court'),
                'Date Filed': case.get('date', 'N/A'),
                'Last Update': case.get('last_modified', 'N/A'),
                'Status': "Pending",  
                'Key Rulings': "N/A",
                'Impact on Federal Grants': "Unknown",
                'Case Link': recap_data.get('Case Link', 'N/A')
            }
            combined_case.update(recap_data)
            combined_case.update(pacer_data)
            combined_data.append(combined_case)
    
    return combined_data

# Streamlit UI
st.set_page_config(page_title="Federal Litigation Tracker", layout="wide")
st.title("Federal Litigation Tracker")
st.write("Monitor federal lawsuits, key rulings, and policy changes affecting grant programs.")

start_date = '2024-01-20'
case_number = 'specific_case_number'
case_data = integrate_case_data(start_date, case_number)
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

# Alerts & Notifications Section
st.sidebar.header("Alerts & Notifications")
st.sidebar.write("Coming soon: Email & Slack notifications for case updates.")
st.sidebar.button("Subscribe to Alerts")
