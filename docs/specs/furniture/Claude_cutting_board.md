# Wooden Cutting Board
- Asset ID: Claude_cutting_board
- Base ID: cutting_board
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Kitchen dressing (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A beech chopping board from the knife drawer side of the counter, scored grey in the middle by years of onions, with the little paring knife still lying on it from the last meal anyone made.

Condition: **used**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 0.425 m
- Depth (Y): 0.3 m
- Height (Z): 0.05 m
- Grid: 34 x 24 x 4 cells at 0.0125 m (micro tier), 1,643 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [17.0, 12.0, 0.0])
- Resolution rationale: 1.25 cm cells: a hand-sized pickup would be only 3-6 cells at 2.5 cm, losing the grip, cap or label that identifies it.

## Materials and colors
`brass`, `pine_dark`, `pine_hi`, `pine_light`, `pine_mid`, `steel`, `steel_hi`, `steel_light`, `wood_stain`

## Details included
- Edge-glued strips in three close tones, rounded corners
- Hanging hole at the left end
- Knife-scored, greyed work zone in the middle and a darker damp end-grain stain
- Small paring knife: steel blade with a pale edge, dark wooden handle with two brass rivets

## Details excluded
- No food
- No brand burn mark

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 0.425 x 0.3 m

## Outputs
- `models/furniture/Claude_cutting_board/Claude_cutting_board.vox` (editable master)
- `models/furniture/Claude_cutting_board/model.json`
- `models/furniture/Claude_cutting_board/Claude_cutting_board.glb` (derived)
- `previews/furniture/Claude_cutting_board/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a3_kitchen.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
