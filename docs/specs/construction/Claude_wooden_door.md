# Wooden Door
- Asset ID: Claude_wooden_door
- Base ID: wooden_door
- Creator: Claude
- Category: construction
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Build piece 'Door' (frame 1.0 x 2.1 m) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A four-panel front door taken off a house down the street and rehung in a new frame to open outward, so it cannot be kicked in. Teal paint from three owners ago is rubbed back to bare wood around the handle.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.0 m
- Depth (Y): 0.2 m
- Height (Z): 2.1 m
- Grid: 20 x 4 x 42 cells at 0.05 m (detail tier), 1,894 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the outside face; the module fills its full span.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [10.0, 2.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`black`, `brass`, `brass_dark`, `cream`, `cream_mid`, `cream_shadow`, `pine_dark`, `pine_mid`, `teal`, `teal_dark`, `teal_hi`, `wgrey_dark`, `wood_stain`

## Details included
- Painted frame filling the 1.0 x 2.1 m opening, oak threshold
- Four raised-and-fielded panels, stiles, rails and a centre muntin
- Lever handle, deadbolt and a brass letter slot in the lock rail
- Three hinge knuckles on the outside (outward-opening)
- Paint worn to bare pine along the lock stile at hand height; scuffed bottom rail

## Details excluded
- Closed state only
- No glazing
- No house number or text

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.0 x 0.2 m

## Outputs
- `models/construction/Claude_wooden_door/Claude_wooden_door.vox` (editable master)
- `models/construction/Claude_wooden_door/model.json`
- `models/construction/Claude_wooden_door/Claude_wooden_door.glb` (derived)
- `previews/construction/Claude_wooden_door/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b3_construction.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
