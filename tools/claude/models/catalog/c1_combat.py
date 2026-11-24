"""Batch C1 - combat: firearms, melee, ammunition and protective gear (creator: Claude).

X right, Y front (+Y), Z up; inclusive cells. Handheld weapons are modelled in their held
orientation: muzzle / working end toward +Y, top up, lowest point on z = 0, with a `grip`
attachment at the main hand. Side profiles are drawn as small ASCII elevations (column = y,
row = z, top row first) and extruded across X; details are then painted onto the faces.
All props are generic and unbranded: no markings, no readable text, no internal mechanism.
"""
from catalog_registry import model
from voxkit import Grid


# ---------------------------------------------------------------------------
# local helpers
# ---------------------------------------------------------------------------
def extrude(g, rows, legend, y0=0, z0=0):
    """Extrude an ASCII side elevation. `rows` run top -> bottom (the last row is z = z0);
    column i is y = y0 + i. legend: char -> (colour, x0, x1). Unknown chars are empty."""
    n = len(rows)
    for r, line in enumerate(rows):
        z = z0 + (n - 1 - r)
        for i, ch in enumerate(line):
            if ch in legend:
                c, x0, x1 = legend[ch]
                g.box(x0, y0 + i, z, x1, y0 + i, z, c)


def side_paint(g, x, cells, c):
    """Paint a list of (y, z) cells on the face column x (occupied cells only)."""
    for (y, z) in cells:
        g.paint_cell(x, y, z, c)


def rows_cells(rows, ch, y0=0, z0=0):
    """(y, z) cells where an ASCII elevation holds `ch` (for painting side panels)."""
    n = len(rows)
    out = []
    for r, line in enumerate(rows):
        for i, c in enumerate(line):
            if c == ch:
                out.append((y0 + i, z0 + n - 1 - r))
    return out


def round_grip(g, rows, ch, xa, xb):
    """Round a grip's section: on the outline of the `ch` region (front strap, back strap,
    butt) keep only the inner columns, so the side panels sit inset like real grip panels."""
    cells = set(rows_cells(rows, ch))
    for (y, z) in cells:
        if any((y + dy, z + dz) not in cells and not _solid(g, xa + 1, y + dy, z + dz)
               for dy, dz in ((1, 0), (-1, 0), (0, -1))):
            g.set(xa, y, z, 0)
            g.set(xb, y, z, 0)


def _solid(g, x, y, z):
    return g.get(x, y, z) != 0


def recolour(g, frm, to, box=None):
    """Swap one palette role for another (optionally inside a box)."""
    from voxkit import P
    x0, y0, z0, x1, y1, z1 = box or (0, 0, 0, *[s - 1 for s in g.shape])
    sub = g.v[x0:x1 + 1, y0:y1 + 1, z0:z1 + 1]
    sub[sub == P(frm)] = P(to)


# ---------------------------------------------------------------------------
# handgun
# ---------------------------------------------------------------------------
HANDGUN = [
    # y: 0123456789012345678
    "..r..............f.",   # z12 sights
    "..SSSSSSSSSSSSSSSSS",   # z11 slide
    "..SSSSSSSSSSSSSSSSS",   # z10
    "..SSSSSSSSSSSSSSSSS",   # z9
    ".BFFFFFFFFFFFFFFFF.",   # z8 frame / beavertail
    "..GGGGGGTFFFFFFFFF.",   # z7 grip top, dust cover
    "..GGGGGG.t..T......",   # z6 trigger, guard front
    ".GGGGGG..t..T......",   # z5
    ".GGGGGGTTTTTT......",   # z4 guard bottom
    ".GGGGG.............",   # z3
    "GGGGGG.............",   # z2
    "GGGGG..............",   # z1
    "MMMMMM.............",   # z0 magazine base plate
]


@model("handgun", name="Handgun",
       story="A police-pattern service pistol carried in a belt holster for years, then left in a "
             "kitchen drawer when the sirens stopped. The slide's front edges are rubbed bright "
             "by the holster; the grip texture is worn smooth where the thumb rested.",
       details=["Steel slide, lighter than the dark polymer frame, with rear serrations",
                "Front and rear sights", "Exposed barrel hood at the ejection port",
                "Stippled grip panels with a hand-polished front strap",
                "Trigger guard with trigger", "Holster-worn muzzle edges"],
       exclusions=["No markings or serial plates", "No internal mechanism",
                   "No light, optic or accessories"],
       attachments={"grip": {"description": "Main hand on the grip, under the slide's rear."}},
       notes=["Generic semi-automatic pistol, dark polymer frame and steel slide; no brand.",
              "3 cells (3.75 cm) wide like a real service pistol; GPT's 6 cm reference width "
              "would make it look like a toy, so only length and height follow the reference."])
def handgun():
    g = Grid(3, 19, 13)
    legend = {"S": ("steel_dark", 0, 2), "F": ("charcoal", 0, 2), "B": ("charcoal", 1, 1),
              "G": ("charcoal", 0, 2), "M": ("iron", 0, 2), "T": ("charcoal", 1, 1),
              "t": ("black", 1, 1), "r": ("steel_dark", 0, 2), "f": ("steel_dark", 1, 1)}
    extrude(g, HANDGUN, legend)
    # slide: catch-light top, rear serrations, barrel hood, bore, holster wear
    g.paint(0, 2, 11, 2, 18, 11, "steel")
    for y in (3, 5):
        for x in (0, 2):
            g.paint(x, y, 9, x, y, 11, "charcoal")
    g.paint(1, 9, 11, 2, 11, 11, "steel_light")       # barrel hood seen through the port
    g.paint(2, 9, 10, 2, 11, 10, "black")             # ejection port shadow (right side)
    g.paint(0, 17, 9, 2, 18, 11, "steel")              # muzzle end rubbed by the holster
    for x in (0, 2):
        g.paint_cell(x, 18, 11, "steel_light")
        g.paint_cell(x, 18, 9, "steel_light")
    g.paint_cell(1, 18, 10, "black")                  # bore
    # frame: rail slots under the dust cover, slide/frame parting line shadow
    for y in (11, 13, 15):
        g.paint(0, y, 7, 2, y, 7, "black")
    # grip: stippled panels inset from the edges, polished front strap and back strap
    panel = [(y, z) for (y, z) in rows_cells(HANDGUN, "G") if 1 <= z <= 6]
    for (y, z) in panel:
        edge = any((y + dy, z) not in set(panel) for dy in (-1, 1))
        if not edge and 2 <= z <= 6:
            for x in (0, 2):
                g.paint_cell(x, y, z, "black")
    for (y, z) in [(7, 6), (6, 5), (6, 4), (5, 3), (5, 2), (4, 1)]:
        g.paint(0, y, z, 2, y, z, "iron_edge")      # front strap, polished by the fingers
    return {"grid": g, "attachments": {"grip": (1, 3, 4)}}


# ---------------------------------------------------------------------------
# revolver
# ---------------------------------------------------------------------------
REVOLVER = [
    # y: 01234567890123456
    ".HH............f.",   # z12 hammer spur, front sight
    "..HHTTTTTTBBBBBBB",   # z11 hammer, top strap, barrel
    "..RRRccccFBBBBBBB",   # z10 recoil shield, cylinder top, frame front, barrel
    "..RRRCCCCFLLLLLL.",   # z9  cylinder, ejector-rod lug
    "..RRRCCCCF.......",   # z8
    "..WRRccccF.......",   # z7  cylinder bottom
    ".WWWRFFFFF.......",   # z6  frame under the cylinder
    ".WWWW.t.Q........",   # z5  trigger, guard front
    ".WWWWQQQQ........",   # z4  guard bottom
    "WWWW.............",   # z3
    "WWWW.............",   # z2
    "WWWW.............",   # z1
    ".WWW.............",   # z0  rounded butt
]


@model("revolver", name="Revolver",
       story="A six-shot revolver that spent decades in a bedside drawer before it was carried "
             "every day. The bluing has worn silver on the cylinder, muzzle and frame edges, and "
             "the walnut grip is darkened and polished where the palm sits.",
       details=["Fluted six-shot cylinder bulging past the narrow frame",
                "Barrel with ejector-rod lug and ramp front sight", "Hammer spur",
                "Walnut plow-handle grip, polished at the palm swell",
                "Worn bluing: silver edges on the cylinder, muzzle and top strap"],
       exclusions=["No markings, logos or grip medallion", "No internal mechanism",
                   "No visible cartridges"],
       attachments={"grip": {"description": "Main hand around the wooden grip."}},
       notes=["Generic six-shot revolver with a wooden grip and worn bluing.",
              "Modelled muzzle +Y (held orientation), so GPT's 0.19 m X / 0.08 m Y reference "
              "becomes 0.21 m long (Y) and 5 cm wide (X) at the cylinder."])
def revolver():
    g = Grid(4, 17, 13)
    legend = {"H": ("iron_blue", 1, 2), "T": ("iron_blue", 1, 2), "B": ("iron_blue", 1, 2),
              "R": ("iron_blue", 1, 2), "F": ("iron_blue", 1, 2), "L": ("iron_blue", 1, 2),
              "C": ("steel", 0, 3), "c": ("steel", 1, 2),
              "W": ("pine_dark", 0, 3), "Q": ("iron_blue", 1, 2), "t": ("black", 1, 2),
              "f": ("iron_blue", 1, 2)}
    extrude(g, REVOLVER, legend)
    # cylinder: worn silver lobes, dark flutes, darker rear face, bright front edge
    for x in (0, 3):
        g.paint(x, 6, 8, x, 7, 8, "iron_blue")
    g.paint(0, 5, 7, 3, 5, 10, "steel_dark")
    g.paint(1, 8, 7, 2, 8, 10, "steel_light")
    # worn bluing on edges: top strap, muzzle, hammer spur
    g.paint(1, 4, 11, 2, 9, 11, "iron_edge")
    g.paint(1, 16, 10, 2, 16, 11, "steel")
    g.paint_cell(1, 16, 11, "black")                    # bore
    g.paint(1, 1, 12, 2, 1, 12, "steel")
    # walnut grip: darker butt, front strap polished lighter by the fingers
    g.paint(0, 0, 0, 3, 3, 0, "wood_stain")
    for (y, z) in [(4, 4), (4, 5), (3, 3), (3, 2), (3, 1)]:
        g.paint(0, y, z, 3, y, z, "pine_aged")
    return {"grid": g, "attachments": {"grip": (1, 2, 3)}}


# ---------------------------------------------------------------------------
# long guns: shared stock builder
# ---------------------------------------------------------------------------
LONG_GUN_WHY = ("Overridden from the manifest's 2.5 cm to 1.25 cm so the whole firearms family "
                "shares one voxel rhythm with the pistol, revolver and SMG: at 2.5 cm the barrel, "
                "magazine tube, trigger guard and scope would each be a single cell and the "
                "weapon would lose its value structure.")


def stock(g, y_heel, y_wrist, heel_top, wrist_top, wrist_bot, toe, wood, x0=0, x1=3,
          grip_drop=0, grip_span=(0, -1)):
    """Butt stock from the heel/toe (y_heel) to the wrist (y_wrist): a gently rising comb
    and a straight underline from the toe up to the wrist, optional pistol-grip drop."""
    n = y_wrist - y_heel
    for i in range(n + 1):
        y = y_heel + i
        top = round(heel_top + (wrist_top - heel_top) * i / n)
        bot = round(toe + (wrist_bot - toe) * i / n)
        if grip_span[0] <= y <= grip_span[1]:
            bot -= grip_drop
        g.box(x0, y, bot, x1, y, top, wood)


@model("shotgun", name="Pump Shotgun", cell=0.0125, why=LONG_GUN_WHY,
       story="A farm-store pump shotgun that lived behind a garage door for bird season. Since "
             "the catastrophe it has been carried daily: the fore-end grooves are polished by "
             "the pumping hand, the bluing has rubbed off the receiver edges and the muzzle.",
       details=["Grooved wooden pump fore-end around the magazine tube",
                "Dark receiver with worn bright edges and ejection port",
                "Long barrel with bead sight and barrel-to-magazine clamp",
                "Wooden stock with semi-pistol grip and black rubber recoil pad",
                "Trigger guard with trigger"],
       exclusions=["No markings or engraving", "No sling, no shells, no internal mechanism"],
       attachments={"grip": {"description": "Main hand at the stock's wrist behind the trigger."},
                    "support": {"description": "Support hand on the pump fore-end."}},
       notes=["Generic pump shotgun with wooden stock and fore-end.",
              "4 cells (5 cm) wide like the real weapon; GPT's 12 cm reference width and 23 cm "
              "height are not followed (no sling is in the brief)."])
def shotgun():
    g = Grid(4, 80, 16)
    wood, wood_d, wood_l = "pine_aged", "pine_dark", "pine_mid"
    # stock: heel 0, wrist 23
    stock(g, 2, 17, 9, 10, 4, 0, wood)
    stock(g, 18, 23, 10, 10, 4, 6, wood, grip_drop=1, grip_span=(18, 20))
    g.box(0, 0, 0, 3, 1, 9, "black")                       # recoil pad
    g.clear(0, 0, 9, 3, 0, 9)                              # rounded heel
    g.clear(0, 0, 0, 3, 0, 0)                              # rounded toe
    # receiver
    g.box(0, 24, 6, 3, 38, 12, "iron")
    g.clear(0, 24, 12, 3, 24, 12)                          # rounded rear top
    g.paint(0, 24, 12, 3, 38, 12, "iron_edge")             # worn top edge
    g.paint(0, 38, 6, 3, 38, 12, "iron_edge")              # front face lip
    g.paint(3, 27, 9, 3, 33, 11, "black")                  # ejection port (right side)
    g.paint(0, 28, 7, 0, 34, 7, "iron_dark")               # loading-port shadow line (left)
    # trigger guard and trigger
    g.box(1, 26, 3, 2, 33, 3, "iron")
    g.box(1, 26, 4, 2, 26, 5, "iron")
    g.box(1, 33, 4, 2, 33, 5, "iron")
    g.box(1, 29, 4, 2, 29, 5, "black")
    # barrel, bead, bore
    g.box(1, 39, 11, 2, 79, 12, "steel_dark")
    g.paint(1, 39, 12, 2, 79, 12, "steel")                 # top catch-light
    g.box(1, 77, 13, 2, 77, 13, "brass")                   # bead
    g.paint(1, 78, 11, 2, 79, 12, "steel_light")           # muzzle rubbed bright
    g.paint(1, 79, 11, 2, 79, 12, "black")                 # bore
    # magazine tube, cap and clamp
    g.box(1, 39, 8, 2, 71, 9, "iron")
    g.box(1, 72, 8, 2, 73, 9, "steel")
    g.box(1, 69, 10, 2, 70, 10, "iron")
    g.box(0, 69, 9, 3, 70, 11, "iron")                     # clamp band
    g.paint(0, 69, 9, 3, 70, 11, "iron_edge")
    # pump fore-end: grooved wood around the tube
    g.box(0, 44, 7, 3, 60, 10, wood)
    for y in range(46, 59, 2):
        g.paint(0, y, 7, 0, y, 9, wood_d)
        g.paint(3, y, 7, 3, y, 9, wood_d)
        g.paint(1, y, 7, 2, y, 7, wood_d)
    for y in (44, 60):
        g.clear(0, y, 7, 0, y, 7)
        g.clear(3, y, 7, 3, y, 7)
    g.paint(0, 45, 10, 3, 59, 10, wood_l)                  # polished upper edge
    # stock wear: darker hand-worn wrist, lighter scuffed toe
    g.paint(0, 18, 3, 3, 23, 5, wood_d)
    g.paint(0, 2, 0, 3, 5, 1, wood_l)
    return {"grid": g, "attachments": {"grip": (1, 20, 8), "support": (1, 52, 8)}}


def octagon_y(g, y0, y1, x0, z0, c):
    """4 x 4 rounded section along Y (rows 2-4-4-2) with its lower-left corner at (x0, z0)."""
    g.box(x0 + 1, y0, z0, x0 + 2, y1, z0 + 3, c)
    g.box(x0, y0, z0 + 1, x0 + 3, y1, z0 + 2, c)


def sling_y(g, ya, za, yb, zb, sag, x0, x1, c):
    """A hanging strap along Y between two swivels (cells), sagging `sag` cells; one cell
    thick, with vertical runs filled so the strap stays face-connected."""
    prev = None
    for y in range(ya, yb + 1):
        u = (y - ya) / (yb - ya)
        z = round(za + (zb - za) * u - sag * 4 * u * (1 - u))
        if prev is not None and abs(z - prev) > 1:
            lo, hi = sorted((z, prev))
            g.box(x0, y - 1, lo + 1, x1, y - 1, hi - 1, c)
        g.box(x0, y, z, x1, y, z, c)
        prev = z


# per-y (bottom, top) of the rifle's butt stock and pistol grip, y = 0..25
RIFLE_STOCK = [(3, 12), (3, 13), (3, 13), (3, 13), (4, 13), (4, 13), (4, 13), (5, 13),
               (5, 13), (5, 13), (6, 13), (6, 13), (6, 13), (6, 13), (7, 13), (7, 13),
               (6, 12), (5, 11), (4, 10), (4, 10), (4, 10), (5, 10), (6, 10), (7, 10),
               (7, 10), (7, 10)]


@model("hunting_rifle", name="Hunting Rifle", cell=0.0125, why=LONG_GUN_WHY,
       story="A deer rifle kept in a locked cabinet by a man who hunted one weekend a year. "
             "It came out of the cabinet the night the sirens stopped; the leather sling is "
             "stiff and cracked, the walnut is still oiled, the scope caps are lost.",
       details=["Walnut stock with pistol grip, darker checkered panels and contrasting tip",
                "Telescopic sight on two rings with turrets and opaque lens faces",
                "Bolt handle with round knob on the right",
                "Trigger guard and magazine floor plate",
                "Leather sling hanging between front and rear swivels",
                "Black recoil pad"],
       exclusions=["No markings, engraving or brand on the scope", "No internal mechanism",
                   "No bipod or cartridges"],
       attachments={"grip": {"description": "Main hand on the pistol grip."},
                    "support": {"description": "Support hand under the fore-end."},
                    "sling_rear": {"description": "Rear sling swivel."},
                    "sling_front": {"description": "Front sling swivel."}},
       notes=["Generic bolt-action rifle with a scope, wooden stock and a sling.",
              "Held orientation: the sling hangs below the stock, so its lowest point is z = 0."])
def hunting_rifle():
    g = Grid(6, 86, 19)
    wood, wood_d, wood_l, tip = "pine_dark", "wood_stain", "pine_aged", "wood_deep"
    # butt stock and pistol grip (y 0..25), recoil pad
    for y, (b, t) in enumerate(RIFLE_STOCK):
        g.box(0, y, b, 3, y, t, wood)
    g.paint(0, 0, 0, 3, 1, 18, "black")
    g.paint(0, 2, 12, 3, 15, 13, wood_l)                   # lit comb line
    g.paint(0, 18, 4, 3, 20, 4, tip)                       # grip cap
    for x in (0, 3):
        g.paint(x, 18, 6, x, 21, 9, wood_d)                # grip checkering panel
    # fore-end stock under the action (y 26..61) tapering toward a dark tip
    for y in range(26, 62):
        b = 7 if y < 46 else 8
        g.box(0, y, b, 3, y, 10, wood)
    g.box(0, 60, 8, 3, 61, 10, tip)
    g.clear(0, 61, 8, 0, 61, 8)
    g.clear(3, 61, 8, 3, 61, 8)
    for x in (0, 3):
        g.paint(x, 46, 8, x, 54, 9, wood_d)                # fore-end checkering panel
    g.paint(0, 26, 10, 3, 59, 10, wood_l)                  # lit upper edge of the wood
    # receiver, bolt shroud, bolt handle (right side)
    g.box(1, 22, 10, 2, 42, 12, "iron")
    g.paint(1, 22, 12, 2, 42, 12, "iron_edge")
    g.box(3, 26, 11, 3, 26, 11, "steel_dark")
    g.box(4, 26, 9, 4, 26, 11, "steel_dark")
    g.box(4, 25, 8, 5, 26, 9, "steel")                     # bolt knob
    # bottom metal: trigger guard, trigger, magazine floor plate
    g.box(1, 27, 4, 2, 32, 4, "iron")
    g.box(1, 32, 5, 2, 32, 6, "iron")
    g.box(1, 27, 5, 2, 27, 6, "iron")
    g.box(1, 29, 5, 2, 29, 6, "black")
    g.box(1, 33, 6, 2, 40, 6, "iron")
    g.paint(1, 33, 6, 2, 40, 6, "iron_edge")
    # barrel
    g.box(1, 43, 10, 2, 85, 11, "steel_dark")
    g.paint(1, 43, 11, 2, 85, 11, "steel")
    g.paint_cell(1, 85, 11, "black")                       # bore
    # scope: rings on bases, eyepiece and objective bells, turrets, lens faces
    for y in (28, 37):
        g.box(1, y, 13, 2, y, 13, "iron")
        octagon_y(g, y, y, 1 - 1, 14, "iron")
    g.box(1, 26, 15, 2, 39, 16, "charcoal")                # tube
    octagon_y(g, 22, 25, 0, 14, "charcoal")                # eyepiece
    octagon_y(g, 40, 45, 0, 14, "charcoal")                # objective bell
    g.box(1, 39, 14, 2, 39, 17, "charcoal")
    g.paint(1, 22, 17, 2, 45, 17, "iron")                  # catch-light along the top
    g.paint(1, 26, 16, 2, 39, 16, "iron")
    g.paint(1, 22, 15, 2, 22, 16, "glass_deep")            # ocular lens
    g.paint(1, 45, 15, 2, 45, 16, "glass_dark")            # objective lens
    g.box(1, 32, 17, 2, 33, 18, "iron")                    # elevation turret
    g.paint(1, 32, 18, 2, 33, 18, "iron_edge")
    g.box(0, 32, 15, 0, 33, 16, "iron")                    # side-focus knob (left)
    g.box(3, 32, 15, 3, 33, 16, "iron")                    # windage turret (right)
    # sling swivels and the hanging leather sling
    g.box(1, 9, 4, 2, 9, 4, "steel")
    g.box(1, 56, 7, 2, 56, 7, "steel")
    sling_y(g, 9, 3, 56, 6, 4.0, 1, 2, "leather")
    g.paint(1, 12, 0, 2, 14, 4, "leather_dark")            # sling keeper / doubled end
    return {"grid": g, "attachments": {"grip": (1, 20, 7), "support": (1, 50, 8),
                                       "sling_rear": (1, 9, 4), "sling_front": (1, 56, 7)}}


# ---------------------------------------------------------------------------
# compact SMG
# ---------------------------------------------------------------------------
SMG = [
    # y: 0123456789012345678901234567890123456789
    "......rr...................ff.............",   # z17 sights
    "......RRRRRRRRRRRRRRRRRRRRRR..............",   # z16 top rail
    "...UUUUUUUUUUUUUUUUUUUUHHHHHHHHHH.........",   # z15 upper receiver, handguard
    "...UUUUUUUUUUUUUUUUUUUUHHHHHHHHHH.........",   # z14
    "..EUUUUUUUUUUUUUUUUUUUUHHHHHHHHHHBBBBBBBNN",   # z13 end cap, barrel, muzzle
    "..EUUUUUUUUUUUUUUUUUUUUHHHHHHHHHHBBBBBBBNN",   # z12
    "..EUUUUUUUUUUUUUUUUUUUUHHHHHHHHHH.........",   # z11
    "...LLLLLLLLLLLLLLLLLLLLHHHHHHHHH..........",   # z10 lower receiver
    "...LLLLLLLLLLLLLLLLLLLLHHHHHHH............",   # z9
    ".....GGGG..t..TWWWWW......................",   # z8 grip, trigger, mag well
    ".....GGGG..t..T.WWW.......................",   # z7
    "....GGGGTTTTTTT.MMM.......................",   # z6 trigger guard
    "....GGGG........MMM.......................",   # z5
    "...GGGG.........MMM.......................",   # z4
    "...GGGG.........MMM.......................",   # z3
    "..GGGG..........MMM.......................",   # z2
    "................MMM.......................",   # z1
    "................PPPP......................",   # z0 magazine base plate
]


@model("compact_smg", name="Compact Submachine Gun",
       story="A compact submachine gun from a patrol car's locked rack, taken when the car was "
             "found abandoned at an intersection. The skeletal stock is still folded; the "
             "receiver's edges and the magazine's base are worn grey from being dragged.",
       details=["Boxy steel upper receiver over a dark polymer lower",
                "Skeletal side-folding stock folded along the left side, rubber butt plate",
                "Vented handguard, short barrel and muzzle", "Top rail with front and rear sights",
                "Straight magazine ahead of the trigger guard", "Left-side charging handle"],
       exclusions=["No markings, logos or selector lettering", "No internal mechanism",
                   "No optic, light or suppressor"],
       attachments={"grip": {"description": "Main hand on the pistol grip."},
                    "support": {"description": "Support hand under the handguard."}},
       notes=["Generic compact SMG with folded stock and straight magazine; dark finish.",
              "0.50 m long with the stock folded (GPT's 0.60 m reads as a carbine); the folded "
              "stock lies along the left side so it shows in the hero view."])
def compact_smg():
    g = Grid(6, 42, 18)
    legend = {"r": ("iron", 2, 3), "f": ("iron", 2, 3), "R": ("iron_edge", 2, 3),
              "U": ("steel_dark", 1, 4), "E": ("iron", 1, 4), "H": ("iron", 1, 4),
              "B": ("steel_dark", 2, 3), "N": ("iron", 2, 3), "L": ("charcoal", 1, 4),
              "G": ("black", 1, 4), "t": ("black", 2, 3), "T": ("charcoal", 2, 3),
              "W": ("charcoal", 1, 4), "M": ("iron_dark", 2, 3), "P": ("iron", 1, 4)}
    extrude(g, SMG, legend)
    g.clear(2, 7, 17, 3, 7, 17)                       # rear sight: single aperture block
    g.box(2, 7, 17, 3, 7, 17, "iron")
    for y in range(7, 27, 2):
        g.paint(2, y, 16, 3, y, 16, "black")          # rail slots
    g.paint(1, 3, 15, 4, 22, 15, "steel")              # receiver top catch-light
    g.paint(4, 16, 13, 4, 20, 14, "black")             # ejection port (right side)
    for (y0, y1) in ((24, 25), (27, 28), (30, 31)):
        g.paint(1, y0, 12, 1, y1, 12, "black")         # handguard vents
        g.paint(4, y0, 12, 4, y1, 12, "black")
    g.paint(2, 41, 12, 3, 41, 13, "black")             # bore
    g.paint(1, 16, 0, 4, 19, 0, "iron_edge")           # magazine base, worn grey
    g.paint(2, 16, 1, 3, 18, 1, "iron")
    # side-folding skeletal stock along the left side (x = 0)
    g.box(0, 2, 10, 0, 3, 14, "iron")                  # hinge block
    g.box(0, 3, 14, 0, 25, 14, "iron_edge")            # upper bar
    g.box(0, 3, 10, 0, 25, 10, "iron_edge")            # lower bar
    g.box(0, 24, 9, 0, 25, 15, "black")                # butt plate, folded forward
    g.paint(0, 24, 15, 0, 25, 15, "charcoal")
    # charging handle ahead of the folded stock (left)
    g.box(0, 29, 13, 0, 30, 13, "black")
    return {"grid": g, "attachments": {"grip": (2, 6, 5), "support": (2, 28, 9)}}


# ---------------------------------------------------------------------------
# baseball bat
# ---------------------------------------------------------------------------
# radius (cells) along the bat from the knob (y = 0) to the barrel end; the section is centred
# on a cell corner so 1.0 -> 2x2, 1.6 -> rows 2-4-4-2, 2.6 -> 2-4-6-6-4-2, 3.0 -> 4-6-6-6-6-4
BAT_PROFILE = ([2.0] * 2 + [1.0] * 21 + [1.6] * 7 + [2.6] * 7 + [3.0] * 24 + [2.6])


@model("baseball_bat", name="Baseball Bat", cell=0.0125,
       why="Overridden from 2.5 cm to 1.25 cm: at 2.5 cm the bat is 3 cells thick and its "
           "taper from barrel to handle, the knob and the taped grip collapse into a stick.",
       story="A youth-league ash bat from a garage shelf. Someone re-wrapped the handle with "
             "black electrical tape for a better grip; the barrel is scuffed grey and chipped "
             "on one side from striking concrete and fence posts.",
       details=["Clear taper from a thick barrel through a long thin handle to a knob",
                "Handle spiral-wrapped in black tape, with the last wrap lifting",
                "Scuffed, darkened hitting zone with grey scrapes and a chipped dent",
                "Rounded barrel end"],
       exclusions=["No brand stamp or lettering", "No nails, blood or gore"],
       attachments={"grip": {"description": "Both hands on the taped handle above the knob."}},
       notes=["Wooden bat with taped grip and a scuffed barrel.",
              "Held orientation: barrel toward +Y, lying level; the barrel's underside is "
              "z = 0."])
def baseball_bat():
    L = len(BAT_PROFILE)
    g = Grid(6, L, 6)
    for y, r in enumerate(BAT_PROFILE):
        g.cyl_y(3.0, 3.0, r, y, y, "pine_light")
    # knob and end grain
    g.paint(0, 0, 0, 5, 1, 5, "pine_mid")
    g.paint(0, L - 1, 0, 5, L - 1, 5, "pine_hi")
    g.paint(0, 37, 5, 5, L - 2, 5, "pine_hi")              # lit top of the barrel
    # taped handle: spiral seams around the 2x2 section, last wrap lifting
    ring = [(2, 2), (3, 2), (3, 3), (2, 3)]
    for y in range(3, 19):
        for k, (x, z) in enumerate(ring):
            g.set(x, y, z, "black" if (y + k) % 4 == 0 else "charcoal")
    g.set(1, 19, 3, "charcoal")                            # lifted tape end
    g.set(2, 19, 3, "charcoal")
    # scuffed hitting zone on the camera (-X / front) side: one darkened, ragged patch
    # (outline drawn per row) with two grey scrape lines, not a speckle
    patch = {1: (46, 53), 2: (44, 55), 3: (45, 56), 4: (47, 54)}
    for z, (y0, y1) in patch.items():
        for x in (0, 1):
            g.paint(x, y0, z, x, y1, z, "pine_aged")
    g.paint(0, 46, 3, 1, 51, 3, "wgrey")                    # scrape lines
    g.paint(0, 49, 1, 1, 54, 1, "wgrey")
    g.paint(0, 45, 5, 2, 52, 5, "pine_mid")                 # scuffed crown
    # chipped dent where it hit a post
    g.clear(0, 50, 2, 0, 52, 2)
    g.paint(1, 50, 2, 1, 52, 2, "pine_dark")
    return {"grid": g, "attachments": {"grip": (2, 8, 2)}}


# ---------------------------------------------------------------------------
# ammunition can
# ---------------------------------------------------------------------------
@model("ammunition_box", name="Ammunition Box",
       story="A surplus steel ammo can bought at a gun show to keep a hunter's cartridges dry. "
             "The olive paint is chipped bare along the lid edge and the latch, and a quiet "
             "stencil block on the side has faded to a dull khaki.",
       details=["Long, narrow, tall steel can with an overhanging lid lip",
                "Cam latch lever on the left end, pull tip worn bright",
                "Folding carry handle lying flat on the lid", "Rear lid hinge knuckles",
                "Faded stencil band as a plain colour block",
                "Chipped paint on the lid's front edge and a corner"],
       exclusions=["No readable stencil text or lot numbers", "No visible cartridges"],
       notes=["Olive steel ammo can with a latch lid and carry handle.",
              "Proportioned like a real .50-calibre can (taller than GPT's 11 cm reference) so "
              "it reads as an ammo can, not a flat tool box."])
def ammunition_box():
    g = Grid(24, 14, 15)
    body, dark, lite = "olive_dark", "green_deep", "olive"
    g.box(2, 1, 0, 21, 12, 10, body)
    g.paint(2, 1, 0, 21, 12, 0, dark)                      # rolled bottom seam
    g.box(1, 0, 11, 22, 13, 11, dark)                      # lid skirt (overhang)
    g.box(2, 1, 12, 21, 12, 12, lite)                      # lid top
    g.paint(1, 0, 11, 22, 0, 11, body)
    for x in (4, 5, 18, 19):                               # hinge knuckles at the back
        g.box(x, 0, 10, x, 0, 10, dark)
    # latch lever on the left end, worn bright pull tip
    g.box(1, 5, 5, 1, 8, 10, lite)
    g.paint(1, 5, 5, 1, 8, 5, "steel_dark")
    g.box(0, 6, 9, 0, 7, 11, dark)                         # lever pivot over the lid lip
    # folding handle lying flat on the lid
    g.box(7, 6, 13, 16, 7, 13, dark)
    g.box(6, 5, 13, 7, 8, 13, body)
    g.box(16, 5, 13, 17, 8, 13, body)
    g.paint(10, 6, 13, 13, 7, 13, "steel_dark")           # grip rubbed to bare metal
    # faded stencil band on the front long side (plain colour blocks)
    g.paint(6, 12, 7, 17, 12, 7, "khaki_dark")
    g.paint(6, 12, 5, 13, 12, 5, "khaki_dark")
    # chipped paint: lid front edge near the left corner, a bottom corner
    g.paint(1, 13, 11, 4, 13, 11, "steel_dark")
    g.paint(2, 12, 0, 3, 12, 0, "rust_deep")
    g.paint(2, 12, 1, 2, 12, 1, "rust_dark")
    return g


# ---------------------------------------------------------------------------
# shotgun shell box
# ---------------------------------------------------------------------------
@model("shotgun_shell_box", name="Shotgun Shell Box",
       story="A fresh box of shotgun shells from a hardware store's back shelf, opened for the "
             "first time: the lid is folded back and two shells have been taken out and set "
             "down in front of it.",
       details=["Printed card box (muted green with a cream band) with its lid standing open",
                "Three rows of five shells standing brass-up, two gaps where shells were taken",
                "Two loose shells against the box (one lying, one standing on its head): red "
                "hulls, brass heads, crimped ends"],
       exclusions=["No brand, gauge or text printing", "No loose powder or wads"],
       notes=["Cardboard box of shells, open, shells with brass bases.",
              "Shells are spaced one cell apart (a slight stylisation) so each brass head reads "
              "separately; the open lid makes the model taller than GPT's 14 cm reference."])
def shotgun_shell_box():
    g = Grid(19, 14, 17)
    ox, oy = 2, 3                                          # box origin (room for loose shells)
    W, D, H = 16, 10, 5
    g.box(ox, oy, 0, ox + W - 1, oy + D - 1, H, "label_green")
    g.clear(ox + 1, oy + 1, 1, ox + W - 2, oy + D - 2, H)
    g.paint(ox + 1, oy + 1, 0, ox + W - 2, oy + D - 2, 0, "card_deep")   # floor
    g.paint(ox, oy, H, ox + W - 1, oy + D - 1, H, "card_hi")             # cut card rim
    g.paint(ox, oy + D - 1, 2, ox + W - 1, oy + D - 1, 3, "label_cream") # front band
    g.paint(ox, oy, 2, ox, oy + D - 1, 3, "label_cream")
    # shells: 5 x 3, pitch 3, brass heads up; two taken from the front-left
    taken = {(0, 2), (1, 2)}
    for i in range(5):
        for j in range(3):
            if (i, j) in taken:
                continue
            x0, y0 = ox + 2 + 3 * i, oy + 1 + 3 * j
            g.box(x0, y0, 1, x0 + 1, y0 + 1, 5, "red")
            g.box(x0, y0, 6, x0 + 1, y0 + 1, 6, "brass")
            g.paint(x0, y0, 5, x0 + 1, y0 + 1, 5, "red_dark")
    # lid: hinged at the back rim, standing open and leaning back one cell near the top
    g.box(ox, oy - 1, 6, ox + W - 1, oy - 1, 10, "card_hi")
    g.box(ox, oy - 2, 11, ox + W - 1, oy - 2, 15, "card_hi")
    g.paint(ox, oy - 2, 11, ox + W - 1, oy - 2, 15, "card_hi")
    for (y, z0, z1) in ((oy - 2, 6, 10), (oy - 3, 11, 15)):
        g.box(ox, y, z0, ox + W - 1, y, z1, "label_green")              # printed outside
    g.box(ox, oy - 2, 16, ox + W - 1, oy - 2, 16, "card")              # tuck flap edge
    g.paint(ox, oy - 3, 12, ox + W - 1, oy - 3, 13, "label_cream")
    # loose shells: one lying in front of the box, one standing beside its left end
    sy = oy + D
    g.box(ox + 2, sy, 0, ox + 6, sy + 1, 1, "red")
    g.box(ox + 7, sy, 0, ox + 7, sy + 1, 1, "brass")
    g.paint(ox + 2, sy, 0, ox + 2, sy + 1, 1, "red_dark")             # crimped end
    g.box(ox - 2, oy + 6, 0, ox - 1, oy + 7, 4, "red")
    g.box(ox - 2, oy + 6, 0, ox - 1, oy + 7, 0, "brass")              # stood on its head
    g.paint(ox - 2, oy + 6, 4, ox - 1, oy + 7, 4, "red_dark")
    return g


# ---------------------------------------------------------------------------
# loose ammunition: pistol magazine with spilled rounds
# ---------------------------------------------------------------------------
def round_9mm(g, x, y, z, axis, sign=1):
    """A 9 mm round as three cells: two brass case cells and a copper bullet, lying along
    `axis` ('x', 'y' or 'z'), bullet toward the positive (sign=1) or negative end."""
    cells = [(0, "brass"), (1, "brass"), (2, "copper")]
    for k, c in cells:
        d = k * sign
        p = {"x": (x + d, y, z), "y": (x, y + d, z), "z": (x, y, z + d)}[axis]
        g.set(*p, c)


@model("loose_ammo_pickup", name="Loose Ammunition",
       story="A spare pistol magazine and the handful of rounds that spilled out of a torn "
             "cardboard box in a glovebox. Someone thumbed a few back in and dropped the rest.",
       details=["Pistol magazine lying on its side: dark body, worn spine edge, witness holes, "
                "base plate", "Top round seated in the feed lips",
                "Eight loose rounds (brass case, copper bullet), one standing on its base, one "
                "resting on the others, all touching the magazine or each other"],
       exclusions=["No box or packaging", "No spent casings", "No headstamp or markings"],
       notes=["A pistol magazine with a handful of loose rounds touching it.",
              "Rounds are 1 x 1 x 3 cells (1.25 x 3.75 cm), close to a real 9 mm round; the "
              "pickup lies flat, so it is lower than GPT's 10 cm reference."])
def loose_ammo_pickup():
    g = Grid(18, 13, 4)
    # magazine on its side: long axis X, front spine toward +Y, base plate at -X
    g.box(3, 5, 0, 12, 7, 1, "charcoal")
    g.paint(3, 7, 0, 12, 7, 1, "iron_edge")               # worn front spine
    g.box(2, 4, 0, 2, 8, 2, "iron")                       # base plate, slightly larger
    for x in (5, 7, 9, 11):
        g.set(x, 6, 1, "black")                           # witness holes on the upper face
    g.box(13, 5, 0, 13, 7, 0, "steel_dark")               # feed lips
    g.set(13, 5, 1, "brass")                              # top round in the lips
    g.set(13, 6, 1, "brass")
    g.set(13, 7, 1, "copper")
    # loose rounds
    round_9mm(g, 6, 8, 0, "x")                            # against the magazine's spine
    round_9mm(g, 8, 9, 0, "x")
    round_9mm(g, 7, 8, 1, "x")                            # resting on the two below
    round_9mm(g, 11, 9, 0, "y")                           # pointing away
    round_9mm(g, 12, 10, 0, "z")                          # standing on its base
    round_9mm(g, 10, 4, 0, "x", -1)                       # behind the magazine
    round_9mm(g, 14, 6, 0, "x")                           # spilled past the feed lips
    round_9mm(g, 1, 6, 0, "y", -1)                        # by the base plate
    return g


# ---------------------------------------------------------------------------
# protective vest (soft armour carrier standing as if worn)
# ---------------------------------------------------------------------------
@model("protective_vest", name="Protective Vest",
       story="A patrol officer's soft armour vest, unstrapped and stood on a locker-room bench "
             "for the last time. The carrier has faded at the shoulders, the hem is rubbed "
             "pale at the front and one shoulder tab has come loose.",
       details=["Front and back panels joined by shoulder straps; open neck and armholes",
                "Velcro ID panel on the chest (blank, no lettering)",
                "Two magazine pouches and a small radio pouch with flaps",
                "Elastic side straps with tabs", "Drag loop at the back collar",
                "Sun-faded shoulders, scuffed front hem, one lifted shoulder tab"],
       exclusions=["No 'POLICE' or other lettering, no badges or flags", "No visible armour plate"],
       notes=["Soft armour vest standing as if worn: dark navy carrier, velcro panel, side "
              "straps, a couple of pouches.", "A closed shell; the inside is hollow."])
def protective_vest():
    W, y0, y1, H = 21, 1, 8, 25                       # torso x 0..20, y 1..8, z 0..24
    g = Grid(W, 12, H)
    base, dark, deep = "navy", "navy_dark", "blue_deep"

    def outline(z, xa, xb, front=True, back=True, sides=True):
        for x in range(xa, xb + 1):
            if front:
                g.set(x, y1, z, base)
            if back:
                g.set(x, y0, z, base)
        if sides:
            for y in range(y0, y1 + 1):
                g.set(xa, y, z, base)
                g.set(xb, y, z, base)

    for z in range(0, 14):                            # body below the armholes
        outline(z, 0, W - 1)
    g.clear(0, y0, 0, 0, y0, 13)                      # soften the four vertical corners
    g.clear(W - 1, y0, 0, W - 1, y0, 13)
    g.clear(0, y1, 0, 0, y1, 13)
    g.clear(W - 1, y1, 0, W - 1, y1, 13)
    for z in range(14, 19):                           # armholes: panels narrow, sides open
        k = 1 if z < 16 else 2
        outline(z, k, W - 1 - k, sides=False)
    for z in range(19, 23):                           # neck scoop in front, back stays up
        for (xa, xb) in ((3, 6), (14, 17)):
            outline(z, xa, xb, sides=False)
        outline(z, 7, 13, front=False, sides=False)
    for (xa, xb) in ((3, 6), (14, 17)):               # shoulder straps over the top
        g.box(xa, y0, 23, xb, y1, 23, base)
        g.paint(xa, y0 + 1, 23, xb, y1 - 1, 23, "denim_dark")   # sun-faded tops
    # side straps (elastic, darker) across the open side gaps
    for x in (0, W - 1):
        g.clear(x, 3, 4, x, 6, 12)
        for z in (5, 6, 10, 11):
            g.box(x, 3, z, x, 6, z, "charcoal")
        g.paint(x, 5, 5, x, 6, 6, "black")
        g.paint(x, 5, 10, x, 6, 11, "black")
    # edge binding: hem, armholes, neck - panel cells that border the openings
    import numpy as np
    occ = g.v > 0
    for (x, y, z) in np.argwhere(occ):
        if z >= 13 and y in (y0, y1):
            if (x == 0 or not occ[x - 1, y, z] or x == W - 1 or not occ[x + 1, y, z]
                    or z == H - 1 or not occ[x, y, z + 1]):
                g.set(x, y, z, dark)
    g.paint(0, 0, 0, W - 1, 11, 0, dark)
    g.paint(2, y1, 0, W - 3, y1, 0, "blue_dark")      # front hem rubbed pale
    g.paint(0, 0, 22, W - 1, 11, 22, dark)
    # chest: velcro ID panel (blank) and a small radio pouch
    g.paint(5, y1, 15, 12, y1, 17, dark)
    g.box(14, y1 + 1, 13, 16, y1 + 1, 18, base)
    g.box(14, y1 + 1, 18, 16, y1 + 2, 18, deep)       # flap
    g.box(15, y1 + 1, 19, 15, y1 + 1, 19, "black")    # antenna stub
    # two magazine pouches on the abdomen with flaps and snap tabs
    for xa in (4, 10):
        g.box(xa, y1 + 1, 2, xa + 4, y1 + 2, 7, base)
        g.box(xa, y1 + 1, 7, xa + 4, y1 + 2, 8, deep)
        g.box(xa + 2, y1 + 3, 6, xa + 2, y1 + 3, 7, "black")
        g.paint(xa, y1 + 2, 2, xa + 4, y1 + 2, 2, dark)
    g.paint(4, y1 + 2, 8, 8, y1 + 2, 8, "blue_dark")  # worn flap edge
    # lifted shoulder tab (front of the left strap)
    g.box(3, y1 + 1, 21, 4, y1 + 1, 22, dark)
    # drag loop at the back collar
    g.box(8, 0, 20, 12, 0, 20, "charcoal")
    g.box(8, 0, 21, 8, 0, 21, "charcoal")
    g.box(12, 0, 21, 12, 0, 21, "charcoal")
    g.box(8, 0, 22, 12, 0, 22, "charcoal")
    g.clear(9, 0, 21, 11, 0, 21)
    return g


# ---------------------------------------------------------------------------
# helmet
# ---------------------------------------------------------------------------
@model("helmet", name="Simple Helmet",
       story="An army-surplus steel helmet bought for a costume decades ago and kept in a "
             "basement. Somebody wore it for real afterwards: the crown is sun-faded, the front "
             "rim is scraped to bare metal, the left side carries a dent, and the unbuckled "
             "chin strap trails on the ground.",
       details=["Round steel dome with a narrow rolled rim", "Sun-faded crown",
                "Rim scraped bare at the front", "Shallow dent on the left side",
                "Khaki webbing chin strap trailing from the left, steel buckle"],
       exclusions=["No insignia, rank or unit markings", "No camouflage cover or net",
                   "No visible liner or suspension"],
       notes=["Army-surplus style olive helmet with chin strap.",
              "Rests on its rim with the strap on the ground, so it is lower than GPT's 25 cm "
              "reference (a helmet shell is about 17 cm tall)."])
def helmet():
    import math
    g = Grid(30, 27, 14)
    cx, cy, rx, ry, rz, q = 17.0, 13.0, 10.6, 12.2, 12.4, 2.15
    for x in range(30):
        for y in range(27):
            r = math.hypot((x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry)
            if r <= 1.0:
                h = rz * (1.0 - r ** q) ** (1.0 / q)  # dome, slightly fuller than an ellipse
                top = max(0, int(round(h - 0.5)))
                g.box(x, y, 0, x, y, top, "olive_dark")
                if top >= 9:
                    g.box(x, y, 9, x, y, top, "olive")  # sun-faded crown
            elif math.hypot((x + 0.5 - cx) / (rx + 1), (y + 0.5 - cy) / (ry + 1)) <= 1.0:
                g.set(x, y, 0, "green_deep")          # narrow flared lip
    g.paint(0, 0, 0, 29, 26, 0, "green_deep")         # rolled steel rim band
    # front rim scraped to bare steel
    for x in range(int(cx) - 6, int(cx) - 1):
        ys = [y for y in range(27) if g.get(x, y, 0)]
        if ys:
            g.set(x, ys[-1], 0, "steel_dark")
    # dent on the left (-X, camera) side
    for (y, z) in [(11, 4), (12, 4), (13, 4), (14, 4), (11, 5), (12, 5), (13, 5), (12, 6),
                   (13, 6)]:
        xs = [x for x in range(30) if g.get(x, y, z)]
        if xs:
            g.set(xs[0], y, z, 0)
            g.set(xs[0] + 1, y, z, "green_deep")
    # unbuckled chin strap: trailing from under the left rim along the ground to its buckle
    g.box(1, 13, 0, 6, 14, 0, "khaki_dark")
    g.box(1, 15, 0, 2, 17, 0, "khaki_dark")
    g.box(0, 18, 0, 3, 19, 0, "steel_dark")           # buckle
    g.paint(1, 18, 0, 2, 18, 0, "steel")
    g.box(1, 20, 0, 2, 21, 0, "khaki")                # cut, frayed end
    return g
