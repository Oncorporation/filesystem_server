#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for the new init() tool in FileSystem MCP Server.
This script tests the init function to verify directory accessibility.
"""

import os
import json
import sys
from typing import Dict, Any

# Import the functions from app.py
sys.path.append('.')
from app import init, allowed_dirs, allowed_extensions

def test_init_tool():
    """Test the new init() tool."""
    
    print("?? TESTING INIT() TOOL")
    print("="*60)
    print(f"Current allowed directories: {allowed_dirs}")
    print(f"Current allowed extensions: {len(allowed_extensions)} extensions")
    print("-" * 60)
    
    try:
        # Call the init tool
        result = init()
        
        print("? INIT TOOL EXECUTED SUCCESSFULLY")
        print(f"Message: {result['message']}")
        print(f"Is Error: {result['isError']}")
        
        if result['isError']:
            print("? INITIALIZATION FAILED")
            print("\n?? Error Details:")
            details = result.get('details', {})
            
            if 'error_details' in details:
                for error in details['error_details']:
                    print(f"  * {error}")
            
            if 'inaccessible_dirs' in details:
                print(f"\n?? Inaccessible Directories ({len(details['inaccessible_dirs'])}):")
                for directory in details['inaccessible_dirs']:
                    print(f"  ? {directory}")
            
            if 'accessible_dirs' in details:
                print(f"\n? Accessible Directories ({len(details['accessible_dirs'])}):")
                for directory in details['accessible_dirs']:
                    print(f"  ? {directory}")
        
        else:
            print("? ALL DIRECTORIES ACCESSIBLE")
            details = result.get('details', {})
            
            print(f"\n?? Summary:")
            print(f"  Total allowed directories: {details.get('total_allowed', 0)}")
            print(f"  Total accessible directories: {details.get('total_accessible', 0)}")
            
            print(f"\n?? Accessible Directories:")
            for directory in details.get('accessible_dirs', []):
                print(f"  ? {directory}")
        
        print("\n?? Full Response:")
        print(json.dumps(result, indent=2))
        
        return result
        
    except Exception as e:
        print(f"? ERROR TESTING INIT TOOL: {e}")
        return None

def test_directory_scenarios():
    """Test various directory scenarios."""
    
    print("\n" + "="*60)
    print("?? TESTING DIRECTORY SCENARIOS")
    print("="*60)
    
    # Test if G:/projects exists
    test_dir = "G:/projects"
    print(f"\n?? Testing directory: {test_dir}")
    print(f"  Exists: {os.path.exists(test_dir)}")
    print(f"  Is directory: {os.path.isdir(test_dir) if os.path.exists(test_dir) else 'N/A'}")
    
    if os.path.exists(test_dir) and os.path.isdir(test_dir):
        try:
            contents = os.listdir(test_dir)
            print(f"  Can list: Yes ({len(contents)} items)")
            print(f"  Sample contents: {contents[:3]}{'...' if len(contents) > 3 else ''}")
        except Exception as e:
            print(f"  Can list: No - {e}")

def main():
    """Run the init tool tests."""
    print("??? FILESYSTEM MCP SERVER - INIT TOOL TEST")
    print(f"Current working directory: {os.getcwd()}")
    
    # Test 1: Test the init tool
    init_result = test_init_tool()
    
    # Test 2: Test directory scenarios
    test_directory_scenarios()
    
    # Summary
    print("\n" + "="*60)
    print("?? TEST SUMMARY")
    print("="*60)
    
    if init_result:
        status = "? PASSED" if not init_result['isError'] else "?? COMPLETED WITH ERRORS"
        print(f"Init Tool Test: {status}")
        
        if init_result['isError']:
            print("?? Recommendation: Check directory paths in config.json")
            print("   * Verify directories exist")
            print("   * Check directory permissions")
            print("   * Ensure paths use correct format for your OS")
        else:
            print("?? All directories are accessible and ready for use!")
    else:
        print("Init Tool Test: ? FAILED")
    
    print("="*60)

if __name__ == "__main__":
    main()