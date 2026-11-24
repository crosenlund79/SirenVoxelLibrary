"""Batch D2 - street and yard props (creator: Claude). X right, Y front (+Y), Z up;
inclusive cell ranges. Story details face the default camera (+Y front, -X side)."""
import math

from catalog_registry import model
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
# wheelie bin (0.05 m)
# ---------------------------------------------------------------------------
@model("trash_bin",
       story="A household wheelie bin left at the kerb for a collection that never came. The "
             "lid will not shut over the last black bag someone forced in, and the lid front "
             "is rubbed pale where hands lifted it every week.",
       details=["Tapered body wider at the top, rolled rim", "Lid propped open at the front "
                "by a bulging black bag", "Two wheels on an axle and a moulded handle at the "
                "back (-Y)", "House number painted on the front as a plain pale block",
                "Grime band at the foot, rubbed lid lip"],
       exclusions=["No readable numbers or council marks", "No loose litter"],
       collision_hint="Box 0.6 x 0.5 x 0.9 m; the lid gap is cosmetic.")
def trash_bin():
    g = Grid(12, 11, 19)
    # body: footprint grows from 10x7 at the foot to 12x9 under the rim (wider at the top)
    for z in range(1, 16):
        xa, xb = (1, 10) if z < 8 else (0, 11)
        ya, yb = (2, 8) if z < 6 else ((2, 9) if z < 11 else (1, 9))
        g.box(xa, ya, z, xb, yb, z, "green_dark")
    g.box(1, 2, 0, 10, 8, 0, "green_deep")                       # base
    g.clear(1, 2, 0, 1, 2, 0)
    g.clear(10, 2, 0, 10, 2, 0)
    g.box(0, 1, 15, 11, 9, 15, "green_deep")                     # rolled rim
    g.paint(0, 9, 15, 11, 9, 15, "green")
    # side shading as material: lower front corners rubbed, foot grimy
    g.paint(0, 0, 1, 11, 10, 2, "green_deep")
    # wheels at the back corners on an axle
    for x in (0, 11):
        for (y, z) in ((1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (3, 1), (0, 2), (1, 2), (2, 2),
                       (3, 2), (1, 3), (2, 3)):
            g.set(x, y, z, "black")
        g.set(x, 1, 1, "steel_dark")
        g.set(x, 2, 2, "steel_dark")
    g.box(1, 1, 1, 10, 2, 2, "iron")                             # axle housing
    # handle across the back below the hinge
    g.box(2, 0, 13, 9, 0, 13, "green_deep")
    g.set(2, 0, 12, "green_deep")
    g.set(9, 0, 12, "green_deep")
    # lid, hinged at the back, lifted 2 cells at the front by the bag
    for y in range(0, 11):
        z = 16 + (1 if y >= 4 else 0) + (1 if y >= 8 else 0)
        g.box(0, y, z, 11, y, z, "green")
        if y in (4, 8):
            g.box(0, y, z - 1, 11, y, z - 1, "green_dark")         # stepped lid stays joined
    g.box(0, 10, 16, 11, 10, 17, "green_dark")                   # front lip hangs down
    g.paint(4, 10, 17, 7, 10, 17, "green")                       # lip rubbed where lifted
    g.box(0, 0, 16, 11, 0, 16, "green_deep")                     # hinge barrel
    g.paint(1, 5, 17, 10, 8, 18, "green_light")                  # sun-faded lid top
    # the black bag bulging out under the lid front
    g.box(3, 9, 16, 8, 9, 16, "black")
    g.box(4, 10, 15, 7, 10, 15, "charcoal")
    g.box(2, 9, 16, 2, 9, 16, "charcoal")
    g.set(5, 10, 14, "black")                                    # tied neck hanging over
    g.set(6, 10, 14, "charcoal")
    # house number: a plain pale painted block on the front
    g.paint(7, 9, 11, 8, 9, 12, "porcelain_shadow")
    return {"grid": g, "footprint_cells": ((0, 11), (1, 9))}


# ---------------------------------------------------------------------------
# mailbox (0.05 m)
# ---------------------------------------------------------------------------
@model("mailbox",
       story="A roadside mailbox on a post the mower has clipped too many times. Its red flag "
             "is still up for a letter nobody collected, and the box has filled with "
             "undelivered mail until the door no longer shuts.",
       details=["Galvanised tunnel-top box on a mounting board and a weathered 4x4 post",
                "Post leaning slightly toward the road verge (-X)", "Red flag raised on the "
                "+X side", "Door hanging open a crack with paper showing", "Rust run under "
                "the door, unmown grass around the foot of the post"],
       exclusions=["No house number text", "No newspaper box"],
       collision_hint="Box 0.1 x 0.1 x 1.0 m (post) plus box 0.3 x 0.5 x 0.25 m on top.")
def mailbox():
    g = Grid(9, 11, 26)
    # post: 2x2, set in the ground, a one-cell lean toward -X above z = 9
    for z in range(0, 18):
        dx = -1 if z >= 9 else 0
        g.box(3 + dx, 4, z, 4 + dx, 5, z, "wgrey_mid")
    g.paint(2, 4, 0, 4, 5, 2, "wgrey_wet")                       # damp foot
    g.paint(2, 4, 12, 2, 5, 17, "wgrey")                         # lit weathered face
    # mounting board
    g.box(1, 1, 18, 5, 8, 18, "wgrey_dark")
    # tunnel-top box, 6 wide (x 0..5), 10 long (y 0..9), z 19..23
    for y in range(0, 10):
        g.box(0, y, 19, 5, y, 22, "galv")
        g.box(1, y, 23, 4, y, 23, "galv_hi")
    g.paint(0, 0, 19, 5, 9, 19, "galv_dark")                     # underside band
    g.paint(0, 0, 19, 0, 9, 22, "galv_dark")
    g.paint(0, 0, 20, 0, 9, 22, "galv")
    g.box(1, 0, 19, 4, 0, 23, "galv_dark")                       # back end cap
    # door at the front: open a crack (tilted out at the top), mail showing in the gap
    g.box(0, 10, 19, 5, 10, 21, "galv_dark")
    g.box(1, 10, 22, 4, 10, 22, "galv_dark")
    g.box(1, 9, 22, 4, 9, 23, "paper")                           # envelopes in the gap
    g.set(2, 9, 23, "label_cream")
    g.box(2, 10, 23, 3, 10, 23, "steel_light")                   # latch tab
    g.paint(1, 10, 19, 1, 10, 20, "rust_deep")                   # rust run under the door
    # flag on the +X side, pivot near the back, raised
    g.box(6, 2, 21, 6, 2, 21, "steel_dark")                      # pivot bolt
    g.box(7, 2, 21, 7, 2, 25, "signal_red_dark")                 # arm
    g.box(7, 2, 24, 7, 4, 25, "signal_red_dark")                 # flag plate
    g.box(7, 3, 25, 7, 4, 25, "signal_red")
    # unmown grass around the post foot
    for (x, y, h) in ((2, 5, 3), (5, 5, 4), (2, 4, 2), (4, 6, 2), (5, 4, 2), (3, 3, 3), (3, 6, 2)):
        g.box(x, y, 0, x, y, h - 1, "grass")
        g.set(x, y, h - 1, "grass_hi")
    return {"grid": g, "footprint_cells": ((3, 4), (4, 5))}


# ---------------------------------------------------------------------------
# park bench (0.05 m)
# ---------------------------------------------------------------------------
# cast end profile (y, z) cells: legs, seat rail, arm with a scrolled front, reclined back
BENCH_END = (
    [(y, z) for y in (10, 11) for z in range(0, 9)] +                    # front leg
    [(y, z) for y in (1, 2) for z in range(0, 9)] +                      # rear leg
    [(y, 8) for y in range(1, 12)] +                                     # seat rail
    [(y, 12) for y in range(3, 12)] + [(11, 11), (11, 10), (10, 10)] +   # arm + scroll
    [(10, 9), (3, 9), (3, 10), (3, 11)] +
    [(2, 9), (2, 10), (2, 11), (2, 12), (1, 12), (1, 13), (1, 14), (0, 14), (0, 15), (0, 16)]
)


@model("outdoor_bench",
       story="A memorial park bench facing the pond path. The slats have silvered and split, "
             "one back slat broke in the middle and sags, and the little brass plaque is the "
             "only part someone still polished.",
       details=["Cast-iron ends with legs, scrolled arms and a reclined back support",
                "Four seat and two back slats of silvered timber with darker wet ends",
                "Broken lower back slat sagging in the middle", "Small brass memorial plaque "
                "(plain block, no text)", "Rust bleeding from the end fixings"],
       exclusions=["No readable plaque text", "No litter"],
       collision_hint="Box 1.55 x 0.6 x 0.45 m (seat) plus a back plane.")
def outdoor_bench():
    W = 31
    g = Grid(W, 13, 17)
    ends = (2, 28)
    for x in ends:
        for (y, z) in BENCH_END:
            g.set(x, y, z, "iron")
        for (y, z) in BENCH_END:                                         # catch-light edges
            if not g.get(x, y, z + 1) and z > 0:
                g.set(x, y, z, "iron_edge")
        g.box(x, 10, 0, x, 11, 0, "iron_dark")
        g.box(x, 1, 0, x, 2, 0, "iron_dark")
    # seat slats along X at z = 9: y 3-4, 5-6, 7-8, 9-10 with small gaps (two-cell boards)
    seat = [(4, 5), (6, 7), (8, 9), (10, 11)]
    for si, (y0, y1) in enumerate(seat):
        col = ("wgrey", "wgrey_hi", "wgrey_warm", "wgrey")[si]
        g.box(0, y0, 9, W - 1, y1, 9, col)
    g.box(0, 3, 9, W - 1, 3, 9, 0)
    for (y0, y1) in seat:
        g.box(0, y0, 9, 0, y1, 9, "wgrey_wet")                          # wet end grain
        g.box(W - 1, y0, 9, W - 1, y1, 9, "wgrey_wet")
    g.paint(0, 11, 9, W - 1, 11, 9, "wgrey_hi")                         # rubbed front edge
    # back slats on the reclined support
    g.box(0, 1, 12, W - 1, 1, 13, "wgrey_mid")
    g.box(0, 0, 15, W - 1, 0, 16, "wgrey")
    g.paint(0, 0, 16, W - 1, 0, 16, "wgrey_hi")
    for x in (0, W - 1):
        g.box(x, 1, 12, x, 1, 13, "wgrey_wet")
        g.box(x, 0, 15, x, 0, 16, "wgrey_wet")
    # the lower back slat snapped near the middle; both halves sag one cell at the break
    g.clear(11, 1, 12, 19, 1, 13)
    g.box(11, 1, 11, 14, 1, 12, "wgrey_mid")
    g.box(16, 1, 11, 19, 1, 12, "wgrey_mid")
    g.set(14, 1, 12, "break_fresh")
    g.set(16, 1, 12, "break_fresh")
    # rust bleeding from the end fixings onto the slat ends
    for x in (3, 27):
        g.paint(x, 1, 12, x, 1, 12, "rust_deep")
    # brass memorial plaque centred on the top back slat
    g.paint(14, 0, 15, 16, 0, 15, "brass")
    g.paint(15, 0, 15, 15, 0, 15, "brass_hi")
    return {"grid": g, "footprint_cells": ((2, 28), (1, 11))}


# ---------------------------------------------------------------------------
# garden table (0.05 m)
# ---------------------------------------------------------------------------
@model("garden_table",
       story="A white resin patio table left out through every season. Rain pooled along its "
             "moulded grooves and around the umbrella hole and grew green algae there; the "
             "legs are streaked on their shaded side, and last autumn's leaves still sit on "
             "the top.",
       details=["Rounded rectangular top with a skirt and moulded grooves", "Central umbrella "
                "hole", "Four flared legs", "Algae in the grooves and round the hole, streaks "
                "down the north (-Y) faces of the legs", "Two dead leaves on the top"],
       exclusions=["No chairs (separate props)", "No umbrella"],
       collision_hint="Box 1.1 x 0.7 x 0.75 m.")
def garden_table():
    W, D, H = 22, 14, 15
    g = Grid(W, D, H)
    g.rbox(0, 0, 13, W - 1, D - 1, 14, "paint_white", r=2)
    g.paint(0, 0, 13, W - 1, D - 1, 13, "paint_white_shadow")            # skirt
    g.clear(2, 2, 13, W - 3, D - 3, 13)                                  # hollow under-top
    # moulded grooves across the top (every 3 cells); algae where water stands in them
    for y in range(2, D - 2, 3):
        for x in range(2, W - 2):
            # the table sits slightly low at the -X end: water and algae collect there
            g.set(x, y, 14, "green_faded" if x < 7 - (y % 2) else "porcelain_mid")
    for (x, y) in ((2, 3), (3, 3), (2, 4), (2, 6), (3, 9), (2, 10), (4, 6)):
        g.set(x, y, 14, "porcelain_mid")
    # umbrella hole with an algae ring
    g.clear(10, 6, 13, 11, 7, 14)
    for (x, y) in ((9, 6), (9, 7), (12, 6), (12, 7), (10, 5), (11, 5), (10, 8), (11, 8)):
        g.set(x, y, 14, "green_faded")
    # legs: 2x2 posts flaring into the skirt at the top, small feet
    # moulded L-section legs set into the corners, flaring into the skirt
    for (x0, y0, sx, sy) in ((1, 1, 1, 1), (W - 2, 1, -1, 1), (1, D - 2, 1, -1),
                             (W - 2, D - 2, -1, -1)):
        for k in range(3):
            g.box(x0 + sx * k, y0, 0, x0 + sx * k, y0, 12, "paint_white_shadow")
            g.box(x0, y0 + sy * k, 0, x0, y0 + sy * k, 12, "paint_white_shadow")
        g.box(min(x0, x0 + sx * 3), min(y0, y0 + sy), 11, max(x0, x0 + sx * 3),
              max(y0, y0 + sy), 12, "paint_white_shadow")
        g.box(min(x0, x0 + sx), min(y0, y0 + sy * 3), 11, max(x0, x0 + sx),
              max(y0, y0 + sy * 3), 12, "paint_white_shadow")
        for k in range(3):
            g.set(x0 + sx * k, y0, 0, "porcelain_deep")
            g.set(x0, y0 + sy * k, 0, "porcelain_deep")
        if sy == 1:                                  # algae streaks on the shaded north legs
            g.paint(x0 + sx, y0, 2, x0 + sx, y0, 9, "green_faded")
            g.paint(x0 + 2 * sx, y0, 4, x0 + 2 * sx, y0, 7, "lichen")
    g.paint(0, 0, 13, W - 1, 0, 13, "porcelain_shadow")                  # grimy back skirt
    # two dead leaves on the top
    for (x, y, c) in ((15, 9, "dead_leaf"), (16, 9, "dead_leaf_dark"), (16, 10, "dead_leaf"),
                      (5, 10, "dead_leaf_dark")):
        g.set(x, y, 14, c)
    return {"grid": g, "footprint_cells": ((0, W - 1), (0, D - 1))}


# ---------------------------------------------------------------------------
# wooden fence section (0.05 m)
# ---------------------------------------------------------------------------
@model("wooden_fence",
       story="A back-garden fence panel that has not been stained since it went up. One board "
             "was kicked out by a dog or a fox, and its neighbour lost its top nail and leans "
             "into the gap; the bottoms have gone green where rain splashes up.",
       details=["Two 4x4 posts and two rails at the back (-Y), twelve dog-eared boards on the "
                "front", "One board missing, the next leaning into the gap from its bottom "
                "nail", "Per-board weathering, silvered tops, green splash-back at the foot"],
       exclusions=["No nail heads (confetti)", "No gate"],
       collision_hint="Box 1.9 x 0.15 x 1.5 m (thin wall); the gap is cosmetic.")
def wooden_fence():
    W, H = 38, 30
    g = Grid(W, 4, H)
    for x0 in (0, W - 2):                                           # posts with a cap
        g.box(x0, 0, 0, x0 + 1, 1, H - 2, "wgrey_dark")
        g.box(x0, 0, H - 1, x0 + 1, 1, H - 1, "wgrey_mid")
        g.paint(x0, 0, 0, x0 + 1, 1, 2, "wgrey_deep")
    for z0 in (5, 23):                                              # rails
        g.box(2, 1, z0, W - 3, 1, z0 + 1, "wgrey_mid")
        g.paint(2, 1, z0 + 1, W - 3, 1, z0 + 1, "wgrey")
    tones = ["wgrey", "wgrey_mid", "wgrey_warm", "wgrey", "wgrey_hi", "wgrey_mid", "wgrey",
             "wgrey_warm", "wgrey_mid", "wgrey", "wgrey_hi", "wgrey_mid"]
    for b in range(12):
        x0 = 1 + 3 * b
        if b == 7:
            continue                                                # missing board
        top = H - 3 if b not in (3, 9) else H - 4                   # two boards settled lower
        for z in range(1, top + 1):
            shift = 0
            if b == 6:                                              # leaning into the gap
                shift = (1 if z >= 12 else 0) + (1 if z >= 21 else 0)
            for dx in range(3):
                x = x0 + dx + shift
                col = tones[b]
                if z <= 3:
                    col = "wgrey_green" if z <= 2 else "wgrey_wet"  # splash-back
                elif z >= top - 1:
                    col = "wgrey_hi"
                g.set(x, 2, z, col)
    # the leaning board's top no longer touches the top rail: show the dark nail hole
    g.set(19, 1, 24, "wgrey_deep")
    return {"grid": g, "footprint_cells": ((0, W - 1), (0, 2))}


# ---------------------------------------------------------------------------
# chain-link fence section (0.05 m)
# ---------------------------------------------------------------------------
def chain_link(x, z):
    """Face-connected diamond lattice (6-cell pitch) standing in for wire mesh."""
    return (x + z) % 6 in (0, 1) or (x - z) % 6 in (0, 1)


@model("metal_fence",
       story="A chain-link section along a school or yard boundary. Someone climbed it at the "
             "left corner until the mesh tore off the top rail and sagged outward, and a "
             "plastic bag has been caught low in the mesh for months.",
       details=["Galvanised posts with caps and a top rail", "Diamond mesh (a 6-cell lattice "
                "standing in for wire finer than a cell)", "Top-left corner torn off the "
                "rail, sagging down and outward", "Bottom tension wire", "A faded bag snagged "
                "in the mesh"],
       exclusions=["No barbed wire", "No gate"],
       collision_hint="Box 1.9 x 0.1 x 1.6 m; mesh blocks movement, not sight.")
def metal_fence():
    W, H = 38, 33
    g = Grid(W, 4, H)
    for x0 in (0, W - 2):
        g.box(x0, 1, 0, x0 + 1, 2, H - 2, "galv")
        g.paint(x0, 1, 0, x0 + 1, 2, 1, "galv_dark")
        g.box(x0, 1, H - 1, x0 + 1, 2, H - 1, "galv_dark")         # cap
        g.paint(x0, 2, 2, x0, 2, H - 3, "galv_hi")                  # catch-light edge
    g.box(2, 1, H - 3, W - 3, 1, H - 3, "galv_hi")                  # top rail
    g.box(2, 1, 1, W - 3, 1, 1, "galv_dark")                        # tension wire
    # mesh; at the -X end it has torn off the rail and the post and sags into a triangle
    for x in range(2, W - 2):
        drop = max(0, (13 - x) // 2)                                # 0 .. 5 cells
        for z in range(2, H - 3 - drop):
            if x == 2 and z > 9:
                continue                                            # pulled away from the post
            if chain_link(x, z) or (drop and z == H - 4 - drop and x % 2 == 0):
                g.set(x, 1, z, "galv_dark")
    # snagged plastic bag low in the mesh, to the right of centre
    g.box(22, 2, 5, 24, 2, 6, "porcelain_shadow")
    g.box(23, 2, 4, 23, 2, 4, "porcelain_deep")
    g.box(22, 1, 5, 24, 1, 6, "porcelain_deep")
    return {"grid": g, "footprint_cells": ((0, W - 1), (1, 2))}


# ---------------------------------------------------------------------------
# streetlight (0.1 m)
# ---------------------------------------------------------------------------
# arm (y, z) cells relative to the pole's front face, rising in a short curve then level
LIGHT_ARM = [(2, 37), (2, 38), (3, 38), (3, 39), (4, 39), (5, 39), (5, 40), (6, 40), (7, 40),
             (8, 40), (9, 40), (10, 40)]


@model("streetlight",
       story="The streetlight outside a row of houses, dark since the grid went down. Someone "
             "has prised off the access cover at its foot to strip the copper, and rust is "
             "creeping up from the base.",
       details=["Galvanised 0.2 m pole on a concrete footing with a bolted flange",
                "Curved arm reaching 1.4 m over the road (+Y) to a cobra-head lantern with a "
                "dark, unlit lens and a photocell", "Access cover missing at the foot, dark "
                "cavity", "Rust at the flange and the bottom of the pole"],
       exclusions=["No lit or emissive lamp", "No banners or signs"],
       notes=["The arm reaches 1.4 m over the road as the brief's curved arm and cobra head "
              "require, so the footprint is 0.4 x 1.7 m (the reference is 0.45 x 0.35 m).",
              "Height 4.3 m matches the reference."],
       pivot_note="Centre of the pole base at ground level (not the bounding-box centre).",
       collision_hint="Cylinder r=0.12 m, h=4.2 m at the pivot; the arm is non-colliding.")
def streetlight():
    g = Grid(6, 18, 44)
    px, py = 1, 1                                                   # pole cells x 1..2, y 1..2
    g.box(0, 0, 0, 3, 3, 0, "concrete")                             # footing
    g.paint(0, 0, 0, 3, 0, 0, "concrete_dark")
    g.box(1, 1, 1, 2, 2, 1, "iron")                                 # flange
    for (x, y) in ((0, 0), (3, 0), (0, 3), (3, 3)):
        g.set(x, y, 1, "steel_dark")                                # anchor nuts
    g.box(px, py, 2, px + 1, py + 1, 41, "galv")
    g.paint(px, py, 2, px + 1, py + 1, 6, "galv_dark")
    g.paint(px, py, 2, px + 1, py + 1, 2, "rust_deep")              # rust at the flange
    g.paint(px, py + 1, 3, px, py + 1, 3, "rust_deep")              # streak under the door
    g.paint(px, py, 7, px, py + 1, 41, "galv_hi")                   # lit -X edge column
    g.paint(px, py, 7, px, py, 41, "galv")
    # access door missing on the front: a dark cavity
    g.set(px, py + 1, 4, "black")
    g.set(px, py + 1, 5, "soot")
    g.box(px, py, 42, px + 1, py + 1, 42, "galv_dark")              # pole cap
    for (y, z) in LIGHT_ARM:
        g.set(px, py + y - 1, z, "galv")
        g.set(px + 1, py + y - 1, z, "galv_dark")
    # cobra-head lantern: 4 wide, 6 long, lens underneath, photocell on top
    hy = py + 9
    g.box(px - 1, hy, 40, px + 2, hy + 5, 41, "galv_hi")
    g.clear(px - 1, hy, 41, px - 1, hy, 41)
    g.clear(px + 2, hy, 41, px + 2, hy, 41)
    g.clear(px - 1, hy + 5, 41, px + 2, hy + 5, 41)
    g.paint(px - 1, hy, 40, px + 2, hy + 5, 40, "galv")
    g.box(px, hy + 1, 39, px + 1, hy + 4, 39, "glass_deep")         # unlit lens
    g.set(px, hy + 2, 39, "glass_dark")
    g.box(px - 1, hy + 1, 39, px - 1, hy + 4, 39, "galv_dark")
    g.box(px + 2, hy + 1, 39, px + 2, hy + 4, 39, "galv_dark")
    g.set(px, hy + 2, 42, "charcoal")                               # photocell
    return {"grid": g, "pivot_cells": (2.0, 2.0, 0.0)}


# ---------------------------------------------------------------------------
# stop sign (0.05 m)
# ---------------------------------------------------------------------------
STOP_OCT = [5, 7, 9, 11, 13, 13, 13, 13, 13, 11, 9, 7, 5]            # row widths, bottom up
STOP_TEXT = ["##.#.##.#", "##.#.##.#", "##.#.##.#"]       # broken pale band: not letters


@model("road_sign",
       story="The stop sign at the end of the residential street. A reversing van clipped it "
             "and bent the post back; nobody came to straighten it, and the face is fading.",
       details=["Octagonal red face with a pale rim and a broken pale band suggesting a "
                "legend (blocks, not letters)", "Square galvanised post bent backward at 0.55 m, the "
                "sign tilting with it", "Scraped zinc at the bend, rust at the foot"],
       exclusions=["No readable text", "No street-name blades"],
       notes=["0.65 m octagon (the reference is 0.51 m; real stop signs are 0.6-0.75 m). At "
              "11 cells the octagon read as a round no-entry sign."],
       collision_hint="Box 0.06 x 0.06 x 2.4 m (post); the sign face is non-colliding.")
def road_sign():
    g = Grid(13, 10, 50)
    cx = 6
    kink = 11

    def back(z):                                    # backward lean above the kink (about 6 deg)
        return -((z - kink) // 9) - 1 if z > kink else 0

    yb = 7
    z0 = 36
    ys = yb + back(z0 + 6) + 1                      # the face is one rigid plane
    def post_y(z):
        return yb + back(min(z, z0 + 6))

    for z in range(0, 47):
        g.set(cx, post_y(z), z, "galv")
        if z and post_y(z) != post_y(z - 1):                   # keep the bent post solid
            g.set(cx, post_y(z - 1), z, "galv")
        if z <= 1:
            g.set(cx, yb, z, "rust_deep")
        if kink - 1 <= z <= kink + 1:
            g.set(cx, post_y(z), z, "galv_hi")                      # scraped at the bend
    # octagon face in front of the post: red with a one-cell pale rim
    face = set()
    for r, w in enumerate(STOP_OCT):
        for x in range(cx - w // 2, cx - w // 2 + w):
            face.add((x, z0 + r))
    for (x, z) in face:
        rim = any(n not in face for n in ((x + 1, z), (x - 1, z), (x, z + 1), (x, z - 1)))
        g.set(x, ys, z, "paint_white_shadow" if rim else "signal_red")
    for r, row in enumerate(STOP_TEXT):                             # legend band, mid face
        z = z0 + 7 - r
        for k, ch in enumerate(row):
            if ch == "#":
                g.set(cx - 4 + k, ys, z, "paint_white_shadow")
    g.set(cx, ys - 1, z0 + 2, "steel_dark")                          # mounting bolts
    g.set(cx, ys - 1, z0 + 9, "steel_dark")
    return {"grid": g, "pivot_cells": (cx + 0.5, yb + 0.5, 0.0)}


# ---------------------------------------------------------------------------
# traffic cone (0.025 m)
# ---------------------------------------------------------------------------
@model("traffic_cone",
       story="A road cone left from roadworks that stopped mid-job. It has been knocked over "
             "and stood back up more than once: the base is chipped and a tyre has scuffed "
             "one side black.",
       details=["Square rubber base with chamfered corners", "Stepped round cone with an open "
                "top", "Two pale reflective bands", "Tyre scuff on the camera side, grime "
                "on the lower cone, a chipped base corner"],
       exclusions=["No printed markings"],
       collision_hint="Cylinder r=0.15 m, h=0.53 m.")
def traffic_cone():
    g = Grid(13, 13, 22)
    g.rbox(0, 0, 0, 12, 12, 1, "charcoal", r=2)
    g.paint(0, 0, 1, 12, 12, 1, "iron_edge")
    g.clear(12, 0, 0, 12, 1, 1)                                     # chipped base corner
    c = 6.5
    radii = [4.5, 4.5, 4.5, 4.3, 4.2, 4.2, 3.7, 3.7, 3.7, 3.2, 3.2, 3.2, 2.9, 2.9, 2.3, 2.3,
             1.5, 1.5, 1.5]                         # nested clean discs, bottom to top
    for z in range(2, 21):
        r = radii[z - 2]
        for (i, j) in g.disc_cells(c, c, r):
            col = "safety_orange"
            if 13 <= z <= 15 or 8 <= z <= 9:
                col = "porcelain_mid"                               # reflective bands
            elif z <= 4:
                col = "safety_orange_dark"                          # grime low down
            g.set(i, j, z, col)
    g.clear(6, 6, 20, 6, 6, 20)                                     # open top
    # tyre scuff on the -X side across the lower band
    for z in range(5, 9):
        for (i, j) in g.disc_cells(c, c, 4.6):
            if g.get(i, j, z) and i <= 3 and 5 + (z % 2) <= j <= 8 and not g.get(i - 1, j, z):
                g.set(i, j, z, "asphalt_hi")
    return g


# ---------------------------------------------------------------------------
# wooden pallet (0.025 m)
# ---------------------------------------------------------------------------
@model("wooden_pallet",
       story="A stringer pallet that sat out behind a shop for a year. The boards have gone "
             "grey, one top board split along its length and lost a corner when it was "
             "dropped, and an earlier repair left one fresh pale board.",
       details=["Three notched stringers along X with fork notches", "Seven top deck boards "
                "and three bottom boards", "One top board split lengthwise with a broken-off "
                "corner, pale wood at the break", "One newer replacement board"],
       exclusions=["No stamps or markings", "No nail heads"],
       why="Deck boards are 2.5 cm thick; at 5 cm the pallet becomes three thick slabs.",
       collision_hint="Box 1.12 x 0.8 x 0.15 m.")
def wooden_pallet():
    W, D = 45, 32
    g = Grid(W, D, 6)
    for (y0, y1) in ((0, 1), (15, 16), (30, 31)):                   # stringers z 1..4
        g.box(0, y0, 1, W - 1, y1, 4, "wgrey_dark")
        for (x0, x1) in ((8, 14), (30, 36)):                        # fork notches
            g.clear(x0, y0, 1, x1, y1, 2)
        g.paint(0, y0, 1, 0, y1, 4, "wgrey_deep")                   # end grain
        g.paint(W - 1, y0, 1, W - 1, y1, 4, "wgrey_deep")
    for (x0, x1) in ((0, 3), (20, 24), (41, 44)):                   # bottom boards
        g.box(x0, 0, 0, x1, D - 1, 0, "wgrey_mid")
    tones = ["wgrey", "wgrey_mid", "wgrey_hi", "wgrey", "pine_light", "wgrey_mid", "wgrey"]
    xs = [0, 7, 14, 20, 27, 34, 41]
    for b, x0 in enumerate(xs):
        g.box(x0, 0, 5, x0 + 3, D - 1, 5, tones[b])
        g.paint(x0, 0, 5, x0 + 3, 0, 5, "wgrey_dark")               # weathered board ends
        g.paint(x0, D - 1, 5, x0 + 3, D - 1, 5, "wgrey_dark")
    # the replacement board is newer: pale pine, clean ends
    g.paint(27, 0, 5, 30, 0, 5, "pine_mid")
    g.paint(27, D - 1, 5, 30, D - 1, 5, "pine_mid")
    # split board (x 14..17): a lengthwise crack from y 9, the outer strip broken off at the end
    g.clear(16, 9, 5, 16, D - 1, 5)
    g.clear(17, 24, 5, 17, D - 1, 5)
    for y in range(9, 24):
        g.set(17, y, 5, "wgrey_hi")
    g.set(15, 9, 5, "break_fresh")
    g.box(17, 22, 5, 17, 23, 5, "break_fresh")
    g.box(15, 24, 5, 15, 26, 5, "break_fresh")
    return g


# ---------------------------------------------------------------------------
# utility pole (0.1 m)
# ---------------------------------------------------------------------------
@model("utility_pole",
       story="The wooden distribution pole at the corner, its line cut and left hanging "
             "after a storm or a looter. Years of stapled notices have left a ragged patch at "
             "eye height, and the newest one, a missing-person flyer, is still legible from "
             "across the street as a pale sheet.",
       details=["0.3 m creosoted pole weathering from brown at the foot to grey at the top",
                "Crossarm with braces and four glass insulators", "Pole-top transformer can "
                "with bushings, straps and a rust run", "A cut line dangling from the outer "
                "insulator on the camera side", "Step bolts, a pale flyer over a ragged patch "
                "of old staples and paper"],
       exclusions=["No readable flyer text", "No live wires to other poles"],
       notes=["The crossarm makes the footprint 1.9 m wide (the reference is 0.35 m); the "
              "brief asks for a crossarm with insulators.", "Height 4.8 m, a little above the "
              "4.45 m reference so the pole stands taller than the 4.3 m streetlight."],
       pivot_note="Centre of the pole base at ground level.",
       collision_hint="Box 0.3 x 0.3 x 4.8 m at the pivot; crossarm and can non-colliding.")
def utility_pole():
    g = Grid(20, 10, 49)
    px, py = 9, 4                                                   # pole cells 9..11, 4..6
    for z in range(0, 47):
        col = ("wood_deep" if z < 3 else "wood_stain" if z < 16 else
               "wgrey_dark" if z < 34 else "wgrey_mid")
        g.box(px, py, z, px + 2, py + 2, z, col)
    # vertical drying checks on the two camera faces (dark lines, not specks)
    for (x, y, z0, z1) in ((px, py + 1, 6, 15), (px, py + 2, 20, 29), (px + 1, py + 2, 9, 13),
                           (px, py, 31, 38)):
        g.paint(x, y, z0, x, y, z1, "wood_deep")
    g.box(px, py, 47, px + 2, py + 2, 47, "wgrey_hi")               # bleached top
    # crossarm on the front face, braces down to the pole
    za = 43
    g.box(0, py + 3, za, 19, py + 3, za, "wgrey_mid")
    g.paint(0, py + 3, za, 19, py + 3, za, "wgrey_mid")
    for k in range(4):
        g.set(px - 1 - k, py + 3, za - 4 + k, "steel_dark")
        g.set(px + 3 + k, py + 3, za - 4 + k, "steel_dark")
    # glass insulators
    for x in (1, 5, 14, 18):
        g.set(x, py + 3, za + 1, "glass")
        g.set(x, py + 3, za + 2, "glass_hi")
    # transformer can on the -X side of the pole
    for z in range(31, 38):
        for (i, j) in g.disc_cells(px - 2.0, py + 1.5, 2.6):
            col = "galv" if z not in (32, 36) else "galv_dark"
            if z == 31:
                col = "galv_dark"
            g.set(i, j, z, col)
    for (i, j) in g.disc_cells(px - 2.0, py + 1.5, 1.6):
        g.set(i, j, 38, "galv_hi")                                  # lid
    g.paint(px - 4, py, 33, px - 4, py + 2, 37, "galv_hi")          # lit -X face
    g.set(px - 3, py + 1, 39, "porcelain_shadow")                   # bushings
    g.set(px - 1, py + 1, 39, "porcelain_shadow")
    for z in range(31, 37):                                         # rust run from the lid
        g.set(px - 4, py + 2, z, "rust_dark" if z > 33 else "rust_deep")
    g.box(px - 1, py, 34, px - 1, py + 2, 34, "steel_dark")         # strap to the pole
    for z in range(40, za):                                         # lead to the crossarm
        g.set(px - 3, py + 1, z, "black")
    g.set(px - 3, py + 2, za - 1, "black")
    g.set(px - 3, py + 3, za - 1, "black")
    # cut line: from the outer -X insulator it droops over the front and hangs down
    wire = [(1, py + 4, za + 2), (1, py + 5, za + 2), (1, py + 5, za + 1)]
    wire += [(1 - (1 if z < 34 else 0), py + 5, z) for z in range(za, 23, -1)]
    last = None
    for c in wire:
        if last and abs(c[0] - last[0]) + abs(c[2] - last[2]) > 1:
            g.set(c[0], c[1], last[2], "black")
        g.set(*c, "black")
        last = c
    g.set(1, py + 5, 34, "black")
    g.set(0, py + 5, 24, "copper")                                  # frayed end
    g.set(0, py + 4, 24, "copper")
    # step bolts, staggered
    for (x, y, z) in ((px + 3, py + 1, 22), (px - 1, py + 1, 25), (px + 3, py + 1, 28),
                      (px - 1, py + 2, 18)):
        g.set(x, y, z, "steel_dark")
    # ragged patch of old notices and the newest pale flyer at eye height (front face)
    g.paint(px, py + 2, 13, px + 2, py + 2, 17, "card_dark")
    g.paint(px + 2, py + 2, 16, px + 2, py + 2, 17, "wgrey_dark")
    g.paint(px, py + 2, 14, px + 1, py + 2, 16, "paper")
    g.paint(px, py + 2, 14, px, py + 2, 14, "label_cream")
    weld(g)
    return {"grid": g, "pivot_cells": (px + 1.5, py + 1.5, 0.0)}


# ---------------------------------------------------------------------------
# abandoned bicycle (0.025 m), lying on its right side
# ---------------------------------------------------------------------------
def _bike_line(g, a, b, col, z=1, w=0):
    """Line in the bike plane (u, v) at height z; w=1 adds a parallel row (thicker tube)."""
    g.line((a[0], a[1], z), (b[0], b[1], z), col)
    if w:
        g.line((a[0], a[1] + 1, z), (b[0], b[1] + 1, z), col)


@model("abandoned_bicycle",
       story="A commuter's bike dropped on the pavement and never picked up. The front wheel "
             "folded when something drove over it; the chain has rusted and the saddle has "
             "split, but the rear rack still carries a frayed bungee.",
       details=["Diamond frame in faded teal lying flat on its right side", "Rear wheel true, "
                "front wheel buckled up out of plane", "Handlebar turned and standing up from "
                "the ground, left pedal raised", "Rusted chain, split saddle, rear rack with a "
                "bungee"],
       exclusions=["No brand decals", "No lights or bell (sub-cell)"],
       why="Tubes, spokes and the rack need 2.5 cm cells; at 5 cm the frame is a thick "
           "outline with no wheel structure.",
       notes=["Lying on its side as the brief says, so it is 1.65 m long, 0.95 m wide (the "
              "bike's height) and 0.33 m tall; the reference box (1.62 x 0.47 x 1.06 m) "
              "describes a standing bike."],
       collision_hint="Box 1.65 x 0.95 x 0.1 m (flat); trip hazard only.")
def abandoned_bicycle():
    g = Grid(68, 40, 14)
    R, F = (13, 13), (53, 13)
    BB, S, H1, H2 = (29, 11), (25, 32), (46, 31), (47, 26)

    def wheel(c, bent):
        cu, cv = c[0] + 0.5, c[1] + 0.5
        for (i, j) in g.disc_cells(cu, cv, 12.2):
            d = math.hypot(i + 0.5 - cu, j + 0.5 - cv)
            if d < 9.4:
                continue
            z = 0
            if bent:                                   # buckled: the upper-front arc lifts
                ang = math.atan2(j + 0.5 - cv, i + 0.5 - cu)
                lift = max(0.0, math.cos(ang - math.radians(70)))
                z = int(round(4.0 * lift ** 2))
            col = "black" if d >= 10.6 else ("steel_light" if d >= 9.9 else "steel")
            g.box(i, j, z, i, j, z + (1 if d >= 10.6 else 0), col)
            if z:                                      # keep the lifted arc joined
                for zz in range(0, z):
                    if not g.get(i, j, zz) and d >= 10.6 and lift > 0.0 and zz == z - 1:
                        g.set(i, j, zz, "black")
        # spokes: four straight and four diagonal, in the plane
        for k in range(8):
            a = math.radians(22.5 + 45 * k)
            end = (c[0] + math.cos(a) * 9.6, c[1] + math.sin(a) * 9.6)
            if bent and 20 < (22.5 + 45 * k) % 360 < 130:
                continue                               # spokes snapped where it folded
            g.line((c[0], c[1], 1), (end[0], end[1], 1), "steel_dark")
        g.box(c[0] - 1, c[1] - 1, 0, c[0] + 1, c[1] + 1, 2, "steel_dark")   # hub
        g.set(c[0], c[1], 3, "steel")

    wheel(R, False)
    wheel(F, True)
    # frame (teal), lying at z = 1..2
    for a, b, w in ((BB, S, 1), (S, H1, 0), (BB, H2, 1), (BB, R, 0), (S, R, 0), (H2, F, 0)):
        _bike_line(g, a, b, "teal", 1, w)
        _bike_line(g, a, b, "teal_dark", 2, 0) if w else None
    g.line((H2[0], H2[1], 1), (H1[0], H1[1] + 2, 1), "teal")             # head tube
    g.line((H2[0] + 1, H2[1], 1), (H1[0] + 1, H1[1] + 2, 1), "teal_dark")
    g.line((H2[0], H2[1], 2), (F[0], F[1], 2), "teal_dark")             # fork, upper leg
    # seat post and split saddle
    g.line((S[0], S[1], 1), (S[0] - 1, S[1] + 3, 1), "steel")
    g.box(19, 35, 1, 27, 36, 2, "black")
    g.box(21, 36, 2, 24, 36, 2, "leather_deep")                          # split cover
    g.set(22, 36, 3, "foam" if False else "cream_deep")                  # foam showing
    # stem and handlebar, turned and standing up out of the plane
    g.line((H1[0], H1[1] + 2, 1), (H1[0] + 1, H1[1] + 4, 1), "steel")
    g.line((H1[0] + 3, H1[1] + 3, 0), (H1[0] - 1, H1[1] + 5, 12), "steel_light")
    for z in range(0, 3):
        g.set(H1[0] + 3, H1[1] + 3, z, "black")                          # grip on the ground
    g.box(H1[0] - 1, H1[1] + 5, 10, H1[0] - 1, H1[1] + 5, 13, "black")  # raised grip
    # drivetrain: chainring under the BB, rusted chain to the rear cog, raised left pedal
    for (i, j) in g.ring_cells(BB[0] + 0.5, BB[1] + 0.5, 4.2):
        g.set(i, j, 0, "steel_dark")
    g.line((BB[0], BB[1] + 4, 0), (R[0], R[1] + 2, 0), "rust_dark")
    g.line((BB[0], BB[1] - 4, 0), (R[0], R[1] - 2, 0), "rust_deep")
    g.line((BB[0], BB[1], 3), (BB[0] + 5, BB[1] - 6, 3), "steel")        # left crank
    g.box(BB[0] + 4, BB[1] - 8, 3, BB[0] + 6, BB[1] - 6, 5, "charcoal")  # pedal
    g.box(BB[0], BB[1], 1, BB[0], BB[1], 3, "steel_dark")
    # rear rack: struts from the hub and seat stays, platform standing up out of the plane
    g.line((R[0], R[1], 1), (R[0] - 4, R[1] + 16, 1), "steel")
    g.line((S[0] - 2, S[1] - 2, 1), (R[0] - 4, R[1] + 16, 1), "steel")
    g.box(R[0] - 7, R[1] + 16, 1, R[0] + 6, R[1] + 16, 4, "steel")
    g.box(R[0] - 6, R[1] + 16, 2, R[0] + 5, R[1] + 16, 3, 0)
    g.box(R[0] - 7, R[1] + 16, 1, R[0] - 7, R[1] + 16, 4, "steel")
    g.box(R[0] - 2, R[1] + 16, 1, R[0] - 2, R[1] + 16, 4, "steel")
    g.box(R[0] - 5, R[1] + 17, 1, R[0] + 3, R[1] + 17, 1, "safety_orange_dark")  # bungee
    g.set(R[0] + 4, R[1] + 18, 0, "safety_orange_dark")
    g.set(R[0] + 4, R[1] + 17, 0, "safety_orange_dark")
    weld(g)
    return {"grid": g, "footprint_cells": ((1, 66), (1, 38))}
