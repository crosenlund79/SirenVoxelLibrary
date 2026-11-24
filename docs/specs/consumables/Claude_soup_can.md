# Soup Can
- Asset ID: Claude_soup_can
- Base ID: soup_can
- Creator: Claude
- Category: consumables
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_C
- Scale family: full
- Intended uses: Food pickup variant (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A squat can of soup with an easy-open lid, the kind kept for power cuts. It is unopened; the ring-pull still lies flat against the lid.

Condition: **new**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.0875 m
- Depth (Y): 0.0875 m
- Height (Z): 0.1 m
- Grid: 7 x 7 x 8 cells at 0.0125 m (micro tier), 218 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the label / opening side.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [3.5, 3.5, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it.

## Materials and colors
`chrome`, `galv`, `label_cream`, `label_red`, `steel`, `steel_dark`, `steel_light`

## Details included
- Squat 7-cell round can, clearly shorter and wider-looking than canned_food
- Cream label with one broad muted red band
- Ring-pull lid: rolled seam and a flat pull ring around its rivet

## Details excluded
- No text, brand or picture on the label

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.0875 x 0.0875 m

## Outputs
- `models/consumables/Claude_soup_can/Claude_soup_can.vox` (editable master)
- `models/consumables/Claude_soup_can/model.json`
- `models/consumables/Claude_soup_can/Claude_soup_can.glb` (derived)
- `previews/consumables/Claude_soup_can/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/c2_consumables.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
