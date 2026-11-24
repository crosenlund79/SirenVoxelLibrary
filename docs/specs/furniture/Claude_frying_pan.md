# Cast-Iron Skillet
- Asset ID: Claude_frying_pan
- Base ID: frying_pan
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Cooking utensil; improvised melee (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A heavy cast-iron skillet seasoned black by years of cooking. It was left on a cold stove, so a little rust has started where the rim met the damp air; the inside is still smooth from the last oiling.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.575 m
- Depth (Y): 0.275 m
- Height (Z): 0.1 m
- Grid: 23 x 11 x 4 cells at 0.025 m (fine tier), 226 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [11.5, 5.5, 0.0])
- Resolution rationale: 2.5 cm cells: a handheld or small gear item whose handles, straps and blades would be 2-4x too thick at 5 cm.

## Materials and colors
`iron`, `iron_blue`, `iron_dark`, `iron_edge`, `rust_dark`, `rust_deep`

## Details included
- 11-cell (27 cm) pan with flared walls and a lit rim edge
- Seasoned interior with a polished cooking zone
- Long cast handle with a hanging hole and a small helper lug opposite
- Rust beginning along one arc of the rim

## Details excluded
- No non-stick coating colours
- No food

## Attachment points
- `grip`: voxel [3, 5, 3], [np.float64(-0.2), np.float64(0.0), np.float64(0.0875)] m from the pivot. 

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.575 x 0.275 m

## Outputs
- `models/furniture/Claude_frying_pan/Claude_frying_pan.vox` (editable master)
- `models/furniture/Claude_frying_pan/model.json`
- `models/furniture/Claude_frying_pan/Claude_frying_pan.glb` (derived)
- `previews/furniture/Claude_frying_pan/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a3_kitchen.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
