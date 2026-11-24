"""Evidence for two resolution decisions in Claude_pilot_001 (rendered, not illustrated).

    python3 tools/claude/resolution_study.py   -> previews/batches/Claude_pilot_001_resolution_study.png

Left:  rain collector - rejected 0.10 m block-out (tools/claude/studies/) vs chosen 0.05 m.
Right: the SAME metric pine design voxelised at 0.20, 0.10 (chosen) and 0.05 m.
Each half uses one camera, one light and one world scale.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import voxkit as vk  # noqa: E402
import voxrender as vr  # noqa: E402
from preview import font, HERO  # noqa: E402
from models import pine_dead_small, rain_collector_basic  # noqa: E402

QUICK = "--quick" in sys.argv
AA, K = (2, 6) if QUICK else (4, 12)


def load_rejected():
    p = HERE / "studies" / "rain_collector_basic_0p10_rejected.py"
    spec = importlib.util.spec_from_file_location("rain_0p10", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.build()


def panel(entries, width, height, gap):
    """entries: list of (build result, caption). One scene, one scale, side by side."""
    cam = vr.Camera(HERO[0], HERO[1], width, height)
    f, r, u = cam.basis()
    items, centers, s = [], [], 0.0
    for res, _ in entries:
        g, _ = res["grid"].cropped()
        it = vr.Item(g.v, vk.PALETTE_RGB, res["cell"], (0, 0, 0))
        pts, _, _ = vr.Scene([it]).occupied_corners()
        pr = pts @ r
        start = s - pr.min()
        pos = r[:2] * start
        snap = 0.1
        items.append(vr.Item(g.v, vk.PALETTE_RGB, res["cell"],
                             (round(pos[0] / snap) * snap, round(pos[1] / snap) * snap, 0.0)))
        centers.append(start + (pr.min() + pr.max()) / 2)
        s = start + pr.max() + gap
    sc = vr.Scene(items)
    pts, _, _ = sc.occupied_corners()
    pr, pu = pts @ r, pts @ u
    cam.ppm = min((width - 60) / np.ptp(pr), (height - 190) / np.ptp(pu))
    cx = (pr.max() + pr.min()) / 2
    cam.center = cx * r + ((pu.max() + pu.min()) / 2 - 20 / cam.ppm) * u
    img = Image.fromarray(vr.tonemap(vr.render(sc, cam, aa=AA, k=K)[0]))
    d = ImageDraw.Draw(img)
    for (res, cap), c in zip(entries, centers):
        x = width / 2 + (c - cx) * cam.ppm
        g = res["grid"]
        lines = cap.split("\n") + [f"{g.count():,} voxels"]
        for i, ln in enumerate(lines):
            d.text((x, height - 92 + i * 22), ln, font=font(17, i == 0), fill=(45, 49, 50),
                   anchor="mt")
    return img


def main():
    left = panel([(load_rejected(), "0.10 m (suggested)\nrejected: lumpy tank, cube tap"),
                  (rain_collector_basic.build(), "0.05 m (chosen)\nclean circle, readable tap")],
                 700, 900, 0.5)
    right = panel([(pine_dead_small.build(cell=0.2), "0.20 m (suggested)\nlimb = trunk: blob"),
                   (pine_dead_small.build(cell=0.1), "0.10 m (chosen)\ncoarsest that reads"),
                   (pine_dead_small.build(cell=0.05), "0.05 m\nfiner, single-cell twigs")],
                  900, 900, 0.6)
    sheet = Image.new("RGB", (1600, 900), (180, 181, 176))
    sheet.paste(left, (0, 0))
    sheet.paste(right, (700, 0))
    d = ImageDraw.Draw(sheet)
    d.line([(700, 110), (700, 860)], fill=(150, 152, 148), width=2)
    d.text((36, 24), "Claude_pilot_001 · resolution study", font=font(30, True), fill=(40, 44, 45))
    d.text((36, 64), "Real renders of real voxel grids. Each half: one scene, one light, one world "
                     "scale. Left: rain collector. Right: one metric pine design at three cell sizes.",
           font=font(17), fill=(70, 74, 74))
    out = ROOT / "previews" / "batches" / "Claude_pilot_001_resolution_study.png"
    sheet.save(out, optimize=True)
    print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
