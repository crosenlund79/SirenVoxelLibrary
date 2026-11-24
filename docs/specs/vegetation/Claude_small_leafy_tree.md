# Small Leafy Tree
- Asset ID: Claude_small_leafy_tree
- Base ID: small_leafy_tree
- Creator: Claude
- Category: vegetation
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_D
- Scale family: full
- Intended uses: Garden tree (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
An ornamental garden tree planted when the house was new. Nobody has watered or pruned it since the summer things stopped; the lower clump on the path side is already yellowing and a water sprout has shot up from the fork.

Condition: **living**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 2.7 m
- Depth (Y): 2.6 m
- Height (Z): 3.7 m
- Grid: 27 x 26 x 37 cells at 0.1 m (standard tier), 2,197 occupied voxels
- Front direction: +Y (library voxel)
- Front: No functional front; character details face the default camera (-X/+Y).
- Pivot: Trunk base centre at ground level. (pivot_voxel [13.0, 13.0, 0.0])
- Resolution rationale: 10 cm cells (the game's structural grid): large silhouettes such as walls, vehicles and trees read clearly without inflating the voxel count.

## Materials and colors
`bark`, `bark_dark`, `bark_deep`, `bark_hi`, `bark_mid`, `grass`, `grass_hi`, `leaf`, `leaf_dark`, `leaf_deep`, `leaf_hi`, `leaf_mid`, `snag_dark`

## Details included
- Short trunk forking at 1.3 m into five limbs
- Six lumpy foliage clumps with gaps between them so limbs show through
- Lit crowns and darker undersides as material zones, not noise
- One clump yellowing on the camera side
- Root flares and a pruning scar on the trunk

## Details excluded
- No individual leaves
- No fruit or blossom

## Construction and placement notes
- Collision suggestion: Capsule r=0.12 m, h=1.3 m at the pivot (trunk); crown non-colliding.

## Outputs
- `models/vegetation/Claude_small_leafy_tree/Claude_small_leafy_tree.vox` (editable master)
- `models/vegetation/Claude_small_leafy_tree/model.json`
- `models/vegetation/Claude_small_leafy_tree/Claude_small_leafy_tree.glb` (derived)
- `previews/vegetation/Claude_small_leafy_tree/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/d1_vegetation.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
