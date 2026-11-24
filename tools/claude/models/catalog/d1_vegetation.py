"""Batch D1 - vegetation (creator: Claude). X right, Y front (+Y), Z up; inclusive cells.

Trees are siblings of Claude_pine_dead_small: each is a hand-authored table of limbs and
foliage masses described in metres, then voxelised (no random generators; hash01 only for
sparse, repeatable variation). Pivot of every tree = trunk base. Ground props (shrubs, logs,
stones) are drawn directly in cells.
"""
import math

import numpy as np

from catalog_registry import model
from models.pine_dead_small import _seg_cells, branch_path
from voxkit import Grid, P, hash01



def weld(g):
    """Join pieces that touch the main body only along an edge or corner (diagonal voxel
    contact) by filling one bridging cell in the piece's own colour, lowest first, so thin
    organic parts stay one 6-connected piece. Raises if a piece truly floats."""
    from collections import deque
    import numpy as np
    for _ in range(200):
        occ = g.v > 0
        lab = np.zeros(occ.shape, int)
        n = 0
        for s in map(tuple, np.argwhere(occ)):
            if lab[s]:
                continue
            n += 1
            lab[s] = n
            q = deque([s])
            while q:
                c = q.popleft()
                for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
                    b = (c[0] + d[0], c[1] + d[1], c[2] + d[2])
                    if all(0 <= b[i] < occ.shape[i] for i in range(3)) and occ[b] and \
                            not lab[b]:
                        lab[b] = n
                        q.append(b)
        if n <= 1:
            return
        sizes = np.bincount(lab.ravel())[1:]
        main = int(np.argmax(sizes)) + 1
        joined = False
        for k in range(1, n + 1):
            if k == main:
                continue
            best = None
            for c in map(tuple, np.argwhere(lab == k)):
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        for dz in (-1, 0, 1):
                            m = (c[0] + dx, c[1] + dy, c[2] + dz)
                            if not all(0 <= m[i] < occ.shape[i] for i in range(3)) or \
                                    lab[m] != main or abs(dx) + abs(dy) + abs(dz) < 2:
                                continue
                            rank = abs(dx) + abs(dy) + abs(dz)   # 2 = edge, 3 = corner
                            for ax, st in ((0, dx), (1, dy), (2, dz)):
                                if not st:
                                    continue
                                b = list(c)
                                b[ax] += st
                                b = tuple(b)
                                key = (rank, b[2])
                                if not occ[b] and (best is None or key < best[2]):
                                    best = (b, c, key)
            if best:
                b, c, _ = best
                g.v[b] = g.v[c]
                joined = True
                break
        if not joined:
            raise ValueError("a piece floats free of the model")


# ---------------------------------------------------------------------------
# metric canvas shared by the trees
# ---------------------------------------------------------------------------
class Canvas:
    """Sparse cell -> (palette role, priority, tag). Higher priority wins a cell."""

    def __init__(self, cell):
        self.cell = cell
        self.c = {}

    def put(self, q, name, prio, tag=""):
        q = tuple(int(v) for v in q)
        old = self.c.get(q)
        if old is None or prio >= old[1]:
            self.c[q] = (name, prio, tag)

    def q(self, p):
        return tuple(int(math.floor(v / self.cell)) for v in p)

    def tube(self, pts, radii, colour, prio, tag=""):
        """Polyline limb; colour is a role or fn(cell, t_along) -> role."""
        n = len(pts)
        rs = np.interp(np.linspace(0, 1, n), np.linspace(0, 1, len(radii)), radii)
        for i in range(n - 1):
            for c, t in _seg_cells(np.asarray(pts[i], float), np.asarray(pts[i + 1], float),
                                   rs[i], rs[i + 1], self.cell).items():
                tt = (i + t) / (n - 1)
                self.put(c, colour(c, tt) if callable(colour) else colour, prio, tag)

    def blob(self, ctr, rh, rz, colour, prio, tag="", ry=None, skip=None):
        """Ellipsoid mass (metres). colour may be fn(cell, d) where d is 0 centre .. 1 rim."""
        ry = rh if ry is None else ry
        cell = self.cell
        lo = [int(math.floor((ctr[i] - r) / cell)) - 1 for i, r in enumerate((rh, ry, rz))]
        hi = [int(math.ceil((ctr[i] + r) / cell)) + 1 for i, r in enumerate((rh, ry, rz))]
        for x in range(lo[0], hi[0] + 1):
            for y in range(lo[1], hi[1] + 1):
                for z in range(lo[2], hi[2] + 1):
                    cc = (np.array((x, y, z)) + 0.5) * cell - ctr
                    d = (cc[0] / rh) ** 2 + (cc[1] / ry) ** 2 + (cc[2] / rz) ** 2
                    if d <= 1.0 and not (skip and skip((x, y, z), d)):
                        self.put((x, y, z), colour((x, y, z), d) if callable(colour) else colour,
                                 prio, tag)

    def tags(self, tag):
        return {k for k, v in self.c.items() if v[2] == tag}

    def to_grid(self, pivot_m=(0.0, 0.0)):
        keys = np.array([k for k in self.c if k[2] >= 0])
        lo, hi = keys.min(0), keys.max(0)
        g = Grid(*(hi - lo + 1))
        for k in keys:
            g.v[tuple(k - lo)] = P(self.c[tuple(k)][0])
        piv = np.array(pivot_m) / self.cell - lo[:2]
        weld(g)
        return {"grid": g, "pivot_cells": (float(piv[0]), float(piv[1]), 0.0)}


def polyline_at(nodes, z):
    """Point and radius along a list of ((x, y, z), r) nodes at height z (metres)."""
    for (p0, r0), (p1, r1) in zip(nodes, nodes[1:]):
        if p0[2] <= z <= p1[2]:
            t = (z - p0[2]) / max(1e-9, p1[2] - p0[2])
            return np.array(p0) + (np.array(p1) - np.array(p0)) * t, r0 + (r1 - r0) * t
    return np.array(nodes[-1][0], float), nodes[-1][1]


def roots(cv, table, colour_top="bark_dark", colour_ground="bark_deep", z0=0.16, prio=4):
    """Root flares: (bearing deg, length m, base radius m)."""
    for az, ln, r in table:
        a = math.radians(az)
        p0 = np.array([0.0, 0.0, z0])
        p1 = np.array([math.cos(a) * ln * 0.5, math.sin(a) * ln * 0.5, 0.05])
        p2 = np.array([math.cos(a + 0.15) * ln, math.sin(a + 0.15) * ln, 0.0])
        cv.tube([p0, p1, p2], [r, r * 0.65, r * 0.35],
                lambda c, t: colour_ground if c[2] == 0 else colour_top, prio, "root")


# ---------------------------------------------------------------------------
# healthy pine
# ---------------------------------------------------------------------------
PINE_TRUNK = [((0.00, 0.00, 0.00), 0.15), ((0.02, 0.01, 1.00), 0.12),
              ((0.05, 0.00, 2.40), 0.09), ((0.04, -0.02, 3.80), 0.06),
              ((0.06, -0.01, 4.70), 0.04), ((0.06, -0.01, 5.08), 0.03)]

# Whorls (height m, [(bearing deg, length m, kind), ...]); 0 deg = +X, 90 = +Y (camera side).
# Irregular spacing (a wet year grows a long internode). Wind from -X has kept the windward
# (around 180 deg) limbs short and the lee (around 0 deg) limbs long; one low limb on the
# camera side is browning ("sick"); a whorl near the top lost a limb to snow load.
PINE_WHORLS = [
    (0.58, [(30, 0.22, "stub"), (215, 0.20, "stub")]),
    (0.98, [(8, 1.38, "limb"), (70, 1.30, "limb"), (124, 1.02, "limb"), (178, 1.22, "sick"),
            (248, 1.22, "limb"), (318, 1.24, "limb")]),
    (1.44, [(40, 1.28, "limb"), (102, 1.22, "limb"), (166, 0.86, "limb"), (232, 1.04, "limb"),
            (284, 1.24, "limb"), (352, 1.30, "limb")]),
    (1.84, [(18, 1.10, "limb"), (88, 1.10, "limb"), (148, 0.84, "limb"), (214, 0.74, "limb"),
            (272, 1.08, "limb")]),
    (2.30, [(60, 0.98, "limb"), (124, 0.80, "limb"), (190, 0.62, "limb"), (250, 0.82, "limb"),
            (318, 0.96, "limb"), (2, 1.04, "limb")]),
    (2.68, [(30, 0.84, "limb"), (104, 0.66, "limb"), (172, 0.52, "limb"), (288, 0.74, "limb")]),
    (3.12, [(72, 0.66, "limb"), (140, 0.52, "limb"), (208, 0.44, "limb"), (262, 0.58, "limb"),
            (342, 0.72, "limb")]),
    (3.50, [(16, 0.56, "limb"), (96, 0.46, "limb"), (178, 0.36, "limb"), (300, 0.50, "limb")]),
    (3.90, [(56, 0.42, "limb"), (132, 0.34, "limb"), (226, 0.30, "limb"), (330, 0.44, "limb")]),
    (4.26, [(4, 0.34, "limb"), (110, 0.26, "limb"), (282, 0.28, "limb")]),   # lost one to snow
    (4.58, [(48, 0.22, "limb"), (168, 0.16, "limb"), (290, 0.20, "limb")]),
]


@model("healthy_pine",
       story="A self-sown pine at the back of a garden that nobody got round to taking down. "
             "It is thriving now: dense dark tiers, the windward side clipped short by winter "
             "storms, one low limb on the path side browning where road salt splashed it.",
       details=["Eleven hand-authored whorls of drooping, slightly upturned limbs carrying "
                "layered needle pads", "Gaps between tiers so the layering reads from the "
                "game camera", "Short windward (-X) limbs, a top whorl that lost a limb",
                "Bare lower trunk with two old snapped stubs and gripping root flares",
                "One browning lower limb on the camera side"],
       exclusions=["No pine cones (sub-cell)", "No random scatter of needle colours"],
       pivot_note="Trunk base centre at ground level; the crown is slightly lopsided toward "
                  "the lee (+X) side.",
       collision_hint="Capsule r=0.15 m, h=5.1 m at the pivot (trunk); foliage non-colliding.",
       notes=["Same metric whorl-table method as Claude_pine_dead_small (its dead sibling).",
              "Prevailing wind modelled from -X like the dead pine."])
def healthy_pine():
    cv = Canvas(0.1)
    cv.tube([np.array(p) for p, _ in PINE_TRUNK], [r for _, r in PINE_TRUNK],
            lambda c, t: "bark_dark" if c[2] < 4 else ("bark_mid" if c[2] < 14 else "bark"),
            5, "trunk")
    roots(cv, [(190, 0.50, 0.09), (285, 0.42, 0.08), (25, 0.46, 0.09), (115, 0.36, 0.07)])
    pads = []                      # (centre, rh, rz, scheme, outer)
    for wi, (h, limbs) in enumerate(PINE_WHORLS):
        base, _ = polyline_at(PINE_TRUNK, h)
        for li, (az, ln, kind) in enumerate(limbs):
            j = hash01(wi, li, seed=41) - 0.5
            if kind == "stub":
                pts = branch_path(base, az, ln, 6, 2, 0, n=3)
                cv.tube(pts, [0.04, 0.03], "bark_mid", 3, "limb")
                cv.put(cv.q(pts[-1]), "snag", 3, "limb")
                continue
            sick = kind == "sick"
            # limb: level near the trunk, drooping, the very tip lifting again (a sick limb
            # just droops)
            pts = branch_path(base, az, ln, 3 + 4 * j, (-34 if sick else -15) - 6 * j, 8 * j,
                              n=7)
            if not sick:
                pts[-1] = pts[-1] + np.array([0, 0, 0.07])
            # inner third of the limb shows bark; the outer part is hidden by its needle pad
            cv.tube(pts[:3], [0.045, 0.035], "bark_mid", 3, "limb")
            cv.tube(pts[2:], [0.035, 0.02], "twig" if sick else "conifer_deep", 0, "limb")
            ts = (0.42, 0.62, 0.80, 0.96) if sick else (0.30, 0.48, 0.66, 0.83, 0.97)
            for k, t in enumerate(ts):
                i = t * (len(pts) - 1)
                p = pts[int(i)] + (pts[min(int(i) + 1, len(pts) - 1)] - pts[int(i)]) * (i % 1)
                w = 0.15 + 0.17 * math.sin(math.pi * min(1.0, t * 1.04)) + 0.03 * (k % 2)
                w *= min(1.0, 0.55 + ln * 0.45) * (0.8 if sick else 1.0)
                rz = (0.10 if sick else 0.12) + 0.03 * ((k + wi) % 2)
                pads.append((p + np.array([0, 0, 0.03]), w, rz, "sick" if sick else "live",
                             t > 0.78))
        # inner core of each tier so the trunk does not show through the crown
        if h > 0.8:
            rmax = max(l for _, l, k in limbs if k != "stub")
            pads.append((base + np.array([0, 0, 0.03]), 0.26 + 0.22 * rmax, 0.13, "core",
                         False))
    # leader spire above the last whorl
    top, _ = polyline_at(PINE_TRUNK, 4.70)
    for dz, w in [(0.0, 0.15), (0.14, 0.11), (0.27, 0.07)]:
        pads.append((top + np.array([0, 0, dz]), w, 0.11, "live", False))
    for ctr, rh, rz, scheme, outer in pads:
        tag = scheme + ("_tip" if outer else "")
        cv.blob(np.asarray(ctr, float), rh, rz, tag, 2 if scheme == "sick" else 1, "needles")
    # colour the needles by exposure: lit crowns, dark undersides, deep core near the trunk;
    # the lightest green only on the upper face of the outermost (new-growth) tips
    for q in cv.tags("needles"):
        scheme = cv.c[q][0]
        up = (q[0], q[1], q[2] + 1) in cv.c
        down = (q[0], q[1], q[2] - 1) in cv.c
        rad = math.hypot((q[0] + 0.5) * 0.1, (q[1] + 0.5) * 0.1)
        if scheme.startswith("sick"):
            # browning from the tip inward: the half nearest the trunk is still dull green
            if rad < 0.62:
                name = "needle_olive" if not up else "needle_dark"
            else:
                name = "needle_rust" if not up else ("needle_dry" if not down else "needle_dark")
        elif scheme == "core" or rad < 0.3:
            name = "conifer_deep" if up else "conifer_dark"
        elif not up:
            name = "conifer_hi" if scheme == "live_tip" else "conifer"
        elif not down:
            name = "conifer_deep" if rad < 0.6 else "conifer_dark"
        else:
            name = "conifer_mid"
        cv.c[q] = (name, cv.c[q][1], "needles")
    return cv.to_grid()


# ---------------------------------------------------------------------------
# leafless deciduous tree
# ---------------------------------------------------------------------------
# Hand-authored limbs: (name, [(x, y, z) m ...], (r_start, r_end) m, twig fan at the end?)
# An oak-like yard tree: short trunk, three spreading scaffold limbs from one fork, a leader,
# a lower limb to the back, secondary limbs that arch upward at their ends.
DECID_LIMBS = [
    ("trunk", [(0, 0, 0), (0.02, 0.0, 0.8), (0.06, 0.02, 1.5), (0.08, 0.03, 1.86)],
     (0.24, 0.16), False),
    ("lee", [(0.08, 0.03, 1.86), (0.45, 0.0, 2.12), (0.95, -0.08, 2.30), (1.38, -0.14, 2.46),
             (1.60, -0.18, 2.78)], (0.10, 0.04), True),
    ("camera", [(0.08, 0.03, 1.86), (-0.22, 0.30, 2.16), (-0.66, 0.62, 2.38),
                (-1.10, 0.86, 2.56), (-1.42, 0.98, 2.90)], (0.10, 0.04), True),
    ("leader", [(0.08, 0.03, 1.86), (0.10, -0.04, 2.60), (0.06, -0.18, 3.30),
                (0.12, -0.28, 3.74), (0.10, -0.32, 4.06)], (0.11, 0.035), True),
    ("back", [(0.06, 0.02, 1.52), (0.00, -0.36, 1.78), (-0.10, -0.84, 1.98),
              (-0.20, -1.28, 2.24), (-0.26, -1.48, 2.56)], (0.08, 0.035), True),
    ("leader_w", [(0.10, -0.04, 2.60), (-0.40, -0.08, 2.92), (-0.88, -0.16, 3.18),
                  (-1.18, -0.24, 3.54)], (0.07, 0.03), True),
    ("leader_e", [(0.06, -0.18, 3.30), (0.44, 0.08, 3.56), (0.84, 0.30, 3.80),
                  (1.00, 0.44, 4.12)], (0.06, 0.03), True),
    ("lee_up", [(0.95, -0.08, 2.30), (1.04, 0.30, 2.70), (1.12, 0.62, 3.10), (1.16, 0.78, 3.46)],
     (0.05, 0.03), True),
    ("lee_back", [(1.38, -0.14, 2.46), (1.30, -0.55, 2.70), (1.22, -0.92, 3.00)],
     (0.04, 0.03), True),
    ("camera_up", [(-0.66, 0.62, 2.38), (-0.72, 0.48, 2.90), (-0.78, 0.42, 3.36),
                   (-0.68, 0.36, 3.78)], (0.05, 0.03), True),
    ("camera_low", [(-1.10, 0.86, 2.56), (-1.20, 1.30, 2.62), (-1.26, 1.52, 2.86)],
     (0.04, 0.03), True),
    ("back_w", [(-0.10, -0.84, 1.98), (-0.54, -1.00, 2.28), (-0.94, -1.12, 2.58)],
     (0.045, 0.03), True),
    # a limb that snapped in a storm: a short jagged stub with pale broken wood
    ("snapped", [(0.04, 0.05, 1.20), (0.10, 0.34, 1.32), (0.12, 0.50, 1.38)], (0.07, 0.05),
     False),
]
# Branchlets at a limb end, in the limb's local frame (forward, side, up) metres: long enough
# (0.4-0.6 m) to stay separate lines at 0.1 m cells, steep enough to avoid 45-degree stairs.
TWIG_FAN = [[(0.10, 0.08, 0.30), (0.16, 0.14, 0.62)], [(0.24, -0.04, 0.18), (0.46, -0.08, 0.34)],
            [(0.04, -0.20, 0.26), (0.06, -0.34, 0.54)], [(0.28, 0.20, 0.04), (0.50, 0.30, 0.10)],
            [(-0.04, 0.24, 0.22), (-0.08, 0.40, 0.40)]]
CROWN_SCALE = 0.75          # the table was drawn large; scaled to the 3.3 x 3.1 m brief


@model("leafless_deciduous",
       story="An old yard oak that died the summer before everything stopped. Nobody came to "
             "fell it: a storm has already snapped one low limb, bracket fungus is eating the "
             "trunk and the bark is lifting off the big limbs in pale patches.",
       details=["Short buttressed trunk forking at 1.9 m into three spreading scaffold limbs "
                "and a leader", "Secondary limbs arch upward and end in fans of fine twigs, "
                "giving a broad, lacy crown outline", "Snapped low limb with pale broken wood",
                "Two shelves of bracket fungus on the trunk (camera side)",
                "Bark lifted off the tops of the main limbs"],
       exclusions=["No leaves (dead tree)", "No random branching generator"],
       pivot_note="Trunk base centre at ground level.",
       collision_hint="Capsule r=0.18 m, h=1.9 m at the pivot (trunk); crown non-colliding.",
       notes=["Limbs and twig fans are a hand-authored table, voxelised from metres."])
def leafless_deciduous():
    cv = Canvas(0.1)
    off = np.array([0.05, 0.05, 0.0])            # trunk on a cell centre: odd-width trunk
    roots(cv, [(200, 0.60, 0.11), (300, 0.44, 0.09), (30, 0.55, 0.11), (120, 0.46, 0.10),
               (250, 0.34, 0.08)], z0=0.24)

    def scaled(p):
        p = np.array(p, float)
        return off + np.array([p[0] * CROWN_SCALE, p[1] * CROWN_SCALE, p[2]])

    ends = []
    for name, pts, (r0, r1), fan in DECID_LIMBS:
        pts = [scaled(p) for p in pts]
        if name == "trunk":
            def col(c, t):
                if c[2] < 3:
                    return "bark_dark"
                # dark vertical furrows keep the trunk from reading as a smooth block
                return "bark_mid" if (c[0] * 2 + c[1]) % 4 else "bark_dark"
        else:
            def col(c, t, r0=r0):
                return "bark" if r0 >= 0.06 else "bark_hi"
        cv.tube(pts, [r0, r1], col, 5 if name == "trunk" else 4, "wood")
        if fan:
            ends.append((pts[-1], pts[-1] - pts[-2]))
        if name == "snapped":
            cv.put(cv.q(pts[-1]), "break_fresh", 6, "wood")
            cv.put(cv.q(pts[-1] + np.array([0, -0.06, 0.1])), "snag_light", 6, "wood")
    # bark lifted off the upper faces of the two big scaffold limbs (pale dead wood)
    for q, (nm, pr, tg) in list(cv.c.items()):
        top = (q[0], q[1], q[2] + 1) not in cv.c
        if tg == "wood" and nm == "bark" and top and 6 <= q[0] <= 10 and -2 <= q[1] <= 1:
            cv.c[q] = ("snag", pr, tg)
        if tg == "wood" and nm == "bark" and top and -7 <= q[0] <= -4 and 4 <= q[1] <= 7:
            cv.c[q] = ("snag_dark", pr, tg)
    # branchlets: the fine outer crown, lighter grey than the limbs
    for ei, (p, d) in enumerate(ends):
        f = np.array([d[0], d[1], 0.0])
        f = f / (np.linalg.norm(f) or 1)
        s = np.array([-f[1], f[0], 0.0])
        u = np.array([0, 0, 1.0])
        for ti, tw in enumerate(TWIG_FAN):
            if hash01(ei, ti, seed=77) < 0.2:
                continue                          # sparse, repeatable gaps
            path = [p] + [p + f * a + s * b + u * c for a, b, c in tw]
            cv.tube(path, [0.03, 0.02], "bark_hi", 2, "twig")
    # bracket fungus: two shelves on the camera (-X) side of the trunk
    for zc, ys, xs in ((6, (-1, 0, 1), (-2, -3)), (9, (0, 1), (-2,))):
        for y in ys:
            for x in xs:
                cv.put((x, y, zc), "card_hi", 6, "fungus")
            cv.put((-2, y, zc - 1), "card_dark", 6, "fungus")
    return cv.to_grid(pivot_m=(0.05, 0.05))


# ---------------------------------------------------------------------------
# small leafy tree
# ---------------------------------------------------------------------------
# Foliage clumps (centre m, rh, rz, lobes [(dx, dy, dz, r) relative, metres], yellowing?)
LEAFY_CLUMPS = [
    ((-0.76, 0.26, 2.22), 0.54, 0.48, [(-0.18, 0.26, 0.10, 0.30)], True),     # yellowing
    ((0.78, -0.10, 2.42), 0.58, 0.50, [(0.20, -0.30, 0.14, 0.32)], False),
    ((0.04, 0.00, 3.20), 0.60, 0.54, [(-0.24, -0.16, 0.18, 0.32)], False),
    ((0.14, 0.80, 2.02), 0.50, 0.44, [(0.24, 0.10, 0.08, 0.26)], False),
    ((-0.26, -0.76, 2.52), 0.52, 0.46, [(-0.22, -0.14, 0.04, 0.28)], False),
    ((0.58, 0.56, 2.82), 0.44, 0.42, [], False),
    ((-0.56, -0.14, 2.92), 0.44, 0.42, [], False),
]
# unit-ish directions for the bumps on a clump (hand-picked, deliberately not symmetric)
BUMP_DIRS = [(0.0, 0.0, 1.0), (0.62, 0.10, 0.70), (-0.55, 0.32, 0.72), (0.12, -0.66, 0.66),
             (-0.20, 0.70, 0.55), (0.92, -0.30, 0.10), (-0.88, -0.36, 0.20), (0.30, 0.90, 0.05),
             (-0.30, -0.92, 0.0), (0.70, 0.62, -0.30), (-0.66, 0.58, -0.32),
             (0.52, -0.70, -0.30)]
LEAFY_TRUNK = [((0.0, 0.0, 0.0), 0.13), ((0.03, 0.01, 0.7), 0.11), ((0.06, 0.03, 1.28), 0.10)]


def leafy_masses(cv, clumps, seed=12, bump=0.34, dark=False):
    """Foliage clumps [(centre m, rh, rz, lobes, yellowing)] drawn as a core plus a ring of
    bumps (crests and cavities, not smooth stepped shells), then coloured as material zones:
    light crests, mid tops, darker sides low down, deep undersides."""
    cell = cv.cell
    owner = {}
    for ci, (ctr, rh, rz, lobes, yel) in enumerate(clumps):
        c = np.array(ctr)
        parts = [(c, rh * 0.78, rz * 0.8)]
        for k, (dx, dy, dz) in enumerate(BUMP_DIRS):
            if hash01(ci, k, seed=seed) < 0.18:
                continue
            br = rh * (bump + 0.08 * hash01(ci, k, seed=seed + 1))
            parts.append((c + np.array([dx * rh * 0.7, dy * rh * 0.7, dz * rz * 0.72]), br,
                          br * 0.85))
        parts += [(c + np.array(l[:3]), l[3], l[3] * 0.8) for l in lobes]
        for pc, prh, prz in parts:
            cv.blob(pc, prh, prz, "leaf", 1, "leaf",
                    skip=lambda q, d: (q[2] + 0.5) * cell < 0)
            for q, v in cv.c.items():
                if v[2] == "leaf" and q not in owner:
                    owner[q] = ci
    for q in cv.tags("leaf"):
        ctr, rh, rz, lobes, yel = clumps[owner.get(q, 0)]
        x, y, z = q
        up = (x, y, z + 1) in cv.c
        down = (x, y, z - 1) in cv.c or z == 0
        zrel = ((z + 0.5) * cell - ctr[2]) / rz
        crest = not up and sum((n in cv.c) for n in ((x + 1, y, z + 1), (x - 1, y, z + 1),
                                                     (x, y + 1, z + 1), (x, y - 1, z + 1))) == 0
        if yel:
            hi, mid, lo = ("grass_hi", "grass_hi", "grass") if not dark else \
                ("dead_leaf_dark", "twig", "leaf_dark")
        else:
            hi, mid, lo = ("leaf_hi", "leaf", "leaf_mid") if not dark else \
                ("leaf", "leaf_mid", "leaf_dark")
        if not down:
            name = "leaf_deep" if zrel > -0.25 or dark else "leaf_dark"
        elif not up:
            name = hi if crest and zrel > -0.1 else mid
        elif zrel < -0.35:
            name = "leaf_deep" if dark else "leaf_dark"
        else:
            name = lo
        cv.c[q] = (name, 1, "leaf")
    return owner



@model("small_leafy_tree",
       story="An ornamental garden tree planted when the house was new. Nobody has watered or "
             "pruned it since the summer things stopped; the lower clump on the path side is "
             "already yellowing and a water sprout has shot up from the fork.",
       details=["Short trunk forking at 1.3 m into five limbs", "Six lumpy foliage clumps "
                "with gaps between them so limbs show through", "Lit crowns and darker "
                "undersides as material zones, not noise", "One clump yellowing on the camera "
                "side", "Root flares and a pruning scar on the trunk"],
       exclusions=["No individual leaves", "No fruit or blossom"],
       pivot_note="Trunk base centre at ground level.",
       collision_hint="Capsule r=0.12 m, h=1.3 m at the pivot (trunk); crown non-colliding.",
       notes=["Clumps and limbs are a hand-authored table, voxelised from metres."])
def small_leafy_tree():
    cv = Canvas(0.1)
    cv.tube([np.array(p) for p, _ in LEAFY_TRUNK], [r for _, r in LEAFY_TRUNK],
            lambda c, t: "bark_dark" if c[2] < 3 else "bark_mid", 5, "wood")
    roots(cv, [(210, 0.42, 0.08), (320, 0.34, 0.07), (40, 0.40, 0.08), (130, 0.30, 0.07)])
    fork = np.array(LEAFY_TRUNK[-1][0])
    # limbs from the fork up into each clump (stopping inside it)
    for ci, (ctr, rh, rz, lobes, yel) in enumerate(LEAFY_CLUMPS):
        c = np.array(ctr)
        mid = fork + (c - fork) * np.array([0.45, 0.45, 0.62])
        cv.tube([fork, mid, c - np.array([0, 0, rz * 0.5])], [0.08, 0.05, 0.035], "bark", 4,
                "wood")
    cv.tube([fork, fork + np.array([0.02, -0.04, 0.55]), fork + np.array([-0.02, -0.06, 0.95])],
            [0.04, 0.025], "bark_hi", 3, "wood")                  # water sprout
    cv.put((-1, 0, 8), "snag_dark", 6, "wood")                    # old pruning scar
    leafy_masses(cv, LEAFY_CLUMPS, seed=12)
    return cv.to_grid()


# ---------------------------------------------------------------------------
# bush
# ---------------------------------------------------------------------------
BUSH_CLUMPS = [
    ((-0.27, 0.10, 0.36), 0.31, 0.30, [(-0.10, 0.16, -0.08, 0.16)], False),
    ((0.22, 0.14, 0.42), 0.32, 0.33, [(0.16, 0.10, 0.10, 0.15)], False),
    ((0.00, -0.20, 0.52), 0.33, 0.31, [(-0.12, -0.06, 0.16, 0.15)], False),
    ((0.36, -0.18, 0.30), 0.21, 0.24, [], False),
    ((-0.37, -0.20, 0.27), 0.20, 0.22, [], False),
    ((-0.20, 0.32, 0.25), 0.20, 0.21, [], True),        # browning where the dog went
    ((0.14, 0.33, 0.27), 0.18, 0.18, [], False),
]


@model("bush",
       story="A privet-type shrub under a front window, clipped square for years and now "
             "growing out shaggy. The top has gone lumpy and uneven, and one low corner by "
             "the path has browned.",
       details=["Six overlapping lobes of different heights for an uneven top", "Bumpy crest "
                "and cavity structure, dark gaps between lobes", "Bare stems visible under "
                "the lifted front lobe", "One small browning lobe at a low corner"],
       exclusions=["No flowers or berries", "No soil mound (sits on any ground)"],
       why="At 0.10 m the 1 m shrub is a 10-cell lump with no lobes; 0.05 m keeps the uneven "
           "top and the gaps.",
       collision_hint="Ellipsoid 1.1 x 0.95 x 0.8 m on the pivot; soft, non-blocking.")
def bush():
    cv = Canvas(0.05)
    stems = [((0.02, 0.24, 0.0), (0.04, 0.28, 0.22)), ((-0.06, 0.18, 0.0), (-0.14, 0.22, 0.24)),
             ((0.10, 0.16, 0.0), (0.18, 0.20, 0.26)), ((0.0, 0.0, 0.0), (0.02, -0.04, 0.40)),
             ((-0.08, 0.04, 0.0), (-0.22, 0.08, 0.30)), ((0.08, 0.02, 0.0), (0.22, 0.10, 0.34))]
    for a, b in stems:
        cv.tube([np.array(a), np.array(b)], [0.03, 0.025],
                lambda c, t: "twig" if c[2] else "bark_deep", 3, "wood")
    leafy_masses(cv, BUSH_CLUMPS, seed=21, bump=0.36, dark=True)
    return cv.to_grid()


# ---------------------------------------------------------------------------
# dead shrub
# ---------------------------------------------------------------------------
# Main stems from the woody crown (polylines, metres) and side shoots (stem index, t, end).
SHRUB_STEMS = [
    [(0.00, 0.00, 0.03), (-0.10, 0.05, 0.30), (-0.24, 0.10, 0.56), (-0.36, 0.14, 0.74)],
    [(0.02, 0.00, 0.03), (0.10, 0.06, 0.32), (0.20, 0.12, 0.60), (0.28, 0.16, 0.80)],
    [(0.00, -0.02, 0.03), (0.02, -0.12, 0.36), (0.06, -0.22, 0.64), (0.03, -0.28, 0.84)],
    [(-0.02, 0.00, 0.03), (-0.16, -0.12, 0.20), (-0.34, -0.26, 0.34), (-0.48, -0.36, 0.42)],
    [(0.02, -0.02, 0.03), (0.18, -0.08, 0.18), (0.36, -0.16, 0.30), (0.54, -0.22, 0.38)],
    [(0.00, 0.02, 0.03), (-0.04, 0.16, 0.22), (-0.08, 0.34, 0.42), (-0.10, 0.48, 0.54)],
    [(0.02, 0.02, 0.03), (0.14, 0.18, 0.14), (0.28, 0.32, 0.24), (0.42, 0.42, 0.28)],
]
SHRUB_SHOOTS = [(0, 0.55, (0.02, 0.10, 0.20)), (0, 0.8, (-0.12, -0.04, 0.10)),
                (1, 0.5, (0.14, -0.06, 0.18)), (1, 0.75, (-0.08, 0.10, 0.14)),
                (2, 0.6, (-0.12, -0.04, 0.16)), (3, 0.6, (0.00, -0.10, 0.20)),
                (4, 0.6, (0.06, 0.12, 0.18)), (5, 0.6, (0.14, 0.06, 0.18)),
                (6, 0.55, (0.00, 0.10, 0.20)), (2, 0.85, (0.10, 0.02, 0.06)),
                (0, 0.35, (-0.14, 0.04, 0.12)), (1, 0.3, (0.04, 0.12, 0.16)),
                (2, 0.35, (0.10, -0.06, 0.22)), (3, 0.35, (-0.08, 0.06, 0.20)),
                (3, 0.8, (-0.06, -0.12, 0.12)), (4, 0.35, (0.02, -0.12, 0.20)),
                (4, 0.85, (0.10, 0.04, 0.12)), (5, 0.35, (-0.12, 0.02, 0.18)),
                (5, 0.9, (0.08, 0.06, 0.10)), (6, 0.85, (0.08, -0.06, 0.14)),
                (1, 0.9, (0.10, 0.02, 0.06))]
# a few brown leaves still clinging: (stem index, t)
SHRUB_LEAVES = [(0, 0.95), (5, 0.7), (6, 0.85), (1, 0.62), (3, 0.9)]


@model("dead_shrub",
       story="A flowering shrub by a driveway that died of drought after the sprinklers "
             "stopped. Only a few curled brown leaves still cling to the stems, and dry grass "
             "has grown up around the woody base.",
       details=["Seven stems from one woody crown, each with side shoots, splaying into a "
                "loose vase", "Weathered grey tips, browner wood low down", "Five small "
                "clusters of curled brown leaves", "Tuft of dry grass around the base"],
       exclusions=["No green growth", "No random branching generator"],
       why="Twigs at 0.10 m would be as thick as a wrist; 0.05 m keeps the stems spindly.",
       collision_hint="None (walk-through dressing); optional cylinder r=0.4 m, h=0.8 m.")
def dead_shrub():
    cv = Canvas(0.05)
    paths = []
    for si, st in enumerate(SHRUB_STEMS):
        pts = [np.array(p, float) + np.array([0.025, 0.025, 0]) for p in st]
        paths.append(pts)
        cv.tube(pts, [0.035, 0.022],
                lambda c, t: "bark_mid" if t < 0.3 else ("twig" if t < 0.7 else "snag_dark"),
                3, "wood")
    for si, t, d in SHRUB_SHOOTS:
        pts = paths[si]
        i = t * (len(pts) - 1)
        p = pts[int(i)] + (pts[min(int(i) + 1, len(pts) - 1)] - pts[int(i)]) * (i % 1)
        cv.tube([p, p + np.array(d)], [0.02, 0.02], "snag_dark", 2, "wood")
    for si, t in SHRUB_LEAVES:
        pts = paths[si]
        i = t * (len(pts) - 1)
        p = pts[int(i)] + (pts[min(int(i) + 1, len(pts) - 1)] - pts[int(i)]) * (i % 1)
        q = cv.q(p)
        for dx, dy, dz, col in ((0, 0, -1, "dead_leaf_dark"), (1, 0, -1, "dead_leaf"),
                                (0, 1, -1, "dead_leaf"), (1, 0, 0, "dead_leaf")):
            cv.put((q[0] + dx, q[1] + dy, q[2] + dz), col, 1, "leaf")
    # woody crown and dry grass skirt around it
    cv.blob(np.array([0.025, 0.025, 0.02]), 0.09, 0.07, "bark_dark", 4, "wood",
            skip=lambda q, d: q[2] < 0)
    for k, (ang, h) in enumerate(((20, 4), (75, 5), (130, 3), (200, 5), (250, 4), (310, 3),
                                  (350, 4), (165, 4))):
        a = math.radians(ang)
        x, y = int(round(2.2 * math.cos(a))), int(round(2.2 * math.sin(a)))
        for z in range(h):
            lean = 1 if z >= h - 1 else 0
            cv.put((x + int(round(math.cos(a))) * lean, y + int(round(math.sin(a))) * lean, z),
                   "grass_dry" if z >= h - 2 else "grass", 2, "grass")
    return cv.to_grid(pivot_m=(0.025, 0.025))


# ---------------------------------------------------------------------------
# grass clump
# ---------------------------------------------------------------------------
# Blades (base x, base y, height cells, bearing deg, reach cells, kind): kind "g" green with a
# dry tip, "d" last year's dead blade (dry all along, flopped further), "s" short new shoot.
GRASS_BLADES = [
    (12, 9, 17, 95, 2, "g"), (13, 8, 16, 30, 2, "g"), (11, 8, 15, 160, 2, "g"),
    (13, 10, 15, 60, 3, "g"), (11, 10, 14, 130, 3, "g"), (12, 11, 14, 85, 3, "g"),
    (14, 8, 13, 0, 4, "g"), (10, 9, 13, 185, 4, "g"), (12, 7, 14, 265, 3, "g"),
    (14, 7, 12, 320, 4, "g"), (10, 7, 12, 225, 4, "g"), (15, 10, 11, 20, 5, "g"),
    (9, 11, 11, 165, 5, "g"), (11, 11, 12, 110, 4, "g"), (15, 11, 8, 50, 7, "d"),
    (9, 8, 8, 190, 9, "d"), (13, 6, 8, 290, 6, "d"), (16, 9, 7, 352, 9, "d"),
    (12, 10, 9, 75, 1, "s"), (11, 9, 8, 200, 1, "s"), (14, 9, 9, 340, 1, "s"),
    (10, 12, 10, 140, 4, "g"), (14, 12, 7, 70, 6, "d"), (16, 8, 9, 0, 4, "s"),
    (12, 8, 16, 250, 1, "g"), (13, 9, 15, 10, 1, "g"), (12, 10, 13, 120, 2, "g"),
    (11, 7, 11, 240, 3, "g"), (13, 11, 12, 45, 3, "g"), (10, 8, 10, 170, 5, "g"),
]


@model("grass_clump",
       story="A tussock of rough grass that has seeded itself in a crack at the edge of a "
             "lawn nobody mows any more, with a broad-leaved weed and one tall seed stalk "
             "pushing through it.",
       details=["24 hand-placed blades arching outward from one crown, green bodies with "
                "straw-dry tips", "Last year's dead blades flopped over at the sides",
                "A broad-leaved weed rosette and one tall seed stalk", "Dense dark root crown"],
       exclusions=["No flowers", "No soil disc (sits on any ground)"],
       why="Blades need 2.5 cm cells; at 5 cm the clump is a dozen thick sticks.",
       collision_hint="None (walk-through dressing).")
def grass_clump():
    g = Grid(28, 22, 18)
    ox, oy = 1, 1
    for bi, (bx, by, h, az, reach, kind) in enumerate(GRASS_BLADES):
        a = math.radians(az)
        ux, uy = math.cos(a), math.sin(a)
        last = None
        for z in range(h):
            t = z / max(1, h - 1)
            off = reach * t ** (1.5 if kind != "d" else 1.1)
            x = ox + bx + int(round(ux * off))
            y = oy + by + int(round(uy * off))
            zz = z if kind != "d" else int(round(z * (1 - 0.35 * t)))
            if last is not None:                            # walk one axis step at a time
                cur = list(last)
                for ax, tgt in ((0, x), (1, y), (2, zz)):
                    while cur[ax] != tgt:
                        cur[ax] += 1 if tgt > cur[ax] else -1
                        if tuple(cur) != (x, y, zz):
                            g.set(*cur, g.get(*cur) or "grass")
            frac = z / max(1, h - 1)
            if kind == "d":
                col = "grass_dry" if frac > 0.3 else "dead_leaf_dark"
            elif kind == "s":
                col = "grass_hi" if frac > 0.5 else "grass"
            else:
                col = "grass_dry" if z >= h - 2 else ("grass_hi" if frac > 0.5 else
                                                       ("grass" if frac > 0.15 else "leaf_mid"))
            g.set(x, y, zz, col)
            last = (x, y, zz)
    # root crown: dense dark base the blades grow out of
    for x in range(ox + 9, ox + 17):
        for y in range(oy + 6, oy + 13):
            d = ((x - ox - 12.8) / 4.2) ** 2 + ((y - oy - 9.3) / 3.6) ** 2
            if d <= 1.0:
                g.set(x, y, 0, "leaf_dark" if d > 0.5 else "soil_dark")
                if d <= 0.55:
                    g.set(x, y, 1, "leaf_mid")
    # broad-leaved weed rosette on the camera side, leaves lying out from the crown
    for (x0, y0, x1, y1, z) in ((ox + 5, oy + 12, ox + 8, oy + 13, 1),
                                (ox + 8, oy + 15, ox + 9, oy + 17, 1),
                                (ox + 5, oy + 9, ox + 7, oy + 10, 2)):
        g.box(x0, y0, z, x1, y1, z, "leaf")
        g.paint(x0, y0, z, x0, y0, z, "leaf_hi")
    g.box(ox + 8, oy + 10, 0, ox + 9, oy + 14, 1, "leaf_mid")
    g.box(ox + 7, oy + 9, 1, ox + 8, oy + 10, 1, "leaf_mid")
    # seed stalk: thin, tall, a brown seed head
    for z in range(1, 16):
        g.set(ox + 9, oy + 13, z, "twig" if z > 5 else "leaf_mid")
    g.box(ox + 9, oy + 13, 14, ox + 9, oy + 13, 17, "dead_leaf_dark")
    g.set(ox + 8, oy + 13, 15, "dead_leaf_dark")
    g.set(ox + 9, oy + 14, 16, "dead_leaf")
    weld(g)
    return {"grid": g, "footprint_cells": ((ox + 9, ox + 16), (oy + 6, oy + 12))}


# ---------------------------------------------------------------------------
# fallen log
# ---------------------------------------------------------------------------
# Moss strip along the top: (x0, x1, half-width in cells around the crown line)
LOG_MOSS = [(6, 9, 1), (10, 15, 2), (16, 22, 3), (23, 27, 2), (28, 31, 3), (32, 35, 1)]


@model("fallen_log",
       story="A trunk section that came down across the back of a park years ago and was "
             "never cleared. The root end has rotted hollow, moss has crept along the shaded "
             "top, and the far end shows the old splintered break.",
       details=["10-cell round section, bottom row sunk into the ground", "Lengthwise bark "
                "furrows (coherent lines, not speckle)", "Hollow rotted end with punky wood "
                "crumbled onto the ground (camera side)", "Splintered pale break at the far "
                "end", "Moss strip along the top, a patch of bark lost on the front",
                "Three branch stubs"],
       exclusions=["No fungus brackets (kept for the dead tree)", "No leaf litter"],
       collision_hint="Capsule along X, r=0.24 m, length 2.5 m.")
def fallen_log():
    L = 51
    g = Grid(L + 2, 13, 12)
    ox, cy, cz = 1, 6.0, 4.0                 # section centre (cells); bottom row is sunk
    sec = g.disc_cells(cy, cz, 4.9)
    rim = set(g.ring_cells(cy, cz, 4.9))
    sec_far = g.disc_cells(cy - 0.5, cz - 0.5, 4.6)      # far end tapers to 9 cells
    rim_far = set(g.ring_cells(cy - 0.5, cz - 0.5, 4.6))
    TAPER = ox + 33

    def section(x):
        return (sec, rim, cy, cz) if x < TAPER else (sec_far, rim_far, cy - 0.5, cz - 0.5)

    for x in range(ox, ox + L):
        s_, r_, ccy, ccz = section(x)
        for (j, k) in s_:
            if k < 0:
                continue
            g.set(x, j, k, "bark_mid")
            if (j, k) not in r_:
                continue
            ang = math.degrees(math.atan2(k + 0.5 - ccz, j + 0.5 - ccy)) % 360
            line = int(ang // 24)
            # bark furrows: lengthwise lines, each broken at its own places (knots, splits)
            gap = hash01(line, x // 5, seed=19) < 0.22
            if line % 2 == 0 and int(ang) % 24 < 9 and not gap:
                g.set(x, j, k, "bark_dark")
            elif k <= 1:
                g.set(x, j, k, "bark_deep")         # damp underside against the ground
            elif 40 < ang < 140 and k >= 7:
                g.set(x, j, k, "bark")              # weathered top
    # lost bark on the front (+Y) face: silvered wood with grain
    for x in range(ox + 29, ox + 40):
        for (j, k) in rim:
            if j >= cy + 2 and 2 <= k <= 6 and not (x == ox + 29 and k > 4):
                g.set(x, j, k, "snag" if (k + x // 4) % 3 else "snag_dark")
    # rotted hollow at the -X (camera side) end
    for x in range(ox, ox + 7):
        depth = x - ox
        for (j, k) in g.disc_cells(cy, cz + 0.3, 3.0 - 0.25 * depth):
            if k >= 1:
                g.set(x, j, k, 0)
        for (j, k) in g.ring_cells(cy, cz + 0.3, 3.0 - 0.25 * depth):
            if k >= 1 and g.get(x, j, k):
                g.set(x, j, k, "wood_deep" if depth < 2 else "soil_dark")
    g.box(ox, 0, 0, ox, 12, 11, 0)                    # nothing at the far rim face yet
    for (j, k) in sec:                                # ragged end face: punky rotten wood
        if k < 0:
            continue
        if math.hypot(j + 0.5 - cy, k + 0.5 - cz - 0.3) >= 3.0:
            g.set(ox + 1, j, k, "card_dark" if (j + k) % 3 else "wood_stain")
    for (j, k) in ((4, 8), (5, 8), (6, 8), (8, 7), (3, 7)):    # rim broken away on top
        g.set(ox + 1, j, k, 0)
        g.set(ox + 2, j, k, 0)
    for (y, z) in ((3, 0), (4, 0), (5, 0), (6, 0), (4, 1), (5, 1), (7, 0)):  # crumbs on ground
        g.set(ox, y, z, "card_dark" if z else "wood_stain")
    # splintered break at the +X end: pale wood, uneven length
    xe = ox + L - 1
    for (j, k) in sec_far:
        if k < 0:
            continue
        r = math.hypot(j + 0.5 - cy + 0.5, k + 0.5 - cz + 0.5)
        ext = int(hash01(j, k, seed=8) * 2.2) if r < 3.6 else 0
        for e in range(1, ext + 1):
            g.set(xe + e, j, k, "snag_light")
        g.set(xe, j, k, "snag" if r < 3.6 else g.get(xe, j, k))
    # moss along the shaded top
    for x0, x1, hw in LOG_MOSS:
        for x in range(ox + x0, ox + x1 + 1):
            for j in range(int(cy) - hw - 1, int(cy) + hw):
                for k in range(11, -1, -1):
                    if g.get(x, j, k):
                        edge = j in (int(cy) - hw - 1, int(cy) + hw - 1)
                        g.set(x, j, k, "moss_dark" if edge else "moss")
                        break
    for x in range(ox + 18, ox + 25):                      # moss cushion proud of the bark
        g.set(x, int(cy) - 1, 9, "moss")
        g.set(x, int(cy), 9, "moss" if x < ox + 24 else "moss_dark")
    # branch stubs (pale broken ends)
    for (x, y, z, dx, dy, dz, n) in ((ox + 22, 4, 9, 0, -1, 1, 1), (ox + 38, 10, 4, 0, 1, 0, 1),
                                     (ox + 11, 1, 5, 0, -1, -1, 1)):
        for s in range(n + 1):
            for (a, b) in ((0, 0), (1, 0)):
                g.set(x + a, y + dy * s, z + dz * s + b, "bark_mid")
        g.set(x, y + dy * n, z + dz * n, "snag")
        g.set(x + 1, y + dy * n, z + dz * n, "snag_dark")
    weld(g)
    return g


# ---------------------------------------------------------------------------
# tree stump
# ---------------------------------------------------------------------------
# Root buttresses: (bearing deg, reach cells from the centre, height cells at the trunk)
STUMP_ROOTS = [(15, 7.4, 4), (95, 7.6, 3), (165, 7.6, 4), (240, 6.6, 3), (300, 7.2, 4)]


@model("tree_stump",
       story="A street tree felled by the council a season before the sirens stopped; the "
             "stump was never ground out. The cut has weathered but still shows its rings, "
             "the felling hinge and a drying crack, and a sucker is trying to regrow.",
       details=["Round 0.5 m stump with five root buttresses gripping the ground",
                "Saw-cut top with growth rings, dark pith and pale sapwood", "Felling step: "
                "the back cut stands one cell above the notch, with torn hinge fibres",
                "Radial drying crack", "Moss on the shaded north (-Y) foot", "A green sucker "
                "shoot on the camera side"],
       exclusions=["No chainsaw marks finer than a cell", "No mushrooms (confetti)"],
       collision_hint="Cylinder r=0.3 m, h=0.5 m.")
def tree_stump():
    g = Grid(17, 17, 12)
    cx = cy = 8.5                                       # centre on a cell centre
    top = 8
    body = g.disc_cells(cx, cy, 4.9)
    for (i, j) in body:
        g.box(i, j, 0, i, j, top, "bark_mid")
    for (i, j) in g.disc_cells(cx, cy, 5.6):            # flare at the foot
        g.box(i, j, 0, i, j, 1, "bark_mid")
    # bark furrows (vertical) and darker damp foot
    for (i, j) in g.ring_cells(cx, cy, 4.9):
        ang = math.degrees(math.atan2(j + 0.5 - cy, i + 0.5 - cx)) % 360
        if int(ang) % 40 < 11:
            g.paint(i, j, 2, i, j, top, "bark_dark")
        g.paint(i, j, 0, i, j, 1, "bark_dark")
    for az, reach, h in STUMP_ROOTS:
        a = math.radians(az)
        for s10 in range(30, int(reach * 10) + 1, 3):
            s = s10 / 10
            x = int(math.floor(cx + math.cos(a) * s))
            y = int(math.floor(cy + math.sin(a) * s))
            hh = max(0, int(round(h * (1 - (s - 3) / (reach - 3)))))
            g.box(x, y, 0, x, y, hh, "bark_mid")
            g.set(x, y, hh, "bark")
            g.set(x, y, 0, "bark_dark")
    # the saw cut: rings by radius; the back half (-Y) stands one cell higher (back cut)
    for (i, j) in body:
        r = math.hypot(i + 0.5 - cx, j + 0.5 - cy)
        z = top + 1 if j + 0.5 < cy - 0.6 else top
        if r > 4.1:
            col = "bark"
        elif r > 3.2:
            col = "pine_light"                           # pale sapwood band
        elif r < 0.8:
            col = "wood_stain"                           # pith
        elif 2.3 < r <= 3.2:
            col = "pine_aged"                            # one dark growth ring
        else:
            col = "pine_mid"                             # heartwood
        g.box(i, j, top, i, j, z, "bark_mid")
        g.set(i, j, z, col)
    for (i, j) in body:                                  # face of the step
        if j + 0.5 < cy - 0.6 and (i, j + 1) in body and not (j + 1 + 0.5 < cy - 0.6):
            if math.hypot(i + 0.5 - cx, j + 0.5 - cy) < 4.1:
                g.set(i, j, top + 1, "pine_dark" if g.get(i, j, top + 1) != P("wood_stain")
                      else "wood_stain")
    # radial drying crack toward the camera corner (-X, +Y)
    for s in range(1, 6):
        i = int(math.floor(cx - s * 0.72))
        j = int(math.floor(cy + s * 0.70))
        for z in range(top - 2, top + 2):
            if g.get(i, j, z) and (i, j) in body:
                g.set(i, j, z, "wood_deep" if z == top else 0) if z >= top else None
        g.set(i, j, top, "wood_deep")
    # moss on the shaded north foot and roots
    for (i, j) in g.disc_cells(cx, cy, 7.8):
        if j + 0.5 < cy - 2.5:
            for z in range(0, 4):
                if g.get(i, j, z) and not g.get(i, j - 1, z):
                    g.set(i, j, z, "moss" if z else "moss_dark")
    # sucker shoot on the camera side
    sx, sy = 4, 11
    g.box(sx, sy, 2, sx, sy, 5, "twig")
    g.set(sx + 1, sy, 2, "bark_mid")
    for (dx, dy, dz, c) in ((0, 0, 6, "leaf"), (-1, 0, 5, "leaf_mid"), (0, 1, 5, "leaf_hi"),
                            (-1, 1, 6, "leaf"), (0, -1, 4, "leaf_mid")):
        g.set(sx + dx, sy + dy, dz, c)
    weld(g)
    return {"grid": g, "footprint_cells": ((3, 13), (3, 13))}


# ---------------------------------------------------------------------------
# rock and boulder: hand-authored convex facets
# ---------------------------------------------------------------------------
def faceted(g, cx, cy, planes):
    """Fill the convex solid {p : n.p <= d for every (n, d, colour)} standing on z = 0
    (p in cells relative to (cx, cy, 0)). Each surface cell takes the colour of the facet it
    lies on (the plane it is closest to), so facets read as flat chiselled planes.
    Returns {cell: facet index} for the surface."""
    P_ = [(np.array(n, float) / np.linalg.norm(n), d, c) for n, d, c in planes]
    nx, ny, nz = g.shape
    inside = np.zeros(g.shape, bool)
    for x in range(nx):
        for y in range(ny):
            for z in range(nz):
                p = np.array([x + 0.5 - cx, y + 0.5 - cy, z + 0.5])
                inside[x, y, z] = all(n @ p <= d for n, d, _ in P_)
    facet = {}
    for x, y, z in np.argwhere(inside):
        p = np.array([x + 0.5 - cx, y + 0.5 - cy, z + 0.5])
        k = int(np.argmax([n @ p - d for n, d, _ in P_]))
        g.set(x, y, z, P_[k][2])
        facet[(int(x), int(y), int(z))] = k
    return facet


def stone_masses(shape, blobs, cuts=()):
    """Union of superellipsoid masses [(cx, cy, cz, a, b, c, exponent)] (cells), clipped to
    z >= 0, minus planar fracture cuts [(normal, point)]. Returns a boolean array."""
    nx, ny, nz = shape
    X, Y, Z = np.meshgrid(np.arange(nx) + 0.5, np.arange(ny) + 0.5, np.arange(nz) + 0.5,
                          indexing="ij")
    occ = np.zeros(shape, bool)
    for cx, cy, cz, a, b, c, e in blobs:
        occ |= (np.abs((X - cx) / a) ** e + np.abs((Y - cy) / b) ** e +
                np.abs((Z - cz) / c) ** e) <= 1.0
    for n, p0 in cuts:
        n = np.array(n, float) / np.linalg.norm(n)
        occ &= ((X - p0[0]) * n[0] + (Y - p0[1]) * n[1] + (Z - p0[2]) * n[2]) <= 0
    return occ


def stone_colour(g, occ, cut_planes=(), north_moss=0):
    """Colour surface zones by orientation: bleached tops, grey flanks, a warmer front, dark
    damp undersides and foot, fresh pale fracture faces, moss on the north (-Y) side."""
    nx, ny, nz = occ.shape
    pad = np.pad(occ, 1)
    for x, y, z in np.argwhere(occ):
        nb = pad[x:x + 3, y:y + 3, z:z + 3]
        if nb.all():
            g.v[x, y, z] = P("stone")
            continue
        off = np.argwhere(~nb) - 1
        n = off.sum(0).astype(float)
        n /= (np.linalg.norm(n) or 1)
        on_cut = any(abs((np.array([x, y, z]) + 0.5 - np.array(p0)) @
                         (np.array(cn) / np.linalg.norm(cn))) < 0.9 for cn, p0 in cut_planes)
        if z == 0:
            col = "stone_dark"
        elif on_cut:
            col = "concrete_hi"
        elif n[2] > 0.62:
            col = "concrete"
        elif n[2] < -0.25:
            col = "stone_dark"
        elif n[1] < -0.45:
            col = "stone_dark"
        elif n[1] > 0.45:
            col = "gravel"
        else:
            col = "stone"
        if north_moss and n[1] < -0.3 and z >= 1 and (n[2] > -0.2):
            col = "moss" if n[2] > 0.25 or z > north_moss else "moss_dark"
        g.v[x, y, z] = P(col)


@model("rock",
       story="A lump of granite turned up when the estate was built and left at the edge of a "
             "verge as a marker. Decades of weather have rounded its edges and lichen has "
             "taken the top; an old frost split left one flat face.",
       details=["Two overlapping rounded masses, broad at the foot", "One flat fracture face "
                "on the camera side, paler than the weathered skin", "Coherent lichen patch on "
                "the crown, moss on the damp north (-Y) foot"],
       exclusions=["No granite speckle (confetti)"],
       collision_hint="Box 0.7 x 0.55 x 0.44 m.")
def rock():
    g = Grid(16, 13, 10)
    blobs = [(6.8, 6.2, 1.2, 6.4, 5.0, 7.6, 2.4), (11.0, 5.4, 0.6, 3.8, 3.7, 5.6, 2.4)]
    cuts = [((-0.8, 0.55, 0.25), (2.6, 9.0, 4.0))]
    occ = stone_masses(g.shape, blobs, cuts)
    stone_colour(g, occ, cuts)
    for x, y, z in np.argwhere(occ):                   # lichen: one patch on the crown
        if not occ[x, y, min(z + 1, 9)] or z == 9:
            if z >= 6 and (x - 7.5) ** 2 / 7.0 + (y - 5.5) ** 2 / 3.5 <= 1.0:
                g.set(x, y, z, "lichen")
    for x, y, z in np.argwhere(occ):                   # moss at the north foot
        if z <= 1 and y <= 3 and not occ[x, max(y - 1, 0), z] or (z <= 1 and y == 0):
            if occ[x, y, z]:
                g.set(x, y, z, "moss_dark" if z == 0 else "moss")
    return g


@model("boulder",
       story="A glacial erratic the developers built the park around rather than move. Its "
             "north side is furred with moss, frost has opened a fissure down the front, and "
             "a grass tuft has seeded in the crack.",
       details=["Three overlapping rounded masses, broad at the foot", "Fissure down the "
                "front (+Y) where two masses meet, dark inside, a grass tuft at its foot",
                "Moss over the north (-Y) flank and the back of the crown", "A paler old "
                "fracture face on the camera (-X) side"],
       exclusions=["No granite speckle (confetti)"],
       collision_hint="Convex hull of the voxels, or a box 1.85 x 1.55 x 1.25 m.")
def boulder():
    g = Grid(21, 18, 14)
    blobs = [(8.2, 8.6, 1.5, 7.0, 7.2, 11.4, 2.5), (14.0, 8.0, 1.0, 5.8, 6.6, 9.6, 2.5),
             (6.0, 12.2, 0.4, 4.4, 3.6, 5.4, 2.5)]
    cuts = [((-1.0, 0.25, 0.2), (1.8, 9.0, 5.0))]
    occ = stone_masses(g.shape, blobs, cuts)
    stone_colour(g, occ, cuts, north_moss=4)
    for x, y, z in np.argwhere(occ):                   # moss over the back of the crown
        if (z == 13 or not occ[x, y, z + 1]) and y <= 7 and z >= 8:
            g.set(x, y, z, "moss")
    # fissure where the two big masses meet on the front: 1 wide, 3 deep, a jog at mid height
    for z in range(2, 13):
        fx = 11 if z >= 7 else 10
        ys = [y for y in range(18) if g.get(fx, y, z)]
        if len(ys) < 7:
            continue
        yf = max(ys)
        for d in range(3):
            g.set(fx, yf - d, z, 0)
        g.set(fx, yf - 3, z, "soil_dark")
        for side in (fx - 1, fx + 1):                  # darkened lips of the crack
            if g.get(side, yf, z):
                g.set(side, yf, z, "stone_dark")
    # grass tuft seeded at the foot of the fissure: three thin blades
    ys = [y for y in range(18) if g.get(10, y, 1)]
    yb = max(ys) + 1 if ys else 15
    for (dx, h) in ((0, 3), (-1, 2), (1, 2)):
        g.box(10 + dx, yb, 0, 10 + dx, yb, h - 1, "grass")
        g.set(10 + dx, yb, h - 1, "grass_dry" if dx else "grass_hi")
    return g
