# Large Suburban House
- Asset ID: Claude_large_suburban_house
- Base ID: large_suburban_house
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map destination (Nearby Homes) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A two-storey family house with an attached garage. A storm brought a limb down on the garage the first winter nobody was home; its front corner has caved in and the door has jammed half open.

Condition: **abandoned**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 11.5 m
- Depth (Y): 10.0 m
- Height (Z): 9.0 m
- Grid: 23 x 20 x 18 cells at 0.5 m (map tier), 1,758 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the street side / main entrance.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [11.5, 10.0, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled. Two 3 m storeys, 1 x 1 m windows and a 2.5 m garage door read at 0.5 m cells.

## Materials and colors
`black`, `concrete`, `concrete_dark`, `concrete_hi`, `glass_dark`, `grass`, `green_dark`, `leaf`, `paint_white`, `paint_white_shadow`, `roof`, `roof_dark`, `siding_cream`, `wood_stain`

## Details included
- Low-pitch grey hip roof over two storeys, lower hip roof on the garage
- Collapsed front corner of the garage roof with exposed rafters and debris
- Gabled entry portico, shuttered upper windows
- Roll-up garage door jammed 0.5 m open, concrete driveway

## Details excluded
- No readable text, no house number
- No interior beyond the visible hole

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 11.5 x 10.0 m

## Outputs
- `models/map/Claude_large_suburban_house/Claude_large_suburban_house.vox` (editable master)
- `models/map/Claude_large_suburban_house/model.json`
- `models/map/Claude_large_suburban_house/Claude_large_suburban_house.glb` (derived)
- `previews/map/Claude_large_suburban_house/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e1_map_buildings.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
