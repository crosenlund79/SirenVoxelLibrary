"""Batch E1 - regional-map buildings (creator: Claude).

Real-world metres at 0.5 m cells. X right, Y front (+Y = street side / main entrance), Z up;
inclusive cell ranges; everything stands on z = 0 and is one 6-connected piece.

Shared conventions for the whole family (so buildings compare honestly side by side):
  * z = 0 is the lot / ground layer (lawn, asphalt, gravel); walls also start at z = 0 as the
    foundation course, so the visible facade begins at z = 1.
  * Storey = 3 m = 6 cells. Ground floor z = 1..6, first floor z = 7..12, and so on.
  * Doors are 2 cells wide x 4 tall (1.0 x 2.0 m); windows are 2 cells tall (1.0 m) with the
    sill 1 m above the floor (storey z offsets 2..3 -> z = 3..4 on the ground floor) and the
    head aligned with the door head. Windows are recessed one cell so they read as openings.
  * Roof families: pitched = shingle_brown or roof (grey) with 1-cell eaves; flat = parapet
    ring with a grey membrane deck and galvanised HVAC boxes; sheds = galv / roof metal.
"""
from catalog_registry import model
from voxkit import Grid

STOREY = 6


# ---------------------------------------------------------------------------
# helpers (local to this family)
# ---------------------------------------------------------------------------
def opening(g, face, pos, a0, a1, z0, z1, c="glass_dark", inset=1):
    """Window / door in a wall face. face is '+y', '-y', '+x' or '-x'; pos is the coordinate
    of that face's outer wall layer; a0..a1 the range along the wall. The outer layer is
    removed and the cell behind it gets colour c (inset=1), or the outer layer is recoloured
    in place (inset=0, flush: glazing bands, boarded panels)."""
    sgn = 1 if face[0] == "+" else -1
    ax = face[1]
    for d in range(inset + 1):
        p = pos - sgn * d
        col = c if d == inset else 0
        if ax == "y":
            g.box(a0, p, z0, a1, p, z1, col)
        else:
            g.box(p, a0, z0, p, a1, z1, col)


def gable(g, x0, x1, y0, y1, z0, roof, wall=None, s=1, ov=1, axis="x", ridge=None):
    """Gable roof over walls x0..x1, y0..y1 with eaves at z0. axis = direction of the ridge.
    s = horizontal run per 1-cell rise (1 = 45 deg, 2 = ~27 deg). ov = eave/rake overhang.
    Gable-end triangles are painted `wall`. Returns the ridge z."""
    if axis == "x":
        la, lb, ea, eb = y0 - ov, y1 + ov, x0 - ov, x1 + ov
        wa, wb = x0, x1
    else:
        la, lb, ea, eb = x0 - ov, x1 + ov, y0 - ov, y1 + ov
        wa, wb = y0, y1
    layers = []
    k = 0
    while la + k * s <= lb - k * s:
        layers.append((la + k * s, lb - k * s))
        k += 1
    for k, (a, b) in enumerate(layers):
        z = z0 + k
        nxt = layers[k + 1] if k + 1 < len(layers) else None
        for t in range(a, b + 1):
            skin = nxt is None or not (nxt[0] <= t <= nxt[1])
            col = (ridge or roof) if nxt is None else roof
            if skin:
                lo, hi = ea, eb
                fill = col
            else:
                lo, hi = wa, wb
                fill = roof
            for e in range(lo, hi + 1):
                cc = fill
                if not skin and wall and e in (wa, wb):
                    cc = wall
                if axis == "x":
                    g.set(e, t, z, cc)
                else:
                    g.set(t, e, z, cc)
    return z0 + len(layers) - 1


def hip(g, x0, x1, y0, y1, z0, roof, s=1, ov=1, ridge=None):
    """Hip roof over walls x0..x1, y0..y1, eaves at z0. Returns the top z."""
    xa, xb, ya, yb = x0 - ov, x1 + ov, y0 - ov, y1 + ov
    k = 0
    while xa + k * s <= xb - k * s and ya + k * s <= yb - k * s:
        g.box(xa + k * s, ya + k * s, z0 + k, xb - k * s, yb - k * s, z0 + k, roof)
        k += 1
    top = z0 + k - 1
    if ridge:
        g.paint(xa, ya, top, xb, yb, top, ridge)
    return top


def flat_roof(g, x0, y0, x1, y1, z, parapet="concrete", deck="roof", h=1):
    """Parapet ring of height h on top of a solid block whose top layer is z - 1."""
    g.box(x0, y0, z, x1, y1, z + h - 1, parapet)
    g.clear(x0 + 1, y0 + 1, z, x1 - 1, y1 - 1, z + h - 1)
    g.paint(x0 + 1, y0 + 1, z - 1, x1 - 1, y1 - 1, z - 1, deck)


def hvac(g, x, y, z, w=2, d=2, h=1, c="galv"):
    g.box(x, y, z, x + w - 1, y + d - 1, z + h - 1, c)
    g.paint(x, y, z + h - 1, x + w - 1, y + d - 1, z + h - 1, "galv_hi")


def windows_x(g, xs, y, z0, face="+y", w=2, h=2, c="glass_dark", inset=1):
    """A row of windows along X on a +y / -y face; xs are left edges."""
    for x in xs:
        opening(g, face, y, x, x + w - 1, z0, z0 + h - 1, c, inset)


def windows_y(g, ys, x, z0, face="-x", w=2, h=2, c="glass_dark", inset=1):
    for y in ys:
        opening(g, face, x, y, y + w - 1, z0, z0 + h - 1, c, inset)


def stalls(g, x0, x1, y0, y1, every=5, c="line_white", axis="y"):
    """Parking-stall lines painted on z = 0: lines run along `axis`, repeated every `every`."""
    if axis == "y":
        for x in range(x0, x1 + 1, every):
            g.box(x, y0, 0, x, y1, 0, c)
    else:
        for y in range(y0, y1 + 1, every):
            g.box(x0, y, 0, x1, y, 0, c)


def car(g, x, y, body="beige", axis="y", roof=None, z=1):
    """Map-scale parked car, 4 x 9 cells (2 x 4.5 m), 3 cells tall, nose toward +axis."""
    roof = roof or body
    if axis == "y":
        g.box(x, y, z, x + 3, y + 8, z, "black")                 # tyres / underbody shadow
        g.box(x, y + 1, z, x + 3, y + 7, z, body)
        g.box(x, y, z + 1, x + 3, y + 8, z + 1, body)
        g.box(x, y + 2, z + 2, x + 3, y + 6, z + 2, "glass_deep")
        g.box(x, y + 3, z + 2, x + 3, y + 5, z + 2, roof)
        g.paint(x, y + 2, z + 2, x + 3, y + 2, z + 2, "glass_dark")
    else:
        g.box(x, y, z, x + 8, y + 3, z, "black")
        g.box(x + 1, y, z, x + 7, y + 3, z, body)
        g.box(x, y, z + 1, x + 8, y + 3, z + 1, body)
        g.box(x + 2, y, z + 2, x + 6, y + 3, z + 2, "glass_deep")
        g.box(x + 3, y, z + 2, x + 5, y + 3, z + 2, roof)
        g.paint(x + 6, y, z + 2, x + 6, y + 3, z + 2, "glass_dark")


def shrub(g, x, y, w=2, d=2, h=1, c="leaf_mid", top="leaf"):
    g.box(x, y, 1, x + w - 1, y + d - 1, h, c)
    g.paint(x, y, h, x + w - 1, y + d - 1, h, top)


def fence_line(g, x0, y0, x1, y1, h=2, post="steel_dark", panel="mesh", every=4):
    """Chain-link / mesh fence on z = 1..h along an axis-aligned line, posts every `every`."""
    g.box(x0, y0, 1, x1, y1, h, panel)
    if x0 == x1:
        for y in range(min(y0, y1), max(y0, y1) + 1, every):
            g.box(x0, y, 1, x0, y, h, post)
        g.box(x0, max(y0, y1), 1, x0, max(y0, y1), h, post)
    else:
        for x in range(min(x0, x1), max(x0, x1) + 1, every):
            g.box(x, y0, 1, x, y0, h, post)
        g.box(max(x0, x1), y0, 1, max(x0, x1), y0, h, post)




def storefront(g, face, pos, a0, a1, z0, z1, every=3, glass="glass_dark", mull="steel_dark",
               inset=1):
    """Glazed shopfront: the outer wall layer becomes mullions every `every` cells (and at
    both ends); the panes between are recessed glass."""
    for a in range(a0, a1 + 1):
        if (a - a0) % every == 0 or a == a1:
            if face[1] == "y":
                g.box(a, pos, z0, a, pos, z1, mull)
            else:
                g.box(pos, a, z0, pos, a, z1, mull)
        else:
            opening(g, face, pos, a, a, z0, z1, glass, inset)


def cross_y(g, cx, y, cz, arm=1, half=1, c="signal_red"):
    """Greek cross in the XZ plane at row y; arms `arm` cells wide reaching `half` arm-widths
    from the centre square (half=1 -> 3x3 cross of 1-cell arms, arm=2 -> 6x6)."""
    n = arm * (2 * half + 1)
    x0, z0 = cx - n // 2, cz - n // 2
    m0 = arm * half
    g.box(x0 + m0, y, z0, x0 + m0 + arm - 1, y, z0 + n - 1, c)
    g.box(x0, y, z0 + m0, x0 + n - 1, y, z0 + m0 + arm - 1, c)


def pole_sign(g, x, y, z_top_pole, board, c="label_cream", frame="charcoal", post="steel"):
    """Free-standing pole with a blank board facing +Y. board = (x0, x1, z0, z1)."""
    g.box(x, y, 1, x, y, z_top_pole, post)
    bx0, bx1, bz0, bz1 = board
    g.box(bx0, y, bz0, bx1, y, bz1, frame)
    if bx1 - bx0 >= 2 and bz1 - bz0 >= 2:
        g.box(bx0 + 1, y, bz0 + 1, bx1 - 1, y, bz1 - 1, c)


def flagpole(g, x, y, top, flag=("navy", "paint_white"), w=3):
    """Mast on z = 1..top with a plain two-band flag (no emblem) flying toward +X."""
    g.box(x, y, 1, x, y, top, "steel_hi")
    g.box(x + 1, y, top - 2, x + w, y, top - 1, flag[0])
    g.box(x + 1, y, top - 2, x + w, y, top - 2, flag[1])


def sandbags(g, x0, y0, x1, y1, h=2, c="khaki", top="khaki_dark"):
    g.box(x0, y0, 1, x1, y1, h, c)
    for z in range(2, h + 1, 2):
        g.paint(x0, y0, z, x1, y1, z, top)


# ---------------------------------------------------------------------------
# houses and flats
# ---------------------------------------------------------------------------
@model("small_family_house",
       silhouette="Low blue box under a steep brown side-gable, brick chimney up one gable, small porch roof on two white posts.",
       story="A one-storey starter home on a small lot. The family boarded every window and "
             "left in the first week; the lawn has gone to seed around the porch.",
       details=["45-degree side-gable shingle roof with 0.5 m eaves and rakes",
                "Brick chimney running up the camera-side gable",
                "Covered porch on two white posts, door centred on the street side",
                "Pale plywood over every window", "Overgrown lawn, concrete path to the street"],
       exclusions=["No readable text, no house number", "No interior"],
       why="A 45-degree gable reads clearly as a pitched roof at map scale.")
def small_family_house():
    g = Grid(18, 18, 15)
    W0, W1, D0, D1 = 2, 15, 1, 11                     # walls 7.0 x 5.5 m
    g.box(0, 0, 0, 17, 17, 0, "grass")                 # lot 9 x 9 m
    g.box(8, 12, 0, 9, 17, 0, "concrete")              # path
    g.box(0, 13, 0, 5, 17, 0, "grass_hi")              # long grass
    g.box(12, 14, 0, 17, 17, 0, "grass_hi")
    g.box(16, 2, 0, 17, 9, 0, "grass_dry")
    g.box(W0, D0, 0, W1, D1, 6, "siding_blue")
    g.paint(W0, D0, 0, W1, D1, 0, "concrete_dark")
    top = gable(g, W0, W1, D0, D1, 7, "shingle_brown", wall="siding_blue", s=1, ov=1)
    g.box(W0 - 1, 4, 0, W0 - 1, 5, top, "red")         # chimney on the -X gable
    g.paint(W0 - 1, 4, top, W0 - 1, 5, top, "red_dark")
    # front: door and boarded windows
    opening(g, "+y", D1, 8, 9, 1, 4, "wood_stain")
    for x in (3, 13):
        opening(g, "+y", D1, x, x + 1, 3, 4, "pine_light", inset=0)
    # porch: deck, posts, flat shingle roof below the eave
    g.box(6, 12, 0, 11, 14, 1, "wgrey")
    g.box(6, 14, 2, 6, 14, 4, "paint_white")
    g.box(11, 14, 2, 11, 14, 4, "paint_white")
    g.box(5, 12, 5, 12, 15, 5, "shingle_brown")
    # sides, back, gable vent (all boarded)
    opening(g, "-x", W0, 8, 9, 3, 4, "pine_light", inset=0)
    opening(g, "-x", W0, 6, 6, 9, 10, "pine_light", inset=0)
    for y in (3, 8):
        opening(g, "+x", W1, y, y + 1, 3, 4, "pine_light", inset=0)
    for x in (4, 11):
        opening(g, "-y", D0, x, x + 1, 3, 4, "pine_light", inset=0)
    shrub(g, 0, 9, 2, 2, 1)
    shrub(g, 14, 12, 2, 2, 1)
    return g


@model("large_suburban_house",
       silhouette="Two-storey cream block under a broad grey hip roof with a lower hip-roofed garage whose front corner has caved in.",
       story="A two-storey family house with an attached garage. A storm brought a limb down "
             "on the garage the first winter nobody was home; its front corner has caved in "
             "and the door has jammed half open.",
       details=["Low-pitch grey hip roof over two storeys, lower hip roof on the garage",
                "Collapsed front corner of the garage roof with exposed rafters and debris",
                "Gabled entry portico, shuttered upper windows",
                "Roll-up garage door jammed 0.5 m open, concrete driveway"],
       exclusions=["No readable text, no house number", "No interior beyond the visible hole"],
       why="Two 3 m storeys, 1 x 1 m windows and a 2.5 m garage door read at 0.5 m cells.")
def large_suburban_house():
    g = Grid(23, 20, 18)
    g.box(0, 0, 0, 22, 19, 0, "grass")                 # lot 11.5 x 10 m
    g.box(1, 15, 0, 7, 19, 0, "concrete")              # driveway
    g.box(14, 17, 0, 15, 19, 0, "concrete")            # path
    g.box(8, 16, 0, 15, 16, 0, "concrete")
    # garage (camera side), lower hip roof
    g.box(1, 5, 0, 7, 14, 6, "siding_cream")
    g.paint(1, 5, 0, 7, 14, 0, "concrete_dark")
    hip(g, 1, 7, 5, 14, 7, "roof", s=1)
    # main block, two storeys; eaves at z = 12 (upper rooms tuck under the roof)
    M0, M1, D0, D1 = 8, 21, 4, 13
    g.box(M0, D0, 0, M1, D1, 11, "siding_cream")
    g.paint(M0, D0, 0, M1, D1, 0, "concrete_dark")
    hip(g, M0, M1, D0, D1, 12, "roof", s=1, ridge="roof_dark")
    # collapsed front corner of the garage roof: a clean break with exposed timber edges
    g.clear(0, 11, 7, 4, 15, 11)
    g.clear(1, 12, 6, 3, 14, 6)                        # wall plate broken at the corner
    for (x, y, z) in ((5, 11, 9), (5, 12, 8), (5, 13, 8), (5, 14, 7), (5, 15, 7)):
        g.paint_cell(x, y, z, "wood_stain")
    for (x, y, z) in ((1, 10, 8), (2, 10, 9), (3, 10, 10), (4, 10, 10)):
        g.paint_cell(x, y, z, "wood_stain")
    g.box(2, 10, 1, 4, 13, 1, "roof_dark")             # fallen roofing on the floor
    g.box(2, 11, 2, 3, 12, 2, "wood_stain")
    g.paint(2, 6, 0, 6, 13, 0, "concrete_dark")
    # garage door jammed half open
    opening(g, "+y", 14, 3, 6, 1, 1, "black")
    opening(g, "+y", 14, 3, 6, 2, 4, "paint_white_shadow", inset=0)
    # front windows (ground z 3..4, upper z 9..10), shutters on the upper floor
    for x in (10, 18):
        opening(g, "+y", D1, x, x + 1, 3, 4)
    for x in (10, 14, 18):
        opening(g, "+y", D1, x, x + 1, 9, 10)
        g.paint(x - 1, D1, 9, x - 1, D1, 10, "green_dark")
        g.paint(x + 2, D1, 9, x + 2, D1, 10, "green_dark")
    opening(g, "+y", D1, 14, 15, 1, 4, "wood_stain")   # front door
    # portico: two posts carrying a small hip roof
    g.box(13, 14, 0, 16, 16, 0, "concrete_hi")
    g.box(13, 16, 1, 13, 16, 4, "paint_white")
    g.box(16, 16, 1, 16, 16, 4, "paint_white")
    g.box(12, 14, 5, 17, 17, 5, "roof")
    g.box(13, 14, 6, 16, 16, 6, "roof")
    # side windows: upper floor above the garage roof, +X side both floors
    for y in (6, 10):
        opening(g, "-x", M0, y, y + 1, 9, 10)
        opening(g, "+x", M1, y, y + 1, 3, 4)
        opening(g, "+x", M1, y, y + 1, 9, 10)
    for x in (10, 17):
        opening(g, "-y", D0, x, x + 1, 3, 4)
        opening(g, "-y", D0, x, x + 1, 9, 10)
    opening(g, "-x", 1, 7, 8, 3, 4)                     # garage side window
    shrub(g, 9, 14, 3, 1, 1)
    shrub(g, 18, 14, 3, 1, 1)
    return g


@model("apartment_block",
       silhouette="Tall plaster slab with sage-fronted balcony bands and a glazed stair core rising above the parapet.",
       story="A five-storey council block of twenty flats around a central stair core. A fire "
             "gutted one third-floor flat in the first days; the rest were locked and left.",
       details=["Five 3 m storeys, flat roof with parapet, stair penthouse and HVAC",
                "Continuous balcony bands on the street side, glazed stair core with entrance "
                "canopy", "Soot-blackened burnt-out flat on the third floor",
                "Punched windows on the sides and back"],
       exclusions=["No readable text", "No interiors"],
       why="Storey bands, balconies and window rhythm survive at 0.5 m; railings are solid "
           "bands.")
def apartment_block():
    g = Grid(24, 18, 34)
    g.box(0, 0, 0, 23, 17, 0, "concrete")              # lot 12 x 9 m
    g.box(0, 0, 0, 23, 1, 0, "grass")
    g.box(0, 15, 0, 23, 17, 0, "concrete_hi")          # pavement
    X0, X1, Y0, Y1, ZT = 1, 22, 2, 12, 30
    g.box(X0, Y0, 0, X1, Y1, ZT, "plaster")
    g.paint(X0, Y0, 0, X1, Y1, 0, "concrete_dark")
    flat_roof(g, X0, Y0, X1, Y1, ZT + 1, "concrete_hi", "roof")
    # stair core on the front, rising above the roof
    g.box(10, 13, 0, 13, 14, ZT + 3, "concrete")
    g.box(10, 9, ZT + 1, 13, 14, ZT + 3, "concrete")
    g.paint(10, 9, ZT + 3, 13, 14, ZT + 3, "concrete_hi")
    for i in range(5):
        opening(g, "+y", 14, 11, 12, 6 * i + 3, 6 * i + 5, "glass_dark")
    opening(g, "+y", 14, 11, 12, 1, 4, "glass")        # entrance
    g.box(9, 15, 5, 14, 16, 5, "concrete_hi")          # entrance canopy
    # balcony bands on storeys 2..5, doors and windows behind
    for i in range(1, 5):
        z = 6 * i
        for (a, b) in ((X0, 9), (14, X1)):
            g.box(a, 13, z, b, 14, z, "concrete")
            g.box(a, 14, z + 1, b, 14, z + 1, "sage")
            g.box(a, 13, z + 1, a, 13, z + 1, "concrete_hi")
            g.box(b, 13, z + 1, b, 13, z + 1, "concrete_hi")
        for x in (2, 6, 15, 19):
            opening(g, "+y", Y1, x, x + 1, z + 1, z + 4, "glass_dark")
    for x in (2, 6, 15, 19):                            # ground floor windows
        opening(g, "+y", Y1, x, x + 1, 3, 4)
    # side and back windows
    for i in range(5):
        z = 6 * i + 3
        for y in (4, 9):
            opening(g, "-x", X0, y, y + 1, z, z + 1)
            opening(g, "+x", X1, y, y + 1, z, z + 1)
        for x in (3, 7, 11, 15, 19):
            opening(g, "-y", Y0, x, x + 1, z, z + 1)
    # burnt-out flat: third floor (storey 3), left of the core
    z = 12
    g.paint(2, 12, z + 1, 7, 12, z + 6, "char")
    g.paint(3, 12, z + 7, 6, 12, z + 8, "ash_dark")
    g.paint(X0, 13, z, 9, 14, z + 1, "ash_dark")
    g.paint(2, 13, z, 7, 14, z + 1, "char")
    opening(g, "+y", Y1, 2, 3, z + 1, z + 4, "soot")
    opening(g, "+y", Y1, 6, 7, z + 1, z + 4, "soot")
    # roof plant
    hvac(g, 3, 4, ZT + 1, 3, 2)
    hvac(g, 17, 4, ZT + 1, 3, 2)
    hvac(g, 17, 8, ZT + 1, 2, 2)
    return g


# ---------------------------------------------------------------------------
# shops and food
# ---------------------------------------------------------------------------
@model("convenience_store",
       silhouette="Small flat-roofed box with a raised false front, blue sign band and a glazed, partly boarded shopfront.",
       story="A corner convenience store that was looted on the second night: two of the "
             "front panes were smashed and later boarded by the owner, the ice chest is "
             "still chained by the door.",
       details=["Flat roof behind a raised front parapet with a blank colour sign band",
                "Mullioned glass shopfront, two panes boarded with plywood",
                "Ice chest and propane cage beside the door", "Small lot with three stalls"],
       exclusions=["No readable text or logo on the sign band"])
def convenience_store():
    g = Grid(16, 18, 11)
    g.box(0, 0, 0, 15, 17, 0, "asphalt")
    g.box(0, 11, 0, 15, 12, 0, "concrete_hi")          # sidewalk
    stalls(g, 0, 15, 13, 17, every=5)
    X0, X1, Y0, Y1 = 1, 14, 1, 10
    g.box(X0, Y0, 0, X1, Y1, 7, "plaster")
    g.paint(X0, Y0, 0, X1, Y1, 0, "concrete_dark")
    flat_roof(g, X0, Y0, X1, Y1, 8, "concrete_hi", "roof")
    g.box(X0, Y1, 8, X1, Y1, 9, "plaster")             # raised false front
    g.box(X0 + 1, Y1, 7, X1 - 1, Y1, 8, "label_blue")  # blank sign band
    storefront(g, "+y", Y1, 2, 13, 1, 5, every=3)
    opening(g, "+y", Y1, 7, 8, 1, 4, "glass")          # door
    g.paint(7, Y1 - 1, 1, 8, Y1 - 1, 4, "glass")
    for x in (3, 4):                                    # boarded panes
        g.box(x, Y1, 1, x, Y1, 5, "pine_light")
    g.box(X0 + 1, Y1 + 1, 6, X1 - 1, Y1 + 1, 6, "steel_dark")  # awning lip
    g.box(10, 11, 1, 12, 11, 2, "paint_white")         # ice chest
    g.box(13, 11, 1, 13, 11, 3, "galv_dark")           # propane cage
    hvac(g, 4, 3, 8, 3, 2)
    opening(g, "-x", X0, 4, 5, 3, 4)
    return g


@model("supermarket",
       silhouette="Long low beige hall with a raised red sign panel over a glazed entrance canopy, side dock and a striped lot.",
       story="The district supermarket, emptied shelf by shelf in the first fortnight. The "
             "carts are still corralled in the lot and a delivery was never unloaded at the "
             "side dock.",
       details=["Big-box hall with pilaster rhythm, flat roof with HVAC and skylights",
                "Glazed entrance bay under a projecting canopy and a raised blank sign panel",
                "Raised loading dock with two roll-up doors on the camera side",
                "Parking lot with stalls, cart corral and one abandoned car"],
       exclusions=["No readable text or logo"],
       notes=["Footprint 20 x 15 m (GPT reference 17 x 13 m): the lot needs one full row of "
              "5 m stalls plus the side dock to read as a supermarket."])
def supermarket():
    g = Grid(40, 30, 15)
    g.box(0, 0, 0, 39, 29, 0, "asphalt")               # lot 20 x 15 m
    g.box(6, 16, 0, 39, 17, 0, "concrete_hi")          # sidewalk along the front
    stalls(g, 6, 39, 21, 29, every=5)
    g.box(6, 21, 0, 39, 21, 0, "line_white")
    X0, X1, Y0, Y1, ZT = 6, 39, 1, 15, 10
    g.box(X0, Y0, 0, X1, Y1, ZT, "beige")
    g.paint(X0, Y0, 0, X1, Y1, 0, "concrete_dark")
    flat_roof(g, X0, Y0, X1, Y1, ZT + 1, "concrete_hi", "roof")
    for x in (12, 18, 33):                              # pilasters
        g.box(x, Y1 + 1, 1, x, Y1 + 1, ZT, "concrete_hi")
    g.paint(X0, Y1, 1, X1, Y1, 1, "concrete")           # plinth band
    # entrance bay: glass vestibule, canopy and raised sign panel
    storefront(g, "+y", Y1, 20, 31, 1, 5, every=3)
    g.box(23, Y1 + 1, 0, 28, Y1 + 2, 5, "steel_dark")
    g.box(24, Y1 + 2, 1, 27, Y1 + 2, 4, "glass")
    g.box(24, Y1 + 1, 1, 27, Y1 + 1, 4, "glass_dark")
    g.box(19, Y1 + 1, 6, 32, Y1 + 4, 6, "concrete_hi")   # canopy
    g.box(19, Y1 + 4, 1, 19, Y1 + 4, 5, "steel")
    g.box(32, Y1 + 4, 1, 32, Y1 + 4, 5, "steel")
    g.box(20, Y1, ZT + 1, 31, Y1, ZT + 3, "beige")       # raised parapet panel
    g.box(21, Y1, ZT, 30, Y1, ZT + 2, "label_red")
    g.box(22, Y1, ZT + 1, 29, Y1, ZT + 1, "label_cream")
    # loading dock on the -X side
    g.box(1, 3, 0, X0 - 1, 13, 1, "concrete")
    for (a, b) in ((4, 7), (9, 12)):
        opening(g, "-x", X0, a, b, 2, 5, "galv", inset=0)
        g.box(X0 - 1, a - 1, 2, X0 - 1, a - 1, 2, "hazard_yellow_dark")
        g.box(X0 - 1, b + 1, 2, X0 - 1, b + 1, 2, "hazard_yellow_dark")
    g.box(1, 4, 2, 3, 6, 3, "card")                     # unloaded pallets
    g.box(1, 7, 2, 2, 8, 2, "card_dark")
    # roof: HVAC units and skylight strips
    for (x, y) in ((9, 4), (15, 9), (35, 4), (35, 10)):
        hvac(g, x, y, ZT + 1, 3, 2)
    for x in (21, 26, 31):
        g.paint(x, 3, ZT, x + 2, 12, ZT, "glass_hi")
    # cart corral and abandoned car
    g.box(12, 23, 1, 14, 23, 1, "galv")
    g.box(12, 27, 1, 14, 27, 1, "galv")
    g.box(12, 23, 1, 12, 27, 1, "galv")
    g.box(13, 24, 1, 14, 26, 1, "galv_hi")
    car(g, 27, 21, "maroon")
    return g


@model("diner",
       silhouette="Long, low, round-ended steel-and-white body with a maroon stripe, ribbon windows and a framed sign on a roof pole.",
       story="A stainless roadside diner on the county road. Everything was left mid-shift: "
             "the booths are set, the lights are off, the place is otherwise intact.",
       details=["Long low body with a steel skirt, continuous ribbon windows and a maroon "
                "stripe", "Softened roof crown, central glazed vestibule",
                "Blank sign board on a pole above the roof", "Front parking strip"],
       exclusions=["No readable text or logo on the sign"])
def diner():
    g = Grid(22, 16, 13)
    g.box(0, 0, 0, 21, 15, 0, "asphalt")               # lot 11 x 8 m
    g.box(0, 0, 0, 21, 1, 0, "grass")
    g.box(1, 11, 0, 20, 11, 0, "concrete_hi")
    stalls(g, 0, 21, 12, 15, every=5)
    X0, X1, Y0, Y1 = 2, 19, 3, 10
    g.rbox(X0, Y0, 0, X1, Y1, 6, "paint_white", r=1)  # rounded ends
    g.paint(X0, Y0, 0, X1, Y1, 0, "concrete_dark")
    g.paint(X0, Y0, 1, X1, Y1, 2, "chrome")            # steel skirt
    g.paint(X0, Y0, 5, X1, Y1, 5, "maroon")            # stripe
    g.rbox(X0 + 1, Y0 + 1, 7, X1 - 1, Y1 - 1, 7, "steel_light", r=1)   # roof crown
    g.paint(X0, Y0, 6, X1, Y1, 6, "steel_light")
    storefront(g, "+y", Y1, X0 + 1, X1 - 1, 3, 4, every=3)       # ribbon windows
    storefront(g, "-x", X0, Y0 + 1, Y1 - 1, 3, 4, every=3)
    storefront(g, "+x", X1, Y0 + 1, Y1 - 1, 3, 4, every=3)
    # vestibule
    g.box(9, 11, 0, 12, 12, 5, "chrome")
    g.box(9, 11, 5, 12, 12, 5, "maroon")
    opening(g, "+y", 12, 10, 11, 1, 4, "glass")
    g.box(8, 11, 6, 13, 13, 6, "steel_light")
    # roof sign on a pole
    g.box(5, 6, 8, 5, 6, 9, "steel")
    g.box(2, 6, 9, 8, 6, 12, "maroon")
    g.box(3, 6, 10, 7, 6, 11, "label_cream")
    hvac(g, 14, 5, 8, 2, 2)
    opening(g, "-y", Y0, 15, 16, 1, 4, "steel_dark")
    return g


@model("restaurant",
       silhouette="Brick box under a grey side-gable with a small entry gable; one end scorched, timber patio with umbrellas.",
       story="A family restaurant with a timber patio. A kitchen fire burned out the "
             "camera-side end after the staff fled; the patio umbrellas were left open and one "
             "has blown over.",
       details=["Brick walls under a grey side-gable roof with a gabled entry",
                "Fire-scorched end: blackened roof patch, soot over the windows, burnt-out "
                "kitchen door", "Timber patio with planters, two open umbrellas and one "
                "blown over"],
       exclusions=["No readable text", "No furniture beyond umbrellas and planters"])
def restaurant():
    g = Grid(18, 20, 14)
    g.box(0, 0, 0, 17, 19, 0, "grass")                 # lot 9 x 10 m
    g.box(0, 12, 0, 17, 18, 0, "wgrey")                # patio deck
    g.box(7, 12, 0, 10, 19, 0, "concrete_hi")          # entry path
    X0, X1, Y0, Y1 = 1, 16, 1, 11
    g.box(X0, Y0, 0, X1, Y1, 6, "red")
    g.paint(X0, Y0, 0, X1, Y1, 0, "concrete_dark")
    g.paint(X0, Y0, 6, X1, Y1, 6, "red_dark")
    top = gable(g, X0, X1, Y0, Y1, 7, "roof", wall="red", s=2, ov=1)
    # gabled entry vestibule
    g.box(7, 12, 0, 10, 13, 5, "red")
    opening(g, "+y", 13, 8, 9, 1, 4, "glass")
    gable(g, 7, 10, 12, 13, 6, "roof", wall="paint_white", s=1, ov=1, axis="y")
    for x in (3, 12):                                   # tall windows
        opening(g, "+y", Y1, x, x + 2, 2, 4)
    for y in (3, 7):
        opening(g, "+x", X1, y, y + 1, 2, 4)
        opening(g, "-x", X0, y, y + 1, 2, 4, "soot")
    # fire damage on the -X (camera) end
    for y in (3, 7):                                    # soot plumes above the windows
        g.paint(X0, y, 5, X0, y + 1, 6, "char")
        g.paint(X0, y, 7, X0, y + 1, 8, "ash_dark")
    g.paint(X0 - 1, 0, 7, 5, 12, top, "ash_dark")      # scorched roof end
    g.paint(X0 - 1, 1, 8, 3, 11, top, "char")
    g.clear(X0 - 1, 4, top - 1, 2, 8, top)             # ridge burnt through at the gable
    g.paint(X0, 4, top - 2, X0, 8, top - 2, "char")
    g.paint(3, Y1, 5, 5, Y1, 6, "ash_dark")
    opening(g, "+y", Y1, 3, 5, 2, 4, "soot")
    # patio: planter edge, umbrellas
    g.box(0, 18, 1, 6, 18, 1, "wgrey_dark")
    g.box(11, 18, 1, 17, 18, 1, "wgrey_dark")
    g.paint(1, 18, 1, 5, 18, 1, "leaf_mid")
    g.paint(12, 18, 1, 16, 18, 1, "leaf_mid")
    for (x, y, col, hi) in ((13, 15, "sage", "sage_hi"), (3, 15, "cream_mid", "cream_hi")):
        g.box(x, y, 1, x, y, 4, "steel_light")
        g.box(x - 1, y - 1, 4, x + 1, y + 1, 4, col)
        g.set(x, y, 5, hi)
        g.box(x - 1, y, 1, x + 1, y, 1, "wgrey_dark")   # table
    # third umbrella blown over, lying across the deck
    g.box(9, 15, 1, 11, 15, 1, "steel_light")
    g.box(12, 14, 1, 12, 16, 1, "sage_dark")
    return g


@model("fast_food",
       silhouette="Compact box under a projecting terracotta mansard band, wrapped by a drive-through lane, tall empty pole sign.",
       story="A drive-through burger restaurant at the edge of the strip. The drive-through "
             "lane is still marked, the menu board is blank and the tall pole sign has been "
             "dark since the power went.",
       details=["Flat-roofed box with a terracotta mansard band",
                "Drive-through lane wrapping the +X side with a pick-up window canopy and a "
                "blank menu board", "Tall pole sign with a blank dark panel",
                "Glazed front, parking stalls"],
       exclusions=["No readable text or logo"])
def fast_food():
    g = Grid(18, 20, 13)
    g.box(0, 0, 0, 17, 19, 0, "asphalt")               # lot 9 x 10 m
    g.box(0, 0, 0, 17, 1, 0, "grass")
    # drive-through lane: kerbed island around the building on +X and the back
    g.box(1, 2, 0, 14, 3, 0, "asphalt_dark")
    g.box(13, 2, 0, 16, 16, 0, "asphalt_dark")
    g.box(12, 4, 0, 12, 14, 0, "curb")
    g.box(2, 4, 0, 12, 4, 0, "curb")
    g.box(16, 2, 0, 16, 16, 0, "line_yellow")         # lane edge line
    g.box(13, 17, 0, 17, 19, 0, "concrete_hi")        # sign base island
    stalls(g, 0, 10, 16, 19, every=5)
    g.box(1, 15, 0, 11, 15, 0, "concrete_hi")
    X0, X1, Y0, Y1 = 2, 11, 5, 14
    g.box(X0, Y0, 0, X1, Y1, 6, "plaster")
    g.paint(X0, Y0, 0, X1, Y1, 0, "concrete_dark")
    # mansard band: projects one cell at z = 6, steps back at z = 7
    g.box(X0 - 1, Y0 - 1, 6, X1 + 1, Y1 + 1, 6, "terra")
    g.box(X0, Y0, 7, X1, Y1, 7, "terra_dark")
    g.clear(X0 + 1, Y0 + 1, 7, X1 - 1, Y1 - 1, 7)
    g.paint(X0 + 1, Y0 + 1, 6, X1 - 1, Y1 - 1, 6, "roof")
    storefront(g, "+y", Y1, 3, 10, 1, 4, every=3)
    opening(g, "+y", Y1, 5, 6, 1, 4, "glass")
    storefront(g, "-x", X0, 7, 12, 2, 4, every=3)
    # pick-up window and canopy on +X
    opening(g, "+x", X1, 8, 9, 2, 3, "glass")
    g.box(X1 + 1, 7, 5, X1 + 2, 10, 5, "terra_dark")
    # blank menu board beside the lane
    g.box(16, 4, 1, 16, 4, 1, "steel")
    g.box(16, 3, 2, 16, 5, 3, "charcoal")
    hvac(g, 5, 8, 7, 2, 2)
    # tall pole sign, empty frame
    g.box(16, 18, 1, 16, 18, 8, "steel")
    g.box(14, 18, 9, 17, 18, 11, "charcoal")
    g.box(15, 18, 10, 16, 18, 10, "terra")
    return g


@model("hardware_store",
       silhouette="Beige store with a stepped false front and green sign band beside a fenced yard of lumber.",
       story="The town hardware store, stripped of generators, fuel cans and tarps early on. "
             "The lumber yard behind the fence was left nearly full; the gate chain was cut.",
       details=["Flat-roofed store with a stepped false front and a blank green sign band",
                "Glazed front under a metal awning, bagged soil on the sidewalk",
                "Fenced side yard with a lean-to lumber rack, a stacked lumber pile and "
                "plant pallets", "Gate standing open on the street side"],
       exclusions=["No readable text or logo"])
def hardware_store():
    g = Grid(26, 22, 15)
    g.box(0, 0, 0, 25, 21, 0, "asphalt")               # lot 13 x 11 m
    g.box(0, 0, 0, 15, 1, 0, "grass")
    g.box(0, 14, 0, 15, 15, 0, "concrete_hi")
    stalls(g, 0, 15, 17, 21, every=5)
    X0, X1, Y0, Y1 = 1, 15, 2, 13
    g.box(X0, Y0, 0, X1, Y1, 9, "beige")
    g.paint(X0, Y0, 0, X1, Y1, 0, "concrete_dark")
    flat_roof(g, X0, Y0, X1, Y1, 10, "concrete_hi", "roof")
    g.box(X0, Y1, 10, X1, Y1, 12, "beige")             # stepped false front
    g.box(X0 + 3, Y1, 13, X1 - 3, Y1, 13, "beige")
    g.box(X0 + 2, Y1, 9, X1 - 2, Y1, 11, "green_dark")  # blank sign band
    g.box(X0 + 3, Y1, 10, X1 - 3, Y1, 10, "green")
    storefront(g, "+y", Y1, 2, 14, 1, 5, every=3)
    opening(g, "+y", Y1, 7, 9, 1, 4, "glass")
    g.box(X0, Y1 + 1, 6, X1, Y1 + 2, 6, "galv_dark")   # awning
    g.box(2, 14, 1, 4, 15, 1, "khaki")                  # bagged soil
    g.box(2, 14, 2, 3, 15, 2, "khaki_dark")
    g.box(12, 14, 1, 14, 14, 1, "card")
    hvac(g, 4, 4, 10, 3, 2)
    opening(g, "-x", X0, 5, 6, 3, 4)
    # fenced yard on +X
    g.box(16, 2, 0, 25, 17, 0, "gravel")
    fence_line(g, 25, 2, 25, 17, h=3, post="steel_dark", panel="galv_dark", every=3)
    fence_line(g, 16, 2, 25, 2, h=3, post="steel_dark", panel="galv_dark", every=3)
    fence_line(g, 21, 17, 25, 17, h=3, post="steel_dark", panel="galv_dark", every=3)
    g.box(16, 17, 1, 16, 17, 3, "steel_dark")           # gate post
    g.box(16, 18, 1, 16, 20, 3, "galv_dark")            # gate swung open toward the street
    # lean-to lumber rack along the back fence
    for x in (16, 20, 24):
        g.box(x, 6, 1, x, 6, 5, "steel_dark")
    g.box(16, 3, 6, 25, 7, 6, "galv")
    g.box(17, 3, 1, 23, 5, 2, "pine_light")
    g.box(17, 3, 3, 21, 5, 4, "pine_mid")
    g.paint(17, 3, 1, 17, 5, 4, "sawdust")             # end grain
    # stacked lumber bundle and plant pallets in the yard
    g.box(18, 9, 1, 23, 11, 2, "pine_light")
    g.paint(18, 9, 1, 18, 11, 2, "sawdust")
    g.paint(21, 9, 1, 21, 11, 2, "steel_dark")          # strap
    g.box(19, 13, 1, 20, 15, 1, "leaf_mid")
    g.box(22, 13, 1, 23, 15, 1, "leaf")
    return g


@model("lumberyard",
       silhouette="Open metal-roofed saw shed with an inclined conveyor to a sawdust heap, a log pyramid and pale lumber bundles.",
       story="A family sawmill at the edge of the woods. The last log is still on the "
             "carriage under the saw; the yard crew stacked the week's boards and never "
             "came back for them.",
       details=["Open-sided saw shed with a low metal gable roof and a closed back wall",
                "Carriage, log and saw housing inside the shed",
                "Inclined chip conveyor out of the camera-side end onto a sawdust heap",
                "Log deck stacked end-on to the street with pale cut ends",
                "Strapped lumber bundles on a rutted loading area"],
       exclusions=["No vehicles", "No readable text"])
def lumberyard():
    g = Grid(30, 28, 13)
    g.box(0, 0, 0, 29, 27, 0, "gravel")                # yard 15 x 14 m
    g.box(11, 20, 0, 29, 27, 0, "soil")                # rutted loading area
    g.box(1, 11, 0, 11, 19, 0, "sawdust")
    S0, S1, T0, T1 = 12, 28, 8, 19
    g.box(S0, T0, 0, S1, T1, 0, "concrete")
    g.box(S0, T0, 1, S1, T0, 6, "galv")                  # closed back wall
    for x in range(S0, S1 + 1, 4):
        g.paint(x, T0, 1, x, T0, 6, "galv_dark")
        g.box(x, T1, 1, x, T1, 6, "wgrey_dark")          # open front posts
        g.box(x, T0 + 1, 1, x, T0 + 1, 6, "wgrey_dark")
    g.box(S0, T0 + 1, 1, S0, T1, 1, "wgrey_dark")         # sill on the open end
    gable(g, S0, S1, T0, T1, 7, "galv", s=2, ov=1, ridge="galv_hi")
    # saw line
    g.box(13, 13, 1, 27, 14, 1, "steel_dark")
    g.box(15, 13, 2, 21, 14, 2, "bark")
    g.paint(15, 13, 2, 15, 14, 2, "break_fresh")
    g.box(22, 12, 1, 23, 15, 4, "hazard_yellow_dark")
    g.box(22, 12, 4, 23, 15, 4, "steel")
    # chip conveyor rising out of the -X end onto the heap
    for x in range(2, 12):
        z = 2 + (11 - x) // 2
        g.box(x, 15, z, x, 16, z, "black")
        if z > 2:
            g.box(x, 15, z - 1, x, 16, z - 1, "steel_dark")
    for x in (4, 8):
        z = 2 + (11 - x) // 2
        g.box(x, 15, 1, x, 15, z - 1, "steel_dark")
    g.ellipsoid(3.5, 15.5, 0.5, 3.2, 3.0, 4.0, "sawdust", only_empty=True)
    # log deck: logs run along Y so their pale cut ends face the street in a pyramid
    for k, (xa, xb) in enumerate(((1, 9), (2, 8), (3, 7), (4, 6))):
        for x in range(xa, xb + 1):
            col = "bark" if (x + k) % 2 == 0 else "bark_mid"
            g.box(x, 19, 1 + k, x, 26, 1 + k, col)
            end = "break_fresh" if (x + k) % 2 == 0 else "snag_light"
            g.set(x, 26, 1 + k, end)
            g.set(x, 19, 1 + k, end)
    # strapped lumber bundles (boards run along Y; end grain faces the street)
    for x0, h in ((13, 4), (18, 2), (23, 4)):
        g.box(x0, 21, 1, x0 + 3, 25, h, "pine_light")
        g.paint(x0, 25, 1, x0 + 3, 25, h, "sawdust")
        g.paint(x0, 23, 1, x0 + 3, 23, h, "steel_dark")
        if h > 2:
            g.paint(x0, 21, 3, x0 + 3, 25, 3, "pine_mid")
    return g


@model("industrial_warehouse",
       silhouette="Big corrugated front-gabled shed with three tall loading doors (one torn open) and ridge ventilators.",
       story="A distribution warehouse on the industrial estate. Two loading doors are still "
             "locked; the middle one was torn open by a truck that reversed straight through "
             "it.",
       details=["Corrugated steel walls on a concrete base, panel seams every 2 m",
                "Low-pitch front gable with a louvre, ridge ventilators",
                "Three 3 m loading doors, the middle one torn open with its panel hanging",
                "Clerestory windows, yellow bollards, a skip on the apron"],
       exclusions=["No readable text or logo"])
def industrial_warehouse():
    g = Grid(36, 28, 21)
    g.box(0, 0, 0, 35, 27, 0, "concrete")              # apron 18 x 14 m
    g.box(0, 0, 0, 35, 1, 0, "gravel")
    X0, X1, Y0, Y1 = 1, 34, 2, 21
    g.box(X0, Y0, 0, X1, Y1, 13, "galv")
    g.paint(X0, Y0, 0, X1, Y1, 0, "concrete_dark")
    g.paint(X0, Y0, 1, X1, Y1, 2, "concrete")
    for x in range(X0 + 4, X1, 4):
        g.paint(x, Y0, 3, x, Y0, 13, "galv_dark")
        g.paint(x, Y1, 3, x, Y1, 13, "galv_dark")
    for y in range(Y0 + 4, Y1, 4):
        g.paint(X0, y, 3, X0, y, 13, "galv_dark")
        g.paint(X1, y, 3, X1, y, 13, "galv_dark")
    top = gable(g, X0, X1, Y0, Y1, 14, "roof_hi", wall="galv", s=3, ov=1, axis="y")
    for y in (5, 10, 15, 20):                           # ridge ventilators
        g.box(17, y, top + 1, 18, y, top + 1, "galv_hi")
    opening(g, "+y", Y1, 15, 20, top - 3, top - 2, "steel_dark", inset=0)   # gable louvre
    # loading doors
    for x0 in (3, 27):
        opening(g, "+y", Y1, x0, x0 + 5, 1, 6, "galv_hi", inset=0)
        g.paint(x0, Y1, 6, x0 + 5, Y1, 6, "steel")
        g.box(x0 - 1, Y1 + 1, 1, x0 - 1, Y1 + 1, 2, "hazard_yellow_dark")
        g.box(x0 + 6, Y1 + 1, 1, x0 + 6, Y1 + 1, 2, "hazard_yellow_dark")
    opening(g, "+y", Y1, 15, 20, 1, 6, "black")          # torn-open middle door
    g.box(15, Y1, 5, 20, Y1, 6, "galv_hi")
    g.box(15, Y1 + 1, 3, 16, Y1 + 1, 4, "galv_hi")        # bent corner hanging out
    g.box(13, Y1 + 1, 1, 13, Y1 + 1, 2, "hazard_yellow_dark")
    opening(g, "+y", Y1, 10, 11, 1, 4, "steel_dark")     # personnel door
    # clerestory windows
    for x in range(X0 + 2, X1 - 1, 4):
        opening(g, "-y", Y0, x, x + 1, 10, 11)
    for y in range(Y0 + 2, Y1 - 1, 4):
        opening(g, "-x", X0, y, y + 1, 10, 11)
        opening(g, "+x", X1, y, y + 1, 10, 11)
    opening(g, "-x", X0, 16, 17, 1, 4, "steel_dark")
    g.box(29, 23, 1, 32, 25, 2, "green_dark")            # skip
    g.paint(29, 23, 2, 32, 25, 2, "green")
    return g


@model("scrapyard_building",
       silhouette="Patchwork sheet-metal enclosure with stacked car hulks, a yellow mast-and-jib crane and a yellow office cabin.",
       story="A salvage yard behind a wall of patched sheet metal. The crane still holds its "
             "magnet over the stack it was sorting; the office door was kicked in for the "
             "cash box.",
       details=["Patchwork fence of salvaged sheets, rolling gate pushed aside",
                "Portable office cabin on blocks with an overhanging roof",
                "Two stacks of flattened car hulks and one intact wreck",
                "Tracked material handler with a raised boom and hanging magnet"],
       exclusions=["No readable text or logo", "No branded vehicles"])
def scrapyard_building():
    g = Grid(26, 20, 16)
    g.box(0, 0, 0, 25, 19, 0, "gravel")                # yard 13 x 10 m
    g.box(4, 6, 0, 9, 12, 0, "soil_dark")               # oily work area under the crane
    # patchwork sheet fence: back and both sides
    sheets = ["galv_dark", "rust_dark", "galv", "rust_deep", "steel"]
    for x in range(0, 26):
        g.box(x, 0, 1, x, 0, 4, sheets[(x // 3) % 5])
    for y in range(1, 16):
        g.box(0, y, 1, 0, y, 4, sheets[(y // 3 + 1) % 5])
        g.box(25, y, 1, 25, y, 4, sheets[(y // 3 + 3) % 5])
    g.box(1, 16, 1, 7, 16, 3, "mesh")                    # rolling gate pushed aside
    g.box(0, 16, 1, 0, 16, 4, "steel_dark")
    # wreck stacks along the back fence
    hulls = ["rust_dark", "navy_dark", "maroon_dark", "beige_dark", "rust_deep"]
    for k in range(4):
        dx = (0, 1, 0, -1)[k]
        g.box(2 + dx, 1, 1 + k, 9 + dx, 4, 1 + k, hulls[k])
        g.paint(2 + dx, 4, 1 + k, 2 + dx, 4, 1 + k, "rust")
    for k in range(3):
        dx = (0, -1, 1)[k]
        g.box(12 + dx, 1, 1 + k, 19 + dx, 4, 1 + k, hulls[k + 2])
        g.paint(19 + dx, 4, 1 + k, 19 + dx, 4, 1 + k, "rust_dark")
    car(g, 13, 6, "teal_dark", axis="x")                # waiting wreck
    g.paint(13, 6, 2, 15, 9, 2, "rust")
    # office cabin on blocks
    g.box(16, 12, 1, 23, 15, 5, "siding_yellow")
    g.box(16, 12, 1, 23, 15, 1, "concrete_dark")
    g.box(15, 11, 6, 24, 16, 6, "galv")
    opening(g, "+y", 15, 18, 19, 2, 4, "black")          # door kicked in
    opening(g, "+y", 15, 21, 22, 3, 4)
    opening(g, "-x", 16, 13, 14, 3, 4)
    g.box(18, 16, 1, 19, 16, 1, "wgrey_dark")
    # slewing scrap crane on a tracked base: mast, horizontal jib, cable and magnet
    g.box(3, 8, 1, 8, 8, 1, "black")
    g.box(3, 12, 1, 8, 12, 1, "black")
    g.box(3, 9, 1, 8, 11, 2, "hazard_yellow_dark")
    g.box(5, 9, 3, 6, 11, 11, "hazard_yellow_dark")      # mast
    for z in (5, 8):
        g.paint(5, 9, z, 6, 11, z, "hazard_yellow")        # lattice bands
    g.box(4, 10, 3, 4, 11, 5, "hazard_yellow_dark")        # cab beside the mast
    g.box(3, 10, 4, 3, 11, 5, "glass_dark")
    g.box(5, 2, 12, 6, 14, 12, "hazard_yellow_dark")      # jib over the back stack
    g.box(5, 12, 11, 6, 14, 11, "charcoal")                # counterweight
    g.box(5, 3, 9, 5, 3, 11, "steel_dark")                 # cable
    g.box(4, 2, 7, 6, 4, 8, "charcoal")                    # magnet
    g.paint(4, 2, 8, 6, 4, 8, "iron_edge")
    return g


@model("gun_shop",
       silhouette="Banded concrete-block box with barred windows, dark sign band and a sandbag chicane at the door.",
       story="An independent gun shop in a strip of small units. The owner barred everything "
             "that opened, sandbagged a chicane at the door and held out for a week before "
             "the shop went dark.",
       details=["Concrete-block box with a dark blank sign band", "Two barred shopfront "
                "windows and a steel door under a roll-down shutter box",
                "Sandbag chicane in front of the door", "Flat roof with parapet"],
       exclusions=["No readable text, logo or weapon silhouettes"])
def gun_shop():
    g = Grid(16, 18, 11)
    g.box(0, 0, 0, 15, 17, 0, "asphalt")               # lot 8 x 9 m
    g.box(0, 12, 0, 15, 13, 0, "concrete_hi")
    stalls(g, 0, 15, 14, 17, every=5)
    X0, X1, Y0, Y1 = 1, 14, 1, 11
    g.box(X0, Y0, 0, X1, Y1, 8, "concrete")
    g.paint(X0, Y0, 0, X1, Y1, 0, "concrete_dark")
    g.paint(X0, Y0, 1, X1, Y1, 1, "concrete_dark")
    for z in (3, 5, 7):                                  # block coursing bands
        g.paint(X0, Y0, z, X1, Y1, z, "concrete_hi")
    flat_roof(g, X0, Y0, X1, Y1, 9, "concrete_hi", "roof")
    g.box(X0 + 1, Y1, 6, X1 - 1, Y1, 7, "charcoal")     # blank sign band
    g.box(X0 + 2, Y1, 6, X1 - 2, Y1, 6, "olive_dark")
    for (a, b) in ((2, 6), (9, 13)):                     # barred windows
        opening(g, "+y", Y1, a, b, 2, 4, "glass_dark")
        for x in range(a + 1, b, 2):
            g.box(x, Y1, 2, x, Y1, 4, "steel_light")
    opening(g, "+y", Y1, 7, 8, 1, 4, "charcoal")        # steel door
    g.box(6, Y1 + 1, 5, 9, Y1 + 1, 5, "galv")            # shutter box
    opening(g, "-x", X0, 4, 6, 3, 4, "glass_dark")
    g.box(X0, 5, 3, X0, 5, 4, "steel_light")
    sandbags(g, 4, 14, 9, 14, h=2)                       # chicane
    sandbags(g, 4, 12, 4, 13, h=2)
    hvac(g, 9, 3, 9, 2, 2)
    return g


@model("shooting_range",
       silhouette="Low timber clubhouse beside a covered firing line, lanes with paper targets and a tall earth berm behind.",
       story="A members' outdoor range with a timber clubhouse. Targets are still pinned up "
             "from the last practice; the range became a meeting point, then a place to avoid.",
       details=["Low timber clubhouse with a grey gable roof",
                "Covered firing line with benches under a lean-to roof",
                "Four gravel lanes with short baffles and paper target frames",
                "Stepped 4.5 m earth backstop berm with a bare impact face"],
       exclusions=["No readable text", "No weapons or people"])
def shooting_range():
    g = Grid(32, 22, 12)
    g.box(0, 0, 0, 31, 21, 0, "grass")                 # site 16 x 11 m
    g.box(1, 4, 0, 17, 11, 0, "gravel")                 # lanes
    g.box(18, 17, 0, 31, 21, 0, "gravel")               # parking
    # backstop berm (impact face toward the firing line, +Y)
    for (y, zt, col) in ((0, 8, "grass"), (1, 7, "grass"), (2, 6, "soil"), (3, 4, "soil")):
        g.box(0, y, 1, 19, y, zt, "soil")
        g.paint(0, y, zt, 19, y, zt, col)
    g.box(0, 4, 1, 0, 11, 2, "grass")                    # low side berm
    # target frames, one per lane
    for x in (2, 6, 10, 14):
        g.box(x + 1, 6, 1, x + 1, 6, 1, "pine_dark")       # stand legs
        g.box(x + 2, 6, 1, x + 2, 6, 1, "pine_dark")
        g.box(x + 1, 6, 2, x + 2, 6, 3, "paper")
        g.box(x + 1, 6, 4, x + 2, 6, 4, "pine_dark")
    for x in (5, 9, 13):                                 # short baffles
        g.box(x, 9, 1, x, 11, 1, "wgrey_dark")
    # covered firing line
    g.box(1, 12, 0, 17, 15, 0, "concrete")
    for x in (1, 5, 9, 13, 17):
        g.box(x, 15, 1, x, 15, 4, "wgrey_dark")
        g.box(x, 12, 1, x, 12, 4, "wgrey_dark")
    g.box(1, 15, 1, 17, 15, 2, "wgrey")                  # back safety wall
    g.box(0, 12, 5, 17, 16, 5, "galv")
    for x in (2, 6, 10, 14):
        g.box(x, 13, 1, x + 2, 13, 1, "wgrey_dark")      # benches
    # clubhouse
    X0, X1, Y0, Y1 = 18, 30, 11, 17
    g.box(X0, Y0, 0, X1, Y1, 5, "wgrey")
    g.paint(X0, Y0, 0, X1, Y1, 0, "concrete_dark")
    gable(g, X0, X1, Y0, Y1, 6, "roof", wall="wgrey", s=1, ov=1)
    opening(g, "+y", Y1, 23, 24, 1, 4, "wood_stain")
    for x in (20, 27):
        opening(g, "+y", Y1, x, x + 1, 2, 3)
    opening(g, "-y", Y0, 21, 22, 2, 3)
    opening(g, "+x", X1, 13, 14, 2, 3)
    g.box(22, 18, 0, 25, 18, 0, "concrete_hi")
    return g


@model("police_station",
       silhouette="Two-storey brick block with a navy band, navy entrance canopy, flagpole and two white cruisers.",
       story="The district police station, the last place in town with lights on. The cruisers "
             "are parked in their bays and the flag is still up, faded; nobody answered the "
             "front desk after the third day.",
       details=["Two-storey brick block with a navy band under the parapet",
                "Projecting entrance bay with a canopy on two columns",
                "Flagpole with a plain two-band flag, lattice radio mast on the roof",
                "Two patrol cars with unlit light bars in marked bays"],
       exclusions=["No readable text, badge or real department markings"])
def police_station():
    g = Grid(32, 24, 19)
    g.box(0, 0, 0, 31, 23, 0, "asphalt")               # lot 16 x 12 m
    g.box(10, 14, 0, 31, 23, 0, "grass")
    g.box(10, 14, 0, 31, 15, 0, "concrete_hi")
    g.box(19, 16, 0, 22, 23, 0, "concrete_hi")          # entrance walk
    X0, X1, Y0, Y1 = 10, 31, 2, 13
    g.box(X0, Y0, 0, X1, Y1, 12, "red")
    g.paint(X0, Y0, 0, X1, Y1, 0, "concrete_dark")
    g.paint(X0, Y0, 6, X1, Y1, 6, "concrete_hi")        # floor band
    g.paint(X0, Y0, 11, X1, Y1, 12, "navy")
    flat_roof(g, X0, Y0, X1, Y1, 13, "concrete_hi", "roof")
    for x in (11, 14, 17, 23, 26, 29):
        opening(g, "+y", Y1, x, x + 1, 3, 4)
    for x in (11, 14, 17, 20, 23, 26, 29):
        opening(g, "+y", Y1, x, x + 1, 8, 9)
    for y in (4, 9):
        opening(g, "-x", X0, y, y + 1, 3, 4)
        opening(g, "-x", X0, y, y + 1, 8, 9)
    for x in (12, 18, 24, 28):
        opening(g, "-y", Y0, x, x + 1, 3, 4)
        opening(g, "-y", Y0, x, x + 1, 8, 9)
    # entrance bay and canopy
    g.box(18, 14, 0, 23, 15, 6, "concrete_hi")
    storefront(g, "+y", 15, 18, 23, 1, 4, every=5, mull="concrete_hi")
    g.box(17, 14, 7, 24, 17, 7, "navy")
    g.box(17, 17, 1, 17, 17, 6, "concrete_hi")
    g.box(24, 17, 1, 24, 17, 6, "concrete_hi")
    # roof: radio mast, HVAC
    g.box(28, 5, 13, 28, 5, 18, "steel_dark")             # radio mast
    g.box(28, 6, 16, 28, 6, 17, "galv_hi")                 # panel antenna
    g.box(27, 4, 14, 28, 4, 15, "galv")                    # dish
    hvac(g, 13, 5, 13, 3, 3)
    hvac(g, 21, 5, 13, 2, 2)
    flagpole(g, 10, 21, 16)
    # cruiser bays on the camera side
    stalls(g, 0, 10, 2, 11, every=5)
    for x0 in (1, 6):
        car(g, x0, 2, "paint_white")
        g.paint(x0, 5, 1, x0 + 3, 7, 2, "navy")          # navy doors
        g.box(x0, 6, 4, x0 + 1, 6, 4, "lamp_red")         # unlit light bar
        g.box(x0 + 2, 6, 4, x0 + 3, 6, 4, "lamp_blue")
    return g


@model("clinic",
       silhouette="Single-storey white clinic with a raised entrance tower carrying a red cross and a side ambulance canopy.",
       story="The walk-in medical clinic where people queued for days after the sirens stopped. "
             "The ambulance under the canopy never left; the doors are chained from inside.",
       details=["Single-storey flat-roofed clinic with a raised entrance tower",
                "White sign panel with a red cross on the tower",
                "Ambulance canopy on two posts over the side bay, ambulance parked under it",
                "Front parking stalls and a kerbed walk"],
       exclusions=["No readable text or real-organisation emblems"])
def clinic():
    g = Grid(22, 22, 13)
    g.box(0, 0, 0, 21, 21, 0, "asphalt")               # lot 11 x 11 m
    g.box(7, 15, 0, 21, 16, 0, "concrete_hi")
    stalls(g, 8, 21, 17, 21, every=5)
    X0, X1, Y0, Y1 = 7, 20, 2, 13
    g.box(X0, Y0, 0, X1, Y1, 7, "plaster")
    g.paint(X0, Y0, 0, X1, Y1, 0, "concrete_dark")
    g.paint(X0, Y0, 7, X1, Y1, 7, "bluegrey")
    flat_roof(g, X0, Y0, X1, Y1, 8, "concrete_hi", "roof")
    # entrance tower with the cross panel
    g.box(10, 12, 0, 16, 14, 10, "plaster")
    g.box(10, 12, 11, 16, 14, 11, "concrete_hi")
    g.box(11, 14, 6, 15, 14, 10, "paint_white")
    cross_y(g, 13, 14, 8, arm=1, half=1)
    opening(g, "+y", 14, 12, 14, 1, 4, "glass")
    g.box(10, 15, 5, 16, 16, 5, "concrete_hi")
    for x in (8, 18):
        opening(g, "+y", Y1, x, x + 1, 3, 4)
    for y in (4, 9):
        opening(g, "+x", X1, y, y + 1, 3, 4)
    # ambulance canopy on -X with the doors under it
    g.box(0, 3, 6, X0 - 1, 12, 6, "concrete_hi")
    g.box(0, 3, 1, 0, 3, 5, "steel")
    g.box(0, 12, 1, 0, 12, 5, "steel")
    opening(g, "-x", X0, 6, 8, 1, 4, "glass")
    g.box(1, 13, 0, 6, 21, 0, "asphalt_dark")            # ambulance lane
    # ambulance (nose +Y)
    g.box(2, 4, 1, 5, 9, 4, "paint_white")
    g.box(2, 10, 1, 5, 12, 3, "paint_white")
    g.paint(2, 10, 3, 5, 12, 3, "glass_dark")
    g.paint(2, 10, 3, 5, 11, 3, "paint_white")
    g.paint(2, 4, 1, 5, 12, 1, "black")
    g.paint(2, 4, 2, 5, 12, 2, "signal_red")
    g.box(2, 9, 5, 5, 9, 5, "lamp_red")
    hvac(g, 15, 4, 8, 3, 2)
    return g


@model("pharmacy",
       silhouette="Brick corner shop with a recessed corner door, green awnings and a projecting white blade sign with a green cross.",
       story="A corner pharmacy on the high street, the first shop people broke into. The "
             "corner doors were forced and the shelves cleared; the green cross still hangs "
             "over the pavement.",
       details=["Brick corner building with a stone cornice and flat roof",
                "Recessed corner entrance behind a single column",
                "Shopfront glazing on both street faces under dark green awnings",
                "Projecting blade sign: green cross on a white panel"],
       exclusions=["No readable text or real-chain branding"])
def pharmacy():
    g = Grid(16, 19, 12)
    g.box(0, 0, 0, 15, 18, 0, "asphalt")               # corner lot 8 x 9.5 m
    g.box(0, 0, 0, 1, 18, 0, "concrete_hi")             # pavements on the two street sides
    g.box(0, 14, 0, 15, 18, 0, "concrete_hi")
    g.box(0, 18, 0, 15, 18, 0, "curb")
    g.box(0, 0, 0, 0, 18, 0, "curb")
    X0, X1, Y0, Y1 = 2, 14, 1, 13
    g.box(X0, Y0, 0, X1, Y1, 8, "red")
    g.paint(X0, Y0, 0, X1, Y1, 0, "concrete_dark")
    g.paint(X0, Y0, 8, X1, Y1, 8, "concrete_hi")        # cornice
    flat_roof(g, X0, Y0, X1, Y1, 9, "concrete_hi", "roof")
    storefront(g, "+y", Y1, 6, 13, 1, 5, every=4)
    storefront(g, "-x", X0, 2, 9, 1, 5, every=4)
    g.box(6, Y1 + 1, 6, 13, Y1 + 1, 6, "green_dark")    # awnings
    g.box(X0 - 1, 2, 6, X0 - 1, 9, 6, "green_dark")
    # recessed corner entrance behind a single column
    g.clear(X0, Y1 - 2, 1, X0 + 2, Y1, 5)
    g.box(X0, Y1, 1, X0, Y1, 5, "concrete_hi")
    g.paint(X0, Y1 - 3, 1, X0 + 2, Y1 - 3, 5, "glass_dark")
    g.paint(X0 + 3, Y1 - 2, 1, X0 + 3, Y1, 5, "glass")
    g.box(X0, Y1 - 2, 0, X0 + 2, Y1, 0, "concrete_hi")
    # blade sign: white panel with a green cross, projecting over the pavement
    g.box(X0, Y1 + 1, 6, X0, Y1 + 5, 10, "paint_white")
    g.box(X0, Y1 + 2, 7, X0, Y1 + 4, 9, "paint_white")
    g.box(X0, Y1 + 3, 7, X0, Y1 + 3, 9, "label_green")
    g.box(X0, Y1 + 2, 8, X0, Y1 + 4, 8, "label_green")
    hvac(g, 9, 3, 9, 3, 2)
    opening(g, "+x", X1, 4, 5, 3, 4)
    return g


@model("veterinary_clinic",
       silhouette="Sage front-gabled building with a white entrance canopy and a fenced dog run with a red-roofed dog house.",
       story="A small-town vet in a converted house. Before leaving, the staff opened the "
             "kennels and the dog-run gate so the boarders could fend for themselves.",
       details=["Sage-sided building with a 45-degree front gable and entrance canopy",
                "Fenced gravel dog run on the camera side with a red-roofed dog house",
                "Dog-run gate standing open", "Two parking stalls and a low blank sign"],
       exclusions=["No readable text, paw logos or animals"])
def veterinary_clinic():
    g = Grid(20, 20, 15)
    g.box(0, 0, 0, 19, 19, 0, "grass")                 # lot 10 x 10 m
    g.box(7, 15, 0, 19, 19, 0, "asphalt")
    stalls(g, 9, 19, 16, 19, every=5)
    g.box(11, 13, 0, 14, 19, 0, "concrete_hi")
    X0, X1, Y0, Y1 = 7, 18, 2, 12
    g.box(X0, Y0, 0, X1, Y1, 6, "siding_sage")
    g.paint(X0, Y0, 0, X1, Y1, 0, "concrete_dark")
    gable(g, X0, X1, Y0, Y1, 7, "roof", wall="siding_sage", s=1, ov=1, axis="y")
    opening(g, "+y", Y1, 12, 13, 1, 4, "glass")
    for x in (8, 16):
        opening(g, "+y", Y1, x, x + 1, 3, 4)
    opening(g, "+y", Y1, 12, 13, 9, 10)
    for y in (4, 8):
        opening(g, "+x", X1, y, y + 1, 3, 4)
    opening(g, "-x", X0, 9, 10, 3, 4)
    opening(g, "-x", X0, 5, 6, 1, 4, "wood_stain")      # door to the run
    g.box(10, 13, 5, 15, 14, 5, "paint_white")          # entrance canopy
    g.box(10, 14, 1, 10, 14, 4, "steel_light")
    g.box(15, 14, 1, 15, 14, 4, "steel_light")
    g.box(16, 18, 1, 18, 18, 2, "concrete_hi")          # low blank sign
    g.box(16, 18, 2, 18, 18, 2, "label_blue")
    # dog run on the -X side
    g.box(0, 2, 0, 6, 14, 0, "gravel")
    fence_line(g, 0, 2, 0, 14, h=2, post="steel_dark", panel="galv_dark", every=3)
    fence_line(g, 0, 2, 6, 2, h=2, post="steel_dark", panel="galv_dark", every=3)
    fence_line(g, 0, 14, 1, 14, h=2, post="steel_dark", panel="galv_dark", every=3)
    fence_line(g, 5, 14, 6, 14, h=2, post="steel_dark", panel="galv_dark", every=3)
    g.box(4, 14, 1, 4, 14, 3, "steel_dark")               # gate post, gate swung out
    g.box(4, 15, 1, 4, 17, 2, "galv_dark")
    g.box(1, 4, 1, 3, 6, 2, "wgrey_warm")                # dog house
    gable(g, 1, 3, 4, 6, 3, "red_dark", wall="wgrey_warm", s=1, ov=0, axis="x")
    opening(g, "+y", 6, 2, 2, 1, 1, "black", inset=0)
    return g


@model("hospital",
       silhouette="Four-storey glazed tower with a red-cross panel and rooftop helipad ring, flanked by two-storey wings.",
       story="The regional hospital, overwhelmed in the first week and evacuated by "
             "helicopter in the second. The ambulances were left under the emergency canopy.",
       details=["Four-storey main tower with glazed ribbon windows and a rooftop helipad "
                "(white ring, red cross)", "Large red cross on a white panel on the tower's "
                "top storey", "Two-storey wings; emergency canopy with an ambulance on the "
                "camera-side wing", "Glazed main entrance, drop-off lot with stalls"],
       exclusions=["No readable text, H marking or real-organisation emblems"],
       notes=["Footprint 20 x 18 m (GPT reference 18 x 16 m): a 7 m helipad ring needs an "
              "8 x 8 m tower roof, and the wings need room for the emergency canopy."])
def hospital():
    g = Grid(40, 36, 27)
    g.box(0, 0, 0, 39, 35, 0, "asphalt")               # site 20 x 18 m
    g.box(0, 0, 0, 39, 1, 0, "grass")
    g.box(13, 23, 0, 39, 26, 0, "concrete_hi")          # entrance plaza and walk
    stalls(g, 24, 39, 28, 35, every=5)
    # wings (two storeys)
    for (a, b, c, d) in ((1, 12, 9, 25), (29, 38, 9, 21)):
        g.box(a, c, 0, b, d, 12, "plaster")
        g.paint(a, c, 0, b, d, 0, "concrete_dark")
        g.paint(a, c, 6, b, d, 6, "concrete_hi")
        flat_roof(g, a, c, b, d, 13, "concrete_hi", "roof")
    for x in (2, 5, 8):
        opening(g, "+y", 25, x, x + 1, 9, 10)
    for y in (11, 14, 17, 20, 23):
        opening(g, "-x", 1, y, y + 1, 3, 4)
        opening(g, "-x", 1, y, y + 1, 9, 10)
    for x in (30, 33, 36):
        opening(g, "+y", 21, x, x + 1, 3, 4)
        opening(g, "+y", 21, x, x + 1, 9, 10)
    for y in (11, 15, 19):
        opening(g, "+x", 38, y, y + 1, 3, 4)
        opening(g, "+x", 38, y, y + 1, 9, 10)
    hvac(g, 4, 11, 13, 3, 3)
    hvac(g, 32, 12, 13, 3, 2)
    hvac(g, 32, 16, 13, 2, 2)
    # emergency doors and canopy on the west wing front
    opening(g, "+y", 25, 3, 8, 1, 4, "glass")
    g.box(0, 26, 6, 12, 31, 6, "concrete_hi")
    g.paint(0, 26, 6, 12, 31, 6, "concrete_hi")
    g.box(0, 31, 7, 12, 31, 7, "signal_red_dark")
    for x in (0, 12):
        g.box(x, 31, 1, x, 31, 5, "steel")
    g.box(0, 26, 0, 12, 35, 0, "asphalt_dark")
    g.box(4, 26, 1, 7, 31, 4, "paint_white")            # ambulance, nose +Y
    g.box(4, 32, 1, 7, 34, 3, "paint_white")
    g.paint(4, 26, 1, 7, 34, 1, "black")
    g.paint(4, 26, 2, 7, 34, 2, "signal_red")
    g.paint(4, 34, 3, 7, 34, 3, "glass_dark")
    # main tower (four storeys)
    T0, T1, U0, U1, ZT = 13, 28, 7, 22, 24
    g.box(T0, U0, 0, T1, U1, ZT, "plaster")
    g.paint(T0, U0, 0, T1, U1, 0, "concrete_dark")
    for i in range(1, 4):
        g.paint(T0, U0, 6 * i, T1, U1, 6 * i, "concrete_hi")
    flat_roof(g, T0, U0, T1, U1, ZT + 1, "concrete_hi", "concrete")
    for i in range(4):
        z = 6 * i + 2
        storefront(g, "+y", U1, T0 + 1, T1 - 1, z, z + 2, every=3, mull="concrete_hi")
        storefront(g, "-x", T0, U0 + 1, U1 - 1, z, z + 2, every=3, mull="concrete_hi")
        storefront(g, "+x", T1, U0 + 1, U1 - 1, z, z + 2, every=3, mull="concrete_hi")
        storefront(g, "-y", U0, T0 + 1, T1 - 1, z, z + 2, every=3, mull="concrete_hi")
    g.box(17, U1, 16, 24, U1, ZT, "paint_white")         # cross panel
    cross_y(g, 21, U1, 20, arm=2, half=1)
    # helipad on the tower roof: white ring, red cross
    for (i, j) in g.ring_cells(21.0, 15.0, 6.2):
        g.paint(i, j, ZT, i, j, ZT, "line_white")
    g.paint(20, 12, ZT, 21, 17, ZT, "signal_red")
    g.paint(18, 14, ZT, 23, 15, ZT, "signal_red")
    # main entrance
    g.box(18, U1 + 1, 0, 23, U1 + 2, 5, "steel_dark")
    g.box(19, U1 + 2, 1, 22, U1 + 2, 4, "glass")
    g.box(16, U1 + 1, 6, 25, U1 + 4, 6, "concrete_hi")
    g.box(16, U1 + 4, 1, 16, U1 + 4, 5, "steel")
    g.box(25, U1 + 4, 1, 25, U1 + 4, 5, "steel")
    return g


@model("military_outpost",
       silhouette="Square ring of tan barrier baskets around prefab barracks, olive tents, a truck and a thin radio mast.",
       story="A forward checkpoint compound thrown up to hold the county road. The unit pulled "
             "out in a hurry: the boom is down, the tents still pitched and one truck left "
             "behind.",
       details=["Perimeter of 1 m sand-filled barrier baskets with a boom gate and a "
                "sandbagged guard post", "Two prefab barrack units with a radio mast",
                "Two olive ridge tents on the camera side", "Utility truck and fuel drums"],
       exclusions=["No readable text, insignia or real-army markings"])
def military_outpost():
    g = Grid(28, 28, 16)
    g.box(0, 0, 0, 27, 27, 0, "gravel")                # compound 14 x 14 m
    g.box(10, 18, 0, 17, 27, 0, "soil")                 # rutted track from the gate

    def basket(x, y):
        col = "khaki" if (x // 2 + y // 2) % 2 == 0 else "khaki_dark"
        g.box(x, y, 1, x + 1, y + 1, 2, col)
        g.paint(x, y, 2, x + 1, y + 1, 2, "card_dark")

    for x in range(0, 28, 2):
        basket(x, 0)
        if not 12 <= x <= 15:
            basket(x, 26)
    for y in range(2, 26, 2):
        basket(0, y)
        basket(26, y)
    for x in range(12, 16):                              # boom gate, down
        g.set(x, 27, 2, "paint_white" if (x // 2) % 2 == 0 else "signal_red_dark")
    sandbags(g, 18, 22, 20, 24, h=2)                     # guard post
    g.clear(19, 23, 1, 19, 23, 2)
    g.box(18, 22, 3, 18, 22, 3, "olive_dark")
    g.box(20, 24, 3, 20, 24, 3, "olive_dark")
    g.box(17, 21, 4, 21, 25, 4, "olive_dark")
    # prefab barrack units along the back
    for (a, b) in ((3, 10), (15, 23)):
        g.box(a, 3, 1, b, 7, 5, "olive")
        g.paint(a, 3, 1, b, 7, 1, "olive_dark")
        for x in range(a + 2, b, 3):
            g.paint(x, 7, 2, x, 7, 5, "olive_dark")
        g.box(a - 1, 2, 6, b + 1, 8, 6, "galv_dark")
        opening(g, "+y", 7, a + 4, a + 5, 1, 4, "olive_dark")
        opening(g, "+y", 7, a + 1, a + 2, 3, 4)
        opening(g, "+y", 7, b - 2, b - 1, 3, 4)
    g.box(12, 5, 1, 13, 6, 2, "olive_dark")             # radio set at the mast foot
    g.box(13, 5, 3, 13, 5, 15, "steel_dark")             # radio mast
    g.box(13, 6, 14, 13, 6, 15, "steel_light")           # whip antenna head
    # ridge tents on the camera side
    for (y0, y1) in ((11, 16), (18, 23)):
        g.box(3, y0, 1, 8, y1, 1, "olive_dark")
        gable(g, 3, 8, y0, y1, 2, "olive", wall="olive_dark", s=1, ov=0, axis="y")
        opening(g, "+y", y1, 5, 6, 1, 2, "black")
    # utility truck and fuel drums
    car(g, 14, 11, "olive_dark")
    g.box(14, 11, 2, 17, 14, 3, "olive")                 # cargo box behind the cab
    g.box(21, 14, 1, 22, 15, 2, "green_dark")
    g.box(23, 14, 1, 23, 14, 2, "green_dark")
    g.paint(21, 14, 2, 23, 15, 2, "green")
    return g


@model("guard_tower",
       silhouette="Tall braced timber stilt frame carrying a box cabin with an open window band and a pyramid metal roof.",
       story="A timber watchtower over a perimeter road. The last guard climbed down and "
             "never came back; the searchlight still points at the gate.",
       details=["Four timber legs with girts and diagonal braces",
                "Cabin with a solid lower wall, open window band and corner posts",
                "Galvanised pyramid roof, timber ladder on the street side",
                "Searchlight on the front corner"],
       exclusions=["No readable text"])
def guard_tower():
    g = Grid(8, 8, 21)
    legs = (1, 6)
    for x in legs:
        for y in legs:
            g.box(x, y, 0, x, y, 11, "wgrey_dark")
    for z in (5, 11):                                     # girts
        g.box(1, 1, z, 6, 1, z, "wgrey_mid")
        g.box(1, 6, z, 6, 6, z, "wgrey_mid")
        g.box(1, 1, z, 1, 6, z, "wgrey_mid")
        g.box(6, 1, z, 6, 6, z, "wgrey_mid")
    for (p0, p1) in (((1, 1, 0), (6, 1, 5)), ((6, 6, 0), (1, 6, 5)),
                     ((1, 6, 0), (1, 1, 5)), ((6, 1, 0), (6, 6, 5)),
                     ((6, 1, 5), (1, 1, 11)), ((1, 6, 5), (6, 6, 11)),
                     ((1, 1, 5), (1, 6, 11)), ((6, 6, 5), (6, 1, 11))):
        g.line(p0, p1, "wgrey_mid")
    # cabin
    g.box(0, 0, 12, 7, 7, 12, "wgrey_dark")               # floor
    g.box(0, 0, 13, 7, 7, 14, "wgrey")                    # solid lower wall
    g.clear(1, 1, 13, 6, 6, 14)
    for x in (0, 7):
        for y in (0, 7):
            g.box(x, y, 15, x, y, 16, "wgrey_dark")        # corner posts
    g.box(0, 0, 17, 7, 7, 17, "galv")                     # pyramid roof
    g.box(1, 1, 18, 6, 6, 18, "galv")
    g.box(2, 2, 19, 5, 5, 19, "galv")
    g.box(3, 3, 20, 4, 4, 20, "galv_hi")
    g.box(1, 1, 12, 6, 6, 12, "wgrey_dark")
    # ladder on the street side up to the hatch
    for z in range(0, 12):
        g.set(4, 7, z, "wgrey_hi" if z % 2 else "wgrey_deep")
    # searchlight on the front -X corner
    g.box(0, 7, 15, 0, 7, 15, "steel")
    g.set(0, 7, 16, "steel_hi")
    return g


@model("quarry_structure",
       silhouette="Orange crusher on a steel frame under a flared hopper, a conveyor rising to a gravel heap, a cut rock bench.",
       story="A gravel quarry's processing plant. The crusher stopped with a load still in "
             "its hopper; weeds have taken the cut rock bench and the site office door hangs "
             "open.",
       details=["Crusher on a four-leg steel frame with a flared hopper",
                "Inclined conveyor feeding a rounded gravel stockpile",
                "Second, smaller sand pile", "Cut rock bench with weeds along the back",
                "Portable site office with steps"],
       exclusions=["No vehicles", "No readable text"])
def quarry_structure():
    g = Grid(30, 24, 16)
    g.box(0, 0, 0, 29, 23, 0, "stone")                 # yard 15 x 12 m
    g.box(0, 18, 0, 29, 23, 0, "gravel")                # haul road
    g.box(0, 0, 1, 29, 1, 4, "stone_dark")              # cut rock bench along the back
    g.paint(0, 0, 4, 29, 1, 4, "stone")
    g.box(0, 2, 1, 29, 2, 2, "stone_dark")
    g.paint(0, 2, 2, 29, 2, 2, "stone")
    g.paint(9, 0, 4, 13, 1, 4, "moss")                  # weeds on the bench
    # crusher frame, body and hopper
    for x in (18, 23):
        for y in (8, 13):
            g.box(x, y, 1, x, y, 6, "steel_dark")
    g.box(18, 8, 4, 23, 8, 4, "steel_dark")
    g.box(18, 13, 4, 23, 13, 4, "steel_dark")
    g.box(18, 8, 7, 23, 13, 10, "safety_orange_dark")
    g.paint(18, 8, 7, 23, 13, 7, "rust_dark")
    g.box(17, 7, 11, 24, 14, 12, "steel")
    g.box(16, 6, 13, 25, 15, 13, "steel")
    g.clear(18, 8, 12, 23, 13, 13)
    g.box(18, 8, 11, 23, 13, 11, "stone")                # load left in the hopper
    g.paint(18, 9, 11, 22, 12, 11, "stone_dark")
    g.box(20, 10, 1, 21, 11, 6, "steel_dark")             # discharge chute
    # conveyor from under the crusher up to the stockpile
    for x in range(5, 20):
        z = 3 + (19 - x) // 3
        g.box(x, 10, z, x, 11, z, "charcoal")
        g.box(x, 10, z - 1, x, 11, z - 1, "steel_dark")
    for x in (8, 14):
        z = 3 + (19 - x) // 3
        g.box(x, 10, 1, x, 10, z - 2, "steel_dark")
    g.box(20, 10, 1, 21, 11, 2, "steel_dark")
    g.ellipsoid(4.0, 10.5, 0.5, 4.4, 4.4, 6.0, "gravel", only_empty=True)
    g.ellipsoid(11.0, 18.5, 0.5, 3.2, 3.0, 3.5, "khaki", only_empty=True)
    # site office
    g.box(22, 16, 1, 28, 20, 5, "almond")
    g.box(22, 16, 1, 28, 20, 1, "concrete_dark")
    g.box(21, 15, 6, 29, 21, 6, "galv")
    opening(g, "+y", 20, 24, 25, 2, 4, "black")
    opening(g, "+y", 20, 26, 27, 3, 4)
    opening(g, "-x", 22, 17, 18, 3, 4)
    g.box(24, 21, 1, 25, 21, 1, "steel_dark")
    return g


@model("gas_station",
       silhouette="Wide flat white canopy with a red stripe on columns over two pump islands, kiosk behind, blank price sign.",
       story="A two-island filling station on the main road. The tanks were pumped dry in "
             "the first days; a car was abandoned at the pumps and one pump was knocked flat "
             "by a reversing truck.",
       details=["Flat canopy with a white fascia and red stripe on four columns",
                "Two kerbed pump islands with four pumps, one knocked over",
                "Kiosk shop with a glazed front at the back of the forecourt",
                "Blank price sign on a pole at the corner"],
       exclusions=["No readable text, prices or brand"])
def gas_station():
    g = Grid(26, 24, 11)
    g.box(0, 0, 0, 25, 23, 0, "concrete")              # forecourt 13 x 12 m
    g.box(0, 22, 0, 25, 23, 0, "concrete_hi")
    g.box(0, 0, 0, 25, 0, 0, "grass")
    # kiosk shop
    X0, X1, Y0, Y1 = 2, 13, 1, 7
    g.box(X0, Y0, 0, X1, Y1, 6, "plaster")
    g.paint(X0, Y0, 0, X1, Y1, 0, "concrete_dark")
    g.paint(X0, Y0, 5, X1, Y1, 6, "paint_white")
    g.paint(X0, Y0, 5, X1, Y1, 5, "label_red")
    flat_roof(g, X0, Y0, X1, Y1, 7, "paint_white", "roof")
    storefront(g, "+y", Y1, 3, 12, 1, 4, every=3)
    opening(g, "+y", Y1, 7, 8, 1, 4, "glass")
    hvac(g, 4, 3, 7, 2, 2)
    # pump islands, columns, pumps
    for xi in (9, 17):
        g.box(xi, 12, 1, xi + 1, 18, 1, "concrete_hi")
        g.box(xi, 15, 2, xi + 1, 15, 7, "paint_white")
        for y in (13, 17):
            g.box(xi, y, 2, xi + 1, y, 3, "paint_white_shadow")
            g.box(xi, y, 4, xi + 1, y, 4, "label_red")
    g.clear(17, 17, 2, 18, 17, 4)                         # knocked-over pump
    g.box(17, 19, 1, 18, 21, 1, "paint_white_shadow")
    g.box(17, 21, 1, 18, 21, 1, "label_red")
    g.box(15, 19, 0, 20, 21, 0, "concrete_deep")           # spill stain
    # canopy: deck, white fascia with a red stripe
    g.box(4, 10, 8, 23, 20, 9, "paint_white")
    g.clear(5, 11, 9, 22, 19, 9)
    g.paint(5, 11, 8, 22, 19, 8, "roof")
    g.paint(4, 10, 8, 23, 20, 8, "label_red")
    g.paint(5, 11, 8, 22, 19, 8, "roof")
    # abandoned car at island one
    car(g, 4, 11, "bluegrey")
    # blank price sign at the corner
    g.box(2, 21, 1, 2, 21, 5, "steel")
    g.box(0, 21, 5, 4, 21, 9, "charcoal")
    g.box(1, 21, 6, 3, 21, 8, "paint_white")
    g.box(1, 21, 8, 3, 21, 8, "label_red")
    g.box(1, 21, 6, 3, 21, 6, "screen")
    return g
