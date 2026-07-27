from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .service import CanonService

TOOLS = [
    ("load_project_context", "Load the compact authoritative project baseline."),
    ("search_knowledge", "Search canon with authority-aware hybrid retrieval."),
    ("get_source", "Read one authoritative source at an exact revision."),
    ("get_asset", "Read one asset record at an exact revision."),
    ("get_canon_revision", "Report source/index revision and stale status."),
    ("explain_retrieval", "Search and include score/ranking explanations."),
]


def tool_definitions() -> list[dict[str, object]]:
    return [{"name": name, "description": description, "inputSchema": {"type": "object", "additionalProperties": True}} for name, description in TOOLS]


def call(service: CanonService, name: str, arguments: dict[str, object]) -> object:
    if name == "load_project_context":
        return service.load_project_context(str(arguments["project"]))
    if name == "search_knowledge":
        return service.search_knowledge(str(arguments["project"]), str(arguments["query"]), arguments.get("filters") if isinstance(arguments.get("filters"), dict) else None)
    if name == "get_source":
        return service.get_source(str(arguments["project"]), str(arguments["path"]), str(arguments["commit_sha"]))
    if name == "get_asset":
        return service.get_asset(str(arguments["project"]), str(arguments["asset_id"]), str(arguments["commit_sha"]))
    if name == "get_canon_revision":
        return service.revision_info()
    if name == "explain_retrieval":
        return service.explain_retrieval(str(arguments["project"]), str(arguments["query"]))
    raise ValueError(f"unknown tool: {name}")


def serve(service: CanonService) -> None:
    for line in sys.stdin:
        try:
            request = json.loads(line)
            method = request.get("method")
            if method == "initialize":
                result = {"protocolVersion": "2025-03-26", "capabilities": {"tools": {}}, "serverInfo": {"name": "chloe-canon-rag", "version": "0.2.0"}}
            elif method == "tools/list":
                result = {"tools": tool_definitions()}
            elif method == "tools/call":
                params = request.get("params", {})
                value = call(service, str(params["name"]), params.get("arguments", {}))
                result = {"content": [{"type": "text", "text": json.dumps(value, ensure_ascii=False)}], "isError": False}
            elif method == "ping":
                result = {}
            elif method and method.startswith("notifications/"):
                continue
            else:
                raise ValueError(f"unsupported method: {method}")
            print(json.dumps({"jsonrpc": "2.0", "id": request.get("id"), "result": result}), flush=True)
        except Exception as error:  # The protocol must return structured errors.
            print(json.dumps({"jsonrpc": "2.0", "id": request.get("id") if "request" in locals() else None, "error": {"code": -32000, "message": str(error)}}), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--index-root", type=Path, default=Path("generated/chloekatastrophe"))
    args = parser.parse_args()
    index = args.index_root if args.index_root.is_absolute() else args.root / args.index_root
    serve(CanonService(args.root, index))


if __name__ == "__main__":
    main()
