"""Review sheets for Claude's catalog, rendered from the actual .vox files.

    python3 tools/claude/sheets.py batch catalog_A        # previews/batches/Claude_catalog_A*.png
    python3 tools/claude/sheets.py category furniture     # previews/categories/Claude_furniture*.png
    python3 tools/claude/sheets.py gamecam catalog_A      # true game-camera readability strip
    python3 tools/claude/sheets.py overview               # previews/batches/Claude_catalog_overview.png

Contact sheets ("pages"): every tile on one page uses the SAME camera (three-quarter, az -35,
el 30), the same light and the SAME pixels-per-metre, so sizes compare honestly; models are
split into a large-object page and a small-object page so pickups are not reduced to dots.
The first tile of each full-scale page is the 1.75 m reference figure.

Game-camera strip: Sirens Went Quiet's camera looks down at 56 degrees from ~20 m with a 40
degree vertical FOV on a 1600 x 900 view: 900 / (2 * 20 * tan 20) = ~62 px per metre in the
view plane, so a standing 1.75 m character (foreshortened by the 56 degree pitch) is ~60 px.
Each model is rendered at exactly that scale and elevation (orthographic approximation),
then shown enlarged 2x with nearest-neighbour so the true pixels stay visible.

Showcase scenes are defined in tools/claude/scenes.py and use render_scene() below.
"""
from __future__ import annotations

import json
import math
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

import voxrender as vr  # noqa: E402
from render_previews import (HERO, font, item_at, load_model, mannequin_item,  # noqa: E402
                             smooth_background)

BG = (180, 181, 176)
INK = (40, 44, 45)
SUB = (70, 74, 74)
CATEGORY_TITLES = {
    "furniture": "Household furniture", "household": "Household items",
    "consumables": "Consumables (food and water)", "medical": "Medical", "survival":
    "Survival and workshop equipment", "architecture": "Construction", "combat": "Combat",
    "vegetation": "Vegetation", "exterior": "Exterior props", "vehicles": "Vehicles",
    "regional": "Regional map", "characters": "Characters",
}
BATCH_TITLES = {"catalog_A": "Batch A - Household essentials",
                "catalog_B": "Batch B - Building and survival",
                "catalog_C": "Batch C - Combat and medical",
                "catalog_D": "Batch D - Outdoor world",
                "catalog_E": "Batch E - Regional map",
                "catalog_F": "Batch F - Characters and enemies"}


def _rel(p):
    try:
        return p.relative_to(ROOT)
    except ValueError:
        return p


def all_metas():
    return [json.loads(p.read_text()) for p in sorted(ROOT.glob("models/*/Claude_*/model.json"))]


# ---------------------------------------------------------------------------
# tile rendering (each tile is its own scene -> no giant mixed-resolution grids)
# ---------------------------------------------------------------------------
def _extent(base_id, az, el, with_ref=False):
    m = load_model(base_id)
    sc = vr.Scene([item_at(m)])
    pts, _, _ = sc.occupied_corners()
    _, r, u = vr.Camera(az, el, 10, 10).basis()
    return np.ptp(pts @ r), np.ptp(pts @ u)


def _ref_extent(az, el, map_scale=False):
    it = mannequin_item(0, 0, 0.25 if map_scale else 0.05)
    sc = vr.Scene([it])
    pts, _, _ = sc.occupied_corners()
    _, r, u = vr.Camera(az, el, 10, 10).basis()
    return np.ptp(pts @ r), np.ptp(pts @ u)


def render_tile(args):
    """args: (base_id | '__ref__' | '__refmap__', w, h, ppm, az, el, aa, k)"""
    key, w, h, ppm, az, el, aa, k = args
    if key.startswith("__ref"):
        sc = vr.Scene([mannequin_item(0, 0, 0.25 if key == "__refmap__" else 0.05)])
    else:
        sc = vr.Scene([item_at(load_model(key))])
    pts, _, _ = sc.occupied_corners()
    cam = vr.Camera(az, el, w, h).fit(pts, margin=0.0)
    cam.ppm = ppm
    lin, cover = vr.render(sc, cam, aa=aa, k=k)
    return np.asarray(smooth_background(vr.tonemap(lin), cover))


def contact_page(ids, title, subtitle, out, cols=5, W=1600, map_scale=False, ref=True,
                 aa=4, k=12, workers=3):
    az, el = HERO
    margin, head, lab = 36, 104, 58
    tw = (W - 2 * margin) // cols
    keys = (["__refmap__" if map_scale else "__ref__"] if ref else []) + list(ids)
    ext = [(_ref_extent(az, el, map_scale) if kk.startswith("__ref") else _extent(kk, az, el))
           for kk in keys]
    wmax = max(e[0] for e in ext)
    hmax = max(e[1] for e in ext)
    # one scale for the page: limited by the widest object and (softly) by the tallest
    ppm = min((tw - 24) / wmax, (tw * 1.7 - 24) / hmax)
    rows = math.ceil(len(keys) / cols)
    row_h = []
    for r_ in range(rows):
        hs = [e[1] for e in ext[r_ * cols:(r_ + 1) * cols]]
        row_h.append(int(max(tw * 0.45, max(hs) * ppm + 30)) + lab)
    row_y = [head + sum(row_h[:i]) for i in range(rows)]
    H = head + sum(row_h) + 28
    img = Image.new("RGB", (W, H), BG)
    jobs = [(kk, tw, row_h[n // cols] - lab, ppm, az, el, aa, k) for n, kk in enumerate(keys)]
    with ProcessPoolExecutor(max_workers=workers) as ex:
        tiles = list(ex.map(render_tile, jobs))
    d = ImageDraw.Draw(img)
    d.text((margin, 22), title, font=font(30, True), fill=INK)
    d.text((margin, 64), subtitle + f" · one camera, one light, {ppm:.0f} px/m on every tile · "
           "status: candidate (awaiting user review)", font=font(15), fill=SUB)
    metas = {m["base_id"]: m for m in all_metas()}
    for n, (kk, t) in enumerate(zip(keys, tiles)):
        x = margin + (n % cols) * tw
        y = row_y[n // cols]
        th = row_h[n // cols]
        img.paste(Image.fromarray(t), (x, y))
        if kk.startswith("__ref"):
            d.text((x + 10, y + th - lab + 6), "1.75 m reference figure", font=font(14, True),
                   fill=INK)
            d.text((x + 10, y + th - lab + 26), "same scale as every tile", font=font(12), fill=SUB)
            continue
        m = metas[kk]
        dims = " × ".join(f"{v:g}" for v in m["dimensions_m"]) + " m"
        d.text((x + 10, y + th - lab + 4), m["id"], font=font(14, True), fill=INK)
        d.text((x + 10, y + th - lab + 23), f"{dims} · {m['voxel_size_m']:g} m cells", font=font(12),
               fill=SUB)
        d.text((x + 10, y + th - lab + 39), f"{m['occupied_voxels']:,} voxels · {m.get('condition', 'pilot model')}",
               font=font(12), fill=SUB)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.quantize(colors=224, method=Image.Quantize.MEDIANCUT,
                 dither=Image.Dither.NONE).save(out, optimize=True)
    print("wrote", _rel(out), f"({len(ids)} models, {ppm:.1f} px/m)")
    return out


def split_pages(metas):
    """Large objects vs small objects, so a can is not drawn at sofa scale."""
    large = [m for m in metas if m["voxel_size_m"] >= 0.05]
    small = [m for m in metas if m["voxel_size_m"] < 0.05]
    pages = []
    if large:
        pages.append(("large objects", large))
    if small:
        pages.append(("small objects and pickups", small))
    return pages


def sort_key(m):
    return (m["category"], -max(m["dimensions_m"]), m["base_id"])


def sheet_for(metas, stem, title, outdir, cols_large=5, cols_small=6):
    outs = []
    pages = split_pages(sorted(metas, key=sort_key))
    for i, (label, ms) in enumerate(pages):
        suffix = "" if len(pages) == 1 or i == 0 else "_small"
        map_scale = all(m["voxel_size_m"] >= 0.5 for m in ms)
        # very large pages are split into chunks of 20 to keep the scale useful
        chunks = [ms[j:j + 19] for j in range(0, len(ms), 19)]
        for c, chunk in enumerate(chunks):
            sfx = suffix + (f"_{c + 1}" if len(chunks) > 1 else "")
            outs.append(contact_page(
                [m["base_id"] for m in chunk], title + (f" ({label}" + (
                    f", page {c + 1}/{len(chunks)})" if len(chunks) > 1 else ")")),
                f"{len(chunk)} Claude candidates", outdir / f"{stem}{sfx}.png",
                cols=cols_large if "large" in label else cols_small, map_scale=map_scale))
    return outs


# ---------------------------------------------------------------------------
# true game-camera readability strip
# ---------------------------------------------------------------------------
GAME_EL = 56.0
GAME_PPM = 62.0


def gamecam(ids, title, out, enlarge=2):
    keys = ["__ref__"] + list(ids)
    tiles = []
    jobs = []
    for kk in keys:
        if kk == "__ref__":
            w, h = _ref_extent(0.0, GAME_EL)
        else:
            w, h = _extent(kk, 0.0, GAME_EL)
        tw = int(max(28, math.ceil(w * GAME_PPM) + 12))
        th = int(max(28, math.ceil(h * GAME_PPM) + 12))
        jobs.append((kk, tw, th, GAME_PPM, 0.0, GAME_EL, 4, 8))
    with ProcessPoolExecutor(max_workers=3) as ex:
        tiles = list(ex.map(render_tile, jobs))
    W = 1600
    pad, gap, lab = 30, 14, 34
    x, y, rowh = pad, 110, 0
    placed = []
    for kk, t in zip(keys, tiles):
        im = Image.fromarray(t).resize((t.shape[1] * enlarge, t.shape[0] * enlarge), Image.NEAREST)
        cw = max(im.width, 104)
        if x + cw > W - pad:
            x, y, rowh = pad, y + rowh + lab + gap, 0
        placed.append((kk, im, x, y, cw))
        x += cw + gap
        rowh = max(rowh, im.height)
    H = y + rowh + lab + pad
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((pad, 22), title, font=font(28, True), fill=INK)
    d.text((pad, 62), f"True game-camera scale: {GAME_EL:.0f}° down, {GAME_PPM:.0f} px/m "
           "(a 1.75 m figure is ~60 px at the default 20 m zoom), each tile enlarged "
           f"{enlarge}x with nearest-neighbour so the real pixels stay visible.", font=font(14),
           fill=SUB)
    for kk, im, px, py, cw in placed:
        img.paste(im, (px + (cw - im.width) // 2, py + rowh_for(placed, py) - im.height))
        name = "1.75 m ref" if kk == "__ref__" else kk
        d.text((px + cw / 2, py + rowh_for(placed, py) + 6), name[:17], font=font(11), fill=SUB,
               anchor="mt")
    out.parent.mkdir(parents=True, exist_ok=True)
    img.quantize(colors=200, method=Image.Quantize.MEDIANCUT,
                 dither=Image.Dither.NONE).save(out, optimize=True)
    print("wrote", _rel(out))
    return out


def rowh_for(placed, py):
    return max(im.height for _, im, _, y, _ in placed if y == py)


# ---------------------------------------------------------------------------
# showcase scenes
# ---------------------------------------------------------------------------
def top_height(base_id, fx=0.5, fy=0.5):
    """Height (m) of the highest voxel at a fractional footprint position of a model."""
    m = load_model(base_id)
    g = m["grid"]
    i = min(g.shape[0] - 1, int(fx * g.shape[0]))
    j = min(g.shape[1] - 1, int(fy * g.shape[1]))
    col = np.nonzero(g[i, j, :])[0]
    return 0.0 if col.size == 0 else (col.max() + 1) * m["meta"]["voxel_size_m"]


def render_scene(placements, out, title, subtitle, views=("hero", "game"), W=1600, H=900,
                 ref_at=None, aa=4, k=16, grid=1.0):
    """placements: list of dicts {id, x, y, z=0, rot=0}; x, y are pivot positions in metres."""
    items = []
    for p in placements:
        m = load_model(p["id"])
        items.append((m, p))
    base = min([m["meta"]["voxel_size_m"] for m, _ in items] + [0.05])
    its = [item_at(m, (p["x"], p["y"]), z=p.get("z", 0.0), quarter_turns=p.get("rot", 0), snap=base)
           for m, p in items]
    if ref_at is not None:
        its.append(mannequin_item(ref_at[0], ref_at[1], 0.05))
    sc = vr.Scene(its, base_cell=base)
    pts, _, _ = sc.occupied_corners()
    outs = []
    for v in views:
        az, el = (HERO if v == "hero" else (0.0, GAME_EL))
        cam = vr.Camera(az, el, W, H).fit(pts, margin=0.06)
        cam.center = cam.center - vr.Camera(az, el, 1, 1).basis()[2] * (30 / cam.ppm)
        lin, cover = vr.render(sc, cam, aa=aa, k=k, grid_lines=grid)
        img = smooth_background(vr.tonemap(lin), cover)
        d = ImageDraw.Draw(img)
        d.text((32, 22), title, font=font(28, True), fill=INK)
        view = ("three-quarter review camera" if v == "hero" else
                f"game-camera angle ({GAME_EL:.0f}° down, orthographic)")
        d.text((32, 60), f"{subtitle} · {view} · {cam.ppm:.0f} px/m · floor grid {grid:g} m",
               font=font(15), fill=SUB)
        o = out.with_name(out.stem + ("" if v == "hero" else "_gamecam") + out.suffix)
        o.parent.mkdir(parents=True, exist_ok=True)
        img.quantize(colors=224, method=Image.Quantize.MEDIANCUT,
                     dither=Image.Dither.NONE).save(o, optimize=True)
        print("wrote", _rel(o))
        outs.append(o)
    return outs


# ---------------------------------------------------------------------------
# overview (thumbnails from hero.png - not to scale)
# ---------------------------------------------------------------------------
def overview(out):
    metas = sorted(all_metas(), key=lambda m: (list(CATEGORY_TITLES).index(m["category"]),
                                               m["base_id"]))
    W, cols, th, pad = 1600, 12, 128, 24
    cats = []
    for c in CATEGORY_TITLES:
        ms = [m for m in metas if m["category"] == c]
        if ms:
            cats.append((c, ms))
    H = 96 + sum(36 + math.ceil(len(ms) / cols) * (th + 22) for _, ms in cats) + pad
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((pad, 20), "Claude catalog overview", font=font(30, True), fill=INK)
    d.text((pad, 60), f"{len(metas)} Claude candidates · hero thumbnails (auto-framed, NOT to "
           "scale; see the category sheets for one-scale comparisons) · all awaiting user review",
           font=font(15), fill=SUB)
    y = 96
    for c, ms in cats:
        d.text((pad, y + 6), f"{CATEGORY_TITLES[c]} ({len(ms)})", font=font(18, True), fill=INK)
        y += 36
        for n, m in enumerate(ms):
            x = pad + (n % cols) * ((W - 2 * pad) // cols)
            yy = y + (n // cols) * (th + 22)
            p = ROOT / m["previews"]["hero"] if "previews" in m else None
            if not p or not p.exists():
                p = ROOT / "previews" / m["category"] / m["id"] / "hero.png"
            if p.exists():
                im = Image.open(p).convert("RGB")
                im = im.crop((0, 0, im.width, int(im.height * 0.86))).resize((th, int(th * 0.86)))
                img.paste(im, (x, yy))
            d.text((x, yy + int(th * 0.86) + 4), m["base_id"][:20], font=font(10), fill=SUB)
        y += math.ceil(len(ms) / cols) * (th + 22)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.quantize(colors=240, method=Image.Quantize.MEDIANCUT,
                 dither=Image.Dither.NONE).save(out, optimize=True)
    print("wrote", _rel(out))


def main():
    a = sys.argv[1:]
    if not a:
        raise SystemExit(__doc__)
    cmd = a[0]
    metas = all_metas()
    if cmd == "batch":
        b = a[1]
        ms = [m for m in metas if m.get("batch") == f"Claude_{b}"]
        sheet_for(ms, f"Claude_{b}", f"Claude_{b} · {BATCH_TITLES.get(b, b)}",
                  ROOT / "previews" / "batches")
    elif cmd == "category":
        c = a[1]
        ms = [m for m in metas if m["category"] == c]
        sheet_for(ms, f"Claude_{c}", f"Claude {CATEGORY_TITLES.get(c, c)}",
                  ROOT / "previews" / "categories")
    elif cmd == "gamecam":
        b = a[1]
        ms = sorted([m for m in metas if m.get("batch") == f"Claude_{b}"], key=sort_key)
        gamecam([m["base_id"] for m in ms], f"Claude_{b} at the game camera",
                ROOT / "previews" / "batches" / f"Claude_{b}_gamecam.png")
    elif cmd == "overview":
        overview(ROOT / "previews" / "batches" / "Claude_catalog_overview.png")
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
