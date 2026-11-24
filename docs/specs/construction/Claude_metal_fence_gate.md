# Metal Gate
- Asset ID: Claude_metal_fence_gate
- Base ID: metal_fence_gate
- Creator: Claude
- Category: construction
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Defensive gate / metal fence (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A welded tube gate from a builder's yard, hung between two square posts across a driveway. The latch broke long ago, so it is held with a chain and a brass padlock that has rubbed the paint off the stile.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.15 m
- Depth (Y): 0.15 m
- Height (Z): 2.0 m
- Grid: 23 x 3 x 40 cells at 0.05 m (detail tier), 711 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the outside face; the module fills its full span.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [11.5, 1.5, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`brass`, `brass_dark`, `charcoal`, `green`, `green_dark`, `green_deep`, `green_light`, `rust_dark`, `rust_deep`, `steel`, `steel_dark`, `steel_light`

## Details included
- Two 0.1 m square-tube posts with caps
- Tube frame with top, middle and bottom rails, vertical bars every 0.1 m
- 45-degree brace in the lower panel from the bottom hinge corner up to the middle rail
- Barrel hinges, chain wrapped round stile and post, hanging brass padlock
- Dark green paint worn to rust at the welds and bottom rail, bright where the chain rubs

## Details excluded
- No barbed wire
- Closed state only

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.15 x 0.15 m

## Outputs
- `models/construction/Claude_metal_fence_gate/Claude_metal_fence_gate.vox` (editable master)
- `models/construction/Claude_metal_fence_gate/model.json`
- `models/construction/Claude_metal_fence_gate/Claude_metal_fence_gate.glb` (derived)
- `previews/construction/Claude_metal_fence_gate/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b3_construction.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
