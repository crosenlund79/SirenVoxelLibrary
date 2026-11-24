"""Batch B - construction modules (creator: Claude). X right, Y front (+Y), Z up; inclusive cells.

Shared rules for this family:
  * Wall modules fill exactly their 1.0 m span (x 0..9 at 0.1 m cells) and stand 2.6 m tall
    (the game's wall height); the outside face is +Y. Patterns that cross the module edge
    (stone, brick, block bonds) are laid out periodically in X so two modules side by side
    continue the bond instead of showing a seam.
  * Player-built timber walls are two cells thick: studs, plates and a noggin on the inside
    (y 0), scavenged horizontal boards two cells tall on the outside (y 1) nailed on the stud
    lines. The damaged and metal-sheathed walls are built on the same frame.
  * Doors, windows, barricades, gates and thin steel members use 0.05 m cells (game props with
    thin members); door modules fill the 1.0 x 2.1 m opening with a 0.2 m deep frame so they
    sit flush in a 0.2 m timber wall.
  * Condition varies on purpose: new lumber (floor, stairs, post, beam, foundation pier), used
    salvaged house parts (door, window), improvised scrap (walls, barricades), worn steel and
    damaged / destroyed variants that keep their intact sibling's boards and colours.
"""
import math

from catalog_registry import model
from voxkit import Grid, hash01, role_of


# ---- small local helpers ---------------------------------------------------------------------
def _path4(a0, b0, a1, b1):
    """4-connected cell path between two 2D cells (diagonals become clean face-joined steps)."""
    n = max(abs(a1 - a0), abs(b1 - b0))
    out, prev = [], None
    for i in range(n + 1):
        t = i / n if n else 0.0
        a = int(math.floor(a0 + (a1 - a0) * t + 0.5))
        b = int(math.floor(b0 + (b1 - b0) * t + 0.5))
        if prev and a != prev[0] and b != prev[1]:
            out.append((a, prev[1]))
        if (a, b) != prev:
            out.append((a, b))
        prev = (a, b)
    return out


def _strut_yz(g, y0, z0, y1, z1, x0, x1, c, w=1):
    """Diagonal member in the Y-Z plane, w cells wide (in Z), extruded over x0..x1."""
    for (y, z) in _path4(y0, z0, y1, z1):
        g.box(x0, y, z, x1, y, z + w - 1, c)


def _band_xz(g, x0, z0, x1, z1, y0, y1, c, w=2):
    """Diagonal flat bar in the X-Z plane: for every row z, w cells centred on the line.
    Steeper and smoother than a 4-connected staircase (rows always overlap by a cell)."""
    for z in range(min(z0, z1), max(z0, z1) + 1):
        t = (z - z0) / (z1 - z0) if z1 != z0 else 0.0
        xc = x0 + (x1 - x0) * t
        xa = int(math.floor(xc - (w - 1) / 2 + 0.5))
        g.box(xa, y0, z, xa + w - 1, y1, z, c)


# =============================================================================================
# Timber wall frame shared by the wooden, damaged and metal-sheathed walls (0.1 m cells)
# =============================================================================================
WALL_H = 26                       # 2.6 m
STUDS = (0, 5, 9)                 # stud columns (end studs double up when modules tile)
# Scavenged boards, bottom to top, two cells tall each: list of (x0, x1, colour).
# Values alternate light / dark so every board edge reads without painted seams.
BOARDS = [
    [(0, 9, "wgrey_dark")],                                  # splash-darkened bottom board
    [(0, 9, "wgrey_hi")],
    [(0, 5, "pine_aged"), (6, 9, "wgrey_mid")],              # butt joint on the middle stud
    [(0, 9, "wgrey")],
    [(0, 9, "siding_cream")],                                # old painted siding board
    [(0, 9, "wgrey_mid")],
    [(0, 4, "pine_light"), (5, 9, "wgrey_warm")],
    [(0, 9, "wgrey_dark")],
    [(0, 9, "wgrey_hi")],
    [(0, 9, "sage_dark")],                                   # painted shed board
    [(0, 5, "wgrey"), (6, 9, "pine_mid")],
    [(0, 9, "wgrey_mid")],
    [(0, 9, "wgrey_hi")],
]
def _timber_frame(g, y=0, h=WALL_H, frame="pine_mid"):
    """Studs, bottom/top plate and a mid-height noggin on the inside face (row y)."""
    for x in STUDS:
        g.box(x, y, 0, x, y, h - 1, frame)
    g.box(0, y, 0, 9, y, 0, "pine_aged")                       # bottom plate
    g.box(0, y, h - 1, 9, y, h - 1, frame)                     # top plate
    g.box(1, y, 12, 4, y, 12, "pine_aged")                     # noggins (staggered)
    g.box(6, y, 13, 8, y, 13, "pine_aged")


DRIP = {"wgrey_dark": "wgrey_deep", "pine_aged": "pine_dark", "wgrey_hi": "wgrey",
        "pine_light": "pine_mid", "wgrey_mid": "wgrey_dark", "siding_cream": "cream_shadow",
        "pine_mid": "pine_aged", "wgrey_warm": "wgrey_mid", "wgrey": "wgrey_mid",
        "sage_dark": "sage_deep", "sage": "sage_dark"}


def _boards(g, y=1, boards=BOARDS, nails=True):
    """Two-cell scavenged boards on row y, nailed on every stud line they cross. The lower row
    of each board is its weathered drip edge (rain runs off the board's bottom arris), which
    also separates one board from the next. Nail heads take the drip tone: an iron dot would
    be a 10 cm black square at this cell size."""
    for i, segs in enumerate(boards):
        z0 = 2 * i
        for (x0, x1, c) in segs:
            g.box(x0, y, z0 + 1, x1, y, z0 + 1, c)
            g.box(x0, y, z0, x1, y, z0, DRIP.get(c, c))
            if nails:
                for sx in STUDS + ((6,) if x0 == 6 else ()) + ((4,) if x1 == 4 else ()):
                    if x0 <= sx <= x1:
                        g.set(sx, y, z0 + 1, DRIP.get(c, c))


# ---- wooden_wall_section ---------------------------------------------------------------------
@model("wooden_wall_section",
       story="Put up in an afternoon by survivors closing a gap between two houses: a 2x4 frame "
             "with whatever boards the street gave them - fence pickets gone grey, offcuts of "
             "fresh pine, a strip of cream siding and a green board from a garden shed.",
       details=["Studs, bottom and top plate and staggered noggins on the inside (-Y) face",
                "Thirteen horizontal boards two cells (0.2 m) tall on the outside (+Y), "
                "mismatched by origin, two butt-jointed on the middle stud",
                "Nail heads on every stud line",
                "One board end stops short of the right edge, showing the stud behind"],
       exclusions=["No paint graffiti or text", "No window or door cut-out (separate modules)"],
       notes=["2.6 m tall (the game's wall height) instead of the 2.55 m reference so every "
              "full-height wall module in this family shares one height; 1.0 m wide, "
              "0.2 m thick, tiles seamlessly along X."])
def wooden_wall_section():
    g = Grid(10, 2, WALL_H)
    _timber_frame(g)
    _boards(g)
    g.clear(9, 1, 16, 9, 1, 17)                                 # short board shows the stud
    return g


# ---- damaged_wooden_wall ---------------------------------------------------------------------
@model("damaged_wooden_wall",
       story="The same scavenged-board wall after something heavy came through it: four boards "
             "were smashed out of the left bay, the noggin behind them snapped, the pine offcut "
             "swung down on its last nail and the broken pieces still lie at the foot.",
       details=["Same frame, boards and colours as Claude_wooden_wall_section",
                "Hole through the left bay (camera side) with ragged, fresh-coloured board ends",
                "Snapped noggin behind the hole",
                "The pine offcut hanging vertically from its last nail",
                "Top board torn off at one corner, top plate showing",
                "Broken board pieces lying and leaning against the foot of the wall (attached)"],
       exclusions=["No fire damage", "No loose confetti debris"],
       variant_of="wooden_wall_section",
       notes=["Same 1.0 x 2.6 m wall as the intact module; debris at the foot adds 0.2 m of "
              "depth in front (bounds 0.4 m)."])
def damaged_wooden_wall():
    g = Grid(10, 5, WALL_H)
    F, B = 1, 2                                                 # frame row, board row
    _timber_frame(g, y=F)
    _boards(g, y=B)
    g.clear(9, B, 16, 9, B, 17)
    # the hole: per board (z of board, x range knocked out); each breaks at its own length
    hole = {4: (2, 4), 5: (1, 4), 6: (1, 4), 7: (3, 4)}
    for bi, (xa, xb) in hole.items():
        z0 = 2 * bi
        g.clear(xa, B, z0, xb, B, z0 + 1)
        # fresh splinters at the broken ends: the top row tears one cell further
        if g.get(xa - 1, B, z0 + 1):
            g.set(xa - 1, B, z0 + 1, "break_fresh")
        if g.get(xa - 1, B, z0) and xa - 1 > 0:
            g.clear(xa - 1, B, z0, xa - 1, B, z0)
            g.set(xa - 2, B, z0, "snag_light") if g.get(xa - 2, B, z0) else None
    g.set(0, B, 11, "break_fresh")                              # stub left on the end stud
    g.set(0, B, 13, "break_fresh")
    # noggin snapped in the middle
    g.clear(2, F, 12, 3, F, 12)
    g.set(1, F, 12, "break_fresh")
    g.set(4, F, 12, "break_fresh")
    # the pine offcut (board 6) swung down from a nail at its left end, hanging vertically
    g.box(1, B, 9, 2, B, 13, "pine_light")
    g.box(1, B, 9, 1, B, 13, "pine_mid")
    g.set(1, B, 13, "iron")                                     # the last nail
    g.set(2, B, 9, "break_fresh")
    # torn-off corner of the top board
    g.clear(0, B, 24, 2, B, 25)
    g.set(3, B, 25, "break_fresh")
    # pieces at the foot, outside, touching the wall
    g.box(1, B + 1, 0, 4, B + 1, 0, "wgrey_mid")                # board 5 piece, lying
    g.set(4, B + 1, 0, "break_fresh")
    g.box(2, B + 2, 0, 6, B + 2, 0, "wgrey_dark")               # board 7 piece across it
    g.set(6, B + 2, 0, "break_fresh")
    g.box(3, B + 1, 1, 3, B + 1, 1, "wgrey_dark")
    for (yy, zz) in ((B + 2, 1), (B + 1, 1), (B + 1, 2), (B + 1, 3)):   # board end leaning
        g.box(6, yy, zz, 7, yy, zz, "wgrey_mid")
    g.box(6, B + 1, 3, 7, B + 1, 3, "wgrey_dark")
    g.set(7, B + 1, 3, "break_fresh")
    return {"grid": g, "footprint_cells": ((0, 9), (F, B))}


# ---- wooden_floor_section --------------------------------------------------------------------
@model("wooden_floor_section",
       story="A fresh deck module from a builder's merchant pallet: pine decking screwed square "
             "across three joists and a rim, nothing walked on it yet but the builder.",
       details=["Rim joists front and back, three joists along Y underneath",
                "Ten decking planks across the joists with staggered butt joints",
                "Fastener lines over each joist"],
       exclusions=["No railing (separate module)"],
       notes=["1.0 x 1.0 m, two cells (0.2 m) deep: one cell of joists under one cell of "
              "decking - the thinnest honest structure at 0.1 m cells (reference 0.15 m)."])
def wooden_floor_section():
    g = Grid(10, 10, 2)
    for y in (1, 5, 8):
        g.box(0, y, 0, 9, y, 0, "pine_aged")                    # joists along X, inset
    tones = ["pine_light", "pine_hi", "pine_mid", "pine_light", "pine_hi",
             "pine_mid", "pine_light", "pine_hi", "pine_light", "pine_mid"]
    for x in range(10):
        g.box(x, 0, 1, x, 9, 1, tones[x])                        # planks along Y
    # staggered butt joints over the middle joist: these planks are two offcuts
    for x, c in ((1, "pine_light"), (4, "pine_light"), (6, "pine_hi"), (8, "pine_mid")):
        g.box(x, 6, 1, x, 9, 1, c)
    # fastener lines over the joists: one step darker than the plank they are driven into
    step = {"pine_hi": "pine_light", "pine_light": "pine_mid", "pine_mid": "pine_aged"}
    for x in range(10):
        for y in (1, 5, 8):
            g.set(x, y, 1, step[role_of(g.get(x, y, 1))])
    return g


# ---- wooden_foundation_support ---------------------------------------------------------------
@model("wooden_foundation_support",
       cell=0.05,
       why="Cribbing is read from its alternating crossed sleepers; at 0.1 m cells a 0.3 m pier "
           "is three cells and each sleeper a single cell, which reads as a chequered stick. "
           "At 0.05 m the 0.1 m sleepers keep their square ends and the overhang of each layer.",
       story="A cribbing pier stacked by a careful builder: old creosoted sleeper offcuts laid "
             "log-cabin fashion on a cast concrete pad, capped with a steel bearing plate.",
       details=["Cast concrete pad with chamfered top edges",
                "Ten layers of 0.1 m sleepers, each layer crossing the one below, ends "
                "overhanging the crossing by one cell",
                "Steel bearing plate on top with four lag bolts"],
       exclusions=["No beam on top (separate module)"],
       notes=["0.35 x 0.35 x 1.2 m: a crib narrower than ~0.3 m cannot show alternating "
              "sleepers (reference 0.24 m square)."])
def wooden_foundation_support():
    g = Grid(7, 7, 24)
    g.box(0, 0, 0, 6, 6, 2, "concrete")                         # pad 0.15 m
    g.paint(0, 0, 2, 6, 6, 2, "concrete_hi")
    for (x, y) in ((0, 0), (6, 0), (0, 6), (6, 6)):
        g.set(x, y, 2, 0)                                       # chamfered corners
    g.paint(0, 0, 0, 6, 6, 0, "concrete_dark")                  # damp foot line
    sleepers = ["wood_deep", "wood_stain", "wood_deep", "bark_dark", "wood_stain"]
    for k in range(10):
        z0 = 3 + 2 * k
        c = sleepers[k % 5]
        end = "wood_stain" if c != "wood_stain" else "pine_dark"
        if k % 2 == 0:                                           # pair along X
            for y0 in (1, 4):
                g.box(0, y0, z0, 6, y0 + 1, z0 + 1, c)
                g.box(0, y0, z0, 0, y0 + 1, z0 + 1, end)       # sawn end grain
                g.box(6, y0, z0, 6, y0 + 1, z0 + 1, end)
        else:                                                    # pair along Y
            for x0 in (1, 4):
                g.box(x0, 0, z0, x0 + 1, 6, z0 + 1, c)
                g.box(x0, 0, z0, x0 + 1, 0, z0 + 1, end)
                g.box(x0, 6, z0, x0 + 1, 6, z0 + 1, end)
    g.box(1, 1, 23, 5, 5, 23, "steel_dark")                     # bearing plate
    g.paint(1, 1, 23, 5, 1, 23, "steel")
    for (x, y) in ((1, 1), (5, 1), (1, 5), (5, 5)):
        g.set(x, y, 23, "steel_light")                          # lag bolt heads at the corners
    return g


# ---- wooden_post -----------------------------------------------------------------------------
@model("wooden_post",
       cell=0.05,
       why="A 0.2 m post is two cells wide at 0.1 m, so its steel base would be a 10 cm slab and "
           "the beam notch would remove half the post; at 0.05 m the base plate, stirrup "
           "flanges and a half-depth notch keep real proportions.",
       story="A fresh 8x8 post from a pallet of yard lumber, set on a galvanised stirrup base "
             "bolted to the slab, its top already notched to take a beam that was never "
             "delivered.",
       details=["0.2 m square post with lighter arrises and a few long grain streaks",
                "Galvanised stirrup base: plate with anchor nuts and two side flanges, "
                "through-bolted",
                "Half-lap notch at the top on the +Y side with a crisp sawn shoulder",
                "One drying check running down the front face"],
       exclusions=["No beam in the notch (separate module)"],
       notes=["0.3 x 0.3 x 2.5 m including the base plate; the post itself is 0.2 m square so "
              "it lands on the 0.1 m structure grid (reference 0.17 m)."])
def wooden_post():
    g = Grid(6, 6, 50)
    top = 49
    g.box(1, 1, 1, 4, 4, top, "pine_light")
    for (x, y) in ((1, 1), (4, 1), (1, 4), (4, 4)):
        g.box(x, y, 1, x, y, top, "pine_hi")                   # arrises catch the light
    # grain streaks (long, few) and one drying check on the front
    g.box(2, 4, 9, 2, 4, 26, "pine_mid")
    g.box(3, 1, 14, 3, 1, 37, "pine_mid")
    g.box(1, 3, 20, 1, 3, 41, "pine_mid")
    g.box(3, 4, 30, 3, 4, 39, "pine_dark")                     # the check
    g.box(3, 4, 29, 3, 4, 29, "pine_aged")
    # notch: front half removed for the top 0.2 m
    g.clear(1, 3, top - 3, 4, 4, top)
    g.box(1, 1, top, 4, 2, top, "pine_aged")                   # end grain
    g.box(1, 3, top - 4, 4, 4, top - 4, "pine_aged")           # notch seat (end grain)
    g.box(1, 2, top - 3, 4, 2, top - 3, "pine_mid")            # sawn shoulder line
    # galvanised stirrup base
    g.box(0, 0, 0, 5, 5, 0, "galv")
    g.paint(0, 5, 0, 5, 5, 0, "galv_hi")
    for (x, y) in ((0, 0), (5, 0), (0, 5), (5, 5)):
        g.box(x, y, 1, x, y, 1, "steel_dark")                  # anchor nuts
    for x in (0, 5):
        g.box(x, 2, 1, x, 3, 6, "galv")                        # side flanges
        g.box(x, 2, 6, x, 3, 6, "galv_hi")
        g.set(x, 2, 4, "steel_dark")                           # through-bolt heads
    return g


# ---- wooden_beam -----------------------------------------------------------------------------
@model("wooden_beam",
       cell=0.05,
       why="Its glulam laminations (~4 cm) and the bolted end plates only exist at 0.05 m; at "
           "0.1 m the beam is a 2 x 2 stick with a 10 cm steel slab on each end.",
       story="A short glulam beam bought for a carport that never went up; a fabricator welded "
             "steel end plates on so it bolts straight between two posts.",
       details=["Four visible laminations along the length",
                "Steel end plates wider and taller than the timber, four bolt holes each",
                "Two through-bolts near each end on both faces (knife-plate connection)"],
       exclusions=["No posts (separate module)"],
       notes=["1.0 m long to match the 1 m module span (the brief's 2 m beam is two of these); "
              "0.2 m timber, 0.3 m end plates (reference 0.18 m square)."])
def wooden_beam():
    L = 20
    g = Grid(L, 6, 6)
    lams = ["pine_mid", "pine_light", "pine_hi", "pine_light"]
    for k, c in enumerate(lams):
        g.box(1, 1, 1 + k, L - 2, 4, 1 + k, c)
    for x0 in (0, L - 1):
        g.box(x0, 0, 0, x0, 5, 5, "steel")
        g.paint(x0, 0, 5, x0, 5, 5, "steel_light")              # lit top edge
        for (y, z) in ((0, 0), (5, 0), (0, 5), (5, 5)):
            g.set(x0, y, z, "charcoal")                         # bolt holes
    for x in (2, 4, L - 5, L - 3):                              # through-bolts, both faces
        for y in (1, 4):
            g.set(x, y, 2, "steel_dark")
    return g


# ---- wooden_stairs ---------------------------------------------------------------------------
@model("wooden_stairs",
       story="Porch steps cut from new lumber last week: two notched stringers, five two-board "
             "treads and a precast pad at the foot. The first muddy boots have already worn a "
             "path up the middle.",
       details=["Two cut (sawtooth) stringers flush with the tread ends, darker than the treads",
                "Five treads of two boards each rising 0.2 m per step to 1.0 m",
                "Precast concrete pad at the foot",
                "A darker walking path on the lower treads"],
       exclusions=["No handrail", "No deck at the top (stairs hang from the deck rim)"],
       front_note="+Y is the foot of the stairs (the approach side); they rise toward -Y.")
def wooden_stairs():
    g = Grid(11, 17, 10)
    # tread i (1 = bottom): z = 2i - 1, y range from the front
    for i in range(1, 6):
        z = 2 * i - 1
        y1 = 14 - 3 * (i - 1)
        y0 = y1 - 2
        for x in (0, 10):                                       # stringer block under tread
            g.box(x, y0, max(0, z - 4), x, y1, z - 1, "pine_mid")
        g.box(0, y0 + 1, z, 10, y1, z, "pine_light")            # front board (nosing)
        g.box(0, y0, z, 10, y0, z, "pine_hi")                   # back board
        if i <= 3:                                              # the muddy path
            g.box(4, y0 + 1, z, 6, y1, z, "pine_mid" if i < 3 else "pine_light")
            g.box(5, y0 + 2, z, 5, y1, z, "pine_aged" if i == 1 else "pine_mid")
    for x in (0, 10):
        g.box(x, 0, 5, x, 0, 8, "pine_aged")                    # stringer heads (end grain)
        g.box(x, 14, 0, x, 14, 0, "pine_aged")
    g.box(0, 15, 0, 10, 16, 0, "concrete")                      # precast pad
    g.paint(0, 15, 0, 0, 16, 0, "concrete_dark")
    return g


# =============================================================================================
# Door and window modules (0.05 m): fill the 1.0 m span, 0.2 m deep frames (flush in a
# 0.2 m timber wall). Low X is the camera side (screen-right in the hero view).
# =============================================================================================
FRAME = "cream_mid"          # painted trim
FRAME_WORN = "cream_shadow"


def _door_frame(g, H=42, depth=3, col=FRAME):
    """Jambs (2 cells) and head (2 cells) around a 16 x (H-2) opening, threshold at z 0."""
    g.box(0, 0, 0, 1, depth - 1, H - 1, col)
    g.box(18, 0, 0, 19, depth - 1, H - 1, col)
    g.box(0, 0, H - 2, 19, depth - 1, H - 1, col)
    # architrave: the outer cell row stands one cell proud of the inner one (stepped profile)
    g.box(0, depth, 0, 0, depth, H - 1, col)
    g.box(19, depth, 0, 19, depth, H - 1, col)
    g.box(0, depth, H - 1, 19, depth, H - 1, col)


# ---- wooden_door -----------------------------------------------------------------------------
@model("wooden_door",
       story="A four-panel front door taken off a house down the street and rehung in a new "
             "frame to open outward, so it cannot be kicked in. Teal paint from three owners "
             "ago is rubbed back to bare wood around the handle.",
       details=["Painted frame filling the 1.0 x 2.1 m opening, oak threshold",
                "Four raised-and-fielded panels, stiles, rails and a centre muntin",
                "Lever handle, deadbolt and a brass letter slot in the lock rail",
                "Three hinge knuckles on the outside (outward-opening)",
                "Paint worn to bare pine along the lock stile at hand height; scuffed bottom rail"],
       exclusions=["Closed state only", "No glazing", "No house number or text"],
       notes=["Closed. Frame 1.0 x 2.1 m and 0.2 m deep so it sits flush in the timber wall; "
              "the leaf is set back one cell and the handle stays inside the frame depth."])
def wooden_door():
    H = 42
    g = Grid(20, 4, H)
    _door_frame(g, H)
    g.box(2, 0, 0, 17, 3, 0, "wood_stain")                     # threshold
    g.box(6, 1, 0, 13, 3, 0, "pine_dark")                      # worn walking line
    # leaf: back skin y 0, stiles/rails/fields y 1 (face one cell behind the frame face)
    L = "teal"
    g.box(2, 0, 1, 17, 1, H - 3, L)
    panels = [((4, 8), (5, 16)), ((11, 15), (5, 16)), ((4, 8), (20, 36)), ((11, 15), (20, 36))]
    for (xa, xb), (za, zb) in panels:
        g.clear(xa, 1, za, xb, 1, zb)                           # recess (groove ring shows)
        g.box(xa, 0, za, xb, 0, zb, "teal_dark")
        g.box(xa + 1, 1, za + 1, xb - 1, 1, zb - 1, L)          # raised field
        g.box(xa + 1, 1, zb - 1, xb - 1, 1, zb - 1, "teal_hi")  # lit top bevel of the field
    # hinge knuckles on the outside of the hinge stile (high X)
    for z0 in (4, 19, 34):
        g.box(17, 2, z0, 17, 2, z0 + 2, "brass_dark")
        g.set(17, 2, z0 + 2, "brass")
    # hardware on the lock stile (low X, camera side)
    g.box(3, 2, 17, 3, 2, 21, "brass_dark")                     # backplate
    g.set(3, 2, 18, "black")                                    # keyway
    g.set(3, 2, 20, "brass")
    g.box(3, 3, 20, 5, 3, 20, "brass")                          # lever
    g.set(3, 2, 25, "brass")                                    # deadbolt cylinder
    g.box(7, 1, 17, 12, 1, 19, "brass_dark")                    # flush letter plate
    g.box(8, 1, 18, 11, 1, 18, "black")                         # the slot
    # wear: paint rubbed through on the lock stile edge and around the handle
    g.box(2, 1, 16, 2, 1, 23, "pine_mid")
    g.box(2, 0, 17, 2, 0, 22, "pine_mid")
    g.box(3, 1, 15, 4, 1, 16, "teal_hi")
    g.box(3, 1, 22, 4, 1, 24, "teal_hi")
    g.box(2, 1, 24, 2, 1, 26, "teal_hi")
    g.box(4, 1, 1, 15, 1, 2, "teal_dark")                       # kicked bottom rail
    g.box(6, 1, 1, 9, 1, 1, "wgrey_dark")
    # frame weathering where the rain hits: bottom of the jambs, head lit edge
    g.box(0, 3, 0, 0, 3, 3, FRAME_WORN)
    g.box(19, 3, 0, 19, 3, 2, FRAME_WORN)
    g.box(0, 3, H - 1, 19, 3, H - 1, "cream")
    return g


# ---- window_frame ----------------------------------------------------------------------------
@model("window_frame",
       story="A six-over-six sash window salvaged whole, frame and all, from a house that "
             "burned. One cracked pane was replaced with cardboard and tape; the sill paint "
             "has weathered through where rain sat on it.",
       details=["Painted frame and head, sill projecting 5 cm beyond the outside face",
                "Upper sash outside, lower sash inside (offset one cell), meeting rails overlap",
                "Sash bars dividing each sash into 3 x 2 lites, glass set back behind the bars",
                "One lower lite replaced with taped cardboard",
                "Weathered sill and lower rail"],
       exclusions=["Glass is opaque (glass palette roles)", "No curtains"],
       notes=["1.0 x 1.2 m to fill a 1 m wall bay; 0.2 m deep frame plus the sill nose."])
def window_frame():
    g = Grid(20, 5, 24)
    g.box(0, 0, 0, 1, 2, 23, FRAME)                             # jambs
    g.box(18, 0, 0, 19, 2, 23, FRAME)
    g.box(0, 0, 22, 19, 2, 23, FRAME)                           # head
    g.box(0, 3, 0, 0, 3, 23, FRAME)                             # stepped architrave
    g.box(19, 3, 0, 19, 3, 23, FRAME)
    g.box(0, 3, 23, 19, 3, 23, "cream")
    g.box(0, 0, 0, 19, 4, 1, FRAME)                             # sill, nose at y 4
    g.box(0, 4, 0, 19, 4, 0, FRAME_WORN)                        # drip edge
    g.box(10, 4, 1, 12, 4, 1, "wgrey_hi")                       # paint failed on the nose
    g.box(2, 3, 1, 17, 3, 1, FRAME_WORN)                        # water sits here

    def sash(y, z0, z1, rail_lo, rail_hi, hbar):
        g.box(2, y - 1, z0, 17, y, z1, FRAME)                   # sash, two cells deep, so the
        # glass set in its back row is held by the bars (and stays recessed behind their face)
        for (xa, xb) in ((3, 6), (8, 11), (13, 16)):
            for (za, zb) in ((z0 + rail_lo, hbar - 1), (hbar + 1, z1 - rail_hi)):
                g.clear(xa, y, za, xb, y, zb)
                g.box(xa, y - 1, za, xb, y - 1, zb, "glass_dark")
                for x in range(xa, xb + 1):                     # one diagonal sky reflection
                    for z in range(za, zb + 1):                 # crossing the whole window
                        if (x + z) in (27, 28, 33):
                            g.set(x, y - 1, z, "glass")
    g.box(1, 0, 2, 1, 2, 21, FRAME)                             # jamb stop beside the sashes
    g.box(18, 0, 2, 18, 2, 21, FRAME)
    sash(2, 12, 21, 1, 2, 16)                                   # upper sash, outside
    sash(1, 2, 11, 2, 1, 7)                                     # lower sash, inside
    # cardboard patch in the lower sash, camera side
    g.box(3, 0, 4, 6, 0, 6, "card")
    g.box(3, 0, 6, 6, 0, 6, "card_hi")
    g.box(5, 0, 4, 5, 0, 6, "label_cream")                      # tape strip
    g.box(3, 0, 4, 4, 0, 4, "card_dark")                        # water stain
    g.box(2, 1, 2, 17, 1, 2, FRAME_WORN)                        # weathered bottom rail
    return g


# =============================================================================================
# Barricades (0.05 m). Uprights and plank stock shared by the three barricade states.
# Planks run along X on the +Y face; the brace foot (runner + diagonal brace) stands behind.
# =============================================================================================
# (z0, z1, x0, x1, colour) bottom to top; gaps between some planks, a viewing slot at 1.5 m
BARR_PLANKS = [
    (1, 4, 0, 19, "wgrey_dark"),
    (6, 8, 2, 19, "pine_mid"),          # ends on the near upright
    (9, 12, 0, 18, "sage_dark"),        # painted fence board
    (13, 15, 1, 17, "wgrey"),           # ends on the far upright
    (17, 20, 0, 19, "pine_light"),
    (21, 23, 0, 16, "wgrey_mid"),
    (24, 27, 1, 19, "wgrey_warm"),
    (28, 29, 2, 19, "pine_hi"),         # pallet slat
    (32, 35, 0, 19, "wgrey_dark"),      # (gap z 30-31: the viewing slot)
    (36, 38, 1, 18, "pine_aged"),
]
PLANK_END = {"wgrey_dark": "wgrey_deep", "pine_mid": "pine_aged", "sage_dark": "sage_deep",
             "wgrey": "wgrey_mid", "pine_light": "pine_mid", "wgrey_mid": "wgrey_dark",
             "wgrey_warm": "wgrey_mid", "pine_hi": "pine_light", "pine_aged": "pine_dark"}
NAIL_HEAD = "iron_edge"


def _plank(g, z0, z1, x0, x1, y, c, nail_x=(), ragged=None):
    """A plank on row y; darker end grain at both ends, a nail head at each upright it
    crosses. ragged='lo'/'hi' tears the top row of that end back one cell (split end)."""
    g.box(x0, y, z0, x1, y, z1, c)
    g.box(x0, y, z0, x1, y, z0, PLANK_END.get(c, c))            # lower arris / drip edge
    if ragged == "lo":
        g.clear(x0, y, z1 - 1, x0, y, z1)
        g.set(x0 + 1, y, z1, "break_fresh")
    elif ragged == "hi":
        g.clear(x1, y, z1 - 1, x1, y, z1)
        g.set(x1 - 1, y, z1, "break_fresh")
    for x in nail_x:
        if x0 <= x <= x1:
            g.set(x, y, (z0 + z1 + 1) // 2, NAIL_HEAD)


def _brace_foot(g, x0, x1, y_back, y_up, z_top, col="pine_mid"):
    """Runner on the ground from y_back to y_up and a diagonal brace up to the upright."""
    g.box(x0, y_back, 0, x1, y_up, 0, col)
    g.box(x0, y_back, 0, x1, y_back, 0, "pine_aged")
    _strut_yz(g, y_back, 1, y_up - 1, z_top, x0, x1, col, w=2)


# ---- wooden_barricade ------------------------------------------------------------------------
@model("wooden_barricade",
       story="Thrown up across a side passage on the first night: two 4x4 uprights on braced "
             "feet and every plank within reach - fence boards, a green shed board, pallet "
             "slats. A gap was left at eye height to watch the street.",
       details=["Two 0.1 m uprights on runner feet with diagonal braces behind",
                "Ten mismatched planks of different widths, lengths and sources, nailed on the "
                "outside face, gaps between some",
                "A viewing slot at about 1.5 m",
                "Split plank ends, nail heads at each upright"],
       exclusions=["No barbed wire", "No sheet metal (see the reinforced barricade)"],
       notes=["1.0 x 2.0 m face; the braced feet need 0.35 m of depth to stand (reference "
              "0.23 m)."])
def wooden_barricade():
    g = Grid(20, 8, 40)
    YP = 7                                                       # plank row (outside face)
    for (x0, x1) in ((2, 3), (16, 17)):
        g.box(x0, 5, 0, x1, 6, 39, "pine_aged")
        g.box(x0, 6, 0, x1, 6, 39, "pine_aged")
        _brace_foot(g, x0, x1, 0, 4, 16)
    g.box(2, 5, 39, 3, 6, 39, "pine_dark")                      # sawn tops
    g.clear(16, 5, 39, 16, 6, 39)                                # rough-cut top
    g.box(17, 5, 39, 17, 6, 39, "break_fresh")
    for (z0, z1, x0, x1, c) in BARR_PLANKS:
        rag = "hi" if c in ("pine_mid", "wgrey_warm") else ("lo" if c == "wgrey" else None)
        _plank(g, z0, z1, x0, x1, YP, c, nail_x=(3, 16), ragged=rag)
    return {"grid": g, "footprint_cells": ((0, 19), (0, YP))}


# ---- reinforced_wooden_barricade -------------------------------------------------------------
@model("reinforced_wooden_barricade",
       story="The side-passage barricade after a bad week: rebuilt on three uprights with a "
             "second layer of boards, propped from behind, and patched with whatever steel "
             "turned up - a corrugated garage panel and a rusty plate - bolted through.",
       details=["Three uprights, each propped by a heavy angled strut to a ground block",
                "Double planking: vertical boards behind, horizontal planks in front",
                "Corrugated galvanised sheet and a rusty steel plate bolted over the planks",
                "Viewing slot cut through all layers at about 1.7 m",
                "Uneven board tops above the frame"],
       exclusions=["No barbed wire", "No firing ports or weapons"],
       variant_of="wooden_barricade",
       notes=["1.0 x 2.05 m face; the props need 0.5 m of depth (reference 0.25 m)."])
def reinforced_wooden_barricade():
    g = Grid(20, 10, 41)
    YU, YV, YP, YM = 5, 7, 8, 9                    # uprights 5-6, vertical boards, planks, metal
    for (x0, x1) in ((1, 2), (9, 10), (17, 18)):
        g.box(x0, YU, 0, x1, YU + 1, 39, "pine_aged")
        g.box(x0, YU, 39, x1, YU + 1, 39, "pine_dark")
        g.box(x0, 0, 0, x1, YU + 1, 0, "pine_mid")               # runner
        g.box(x0, 0, 0, x1, 1, 1, "wood_stain")                  # ground block
        _strut_yz(g, 1, 2, YU - 1, 27, x0, x1, "wgrey_warm", w=2)  # heavy prop
    # inner layer: vertical boards, uneven tops
    vb = [(0, 3, "pine_mid", 38), (4, 6, "wgrey_mid", 40), (7, 10, "pine_aged", 37),
          (11, 13, "wgrey", 39), (14, 16, "pine_mid", 40), (17, 19, "wgrey_dark", 38)]
    for (x0, x1, c, top) in vb:
        g.box(x0, YV, 1, x1, YV, top, c)
        g.box(x0, YV, top, x1, YV, top, PLANK_END.get(c, c))
    # outer layer: horizontal planks (fewer gaps than the basic barricade)
    planks = [(1, 4, 0, 19, "wgrey_dark"), (5, 8, 0, 19, "pine_light"),
              (9, 12, 1, 19, "sage_dark"), (13, 16, 0, 18, "wgrey"),
              (17, 20, 0, 19, "pine_mid"), (21, 24, 0, 19, "wgrey_mid"),
              (25, 28, 1, 19, "wgrey_warm"), (29, 32, 0, 18, "pine_light"),
              (36, 38, 0, 19, "wgrey_dark")]
    for (z0, z1, x0, x1, c) in planks:
        _plank(g, z0, z1, x0, x1, YP, c, nail_x=(2, 9, 17),
               ragged="hi" if c == "sage_dark" else None)
    # viewing slot through both board layers (z 33-35)
    g.clear(4, YV, 33, 14, YV, 35)
    # corrugated galvanised panel, low and wide; ribs are alternating value columns
    g.box(3, YM, 3, 15, YM, 17, "galv")
    for x in range(3, 16, 2):
        g.box(x, YM, 3, x, YM, 17, "galv_dark")
    g.box(3, YM, 17, 15, YM, 17, "galv_hi")                      # lit top edge
    g.box(3, YM, 3, 15, YM, 3, "rust_deep")                      # rusted foot
    g.box(13, YM, 4, 13, YM, 6, "rust_deep")                     # rust run up one rib
    for x in (4, 9, 14):
        for z in (5, 15):
            g.set(x, YM, z, "steel_dark")                        # bolt heads
    # rusty steel plate, upper camera side, overlapping the slot's lower edge
    g.box(0, YM, 21, 8, YM, 32, "iron_warm")                     # old steel plate
    g.box(0, YM, 32, 8, YM, 32, "steel")                         # lit top edge
    g.box(0, YM, 21, 8, YM, 22, "rust_deep")                     # rusted where water sits
    g.box(3, YM, 23, 5, YM, 23, "rust_deep")
    g.box(7, YM, 27, 7, YM, 30, "rust_deep")                     # streak under one bolt
    for (x, z) in ((1, 22), (7, 22), (1, 31), (7, 31)):
        g.set(x, YM, z, "steel_light")
    return {"grid": g, "footprint_cells": ((0, 19), (0, YP))}


# ---- destroyed_barricade ---------------------------------------------------------------------
@model("destroyed_barricade",
       story="What was left of the side-passage barricade the morning after: the near upright "
             "snapped at the foot, the far one still standing on its brace with a few planks "
             "nailed on, one swinging from a single nail, the rest lying where they fell.",
       details=["Same uprights, brace feet and plank stock as Claude_wooden_barricade",
                "Far upright standing (1.35 m, splintered top) with broken plank stubs",
                "Near upright snapped into a stump, its upper half lying on the planks",
                "One broken plank hanging vertically from its last nail, foot on the pile",
                "Fallen planks lying in front, touching each other, the stump and the stubs"],
       exclusions=["No fire or scorch marks", "No scattered single-voxel debris"],
       variant_of="wooden_barricade",
       notes=["Fallen planks lie up to 0.2 m in front of the barricade line (bounds 0.55 m)."])
def destroyed_barricade():
    g = Grid(20, 12, 27)
    YP = 7
    # far upright standing, near upright a stump; both brace feet survive
    g.box(16, 5, 0, 17, 6, 25, "pine_aged")
    g.box(16, 5, 26, 16, 6, 26, "pine_aged")
    g.set(16, 6, 26, "break_fresh")
    g.box(17, 5, 25, 17, 6, 25, "break_fresh")
    _brace_foot(g, 16, 17, 0, 4, 16)
    g.box(2, 5, 0, 3, 6, 4, "pine_aged")
    g.box(2, 5, 5, 2, 6, 5, "break_fresh")
    g.set(3, 5, 5, "snag_light")
    g.box(2, 0, 0, 3, 4, 0, "pine_mid")                         # runner (its brace torn away)
    g.box(2, 0, 0, 3, 0, 0, "pine_aged")
    # plank stubs still nailed to the far upright (broken ends toward the camera)
    stubs = [(1, 4, 9, 19, "wgrey_dark"), (9, 12, 13, 19, "sage_dark"),
             (17, 20, 11, 19, "pine_light"), (21, 23, 14, 18, "wgrey_mid")]
    for (z0, z1, x0, x1, c) in stubs:
        _plank(g, z0, z1, x0, x1, YP, c, nail_x=(16,), ragged="lo")
        g.box(x0, YP, z0, x0, YP, z1 - 2, "break_fresh")
    # fallen pieces in front, lying against the barricade line: a wide grey plank (touching the
    # stump and lying under the bottom stub), a pine plank across it, the snapped upright on top
    g.box(0, YP, 0, 11, YP + 3, 0, "wgrey_dark")
    g.box(0, YP, 0, 0, YP + 3, 0, "break_fresh")
    g.box(12, YP, 0, 17, YP + 2, 0, "wgrey_warm")
    g.box(4, YP + 1, 1, 12, YP + 3, 1, "pine_light")
    g.box(4, YP + 1, 1, 12, YP + 1, 1, "pine_mid")
    g.box(12, YP + 1, 1, 12, YP + 3, 1, "break_fresh")
    g.box(1, YP + 2, 2, 9, YP + 3, 3, "pine_aged")               # upper half of the upright
    g.box(9, YP + 2, 2, 9, YP + 3, 3, "break_fresh")
    # a broken plank swung down on its last nail, its foot resting on the fallen planks
    g.box(13, YP + 1, 1, 15, YP + 1, 16, "wgrey")
    g.box(13, YP + 1, 1, 13, YP + 1, 16, "wgrey_mid")
    g.set(15, YP + 1, 15, NAIL_HEAD)
    g.box(13, YP + 1, 1, 14, YP + 1, 1, "break_fresh")
    return {"grid": g, "footprint_cells": ((0, 19), (0, YP))}


# =============================================================================================
# Masonry (0.1 m). Units are laid out on a course table that repeats every 10 cells in X, so
# modules placed side by side continue the bond. Tones are picked per unit with hash01 and
# never repeat a neighbour's tone (left or below).
# =============================================================================================
def _course_units(courses, period=10):
    """courses: list of (height, widths, offset) bottom to top -> list of units
    (unit_id, x_cells (list, wrapped), z0, z1)."""
    units, z = [], 0
    for ci, (h, widths, off) in enumerate(courses):
        x = off
        for wi, w in enumerate(widths):
            units.append(((ci, wi), [(x + k) % period for k in range(w)], z, z + h - 1))
            x += w
        z += h
    return units, z


def _assign_tones(units, tones, seed):
    """Unit id -> tone, avoiding the tone of the unit to the left and those directly below."""
    owner = {}
    for (uid, xs, z0, z1) in units:
        for x in xs:
            for z in range(z0, z1 + 1):
                owner[(x, z)] = uid
    out = {}
    for (uid, xs, z0, z1) in units:
        ban = set()
        for x in xs:
            below = owner.get((x, z0 - 1))
            if below in out:
                ban.add(out[below])
        left = owner.get(((xs[0] - 1) % 10, z0))
        if left in out:
            ban.add(out[left])
        cands = [t for t in tones if t not in ban] or tones
        out[uid] = cands[int(hash01(uid[0], uid[1], seed=seed) * len(cands))]
    return out, owner


# ---- brick_wall_section ----------------------------------------------------------------------
# weighted tone pool (repeats = weight)
BRICK_TONES = ["red", "red", "red", "red_dark", "red_dark", "terra", "terra", "red_hi",
               "terra_dark"]
BRICK_COURSES = [(1, [2] * 5, (k % 2)) for k in range(WALL_H)]
BRICK_SILL_Z = 10
BRICK_SOLDIER_Z = (23, 24)


def _brick_wall(g, y0=0, y1=1):
    """Running bond, plinth, projecting rowlock sill course, soldier course and coping."""
    units, _ = _course_units(BRICK_COURSES)
    tone, owner = _assign_tones(units, BRICK_TONES, seed=11)
    for (uid, xs, z0, z1) in units:
        c = tone[uid]
        if z0 <= 1:                                              # engineering-brick plinth
            c = ("red_deep", "maroon_dark", "red_dark")[int(hash01(*uid, seed=3) * 3)]
        for x in xs:
            g.box(x, y0, z0, x, y1, z1, c)
    for x in range(10):                                          # rowlock sill, proud 1 cell
        g.box(x, y0, BRICK_SILL_Z, x, y1 + 1, BRICK_SILL_Z,
              ("red_dark", "terra_dark", "red_deep", "terra_dark")[x % 4])
    za, zb = BRICK_SOLDIER_Z
    for x in range(10):                                          # soldier course (bricks on end)
        g.box(x, y0, za, x, y1, zb, ("red", "red_dark", "terra", "red_dark", "red_hi")[x % 5])
    g.box(0, y0, WALL_H - 1, 9, y1 + 1, WALL_H - 1, "concrete")  # coping with a front drip
    g.box(0, y0, WALL_H - 1, 9, y1, WALL_H - 1, "concrete_hi")
    return units, tone


@model("brick_wall_section",
       story="Garden-wall brickwork laid new by someone who knew the trade: running bond in "
             "mixed reds, a dark engineering-brick plinth, a projecting rowlock sill course at "
             "window height, a soldier course and a cast coping.",
       details=["Running-bond bricks at true size (0.2 x 0.1 m) with per-brick tone variation",
                "Two-course dark plinth", "Rowlock sill course projecting 0.1 m at 1.0 m",
                "Soldier course under a cast concrete coping with a front drip"],
       exclusions=["No graffiti or posters"],
       notes=["At 0.1 m cells a true-scale brick is 2 x 1 cells and its 1 cm mortar joint is "
              "sub-cell, so the bond is carried by per-brick tone (no neighbour repeats) and "
              "the course features; a one-cell mortar line would double the joint area.",
              "2.6 m tall like every full wall module; the bond repeats every 1 m so modules "
              "tile; 0.2 m body, 0.3 m at sill course and coping."])
def brick_wall_section():
    g = Grid(10, 3, WALL_H)
    _brick_wall(g)
    return g


# ---- stone_wall_section ----------------------------------------------------------------------
STONE_TONES = ["stone", "stone_dark", "concrete", "concrete_dark", "wgrey", "stone",
               "bark_hi", "wgrey_warm", "concrete_deep"]
MORTAR = "cream_mid"
# Random-coursed rubble: each course = stone faces (h-1 rows) + a recessed mortar bed row on
# top; each stone has a mortar head joint on its right. Stones stand one cell proud of the
# mortar. (height, widths summing to the 1 m period, offset), bottom to top.
RUBBLE_COURSES = [(4, [4, 3, 3], 0), (3, [3, 4, 3], 2), (4, [5, 5], 1), (3, [3, 3, 4], 3),
                  (3, [4, 6], 0), (4, [3, 4, 3], 2), (3, [5, 5], 4), (2, [6, 4], 1)]


def _rubble_face(g, y_face, courses=RUBBLE_COURSES, seed=5, flat_top=True, keep=None):
    """Proud fieldstones on row y_face (mortar must exist behind). Corners of larger stones
    are clipped back to the mortar so the stones read as rounded, not as bricks.
    keep(x, z) -> bool can veto cells (used by the broken wall). Returns the unit cells."""
    units, top = _course_units(courses)
    tone, owner = _assign_tones(units, STONE_TONES, seed=seed)
    cells = {}
    for (uid, xs, z0, z1) in units:
        last = flat_top and z1 == top - 1
        zf = z1 if last else z1 - 1                              # top row is the bed joint
        face_x = xs[:-1] if len(xs) > 2 else xs
        big = len(face_x) >= 3 and zf - z0 >= 1
        clips = set()
        for k, (x, z) in enumerate(((face_x[0], z0), (face_x[-1], zf), (face_x[0], zf),
                                    (face_x[-1], z0))):
            if (z0 == 0 and z == z0) or last or not big:
                continue
            if hash01(*uid, k, seed=seed + 1) < 0.4 and len(clips) < 2:
                clips.add((x, z))
        for x in face_x:
            for z in range(z0, zf + 1):
                if (x, z) in clips or (keep and not keep(x, z)):
                    continue
                g.set(x, y_face, z, tone[uid])
                cells[(x, z)] = uid
    return cells


@model("stone_wall_section",
       story="A new wall of local fieldstone laid by a mason who sorted every load: big stones "
             "at the foot, long flat ones on top, set proud of a light lime mortar.",
       details=["Random-coursed fieldstone, stones 0.2-0.5 m in varied grey-brown tones",
                "Stones stand 0.1 m proud of recessed light lime mortar beds and head joints",
                "Larger stones have clipped corners so they read rounded, not squared",
                "Both faces built; long flat cap stones on top",
                "Course pattern repeats every 1 m so modules continue the wall"],
       exclusions=["No moss or graffiti (new wall)"],
       notes=["2.6 m tall like every full wall module (reference 2.4 m); 0.3 m thick."])
def stone_wall_section():
    g = Grid(10, 3, WALL_H)
    g.box(0, 1, 0, 9, 1, WALL_H - 1, MORTAR)                     # mortar core
    _rubble_face(g, 2)                                            # outside face
    _rubble_face(g, 0, seed=9)                                    # inside face
    return g


# ---- stone_foundation ------------------------------------------------------------------------
@model("stone_foundation",
       story="A levelled fieldstone footing block from the same mason: rough stones on the "
             "sides, the top dressed flat with big flags so a floor frame can sit on it.",
       details=["One course of full-height fieldstones on all four sides, lime mortar joints "
                "open to the top", "Flat top: four large flags with flush joints inside the "
                "ring of side stones",
                "Flag layout repeats every 1 m in both directions so modules tile"],
       exclusions=["No moss (new)"],
       notes=["1.0 x 1.0 x 0.3 m module (reference 0.27 m)."])
def stone_foundation():
    g = Grid(10, 10, 3)
    g.box(1, 1, 0, 8, 8, 2, MORTAR)                              # mortar core, recessed 1 cell
    # sides: one ring of fieldstones the full 0.3 m height, laid round the perimeter so the
    # corner stones wrap round the corners; head joints (recessed, open to the top) are kept at
    # least two cells from every corner. Ring order: y- face, x+ face, y+ face, x- face.
    ring = ([(x, 0) for x in range(10)] + [(9, y) for y in range(1, 10)] +
            [(x, 9) for x in range(8, -1, -1)] + [(0, y) for y in range(8, 0, -1)])
    widths, pos, prev = [4, 4, 5, 4, 5, 4, 5, 5], 4, None
    for k, w in enumerate(widths):
        cands = [t for t in STONE_TONES if t != prev]
        c = cands[int(hash01(k, seed=37) * len(cands))]
        prev = c
        for j in range(w - 1):                                    # last cell = head joint
            x, y = ring[(pos + j) % len(ring)]
            g.box(x, y, 0, x, y, 2, c)
        pos += w
    # flat top inside the ring: four flags with flush joints
    J = "cream_deep"                                             # dirt-darkened top joints
    g.box(1, 1, 2, 8, 8, 2, J)
    flags = [((1, 3), (1, 4), "stone"), ((5, 8), (1, 2), "concrete_dark"),
             ((5, 8), (4, 8), "wgrey"), ((1, 3), (6, 8), "concrete")]
    for (xa, xb), (ya, yb), c in flags:
        g.box(xa, ya, 2, xb, yb, 2, c)
    return g


# ---- concrete_wall_section -------------------------------------------------------------------
CMU_TONES = ["concrete", "curb", "concrete_hi"]


@model("concrete_wall_section",
       story="Concrete-block wall from a contractor's yard, laid in running bond and capped "
             "with a poured bond beam whose anchor plates waited for a roof that never came; "
             "the first rains have already run rust down the face.",
       details=["0.4 x 0.2 m blocks in running bond, half-block offset, darker struck head "
                "joints, subtle per-block tone",
                "Poured bond beam (0.2 m) along the top with two steel anchor plates",
                "One rust streak running down the face from an anchor plate"],
       exclusions=["No render or paint"],
       notes=["2.6 m tall like every full wall module; 0.3 m thick (12-inch block)."])
def concrete_wall_section():
    g = Grid(10, 3, WALL_H)
    courses = [(2, [4, 4, 2], 0) if k % 2 == 0 else (2, [2, 4, 4], 0) for k in range(12)]
    units, _ = _course_units(courses)
    tone, owner = _assign_tones(units, CMU_TONES, seed=21)
    for (uid, xs, z0, z1) in units:
        for x in xs:
            g.box(x, 0, z0, x, 2, z1, tone[uid])
        g.box(xs[-1], 0, z0, xs[-1], 2, z1, "concrete_dark")     # struck head joint
    g.box(0, 0, 24, 9, 2, 25, "concrete_hi")                     # bond beam
    g.box(0, 0, 24, 9, 2, 24, "concrete")
    for x in (2, 7):
        g.set(x, 1, 25, "steel_dark")                            # anchor plates for a roof plate
    # rust from the anchor plate runs over the beam edge and down the face
    g.paint(7, 2, 24, 7, 2, 25, "rust_dark")
    g.paint(7, 2, 18, 7, 2, 23, "rust_deep")
    g.paint(8, 2, 21, 8, 2, 23, "rust_deep")
    g.paint(7, 2, 15, 7, 2, 17, "gravel")
    return g


# ---- broken_brick_wall -----------------------------------------------------------------------
@model("broken_brick_wall",
       story="The garden wall after a vehicle clipped its top: the upper courses broke away "
             "along the mortar in steps, taking the coping with them, and the bricks lie in a "
             "heap at the foot where they fell.",
       details=["Same bond, plinth, sill course and tones as Claude_brick_wall_section",
                "Upper part knocked out along a stepped break that follows the brick joints, "
                "higher at the far end, broken half-bricks on the edge",
                "Rubble heap at the foot, deepest under the low end: dust-dulled bricks in "
                "alternating directions, loose bricks sticking out, a lump of mortar and the "
                "broken coping at its toe", "One loosened brick pushed half out of the face"],
       exclusions=["No scorch marks", "No loose single-cell confetti"],
       variant_of="brick_wall_section",
       notes=["Remaining wall up to 2.3 m; the rubble heap spreads 0.5 m in front (bounds "
              "0.7 m deep)."])
def broken_brick_wall():
    g = Grid(10, 7, WALL_H)
    Y0 = 0                                                       # wall body on y 0..1
    units, tone = _brick_wall(g, Y0, Y0 + 1)
    # stepped break line: highest surviving course per brick column (x low = camera side)
    top_at = {0: 8, 1: 9, 2: 9, 3: 13, 4: 14, 5: 14, 6: 15, 7: 20, 8: 22, 9: 21}
    for (uid, xs, z0, z1) in units:
        hi = max(top_at[x] for x in xs)
        lo = min(top_at[x] for x in xs)
        if z0 > hi:
            for x in xs:
                g.clear(x, 0, z0, x, 2, z1)
        elif z0 > lo:                                            # brick on the edge: half survives
            for x in xs:
                if z0 > top_at[x]:
                    g.clear(x, 0, z0, x, 2, z1)
                else:
                    g.set(x, 0, z0, "red_hi")                    # fresh broken face
    g.clear(0, 0, 23, 9, 2, WALL_H - 1)                          # soldier course and coping gone
    g.clear(0, 2, 10, 3, 2, 10)                                  # sill course broken back
    g.set(4, 2, 10, "terra_hi")
    g.box(4, 2, 14, 5, 2, 14, tone[[u for u in units if u[2] == 14 and 4 in u[1]][0][0]])
    g.clear(4, 0, 14, 5, 0, 14)                                  # loosened brick, pushed out
    # rubble heap at the foot, deepest under the low (camera-side) end where the wall fell:
    # an uneven height map filled with bricks lying in alternating directions, dust-dulled
    heights = {2: [5, 6, 4, 5, 3, 3, 2, 2, 1, 1], 3: [4, 5, 4, 2, 3, 1, 2, 1, 0, 1],
               4: [2, 3, 3, 2, 1, 1, 1, 0, 0, 0], 5: [1, 2, 1, 1, 0, 1, 0, 0, 0, 0],
               6: [1, 0, 1, 0, 0, 0, 0, 0, 0, 0]}
    rub = ["red_dark", "terra", "red", "terra_dark", "red_deep", "red_dark", "terra_hi"]
    for y, row in heights.items():
        for x, h in enumerate(row):
            for z in range(h):
                key = (x // 2, y, z) if z % 2 == 0 else (x, y // 2, z)
                g.set(x, y, z, rub[int(hash01(*key, seed=17) * len(rub))])
    # loose bricks lying across the heap, sticking out of it
    g.box(1, 4, 3, 1, 5, 3, "red_hi")                            # along Y, cantilevered
    g.box(3, 2, 5, 4, 2, 5, "terra")                             # along X on the crest
    g.box(6, 5, 0, 6, 6, 0, "red_dark")                          # tumbled to the toe
    g.box(4, 6, 0, 7, 6, 0, "concrete")                          # broken coping piece
    g.set(4, 6, 0, "concrete_hi")
    g.set(7, 6, 0, "concrete_dark")
    g.box(2, 3, 3, 3, 3, 3, "cream_deep")                        # lump of old mortar
    return {"grid": g, "footprint_cells": ((0, 9), (0, 1))}


# ---- concrete_foundation ---------------------------------------------------------------------
@model("concrete_foundation",
       story="A slab section poured last month for a shed that never got built: floated top, "
             "a chamfered outside edge, two anchor bolts waiting for a sill plate, and the "
             "screed board the builder left on it when the sirens went quiet.",
       details=["Poured slab with a chamfered top edge on the outside (+Y) face",
                "Two galvanised anchor bolts with washers on the sill line",
                "Float-finished lighter top, damp foot",
                "The screed board still lying on it"],
       exclusions=["No reinforcement visible", "No cracks (new)"],
       notes=["1.0 x 1.0 x 0.3 m module; bolts stand 0.1 m above the slab (bounds 0.4 m).",
              "Only the outside (+Y) edge is chamfered so slabs tiled in a row stay flat; at "
              "0.1 m cells the 45-degree chamfer is a one-cell step."])
def concrete_foundation():
    g = Grid(10, 10, 4)
    g.box(0, 0, 0, 9, 9, 2, "concrete")
    g.paint(0, 0, 0, 9, 9, 0, "concrete_dark")                   # damp foot
    g.paint(0, 0, 2, 9, 9, 2, "concrete_hi")                     # float-finished top
    g.clear(0, 9, 2, 9, 9, 2)                                    # chamfer on the outside edge
    g.paint(0, 9, 1, 9, 9, 1, "concrete_hi")                     # chamfer face catches light
    g.paint(0, 0, 1, 9, 8, 1, "concrete")
    g.box(1, 2, 3, 7, 2, 3, "pine_aged")                         # forgotten screed board
    g.box(1, 2, 3, 1, 2, 3, "pine_dark")
    for x in (3, 7):                                             # anchor bolts on the sill line
        g.set(x, 6, 2, "steel_dark")                             # washer seat
        g.set(x, 6, 3, "galv")
    return g


# ---- metal_reinforced_wall -------------------------------------------------------------------
@model("metal_reinforced_wall",
       story="The scavenged-board wall after its owners got scared: they bolted whatever steel "
             "they could carry over the outside - a galvanised roofing sheet, a rusty plate and "
             "an old almond appliance panel - and left the top boards bare.",
       details=["Same timber frame and boards as Claude_wooden_wall_section behind",
                "Corrugated galvanised sheet (vertical ribs) over the lower camera-side bay",
                "Rusty steel plate lapping it, rust bleeding from its bolts",
                "Old almond appliance panel higher up, bare boards visible above and between",
                "Bolt heads in rows on the stud lines"],
       exclusions=["No barbed wire", "No graffiti"],
       variant_of="wooden_wall_section",
       notes=["2.6 m tall; 0.3 m deep (0.2 m wall + 0.1 m of sheathing)."])
def metal_reinforced_wall():
    g = Grid(10, 3, WALL_H)
    _timber_frame(g, y=0)
    _boards(g, y=1)
    M = 2
    # corrugated galvanised sheet, x 0..5, z 0..14
    g.box(0, M, 0, 5, M, 14, "galv")
    for x in range(0, 6, 2):
        g.box(x, M, 0, x, M, 14, "galv_dark")
    g.box(0, M, 14, 5, M, 14, "galv_hi")
    g.box(0, M, 0, 5, M, 0, "rust_deep")
    g.box(3, M, 1, 3, M, 2, "rust_deep")
    # rusty plate lapping the sheet, x 4..9, z 3..12
    g.box(4, M, 3, 9, M, 12, "iron_warm")
    g.box(4, M, 12, 9, M, 12, "steel")
    g.box(4, M, 3, 9, M, 3, "rust_deep")
    g.box(6, M, 4, 9, M, 4, "rust_deep")
    g.box(4, M, 4, 4, M, 12, "steel")                             # lapped edge catches light
    for (x, z) in ((5, 11), (8, 11), (5, 5), (8, 5)):
        g.set(x, M, z, "steel_light")
    g.box(8, M, 7, 8, M, 10, "rust_dark")                         # bleed under a bolt
    # white appliance panel, x 0..6, z 16..22 (dented, chipped at the corners)
    g.box(0, M, 16, 6, M, 22, "almond")
    g.box(0, M, 16, 6, M, 16, "almond_dark")
    g.box(6, M, 16, 6, M, 18, "rust_deep")                        # rust bloom at a cut corner
    g.box(6, M, 22, 6, M, 22, "almond_dark")
    for z in (17, 21):
        for x in (0, 5):
            g.set(x, M, z, "galv_dark")                           # bolts on the stud lines
    # bolt heads on the galvanised sheet along the stud lines
    for z in (2, 7, 12):
        for x in (0, 5):
            if g.get(x, M, z) in (0,):
                continue
            g.set(x, M, z, "steel_dark")
    return g


# =============================================================================================
# Steel (0.05 m): dark painted or mill-scale steel with lit edges, lighter hardware and rust
# where water sits, so the dark masses keep their value structure.
# =============================================================================================
# ---- metal_door ------------------------------------------------------------------------------
@model("metal_door",
       story="A steel security door from a pharmacy's back entrance, rehung in a welded frame "
             "by survivors. The heavy bar latch is scratched bright from use and the bottom "
             "has rusted where rain sat against it.",
       details=["Pressed-steel frame filling the 1.0 x 2.1 m opening",
                "Leaf faced with two riveted cover plates, rivet rows along their edges",
                "Peephole with a steel bezel at eye height",
                "Heavy sliding bar latch in two guide straps, shooting into a keeper on the "
                "frame; its handle and track rubbed bright",
                "Weld-on barrel hinges, rusted kick zone and frame feet"],
       exclusions=["Closed state only", "No signage or text"],
       notes=["Closed. 1.0 x 2.1 m frame, 0.15 m deep; the latch bar stands 5 cm proud "
              "(bounds 0.2 m)."])
def metal_door():
    H = 42
    g = Grid(20, 4, H)
    F = "charcoal"
    g.box(0, 0, 0, 1, 2, H - 1, F)
    g.box(18, 0, 0, 19, 2, H - 1, F)
    g.box(0, 0, H - 2, 19, 2, H - 1, F)
    g.box(0, 2, 0, 0, 2, H - 1, "steel_dark")                   # lit outer arris of the frame
    g.box(19, 2, 0, 19, 2, H - 1, "steel_dark")
    g.box(0, 2, H - 1, 19, 2, H - 1, "steel")
    g.box(2, 0, 0, 17, 2, 0, "steel_dark")                      # steel threshold
    g.box(0, 2, 0, 1, 2, 2, "rust_deep")                        # rusted frame feet
    g.box(18, 2, 0, 19, 2, 1, "rust_deep")
    # leaf (2 cells), painted blue-grey
    L, LP = "bluegrey_deep", "bluegrey_dark"
    g.box(2, 0, 1, 17, 1, H - 3, L)
    for (z0, z1) in ((2, 18), (22, 38)):                         # riveted cover plates (y 2)
        g.box(3, 2, z0, 16, 2, z1, LP)
        g.box(3, 2, z1, 16, 2, z1, "bluegrey")                  # lit top edge
        for x in range(4, 16, 3):
            g.set(x, 2, z0 + 1, "steel_light")
            g.set(x, 2, z1 - 1, "steel_light")
        for z in range(z0 + 4, z1 - 1, 4):
            g.set(4, 2, z, "steel_light")
            g.set(15, 2, z, "steel_light")
    # wear: rust along the bottom of the leaf and lower plate
    g.box(2, 1, 1, 17, 1, 1, "rust_deep")
    g.box(3, 2, 2, 16, 2, 2, "rust_deep")
    g.box(5, 2, 3, 7, 2, 3, "rust_deep")
    g.box(11, 2, 3, 13, 2, 3, "rust_dark")
    # peephole at ~1.55 m
    g.box(9, 2, 30, 11, 2, 32, "steel")
    g.set(10, 2, 31, "black")
    # barrel hinges on the hinge stile (high X)
    for z0 in (5, 33):
        g.box(17, 2, z0, 17, 2, z0 + 3, "iron_edge")
        g.set(17, 2, z0 + 3, "steel")
    # bar latch across the gap between the plates (z 20), proud at y 3
    g.box(3, 3, 20, 19, 3, 20, "steel")
    g.box(3, 3, 20, 3, 3, 22, "steel_light")                     # handle, turned up
    for x in (6, 13):                                            # guide straps
        g.box(x, 2, 19, x, 3, 19, "iron")
        g.box(x, 2, 21, x, 3, 21, "iron")
    g.box(18, 3, 19, 19, 3, 21, "iron")                          # keeper on the frame
    g.box(18, 3, 20, 19, 3, 20, "steel")
    g.box(4, 2, 20, 12, 2, 20, "steel_hi")                       # track rubbed bright
    g.set(3, 2, 25, "brass_dark")                                # lock cylinder
    return g


# ---- metal_support_beam ----------------------------------------------------------------------
@model("metal_support_beam",
       story="A rolled-steel column salvaged from a collapsed carport and stood up again on new "
             "bolts. Its paint is long gone; rust has taken the foot where water pooled and "
             "runs down from the cap plate.",
       details=["0.25 m I-section column: two flanges and a web, open sides to +/-X",
                "Base and cap end plates with four nuts each, fillet welds at the joints",
                "Mill-scale dark steel with lit flange edges; rust at the foot and streaks "
                "from the cap"],
       exclusions=["No paint", "No beam on top (separate module)"],
       notes=["Stands as a 2.55 m column (reference 0.23 x 0.23 x 2.46 m); end plates "
              "0.35 m square."])
def metal_support_beam():
    H = 51
    g = Grid(7, 7, H)
    B = "iron"
    g.box(0, 0, 0, 6, 6, 0, "iron_dark")                         # base plate
    g.box(0, 0, H - 1, 6, 6, H - 1, "iron_dark")                 # cap plate
    g.box(0, 0, H - 1, 6, 0, H - 1, "iron_edge")
    g.box(0, 6, 0, 6, 6, 0, "iron_edge")
    for z in (1, H - 2):                                         # nuts on both plates
        for (x, y) in ((0, 0), (6, 0), (0, 6), (6, 6)):
            g.set(x, y, z, "steel_dark")
    g.box(1, 1, 1, 5, 1, H - 2, B)                               # back flange
    g.box(1, 5, 1, 5, 5, H - 2, B)                               # front flange
    g.box(3, 2, 1, 3, 4, H - 2, "iron_dark")                     # web
    for x in (1, 5):                                             # flange tips catch the light
        g.box(x, 1, 1, x, 1, H - 2, "iron_edge")
        g.box(x, 5, 1, x, 5, H - 2, "iron_edge")
    g.paint(1, 1, 1, 5, 5, 1, "steel_dark")                      # fillet weld at the base
    g.paint(1, 1, H - 2, 5, 5, H - 2, "steel_dark")              # and under the cap
    # rust: the foot where water pooled, a few runs from the cap down the front flange
    g.paint(1, 1, 2, 5, 5, 5, "rust_deep")
    g.paint(1, 5, 6, 3, 5, 8, "rust_deep")
    g.paint(2, 2, 2, 4, 4, 6, "rust_dark")
    g.paint(0, 0, 0, 6, 6, 0, "rust_deep")
    g.box(1, 0, 0, 5, 0, 0, "iron_dark")
    for (x, z0, z1) in ((2, 38, 48), (4, 43, 48)):
        g.paint(x, 5, z0, x, 5, z1, "rust_deep")
    g.paint(1, 1, 46, 5, 1, 48, "rust_deep")
    return g


# ---- steel_reinforcement_panel ---------------------------------------------------------------
@model("steel_reinforcement_panel",
       story="Cut from a road-plate by a welder in the group and framed in angle iron so it can "
             "be bolted over a window or a weak wall. Grinder marks still show where the cut "
             "was dressed.",
       details=["Steel plate set in a perimeter angle-iron frame (L profile visible at the ends)",
                "A horizontal mid rail and one diagonal flat-bar brace welded corner to corner",
                "Bolt holes drilled right through the frame's flat leg",
                "Weld beads at the brace ends, a ground-bright cut edge, rust along the bottom"],
       exclusions=["No mounting bolts (the holes are empty)"],
       notes=["1.0 x 2.3 m, 0.1 m deep including the frame."])
def steel_reinforcement_panel():
    W, H = 20, 46
    g = Grid(W, 2, H)
    g.box(0, 0, 0, W - 1, 0, H - 1, "steel")                     # plate (y 0)
    # angle frame: outstanding leg (outer ring, y 0..1), flat leg (inner ring on the plate)
    for (x0, x1, z0, z1) in ((0, 0, 0, H - 1), (W - 1, W - 1, 0, H - 1),
                             (0, W - 1, 0, 0), (0, W - 1, H - 1, H - 1)):
        g.box(x0, 0, z0, x1, 1, z1, "iron")
    for (x0, x1, z0, z1) in ((1, 1, 1, H - 2), (W - 2, W - 2, 1, H - 2),
                             (1, W - 2, 1, 1), (1, W - 2, H - 2, H - 2)):
        g.box(x0, 0, z0, x1, 0, z1, "iron_dark")
    g.box(0, 1, H - 1, W - 1, 1, H - 1, "iron_edge")             # lit top of the frame
    g.box(W - 1, 1, 0, W - 1, 1, H - 1, "iron_edge")
    # bolt holes through the flat leg
    for z in range(5, H - 3, 8):
        for x in (1, W - 2):
            g.set(x, 0, z, 0)
    for x in (5, 10, 14):
        for z in (1, H - 2):
            g.set(x, 0, z, 0)
    # diagonal flat-bar brace, corner to corner, welded
    g.box(1, 1, 22, W - 2, 1, 23, "iron")                        # mid rail (angle, leg out)
    g.box(1, 1, 23, W - 2, 1, 23, "iron_edge")
    _band_xz(g, 3, 2, W - 4, H - 3, 1, 1, "iron_dark", w=3)
    for (x, z) in ((3, 2), (W - 4, H - 3)):                      # weld beads at the brace ends
        g.box(x - 1, 1, z, x + 1, 1, z, "iron_edge")
    # plate surface: the dressed cut edge along the top is brighter, rust along the bottom
    g.box(2, 0, H - 3, W - 3, 0, H - 3, "steel_light")
    g.box(2, 0, 2, W - 3, 0, 3, "rust_dark")
    g.box(4, 0, 4, 8, 0, 4, "rust_deep")
    g.box(0, 1, 0, W - 1, 1, 0, "rust_deep")
    return g


# ---- metal_fence_gate ------------------------------------------------------------------------
@model("metal_fence_gate",
       story="A welded tube gate from a builder's yard, hung between two square posts across a "
             "driveway. The latch broke long ago, so it is held with a chain and a brass "
             "padlock that has rubbed the paint off the stile.",
       details=["Two 0.1 m square-tube posts with caps",
                "Tube frame with top, middle and bottom rails, vertical bars every 0.1 m",
                "45-degree brace in the lower panel from the bottom hinge corner up to the "
                "middle rail",
                "Barrel hinges, chain wrapped round stile and post, hanging brass padlock",
                "Dark green paint worn to rust at the welds and bottom rail, bright where the "
                "chain rubs"],
       exclusions=["No barbed wire", "Closed state only"],
       notes=["1.15 x 2.0 m including both posts, 0.15 m deep with the chain."])
def metal_fence_gate():
    W, H = 23, 40
    g = Grid(W, 3, H)
    P, Pd = "green_dark", "green_deep"
    for x0 in (0, W - 2):                                         # posts
        g.box(x0, 0, 0, x0 + 1, 1, H - 2, Pd)
        g.box(x0 + 1, 1, 0, x0 + 1, 1, H - 2, P)                  # lit front arris
        g.box(x0, 0, H - 1, x0 + 1, 1, H - 1, "charcoal")         # cap
        g.box(x0, 0, 0, x0 + 1, 1, 1, "rust_deep")                # rusted at the ground
    # leaf x 3..19 in the y 1 plane; latch stile at x 3 (camera side), hinges at x 19/20
    X0, X1, Z0, Z1, ZM = 3, 19, 2, 37, 19
    Y = 1
    for z in (Z0, ZM, Z1):
        g.box(X0, Y, z, X1, Y, z, P)                              # rails
    g.box(X0, Y, Z0, X0, Y, Z1, P)                                # latch stile
    g.box(X1, Y, Z0, X1, Y, Z1, P)                                # hinge stile
    for x in range(X0 + 2, X1, 2):                                # vertical bars
        g.box(x, Y, Z0 + 1, x, Y, Z1 - 1, Pd)
    for (x, z) in _path4(X1 - 1, Z0 + 1, X0 + 1, ZM - 1):          # 45-degree brace, lower panel
        g.set(x, Y, z, P)
    g.box(X0, Y, Z1, X1, Y, Z1, "green")                          # top rail catches the light
    # hinges bridging the gap to the hinge post
    for z0 in (5, 31):
        g.box(20, 0, z0, 20, 1, z0 + 2, "charcoal")
        g.set(20, 1, z0 + 2, "steel")
    # wear: rust on the bottom rail and its welds, paint rubbed where hands push the top rail
    g.box(X0, Y, Z0, X1, Y, Z0, "rust_dark")
    for x in range(X0 + 2, X1, 4):
        g.set(x, Y, Z0 + 1, "rust_deep")
    g.box(X0, Y, Z1, X0 + 4, Y, Z1, "green_light")
    # chain wrapped round the latch stile and post, brass padlock hanging in front
    for x in range(0, X0 + 2):
        g.set(x, 2, 21, "steel" if x % 2 else "steel_dark")
    g.set(X0 + 1, 2, 20, "steel")
    g.set(X0 + 1, 2, 22, "steel_dark")
    g.box(X0, Y, 20, X0, Y, 22, "steel_light")                   # paint rubbed off by the chain
    g.box(1, 2, 20, 1, 2, 22, "steel_dark")
    g.box(2, 2, 18, 2, 2, 20, "steel_light")                      # shackle
    g.box(1, 2, 16, 2, 2, 17, "brass")                            # padlock body
    g.box(1, 2, 16, 2, 2, 16, "brass_dark")
    return g
