# Small Storage Cabinet
- Asset ID: Claude_small_storage_cabinet
- Base ID: small_storage_cabinet
- Creator: Claude
- Category: furniture
- Status: Candidate (generated; awaiting user review - not approved)
- Batch: Claude_catalog_A
- Scale family: full
- Intended uses: Lootable cabinet (possible use in Sirens Went Quiet; not authorization to integrate)
- Brief approved by: user commission for the full Claude catalog (2026-11-24); the model itself is not approved

## Function and story
A sage-painted cupboard from the hallway that held the towels. The near door's paint is worn through to the pine around its knob from years of hands; the other door was left open by whoever took the first-aid box from the top shelf.

Condition: **worn**.

## Silhouette
See the generator docstring and previews.

## Dimensions and orientation
- Width (X): 1.0 m
- Depth (Y): 0.75 m
- Height (Z): 1.1 m
- Grid: 20 x 15 x 22 cells at 0.05 m (detail tier), 1,851 occupied voxels
- Front direction: +Y (library voxel)
- Front: +Y is the side a person uses (seat, doors, drawers, controls).
- Pivot: Bottom centre of the occupied footprint at ground level. (pivot_voxel [10.0, 4.5, 0.0])
- Resolution rationale: 5 cm cells (the library's furniture/prop tier): real member thicknesses (boards, rails, cushions, doors) stay believable instead of toy-like; matches the game's 0.05 m character rig.

## Materials and colors
`bluegrey`, `bluegrey_hi`, `card`, `cream`, `cream_hi`, `cream_mid`, `cream_shadow`, `pine_aged`, `pine_dark`, `pine_mid`, `sage`, `sage_dark`, `sage_deep`, `sage_hi`, `steel_dark`, `terra_hi`

## Details included
- Painted sage carcass on four short feet
- Recessed doors with wooden knobs
- Paint worn through to bare pine around the near door's knob
- Far door left open showing two shelves and stacks of folded towels

## Details excluded
- No first-aid box (taken; it is a separate pickup)

## Construction and placement notes
- Collision suggestion: Box matching dimensions_m, centred on the pivot.
- Placement footprint: 1.0 x 0.45 m

## Outputs
- `models/furniture/Claude_small_storage_cabinet/Claude_small_storage_cabinet.vox` (editable master)
- `models/furniture/Claude_small_storage_cabinet/model.json`
- `models/furniture/Claude_small_storage_cabinet/Claude_small_storage_cabinet.glb` (derived)
- `previews/furniture/Claude_small_storage_cabinet/{hero,front,side,scale}.png`
- Generator: `tools/claude/models/catalog/a1_living_room.py`

## Acceptance checks
- [x] Source parses and matches render (tools/claude/validate.py)
- [x] Preview images are actual renders from source, not generated concept images
- [ ] Recognizable silhouette at thumbnail size (user review)
- [ ] Physically believable scale next to 1.75 m person (user review)
- [ ] User has reviewed and explicitly approved this revision
