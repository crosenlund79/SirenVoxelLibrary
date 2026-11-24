# Traffic Cone
- Asset ID: Claude_traffic_cone
- Base ID: traffic_cone
- Creator: Claude
- Category: decorations
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_D
- Scale family: full
- Intended uses: Street prop (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A road cone left from roadworks that stopped mid-job. It has been knocked over and stood back up more than once: the base is chipped and a tyre has scuffed one side black.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.325 m
- Depth (Y): 0.325 m
- Height (Z): 0.525 m
- Grid: 13 x 13 x 21 cells at 0.025 m (fine tier), 738 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y faces the street or the person using it.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [6.5, 6.5, 0.0])
- Resolution rationale: 2.5 cm cells: a handheld or small gear item whose handles, straps and blades would be 2-4x too thick at 5 cm.

## Materials and colors
`asphalt_hi`, `charcoal`, `iron_edge`, `porcelain_mid`, `safety_orange`, `safety_orange_dark`

## Details included
- Square rubber base with chamfered corners
- Stepped round cone with an open top
- Two pale reflective bands
- Tyre scuff on the camera side, grime on the lower cone, a chipped base corner

## Details excluded
- No printed markings

## Construction and placement notes
- Collision suggestion: Cylinder r=0.15 m, h=0.53 m.
- Placement footprint: 0.325 x 0.325 m

## Outputs
- `models/decorations/Claude_traffic_cone/Claude_traffic_cone.vox` (editable master)
- `models/decorations/Claude_traffic_cone/model.json`
- `models/decorations/Claude_traffic_cone/Claude_traffic_cone.glb` (derived)
- `previews/decorations/Claude_traffic_cone/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/d2_street.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
