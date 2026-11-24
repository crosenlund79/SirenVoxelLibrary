# Family Car
- Asset ID: Claude_family_car
- Base ID: family_car
- Creator: Claude
- Category: vehicles
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_D
- Scale family: full
- Intended uses: Driveway/street prop (game car) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A blue-grey family hatchback left on the street when the family went on foot. The front tyre on the kerb side has gone flat, a summer of dust has settled on every top surface, and through the rear window, left open a crack too wide, a packed bag is still on the back seat.

Condition: **abandoned**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.9 m
- Depth (Y): 4.2 m
- Height (Z): 1.4 m
- Grid: 19 x 42 x 14 cells at 0.1 m (standard tier), 2,884 occupied voxels
- Front direction: +Y (library voxel)
- Front: The vehicle's nose is +Y.
- Pivot: Bottom centre between the axles (wheel centres at y = 8 and y = 33). (pivot_voxel [9.5, 21.0, 0.0])
- Resolution rationale: 10 cm cells (the game's structural grid): large silhouettes such as walls, vehicles and trees read clearly without inflating the voxel count. Body panels, pillars and 0.65 m wheels need 0.1 m cells to keep round wheels and a readable glasshouse; the game's structure grid is also 0.1 m.

## Materials and colors
`black`, `bluegrey`, `bluegrey_dark`, `bluegrey_deep`, `bluegrey_hi`, `charcoal`, `chrome`, `glass_dark`, `glass_deep`, `glass_hi`, `label_cream`, `olive`, `olive_dark`, `olive_hi`, `screen`, `signal_red_dark`, `slate`, `slate_dark`, `slate_deep`, `soot`, `steel_dark`, `steel_light`

## Details included
- Five-door hatchback: short bonnet, raked screen, long roof, steep hatch
- 7-cell wheels (shared family profile), front-left tyre flat with the rim sitting one cell low
- Dust and sun fade on every upward surface
- Rear-left window wound down: back seat and a packed olive bag visible
- Two-tone opaque glass, door seams, handles, mirrors, unlit lamps, blank plates

## Details excluded
- No badges, logos or plate text
- No transparent glass

## Construction and placement notes
- Collision suggestion: Box 1.75 x 4.2 x 1.4 m centred on the pivot.

## Outputs
- `models/vehicles/Claude_family_car/Claude_family_car.vox` (editable master)
- `models/vehicles/Claude_family_car/model.json`
- `models/vehicles/Claude_family_car/Claude_family_car.glb` (derived)
- `previews/vehicles/Claude_family_car/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/d3_vehicles.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
