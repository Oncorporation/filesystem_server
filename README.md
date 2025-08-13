# FileSystem MCP Server

Local MCP server for Visual Studio 2022 that provides code-workspace functionality by giving AI agents selective access to project folders and files

## 🎯 Target Environment

This MCP server is optimized for:
- **Visual Studio 2022** development workflows
- **Local development environments** without complex workspace setups
- **Direct folder access** scenarios where you need filesystem operations
- **Development environments that don't use `.code-workspace` files**
- **Individual project directories** rather than multi-root workspaces

## Features

- **Directory Traversal**: List contents of allowed directories
- **File Reading**: Read contents of files with allowed extensions  
- **Directory Validation**: Check accessibility of configured directories
- **Hybrid Configuration**: Command-line arguments (MCP) + config.json fallback (debugging)
- **Visual Studio 2022 Debugging**: No-argument startup support
- **Cross-Platform Path Support**: Automatically handles both Windows (`\`) and Unix (`/`) path separators
- **Security**: Access restricted to explicitly specified directories and file types
- **Local Development Focus**: Perfect for Visual Studio 2022 and similar environments

## Installation

1. Ensure you have **Python 3.10+** installed
2. Navigate to the project directory
3. Install dependencies using uv:
   ```bash
   uv sync
   ```

## Configuration Options

### Option 1: Config.json File (Simplest - Recommended for Beginners)

**The easiest way to get started!** Create a `config.json` file:

**For debugging (Visual Studio 2022):**
- Place `config.json` in the same directory as `app.py` (`D:\Projects\filesystem_server\`)

**For MCP server usage:**
- Place `config.json` in the same folder as your `.mcp.json` file (usually `C:\Users\YourUsername\`)

```json
{
  "allowed_dirs": [
    "C:/Users/YourUsername/Documents/projects",
    "D:/projects",
    "D:/Webs"
  ],
  "allowed_extensions": [
    ".py", ".js", ".ts", ".json", ".md", ".txt",
    ".yml", ".yaml", ".toml", ".cfg", ".ini", ".cs",
    ".css", ".scss", ".htm", ".html", ".xml", ".xaml"
  ]
}
```

**Benefits:**
- ✅ **No command-line arguments needed**
- ✅ **Perfect for Visual Studio 2022 debugging** (just press F5)
- ✅ **Works with MCP clients when placed in correct location**
- ✅ **Easy to edit and modify**
- ✅ **Great for testing and development**

**Usage:**
```bash
# For debugging in Visual Studio 2022:
python app.py  # Uses config.json from same directory as app.py

# For MCP server usage:
# The MCP client automatically finds config.json in the .mcp.json directory
```

**Important Location Notes:**
- 🔧 **Debugging**: `config.json` goes next to `app.py`
- 🌐 **MCP Server**: `config.json` goes next to `.mcp.json` 
- 📁 **Different locations** for different use cases!

### Option 2: Command-Line Arguments (Advanced - For MCP Clients)

Best for production MCP client configurations where you want everything in one place:

```bash
python app.py --allowed-dirs "D:/projects" "D:/Webs" --allowed-extensions ".py" ".js" ".md"
```

**MCP Client Configuration:**
```json
{
  "servers": {
    "filesystem-server": {
      "command": "python",
      "args": [
        "D:/Projects/filesystem_server/app.py",
        "--allowed-dirs", "D:/projects", "D:/Webs",
        "--allowed-extensions", ".py", ".js", ".ts", ".json", ".md", ".txt"
      ],
      "cwd": "D:/Projects/filesystem_server"
    }
  }
}
```

**Benefits:**
- ✅ **Self-contained configuration**
- ✅ **No external config files needed**
- ✅ **Version control friendly**
- ✅ **Explicit and visible in MCP setup**

### Option 3: Hybrid Approach (Best of Both Worlds)

The server automatically uses **command-line arguments first**, then **falls back to config.json** if no arguments provided.

**How it works:**
- **MCP clients**: Use command-line arguments (Option 2)
- **Visual Studio debugging**: Automatically uses config.json (Option 1)
- **Priority**: Command-line args override config.json when present

**Benefits:**
- ✅ **Works for both MCP clients and debugging**
- ✅ **No conflicts between different usage scenarios**
- ✅ **Flexible and developer-friendly**
- ✅ **Choose the best option for each situation**

## Usage

### Command Line Examples

```bash
# With command line arguments (MCP clients):
python app.py --allowed-dirs "D:/projects" "D:/Webs" --allowed-extensions ".py" ".js" ".md"

# Using config.json fallback (Visual Studio 2022 debugging):
python app.py

# Show MCP configuration help:
python app.py --help-mcp
```

**Available Tools:**

1. `init()` - Validates accessibility of configured directories
   - Returns `{"message": "OK", "isError": false}` if all directories accessible
   - Returns error details if any directories are inaccessible
   - Shows configuration source (command-line args vs config file)
   - Use this to verify your configuration before using other tools

2. `list_directory(directory)` - Lists files and subdirectories in a given directory
   - Returns a list of file and directory names on success
   - Returns `["error", "error_message"]` if an error occurs (access denied, directory not found, etc.)
   - No exceptions are raised - all errors are returned as part of the result list

3. `read_file(file_path)` - Reads the content of a specified file


## Why This Hybrid Approach is Perfect

- ✅ **MCP clients**: Use efficient command-line arguments
- ✅ **Visual Studio 2022**: Zero-friction debugging with config.json fallback
- ✅ **No conflicts**: Priority system handles both scenarios gracefully
- ✅ **Developer-friendly**: Works however you want to run it
- ✅ **Best of both worlds**: MCP efficiency + debugging convenience

## Getting Started

1. **For MCP usage**: Add the corrected configuration to your `.mcp.json`
2. **For debugging**: Just press F5 in Visual Studio 2022 - uses config.json automatically
3. **Test your configuration** by calling the `init()` tool first
4. **If init() returns errors**, check your directory paths and permissions

## Visual Studio 2022 Debugging

**Perfect debugging experience:**
- ✅ No command-line arguments needed
- ✅ Just press F5 to start debugging
- ✅ Automatically uses config.json
- ✅ Set breakpoints and debug normally
- ✅ Full IntelliSense and debugging support

**Debugging setup:**
1. Open the project in Visual Studio 2022
2. Ensure `config.json` exists (already created for you)
3. Press F5 or Debug > Start Debugging
4. Server starts with your configured directories

## Security

- Only directories specified in `--allowed-dirs` or config.json can be accessed
- Only files with extensions in `--allowed-extensions` or config.json can be read
- All paths are validated before access
- The server runs with the permissions of the user account
- **Perfect for local development**: Secure access to your project directories

## Error Handling

The server provides detailed error messages for:
- Unauthorized directory access
- Invalid file paths
- Unsupported file extensions
- Missing configuration (shows helpful guidance for both MCP and debugging scenarios)
- Directory accessibility issues (via `init()` tool)

**New Error Handling for list_directory():**
- The `list_directory()` function now returns errors as part of the result list instead of raising exceptions
- Error format: `["error", "detailed_error_message"]`
- This makes it easier for MCP clients to handle errors gracefully without exception handling
- Successful calls return the normal list of directory contents

## Troubleshooting

### MCP Configuration Issues

Your original config had a **missing comma** after `"D:/Webs"`. The corrected version above fixes this.

### Visual Studio 2022 Debugging

1. **Ensure config.json exists** (already created for your directories)
2. **Start with the `init()` tool** to validate your configuration
3. **Set breakpoints** and debug normally
4. **Check output window** for configuration source confirmation

### Common Issues

1. **Missing configuration**: The server shows helpful messages for both MCP and debugging scenarios
2. **Path access errors**: Verify your directories exist and are accessible
3. **Permission issues**: Check directory permissions on your configured paths
4. **MCP client issues**: Use the corrected configuration above

## Command Line Reference

```bash
python app.py --help                         # Show help
python app.py --help-mcp                     # Show MCP configuration examples  
python app.py --allowed-dirs DIR1 DIR2       # Set allowed directories
python app.py --allowed-extensions EXT1 EXT2 # Set allowed extensions
python app.py --config custom.json           # Use custom config file
python app.py                                # Use config.json fallback (debugging)
```

## Cross-Platform Path Support

The filesystem server automatically normalizes paths to handle different operating system conventions:

### ✅ **Windows Users - Both Formats Work**
```json
{
  "allowed_dirs": [
    "D:\\projects",           // Windows-style backslashes
    "F:/sd/wipes",           // Unix-style forward slashes  
    "C:\\Users\\Me\\Docs"    // Mixed formats work too
  ]
}
```

### ✅ **Automatic Path Normalization**
- **Input**: `"F:\sd\wipes"` (Windows natural format)
- **Normalized**: `"F:/sd/wipes"` (Python-friendly format)
- **Result**: ✅ Works seamlessly, no errors!

### ✅ **MCP Tool Examples**
```python
# All of these work identically:
list_directory("F:\\sd\\wipes")    # Windows format
list_directory("F:/sd/wipes")      # Unix format  
list_directory("F:\\sd/wipes")     # Mixed format
```

### **Why This Matters**
- 🪟 **Windows users** can naturally type `F:\sd\wipes`
- 🐧 **Unix users** can use traditional `F:/sd/wipes`
- 🔧 **No more path format errors** - everything just works
- 🛡️ **Security checks work correctly** regardless of separator style