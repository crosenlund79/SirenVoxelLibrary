# First-Aid Kit
- Asset ID: Claude_first_aid_kit
- Base ID: first_aid_kit
- Creator: Claude
- Category: consumables
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_C
- Scale family: full
- Intended uses: Inventory item 'medkit' (health +50) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A hard-case first-aid kit that hung on a utility-room wall for years and was carried out to the car when things went wrong. The off-white plastic is grubby along the bottom and scuffed at the corners; it still closes.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.375 m
- Depth (Y): 0.1375 m
- Height (Z): 0.2625 m
- Grid: 30 x 11 x 21 cells at 0.0125 m (micro tier), 1,912 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the label / opening side.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [15.0, 5.5, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it.

## Materials and colors
`charcoal`, `iron_edge`, `porcelain`, `porcelain_deep`, `porcelain_mid`, `porcelain_shadow`, `signal_red`

## Details included
- Off-white clamshell case with rounded corners and a visible parting line
- Large red cross on the front
- Dark carry handle and two latches on top
- Hinge knuckles along the bottom, wall-hanging slots on the back
- Grubby bottom edge and scuffed corners

## Details excluded
- No text, symbols other than the cross, or brand

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.375 x 0.1375 m

## Outputs
- `models/consumables/Claude_first_aid_kit/Claude_first_aid_kit.vox` (editable master)
- `models/consumables/Claude_first_aid_kit/model.json`
- `models/consumables/Claude_first_aid_kit/Claude_first_aid_kit.glb` (derived)
- `previews/consumables/Claude_first_aid_kit/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/c2_consumables.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
