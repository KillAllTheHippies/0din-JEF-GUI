#!/usr/bin/env python3
"""
Debug script to test file tree generation
Run this to see if the file tree logic works
"""

from pathlib import Path
import json

def build_tree(path, max_depth=2, current_depth=0):
    tree = {}
    
    if current_depth >= max_depth:
        return tree
        
    try:
        items = list(path.iterdir())
        print(f"Processing {path}: found {len(items)} items")
        
        for item in items:
            if item.name.startswith('.'):
                continue
            
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
    except Exception as e:
        print(f"Error accessing {path}: {e}")
    
    return tree

if __name__ == "__main__":
    base_path = Path("ChatGPT chats/ChatGPT chats")
    print(f"Base path: {base_path}")
    print(f"Exists: {base_path.exists()}")
    
    if base_path.exists():
        tree = build_tree(base_path)
        print(f"\nGenerated tree with {len(tree)} root items:")
        print(json.dumps(tree, indent=2)[:500] + "...")
    else:
        print("Base path does not exist!")
        print("Current directory contents:")
        for item in Path(".").iterdir():
            print(f"  - {item}")