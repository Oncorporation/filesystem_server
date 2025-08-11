#!/usr/bin/env python3
"""
Test script for FileSystem MCP Server functions.
This script tests the list_directory and read_file functions.
"""

import os
import json
import sys
from typing import List

# Import the functions from app.py
sys.path.append('.')
from app import list_directory, read_file, is_allowed_path, allowed_dirs, allowed_extensions

def test_list_directory():
    """Test the list_directory function."""
    test_directory = "D:/Projects/modal_mcp_server"
    
    print("="*60)
    print("?? TESTING LIST_DIRECTORY FUNCTION")
    print("="*60)
    print(f"Test directory: {test_directory}")
    print(f"Allowed directories: {allowed_dirs}")
    print(f"Is path allowed: {is_allowed_path(test_directory)}")
    print("-" * 60)
    
    try:
        result = list_directory(test_directory)
        print(f"? SUCCESS: Found {len(result)} items in directory")
        print("\n?? Directory contents:")
        for i, item in enumerate(result[:10], 1):  # Show first 10 items
            print(f"  {i}. {item}")
        if len(result) > 10:
            print(f"  ... and {len(result) - 10} more items")
        return result
    except Exception as e:
        print(f"? ERROR: {e}")
        return None

def test_read_file():
    """Test the read_file function."""
    test_file = "D:/Projects/modal_mcp_server/mcp_client.py"
    
    print("\n" + "="*60)
    print("?? TESTING READ_FILE FUNCTION")
    print("="*60)
    print(f"Test file: {test_file}")
    print(f"Allowed extensions: {allowed_extensions}")
    print(f"File extension: {os.path.splitext(test_file)[1].lower()}")
    print(f"Is path allowed: {is_allowed_path(test_file)}")
    print(f"File exists: {os.path.exists(test_file)}")
    print(f"Is file: {os.path.isfile(test_file) if os.path.exists(test_file) else 'N/A'}")
    print("-" * 60)
    
    try:
        content = read_file(test_file)
        print(f"? SUCCESS: File read successfully")
        print(f"?? File size: {len(content)} characters")
        print(f"?? Number of lines: {len(content.splitlines())}")
        
        # Show first few lines of content
        lines = content.splitlines()
        print("\n?? File content preview (first 10 lines):")
        for i, line in enumerate(lines[:10], 1):
            print(f"  {i:2d}: {line[:80]}{' ...' if len(line) > 80 else ''}")
        
        if len(lines) > 10:
            print(f"  ... and {len(lines) - 10} more lines")
            
        return content
    except Exception as e:
        print(f"? ERROR: {e}")
        return None

def main():
    """Run the tests."""
    print("??? FILESYSTEM MCP SERVER - FUNCTION TESTS")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Config loaded - Allowed dirs: {len(allowed_dirs)}, Allowed extensions: {len(allowed_extensions)}")
    
    # Test 1: list_directory
    directory_result = test_list_directory()
    
    # Test 2: read_file
    file_result = test_read_file()
    
    # Summary
    print("\n" + "="*60)
    print("?? TEST SUMMARY")
    print("="*60)
    print(f"List Directory Test: {'? PASSED' if directory_result is not None else '? FAILED'}")
    print(f"Read File Test: {'? PASSED' if file_result is not None else '? FAILED'}")
    print("="*60)

if __name__ == "__main__":
    main()