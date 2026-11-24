# Hand Saw
- Asset ID: Claude_saw
- Base ID: saw
- Creator: Claude
- Category: survival
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_B
- Scale family: full
- Intended uses: Woodworking tool (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A panel saw from a retired neighbour's workshop, still sharp. The beech handle has gone dark and glossy where the fingers wrap; a little rust has bloomed near the toe where it hung on a damp shed wall.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.125 m
- Depth (Y): 0.6875 m
- Height (Z): 0.025 m
- Grid: 10 x 55 x 2 cells at 0.0125 m (micro tier), 426 occupied voxels
- Front direction: +Y (library voxel)
- Front: Lies on its side as it would rest on a bench: handle along Y, working end at +Y, lowest point on z = 0. Rotate to the hand for a held pose. Teeth toward -X (camera side), spine toward +X.
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [5.0, 27.5, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it.

## Materials and colors
`brass_hi`, `pine_aged`, `pine_dark`, `pine_mid`, `rust_dark`, `steel`, `steel_light`, `wood_stain`

## Details included
- Closed D-handle with a hand hole and three brass saw nuts
- Blade tapering from heel to toe with a serrated tooth edge
- Straight spine; light rust bloom near the toe

## Details excluded
- No etched logo
- No teeth finer than a cell (stylised serration)

## Attachment points
- `grip`: voxel [4, 2, 1], [np.float64(-0.0062), np.float64(-0.3125), np.float64(0.0188)] m from the pivot. Fingers through the hand hole around the rear grip of the D-handle.

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.125 x 0.6875 m

## Outputs
- `models/survival/Claude_saw/Claude_saw.vox` (editable master)
- `models/survival/Claude_saw/model.json`
- `models/survival/Claude_saw/Claude_saw.glb` (derived)
- `previews/survival/Claude_saw/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/b1_storage_tools.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
