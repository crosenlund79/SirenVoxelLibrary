# Police Car
- Asset ID: Claude_police_car
- Base ID: police_car
- Creator: Claude
- Category: vehicles
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_D
- Scale family: full
- Intended uses: Police-station dressing (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A patrol car abandoned at a roadblock that was never finished. The driver's door was flung open and left that way; the lightbar is dark, the push bar is scuffed from pushing stalled cars off the road, and there is no marking left that says which force it belonged to.

Condition: **abandoned**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 2.7 m
- Depth (Y): 4.9 m
- Height (Z): 1.5 m
- Grid: 27 x 49 x 15 cells at 0.1 m (standard tier), 3,092 occupied voxels
- Front direction: +Y (library voxel)
- Front: The vehicle's nose is +Y.
- Pivot: Bottom centre between the axles (wheel centres at y = 10 and y = 37 of the body), not the bounding-box centre (the open door widens the -X side). (pivot_voxel [17.0, 24.0, 0.0])
- Resolution rationale: 10 cm cells (the game's structural grid): large silhouettes such as walls, vehicles and trees read clearly without inflating the voxel count. Body panels, pillars and 0.65 m wheels need 0.1 m cells; the game's structure grid is also 0.1 m.

## Materials and colors
`black`, `charcoal`, `chrome`, `glass_dark`, `glass_deep`, `glass_hi`, `iron_edge`, `label_cream`, `lamp_blue`, `lamp_red`, `navy`, `navy_dark`, `paint_white`, `paint_white_shadow`, `porcelain_shadow`, `screen`, `signal_red_dark`, `slate_dark`, `slate_deep`, `soot`, `steel_dark`, `steel_light`

## Details included
- Three-box sedan on the shared 7-cell wheels
- Navy ends and white doors and roof (generic, no text or crest)
- Unlit lightbar: red and blue lens blocks on a dark base
- Black push bar on the nose, A-pillar spotlight
- Driver's door flung open about 75 degrees: seat, wheel and dash visible

## Details excluded
- No department names, numbers or crests
- No lit or emissive lamps

## Construction and placement notes
- Collision suggestion: Box 1.8 x 4.9 x 1.45 m centred on the pivot; the open door separately if needed.

## Outputs
- `models/vehicles/Claude_police_car/Claude_police_car.vox` (editable master)
- `models/vehicles/Claude_police_car/model.json`
- `models/vehicles/Claude_police_car/Claude_police_car.glb` (derived)
- `previews/vehicles/Claude_police_car/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/d3_vehicles.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
