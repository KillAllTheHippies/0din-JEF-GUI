# How to Run the ChatGPT Archive Search Tool

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

### 3. Open in Browser
```
http://localhost:5000
```

## Initial Setup

### Configure Archive Path
1. Click **Settings** in the top navigation
2. Set **Root Archive Folder** to your ChatGPT markdown files directory
3. Click **Validate** to verify the path
4. Click **Save Settings**

Example path: `C:\Users\YourName\Documents\ChatGPT_Archive`

### Basic Usage
1. Enter search terms in the main search box
2. Choose **ALL** (AND logic) or **ANY** (OR logic)
3. Click **Search**
4. Use the file tree to include/exclude folders
5. Export results as CSV or JSON

## Troubleshooting

**"Module not found" errors:**
```bash
pip install -r requirements.txt
```

**Port already in use:**
- Change port in `app.py` line 1260: `app.run(port=5001)`

**Archive not found:**
- Use Settings to set correct archive path
- Ensure folder contains .md files

**JEF integration issues:**
- Set JEF path in settings if you have JEF installed
- JEF is optional - app works without it

## Expected Output
```
Starting ChatGPT Archive Search Tool...
Archive path: C:\path\to\your\archive
JEF integration: Disabled
Server: http://0.0.0.0:5000
 * Running on http://127.0.0.1:5000
```

## File Format
Your markdown files should have this structure:
```markdown
---
aliases: "Conversation Title"
conversation_id: abc123
create_time: 28/11/2024 at 04:02
---

# Title: Conversation Title

### User, on 28/11/2024 at 04:02;
> User message

#### Assistant, on 28/11/2024 at 04:02;
>> Assistant response
```

## JEF Integration (Optional)

JEF (Jailbreak Evaluation Framework) provides security analysis of ChatGPT conversations.

### Installing JEF
1. **Clone JEF repository:**
   ```bash
   git clone https://github.com/0din-ai/0din-JEF.git
   cd 0din-JEF
   pip install -e .
   ```

2. **Note the installation path** (example: `C:\Users\YourName\0din-JEF` or `/home/user/0din-JEF`)

**Important**: The application expects to import JEF modules directly, so ensure the JEF installation is complete and working.

### Configure JEF in Application
1. Go to **Settings** in the web interface
2. Find **JEF Integration** section
3. Set **JEF Path** to your JEF installation directory
4. Enable **JEF Integration**
5. Click **Save Settings**

### Using JEF Analysis
1. Perform a search to get results
2. Click on a file result to select it
3. Choose analysis type (Tiananmen, Nerve Agent, etc.)
4. Click **Run Analysis** for single file or **Batch Analysis** for all results
5. View security analysis scores in the results

### JEF Troubleshooting
**JEF not found:**
- Verify the JEF path points to the correct directory
- Ensure JEF dependencies are installed: `pip install -e .` in JEF directory

**Analysis fails:**
- Check that JEF modules are properly installed
- Verify file permissions in JEF directory

---

For detailed documentation, see the `docs/` folder.