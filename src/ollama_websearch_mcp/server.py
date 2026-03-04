"""MCP server for Ollama web search and web fetch APIs.

This server exposes two tools:
- web_search: Perform a web search using Ollama's hosted search API
- web_fetch: Fetch the content of a web page

Environment Variables:
- OLLAMA_API_KEY (optional): API key for Ollama cloud services
- OLLAMA_HOST (optional): Host URL for Ollama (default: https://ollama.com)
"""

from __future__ import annotations

import os
from typing import Any

from mcp.server.fastmcp import FastMCP
from ollama import Client

mcp = FastMCP("ollama-websearch-mcp")

_ollama_client: Client | None = None


def get_ollama_client() -> Client:
    """Get or create the Ollama client instance."""
    global _ollama_client
    if _ollama_client is None:
        api_key = os.environ.get("OLLAMA_API_KEY")
        host = os.environ.get("OLLAMA_HOST", "https://ollama.com")

        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        _ollama_client = Client(host=host, headers=headers)
    return _ollama_client


@mcp.tool()
def web_search(query: str, max_results: int = 5) -> dict[str, Any]:
    """Perform a web search using Ollama's hosted search API.

    Args:
        query: The search query to run.
        max_results: Maximum number of results to return (default: 5).

    Returns:
        A dictionary containing search results with title, url, and snippet.
    """
    client = get_ollama_client()
    result = client.web_search(query=query, max_results=max_results)
    return result.model_dump()


@mcp.tool()
def web_fetch(url: str) -> dict[str, Any]:
    """Fetch the content of a web page.

    Args:
        url: The absolute URL to fetch.

    Returns:
        A dictionary containing the fetched content with html, text, and metadata.
    """
    client = get_ollama_client()
    result = client.web_fetch(url=url)
    return result.model_dump()


def main():
    """Main entry point for the MCP server."""
    import sys

    transport = "stdio"
    if len(sys.argv) > 1:
        if sys.argv[1] == "--http":
            transport = "streamable-http"
        elif sys.argv[1] == "--sse":
            transport = "sse"

    mcp.run(transport=transport)


if __name__ == "__main__":
    main()
