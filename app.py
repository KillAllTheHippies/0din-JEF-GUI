from flask import Flask, render_template, request, jsonify, send_file
import os
import re
import sys
import subprocess
from pathlib import Path
import yaml
from datetime import datetime
import json
import csv
import tempfile
import markdown
from markdown.extensions import codehilite, toc, tables

# Import configuration manager
from config_manager import config

app = Flask(__name__)

@app.route('/api/theme.css')
def theme_css():
    """
    Generate a dynamic CSS file with theme variables.
    """
    css_vars = config.get_theme_css_variables()
    
    css_rules = ":root {\n"
    for var, value in css_vars.items():
        css_rules += f"  {var}: {value};\n"
    css_rules += "}\n"
    
    return css_rules, 200, {'Content-Type': 'text/css'}

# Initialize JEF based on configuration
def initialize_jef():
    """Initialize JEF integration based on configuration settings."""
    global JEF_AVAILABLE, JEF_PATH, tiananmen, nerve_agent, meth, harry_potter, copyrights
    
    jef_path = config.get("jef_path")
    jef_enabled = config.get("enable_jef_integration", False)
    
    if not jef_enabled or not jef_path:
        JEF_AVAILABLE = False
        print("JEF integration disabled in configuration")
        return
    
    JEF_PATH = Path(jef_path)
    if JEF_PATH.exists():
        sys.path.insert(0, str(JEF_PATH))
        try:
            from jef import tiananmen, nerve_agent, meth, harry_potter, copyrights
            # Make modules available globally
            globals()['tiananmen'] = tiananmen
            globals()['nerve_agent'] = nerve_agent
            globals()['meth'] = meth
            globals()['harry_potter'] = harry_potter
            globals()['copyrights'] = copyrights
            JEF_AVAILABLE = True
            print(f"JEF integration loaded successfully from {JEF_PATH}")
        except ImportError as e:
            JEF_AVAILABLE = False
            print(f"JEF not available: {e}")
    else:
        JEF_AVAILABLE = False
        print(f"JEF path not found: {JEF_PATH}")

# Initialize JEF modules as None initially
tiananmen = None
nerve_agent = None
meth = None
harry_potter = None
copyrights = None

# Initialize JEF
initialize_jef()

class ChatSearchEngine:
    """
    Main search engine for ChatGPT conversation archives.
    
    Handles file discovery, metadata extraction, content searching,
    and result ranking for markdown files in the archive directory.
    
    Attributes:
        base_path (Path): Root directory containing ChatGPT archive files
    """
    
    def __init__(self, base_path: str):
        """
        Initialize the search engine with the archive base path.
        
        Args:
            base_path: Path to the root directory containing ChatGPT archive files
            
        Raises:
            FileNotFoundError: If the base path doesn't exist
        """
        self.base_path = Path(base_path)
        print(f"Initializing search engine with path: {self.base_path}")
        
    def extract_metadata(self, file_path: Path) -> dict:
        """
        Extract YAML frontmatter and basic file information from a markdown file.
        
        Parses YAML frontmatter to extract conversation metadata like title,
        conversation ID, timestamps, etc. Also extracts basic file stats.
        
        Args:
            file_path: Path to the markdown file to process
            
        Returns:
            Dictionary containing extracted metadata:
            - title: Conversation title from YAML or filename
            - conversation_id: Unique conversation identifier
            - create_time: Creation timestamp
            - update_time: Last update timestamp
            - file_size: File size in bytes
            - modified_date: File modification date
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            UnicodeDecodeError: If the file can't be decoded as UTF-8
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract YAML frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    yaml_content = parts[1].strip()
                    try:
                        metadata = yaml.safe_load(yaml_content)
                    except:
                        metadata = {}
                    body_content = parts[2].strip()
                else:
                    metadata = {}
                    body_content = content
            else:
                metadata = {}
                body_content = content
            
            # Extract title from metadata or fallbacks
            # Some archives use `title` while others may use `aliases` for the
            # conversation title. Try both before falling back to the content
            # or filename.
            title = metadata.get('title') or metadata.get('aliases', '')
            if not title:
                # Try to find title in content
                title_match = re.search(r'^# Title: (.+)$', body_content, re.MULTILINE)
                if title_match:
                    title = title_match.group(1)
                else:
                    # Use filename as fallback
                    title = file_path.stem
            
            return {
                'metadata': metadata,
                'title': title,
                'content': body_content,
                'file_size': file_path.stat().st_size,
                'modified_date': datetime.fromtimestamp(file_path.stat().st_mtime)
            }
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return {
                'metadata': {},
                'title': file_path.stem,
                'content': '',
                'file_size': 0,
                'modified_date': datetime.now()
            }
    
    def search_in_content(self, content: str, search_terms: str, mode: str = 'ALL', case_sensitive: bool = False) -> int:
        """
        Search for terms within text content using boolean logic.
        
        Supports both ALL (AND) and ANY (OR) search modes with optional
        case sensitivity. Handles quoted phrases as exact matches.
        
        Args:
            content: Text content to search within
            search_terms: Space-separated search terms (use quotes for phrases)
            mode: Search mode - "ALL" for AND logic, "ANY" for OR logic
            case_sensitive: Whether to perform case-sensitive matching
            
        Returns:
            Number of matching terms found (for ranking purposes)
            
        Example:
            >>> engine.search_in_content("Hello world", "hello world", "ALL", False)
            2
            >>> engine.search_in_content("Hello world", '"hello world"', "ALL", False)
            1
        """
        if not search_terms.strip():
            return False, []
        
        # Prepare content for searching
        search_content = content if case_sensitive else content.lower()
        
        # Split search terms (handle quoted phrases)
        terms = []
        current_term = ""
        in_quotes = False
        
        for char in search_terms:
            if char == '"':
                if in_quotes:
                    if current_term.strip():
                        terms.append(current_term.strip())
                    current_term = ""
                    in_quotes = False
                else:
                    in_quotes = True
            elif char == ' ' and not in_quotes:
                if current_term.strip():
                    terms.append(current_term.strip())
                current_term = ""
            else:
                current_term += char
        
        if current_term.strip():
            terms.append(current_term.strip())
        
        # Prepare terms for searching
        if not case_sensitive:
            terms = [term.lower() for term in terms]
        
        # Find matches
        matches = []
        found_terms = []
        
        for term in terms:
            if term in search_content:
                matches.extend([m.start() for m in re.finditer(re.escape(term), search_content)])
                found_terms.append(term)
        
        # Apply search mode logic
        if mode == 'ALL':
            return len(found_terms) == len(terms), matches
        else:  # ANY
            return len(found_terms) > 0, matches
    
    def search(self, query_data: dict) -> dict:
        """
        Main search function that processes search queries and returns ranked results.
        
        Searches through all markdown files in the archive directory based on
        the provided query parameters. Supports folder filtering, date ranges,
        and various search modes.
        
        Args:
            query_data: Dictionary containing search parameters:
                - terms: Search terms string
                - mode: "ALL" or "ANY" for boolean logic
                - exclude: Terms to exclude from results
                - case_sensitive: Boolean for case sensitivity
                - search_in: "all", "title", or "content"
                - date_from/date_to: Date range filters
                - included_folders/excluded_folders: Folder filters
                
        Returns:
            Dictionary containing:
            - results: List of matching files with metadata
            - total: Total number of results
            - search_time: Time taken for search
            
        Example:
            >>> query = {"terms": "python code", "mode": "ALL"}
            >>> results = engine.search(query)
            >>> len(results['results'])
            15
        """
        search_terms = query_data.get('terms', '').strip()
        exclude_terms = query_data.get('exclude', '').strip()
        mode = query_data.get('mode', 'ALL')
        search_in = query_data.get('searchIn', 'all')
        case_sensitive = query_data.get('caseSensitive', False)
        date_from = query_data.get('dateFrom', '')
        date_to = query_data.get('dateTo', '')
        included_folders = query_data.get('includedFolders', [])
        excluded_folders = query_data.get('excludedFolders', [])
        
        results = []
        
        if not search_terms:
            return results
        
        # Find all markdown files
        md_files = list(self.base_path.rglob("*.md"))
        print(f"Found {len(md_files)} markdown files")
        
        for file_path in md_files:
            try:
                # Check folder filters
                relative_path = str(file_path.relative_to(self.base_path))
                file_folder = str(file_path.parent.relative_to(self.base_path))
                
                # Apply folder filtering
                if included_folders:
                    # If there are included folders, only search in those
                    folder_included = False
                    for included in included_folders:
                        if file_folder.startswith(included) or included.startswith(file_folder):
                            folder_included = True
                            break
                    if not folder_included:
                        continue
                
                if excluded_folders:
                    # Skip files in excluded folders
                    folder_excluded = False
                    for excluded in excluded_folders:
                        if file_folder.startswith(excluded):
                            folder_excluded = True
                            break
                    if folder_excluded:
                        continue
                
                file_info = self.extract_metadata(file_path)
                
                # Date filtering
                if date_from:
                    try:
                        from_date = datetime.strptime(date_from, '%Y-%m-%d')
                        if file_info['modified_date'].date() < from_date.date():
                            continue
                    except:
                        pass
                
                if date_to:
                    try:
                        to_date = datetime.strptime(date_to, '%Y-%m-%d')
                        if file_info['modified_date'].date() > to_date.date():
                            continue
                    except:
                        pass
                
                # Determine what to search in
                search_content = ""
                if search_in == 'title':
                    search_content = file_info['title']
                elif search_in == 'content':
                    search_content = file_info['content']
                else:  # all
                    search_content = f"{file_info['title']} {file_info['content']}"
                
                # Check for matches
                has_match, match_positions = self.search_in_content(
                    search_content, search_terms, mode, case_sensitive
                )
                
                # Check exclude terms
                if has_match and exclude_terms:
                    has_exclude, _ = self.search_in_content(
                        search_content, exclude_terms, 'ANY', case_sensitive
                    )
                    if has_exclude:
                        has_match = False
                
                if has_match:
                    relative_path = str(file_path.relative_to(self.base_path))
                    
                    results.append({
                        'path': relative_path,
                        'title': file_info['title'],
                        'matches': len(match_positions),
                        'file_size': file_info['file_size'],
                        'modified_date': file_info['modified_date'].strftime('%Y-%m-%d %H:%M'),
                        'create_time': file_info['metadata'].get('create_time', ''),
                        'conversation_id': file_info['metadata'].get('conversation_id', '')
                    })
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                continue
        
        # Sort results by number of matches (descending)
        results.sort(key=lambda x: x['matches'], reverse=True)
        
        print(f"Search completed. Found {len(results)} matching files")
        return results

# Initialize search engine with configured path
search_engine = ChatSearchEngine(config.get("archive_path"))

@app.route('/')
def index():
    """
    Render the main search interface.
    
    Returns the primary web interface with search form, file explorer,
    and result display areas. Includes all necessary JavaScript and CSS
    for interactive functionality.
    
    Returns:
        Rendered HTML template for the main application interface
    """
    return render_template('index.html')

@app.route('/settings')
def settings():
    """
    Render the settings/configuration interface.
    
    Returns the settings page where users can configure the application
    including archive path, theme, search preferences, and other options.
    
    Returns:
        Rendered HTML template for the settings interface
    """
    return render_template('settings.html')

@app.route('/api/settings', methods=['GET'])
def get_settings():
    """
    Get current application settings.
    
    Returns:
        JSON response containing all current configuration settings
    """
    try:
        settings = config.get_all()
        return jsonify(settings)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/settings', methods=['POST'])
def save_settings():
    """
    Save application settings.
    
    Accepts JSON payload with configuration settings and validates
    them before saving to the configuration file.
    
    Request JSON:
        {
            "archive_path": "path/to/archive",
            "theme_mode": "auto|light|dark",
            "accent_color": "blue|purple|green|...",
            "custom_primary_color": "#hexcolor",
            ...
        }
    
    Returns:
        JSON response indicating success or failure
    """
    try:
        new_settings = request.get_json()
        
        if not new_settings:
            return jsonify({'error': 'No settings provided'}), 400
        
        # Validate settings
        old_settings = config.get_all()
        config.update(new_settings)
        errors = config.validate_settings()
        
        if errors:
            # Restore old settings if validation fails
            config.settings = old_settings
            return jsonify({
                'error': 'Validation failed',
                'validation_errors': errors
            }), 400
        
        # Save settings
        if config.save_settings():
            # Reinitialize components that depend on settings
            global search_engine
            archive_path = config.get("archive_path")
            if archive_path and Path(archive_path).exists():
                search_engine = ChatSearchEngine(archive_path)
            
            # Reinitialize JEF if settings changed
            if 'jef_path' in new_settings or 'enable_jef_integration' in new_settings:
                initialize_jef()
            
            return jsonify({
                'success': True,
                'message': 'Settings saved successfully'
            })
        else:
            return jsonify({'error': 'Failed to save settings'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/settings/validate', methods=['POST'])
def validate_settings():
    """
    Validate settings without saving them.
    
    Returns:
        JSON response with validation results
    """
    try:
        test_settings = request.get_json()
        
        if not test_settings:
            return jsonify({'error': 'No settings provided'}), 400
        
        # Temporarily update settings for validation
        old_settings = config.get_all()
        config.update(test_settings)
        errors = config.validate_settings()
        
        # Restore original settings
        config.settings = old_settings
        
        return jsonify({
            'valid': len(errors) == 0,
            'errors': errors
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/settings/reset', methods=['POST'])
def reset_settings():
    """
    Reset all settings to default values.
    
    Returns:
        JSON response indicating success or failure
    """
    try:
        config.reset_to_defaults()
        
        if config.save_settings():
            # Reinitialize components
            global search_engine
            search_engine = ChatSearchEngine(config.get("archive_path"))
            initialize_jef()
            
            return jsonify({
                'success': True,
                'message': 'Settings reset to defaults'
            })
        else:
            return jsonify({'error': 'Failed to save default settings'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/settings/export')
def export_settings():
    """
    Export current settings as a downloadable JSON file.
    
    Returns:
        JSON file download with current settings
    """
    try:
        # Create temporary file with settings
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json', encoding='utf-8')
        
        export_data = {
            **config.get_all(),
            'exported_at': datetime.now().isoformat(),
            'export_version': '1.0'
        }
        
        json.dump(export_data, temp_file, indent=2, ensure_ascii=False)
        temp_file.close()
        
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=f'chatgpt-search-settings-{datetime.now().strftime("%Y%m%d_%H%M%S")}.json',
            mimetype='application/json'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/browse-folder', methods=['POST'])
def browse_folder():
    """
    Open a folder selection dialog on the server side.
    
    Returns:
        JSON response with selected folder path
    """
    try:
        import tkinter as tk
        from tkinter import filedialog
        
        # Create a root window and hide it
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        # Open folder selection dialog
        folder_path = filedialog.askdirectory(
            title="Select ChatGPT Archive Folder",
            mustexist=True
        )
        
        # Clean up
        root.destroy()
        
        if folder_path:
            return jsonify({
                'success': True,
                'path': folder_path,
                'message': f'Selected folder: {folder_path}'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'No folder selected'
            })
            
    except ImportError:
        return jsonify({
            'success': False,
            'error': 'tkinter not available - cannot open folder dialog'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/validate-archive-path', methods=['POST'])
def validate_archive_path():
    """
    Validate an archive path to check if it exists and contains markdown files.
    
    Returns:
        JSON response with validation results
    """
    try:
        data = request.get_json()
        path = data.get('path', '').strip()
        
        if not path:
            return jsonify({
                'valid': False,
                'error': 'No path provided'
            })
        
        archive_path = Path(path)
        
        # Check if path exists
        if not archive_path.exists():
            return jsonify({
                'valid': False,
                'error': 'Path does not exist'
            })
        
        # Check if it's a directory
        if not archive_path.is_dir():
            return jsonify({
                'valid': False,
                'error': 'Path is not a directory'
            })
        
        # Count markdown files and folders
        try:
            md_files = list(archive_path.rglob("*.md"))
            folders = set()
            
            for file_path in md_files:
                folders.add(str(file_path.parent))
            
            return jsonify({
                'valid': True,
                'file_count': len(md_files),
                'folder_count': len(folders),
                'message': f'Found {len(md_files)} markdown files in {len(folders)} folders'
            })
            
        except PermissionError:
            return jsonify({
                'valid': False,
                'error': 'Permission denied - cannot access this directory'
            })
        except Exception as e:
            return jsonify({
                'valid': False,
                'error': f'Error scanning directory: {str(e)}'
            })
            
    except Exception as e:
        return jsonify({
            'valid': False,
            'error': str(e)
        })

@app.route('/api/settings/import', methods=['POST'])
def import_settings():
    """
    Import settings from an uploaded JSON file.
    
    Returns:
        JSON response indicating success or failure
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.json'):
            return jsonify({'error': 'File must be a JSON file'}), 400
        
        # Read and parse the file
        content = file.read().decode('utf-8')
        imported_settings = json.loads(content)
        
        # Remove export metadata
        imported_settings.pop('exported_at', None)
        imported_settings.pop('export_version', None)
        
        # Validate imported settings
        old_settings = config.get_all()
        config.update(imported_settings)
        errors = config.validate_settings()
        
        if errors:
            # Restore original settings if validation fails
            config.settings = old_settings
            return jsonify({
                'error': 'Validation failed',
                'validation_errors': errors
            }), 400
        
        # Save imported settings
        if config.save_settings():
            # Reinitialize components
            global search_engine
            archive_path = config.get("archive_path")
            if archive_path and Path(archive_path).exists():
                search_engine = ChatSearchEngine(archive_path)
            initialize_jef()
            
            return jsonify({
                'success': True,
                'message': 'Settings imported successfully'
            })
        else:
            # Restore original settings if save fails
            config.settings = old_settings
            return jsonify({'error': 'Failed to save imported settings'}), 500
            
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON file'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/search', methods=['POST'])
def search():
    """
    AJAX endpoint for processing search requests.
    
    Accepts JSON payload with search parameters and returns matching
    files with metadata. Supports advanced filtering, boolean logic,
    and folder-based restrictions.
    
    Request JSON:
        {
            "terms": "search terms",
            "mode": "ALL|ANY", 
            "exclude": "excluded terms",
            "case_sensitive": boolean,
            "search_in": "all|title|content",
            "date_from": "YYYY-MM-DD",
            "date_to": "YYYY-MM-DD",
            "included_folders": ["folder1", "folder2"],
            "excluded_folders": ["folder3"]
        }
    
    Returns:
        JSON response with search results:
        {
            "results": [
                {
                    "title": "Conversation Title",
                    "path": "relative/path/to/file.md",
                    "matches": 5,
                    "file_size": 1024,
                    "modified_date": "2024-01-01",
                    "snippet": "...highlighted content..."
                }
            ],
            "total": 42,
            "search_time": "0.123s"
        }
    
    Raises:
        400: If request data is invalid
        500: If search processing fails
    """
    try:
        query_data = request.get_json()
        results = search_engine.search(query_data)
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
    except Exception as e:
        print(f"Search error: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'results': [],
            'count': 0
        })

@app.route('/api/file-tree')
def get_file_tree():
    """
    Generate hierarchical file tree structure for the sidebar explorer.
    
    Recursively scans the archive directory to build a nested tree
    structure showing folders and markdown files. Limits depth to
    prevent performance issues with very deep directory structures.
    
    Returns:
        JSON tree structure:
        {
            "folder_name": {
                "type": "folder",
                "name": "folder_name", 
                "children": {
                    "subfolder": {...},
                    "file.md": {
                        "type": "file",
                        "name": "file.md"
                    }
                }
            }
        }
    
    Note:
        - Hidden files/folders (starting with .) are excluded
        - Only .md files are included in the tree
        - Maximum depth is limited to 3 levels by default
        - Inaccessible directories are silently skipped
    """
    try:
        def build_tree(path, max_depth=3, current_depth=0):
            tree = {}
            
            # Limit depth to prevent performance issues
            if current_depth >= max_depth:
                return tree
                
            try:
                items = list(path.iterdir())
                print(f"Processing {path}: found {len(items)} items")
                
                for item in items:
                    if item.name.startswith('.'):
                        continue  # Skip hidden files/folders
                    
                    if item.is_dir():
                        tree[item.name] = {
                            'type': 'folder',
                            'name': item.name,
                            'children': build_tree(item, max_depth, current_depth + 1)
                        }
                    elif item.suffix == '.md':
                        tree[item.name] = {
                            'type': 'file',
                            'name': item.name
                        }
            except (PermissionError, OSError) as e:
                print(f"Error accessing {path}: {e}")
                pass  # Skip directories we can't access
            
            return tree
        
        print(f"Building file tree from: {search_engine.base_path}")
        file_tree = build_tree(search_engine.base_path)
        print(f"File tree built successfully with {len(file_tree)} root items")
        return jsonify(file_tree)
    
    except Exception as e:
        print(f"File tree error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/export/<format>')
def export_results(format):
    """Export search results"""
    try:
        # Get search parameters from query string
        search_terms = request.args.get('terms', '')
        exclude_terms = request.args.get('exclude', '')
        mode = request.args.get('mode', 'ALL')
        search_in = request.args.get('searchIn', 'all')
        case_sensitive = request.args.get('caseSensitive', 'false') == 'true'
        path_type = request.args.get('pathType', 'relative')  # relative or full
        
        # Perform search again to get current results
        query_data = {
            'terms': search_terms,
            'exclude': exclude_terms,
            'mode': mode,
            'searchIn': search_in,
            'caseSensitive': case_sensitive
        }
        
        results = search_engine.search(query_data)
        
        if format == 'csv':
            # Create temporary CSV file - Full export
            temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8')
            
            writer = csv.writer(temp_file)
            writer.writerow(['File Path', 'Title', 'Matches', 'File Size', 'Modified Date', 'Create Time', 'Conversation ID'])
            
            for result in results:
                file_path = result['path']
                if path_type == 'full':
                    file_path = str(search_engine.base_path / result['path'])
                
                writer.writerow([
                    file_path,
                    result['title'],
                    result['matches'],
                    result['file_size'],
                    result['modified_date'],
                    result['create_time'],
                    result['conversation_id']
                ])
            
            temp_file.close()
            
            return send_file(
                temp_file.name,
                as_attachment=True,
                download_name=f'chatgpt_search_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                mimetype='text/csv'
            )
        
        elif format == 'csv-paths':
            # Create temporary CSV file - Paths only
            temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8')
            
            writer = csv.writer(temp_file)
            writer.writerow(['File Path'])
            
            for result in results:
                file_path = result['path']
                if path_type == 'full':
                    file_path = str(search_engine.base_path / result['path'])
                
                writer.writerow([file_path])
            
            temp_file.close()
            
            return send_file(
                temp_file.name,
                as_attachment=True,
                download_name=f'chatgpt_search_paths_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                mimetype='text/csv'
            )
        
        elif format == 'json':
            # Create temporary JSON file
            temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json', encoding='utf-8')
            
            export_data = {
                'search_query': query_data,
                'timestamp': datetime.now().isoformat(),
                'total_results': len(results),
                'results': results
            }
            
            json.dump(export_data, temp_file, indent=2, ensure_ascii=False)
            temp_file.close()
            
            return send_file(
                temp_file.name,
                as_attachment=True,
                download_name=f'chatgpt_search_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json',
                mimetype='application/json'
            )
    
    except Exception as e:
        return f"Export error: {str(e)}", 500

@app.route('/api/jef-status')
def jef_status():
    """Check if JEF is available"""
    return jsonify({
        'available': JEF_AVAILABLE,
        'path': str(JEF_PATH) if JEF_PATH.exists() else None
    })

@app.route('/api/jef-tests')
def get_jef_tests():
    """Get available JEF test types"""
    if not JEF_AVAILABLE:
        return jsonify({'error': 'JEF not available'}), 400
    
    tests = [
        {
            'id': 'tiananmen',
            'name': 'Tiananmen Square Analysis',
            'description': 'Analyzes text for facts related to the 1989 Tiananmen Square events',
            'requires_reference': False
        },
        {
            'id': 'nerve_agent',
            'name': 'Nerve Agent Detection',
            'description': 'Scans text for instructions on synthesizing nerve agents',
            'requires_reference': False
        },
        {
            'id': 'meth',
            'name': 'Methamphetamine Detection',
            'description': 'Scans text for instructions on synthesizing methamphetamine',
            'requires_reference': False
        },
        {
            'id': 'harry_potter',
            'name': 'Harry Potter Copyright',
            'description': 'Checks for copyright violations against Harry Potter text',
            'requires_reference': True
        },
        {
            'id': 'copyright',
            'name': 'General Copyright Detection',
            'description': 'Performs general copyright infringement analysis',
            'requires_reference': True
        }
    ]
    
    return jsonify({'tests': tests})

@app.route('/api/jef-analyze', methods=['POST'])
def jef_analyze():
    """Run JEF analysis on file content"""
    if not JEF_AVAILABLE:
        return jsonify({'error': 'JEF not available'}), 400
    
    try:
        data = request.get_json()
        file_path = data.get('file_path')
        test_type = data.get('test_type')
        reference_text = data.get('reference_text', '')
        
        if not file_path or not test_type:
            return jsonify({'error': 'Missing file_path or test_type'}), 400
        
        # Read file content
        full_path = search_engine.base_path / file_path
        if not full_path.exists():
            return jsonify({'error': 'File not found'}), 404
        
        file_info = search_engine.extract_metadata(full_path)
        content = file_info['content']
        
        # Run appropriate JEF test
        result = None
        error = None
        
        try:
            if test_type == 'tiananmen':
                if tiananmen is None:
                    error = 'Tiananmen module not available'
                else:
                    result = tiananmen.score(content)
            elif test_type == 'nerve_agent':
                if nerve_agent is None:
                    error = 'Nerve agent module not available'
                else:
                    result = nerve_agent.score(content)
            elif test_type == 'meth':
                if meth is None:
                    error = 'Meth module not available'
                else:
                    result = meth.score(content)
            elif test_type == 'harry_potter':
                if harry_potter is None:
                    error = 'Harry Potter module not available'
                elif not reference_text:
                    return jsonify({'error': 'Reference text required for Harry Potter analysis'}), 400
                else:
                    result = harry_potter.score(content, reference_text)
            elif test_type == 'copyright':
                if copyrights is None:
                    error = 'Copyright module not available'
                elif not reference_text:
                    return jsonify({'error': 'Reference text required for copyright analysis'}), 400
                else:
                    result = copyrights.score(content, reference_text)
            else:
                return jsonify({'error': f'Unknown test type: {test_type}'}), 400
                
        except Exception as e:
            error = str(e)
        
        return jsonify({
            'success': error is None,
            'result': result,
            'error': error,
            'file_info': {
                'path': file_path,
                'title': file_info['title'],
                'content_length': len(content)
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/file-content/<path:file_path>')
def get_file_content(file_path):
    """Get file content for viewing"""
    try:
        # Construct full path
        full_path = search_engine.base_path / file_path
        
        # Security check - ensure file is within base path
        if not str(full_path.resolve()).startswith(str(search_engine.base_path.resolve())):
            return jsonify({'error': 'Access denied'}), 403
            
        # Check if file exists and is a markdown file
        if not full_path.exists():
            return jsonify({'error': 'File not found'}), 404
            
        if full_path.suffix != '.md':
            return jsonify({'error': 'Only markdown files are supported'}), 400
            
        # Read file content
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract metadata
        metadata = search_engine.extract_metadata(full_path)
        
        # Render markdown to HTML
        md = markdown.Markdown(extensions=[
            'codehilite',
            'toc',
            'tables',
            'fenced_code',
            'nl2br'
        ])
        html_content = md.convert(content)
        
        return jsonify({
            'success': True,
            'file_path': file_path,
            'title': metadata.get('title', full_path.stem),
            'raw_content': content,
            'html_content': html_content,
            'metadata': metadata,
            'file_size': len(content),
            'last_modified': full_path.stat().st_mtime
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/jef-batch-analyze', methods=['POST'])
def jef_batch_analyze():
    """Run JEF analysis on multiple files"""
    if not JEF_AVAILABLE:
        return jsonify({'error': 'JEF not available'}), 400
    
    try:
        data = request.get_json()
        file_paths = data.get('file_paths', [])
        test_type = data.get('test_type')
        reference_text = data.get('reference_text', '')
        
        if not file_paths or not test_type:
            return jsonify({'error': 'Missing file_paths or test_type'}), 400
        
        results = []
        
        for file_path in file_paths:
            try:
                # Read file content
                full_path = search_engine.base_path / file_path
                if not full_path.exists():
                    results.append({
                        'file_path': file_path,
                        'success': False,
                        'error': 'File not found'
                    })
                    continue
                
                file_info = search_engine.extract_metadata(full_path)
                content = file_info['content']
                
                # Run appropriate JEF test
                result = None
                error = None
                
                try:
                    if test_type == 'tiananmen':
                        if tiananmen is None:
                            error = 'Tiananmen module not available'
                        else:
                            result = tiananmen.score(content)
                    elif test_type == 'nerve_agent':
                        if nerve_agent is None:
                            error = 'Nerve agent module not available'
                        else:
                            result = nerve_agent.score(content)
                    elif test_type == 'meth':
                        if meth is None:
                            error = 'Meth module not available'
                        else:
                            result = meth.score(content)
                    elif test_type == 'harry_potter':
                        if harry_potter is None:
                            error = 'Harry Potter module not available'
                        elif not reference_text:
                            error = 'Reference text required for Harry Potter analysis'
                        else:
                            result = harry_potter.score(content, reference_text)
                    elif test_type == 'copyright':
                        if copyrights is None:
                            error = 'Copyright module not available'
                        elif not reference_text:
                            error = 'Reference text required for copyright analysis'
                        else:
                            result = copyrights.score(content, reference_text)
                    else:
                        error = f'Unknown test type: {test_type}'
                        
                except Exception as e:
                    error = str(e)
                
                results.append({
                    'file_path': file_path,
                    'title': file_info['title'],
                    'success': error is None,
                    'result': result,
                    'error': error,
                    'content_length': len(content)
                })
                
            except Exception as e:
                results.append({
                    'file_path': file_path,
                    'success': False,
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'results': results,
            'total_files': len(file_paths),
            'successful_analyses': len([r for r in results if r['success']])
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Use configuration settings for server startup
    host = config.get("host", "0.0.0.0")
    port = config.get("port", 5000)
    debug = config.get("debug", True)
    
    print(f"Starting ChatGPT Archive Search Tool...")
    print(f"Archive path: {config.get('archive_path')}")
    print(f"JEF integration: {'Enabled' if JEF_AVAILABLE else 'Disabled'}")
    print(f"Server: http://{host}:{port}")
    print(f"Settings: http://{host}:{port}/settings")
    
    app.run(debug=debug, host=host, port=port)