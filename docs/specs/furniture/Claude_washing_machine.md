# Washing Machine
- Asset ID: Claude_washing_machine
- Base ID: washing_machine
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Utility appliance; game prop 'washer' (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A white front-loader in the utility room, only a few years old and still clean. The last load was pulled out in a hurry; one mustard sock stayed caught in the door seal and hangs down the front (its partner is in the laundry basket).

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.65 m
- Depth (Y): 0.65 m
- Height (Z): 0.85 m
- Grid: 13 x 13 x 17 cells at 0.05 m (detail tier), 1,045 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [6.5, 6.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`charcoal`, `glass_dark`, `glass_deep`, `mustard`, `mustard_dark`, `porcelain`, `porcelain_hi`, `porcelain_mid`, `porcelain_shadow`, `screen`, `steel_light`

## Details included
- Round porthole door: grey ring, dark recessed glass, handle on the right
- Detergent drawer, small display and program dial on the control strip
- Separate top panel seam, plinth with a filter hatch
- Mustard sock caught in the seal at the bottom of the door

## Details excluded
- No brand or readable controls
- No water or suds behind the glass

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.65 x 0.6 m

## Outputs
- `models/furniture/Claude_washing_machine/Claude_washing_machine.vox` (editable master)
- `models/furniture/Claude_washing_machine/model.json`
- `models/furniture/Claude_washing_machine/Claude_washing_machine.glb` (derived)
- `previews/furniture/Claude_washing_machine/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a4_bath_utility.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
