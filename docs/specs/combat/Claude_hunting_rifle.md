# Hunting Rifle
- Asset ID: Claude_hunting_rifle
- Base ID: hunting_rifle
- Creator: Claude
- Category: combat
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_C
- Scale family: full
- Intended uses: Planned weapon (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A deer rifle kept in a locked cabinet by a man who hunted one weekend a year. It came out of the cabinet the night the sirens stopped; the leather sling is stiff and cracked, the walnut is still oiled, the scope caps are lost.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.075 m
- Depth (Y): 1.075 m
- Height (Z): 0.2375 m
- Grid: 6 x 86 x 19 cells at 0.0125 m (micro tier), 1,545 occupied voxels
- Front direction: +Y (library voxel)
- Front: Working end / muzzle points +Y, top side up; lowest point on z = 0.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [3.0, 43.0, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it. Overridden from the manifest's 2.5 cm to 1.25 cm so the whole firearms family shares one voxel rhythm with the pistol, revolver and SMG: at 2.5 cm the barrel, magazine tube, trigger guard and scope would each be a single cell and the weapon would lose its value structure.

## Materials and colors
`black`, `charcoal`, `glass_dark`, `glass_deep`, `iron`, `iron_edge`, `leather`, `leather_dark`, `pine_aged`, `pine_dark`, `steel`, `steel_dark`, `wood_deep`, `wood_stain`

## Details included
- Walnut stock with pistol grip, darker checkered panels and contrasting tip
- Telescopic sight on two rings with turrets and opaque lens faces
- Bolt handle with round knob on the right
- Trigger guard and magazine floor plate
- Leather sling hanging between front and rear swivels
- Black recoil pad

## Details excluded
- No markings, engraving or brand on the scope
- No internal mechanism
- No bipod or cartridges

## Attachment points
- `grip`: voxel [1, 20, 7], [np.float64(-0.0188), np.float64(-0.2812), np.float64(0.0938)] m from the pivot. Main hand on the pistol grip.
- `support`: voxel [1, 50, 8], [np.float64(-0.0188), np.float64(0.0938), np.float64(0.1062)] m from the pivot. Support hand under the fore-end.
- `sling_rear`: voxel [1, 9, 4], [np.float64(-0.0188), np.float64(-0.4188), np.float64(0.0562)] m from the pivot. Rear sling swivel.
- `sling_front`: voxel [1, 56, 7], [np.float64(-0.0188), np.float64(0.1688), np.float64(0.0938)] m from the pivot. Front sling swivel.

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.075 x 1.075 m

## Outputs
- `models/combat/Claude_hunting_rifle/Claude_hunting_rifle.vox` (editable master)
- `models/combat/Claude_hunting_rifle/model.json`
- `models/combat/Claude_hunting_rifle/Claude_hunting_rifle.glb` (derived)
- `previews/combat/Claude_hunting_rifle/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/c1_combat.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
