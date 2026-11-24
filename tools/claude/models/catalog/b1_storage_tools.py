"""Batch B1 - workshop storage and hand tools (creator: Claude).

X right, Y front (+Y), Z up; inclusive cell ranges.
Hand tools lie on their side as they would rest on a bench or the ground: handle along Y,
working end at +Y, lowest point on z = 0, and a 'grip' attachment where the main hand holds.
Shared hand-tool woods: pale hickory/ash ("sawdust", "pine_hi", "pine_light") darkened by
hands at the grip ("pine_aged", "pine_mid"); forged heads in "charcoal"/"iron" with bright
worn edges, so every tool in the family reads the same way at the game camera.
"""
import math

from catalog_registry import model
from voxkit import Grid

LIES_FLAT = ("Lies on its side as it would rest on a bench: handle along Y, working end at +Y, "
             "lowest point on z = 0. Rotate to the hand for a held pose.")
THIN_Z = ("Height (Z) is the tool's real thickness lying on its side; the reference's larger "
          "Z is a coarse-cell minimum.")


def _fline(g, p0, p1, c):
    """Line between two cells that steps one axis at a time, so every cell shares a face
    with the next (voxkit's Grid.line can step diagonally)."""
    x, y, z = p0
    g.set(x, y, z, c)
    n = max(abs(p1[0] - x), abs(p1[1] - y), abs(p1[2] - z))
    for t in range(1, n + 1):
        tgt = [round(p0[k] + (p1[k] - p0[k]) * t / n) for k in range(3)]
        for k in range(3):
            while (x, y, z)[k] != tgt[k]:
                step = 1 if tgt[k] > (x, y, z)[k] else -1
                if k == 0:
                    x += step
                elif k == 1:
                    y += step
                else:
                    z += step
                g.set(x, y, z, c)


def _arc_cells(cx, cy, r_in, r_out, a0, a1):
    """Cells (i, j) whose centres lie in an annulus sector (degrees, counter-clockwise from +X)."""
    out = []
    for i in range(int(cx - r_out) - 1, int(cx + r_out) + 2):
        for j in range(int(cy - r_out) - 1, int(cy + r_out) + 2):
            dx, dy = i + 0.5 - cx, j + 0.5 - cy
            d = math.hypot(dx, dy)
            a = math.degrees(math.atan2(dy, dx)) % 360
            if r_in <= d <= r_out and a0 <= a <= a1:
                out.append((i, j, a, d))
    return out


# =====================================================================================
# Hand tools
# =====================================================================================
@model("hammer",
       story="The everyday claw hammer from a kitchen drawer, now the one that builds every "
             "barricade. Years of the same hand have darkened the hickory grip; the face is "
             "polished bright and the black paint has worn off the claw from pulling nails.",
       details=["Hickory handle with a slight butt swell and a hand-darkened grip",
                "Black-painted head with a polished round striking face",
                "Curved split claw worn to bare steel on the inside",
                "Handle end grain and wedge visible in the top of the eye"],
       exclusions=["No brand stamp or sticker", "No fibreglass/rubber handle"],
       notes=["Claw hammer with hickory handle and steel head, grip darkened by hands.", THIN_Z],
       front_note=LIES_FLAT + " The claw faces -X (camera side), the striking face +X.",
       attachments={"grip": {"description": "Main hand around the darkened lower handle, "
                                            "about 8 cm from the butt."}})
def hammer():
    g = Grid(12, 31, 3)
    # handle: 3 cells wide in the swing plane, 2 thick; pale hickory with a grain stripe
    g.box(5, 0, 0, 7, 27, 1, "sawdust")
    g.paint(6, 0, 1, 6, 27, 1, "pine_hi")
    g.box(5, 0, 0, 7, 1, 2, "pine_mid")                  # butt swell, one cell fuller
    g.paint(5, 0, 0, 7, 0, 2, "pine_aged")               # end grain
    g.paint(5, 2, 0, 7, 10, 1, "pine_aged")              # grip darkened by hands
    g.paint(6, 3, 1, 6, 9, 1, "pine_mid")                # ...polished a little on the crown
    g.paint(5, 11, 0, 7, 12, 1, "pine_mid")              # grime fades out
    # head: eye boss collars the handle; top of the head is y = 30
    g.box(4, 27, 0, 8, 30, 2, "charcoal")
    g.clear(4, 27, 0, 4, 27, 2)                          # soften the collar corners
    g.clear(8, 27, 0, 8, 27, 2)
    g.box(9, 28, 0, 9, 30, 1, "charcoal")                # neck, slimmer
    g.box(10, 28, 0, 11, 30, 2, "charcoal")              # bell
    g.paint(11, 28, 0, 11, 30, 2, "steel_hi")            # polished striking face
    g.paint(10, 28, 0, 10, 30, 2, "steel")               # worn bevel behind the face
    # claw sweeps back toward the handle; split tip, paint rubbed off its inner edge
    for x, (y0, y1) in {3: (28, 30), 2: (28, 30), 1: (27, 29), 0: (26, 28)}.items():
        g.box(x, y0, 0, x, y1, 2, "charcoal")
    for (x, y) in [(1, 27), (0, 26)]:
        g.paint(x, y, 0, x, y, 2, "steel")               # inner edge that bears on nails
    g.paint(0, 26, 1, 0, 26, 1, "steel_dark")            # the V slot between the tines
    return {"grid": g, "attachments": {"grip": (6, 6, 1)}}


@model("crowbar", cell=0.0125,
       why="A 2.5 cm hex bar is one cell at 2.5 cm, too thin to show the gooseneck's taper, the "
           "split claw or the flattened pry end; at 1.25 cm the bar is 2x2 cells and the hook "
           "is a smooth 8-cell curve. Matches the other small hand tools of the family.",
       story="A wrecking bar from a builder's van, used to pry open sheds, car boots and boarded "
             "doors. The dusty-red paint survives only along the middle of the bar; the hook "
             "and the pry end are rubbed back to dark steel.",
       details=["2x2-cell bar with a gooseneck hook ending in a split nail claw",
                "Flattened chisel pry end",
                "Paint worn off at the fulcrum of the hook, the claw and the pry end",
                "One coherent chipped zone where it was hammered on"],
       exclusions=["No hex facets (below cell size)", "No text or brand"],
       notes=["Hex-bar crowbar with a curved claw end and chipped dusty-red paint.", THIN_Z],
       front_note=LIES_FLAT + " The gooseneck lies flat with its claw pointing back toward "
                              "the bar.",
       attachments={"grip": {"description": "Main hand on the bar about a third of the way "
                                            "from the pry end."}})
def crowbar():
    g = Grid(9, 56, 3)
    cx, cy, R = 4.0, 51.0, 3.0                            # bar centreline x = 7.0
    g.box(6, 3, 0, 7, 50, 1, "red")                       # straight bar
    # pry end: flattened to one cell and slightly widened
    g.box(6, 0, 0, 7, 2, 0, "steel_dark")
    g.box(6, 3, 0, 7, 5, 1, "steel_dark")
    g.paint(6, 0, 0, 7, 0, 0, "steel_light")              # sharpened edge
    # gooseneck hook, the claw end thinning as it turns back toward the bar
    arc = _arc_cells(cx, cy, R - 1.0, R + 1.0, 0, 222)
    for (i, j, a, d) in arc:
        if a > 175 and d < R - 0.3:
            continue
        g.box(i, j, 0, i, j, 1, "red")
    # paint worn through where the hook bears and on the claw
    for (i, j, a, d) in arc:
        if a > 165:
            g.paint(i, j, 0, i, j, 1, "steel_dark")
        elif 75 < a < 125 and d > R:
            g.paint(i, j, 0, i, j, 1, "red_dark")         # fulcrum, rubbed thin
    for (i, j, a, d) in arc:
        if a > 210:
            g.paint(i, j, 0, i, j, 1, "steel")            # bright split claw tip
    # worn paint near the pry end and one hammered zone mid-bar
    g.paint(6, 6, 0, 7, 8, 1, "red_dark")
    for (x, y) in [(6, 6), (7, 7), (6, 9)]:
        g.paint(x, y, 1, x, y, 1, "steel_dark")
    g.paint(6, 30, 1, 7, 32, 1, "red_dark")
    g.paint(7, 31, 1, 7, 31, 1, "steel_dark")
    return {"grid": g, "attachments": {"grip": (7, 16, 1)}}


@model("hatchet",
       story="A camping hatchet that became the household's firewood axe. Missed swings "
             "chewed the handle under the head, so someone wrapped the grip in black tape; "
             "the head was left out in the rain and has rusted around the eye and poll.",
       details=["Bearded steel head with a bright sharpened edge",
                "Rust gathered around the eye and the poll, not over the whole head",
                "Ash handle with a flared knob, black tape wrapped over the grip",
                "Overstrike bruising on the handle just under the head"],
       exclusions=["No leather sheath", "No brand stamp"],
       notes=["Hatchet with tape-wrapped wooden handle and a rust-flecked steel head.", THIN_Z],
       front_note=LIES_FLAT + " The bit faces -X (camera side), the poll +X.",
       attachments={"grip": {"description": "Main hand on the taped grip just above the knob."}})
def hatchet():
    g = Grid(16, 35, 3)
    HX0, HX1 = 10, 12                                     # handle columns
    g.box(HX0, 1, 0, HX1, 30, 1, "pine_light")
    g.paint(11, 1, 1, 11, 30, 1, "pine_hi")               # grain stripe
    g.box(9, 0, 0, 12, 1, 1, "pine_mid")                  # fawn-foot knob, flares to the bit side
    g.paint(9, 0, 0, 12, 0, 1, "pine_aged")
    # black tape over the grip; overlapping turns read as darker seams
    g.paint(HX0, 2, 0, HX1, 12, 1, "charcoal")
    for y in (4, 7, 10):
        g.paint(HX0, y, 0, HX1, y, 1, "black")
    g.set(13, 12, 0, "charcoal")                          # loose tape end lifting off
    # overstrike bruising just under the head
    g.paint(HX0, 25, 0, HX1, 27, 1, "pine_aged")
    g.paint(HX0, 26, 0, HX0, 27, 1, "pine_dark")
    # head: bare forged steel; eye collars the handle, poll +X, bearded bit -X
    g.box(9, 28, 0, 13, 33, 2, "steel_dark")
    g.box(14, 29, 0, 15, 32, 2, "steel_dark")             # flat poll
    bit = {8: (28, 33), 7: (28, 33), 6: (28, 33), 5: (27, 33), 4: (27, 33), 3: (26, 33),
           2: (25, 34), 1: (25, 34), 0: (26, 33)}
    for x, (y0, y1) in bit.items():
        g.box(x, y0, 0, x, y1, 1 if x >= 6 else 0, "steel_dark")
    g.paint(2, 0, 0, 2, 40, 0, "steel")                   # grinding bevel
    g.paint(0, 0, 0, 1, 40, 0, "steel_hi")                # sharpened edge
    g.paint(15, 29, 0, 15, 32, 2, "steel")                # poll face, struck smooth
    # rust where water sat: on top of the eye toward the poll and along the beard's top
    for (x, y, z, c) in [(12, 33, 2, "rust_deep"), (13, 33, 2, "rust_dark"),
                         (13, 32, 2, "rust_deep"), (14, 32, 2, "rust_dark"),
                         (14, 31, 2, "rust_deep"), (13, 28, 2, "rust_deep"),
                         (12, 28, 2, "rust_deep"), (8, 33, 1, "rust_deep"),
                         (7, 33, 1, "rust_dark"), (6, 33, 1, "rust_deep"),
                         (5, 27, 0, "rust_deep"), (4, 27, 0, "rust_deep")]:
        g.paint(x, y, z, x, y, z, c)
    g.paint(11, 33, 1, 11, 33, 1, "pine_aged")            # handle end grain in the eye
    return {"grid": g, "attachments": {"grip": (11, 6, 1)}}



@model("shovel",
       story="The garden shovel that dug the latrine and the graves behind the house. Dried "
             "clay is caked at the tip and in the corners of the blade; the paint has worn "
             "off the cutting edge and the ash shaft is dark where two hands always hold it.",
       details=["Round-point dished blade with turned steps for the boot",
                "Riveted socket on an ash shaft",
                "Wooden D-grip with a steel Y-ferrule",
                "Dried clay at the tip and in the step corners, bare steel at the edge"],
       exclusions=["No fresh wet mud", "No brand sticker"],
       notes=["Round-point shovel with a wooden shaft and D-grip, dried dirt on the blade.",
              "Lies on its back with the dished face up; the shaft rests one cell above "
              "the ground between blade and grip, as a real shovel does. " + THIN_Z],
       front_note=LIES_FLAT,
       attachments={"grip": {"description": "Main hand on the D-grip crossbar; the other hand "
                                            "low on the shaft."}})
def shovel():
    g = Grid(8, 46, 3)
    # D-grip (y 0..4) lying flat; crossbar at y 0 darkened by the hand
    g.box(1, 0, 0, 6, 0, 1, "pine_aged")
    g.box(1, 1, 0, 1, 3, 1, "pine_mid")
    g.box(6, 1, 0, 6, 3, 1, "pine_mid")
    g.box(1, 4, 0, 6, 4, 1, "pine_mid")
    g.clear(1, 4, 1, 1, 4, 1)                             # rounded shoulders of the D
    g.clear(6, 4, 1, 6, 4, 1)
    g.box(2, 5, 0, 5, 6, 2, "iron")                       # steel Y-ferrule
    g.paint(2, 6, 2, 5, 6, 2, "steel_dark")
    # shaft, 2x2 cells, resting one cell up between grip and blade
    g.box(3, 7, 1, 4, 30, 2, "pine_light")
    g.paint(3, 7, 2, 3, 30, 2, "pine_hi")                 # grain stripe
    g.paint(3, 7, 1, 4, 11, 2, "pine_aged")               # upper hand
    g.paint(3, 22, 1, 4, 26, 2, "pine_mid")               # lower hand
    # socket (frog), riveted
    g.box(2, 28, 0, 5, 32, 2, "iron")
    g.box(3, 27, 1, 4, 27, 2, "iron")
    g.clear(2, 28, 2, 2, 29, 2)
    g.clear(5, 28, 2, 5, 29, 2)
    g.set(3, 30, 2, "steel_light")                        # rivet
    # blade: painted muted green, turned step at y 33, round point at y 45
    rows = {y: (0, 7) for y in range(33, 42)}
    rows.update({42: (1, 6), 43: (1, 6), 44: (2, 5), 45: (3, 4)})
    for y, (x0, x1) in rows.items():
        g.box(x0, y, 0, x1, y, 0, "green_dark")
    g.box(0, 33, 0, 7, 33, 1, "green_deep")               # turned step
    g.paint(0, 33, 1, 1, 33, 1, "steel")                  # boot-worn step ends
    g.paint(6, 33, 1, 7, 33, 1, "steel")
    # paint worn back to steel around the cutting edge
    for y, (x0, x1) in rows.items():
        if y >= 43:
            g.paint(x0, y, 0, x1, y, 0, "steel")
        if y >= 40:
            g.paint(x0, y, 0, x0, y, 0, "steel")
            g.paint(x1, y, 0, x1, y, 0, "steel")
    g.paint(2, 44, 0, 5, 45, 0, "steel_light")
    # dried clay: one crust behind the tip, and packed into the step corners
    g.paint(1, 39, 0, 6, 42, 0, "card_dark")
    g.paint(1, 39, 0, 1, 39, 0, "green_dark")
    g.paint(6, 39, 0, 6, 40, 0, "green_dark")
    g.paint(2, 42, 0, 4, 42, 0, "card_deep")
    g.paint(3, 40, 0, 4, 41, 0, "card")
    g.paint(1, 34, 0, 1, 36, 0, "card_deep")
    g.paint(6, 34, 0, 6, 35, 0, "card_deep")
    return {"grid": g, "attachments": {"grip": (3, 0, 1)}}



@model("pickaxe",
       story="A pick from the landscaping company's yard, taken to dig through the frozen "
             "verge and later to quarry stone. The head is rusted where it lay in the wet, the "
             "point and chisel are scraped bright, and the haft is grey from weather.",
       details=["Curved head: long point on one side, chisel on the other",
                "Rust on the arms, bright steel at the point and chisel edge",
                "Weathered ash haft with a swelled butt and a darker grip",
                "Splintered overstrike zone under the head"],
       exclusions=["No fantasy double-axe head", "No brand"],
       notes=["Pickaxe with a long wooden haft and a pointed/chisel head.", THIN_Z],
       front_note=LIES_FLAT + " The point faces -X (camera side), the chisel +X.",
       attachments={"grip": {"description": "Main hand near the butt swell; the other hand "
                                            "slides up the haft."}})
def pickaxe():
    g = Grid(20, 34, 3)
    # weathered ash haft 2x2, y 0..32, swelled butt
    g.box(9, 0, 0, 10, 32, 1, "wgrey_warm")
    g.paint(9, 0, 1, 9, 32, 1, "wgrey_hi")                # weathered crown / grain
    g.box(8, 0, 0, 11, 1, 1, "wgrey_warm")
    g.paint(8, 0, 0, 11, 0, 1, "wgrey_mid")               # end grain
    g.paint(9, 2, 0, 10, 8, 1, "pine_aged")               # grip, darkened
    g.paint(9, 25, 0, 10, 28, 1, "wgrey_hi")              # splintered overstrike
    g.set(8, 27, 0, "wgrey_hi")                           # a lifted splinter
    # head: eye, a long curved point (-X) and a chisel that widens across (+X)
    g.box(8, 29, 0, 11, 33, 2, "iron")
    pick = {7: (30, 32, 1), 6: (30, 31, 1), 5: (30, 31, 1), 4: (29, 30, 1), 3: (29, 30, 1),
            2: (28, 29, 1), 1: (28, 28, 0), 0: (28, 28, 0)}
    chisel = {12: (30, 32, 1), 13: (30, 31, 1), 14: (30, 31, 1), 15: (29, 30, 1),
              16: (29, 30, 1), 17: (29, 30, 2), 18: (28, 29, 2), 19: (28, 28, 2)}
    for arm in (pick, chisel):
        for x, (y0, y1, z1) in arm.items():
            g.box(x, y0, 0, x, y1, z1, "iron")
    # rust gathered on the upper faces near the eye; working ends scraped bright
    for (x, y) in [(4, 29), (5, 30), (5, 31), (6, 30), (6, 31), (7, 31), (13, 30), (13, 31),
                   (14, 31), (15, 30), (12, 31)]:
        g.paint(x, y, 1, x, y, 1, "rust_deep")
    for (x, y) in [(5, 30), (14, 30), (6, 31)]:
        g.paint(x, y, 1, x, y, 1, "rust_dark")
    g.paint(0, 28, 0, 1, 28, 0, "steel_light")
    g.paint(2, 29, 0, 2, 29, 1, "steel")
    g.paint(19, 28, 0, 19, 28, 2, "steel_light")
    g.paint(18, 28, 0, 18, 29, 2, "steel")
    g.paint(8, 33, 0, 11, 33, 2, "iron_edge")             # top of the eye, struck smooth

    return {"grid": g, "attachments": {"grip": (9, 4, 1)}}



@model("saw",
       story="A panel saw from a retired neighbour's workshop, still sharp. The beech handle "
             "has gone dark and glossy where the fingers wrap; a little rust has bloomed near "
             "the toe where it hung on a damp shed wall.",
       details=["Closed D-handle with a hand hole and three brass saw nuts",
                "Blade tapering from heel to toe with a serrated tooth edge",
                "Straight spine; light rust bloom near the toe"],
       exclusions=["No etched logo", "No teeth finer than a cell (stylised serration)"],
       notes=["Hand saw with a wooden D-handle and a tapering blade.", THIN_Z],
       front_note=LIES_FLAT + " Teeth toward -X (camera side), spine toward +X.",
       attachments={"grip": {"description": "Fingers through the hand hole around the rear "
                                            "grip of the D-handle."}})
def saw():
    g = Grid(10, 55, 2)
    # blade (z 0): spine at x 8, tooth edge tapering from x 1 (heel) to x 5 (toe)
    for y in range(9, 55):
        xe = 1 + round(4 * (y - 9) / 45)
        g.box(xe, y, 0, 8, y, 0, "steel_light")
        g.set(8, y, 0, "steel")                            # spine
        if y % 2:
            g.set(xe, y, 0, "steel")                       # tooth
        else:
            g.set(xe, y, 0, 0)                             # gullet
            g.set(xe + 1, y, 0, "steel")
    g.box(5, 54, 0, 8, 54, 0, "steel")                     # square toe
    for (x, y) in [(6, 50), (7, 50), (6, 51), (7, 52), (6, 52), (5, 51), (7, 51)]:
        g.set(x, y, 0, "rust_dark")                        # rust bloom near the toe
    # closed D-handle (z 0..1): top horn behind the spine, slanted grip, hand hole
    rows = {0: [(6, 9)], 1: [(3, 9)], 2: [(1, 9)], 3: [(0, 9)], 4: [(0, 1), (8, 9)],
            5: [(0, 1), (8, 9)], 6: [(0, 1), (8, 9)], 7: [(0, 9)], 8: [(0, 9)], 9: [(0, 9)],
            10: [(0, 9)], 11: [(0, 9)], 12: [(1, 9)]}
    for y, spans in rows.items():
        for (x0, x1) in spans:
            g.box(x0, y, 0, x1, y, 1, "pine_mid")
    g.paint(0, 0, 0, 9, 12, 0, "pine_aged")                # lower face / edges
    g.paint(1, 1, 1, 7, 3, 1, "wood_stain")                # grip glossed dark by fingers
    g.paint(2, 2, 1, 6, 2, 1, "pine_dark")
    g.paint(6, 0, 1, 9, 0, 1, "pine_aged")                 # thumb-rubbed horn
    for (x, y) in [(2, 10), (7, 10), (5, 12)]:
        g.set(x, y, 1, "brass_hi")                         # saw nuts
    return {"grid": g, "attachments": {"grip": (4, 2, 1)}}


# =====================================================================================
# Storage
# =====================================================================================
@model("wooden_storage_crate",
       story="Knocked together in the garage from backyard fence boards, a pallet and one "
             "sage-painted kitchen cabinet panel. The lid swings on two strap hinges taken off "
             "the garden gate, and the rope handles are cut from an old washing line.",
       details=["Horizontal boards of four different woods per side, one left long at the "
                "corner", "Rows of nail heads where boards meet the inner corner posts",
                "Three-board lid with a front lip, two gate strap hinges and a hasp",
                "Washing-line rope loops through holes in both ends"],
       exclusions=["No stencilled text or shipping marks", "No gaps between boards (would be "
                   "5 cm slots at this tier)"],
       notes=["Player-built crate of mismatched scavenged boards with a hinged lid and rope "
              "handles; nail heads visible."],
       collision_hint="Box 0.85 x 0.62 x 0.6 m; rope handles and the lid lip are overhangs.")
def wooden_storage_crate():
    g = Grid(18, 13, 12)
    X0, X1, Y0, Y1, TOP = 1, 16, 0, 11, 10
    g.box(X0, Y0, 0, X1, Y1, 0, "pine_dark")                       # floor boards
    left = [(0, 2, "wgrey_mid"), (3, 5, "pine_light"), (6, 8, "pine_aged"), (9, 10, "wgrey")]
    right = [(0, 2, "pine_mid"), (3, 4, "wgrey"), (5, 7, "pine_light"), (8, 10, "pine_aged")]
    front = [(0, 2, "pine_aged"), (3, 5, "wgrey"), (6, 7, "sage_dark"), (8, 10, "pine_light")]
    back = [(0, 2, "pine_mid"), (3, 5, "pine_aged"), (6, 8, "wgrey_mid"), (9, 10, "pine_light")]
    for z0, z1, c in left:
        g.box(X0, Y0, z0, X0, Y1, z1, c)
    for z0, z1, c in right:
        g.box(X1, Y0, z0, X1, Y1, z1, c)
    for z0, z1, c in back:
        g.box(X0, Y0, z0, X1, Y0, z1, c)
    for z0, z1, c in front:                                        # front boards lap the ends
        g.box(X0, Y1, z0, X1, Y1, z1, c)
    g.box(0, Y1, 3, 0, Y1, 5, "wgrey")                             # fence board left long
    g.paint(0, Y1, 3, 0, Y1, 3, "wgrey_mid")
    # the painted cabinet panel: paint rubbed off its ends and lower arris
    g.paint(X0, Y1, 6, X0 + 1, Y1, 7, "pine_aged")
    g.paint(X1 - 1, Y1, 6, X1, Y1, 6, "pine_aged")
    g.paint(X0 + 2, Y1, 6, X1 - 2, Y1, 6, "sage_deep")
    # weathered fence boards darker at the bottom where the crate stands on wet ground
    g.paint(X0, Y1, 0, X1, Y1, 0, "pine_dark")
    g.paint(X0, Y0, 0, X0, Y1, 0, "wgrey_dark")
    # nail heads: one per board end, where they go into the inner corner posts
    for z0, z1, _ in front:
        zc = (z0 + z1) // 2
        g.set(X0 + 1, Y1, zc, "wgrey_deep")
        g.set(X1 - 1, Y1, zc, "wgrey_deep")
    # lid: three boards along X, front lip overhanging by one cell
    lid = [((0, 3), (X0, X1), "pine_light"), ((4, 7), (X0, X1 - 1), "wgrey_hi"),
           ((8, 12), (X0, X1), "pine_mid")]
    for (ya, yb), (xa, xb), c in lid:
        g.box(xa, ya, TOP + 1, xb, yb, TOP + 1, c)
    g.paint(X0, 12, TOP + 1, X1, 12, TOP + 1, "pine_aged")         # lip, hand-darkened
    g.paint(6, 12, TOP + 1, 11, 12, TOP + 1, "pine_dark")
    # gate strap hinges across the lid and down the back
    for hx in (3, 13):
        g.paint(hx, 0, TOP + 1, hx + 1, 4, TOP + 1, "iron")
        g.paint(hx, 5, TOP + 1, hx, 5, TOP + 1, "iron")
        g.paint(hx, 0, TOP - 1, hx + 1, 0, TOP, "iron")
        g.paint(hx + 1, 4, TOP + 1, hx + 1, 4, TOP + 1, "rust_deep")
    # hasp hanging from the lip over a staple
    g.box(8, 12, TOP - 1, 9, 12, TOP, "iron")
    g.set(8, 12, TOP - 1, "rust_deep")
    # rope handles: loops out of two holes in each end
    for x, wall in ((0, X0), (17, X1)):
        for y in (3, 8):
            g.box(x, y, 6, x, y, 8, "khaki")
            g.set(x, y, 8, "khaki_dark")                            # knot through the hole
        g.box(x, 4, 6, x, 7, 6, "khaki")
        g.box(x, 5, 6, x, 6, 6, "khaki_dark")                       # hand-worn grip
    return {"grid": g, "footprint_cells": ((X0, X1), (Y0, Y1))}


@model("metal_storage_cabinet",
       story="Bought for the garage to keep the chemicals and the good tools locked up. "
             "Someone tried to force it with a bar: the right-hand door is dented and the paint is "
             "scraped bright around the handle and hasp, but the padlock held.",
       details=["Two flush doors with a dark centre gap and a recessed plinth",
                "Pressed louvres top and bottom on both doors",
                "Lever handle and a welded hasp with a brass padlock",
                "Crowbar dent in the right-hand door, scrape marks around the handle",
                "Rust creeping up the bottom corners where the floor was wet"],
       exclusions=["No hazard stickers or labels", "No interior shelves (doors closed)"],
       notes=["Grey steel two-door cabinet, one door dented, padlock hasp, louvres, scratches "
              "at the handle."])
def metal_storage_cabinet():
    W, D, H = 17, 9, 37
    g = Grid(W, D + 1, H)
    F = D - 1                                                      # front face row
    g.box(0, 0, 2, W - 1, D - 1, H - 1, "steel_light")             # carcass z 2..36
    g.box(0, 0, 0, W - 1, D - 2, 1, "steel_dark")                  # plinth, front set back
    g.paint(0, 0, 0, W - 1, D - 2, 0, "charcoal")
    g.paint(0, 0, H - 1, W - 1, F, H - 1, "steel_light")
    g.paint(0, F, H - 1, W - 1, F, H - 1, "steel_hi")              # catch-light on the top edge
    g.paint(0, 0, H - 1, 0, F, H - 1, "steel_hi")
    # door frame, the two doors and the centre gap
    g.paint(0, F, 2, W - 1, F, H - 1, "steel")
    g.paint(1, F, 3, 7, F, H - 2, "steel_light")
    g.paint(9, F, 3, 15, F, H - 2, "steel_light")
    g.paint(8, F, 3, 8, F, H - 2, "steel_dark")
    g.paint(0, F, H - 1, W - 1, F, H - 1, "steel_hi")
    # pressed louvres, top and bottom of each door
    for (x0, x1) in ((2, 6), (10, 14)):
        for z in (31, 33, 5, 7):
            g.paint(x0, F, z, x1, F, z, "steel_dark")
    # lever handle on the right door, padlocked hasp across the gap
    g.box(10, F + 1, 16, 10, F + 1, 18, "steel_hi")
    g.set(10, F + 1, 18, "chrome")
    g.box(6, F + 1, 21, 9, F + 1, 21, "steel")                     # hasp over the staple
    g.set(8, F + 1, 20, "steel_hi")                                # padlock shackle
    g.box(8, F + 1, 18, 8, F + 1, 19, "brass")                     # padlock body
    g.set(8, F + 1, 18, "brass_dark")
    # crowbar dent in the left door: pushed in a cell, paint cracked bright around it
    dent = [(3, 12), (4, 12), (2, 13), (3, 13), (4, 13), (5, 13), (3, 14), (4, 14), (5, 14),
            (4, 15), (5, 15), (6, 14)]
    for (x, z) in dent:
        g.clear(x, F, z, x, F, z)
        g.set(x, F - 1, z, "steel")
    for (x, z) in [(2, 12), (2, 14), (3, 15), (6, 15), (6, 13), (5, 12), (4, 16)]:
        g.paint(x, F, z, x, F, z, "steel_hi")
    g.set(5, F - 1, 15, "steel_dark")
    # pry and scrape marks around the gap, the hasp and the handle
    for (x, z) in [(7, 19), (7, 22), (7, 23), (9, 22), (9, 23), (9, 19), (11, 17), (11, 18),
                   (9, 17), (7, 20)]:
        g.paint(x, F, z, x, F, z, "steel_hi")
    g.paint(8, F, 19, 8, F, 23, "charcoal")                        # gap levered open
    # rust creeping up the bottom corners and the plinth
    for (x, z, c) in [(0, 2, "rust_dark"), (0, 3, "rust_deep"), (1, 2, "rust_deep"),
                      (W - 1, 2, "rust_dark"), (W - 2, 2, "rust_deep"), (W - 1, 3, "rust_deep")]:
        g.paint(x, F, z, x, F, z, c)
    for (y, z, c) in [(F - 1, 2, "rust_deep"), (F - 2, 2, "rust_deep"), (F - 1, 3, "rust_dark")]:
        g.paint(0, y, z, 0, y, z, c)
    g.paint(0, F - 1, 0, 3, F - 1, 1, "rust_deep")
    return {"grid": g, "footprint_cells": ((0, W - 1), (0, D - 1))}


@model("tool_chest", cell=0.025,
       why="At 5 cm a 0.47 m chest is nine cells tall: its drawers, pulls and casters would "
           "be single cells. At 2.5 cm the four drawers, full-width pulls, swivel casters "
           "and the open drawer's contents read; the voxel count stays modest.",
       story="A mechanic's rolling chest from the auto shop on the corner, dragged home "
             "for the generator tools. The top drawer was left open with a few spanners in it; "
             "a greasy shop rag still hangs over the side handle.",
       details=["Four drawers with full-width aluminium pulls, the top one pulled open",
                "Spanners and a socket in the open drawer",
                "Ribbed rubber mat on the top", "Four swivel casters",
                "Tube side handle with a greasy rag draped over it",
                "Paint scuffed at the top corners and the kick line"],
       exclusions=["No brand badge or sticker", "No full tool set (loose tools are their own "
                   "models)"],
       notes=["Rolling mechanic's tool chest in dusty red, stacked drawers with one open, "
              "casters, side handle.",
              "Depth includes the open drawer (+0.12 m beyond the closed pulls)."],
       collision_hint="Box 0.8 x 0.36 x 0.475 m on the body; handle, rag and open drawer "
                      "are overhangs.")
def tool_chest():
    g = Grid(35, 20, 20)
    X0, X1, Y0, Y1, Z0, Z1 = 3, 34, 0, 13, 4, 17
    g.box(X0, Y0, Z0, X1, Y1, Z1, "red")
    g.box(X0, Y0, Z1 + 1, X1, Y1, Z1 + 1, "red")                   # top
    g.paint(X0 + 1, Y0 + 1, Z1 + 1, X1 - 1, Y1 - 1, Z1 + 1, "charcoal")   # rubber mat
    for y in range(Y0 + 2, Y1 - 1, 2):
        g.paint(X0 + 1, y, Z1 + 1, X1 - 1, y, Z1 + 1, "iron")      # ribs
    g.paint(X0, Y0, Z0, X1, Y1, Z0, "red_dark")                    # bottom pan
    # front: stiles and four drawers, each with a full-width pull along its top
    g.paint(X0, Y1, Z0, X0, Y1, Z1, "red_dark")
    g.paint(X1, Y1, Z0, X1, Y1, Z1, "red_dark")
    drawers = [(5, 8), (9, 11), (12, 14), (15, 17)]
    for k, (za, zb) in enumerate(drawers):
        g.paint(X0 + 1, Y1, za, X1 - 1, Y1, zb, "red")
        g.paint(X0 + 1, Y1, za, X1 - 1, Y1, za, "red_dark")        # shadow gap under the face
        if k < 3:
            g.box(X0 + 2, Y1 + 1, zb, X1 - 2, Y1 + 1, zb, "chrome")
            g.paint(X0 + 12, Y1 + 1, zb, X1 - 12, Y1 + 1, zb, "steel_light")  # hand-dulled
    # top drawer pulled out 5 cells: steel tray, painted front, contents
    za, zb = drawers[3]
    g.clear(X0 + 1, Y1, za, X1 - 1, Y1, zb)
    g.box(X0 + 1, Y1 - 3, za, X1 - 1, Y1 - 1, za, "charcoal")      # cavity floor in shadow
    OY = Y1 + 5
    g.box(X0 + 2, Y1 - 2, za, X1 - 2, OY - 1, za, "steel_dark")    # drawer bottom
    g.box(X0 + 2, Y1 - 2, za + 1, X0 + 2, OY - 1, za + 1, "steel")  # drawer sides
    g.box(X1 - 2, Y1 - 2, za + 1, X1 - 2, OY - 1, za + 1, "steel")
    g.box(X0 + 1, OY, za, X1 - 1, OY, zb, "red")                   # drawer front
    g.paint(X0 + 1, OY, za, X1 - 1, OY, za, "red_dark")
    g.box(X0 + 2, OY + 1, zb, X1 - 2, OY + 1, zb, "chrome")        # its pull
    g.paint(X0 + 12, OY + 1, zb, X1 - 12, OY + 1, zb, "steel_light")
    # contents: two combination spanners and a socket, lying in the tray
    g.box(8, Y1 + 1, za + 1, 19, Y1 + 1, za + 1, "steel_light")
    g.box(7, Y1, za + 1, 7, Y1 + 2, za + 1, "steel_hi")
    g.box(11, Y1 + 3, za + 1, 21, Y1 + 3, za + 1, "steel_light")
    g.box(22, Y1 + 2, za + 1, 22, Y1 + 4, za + 1, "steel_hi")
    g.box(26, Y1 + 1, za + 1, 27, Y1 + 2, za + 1, "steel")
    # casters
    for cx in (X0 + 1, X1 - 2):
        for cy in (Y0 + 1, Y1 - 2):
            g.box(cx, cy, 3, cx + 1, cy + 1, 3, "steel_dark")      # swivel plate
            g.box(cx, cy, 0, cx, cy + 2, 2, "black")               # wheel
            g.set(cx, cy + 1, 1, "steel")                          # hub
            g.box(cx + 1, cy, 2, cx + 1, cy + 1, 2, "steel_dark")  # fork
    # tube side handle on -X, a greasy rag draped over it
    g.box(1, 3, 13, 2, 3, 13, "chrome")
    g.box(1, 10, 13, 2, 10, 13, "chrome")
    g.box(1, 3, 14, 1, 10, 14, "chrome")
    g.box(0, 5, 15, 2, 8, 15, "blue")                              # shop towel over the bar
    g.box(0, 5, 10, 0, 8, 14, "blue")                              # outer fall
    g.box(0, 8, 8, 0, 8, 9, "blue")                                # one corner hangs lower
    g.box(0, 5, 10, 0, 5, 10, 0)
    g.box(2, 5, 12, 2, 8, 14, "blue_dark")                         # inner fall
    g.paint(0, 6, 10, 0, 6, 14, "blue_mid")                        # fold
    g.paint(0, 7, 11, 0, 8, 13, "blue_deep")                       # oily smear
    g.paint(0, 7, 12, 0, 7, 12, "soot")
    g.paint(0, 5, 15, 2, 6, 15, "blue_hi")
    # wear: scuffed top corners, kicked lower front, chipped stile edges
    for (x, y, z) in [(X0, Y1, Z1 + 1), (X0 + 1, Y1, Z1 + 1), (X0, Y1 - 1, Z1 + 1),
                      (X1, Y1, Z1 + 1), (X1 - 1, Y1, Z1 + 1), (X0, Y0, Z1 + 1)]:
        g.paint(x, y, z, x, y, z, "steel")
    g.paint(X0 + 3, Y1, Z0, X1 - 3, Y1, Z0, "red_deep")
    for (x, z) in [(X0, 10), (X0, 6), (X1, 12)]:
        g.paint(x, Y1, z, x, Y1, z, "red_hi")
    return {"grid": g, "footprint_cells": ((X0, X1), (Y0, Y1))}


@model("toolbox",
       story="The household's blue-grey cantilever toolbox, left open on the floor with "
             "both trays fanned out. Whoever used it last grabbed what they needed and left "
             "the hammer, a screwdriver and a tape measure in the bottom.",
       details=["Steel base box with two trays raised out on linkage arms at each end",
                "Fixed carry handle bridging the ends, black grip sleeve",
                "Hammer, screwdriver, spanner and tape measure in the base",
                "Screws, a pencil and pliers in the trays",
                "Chipped paint on the rims, a little rust at the bottom corners"],
       exclusions=["No brand plate or sticker", "Distinct from the red box on the pilot "
                   "workbench"],
       notes=["Blue-grey steel cantilever toolbox with the trays opened, a few tool handles "
              "visible (distinct from the red box on the pilot workbench).",
              "Depth includes both trays fanned open (closed it would be 0.15 m deep)."],
       collision_hint="Box 0.48 x 0.15 x 0.14 m on the base; trays and handle are overhangs.")
def toolbox():
    g = Grid(40, 22, 18)
    BX0, BX1, BY0, BY1, BZ1 = 1, 38, 6, 15, 10
    body, rim, inside = "bluegrey", "bluegrey_hi", "bluegrey_deep"
    # base: open-top steel box
    g.box(BX0, BY0, 0, BX1, BY1, BZ1, body)
    g.clear(BX0 + 1, BY0 + 1, 1, BX1 - 1, BY1 - 1, BZ1)
    g.paint(BX0 + 1, BY0 + 1, 0, BX1 - 1, BY1 - 1, 0, inside)
    g.paint(BX0, BY0, BZ1, BX1, BY1, BZ1, rim)                      # rolled rim
    g.paint(BX0, BY0, 0, BX1, BY1, 0, "bluegrey_dark")
    for (x, y) in [(BX0, BY1), (BX1, BY1), (BX0, BY0), (BX0 + 1, BY1)]:
        g.paint(x, y, 0, x, y, 1, "rust_dark")                      # rust at the feet
    # trays swung out level on the parallelogram arms, one each side of the open base
    trays = [(BY1 + 1, BY1 + 5), (BY0 - 5, BY0 - 1)]
    for (ty0, ty1) in trays:
        g.box(BX0, ty0, BZ1, BX1, ty1, BZ1 + 2, body)
        g.clear(BX0 + 1, ty0 + 1, BZ1 + 1, BX1 - 1, ty1 - 1, BZ1 + 2)
        g.paint(BX0 + 1, ty0 + 1, BZ1, BX1 - 1, ty1 - 1, BZ1, inside)
        g.paint(BX0, ty0, BZ1 + 2, BX1, ty1, BZ1 + 2, rim)
        g.paint(BX0, ty0, BZ1, BX1, ty1, BZ1, "bluegrey_dark")       # tray underside
        for dx in (13, 26):                                          # dividers
            g.box(dx, ty0 + 1, BZ1 + 1, dx, ty1 - 1, BZ1 + 1, "bluegrey_dark")
    # linkage arms on both ends: base pivots low in the middle, tray pivots at the ends
    for x in (0, 39):
        _fline(g, (x, 9, 4), (x, 18, 11), "steel_dark")
        _fline(g, (x, 12, 4), (x, 3, 11), "steel_dark")
        g.set(x, 9, 4, "steel_light")
        g.set(x, 12, 4, "steel_light")
    # carry handle bridging the two ends above the open base
    for hx in (BX0, BX1):
        g.box(hx, 10, BZ1 + 1, hx, 11, 15, "bluegrey_dark")
    g.box(BX0, 10, 16, BX1, 11, 16, "steel")
    g.box(14, 10, 16, 25, 11, 16, "charcoal")                       # grip sleeve
    g.paint(14, 10, 16, 25, 10, 16, "iron")
    # contents of the base
    g.box(9, 13, 7, 26, 13, 8, "sawdust")                           # hammer handle
    g.paint(20, 13, 7, 26, 13, 8, "pine_aged")
    g.box(6, 11, 6, 8, 14, 8, "charcoal")                           # hammer head
    g.set(6, 14, 8, "steel_hi")
    g.box(27, 8, 8, 31, 8, 8, "steel_light")                        # screwdriver shaft
    g.box(32, 8, 7, 36, 9, 8, "mustard_dark")                       # its amber handle
    g.paint(36, 8, 7, 36, 9, 8, "mustard_deep")
    g.box(10, 9, 5, 22, 9, 6, "steel")                              # spanner
    g.box(9, 8, 5, 9, 10, 6, "steel_light")
    g.box(23, 8, 5, 23, 10, 6, "steel_light")
    g.box(28, 11, 4, 31, 14, 7, "charcoal")                         # tape measure
    g.paint(28, 11, 7, 31, 14, 7, "iron")
    g.set(31, 14, 5, "mustard")                                     # its tape end
    g.box(2, 7, 1, 37, 14, 3, "bluegrey_deep")                      # more tools below
    g.paint(3, 8, 3, 20, 12, 3, "steel_dark")
    # tray contents, standing proud of the shallow trays
    fy = trays[0][0] + 1
    for (x, dy, z) in [(3, 0, 11), (4, 1, 11), (5, 0, 11), (3, 2, 11), (6, 1, 11), (4, 2, 11),
                       (5, 2, 11), (7, 2, 11), (6, 0, 11), (4, 1, 12), (5, 1, 12)]:
        g.set(x, fy + dy, z, "galv")                                # screws
    g.box(15, fy + 1, 11, 23, fy + 1, 11, "mustard")                # carpenter's pencil
    g.set(23, fy + 1, 11, "charcoal")
    g.box(29, fy, 11, 32, fy, 11, "red_dark")                       # pliers, grips
    g.box(29, fy + 2, 11, 32, fy + 2, 11, "red_dark")
    g.box(33, fy, 11, 35, fy + 2, 11, "steel")                      # ...and jaws
    by = trays[1][0] + 1
    g.box(4, by, 11, 7, by + 2, 12, "copper")                       # spool of wire
    g.box(5, by + 1, 12, 6, by + 1, 12, "wood_stain")
    g.box(16, by, 11, 21, by + 2, 12, "card")                       # box of nails
    g.paint(16, by, 12, 21, by + 2, 12, "card_hi")
    # chipped paint on rims and corners
    for (x, y, z) in [(BX0, trays[0][1], 12), (BX0, trays[0][1], 11), (BX0 + 1, trays[0][1], 12),
                      (BX1, trays[0][1], 12), (BX0, trays[1][0], 12), (BX0, BY1, 5),
                      (BX0, BY1, 6)]:
        g.paint(x, y, z, x, y, z, "steel")
    return {"grid": g, "footprint_cells": ((BX0, BX1), (BY0, BY1))}
