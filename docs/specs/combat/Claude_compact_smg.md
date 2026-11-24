# Compact Submachine Gun
- Asset ID: Claude_compact_smg
- Base ID: compact_smg
- Creator: Claude
- Category: combat
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_C
- Scale family: full
- Intended uses: Planned weapon (police/military loot) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A compact submachine gun from a patrol car's locked rack, taken when the car was found abandoned at an intersection. The skeletal stock is still folded; the receiver's edges and the magazine's base are worn grey from being dragged.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.0625 m
- Depth (Y): 0.5 m
- Height (Z): 0.225 m
- Grid: 5 x 40 x 18 cells at 0.0125 m (micro tier), 908 occupied voxels
- Front direction: +Y (library voxel)
- Front: Working end / muzzle points +Y, top side up; lowest point on z = 0.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [2.5, 20.0, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it.

## Materials and colors
`black`, `charcoal`, `iron`, `iron_dark`, `iron_edge`, `steel`, `steel_dark`

## Details included
- Boxy steel upper receiver over a dark polymer lower
- Skeletal side-folding stock folded along the left side, rubber butt plate
- Vented handguard, short barrel and muzzle
- Top rail with front and rear sights
- Straight magazine ahead of the trigger guard
- Left-side charging handle

## Details excluded
- No markings, logos or selector lettering
- No internal mechanism
- No optic, light or suppressor

## Attachment points
- `grip`: voxel [2, 4, 5], [np.float64(0.0), np.float64(-0.1938), np.float64(0.0688)] m from the pivot. Main hand on the pistol grip.
- `support`: voxel [2, 26, 9], [np.float64(0.0), np.float64(0.0812), np.float64(0.1188)] m from the pivot. Support hand under the handguard.

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.0625 x 0.5 m

## Outputs
- `models/combat/Claude_compact_smg/Claude_compact_smg.vox` (editable master)
- `models/combat/Claude_compact_smg/model.json`
- `models/combat/Claude_compact_smg/Claude_compact_smg.glb` (derived)
- `previews/combat/Claude_compact_smg/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/c1_combat.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
