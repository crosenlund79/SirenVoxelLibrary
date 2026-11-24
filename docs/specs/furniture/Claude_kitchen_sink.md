# Kitchen Sink Unit
- Asset ID: Claude_kitchen_sink
- Base ID: kitchen_sink
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Sink unit; game prop 'sink_counter' (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The family washed up here every evening. The last water dried in the basin and left a brown tide ring round the drain; two plates are still standing in the rack where somebody left them to drain.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.05 m
- Depth (Y): 0.65 m
- Height (Z): 1.2 m
- Grid: 21 x 13 x 24 cells at 0.05 m (detail tier), 1,794 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [10.5, 6.5, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`black`, `card_dark`, `charcoal`, `chrome`, `pine_light`, `pine_mid`, `porcelain_hi`, `porcelain_mid`, `rust_deep`, `sage`, `sage_dark`, `sage_deep`, `sage_hi`, `steel`, `steel_hi`, `steel_light`, `terra`, `terra_dark`

## Details included
- Same sage shaker base as the counter, with a false drawer front
- Inset stainless basin and ribbed drainer in the pine worktop
- Swan-neck mixer tap with two cross-head valves
- Wire dish rack with two upright plates and a mug
- Dry brown tide ring and drip marks in the basin

## Details excluded
- No running water or soap foam
- No brand on the tap

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.05 x 0.65 m

## Outputs
- `models/furniture/Claude_kitchen_sink/Claude_kitchen_sink.vox` (editable master)
- `models/furniture/Claude_kitchen_sink/model.json`
- `models/furniture/Claude_kitchen_sink/Claude_kitchen_sink.glb` (derived)
- `previews/furniture/Claude_kitchen_sink/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a3_kitchen.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
