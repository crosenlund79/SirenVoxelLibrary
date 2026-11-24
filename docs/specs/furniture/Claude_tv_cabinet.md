# TV Cabinet
- Asset ID: Claude_tv_cabinet
- Base ID: tv_cabinet
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Media cabinet; game prop 'tv_stand' (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A walnut media cabinet that has been moved through three houses. The near door came off its top hinge and now hangs askew on the bottom one; the set-top box is still in the open bay, its cable pulled out when someone took the console.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.7 m
- Depth (Y): 0.6 m
- Height (Z): 0.6 m
- Grid: 34 x 12 x 12 cells at 0.05 m (detail tier), 1,457 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [17.0, 4.5, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`black`, `brass`, `brass_dark`, `charcoal`, `pine_aged`, `pine_dark`, `steel_dark`, `steel_light`, `wood_deep`, `wood_stain`

## Details included
- Recessed doors inside a walnut frame with brass bar pulls, on short legs
- Open middle bay with a set-top box
- A loose cable trailing to the floor
- Near door hanging askew off its top hinge, dark gap above it
- Front edge of the top rubbed pale above the bay

## Details excluded
- No television on top (separate model)
- No logo on the box

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.7 x 0.45 m

## Outputs
- `models/furniture/Claude_tv_cabinet/Claude_tv_cabinet.vox` (editable master)
- `models/furniture/Claude_tv_cabinet/model.json`
- `models/furniture/Claude_tv_cabinet/Claude_tv_cabinet.glb` (derived)
- `previews/furniture/Claude_tv_cabinet/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a1_living_room.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
