
# Notion Tracker Pro

Welcome to **Notion Tracker Pro** — a powerful Streamlit app designed to help you track tasks across multiple Notion databases with ease. Fetch, view, and download tasks by user with just a few clicks!

## Features

- Fetch tasks from different Notion databases for multiple users.
- View task data in an organized, tabular format, with details like Task Name, Assignee, Due Date, and Last Updated timestamp.
- Download task data as a CSV file for further analysis.

## Requirements

Before running the app, ensure you have the following libraries installed:

### Install Dependencies:

1. **Streamlit**: For building the interactive web application.
2. **Requests**: To make HTTP requests to the Notion API.
3. **Pandas**: For handling and displaying data in tabular format.
4. **Datetime** and **pytz**: For handling time zones and formatting timestamps.

### Install Libraries:

To install the necessary libraries, run:

```bash
pip install streamlit requests pandas pytz
````

## How to Run

### Step 1: Set Up Your Notion API Key

To fetch data from Notion, you'll need a Notion integration API key. Follow these steps to get your API key:

1. Go to [Notion Developers](https://www.notion.so/my-integrations).
2. Create a new integration and generate an API key.
3. Copy the API key for use in the app.

### Step 2: Prepare the CSV File

The app requires a CSV file containing two columns:

* `user`: The name or identifier of the user.
* `database_id`: The ID of the Notion database to fetch tasks from.

Sample CSV structure:

```
user,database_id
Alice,xxxxxx
Bob,yyyyyy
```

### Step 3: Run the Streamlit App

1. Save the provided Python script to a file (e.g., `notion_tracker_pro.py`).
2. Open a terminal and navigate to the directory containing the script.
3. Run the Streamlit app by executing the following command:

```bash
streamlit run notion_tracker_pro.py
```

### Step 4: Enter API Key and Upload CSV File

1. Open the app in your browser (it will open automatically).
2. Enter your Notion API key in the provided input box.
3. Upload the CSV file with user and database IDs.
4. Click "Fetch Tasks" to retrieve the task data for all users.

The app will display the task data in a table, and you can download it as a CSV file.

## Functionality

* **API Key Input**: Enter your Notion API key to authenticate and fetch data from your Notion workspace.
* **CSV Upload**: Upload a CSV file containing `user` and `database_id` columns for each user and their associated Notion databases.
* **Fetch Tasks**: Click the button to fetch the tasks associated with each user’s database.
* **Data Table**: View tasks in an easy-to-read table format showing Task Name, Assignee, Due Date, and Last Updated timestamp.
* **Download CSV**: Download the task data as a CSV file.

## Important Notes

* Ensure that the Notion databases you are accessing are shared with your integration for proper access permissions.
* The app fetches tasks based on the database and user provided in the CSV file. If the database ID is invalid or the user does not have tasks, the app will notify you.
* The time in the "Last Updated" column is adjusted to Indian Standard Time (IST).



