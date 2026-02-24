# 🚀 Ready to Publish - Quick Start Guide

## ✅ Current Status

Your MCP server is **fully configured and ready to publish** to both PyPI and the MCP Registry!

### Validated Components

- ✅ **server.json** - Valid against official MCP schema
- ✅ **GitHub Actions workflow** - Automated publishing configured
- ✅ **Package metadata** - pyproject.toml properly configured
- ✅ **Verification** - README.md contains MCP verification comment
- ✅ **Version** - 0.1.1 synchronized across all files
- ✅ **Build tools** - build and twine installed and ready
- ✅ **Git** - All changes committed

## 🎯 Publishing Method: Automated CI (Recommended)

Your setup uses **GitHub Actions with OIDC authentication** - the official recommended approach.

### Why This Is Best

1. **No secret management** - Uses GitHub's native authentication
2. **Fully automated** - Just push a tag to publish
3. **Secure** - OIDC tokens are temporary and scoped
4. **Dual publishing** - Publishes to PyPI and MCP Registry automatically

## 📋 First-Time Setup Steps

### Step 1: Manual First Publish to PyPI (Required Once)

GitHub Actions can't create a new PyPI project - you must do this manually first:

```powershell
# Clean any old builds
Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue

# Build the package
python -m build

# Verify what was built
Get-ChildItem dist/
# Should show:
# - vs-filesystem-mcp-server-0.1.1.tar.gz
# - vs_filesystem_mcp_server-0.1.1-py3-none-any.whl

# Upload to PyPI (creates the project)
twine upload dist/*
# Enter your PyPI username (or __token__)
# Enter your PyPI API token as the password
```

### Step 2: Configure GitHub Trusted Publisher

After the first manual upload succeeds:

1. Visit: https://pypi.org/manage/project/vs-filesystem-mcp-server/settings/publishing/
2. Click **"Add a new publisher"**
3. Fill in:
   - **PyPI Project Name**: `vs-filesystem-mcp-server`
   - **Owner**: `Oncorporation`
   - **Repository name**: `filesystem_server`
   - **Workflow name**: `publish-mcp.yml`
   - **Environment name**: (leave empty)
4. Click **"Add"**

**Important**: You can only access this page AFTER the first manual upload creates the project.

### Step 3: Future Automated Releases

After trusted publisher is configured, publishing is automatic:

```powershell
# 1. Update version in pyproject.toml and server.json
#    Example: version = "0.1.2"

# 2. Commit the version bump
git add pyproject.toml server.json
git commit -m "Bump version to 0.1.2"
git push

# 3. Create and push a version tag
git tag v0.1.2
git push origin v0.1.2

# 4. GitHub Actions automatically:
#    - Builds the package
#    - Publishes to PyPI
#    - Publishes to MCP Registry
```

## 🔍 Monitoring the Workflow

After pushing a tag:

1. Go to: https://github.com/Oncorporation/filesystem_server/actions
2. Find the "Publish to MCP Registry" workflow
3. Watch it execute:
   - ✅ Build package
   - ✅ Publish to PyPI
   - ✅ Authenticate with MCP Registry via OIDC
   - ✅ Publish to MCP Registry

## 🎉 Verification After Publishing

### Check PyPI

Visit: https://pypi.org/project/vs-filesystem-mcp-server/

Install and test:
```powershell
pip install vs-filesystem-mcp-server
vs-filesystem-mcp-server --help
```

### Check MCP Registry

Query the API:
```powershell
curl "https://registry.modelcontextprotocol.io/v0.1/servers?search=filesystem-server"
```

Browse: https://modelcontextprotocol.io/ (may take a few minutes to appear)

## 🔧 How Your Setup Works

### server.json Configuration

```json
{
  "name": "io.github.oncorporation/filesystem-server",  // MCP Registry name
  "packages": [{
    "registryType": "pypi",                             // Package type
    "identifier": "vs-filesystem-mcp-server"            // PyPI package name
  }]
}
```

### Verification Chain

1. **README.md** contains: `<!-- mcp-name: io.github.oncorporation/filesystem-server -->`
2. This **matches** server.json `name` field
3. MCP Registry validates ownership via this comment in the published PyPI package
4. GitHub OIDC confirms you own the `Oncorporation/filesystem_server` repository

### Authentication Flow

```
GitHub Actions (on tag push)
    ↓
OIDC Token (temporary, auto-generated)
    ↓
MCP Registry validates:
  - Repository ownership
  - Server name format (io.github.oncorporation/*)
  - PyPI package verification comment
    ↓
Publishes to registry ✅
```

## 📝 Quick Reference

### Package Names

- **PyPI**: `vs-filesystem-mcp-server` (install via `pip install vs-filesystem-mcp-server`)
- **MCP Registry**: `io.github.oncorporation/filesystem-server`
- **Command**: `vs-filesystem-mcp-server` (entry point after pip install)

### Version Management

Always update both files together:
- `pyproject.toml` → `version = "X.Y.Z"`
- `server.json` → `version` and `packages[0].version` = `"X.Y.Z"`

### File Locations

- **Workflow**: `.github/workflows/publish-mcp.yml`
- **Metadata**: `server.json`, `pyproject.toml`
- **Verification**: `README.md` (contains mcp-name comment)
- **Packaging**: `MANIFEST.in` (controls what gets included)

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Project not found on PyPI" | Do the first manual upload (Step 1) |
| "Trusted publisher not configured" | Complete Step 2 after first upload |
| "Registry validation failed" | Verify README.md has correct mcp-name comment |
| "Version mismatch" | Ensure versions match in pyproject.toml and server.json |
| "OIDC token invalid" | Check GitHub Actions has `id-token: write` permission |

## 🎓 Best Practices

1. **Always test locally** before publishing:
   ```powershell
   python -m build
   pip install dist/*.whl
   vs-filesystem-mcp-server --help
   ```

2. **Use semantic versioning**: MAJOR.MINOR.PATCH (e.g., 0.1.1)

3. **Tag format**: Always use `v` prefix (e.g., `v0.1.1`, not `0.1.1`)

4. **Commit before tagging**: Ensure all version changes are committed first

5. **Monitor Actions**: Always check the GitHub Actions tab after pushing a tag

## 📚 Additional Resources

- **MCP Registry**: https://modelcontextprotocol.io/
- **GitHub Actions docs**: https://docs.github.com/en/actions
- **PyPI packaging**: https://packaging.python.org/
- **Your workflow**: `.github/workflows/publish-mcp.yml`
- **Detailed publishing guide**: `PUBLISHING.md`

---

**Ready to publish?** Run Step 1 above to do your first manual upload! 🚀
