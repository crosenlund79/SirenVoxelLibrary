# Dead Shrub
- Asset ID: Claude_dead_shrub
- Base ID: dead_shrub
- Creator: Claude
- Category: vegetation
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_D
- Scale family: full
- Intended uses: Yard dressing (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A flowering shrub by a driveway that died of drought after the sprinklers stopped. Only a few curled brown leaves still cling to the stems, and dry grass has grown up around the woody base.

Condition: **dead**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.1 m
- Depth (Y): 0.95 m
- Height (Z): 0.85 m
- Grid: 22 x 19 x 17 cells at 0.05 m (detail tier), 329 occupied voxels
- Front direction: +Y (library voxel)
- Front: No functional front; character details face the default camera (-X/+Y).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [10.5, 8.5, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig. Twigs at 0.10 m would be as thick as a wrist; 0.05 m keeps the stems spindly.

## Materials and colors
`bark_dark`, `bark_mid`, `dead_leaf`, `dead_leaf_dark`, `grass`, `grass_dry`, `snag_dark`, `twig`

## Details included
- Seven stems from one woody crown, each with side shoots, splaying into a loose vase
- Weathered grey tips, browner wood low down
- Five small clusters of curled brown leaves
- Tuft of dry grass around the base

## Details excluded
- No green growth
- No random branching generator

## Construction and placement notes
- Collision suggestion: None (walk-through dressing); optional cylinder r=0.4 m, h=0.8 m.

## Outputs
- `models/vegetation/Claude_dead_shrub/Claude_dead_shrub.vox` (editable master)
- `models/vegetation/Claude_dead_shrub/model.json`
- `models/vegetation/Claude_dead_shrub/Claude_dead_shrub.glb` (derived)
- `previews/vegetation/Claude_dead_shrub/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/d1_vegetation.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
