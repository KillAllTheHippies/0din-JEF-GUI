# API Documentation

This document provides comprehensive documentation for the ChatGPT Archive Search Tool's REST API endpoints.

## 📋 Overview

The API provides programmatic access to search functionality, file management, and JEF integration features. All endpoints return JSON responses and use standard HTTP status codes.

### Base URL
```
http://localhost:5000
```

### Content Types
- **Request**: `application/json`
- **Response**: `application/json`

### Authentication
No authentication required for local deployment. For production deployments, consider implementing appropriate authentication mechanisms.

## 🔍 Search Endpoints

### Search Files
Search through ChatGPT archive files with advanced filtering options.

**Endpoint:** `POST /search`

**Request Body:**
```json
{
  "terms": "search terms here",
  "mode": "ALL",
  "exclude": "terms to exclude",
  "case_sensitive": false,
  "search_in": "all",
  "date_from": "2024-01-01",
  "date_to": "2024-12-31",
  "included_folders": ["folder1", "folder2"],
  "excluded_folders": ["temp", "drafts"]
}
```

**Parameters:**
- `terms` (string, required): Search terms, use quotes for exact phrases
- `mode` (string): Search logic - "ALL" (AND) or "ANY" (OR). Default: "ALL"
- `exclude` (string): Terms to exclude from results
- `case_sensitive` (boolean): Enable case-sensitive search. Default: false
- `search_in` (string): Search scope - "all", "title", or "content". Default: "all"
- `date_from` (string): Start date filter (YYYY-MM-DD format)
- `date_to` (string): End date filter (YYYY-MM-DD format)
- `included_folders` (array): Only search in these folders
- `excluded_folders` (array): Exclude these folders from search

**Response:**
```json
{
  "results": [
    {
      "title": "Python Programming Discussion",
      "path": "2024/11/python-help.md",
      "matches": 5,
      "file_size": 2048,
      "modified_date": "2024-11-15",
      "snippet": "...highlighted search results...",
      "conversation_id": "abc123-def456",
      "create_time": "15/11/2024 at 10:30",
      "update_time": "15/11/2024 at 11:45"
    }
  ],
  "total": 25,
  "search_time": "0.156s"
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid request parameters
- `500`: Server error during search

**Example:**
```bash
curl -X POST http://localhost:5000/search \
  -H "Content-Type: application/json" \
  -d '{
    "terms": "python machine learning",
    "mode": "ALL",
    "case_sensitive": false
  }'
```

## 📁 File Management Endpoints

### Get File Tree
Retrieve the hierarchical structure of the archive directory.

**Endpoint:** `GET /api/file-tree`

**Response:**
```json
{
  "2024": {
    "type": "folder",
    "name": "2024",
    "children": {
      "11": {
        "type": "folder", 
        "name": "11",
        "children": {
          "conversation1.md": {
            "type": "file",
            "name": "conversation1.md"
          }
        }
      }
    }
  }
}
```

**Status Codes:**
- `200`: Success
- `500`: Error accessing file system

### Get File Content
Retrieve the content and metadata of a specific file.

**Endpoint:** `GET /file-content/<path:file_path>`

**Parameters:**
- `file_path` (path): Relative path to the file within the archive

**Response:**
```json
{
  "content": "# Title: Conversation Title\n\n### User...",
  "html_content": "<h1>Title: Conversation Title</h1>...",
  "metadata": {
    "title": "Conversation Title",
    "conversation_id": "abc123-def456",
    "create_time": "15/11/2024 at 10:30",
    "update_time": "15/11/2024 at 11:45",
    "file_size": 2048,
    "modified_date": "2024-11-15"
  }
}
```

**Status Codes:**
- `200`: Success
- `404`: File not found
- `403`: Access denied (path traversal attempt)
- `500`: Error reading file

**Example:**
```bash
curl http://localhost:5000/file-content/2024/11/conversation.md
```

## 📤 Export Endpoints

### Export Search Results (CSV)
Export search results in CSV format with full metadata.

**Endpoint:** `GET /export/csv`

**Query Parameters:**
All search parameters from the search endpoint, plus:
- `pathType` (string): "relative" or "full" paths. Default: "relative"

**Response:**
CSV file download with headers:
- Title
- Path
- Matches
- File Size
- Modified Date
- Conversation ID
- Create Time
- Update Time

**Example:**
```bash
curl "http://localhost:5000/export/csv?terms=python&mode=ALL&pathType=relative" \
  -o search_results.csv
```

### Export Paths Only (CSV)
Export only file paths from search results.

**Endpoint:** `GET /export/csv-paths`

**Query Parameters:**
Same as full CSV export.

**Response:**
Simple CSV with just file paths.

### Export JSON
Export search results in JSON format with complete metadata.

**Endpoint:** `GET /export/json`

**Query Parameters:**
Same as CSV export.

**Response:**
```json
{
  "search_info": {
    "terms": "python",
    "mode": "ALL",
    "timestamp": "2024-11-15T10:30:00Z",
    "total_results": 25
  },
  "results": [
    {
      "title": "Python Discussion",
      "path": "2024/11/python.md",
      "matches": 3,
      "file_size": 1024,
      "modified_date": "2024-11-15",
      "metadata": {...}
    }
  ]
}
```

## 🛡️ JEF Integration Endpoints

### Check JEF Status
Verify if JEF framework is available and functional.

**Endpoint:** `GET /jef/status`

**Response:**
```json
{
  "available": true,
  "version": "1.0.0",
  "tests": ["tiananmen", "nerve_agent", "meth", "harry_potter", "copyrights"]
}
```

**Status Codes:**
- `200`: JEF status retrieved successfully
- `503`: JEF not available

### Get Available JEF Tests
List all available JEF analysis types.

**Endpoint:** `GET /jef/tests`

**Response:**
```json
{
  "tests": [
    {
      "name": "tiananmen",
      "description": "Tiananmen Square content analysis",
      "requires_reference": false
    },
    {
      "name": "copyrights", 
      "description": "Copyright violation detection",
      "requires_reference": true
    }
  ]
}
```

### Analyze Single File
Run JEF analysis on file content.

**Endpoint:** `POST /jef/analyze`

**Request Body:**
```json
{
  "content": "Text content to analyze",
  "test_type": "tiananmen",
  "reference": "Reference text for comparison (optional)"
}
```

**Parameters:**
- `content` (string, required): Text content to analyze
- `test_type` (string, required): Analysis type ("tiananmen", "nerve_agent", "meth", "harry_potter", "copyrights")
- `reference` (string): Reference text (required for copyright analysis)

**Response:**
```json
{
  "test_type": "tiananmen",
  "score": 0.75,
  "result": "DETECTED",
  "details": {
    "confidence": "high",
    "matches": ["sensitive term 1", "sensitive term 2"]
  },
  "timestamp": "2024-11-15T10:30:00Z"
}
```

**Status Codes:**
- `200`: Analysis completed successfully
- `400`: Invalid request parameters
- `503`: JEF not available
- `500`: Analysis failed

### Batch Analysis
Run JEF analysis on multiple files from search results.

**Endpoint:** `POST /jef/batch-analyze`

**Request Body:**
```json
{
  "file_paths": ["2024/11/file1.md", "2024/11/file2.md"],
  "test_type": "tiananmen"
}
```

**Response:**
```json
{
  "results": [
    {
      "file_path": "2024/11/file1.md",
      "test_type": "tiananmen",
      "score": 0.25,
      "result": "CLEAN",
      "timestamp": "2024-11-15T10:30:00Z"
    },
    {
      "file_path": "2024/11/file2.md", 
      "test_type": "tiananmen",
      "score": 0.85,
      "result": "DETECTED",
      "timestamp": "2024-11-15T10:30:01Z"
    }
  ],
  "summary": {
    "total_files": 2,
    "clean_files": 1,
    "detected_files": 1,
    "failed_files": 0
  }
}
```

## 🔧 Utility Endpoints

### Health Check
Check application health and status.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-11-15T10:30:00Z",
  "version": "2.0.0",
  "archive_path": "/path/to/archive",
  "jef_available": true
}
```

### Application Info
Get application configuration and capabilities.

**Endpoint:** `GET /info`

**Response:**
```json
{
  "name": "ChatGPT Archive Search Tool",
  "version": "2.0.0",
  "features": {
    "search": true,
    "export": true,
    "jef_integration": true,
    "file_viewer": true
  },
  "limits": {
    "max_file_size": 16777216,
    "max_search_results": 1000,
    "file_tree_depth": 3
  }
}
```

## 📊 Error Handling

### Standard Error Response
All endpoints return errors in a consistent format:

```json
{
  "error": {
    "code": "INVALID_SEARCH_TERMS",
    "message": "Search terms cannot be empty",
    "details": {
      "field": "terms",
      "provided": ""
    }
  },
  "timestamp": "2024-11-15T10:30:00Z"
}
```

### Common Error Codes
- `INVALID_REQUEST`: Malformed request data
- `INVALID_SEARCH_TERMS`: Empty or invalid search terms
- `FILE_NOT_FOUND`: Requested file doesn't exist
- `ACCESS_DENIED`: Path traversal or permission denied
- `JEF_UNAVAILABLE`: JEF framework not available
- `ANALYSIS_FAILED`: JEF analysis encountered an error
- `EXPORT_FAILED`: Export generation failed
- `INTERNAL_ERROR`: Unexpected server error

## 🚀 Rate Limiting

Currently no rate limiting is implemented for local deployment. For production use, consider implementing:

- Request rate limiting per IP
- Concurrent search limitations
- File access throttling
- Export download limits

## 📝 Usage Examples

### Python Client Example
```python
import requests
import json

# Search for files
search_data = {
    "terms": "python machine learning",
    "mode": "ALL",
    "case_sensitive": False
}

response = requests.post(
    "http://localhost:5000/search",
    json=search_data
)

if response.status_code == 200:
    results = response.json()
    print(f"Found {results['total']} files")
    for file in results['results']:
        print(f"- {file['title']} ({file['matches']} matches)")
```

### JavaScript Client Example
```javascript
// Search files
async function searchFiles(terms) {
    const response = await fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            terms: terms,
            mode: 'ALL'
        })
    });
    
    if (response.ok) {
        const results = await response.json();
        console.log(`Found ${results.total} files`);
        return results;
    } else {
        const error = await response.json();
        console.error('Search failed:', error.error.message);
    }
}

// Get file content
async function getFileContent(filePath) {
    const response = await fetch(`/file-content/${filePath}`);
    
    if (response.ok) {
        const data = await response.json();
        return data;
    } else {
        console.error('Failed to load file:', response.statusText);
    }
}
```

### cURL Examples
```bash
# Basic search
curl -X POST http://localhost:5000/search \
  -H "Content-Type: application/json" \
  -d '{"terms": "python", "mode": "ALL"}'

# Advanced search with filters
curl -X POST http://localhost:5000/search \
  -H "Content-Type: application/json" \
  -d '{
    "terms": "machine learning",
    "mode": "ANY",
    "exclude": "deprecated old",
    "date_from": "2024-01-01",
    "included_folders": ["2024"]
  }'

# Export results
curl "http://localhost:5000/export/csv?terms=python&mode=ALL" \
  -o results.csv

# JEF analysis
curl -X POST http://localhost:5000/jef/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Text to analyze",
    "test_type": "tiananmen"
  }'
```

---

For more information about specific features or integration examples, refer to the main documentation files in the repository.