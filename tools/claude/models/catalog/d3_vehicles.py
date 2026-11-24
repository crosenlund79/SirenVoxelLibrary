"""Batch D3 - vehicles (creator: Claude). 0.1 m cells. X right, Y front (+Y = nose), Z up.

All five vehicles share one construction kit so they read as one family: the same
hand-authored wheel profiles (7-cell car wheel, 8-cell truck wheel, and their flat-tyre
variants), the same arch cut and dark wheel well, the same two-tone opaque glass with a dark
top row, the same lights, mirrors, seams and plates (plain blocks, never text or logos).
Pivot = bottom centre between the axles.
"""
from catalog_registry import model
from voxkit import Grid, P

# Wheel profiles in the Y-Z plane, bottom row first. T tyre, R rim, C hub cap.
WHEELS = {
    7: ["..TTT..", ".TTTTT.", "TTRRRTT", "TTRCRTT", "TTRRRTT", ".TTTTT.", "..TTT.."],
    8: ["..TTTT..", ".TTTTTT.", "TTRRRRTT", "TTRCCRTT", "TTRCCRTT", "TTRRRRTT", ".TTTTTT.",
        "..TTTT.."],
    # flat tyres: rim one cell lower, the tyre squashed into a wide contact patch
    "7f": [".TTTTT.", "TTRRRTT", "TTRCRTT", "TTRRRTT", ".TTTTT.", "..TTT.."],
    "8f": [".TTTTTT.", "TTRRRRTT", "TTRCCRTT", "TTRCCRTT", "TTRRRRTT", ".TTTTTT.", "..TTTT.."],
}


def wheel(g, xs, yc, kind=7, outer=None, rim="steel_light"):
    """Wheel at axle cells xs (two x columns), centred on y = yc (cell index of the middle
    column for odd widths, the right-of-centre column for even widths). `outer` is the
    x column facing outward (gets the bulge on a flat tyre)."""
    rows = WHEELS[kind]
    w = len(rows[0])
    y0 = yc - w // 2
    for z, row in enumerate(rows):
        for k, ch in enumerate(row):
            if ch == ".":
                continue
            edge = (k == 0 or k == w - 1 or row[k - 1] == "." or row[k + 1] == "." or
                    z == 0 or z == len(rows) - 1 or rows[z - 1][k] == "." or
                    (z + 1 < len(rows) and rows[z + 1][k] == "."))
            col = {"T": "black" if edge else "charcoal", "R": rim, "C": "steel_dark"}[ch]
            for x in xs:
                g.set(x, y0 + k, z, col)
            if str(kind).endswith("f") and ch == "T" and z <= 1 and outer is not None:
                g.set(outer, y0 + k, z, "black")              # sidewall bulge


def arch(g, x_out, x_in, yc, zc, r, well="soot"):
    """Cut a wheel arch (cells within r of (yc, zc), z >= 1) through the outer body columns
    x_out..x_in (inclusive, ordered outer->inner) and paint the next column in as the well."""
    xs = range(min(x_out, x_in), max(x_out, x_in) + 1)
    step = 1 if x_in > x_out else -1
    for y in range(int(yc - r) - 1, int(yc + r) + 2):
        for z in range(0, int(zc + r) + 2):
            if (y + 0.5 - yc) ** 2 + (z + 0.5 - zc) ** 2 <= r * r:
                for x in xs:
                    g.set(x, y, z, 0)
                if g.get(x_in + step, y, z):
                    g.set(x_in + step, y, z, well)


def glass_rows(g, x, ys, z0, z1, top="glass_dark", body="glass_deep"):
    """Paint a side window on column x: dark top row, deep body (opaque, value-structured)."""
    for y in ys:
        for z in range(z0, z1 + 1):
            if g.get(x, y, z):
                g.set(x, y, z, top if z == z1 else body)


def sloped_glass(g, ys, xa, xb, z_min, facing):
    """Glass on a stepped screen: every cell in the zone exposed upward or toward `facing`
    (+1 front, -1 rear) is glass, so treads and risers read as one dark pane (no venetian-
    blind stripes); the top row is a shade lighter and one soft vertical streak breaks it."""
    cells = []
    for y in ys:
        for x in range(xa, xb + 1):
            for z in range(z_min, g.shape[2]):
                if g.get(x, y, z) and (not g.get(x, y, z + 1) or not g.get(x, y + facing, z)):
                    cells.append((x, y, z))
    ztop = max(c[2] for c in cells)
    streak = range(xa + 3, xa + 5)                  # one soft vertical reflection streak
    for (x, y, z) in cells:
        if z >= ztop:
            col = "glass_dark"
        elif x in streak and z >= z_min + 1:
            col = "glass_deep"
        else:
            col = "screen"
        g.set(x, y, z, col)

def mirrors(g, y, z, xl, xr, col):
    """Door mirrors: a two-cell head on a short stalk back to the glasshouse or door, the
    rear face dark (mirror glass)."""
    for x, inward in ((xl, 1), (xr, -1)):
        g.box(x, y, z, x, y + 1, z, col)
        g.set(x, y, z, "glass_dark")
        k = x + inward                      # stalk: at most two cells in, then down to the door
        for _ in range(2):
            if g.get(k, y + 1, z):
                break
            g.set(k, y + 1, z, col)
            if g.get(k + inward, y + 1, z):
                break
            k += inward
        zz = z - 1
        while not g.get(k + inward, y + 1, zz + 1) and zz >= 0 and not g.get(k, y + 1, zz):
            g.set(k, y + 1, zz, col)
            zz -= 1


def profile_body(g, x0, x1, prof, col, deep):
    """Body from a side profile {y: (z_bottom, z_body_top, z_glass_top or None)}: lower body
    full width, glasshouse inset one cell with its roof edge inset again, shoulders rounded
    where there is no glasshouse, and the four plan corners chamfered."""
    for y, (zb, top, gt) in prof.items():
        g.box(x0, y, zb, x1, y, top, col)
        g.box(x0, y, zb, x1, y, zb, deep)
        if gt is not None:
            g.box(x0 + 1, y, top + 1, x1 - 1, y, gt, col)
            g.set(x0 + 1, y, gt, 0)
            g.set(x1 - 1, y, gt, 0)
        else:
            g.set(x0, y, top, 0)
            g.set(x1, y, top, 0)
    ys = sorted(prof)
    for y in (ys[0], ys[-1]):
        for x in (x0, x1):
            g.clear(x, y, 0, x, y, g.shape[2] - 1)


def arch_lip(g, x, yc, zc, r, col):
    """Darken the body cells on column x that ring an arch opening (a lip, not a decal)."""
    for y in range(int(yc - r) - 2, int(yc + r) + 3):
        for z in range(1, int(zc + r) + 3):
            d = ((y + 0.5 - yc) ** 2 + (z + 0.5 - zc) ** 2) ** 0.5
            if r < d <= r + 1.0 and g.get(x, y, z):
                g.set(x, y, z, col)


def seam(g, x, y, z0, z1, col):
    for z in range(z0, z1 + 1):
        if g.get(x, y, z):
            g.set(x, y, z, col)


def tops(g, col, z_min=0, only=None):
    """Recolour every upward-facing surface cell above z_min (dust and sun fade)."""
    nx, ny, nz = g.shape
    keep = {P(c) for c in (only or [])}
    for x in range(nx):
        for y in range(ny):
            for z in range(nz - 1, z_min - 1, -1):
                v = g.get(x, y, z)
                if v:
                    if not keep or v in keep:
                        g.set(x, y, z, col)
                    break


# ---------------------------------------------------------------------------
# family car (hatchback)
# ---------------------------------------------------------------------------
# side profile, y (rear 0 -> nose 41): (z_bottom, z_body_top, z_glass_top or None)
def _car_profile():
    prof = {}
    for y in range(42):
        zb = 2
        if y <= 2:
            top, gt = 8, None                      # tail and bumper
        elif y <= 6:
            top, gt = 9, None
        elif y <= 12:                              # steep hatch glass rising to the roof
            top, gt = 8, {7: 10, 8: 11, 9: 12, 10: 12, 11: 13, 12: 13}[y]
        elif y <= 24:
            top, gt = 8, 13                        # roof
        elif y <= 30:                              # windscreen falling to the scuttle
            top, gt = 8, {25: 13, 26: 12, 27: 12, 28: 11, 29: 10, 30: 9}[y]
        elif y <= 36:
            top, gt = 8, None                      # bonnet
        else:
            top, gt = (7 if y <= 39 else 6), None  # nose drops toward the bumper
        prof[y] = (zb, top, gt)
    return prof


@model("family_car",
       story="A blue-grey family hatchback left on the street when the family went on foot. "
             "The front tyre on the kerb side has gone flat, a summer of dust has settled on "
             "every top surface, and through the rear window, left open a crack too wide, a "
             "packed bag is still on the back seat.",
       details=["Five-door hatchback: short bonnet, raked screen, long roof, steep hatch",
                "7-cell wheels (shared family profile), front-left tyre flat with the rim "
                "sitting one cell low", "Dust and sun fade on every upward surface",
                "Rear-left window wound down: back seat and a packed olive bag visible",
                "Two-tone opaque glass, door seams, handles, mirrors, unlit lamps, blank "
                "plates"],
       exclusions=["No badges, logos or plate text", "No transparent glass"],
       why="Body panels, pillars and 0.65 m wheels need 0.1 m cells to keep round wheels "
           "and a readable glasshouse; the game's structure grid is also 0.1 m.",
       pivot_note="Bottom centre between the axles (wheel centres at y = 8 and y = 33).",
       collision_hint="Box 1.75 x 4.2 x 1.4 m centred on the pivot.")
def family_car():
    W = 19
    g = Grid(W, 42, 14)
    x0, x1 = 1, 17                                       # body sides
    prof = _car_profile()
    profile_body(g, x0, x1, prof, "bluegrey", "bluegrey_deep")
    # lower body: darker grime band and wheel arches
    g.paint(x0, 0, 3, x1, 41, 3, "bluegrey_dark")
    for yc in (8.5, 33.5):
        arch_lip(g, x0, yc, 3.0, 4.3, "bluegrey_dark")
        arch_lip(g, x1, yc, 3.0, 4.3, "bluegrey_dark")
        arch(g, x0, x0 + 1, yc, 3.0, 4.3)
        arch(g, x1, x1 - 1, yc, 3.0, 4.3)
    # windows: side glass (A pillar at y 26-27, B at 19, C at 12), screen and hatch glass
    for x in (x0 + 1, x1 - 1):
        glass_rows(g, x, range(20, 26), 9, 12)
        glass_rows(g, x, range(13, 19), 9, 12)
        glass_rows(g, x, range(9, 12), 9, 11)
    sloped_glass(g, range(25, 31), x0 + 2, x1 - 2, 9, +1)            # windscreen
    sloped_glass(g, range(7, 13), x0 + 2, x1 - 2, 9, -1)             # hatch glass
    # door seams, handles
    for x in (x0, x1):
        for y in (30, 19, 11):
            seam(g, x, y, 4, 8, "bluegrey_deep")
        for y in (22, 14):
            g.set(x, y, 7, "chrome")
    # mirrors
    mirrors(g, 27, 9, 0, W - 1, "bluegrey")
    # front: bumper lip, grille slot, headlights, plate
    g.box(x0, 41, 2, x1, 41, 2, "charcoal")
    g.box(6, 41, 5, 12, 41, 5, "black")
    g.box(7, 41, 4, 11, 41, 4, "charcoal")
    for xa, xb in ((2, 4), (14, 16)):
        g.box(xa, 41, 5, xb, 41, 5, "glass_hi")
    g.box(8, 41, 3, 10, 41, 3, "label_cream")
    # rear: tail lamps, bumper, plate, wiper-less hatch lip
    g.box(x0, 0, 2, x1, 0, 2, "charcoal")
    for xa, xb in ((1, 3), (15, 17)):
        g.box(xa, 0, 6, xb, 0, 7, "signal_red_dark")
    g.box(8, 0, 5, 10, 0, 5, "label_cream")
    # dust and fade on every top surface (body colour only, not glass)
    tops(g, "bluegrey_hi", only=["bluegrey"])
    # the rear-left window is wound right down: carve into the cabin; the back seat and the
    # packed bag sit right at the sill where the camera can see them
    g.clear(x0 + 1, 13, 9, x0 + 1, 18, 12)                  # window opening
    g.clear(x0 + 2, 13, 6, 9, 18, 12)                       # cabin pocket
    g.box(x0 + 2, 12, 6, 9, 12, 12, "slate_dark")           # seat back / cabin rear
    g.box(x0 + 2, 13, 6, 9, 18, 6, "slate")                 # seat cushion
    g.box(10, 13, 6, 10, 18, 12, "black")                   # cabin depth (shadow)
    g.box(x0 + 2, 13, 12, 9, 18, 12, "slate_deep")          # headliner in shadow
    g.box(x0 + 1, 13, 12, x0 + 1, 18, 12, "bluegrey_hi")    # roof drip rail
    g.box(x0 + 2, 19, 6, 9, 19, 12, "slate_deep")           # front seat back
    g.box(x0 + 2, 14, 7, x0 + 5, 17, 10, "olive")           # the packed bag
    g.box(x0 + 2, 14, 10, x0 + 5, 17, 10, "olive_hi")
    g.box(x0 + 3, 15, 11, x0 + 4, 16, 11, "olive_dark")     # strap handles
    g.box(x0 + 2, 14, 7, x0 + 2, 17, 9, "olive_dark")
    # wheels: shared profile, front-left tyre flat
    wheel(g, (1, 2), 8, 7)
    wheel(g, (W - 3, W - 2), 8, 7)
    wheel(g, (1, 2), 33, "7f", outer=0)
    wheel(g, (W - 3, W - 2), 33, 7)
    return {"grid": g, "pivot_cells": (W / 2, 21.0, 0.0)}


def fline(g, a, b, col):
    """Face-connected straight line between cell centres (a staircase, never diagonal-only)."""
    n = max(abs(b[i] - a[i]) for i in range(3)) * 2 + 1
    last = None
    for k in range(n + 1):
        t = k / n
        q = tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))
        if last is not None:
            cur = list(last)
            for ax in range(3):
                while cur[ax] != q[ax]:
                    cur[ax] += 1 if q[ax] > cur[ax] else -1
                    g.set(*cur, col)
        g.set(*q, col)
        last = q


# ---------------------------------------------------------------------------
# police car (sedan)
# ---------------------------------------------------------------------------
def _sedan_profile():
    prof = {}
    for y in range(47):
        if y <= 1:
            top, gt = 7, None                      # bumper and tail
        elif y <= 9:
            top, gt = 8, None                      # boot lid
        elif y <= 14:                              # rear screen
            top, gt = 8, {10: 9, 11: 10, 12: 11, 13: 12, 14: 13}[y]
        elif y <= 26:
            top, gt = 8, 13                        # roof
        elif y <= 32:                              # windscreen
            top, gt = 8, {27: 13, 28: 12, 29: 12, 30: 11, 31: 10, 32: 9}[y]
        elif y <= 42:
            top, gt = 8, None                      # bonnet
        else:
            top, gt = (7 if y <= 45 else 6), None
        prof[y] = (2, top, gt)
    return prof


@model("police_car",
       story="A patrol car abandoned at a roadblock that was never finished. The driver's door "
             "was flung open and left that way; the lightbar is dark, the push bar is "
             "scuffed from pushing stalled cars off the road, and there is no marking left "
             "that says which force it belonged to.",
       details=["Three-box sedan on the shared 7-cell wheels", "Navy ends and white doors and "
                "roof (generic, no text or crest)", "Unlit lightbar: red and blue lens blocks "
                "on a dark base", "Black push bar on the nose, A-pillar spotlight",
                "Driver's door flung open about 75 degrees: seat, wheel and dash visible"],
       exclusions=["No department names, numbers or crests", "No lit or emissive lamps"],
       notes=["The open door adds 0.8 m to the width (2.8 m with the door, 2.0 m closed)."],
       why="Body panels, pillars and 0.65 m wheels need 0.1 m cells; the game's structure "
           "grid is also 0.1 m.",
       pivot_note="Bottom centre between the axles (wheel centres at y = 10 and y = 37 of the "
                  "body), not the bounding-box centre (the open door widens the -X side).",
       collision_hint="Box 1.8 x 4.9 x 1.45 m centred on the pivot; the open door separately "
                      "if needed.")
def police_car():
    OX = 8                                               # room for the open door on -X
    g = Grid(OX + 20, 50, 15)
    x0, x1 = OX + 1, OX + 18
    prof = _sedan_profile()
    profile_body(g, x0, x1, prof, "paint_white", "navy_dark")
    # two-tone: navy nose and tail sections, white doors and roof
    for y in list(range(0, 13)) + list(range(33, 47)):
        g.paint(x0, y, 0, x1, y, 9, "navy")
    g.paint(x0, 0, 3, x1, 46, 3, "navy_dark")                       # rocker band
    for yc in (10.5, 37.5):
        arch_lip(g, x0, yc, 3.0, 4.3, "navy_dark")
        arch_lip(g, x1, yc, 3.0, 4.3, "navy_dark")
        arch(g, x0, x0 + 1, yc, 3.0, 4.3)
        arch(g, x1, x1 - 1, yc, 3.0, 4.3)
    for x in (x0 + 1, x1 - 1):
        glass_rows(g, x, range(23, 28), 9, 12)
        glass_rows(g, x, range(15, 22), 9, 12)
    sloped_glass(g, range(27, 33), x0 + 2, x1 - 2, 9, +1)
    sloped_glass(g, range(10, 15), x0 + 2, x1 - 2, 9, -1)
    for x in (x0, x1):
        for y in (32, 22, 13):
            seam(g, x, y, 4, 8, "porcelain_shadow" if 13 < y < 33 else "navy_dark")
        g.set(x, 16, 7, "chrome")
    g.set(x1, 25, 7, "chrome")
    mirrors(g, 30, 9, x0 - 1, x1 + 1, "navy")
    g.clear(x0 - 1, 30, 9, x0 - 1, 31, 9)                           # left mirror is on the door
    g.set(x0 + 1, 31, 10, "chrome")                                 # A-pillar spotlight
    g.set(x0 + 1, 31, 11, "steel_dark")
    # unlit lightbar across the roof
    g.box(x0 + 3, 20, 14, x1 - 3, 22, 14, "charcoal")
    g.box(x0 + 3, 20, 14, x0 + 7, 22, 14, "lamp_red")
    g.box(x1 - 7, 20, 14, x1 - 3, 22, 14, "lamp_blue")
    g.box(x0 + 3, 21, 14, x1 - 3, 21, 14, "charcoal")               # dark divider
    # nose: grille, lamps, bumper, plate; push bar in front
    g.box(x0, 46, 2, x1, 46, 2, "charcoal")
    g.box(x0 + 5, 46, 4, x1 - 5, 46, 5, "black")
    for xa in (x0 + 1, x1 - 3):
        g.box(xa, 46, 5, xa + 2, 46, 5, "glass_hi")
    g.box(x0 + 8, 46, 3, x0 + 9, 46, 3, "label_cream")
    for xa in (x0 + 4, x1 - 5):
        g.box(xa, 47, 2, xa + 1, 48, 2, "black")                    # mounts
        g.box(xa, 48, 3, xa + 1, 48, 7, "black")                    # uprights
    g.box(x0 + 4, 48, 7, x1 - 4, 48, 7, "black")
    g.box(x0 + 4, 48, 4, x1 - 4, 48, 4, "iron_edge")                # scuffed rail
    # tail
    g.box(x0, 0, 2, x1, 0, 2, "charcoal")
    for xa in (x0, x1 - 2):
        g.box(xa, 0, 5, xa + 2, 0, 6, "signal_red_dark")
    g.box(x0 + 8, 0, 4, x0 + 9, 0, 4, "label_cream")
    tops(g, "paint_white_shadow", only=["paint_white"])
    tops(g, "navy", only=["navy"])
    # driver's door opening: carve the door out of the body, show the cabin
    g.clear(x0, 23, 3, x0, 31, 12)
    g.clear(x0 + 1, 23, 9, x0 + 1, 31, 12)
    g.box(x0 + 1, 23, 3, x0 + 6, 31, 3, "black")                    # floor / sill shadow
    g.box(x0 + 1, 23, 4, x0 + 1, 31, 4, "navy_dark")                # sill
    g.box(x0 + 2, 23, 4, x0 + 6, 26, 5, "slate_deep")               # seat cushion
    g.box(x0 + 2, 22, 6, x0 + 6, 23, 11, "slate_deep")              # seat back
    g.box(x0 + 2, 31, 6, x0 + 6, 31, 8, "charcoal")                 # dash
    g.box(x0 + 3, 29, 7, x0 + 5, 29, 9, "black")                    # steering wheel
    g.set(x0 + 4, 29, 8, "charcoal")
    g.box(x0 + 2, 27, 4, x0 + 6, 30, 4, "black")                    # footwell
    g.box(x0 + 7, 23, 4, x0 + 7, 31, 12, "black")                   # cabin depth
    g.box(x0 + 2, 23, 12, x0 + 6, 31, 12, "slate_dark")             # headliner in shadow
    g.box(x0 + 1, 23, 12, x0 + 1, 31, 12, "paint_white_shadow")     # roof drip rail
    # the door itself, swung ~75 degrees about its front hinge
    hx, hy = x0 - 1, 31
    ex, ey = x0 - 8, 29
    for z in range(3, 13):
        col = "paint_white" if z <= 8 else ("glass_deep" if z <= 11 else "paint_white")
        if z == 3:
            col = "navy_dark"
        fline(g, (hx, hy, z), (ex, ey, z), col)
    fline(g, (ex, ey, 9), (ex, ey, 12), "paint_white")              # window frame edge
    fline(g, (hx + 1, hy, 4), (hx + 1, hy, 8), "steel_dark")        # hinge
    fline(g, (hx, hy, 9), (ex, ey, 9), "paint_white")               # window sill
    g.box(hx - 1, hy + 1, 9, hx - 2, hy + 1, 9, "navy")             # its mirror
    g.set(hx - 2, hy + 1, 9, "glass_dark")
    # wheels
    wheel(g, (x0, x0 + 1), 10, 7)
    wheel(g, (x1 - 1, x1), 10, 7)
    wheel(g, (x0, x0 + 1), 37, 7)
    wheel(g, (x1 - 1, x1), 37, 7)
    return {"grid": g, "pivot_cells": (OX + 10.0, 24.0, 0.0)}


# ---------------------------------------------------------------------------
# pickup truck
# ---------------------------------------------------------------------------
@model("pickup_truck",
       story="An old full-size pickup that belonged to someone who fixed things for the "
             "neighbours. It was being loaded when it was left: tailgate dropped, a blue tarp "
             "half pulled over the side of the bed, one jerry can still standing by the gate. "
             "The maroon paint has oxidised pale on the bonnet and roof.",
       details=["Regular cab, square bonnet, tall chrome grille and chrome bumpers",
                "8-cell truck wheels (shared family profile) in rust-lipped arches",
                "Tailgate down; black bed liner", "Faded blue tarp heaped in the bed and "
                "draped over the camera-side wall", "Olive steel jerry can on the dropped tailgate",
                "Oxidised paint on the upper surfaces, rust at the arch lips and bed corners"],
       exclusions=["No badges or plate text", "No load straps (sub-cell)"],
       why="Body panels, pillars and 0.8 m wheels need 0.1 m cells; the game's structure grid "
           "is also 0.1 m.",
       notes=["Length 5.1 m includes the dropped tailgate (4.6 m body)."],
       pivot_note="Bottom centre between the axles (wheel centres at y = 13.5 and y = 41.5).",
       collision_hint="Box 1.8 x 4.7 x 1.7 m centred on the pivot.")
def pickup_truck():
    W = 20
    g = Grid(W, 51, 18)
    x0, x1 = 1, 18
    # cab (y 23..36), bonnet (37..48), nose (49..50)
    g.box(x0, 23, 3, x1, 48, 10, "maroon")
    g.box(x0, 23, 3, x1, 48, 3, "maroon_dark")
    for y, gt in ((23, 16), (24, 16), (25, 16), (26, 16), (27, 16), (28, 16), (29, 16),
                  (30, 16), (31, 16), (32, 15), (33, 14), (34, 13), (35, 12)):
        g.box(x0 + 1, y, 11, x1 - 1, y, gt, "maroon")
        g.set(x0 + 1, y, gt, 0)
        g.set(x1 - 1, y, gt, 0)
    g.box(x0, 37, 10, x1, 48, 10, "maroon")                       # square bonnet
    g.set(x0, 48, 10, 0)
    g.set(x1, 48, 10, 0)
    # bed: floor, walls, bulkhead
    g.box(x0, 5, 4, x1, 22, 5, "maroon_dark")
    g.box(x0 + 1, 5, 6, x1 - 1, 21, 6, "black")                     # liner floor
    for x in (x0, x1):
        g.box(x, 5, 4, x, 22, 10, "maroon")
        g.box(x, 5, 11, x, 22, 11, "maroon")
    g.box(x0, 22, 6, x1, 22, 11, "maroon")
    g.box(x0 + 1, 5, 6, x0 + 1, 21, 10, "charcoal")                 # liner walls
    g.box(x1 - 1, 5, 6, x1 - 1, 21, 10, "charcoal")
    g.box(x0 + 1, 21, 6, x1 - 1, 21, 10, "charcoal")
    # tailgate down: a slab behind the bed at floor level, inner face up (liner)
    g.box(x0, 0, 5, x1, 4, 5, "maroon")
    g.box(x0 + 1, 0, 6, x1 - 1, 4, 6, "charcoal")
    g.box(x0, 0, 4, x1, 0, 5, "maroon_dark")
    g.box(x0 + 3, 0, 6, x0 + 5, 0, 6, "steel_dark")                 # latch
    # rear bumper under the bed, chrome
    g.box(x0, 5, 2, x1, 6, 3, "chrome")
    g.box(x0 + 7, 5, 3, x0 + 10, 5, 3, "label_cream")              # plate
    for xa in (x0, x1):                                             # tail lamps on the posts
        g.box(xa, 5, 8, xa, 5, 10, "signal_red_dark")
    # nose: tall grille, lamps, chrome bumper
    g.box(x0, 49, 3, x1, 49, 10, "maroon")
    g.box(x0 + 4, 50, 5, x1 - 4, 50, 9, "chrome")
    g.box(x0 + 5, 50, 6, x1 - 5, 50, 8, "steel_dark")
    g.box(x0 + 5, 50, 7, x1 - 5, 50, 7, "chrome")
    for xa in (x0 + 1, x1 - 2):
        g.box(xa, 50, 7, xa + 1, 50, 8, "glass_hi")
    g.box(x0, 50, 3, x1, 50, 4, "chrome")
    g.box(x0 + 7, 50, 4, x0 + 10, 50, 4, "label_cream")
    for x in (x0, x1):
        g.set(x, 49, 10, 0)
    # arches, wheels and rust lips
    for yc in (13.0, 41.0):
        for x, xi in ((x0, x0 + 1), (x1, x1 - 1)):
            arch_lip(g, x, yc, 3.5, 4.8, "rust_dark")
            arch(g, x, xi, yc, 3.5, 4.8)
    # glass: side windows, back window, windscreen
    for x in (x0 + 1, x1 - 1):
        glass_rows(g, x, range(25, 32), 11, 15)
    for x in range(x0 + 2, x1 - 1):
        for z in range(11, 16):
            g.set(x, 23, z, "glass_dark" if z == 15 else "glass_deep")
    sloped_glass(g, range(31, 36), x0 + 2, x1 - 2, 11, +1)
    for x in (x0, x1):
        seam(g, x, 35, 4, 10, "maroon_dark")
        seam(g, x, 24, 4, 10, "maroon_dark")
        g.set(x, 32, 9, "chrome")
    mirrors(g, 33, 11, 0, W - 1, "chrome")
    # oxidised paint on the upper surfaces, rust at the bed corners
    tops(g, "red_dark", only=["maroon"])
    for x in (x0, x1):
        g.box(x, 5, 4, x, 6, 5, "rust_dark")
        g.set(x, 7, 4, "rust_deep")
    # blue tarp heaped in the front of the bed (two lumps above the rails) and draped over
    # the camera-side wall
    lumps = [(6.0, 17.0, 13.6, 4.6), (12.5, 18.0, 12.6, 4.0), (9.0, 13.0, 11.2, 3.4)]
    for x in range(x0 + 1, x1):
        for y in range(11, 21):
            h = max(zt - ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 * (zt - 7) / r
                    for cx, cy, zt, r in lumps)
            h = int(round(h))
            if h < 7:
                continue
            g.box(x, y, 7, x, y, h, "bottle_cap")
            g.set(x, y, h, "label_blue")
    for x in range(x0 + 1, x1):                    # fold shadows where the heap drops away
        for y in range(11, 21):
            for z in range(12, 6, -1):
                if g.get(x, y, z) == P("label_blue") and not g.get(x, y - 1, z) and z <= 10:
                    g.set(x, y, z, "blue_deep")
    for y in range(13, 21):                        # over the wall and hanging down the side
        g.set(x0, y, 12, "label_blue")
        g.set(x0 + 1, y, 12, "label_blue")
        drop = 8 if y in (15, 16, 17, 18) else 9
        for z in range(drop, 13):
            g.set(x0 - 1, y, z, "blue_deep" if z == drop else "bottle_cap")
        g.set(x0 - 1, y, 12, "label_blue")
    # jerry can standing on the dropped tailgate
    g.box(x0 + 2, 1, 6, x0 + 3, 4, 9, "olive_dark")
    g.box(x0 + 2, 1, 9, x0 + 3, 4, 9, "olive")
    g.box(x0 + 2, 2, 10, x0 + 2, 3, 10, "olive_dark")               # handle
    g.set(x0 + 3, 4, 10, "steel_dark")                              # spout cap
    wheel(g, (x0, x0 + 1), 13, 8)
    wheel(g, (x1 - 1, x1), 13, 8)
    wheel(g, (x0, x0 + 1), 41, 8)
    wheel(g, (x1 - 1, x1), 41, 8)
    return {"grid": g, "pivot_cells": (W / 2, 27.0, 0.0)}


# ---------------------------------------------------------------------------
# delivery van (high-roof panel van)
# ---------------------------------------------------------------------------
@model("delivery_van",
       story="A plain white delivery van stopped mid-round. The driver opened the back for "
             "the next drop and never came back: one rear door swung right out, the other "
             "folded against the side, parcels still stacked inside and one fallen against "
             "the bumper. Grime has run down from the roof edges.",
       details=["High-roof panel van: short bonnet, tall raked screen, windowless cargo sides",
                "7-cell wheels (shared family profile)", "Left rear door open 180 degrees "
                "(sticking out beside the rear), right rear door folded flat against the "
                "side at 270 degrees", "Plywood cargo floor, stacked and toppled cardboard "
                "parcels, one on the ground", "Sliding side door seams on the kerb (+X) side",
                "Grime streaks running down from the roof edge, dirt band at the sills"],
       exclusions=["No logos, livery or lettering", "No transparent glass"],
       why="Body panels, pillars and 0.65 m wheels need 0.1 m cells; the game's structure "
           "grid is also 0.1 m.",
       notes=["The open left door adds 0.9 m to the width at the rear (3.0 m with the door, "
              "2.1 m across the mirrors)."],
       pivot_note="Bottom centre between the axles (wheel centres at y = 13.5 and y = 41.5 "
                  "of the body), not the bounding-box centre.",
       collision_hint="Box 1.9 x 5.1 x 2.5 m centred on the pivot; the open doors separately "
                      "if needed.")
def delivery_van():
    OX = 9                                              # room for the open door on -X
    g = Grid(OX + 22, 52, 26)
    x0, x1 = OX + 1, OX + 19
    # cargo box (y 0..37) up to the high roof (z 24), cab (38..44) and nose (45..51)
    g.box(x0, 1, 2, x1, 38, 23, "paint_white")
    g.box(x0 + 1, 1, 24, x1 - 1, 38, 24, "paint_white")          # roof, edges rounded
    for y in range(39, 52):
        gt = {39: 23, 40: 22, 41: 21, 42: 19, 43: 18, 44: 16, 45: 14}.get(y)
        top = 12 if y <= 48 else (11 if y <= 50 else 10)
        g.box(x0, y, 2, x1, y, top, "paint_white")
        if gt:
            g.box(x0, y, top + 1, x1, y, gt, "paint_white")
            g.set(x0, y, gt, 0)
            g.set(x1, y, gt, 0)
        else:
            g.set(x0, y, top, 0)
            g.set(x1, y, top, 0)
    for y in (1, 51):                                           # chamfered corners
        for x in (x0, x1):
            g.clear(x, y, 0, x, y, 25)
    g.paint(x0, 0, 2, x1, 51, 3, "porcelain_shadow")           # dirt band at the sills
    g.paint(x0, 0, 2, x1, 51, 2, "porcelain_deep")
    # roof-edge grime streaks running down the cargo sides
    for x in (x0, x1):
        for (y, n) in ((4, 5), (9, 3), (15, 6), (22, 4), (30, 5), (35, 3)):
            seam(g, x, y, 23 - n, 23, "porcelain_mid")
    for yc in (13.5, 41.5):
        for x, xi in ((x0, x0 + 1), (x1, x1 - 1)):
            arch_lip(g, x, yc, 3.0, 4.3, "porcelain_shadow")
            arch(g, x, xi, yc, 3.0, 4.3)
    # cab glass: door windows, windscreen
    for x in (x0, x1):
        glass_rows(g, x, range(39, 44), 13, 19)
        for y in range(39, 44):
            for z in range(13, 20):
                if g.get(x, y, z) and not g.get(x, y, z + 1) and z < 19:
                    g.set(x, y, z, "paint_white")              # window follows the A pillar
    sloped_glass(g, range(39, 46), x0 + 1, x1 - 1, 13, +1)
    for x in (x0, x1):
        seam(g, x, 45, 4, 12, "porcelain_mid")
        seam(g, x, 38, 4, 21, "porcelain_mid")
        g.set(x, 40, 11, "steel_dark")                         # cab door handles
    # sliding door on the kerb (+X) side: seams, rail, handle
    for y in (24, 36):
        seam(g, x1, y, 3, 21, "porcelain_mid")
    g.box(x1, 24, 21, x1, 36, 21, "porcelain_shadow")
    g.set(x1, 34, 12, "steel_dark")
    mirrors(g, 44, 15, x0 - 1, x1 + 1, "charcoal")
    # nose: grille, lamps, bumper, plate
    g.box(x0, 51, 2, x1, 51, 4, "charcoal")
    g.box(x0 + 5, 51, 7, x1 - 5, 51, 9, "black")
    for xa in (x0 + 1, x1 - 3):
        g.box(xa, 51, 8, xa + 2, 51, 9, "glass_hi")
    g.box(x0 + 8, 51, 3, x0 + 10, 51, 3, "label_cream")
    tops(g, "paint_white_shadow", only=["paint_white"])
    # rear: open cargo bay
    g.clear(x0 + 1, 0, 3, x1 - 1, 36, 22)
    g.box(x0 + 1, 1, 3, x1 - 1, 36, 3, "pine_aged")                # plywood floor
    g.box(x0 + 1, 37, 3, x1 - 1, 37, 22, "galv_dark")             # bulkhead
    g.box(x0, 0, 2, x1, 0, 3, "charcoal")                          # rear step bumper
    g.box(x0 + 8, 0, 3, x0 + 10, 0, 3, "label_cream")
    for xa in (x0, x1):
        g.box(xa, 1, 15, xa, 1, 19, "signal_red_dark")             # tall tail lamps
    g.box(x0 + 1, 1, 23, x1 - 1, 1, 23, "paint_white_shadow")      # door header
    # parcels: a stack at the front of the bay, a toppled one near the doors
    for (xa, ya, za, sx, sy, sz, c) in ((x0 + 2, 28, 4, 5, 5, 5, "card"),
                                        (x0 + 2, 29, 9, 4, 4, 4, "card_hi"),
                                        (x0 + 8, 30, 4, 4, 6, 4, "card_dark"),
                                        (x1 - 6, 26, 4, 5, 4, 7, "card"),
                                        (x1 - 5, 27, 11, 3, 3, 3, "card_hi"),
                                        (x0 + 4, 6, 4, 5, 3, 3, "card"),
                                        (x0 + 10, 3, 4, 3, 4, 3, "card_hi")):
        g.box(xa, ya, za, xa + sx - 1, ya + sy - 1, za + sz - 1, c)
        g.box(xa, ya, za + sz - 1, xa + sx - 1, ya + sy - 1, za + sz - 1, "card_hi"
              if c != "card_hi" else "card")
    # left rear door open 180 degrees: hinged at the rear-left corner, sticking out to -X
    hx = x0 - 1
    g.box(hx - 8, 0, 3, hx, 0, 22, "paint_white_shadow")
    g.box(hx - 7, 0, 14, hx - 1, 0, 20, "glass_deep")              # its window
    g.box(hx - 7, 0, 20, hx - 1, 0, 20, "glass_dark")
    g.box(hx - 6, 0, 8, hx - 5, 0, 8, "steel_dark")                # inner handle
    g.box(hx, 1, 5, hx, 1, 6, "steel_dark")                        # hinges on the body
    g.box(hx, 1, 17, hx, 1, 18, "steel_dark")
    # right rear door folded flat against the kerb side (270 degrees)
    g.box(x1 + 1, 1, 3, x1 + 1, 9, 22, "paint_white")
    g.box(x1 + 1, 2, 14, x1 + 1, 8, 20, "glass_deep")
    g.box(x1 + 1, 2, 20, x1 + 1, 8, 20, "glass_dark")
    # a parcel fallen out against the bumper
    g.box(x0 + 4, -0 + 0, 0, x0 + 7, 0, 1, "card")
    wheel(g, (x0, x0 + 1), 13, 7)
    wheel(g, (x1 - 1, x1), 13, 7)
    wheel(g, (x0, x0 + 1), 41, 7)
    wheel(g, (x1 - 1, x1), 41, 7)
    return {"grid": g, "pivot_cells": (OX + 10.5, 27.5, 0.0)}


# ---------------------------------------------------------------------------
# utility (bucket) truck
# ---------------------------------------------------------------------------
def cone_stack(g, x, y, z, n=3):
    """A stack of n road cones on a 3x3 footprint at 0.1 m: one dark rim per cone, an orange
    body with a pale band, a narrow top."""
    for k in range(n):
        g.box(x, y, z + k, x + 2, y + 2, z + k, "charcoal" if k == 0 else "safety_orange_dark")
    zt = z + n
    g.box(x, y, zt, x + 2, y + 2, zt, "safety_orange")
    g.box(x, y, zt + 1, x + 2, y + 2, zt + 1, "porcelain_mid")
    g.box(x + 1, y + 1, zt + 2, x + 1, y + 1, zt + 3, "safety_orange")


@model("utility_truck",
       story="A line crew's bucket truck abandoned on the shoulder with its boom still "
             "stowed. It was already old: rust is eating the compartment doors and arch lips, "
             "the rear tyre on the road side has gone flat, and the crew's cones are still "
             "stacked on the back step.",
       details=["Conventional cab, square bonnet and a utility body with side compartment "
                "doors", "Turret and two-section boom stowed rearward on a rest, fibreglass "
                "bucket at the rear corner", "8-cell truck wheels (shared family profile), "
                "rear-left tyre flat", "Cone stack on the rear step", "Faded safety orange "
                "(paler on top), rust along door bottoms and arch lips, unlit amber beacon"],
       exclusions=["No company names, numbers or hazard text", "No lit beacon"],
       why="Compartment doors, boom and 0.8 m wheels need 0.1 m cells; the game's structure "
           "grid is also 0.1 m.",
       pivot_note="Bottom centre between the axles (wheel centres at y = 13 and y = 46).",
       collision_hint="Box 2.2 x 5.6 x 2.3 m centred on the pivot.")
def utility_truck():
    W = 23
    g = Grid(W, 56, 24)
    sx0, sx1 = 1, 21                                     # service body
    cx0, cx1 = 2, 20                                     # cab
    # rear step bumper and the service body (y 3..36)
    g.box(sx0, 0, 2, sx1, 2, 3, "charcoal")
    g.box(sx0, 3, 3, sx1, 36, 15, "safety_orange")
    g.box(sx0, 3, 3, sx1, 36, 4, "safety_orange_dark")
    g.clear(sx0 + 5, 3, 9, sx1 - 5, 33, 15)              # open bed between the compartments
    g.box(sx0 + 5, 3, 8, sx1 - 5, 33, 8, "galv_dark")    # tread-plate floor
    g.box(sx0 + 5, 3, 9, sx1 - 5, 3, 10, "safety_orange_dark")  # tailboard
    # compartment door seams, handles and rusted bottoms on both sides
    for x in (sx0, sx1):
        for y in (3, 10, 19, 27, 36):
            seam(g, x, y, 4, 15, "safety_orange_dark")
        for y in (6, 23, 31):
            g.set(x, y, 11, "steel_dark")
        for (ya, yb) in ((4, 9), (20, 26), (28, 35)):
            g.box(x, ya, 4, x, yb, 4, "rust_dark")
            g.set(x, ya + 1, 5, "rust_deep")
        g.box(x, 3, 15, x, 36, 15, "safety_orange_dark")  # top rail
    # cab (y 37..46), bonnet (47..53), nose (54..55)
    g.box(cx0, 37, 3, cx1, 53, 12, "safety_orange")
    g.box(cx0, 37, 3, cx1, 53, 4, "safety_orange_dark")
    for y, gt in ((37, 20), (38, 20), (39, 20), (40, 20), (41, 20), (42, 20), (43, 19),
                  (44, 18), (45, 16), (46, 14)):
        g.box(cx0 + 1, y, 13, cx1 - 1, y, gt, "safety_orange")
        g.set(cx0 + 1, y, gt, 0)
        g.set(cx1 - 1, y, gt, 0)
    for x in (cx0, cx1):
        g.set(x, 53, 12, 0)
    g.box(cx0, 54, 3, cx1, 54, 11, "safety_orange")
    g.box(cx0 + 4, 55, 5, cx1 - 4, 55, 10, "charcoal")           # grille
    g.box(cx0 + 5, 55, 6, cx1 - 5, 55, 9, "black")
    for xa in (cx0 + 1, cx1 - 2):
        g.box(xa, 55, 8, xa + 1, 55, 9, "glass_hi")
    g.box(sx0, 55, 2, sx1, 55, 4, "steel")                        # bumper
    g.box(cx0 + 7, 55, 4, cx0 + 10, 55, 4, "label_cream")
    for x in (cx0 + 1, cx1 - 1):
        glass_rows(g, x, range(38, 44), 13, 18)
    for x in range(cx0 + 3, cx1 - 2):
        for z in (16, 17):
            g.set(x, 37, z, "glass_deep" if z == 16 else "glass_dark")   # small back window
    sloped_glass(g, range(42, 47), cx0 + 2, cx1 - 2, 13, +1)
    for x in (cx0, cx1):
        seam(g, x, 46, 5, 12, "safety_orange_dark")
        g.set(x, 43, 10, "steel_dark")
    # big truck mirrors on stalks
    for x, inner in ((0, 1), (W - 1, W - 2)):
        g.box(x, 45, 12, x, 45, 16, "charcoal")
        g.set(inner, 45, 12, "steel_dark")
        g.set(inner, 45, 15, "steel_dark")
        g.set(inner, 45, 16, "steel_dark")
        g.set(inner + (1 if x == 0 else -1), 45, 16, "steel_dark")
    g.box(cx0 + 9, 39, 21, cx0 + 10, 40, 21, "hazard_yellow_dark")  # unlit beacon
    # faded upper surfaces
    tops(g, "rust_hi", only=["safety_orange"])
    # turret and the stowed boom (lower boom steel-orange, insulated upper boom white)
    for (i, j) in g.disc_cells(11.5, 31.5, 2.6):
        g.box(i, j, 9, i, j, 15, "safety_orange_dark")
        g.set(i, j, 16, "charcoal")
    g.box(10, 18, 17, 13, 33, 18, "safety_orange")                  # lower boom
    g.box(10, 18, 18, 13, 33, 18, "rust_hi")
    g.box(11, 3, 17, 12, 18, 18, "paint_white_shadow")             # upper boom
    g.box(11, 3, 18, 12, 18, 18, "paint_white")
    g.box(10, 17, 16, 13, 19, 19, "charcoal")                      # elbow
    g.box(11, 6, 9, 12, 7, 16, "steel_dark")                       # boom rest on the bed
    # bucket resting at the rear-right corner, open top, dark liner
    g.box(14, 1, 15, 19, 6, 22, "paint_white_shadow")
    g.box(15, 2, 17, 18, 5, 22, 0)
    g.box(15, 2, 16, 18, 5, 16, "black")
    for (xa, ya, xb, yb) in ((14, 1, 19, 1), (14, 6, 19, 6), (14, 1, 14, 6), (19, 1, 19, 6)):
        g.box(xa, ya, 22, xb, yb, 22, "porcelain_deep")            # scuffed rim (a ring)
    g.box(14, 1, 15, 14, 6, 16, "porcelain_deep")
    g.box(13, 3, 17, 13, 4, 18, "steel_dark")                      # boom tip to bucket
    # cone stack on the rear step (camera-side corner)
    cone_stack(g, 1, 0, 4, 3)
    # arches with rusted lips, wheels; rear-left tyre flat
    for yc, wc in ((13.0, "8f"), (46.0, 8)):
        for x, xi in ((sx0, sx0 + 1), (sx1, sx1 - 1)):
            arch_lip(g, x, yc, 3.5, 4.8, "rust_dark")
            arch(g, x, xi, yc, 3.5, 4.8)
    wheel(g, (sx0, sx0 + 1), 13, "8f", outer=0)
    wheel(g, (sx1 - 1, sx1), 13, 8)
    wheel(g, (sx0, sx0 + 1), 46, 8)
    wheel(g, (sx1 - 1, sx1), 46, 8)
    return {"grid": g, "pivot_cells": (W / 2, 29.5, 0.0)}
