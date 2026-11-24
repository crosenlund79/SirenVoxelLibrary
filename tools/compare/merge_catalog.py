"""Union of the two creators' catalogs for the shared comparison branch.

    python3 tools/compare/merge_catalog.py <gpt_catalog.json> <claude_catalog.json> [out]

Every GPT entry is kept exactly as GPT wrote it, in GPT's order; every Claude entry is appended
as Claude wrote it. Entries are keyed by `id`; an id present in both inputs with different
content is a hard error (the creators own disjoint GPT_ / Claude_ namespaces, so this should
never happen). Nothing is approved, renamed or removed.
"""
import json
import sys
from pathlib import Path


def main(gpt_path, claude_path, out_path="catalog.json"):
    gpt = json.loads(Path(gpt_path).read_text())
    cla = json.loads(Path(claude_path).read_text())
    seen = {}
    merged = []
    for src, cat in (("GPT", gpt), ("Claude", cla)):
        for m in cat.get("models", []):
            if m["id"] in seen:
                if seen[m["id"]] != m:
                    raise SystemExit(f"conflicting entries for {m['id']}")
                continue
            if not m["id"].startswith(m.get("creator", src) + "_"):
                raise SystemExit(f"{m['id']} does not carry its creator prefix")
            seen[m["id"]] = m
            merged.append(m)
    out = {
        "schema_version": gpt.get("schema_version", 1),
        "library": "SirenVoxelLibrary",
        "description": ("Shared comparison catalog: GPT_ and Claude_ candidates side by side. "
                        "Entries are copied unchanged from each creator's branch; none is "
                        "approved. Pair models by base_id (Claude entries may carry "
                        "compare_base_id when an earlier Claude model satisfies a GPT object "
                        "under a different name)."),
        "models": merged,
    }
    Path(out_path).write_text(json.dumps(out, indent=2) + "\n")
    by = {}
    for m in merged:
        by[m["creator"]] = by.get(m["creator"], 0) + 1
    print(f"wrote {out_path}: {by}")


if __name__ == "__main__":
    main(*sys.argv[1:])
