# FileSystem MCP Server

A Model Context Protocol (MCP) server that provides filesystem access tools for AI assistants like GitHub Copilot. This server is **specifically designed for local development environments** such as **Visual Studio 2022**, Visual Studio Code (without workspace files), and other IDEs that don't rely on code-workspace configurations.

## ?? Target Environment

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
- **Security**: Access restricted to configured directories and file types
- **Configuration**: JSON-based configuration for easy setup
- **Local Development Focus**: Perfect for Visual Studio 2022 and similar environments

## Installation

1. Ensure you have **Python 3.10+** installed
2. Navigate to the project directory
3. Install dependencies using uv:
   ```bash
   uv sync
   ```

## Configuration

Edit the `config.json` file to specify your local development directories:
- `allowed_dirs`: List of directory paths that can be accessed (your project folders)
- `allowed_extensions`: List of file extensions that can be read

Example configuration for local development:
```json
{
  "allowed_dirs": [
    "C:/Users/YourUsername/Documents/projects",
    "G:/projects",
    "D:/development",
    "C:/source/repos"
  ],
  "allowed_extensions": [
    ".py", ".js", ".ts", ".json", ".md", ".txt",
    ".yml", ".yaml", ".toml", ".cfg", ".ini",
    ".cs", ".cpp", ".h", ".hpp", ".xml", ".xaml"
  ]
}
```

## Usage

Start the MCP server:
```bash
uv run app.py
```

The server will display connection information including MCP client configuration examples tailored for your development environment.

**Available Tools:**

1. `init()` - **NEW!** Validates accessibility of configured directories
   - Returns `{"message": "OK", "isError": false}` if all directories accessible
   - Returns error details if any directories are inaccessible
   - Use this to verify your configuration before using other tools

2. `list_directory(directory)` - Lists files and subdirectories in a given directory

3. `read_file(file_path)` - Reads the content of a specified file

## MCP Client Configuration

### For Visual Studio 2022 & Local Development

Add this to your MCP client configuration file:

**Recommended configuration (using uv):**
```json
{
  "mcpServers": {
    "filesystem-server": {
      "command": "uv",
      "args": ["run", "app.py"],
      "cwd": "G:/Projects/filesystem_server"
    }
  }
}
```

**Alternative configuration (direct Python):**
```json
{
  "mcpServers": {
    "filesystem-server": {
      "command": "python",
      "args": ["G:/Projects/filesystem_server/app.py"],
      "cwd": "G:/Projects/filesystem_server"
    }
  }
}
```

### Why This Server is Perfect for Visual Studio 2022

- ? **No workspace dependencies**: Works with individual solution/project folders
- ? **Simple configuration**: Just edit `config.json` with your project paths
- ? **Local file access**: Direct access to your development directories
- ? **IDE agnostic**: Works with Visual Studio 2022, VS Code, and other editors
- ? **Security focused**: Only accesses directories you explicitly allow
- ? **Configuration validation**: `init()` tool verifies setup before use

## Development Workflow Integration

This server integrates seamlessly with:
- **Visual Studio 2022 solutions and projects**
- **Individual project folders** (no multi-root workspace required)
- **Local development directories** on Windows, macOS, and Linux
- **Standard development environments** without complex configuration

## Getting Started

1. **Test your configuration** by calling the `init()` tool first
2. **If init() returns errors**, check your `config.json` file:
   - Verify directory paths exist
   - Check directory permissions
   - Ensure paths use correct format for your OS
3. **Once init() returns "OK"**, use `list_directory()` and `read_file()` tools

## Security

- Only directories listed in `allowed_dirs` can be accessed
- Only files with extensions in `allowed_extensions` can be read
- All paths are validated before access
- The server runs with the permissions of the user account
- **Perfect for local development**: Secure access to your project directories
- **Configuration validation**: `init()` tool helps identify permission issues

## Integration

This server is designed to work with MCP-compatible AI assistants and can be configured in your MCP client configuration file. The server communicates via stdio (standard input/output) transport, making it ideal for development environments like Visual Studio 2022.

**Key Benefits for Local Development:**
- No complex workspace setup required
- Works with existing project structures
- Simple JSON configuration
- Secure, controlled filesystem access
- Built-in configuration validation

## Error Handling

The server provides detailed error messages for:
- Unauthorized directory access
- Invalid file paths
- Unsupported file extensions
- Missing configuration files
- Directory accessibility issues (via `init()` tool)

## Troubleshooting

### Common Issues in Visual Studio 2022

1. **Start with the `init()` tool** to validate your configuration
2. If `init()` reports errors:
   - Ensure your project directories are listed in `allowed_dirs`
   - Verify directories exist and are accessible
   - Check file permissions on directories
3. Ensure the MCP client configuration points to the correct server path
4. Check that file extensions you want to access are in `allowed_extensions`
5. Make sure the server is running before connecting your MCP client

### Example `init()` Tool Usage

```javascript
// Call the init tool to validate configuration
const result = await init();

if (result.isError) {
  console.log("Configuration issues:", result.message);
  console.log("Details:", result.details);
} else {
  console.log("All directories accessible:", result.message);
  // Now safe to use list_directory() and read_file()
}