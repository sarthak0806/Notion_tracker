Here’s a revised and professional README for your repository [sarthak0806/Notion_tracker](https://github.com/sarthak0806/Notion_tracker), including a prominent live demo link and reflecting your latest features and structure[1]:

# Notion Subpages Latest Edited Time (IST)

A simple Streamlit app to view each subpage of a Notion page and display the most recent edit time (in Indian Standard Time) among all its nested children (pages and databases).

## 🚀 Live Demo

**Try it instantly:**  
👉 [https://notiontracker.streamlit.app](https://notiontracker.streamlit.app)

## Features

- **Secure:** No API keys or secrets are stored; users provide their own Notion API key and Page ID.
- **Easy to use:** Enter your credentials and view results in a clean, sortable table.
- **Time zone conversion:** All times are shown in IST (Indian Standard Time).
- **No installation required:** Deployable on [Streamlit Cloud](https://streamlit.io/cloud) or run locally.

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/sarthak0806/Notion_tracker.git
cd Notion_tracker
```

### 2. Install Requirements

```bash
pip install -r requirement.txt
```

### 3. Run the App Locally

```bash
streamlit run final_check_2.py
```

## Usage

1. **Obtain your Notion Integration Token (API Key):**  
   [Create an integration](https://www.notion.so/my-integrations) and copy the secret.
2. **Share your Notion page with the integration** (so it has access).
3. **Copy the Notion Page ID** from the URL of your page.
4. **Enter your API Key and Page ID** in the app and click "Fetch Subpages".
5. **View the table** of subpages and their latest edited times (in IST).

## Security

- **No secrets are stored or logged.**
- Each user provides their own Notion API key and Page ID.
- **Never share your API key publicly.**

## Example Table

| Page Name                 | Page ID                                   | Latest Edited (IST)     |
|---------------------------|-------------------------------------------|-------------------------|
| Sarthak Modanwal Worksheet| 20bdcb16-6c13-806a-bfc9-e910f6c3f2b7      | 2025-07-02 13:40:00 IST |
| Tvisha WorkSheet          | 223dcb16-6c13-8031-889f-f31f0a937d57      | 2025-07-01 12:08:00 IST |

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)

**Live Demo:** [https://notiontracker.streamlit.app](https://notiontracker.streamlit.app)

If you want a badge or screenshot added, just let me know![1]

[1] https://github.com/sarthak0806/Notion_tracker
