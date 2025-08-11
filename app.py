"""
FileSystem MCP Server
A secure filesystem access server for MCP clients.
"""

import os
import json
import sys
from typing import List
from mcp.server.fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP(name="FileSystemServer")

# Load configuration
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
    allowed_dirs = [os.path.abspath(d) for d in config.get('allowed_dirs', [])]
    allowed_extensions = [ext.lower() for ext in config.get('allowed_extensions', [])]
except FileNotFoundError:
    print("config.json not found. Using empty configuration - no paths allowed.")
    allowed_dirs = []
    allowed_extensions = []
except Exception as e:
    print(f"Error loading config: {e}. Using empty configuration.")
    allowed_dirs = []
    allowed_extensions = []

def is_allowed_path(path: str) -> bool:
    """Check if the given path is within one of the allowed directories."""
    abs_path = os.path.abspath(path)
    for allowed in allowed_dirs:
        if os.path.commonpath([abs_path, allowed]) == allowed:
            return True
    return False

@mcp.tool()
def list_directory(directory: str) -> List[str]:
    """
    List files and subdirectories in the given directory.
    
    Args:
        directory: The absolute or relative path to the directory.
    
    Returns:
        A list of file and directory names in the directory.
    
    Raises:
        ValueError: If the directory is not allowed or does not exist.
    """
    if not is_allowed_path(directory):
        raise ValueError("Access to this directory is not allowed.")
    if not os.path.isdir(directory):
        raise ValueError("The provided path is not a directory or does not exist.")
    return os.listdir(directory)

@mcp.tool()
def read_file(file_path: str) -> str:
    """
    Read the content of a file.
    
    Args:
        file_path: The absolute or relative path to the file.
    
    Returns:
        The text content of the file.
    
    Raises:
        ValueError: If the file is not allowed, does not exist, or has a disallowed extension.
    """
    if not is_allowed_path(file_path):
        raise ValueError("Access to this file is not allowed.")
    if not os.path.isfile(file_path):
        raise ValueError("The provided path is not a file or does not exist.")
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in allowed_extensions:
        raise ValueError("This file type is not allowed for reading.")
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def print_connection_info():
    """Print server connection information."""
    current_dir = os.getcwd()
    python_path = sys.executable
    
    print("\n" + "="*60)
    print("???  FILESYSTEM MCP SERVER CONNECTION INFO")
    print("="*60)
    print(f"Server Name: FileSystemServer")
    print(f"Server Directory: {current_dir}")
    print(f"Python Path: {python_path}")
    print(f"Transport: stdio (Standard Input/Output)")
    print("\n?? MCP Client Configuration:")
    print("Add this to your MCP client configuration:")
    print("-" * 40)
    print(f'{{')
    print(f'  "mcpServers": {{')
    print(f'    "filesystem-server": {{')
    print(f'      "command": "uv",')
    print(f'      "args": ["run", "app.py"],')
    print(f'      "cwd": "{current_dir.replace(os.sep, "/")}"')
    print(f'    }}')
    print(f'  }}')
    print(f'}}')
    print("-" * 40)
    print("\n?? Alternative configuration (direct Python):")
    print("-" * 40)
    print(f'{{')
    print(f'  "mcpServers": {{')
    print(f'    "filesystem-server": {{')
    print(f'      "command": "{python_path.replace(os.sep, "/")}",')
    print(f'      "args": ["{os.path.join(current_dir, "app.py").replace(os.sep, "/")}"],')
    print(f'      "cwd": "{current_dir.replace(os.sep, "/")}"')
    print(f'    }}')
    print(f'  }}')
    print(f'}}')
    print("-" * 40)
    print("\n?? Usage Instructions:")
    print("1. Add the configuration above to your MCP client")
    print("2. The server communicates via stdio (stdin/stdout)")
    print("3. Available tools: list_directory(), read_file()")
    print("4. Server will respect the allowed_dirs and allowed_extensions in config.json")
    print("="*60)

def main():
    """Main entry point for the server."""
    print(f"Starting MCP server with allowed dirs: {allowed_dirs}")
    print(f"Allowed extensions: {allowed_extensions}")
    print_connection_info()
    mcp.run()

if __name__ == "__main__":
    main()