"""Claude_pine_dead_small - generator (creator: Claude).

A young pine that died standing at the edge of a clearing. The trunk leans away from
the prevailing wind (wind from -X) with an old kink; the leader snapped near 4 m and a
side branch below the break has turned up to become a crooked new top. Whorls follow
real pine growth (a ring of branches every ~0.4 m), lower whorls reduced to broken
stubs, the windward side stripped short, the lee side carrying the longest drooping
limbs and a few clinging tufts of rust-brown needles. Bark sloughs off the windward
face in pale strips; root flares grip the ground.

The tree is described in metres and voxelised at CELL, so the same design can be
compared at several resolutions. X right, Y front (+Y), Z up; pivot = trunk base.
"""
import math

import numpy as np

from voxkit import Grid, P, hash01

BASE_ID = "pine_dead_small"
CATEGORY = "vegetation"
NAME = "Small Dead Pine"
CELL = 0.10

# trunk centreline (m) and radius (m) at each node
TRUNK = [((0.00, 0.00, 0.00), 0.13), ((0.03, 0.00, 0.60), 0.11), ((0.08, -0.02, 1.40), 0.095),
         ((0.15, -0.04, 2.20), 0.08), ((0.13, 0.02, 2.75), 0.07),   # old kink
         ((0.22, 0.03, 3.40), 0.055), ((0.27, 0.02, 4.02), 0.045)]   # snapped top


def trunk_point(z):
    for (p0, r0), (p1, r1) in zip(TRUNK, TRUNK[1:]):
        if p0[2] <= z <= p1[2]:
            t = (z - p0[2]) / (p1[2] - p0[2])
            return np.array(p0) + (np.array(p1) - np.array(p0)) * t, r0 + (r1 - r0) * t
    return np.array(TRUNK[-1][0]), TRUNK[-1][1]


def branch_path(start, az, length, e0, e1, drift, n=6):
    pts = [np.array(start, float)]
    seg = length / n
    for i in range(n):
        t = (i + 0.5) / n
        e = math.radians(e0 + (e1 - e0) * t)
        a = math.radians(az + drift * t)
        d = np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)])
        pts.append(pts[-1] + d * seg)
    return pts


# Hand-authored whorls: (height m, [(bearing deg, length m, kind, tuft), ...]).
# Bearing 0 = +X (lee side, away from the wind), 90 = +Y (front), 180 = -X (windward).
# kind: "stub" = dead, snapped short; "branch" = full limb drooping at the tip.
# tuft: None, "tip" (rust needles clinging at the end) or "mid".
WHORL_TABLE = [
    (0.85, [(30, 0.26, "stub", None), (152, 0.20, "stub", None), (262, 0.30, "stub", None)]),
    (1.25, [(82, 0.32, "stub", None), (205, 0.24, "stub", None), (322, 0.36, "stub", None)]),
    (1.65, [(8, 1.28, "branch", "tip"), (104, 0.95, "branch", None), (190, 0.30, "stub", None),
            (282, 0.98, "branch", "mid")]),
    (2.05, [(338, 1.10, "branch", "tip"), (62, 1.02, "branch", None), (158, 0.30, "stub", None),
            (236, 0.30, "stub", None)]),
    (2.45, [(22, 0.98, "branch", "tip"), (128, 0.62, "branch", None), (212, 0.26, "stub", None),
            (300, 0.80, "branch", "tip")]),
    (2.85, [(352, 0.78, "branch", "tip"), (176, 0.30, "stub", None),
            (252, 0.52, "branch", None)]),
    (3.25, [(34, 0.56, "branch", None), (272, 0.46, "branch", "tip")]),
    (3.62, [(4, 0.40, "branch", None), (112, 0.28, "branch", None), (206, 0.22, "stub", None)]),
]


def design():
    """Return drawing primitives in metres: (kind, points, radii)."""
    prims = [("trunk", [np.array(p) for p, _ in TRUNK], [r for _, r in TRUNK])]
    # roots gripping the ground
    for az, ln in [(200, 0.55), (290, 0.45), (20, 0.5), (110, 0.35), (160, 0.3)]:
        a = math.radians(az)
        p0 = np.array([0, 0, 0.16])
        p1 = np.array([math.cos(a) * ln * 0.55, math.sin(a) * ln * 0.55, 0.05])
        p2 = np.array([math.cos(a + 0.2) * ln, math.sin(a + 0.2) * ln, 0.0])
        prims.append(("root", [p0, p1, p2], [0.09, 0.06, 0.03]))
    for wi, (h, limbs) in enumerate(WHORL_TABLE):
        base, _ = trunk_point(h)
        for li, (az, length, kind, tuft) in enumerate(limbs):
            j = hash01(wi, li, seed=17) - 0.5                    # tiny, repeatable variation
            if kind == "branch":
                # near-horizontal limb, drooping only toward the tip
                pts = branch_path(base, az, length, 2 + 4 * j, -10 - 6 * j, 6 * j)
            else:
                pts = branch_path(base, az, length, 4 + 6 * j, 4 + 6 * j, 0, n=3)
            prims.append((kind, pts, [0.045, 0.02]))
            if kind == "branch" and length >= 0.75:              # a side twig or two
                side = 1 if (wi + li) % 2 else -1
                for tt, sgn in ([(0.55, side), (0.78, -side)] if length >= 0.95 else [(0.6, side)]):
                    i = int(tt * (len(pts) - 1))
                    tw = branch_path(pts[i], az + sgn * 58, 0.24, -4, -12, 0, n=3)
                    prims.append(("twig", tw, [0.02, 0.015]))
            if tuft == "tip":
                prims.append(("needles", [pts[-1] - np.array([0, 0, 0.03])], [0.19]))
            elif tuft == "mid":
                prims.append(("needles", [pts[len(pts) // 2] - np.array([0, 0, 0.02])], [0.14]))
    # one long dead lower limb drooping toward the viewer, broken at the end
    base, _ = trunk_point(1.25)
    prims.append(("branch", branch_path(base, 138, 0.95, -6, -42, 10, n=7), [0.05, 0.025]))
    # the replacement leader: a branch below the break that turned skyward
    base, _ = trunk_point(3.72)
    lead = [base, base + np.array([0.10, 0.02, 0.12]), base + np.array([0.13, 0.03, 0.38]),
            base + np.array([0.11, 0.02, 0.66])]
    prims.append(("leader", lead, [0.04, 0.025]))
    prims.append(("needles", [lead[-1] + np.array([0.04, 0.0, -0.10])], [0.13]))
    return prims


def _seg_cells(p0, p1, r0, r1, cell):
    """Cells along a capsule-ish segment; at least a 6-connected 1-cell line."""
    out = {}
    L = np.linalg.norm(p1 - p0)
    n = max(2, int(L / (cell * 0.25)) + 1)
    last = None
    for t in np.linspace(0, 1, n):
        p = p0 + (p1 - p0) * t
        r = r0 + (r1 - r0) * t
        c = tuple(int(math.floor(v / cell)) for v in p)
        if last is not None and sum(abs(a - b) for a, b in zip(c, last)) > 1:
            # insert face-connected steps, dropping z last so limbs sag rather than hover
            cur = list(last)
            for ax in (0, 1, 2):
                if cur[ax] != c[ax]:
                    cur[ax] = c[ax]
                    out[tuple(cur)] = t
        out[c] = t
        last = c
        if r > cell * 0.55:
            rr = int(math.ceil(r / cell))
            for dx in range(-rr, rr + 1):
                for dy in range(-rr, rr + 1):
                    q = (c[0] + dx, c[1] + dy, c[2])
                    cc = (np.array(q[:2]) + 0.5) * cell
                    if np.hypot(*(cc - p[:2])) <= r:
                        out.setdefault(q, t)
    return out


def build(cell=CELL):
    prims = design()
    cells = {}           # (x,y,z) -> palette name; later writes win by priority
    prio = {"needles": 0, "twig": 1, "stub": 2, "branch": 2, "leader": 3, "root": 4, "trunk": 5}
    owner = {}

    def put(c, name, kind):
        if c not in owner or prio[kind] >= prio[owner[c]]:
            cells[c] = name
            owner[c] = kind

    for kind, pts, radii in prims:
        if kind == "needles":
            ctr, r = pts[0], radii[0]
            tuft = "needle_rust" if ctr[0] > 0.3 or ctr[2] < 2.4 else "needle_dry"
            if ctr[2] > 3.9:
                tuft = "needle_olive"                            # the last living tuft
            rc = int(math.ceil(r / cell)) + 1
            ci = [int(math.floor(v / cell)) for v in ctr]
            for dx in range(-rc, rc + 1):
                for dy in range(-rc, rc + 1):
                    for dz in range(-1, 2):
                        q = (ci[0] + dx, ci[1] + dy, ci[2] + dz)
                        cc = (np.array(q) + 0.5) * cell - ctr
                        d = (cc[0] / r) ** 2 + (cc[1] / r) ** 2 + (cc[2] / (r * 0.45)) ** 2
                        if d <= 1.0 and (d < 0.55 or hash01(*q, seed=3) < 0.55):
                            # one colour per tuft, darker underside: reads as a clump
                            name = tuft if dz >= 0 else "needle_dark"
                            put(q, name, kind)
            continue
        n = len(pts)
        rs = np.interp(np.linspace(0, 1, n), np.linspace(0, 1, len(radii)), radii)
        for i in range(n - 1):
            seg = _seg_cells(pts[i], pts[i + 1], rs[i], rs[i + 1], cell)
            for c, t in seg.items():
                z_m = (c[2] + 0.5) * cell
                if kind == "trunk":
                    name = "bark_dark" if z_m < 0.5 else ("bark_mid" if z_m < 1.6 else "bark")
                    # one long pale strip where bark sloughed off the windward (-X) face,
                    # and a top that has bleached silver above the old kink
                    tp, _ = trunk_point(z_m)
                    if (c[0] + 0.5) * cell < tp[0] - cell * 0.25 and 1.1 < z_m < 2.7:
                        name = "snag"
                    if z_m > 2.9:
                        name = "snag" if z_m < 3.6 else "snag_light"
                elif kind == "root":
                    name = "bark_deep" if c[2] == 0 else "bark_dark"
                elif kind == "twig":
                    name = "bark"
                else:
                    name = "bark_mid" if kind != "leader" else "bark"
                put(c, name, kind)
        # broken / dead tips show pale wood
        if kind in ("stub", "branch", "twig"):
            tip = tuple(int(math.floor(v / cell)) for v in pts[-1])
            if kind == "stub":
                # pale broken ends only on the low stubs; higher ones weather to bark tone
                put(tip, "snag" if pts[0][2] < 1.5 else "bark_hi", kind)
    cells[tuple(int(math.floor(v / cell)) for v in TRUNK[-1][0])] = "break_fresh"
    # sparse lichen on the shaded north (-Y) face of the lower trunk
    for c in list(cells):
        if owner.get(c) == "trunk" and 0.4 < (c[2] + 0.5) * cell < 1.8 and \
                hash01(*c, seed=31) < 0.22:
            tp, _ = trunk_point((c[2] + 0.5) * cell)
            if (c[1] + 0.5) * cell < tp[1] - cell * 0.2:
                cells[c] = "lichen"

    keys = np.array(list(cells))
    keys = keys[keys[:, 2] >= 0]
    lo = keys.min(0)
    hi = keys.max(0)
    g = Grid(*(hi - lo + 1))
    for c in keys:
        g.v[tuple(c - lo)] = P(cells[tuple(c)])
    base_cell = (np.array([0, 0]) / cell - lo[:2])
    return {"grid": g, "cell": cell, "pivot_cells": (float(base_cell[0]), float(base_cell[1]), 0.0)}


META = {
    "story": ("A young pine that died standing at the edge of a clearing: leaning away from "
              "the wind, leader snapped and replaced by a crooked branch, the windward side "
              "stripped, a few rust-brown tufts clinging on the lee side."),
    "resolution_tier": "standard",
    "resolution_rationale": (
        "The same metric design was voxelised at 0.20, 0.10 and 0.05 m and compared. At "
        "0.20 m (165 voxels) every branch is as thick as the trunk and the tree becomes "
        "a blobby column with no pine branching. At 0.05 m the silhouette is finer but turns "
        "into many single-cell twigs that the brief warns against and that would shimmer at "
        "distance. 0.10 m is the coarsest tier that keeps whorled pine branching, the broken "
        "ends and the snapped leader readable (trunk 2 cells, limbs 1 cell)."),
    "pivot_note": "Trunk base centre at ground level (not the bounding-box centre; the crown "
                  "leans toward +X).",
    "front_note": "Vegetation has no functional front; the drooping dead limb and the "
                  "stripped windward face are arranged toward the default camera (-X / +Y).",
    "notes": ["Prevailing wind modelled from -X: the lee (+X) side carries the longest limbs.",
              "Roots spread on the ground plane (z = 0); no soil mound, so it sits on any terrain."],
    "attachments": {},
    "collision_hint": "Capsule r=0.12 m, h=4.4 m at the pivot (trunk only); branches non-colliding.",
}
