# Revolver
- Asset ID: Claude_revolver
- Base ID: revolver
- Creator: Claude
- Category: combat
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_C
- Scale family: full
- Intended uses: Planned weapon (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A six-shot revolver that spent decades in a bedside drawer before it was carried every day. The bluing has worn silver on the cylinder, muzzle and frame edges, and the walnut grip is darkened and polished where the palm sits.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.05 m
- Depth (Y): 0.2125 m
- Height (Z): 0.1625 m
- Grid: 4 x 17 x 13 cells at 0.0125 m (micro tier), 260 occupied voxels
- Front direction: +Y (library voxel)
- Front: Working end / muzzle points +Y, top side up; lowest point on z = 0.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [2.0, 8.5, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it.

## Materials and colors
`black`, `iron_blue`, `iron_edge`, `pine_aged`, `pine_dark`, `steel`, `steel_dark`, `steel_light`, `wood_stain`

## Details included
- Fluted six-shot cylinder bulging past the narrow frame
- Barrel with ejector-rod lug and ramp front sight
- Hammer spur
- Walnut plow-handle grip, polished at the palm swell
- Worn bluing: silver edges on the cylinder, muzzle and top strap

## Details excluded
- No markings, logos or grip medallion
- No internal mechanism
- No visible cartridges

## Attachment points
- `grip`: voxel [1, 2, 3], [np.float64(-0.0062), np.float64(-0.075), np.float64(0.0438)] m from the pivot. Main hand around the wooden grip.

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.05 x 0.2125 m

## Outputs
- `models/combat/Claude_revolver/Claude_revolver.vox` (editable master)
- `models/combat/Claude_revolver/model.json`
- `models/combat/Claude_revolver/Claude_revolver.glb` (derived)
- `previews/combat/Claude_revolver/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/c1_combat.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
