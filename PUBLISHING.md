# Publishing to MCP Registry

This document explains how to publish the vs-filesystem-mcp-server to the MCP Registry at modelcontextprotocol.info.

## Overview

The vs-filesystem-mcp-server is configured to be automatically published to both PyPI and the MCP Registry using GitHub Actions whenever you create a new version tag.

## Prerequisites

### Required Accounts
- **PyPI Account**: For publishing the Python package ([register here](https://pypi.org/account/register/))
- **GitHub Account**: Already configured (repository owner)

### Required Secrets

PyPI publishing uses **Trusted Publisher (OIDC)**, so no PyPI token secret is required.

## Publishing Process

### Automatic Publishing (Recommended)

The GitHub Actions workflow (`.github/workflows/publish-mcp.yml`) automatically handles publishing when you create a version tag:

1. **Update version numbers:**
   ```bash
   # Update version in pyproject.toml
   # Example: version = "0.1.1"
   ```

2. **Commit your changes:**
   ```bash
   git add pyproject.toml server.json
   git commit -m "Bump version to 0.1.1"
   git push
   ```

3. **Create and push a version tag:**
   ```bash
   git tag v0.1.1
   git push origin v0.1.1
   ```

4. **Monitor the workflow:**
   - Go to the **Actions** tab in your GitHub repository
   - Watch the "Publish to MCP Registry" workflow run
   - It will:
     - Build the Python package
     - Publish to PyPI using **Trusted Publisher (OIDC)**
     - Authenticate with MCP Registry using GitHub OIDC
     - Update version in server.json
     - Publish to MCP Registry

### Manual Publishing

If you need to publish manually:

1. **Publish to PyPI first:**
   ```bash
   python -m build
   python -m twine upload dist/*
   ```

2. **Install mcp-publisher:**
   ```bash
   # On Windows (PowerShell):
   $arch = if ([System.Runtime.InteropServices.RuntimeInformation]::ProcessArchitecture -eq "Arm64") { "arm64" } else { "amd64" }
   Invoke-WebRequest -Uri "https://github.com/modelcontextprotocol/registry/releases/latest/download/mcp-publisher_windows_$arch.tar.gz" -OutFile "mcp-publisher.tar.gz"
   tar xf mcp-publisher.tar.gz mcp-publisher.exe
   rm mcp-publisher.tar.gz
   ```

3. **Authenticate:**
   ```bash
   ./mcp-publisher login github
   # Follow the prompts to authenticate
   ```

4. **Update server.json version** to match your release

5. **Publish:**
   ```bash
   ./mcp-publisher publish
   ```

## Verification Files

The following files are configured for MCP Registry verification:

### README.md
Contains the verification comment:
```markdown
<!-- mcp-name: io.github.oncorporation/filesystem-server -->
```
This must match the `name` field in `server.json`.

### server.json
The MCP Registry metadata file with:
- Server name: `io.github.oncorporation/filesystem-server`
- Package type: `pypi`
- Package identifier: `vs-filesystem-mcp-server`

### pyproject.toml
Contains package metadata including repository URLs.

## Troubleshooting

| Error | Solution |
|-------|----------|
| "Registry validation failed for package" | Ensure README.md contains the MCP verification comment and it matches server.json |
| "Invalid or expired Registry JWT token" | Re-authenticate with `mcp-publisher login github` |
| "Package not found on PyPI" | Ensure the package is published to PyPI first |
| "Version mismatch" | Ensure versions match in pyproject.toml and server.json |
| "Trusted publishing disabled" | Remove PyPI token from the workflow so OIDC is used |
| "This project name is too similar to an existing project" | The name is already taken on PyPI - choose a unique name like `vs-filesystem-mcp-server` or `oncorp-filesystem-server` |

## Finding Your Server

After successful publication, your server will be available:

1. **Via MCP Registry API:**
   ```bash
   curl "https://registry.modelcontextprotocol.io/v0.1/servers?search=filesystem-server"
   ```

2. **On modelcontextprotocol.info** (may take a few minutes to appear)

3. **In MCP-enabled tools** like Visual Studio Code with MCP extensions

4. **Via pip:**
   ```bash
   pip install vs-filesystem-mcp-server
   ```

## Authentication Method

This project uses **GitHub OIDC authentication** (recommended) which:
- Doesn't require storing credentials as secrets
- Uses GitHub's native authentication via workflow permissions
- Automatically validates your GitHub organization ownership

The server name `io.github.oncorporation/filesystem-server` is automatically verified because:
- It starts with `io.github.oncorporation/` (matching your GitHub org)
- The workflow runs in the `Oncorporation/filesystem_server` repository
- GitHub OIDC confirms the repository context

## Next Steps

After publishing:
1. Check your server appears in the registry search
2. Test installation in an MCP client
3. Consider adding:
   - Environment variable configuration if needed
   - Multiple platform support (if applicable)
   - Version compatibility documentation

## Resources

- [MCP Registry Documentation](https://modelcontextprotocol.io/)
- [MCP Registry GitHub](https://github.com/modelcontextprotocol/registry)
- [Publishing Guide](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/quickstart.mdx)
- [GitHub Actions Guide](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/github-actions.mdx)
