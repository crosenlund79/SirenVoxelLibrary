# Food Box
- Asset ID: Claude_food_box
- Base ID: food_box
- Creator: Claude
- Category: consumables
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_C
- Scale family: full
- Intended uses: Food pickup (crackers/cereal) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A family box of crackers torn open in a hurry: the back flap stands up, the front flap is folded out, the waxed inner bag is crumpled at the top and the front corner is creased where it was squeezed into a backpack.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.25 m
- Depth (Y): 0.1125 m
- Height (Z): 0.3 m
- Grid: 20 x 9 x 24 cells at 0.0125 m (micro tier), 1,348 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the label / opening side.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [10.0, 4.5, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it.

## Materials and colors
`card`, `card_hi`, `cream_shadow`, `label_cream`, `mustard`, `mustard_dark`, `paper`, `terra`

## Details included
- Printed card box: muted mustard with a cream window panel and a rust title band
- Open top: back flap standing, front flap folded forward, one dust flap out
- Crumpled waxed-paper inner bag showing at the opening
- Creased front-left corner

## Details excluded
- No text, logo, mascot or food photograph

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.25 x 0.1125 m

## Outputs
- `models/consumables/Claude_food_box/Claude_food_box.vox` (editable master)
- `models/consumables/Claude_food_box/model.json`
- `models/consumables/Claude_food_box/Claude_food_box.glb` (derived)
- `previews/consumables/Claude_food_box/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/c2_consumables.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
