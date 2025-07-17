# ChatGPT Archive Search Tool

A modern, feature-rich web application for searching through your ChatGPT conversation archive with advanced filtering, folder management, and export capabilities.

![ChatGPT Archive Search Tool](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

### 🔍 Advanced Search
- **Boolean Logic**: ALL/ANY term matching with complex queries
- **Exact Phrase Matching**: Use quotes for precise searches
- **Exclusion Filters**: Exclude unwanted terms from results
- **Case Sensitivity**: Toggle case-sensitive search
- **Content Scope**: Search in titles, content, or all text
- **Date Range Filtering**: Limit results by creation/modification date

### 📁 File Explorer & Management
- **Interactive File Tree**: Visual folder structure with expand/collapse
- **Right-Click Context Menu**: Comprehensive folder operations
- **Include/Exclude Folders**: Focus searches on specific directories
- **Recursive Operations**: Apply actions to entire folder trees
- **Ignore Lists**: Hide unwanted folders from view
- **Visual Status Indicators**: Color-coded folder states

### 📊 Export & Results
- **Multiple Export Formats**: CSV (full/paths-only) and JSON
- **Path Options**: Relative or absolute file paths
- **Rich Metadata**: File sizes, dates, match counts, conversation IDs
- **Real-time Results**: Live search as you type
- **Result Statistics**: Search timing and match counts

### 🎨 Modern UI/UX
- **Dark/Light Themes**: Auto-detects browser preference
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Smooth Animations**: Professional micro-interactions
- **Modern Typography**: Clean, readable interface
- **Accessibility**: WCAG compliant color contrasts

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- ChatGPT conversation exports in markdown format
- Web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone or download** the application files:
   ```
   chatgpt-search-tool/
   ├── app.py
   ├── requirements.txt
   ├── templates/
   │   ├── base.html
   │   └── index.html
   └── README.md
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Organize your ChatGPT archive**:
   ```
   ChatGPT chats/
   └── ChatGPT chats/
       ├── 2022/
       │   └── 12/
       │       └── 2022-12-23 - Example Chat.md
       ├── 2023/
       │   ├── 01/
       │   └── 02/
       └── 2024/
           └── 11/
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## 📖 User Guide

### Basic Search
1. Enter search terms in the main search box
2. Choose between ALL (AND) or ANY (OR) logic
3. Press Enter or click Search
4. View results with match counts and metadata

### Advanced Filtering
- **Exclude Terms**: Add terms to exclude from results
- **Search Scope**: Choose titles only, content only, or all
- **Date Range**: Set from/to dates to limit results
- **Case Sensitivity**: Toggle for exact case matching

### File Explorer Operations

#### Folder Management
- **Click arrows** (▶/▼) to expand/collapse folders
- **Right-click folders** for context menu options:
  - Include/Exclude this folder
  - Include/Exclude folder + subfolders
  - Expand/Collapse tree from here
  - Add to ignore list
  - Copy path to clipboard

#### Visual Indicators
- 🟢 **Green folders**: Included in search
- 🔴 **Red folders**: Excluded from search
- **Normal folders**: No filter applied
- **Hidden folders**: Added to ignore list

### Export Options
1. **Export Full CSV**: Complete data with all metadata
2. **Export Paths Only**: Simple list of file paths
3. **Export JSON**: Detailed format with search context

For each export, choose:
- **Relative paths**: `2024/11/filename.md`
- **Full paths**: `C:\full\path\to\filename.md`

### Theme Switching
- **Auto-detection**: Uses your browser's dark/light preference
- **Manual toggle**: Click the moon/sun icon in the header
- **Persistent**: Remembers your choice across sessions

## 🛠️ Technical Details

### Architecture
- **Backend**: Flask web framework with Python
- **Frontend**: Bootstrap 5, jQuery, modern CSS
- **File Processing**: YAML frontmatter parsing
- **Search Engine**: Custom implementation with boolean logic
- **Export**: CSV and JSON generation with metadata

### File Format Support
The application works with ChatGPT conversation exports in this format:
```markdown
---
nexus: nexus-ai-chat-importer
provider: chatgpt
aliases: "Conversation Title"
conversation_id: abc123-def456
create_time: 28/11/2024 at 04:02
update_time: 28/11/2024 at 04:06
---

# Title: Conversation Title

### User, on 28/11/2024 at 04:02;
> User message content

#### Assistant, on 28/11/2024 at 04:02;
>> Assistant response content
```

### Performance Considerations
- **File Tree Depth**: Limited to 3 levels by default
- **Search Debouncing**: 500ms delay for live search
- **Memory Usage**: Efficient file processing
- **Large Archives**: Handles thousands of files

## 🔧 Configuration

### Changing the Archive Path
Edit `app.py` line 286:
```python
search_engine = ChatSearchEngine("your/custom/path")
```

### Adjusting File Tree Depth
Edit `app.py` in the `build_tree` function:
```python
def build_tree(path, max_depth=3, current_depth=0):
```

### Customizing the Port
Edit `app.py` line 367:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change port here
```

## 🐛 Troubleshooting

### Common Issues

#### "No results found" with valid search terms
- Check that your archive path is correct
- Verify file permissions
- Ensure markdown files have proper format

#### File tree not loading
- Check browser console (F12) for JavaScript errors
- Verify the `/api/file-tree` endpoint returns data
- Check Flask console for Python errors

#### Export downloads empty files
- Ensure you have search results before exporting
- Check browser's download settings
- Verify write permissions for temporary files

#### Theme not switching
- Clear browser cache and localStorage
- Check browser console for JavaScript errors
- Ensure the theme toggle button is clickable

### Debug Mode
Run with debug output:
```bash
python app.py
```
Check the console for detailed logging information.

### Browser Compatibility
- **Chrome**: Full support
- **Firefox**: Full support
- **Safari**: Full support
- **Edge**: Full support
- **Mobile browsers**: Responsive design supported

## 📝 API Reference

### Search Endpoint
```
POST /search
Content-Type: application/json

{
  "terms": "search terms",
  "exclude": "excluded terms",
  "mode": "ALL|ANY",
  "searchIn": "all|title|content",
  "caseSensitive": true|false,
  "dateFrom": "YYYY-MM-DD",
  "dateTo": "YYYY-MM-DD",
  "includedFolders": ["folder1", "folder2"],
  "excludedFolders": ["folder3"]
}
```

### File Tree Endpoint
```
GET /api/file-tree

Returns: JSON tree structure of the archive
```

### Export Endpoints
```
GET /export/csv?[search_params]
GET /export/csv-paths?[search_params]
GET /export/json?[search_params]
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Maintain consistent indentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Bootstrap**: For the responsive UI framework
- **Font Awesome**: For the beautiful icons
- **jQuery**: For DOM manipulation and AJAX
- **Flask**: For the lightweight web framework
- **PyYAML**: For YAML frontmatter parsing

## 📞 Support

For issues, questions, or feature requests:
1. Check the troubleshooting section
2. Search existing issues
3. Create a new issue with detailed information
4. Include your Python version, browser, and error messages

---

**Made with ❤️ for the ChatGPT community**