# Food Storage Crate
- Asset ID: Claude_food_storage_crate
- Base ID: food_storage_crate
- Creator: Claude
- Category: consumables
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_C
- Scale family: full
- Intended uses: Pantry/stockpile storage (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A ventilated stacking crate from a garage pantry shelf, half emptied: tins stacked two high at the front, jars of preserves at the back, a gap where the first tins were taken. Its lid leans against the back where it was dropped.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.45 m
- Depth (Y): 0.3625 m
- Height (Z): 0.325 m
- Grid: 36 x 29 x 26 cells at 0.0125 m (micro tier), 7,627 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the label / opening side.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [18.0, 14.5, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it. Overridden from 2.5 cm to 1.25 cm so the tins and jars inside are built at the same scale and roundness as the canned_food and soup_can pickups (6-7 cell circles, not 3-cell squares).

## Materials and colors
`galv`, `glass_hi`, `iron_warm`, `label_cream`, `label_green`, `label_red`, `mustard_dark`, `red_dark`, `rust`, `sage`, `sage_dark`, `sage_hi`, `steel_dark`, `steel_light`

## Details included
- Grey-green plastic crate with two bands of vent slots and end hand-holds
- Rolled top lip
- Stacks of tins (green and red labels) and three jars with lids
- Gap at the front-left where tins were taken
- Ribbed lid leaning against the back

## Details excluded
- No brand or text on the tins or crate
- No loose food

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.45 x 0.3625 m

## Outputs
- `models/consumables/Claude_food_storage_crate/Claude_food_storage_crate.vox` (editable master)
- `models/consumables/Claude_food_storage_crate/model.json`
- `models/consumables/Claude_food_storage_crate/Claude_food_storage_crate.glb` (derived)
- `previews/consumables/Claude_food_storage_crate/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/c2_consumables.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
