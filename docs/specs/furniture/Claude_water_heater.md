# Gas Water Heater
- Asset ID: Claude_water_heater
- Base ID: water_heater
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Utility; emergency water source; game prop 'water_heater' (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The tank water heater in the utility corner. After the gas went off it became the house's emergency water: someone has been drawing off the drain valve into buckets, and the valve's slow drip has left a rust streak down the jacket.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.65 m
- Depth (Y): 0.75 m
- Height (Z): 1.6 m
- Grid: 13 x 15 x 32 cells at 0.05 m (detail tier), 1,469 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [7.0, 7.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`brass`, `brass_dark`, `charcoal`, `copper`, `cream_deep`, `cream_shadow`, `galv`, `galv_dark`, `galv_hi`, `label_cream`, `paint_white`, `paint_white_shadow`, `rust`, `rust_dark`, `rust_deep`, `signal_red_dark`, `steel_dark`, `steel_hi`, `steel_light`

## Details included
- 60 cm cylindrical jacket with a top cap and a base ring
- Copper cold-in and hot-out pipes with brass valves, turning back to the wall
- Galvanised flue with a draft hood in the middle of the top
- Relief valve near the top with its copper discharge pipe down the side
- Drain valve at the bottom with a rust streak below it
- Gas control with a red knob, burner access cover, plain data plate

## Details excluded
- No readable data plate
- No brand

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.6 x 0.6 m

## Outputs
- `models/furniture/Claude_water_heater/Claude_water_heater.vox` (editable master)
- `models/furniture/Claude_water_heater/model.json`
- `models/furniture/Claude_water_heater/Claude_water_heater.glb` (derived)
- `previews/furniture/Claude_water_heater/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a4_bath_utility.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
