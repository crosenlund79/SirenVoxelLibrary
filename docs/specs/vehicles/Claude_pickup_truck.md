# Pickup Truck
- Asset ID: Claude_pickup_truck
- Base ID: pickup_truck
- Creator: Claude
- Category: vehicles
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_D
- Scale family: full
- Intended uses: Street prop (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
An old full-size pickup that belonged to someone who fixed things for the neighbours. It was being loaded when it was left: tailgate dropped, a blue tarp half pulled over the side of the bed, one jerry can still standing by the gate. The maroon paint has oxidised pale on the bonnet and roof.

Condition: **abandoned**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 2.0 m
- Depth (Y): 5.1 m
- Height (Z): 1.7 m
- Grid: 20 x 51 x 17 cells at 0.1 m (standard tier), 3,600 occupied voxels
- Front direction: +Y (library voxel)
- Front: The vehicle's nose is +Y.
- Pivot: Bottom centre between the axles (wheel centres at y = 13.5 and y = 41.5). (pivot_voxel [10.0, 27.0, 0.0])
- Resolution rationale: 10 cm cells (the game's structural grid): large silhouettes such as walls, vehicles and trees read clearly without inflating the voxel count. Body panels, pillars and 0.8 m wheels need 0.1 m cells; the game's structure grid is also 0.1 m.

## Materials and colors
`black`, `blue_deep`, `bottle_cap`, `charcoal`, `chrome`, `glass_dark`, `glass_deep`, `glass_hi`, `label_blue`, `label_cream`, `maroon`, `maroon_dark`, `olive`, `olive_dark`, `red_dark`, `rust_dark`, `rust_deep`, `screen`, `signal_red_dark`, `soot`, `steel_dark`, `steel_light`

## Details included
- Regular cab, square bonnet, tall chrome grille and chrome bumpers
- 8-cell truck wheels (shared family profile) in rust-lipped arches
- Tailgate down; black bed liner
- Faded blue tarp heaped in the bed and draped over the camera-side wall
- Olive steel jerry can on the dropped tailgate
- Oxidised paint on the upper surfaces, rust at the arch lips and bed corners

## Details excluded
- No badges or plate text
- No load straps (sub-cell)

## Construction and placement notes
- Collision suggestion: Box 1.8 x 4.7 x 1.7 m centred on the pivot.

## Outputs
- `models/vehicles/Claude_pickup_truck/Claude_pickup_truck.vox` (editable master)
- `models/vehicles/Claude_pickup_truck/model.json`
- `models/vehicles/Claude_pickup_truck/Claude_pickup_truck.glb` (derived)
- `previews/vehicles/Claude_pickup_truck/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/d3_vehicles.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
