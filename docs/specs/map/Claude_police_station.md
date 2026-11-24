# Police Station
- Asset ID: Claude_police_station
- Base ID: police_station
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map destination (Weapons) (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
The district police station, the last place in town with lights on. The cruisers are parked in their bays and the flag is still up, faded; nobody answered the front desk after the third day.

Condition: **abandoned**.

## Silhouette
Two-storey brick block with a navy band, navy entrance canopy, flagpole and two white cruisers.

## Dimensions and orientation
- Width (X): 16.0 m
- Depth (Y): 12.0 m
- Height (Z): 9.5 m
- Grid: 32 x 24 x 19 cells at 0.5 m (map tier), 2,298 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the street side / main entrance.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [16.0, 12.0, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled.

## Materials and colors
`asphalt`, `black`, `concrete_dark`, `concrete_hi`, `galv`, `galv_hi`, `glass_dark`, `glass_deep`, `grass`, `lamp_blue`, `lamp_red`, `line_white`, `navy`, `paint_white`, `red`, `roof`, `steel_dark`, `steel_hi`

## Details included
- Two-storey brick block with a navy band under the parapet
- Projecting entrance bay with a canopy on two columns
- Flagpole with a plain two-band flag, lattice radio mast on the roof
- Two patrol cars with unlit light bars in marked bays

## Details excluded
- No readable text, badge or real department markings

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 16.0 x 12.0 m

## Outputs
- `models/map/Claude_police_station/Claude_police_station.vox` (editable master)
- `models/map/Claude_police_station/model.json`
- `models/map/Claude_police_station/Claude_police_station.glb` (derived)
- `previews/map/Claude_police_station/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e1_map_buildings.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
