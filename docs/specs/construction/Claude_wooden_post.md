# Wooden Post
- Asset ID: Claude_wooden_post
- Base ID: wooden_post
- Creator: Claude
- Category: construction
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Structural post (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A fresh 8x8 post from a pallet of yard lumber, set on a galvanised stirrup base bolted to the slab, its top already notched to take a beam that was never delivered.

Condition: **new**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.3 m
- Depth (Y): 0.3 m
- Height (Z): 2.5 m
- Grid: 6 x 6 x 50 cells at 0.05 m (detail tier), 640 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the outside face; the module fills its full span.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [3.0, 3.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig. A 0.2 m post is two cells wide at 0.1 m, so its steel base would be a 10 cm slab and the beam notch would remove half the post; at 0.05 m the base plate, stirrup flanges and a half-depth notch keep real proportions.

## Materials and colors
`galv`, `galv_hi`, `pine_aged`, `pine_dark`, `pine_hi`, `pine_light`, `pine_mid`, `steel_dark`

## Details included
- 0.2 m square post with lighter arrises and a few long grain streaks
- Galvanised stirrup base: plate with anchor nuts and two side flanges, through-bolted
- Half-lap notch at the top on the +Y side with a crisp sawn shoulder
- One drying check running down the front face

## Details excluded
- No beam in the notch (separate module)

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.3 x 0.3 m

## Outputs
- `models/construction/Claude_wooden_post/Claude_wooden_post.vox` (editable master)
- `models/construction/Claude_wooden_post/model.json`
- `models/construction/Claude_wooden_post/Claude_wooden_post.glb` (derived)
- `previews/construction/Claude_wooden_post/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b3_construction.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
