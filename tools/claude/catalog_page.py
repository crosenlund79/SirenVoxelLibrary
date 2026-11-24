"""Generate catalog/index.html - a static, dependency-free browser for the library catalog.

    python3 tools/claude/catalog_page.py

Reads catalog.json (every creator's entries) and each entry's model.json. Thumbnails are the
committed hero previews; every card links to the read-only viewer (viewer/?model=<id>), the
other preview views, the .vox master, the derived .glb, model.json and the spec page.
Works from a local clone (file://) and on GitHub Pages. No build step, no external libraries.
"""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATS = ["furniture", "household", "consumables", "medical", "survival", "architecture", "combat",
        "vegetation", "exterior", "vehicles", "regional", "characters"]
TITLES = {"furniture": "Household furniture", "household": "Household items",
          "consumables": "Consumables", "medical": "Medical", "survival": "Survival equipment",
          "architecture": "Construction", "combat": "Combat", "vegetation": "Vegetation",
          "exterior": "Exterior props", "vehicles": "Vehicles", "regional": "Regional map",
          "characters": "Characters"}


def esc(s) -> str:
    return html.escape(str(s), quote=True)


def card(m: dict, meta: dict | None) -> str:
    pid = m["preview_path"].rstrip("/")
    hero = None
    for ext in ("png", "svg"):
        if (ROOT / pid / f"hero.{ext}").exists():
            hero = f"../{pid}/hero.{ext}"
            break
    dims = " × ".join(f"{v:g}" for v in m.get("dimensions_m", [])) + " m" if m.get("dimensions_m") else ""
    cell = f"{m['voxel_size_m']:g} m cells" if m.get("voxel_size_m") else ""
    vox = f"{m['occupied_voxels']:,} voxels" if m.get("occupied_voxels") else ""
    cond = (meta or {}).get("condition") or m.get("condition") or ""
    story = (meta or {}).get("story", "")
    links = [f'<a href="../viewer/?model={esc(m["id"])}">3D viewer</a>']
    for v in ("front", "side", "scale"):
        for ext in ("png", "svg"):
            if (ROOT / pid / f"{v}.{ext}").exists():
                links.append(f'<a href="../{pid}/{v}.{ext}">{v}</a>')
                break
    links.append(f'<a href="../{esc(m["source_path"])}" download>.vox</a>')
    for d in m.get("derived_paths", []):
        links.append(f'<a href="../{esc(d)}" download>.glb</a>')
    if m.get("metadata_path"):
        links.append(f'<a href="../{esc(m["metadata_path"])}">model.json</a>')
    if meta and meta.get("spec"):
        links.append(f'<a href="../{esc(meta["spec"])}">spec</a>')
    img = (f'<img loading="lazy" src="{esc(hero)}" alt="{esc(m["id"])} hero render">' if hero
           else '<div class="noimg">no preview</div>')
    search = " ".join([m["id"], m.get("name", ""), m["category"], cond, m.get("creator", "")]).lower()
    return f'''<article class="card" data-s="{esc(search)}" data-creator="{esc(m.get("creator", ""))}">
<a class="thumb" href="{esc(hero) if hero else '#'}">{img}</a>
<div class="body"><div class="row"><span class="badge {esc(m.get('creator', '').lower())}">{esc(m.get('creator', ''))}</span>
<span class="status">{esc(m.get('status', ''))}</span></div>
<h3>{esc(m["id"])}</h3><p class="name">{esc(m.get("name", ""))}</p>
<p class="facts">{esc(dims)}<br>{esc(cell)} · {esc(vox)}{(' · ' + esc(cond)) if cond else ''}</p>
{f'<p class="story">{esc(story)}</p>' if story else ''}
<p class="links">{" · ".join(links)}</p></div></article>'''


def main():
    cat = json.loads((ROOT / "catalog.json").read_text())
    models = cat.get("models", [])
    metas = {}
    for m in models:
        p = ROOT / m.get("metadata_path", "")
        if m.get("metadata_path") and p.exists():
            metas[m["id"]] = json.loads(p.read_text())
    by = {}
    for m in models:
        by.setdefault(m["category"], []).append(m)
    order = CATS + sorted(c for c in by if c not in CATS)
    counts = {}
    for m in models:
        counts[m.get("creator", "?")] = counts.get(m.get("creator", "?"), 0) + 1
    nav = " ".join(f'<a href="#{c}">{esc(TITLES.get(c, c))} <span>{len(by[c])}</span></a>'
                   for c in order if c in by)
    sections = []
    for c in order:
        if c not in by:
            continue
        ms = sorted(by[c], key=lambda m: (m["base_id"], m.get("creator", "")))
        sheets = []
        for p in sorted((ROOT / "previews" / "categories").glob(f"Claude_{c}*.png")):
            sheets.append(f'<a href="../previews/categories/{p.name}">{p.stem}</a>')
        sheet_html = f'<p class="sheets">One-scale contact sheets: {" · ".join(sheets)}</p>' if sheets else ""
        sections.append(f'<section id="{c}"><h2>{esc(TITLES.get(c, c))} <span>{len(ms)}</span></h2>'
                        f'{sheet_html}<div class="grid">' +
                        "\n".join(card(m, metas.get(m["id"])) for m in ms) + "</div></section>")
    batch_links = " · ".join(f'<a href="../previews/batches/{p.name}">{p.stem}</a>'
                             for p in sorted((ROOT / "previews" / "batches").glob("*.png")))
    scene_links = " · ".join(f'<a href="../previews/scenes/{p.name}">{p.stem}</a>'
                             for p in sorted((ROOT / "previews" / "scenes").glob("*.png")))
    total = " · ".join(f"{k}: {v}" for k, v in sorted(counts.items()))
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Voxel Library Catalog</title>
<style>
:root{{--bg:#e9e8e3;--panel:#f6f5f1;--ink:#26292a;--sub:#5b605f;--line:#cfcdc5;--accent:#8a5a3b;--claude:#7a5c46;--gpt:#3f6258}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#1d1f1f;--panel:#262928;--ink:#e6e4de;--sub:#a5a7a2;--line:#3a3d3c;--accent:#d2a07a;--claude:#c8a083;--gpt:#8fb5a9}}}}
:root[data-theme="dark"]{{--bg:#1d1f1f;--panel:#262928;--ink:#e6e4de;--sub:#a5a7a2;--line:#3a3d3c;--accent:#d2a07a;--claude:#c8a083;--gpt:#8fb5a9}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif}}
header{{padding:28px 16px 12px;max-width:1400px;margin:auto}}h1{{margin:0 0 6px;font-size:26px}}
.lede{{color:var(--sub);margin:0 0 12px;max-width:900px}}a{{color:var(--accent)}}
nav{{position:sticky;top:0;z-index:2;background:var(--bg);border-bottom:1px solid var(--line);padding:8px 16px;display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center}}
nav a{{text-decoration:none;color:var(--ink);white-space:nowrap}}nav a span,h2 span{{color:var(--sub);font-weight:400}}
nav input{{margin-left:auto;padding:6px 10px;border:1px solid var(--line);border-radius:6px;background:var(--panel);color:var(--ink);min-width:200px}}
main{{max-width:1400px;margin:auto;padding:0 16px 40px}}h2{{margin:28px 0 4px;font-size:20px}}
.sheets{{margin:0 0 10px;color:var(--sub);font-size:13px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px}}
.card{{background:var(--panel);border:1px solid var(--line);border-radius:8px;overflow:hidden;display:flex;flex-direction:column}}
.thumb img{{display:block;width:100%;aspect-ratio:1/1;object-fit:cover;background:#b4b5b0}}.noimg{{aspect-ratio:1/1;display:grid;place-items:center;color:var(--sub)}}
.body{{padding:10px 12px 12px}}.row{{display:flex;justify-content:space-between;font-size:12px}}
.badge{{font-weight:600}}.badge.claude{{color:var(--claude)}}.badge.gpt{{color:var(--gpt)}}.status{{color:var(--sub)}}
h3{{margin:4px 0 0;font-size:14px;word-break:break-all}}.name{{margin:0;color:var(--sub)}}
.facts{{margin:6px 0;font-size:12px;color:var(--sub)}}.story{{margin:6px 0;font-size:12px}}.links{{margin:6px 0 0;font-size:12px}}
.hide{{display:none}}footer{{max-width:1400px;margin:auto;padding:0 16px 40px;color:var(--sub);font-size:12px}}
</style></head><body>
<header><h1>SirenVoxelLibrary catalog</h1>
<p class="lede">Every entry in <code>catalog.json</code> ({esc(total)}). All models are <strong>candidates</strong> awaiting the user's review; nothing here is approved or integrated into a game. Thumbnails are actual renders of the <code>.vox</code> sources. “3D viewer” opens the read-only viewer (needs the page served over http, e.g. <code>python -m http.server</code> in the repo root, or GitHub Pages).</p>
<p class="lede">Batch sheets: {batch_links or "none yet"}<br>Showcase scenes: {scene_links or "none yet"}<br>Planning: <a href="../docs/claude/MASTER_MANIFEST.md">master manifest</a> · <a href="../docs/claude/CATALOG_STYLE.md">Claude style guide</a></p></header>
<nav>{nav}<input id="q" type="search" placeholder="Filter by name, category, condition…" aria-label="Filter models"></nav>
<main>{"".join(sections)}</main>
<footer>Generated by tools/claude/catalog_page.py from catalog.json. Library axes: X right, Y front, Z up; Godot mapping in each model.json.</footer>
<script>
const q=document.getElementById('q');
q.addEventListener('input',()=>{{const t=q.value.trim().toLowerCase();
document.querySelectorAll('.card').forEach(c=>c.classList.toggle('hide',!!t&&!c.dataset.s.includes(t)));
document.querySelectorAll('section').forEach(s=>s.classList.toggle('hide',!s.querySelector('.card:not(.hide)')));}});
</script></body></html>
'''
    out = ROOT / "catalog" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page)
    print("wrote catalog/index.html with", len(models), "entries")


if __name__ == "__main__":
    main()
