# Claude catalog — production style guide

This guide turns `docs/VOXEL_ART_BIBLE.md` into concrete, repeatable decisions for the full Claude catalog (about 180 candidates). **The art bible remains the authority**; where this guide is more specific, it records Claude's interpretation for the user to accept or reject. It applies only to `Claude_` models; GPT is not bound by it.

Reference models: the five pilot candidates (`Claude_pilot_001`) and `Claude_dining_table` (generator `tools/claude/models/dining_table.py`), which shows the expected generator layout, metadata and restraint.

## 1. One world

Contemporary suburban survival after an unexplained catastrophe. Overcast, quiet, slightly eerie. Objects are ordinary, believable and unbranded, slightly simplified for readability.

- **Condition varies on purpose.** Each model records a `condition`: `new`, `lightly_used`, `used`, `worn`, `damaged`, `improvised`, `abandoned`, `destroyed` (or `living` / `dead` / `n/a`). Across a family, mix them: a nearly new side table beside a worn sofa. Do not make everything equally battered.
- **Every model has a small story** (`META["story"]`): one or two sentences about who used it and what happened. Details should follow from that story (a drawer pulled out in a hurry, a forearm-polished edge, a sock caught in a washer seal), not from a wish to add noise.
- **Wear lives where hands, feet, water, heat and weather go.** Edges, handles, feet, tops, burners, the windward side. No uniform speckle, no random single-voxel confetti, no decal-like rectangles in the middle of a clean surface.

## 2. Resolution tiers

Choose **the coarsest tier that keeps the silhouette and function readable**, record the reason in `resolution_rationale`, and keep the same tier inside a family so objects that meet in a room share a voxel rhythm.

| Tier | Cell | Used for | Examples |
|---|---:|---|---|
| `micro` | 0.0125 m | Pickups and hand items under ~0.45 m that would be 3–6 cells at 0.025 | cans, bottles, pistols, hammer, flashlight, candle, medicine |
| `fine` | 0.025 m | Handhelds 0.45–1.2 m and small gear | shotgun, rifle, crowbar, shovel, backpack, generator, cone, pallet |
| `detail` | 0.05 m | Furniture, appliances, fixtures, workshop furniture, characters, mid-size outdoor props | sofa, fridge, toilet, crate, mailbox, characters (the game's character rig is 0.05 m) |
| `standard` | 0.10 m | Structural construction modules, vehicles, trees, poles | walls, floors, foundations, cars, pines, streetlights (the game's structure grid is 0.1 m) |
| `map` | 0.50 m | Regional-map buildings and infrastructure (real-world metres, far fewer voxels) | houses, hospital, roads, bridge |

All tiers are integer multiples of 0.0125 m, so mixed scenes (a pot on a stove, tools on a bench) compose on one grid. Doors, windows, barricades and gates are game props with thin members, so they use `detail` even though walls use `standard`.

**Budgets** (guides, not limits; `validate.py` warns above them): under ~10k voxels for ordinary furniture, ~20k for featured objects, ~30k for the largest map buildings. Never fill invisible interiors: mattresses, tanks, bodies and buildings are closed shells (the validator warns when more than 25 % of voxels are hidden).

## 3. Axes, front and pivot

Library axes: **X right, Y front, Z up**; the model's front faces **+Y**. Models stand on z = 0 with no floating parts.

| Family | Front (+Y) | Pivot | Notes |
|---|---|---|---|
| Furniture, appliances, props | the side a person uses (doors, drawers, seat, controls) | bottom centre of the body footprint | overhangs (handles, a drooping blanket) are excluded from `footprint_cells` |
| Wall-mounted items | the side facing into the room; back face flat for the wall | bottom centre of the back face | add `META["mount"] = {"type": "wall", "recommended_bottom_height_m": ...}` |
| Handheld tools and weapons | **working end / muzzle points +Y**, top side up (+Z), lowest point on z = 0 | bottom centre | add a `grip` attachment (cell where the main hand holds it); this is the held orientation for a character facing +Y |
| Wall / floor construction modules | outside face of a wall is +Y; a module fills exactly its 1 m (or 2 m) span | bottom centre | dimensions match the game: wall 1.0 m wide, 2.6 m high, 0.2 m (built) or 0.3 m (exterior) thick; door opening 1.0 × 2.1 m |
| Vehicles | the vehicle's nose is +Y | bottom centre between the axles | |
| Characters | the character faces +Y, neutral standing pose, arms slightly away from the body | between the feet | 0.05 m cells like the game rig; player height 1.75 m |
| Map buildings | main entrance / street side is +Y | bottom centre | real-world metres at 0.5 m cells; map tiles are 20 × 20 m with roads along Y for the straight tile |

## 4. Palette

All new models use **palette v2** (`tools/claude/voxkit.py`): the 112 pilot colours unchanged plus new rows (ceramic/enamel, glass and screens, slate/mauve/mustard/terracotta/sage/teal upholstery and paint matching Sirens Went Quiet's props, leather, cardboard, skin, hair and clothes, foliage, conifer, asphalt and road paint, vehicle paints, roofing/siding, plastics and labels). Use palette roles by name (`"pine_light"`, `"porcelain"`, `"slate"`).

- One material = one ramp, used as light / mid / shadow blocks, not as dithering.
- Most surfaces stay quiet; contrast goes to edges, openings, controls and meaningful damage.
- The `signal_*`, `hazard_*`, `safety_orange*` and `lamp_*` accents are rare: a medical cross, a cone, a hazard stripe, an unlit lightbar. Nothing glows; no emissive colours.
- Glass is opaque (`glass*`, `screen*`). Water is opaque (`water*`).
- No logos, brand shapes, readable text or real department names. Labels are plain colour blocks.

## 5. Construction rules

1. Silhouette first, then secondary masses, then a few functional details. A detail thinner than one cell is either exaggerated to one cell on purpose or left out.
2. Show how it is built: legs under tops, hinges on doors, valves on pipes, wheels on axles.
3. One 6-connected piece. If a model genuinely needs separate pieces (a set of plates, a scatter of rounds), set `META["allowed_components"]` and `META["components_reason"]`; prefer joining them on a cloth, tray or base.
4. Real thickness: do not make cloth, boards or blades thicker than the tier forces. If a part would become a toy-like slab at the chosen tier, reconsider the tier.
5. No baked lighting: do not darken faces to fake shadows; the renderer and game light the model. Local occlusion colours (a darker underside of a drawer slot, grime at a foot) are fine.
6. Small loose items (plates, tools, cans) are their own models, not baked onto furniture, unless they are part of the object's story and inseparable (a book on a nightstand is fine; a full dinner service on a table is not).

## 6. Generator contract (`tools/claude/models/<base_id>.py`)

```python
BASE_ID = "sofa"; CATEGORY = "furniture"; NAME = "Worn Three-Seat Sofa"
CELL = 0.05; BATCH = "catalog_A"            # SCALE = "map" for regional assets
def build():  # -> {"grid": Grid, "cell": CELL, "footprint_cells": ((x0, x1), (y0, y1))}
    ...       #    or "pivot_cells": (px, py, 0); optional "attachments": {"grip": (x, y, z)}
META = {"story", "condition", "gameplay_use", "silhouette", "details", "exclusions",
        "resolution_tier", "resolution_rationale", "pivot_note", "front_note", "notes",
        "attachments", "collision_hint"}      # optional: mount, allowed_components, variant_of, pairs_with
```

Generators are deterministic (use `voxkit.hash01` for any controlled variation, never `random`). The `.vox` is the editable master; once a person edits it in MagicaVoxel, that file wins.

## 7. Pipeline

```bash
python3 tools/claude/build.py <base_id>                                   # .vox, model.json, .glb, spec page
python3 tools/claude/render_previews.py <base_id> --quick --out <scratch>  # fast iteration renders
python3 tools/claude/render_previews.py <base_id>                          # final hero/front/side/scale
python3 tools/claude/validate.py <base_id>                                 # format, counts, GLB, Goxel, lints
python3 tools/claude/sheets.py ...                                         # batch/category sheets, scenes
python3 tools/claude/catalog_sync.py                                       # catalog.json + catalog page (lead only)
python3 tools/claude/manifest.py                                           # manifest status from disk
```

## 8. Review checklist (every model, before it is called done)

- [ ] Recognisable from the hero thumbnail alone, without reading the label.
- [ ] Proportions right beside the 1.75 m figure in `scale.png` (seat ~0.45 m, worktop ~0.9 m, door 2.1 m).
- [ ] Front is +Y and obvious; pivot and ground contact correct; nothing floating.
- [ ] Materials separate by value, not only hue; dark parts do not merge into one blob.
- [ ] Wear tells the story and is localised; no noise, no stickers.
- [ ] Consistent with its family (same tier, same palette ramps, same level of detail).
- [ ] `validate.py` passes with no unexplained warnings.

Passing validation is not approval. Every model stays a **candidate** until the user decides.
