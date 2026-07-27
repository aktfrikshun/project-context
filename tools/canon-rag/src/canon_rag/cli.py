from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .build import revision, write_artifacts
from .service import CanonService
from .storage import FileIndexStore
from .validate import validate


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="canon-rag")
    result.add_argument("--root", type=Path, default=Path.cwd(), help="repository root")
    result.add_argument("--index-root", type=Path, default=Path("generated/chloekatastrophe"), help="published index root")
    commands = result.add_subparsers(dest="command", required=True)
    build = commands.add_parser("build", help="atomically build and publish a commit-addressed index")
    build.add_argument("--output", type=Path, help="deprecated alias for --index-root")
    build.add_argument("--full", action="store_true", help="ignore the previous projection")
    commands.add_parser("validate", help="validate sources and retrieval metadata")
    search_command = commands.add_parser("search", help="run hybrid canon retrieval")
    search_command.add_argument("query")
    search_command.add_argument("--limit", type=int, default=10)
    explain = commands.add_parser("explain", help="show retrieval results and score components")
    explain.add_argument("query")
    commands.add_parser("revision", help="show source and index revisions")
    commands.add_parser("rollback", help="atomically select the previous good index")
    commands.add_parser("health", help="report process health")
    commands.add_parser("ready", help="report index readiness and staleness")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    root = args.root.resolve()
    if args.command == "validate":
        errors = validate(root)
        if errors:
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1
        print("Canon retrieval sources are valid.")
        return 0
    index_root = args.index_root if args.index_root.is_absolute() else root / args.index_root
    if args.command == "build":
        if args.output:
            index_root = args.output if args.output.is_absolute() else root / args.output
        store = FileIndexStore(index_root)
        current = store.current_revision()
        previous = store.release_path(current) / "chunks.jsonl" if current else None
        staging = store.stage()
        manifest = write_artifacts(root, staging, previous_chunks=previous, full_rebuild=args.full)
        destination = store.publish(staging, str(manifest["source_revision"]))
        print(json.dumps({**manifest, "published_path": destination.as_posix()}, indent=2, sort_keys=True))
        return 0
    service = CanonService(root, index_root)
    if args.command == "search":
        print(json.dumps(service.search_knowledge("chloekatastrophe", args.query, {"limit": args.limit}), indent=2, ensure_ascii=False, sort_keys=True))
    elif args.command == "explain":
        print(json.dumps(service.explain_retrieval("chloekatastrophe", args.query), indent=2, ensure_ascii=False, sort_keys=True))
    elif args.command == "revision":
        print(json.dumps(service.revision_info(), indent=2, sort_keys=True))
    elif args.command == "rollback":
        print(json.dumps({"source_revision": FileIndexStore(index_root).rollback()}, indent=2))
    elif args.command == "health":
        print(json.dumps(service.health(), indent=2))
    elif args.command == "ready":
        result = service.readiness()
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["status"] == "ready" else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
