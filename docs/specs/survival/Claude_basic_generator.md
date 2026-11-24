# Basic Generator
- Asset ID: Claude_basic_generator
- Base ID: basic_generator
- Creator: Claude
- Category: survival
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Power (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A small open-frame petrol generator bought for camping trips. It now runs a few hours each evening for the fridge and lights; the tank paint is stained under the filler, the muffler has rusted, and oil has blackened the engine base.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.75 m
- Depth (Y): 0.5 m
- Height (Z): 0.625 m
- Grid: 30 x 20 x 25 cells at 0.025 m (fine tier), 2,997 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the working / interaction side.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [15.0, 10.0, 0.0])
- Resolution rationale: 2.5 cm cells: a handheld or small gear item whose handles, straps and blades would be 2-4x too thick at 5 cm.

## Materials and colors
`black`, `charcoal`, `glass_dark`, `iron`, `iron_edge`, `mustard`, `mustard_dark`, `mustard_deep`, `mustard_hi`, `porcelain_shadow`, `rust_dark`, `rust_deep`, `soot`, `steel`, `steel_dark`, `steel_light`

## Details included
- Black tube frame with carry loops at both ends
- Mustard fuel tank on top with filler cap and gauge
- Finned engine with the recoil pull-start on the camera side
- Alternator drum and an outlet panel with two sockets and a switch
- Rusted muffler, oily grime at the engine base

## Details excluded
- No brand or warning stickers
- No fuel hose or extension leads

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.75 x 0.5 m

## Outputs
- `models/survival/Claude_basic_generator/Claude_basic_generator.vox` (editable master)
- `models/survival/Claude_basic_generator/model.json`
- `models/survival/Claude_basic_generator/Claude_basic_generator.glb` (derived)
- `previews/survival/Claude_basic_generator/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b2_survival_gear.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
