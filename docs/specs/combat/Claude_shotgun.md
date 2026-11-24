# Pump Shotgun
- Asset ID: Claude_shotgun
- Base ID: shotgun
- Creator: Claude
- Category: combat
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_C
- Scale family: full
- Intended uses: Planned second weapon (Experiment 003) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A farm-store pump shotgun that lived behind a garage door for bird season. Since the catastrophe it has been carried daily: the fore-end grooves are polished by the pumping hand, the bluing has rubbed off the receiver edges and the muzzle.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.05 m
- Depth (Y): 1.0 m
- Height (Z): 0.175 m
- Grid: 4 x 80 x 14 cells at 0.0125 m (micro tier), 1,294 occupied voxels
- Front direction: +Y (library voxel)
- Front: Working end / muzzle points +Y, top side up; lowest point on z = 0.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [2.0, 40.0, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it. Overridden from the manifest's 2.5 cm to 1.25 cm so the whole firearms family shares one voxel rhythm with the pistol, revolver and SMG: at 2.5 cm the barrel, magazine tube, trigger guard and scope would each be a single cell and the weapon would lose its value structure.

## Materials and colors
`black`, `brass`, `iron`, `iron_dark`, `iron_edge`, `pine_aged`, `pine_dark`, `pine_mid`, `steel`, `steel_dark`, `steel_light`

## Details included
- Grooved wooden pump fore-end around the magazine tube
- Dark receiver with worn bright edges and ejection port
- Long barrel with bead sight and barrel-to-magazine clamp
- Wooden stock with semi-pistol grip and black rubber recoil pad
- Trigger guard with trigger

## Details excluded
- No markings or engraving
- No sling, no shells, no internal mechanism

## Attachment points
- `grip`: voxel [1, 20, 8], [np.float64(-0.0062), np.float64(-0.2438), np.float64(0.1062)] m from the pivot. Main hand at the stock's wrist behind the trigger.
- `support`: voxel [1, 52, 8], [np.float64(-0.0062), np.float64(0.1562), np.float64(0.1062)] m from the pivot. Support hand on the pump fore-end.

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.05 x 1.0 m

## Outputs
- `models/combat/Claude_shotgun/Claude_shotgun.vox` (editable master)
- `models/combat/Claude_shotgun/model.json`
- `models/combat/Claude_shotgun/Claude_shotgun.glb` (derived)
- `previews/combat/Claude_shotgun/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/c1_combat.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
