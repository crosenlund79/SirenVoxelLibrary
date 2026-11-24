# Living-Room Rug
- Asset ID: Claude_rug
- Base ID: rug
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Floor rug; game prop 'rug' (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A flat-woven living-room rug laid across the route from the hall to the kitchen. A grey track is trodden into it along that line, and the near corner got kicked over in the last rush through the room and was never laid flat again.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 2.55 m
- Depth (Y): 1.75 m
- Height (Z): 0.05 m
- Grid: 102 x 70 x 2 cells at 0.025 m (fine tier), 6,941 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [51.0, 35.0, 0.0])
- Resolution rationale: 2.5 cm cells: a handheld or small gear item whose handles, straps and blades would be 2-4x too thick at 5 cm. A flat-weave rug is about 1 cm thick: 2.5 cm is the thinnest honest layer, and the finer cells carry the border motif and fringe.

## Materials and colors
`blue_dark`, `blue_deep`, `bluegrey_dark`, `bluegrey_deep`, `cream_deep`, `cream_mid`, `cream_shadow`, `red_dark`, `red_deep`, `terra_dark`, `wgrey_warm`, `wool`, `wool_dark`

## Details included
- Oatmeal field, slate-blue border with a running diamond motif and a brick inner stripe
- Fringes on the short ends
- Trodden walking track crossing it front to back
- Near corner folded over, showing the duller reverse

## Details excluded
- No pile texture noise; flat weave
- No furniture dents

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 2.4 x 1.75 m

## Outputs
- `models/furniture/Claude_rug/Claude_rug.vox` (editable master)
- `models/furniture/Claude_rug/model.json`
- `models/furniture/Claude_rug/Claude_rug.glb` (derived)
- `previews/furniture/Claude_rug/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a1_living_room.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
