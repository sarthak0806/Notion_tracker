import streamlit as st
from datetime import datetime, timedelta
import requests

# --- Utility Functions ---

def fetch_block_children(block_id, headers):
    """Fetch all child blocks for a given Notion block ID."""
    BASE_URL = "https://api.notion.com/v1"
    url = f"{BASE_URL}/blocks/{block_id}/children"
    children = []
    next_cursor = None

    while True:
        params = {"start_cursor": next_cursor} if next_cursor else {}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        children.extend(data.get("results", []))
        next_cursor = data.get("next_cursor")
        if not next_cursor:
            break
    return children

def get_latest_edited_time_recursive(block_id, headers):
    """Recursively find the latest edited time for a block and all its descendants."""
    children = fetch_block_children(block_id, headers)
    latest_time = None

    for block in children:
        block_last_edited = block.get('last_edited_time')
        block_latest = None

        if block.get('has_children', False):
            block_latest = get_latest_edited_time_recursive(block['id'], headers)

        times_to_compare = []
        if block_last_edited:
            times_to_compare.append(datetime.fromisoformat(block_last_edited.replace('Z', '+00:00')))
        if block_latest:
            times_to_compare.append(datetime.fromisoformat(block_latest.replace('Z', '+00:00')))

        if times_to_compare:
            max_time = max(times_to_compare)
            if latest_time is None or max_time > latest_time:
                latest_time = max_time

    return latest_time.isoformat().replace('+00:00', 'Z') if latest_time else None

def convert_to_ist(utc_time_str):
    """Convert ISO 8601 UTC time string to IST formatted string."""
    if not utc_time_str:
        return "Unknown"
    utc_time = datetime.fromisoformat(utc_time_str.replace('Z', '+00:00'))
    ist_time = utc_time + timedelta(hours=5, minutes=30)
    return ist_time.strftime('%Y-%m-%d %H:%M:%S IST')

def get_subpages_latest_only(block_id, headers):
    """Return a list of dicts for each subpage and its latest edited time in IST."""
    children = fetch_block_children(block_id, headers)
    results = []
    for block in children:
        block_type = block.get("type")
        if block_type == "child_page":
            title = block[block_type].get("title", "Untitled Page")
            latest_time_utc = get_latest_edited_time_recursive(block["id"], headers)
            latest_time_ist = convert_to_ist(latest_time_utc)
            results.append({
                "Page Name": title,
                "Page ID": block['id'],
                "Latest Edited (IST)": latest_time_ist
            })
    return results

# --- Streamlit UI ---
st.title('Notion Subpages Latest Edited Time (IST)')
st.caption('Shows each subpage and the most recent edit time among all its nested children, in Indian Standard Time.')

with st.form("notion_form"):
    api_key = st.text_input("Notion API Key", type="password")
    page_id = st.text_input("Notion Page ID")
    submit = st.form_submit_button("Fetch Subpages")

if submit:
    if not api_key or not page_id:
        st.warning("Please enter both API Key and Page ID.")
    else:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        try:
            data = get_subpages_latest_only(page_id, headers)
            if data:
                st.dataframe(data)
            else:
                st.info("No subpages found for this page.")
        except Exception as e:
            st.error(f"Error: {e}")
