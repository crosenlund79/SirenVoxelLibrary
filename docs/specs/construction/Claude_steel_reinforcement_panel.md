# Steel Reinforcement Panel
- Asset ID: Claude_steel_reinforcement_panel
- Base ID: steel_reinforcement_panel
- Creator: Claude
- Category: construction
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Bolt-on reinforcement for windows/walls (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
Cut from a road-plate by a welder in the group and framed in angle iron so it can be bolted over a window or a weak wall. Grinder marks still show where the cut was dressed.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.0 m
- Depth (Y): 0.1 m
- Height (Z): 2.3 m
- Grid: 20 x 2 x 46 cells at 0.05 m (detail tier), 1,188 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the outside face; the module fills its full span.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [10.0, 1.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`iron`, `iron_dark`, `iron_edge`, `rust_dark`, `rust_deep`, `steel`, `steel_light`

## Details included
- Steel plate set in a perimeter angle-iron frame (L profile visible at the ends)
- A horizontal mid rail and one diagonal flat-bar brace welded corner to corner
- Bolt holes drilled right through the frame's flat leg
- Weld beads at the brace ends, a ground-bright cut edge, rust along the bottom

## Details excluded
- No mounting bolts (the holes are empty)

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.0 x 0.1 m

## Outputs
- `models/construction/Claude_steel_reinforcement_panel/Claude_steel_reinforcement_panel.vox` (editable master)
- `models/construction/Claude_steel_reinforcement_panel/model.json`
- `models/construction/Claude_steel_reinforcement_panel/Claude_steel_reinforcement_panel.glb` (derived)
- `previews/construction/Claude_steel_reinforcement_panel/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b3_construction.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
