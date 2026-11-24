# Water Bottle
- Asset ID: Claude_water_bottle
- Base ID: water_bottle
- Creator: Claude
- Category: survival
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Inventory item water (hydration +30) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
One of the last sealed bottles from the corner shop's stockroom, still full and unopened.

Condition: **new**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.0875 m
- Depth (Y): 0.0875 m
- Height (Z): 0.2875 m
- Grid: 7 x 7 x 23 cells at 0.0125 m (micro tier), 510 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the working / interaction side.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [3.5, 3.5, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it.

## Materials and colors
`blue_hi`, `bluegrey`, `bluegrey_hi`, `bottle`, `bottle_cap`, `bottle_hi`, `label_blue`, `label_cream`

## Details included
- Full 1.5 L bottle: water level just under the shoulder
- Ribbed waist, plain cream label band with one blue stripe
- Blue screw cap above a neck collar

## Details excluded
- No brand text
- No transparency (opaque stylisation)

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.0875 x 0.0875 m

## Outputs
- `models/survival/Claude_water_bottle/Claude_water_bottle.vox` (editable master)
- `models/survival/Claude_water_bottle/model.json`
- `models/survival/Claude_water_bottle/Claude_water_bottle.glb` (derived)
- `previews/survival/Claude_water_bottle/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b2_survival_gear.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
