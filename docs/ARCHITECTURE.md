# Architecture Documentation

This document provides a comprehensive overview of the ChatGPT Archive Search Tool's architecture, design decisions, and implementation details.

## 🏗️ System Overview

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                        Web Browser                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Search UI     │  │  File Explorer  │  │  Content Viewer │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ HTTP/AJAX
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Flask Web Server                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   API Routes    │  │  Template Engine│  │  Static Assets  │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ Function Calls
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Core Application Layer                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ ChatSearchEngine│  │  File Processor │  │  Export Manager │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ Optional Integration
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    JEF Analysis Framework                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Tiananmen     │  │   Nerve Agent   │  │   Copyright     │ │
│  │   Analysis      │  │   Detection     │  │   Detection     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ File System Access
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      File System Layer                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ ChatGPT Archive │  │   Temp Files    │  │   Log Files     │ │
│  │   Directory     │  │   (Exports)     │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 🧩 Component Architecture

### Frontend Components

#### 1. Search Interface
**Location**: `templates/index.html` (lines 82-142)
**Responsibilities**:
- User input collection and validation
- Search mode selection (ALL/ANY)
- Advanced filtering options
- Real-time search suggestions

**Key Features**:
- Debounced search input (500ms delay)
- Boolean logic selection
- Date range filtering
- Case sensitivity toggle

#### 2. File Explorer
**Location**: `templates/index.html` (lines 4-38)
**Responsibilities**:
- Hierarchical directory visualization
- Folder include/exclude management
- File tree navigation
- Context menu operations

**Data Flow**:
```
User Action → JavaScript Event → AJAX Request → Flask Route → File System → JSON Response → DOM Update
```

#### 3. Content Viewer
**Location**: `templates/index.html` (lines 40-77)
**Responsibilities**:
- Markdown file content display
- Syntax highlighting
- Raw/rendered view toggle
- Content copying functionality

### Backend Components

#### 1. Flask Application (`app.py`)
**Core Routes**:
- `/` - Main interface
- `/search` - Search API endpoint
- `/api/file-tree` - File structure API
- `/file-content/<path>` - File content API
- `/export/*` - Export functionality
- `/jef/*` - JEF integration endpoints

**Middleware**:
- Request validation
- Error handling
- Security headers
- CORS handling (if needed)

#### 2. ChatSearchEngine Class
**Location**: `app.py` (lines 32-310)

**Core Methods**:
```python
class ChatSearchEngine:
    def __init__(base_path: str)           # Initialize with archive path
    def extract_metadata(file_path: Path)  # Parse YAML frontmatter
    def search_in_content(content: str)    # Content matching logic
    def search(query_data: dict)           # Main search orchestration
```

**Search Algorithm**:
1. **File Discovery**: Recursively scan archive directory
2. **Metadata Extraction**: Parse YAML frontmatter and file stats
3. **Content Processing**: Extract searchable text content
4. **Term Matching**: Apply boolean logic (ALL/ANY)
5. **Filtering**: Apply date, folder, and exclusion filters
6. **Ranking**: Sort by relevance (match count)
7. **Result Formatting**: Prepare JSON response

#### 3. JEF Integration Layer
**Location**: `app.py` (lines 14-27, 515-671)

**Integration Pattern**:
```python
# Dynamic import with fallback
try:
    from jef import tiananmen, nerve_agent, meth, harry_potter, copyrights
    JEF_AVAILABLE = True
except ImportError:
    JEF_AVAILABLE = False
```

**Analysis Flow**:
1. Check JEF availability
2. Load file content
3. Run specified analysis
4. Return structured results
5. Handle errors gracefully

## 🔄 Data Flow Architecture

### Search Request Flow
```
1. User Input
   ├── Search Terms
   ├── Filter Options
   └── Mode Selection
   
2. Frontend Validation
   ├── Input Sanitization
   ├── Parameter Validation
   └── AJAX Request Formation
   
3. Backend Processing
   ├── Request Parsing
   ├── File System Scan
   ├── Content Analysis
   ├── Result Ranking
   └── Response Formation
   
4. Frontend Rendering
   ├── Result Display
   ├── Pagination
   ├── Export Options
   └── User Feedback
```

### File Processing Pipeline
```
Markdown File → YAML Parser → Metadata Extraction → Content Extraction → Search Index → Results
     │              │              │                    │                │            │
     │              │              ├── Title           │                │            │
     │              │              ├── Conversation ID │                │            │
     │              │              ├── Timestamps      │                │            │
     │              │              └── File Stats      │                │            │
     │              │                                   │                │            │
     │              └── Frontmatter ────────────────────┘                │            │
     │                                                                   │            │
     └── Raw Content ──────────────────────────────────────────────────┘            │
                                                                                      │
Search Terms → Term Processing → Boolean Logic → Match Scoring ──────────────────────┘
```

## 🗄️ Data Models

### File Metadata Structure
```python
{
    "title": str,              # Conversation title
    "path": str,               # Relative file path
    "conversation_id": str,    # Unique conversation identifier
    "create_time": str,        # Original creation timestamp
    "update_time": str,        # Last update timestamp
    "file_size": int,          # File size in bytes
    "modified_date": str,      # File system modification date
    "matches": int,            # Number of search term matches
    "snippet": str             # Highlighted content preview
}
```

### Search Query Structure
```python
{
    "terms": str,              # Search terms (space-separated)
    "mode": str,               # "ALL" or "ANY"
    "exclude": str,            # Terms to exclude
    "case_sensitive": bool,    # Case sensitivity flag
    "search_in": str,          # "all", "title", or "content"
    "date_from": str,          # Start date (YYYY-MM-DD)
    "date_to": str,            # End date (YYYY-MM-DD)
    "included_folders": list,  # Folders to include
    "excluded_folders": list   # Folders to exclude
}
```

### JEF Analysis Result
```python
{
    "test_type": str,          # Analysis type performed
    "score": float,            # Confidence score (0.0-1.0)
    "result": str,             # "CLEAN", "DETECTED", or "ERROR"
    "details": dict,           # Analysis-specific details
    "timestamp": str,          # Analysis timestamp
    "file_path": str           # Source file path
}
```

## 🔧 Design Patterns

### 1. Model-View-Controller (MVC)
- **Model**: `ChatSearchEngine` class and data structures
- **View**: Jinja2 templates and JavaScript frontend
- **Controller**: Flask route handlers

### 2. Strategy Pattern
**Search Modes**: Different search strategies (ALL/ANY) implemented as configurable behavior
```python
def search_in_content(self, content, search_terms, mode='ALL'):
    if mode == 'ALL':
        return all(term in content for term in terms)
    else:  # ANY
        return any(term in content for term in terms)
```

### 3. Factory Pattern
**JEF Analysis**: Dynamic analysis type selection
```python
def get_jef_analyzer(test_type):
    analyzers = {
        'tiananmen': tiananmen.score,
        'nerve_agent': nerve_agent.score,
        'meth': meth.score,
        'harry_potter': harry_potter.score,
        'copyrights': copyrights.score
    }
    return analyzers.get(test_type)
```

### 4. Observer Pattern
**Frontend Updates**: Event-driven UI updates
```javascript
// Search input observer
$('#searchTerms').on('input', debounce(performSearch, 500));

// File tree observer
$(document).on('click', '.folder-toggle', updateFolderState);
```

## 🔒 Security Architecture

### Input Validation Layer
```python
def validate_search_input(query_data):
    """Validate and sanitize search input"""
    # Sanitize search terms
    terms = re.escape(query_data.get('terms', ''))
    
    # Validate mode
    mode = query_data.get('mode', 'ALL')
    if mode not in ['ALL', 'ANY']:
        raise ValueError("Invalid search mode")
    
    # Validate date format
    date_pattern = r'^\d{4}-\d{2}-\d{2}$'
    # ... validation logic
```

### Path Security
```python
def secure_file_access(base_path, requested_path):
    """Prevent path traversal attacks"""
    # Normalize paths
    base = os.path.abspath(base_path)
    requested = os.path.abspath(os.path.join(base, requested_path))
    
    # Ensure requested path is within base
    if not requested.startswith(base):
        raise SecurityError("Access denied")
    
    return requested
```

### Content Security Policy
```html
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'self' 'unsafe-inline' cdn.jsdelivr.net; 
               style-src 'self' 'unsafe-inline' cdn.jsdelivr.net;">
```

## 📈 Performance Architecture

### Optimization Strategies

#### 1. File System Optimization
- **Lazy Loading**: File tree loads incrementally
- **Depth Limiting**: Prevents deep recursion performance issues
- **Caching**: File metadata cached in memory during search

#### 2. Search Optimization
- **Early Termination**: Stop processing when enough results found
- **Parallel Processing**: Multiple files processed concurrently (future enhancement)
- **Index Building**: Pre-built search index for large archives (future enhancement)

#### 3. Frontend Optimization
- **Debouncing**: Prevents excessive search requests
- **Virtual Scrolling**: Handles large result sets efficiently
- **Progressive Loading**: Results load incrementally

### Memory Management
```python
def process_large_file(file_path, chunk_size=8192):
    """Process large files in chunks to manage memory"""
    with open(file_path, 'r', encoding='utf-8') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield process_chunk(chunk)
```

## 🔮 Extensibility Architecture

### Plugin System (Future Enhancement)
```python
class AnalysisPlugin:
    """Base class for analysis plugins"""
    
    def analyze(self, content: str) -> dict:
        raise NotImplementedError
    
    def get_name(self) -> str:
        raise NotImplementedError

class CustomAnalyzer(AnalysisPlugin):
    def analyze(self, content: str) -> dict:
        # Custom analysis logic
        return {"score": 0.5, "details": {}}
```

### Configuration System
```python
class Config:
    """Centralized configuration management"""
    
    ARCHIVE_PATH = os.environ.get('ARCHIVE_PATH', 'ChatGPT chats/ChatGPT chats')
    MAX_RESULTS = int(os.environ.get('MAX_RESULTS', 1000))
    SEARCH_TIMEOUT = int(os.environ.get('SEARCH_TIMEOUT', 30))
    JEF_PATH = os.environ.get('JEF_PATH', 'K:/0din/0din-JEF')
```

### API Versioning (Future Enhancement)
```python
@app.route('/api/v1/search', methods=['POST'])
def search_v1():
    # Version 1 API implementation
    pass

@app.route('/api/v2/search', methods=['POST'])
def search_v2():
    # Version 2 API with enhanced features
    pass
```

## 🧪 Testing Architecture

### Test Structure
```
tests/
├── unit/
│   ├── test_search_engine.py
│   ├── test_file_processing.py
│   └── test_jef_integration.py
├── integration/
│   ├── test_api_endpoints.py
│   └── test_file_operations.py
├── e2e/
│   ├── test_search_workflow.py
│   └── test_export_functionality.py
└── fixtures/
    ├── sample_conversations/
    └── test_data.json
```

### Test Categories
1. **Unit Tests**: Individual component testing
2. **Integration Tests**: Component interaction testing
3. **End-to-End Tests**: Full workflow testing
4. **Performance Tests**: Load and stress testing
5. **Security Tests**: Vulnerability and penetration testing

## 📊 Monitoring and Observability

### Logging Architecture
```python
import logging
from logging.handlers import RotatingFileHandler

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Add file rotation
handler = RotatingFileHandler('logs/app.log', maxBytes=10485760, backupCount=5)
app.logger.addHandler(handler)
```

### Metrics Collection (Future Enhancement)
```python
from prometheus_client import Counter, Histogram, generate_latest

# Define metrics
search_requests = Counter('search_requests_total', 'Total search requests')
search_duration = Histogram('search_duration_seconds', 'Search duration')

@app.route('/metrics')
def metrics():
    return generate_latest()
```

## 🚀 Deployment Architecture

### Development Environment
- **Local Flask server** with debug mode
- **Hot reloading** for development
- **SQLite** for development data (if needed)

### Production Environment
- **WSGI server** (Gunicorn/uWSGI)
- **Reverse proxy** (Nginx/Apache)
- **Process management** (systemd/supervisor)
- **SSL termination** at proxy level

### Containerized Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

---

This architecture supports the current feature set while providing a foundation for future enhancements and scalability improvements.