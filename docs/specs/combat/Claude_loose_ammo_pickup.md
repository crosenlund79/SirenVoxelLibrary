# Loose Ammunition
- Asset ID: Claude_loose_ammo_pickup
- Base ID: loose_ammo_pickup
- Creator: Claude
- Category: combat
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_C
- Scale family: full
- Intended uses: Inventory item 'ammo' (9 mm rounds) pickup (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A spare pistol magazine and the handful of rounds that spilled out of a torn cardboard box in a glovebox. Someone thumbed a few back in and dropped the rest.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.2 m
- Depth (Y): 0.1 m
- Height (Z): 0.0375 m
- Grid: 16 x 8 x 3 cells at 0.0125 m (micro tier), 105 occupied voxels
- Front direction: +Y (library voxel)
- Front: Working end / muzzle points +Y, top side up; lowest point on z = 0.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [8.0, 4.0, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it.

## Materials and colors
`black`, `brass`, `charcoal`, `copper`, `iron`, `iron_edge`, `steel_dark`

## Details included
- Pistol magazine lying on its side: dark body, worn spine edge, witness holes, base plate
- Top round seated in the feed lips
- Eight loose rounds (brass case, copper bullet), one standing on its base, one resting on the others, all touching the magazine or each other

## Details excluded
- No box or packaging
- No spent casings
- No headstamp or markings

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.2 x 0.1 m

## Outputs
- `models/combat/Claude_loose_ammo_pickup/Claude_loose_ammo_pickup.vox` (editable master)
- `models/combat/Claude_loose_ammo_pickup/model.json`
- `models/combat/Claude_loose_ammo_pickup/Claude_loose_ammo_pickup.glb` (derived)
- `previews/combat/Claude_loose_ammo_pickup/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/c1_combat.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
