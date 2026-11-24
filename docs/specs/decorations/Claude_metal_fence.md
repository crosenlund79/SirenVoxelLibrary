# Metal Fence Section
- Asset ID: Claude_metal_fence
- Base ID: metal_fence
- Creator: Claude
- Category: decorations
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_D
- Scale family: full
- Intended uses: Yard/industrial boundary (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A chain-link section along a school or yard boundary. Someone climbed it at the left corner until the mesh tore off the top rail and sagged outward, and a plastic bag has been caught low in the mesh for months.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.9 m
- Depth (Y): 0.1 m
- Height (Z): 1.65 m
- Grid: 38 x 2 x 33 cells at 0.05 m (detail tier), 854 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y faces the street or the person using it.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [19.0, 1.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`galv`, `galv_dark`, `galv_hi`, `porcelain_deep`, `porcelain_shadow`

## Details included
- Galvanised posts with caps and a top rail
- Diamond mesh (a 6-cell lattice standing in for wire finer than a cell)
- Top-left corner torn off the rail, sagging down and outward
- Bottom tension wire
- A faded bag snagged in the mesh

## Details excluded
- No barbed wire
- No gate

## Construction and placement notes
- Collision suggestion: Box 1.9 x 0.1 x 1.6 m; mesh blocks movement, not sight.
- Placement footprint: 1.9 x 0.1 m

## Outputs
- `models/decorations/Claude_metal_fence/Claude_metal_fence.vox` (editable master)
- `models/decorations/Claude_metal_fence/model.json`
- `models/decorations/Claude_metal_fence/Claude_metal_fence.glb` (derived)
- `previews/decorations/Claude_metal_fence/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/d2_street.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
