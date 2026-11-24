"""Render catalog previews for Claude candidates straight from the .vox files on disk.

    python3 tools/claude/render_previews.py sofa armchair        # final previews
    python3 tools/claude/render_previews.py --batch catalog_A
    python3 tools/claude/render_previews.py sofa --quick --out /tmp/x   # fast iteration renders

Per model (previews/<category>/Claude_<base_id>/), all from the same .vox:
  hero.png   640x640  three-quarter view (az -35, el 30), auto-framed
  front.png  480x480  orthographic front elevation (+Y side)
  side.png   480x480  orthographic side elevation (+X side)
  scale.png  1280 wide, three-quarter view at a FIXED px/m (stated on the image) with the
             1.75 m reference figure; floor grid 0.5 m (5 m for map-scale assets)

Same sun, sky, floor and camera elevations as Claude_pilot_001 (tools/claude/voxrender.py);
the catalog profile only lowers the pixel size and stores 192-colour PNGs so ~200 models stay
light enough for git. Pilot previews were rendered at 1200 px by tools/claude/preview.py.
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

HERO = (-35.0, 30.0)
FONT_DIR = Path("/usr/share/fonts/opentype/inter")
PPM_LADDER = [480, 400, 320, 250, 200, 160, 120, 100, 80, 64, 50, 40, 32, 25, 20, 16, 12, 10,
              8, 6, 5, 4]


def font(size, bold=False):
    for name in (["Inter-SemiBold.otf", "Inter-Bold.otf"] if bold else ["Inter-Regular.otf"]):
        p = FONT_DIR / name
        if p.exists():
            return ImageFont.truetype(str(p), size)
    p = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    return ImageFont.truetype(str(p), size) if p.exists() else ImageFont.load_default()


# ---------------------------------------------------------------------------
# model loading / placement
# ---------------------------------------------------------------------------
def model_json_paths():
    return sorted(ROOT.glob("models/*/Claude_*/model.json"))


def load_model(base_or_id: str) -> dict:
    asset = base_or_id if base_or_id.startswith("Claude_") else f"Claude_{base_or_id}"
    hits = list(ROOT.glob(f"models/*/{asset}/model.json"))
    if not hits:
        raise SystemExit(f"no model.json for {asset} - run build.py first")
    meta = json.loads(hits[0].read_text())
    info = vk.read_vox(hits[0].parent / meta["source"])
    return {"meta": meta, "grid": vk.vox_to_grid(info), "palette": info["palette"][:, :3]}


def ids_for_batch(batch: str) -> list[str]:
    out = []
    for p in model_json_paths():
        m = json.loads(p.read_text())
        if m.get("batch") in (batch, f"Claude_{batch}"):
            out.append(m["base_id"])
    return out


def item_at(m, pivot_world=(0.0, 0.0), z=0.0, quarter_turns=0, snap=None):
    """Place a model so its (rotated) pivot sits at pivot_world, bottom at height z."""
    g = m["grid"]
    cell = m["meta"]["voxel_size_m"]
    px, py, _ = m["meta"]["pivot_voxel"]
    nx, ny, _ = g.shape
    q = quarter_turns % 4
    if q:
        g = vr.rot_item_z(g, q)
        for _ in range(q):  # rotate the pivot with the grid (np.rot90 CCW on axes (0, 1))
            px, py = ny - py, px
            nx, ny = ny, nx
    snap = snap or cell
    origin = (pivot_world[0] - px * cell, pivot_world[1] - py * cell, z)
    origin = tuple(round(o / snap) * snap for o in origin)
    return vr.Item(g, m["palette"], cell, origin, m["meta"]["id"])


def mannequin_item(x, y, cell):
    """1.75 m reference figure; 0.05 m cells, or a blocky 0.25 m version for map scale."""
    if cell >= 0.25:
        pal = np.zeros((256, 3), np.uint8)
        pal[1], pal[2], pal[4] = (172, 178, 179), (126, 133, 136), (150, 157, 160)
        g = np.zeros((3, 1, 7), np.uint8)
        g[0, 0, 0:3] = 2
        g[2, 0, 0:3] = 2
        g[0:3, 0, 3:6] = 4
        g[1, 0, 6] = 1
        c = 0.25
    else:
        g, pal = vr.mannequin()
        c = 0.05
    return vr.Item(g, pal, c, (round(x / c) * c, round(y / c) * c, 0.0), "ref")


# ---------------------------------------------------------------------------
# rendering
# ---------------------------------------------------------------------------
def finish(img: Image.Image, out: Path):
    out.parent.mkdir(parents=True, exist_ok=True)
    q = img.convert("RGB").quantize(colors=192, method=Image.Quantize.MEDIANCUT,
                                    dither=Image.Dither.NONE)
    q.save(out, optimize=True)


def smooth_background(rgb8: np.ndarray, cover: np.ndarray) -> Image.Image:
    """Blur only floor/background pixels (Monte-Carlo shadow grain) so PNGs compress well.
    Pixels covered by voxels are left exactly as rendered."""
    from PIL import ImageFilter
    img = Image.fromarray(rgb8)
    soft = img.filter(ImageFilter.GaussianBlur(1.6))
    w = np.clip(cover * 1.0, 0, 1)[..., None]
    out = rgb8 * w + np.asarray(soft, np.float64) * (1 - w)
    return Image.fromarray(np.clip(np.round(out), 0, 255).astype(np.uint8))


def label(img, meta, kind, extra=""):
    d = ImageDraw.Draw(img)
    W, H = img.size
    small = W < 700
    dims = " × ".join(f"{v:.2f}" for v in meta["dimensions_m"])
    view = {"hero": "three-quarter", "front": "front (+Y)", "side": "side (+X)",
            "scale": "scale view"}[kind]
    d.text((18, H - (52 if small else 62)), meta["id"], font=font(17 if small else 22, True),
           fill=(45, 49, 50))
    sub = f"{view} · {dims} m · {meta['voxel_size_m']} m cells · {meta['occupied_voxels']:,} vox"
    if not small:
        sub += " · candidate"
    if extra:
        sub += f" · {extra}"
    d.text((18, H - (26 if small else 30)), sub, font=font(12 if small else 15), fill=(70, 74, 74))


def render_view(args):
    kind, base_id, out, quick = args
    aa, k = (1, 4) if quick else (4, 16)
    m = load_model(base_id)
    meta = m["meta"]
    if kind in ("hero", "front", "side"):
        size = 640 if kind == "hero" else 480
        sc = vr.Scene([item_at(m)])
        pts, _, _ = sc.occupied_corners()
        az, el = {"hero": HERO, "front": (0.0, 0.0), "side": (90.0, 0.0)}[kind]
        cam = vr.Camera(az, el, size, size).fit(pts, margin=0.08)
        cam.center = cam.center - vr.Camera(az, el, 1, 1).basis()[2] * (22 / cam.ppm)
        lin, cover = vr.render(sc, cam, aa=aa, k=k)
        img = smooth_background(vr.tonemap(lin), cover)
        if el == 0:   # mark the support plane in elevations (the floor is edge-on)
            _, y = cam.project(np.array([0.0, 0.0, 0.0]))
            ImageDraw.Draw(img).rectangle([0, int(round(y)), size, int(round(y)) + 1],
                                          fill=(150, 151, 146))
        label(img, meta, kind)
    else:
        cell = meta["voxel_size_m"]
        mapscale = cell >= 0.5
        px, _, _ = meta["pivot_voxel"]
        minx = -px * cell
        gap = 2.0 if mapscale else 0.5
        hx = minx - gap - 0.65
        hum = mannequin_item(hx, -0.15, 0.25 if mapscale else 0.05)
        base = min(cell, hum.cell)
        sc = vr.Scene([item_at(m, snap=base), hum])
        pts, _, _ = sc.occupied_corners()
        f_, r_, u_ = vr.Camera(HERO[0], HERO[1], 10, 10).basis()
        w, h = np.ptp(pts @ r_), np.ptp(pts @ u_)
        W, HMAX = 1024, 768
        fit = min((W - 90) / w, (HMAX - 140) / h, 250)
        ppm = next((p for p in PPM_LADDER if p <= fit), PPM_LADDER[-1])
        H = int(min(HMAX, max(512, np.ceil((h * ppm + 150) / 32) * 32)))
        cam = vr.Camera(HERO[0], HERO[1], W, H).fit(pts, margin=0.0)
        cam.ppm = ppm
        cam.center = cam.center - u_ * (28 / ppm)
        lin, cover = vr.render(sc, cam, aa=aa, k=k, grid_lines=5.0 if mapscale else 0.5)
        img = smooth_background(vr.tonemap(lin), cover)
        d = ImageDraw.Draw(img)
        tx, ty = cam.project(np.array([hx + 0.33, 0.0, 1.80]))
        d.text((tx, ty - 6), "1.75 m", font=font(15), fill=(70, 74, 74), anchor="mb")
        label(img, meta, "scale",
              extra=f"fixed {ppm} px/m · grid {'5' if mapscale else '0.5'} m")
    finish(img, out)
    return str(out)


def main():
    args = sys.argv[1:]
    quick = "--quick" in args
    out_dir = Path(args[args.index("--out") + 1]) if "--out" in args else None
    views = ["hero", "front", "side", "scale"]
    if "--views" in args:
        views = args[args.index("--views") + 1].split(",")
    skip = {args[args.index(f) + 1] for f in ("--out", "--views", "--batch") if f in args}
    if "--batch" in args:
        ids = ids_for_batch(args[args.index("--batch") + 1])
    else:
        ids = [a for a in args if not a.startswith("--") and a not in skip]
    if not ids:
        raise SystemExit(__doc__)
    jobs = []
    for b in ids:
        meta = load_model(b)["meta"]
        if meta["base_id"] in {"workbench_worn", "rain_collector_basic", "wood_stove_compact",
                               "single_bed_unmade", "pine_dead_small"} and not out_dir:
            raise SystemExit(f"{b}: pilot previews are frozen (tools/claude/preview.py)")
        pdir = (out_dir / meta["id"]) if out_dir else ROOT / "previews" / meta["category"] / meta["id"]
        for kind in views:
            jobs.append((kind, meta["base_id"], pdir / f"{kind}.png", quick))
    workers = 1 if len(jobs) == 1 else 2
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for p in ex.map(render_view, jobs):
            print("wrote", p)


if __name__ == "__main__":
    main()
