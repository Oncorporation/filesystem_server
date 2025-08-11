# FileSystem MCP Server

A Model Context Protocol (MCP) server that provides filesystem access tools for AI assistants like Copilot. This server allows controlled access to local directories and files with configurable restrictions.

## Features

- **Directory Traversal**: List contents of allowed directories
- **File Reading**: Read contents of files with allowed extensions
- **Security**: Access restricted to configured directories and file types
- **Configuration**: JSON-based configuration for easy setup

## Installation

1. Ensure you have Python 3.10+ installed
2. Navigate to the project directory
3. Install dependencies using uv:
   ```bash
   uv sync
   ```

## Configuration

Edit the `config.json` file to specify:
- `allowed_dirs`: List of directory paths that can be accessed
- `allowed_extensions`: List of file extensions that can be read (e.g., ".py", ".js", ".md")

Example configuration:
```json
{
  "allowed_dirs": [
    "C:/Users/YourUsername/Documents/projects",
    "G:/projects",
    "D:/development"
  ],
  "allowed_extensions": [
    ".py", ".js", ".ts", ".json", ".md", ".txt",
    ".yml", ".yaml", ".toml", ".cfg", ".ini"
  ]
}
```

## Usage

Start the MCP server:
```bash
uv run app.py
```

The server will display connection information including MCP client configuration examples.

The server provides two main tools:
1. `list_directory(directory)` - Lists files and subdirectories in a given directory
2. `read_file(file_path)` - Reads the content of a specified file

## MCP Client Configuration

Add this to your MCP client configuration file:

```json
{
  "mcpServers": {
    "filesystem-server": {
      "command": "uv",
      "args": ["run", "app.py"],
      "cwd": "/path/to/filesystem_server"
    }
  }
}
```

Or using direct Python:

```json
{
  "mcpServers": {
    "filesystem-server": {
      "command": "python",
      "args": ["/path/to/filesystem_server/app.py"],
      "cwd": "/path/to/filesystem_server"
    }
  }
}
```

## Security

- Only directories listed in `allowed_dirs` can be accessed
- Only files with extensions in `allowed_extensions` can be read
- All paths are validated before access
- The server runs with the permissions of the user account

## Integration

This server is designed to work with MCP-compatible AI assistants and can be configured in your MCP client configuration file. The server communicates via stdio (standard input/output) transport.

## Error Handling

The server provides detailed error messages for:
- Unauthorized directory access
- Invalid file paths
- Unsupported file extensions
- Missing configuration files