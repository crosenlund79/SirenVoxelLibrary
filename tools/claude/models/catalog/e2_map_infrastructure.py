"""Batch E2 - regional-map infrastructure (creator: Claude).

Real-world metres at 0.5 m cells. X right, Y front, Z up; inclusive cell ranges; z = 0 is the
ground / slab layer. Road pieces are single-layer slabs (0.5 m, the cell size; GPT's reference
is 0.4 m) and all share ONE cross-section so straight, curve, intersection, railway crossing
and bridge tile against each other:

    offset from the centre line (cells): 0 centre dash | 1-5 lane | 6 kerb | 7 sidewalk | 8 verge
    -> 17 cells = 8.5 m: two 2.5 m lanes, a 0.5 m dashed yellow centre line, 0.5 m kerbs,
       0.5 m sidewalks and 0.5 m grass verges.

Centre-line dashes are 2 m long with 2 m gaps (period 8 cells); every straight piece starts
and ends with a 1 m half-gap, so dashes continue across tile joints.
"""
import math

from catalog_registry import model
from voxkit import Grid

HALF = 8                      # cells from the centre line to the outer verge cell
SECTION = ["line_yellow", "asphalt", "asphalt", "asphalt", "asphalt", "asphalt",
           "curb", "concrete_hi", "grass"]


def section_colour(off, dash=True):
    """Colour for a cell at integer offset `off` from the centre line."""
    a = abs(off)
    if a > HALF:
        return "grass"
    c = SECTION[a]
    if a == 0 and not dash:
        return "asphalt"
    return c


def dash_on(s):
    """Dash pattern along a straight: s = cell index along the road from a tile end."""
    return 2 <= s % 8 <= 5


def straight_strip(g, x0, y0, y1, length_from=0):
    """Road along Y occupying x0..x0+16, rows y0..y1, on z = 0."""
    for y in range(y0, y1 + 1):
        s = y - y0 + length_from
        for off in range(-HALF, HALF + 1):
            g.set(x0 + HALF + off, y, 0, section_colour(off, dash_on(s)))


def wear_patch(g, x0, y0, x1, y1, c="asphalt_dark"):
    """Recolour asphalt cells only (patched repairs, worn tracks)."""
    for x in range(min(x0, x1), max(x0, x1) + 1):
        for y in range(min(y0, y1), max(y0, y1) + 1):
            if g.get(x, y, 0) in (_IDX["asphalt"], _IDX["asphalt_dark"]):
                g.set(x, y, 0, c)


def _idx():
    from voxkit import P
    return {k: P(k) for k in ("asphalt", "asphalt_dark", "asphalt_hi")}


_IDX = _idx()


# ---------------------------------------------------------------------------
# roads
# ---------------------------------------------------------------------------
@model("road_straight",
       silhouette="Flat 8.5 m road strip: dark asphalt, yellow centre dashes, pale kerbs and sidewalks, green verges.",
       story="A two-lane suburban street. Years of patching show in darker squares, a pothole "
             "has opened in one lane and grass has started to creep over the sidewalk.",
       details=["Shared road section: 2 x 2.5 m lanes, dashed yellow centre line, kerbs, "
                "sidewalks and verges", "Two patched repairs and one pothole",
                "Two kerb drains", "Dash phase continues across tile joints"],
       exclusions=["No vehicles", "No readable markings"],
       front_note="Road runs along Y; +Y is an arbitrary end (the tile is symmetric).",
       notes=["8.5 x 16 m (GPT reference 8 x 16 m): one cell wider so the centre line sits "
              "on a cell. Slab is one 0.5 m cell thick (reference 0.4 m)."])
def road_straight():
    g = Grid(17, 32, 1)
    straight_strip(g, 0, 0, 31)
    wear_patch(g, 9, 22, 13, 22)                         # trench repair across one lane
    wear_patch(g, 3, 6, 5, 9)                            # patched area around a pothole
    wear_patch(g, 4, 7, 4, 8, "asphalt_deep")
    g.set(3, 15, 0, "iron_dark")                         # kerb drains
    g.set(13, 26, 0, "iron_dark")
    for (x, y) in ((1, 3), (1, 4), (15, 22), (15, 23), (15, 24)):
        g.set(x, y, 0, "grass_dry")                      # grass creeping onto the sidewalk
    return g


@model("road_curve",
       silhouette="Square tile with the road section swept through a quarter circle, grass inside and outside the bend.",
       story="A 90-degree bend where the street turns along the creek. Drivers cut the "
             "corner for years and wore the inside verge bare; the outer lane is patched.",
       details=["Same section as the straight tile, swept around a 6.25 m centre-line "
                "radius", "Two dashes per bend so the dash rhythm meets the straight tiles",
                "Patched outer lane, worn inside verge"],
       exclusions=["No vehicles", "No readable markings"],
       front_note="Road enters at the +Y edge and leaves at the -X edge, centred on each "
                  "edge like the straight tile.",
       notes=["12.5 x 12.5 m (GPT reference 12 x 12 m) so the 17-cell section stays centred "
              "on both edges."])
def road_curve():
    N = 25
    g = Grid(N, N, 1)
    cx, cy, R = 0.0, 25.0, 12.5                          # bend centre at the -X / +Y corner
    arc = R * math.pi / 2
    for x in range(N):
        for y in range(N):
            px, py = x + 0.5, y + 0.5
            u = math.hypot(px - cx, py - cy) - R
            a = abs(u)
            if a < 0.5:
                s = R * math.atan2(cy - py, px - cx)
                on = 3.0 <= s < 7.0 or arc - 7.0 <= s < arc - 3.0
                c = "line_yellow" if on else "asphalt"
            elif a < 5.5:
                c = "asphalt"
            elif a < 6.6:
                c = "curb"
            elif a < 7.5:
                c = "concrete_hi"
            else:
                c = "grass"
            g.set(x, y, 0, c)
    # patched outer lane; worn verge where drivers cut across the inside corner
    wear_patch(g, 14, 6, 17, 9, "asphalt_dark")
    for (x, y) in ((4, 20), (5, 20), (4, 21)):
        g.set(x, y, 0, "grass_dry")
    return g


@model("road_intersection",
       silhouette="Plus-shaped asphalt crossing with zebra stripes on each arm and grass corner squares.",
       story="A four-way junction at the centre of the subdivision. The traffic lights were "
             "on another tile; here only the zebra crossings and the corner kerbs remain, "
             "worn white where buses turned.",
       details=["Four arms with the shared road section", "Zebra crossing on every arm",
                "Rounded kerb corners (1 m radius) with sidewalks wrapping the corners",
                "Grass corner squares, one patched arm"],
       exclusions=["No signals or signs", "No readable markings"],
       front_note="Symmetric; arms leave every edge centred like the straight tile.",
       notes=["12.5 x 12.5 m (GPT reference 12 x 12 m) to keep the 17-cell section centred."])
def road_intersection():
    N, C, A, R = 25, 12.5, 5.5, 2.0
    g = Grid(N, N, 1)
    for x in range(N):
        for y in range(N):
            X, Y = abs(x + 0.5 - C), abs(y + 0.5 - C)
            if X < A or Y < A:
                e = -1.0
            elif X < A + R and Y < A + R:
                e = R - math.hypot(A + R - X, A + R - Y)
            else:
                e = min(X, Y) - A
            if e < 0:
                c = "asphalt"
            elif e < 1:
                c = "curb"
            elif e < 2:
                c = "concrete_hi"
            else:
                c = "grass"
            g.set(x, y, 0, c)
    # zebra crossings on each arm (three cells deep, five stripes)
    for k in (-4, -2, 0, 2, 4):
        for d in (8, 9, 10):
            for (x, y) in ((12 + k, 12 + d), (12 + k, 12 - d), (12 + d, 12 + k),
                           (12 - d, 12 + k)):
                g.set(x, y, 0, "line_white")
    wear_patch(g, 14, 2, 16, 5, "asphalt_dark")          # patched arm
    return g


# ---------------------------------------------------------------------------
# crossings and bridges
# ---------------------------------------------------------------------------
@model("railway_crossing",
       silhouette="Road tile crossed by a ballasted track with raised rails, two signal posts and striped barrier arms down.",
       story="A level crossing on the freight line out of town. The barriers came down when "
             "the power failed and have stayed down ever since.",
       details=["Shared road section along Y crossed by a single track along X",
                "Ballast bed with timber sleepers, raised rails off the road and flush rails "
                "in the crossing panels", "Two crossing signals with paired red lamps and "
                "striped barrier arms lowered across the approach lanes",
                "Relay cabinet beside one signal"],
       exclusions=["No readable signs or crossbuck text", "No train"],
       notes=["Height 4 m (GPT reference 0.6 m): the brief's crossing signals and barrier "
              "arms cannot fit in a 0.6 m slab; the road slab itself stays one cell thick.",
              "12.5 x 12.5 m tile (reference 12 x 12 m) to centre the 17-cell road section."])
def railway_crossing():
    N = 25
    g = Grid(N, N, 8)
    g.box(0, 0, 0, N - 1, N - 1, 0, "grass")
    straight_strip(g, 4, 0, N - 1, length_from=0)
    # ballast and sleepers across the whole tile, crossing panels on the road
    for x in range(N):
        on_road = 6 <= x <= 18
        for y in range(9, 16):
            if on_road:
                g.set(x, y, 0, "concrete_dark")
            else:
                g.set(x, y, 0, "gravel")
                if 10 <= y <= 14 and x % 2 == 0:
                    g.set(x, y, 0, "wood_stain")
        for y in (11, 13):
            if on_road:
                g.set(x, y, 0, "steel")
            else:
                g.set(x, y, 1, "steel_light")
    # signals: post, lamp pair, barrier arm lowered across the approach lanes
    for (px, py, arm, cw) in ((3, 17, range(4, 12), 2), (21, 7, range(13, 21), 22)):
        g.box(px, py, 1, px, py, 7, "paint_white")
        g.box(px - 1, py, 6, px + 1, py, 6, "charcoal")
        g.set(px - 1, py, 6, "lamp_red")
        g.set(px + 1, py, 6, "lamp_red")
        g.box(px, py, 7, px, py, 7, "charcoal")
        for i, x in enumerate(arm):
            g.set(x, py, 2, "signal_red" if (i // 2) % 2 else "paint_white")
        g.set(cw, py, 2, "charcoal")                     # counterweight
        g.box(px, py, 1, px, py, 2, "galv_dark")
    g.box(22, 4, 1, 23, 5, 2, "galv")                    # relay cabinet
    g.paint(22, 4, 2, 23, 5, 2, "galv_hi")
    return g


@model("bridge",
       silhouette="Long road deck with posted steel railings on a central two-column pier and end abutments.",
       story="A two-span concrete road bridge over the creek on the county road. Its "
             "parapets are chipped where a truck once scraped along them, and the expansion "
             "joint over the pier has opened.",
       details=["Deck carrying the shared road section; kerbs with concrete posts every 2 m and "
                "a steel top rail in place of the verges", "0.5 m slab deck on a central pier of two columns under a cap "
                "beam, solid abutments", "Expansion joint over the pier, "
                "scraped kerb stretch where the top rail was torn away"],
       exclusions=["No water, no vehicles", "No readable markings"],
       front_note="Road runs along Y; +Y is an arbitrary end (symmetric piece).",
       notes=["8.5 x 20 x 2.5 m (GPT reference 8 x 19 x 2.2 m): 20 m keeps the 2 m dash "
              "rhythm whole across both ends; the 1 m railing (two cells) sets the 2.5 m height."])
def bridge():
    W, L = 17, 40
    g = Grid(W, L, 5)
    D = 2                                                # deck layer (top at 1.5 m)
    for y in range(L):
        for off in range(-HALF, HALF + 1):
            x = HALF + off
            if abs(off) == HALF:
                g.set(x, y, D, "concrete")                   # parapet kerb
                if y % 4 == 1 or y in (0, L - 1):
                    g.set(x, y, D + 1, "concrete_hi")        # railing posts every 2 m
                g.set(x, y, D + 2, "steel_light")            # continuous top rail
            else:
                g.set(x, y, D, section_colour(off, dash_on(y)))
    for x in range(1, W - 1):                             # opened expansion joint
        g.set(x, 20, D, "asphalt_dark")
    g.box(1, 19, D - 1, W - 2, 20, D - 1, "concrete_dark")  # pier cap beam
    for x0 in (3, 12):
        g.box(x0, 19, 0, x0 + 1, 20, D - 2, "concrete_dark")
    for (y0, y1) in ((0, 1), (L - 2, L - 1)):            # abutments
        g.box(0, y0, 0, W - 1, y1, D - 1, "concrete_deep")
        g.paint(0, y0, D - 1, W - 1, y1, D - 1, "concrete_dark")
    g.paint(0, 8, D, 0, 15, D + 2, "concrete_dark")       # scraped parapet
    g.paint(0, 8, D + 2, 0, 15, D + 2, "steel")
    g.clear(0, 11, D + 2, 0, 13, D + 2)                   # rail torn away
    return g


# ---------------------------------------------------------------------------
# waterfront
# ---------------------------------------------------------------------------
@model("harbor_dock",
       silhouette="Raised concrete jetty with black fenders and bollards round its edge, an orange jib crane and a crate stack.",
       story="A small concrete jetty in the fishing harbour. The last boats left in a hurry: "
             "a crate stack was abandoned on the quay and the jib crane still has its hook "
             "out over the water.",
       details=["1.5 m concrete jetty projecting from the shore (+Y) with joint lines",
                "Black rubber fenders and iron bollards along both sides and the end",
                "Yellow safety line, steps down to the water on the camera side",
                "Orange jib crane over the -X side, stacked timber crates and a pallet"],
       exclusions=["No water, no boats", "No readable markings"],
       front_note="+Y is the shore end; the jetty projects toward -Y with water on three "
                  "sides.",
       notes=["Crane raises the height to 4.5 m (reference 1.5 m slab): the brief asks for a "
              "small crane."])
def harbor_dock():
    W, L = 20, 32
    g = Grid(W, L, 10)
    X0, X1 = 1, W - 2
    g.box(X0, 0, 0, X1, L - 1, 2, "concrete")             # jetty slab 1.5 m
    g.paint(X0, 0, 2, X1, 0, 2, "concrete_hi")             # coping
    g.paint(X0, 0, 2, X0, L - 1, 2, "concrete_hi")
    g.paint(X1, 0, 2, X1, L - 1, 2, "concrete_hi")
    g.paint(X0, 0, 0, X1, L - 1, 0, "concrete_dark")      # wet base
    for y in range(4, L, 8):                               # joints
        g.paint(X0 + 1, y, 2, X1 - 1, y, 2, "concrete_dark")
    g.paint(X0 + 2, 2, 2, X0 + 2, L - 1, 2, "line_yellow")
    g.paint(X1 - 2, 2, 2, X1 - 2, L - 1, 2, "line_yellow")
    g.paint(X0 + 2, 2, 2, X1 - 2, 2, 2, "line_yellow")
    for y in range(3, L - 2, 6):                           # fenders
        g.box(0, y, 1, 0, y + 1, 2, "black")
        g.box(W - 1, y, 1, W - 1, y + 1, 2, "black")
    S0, S1 = 17, 20                                        # steps between two fenders
    for x in (5, 14):
        g.box(x, 0, 1, x + 1, 0, 2, "black")
    for y in (2, 10, 18, 26):                              # bollards
        g.set(X0 + 1, y, 3, "iron")
        g.set(X1 - 1, y, 3, "iron")
    # steps down to the water on the -X side
    g.clear(X0, S0, 1, X0 + 1, S1, 2)
    g.box(X0, S0, 0, X0, S1, 0, "concrete_hi")
    g.box(X0 + 1, S0, 1, X0 + 1, S1, 1, "concrete_hi")
    # jib crane
    g.box(4, 12, 3, 5, 13, 3, "concrete_dark")
    g.box(4, 12, 4, 5, 13, 8, "safety_orange_dark")
    g.box(0, 12, 9, 6, 13, 9, "safety_orange_dark")
    g.box(6, 12, 8, 6, 13, 8, "charcoal")                  # counterweight
    g.box(1, 12, 6, 1, 12, 8, "steel_dark")                 # hook line
    g.box(1, 12, 5, 1, 13, 5, "charcoal")
    # crates and a pallet
    g.box(11, 20, 3, 14, 23, 4, "pine_mid")
    g.paint(11, 20, 4, 14, 23, 4, "pine_light")
    g.box(11, 24, 3, 12, 25, 4, "card")
    g.box(13, 24, 3, 14, 25, 3, "card_dark")
    g.box(12, 21, 5, 13, 22, 5, "pine_aged")
    g.box(8, 27, 3, 10, 29, 3, "wgrey_mid")
    return g


@model("pier",
       silhouette="Narrow grey timber deck on paired piles whose heads stand proud along both edges.",
       story="A timber fishing pier off the beach road. A winter storm took two deck boards "
             "near the far end; the rest is grey and splintered but still walked on.",
       details=["Grey timber deck 1 m above the water on paired piles",
                "Pile heads standing proud of the deck along both edges",
                "Lighter worn walking line down the middle", "Two missing boards at the far "
                "end, steel ladder down to the water"],
       exclusions=["No water, no boats"],
       front_note="+Y is the shore end; the pier runs out toward -Y.")
def pier():
    W, L = 8, 30
    g = Grid(W, L, 3)
    g.box(0, 0, 1, W - 1, L - 1, 1, "wgrey")               # deck at 0.5-1.0 m
    for y in range(0, L, 4):
        g.paint(0, y, 1, W - 1, y, 1, "wgrey_mid")          # joist lines
    g.paint(3, 0, 1, 4, L - 1, 1, "wgrey_warm")             # worn walking line
    for y in list(range(1, L, 4)) + [L - 1]:
        for x in (0, W - 1):
            g.box(x, y, 0, x, y, 2, "wgrey_dark")           # piles, heads proud
        g.box(1, y, 0, W - 2, y, 0, "wgrey_deep")           # cross beam under the deck
    g.clear(5, 3, 1, 6, 4, 1)                               # storm-lost boards
    g.box(3, 0, 0, 4, 0, 0, "steel")                        # ladder
    g.paint(3, 0, 1, 4, 0, 1, "steel_light")
    return g


@model("seawall",
       silhouette="Long, three-step concrete revetment, green-stained at the foot, pale coping on top.",
       story="A stretch of stepped concrete seawall below the beach promenade. Storm waves "
             "have stained the lower steps green and opened one expansion joint.",
       details=["Three 0.5 m steps facing the sea with a pale coping on the promenade edge",
                "Algae and wet staining on the lowest step", "Expansion joint and a drain "
                "outfall in the bottom riser"],
       exclusions=["No water, no railings"],
       front_note="+Y is the stepped sea face (shown to the camera); the flat promenade "
                  "side is -Y.",
       notes=["10 x 1.5 x 2 m (GPT reference 10 x 1.2 x 2 m): three readable steps need "
              "three 0.5 m cells of depth."])
def seawall():
    g = Grid(20, 3, 4)
    g.box(0, 0, 0, 19, 0, 3, "concrete")
    g.box(0, 1, 0, 19, 1, 2, "concrete")
    g.box(0, 2, 0, 19, 2, 1, "concrete")
    g.paint(0, 0, 3, 19, 0, 3, "concrete_hi")               # coping
    g.paint(0, 2, 0, 19, 2, 1, "concrete_dark")             # wet lowest step
    g.paint(0, 2, 0, 19, 2, 0, "algae_dark")
    for x in (2, 3, 4, 11, 12, 16, 17, 18):
        g.paint(x, 2, 1, x, 2, 1, "algae")
    g.paint(9, 0, 0, 9, 2, 3, "concrete_deep")              # expansion joint
    g.paint(14, 2, 0, 15, 2, 0, "black")                    # drain outfall
    return g


@model("road_barrier",
       silhouette="Two short concrete barriers bridged by a red-and-white boom on a dark post, an orange cone at each.",
       story="A checkpoint line thrown across a road: two concrete barriers, a manual boom "
             "between them and a cone at each end. Whoever manned it is gone; the boom is "
             "still down.",
       details=["Two 1.5 m concrete barriers with a darker scuffed base",
                "Boom post with counterweight; striped arm lowered onto the right barrier",
                "A traffic cone in front of each barrier"],
       exclusions=["No readable signs", "No people or vehicles"],
       notes=["4.5 x 1.0 x 1.5 m (GPT reference 4 x 0.6 x 0.9 m): at 0.5 m cells the cones "
              "need their own row in front of the barrier line, and the boom must clear the "
              "barriers to read as a gate.", "Deliberately tiny (~25 voxels): a 4 m piece at "
              "0.5 m cells."])
def road_barrier():
    g = Grid(9, 2, 3)
    for (a, b) in ((0, 2), (6, 8)):                       # concrete barriers, 1.5 x 1 m
        g.box(a, 0, 0, b, 0, 1, "concrete_hi")
        g.paint(a, 0, 0, b, 0, 0, "concrete")
    g.box(3, 0, 0, 3, 0, 2, "charcoal")                   # boom post
    g.set(2, 0, 2, "iron")                                # counterweight
    for x in range(4, 9):                                 # striped arm resting on the barrier
        g.set(x, 0, 2, "signal_red" if x % 2 else "paint_white")
    g.set(1, 1, 0, "safety_orange")                       # cones
    g.set(7, 1, 0, "safety_orange")
    return g
