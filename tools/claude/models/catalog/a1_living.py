"""Batch A1 - living room (creator: Claude). X right, Y front (+Y), Z up; inclusive cells."""
from catalog_registry import model
from voxkit import Grid


@model("sofa", name="Three-Seat Sofa",
       story="A slate-blue three-seater from a family living room. The middle cushion has sagged "
             "from years of the same person sitting there, the right cushion was pulled forward "
             "and never pushed back, and a mustard throw still lies folded over the left arm.",
       details=["Three seat and three back cushions with seams", "Rolled arms with hand-rubbed fronts",
                "Low dark wooden feet", "Folded knitted throw draped over the left arm"],
       exclusions=["No pattern noise in the fabric", "No scatter cushions pile"])
def sofa():
    W, D = 45, 19                                   # 2.25 x 0.95 m
    g = Grid(W + 2, D + 1, 18)
    o = 1                                           # x offset: room for the throw's drape
    for (fx, fy) in [(1, 2), (W - 3, 2), (1, D - 3), (W - 3, D - 3)]:
        g.box(o + fx, fy, 0, o + fx + 1, fy + 1, 1, "wood_stain")      # feet
    g.box(o, 1, 2, o + W - 1, D - 1, 5, "slate_dark")                   # upholstered base
    g.paint(o, D - 1, 2, o + W - 1, D - 1, 2, "slate_deep")             # lower front shadow band
    for x0 in (0, W - 4):                                               # rolled arms
        g.box(o + x0, 1, 6, o + x0 + 3, D - 1, 11, "slate")
        g.box(o + x0, 1, 12, o + x0 + 3, D - 2, 12, "slate")
        g.box(o + x0 + 1, 1, 13, o + x0 + 2, D - 3, 13, "slate_hi")     # rounded top crown
        g.paint(o + x0 + 1, D - 1, 9, o + x0 + 2, D - 1, 11, "slate_dark")  # rubbed fronts
    # back cushions, leaning back, rounded tops, seams between them
    for i, (x0, x1) in enumerate([(4, 16), (17, 28), (29, W - 5)]):
        g.box(o + x0, 1, 6, o + x1, 5, 15, "slate")
        g.box(o + x0 + 1, 1, 16, o + x1 - 1, 4, 16, "slate")
        g.box(o + x0, 6, 8, o + x1, 6, 13, "slate")                      # cushion belly
        g.paint(o + x0, 1, 6, o + x0, 6, 16, "slate_dark")               # seam
    g.box(o + 4, 0, 4, o + W - 5, 0, 13, "slate_dark")                    # back panel
    # seat cushions: left normal, middle sagging, right pulled forward
    g.box(o + 4, 7, 6, o + 16, D - 1, 8, "slate")
    g.box(o + 17, 7, 6, o + 28, D - 1, 7, "slate")
    g.box(o + 17, 7, 8, o + 18, D - 1, 8, "slate")                        # sag: edges stay up
    g.box(o + 27, 7, 8, o + 28, D - 1, 8, "slate")
    g.box(o + 18, 8, 8, o + 27, 9, 8, "slate")
    g.box(o + 29, 8, 6, o + W - 5, D, 8, "slate")                         # pulled forward 5 cm
    g.box(o + 4, 7, 6, o + W - 5, D, 6, "slate_dark")                     # cushion undersides
    for (x0, x1) in [(4, 16), (17, 28), (29, W - 5)]:
        g.paint(o + x0, 7, 8, o + x1, D, 8, "slate_hi")                   # lit tops
    g.paint(o + 19, 10, 7, o + 26, D - 2, 7, "slate")                     # sag hollow stays mid
    # folded throw over the left arm, hanging down the outside
    g.box(o + 0, 7, 13, o + 3, 13, 13, "mustard_dark")
    g.box(o - 1, 7, 6, o - 1, 13, 13, "mustard_dark")
    g.paint(o - 1, 7, 6, o - 1, 13, 6, "mustard_deep")                    # hem
    for y in (9, 11):
        g.paint(o - 1, y, 7, o - 1, y, 12, "mustard_deep")                # knit folds
    g.box(o + 1, 7, 13, o + 3, 13, 13, "mustard")
    return {"grid": g, "footprint_cells": ((o, o + W - 1), (1, D - 1))}
