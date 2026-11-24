# Boulder
- Asset ID: Claude_boulder
- Base ID: boulder
- Creator: Claude
- Category: vegetation
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_D
- Scale family: full
- Intended uses: Landscape cover (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A glacial erratic the developers built the park around rather than move. Its north side is furred with moss, frost has opened a fissure down the front, and a grass tuft has seeded in the crack.

Condition: **n/a**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.9 m
- Depth (Y): 1.6 m
- Height (Z): 1.3 m
- Grid: 19 x 16 x 13 cells at 0.1 m (standard tier), 1,079 occupied voxels
- Front direction: +Y (library voxel)
- Front: No functional front; character details face the default camera (-X/+Y).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [9.5, 8.0, 0.0])
- Resolution rationale: 10 cm cells (the game's structural grid): large silhouettes such as walls, vehicles and trees read clearly without inflating the voxel count.

## Materials and colors
`concrete`, `concrete_hi`, `grass`, `grass_dry`, `grass_hi`, `gravel`, `moss`, `moss_dark`, `soil_dark`, `stone`, `stone_dark`

## Details included
- Three overlapping rounded masses, broad at the foot
- Fissure down the front (+Y) where two masses meet, dark inside, a grass tuft at its foot
- Moss over the north (-Y) flank and the back of the crown
- A paler old fracture face on the camera (-X) side

## Details excluded
- No granite speckle (confetti)

## Construction and placement notes
- Collision suggestion: Convex hull of the voxels, or a box 1.85 x 1.55 x 1.25 m.
- Placement footprint: 1.9 x 1.6 m

## Outputs
- `models/vegetation/Claude_boulder/Claude_boulder.vox` (editable master)
- `models/vegetation/Claude_boulder/model.json`
- `models/vegetation/Claude_boulder/Claude_boulder.glb` (derived)
- `previews/vegetation/Claude_boulder/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/d1_vegetation.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
