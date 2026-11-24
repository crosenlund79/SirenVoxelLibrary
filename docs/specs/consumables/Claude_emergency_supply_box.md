# Emergency Supply Box
- Asset ID: Claude_emergency_supply_box
- Base ID: emergency_supply_box
- Creator: Claude
- Category: consumables
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_C
- Scale family: full
- Intended uses: Supply crate (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A heavy-duty plastic tote packed by a careful neighbour as an emergency kit and strapped shut. It was never opened: the straps are tight, the plastic is clean and the stencilled crosses are crisp.

Condition: **new**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.55 m
- Depth (Y): 0.375 m
- Height (Z): 0.4 m
- Grid: 22 x 15 x 16 cells at 0.025 m (fine tier), 1,452 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the label / opening side.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [11.0, 7.5, 0.0])
- Resolution rationale: 2.5 cm cells: a handheld or small gear item whose handles, straps and blades would be 2-4x too thick at 5 cm.

## Materials and colors
`charcoal`, `signal_red`, `slate`, `slate_dark`, `slate_deep`, `slate_hi`, `steel`, `steel_dark`

## Details included
- Grey tote with a lighter lid, end hand-holds and a lid parting line
- Two webbing straps over the lid and down the front, cam buckles
- Red stencilled cross on the lid and on the front

## Details excluded
- No text or brand
- No visible contents

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.55 x 0.375 m

## Outputs
- `models/consumables/Claude_emergency_supply_box/Claude_emergency_supply_box.vox` (editable master)
- `models/consumables/Claude_emergency_supply_box/model.json`
- `models/consumables/Claude_emergency_supply_box/Claude_emergency_supply_box.glb` (derived)
- `previews/consumables/Claude_emergency_supply_box/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/c2_consumables.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
