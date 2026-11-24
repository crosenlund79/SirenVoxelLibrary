# Metal Door
- Asset ID: Claude_metal_door
- Base ID: metal_door
- Creator: Claude
- Category: construction
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Upgraded door (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A steel security door from a pharmacy's back entrance, rehung in a welded frame by survivors. The heavy bar latch is scratched bright from use and the bottom has rusted where rain sat against it.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.0 m
- Depth (Y): 0.2 m
- Height (Z): 2.1 m
- Grid: 20 x 4 x 42 cells at 0.05 m (detail tier), 2,048 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the outside face; the module fills its full span.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [10.0, 2.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`black`, `bluegrey`, `bluegrey_dark`, `bluegrey_deep`, `brass_dark`, `charcoal`, `iron`, `iron_edge`, `rust_dark`, `rust_deep`, `steel`, `steel_dark`, `steel_hi`, `steel_light`

## Details included
- Pressed-steel frame filling the 1.0 x 2.1 m opening
- Leaf faced with two riveted cover plates, rivet rows along their edges
- Peephole with a steel bezel at eye height
- Heavy sliding bar latch in two guide straps, shooting into a keeper on the frame; its handle and track rubbed bright
- Weld-on barrel hinges, rusted kick zone and frame feet

## Details excluded
- Closed state only
- No signage or text

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.0 x 0.2 m

## Outputs
- `models/construction/Claude_metal_door/Claude_metal_door.vox` (editable master)
- `models/construction/Claude_metal_door/model.json`
- `models/construction/Claude_metal_door/Claude_metal_door.glb` (derived)
- `previews/construction/Claude_metal_door/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b3_construction.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
