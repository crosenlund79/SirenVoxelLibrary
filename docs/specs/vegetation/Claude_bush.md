# Bush
- Asset ID: Claude_bush
- Base ID: bush
- Creator: Claude
- Category: vegetation
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_D
- Scale family: full
- Intended uses: Yard shrub (game bush) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A privet-type shrub under a front window, clipped square for years and now growing out shaggy. The top has gone lumpy and uneven, and one low corner by the path has browned.

Condition: **living**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.2 m
- Depth (Y): 1.05 m
- Height (Z): 0.85 m
- Grid: 24 x 21 x 17 cells at 0.05 m (detail tier), 1,694 occupied voxels
- Front direction: +Y (library voxel)
- Front: No functional front; character details face the default camera (-X/+Y).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [12.0, 11.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig. At 0.10 m the 1 m shrub is a 10-cell lump with no lobes; 0.05 m keeps the uneven top and the gaps.

## Materials and colors
`bark_deep`, `dead_leaf_dark`, `leaf`, `leaf_dark`, `leaf_deep`, `leaf_mid`, `twig`

## Details included
- Six overlapping lobes of different heights for an uneven top
- Bumpy crest and cavity structure, dark gaps between lobes
- Bare stems visible under the lifted front lobe
- One small browning lobe at a low corner

## Details excluded
- No flowers or berries
- No soil mound (sits on any ground)

## Construction and placement notes
- Collision suggestion: Ellipsoid 1.1 x 0.95 x 0.8 m on the pivot; soft, non-blocking.

## Outputs
- `models/vegetation/Claude_bush/Claude_bush.vox` (editable master)
- `models/vegetation/Claude_bush/model.json`
- `models/vegetation/Claude_bush/Claude_bush.glb` (derived)
- `previews/vegetation/Claude_bush/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/d1_vegetation.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
