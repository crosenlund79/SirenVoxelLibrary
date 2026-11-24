# Delivery Van
- Asset ID: Claude_delivery_van
- Base ID: delivery_van
- Creator: Claude
- Category: vehicles
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_D
- Scale family: full
- Intended uses: Street prop (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A plain white delivery van stopped mid-round. The driver opened the back for the next drop and never came back: one rear door swung right out, the other folded against the side, parcels still stacked inside and one fallen against the bumper. Grime has run down from the roof edges.

Condition: **abandoned**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 2.9 m
- Depth (Y): 5.2 m
- Height (Z): 2.5 m
- Grid: 29 x 52 x 25 cells at 0.1 m (standard tier), 6,642 occupied voxels
- Front direction: +Y (library voxel)
- Front: The vehicle's nose is +Y.
- Pivot: Bottom centre between the axles (wheel centres at y = 13.5 and y = 41.5 of the body), not the bounding-box centre. (pivot_voxel [18.5, 27.5, 0.0])
- Resolution rationale: 10 cm cells (the game's structural grid): large silhouettes such as walls, vehicles and trees read clearly without inflating the voxel count. Body panels, pillars and 0.65 m wheels need 0.1 m cells; the game's structure grid is also 0.1 m.

## Materials and colors
`black`, `card`, `card_dark`, `card_hi`, `charcoal`, `galv_dark`, `glass_dark`, `glass_deep`, `glass_hi`, `label_cream`, `paint_white`, `paint_white_shadow`, `pine_aged`, `porcelain_deep`, `porcelain_mid`, `porcelain_shadow`, `screen`, `signal_red_dark`, `soot`, `steel_dark`, `steel_light`

## Details included
- High-roof panel van: short bonnet, tall raked screen, windowless cargo sides
- 7-cell wheels (shared family profile)
- Left rear door open 180 degrees (sticking out beside the rear), right rear door folded flat against the side at 270 degrees
- Plywood cargo floor, stacked and toppled cardboard parcels, one on the ground
- Sliding side door seams on the kerb (+X) side
- Grime streaks running down from the roof edge, dirt band at the sills

## Details excluded
- No logos, livery or lettering
- No transparent glass

## Construction and placement notes
- Collision suggestion: Box 1.9 x 5.1 x 2.5 m centred on the pivot; the open doors separately if needed.

## Outputs
- `models/vehicles/Claude_delivery_van/Claude_delivery_van.vox` (editable master)
- `models/vehicles/Claude_delivery_van/model.json`
- `models/vehicles/Claude_delivery_van/Claude_delivery_van.glb` (derived)
- `previews/vehicles/Claude_delivery_van/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/d3_vehicles.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
