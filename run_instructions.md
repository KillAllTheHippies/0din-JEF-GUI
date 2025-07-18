# How to Run the ChatGPT Archive Search Tool

## 🚀 Quick Start

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Application:**
    ```bash
    python app.py
    ```

3.  **Open in Browser:**
    Navigate to `http://localhost:5000`

## ⚙️ Initial Setup

### Configure Archive Path

1.  Click the **Settings** button in the top navigation bar.
2.  In the **Archive Settings** section, set the **Root Archive Folder** to the directory where your ChatGPT markdown files are stored.
3.  Click **Validate** to ensure the path is correct.
4.  Click **Save Settings** at the bottom of the page.

**Example Path:** `C:\Users\YourName\Documents\ChatGPT_Archive`

### Basic Usage

1.  Enter your search query in the main search bar.
2.  Choose the search mode: **ALL** (for AND logic) or **ANY** (for OR logic).
3.  Click the **Search** button.
4.  Use the interactive file tree on the left to include or exclude specific folders from your search.
5.  Export your search results to CSV or JSON using the **Export** buttons.

## 🔬 JEF Integration (Optional)

JEF (Jailbreak Evaluation Framework) provides advanced security analysis of ChatGPT conversations.

### Installing JEF

1.  **Clone the JEF repository:**
    ```bash
    git clone https://github.com/0din-ai/0din-JEF.git
    ```
    **Note:** You do not need to install it, just clone it.

2.  **Note the path** to the cloned repository (e.g., `C:\Users\YourName\0din-JEF`). This is the path you will use in the application settings.

### Configure JEF in the Application

1.  Go to **Settings** in the web interface.
2.  Find the **JEF Integration** section.
3.  Set the **JEF Path** to the directory where you cloned the `0din-JEF` repository.
4.  Enable the **JEF Integration** toggle.
5.  Click **Save Settings**.

### Using JEF Analysis

1.  After performing a search, click on a file in the results list to select it.
2.  Choose an analysis type from the dropdown menu (e.g., Tiananmen, Nerve Agent).
3.  Click **Run Analysis** for a single file or **Batch Analysis** to analyze all files in the current search results.
4.  View the security analysis scores in the results table.

## 🔧 Troubleshooting

-   **"Module not found" errors:** Ensure you have installed all dependencies by running `pip install -r requirements.txt`.
-   **Port already in use:** You can change the port by editing `app.py` around line 1260: `app.run(port=5001)`.
-   **Archive not found:** Double-check the **Root Archive Folder** path in the settings. Make sure the folder contains `.md` files.
-   **JEF not found:** Verify that the **JEF Path** in the settings points to the correct directory where you cloned the `0din-JEF` repository.

---

For more detailed documentation, please refer to the files in the `docs/` folder.
