# CLAUDE.md - VS Code Configuration

## Overview

The `.vscode/` directory contains Visual Studio Code workspace configuration files.

## Current Contents

```
.vscode/
└── launch.json          # Debug configurations
```

## Debug Configuration

### launch.json

Defines debug configurations for the FastAPI application.

**Available Configurations:**
- Python debugger configurations for FastAPI
- Uvicorn server with debug attachment

**Usage:**
1. Open VS Code
2. Go to Run and Debug (Ctrl+Shift+D)
3. Select configuration from dropdown
4. Press F5 to start debugging

## Recommended VS Code Extensions

For optimal development experience:

- **Python** (ms-python.python): Python language support
- **Pylance** (ms-python.vscode-pylance): Advanced Python analysis
- **Python Debugger** (ms-python.debugpy): Debug Python applications
- **autoDocstring** (njpwerner.autodocstring): Generate Python docstrings

## Adding New Configurations

### Workspace Settings (settings.json)

If you need project-specific VS Code settings:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true
}
```

### Additional Debug Configurations

To add new debug configurations, edit `launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": ["app.main:app", "--reload"],
            "jinja": true
        }
    ]
}
```

## Guidelines

- Keep configurations project-specific
- Don't commit personal preferences to `.vscode/settings.json`
- Document any required extensions
- Use relative paths in configurations
