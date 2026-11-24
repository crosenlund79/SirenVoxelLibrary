# Abandoned Utility Truck
- Asset ID: Claude_utility_truck
- Base ID: utility_truck
- Creator: Claude
- Category: vehicles
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_D
- Scale family: full
- Intended uses: Street prop (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A line crew's bucket truck abandoned on the shoulder with its boom still stowed. It was already old: rust is eating the compartment doors and arch lips, the rear tyre on the road side has gone flat, and the crew's cones are still stacked on the back step.

Condition: **abandoned**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 2.3 m
- Depth (Y): 5.6 m
- Height (Z): 2.3 m
- Grid: 23 x 56 x 23 cells at 0.1 m (standard tier), 5,475 occupied voxels
- Front direction: +Y (library voxel)
- Front: The vehicle's nose is +Y.
- Pivot: Bottom centre between the axles (wheel centres at y = 13 and y = 46). (pivot_voxel [11.5, 29.5, 0.0])
- Resolution rationale: 10 cm cells (the game's structural grid): large silhouettes such as walls, vehicles and trees read clearly without inflating the voxel count. Compartment doors, boom and 0.8 m wheels need 0.1 m cells; the game's structure grid is also 0.1 m.

## Materials and colors
`black`, `charcoal`, `galv_dark`, `glass_dark`, `glass_deep`, `glass_hi`, `hazard_yellow_dark`, `label_cream`, `paint_white`, `paint_white_shadow`, `porcelain_deep`, `porcelain_mid`, `rust_dark`, `rust_deep`, `rust_hi`, `safety_orange`, `safety_orange_dark`, `screen`, `soot`, `steel`, `steel_dark`, `steel_light`

## Details included
- Conventional cab, square bonnet and a utility body with side compartment doors
- Turret and two-section boom stowed rearward on a rest, fibreglass bucket at the rear corner
- 8-cell truck wheels (shared family profile), rear-left tyre flat
- Cone stack on the rear step
- Faded safety orange (paler on top), rust along door bottoms and arch lips, unlit amber beacon

## Details excluded
- No company names, numbers or hazard text
- No lit beacon

## Construction and placement notes
- Collision suggestion: Box 2.2 x 5.6 x 2.3 m centred on the pivot.

## Outputs
- `models/vehicles/Claude_utility_truck/Claude_utility_truck.vox` (editable master)
- `models/vehicles/Claude_utility_truck/model.json`
- `models/vehicles/Claude_utility_truck/Claude_utility_truck.glb` (derived)
- `previews/vehicles/Claude_utility_truck/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/d3_vehicles.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
