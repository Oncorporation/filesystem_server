"""
FileSystem MCP Server
A secure filesystem access server for MCP clients.
"""

import os
import sys
import json
import argparse
import time
import base64
import datetime
from typing import List, Dict, Any, Optional, Callable
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
  
Note: Paths can use either forward slashes (/) or backslashes (\\) - they will be automatically normalized.
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
            with open(args.config, 'r', encoding='utf-8') as f:
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
    """
    Check if the given path is within one of the allowed directories.
    This check is case-insensitive on Windows.
    """
    if not allowed_dirs:
        return False
    
    # Normalize the input path for consistent comparison
    normalized_path = normalize_path(path)
    
    for allowed in allowed_dirs:
        # For Windows, compare paths case-insensitively
        if os.name == 'nt':
            if normalized_path.lower().startswith(allowed.lower()):
                return True
        else:
            # For other OS, use case-sensitive comparison
            if normalized_path.startswith(allowed):
                return True
    return False

@mcp.tool()
def init(directory: str, file_path: str ) -> Dict[str, Any]:
    """
    Initialize and verify accessibility of allowed directories.
    Optionally list a directory and/or read a file if parameters are provided.
    
    Args:
        directory: Optional directory path to list contents
        file_path: Optional file path to read content
    
    Returns:
        A dictionary containing:
        - message: Status message ("OK" if all directories accessible, error description if not)
        - isError: Boolean indicating if there was an error
        - details: Additional information about directory accessibility
        - directory_contents: Optional list of directory contents if directory parameter provided
        - file_content: Optional file content if file_path parameter provided
    """
    # Start with the standard init validation
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
    
    for directory_path in allowed_dirs:
        try:
            # Check if directory exists (directory is already normalized)
            if not os.path.exists(directory_path):
                inaccessible_dirs.append(directory_path)
                error_details.append(f"Directory does not exist: {directory_path}")
                continue
            
            # Check if it's actually a directory
            if not os.path.isdir(directory_path):
                inaccessible_dirs.append(directory_path)
                error_details.append(f"Path exists but is not a directory: {directory_path}")
                continue
            
            # Check if we can read the directory
            try:
                os.listdir(directory_path)
                accessible_dirs.append(directory_path)
            except PermissionError:
                inaccessible_dirs.append(directory_path)
                error_details.append(f"Permission denied accessing directory: {directory_path}")
            except Exception as e:
                inaccessible_dirs.append(directory_path)
                error_details.append(f"Error accessing directory {directory_path}: {str(e)}")
                
        except Exception as e:
            inaccessible_dirs.append(directory_path)
            error_details.append(f"Unexpected error checking directory {directory_path}: {str(e)}")
    
    # Determine if there are any errors
    has_errors = len(inaccessible_dirs) > 0
    
    # Build the base response
    if has_errors:
        error_message = f"Some allowed directories are not accessible: {', '.join(error_details)}"
        response = {
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
        response = {
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
    
    # If directory parameter is provided, call list_directory
    if directory is not None:
        try:
            directory_contents = list_directory(directory, report_progress=True)
            
            # Handle the new return format from list_directory
            if isinstance(directory_contents, dict):
                if directory_contents.get("error", False):
                    response["directory_error"] = directory_contents.get("error_message", "Unknown directory error")
                    response["directory_progress_info"] = directory_contents.get("progress_info", {})
                else:
                    response["directory_contents"] = directory_contents.get("contents", [])
                    response["directory_total_items"] = directory_contents.get("total_items", 0)
                    response["directory_processing_time"] = directory_contents.get("processing_time", 0)
                    response["directory_progress_info"] = directory_contents.get("progress_info", {})
                    response["directory_listed"] = directory
            else:
                # Handle backward compatibility with list return
                if directory_contents and len(directory_contents) > 0 and directory_contents[0] == "error":
                    response["directory_error"] = directory_contents[1] if len(directory_contents) > 1 else "Unknown directory error"
                else:
                    response["directory_contents"] = directory_contents
                    response["directory_listed"] = directory
        except Exception as e:
            response["directory_error"] = f"Error listing directory {directory}: {str(e)}"
    
    # If file_path parameter is provided, call read_file
    if file_path is not None:
        try:
            file_content = read_file(file_path)
            response["file_content"] = file_content
            response["file_read"] = file_path
        except Exception as e:
            response["file_error"] = f"Error reading file {file_path}: {str(e)}"
    
    return response

@mcp.tool()
def list_directory(directory: str, report_progress: bool = True, batch_size: int = 100) -> Dict[str, Any]:
    """
    List files and subdirectories in the given directory with optional progress reporting.
    
    Args:
        directory: The absolute or relative path to the directory (supports both / and \\ separators).
        report_progress: Whether to include progress information in the response.
        batch_size: Number of items to process before reporting progress (default: 100).
    
    Returns:
        If report_progress is False: A list of file and directory names in the directory.
        If report_progress is True: A dictionary containing:
            - contents: List of file and directory names
            - progress_info: Dictionary with progress details
            - total_items: Total number of items found
            - processing_time: Time taken to process the directory
        
        If an error occurs, returns a dictionary with "error" and "error_message" keys.
    """
    start_time = time.time()
    
    try:
        # Normalize the path to handle both Windows and Unix style separators
        normalized_dir = normalize_path(directory)
    
        # Use the normalized path for the allowed path check
        if not is_allowed_path(normalized_dir):
            error_message = f"Access to this directory is not allowed. Requested: {directory}, Normalized: {normalized_dir}"
            if report_progress:
                return {
                    "error": True,
                    "error_message": error_message,
                    "progress_info": {"status": "failed", "stage": "permission_check"}
                }
            return ["error", error_message]
    
        if not os.path.isdir(normalized_dir):
            error_message = f"The provided path is not a directory or does not exist: Requested: {directory}, Normalized: {normalized_dir}"
            if report_progress:
                return {
                    "error": True,
                    "error_message": error_message,
                    "progress_info": {"status": "failed", "stage": "directory_validation"}
                }
            return ["error", error_message]
    
        # List directory contents with progress reporting
        try:
            if report_progress:
                # Get initial count estimate if possible
                progress_info = {
                    "status": "scanning",
                    "stage": "directory_listing",
                    "start_time": start_time
                }
            
            directory_contents = os.listdir(normalized_dir)
            total_items = len(directory_contents)
            
            if report_progress:
                # For large directories, we can simulate processing in batches
                processed_items = []
                progress_updates = []
                
                for i, item in enumerate(directory_contents):
                    processed_items.append(item)
                    
                    # Report progress every batch_size items or at the end
                    if (i + 1) % batch_size == 0 or (i + 1) == total_items:
                        current_time = time.time()
                        progress_update = {
                            "processed": i + 1,
                            "total": total_items,
                            "percentage": round(((i + 1) / total_items) * 100, 2),
                            "elapsed_time": round(current_time - start_time, 3),
                            "items_per_second": round((i + 1) / (current_time - start_time), 2) if current_time > start_time else 0
                        }
                        progress_updates.append(progress_update)
                        
                        # Add a small delay for demonstration purposes (remove in production)
                        if total_items > batch_size and i + 1 < total_items:
                            time.sleep(0.01)
                
                end_time = time.time()
                processing_time = round(end_time - start_time, 3)
                
                return {
                    "error": False,
                    "contents": directory_contents,
                    "total_items": total_items,
                    "processing_time": processing_time,
                    "progress_info": {
                        "status": "completed",
                        "stage": "finished",
                        "final_progress": progress_updates[-1] if progress_updates else None,
                        "progress_updates": progress_updates,
                        "directory_path": directory,
                        "normalized_path": normalized_dir
                    }
                }
            else:
                # Return simple list for backward compatibility
                return directory_contents
                
        except PermissionError:
            error_message = f"Permission denied accessing directory: {directory}, Normalized: {normalized_dir}"
            if report_progress:
                return {
                    "error": True,
                    "error_message": error_message,
                    "progress_info": {"status": "failed", "stage": "permission_denied"}
                }
            return ["error", error_message]
        except FileNotFoundError:
            error_message = f"Directory not found: {directory}, Normalized: {normalized_dir}"
            if report_progress:
                return {
                    "error": True,
                    "error_message": error_message,
                    "progress_info": {"status": "failed", "stage": "not_found"}
                }
            return ["error", error_message]
        except OSError as e:
            error_message = f"OS error accessing directory {directory}: {str(e)}, Normalized: {normalized_dir}"
            if report_progress:
                return {
                    "error": True,
                    "error_message": error_message,
                    "progress_info": {"status": "failed", "stage": "os_error", "details": str(e)}
                }
            return ["error", error_message]
        except Exception as e:
            error_message = f"Error accessing directory {directory}: {str(e)}, Normalized: {normalized_dir}"
            if report_progress:
                return {
                    "error": True,
                    "error_message": error_message,
                    "progress_info": {"status": "failed", "stage": "unexpected_error", "details": str(e)}
                }
            return ["error", error_message]
    except Exception as e:
        error_message = f"Unexpected error accessing directory {directory}: {str(e)}"
        if report_progress:
            return {
                "error": True,
                "error_message": error_message,
                "progress_info": {"status": "failed", "stage": "outer_exception", "details": str(e)}
            }
        return ["error", error_message]

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
    
    # Use normalized path for consistency
    if not is_allowed_path(normalized_file):
        raise ValueError(f"Access to this file is not allowed. Requested: {file_path}, Normalized: {normalized_file}")
    
    if not os.path.isfile(normalized_file):
        raise ValueError(f"The provided path is not a file or does not exist: {normalized_file}")
    
    ext = os.path.splitext(normalized_file)[1].lower()
    if ext not in allowed_extensions:
        raise ValueError(f"This file type '{ext}' is not allowed for reading. Allowed extensions: {allowed_extensions}")
    
    try:
        with open(normalized_file, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except UnicodeDecodeError:
        # Fallback for files that can't be decoded as UTF-8
        with open(normalized_file, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()

@mcp.tool()
def list_resources(directory: Optional[str] = None, report_progress: bool = True, batch_size: int = 100) -> Any:
    """
    List all resources (files and directories) in the specified directory (or all allowed_dirs if not specified) in MCP resource format.
    Supports progress reporting for large workspaces.
    Args:
        directory: Directory to start from (optional, defaults to all allowed_dirs)
        report_progress: If True, returns progress info and batches
        batch_size: Number of resources per progress batch
    Returns:
        If report_progress is False: List of all resource objects
        If report_progress is True: Dict with contents, progress_info, total_items, processing_time
    """
    import time
    start_time = time.time()
    resources = []
    progress_updates = []
    processed = 0
    total_items = 0
    dirs_to_walk = []
    if directory:
        dir_norm = normalize_path(directory)
        if not is_allowed_path(dir_norm) or not os.path.isdir(dir_norm):
            return {"error": True, "error_message": f"Directory not allowed or does not exist: {directory}"}
        dirs_to_walk = [dir_norm]
    else:
        dirs_to_walk = [d for d in allowed_dirs if os.path.isdir(d)]
    # Count total items for progress (optional, can be slow for huge trees)
    if report_progress:
        for base_dir in dirs_to_walk:
            for _, dirs, files in os.walk(base_dir):
                total_items += len(dirs) + len(files)
    # Main walk
    for base_dir in dirs_to_walk:
        for root, dirs, files in os.walk(base_dir):
            # Add directories
            for d in dirs:
                dir_path = os.path.join(root, d)
                dir_path_norm = normalize_path(dir_path)
                if is_allowed_path(dir_path_norm):
                    resources.append({
                        "id": dir_path_norm,
                        "type": "directory",
                        "name": d,
                        "path": dir_path_norm,
                        "metadata": {},
                        "actions": ["list"]
                    })
                    processed += 1
                    if report_progress and processed % batch_size == 0:
                        progress_updates.append({
                            "processed": processed,
                            "total": total_items,
                            "percentage": round((processed/total_items)*100, 2) if total_items else None,
                            "elapsed_time": round(time.time() - start_time, 3)
                        })
            # Add files
            for f in files:
                file_path = os.path.join(root, f)
                file_path_norm = normalize_path(file_path)
                ext = os.path.splitext(f)[1].lower()
                if is_allowed_path(file_path_norm) and ext in allowed_extensions:
                    try:
                        stat = os.stat(file_path_norm)
                        modified = datetime.datetime.utcfromtimestamp(stat.st_mtime).isoformat() + "Z"
                        size = stat.st_size
                    except Exception:
                        modified = None
                        size = None
                    resources.append({
                        "id": file_path_norm,
                        "type": "file",
                        "name": f,
                        "path": file_path_norm,
                        "metadata": {
                            "size": size,
                            "modified": modified
                        },
                        "actions": ["read", "read_binary"]
                    })
                    processed += 1
                    if report_progress and processed % batch_size == 0:
                        progress_updates.append({
                            "processed": processed,
                            "total": total_items,
                            "percentage": round((processed/total_items)*100, 2) if total_items else None,
                            "elapsed_time": round(time.time() - start_time, 3)
                        })
    end_time = time.time()
    processing_time = round(end_time - start_time, 3)
    if report_progress:
        return {
            "error": False,
            "contents": resources,
            "total_items": processed,
            "processing_time": processing_time,
            "progress_info": {
                "status": "completed",
                "stage": "finished",
                "final_progress": progress_updates[-1] if progress_updates else None,
                "progress_updates": progress_updates,
                "directory_path": directory,
                "normalized_path": normalize_path(directory) if directory else None
            }
        }
    else:
        return resources

@mcp.tool()
def get_resource(path: str) -> Dict[str, Any]:
    """
    Get metadata and actions for a specific file or directory at the given path.
    Returns a resource object or an error if not found or not allowed.
    """
    normalized_path = normalize_path(path)
    if not is_allowed_path(normalized_path):
        return {"error": True, "error_message": f"Access to this resource is not allowed: {path}"}
    if not os.path.exists(normalized_path):
        return {"error": True, "error_message": f"Resource does not exist: {path}"}
    name = os.path.basename(normalized_path)
    if os.path.isdir(normalized_path):
        return {
            "id": normalized_path,
            "type": "directory",
            "name": name,
            "path": normalized_path,
            "metadata": {},
            "actions": ["list"]
        }
    elif os.path.isfile(normalized_path):
        ext = os.path.splitext(name)[1].lower()
        if ext not in allowed_extensions:
            return {"error": True, "error_message": f"File type '{ext}' is not allowed."}
        try:
            stat = os.stat(normalized_path)
            modified = datetime.datetime.utcfromtimestamp(stat.st_mtime).isoformat() + "Z"
            size = stat.st_size
        except Exception:
            modified = None
            size = None
        return {
            "id": normalized_path,
            "type": "file",
            "name": name,
            "path": normalized_path,
            "metadata": {
                "size": size,
                "modified": modified
            },
            "actions": ["read", "read_binary"]
        }
    else:
        return {"error": True, "error_message": f"Resource is neither file nor directory: {path}"}

@mcp.tool()
def read_file_binary(file_path: str) -> Dict[str, Any]:
    """
    Read the content of a file as base64-encoded bytes.
    Returns a dict with 'content_base64' (base64 string) or an error.
    """
    normalized_file = normalize_path(file_path)
    if not is_allowed_path(normalized_file):
        return {"error": True, "error_message": f"Access to this file is not allowed: {file_path}"}
    if not os.path.isfile(normalized_file):
        return {"error": True, "error_message": f"The provided path is not a file or does not exist: {file_path}"}
    ext = os.path.splitext(normalized_file)[1].lower()
    if ext not in allowed_extensions:
        return {"error": True, "error_message": f"This file type '{ext}' is not allowed for reading."}
    try:
        with open(normalized_file, 'rb') as f:
            data = f.read()
        encoded = base64.b64encode(data).decode('ascii')
        return {"content_base64": encoded, "encoding": "base64", "error": False}
    except Exception as e:
        return {"error": True, "error_message": f"Error reading file: {str(e)}"}

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
    print("3. Available tools:")
    print("   - init(directory, file_path)")
    print("   - list_directory(directory, report_progress=False, batch_size=100)")
    print("   - read_file(file_path)")
    print("   - read_file_binary(file_path)")
    print("   - list_resources()")
    print("   - get_resource(path)")
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