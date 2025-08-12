"""
FileSystem MCP Server
A secure filesystem access server for MCP clients.
"""

import os
import sys
import json
import argparse
from typing import List, Dict, Any
from mcp.server.fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP(name="FileSystemServer")

def normalize_path(path: str) -> str:
    """
    Normalize a path for cross-platform compatibility.
    
    Handles Windows-style backslashes by converting them to forward slashes,
    resolves relative paths to absolute paths, and normalizes the result.
    
    Args:
        path: The path to normalize (can contain backslashes or forward slashes)
    
    Returns:
        A normalized absolute path
    
    Examples:
        normalize_path("F:\\sd\\wipes") -> "F:/sd/wipes" (on Windows)
        normalize_path("F:/sd/wipes") -> "F:/sd/wipes" 
        normalize_path("./relative/path") -> "/full/absolute/path"
    """
    # Convert backslashes to forward slashes for consistency
    normalized = path.replace('\\', '/')
    
    # Convert to absolute path and normalize
    abs_path = os.path.abspath(normalized)
    
    # Convert back to forward slashes (os.path.abspath might add backslashes on Windows)
    return abs_path.replace('\\', '/')

def parse_arguments():
    """Parse command line arguments for configuration."""
    parser = argparse.ArgumentParser(
        description="FileSystem MCP Server - Secure filesystem access for AI assistants",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Using command line arguments (for MCP clients):
  python app.py --allowed-dirs "D:/projects" "D:/Webs" --allowed-extensions ".py" ".js" ".md"
  
  # Using config.json fallback (for debugging in Visual Studio):
  python app.py
  
  # Show MCP configuration help:
  python app.py --help-mcp
  
Note: Paths can use either forward slashes (/) or backslashes (\) - they will be automatically normalized.
        """
    )
    
    parser.add_argument(
        '--allowed-dirs', '--allowed_dirs',
        nargs='*',
        help='List of allowed directory paths (e.g., --allowed-dirs "D:/projects" "D:\\Webs")',
        required=False,
        default=None
    )
    
    parser.add_argument(
        '--allowed-extensions', '--allowed_extensions',
        nargs='*', 
        help='List of allowed file extensions (e.g., --allowed-extensions ".py" ".js" ".md")',
        required=False,
        default=None
    )
    
    parser.add_argument(
        '--config',
        help='Path to config.json file (default: ./config.json)',
        default='config.json'
    )
    
    parser.add_argument(
        '--help-mcp',
        action='store_true',
        help='Show MCP client configuration examples'
    )
    
    return parser.parse_args()

def load_configuration():
    """Load configuration from command line arguments or config.json fallback."""
    args = parse_arguments()
    
    if args.help_mcp:
        show_mcp_help()
        sys.exit(0)
    
    # Priority: command line arguments > config.json > defaults
    allowed_dirs = []
    allowed_extensions = []
    config_source = "none"
    
    # Try command line arguments first
    # Fix: Check if args are provided AND have content, not just not None
    if args.allowed_dirs is not None and len(args.allowed_dirs) > 0:
        # Normalize all directory paths for cross-platform compatibility
        allowed_dirs = [normalize_path(d) for d in args.allowed_dirs]
        config_source = "command_line_args"
        print(f"[OK] Using allowed_dirs from command line: {args.allowed_dirs}")
        print(f"[OK] Normalized paths: {allowed_dirs}")
    
    if args.allowed_extensions is not None and len(args.allowed_extensions) > 0:
        allowed_extensions = [ext.lower() for ext in args.allowed_extensions]
        if config_source != "command_line_args":
            config_source = "command_line_args"
        print(f"[OK] Using allowed_extensions from command line: {args.allowed_extensions}")
    
    # Fallback to config.json if command-line args not provided OR empty
    if not allowed_dirs or not allowed_extensions:
        try:
            with open(args.config, 'r') as f:
                config = json.load(f)
            
            if not allowed_dirs:
                config_dirs = config.get('allowed_dirs', [])
                # Normalize all directory paths from config file too
                allowed_dirs = [normalize_path(d) for d in config_dirs]
                if allowed_dirs:
                    if config_source == "none":
                        config_source = "config_file"
                    print(f"[FILE] Using allowed_dirs from {args.config}: {config_dirs}")
                    print(f"[FILE] Normalized paths: {allowed_dirs}")
            
            if not allowed_extensions:
                allowed_extensions = [ext.lower() for ext in config.get('allowed_extensions', [])]
                if allowed_extensions:
                    if config_source == "none":
                        config_source = "config_file"
                    print(f"[FILE] Using allowed_extensions from {args.config}: {config.get('allowed_extensions', [])}")
                    
        except FileNotFoundError:
            if not allowed_dirs and not allowed_extensions:
                print(f"[WARN] {args.config} not found and no command line arguments provided.")
                print("   For debugging in Visual Studio 2022: Create config.json file")
                print("   For MCP clients: Use command line arguments")
                print("   Note: Paths can use either forward slashes (/) or backslashes (\\)")
        except Exception as e:
            print(f"[ERROR] Error loading {args.config}: {e}. Using command line args or defaults.")
    
    # Show warnings for missing configuration
    if not allowed_dirs:
        print("[WARN] No allowed directories configured")
        print("   For debugging: Create config.json or use --allowed-dirs")
        print("   For MCP: Add --allowed-dirs to your MCP client configuration")
        print("   Note: Paths can use either forward slashes (/) or backslashes (\\)")
    
    if not allowed_extensions:
        print("[WARN] No allowed extensions configured")
        print("   For debugging: Create config.json or use --allowed-extensions")
        print("   For MCP: Add --allowed-extensions to your MCP client configuration")
    
    return allowed_dirs, allowed_extensions, config_source

def show_mcp_help():
    """Show MCP client configuration examples."""
    current_dir = os.getcwd()
    
    print("FILESYSTEM MCP SERVER - CLIENT CONFIGURATION EXAMPLES")
    print("="*70)
    
    print("\nCorrected Configuration for Your Setup:")
    print("-" * 50)
    print('''{
  "filesystem-server": {
    "command": "python",
    "args": [
      "''' + os.path.join(current_dir, "app.py").replace(os.sep, "/") + '''",
      "--allowed-dirs", "D:/projects", "D:/Webs",
      "--allowed-extensions", ".py", ".js", ".ts", ".json", ".md", ".txt", ".yml", ".yaml", ".toml", ".cfg", ".ini", ".css", ".scss", ".htm", ".html"
    ],
    "cwd": "''' + current_dir.replace(os.sep, "/") + '''"
  }
}''')
    
    print("\nWindows Users - Both Path Formats Work:")
    print("-" * 50)  
    print("[OK] Forward slashes:  \"D:/projects\", \"F:/sd/wipes\"")
    print("[OK] Backslashes:     \"D:\\\\projects\", \"F:\\\\sd\\\\wipes\"")
    print("[OK] Mixed formats:    \"D:/projects\", \"F:\\\\sd\\\\wipes\"")
    print("   (Paths are automatically normalized)")
    
    print("\nAlternative: Debugging Configuration (uses config.json):")
    print("-" * 50)
    print('''{
  "filesystem-server": {
    "command": "python",
    "args": ["''' + os.path.join(current_dir, "app.py").replace(os.sep, "/") + '''"],
    "cwd": "''' + current_dir.replace(os.sep, "/") + '''"
  }
}''')
    
    print("\nConfiguration Options:")
    print("  [OK] Command-line args: Best for MCP clients")
    print("  [OK] config.json fallback: Perfect for Visual Studio 2022 debugging")
    print("  [OK] Hybrid approach: Works for both scenarios")
    print("  [OK] Path normalization: Handles both / and \\ automatically")
    print("  [OK] No config file conflicts: Priority system handles both")
    
    print("="*70)

# Load configuration
allowed_dirs, allowed_extensions, config_source = load_configuration()

def is_allowed_path(path: str) -> bool:
    """Check if the given path is within one of the allowed directories."""
    if not allowed_dirs:
        return False
    
    # Normalize the input path for consistent comparison
    normalized_path = normalize_path(path)
    
    for allowed in allowed_dirs:
        try:
            # Both paths are now normalized, so comparison should work reliably
            if os.path.commonpath([normalized_path, allowed]) == allowed:
                return True
        except ValueError:
            # Paths on different drives on Windows
            continue
    return False

@mcp.tool()
def init() -> Dict[str, Any]:
    """
    Initialize and verify accessibility of allowed directories.
    
    Returns:
        A dictionary containing:
        - message: Status message ("OK" if all directories accessible, error description if not)
        - isError: Boolean indicating if there was an error
        - details: Additional information about directory accessibility
    """
    if not allowed_dirs:
        return {
            "message": "No allowed directories configured. Use --allowed-dirs argument or create config.json for debugging.",
            "isError": True,
            "details": {
                "allowed_dirs": allowed_dirs,
                "accessible_dirs": [],
                "inaccessible_dirs": [],
                "configuration_source": config_source,
                "help": "For MCP: Add --allowed-dirs argument. For debugging: Create config.json file. Paths can use / or \\ separators."
            }
        }
    
    if not allowed_extensions:
        return {
            "message": "No allowed extensions configured. Use --allowed-extensions argument or create config.json for debugging.",
            "isError": True,
            "details": {
                "allowed_dirs": allowed_dirs,
                "allowed_extensions": allowed_extensions,
                "accessible_dirs": [],
                "inaccessible_dirs": [],
                "configuration_source": config_source,
                "help": "For MCP: Add --allowed-extensions argument. For debugging: Create config.json file."
            }
        }
    
    accessible_dirs = []
    inaccessible_dirs = []
    error_details = []
    
    for directory in allowed_dirs:
        try:
            # Check if directory exists (directory is already normalized)
            if not os.path.exists(directory):
                inaccessible_dirs.append(directory)
                error_details.append(f"Directory does not exist: {directory}")
                continue
            
            # Check if it's actually a directory
            if not os.path.isdir(directory):
                inaccessible_dirs.append(directory)
                error_details.append(f"Path exists but is not a directory: {directory}")
                continue
            
            # Check if we can read the directory
            try:
                os.listdir(directory)
                accessible_dirs.append(directory)
            except PermissionError:
                inaccessible_dirs.append(directory)
                error_details.append(f"Permission denied accessing directory: {directory}")
            except Exception as e:
                inaccessible_dirs.append(directory)
                error_details.append(f"Error accessing directory {directory}: {str(e)}")
                
        except Exception as e:
            inaccessible_dirs.append(directory)
            error_details.append(f"Unexpected error checking directory {directory}: {str(e)}")
    
    # Determine if there are any errors
    has_errors = len(inaccessible_dirs) > 0
    
    if has_errors:
        error_message = f"Some allowed directories are not accessible: {', '.join(error_details)}"
        return {
            "message": error_message,
            "isError": True,
            "details": {
                "allowed_dirs": allowed_dirs,
                "allowed_extensions": allowed_extensions,
                "accessible_dirs": accessible_dirs,
                "inaccessible_dirs": inaccessible_dirs,
                "error_details": error_details,
                "configuration_source": config_source
            }
        }
    else:
        return {
            "message": "OK",
            "isError": False,
            "details": {
                "allowed_dirs": allowed_dirs,
                "allowed_extensions": allowed_extensions,
                "accessible_dirs": accessible_dirs,
                "inaccessible_dirs": inaccessible_dirs,
                "total_allowed": len(allowed_dirs),
                "total_accessible": len(accessible_dirs),
                "configuration_source": config_source,
                "path_normalization": "Enabled - accepts both / and \\ path separators"
            }
        }

@mcp.tool()
def list_directory(directory: str) -> List[str]:
    """
    List files and subdirectories in the given directory.
    
    Args:
        directory: The absolute or relative path to the directory (supports both / and \\ separators).
    
    Returns:
        A list of file and directory names in the directory.
    
    Raises:
        ValueError: If the directory is not allowed or does not exist.
    """
    # Normalize the path to handle both Windows and Unix style separators
    normalized_dir = normalize_path(directory)
    
    if not is_allowed_path(directory):
        raise ValueError(f"Access to this directory is not allowed. Requested: {directory}, Normalized: {normalized_dir}")
    
    if not os.path.isdir(normalized_dir):
        raise ValueError(f"The provided path is not a directory or does not exist: {normalized_dir}")
    
    return os.listdir(normalized_dir)

@mcp.tool()
def read_file(file_path: str) -> str:
    """
    Read the content of a file.
    
    Args:
        file_path: The absolute or relative path to the file (supports both / and \\ separators).
    
    Returns:
        The text content of the file.
    
    Raises:
        ValueError: If the file is not allowed, does not exist, or has a disallowed extension.
    """
    # Normalize the path to handle both Windows and Unix style separators
    normalized_file = normalize_path(file_path)
    
    if not is_allowed_path(file_path):
        raise ValueError(f"Access to this file is not allowed. Requested: {file_path}, Normalized: {normalized_file}")
    
    if not os.path.isfile(normalized_file):
        raise ValueError(f"The provided path is not a file or does not exist: {normalized_file}")
    
    ext = os.path.splitext(normalized_file)[1].lower()
    if ext not in allowed_extensions:
        raise ValueError(f"This file type '{ext}' is not allowed for reading. Allowed extensions: {allowed_extensions}")
    
    with open(normalized_file, 'r', encoding='utf-8') as f:
        return f.read()

def print_connection_info():
    """Print server connection information."""
    current_dir = os.getcwd()
    python_path = sys.executable
    
    print("\n" + "="*60)
    print("FILESYSTEM MCP SERVER CONNECTION INFO")
    print("="*60)
    print(f"Server Name: FileSystemServer")
    print(f"Server Directory: {current_dir}")
    print(f"Python Path: {python_path}")
    print(f"Configuration Source: {config_source}")
    print(f"Transport: stdio (Standard Input/Output)")
    print(f"Path Normalization: [ENABLED] (supports both / and \\ separators)")
    
    if config_source == "config_file":
        print("\n[DEBUG] DEBUGGING MODE (using config.json)")
        print("Perfect for Visual Studio 2022 development!")
    else:
        print("\nMCP Client Configuration:")
        print("Add this to your MCP client configuration:")
        print("-" * 40)
        print(f'{{')
        print(f'  "filesystem-server": {{')
        print(f'    "command": "python",')
        print(f'    "args": [')
        print(f'      "{os.path.join(current_dir, "app.py").replace(os.sep, "/")}",')
        print(f'      "--allowed-dirs", "D:/projects", "D:/Webs",')
        print(f'      "--allowed-extensions", ".py", ".js", ".ts", ".json", ".md", ".txt", ".css", ".html"')
        print(f'    ],')
        print(f'    "cwd": "{current_dir.replace(os.sep, "/")}"')
        print(f'  }}')
        print(f'}}')
    
    print("-" * 40)
    print("\nUsage Instructions:")
    print("1. For MCP clients: Use command-line arguments (recommended)")
    print("2. For Visual Studio 2022 debugging: Uses config.json fallback")
    print("3. Available tools: init(), list_directory(), read_file()")
    print("4. Use --help-mcp for more configuration examples")
    print("5. Path formats: Both D:/path and D:\\path work automatically")
    print("="*60)

def main():
    """Main entry point for the server."""
    print(f"Starting MCP server with allowed dirs: {allowed_dirs}")
    print(f"Allowed extensions: {allowed_extensions}")
    print(f"Configuration source: {config_source}")
    
    # Allow server to start even without configuration for debugging purposes
    if not allowed_dirs or not allowed_extensions:
        print("\n[WARN] CONFIGURATION WARNING:")
        print("Server starting with limited configuration.")
        if config_source == "none":
            print("For debugging: Create config.json file or use command line arguments")
            print("For MCP clients: Ensure arguments are passed correctly")
        print("Use init() tool to validate configuration.")
    
    print_connection_info()
    mcp.run()

if __name__ == "__main__":
    main()