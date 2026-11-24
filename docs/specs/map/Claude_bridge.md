# Bridge
- Asset ID: Claude_bridge
- Base ID: bridge
- Creator: Claude
- Category: map
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_E
- Scale family: full
- Intended uses: Regional-map infrastructure piece (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A two-span concrete road bridge over the creek on the county road. Its parapets are chipped where a truck once scraped along them, and the expansion joint over the pier has opened.

Condition: **worn**.

## Silhouette
Long road deck with posted steel railings on a central two-column pier and end abutments.

## Dimensions and orientation
- Width (X): 8.5 m
- Depth (Y): 20.0 m
- Height (Z): 2.5 m
- Grid: 17 x 40 x 5 cells at 0.5 m (map tier), 955 occupied voxels
- Front direction: +Y (library voxel)
- Front: Road runs along Y; +Y is an arbitrary end (symmetric piece).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [8.5, 20.0, 0.0])
- Resolution rationale: 50 cm cells: regional-map scale, real-world metres with far fewer voxels; only massing, roofs, entrances and one identifying feature are modelled.

## Materials and colors
`asphalt`, `asphalt_dark`, `concrete`, `concrete_dark`, `concrete_deep`, `concrete_hi`, `curb`, `line_yellow`, `steel`, `steel_light`

## Details included
- Deck carrying the shared road section; kerbs with concrete posts every 2 m and a steel top rail in place of the verges
- 0.5 m slab deck on a central pier of two columns under a cap beam, solid abutments
- Expansion joint over the pier, scraped kerb stretch where the top rail was torn away

## Details excluded
- No water, no vehicles
- No readable markings

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 8.5 x 20.0 m

## Outputs
- `models/map/Claude_bridge/Claude_bridge.vox` (editable master)
- `models/map/Claude_bridge/model.json`
- `models/map/Claude_bridge/Claude_bridge.glb` (derived)
- `previews/map/Claude_bridge/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/e2_map_infrastructure.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
