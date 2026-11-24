"""One-off: re-key Claude's master manifest to GPT's 179 base IDs for automatic pairing.

    python3 tools/claude/manifest_align.py <gpt_manifest.json>

Inputs: the previous Claude manifest (docs/claude/manifest.json, game-informed briefs) and GPT's
docs/GPT_catalog_manifest.json (the reference list of object types). Output: the same file,
re-keyed so that every entry's base_id equals GPT's base_id, with:
  * gpt_id / gpt_dims_m / gpt_cell_m  - GPT's reference record (names and sizes only, no geometry)
  * prior_base_id                     - the earlier Claude name for traceability
  * batch A-F as commissioned on 2026-11-24, category = GPT's category (aligned folders)
  * existing_claude / alias           - existing Claude models that already satisfy an object
Claude-only extras from the earlier manifest are kept with batch "X" (no GPT counterpart).
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRIOR = ROOT / "docs/claude/manifest.json"

RENAME = {  # earlier Claude base_id -> GPT base_id
    "ammo_box": "ammunition_box", "ammo_pickup": "loose_ammo_pickup",
    "barricade_destroyed": "destroyed_barricade", "bicycle_abandoned": "abandoned_bicycle",
    "brick_wall_broken": "broken_brick_wall", "cooler_small": "small_cooler",
    "crockery_set": "dining_crockery", "desk_small": "small_desk",
    "generator_basic": "basic_generator", "helmet_simple": "helmet",
    "metal_fence_section": "metal_fence", "metal_gate": "metal_fence_gate",
    "pine_dead": "dead_pine", "pine_healthy": "healthy_pine", "player_survivor": "survivor",
    "psycho_bomber": "suicide_bomber", "psycho_brute": "brute",
    "psycho_ordinary": "ordinary_psycho", "psycho_runner": "runner", "shelf_small": "small_shelf",
    "shrub_dead": "dead_shrub", "smg_compact": "compact_smg",
    "storage_cabinet_small": "small_storage_cabinet", "stove_oven": "kitchen_oven",
    "tree_deciduous_leafless": "leafless_deciduous", "tree_leafy_small": "small_leafy_tree",
    "utility_truck_abandoned": "utility_truck", "water_container_large": "large_water_container",
    "wood_burning_stove": "wood_stove", "wooden_barricade_reinforced": "reinforced_wooden_barricade",
    "wooden_fence_section": "wooden_fence", "wooden_wall_damaged": "damaged_wooden_wall",
    "map_family_house_small": "small_family_house", "map_suburban_house_large": "large_suburban_house",
    "map_medical_clinic": "clinic", "map_quarry": "quarry_structure",
    "map_scrapyard": "scrapyard_building", "map_small_pier": "pier",
}
for k in ["apartment_block", "bridge", "convenience_store", "diner", "fast_food", "gas_station",
          "guard_tower", "gun_shop", "harbor_dock", "hardware_store", "hospital",
          "industrial_warehouse", "lumberyard", "military_outpost", "pharmacy", "police_station",
          "railway_crossing", "restaurant", "road_barrier", "road_curve", "road_intersection",
          "road_straight", "seawall", "shooting_range", "supermarket", "veterinary_clinic"]:
    RENAME["map_" + k] = k

BATCH = {"furniture": "A", "survival": "B", "construction": "B", "combat": "C",
         "consumables": "C", "vegetation": "D", "decorations": "D", "vehicles": "D",
         "map": "E", "characters": "F"}
BATCH_NAME = {"A": "Household", "B": "Survival and construction", "C": "Combat and consumables",
              "D": "Outdoors and vehicles", "E": "Regional voxel map", "F": "Characters and enemies",
              "X": "Claude-only extras (no GPT counterpart)"}
EXISTING = {  # GPT base_id -> existing Claude model that already satisfies it
    "single_bed": "Claude_single_bed_unmade", "workbench": "Claude_workbench_worn",
    "rainwater_collector": "Claude_rain_collector_basic", "wood_stove": "Claude_wood_stove_compact",
    "dead_pine": "Claude_pine_dead_small", "dining_table": "Claude_dining_table",
}


def main(gpt_path):
    prior = json.loads(PRIOR.read_text())
    gpt = json.loads(Path(gpt_path).read_text())
    by_new = {}
    for a in prior["assets"]:
        by_new[RENAME.get(a["base_id"], a["base_id"])] = a
    out = []
    for it in gpt["items"]:
        b = it["base_id"]
        p = by_new.get(b)
        batch = "C" if b == "handgun" else BATCH[it["category"]]
        e = {
            "base_id": b, "name": (p or {}).get("name", it["name"]).replace("Map: ", ""),
            "batch": batch, "batch_name": BATCH_NAME[batch],
            "category": it["category"],
            "family": (p or {}).get("family", ""),
            "gpt_id": it["id"], "gpt_dims_m": it["dimensions"], "gpt_cell_m": it["voxel_size_m"],
            "prior_base_id": (p or {}).get("base_id"),
            "prior_target_dims_m": (p or {}).get("target_dims_m"),
            "target_dims_m": it["dimensions"],
            "cell_m": (p or {}).get("cell_m", 0.05),
            "condition": (p or {}).get("condition", "used"),
            "gameplay_use": (p or {}).get("gameplay_use", ""),
            "brief": (p or {}).get("brief", ""),
            "existing_claude": EXISTING.get(b),
            "alias": EXISTING.get(b) if EXISTING.get(b, "").replace("Claude_", "") != b else None,
        }
        out.append(e)
    extras = [a for a in prior["assets"] if RENAME.get(a["base_id"], a["base_id"]) not in
              {i["base_id"] for i in gpt["items"]}]
    for a in extras:
        out.append({"base_id": a["base_id"], "name": a["name"], "batch": "X",
                    "batch_name": BATCH_NAME["X"], "category": a["category"],
                    "family": a["family"], "gpt_id": None, "gpt_dims_m": None, "gpt_cell_m": None,
                    "prior_base_id": a["base_id"], "prior_target_dims_m": a["target_dims_m"],
                    "target_dims_m": a["target_dims_m"], "cell_m": a["cell_m"],
                    "condition": a["condition"], "gameplay_use": a["gameplay_use"],
                    "brief": a["brief"], "existing_claude": None, "alias": None})
    doc = {
        "schema_version": 2,
        "description": ("Claude's master manifest, keyed by GPT's 179 base IDs so GPT_<id> and "
                        "Claude_<id> pair automatically. Briefs come from the earlier, "
                        "game-informed Claude manifest; GPT's record supplies names, categories "
                        "and reference sizes only (no geometry). target_dims_m defaults to GPT's "
                        "reference size for a fair comparison; prior_target_dims_m keeps the "
                        "earlier game-informed estimate."),
        "sources": prior.get("sources", []) + ["GPT docs/GPT_catalog_manifest.json "
                                               "(gpt/complete-catalog @ aa6be83)",
                                               "User commission 2026-11-24 (rival catalog)"],
        "batches": BATCH_NAME,
        "assets": out,
    }
    PRIOR.write_text(json.dumps(doc, indent=1) + "\n")
    print(len(out), "entries;", sum(1 for e in out if e["batch"] != "X"), "paired with GPT;",
          len(extras), "Claude-only extras;", sum(1 for e in out if e["existing_claude"]),
          "already covered by existing Claude models")


if __name__ == "__main__":
    main(sys.argv[1])
