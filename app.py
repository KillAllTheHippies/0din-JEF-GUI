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

# Add JEF to Python path
JEF_PATH = Path("K:/0din/0din-JEF")
if JEF_PATH.exists():
    sys.path.insert(0, str(JEF_PATH))
    try:
        from jef import tiananmen, nerve_agent, meth, harry_potter, copyrights
        JEF_AVAILABLE = True
        print("JEF integration loaded successfully")
    except ImportError as e:
        JEF_AVAILABLE = False
        print(f"JEF not available: {e}")
else:
    JEF_AVAILABLE = False
    print(f"JEF path not found: {JEF_PATH}")

app = Flask(__name__)

class ChatSearchEngine:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        print(f"Initializing search engine with path: {self.base_path}")
        
    def extract_metadata(self, file_path):
        """Extract YAML frontmatter and basic file info"""
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
            
            # Extract title from content or filename
            title = metadata.get('aliases', '')
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
    
    def search_in_content(self, content, search_terms, mode='ALL', case_sensitive=False):
        """Search for terms in content"""
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
    
    def search(self, query_data):
        """Main search function"""
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

# Initialize search engine
search_engine = ChatSearchEngine("ChatGPT chats/ChatGPT chats")

@app.route('/')
def index():
    """Main search interface"""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """AJAX search endpoint"""
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
    """Get file tree structure for sidebar"""
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
                result = tiananmen.score(content)
            elif test_type == 'nerve_agent':
                result = nerve_agent.score(content)
            elif test_type == 'meth':
                result = meth.score(content)
            elif test_type == 'harry_potter':
                if not reference_text:
                    return jsonify({'error': 'Reference text required for Harry Potter analysis'}), 400
                result = harry_potter.score(content, reference_text)
            elif test_type == 'copyright':
                if not reference_text:
                    return jsonify({'error': 'Reference text required for copyright analysis'}), 400
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
                        result = tiananmen.score(content)
                    elif test_type == 'nerve_agent':
                        result = nerve_agent.score(content)
                    elif test_type == 'meth':
                        result = meth.score(content)
                    elif test_type == 'harry_potter':
                        if not reference_text:
                            error = 'Reference text required for Harry Potter analysis'
                        else:
                            result = harry_potter.score(content, reference_text)
                    elif test_type == 'copyright':
                        if not reference_text:
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
    app.run(debug=True, host='0.0.0.0', port=5000)