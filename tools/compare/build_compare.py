"""Build the offline GPT vs Claude comparison data and galleries (creator-neutral).

    python3 tools/compare/build_compare.py

Reads catalog.json (both creators) plus each model.json and .vox, then writes:
  viewer/data/index.js            pair index (window.SVL_INDEX) for viewer/index.html
  viewer/data/vox/<id>.js         each .vox file, base64, loaded on demand via <script> tags
                                  (works from file:// where fetch() is blocked)
  claude_gallery/index.html       Claude thumbnails (GPT keeps its own gpt_gallery/)
  compare_gallery/index.html      side-by-side thumbnail gallery, one row per object type
  START_HERE.html                 one-click entry page for GitHub Desktop users
  docs/COMPARISON_COVERAGE.md     coverage of GPT's object list by Claude models

Pairing key: base_id; a Claude model may pair under another key through its model.json
`compare_base_id` or docs/claude/manifest.json `alias` (earlier Claude names). No winner is
computed or displayed anywhere.
"""
from __future__ import annotations

import base64
import html
import json
import os
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VIEW = ROOT / "viewer"
DATA = VIEW / "data"

BATCH_NAMES = {"A": "Household", "B": "Survival and construction", "C": "Combat and consumables",
               "D": "Outdoors and vehicles", "E": "Regional voxel map",
               "F": "Characters and enemies", "X": "Claude-only extras"}


def jload(p):
    try:
        return json.loads(Path(p).read_text())
    except Exception:  # noqa: BLE001
        return None


def preview_set(entry, meta):
    """Existing preview images for a model (relative to the repo root)."""
    pp = entry.get("preview_path") or ""
    folder = pp if pp.endswith("/") else os.path.dirname(pp) + "/"
    if meta and isinstance(meta.get("previews"), dict):
        cands = meta["previews"]
    else:
        cands = {k: folder + f"{k}.png" for k in ("hero", "front", "side", "scale")}
    return {k: v for k, v in cands.items() if v and (ROOT / v).exists()}


def record(entry):
    meta = jload(ROOT / entry["metadata_path"]) if entry.get("metadata_path") else None
    meta = meta or {}
    src = ROOT / entry["source_path"]
    rec = {
        "id": entry["id"], "creator": entry.get("creator"), "base_id": entry.get("base_id"),
        "name": meta.get("name") or entry.get("name") or entry["id"],
        "category": entry.get("category"), "status": meta.get("status") or entry.get("status"),
        "revision": meta.get("revision", entry.get("revision")),
        "voxel_size_m": meta.get("voxel_size_m"), "dimensions_m": meta.get("dimensions_m"),
        "occupied_voxels": meta.get("occupied_voxels"), "pivot_voxel": meta.get("pivot_voxel"),
        "source_path": entry["source_path"], "metadata_path": entry.get("metadata_path"),
        "source_file": os.path.basename(entry["source_path"]),
        "previews": preview_set(entry, meta), "error": None, "data": None,
        "compare_base_id": meta.get("compare_base_id") or entry.get("compare_base_id"),
    }
    if not src.exists():
        rec["error"] = "source .vox not found"
    elif rec["voxel_size_m"] is None:
        rec["error"] = "model.json has no voxel_size_m (physical size unknown)"
    if src.exists():
        DATA.joinpath("vox").mkdir(parents=True, exist_ok=True)
        b64 = base64.b64encode(src.read_bytes()).decode()
        js = (f"(window.SVL_VOX_DATA=window.SVL_VOX_DATA||{{}})[{json.dumps(entry['id'])}]="
              f"{json.dumps(b64)};")
        (DATA / "vox" / f"{entry['id']}.js").write_text(js)
        rec["data"] = f"data/vox/{entry['id']}.js"
    return rec


def main():
    cat = json.loads((ROOT / "catalog.json").read_text())
    gman = jload(ROOT / "docs/GPT_catalog_manifest.json") or {"items": []}
    cman = jload(ROOT / "docs/claude/manifest.json") or {"assets": []}
    gnames = {i["base_id"]: i for i in gman["items"]}
    cinfo = {a["base_id"]: a for a in cman["assets"]}
    alias_rev = {a["alias"]: a["base_id"] for a in cman["assets"] if a.get("alias")}
    revisions = jload(ROOT / "docs/claude/needs_revision.json") or {}

    # stale data files from removed models are dropped
    if (DATA / "vox").exists():
        for f in (DATA / "vox").glob("*.js"):
            f.unlink()
    pairs = defaultdict(lambda: {"gpt": None, "claude": None})
    for e in cat["models"]:
        r = record(e)
        if e.get("creator") == "GPT":
            pairs[e["base_id"]]["gpt"] = r
        elif e.get("creator") == "Claude":
            key = r["compare_base_id"] or alias_rev.get(e["id"]) or e["base_id"]
            r["pair_key"] = key
            if pairs[key]["claude"] is not None:   # keep both: suffix the extra one
                key = f"{key}__{e['id']}"
            pairs[key]["claude"] = r
    order = {b: i for i, b in enumerate(gnames)}
    out = []
    for key, p in pairs.items():
        g = gnames.get(key, {})
        c = cinfo.get(key, {})
        batch = c.get("batch") or ("C" if key == "handgun" else "X")
        name = (c.get("name") or g.get("name") or key.replace("_", " ").title()).replace("Map: ", "")
        out.append({"key": key, "name": name, "batch": batch,
                    "category": g.get("category") or (p["claude"] or p["gpt"])["category"],
                    "gpt": p["gpt"], "claude": p["claude"],
                    "alias": (p["claude"]["id"] if p["claude"] and
                              p["claude"]["id"] != f"Claude_{key}" else None)})
    out.sort(key=lambda x: ("ABCDEFX".index(x["batch"]) if x["batch"] in "ABCDEFX" else 9,
                            order.get(x["key"], 999), x["key"]))
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    index = {"generated": now, "batches": BATCH_NAMES, "pairs": out}
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "index.js").write_text("window.SVL_INDEX=" + json.dumps(index, separators=(",", ":"))
                                   + ";\n")
    write_galleries(out, now)
    reused = {a["existing_claude"] for a in cman["assets"]
              if a.get("existing_claude") and not a.get("alias")}
    write_coverage(out, cat, revisions, now, reused)
    n_g = sum(1 for p in out if p["gpt"])
    n_c = sum(1 for p in out if p["claude"])
    n_both = sum(1 for p in out if p["gpt"] and p["claude"])
    print(f"{len(out)} object types: GPT {n_g}, Claude {n_c}, paired {n_both}")


# ---------------------------------------------------------------------------- HTML
CSS = """:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#0f171b;color:#e9e6dc;
font:14px/1.45 system-ui,Segoe UI,sans-serif}a{color:#e2c391}header{position:sticky;top:0;z-index:2;
background:#17252b;border-bottom:1px solid #2f4148;padding:14px 3vw;display:flex;gap:16px;
align-items:center;flex-wrap:wrap}header h1{margin:0;font-size:20px}header .sub{color:#9fb1ae;font-size:12px}
input[type=search]{padding:8px 10px;border-radius:6px;border:1px solid #46606a;background:#0d1519;
color:#e9e6dc;min-width:240px}main{padding:10px 3vw 40px}h2{margin:26px 0 10px;font-size:17px;
border-bottom:1px solid #2f4148;padding-bottom:6px}.muted{color:#93a6a3;font-size:12px}
nav a{margin-right:12px;font-size:13px}.tag{display:inline-block;font-size:11px;padding:1px 6px;
border-radius:9px;border:1px solid #4d646b;color:#b9c8c4;margin-left:6px}"""


def esc(s):
    return html.escape(str(s if s is not None else ""))


def fmt_dims(d):
    return " × ".join(f"{v:.2f}" for v in d) + " m" if d else "—"


def thumb(rec, prefix="../"):
    if not rec:
        return '<div class="none">Counterpart not available</div>'
    img = rec["previews"].get("hero")
    pic = (f'<img loading="lazy" src="{prefix}{esc(img)}" alt="{esc(rec["id"])} hero preview">'
           if img else '<div class="none">No preview image</div>')
    facts = (f'{fmt_dims(rec["dimensions_m"])} · {esc(rec["voxel_size_m"])} m cells · '
             f'{esc(rec["occupied_voxels"])} voxels · {esc(rec["status"])}')
    links = [f'<a href="{prefix}{esc(rec["source_path"])}">.vox</a>']
    for k in ("front", "side", "scale"):
        if k in rec["previews"]:
            links.append(f'<a href="{prefix}{esc(rec["previews"][k])}">{k}</a>')
    return (f'{pic}<div class="cap"><b>{esc(rec["id"])}</b><br><span class="muted">{facts}</span>'
            f'<br>{" · ".join(links)}</div>')


def write_galleries(pairs, now):
    # --- side-by-side gallery
    rows = []
    for b in "ABCDEFX":
        group = [p for p in pairs if p["batch"] == b]
        if not group:
            continue
        rows.append(f'<h2 id="batch-{b}">{b} · {esc(BATCH_NAMES[b])} '
                    f'<span class="muted">({len(group)})</span></h2>')
        for p in group:
            alias = (f'<span class="tag">Claude model {esc(p["alias"])} paired by alias</span>'
                     if p["alias"] else "")
            rows.append(
                f'<section class="pair" data-k="{esc((p["name"] + " " + p["key"]).lower())}">'
                f'<div class="ph"><b>{esc(p["name"])}</b> <span class="muted">{esc(p["key"])} · '
                f'{esc(p["category"])}</span>{alias} '
                f'<a class="open" href="../viewer/index.html#pair={esc(p["key"])}">Open 3D comparison →</a></div>'
                f'<div class="two"><figure><figcaption>GPT</figcaption>{thumb(p["gpt"])}</figure>'
                f'<figure><figcaption>CLAUDE</figcaption>{thumb(p["claude"])}</figure></div></section>')
    page = f"""<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>GPT vs Claude gallery</title>
<style>{CSS}.pair{{background:#152126;border:1px solid #2c3d43;border-radius:10px;margin:10px 0;padding:10px}}
.ph{{display:flex;gap:8px;align-items:baseline;flex-wrap:wrap}}.ph .open{{margin-left:auto;font-weight:600}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:8px}}figure{{margin:0;background:#0f1a1e;
border-radius:8px;overflow:hidden;border:1px solid #2a393f}}figcaption{{font-size:11px;letter-spacing:.14em;
color:#a9b8b4;padding:6px 10px;border-bottom:1px solid #2a393f}}figure img{{width:100%;max-height:300px;
object-fit:contain;display:block;background:#b4b5b0}}.cap{{padding:8px 10px;font-size:12px}}.none{{height:180px;
display:grid;place-items:center;color:#c9a38a;font-size:13px;background:repeating-linear-gradient(45deg,#121d21,
#121d21 10px,#152328 10px,#152328 20px)}}@media(max-width:700px){{.two{{grid-template-columns:1fr}}}}</style>
<header><div><h1>GPT vs Claude · side-by-side gallery</h1><div class="sub">Preview images rendered by
each creator's own tools (lighting and framing differ). For identical camera, light and world scale, use
<a href="../viewer/index.html">the 3D comparison viewer</a>. No winners are declared. Generated {esc(now)}.</div></div>
<input type="search" id="q" placeholder="Search objects…" aria-label="Search objects">
<nav>{"".join(f'<a href="#batch-{b}">{b}</a>' for b in "ABCDEFX")}</nav></header>
<main>{"".join(rows)}</main>
<script>document.getElementById('q').oninput=e=>{{const q=e.target.value.toLowerCase().trim();
document.querySelectorAll('.pair').forEach(s=>s.style.display=!q||s.dataset.k.includes(q)?'':'none')}}</script></html>"""
    (ROOT / "compare_gallery").mkdir(exist_ok=True)
    (ROOT / "compare_gallery" / "index.html").write_text(page)

    # --- Claude gallery (GPT's gallery lives in gpt_gallery/ and is left untouched)
    by_cat = defaultdict(list)
    for p in pairs:
        if p["claude"]:
            by_cat[p["claude"]["category"]].append(p)
    cards = []
    for c in sorted(by_cat):
        cards.append(f'<h2 id="{esc(c)}">{esc(c)} <span class="muted">({len(by_cat[c])})</span></h2><div class="grid">')
        for p in by_cat[c]:
            r = p["claude"]
            cards.append(f'<article class="card" data-k="{esc((r["id"] + " " + p["name"]).lower())}">'
                         f'{thumb(r)}<div class="cap"><a href="../viewer/index.html#pair={esc(p["key"])}">'
                         f'Compare in 3D →</a></div></article>')
        cards.append("</div>")
    n = sum(len(v) for v in by_cat.values())
    page = f"""<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Claude catalog gallery</title>
<style>{CSS}.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}}
.card{{background:#162227;border:1px solid #2f4148;border-radius:8px;overflow:hidden}}.card img{{width:100%;
display:block;background:#b4b5b0}}.cap{{padding:6px 10px;font-size:12px}}.none{{height:160px;display:grid;
place-items:center;color:#c9a38a}}</style>
<header><div><h1>Claude · catalog gallery</h1><div class="sub">{n} Claude candidates (status: candidate).
Thumbnails are actual renders of each .vox. <a href="../compare_gallery/index.html">Side-by-side gallery</a> ·
<a href="../gpt_gallery/index.html">GPT gallery</a> · <a href="../viewer/index.html">3D viewer</a></div></div>
<input type="search" id="q" placeholder="Search…" aria-label="Search"><nav>{"".join(f'<a href="#{esc(c)}">{esc(c)}</a>' for c in sorted(by_cat))}</nav></header>
<main>{"".join(cards)}</main><script>document.getElementById('q').oninput=e=>{{const q=e.target.value.toLowerCase();
document.querySelectorAll('.card').forEach(s=>s.style.display=!q||s.dataset.k.includes(q)?'':'none')}}</script></html>"""
    (ROOT / "claude_gallery").mkdir(exist_ok=True)
    (ROOT / "claude_gallery" / "index.html").write_text(page)

    # --- START_HERE.html
    n_pairs = sum(1 for p in pairs if p["gpt"] and p["claude"])
    n_g = sum(1 for p in pairs if p["gpt"])
    n_c = sum(1 for p in pairs if p["claude"])
    page = f"""<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Start here · SirenVoxelLibrary</title>
<style>{CSS}main{{max-width:900px;margin:auto;padding:30px 4vw}}.big{{display:grid;grid-template-columns:repeat(auto-fit,
minmax(240px,1fr));gap:14px;margin:20px 0}}.big a{{display:block;padding:18px;border-radius:10px;background:#1a2a30;
border:1px solid #3a525a;text-decoration:none;color:#f0e6d2}}.big a b{{display:block;font-size:17px;margin-bottom:6px;
color:#e8c48e}}.big a span{{color:#a9bab6;font-size:13px}}ol li{{margin:6px 0}}</style>
<main><h1>SirenVoxelLibrary · GPT vs Claude</h1>
<p class="muted">{n_g} GPT models · {n_c} Claude models · {n_pairs} object types with both versions.
Every model is a <b>candidate</b>; nothing is approved or integrated. Generated {esc(now)}.</p>
<div class="big">
<a href="viewer/index.html"><b>3D comparison viewer</b><span>Pick an object, rotate GPT and Claude side by side
with the same camera, light and world scale.</span></a>
<a href="compare_gallery/index.html"><b>Side-by-side gallery</b><span>Thumbnails of both versions for every
object type, with links into 3D.</span></a>
<a href="gpt_gallery/index.html"><b>GPT gallery</b><span>GPT's own thumbnail gallery (unchanged).</span></a>
<a href="claude_gallery/index.html"><b>Claude gallery</b><span>Claude thumbnails by category.</span></a></div>
<h2>Using it from GitHub Desktop (Windows)</h2><ol>
<li>In GitHub Desktop, switch to the branch <b>compare/gpt-vs-claude</b> and click <b>Fetch / Pull origin</b>.</li>
<li>Choose <b>Repository → Show in Explorer</b>.</li>
<li>Double-click <b>START_HERE.html</b> (this page). It opens in your browser straight from disk: no server,
no install, no internet needed.</li>
<li>Open the <b>3D comparison viewer</b>, search or pick an object, then drag to rotate (both views move
together unless you untick <i>Link cameras</i>), scroll to zoom, Shift-drag to pan.</li></ol>
<p class="muted">All model data the viewer needs is in <code>viewer/data/</code> (generated from the .vox files by
<code>tools/compare/build_compare.py</code>), so it works from <code>file://</code>. Coverage report:
<a href="docs/COMPARISON_COVERAGE.md">docs/COMPARISON_COVERAGE.md</a>.</p></main></html>"""
    (ROOT / "START_HERE.html").write_text(page)


def write_coverage(pairs, cat, revisions, now, reused):
    gpt_keys = [p for p in pairs if p["gpt"]]
    rows = []
    stat = defaultdict(int)
    for p in gpt_keys:
        c = p["claude"]
        if not c:
            s = "missing"
        elif c["id"] in revisions:
            s = "needs revision"
        elif p["alias"]:
            s = "existing Claude model (alias)"
        elif c["id"] in reused:
            s = "existing Claude model reused"
        else:
            s = "independent Claude model"
        stat[s] += 1
        note = revisions.get(c["id"], "") if c else ""
        rows.append(f"| {p['batch']} | `{p['key']}` | `{p['gpt']['id']}` | "
                    f"{'`' + c['id'] + '`' if c else '—'} | {s} | {note} |")
    extras = [p for p in pairs if not p["gpt"]]
    lines = [f"# GPT vs Claude coverage", "",
             f"Generated {now} by `tools/compare/build_compare.py` from `catalog.json`.", "",
             f"GPT object types: **{len(gpt_keys)}**. Claude coverage:", ""]
    for k in ("independent Claude model", "existing Claude model reused",
              "existing Claude model (alias)", "needs revision", "missing"):
        lines.append(f"- {k}: **{stat.get(k, 0)}**")
    lines += [f"- Claude-only extras (no GPT counterpart): **{len(extras)}**", "",
              "| Batch | Base ID | GPT | Claude | Status | Note |", "|---|---|---|---|---|---|"] + rows
    if extras:
        lines += ["", "## Claude-only extras", ""] + [f"- `{p['claude']['id']}`" for p in extras]
    (ROOT / "docs" / "COMPARISON_COVERAGE.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
