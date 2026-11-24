# Leafless Deciduous Tree
- Asset ID: Claude_leafless_deciduous
- Base ID: leafless_deciduous
- Creator: Claude
- Category: vegetation
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_D
- Scale family: full
- Intended uses: Yard/street tree (game dead_tree) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
An old yard oak that died the summer before everything stopped. Nobody came to fell it: a storm has already snapped one low limb, bracket fungus is eating the trunk and the bark is lifting off the big limbs in pale patches.

Condition: **dead**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 3.4 m
- Depth (Y): 3.4 m
- Height (Z): 4.8 m
- Grid: 34 x 34 x 48 cells at 0.1 m (standard tier), 888 occupied voxels
- Front direction: +Y (library voxel)
- Front: No functional front; character details face the default camera (-X/+Y).
- Pivot: Trunk base centre at ground level. (pivot_voxel [16.5, 17.5, 0.0])
- Resolution rationale: 10 cm cells (the game's structural grid): large silhouettes such as walls, vehicles and trees read clearly without inflating the voxel count.

## Materials and colors
`bark`, `bark_dark`, `bark_deep`, `bark_hi`, `bark_mid`, `break_fresh`, `card_dark`, `card_hi`, `snag`, `snag_dark`, `snag_light`

## Details included
- Short buttressed trunk forking at 1.9 m into three spreading scaffold limbs and a leader
- Secondary limbs arch upward and end in fans of fine twigs, giving a broad, lacy crown outline
- Snapped low limb with pale broken wood
- Two shelves of bracket fungus on the trunk (camera side)
- Bark lifted off the tops of the main limbs

## Details excluded
- No leaves (dead tree)
- No random branching generator

## Construction and placement notes
- Collision suggestion: Capsule r=0.18 m, h=1.9 m at the pivot (trunk); crown non-colliding.

## Outputs
- `models/vegetation/Claude_leafless_deciduous/Claude_leafless_deciduous.vox` (editable master)
- `models/vegetation/Claude_leafless_deciduous/model.json`
- `models/vegetation/Claude_leafless_deciduous/Claude_leafless_deciduous.glb` (derived)
- `previews/vegetation/Claude_leafless_deciduous/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/d1_vegetation.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
