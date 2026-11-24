# Wooden Fence Section
- Asset ID: Claude_wooden_fence
- Base ID: wooden_fence
- Creator: Claude
- Category: decorations
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_D
- Scale family: full
- Intended uses: Yard boundary (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A back-garden fence panel that has not been stained since it went up. One board was kicked out by a dog or a fox, and its neighbour lost its top nail and leans into the gap; the bottoms have gone green where rain splashes up.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.9 m
- Depth (Y): 0.15 m
- Height (Z): 1.5 m
- Grid: 38 x 3 x 30 cells at 0.05 m (detail tier), 1,261 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y faces the street or the person using it.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [19.0, 1.5, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`wgrey`, `wgrey_dark`, `wgrey_deep`, `wgrey_green`, `wgrey_hi`, `wgrey_mid`, `wgrey_warm`, `wgrey_wet`

## Details included
- Two 4x4 posts and two rails at the back (-Y), twelve dog-eared boards on the front
- One board missing, the next leaning into the gap from its bottom nail
- Per-board weathering, silvered tops, green splash-back at the foot

## Details excluded
- No nail heads (confetti)
- No gate

## Construction and placement notes
- Collision suggestion: Box 1.9 x 0.15 x 1.5 m (thin wall); the gap is cosmetic.
- Placement footprint: 1.9 x 0.15 m

## Outputs
- `models/decorations/Claude_wooden_fence/Claude_wooden_fence.vox` (editable master)
- `models/decorations/Claude_wooden_fence/model.json`
- `models/decorations/Claude_wooden_fence/Claude_wooden_fence.glb` (derived)
- `previews/decorations/Claude_wooden_fence/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/d2_street.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
