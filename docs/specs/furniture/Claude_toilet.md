# Toilet
- Asset ID: Claude_toilet
- Base ID: toilet
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Bathroom fixture; game prop 'toilet' (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
An ordinary close-coupled toilet in a family bathroom, kept clean until the water stopped. The lid was left up; the last of the water in the bowl dried down and left a faint brown line where it stood for weeks.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.6 m
- Depth (Y): 0.7 m
- Height (Z): 0.8 m
- Grid: 12 x 14 x 16 cells at 0.05 m (detail tier), 651 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [6.0, 7.5, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`chrome`, `pine_light`, `pine_mid`, `porcelain`, `porcelain_deep`, `porcelain_hi`, `porcelain_mid`, `porcelain_shadow`, `steel`, `steel_light`, `water`

## Details included
- Oval bowl on a narrower pedestal, seat down and lid up against the cistern
- Cistern with a lid and a chrome dual-flush button
- Chrome supply pipe and stop valve at the back left
- Low water in the bowl with a faint tide line above it

## Details excluded
- No brand
- No toilet roll (a separate pickup)

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.6 x 0.75 m

## Outputs
- `models/furniture/Claude_toilet/Claude_toilet.vox` (editable master)
- `models/furniture/Claude_toilet/model.json`
- `models/furniture/Claude_toilet/Claude_toilet.glb` (derived)
- `previews/furniture/Claude_toilet/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a4_bath_utility.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
