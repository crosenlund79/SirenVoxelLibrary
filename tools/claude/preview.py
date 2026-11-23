"""Render Claude's candidate previews straight from the .vox files on disk.

    python3 tools/claude/preview.py            # all previews + contact sheet
    python3 tools/claude/preview.py --quick    # fast low-sample pass for iteration

Per model (previews/<category>/Claude_<base_id>/):
  hero.png   three-quarter view (az -35 deg, el 30 deg), auto-framed
  front.png  orthographic front elevation (+Y side)
  side.png   orthographic side elevation (+X side)
  scale.png  three-quarter view at a FIXED 180 px/m with the 1.75 m reference figure
Batch: previews/batches/Claude_pilot_001.png (1600x900, one scene, one world scale).
Lighting, background and cameras are identical for every model.
"""
from __future__ import annotations

import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

import voxkit as vk  # noqa: E402
import voxrender as vr  # noqa: E402

QUICK = "--quick" in sys.argv
AA, K = (2, 6) if QUICK else (4, 16)
HERO = (-35.0, 30.0)
SCALE_PPM = 250.0
FONT_DIR = Path("/usr/share/fonts/opentype/inter")


def font(size, bold=False):
    for name in (["Inter-SemiBold.otf", "Inter-Bold.otf"] if bold else ["Inter-Regular.otf"]):
        p = FONT_DIR / name
        if p.exists():
            return ImageFont.truetype(str(p), size)
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def load_models():
    cat = json.loads((ROOT / "catalog.json").read_text())
    out = []
    for m in cat["models"]:
        if m["creator"] != "Claude":
            continue
        meta = json.loads((ROOT / m["metadata_path"]).read_text())
        info = vk.read_vox(ROOT / m["source_path"])
        out.append({"meta": meta, "grid": vk.vox_to_grid(info), "palette": info["palette"][:, :3]})
    return out


def item_at(m, pivot_world=(0.0, 0.0), quarter_turns=0):
    """Place a model so its pivot sits at pivot_world on the floor."""
    g = m["grid"]
    cell = m["meta"]["voxel_size_m"]
    px, py, _ = m["meta"]["pivot_voxel"]
    origin = (pivot_world[0] - px * cell, pivot_world[1] - py * cell, 0.0)
    snap = 0.05
    origin = tuple(round(o / snap) * snap for o in origin)
    return vr.Item(g, m["palette"], cell, origin, m["meta"]["id"])


def render_view(args):
    kind, idx, out = args
    models = load_models()
    m = models[idx]
    meta = m["meta"]
    if kind in ("hero", "front", "side"):
        sc = vr.Scene([item_at(m)])
        pts, _, _ = sc.occupied_corners()
        az, el = {"hero": HERO, "front": (0.0, 0.0), "side": (90.0, 0.0)}[kind]
        cam = vr.Camera(az, el, 1200, 1200).fit(pts, margin=0.07)
        lin, _ = vr.render(sc, cam, aa=AA, k=K)
        img = Image.fromarray(vr.tonemap(lin))
        if el == 0:   # mark the support plane in elevations (ground is edge-on)
            _, y = cam.project(np.array([0.0, 0.0, 0.0]))
            d = ImageDraw.Draw(img)
            d.rectangle([0, int(round(y)), 1200, int(round(y)) + 2], fill=(150, 151, 146))
        label(img, meta, kind)
    else:   # scale view, fixed world scale, human to the -X side
        cell = meta["voxel_size_m"]
        g = m["grid"]
        px, py, _ = meta["pivot_voxel"]
        minx = -px * cell
        human_g, human_p = vr.mannequin()
        hx = minx - 0.5 - 0.65                      # 0.5 m clear gap, figure is 0.65 m wide
        hum = vr.Item(human_g, human_p, 0.05, (round(hx / 0.05) * 0.05, -0.15, 0.0), "ref")
        sc = vr.Scene([item_at(m), hum])
        pts, _, _ = sc.occupied_corners()
        f_, r_, u_ = vr.Camera(HERO[0], HERO[1], 10, 10).basis()
        need_h = np.ptp(pts @ u_) * SCALE_PPM + 230  # fixed world scale; canvas grows instead
        H = int(max(900, np.ceil(need_h / 50) * 50))
        cam = vr.Camera(HERO[0], HERO[1], 1600, H).fit(pts, margin=0.0)
        cam.ppm = SCALE_PPM
        cam.center = cam.center - u_ * (25 / SCALE_PPM)
        lin, _ = vr.render(sc, cam, aa=AA, k=K, grid_lines=0.5)
        img = Image.fromarray(vr.tonemap(lin))
        d = ImageDraw.Draw(img)
        tx, ty = cam.project(np.array([hx + 0.33, 0.0, 1.80]))
        d.text((tx, ty - 12), "1.75 m reference", font=font(20), fill=(70, 74, 74), anchor="mb")
        label(img, meta, "scale", extra=f"fixed scale {int(SCALE_PPM)} px/m · floor grid 0.5 m")
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, optimize=True)
    return str(out)


def label(img, meta, kind, extra=""):
    d = ImageDraw.Draw(img)
    W, H = img.size
    dims = " × ".join(f"{v:.2f}" for v in meta["dimensions_m"])
    view = {"hero": "three-quarter view", "front": "front elevation (+Y)",
            "side": "side elevation (+X)", "scale": "scale view"}[kind]
    d.text((28, H - 66), meta["id"], font=font(26, True), fill=(45, 49, 50))
    sub = (f"{view} · {dims} m · {meta['voxel_size_m']:.2f} m cells · "
           f"{meta['occupied_voxels']:,} voxels · candidate")
    if extra:
        sub += f" · {extra}"
    d.text((28, H - 32), sub, font=font(18), fill=(70, 74, 74))


def contact_sheet(out):
    """All five candidates in ONE scene: same camera, light and world scale."""
    models = load_models()
    by = {m["meta"]["base_id"]: m for m in models}
    W, H, TOP, BOTTOM, SIDE = 1600, 900, 112, 150, 44
    cam = vr.Camera(HERO[0], HERO[1], W, H)
    f, r, u = cam.basis()
    seq = ["pine_dead_small", "rain_collector_basic", "ref", "wood_stove_compact",
           "workbench_worn", "single_bed_unmade"]
    gap = 0.38                                       # metres of screen-space air between objects
    hum_g, hum_p = vr.mannequin()

    def placed(key, pos):
        if key == "ref":
            return vr.Item(hum_g, hum_p, 0.05, (round((pos[0] - 0.33) / .05) * .05,
                                                 round((pos[1] - 0.15) / .05) * .05, 0.0), "ref")
        return item_at(by[key], tuple(pos))

    items, anchors, s = [], {}, 0.0
    for key in seq:
        probe = vr.Scene([placed(key, np.zeros(2))])
        pts, _, _ = probe.occupied_corners()
        pr = pts @ r
        start = s - pr.min() if items else -pr.min()
        pos = r[:2] * start
        items.append(placed(key, pos))
        anchors[key] = (pos, start + (pr.min() + pr.max()) / 2)
        s = start + pr.max() + gap
    sc = vr.Scene(items)
    pts, _, _ = sc.occupied_corners()
    pr, pu = pts @ r, pts @ u
    cam.ppm = min((W - 2 * SIDE) / (pr.max() - pr.min()), (H - TOP - BOTTOM) / (pu.max() - pu.min()))
    # centre horizontally, align the content box between title and labels
    cx = (pr.max() + pr.min()) / 2
    cu = (pu.max() + pu.min()) / 2 - ((BOTTOM - TOP) / 2) / cam.ppm
    cam.center = cx * r + cu * u
    lin, _ = vr.render(sc, cam, aa=AA, k=K, grid_lines=1.0)
    img = Image.fromarray(vr.tonemap(lin))
    d = ImageDraw.Draw(img)
    d.text((SIDE, 24), "Claude_pilot_001", font=font(34, True), fill=(40, 44, 45))
    d.text((SIDE, 68), "Five Claude_ candidates in one scene · one orthographic three-quarter "
                       "camera, one light, one world scale · floor grid 1 m · status: candidate, "
                       "awaiting user review", font=font(17), fill=(70, 74, 74))
    last_right, row = -1e9, 0
    for key, (pos, sx) in anchors.items():
        x = W / 2 + (sx - cx) * cam.ppm
        if key == "ref":
            _, y = cam.project(np.array([pos[0], pos[1], 1.80]))
            d.text((x, y - 4), "1.75 m", font=font(16), fill=(70, 74, 74), anchor="mb")
            continue
        meta = by[key]["meta"]
        dims = " × ".join(f"{v:.2f}" for v in meta["dimensions_m"]) + " m"
        cells = f"{meta['voxel_size_m']:.2f} m cells · {meta['occupied_voxels']:,} voxels"
        wmax = max(d.textlength(meta["id"], font=font(16, True)), d.textlength(cells, font=font(14)))
        row = 1 - row if x - wmax / 2 < last_right + 14 else 0
        last_right = x + wmax / 2
        y = H - BOTTOM + 16 + row * 62
        d.line([(x, y - 6), (x, y - 14)], fill=(120, 124, 122), width=1)
        d.text((x, y), meta["id"], font=font(16, True), fill=(40, 44, 45), anchor="mt")
        d.text((x, y + 21), dims, font=font(14), fill=(70, 74, 74), anchor="mt")
        d.text((x, y + 39), cells, font=font(14), fill=(70, 74, 74), anchor="mt")
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, optimize=True)
    return str(out)


if __name__ == "__main__":
    models = load_models()
    jobs = []
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    for i, m in enumerate(models):
        meta = m["meta"]
        if only and meta["base_id"] not in only:
            continue
        pdir = ROOT / "previews" / meta["category"] / meta["id"]
        for kind in ("hero", "front", "side", "scale"):
            jobs.append((kind, i, pdir / f"{kind}.png"))
    with ProcessPoolExecutor(max_workers=2) as ex:
        for p in ex.map(render_view, jobs):
            print("wrote", Path(p).relative_to(ROOT))
    if not only or "sheet" in only:
        print("wrote", Path(contact_sheet(ROOT / "previews" / "batches" / "Claude_pilot_001.png"))
              .relative_to(ROOT))
