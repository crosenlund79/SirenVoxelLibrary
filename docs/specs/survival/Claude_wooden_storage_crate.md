# Wooden Storage Crate
- Asset ID: Claude_wooden_storage_crate
- Base ID: wooden_storage_crate
- Creator: Claude
- Category: survival
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Build piece 'Storage crate' (3 planks + 4 nails) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
Knocked together in the garage from backyard fence boards, a pallet and one sage-painted kitchen cabinet panel. The lid swings on two strap hinges taken off the garden gate, and the rope handles are cut from an old washing line.

Condition: **improvised**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.9 m
- Depth (Y): 0.65 m
- Height (Z): 0.6 m
- Grid: 18 x 13 x 12 cells at 0.05 m (detail tier), 943 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the working / interaction side.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [9.0, 6.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`iron`, `khaki`, `khaki_dark`, `pine_aged`, `pine_dark`, `pine_light`, `pine_mid`, `rust_deep`, `sage_dark`, `sage_deep`, `wgrey`, `wgrey_dark`, `wgrey_deep`, `wgrey_hi`, `wgrey_mid`

## Details included
- Horizontal boards of four different woods per side, one left long at the corner
- Rows of nail heads where boards meet the inner corner posts
- Three-board lid with a front lip, two gate strap hinges and a hasp
- Washing-line rope loops through holes in both ends

## Details excluded
- No stencilled text or shipping marks
- No gaps between boards (would be 5 cm slots at this tier)

## Construction and placement notes
- Collision suggestion: Box 0.85 x 0.62 x 0.6 m; rope handles and the lid lip are overhangs.
- Placement footprint: 0.8 x 0.6 m

## Outputs
- `models/survival/Claude_wooden_storage_crate/Claude_wooden_storage_crate.vox` (editable master)
- `models/survival/Claude_wooden_storage_crate/model.json`
- `models/survival/Claude_wooden_storage_crate/Claude_wooden_storage_crate.glb` (derived)
- `previews/survival/Claude_wooden_storage_crate/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b1_storage_tools.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
