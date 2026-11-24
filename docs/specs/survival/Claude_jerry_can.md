# Jerry Can
- Asset ID: Claude_jerry_can
- Base ID: jerry_can
- Creator: Claude
- Category: survival
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Fuel/water container (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
An army-surplus jerry can bought for camping, now the household's petrol reserve. The olive paint is chipped at every corner it has been dropped on, the centre handle is rubbed to bare steel, and rust has started on the base seam.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.35 m
- Depth (Y): 0.175 m
- Height (Z): 0.475 m
- Grid: 14 x 7 x 19 cells at 0.025 m (fine tier), 889 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the working / interaction side.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [7.0, 3.5, 0.0])
- Resolution rationale: 2.5 cm cells: a handheld or small gear item whose handles, straps and blades would be 2-4x too thick at 5 cm.

## Materials and colors
`green_deep`, `olive_dark`, `rust_dark`, `rust_deep`, `steel`, `steel_dark`, `steel_light`

## Details included
- Pressed steel body with the recessed X on both faces and a side seam
- Three handles on top, the centre one worn bare
- Cam-lever spout cap at the corner
- Chips at corners and edges, rust along the bottom seam

## Details excluded
- No stencilled text or markings
- No spout attachment

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.35 x 0.175 m

## Outputs
- `models/survival/Claude_jerry_can/Claude_jerry_can.vox` (editable master)
- `models/survival/Claude_jerry_can/model.json`
- `models/survival/Claude_jerry_can/Claude_jerry_can.glb` (derived)
- `previews/survival/Claude_jerry_can/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b2_survival_gear.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
