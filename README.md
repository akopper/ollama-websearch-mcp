# Ollama WebSearch MCP Server

MCP server for Ollama web search and web fetch APIs.

## Overview

This MCP server exposes two tools for interacting with Ollama's web services:

- **web_search**: Perform a web search using Ollama's hosted search API
- **web_fetch**: Fetch the content of a web page

## Requirements

- Python 3.10+
- Ollama account (for cloud API access)

## Installation

### From Source

```bash
# Clone and install
cd ollama-websearch-mcp
pip install -e .
```

### With uv

```bash
uv add ollama-websearch-mcp
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OLLAMA_API_KEY` | API key for Ollama cloud services | None |
| `OLLAMA_HOST` | Host URL for Ollama | `https://ollama.com` |

### Getting an API Key

1. Go to [ollama.com](https://ollama.com)
2. Sign in to your account
3. Navigate to API settings
4. Generate an API key

## Usage

### Running the Server

#### stdio mode (default, for Claude Desktop/Cursor)

```bash
# Using the installed command
ollama-websearch-mcp

# Or directly with Python
python -m ollama_websearch_mcp.server
```

#### HTTP mode (for remote usage)

```bash
python -m ollama_websearch_mcp.server --http
```

The server will start on `http://localhost:8000/mcp` by default.

### Claude Desktop Integration

Add the following to your Claude Desktop configuration:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "ollama-websearch": {
      "command": "ollama-websearch-mcp",
      "env": {
        "OLLAMA_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

Or with a custom Python environment:

```json
{
  "mcpServers": {
    "ollama-websearch": {
      "command": "/path/to/venv/bin/python",
      "args": ["-m", "ollama_websearch_mcp.server"],
      "env": {
        "OLLAMA_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Cursor Integration

Add to Cursor settings (or `.cursor/mcp.json` in project):

```json
{
  "mcpServers": {
    "ollama-websearch": {
      "command": "ollama-websearch-mcp",
      "env": {
        "OLLAMA_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Using with uvx

```bash
# stdio mode
uvx ollama-websearch-mcp

# HTTP mode
uvx ollama-websearch-mcp --http
```

### MCPorter Integration

MCPorter can discover and use this MCP server. Create a config file:

```json
// config/mcporter.json
{
  "mcpServers": {
    "ollama-websearch": {
      "description": "Ollama web search and web fetch MCP server",
      "command": "ollama-websearch-mcp",
      "env": {
        "OLLAMA_API_KEY": "$env:OLLAMA_API_KEY"
      }
    }
  }
}
```

Or run ad-hoc:

```bash
# List tools
npx mcporter list ollama-websearch

# Call a tool
npx mcporter call ollama-websearch.web_search query:python max_results:5
```

## Available Tools

### web_search

Perform a web search using Ollama's hosted search API.

**Parameters:**
- `query` (required): The search query string
- `max_results` (optional): Maximum number of results to return (default: 5)

**Returns:** Dictionary containing search results with title, url, and snippet.

### web_fetch

Fetch the content of a web page.

**Parameters:**
- `url` (required): The absolute URL to fetch

**Returns:** Dictionary containing the fetched content with html, text, and metadata.

## Development

### Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run a single test
pytest tests/test_server.py::TestWebSearch::test_web_search_returns_dict

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=src --cov-report=html
```

### Linting

```bash
# Check code style
ruff check src/ tests/

# Auto-fix issues
ruff check src/ tests/ --fix
```

### Running the Server for Development

```bash
# stdio mode with mcp dev
mcp dev src/ollama_websearch_mcp/server.py

# Or run directly
python -m ollama_websearch_mcp.server
```

## License

MIT
