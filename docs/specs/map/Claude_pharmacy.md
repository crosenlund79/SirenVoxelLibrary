# Pharmacy
- Asset ID: Claude_pharmacy
- Base ID: pharmacy
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map destination (Medical) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A corner pharmacy on the high street, the first shop people broke into. The corner doors were forced and the shelves cleared; the green cross still hangs over the pavement.

Condition: **abandoned**.

## Silhouette
Brick corner shop with a recessed corner door, green awnings and a projecting white blade sign with a green cross.

## Dimensions and orientation
- Width (X): 8.0 m
- Depth (Y): 9.5 m
- Height (Z): 5.5 m
- Grid: 16 x 19 x 11 cells at 0.5 m (map tier), 976 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the street side / main entrance.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [8.0, 9.5, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled.

## Materials and colors
`asphalt`, `concrete_dark`, `concrete_hi`, `curb`, `galv_hi`, `glass`, `glass_dark`, `green_dark`, `label_green`, `paint_white`, `red`, `roof`, `steel_dark`

## Details included
- Brick corner building with a stone cornice and flat roof
- Recessed corner entrance behind a single column
- Shopfront glazing on both street faces under dark green awnings
- Projecting blade sign: green cross on a white panel

## Details excluded
- No readable text or real-chain branding

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 8.0 x 9.5 m

## Outputs
- `models/map/Claude_pharmacy/Claude_pharmacy.vox` (editable master)
- `models/map/Claude_pharmacy/model.json`
- `models/map/Claude_pharmacy/Claude_pharmacy.glb` (derived)
- `previews/map/Claude_pharmacy/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e1_map_buildings.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
