# Fallen Log
- Asset ID: Claude_fallen_log
- Base ID: fallen_log
- Creator: Claude
- Category: vegetation
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_D
- Scale family: full
- Intended uses: Forest dressing / cover (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A trunk section that came down across the back of a park years ago and was never cleared. The root end has rotted hollow, moss has crept along the shaded top, and the far end shows the old splintered break.

Condition: **dead**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 2.6 m
- Depth (Y): 0.6 m
- Height (Z): 0.55 m
- Grid: 52 x 12 x 11 cells at 0.05 m (detail tier), 1,860 occupied voxels
- Front direction: +Y (library voxel)
- Front: No functional front; character details face the default camera (-X/+Y).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [26.0, 6.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`bark`, `bark_dark`, `bark_deep`, `bark_mid`, `card_dark`, `moss`, `moss_dark`, `snag`, `snag_dark`, `snag_light`, `wood_stain`

## Details included
- 10-cell round section, bottom row sunk into the ground
- Lengthwise bark furrows (coherent lines, not speckle)
- Hollow rotted end with punky wood crumbled onto the ground (camera side)
- Splintered pale break at the far end
- Moss strip along the top, a patch of bark lost on the front
- Three branch stubs

## Details excluded
- No fungus brackets (kept for the dead tree)
- No leaf litter

## Construction and placement notes
- Collision suggestion: Capsule along X, r=0.24 m, length 2.5 m.
- Placement footprint: 2.6 x 0.6 m

## Outputs
- `models/vegetation/Claude_fallen_log/Claude_fallen_log.vox` (editable master)
- `models/vegetation/Claude_fallen_log/model.json`
- `models/vegetation/Claude_fallen_log/Claude_fallen_log.glb` (derived)
- `previews/vegetation/Claude_fallen_log/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/d1_vegetation.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
