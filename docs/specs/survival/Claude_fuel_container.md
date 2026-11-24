# Fuel Container
- Asset ID: Claude_fuel_container
- Base ID: fuel_container
- Creator: Claude
- Category: survival
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Fuel for generator (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The plastic petrol can from the lawnmower shelf. The red has faded to salmon where the sun hit it through the garage window; the flexible spout is clipped to its side, and a dribble of fuel has stained the front under the neck.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.35 m
- Depth (Y): 0.2 m
- Height (Z): 0.475 m
- Grid: 14 x 8 x 19 cells at 0.025 m (fine tier), 784 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the working / interaction side.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [7.5, 4.0, 0.0])
- Resolution rationale: 2.5 cm cells: a handheld or small gear item whose handles, straps and blades would be 2-4x too thick at 5 cm.

## Materials and colors
`black`, `charcoal`, `iron`, `red`, `red_dark`, `red_deep`, `red_hi`

## Details included
- Moulded plastic body with a hand loop along the top
- Threaded neck with cap and a small vent plug
- Flexible corrugated spout clipped to the side
- Sun-faded upper surfaces, a fuel dribble stain, scuffed base

## Details excluded
- No warning text or brand moulding

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.325 x 0.2 m

## Outputs
- `models/survival/Claude_fuel_container/Claude_fuel_container.vox` (editable master)
- `models/survival/Claude_fuel_container/model.json`
- `models/survival/Claude_fuel_container/Claude_fuel_container.glb` (derived)
- `previews/survival/Claude_fuel_container/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b2_survival_gear.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
