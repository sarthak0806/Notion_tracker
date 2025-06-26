import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import pytz

# Set time zone to Indian Standard Time (IST)
ist = pytz.timezone('Asia/Kolkata')

# Function to get text from rich text fields in Notion
def get_text_from_rich_text(field):
    return ''.join([t.get('plain_text', '') for t in field or []])

# Function to fetch tasks from a given Notion database
def fetch_tasks(database_id, user, headers):
    url = f"https://api.notion.com/v1/databases/{database_id.strip()}/query"
    res = requests.post(url, headers=headers)

    # Handle possible errors from Notion API
    if res.status_code == 404:
        st.error(f"❌ Database not found for user {user}: {database_id}")
        return []
    if res.status_code != 200:
        st.error(f"⚠️ Error {res.status_code} for {user}'s database")
        return []

    data = res.json()
    results = []

    # Process each task in the returned data
    for row in data.get('results', []):
        props = row.get("properties", {})
        task = get_text_from_rich_text(props.get("Task name", {}).get("title", []))
        people = props.get("Assignee", {}).get("people", [])
        assignee = people[0].get("name", "N/A") if people else "N/A"

        # Parse due date and last edited time
        due_raw = None
        due_prop = props.get("Due date")
        if due_prop and isinstance(due_prop.get("date"), dict):
            due_raw = due_prop["date"].get("start")

        due_date = datetime.fromisoformat(due_raw).astimezone(ist).strftime('%Y-%m-%d') if due_raw else "N/A"
        last_edit = datetime.fromisoformat(row['last_edited_time'].replace('Z', '+00:00')).astimezone(ist)
        last_edit_str = last_edit.strftime('%Y-%m-%d %H:%M:%S')

        # Append the task information to the results list
        results.append({
            "User": user,
            "Task Name": task,
            "Assignee": assignee,
            "Due Date": due_date,
            "Last Updated (IST)": last_edit_str,
        })

    return results

# Main function to handle the Streamlit interface and process tasks
def main():
    # App title
    st.title("📊 Notion Task Tracker by User")

    # Input for API key and CSV file
    api_key = st.text_input("🔐 Enter your Notion API key", type="password")
    csv_file = st.file_uploader("📁 Upload CSV with `user` and `database_id` columns", type="csv")

    # Button to fetch tasks
    if st.button("🚀 Fetch Tasks"):
        if not api_key or not csv_file:
            st.warning("Please provide both API key and CSV file.")
        else:
            # Set up headers for the Notion API request
            headers = {
                'Authorization': f'Bearer {api_key.strip()}',
                'Notion-Version': '2022-06-28',
                'Content-Type': 'application/json',
            }

            # Read the CSV file to get users and their associated Notion database IDs
            db_df = pd.read_csv(csv_file)
            all_tasks = []

            # Fetch tasks for each user/database pair
            for _, row in db_df.iterrows():
                user = str(row['user']).strip()
                db_id = str(row['database_id']).strip()
                st.write(f"🔄 Fetching for `{user}` → `{db_id}`")
                tasks = fetch_tasks(db_id, user, headers)
                all_tasks.extend(tasks)

            # Display results if tasks are fetched
            if all_tasks:
                df = pd.DataFrame(all_tasks)
                st.success(f"✅ Total Tasks Loaded: {len(df)}")
                st.dataframe(df)

                # Provide option to download the data as a CSV file
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download All Tasks", csv, "all_tasks.csv", "text/csv")
            else:
                st.warning("No tasks retrieved from any user database.")

# Run the Streamlit app
if __name__ == "__main__":
    main()
