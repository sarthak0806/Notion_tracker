import streamlit as st
from datetime import datetime, timedelta
import requests
import asyncio
import aiohttp
from functools import lru_cache

# --- Configuration ---
MAX_CONCURRENT_REQUESTS = 5  # Respect Notion API rate limits
REQUEST_TIMEOUT = 30

# --- Async Utility Functions ---

async def fetch_block_children_async(session, block_id, headers):
    # """Asynchronously fetch all child blocks for a given Notion block ID."""
    BASE_URL = "https://api.notion.com/v1"
    url = f"{BASE_URL}/blocks/{block_id}/children"
    children = []
    next_cursor = None

    while True:
        params = {"start_cursor": next_cursor} if next_cursor else {}
        try:
            async with session.get(url, headers=headers, params=params, timeout=REQUEST_TIMEOUT) as response:
                response.raise_for_status()
                data = await response.json()
                children.extend(data.get("results", []))
                next_cursor = data.get("next_cursor")
                if not next_cursor:
                    break
        except Exception as e:
            print(f"Error fetching children for block {block_id}: {e}")
            break

    return children

async def get_latest_edited_time_recursive_async(session, block_id, headers):
    # """Recursively find the latest edited time for a block and all its descendants (async)."""
    children = await fetch_block_children_async(session, block_id, headers)
    latest_time = None

    # Prepare tasks for all child blocks that have children (concurrent recursion)
    child_tasks = []
    for block in children:
        block_last_edited = block.get('last_edited_time')

        # Update latest_time with current block's timestamp
        if block_last_edited:
            block_time = datetime.fromisoformat(block_last_edited.replace('Z', '+00:00'))
            if latest_time is None or block_time > latest_time:
                latest_time = block_time

        # Recurse if block has children
        if block.get('has_children', False):
            task = get_latest_edited_time_recursive_async(session, block['id'], headers)
            child_tasks.append(task)

    # Gather all recursive results
    if child_tasks:
        child_results = await asyncio.gather(*child_tasks, return_exceptions=True)
        for child_latest in child_results:
            if isinstance(child_latest, str) and child_latest:
                child_time = datetime.fromisoformat(child_latest.replace('Z', '+00:00'))
                if latest_time is None or child_time > latest_time:
                    latest_time = child_time

    return latest_time.isoformat().replace('+00:00', 'Z') if latest_time else None

@lru_cache(maxsize=1000)
def convert_to_ist(utc_time_str):
    """Convert ISO 8601 UTC time string to IST formatted string."""
    if not utc_time_str:
        return "Unknown"
    utc_time = datetime.fromisoformat(utc_time_str.replace('Z', '+00:00'))
    ist_time = utc_time + timedelta(hours=5, minutes=30)
    return ist_time.strftime('%Y-%m-%d %H:%M:%S IST')

async def get_subpages_latest_async(block_id, headers):
    # """Async version: return a list of dicts for each subpage and its latest edited time in IST."""
    connector = aiohttp.TCPConnector(limit=MAX_CONCURRENT_REQUESTS)
    timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        children = await fetch_block_children_async(session, block_id, headers)

        subpage_tasks = []
        subpage_info = []

        for block in children:
            block_type = block.get("type")
            if block_type == "child_page":
                title = block[block_type].get("title", "Untitled Page")
                subpage_info.append({
                    "title": title,
                    "id": block['id']
                })
                # Task for recursive timestamp finding
                task = get_latest_edited_time_recursive_async(session, block["id"], headers)
                subpage_tasks.append(task)

        # Execute all subpage processing concurrently
        latest_times = await asyncio.gather(*subpage_tasks, return_exceptions=True) if subpage_tasks else []

        # Combine results
        results = []
        for i, page_info in enumerate(subpage_info):
            latest_time_utc = latest_times[i] if i < len(latest_times) and not isinstance(latest_times[i], Exception) else None
            latest_time_ist = convert_to_ist(latest_time_utc)
            results.append({
                "Page Name": page_info["title"],
                "Page ID": page_info["id"],
                "Latest Edited (IST)": latest_time_ist
            })

        return results

def run_async_function(coro):
    # """Run async function in sync context."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

# --- Streamlit UI ---
st.title('⚡ Notion Subpages Latest Edited Time (IST)')
st.caption('Shows each subpage and the most recent edit time among all its nested children, in Indian Standard Time. (Async optimized)')

with st.form("notion_form"):
    api_key = st.text_input("Notion API Key", type="password")
    page_id = st.text_input("Notion Page ID")
    submit = st.form_submit_button("🔍 Fetch Subpages")

if submit:
    if not api_key or not page_id:
        st.warning("Please enter both API Key and Page ID.")
    else:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        import time
        start_time = time.time()
        try:
            with st.spinner("Analyzing all nested children for latest edits (async)..."):
                data = run_async_function(get_subpages_latest_async(page_id, headers))
            end_time = time.time()
            execution_time = end_time - start_time

            if data:
                st.success(f"✅ Analyzed {len(data)} subpages in {execution_time:.2f} seconds")
                st.dataframe(data, use_container_width=True)
                # CSV download
                csv_data = "Page Name,Page ID,Latest Edited (IST)\n"
                for row in data:
                    csv_data += f'"{row["Page Name"]}",{row["Page ID"]},{row["Latest Edited (IST)"]}\n'
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv_data,
                    file_name=f"notion_subpages_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No subpages found for this page.")

        except ImportError:
            st.error("aiohttp not installed. Please run: pip install aiohttp")
        except Exception as e:
            st.error(f"Error: {e}")
