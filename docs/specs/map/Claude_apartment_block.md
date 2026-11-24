# Apartment Block
- Asset ID: Claude_apartment_block
- Base ID: apartment_block
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map destination (Residential district) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A five-storey council block of twenty flats around a central stair core. A fire gutted one third-floor flat in the first days; the rest were locked and left.

Condition: **abandoned**.

## Silhouette
Tall plaster slab with sage-fronted balcony bands and a glazed stair core rising above the parapet.

## Dimensions and orientation
- Width (X): 12.0 m
- Depth (Y): 9.0 m
- Height (Z): 17.0 m
- Grid: 24 x 18 x 34 cells at 0.5 m (map tier), 3,716 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the street side / main entrance.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [12.0, 9.0, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled. Storey bands, balconies and window rhythm survive at 0.5 m; railings are solid bands.

## Materials and colors
`ash_dark`, `char`, `concrete`, `concrete_dark`, `concrete_hi`, `galv_hi`, `glass`, `glass_dark`, `grass`, `plaster`, `roof`, `sage`, `soot`

## Details included
- Five 3 m storeys, flat roof with parapet, stair penthouse and HVAC
- Continuous balcony bands on the street side, glazed stair core with entrance canopy
- Soot-blackened burnt-out flat on the third floor
- Punched windows on the sides and back

## Details excluded
- No readable text
- No interiors

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 12.0 x 9.0 m

## Outputs
- `models/map/Claude_apartment_block/Claude_apartment_block.vox` (editable master)
- `models/map/Claude_apartment_block/model.json`
- `models/map/Claude_apartment_block/Claude_apartment_block.glb` (derived)
- `previews/map/Claude_apartment_block/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e1_map_buildings.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
