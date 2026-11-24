"""Showcase scenes: do the catalog models belong to one world when they stand together?

    python3 tools/claude/scenes.py catalog_A          # every scene of a batch
    python3 tools/claude/scenes.py catalog_A kitchen  # one scene

Each scene places actual catalog .vox models (no edits, no stand-ins) by their pivots, using
their real dimensions from model.json, and renders a three-quarter review view plus the
game-camera angle into previews/scenes/Claude_<batch>_<scene>.png / _gamecam.png.
A scene is skipped (and reported) if any model it needs has not been generated yet.
Rotation: rot=1 turns a model's front to -X, rot=2 to -Y, rot=3 to +X.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

import sheets  # noqa: E402


def meta(base):
    hits = list(ROOT.glob(f"models/*/Claude_{base}/model.json"))
    return json.loads(hits[0].read_text()) if hits else None


def have(*ids):
    return all(meta(i) for i in ids)


def W(b):
    return meta(b)["dimensions_m"][0]


def Dp(b):
    return meta(b)["dimensions_m"][1]


def H(b):
    return meta(b)["dimensions_m"][2]


def S(b, x, y, z=0.0, rot=0):
    return {"id": b, "x": round(x, 3), "y": round(y, 3), "z": round(z, 4), "rot": rot}


def top(b, fx=0.5, fy=0.5):
    return sheets.top_height(b, fx, fy)


# ---------------------------------------------------------------------------
# Batch A - household
# ---------------------------------------------------------------------------
def a_dining():
    need = ["dining_table", "dining_chair", "sideboard", "crockery_set"]
    if not have(*need):
        return need
    t = "dining_table"
    ps = [S(t, 0, 0)]
    off = Dp(t) / 2 + 0.12
    for x in (-0.42, 0.42):
        ps.append(S("dining_chair", x, off, rot=2))      # front side, facing the table (-Y)
        ps.append(S("dining_chair", x, -off, rot=0))     # back side, facing +Y
    ps.append(S("crockery_set", -0.2, 0.05, z=top(t)))
    ps.append(S("sideboard", 0.0, -off - 0.9, rot=0))
    if have("stool"):
        ps.append(S("stool", W(t) / 2 + 0.6, 0.2))
    if have("shelf_small"):
        ps.append(S("shelf_small", -W(t) / 2 - 0.9, -off - 0.75))
    return ("dining", "Dining corner", "dining_table + dining_chair x4 + crockery_set + sideboard",
            ps, (W(t) / 2 + 1.3, 0.9))


def a_kitchen():
    need = ["kitchen_counter", "kitchen_sink", "stove_oven", "refrigerator", "cooking_pot"]
    if not have(*need):
        return need
    ps, x = [], 0.0
    row = ["refrigerator", "kitchen_counter", "stove_oven", "kitchen_counter", "kitchen_sink"]
    if have("pantry_shelf"):
        row = ["pantry_shelf"] + row
    xs = {}
    for b in row:
        w = W(b)
        if b == "refrigerator" or b == "pantry_shelf":
            w = meta(b).get("footprint_m", [w])[0]
        ps.append(S(b, x + w / 2, -Dp(b) / 2 + 0.31))
        xs.setdefault(b, []).append(x + w / 2)
        x += w + 0.02
    sx = xs["stove_oven"][0]
    cook = top("stove_oven", 0.5, 0.75)
    ps.append(S("cooking_pot", sx - 0.13, 0.08, z=cook))
    if have("kettle"):
        ps.append(S("kettle", sx + 0.15, -0.05, z=cook))
    c2 = xs["kitchen_counter"][-1]
    wt = top("kitchen_counter", 0.5, 0.7)
    if have("cutting_board"):
        ps.append(S("cutting_board", c2, 0.05, z=wt))
    if have("frying_pan"):
        ps.append(S("frying_pan", xs["kitchen_counter"][0], 0.02, z=wt))
    if have("wall_cabinet"):
        ps.append(S("wall_cabinet", xs["kitchen_counter"][0], -0.31 + Dp("wall_cabinet") / 2, z=1.45))
        ps.append(S("wall_cabinet", c2, -0.31 + Dp("wall_cabinet") / 2, z=1.45))
    return ("kitchen", "Kitchen run", "units, appliances and kitchenware placed on the cooktop "
            "and worktop", ps, (x + 0.6, 0.8))


def a_living():
    need = ["sofa", "coffee_table", "tv_cabinet", "television"]
    if not have(*need):
        return need
    ps = []
    if have("rug"):
        ps.append(S("rug", 0, 0.35))
    ps.append(S("sofa", 0, -0.75, rot=0))
    ps.append(S("coffee_table", 0, 0.45))
    tvc_y = 1.9
    ps.append(S("tv_cabinet", 0, tvc_y, rot=2))
    ps.append(S("television", 0, tvc_y, z=top("tv_cabinet", 0.5, 0.5), rot=2))
    if have("armchair"):
        ps.append(S("armchair", W("sofa") / 2 + 0.75, 0.3, rot=1))
    if have("floor_lamp"):
        ps.append(S("floor_lamp", -W("sofa") / 2 - 0.35, -0.85))
    if have("side_table"):
        ps.append(S("side_table", W("sofa") / 2 + 0.35, -0.8))
    if have("bookshelf"):
        ps.append(S("bookshelf", -W("sofa") / 2 - 0.9, 1.0, rot=3))
    if have("potted_plant"):
        ps.append(S("potted_plant", W("sofa") / 2 + 0.6, 1.8))
    if have("storage_cabinet_small"):
        ps.append(S("storage_cabinet_small", -1.6, 1.95, rot=2))
    return ("living", "Living room", "sofa facing the TV across the rug, armchair, lamp, shelves",
            ps, (W("sofa") / 2 + 1.7, -0.6))


def a_bedroom():
    need = ["double_bed", "nightstand", "wardrobe"]
    if not have(*need):
        return need
    b = "double_bed"
    ps = [S(b, 0, 0)]
    hy = -Dp(b) / 2 + 0.25
    ps.append(S("nightstand", -W(b) / 2 - 0.3, hy))
    ps.append(S("nightstand", W(b) / 2 + 0.3, hy))
    ps.append(S("wardrobe", -W(b) / 2 - 1.3, 0.6, rot=3))
    if have("dresser"):
        ps.append(S("dresser", W(b) / 2 + 1.25, 0.5, rot=1))
    if have("desk_small"):
        ps.append(S("desk_small", 0.2, Dp(b) / 2 + 1.0, rot=2))
        if have("desk_chair"):
            ps.append(S("desk_chair", 0.2, Dp(b) / 2 + 0.45, rot=0))
    if have("single_bed_unmade"):
        pass
    return ("bedroom", "Bedroom", "double bed, nightstands, wardrobe, dresser, desk", ps,
            (W(b) / 2 + 1.0, Dp(b) / 2 + 0.6))


def a_bath_utility():
    need = ["toilet", "bathtub", "bathroom_sink", "washing_machine", "clothes_dryer"]
    if not have(*need):
        return need
    ps = [S("bathtub", 0, 0), S("toilet", W("bathtub") / 2 + 0.45, -0.05),
          S("bathroom_sink", W("bathtub") / 2 + 1.25, -Dp("bathtub") / 2 + Dp("bathroom_sink") / 2)]
    if have("medicine_cabinet"):
        sx = W("bathtub") / 2 + 1.25
        ps.append(S("medicine_cabinet", sx, -Dp("bathtub") / 2 + Dp("medicine_cabinet") / 2,
                    z=max(1.25, H("bathroom_sink") + 0.3)))
    x0 = W("bathtub") / 2 + 2.3
    ps += [S("washing_machine", x0 + 0.32, -0.08), S("clothes_dryer", x0 + 0.98, -0.08)]
    if have("water_heater"):
        ps.append(S("water_heater", x0 + 1.75, -0.05))
    if have("laundry_basket"):
        ps.append(S("laundry_basket", x0 + 0.65, 0.75))
    if have("cardboard_boxes"):
        ps.append(S("cardboard_boxes", x0 + 2.6, 0.0))
    return ("bath_utility", "Bathroom and utility room", "fixtures and appliances side by side",
            ps, (-W("bathtub") / 2 - 0.7, 0.4))


def a_supplies():
    need = ["dining_table", "canned_food", "soup_can", "water_bottle"]
    if not have(*need):
        return need
    t = "dining_table"
    z = top(t)
    ps = [S(t, 0, 0)]
    small = [b for b in ["canned_food", "soup_can", "food_box", "snack_package", "water_bottle",
                         "kettle", "candle", "bandage_roll", "medicine_bottle"] if have(b)]
    x = -W(t) / 2 + 0.15
    for b in small:
        ps.append(S(b, x, 0.1, z=z))
        x += max(W(b), 0.08) + 0.06
    floor = [b for b in ["water_container_large", "food_storage_crate", "cooler_small"] if have(b)]
    x = -W(t) / 2
    for b in floor:
        ps.append(S(b, x + W(b) / 2, Dp(t) / 2 + 0.5))
        x += W(b) + 0.2
    return ("supplies", "Supplies on the table", "consumable pickups at true scale on the dining "
            "table, bulk storage on the floor", ps, (W(t) / 2 + 0.7, 0.9))


SCENES = {"catalog_A": [a_dining, a_kitchen, a_living, a_bedroom, a_bath_utility, a_supplies]}


def run(batch, only=None):
    for fn in SCENES.get(batch, []):
        res = fn()
        if isinstance(res, list):
            print(f"skip {fn.__name__}: missing {[m for m in res if not meta(m)]}")
            continue
        name, title, sub, ps, ref = res
        if only and name != only:
            continue
        sheets.render_scene(ps, ROOT / "previews" / "scenes" / f"Claude_{batch}_{name}.png",
                            f"Claude_{batch} · {title}", sub, ref_at=ref, grid=1.0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    run(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
