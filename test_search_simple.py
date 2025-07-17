#!/usr/bin/env python3
"""
Simple command-line version of the ChatGPT archive search tool
This version doesn't require Flask and can be run directly
"""

import os
import re
from pathlib import Path
import json
import csv
from datetime import datetime

class SimpleChatSearch:
    def __init__(self, base_path="ChatGPT chats/ChatGPT chats"):
        self.base_path = Path(base_path)
        print(f"Searching in: {self.base_path.absolute()}")
        
    def extract_title_from_file(self, file_path):
        """Extract title from markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for title in YAML frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    yaml_section = parts[1]
                    # Simple regex to find aliases (title)
                    title_match = re.search(r'aliases:\s*["\']([^"\']+)["\']', yaml_section)
                    if title_match:
                        return title_match.group(1)
            
            # Look for title in content
            title_match = re.search(r'^# Title: (.+)$', content, re.MULTILINE)
            if title_match:
                return title_match.group(1)
            
            # Use filename as fallback
            return file_path.stem
            
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return file_path.stem
    
    def search_files(self, search_terms, mode="ALL", exclude_terms="", case_sensitive=False):
        """Search for terms in markdown files"""
        if not search_terms.strip():
            return []
        
        results = []
        
        # Find all markdown files
        try:
            md_files = list(self.base_path.rglob("*.md"))
            print(f"Found {len(md_files)} markdown files to search")
        except Exception as e:
            print(f"Error accessing directory: {e}")
            return []
        
        # Prepare search terms
        terms = [term.strip().strip('"') for term in search_terms.split() if term.strip()]
        exclude_list = [term.strip() for term in exclude_terms.split() if term.strip()] if exclude_terms else []
        
        if not case_sensitive:
            terms = [term.lower() for term in terms]
            exclude_list = [term.lower() for term in exclude_list]
        
        for file_path in md_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Prepare content for searching
                search_content = content if case_sensitive else content.lower()
                
                # Count matches for each term
                found_terms = []
                total_matches = 0
                
                for term in terms:
                    if term in search_content:
                        matches = len(re.findall(re.escape(term), search_content))
                        found_terms.append(term)
                        total_matches += matches
                
                # Apply search mode logic
                has_match = False
                if mode == "ALL":
                    has_match = len(found_terms) == len(terms)
                else:  # ANY
                    has_match = len(found_terms) > 0
                
                # Check exclude terms
                if has_match and exclude_list:
                    for exclude_term in exclude_list:
                        if exclude_term in search_content:
                            has_match = False
                            break
                
                if has_match:
                    title = self.extract_title_from_file(file_path)
                    relative_path = str(file_path.relative_to(self.base_path))
                    
                    results.append({
                        'path': relative_path,
                        'title': title,
                        'matches': total_matches,
                        'found_terms': found_terms,
                        'file_size': file_path.stat().st_size,
                        'modified_date': datetime.fromtimestamp(file_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
                    })
                    
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                continue
        
        # Sort by number of matches (descending)
        results.sort(key=lambda x: x['matches'], reverse=True)
        return results
    
    def export_to_csv(self, results, filename="search_results.csv"):
        """Export results to CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['File Path', 'Title', 'Matches', 'Found Terms', 'File Size', 'Modified Date'])
            
            for result in results:
                writer.writerow([
                    result['path'],
                    result['title'],
                    result['matches'],
                    ', '.join(result['found_terms']),
                    result['file_size'],
                    result['modified_date']
                ])
        
        print(f"Results exported to {filename}")
    
    def export_to_json(self, results, search_info, filename="search_results.json"):
        """Export results to JSON"""
        export_data = {
            'search_info': search_info,
            'timestamp': datetime.now().isoformat(),
            'total_results': len(results),
            'results': results
        }
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(export_data, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"Results exported to {filename}")

def main():
    """Interactive command-line interface"""
    print("=" * 60)
    print("ChatGPT Archive Search Tool - Command Line Version")
    print("=" * 60)
    
    # Initialize search engine
    search_engine = SimpleChatSearch()
    
    while True:
        print("\n" + "-" * 40)
        print("Search Options:")
        print("1. Perform new search")
        print("2. Exit")
        
        choice = input("\nEnter your choice (1-2): ").strip()
        
        if choice == "2":
            print("Goodbye!")
            break
        elif choice == "1":
            # Get search parameters
            search_terms = input("\nEnter search terms: ").strip()
            if not search_terms:
                print("Please enter some search terms.")
                continue
            
            print("\nSearch mode:")
            print("1. ALL terms (AND)")
            print("2. ANY terms (OR)")
            mode_choice = input("Choose mode (1-2, default 1): ").strip()
            mode = "ANY" if mode_choice == "2" else "ALL"
            
            exclude_terms = input("Exclude terms (optional): ").strip()
            
            case_choice = input("Case sensitive? (y/N): ").strip().lower()
            case_sensitive = case_choice == 'y'
            
            # Perform search
            print(f"\nSearching for: '{search_terms}' (mode: {mode})")
            if exclude_terms:
                print(f"Excluding: '{exclude_terms}'")
            
            results = search_engine.search_files(
                search_terms, mode, exclude_terms, case_sensitive
            )
            
            # Display results
            print(f"\nFound {len(results)} matching files:")
            print("-" * 80)
            
            for i, result in enumerate(results[:10], 1):  # Show top 10
                print(f"{i:2d}. {result['title']}")
                print(f"    Path: {result['path']}")
                print(f"    Matches: {result['matches']}, Size: {result['file_size']} bytes")
                print(f"    Modified: {result['modified_date']}")
                print()
            
            if len(results) > 10:
                print(f"... and {len(results) - 10} more results")
            
            # Export options
            if results:
                export_choice = input("\nExport results? (csv/json/n): ").strip().lower()
                if export_choice == "csv":
                    search_engine.export_to_csv(results)
                elif export_choice == "json":
                    search_info = {
                        'terms': search_terms,
                        'mode': mode,
                        'exclude': exclude_terms,
                        'case_sensitive': case_sensitive
                    }
                    search_engine.export_to_json(results, search_info)
        else:
            print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()