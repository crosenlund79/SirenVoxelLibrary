# Canned Food
- Asset ID: Claude_canned_food
- Base ID: canned_food
- Creator: Claude
- Category: consumables
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_C
- Scale family: full
- Intended uses: Inventory item canned_food (hunger +30) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A tall tin of vegetables from the back of a pantry shelf, still sealed. It was knocked off the shelf at some point: one small dent creases the label near the base.

Condition: **new**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.1 m
- Depth (Y): 0.1 m
- Height (Z): 0.1375 m
- Grid: 8 x 8 x 11 cells at 0.0125 m (micro tier), 358 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the label / opening side.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [4.0, 4.0, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it.

## Materials and colors
`galv`, `label_cream`, `label_green`, `leaf_dark`, `leaf_mid`, `steel`, `steel_dark`, `steel_light`

## Details included
- Clean 8-cell round tin with rolled top and bottom seams
- Flat lid with a bright rolled seam
- Muted green paper label with a cream band
- Two rib lines pressed through the label
- One small dent near the base

## Details excluded
- No text, brand or picture on the label
- No ring-pull (see soup_can)

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.1 x 0.1 m

## Outputs
- `models/consumables/Claude_canned_food/Claude_canned_food.vox` (editable master)
- `models/consumables/Claude_canned_food/model.json`
- `models/consumables/Claude_canned_food/Claude_canned_food.glb` (derived)
- `previews/consumables/Claude_canned_food/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/c2_consumables.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
