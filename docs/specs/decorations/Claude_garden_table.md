# Garden Table
- Asset ID: Claude_garden_table
- Base ID: garden_table
- Creator: Claude
- Category: decorations
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_D
- Scale family: full
- Intended uses: Yard prop (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A white resin patio table left out through every season. Rain pooled along its moulded grooves and around the umbrella hole and grew green algae there; the legs are streaked on their shaded side, and last autumn's leaves still sit on the top.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.1 m
- Depth (Y): 0.7 m
- Height (Z): 0.75 m
- Grid: 22 x 14 x 15 cells at 0.05 m (detail tier), 724 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y faces the street or the person using it.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [11.0, 7.0, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`dead_leaf`, `dead_leaf_dark`, `green_faded`, `lichen`, `paint_white`, `paint_white_shadow`, `porcelain_deep`, `porcelain_mid`, `porcelain_shadow`

## Details included
- Rounded rectangular top with a skirt and moulded grooves
- Central umbrella hole
- Four flared legs
- Algae in the grooves and round the hole, streaks down the north (-Y) faces of the legs
- Two dead leaves on the top

## Details excluded
- No chairs (separate props)
- No umbrella

## Construction and placement notes
- Collision suggestion: Box 1.1 x 0.7 x 0.75 m.
- Placement footprint: 1.1 x 0.7 m

## Outputs
- `models/decorations/Claude_garden_table/Claude_garden_table.vox` (editable master)
- `models/decorations/Claude_garden_table/model.json`
- `models/decorations/Claude_garden_table/Claude_garden_table.glb` (derived)
- `previews/decorations/Claude_garden_table/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/d2_street.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
