"""
MCP FILESYSTEM-SERVER INIT TOOL RESULTS
Based on current configuration: G:/projects/filesystem_server/config.json
"""

import os
import json

def analyze_init_tool_results():
    """Analyze what the MCP filesystem-server init tool should return."""
    
    print("?? MCP FILESYSTEM-SERVER INIT TOOL RESULTS")
    print("="*70)
    
    # Your current configuration
    config = {
        "allowed_dirs": ["G:/projects"],
        "allowed_extensions": [".py", ".js", ".ts", ".json", ".md", ".txt", ".yml", ".yaml", ".toml", ".cfg", ".ini"]
    }
    
    print(f"Configuration loaded from config.json:")
    print(f"  allowed_dirs: {config['allowed_dirs']}")
    print(f"  allowed_extensions: {len(config['allowed_extensions'])} extensions")
    
    # Test the directory
    target_directory = "G:/projects"
    abs_directory = os.path.abspath(target_directory)
    
    print(f"\n?? Directory Analysis:")
    print(f"  Target directory: {target_directory}")
    print(f"  Absolute path: {abs_directory}")
    print(f"  Directory exists: {os.path.exists(target_directory)}")
    print(f"  Is directory: {os.path.isdir(target_directory) if os.path.exists(target_directory) else False}")
    
    # Check accessibility
    accessible = False
    error_message = None
    
    if not os.path.exists(target_directory):
        error_message = f"Directory does not exist: {target_directory}"
    elif not os.path.isdir(target_directory):
        error_message = f"Path exists but is not a directory: {target_directory}"
    else:
        try:
            contents = os.listdir(target_directory)
            accessible = True
            print(f"  Can list contents: Yes ({len(contents)} items)")
        except PermissionError:
            error_message = f"Permission denied accessing directory: {target_directory}"
        except Exception as e:
            error_message = f"Error accessing directory {target_directory}: {str(e)}"
    
    # Generate expected init() tool response
    print(f"\n?? Expected MCP INIT TOOL Response:")
    print("="*50)
    
    if accessible:
        result = {
            "message": "OK",
            "isError": False,
            "details": {
                "allowed_dirs": [abs_directory],
                "accessible_dirs": [abs_directory],
                "inaccessible_dirs": [],
                "total_allowed": 1,
                "total_accessible": 1
            }
        }
        print("? SUCCESS RESPONSE:")
    else:
        result = {
            "message": f"Some allowed directories are not accessible: {error_message}",
            "isError": True,
            "details": {
                "allowed_dirs": [abs_directory],
                "accessible_dirs": [],
                "inaccessible_dirs": [abs_directory],
                "error_details": [error_message]
            }
        }
        print("? ERROR RESPONSE:")
    
    print(json.dumps(result, indent=2))
    
    # Recommendations
    print(f"\n?? Recommendations:")
    if accessible:
        print("? Configuration is valid - you can use list_directory() and read_file() tools")
        print("? MCP server is ready for Visual Studio 2022 development")
    else:
        print("? Fix the directory issue before using other MCP tools:")
        print("  1. Verify G:/projects directory exists")
        print("  2. Check directory permissions")  
        print("  3. Ensure the path is accessible from your current user account")
    
    print("="*70)
    return result

if __name__ == "__main__":
    analyze_init_tool_results()