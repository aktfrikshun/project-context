from __future__ import annotations

import hashlib
import json
from pathlib import Path

ASSET_MANIFEST = "manifest.json"
REQUIRED_ASSET_FIELDS = {
    "asset_id",
    "path",
    "sha256",
    "status",
    "authority",
    "provenance",
    "permitted_uses",
    "view",
    "features",
    "limitations",
    "relationship_to_chloe_model_v1",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def discover_manifests(root: Path, project: Path) -> list[Path]:
    assets = root / project / "assets"
    if not assets.exists():
        return []
    return sorted(path for path in assets.rglob(ASSET_MANIFEST) if path.is_file())


def load_asset_records(root: Path, project: Path, source_revision: str) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for manifest_path in discover_manifests(root, project):
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        pack_id = str(data.get("pack_id") or data.get("milestone_id") or manifest_path.parent.name)
        pack_status = str(data.get("status", "reference"))
        for asset in data.get("assets", []):
            if not isinstance(asset, dict):
                continue
            rich = REQUIRED_ASSET_FIELDS.issubset(asset)
            image_path = asset.get("path") if rich else asset.get("image")
            if not image_path:
                continue
            asset_path = manifest_path.parent / str(image_path)
            if not asset_path.is_file():
                continue
            stable_asset_id = str(asset["asset_id"]) if rich else f"{pack_id}:{asset['asset_id']}"
            features = asset.get("features", data.get("locked_attributes", data.get("locked_performance_traits", [])))
            limitations = asset.get("limitations", [])
            view = asset.get("view", asset.get("label", asset.get("performance", asset.get("canonical_role", "unspecified"))))
            relationship = asset.get("relationship_to_chloe_model_v1", "Approved component of Chloe Model v1." if pack_status in {"approved", "complete"} else "See manifest.")
            text_parts = [str(asset.get("description", asset.get("notes", asset.get("canonical_name", "")))), f"View: {view}", "Features: " + "; ".join(map(str, features)), "Limitations: " + "; ".join(map(str, limitations)), "Relationship to Chloe Model v1: " + str(relationship)]
            status = str(asset.get("status", pack_status))
            authority = str(asset.get("authority", "accepted_canon" if status in {"approved", "complete", "accepted"} else "unresolved"))
            records.append(
                {
                    "id": f"asset:{stable_asset_id}",
                    "record_type": "asset",
                    "project": "chloekatastrophe",
                    "path": asset_path.relative_to(root).as_posix(),
                    "manifest_path": manifest_path.relative_to(root).as_posix(),
                    "asset_id": stable_asset_id,
                    "pack_id": pack_id,
                    "title": str(asset.get("title", asset.get("canonical_name", stable_asset_id))),
                    "heading": stable_asset_id,
                    "heading_path": [pack_id, stable_asset_id],
                    "text": "\n".join(part for part in text_parts if part),
                    "source_revision": source_revision,
                    "source_sha256": str(asset.get("sha256") or sha256_file(asset_path)),
                    "status": status,
                    "authority": authority,
                    "authority_score": int(asset.get("authority_score", 600 if authority == "accepted_canon" else 200)),
                    "default_eligible": bool(asset.get("default_eligible", True)),
                    "requires_status_label": status not in {"accepted", "approved", "complete"},
                    "metadata": {
                        "pack_status": pack_status,
                        "provenance": asset.get("provenance", manifest_path.relative_to(root).as_posix()),
                        "creator": asset.get("creator"),
                        "approval_date": asset.get("approval_date"),
                        "permitted_uses": asset.get("permitted_uses", ["See model card and manifest."]),
                        "view": view,
                        "features": features,
                        "limitations": limitations,
                        "supersedes": asset.get("supersedes", []),
                    },
                }
            )
    return records


def validate_asset_manifests(root: Path, project: Path) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for manifest_path in discover_manifests(root, project):
        relative_manifest = manifest_path.relative_to(root).as_posix()
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"{relative_manifest}: invalid JSON: {error}")
            continue
        assets = data.get("assets", [])
        if not isinstance(assets, list):
            errors.append(f"{relative_manifest}: assets must be a list")
            continue
        for ordinal, asset in enumerate(assets):
            label = f"{relative_manifest}: asset {ordinal}"
            if not isinstance(asset, dict):
                errors.append(f"{label} must be an object")
                continue
            rich = REQUIRED_ASSET_FIELDS.issubset(asset)
            if not rich and not {"asset_id", "image"}.issubset(asset):
                missing = sorted(REQUIRED_ASSET_FIELDS - set(asset))
                errors.append(f"{label} missing rich fields or legacy image fields: {', '.join(missing)}")
                continue
            pack_id = str(data.get("pack_id") or manifest_path.parent.name)
            asset_id = str(asset["asset_id"]) if rich else f"{pack_id}:{asset['asset_id']}"
            if asset_id in seen:
                errors.append(f"duplicate asset_id: {asset_id}")
            seen.add(asset_id)
            asset_path = manifest_path.parent / str(asset["path"] if rich else asset["image"])
            if not asset_path.is_file():
                errors.append(f"{label} missing file: {asset['path']}")
                continue
            actual = sha256_file(asset_path)
            if asset.get("sha256") and actual != str(asset["sha256"]).lower():
                errors.append(f"{label} checksum mismatch for {asset['path']}")
    return errors
